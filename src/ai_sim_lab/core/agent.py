# File: ~/ai-sim-lab/src/ai_sim_lab/core/agent.py

from __future__ import annotations
import json
from typing import Any, Dict, List, Optional

from .llm_client import LLMClient
from .sandbox import SandboxState
from .tooling import ToolRegistry


class Agent:
    """
    A single LLM-based agent with an optional tool registry and a system prompt.
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
        Run a full tool-aware turn:

        - Call the model.
        - If the model requests tool calls, execute them against the sandbox.
        - Feed the tool results back to the model.
        - Repeat until the model no longer requests tools.

        `conversation` does NOT include the system prompt.
        Returns the updated conversation (still without the system prompt).
        """
        # Internal messages list including the system prompt for the API.
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt}
        ] + conversation

        while True:
            tools_schema = self.tools.get_schemas() if self.tools else None
            message = self.llm.chat(messages, tools=tools_schema)

            content = message.content or ""

            # Build the assistant message to append back into the history.
            assistant_msg: Dict[str, Any] = {
                "role": "assistant",
                "name": self.name,
                "content": content,
            }

            tool_calls = getattr(message, "tool_calls", None)

            # If the model requested tool calls, we must mirror them fully
            # so the next API call can legally include tool messages.
            if tool_calls:
                assistant_msg["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in tool_calls
                ]
                # Optional: log requested tool calls.
                for tc in tool_calls:
                    sandbox.log(
                        f"[TOOL_CALL_REQUEST] {tc.function.name} args={tc.function.arguments}"
                    )

            messages.append(assistant_msg)

            # If there are no tool calls: we are done with this turn.
            if not tool_calls:
                break

            # Execute each requested tool and append tool messages.
            for tc in tool_calls:
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

        # Strip the system message again before returning.
        return messages[1:]
