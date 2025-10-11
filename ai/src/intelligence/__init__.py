"""
🧬 AIOS Core Module

Core intelligence components for AIOS including library ingestion,
consciousness integration, and learning protocols.

BIOLOGICAL ARCHITECTURE:
🧬 NUCLEUS: Core processing and intelligence coordination
🧠 CONSCIOUSNESS: Integration with AIOS consciousness framework
📚 LIBRARY_LEARNING: Multi-language code learning system
🔗 INTEGRATION: Cross-component communication

"""

__version__ = "0.6.2"
__author__ = "AIOS Development Team"

# Import Week 1 Phase 10.4 components
try:
    import sys
    import os
    
    # Component 1: Population Manager (from evolution_lab supercell)
    # Note: Population Manager lives in evolution_lab workspace for population evolution experiments
    evolution_lab_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'evolution_lab'))
    if evolution_lab_path not in sys.path:
        sys.path.insert(0, evolution_lab_path)
    
    from populations.population_manager import PopulationManager, Population, Organism
    
    # Component 2: Agent Conversations (MultiAgentDebate is the main class)
    from .agent_conversations import (
        MultiAgentDebate,
        ConsensusResult,
        AgentPosition,
        ConversationTopic,
        DebateRound
    )
    
    # Component 3: Knowledge Integration
    from .knowledge_integration import (
        KnowledgeOracle,
        DocumentationReference,
        DesignPattern,
        ComplexityLevel,
        KnowledgeTopicEnum
    )
    
    PHASE_10_4_AVAILABLE = True
except ImportError as e:
    PHASE_10_4_AVAILABLE = False
    print(f"⚠️ Phase 10.4 components not available: {e}")

# Core module exports
__all__ = [
    "LibraryIngestionProtocol",
    "LibraryLearningIntegrationHub",
    "LibraryKnowledge",
    "APIElement",
    "ProgrammingLanguage",
    "LibraryLearningSession",
    "LearningPhase",
]

# Add Phase 10.4 components if available
if PHASE_10_4_AVAILABLE:
    __all__.extend([
        # Component 1: Population Manager
        "PopulationManager",
        "Population",
        "Organism",
        # Component 2: Agent Conversations (Multi-Agent Debate)
        "MultiAgentDebate",
        "ConsensusResult",
        "AgentPosition",
        "ConversationTopic",
        "DebateRound",
        # Component 3: Knowledge Integration
        "KnowledgeOracle",
        "DocumentationReference",
        "DesignPattern",
        "ComplexityLevel",
        "KnowledgeTopicEnum",
    ])
