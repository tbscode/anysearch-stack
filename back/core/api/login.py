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


@dataclass
class LoginInfo:
    username: str
    password: str


class LoginInfoSerializer(DataclassSerializer):
    class Meta:
        dataclass = LoginInfo


@extend_schema(
    request=LoginInfoSerializer(many=False),
    auth=None,
)
@throttle_classes([AnonRateThrottle])
@api_view(['POST'])
def login_user(request):
    serializer = LoginInfoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.save()

    user = authenticate(username=data.username, password=data.password)

    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    login(request, user)
    return Response(status=status.HTTP_200_OK)
