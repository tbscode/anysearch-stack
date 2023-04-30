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
from core.models import Project, ChatMessage, User, ChatMessage, get_langs_in_project
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async, async_to_sync


def get_project_participants(project):
    data = []
    for participant in project.participants.all():
        data.append({
            "hash": str(participant.hash),
            "email": participant.email,
            "first_name": participant.profile.first_name,
            "language": participant.profile.language,
        })
    return data


def serialize_message(message):
    attachment = None
    if message.file_attachment:
        attachment = message.file_meta + "," + message.get_attachment_b64()
    return {
        "time": str(message.time),
        "data": message.data,
        "text": message.original_message,
        "sender": str(message.sender.hash),
        "hash": str(message.hash),
        "profile_image": message.sender.profile.image,
        "attachment": attachment,
    }


def get_project_messages(project):
    messages = ChatMessage.objects.filter(project=project).order_by('time')
    data = []
    for message in messages:
        data.append(serialize_message(message))
    return data


def get_user_projects(user):
    projects = user.projects.all()
    data = []
    for project in projects:
        data.append({
            "project_hash": str(project.hash),
            "name": project.name,
            "description": project.description,
            "participants": get_project_participants(project),
            "messages": get_project_messages(project),
            "languages": get_langs_in_project(project),
        })
    return data


def get_user_data(user):
    """
    All the relevant user data for one user 
    TODO yeah we don't do any pagination for anything to save time but this would need to be added
    """

    return {
        "hash": str(user.hash),
        "email": user.email,
        "profile_image": user.profile.image,
        "first_name": user.profile.first_name,
        "language": user.profile.language,
        "projects": get_user_projects(user),
    }


@extend_schema(
    auth=["SessionAuthentication"],
)
@api_view(['GET'])
@authentication_classes([SessionAuthentication])
def request_user_data(request):

    return Response(get_user_data(request.user), status=status.HTTP_200_OK)
