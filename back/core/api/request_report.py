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
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async, async_to_sync
from core.models import Project, ChatMessage, translate_to_all_langs_in_list, get_langs_in_project
from core.api.user_data import serialize_message


@dataclass
class RequestReport:
    project_hash: str


class RequestReportSerializer(DataclassSerializer):
    class Meta:
        dataclass = RequestReport


@extend_schema(
    request=RequestReportSerializer(many=False),
    auth=None,
)
@throttle_classes([SessionAuthentication])
@api_view(['POST'])
def login_user(request):
    serializer = RequestReportSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.save()

    channel_layer = get_channel_layer()  # default channel layer

    project_group_slug = f"project-{data.project_hash}"

    project = Project.objects.get(hash=data.project_hash)
    msg = "Ok starting on that report for you give me a moment"

    project_langs = get_langs_in_project(project)
    message = ChatMessage.objects.create(
        project=project,
        original_message=data.text,
        sender=request.user,
        data=translate_to_all_langs_in_list(
            msg, project_langs, str("english")),
    )

    ai_user_for_project = project.ai_user

    # first let the ai say that it's working on the report now
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

    return Response(status=status.HTTP_200_OK)
