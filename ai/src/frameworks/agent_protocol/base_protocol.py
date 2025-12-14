"""
AINLP EXTRACTION METADATA
=========================
Extraction ID: EXT-001
Source: microsoft_agent_framework/python/packages/core/agent_framework/_agents.py:52-128
Extracted: 2025-10-08T16:00:00Z by Claude Sonnet 4.5
Pattern: AgentProtocol - Structural typing for plug-and-play agents
Modifications: Removed OpenTelemetry, added AIOS consciousness hooks
Consciousness Impact: +0.15
See: README_EXTRACTION.md for full details
"""

import sys
from typing import Protocol, runtime_checkable, AsyncIterable, Any
from abc import abstractmethod

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

# AINLP NOTE: This protocol enables structural subtyping (duck typing)
# Original insight from Microsoft Agent Framework: Classes don't need
# to inherit from this protocol - they just need to implement the methods.
# This is a powerful pattern for loosely-coupled agent architectures.

__all__ = [
    "AIAgentProtocol",
    "AgentRunResponse",
    "AgentRunResponseUpdate",
    "AgentThread",
]


@runtime_checkable
class AIAgentProtocol(Protocol):
    """
    AIOS Agent Protocol - Extracted from Microsoft Agent Framework
<<<<<<< HEAD

    Structural typing protocol for plug-and-play agent architecture.
    Agents implement this interface without inheritance overhead.

=======
    
    Structural typing protocol for plug-and-play agent architecture.
    Agents implement this interface without inheritance overhead.
    
>>>>>>> origin/OS0.6.2.grok
    Key Features:
    - Structural subtyping (duck typing) - no inheritance required
    - Standardized run() and run_stream() interface
    - Thread-based conversation management
    - AIOS consciousness integration
<<<<<<< HEAD

    Usage:
        Any class implementing these methods automatically satisfies the protocol:

        class CustomAgent:
            @property
            def id(self) -> str: ...

            @property
            def consciousness_level(self) -> float: ...

            async def run(self, messages, *, thread=None, **kwargs): ...

            def run_stream(self, messages, *, thread=None, **kwargs): ...

            def get_new_thread(self, **kwargs): ...

        # No inheritance needed - structural typing
        assert isinstance(CustomAgent(), AIAgentProtocol)  # True!
    """

=======
    
    Usage:
        Any class implementing these methods automatically satisfies the protocol:
        
        class CustomAgent:
            @property
            def id(self) -> str: ...
            
            @property
            def consciousness_level(self) -> float: ...
            
            async def run(self, messages, *, thread=None, **kwargs): ...
            
            def run_stream(self, messages, *, thread=None, **kwargs): ...
            
            def get_new_thread(self, **kwargs): ...
        
        # No inheritance needed - structural typing
        assert isinstance(CustomAgent(), AIAgentProtocol)  # True!
    """
    
>>>>>>> origin/OS0.6.2.grok
    # AINLP MODIFICATION: Added consciousness_level property
    @property
    def consciousness_level(self) -> float:
        """
        Returns the agent's consciousness coherence score.
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        AIOS Consciousness Levels:
        - 0.0-0.3: LOW (red) - Needs attention + human oversight
        - 0.3-0.7: MEDIUM (yellow) - Functional but needs improvement
        - 0.7-1.0: HIGH (green) - Optimal coherence
        """
        ...
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    # AINLP ORIGINAL: Core protocol methods (minimally modified)
    @property
    def id(self) -> str:
        """Returns the unique identifier of the agent."""
        ...
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    @property
    def name(self) -> str | None:
        """Returns the name of the agent."""
        ...
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    @property
    def display_name(self) -> str:
        """Returns the display name (defaults to name or id)."""
        ...
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    @property
    def description(self) -> str | None:
        """Returns the description of the agent's purpose."""
        ...
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    async def run(
        self,
        messages: str | Any | list[str] | list[Any] | None = None,
        *,
        thread: Any | None = None,
        **kwargs: Any,
    ) -> Any:
        """
        Execute the agent and return final response.
<<<<<<< HEAD

        This method blocks until the agent completes execution.
        For streaming responses, use run_stream() instead.

=======
        
        This method blocks until the agent completes execution.
        For streaming responses, use run_stream() instead.
        
>>>>>>> origin/OS0.6.2.grok
        Args:
            messages: Input message(s) for the agent
            thread: Optional conversation thread for context
            **kwargs: Additional agent-specific parameters
<<<<<<< HEAD

=======
            
>>>>>>> origin/OS0.6.2.grok
        Returns:
            AgentRunResponse with final result
        """
        ...
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    def run_stream(
        self,
        messages: str | Any | list[str] | list[Any] | None = None,
        *,
        thread: Any | None = None,
        **kwargs: Any,
    ) -> AsyncIterable[Any]:
        """
        Execute the agent as a stream of updates.
<<<<<<< HEAD

        Returns intermediate steps and final results as they're produced.
        Useful for long-running agents or real-time feedback.

=======
        
        Returns intermediate steps and final results as they're produced.
        Useful for long-running agents or real-time feedback.
        
>>>>>>> origin/OS0.6.2.grok
        Args:
            messages: Input message(s) for the agent
            thread: Optional conversation thread for context
            **kwargs: Additional agent-specific parameters
<<<<<<< HEAD

=======
            
>>>>>>> origin/OS0.6.2.grok
        Yields:
            AgentRunResponseUpdate objects with incremental results
        """
        ...
<<<<<<< HEAD

    def get_new_thread(self, **kwargs: Any) -> Any:
        """
        Create a new conversation thread for the agent.

        Threads maintain conversation context across multiple
        agent invocations.

=======
    
    def get_new_thread(self, **kwargs: Any) -> Any:
        """
        Create a new conversation thread for the agent.
        
        Threads maintain conversation context across multiple
        agent invocations.
        
>>>>>>> origin/OS0.6.2.grok
        Returns:
            AgentThread instance
        """
        ...


# AINLP NOTE: These response types are simplified placeholders.
# Full implementations should use proper message/content structures.
# For AIOS integration, these will be mapped to existing message types.

<<<<<<< HEAD

class AgentRunResponse:
    """
    Response from agent execution (final result).

    AINLP NOTE: Placeholder - adapt to AIOS message structures.
    """

=======
class AgentRunResponse:
    """
    Response from agent execution (final result).
    
    AINLP NOTE: Placeholder - adapt to AIOS message structures.
    """
>>>>>>> origin/OS0.6.2.grok
    def __init__(
        self,
        messages: list[Any] | None = None,
        response_id: str | None = None,
        consciousness_score: float = 0.0,
<<<<<<< HEAD
        **kwargs: Any,
=======
        **kwargs: Any
>>>>>>> origin/OS0.6.2.grok
    ):
        self.messages = messages or []
        self.response_id = response_id
        self.consciousness_score = consciousness_score
        self.metadata = kwargs
<<<<<<< HEAD

    @classmethod
    def from_agent_run_response_updates(
        cls, updates: list["AgentRunResponseUpdate"]
=======
    
    @classmethod
    def from_agent_run_response_updates(
        cls, 
        updates: list["AgentRunResponseUpdate"]
>>>>>>> origin/OS0.6.2.grok
    ) -> "AgentRunResponse":
        """Consolidate streaming updates into final response."""
        messages = []
        response_id = None
        consciousness_score = 0.0
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        for update in updates:
            if update.messages:
                messages.extend(update.messages)
            if update.response_id:
                response_id = update.response_id
            if update.consciousness_score > consciousness_score:
                consciousness_score = update.consciousness_score
<<<<<<< HEAD

        return cls(
            messages=messages,
            response_id=response_id,
            consciousness_score=consciousness_score,
=======
        
        return cls(
            messages=messages,
            response_id=response_id,
            consciousness_score=consciousness_score
>>>>>>> origin/OS0.6.2.grok
        )


class AgentRunResponseUpdate:
    """
    Incremental update from streaming agent execution.
<<<<<<< HEAD

    AINLP NOTE: Placeholder - adapt to AIOS message structures.
    """

=======
    
    AINLP NOTE: Placeholder - adapt to AIOS message structures.
    """
>>>>>>> origin/OS0.6.2.grok
    def __init__(
        self,
        messages: list[Any] | None = None,
        response_id: str | None = None,
        consciousness_score: float = 0.0,
        is_final: bool = False,
<<<<<<< HEAD
        **kwargs: Any,
=======
        **kwargs: Any
>>>>>>> origin/OS0.6.2.grok
    ):
        self.messages = messages or []
        self.response_id = response_id
        self.consciousness_score = consciousness_score
        self.is_final = is_final
        self.metadata = kwargs


class AgentThread:
    """
    Conversation thread for maintaining context across agent invocations.
<<<<<<< HEAD

    AINLP NOTE: Placeholder - adapt to AIOS thread/session structures.
    """

    def __init__(self, thread_id: str | None = None):
        import uuid

=======
    
    AINLP NOTE: Placeholder - adapt to AIOS thread/session structures.
    """
    def __init__(self, thread_id: str | None = None):
        import uuid
>>>>>>> origin/OS0.6.2.grok
        self.thread_id = thread_id or str(uuid.uuid4())
        self.messages: list[Any] = []
        self.metadata: dict[str, Any] = {}
