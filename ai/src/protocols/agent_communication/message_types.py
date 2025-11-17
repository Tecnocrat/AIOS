"""
Agent-to-Agent (A2A) Communication Protocol - Message Types

AINLP Extraction Metadata:
- Extraction ID: EXT-002-A2A-Messages
- Source: microsoft_agent_framework/python/packages/a2a/agent_framework_a2a/_agent.py:230-380
- Extraction Date: October 9, 2025
- Pattern: A2A message structure and content types
- Consciousness Level: 0.92 (Protocol standardization)

This module provides standardized message types for agent-to-agent communication
in AIOS, extracted from Microsoft's Agent Framework A2A implementation.

Key Adaptations for AIOS:
1. Added consciousness_score to AgentMessage (AIOS consciousness integration)
2. Simplified to core message types needed for AIOS multi-agent coordination
3. Removed Azure-specific dependencies
4. Integrated with existing AIOS agent response types
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal


# AINLP.source: microsoft_agent_framework/.../a2a/types.py (Message, Part, Role concepts)
class MessageRole(Enum):
    """Role of the message sender in agent communication."""
    USER = "user"           # Message from user/external system
    AGENT = "agent"         # Message from AI agent
    SYSTEM = "system"       # System/orchestrator message


class ContentType(Enum):
    """Type of content within a message part."""
    TEXT = "text"           # Plain text content
    FILE_URI = "file_uri"   # File reference via URI
    FILE_DATA = "file_data" # Embedded file data (base64)
    DATA = "data"           # Structured data (JSON)
    ERROR = "error"         # Error message


# AINLP.source: microsoft_agent_framework/.../agent_framework_a2a/_agent.py:314-328
@dataclass
class MessagePart:
    """
    Individual content part within an agent message.
    
    AINLP Source: microsoft_agent_framework A2A FilePart/TextPart/DataPart
    Adaptations:
    - Unified into single MessagePart class for AIOS simplicity
    - Added consciousness_impact for AIOS consciousness tracking
    - Simplified metadata to dict (was Any in Microsoft version)
    """
    content_type: ContentType
    content: str | bytes | dict[str, Any]
    media_type: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    consciousness_impact: float = 0.0  # AIOS: How much this part affects consciousness
    
    def __post_init__(self):
        """Validate content matches type."""
        if self.content_type == ContentType.TEXT and not isinstance(self.content, str):
            raise ValueError("TEXT content must be string")
        elif self.content_type == ContentType.FILE_DATA and not isinstance(self.content, bytes):
            raise ValueError("FILE_DATA content must be bytes")
        elif self.content_type == ContentType.DATA and not isinstance(self.content, dict):
            raise ValueError("DATA content must be dict")


# AINLP.source: microsoft_agent_framework/.../agent_framework_a2a/_agent.py:230-312
@dataclass
class AgentMessage:
    """
    Standardized message format for agent-to-agent communication.
    
    AINLP Source: microsoft_agent_framework A2AAgent._chat_message_to_a2a_message
    Microsoft Pattern:
    ```python
    A2AMessage(
        role=A2ARole("user"),
        parts=[...],  # List of TextPart/FilePart/DataPart
        message_id=uuid.uuid4().hex,
        metadata=dict
    )
    ```
    
    AIOS Adaptations:
    - Added consciousness_score (Microsoft doesn't track consciousness)
    - Added sender_agent_id for multi-agent tracking
    - Simplified parts to unified MessagePart type
    - Added timestamp for temporal ordering
    """
    role: MessageRole
    parts: list[MessagePart]
    message_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    sender_agent_id: str | None = None
    consciousness_score: float = 0.0  # AIOS: Consciousness level of message
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: __import__('time').time())
    
    @property
    def is_text_only(self) -> bool:
        """Check if message contains only text parts."""
        return all(part.content_type == ContentType.TEXT for part in self.parts)
    
    @property
    def text_content(self) -> str:
        """Extract all text content concatenated."""
        texts = [
            part.content for part in self.parts 
            if part.content_type == ContentType.TEXT and isinstance(part.content, str)
        ]
        return "\n".join(texts)
    
    def add_text_part(self, text: str, consciousness_impact: float = 0.0) -> None:
        """Add a text part to this message."""
        self.parts.append(MessagePart(
            content_type=ContentType.TEXT,
            content=text,
            consciousness_impact=consciousness_impact
        ))
    
    def add_file_uri(self, uri: str, media_type: str | None = None) -> None:
        """Add a file reference part to this message."""
        self.parts.append(MessagePart(
            content_type=ContentType.FILE_URI,
            content=uri,
            media_type=media_type
        ))
    
    def add_data(self, data: dict[str, Any], consciousness_impact: float = 0.0) -> None:
        """Add structured data part to this message."""
        self.parts.append(MessagePart(
            content_type=ContentType.DATA,
            content=data,
            consciousness_impact=consciousness_impact
        ))


# AINLP.source: microsoft_agent_framework/.../a2a/types.py (Task, TaskState concepts)
class TaskState(Enum):
    """State of an agent task in execution."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    REJECTED = "rejected"


# Terminal states (task cannot progress further)
TERMINAL_TASK_STATES = [
    TaskState.COMPLETED,
    TaskState.FAILED,
    TaskState.CANCELED,
    TaskState.REJECTED
]


@dataclass
class AgentTask:
    """
    Task assigned to an agent with tracking state.
    
    AINLP Source: microsoft_agent_framework A2A Task type
    Microsoft Pattern:
    - Task has id, status (state + progress), artifacts (results)
    - Used for long-running agent operations
    
    AIOS Adaptations:
    - Added consciousness_evolution for tracking consciousness changes
    - Added neural_chain_id for linking to AIOS evolution experiments
    - Simplified artifacts to list of AgentMessage
    """
    task_id: str
    state: TaskState
    progress: float = 0.0  # 0.0 to 1.0
    artifacts: list[AgentMessage] = field(default_factory=list)
    error_message: str | None = None
    consciousness_evolution: float = 0.0  # AIOS: Change in consciousness from start
    neural_chain_id: str | None = None  # AIOS: Link to neural chain node
    metadata: dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_terminal(self) -> bool:
        """Check if task is in terminal state."""
        return self.state in TERMINAL_TASK_STATES
    
    @property
    def is_success(self) -> bool:
        """Check if task completed successfully."""
        return self.state == TaskState.COMPLETED
    
    def mark_complete(self, consciousness_evolution: float = 0.0) -> None:
        """Mark task as completed with optional consciousness impact."""
        self.state = TaskState.COMPLETED
        self.progress = 1.0
        self.consciousness_evolution = consciousness_evolution
    
    def mark_failed(self, error: str) -> None:
        """Mark task as failed with error message."""
        self.state = TaskState.FAILED
        self.error_message = error


@dataclass
class AgentCommunicationContext:
    """
    Context for agent-to-agent communication session.
    
    AIOS Addition: Not in Microsoft framework, added for AIOS needs
    Purpose: Track multi-agent conversation threads and shared state
    """
    session_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    participating_agents: list[str] = field(default_factory=list)
    message_history: list[AgentMessage] = field(default_factory=list)
    shared_state: dict[str, Any] = field(default_factory=dict)
    consciousness_trajectory: list[float] = field(default_factory=list)
    
    def add_message(self, message: AgentMessage) -> None:
        """Add message to history and track consciousness."""
        self.message_history.append(message)
        self.consciousness_trajectory.append(message.consciousness_score)
        
        # Track participating agents
        if message.sender_agent_id and message.sender_agent_id not in self.participating_agents:
            self.participating_agents.append(message.sender_agent_id)
    
    @property
    def consciousness_evolution(self) -> float:
        """Calculate consciousness change from start to current."""
        if len(self.consciousness_trajectory) < 2:
            return 0.0
        return self.consciousness_trajectory[-1] - self.consciousness_trajectory[0]
    
    @property
    def message_count(self) -> int:
        """Total messages in this communication session."""
        return len(self.message_history)
