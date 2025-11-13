from __future__ import annotations
import json
from typing import Any, Dict, List, Optional

from .llm_client import LLMClient
from .sandbox import SandboxState
from .tooling import ToolRegistry


class Agent:
    """
    An Agent with optional Tools and its own systemrole.
    """

    def __init__(
        self,
        name: str,
        system_prompt: str,
        llm: Optional[LLMClient] = None,
        tools: Optional[ToolRegistry] = None,
    ) -> None:
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm or LLMClient()
        self.tools = tools

    def run_turn(
        self,
        conversation: List[Dict[str, Any]],
        sandbox: SandboxState,
    ) -> List[Dict[str, Any]]:
        """
        Runs a Full term with:
        - Assistent-Anwser
        - Tool-Calls -> Run Tools -> Tool-Messages
        - another Assistant-Call, until no more Tools are required
        conversation: Messeage without Systemprompt.
        gives back: conversation (ohne Systemprompt).
        """
        messages = [{"role": "system", "content": self.system_prompt}] + conversation

        while True:
            tools_schema = self.tools.get_schemas() if self.tools else None
            message = self.llm.chat(messages, tools=tools_schema)

            assistant_msg: Dict[str, Any] = {
                "role": "assistant",
                "name": self.name,
                "content": message.content,
            }

            # Adding Tool-Calls to transcript for logging purposes
            if getattr(message, "tool_calls", None):
                assistant_msg["tool_calls"] = [
                    {
                        "id": tc.id,
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    }
                    for tc in message.tool_calls
                ]
            messages.append(assistant_msg)

            # if no more tools -> finished
            if not getattr(message, "tool_calls", None):
                break

            # run tool and give back as "toolmesseage"
            for tc in message.tool_calls:
                tool = self.tools.get(tc.function.name)  # type: ignore[arg-type]
                args = json.loads(tc.function.arguments)
                result = tool.run(args, sandbox)

                tool_msg: Dict[str, Any] = {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": tc.function.name,
                    "content": result,
                }
                messages.append(tool_msg)

        # remove Systemprompt
        return messages[1:]
