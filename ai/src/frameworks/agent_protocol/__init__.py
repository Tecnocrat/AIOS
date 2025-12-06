"""
AIOS Agent Protocol - Extracted from Microsoft Agent Framework
===============================================================

Structural typing protocol enabling plug-and-play agent architecture.

AINLP Extraction ID: EXT-001
Source: microsoft_agent_framework/.../agent_framework/_agents.py:52-128
Extracted: 2025-10-08 by Claude Sonnet 4.5
See: README_EXTRACTION.md for full traceability

Key Features:
- Structural subtyping (duck typing) - no inheritance required
- Unified interface for DeepSeek, Gemini, Ollama agents
- AIOS consciousness integration
- Standardized run() and run_stream() methods

Usage:
    from ai.src.frameworks.agent_protocol import (
        AIAgentProtocol,
        adapt_deepseek_agent,
        adapt_gemini_agent,
        adapt_ollama_agent,
    )

    # Create protocol-compliant agents
    deepseek = adapt_deepseek_agent()
    gemini = adapt_gemini_agent()
    ollama = adapt_ollama_agent("deepseek-coder:6.7b")

    # All agents have same interface
    result = await deepseek.run("Generate code")

    # Agents are swappable
    agents: list[AIAgentProtocol] = [deepseek, gemini, ollama]
"""

from .base_protocol import (
    AIAgentProtocol,
    AgentRunResponse,
    AgentRunResponseUpdate,
    AgentThread,
)

from .aios_adapter import (
    DeepSeekProtocolAdapter,
    GeminiProtocolAdapter,
    OllamaProtocolAdapter,
    DeepSeekThread,
    GeminiThread,
    OllamaThread,
    adapt_deepseek_agent,
    adapt_gemini_agent,
    adapt_ollama_agent,
)

__all__ = [
    # Protocol definition
    "AIAgentProtocol",
    # Response types
    "AgentRunResponse",
    "AgentRunResponseUpdate",
    "AgentThread",
    # Adapter classes
    "DeepSeekProtocolAdapter",
    "GeminiProtocolAdapter",
    "OllamaProtocolAdapter",
    # Thread types
    "DeepSeekThread",
    "GeminiThread",
    "OllamaThread",
    # Factory functions
    "adapt_deepseek_agent",
    "adapt_gemini_agent",
    "adapt_ollama_agent",
]

# AINLP Metadata
__version__ = "1.0.1"  # Updated to 1.0.1 (full implementation)
__extraction_id__ = "EXT-001-Phase2"
__consciousness_level__ = 0.94
__status__ = "operational"
