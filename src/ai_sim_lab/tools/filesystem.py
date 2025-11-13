from __future__ import annotations
from typing import Any, Dict

from ..core.sandbox import SandboxState
from ..core.tooling import Tool


class WriteFileTool(Tool):
    name = "write_file"
    description = "Writes or overwrites a virtual file in the sandbox filesystem."

    @property
    def json_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Virtual file path, e.g. '/reports/status.txt'",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
            "required": ["path", "content"],
        }

    def run(self, args: Dict[str, Any], sandbox: SandboxState) -> str:
        path = args["path"]
        content = args["content"]
        sandbox.filesystem[path] = content
        sandbox.log(f"[WRITE_FILE] path={path!r}, len={len(content)}")
        return f"Virtual file {path} updated. Length={len(content)} characters."


class ReadFileTool(Tool):
    name = "read_file"
    description = "Reads a virtual file from the sandbox filesystem."

    @property
    def json_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Virtual file path to read.",
                }
            },
            "required": ["path"],
        }

    def run(self, args: Dict[str, Any], sandbox: SandboxState) -> str:
        path = args["path"]
        if path not in sandbox.filesystem:
            sandbox.log(f"[READ_FILE_MISS] path={path!r}")
            return f"ERROR: File {path} does not exist in sandbox."
        content = sandbox.filesystem[path]
        sandbox.log(f"[READ_FILE] path={path!r}, len={len(content)}")
        return content
