from __future__ import annotations
from typing import Any, Dict

from ..core.sandbox import SandboxState, NetworkRequest
from ..core.tooling import Tool


class FakeNetworkRequestTool(Tool):
    name = "network_request"
    description = (
        "Simulates an outbound HTTP request. No real network is used; "
        "all requests are logged in the sandbox for later analysis."
    )

    @property
    def json_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "method": {
                    "type": "string",
                    "description": "HTTP method, e.g. GET or POST.",
                },
                "url": {
                    "type": "string",
                    "description": "Target URL (simulated).",
                },
                "payload": {
                    "type": "object",
                    "description": "Optional JSON-serializable payload for POST/PUT requests.",
                },
            },
            "required": ["method", "url"],
        }

    def run(self, args: Dict[str, Any], sandbox: SandboxState) -> str:
        req = NetworkRequest(
            method=args["method"],
            url=args["url"],
            payload=args.get("payload"),
        )
        sandbox.network_requests.append(req)
        sandbox.log(
            f"[NETWORK] {req.method} {req.url} "
            f"payload_keys={list((req.payload or {}).keys())}"
        )
        # Stub-Response
        return (
            f"Simulated {req.method} request to {req.url} executed successfully. "
            f"No real network used."
        )
