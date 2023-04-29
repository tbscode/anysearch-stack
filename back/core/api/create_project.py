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
from core.models import Project, ChatMessage, User
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async, async_to_sync


@dataclass
class ProjectRequest:
    name: str
    description: str
    participants = Optional[List[str]]


class ProjectRequestSerializer(DataclassSerializer):
    class Meta:
        dataclass = ProjectRequest


@extend_schema(
    request=ProjectRequestSerializer(many=False),
    auth=["SessionAuthentication"],
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication])
def create_project(request):
    serializer = ProjectRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.save()

    project = Project.objects.create(
        name=data.name,
        description=data.description,
    )
    if data.participants:
        for hash in data.participants:
            user = User.objects.get(hash=hash)
            project.participants.add(user)
    project.save()

    return Response({"hash": project.hash}, status=status.HTTP_201_CREATED)
