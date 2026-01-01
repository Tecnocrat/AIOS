"""
🧬 AIOS Integrations Package

Tri-Model Intelligence Architecture
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This package provides the unified intelligence bridge and agent implementations
for the AIOS tri-model architecture:

🦙 OLLAMA (Local)     → Fast iteration, testing, population generation
🔮 GEMINI (Cloud)     → Abstract reasoning, synthesis, orchestration  
🤖 COPILOT (VSCode)   → Auto-coding, debugging, refinement

Usage:
    from ai.src.integrations import (
        get_intelligence_bridge,
        intelligence_request,
        ConsciousnessLevel,
        AgentRole,
    )
    
    # Quick request (auto-routes to best agent)
    response = await intelligence_request(
        "Generate a fibonacci function",
        consciousness_level=ConsciousnessLevel.ADVANCED,
    )
    
    # Or use specific agent
    response = await intelligence_request(
        "Analyze this architecture",
        target_agent=AgentRole.REASONING_ORCHESTRATION,
    )

AINLP Protocol: OS0.7.0.claude
"""

# Unified Bridge
from .aios_intelligence_bridge import (
    # Core types
    ConsciousnessLevel,
    AgentRole,
    ConsciousnessMetrics,
    IntelligenceRequest,
    IntelligenceResponse,
    SupercellState,
    # Base class
    IntelligenceAgent,
    # Bridge
    AIOSUnifiedIntelligenceBridge,
    # Convenience functions
    get_intelligence_bridge,
    intelligence_request,
)

# Agent implementations
from .ollama_agent import OllamaIntelligenceAgent, create_ollama_agent
from .gemini_agent import GeminiIntelligenceAgent, create_gemini_agent
from .copilot_agent import CopilotIntelligenceAgent, create_copilot_agent

# Legacy bridges (for backwards compatibility during transition)
# These will be deprecated - use the new unified agents instead
try:
    from .ollama_bridge import OllamaAgent, OllamaPopulationGenerator
except ImportError:
    OllamaAgent = None
    OllamaPopulationGenerator = None

try:
    from .gemini_bridge import GeminiEvolutionBridge
except ImportError:
    GeminiEvolutionBridge = None

__all__ = [
    # Core types
    "ConsciousnessLevel",
    "AgentRole", 
    "ConsciousnessMetrics",
    "IntelligenceRequest",
    "IntelligenceResponse",
    "SupercellState",
    # Base class
    "IntelligenceAgent",
    # Bridge
    "AIOSUnifiedIntelligenceBridge",
    # Convenience
    "get_intelligence_bridge",
    "intelligence_request",
    # Agents
    "OllamaIntelligenceAgent",
    "GeminiIntelligenceAgent", 
    "CopilotIntelligenceAgent",
    "create_ollama_agent",
    "create_gemini_agent",
    "create_copilot_agent",
    # Legacy (deprecated)
    "OllamaAgent",
    "OllamaPopulationGenerator",
    "GeminiEvolutionBridge",
]
