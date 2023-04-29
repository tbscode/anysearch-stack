from rest_framework_dataclasses.serializers import DataclassSerializer
from typing import Literal, Optional, List, Dict
from datetime import datetime
from drf_spectacular.utils import extend_schema
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


@dataclass
class MessageRequest:
    project_hash: str
    type: Literal["message", "typing", "seen"]
    text: Optional[str]
    data: Optional[Dict]


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

    ChatMessage.objects.create(
        project=project,
        original_message=data.text,
    )

    channel_layer = get_channel_layer()  # default channel layer

    async_to_sync(channel_layer.group_send)(project_group_slug, {
        "type": "broadcast_message",
        "data": {
            "event": data.type,
            "user": {
                "hash": user.hash,
                "name": user.first_name
            }
        }
    })
