from rest_framework_dataclasses.serializers import DataclassSerializer
import openai
from typing import Literal, Optional, List, Dict
from core.api.db_agent import DBChatAgent
from django.conf import settings
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
from core.mdconverter import convert_markdown
from uuid import uuid4
import base64

import sys
import markdown2
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def markdown_to_pdf(markdown_text, output_file):
    # Read input markdown file
    # Convert markdown to HTML
    html_text = markdown2.markdown(markdown_text)

    # Create a PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)

    # Get the default Paragraph style
    style = getSampleStyleSheet()['BodyText']

    # Convert HTML to a list of Paragraphs
    paragraphs = [Paragraph(p, style) for p in html_text.split('<br />')]

    # Build the PDF document using the paragraphs
    doc.build(paragraphs)


def pdf_to_base64(file_path):
    with open(file_path, "rb") as pdf_file:
        # Read the PDF content
        pdf_content = pdf_file.read()

        # Convert PDF content to base64 string
        base64_content = base64.b64encode(pdf_content).decode("utf-8")

    return base64_content


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
def request_report(request):
    serializer = RequestReportSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.save()

    channel_layer = get_channel_layer()  # default channel layer

    project_group_slug = f"project-{data.project_hash}"

    project = Project.objects.get(hash=data.project_hash)
    msg = "Ok starting on that report for you give me a moment\n"
    #msg += "I'll perform the following steps to generate your report:"
    ai_user_for_project = project.ai_user

    project_langs = get_langs_in_project(project)
    message = ChatMessage.objects.create(
        project=project,
        original_message=msg,
        sender=ai_user_for_project,
        data=translate_to_all_langs_in_list(
            msg, project_langs, str("english")),
    )

    # first let the ai say that it's working on the report now
    def send_message(_message):
        async_to_sync(channel_layer.group_send)(project_group_slug, {
            "type": "broadcast_message",
            "data": {
                "event": "new_message",
                **serialize_message(_message),
                "user": {
                    "hash": str(ai_user_for_project.hash),
                    "name": ai_user_for_project.first_name
                }
            }
        })

    send_message(message)

    # THis agent was to overpowerd and needed more tools to use, it would always ask to many questions so we just use the api for now
    # agent = DBChatAgent(
    #    ai_user=ai_user_for_project, project=project,
    #    send_message_func=send_message,
    #    user_lang=str(request.user.profile.language),
    #    memory_state=message_state,
    #    model="gpt-4",
    #    open_ai_api_key=settings.OPENAI_KEY,
    #    buffer_memory_token_limit=500,
    #    verbose=True,
    #    lang_list=project_langs,
    #    tools=[],
    # )
    #out, after_state, token_usage = agent(prompt)

    prompts = [
        "based on the whole conversation determine the topic of the project and generate a short description"]
    #"Based on the whole conversation plase generate an outline of which events took place and return it as a markdown list"
    #"Based on the whole conversation plase generate timeline of events that took flace",
    #"Based on the whole conversation plase judge how the project performance was"
    # ]

    parts = [
        "description",
        "outline",
        "timeline",
        "shedule",
        "technicans",
        "expenses"
    ]

    titles = [
        "## Description",
        "## Overview",
        "## Timeline",
        "## Shedule Performance",
        "## Technicians",
        "## Expenses",
        "## Problems and difficulties"
    ]

    def as_message(message, user="user"):
        return {
            'role': user,
            "content": message
        }

    datas = {}

    i = 0
    for pompt in prompts:
        past_messages = ChatMessage.objects.filter(
            project=project).order_by("-time")[:15]  # TODO: prompt splitting should happen here!

        # setup a db agent:
        # It gets the full message history
        message_state = []

        for message in past_messages:
            if message.sender == ai_user_for_project:
                message_state.append(as_message(
                    message.original_message, "assistant"))
            else:
                message_state.append(as_message(
                    message.original_message, "user"))

        prompt = "Based on the whole conversation plase generate an outline of which events took place and return it as a markdown list"

        message_state.append(as_message(prompt))

        openai.api_key = settings.OPENAI_KEY

        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_state,
            stream=False
        )

        completion = res["choices"][0]["message"]["content"]

        msg = ChatMessage.objects.create(
            project=project,
            original_message=completion,
            sender=ai_user_for_project,
            data=translate_to_all_langs_in_list(
                completion, project_langs, str(project.base_language)),
        )

        datas[parts[i]] = completion

        msg = f"Finished generating {titles[i]}"
        new_message = ChatMessage.objects.create(
            project=project,
            original_message=msg,
            sender=ai_user_for_project,
            data=translate_to_all_langs_in_list(
                msg, project_langs, str("english")),
        )
        send_message(new_message)
        i += 1

    out = f"# Project Report: {project.name} \n\n\n"
    i = 0
    for prompt in prompts:
        out += f"{titles[i]}\n\n"
        key = parts[i]
        out += datas[key]
        i += 1

    msg = "Heres your report"

    uuid = uuid4()
    # convert_markdown(out, output_folder_path="/tmp",
    #                 output_file_name=str(uuid))
    temp_file = f"/tmp/{uuid}.pdf"
    markdown_to_pdf(out, temp_file)

    base64_string = pdf_to_base64(temp_file)
    print("base64_string", base64_string)

    with open(temp_file, 'rb') as file:
        file_content_bytes = file.read()

    new_message = ChatMessage.objects.create(
        project=project,
        original_message=msg,
        sender=ai_user_for_project,
        file_attachment=file_content_bytes,
        file_meta="data:application/pdf;base64",
        data=translate_to_all_langs_in_list(
            msg, project_langs, str("english")),
    )
    send_message(new_message)

    return Response(status=status.HTTP_200_OK)
