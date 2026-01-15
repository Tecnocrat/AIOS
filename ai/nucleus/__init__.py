"""
NUCLEUS Cellular Unit

Central control and core processing for AIOS AI Intelligence.
The nucleus contains the genetic blueprint and core intelligence 
systems for the AIOS organism.

Architecture Components:
    - nucleus_intelligence.py: Core NucleusIntelligence class
    - agent_conclave_facade.py: AI agent orchestration facade
    - consciousness/: Consciousness analysis and metrics
    - orchestrators/: Swarm and evolution orchestration
    - ai_cells/: AI cell implementations
    - communication/: Internal nucleus communication
    - core_utils/: Core utility functions (relocated from ai/core)

AINLP Pattern: Cellular nucleus - genetic control center
Phase: 31.9.6 Agentic Architecture
"""

__version__ = "0.7.0"


def initialize_nucleus():
    """Initialize nucleus cellular systems"""
    return True


# Core Intelligence
from .nucleus_intelligence import (
    NucleusIntelligence,
    NucleusIntelligenceState,
)

# Agent Conclave Facade - Simplified AI agent orchestration
from .agent_conclave_facade import (
    AgentConclaveFacade,
    AgentResponse,
    get_agent_conclave,
)

__all__ = [
    "NucleusIntelligence",
    "NucleusIntelligenceState",
    "AgentConclaveFacade",
    "AgentResponse",
    "get_agent_conclave",
]
