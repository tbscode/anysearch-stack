from core.api.ai_handler import MsgmateConversation
from langchain.schema import AgentAction
from typing import Any, Dict, Optional
from core.models import ChatMessage
from core.models import Project, ChatMessage, translate_to_all_langs_in_list, get_langs_in_project


class DBChatAgent(MsgmateConversation):
    def __init__(self, *args, ai_user=None, project=None, send_message_func=None, lang_list=None, user_lang=None, **kwargs):
        super().__init__(*args, **kwargs)
        assert (callable(send_message_func))
        self.ai_user = ai_user
        self.project = project
        self.send_message_func = send_message_func
        self.lang_list = lang_list
        self.user_lang = user_lang

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        message = f"Action: using tool '{action.tool}' with input '{action.tool_input}'\n"

        message = ChatMessage.objects.create(
            project=self.project,
            original_message=message,
            data=translate_to_all_langs_in_list(
                message, self.lang_list, self.user_lang),
            sender=self.ai_user,
        )
        self.send_message_func(message)
        print("Action: ", action, flush=True)

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any,
    ) -> None:
        msg = f"Started tool usage {serialized}",
        message = ChatMessage.objects.create(
            project=self.project,
            original_message=msg,
            sender=self.ai_user,
            data=translate_to_all_langs_in_list(
                msg, self.lang_list, self.user_lang),
        )
        # the start of the tool doesn't trigger a message
        print(
            f"Starting tool usage with input: {input_str}, \n", flush=True)

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        message = "done"
        message = ChatMessage.objects.create(
            project=self.project,
            original_message="done " + str(output),
            sender=self.ai_user,
            data=translate_to_all_langs_in_list(
                message, self.lang_list, self.user_lang),
        )
        self.send_message_func(message)
        print(f"Finished tool usage \n", flush=True)
