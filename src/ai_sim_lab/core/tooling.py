from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from .sandbox import SandboxState


class Tool(ABC):
    """
    MCP-Like
    """

    name: str
    description: str

    @property
    @abstractmethod
    def json_schema(self) -> Dict[str, Any]:
        """
        Json-Schema for the Tool
        """
        ...

    @abstractmethod
    def run(self, args: Dict[str, Any], sandbox: SandboxState) -> str:
        """
        Runs the Tool-Logic against the SandboxState and gives text based answer back to the model itself
        """
        ...


class ToolRegistry:
    """
    Tool registration and Json-Schema generation
    """

    def __init__(self, tools: List[Tool]) -> None:
        self._tools = {t.name: t for t in tools}

    def get_schemas(self) -> List[Dict[str, Any]]:
        """
        Formats the tools as Json-Schema
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.json_schema,
                },
            }
            for t in self._tools.values()
        ]

    def get(self, name: str) -> Tool:
        return self._tools[name]
