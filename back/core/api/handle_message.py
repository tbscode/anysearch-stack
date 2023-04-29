from rest_framework_dataclasses.serializers import DataclassSerializer
from typing import Literal, Optional, List, Dict
from datetime import datetime
from drf_spectacular.utils import extend_schema
import base64
from dataclasses import dataclass
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, throttle_classes
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate, login
from core.models import Project, ChatMessage
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async, async_to_sync
from core.api.user_data import serialize_message


@dataclass
class MessageRequest:
    project_hash: str
    type: Literal["new_message", "typing", "seen"]
    text: Optional[str]
    data: Optional[Dict]
    file_attachment: Optional[str]


class MessageRequestSerializer(DataclassSerializer):
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

    message = ChatMessage.objects.create(
        project=project,
        original_message=data.text,
        sender=user,
        **extra_params
    )

    channel_layer = get_channel_layer()  # default channel layer

    # Now nofify all users connected to that channel group
    async_to_sync(channel_layer.group_send)(project_group_slug, {
        "type": "broadcast_message",
        "data": {
            "event": data.event,
            **serialize_message(message),
            "user": {
                "hash": user.hash,
                "name": user.first_name
            }
        }
    })

    # Now check if the message requres additional actions
    # if it starts with `@ai` an AI assistant should reply
    if data.test.startswith("@ai"):
        # TODO ....
        pass
