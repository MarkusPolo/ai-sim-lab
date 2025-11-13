from __future__ import annotations
from typing import Any, Dict, List, Optional

from openai import OpenAI
from ..config import OPENAI_MODEL

_client = OpenAI()


class LLMClient:
    """
    thin wrapper for OpenAI-Client
    """

    def __init__(self, model: str | None = None) -> None:
        self.model = model or OPENAI_MODEL

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: str = "auto",
    ):
        """
        messages: Chat-History (w/o systemprompts).
        tools: OpenAI-Tool-Schema (function calling).
        """
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice

        response = _client.chat.completions.create(**kwargs)
        return response.choices[0].message
