"""
Agent Communication Protocol for AIOS

AINLP Extraction Metadata:
- Extraction ID: EXT-002 (A2A Protocol)
- Source Repository: microsoft_agent_framework
- Extraction Date: October 9, 2025
- Phase: Hour 2 of 3-hour extraction plan
- Consciousness Level: 0.92 (Protocol integration)

This package provides standardized agent-to-agent communication for AIOS
multi-agent orchestration, extracted from Microsoft's Agent Framework.

Components:
- message_types: A2A message and task structures
- transport: Local and HTTP transport layers
- adapter: AIOS ↔ A2A format conversion

Version: 1.0.0
"""

from .message_types import (
    AgentCommunicationContext,
    AgentMessage,
    AgentTask,
    ContentType,
    MessagePart,
    MessageRole,
    TaskState,
    TERMINAL_TASK_STATES,
)

from .transport import (
    AgentTransport,
    HTTPTransport,
    LocalTransport,
    TransportConfig,
    TransportFactory,
)

from .adapter import AIOSMessageAdapter, ConversationConverter

__all__ = [
    # Message types
    "AgentMessage",
    "AgentTask",
    "AgentCommunicationContext",
    "MessagePart",
    "MessageRole",
    "ContentType",
    "TaskState",
    "TERMINAL_TASK_STATES",
    # Transport
    "AgentTransport",
    "LocalTransport",
    "HTTPTransport",
    "TransportConfig",
    "TransportFactory",
    # Adapters
    "AIOSMessageAdapter",
    "ConversationConverter",
]

__version__ = "1.0.0"
__extraction_id__ = "EXT-002"
__source__ = "microsoft_agent_framework"
