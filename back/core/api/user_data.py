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


def get_project_participants(project):
    data = []
    for participant in project.participants.all():
        data.append({
            "hash": participant.hash,
            "email": participant.email,
            "first_name": participant.profile.first_name,
            "last_name": participant.profile.last_name,
            "language": participant.profile.language,
        })
    return data


def get_user_projects(user):
    projects = user.projects.all()
    data = []
    for project in projects:
        data.append({
            "project_hash": project.hash,
            "name": project.name,
            "description": project.description,
            "participants": get_project_participants(project),
        })
    return projects


def get_user_data(user):
    """
    All the relevant user data for one user 
    TODO yeah we don't do any pagination for anything to save time but this would need to be added
    """

    return {
        "hash": user.hash,
        "email": user.email,
        "first_name": user.profile.first_name,
        "last_name": user.profile.last_name,
        "language": user.profile.language,
        "projects": get_user_projects(user),
    }


@extend_schema(
    auth=["SessionAuthentication"],
)
@api_view(['GET'])
@authentication_classes([SessionAuthentication])
def user_data(request):

    return Response(get_user_data(request.user), status=status.HTTP_200_OK)
