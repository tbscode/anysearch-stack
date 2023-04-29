"""
Copyright Tim Schupp (C) tim@timschupp.de
These are advanced wrappers of langchain classes
I've originally developed them for msgmate.io
"""
from langchain.schema import messages_from_dict, messages_to_dict, OutputParserException
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
from typing import Any, Dict, Optional
from langchain.callbacks import get_openai_callback
from langchain.schema import AgentAction
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import messages_from_dict
from langchain.agents import AgentType
from langchain.callbacks.base import CallbackManager
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool
from langchain.agents import initialize_agent
from abc import ABC, abstractmethod


class MsgmateTooling(ABC):

    def __init__(self, *args, **kwargs):
        self.tool = self.initalize_tooling(*args, **kwargs)

    @abstractmethod
    def initalize_tooling(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_tooling(self):
        pass


class ToolGSearch(MsgmateTooling):
    def initalize_tooling(
        self,
        google_api_key: str = "",
        google_cse_id: str = "",
    ):
        return GoogleSearchAPIWrapper(
            search_engine=None,
            google_api_key=google_api_key,
            google_cse_id=google_cse_id
        )

    def get_tooling(self):
        return Tool(
            name="Current Search",
            func=self.tool.run,
            description="useful for when you need to answer questions about current events or the current state of the world"
        )


class MsgmateConversation(ABC):

    def __init__(
        self,
        memory_state: list = [],
        model: str = "gpt-3.5-turbo",
        open_ai_api_key=None,
        buffer_memory_token_limit=150,
        verbose=False,
        tools: list = [],
    ):
        """
        Initalize langchain tooling and load memory state
        """

        self.token_usages = []

        llm = ChatOpenAI(
            temperature=0.3,
            openai_api_key=open_ai_api_key,
            model_name="gpt-3.5-turbo",
            streaming=True,  # Doesn't seem to work with agents
            client=None
        )

        memory = ConversationSummaryBufferMemory(
            return_messages=True,
            llm=llm,
            max_token_limit=buffer_memory_token_limit,
            memory_key="chat_history"
        )

        memory.output_key = "output"

        memory.chat_memory.messages = messages_from_dict(memory_state)

        self.agent_chain = initialize_agent(
            tools,
            llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=verbose,
            memory=memory
        )

    @abstractmethod
    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any,
    ) -> None:
        pass

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        pass

    def __call__(self, input: str):
        with get_openai_callback() as cb:
            cb.on_agent_action = self.on_agent_action
            cb.on_tool_start = self.on_tool_start
            cb.on_tool_end = self.on_tool_end

            try:
                output = self.agent_chain(inputs=[input])
                # we want to forward parse erros cause sometimes this just means the ai is asking for more input
            except OutputParserException as e:
                print("Parse output exception", str(e))
                output = str(e)

            # some even more fine grained token usage tracking would be cool
            self.token_usages.append({
                "total_tokens": cb.total_tokens,
                "completion_tokens": cb.completion_tokens,
                "prompt_tokens": cb.prompt_tokens,
                "cost_estimate": cb.total_cost
            })

            message_state = messages_to_dict(
                self.agent_chain.memory.chat_memory.messages)
        return output, message_state, self.token_usages
