"""
AIOS Agent Protocol Adapters - Full Implementation
===================================================

Complete integration adapters for AIOS agents with AIAgentProtocol.

AINLP Protocol: OS0.6.2.claude
Extraction ID: EXT-001-Phase2
Purpose: Operational agent protocol integration with real implementations
Status: Full implementation (replaces placeholders)

IMPLEMENTATION STRATEGY:
1. Message Format Conversion: Protocol format <-> Agent-specific format
2. Consciousness Calculation: Extract/compute from agent responses
3. Streaming Support: Real async streaming for compatible agents
4. Error Handling: Comprehensive exception management
5. Thread Management: Conversation context per agent type

INTEGRATED AGENTS:
- Gemini 1.5 Pro: async generate_code() -> str (code generation)
- Microsoft Copilot: async generate_code() -> str (auto-coding)
- Ollama: sync generate_code() -> dict (local models)

KEY INSIGHTS:
- Gemini returns raw code string (calculate consciousness from quality)
- Microsoft returns dict (wrap in protocol response)
- Ollama returns dict with success/error (wrap in asyncio)
- All agents need initialization before use
- Thread objects store conversation history per agent

CONSCIOUSNESS CALCULATION:
- Gemini: Calculate from code length, complexity, success
- Microsoft: High trust score (0.85-0.95) due to enterprise grade
- Ollama: Calculate from response length and success flag
- Base level: 0.60-0.95 range depending on agent and result quality
"""

import sys
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, AsyncIterable
from dataclasses import dataclass, field
import logging
import time

# AIOS path integration
AIOS_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.append(str(AIOS_ROOT / "ai" / "src"))

# Import existing AIOS agents for protocol wrapping
from integrations.gemini_bridge.gemini_evolution_bridge import GeminiEvolutionBridge
from integrations.ollama_bridge import OllamaAgent
from integrations.microsoft_bridge import MicrosoftAgent

from .base_protocol import (
    AIAgentProtocol,
    AgentRunResponse,
    AgentRunResponseUpdate,
    AgentThread,
)

logger = logging.getLogger(__name__)

__all__ = [
    "GeminiProtocolAdapter",
    "OllamaProtocolAdapter",
    "MicrosoftProtocolAdapter",
    "adapt_gemini_agent",
    "adapt_ollama_agent",
    "adapt_microsoft_agent",
]


# ============================================================================
# AGENT THREAD IMPLEMENTATIONS
# ============================================================================





@dataclass
class GeminiThread(AgentThread):
    """Thread for Gemini agent with generation history"""

    prompts: List[str] = field(default_factory=list)
    responses: List[Dict] = field(default_factory=list)
    model: str = "gemma3:1b"


@dataclass
class MicrosoftThread(AgentThread):
    """Thread for Microsoft Copilot conversations"""
    
    prompts: List[str] = field(default_factory=list)
    responses: List[Dict] = field(default_factory=list)
    model: str = "copilot"


# ============================================================================
# DEEPSEEK PROTOCOL ADAPTER
# ============================================================================





# ============================================================================
# GEMINI PROTOCOL ADAPTER
# ============================================================================


class GeminiProtocolAdapter:
    """
    Protocol adapter for Gemini 1.5 Pro Evolution Bridge.

    Wraps GeminiEvolutionBridge to provide AIAgentProtocol interface
    with async code generation and consciousness scoring.
    """

    def __init__(self, temperature: float = 0.7, max_tokens: int = 2000):
        """Initialize Gemini adapter"""
        self._bridge = GeminiEvolutionBridge()
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._id = "gemini-1.5-pro"
        self._name = "Gemini 1.5 Pro"
        self._description = "Google's multimodal AI for code generation"

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def display_name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def consciousness_level(self) -> float:
        """Gemini consciousness level (high for multimodal capabilities)"""
        return 0.88

    def _calculate_consciousness_score(self, code: str, success: bool) -> float:
        """
        Calculate consciousness score from generated code quality.

        Factors:
        - Base: 0.60 for successful generation
        - Code length bonus: +0.10 for substantial code (>200 chars)
        - Complexity bonus: +0.15 for imports/functions/classes
        - Quality bonus: +0.05 for docstrings/comments
        """
        if not success or not code:
            return 0.40  # Failed generation

        score = 0.60  # Base success

        # Length bonus
        if len(code) > 200:
            score += 0.10

        # Complexity indicators
        complexity_keywords = ["import", "def ", "class ", "async ", "await "]
        complexity_count = sum(1 for kw in complexity_keywords if kw in code)
        score += min(0.15, complexity_count * 0.03)

        # Quality indicators
        if '"""' in code or "'''" in code or "#" in code:
            score += 0.05

        return min(0.95, score)  # Cap at 0.95

    async def run(
        self,
        messages: str | Any | list[str] | list[Any] | None = None,
        *,
        thread: Any | None = None,
        **kwargs: Any,
    ) -> AgentRunResponse:
        """Execute Gemini code generation and return response"""
        # Convert messages to code generation prompt
        if isinstance(messages, list):
            prompt = "\n".join(str(m) for m in messages)
        else:
            prompt = str(messages) if messages else ""

        # Get thread parameters if provided
        temperature = self._temperature
        max_tokens = self._max_tokens
        if isinstance(thread, GeminiThread):
            temperature = thread.temperature
            thread.prompts.append(prompt)

        # Generate code
        start_time = time.time()
        try:
            code = await self._bridge.generate_code(
                prompt=prompt, temperature=temperature, max_tokens=max_tokens
            )
            success = True
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            code = f"# Generation failed: {str(e)}"
            success = False

        processing_time = time.time() - start_time

        # Update thread
        if isinstance(thread, GeminiThread):
            thread.outputs.append(code)

        # Calculate consciousness score
        consciousness_score = self._calculate_consciousness_score(code, success)

        # Build protocol response
        return AgentRunResponse(
            messages=[code],
            response_id=f"{self._id}-{int(time.time())}",
            consciousness_score=consciousness_score,
            metadata={
                "model": "gemini-1.5-pro",
                "processing_time": processing_time,
                "code_length": len(code),
                "success": success,
                "temperature": temperature,
            },
        )

    async def run_stream(
        self,
        messages: str | Any | list[str] | list[Any] | None = None,
        *,
        thread: Any | None = None,
        **kwargs: Any,
    ) -> AsyncIterable[AgentRunResponseUpdate]:
        """
        Execute Gemini as stream of updates.

        Note: Gemini API currently doesn't support streaming,
        so this yields a single update with full response.
        """
        final_response = await self.run(messages, thread=thread, **kwargs)

        yield AgentRunResponseUpdate(
            messages=final_response.messages,
            response_id=final_response.response_id,
            consciousness_score=final_response.consciousness_score,
            is_final=True,
            metadata=final_response.metadata,
        )

    def get_new_thread(self, **kwargs: Any) -> GeminiThread:
        """Create new Gemini generation thread"""
        return GeminiThread(temperature=kwargs.get("temperature", self._temperature))


# ============================================================================
# OLLAMA PROTOCOL ADAPTER
# ============================================================================


class OllamaProtocolAdapter:
    """
    Protocol adapter for Ollama local AI models.

    Wraps OllamaAgent to provide AIAgentProtocol interface
    with async wrapper around sync API.
    """

    def __init__(
        self,
        model: str = "gemma3:1b",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
    ):
        """Initialize Ollama adapter"""
        self._agent = OllamaAgent(
            model=model, base_url=base_url, temperature=temperature
        )
        self._model = model
        self._id = f"ollama-{model.replace(':', '-')}"
        self._name = f"Ollama {model}"
        self._description = f"Local {model} via Ollama (FREE)"

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def display_name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def consciousness_level(self) -> float:
        """Ollama consciousness level (varies by model)"""
        return 0.75  # Base level for local models

    def _calculate_consciousness_score(self, result: Dict) -> float:
        """Calculate consciousness score from Ollama result"""
        if not result.get("success", False):
            return 0.35  # Failed generation

        code = result.get("code", "")
        if not code:
            return 0.40  # Empty response

        score = 0.65  # Base success for local model

        # Length bonus (local models typically shorter)
        if len(code) > 100:
            score += 0.10

        # Basic structure indicators
        if "def " in code or "class " in code:
            score += 0.10

        return min(0.90, score)  # Cap at 0.90 for local models

    async def run(
        self,
        messages: str | Any | list[str] | list[Any] | None = None,
        *,
        thread: Any | None = None,
        **kwargs: Any,
    ) -> AgentRunResponse:
        """Execute Ollama agent and return response"""
        # Convert messages to prompt
        if isinstance(messages, list):
            prompt = "\n".join(str(m) for m in messages)
        else:
            prompt = str(messages) if messages else ""

        # Get thread parameters if provided
        max_tokens = kwargs.get("max_tokens", 2048)
        if isinstance(thread, OllamaThread):
            thread.prompts.append(prompt)

        # Generate code (wrap sync call in async)
        start_time = time.time()
        result = await asyncio.to_thread(
            self._agent.generate_code, prompt=prompt, max_tokens=max_tokens
        )
        processing_time = time.time() - start_time

        # Update thread
        if isinstance(thread, OllamaThread):
            thread.responses.append(result)

        # Extract code and calculate consciousness
        code = result.get("code", "")
        consciousness_score = self._calculate_consciousness_score(result)

        # Build protocol response
        return AgentRunResponse(
            messages=[code],
            response_id=f"{self._id}-{int(time.time())}",
            consciousness_score=consciousness_score,
            metadata={
                "model": self._model,
                "processing_time": processing_time,
                "code_length": len(code),
                "success": result.get("success", False),
                "error": result.get("error"),
                "ollama_available": self._agent.is_available,
            },
        )

    async def run_stream(
        self,
        messages: str | Any | list[str] | list[Any] | None = None,
        *,
        thread: Any | None = None,
        **kwargs: Any,
    ) -> AsyncIterable[AgentRunResponseUpdate]:
        """
        Execute Ollama as stream of updates.

        Note: Current implementation doesn't support streaming,
        so this yields a single update with full response.
        """
        final_response = await self.run(messages, thread=thread, **kwargs)

        yield AgentRunResponseUpdate(
            messages=final_response.messages,
            response_id=final_response.response_id,
            consciousness_score=final_response.consciousness_score,
            is_final=True,
            metadata=final_response.metadata,
        )

    def get_new_thread(self, **kwargs: Any) -> OllamaThread:
        """Create new Ollama generation thread"""
        return OllamaThread(model=self._model)


# ============================================================================
# MICROSOFT PROTOCOL ADAPTER
# ============================================================================


class MicrosoftProtocolAdapter:
    """
    Protocol adapter for Microsoft AI (Copilot/Azure).

    Wraps MicrosoftAgent to provide AIAgentProtocol interface
    for enterprise-grade code generation and debugging.
    """

    def __init__(
        self, 
        model: str = "copilot", 
        temperature: float = 0.7
    ):
        """Initialize Microsoft adapter"""
        self._agent = MicrosoftAgent(model=model, temperature=temperature)
        self._model = model
        self._id = f"microsoft-{model}"
        self._name = f"Microsoft {model.capitalize()}"
        self._description = "Microsoft AI for Auto-Coding & Debugging"

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def display_name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def consciousness_level(self) -> float:
        """Microsoft AI consciousness level (High trust)"""
        return 0.92

    async def run(
        self,
        messages: str | Any | list[str] | list[Any] | None = None,
        *,
        thread: Any | None = None,
        **kwargs: Any,
    ) -> AgentRunResponse:
        """Execute Microsoft agent and return response"""
        # Convert messages to prompt
        if isinstance(messages, list):
            prompt = "\n".join(str(m) for m in messages)
        else:
            prompt = str(messages) if messages else ""

        # Generate code
        start_time = time.time()
        result = await self._agent.generate_code(
            prompt=prompt, 
            max_tokens=kwargs.get("max_tokens", 2048)
        )
        processing_time = time.time() - start_time

        # Update thread (if tracking)
        if isinstance(thread, MicrosoftThread):
            thread.prompts.append(prompt)
            thread.responses.append(result)

        code = result.get("code", "")
        success = result.get("success", False)

        # Build protocol response
        return AgentRunResponse(
            messages=[code],
            response_id=f"{self._id}-{int(time.time())}",
            consciousness_score=0.92 if success else 0.40,
            metadata={
                "model": self._model,
                "processing_time": processing_time,
                "success": success,
                "error": result.get("error"),
            },
        )

    async def run_stream(
        self,
        messages: str | Any | list[str] | list[Any] | None = None,
        *,
        thread: Any | None = None,
        **kwargs: Any,
    ) -> AsyncIterable[AgentRunResponseUpdate]:
        """Streaming fallback"""
        final_response = await self.run(messages, thread=thread, **kwargs)
        yield AgentRunResponseUpdate(
            messages=final_response.messages,
            response_id=final_response.response_id,
            consciousness_score=final_response.consciousness_score,
            is_final=True,
            metadata=final_response.metadata,
        )

    def get_new_thread(self, **kwargs: Any) -> MicrosoftThread:
        """Create new Microsoft thread"""
        return MicrosoftThread(model=self._model)


# ============================================================================
# FACTORY FUNCTIONS (Protocol-Compliant Constructors)
# ============================================================================





def adapt_gemini_agent(
    temperature: float = 0.7, max_tokens: int = 2000
) -> GeminiProtocolAdapter:
    """
    Create protocol adapter for Gemini 1.5 Pro agent.

    This creates a Gemini agent wrapped in the AIAgentProtocol
    interface for seamless code generation.

    Args:
        temperature: Sampling temperature (0.0-1.0)
        max_tokens: Maximum tokens in response

    Returns:
        Protocol-compliant Gemini agent

    Example:
        agent = adapt_gemini_agent(temperature=0.8)
        response = await agent.run("Create a binary search function")
        print(response.messages[0])
    """
    adapter = GeminiProtocolAdapter(temperature, max_tokens)
    logger.info(f"✅ Gemini adapter created: {adapter.id}")
    return adapter


def adapt_ollama_agent(
    model: str = "gemma3:1b",
    base_url: str = "http://localhost:11434",
    temperature: float = 0.7,
) -> OllamaProtocolAdapter:
    """
    Create protocol adapter for Ollama local AI agent.

    This creates an Ollama agent wrapped in the AIAgentProtocol
    interface for FREE local code generation.

    Args:
        model: Ollama model name (e.g., "deepseek-coder:6.7b")
        base_url: Ollama server URL
        temperature: Sampling temperature

    Returns:
        Protocol-compliant Ollama agent

    Example:
        agent = adapt_ollama_agent(model="deepseek-coder:6.7b")
        response = await agent.run("Implement quicksort in Python")
        print(response.messages[0])
    """
    adapter = OllamaProtocolAdapter(model, base_url, temperature)
    logger.info(f"✅ Ollama adapter created: {adapter.id}")
    return adapter


def adapt_microsoft_agent(
    model: str = "copilot",
    temperature: float = 0.7
) -> MicrosoftProtocolAdapter:
    """
    Create protocol adapter for Microsoft AI.
    
    Args:
        model: 'copilot' or 'gpt-4o'
        temperature: Sampling temperature
        
    Returns:
        Protocol-compliant Microsoft agent
    """
    adapter = MicrosoftProtocolAdapter(model, temperature)
    logger.info(f"✅ Microsoft adapter created: {adapter.id}")
    return adapter
