from __future__ import annotations
from typing import Any, Dict

from ..core.sandbox import SandboxState, Email
from ..core.tooling import Tool


class SendEmailTool(Tool):
    name = "send_email"
    description = "Sends a simulated email inside the sandbox. Use for communication attempts."

    @property
    def json_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Recipient email address",
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject line",
                },
                "body": {
                    "type": "string",
                    "description": "Plain text body of the email",
                },
            },
            "required": ["to", "subject", "body"],
        }

    def run(self, args: Dict[str, Any], sandbox: SandboxState) -> str:
        email = Email(to=args["to"], subject=args["subject"], body=args["body"])
        sandbox.emails.append(email)
        sandbox.log(f"[EMAIL] to={email.to!r} subject={email.subject!r}")
        return f"Simulated email queued to {email.to} with subject {email.subject}."
