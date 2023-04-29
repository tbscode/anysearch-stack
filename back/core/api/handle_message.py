from rest_framework_dataclasses.serializers import DataclassSerializer
from typing import Literal, Optional, List, Dict
from datetime import datetime
from django.conf import settings
from drf_spectacular.utils import extend_schema
import base64
from core.api.ai_handler import ToolGSearch
from dataclasses import dataclass
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, throttle_classes
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate, login
from rest_framework import serializers
from core.models import Project, ChatMessage, translate_to_all_langs_in_list, get_langs_in_project
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async, async_to_sync
from core.api.user_data import serialize_message
from core.api.db_agent import DBChatAgent


@dataclass
class MessageRequest:
    project_hash: str
    type: Literal["new_message", "typing", "seen"]
    text: Optional[str]
    data: Optional[Dict]
    file_attachment: Optional[str] = None


class MessageRequestSerializer(DataclassSerializer):
    file_attachment = serializers.CharField(required=False)

    class Meta:
        dataclass = MessageRequest


@extend_schema(
    request=MessageRequestSerializer(many=False),
    auth=["SessionAuthentication"],
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def send_message(request):
    """
    Handles incoming messages and distributes the to user chats, processes ...
    The api used there is idential to the api that can be called via websocket
    """
    handle_socket_message(request.data, request.user)


def handle_socket_message(data, user):
    """
    Handling incoming websocket involves
    - updating all connected users of a receiving project chat
    - possibly processing commands or ai action calls
    - translating messsage in all languages for a users in a project

    """
    print("CALLED HANDLE SOCKET MESSAGE")
    serializer = MessageRequestSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    data = serializer.save()

    project = Project.objects.get(hash=data.project_hash)
    project_group_slug = f"project-{project.hash}"

    extra_params = {}
    if data.file_attachment:
        file_data = data.file_attachment.encode()
        content = base64.b64decode(file_data)
        extra_params["file_attachment"] = content

    # translate the message in all languages that are used in that project
    # TODO ... which api to use again ?
    translated_message = translate_to_all_langs_in_list(
        data.text, get_langs_in_project(project), str(project.base_language))

    message = ChatMessage.objects.create(
        project=project,
        original_message=data.text,
        sender=user,
        data=translated_message,
        **extra_params
    )

    channel_layer = get_channel_layer()  # default channel layer

    # Now nofify all users connected to that channel group
    async_to_sync(channel_layer.group_send)(project_group_slug, {
        "type": "broadcast_message",
        "data": {
            "event": data.type,
            **serialize_message(message),
            "user": {
                "hash": str(user.hash),
                "name": user.first_name
            }
        }
    })

    # Now check if the message requres additional actions
    # if it starts with `@ai` an AI assistant should reply

    def as_message(message, user="human"):
        return {'type': user, 'data': {
            'content': message, 'additional_kwargs': {}}}

    if data.text.startswith("@ai"):
        # TODO ugly as fuck like that should be moved somehere else and implemented cleaner

        past_4_messages = ChatMessage.objects.filter(
            project=project).order_by("-time")[:5]
        ai_user_for_project = project.ai_user

        def send_message(message):
            async_to_sync(channel_layer.group_send)(project_group_slug, {
                "type": "broadcast_message",
                "data": {
                    "event": data.type,
                    **serialize_message(message),
                    "user": {
                        "hash": str(ai_user_for_project.hash),
                        "name": ai_user_for_project.first_name
                    }
                }
            })
            pass
        # TODO: generate ai response based on past 4 messages

        message_state = []

        for message in past_4_messages:
            if message.sender == ai_user_for_project:
                message_state.append(as_message(
                    message.original_message, "ai"))
            else:
                message_state.append(as_message(
                    message.original_message, "human"))

        agent = DBChatAgent(
            ai_user=ai_user_for_project, project=project,
            send_message_func=send_message,
            memory_state=message_state,
            model="gpt-3.5-turbo",
            open_ai_api_key=settings.OPENAI_KEY,
            buffer_memory_token_limit=500,
            verbose=True,
            tools=[
                ToolGSearch(
                    google_api_key=settings.GOOGLE_API_KEY,
                    google_cse_id=settings.GOOGLE_APP_CSE_ID,
                ).get_tooling()
            ],
        )

        out, after_state, token_usage = agent(data.text.replace("@ai ", "", 1))

        msg = ChatMessage.objects.create(
            project=project,
            original_message=out,
            sender=ai_user_for_project,
        )

        send_message(msg)

        # save the ai reply to the database
