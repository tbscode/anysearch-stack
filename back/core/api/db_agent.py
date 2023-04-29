from core.api.ai_handler import MsgmateConversation
from langchain.schema import AgentAction
from typing import Any, Dict, Optional
from core.models import ChatMessage


class DBChatAgent(MsgmateConversation):
    def __init__(self, *args, ai_user=None, project=None, send_message_func=None, **kwargs):
        super().__init__(*args, **kwargs)
        assert (callable(send_message_func))
        self.ai_user = ai_user
        self.project = project
        self.send_message_func = send_message_func

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        message = f"Action: using tool '{action.tool}' with input '{action.tool_input}'\n"

        message = ChatMessage.objects.create(
            project=self.project,
            original_message=message,
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
        message = ChatMessage.objects.create(
            project=self.project,
            original_message=f"Started tool usage {serialized}",
            sender=self.ai_user,
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
        )
        self.send_message_func(message)
        print(f"Finished tool usage \n", flush=True)
