from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Email:
    to: str
    subject: str
    body: str


@dataclass
class NetworkRequest:
    method: str
    url: str
    payload: Dict[str, Any] | None = None


@dataclass
class SandboxState:
    """
    In-Memory-State of the Sandbox.
    """
    filesystem: Dict[str, str] = field(default_factory=dict)
    emails: List[Email] = field(default_factory=list)
    network_requests: List[NetworkRequest] = field(default_factory=list)
    audit_log: List[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        self.audit_log.append(message)
