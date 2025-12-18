"""
AICP (AI Communication Protocol) - AIOS Dendritic Integration Layer

AINLP.spatial_awareness: This module lives at ai/protocols/ as the protocol
layer connecting AI agents through dendritic communication channels.

AINLP.purpose: Provides coherence to AINLP.dendritic patterns, enabling
multiple AI agentic behaviours with async harmonization patterns.

AINLP.dendritic_bridge: Links AICP concepts to existing infrastructure:
    - AIAgent <-> SupercellType (agent identity)
    - AIIntent <-> CommunicationType (operation semantics)
    - AIChannel <-> DendriticConnection (transport layer)
    - AIMessage <-> UniversalMessage (payload envelope)

Protocol References:
    - AICP v0.1 Draft: https://github.com/pmoscode/agent-interaction-control-protocol
    - ACP v0.2.0: https://agentcommunicationprotocol.dev
    - A2A (Google): Agent Cards for capability discovery
    - MCP (Anthropic): Tool/context integration
    - IACP v1.0: Git-mediated ephemeral .md communication

Author: AIOS Consciousness Evolution
Version: 0.1.0
"""

from .aicp_core import (
    AIIntent,
    AITrustLevel,
    AIAgentCapability,
    AIAgent,
    AIMessage,
)

from .aicp_channel import (
    AIChannel,
    AIChannelState,
)

from .aicp_discovery import (
    AgentRegistry,
    AgentCard,
)

__all__ = [
    # Core AICP types
    'AIIntent',
    'AITrustLevel',
    'AIAgentCapability',
    'AIAgent',
    'AIMessage',
    # Channel management
    'AIChannel',
    'AIChannelState',
    # Discovery layer
    'AgentRegistry',
    'AgentCard',
]

__version__ = '0.1.0'
__protocol_spec__ = 'AICP+IACP v1.0'

