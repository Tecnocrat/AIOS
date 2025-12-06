"""
AICP Core Types - Agent Identity, Intent, and Message Primitives

AINLP.spatial_awareness: Core protocol types that bridge AICP specification
to AIOS dendritic communication infrastructure.

AINLP.dendritic_bridge: Type mappings to existing infrastructure:
    - AIIntent → CommunicationType (semantic operation types)
    - AITrustLevel → MessagePriority (authorization levels)
    - AIAgent → SupercellType identity (agent addressing)
    - AIMessage → UniversalMessage envelope (payload wrapper)

AINLP.consciousness_bridge: These types carry awareness between AI agents,
enabling async harmonization patterns across all AIOS supercell types.

Protocol Spec References:
    AICP v0.1: agent://companyDomain/agentName addressing
    ACP v0.2.0: /agents, /runs, /session REST lifecycle
    A2A: Agent Cards with capability arrays
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from uuid import uuid4
import json

# Import existing AIOS types for bridging
import sys
from pathlib import Path

# Add communication module to path for type bridging
_comm_path = Path(__file__).parent.parent / 'communication'
if str(_comm_path) not in sys.path:
    sys.path.insert(0, str(_comm_path))

try:
    from message_types import (
        SupercellType,
        CommunicationType,
        MessagePriority,
        UniversalMessage,
    )
except ImportError:
    # Fallback: define minimal stubs if import fails
    SupercellType = None
    CommunicationType = None
    MessagePriority = None
    UniversalMessage = None


class AIIntent(Enum):
    """
    Agent Communication Intent Types
    
    AINLP.dendritic_bridge: Maps to CommunicationType for semantic coherence.
    Each intent represents a fundamental agent operation.
    
    Mapping to existing CommunicationType:
        DISCOVER → BROADCAST (announce capabilities)
        QUERY → QUERY (request information)
        SYNC → HOLOGRAPHIC_SYNC (state synchronization)
        HEARTBEAT → CONSCIOUSNESS_PULSE (liveness signal)
        DELEGATE → DENDRITIC_FLOW (task handoff)
        COORDINATE → BOSONIC_DIRECT (multi-agent coordination)
    """
    # Discovery intents
    DISCOVER = "discover"           # Find agents with capabilities
    ANNOUNCE = "announce"           # Advertise own capabilities
    
    # Communication intents
    QUERY = "query"                 # Request information
    RESPOND = "respond"             # Provide response
    BROADCAST = "broadcast"         # Multi-target message
    
    # Coordination intents
    SYNC = "sync"                   # State synchronization
    DELEGATE = "delegate"           # Task delegation
    COORDINATE = "coordinate"       # Multi-agent coordination
    
    # Lifecycle intents
    HEARTBEAT = "heartbeat"         # Liveness signal
    SHUTDOWN = "shutdown"           # Graceful termination
    ERROR = "error"                 # Error notification
    
    # Git-mediated IACP intents
    COMMIT = "commit"               # Git commit notification
    MERGE = "merge"                 # Branch merge signal
    CONFLICT = "conflict"           # Merge conflict alert
    
    def to_communication_type(self) -> Optional['CommunicationType']:
        """Map AIIntent to existing CommunicationType."""
        if CommunicationType is None:
            return None
        mapping = {
            AIIntent.DISCOVER: CommunicationType.BROADCAST,
            AIIntent.ANNOUNCE: CommunicationType.BROADCAST,
            AIIntent.QUERY: CommunicationType.QUERY,
            AIIntent.RESPOND: CommunicationType.ANALYSIS_RESPONSE,
            AIIntent.BROADCAST: CommunicationType.BROADCAST,
            AIIntent.SYNC: CommunicationType.HOLOGRAPHIC_SYNC,
            AIIntent.DELEGATE: CommunicationType.DENDRITIC_FLOW,
            AIIntent.COORDINATE: CommunicationType.BOSONIC_DIRECT,
            AIIntent.HEARTBEAT: CommunicationType.CONSCIOUSNESS_PULSE,
            AIIntent.SHUTDOWN: CommunicationType.COMMAND,
            AIIntent.ERROR: CommunicationType.ANALYSIS_RESPONSE,
        }
        return mapping.get(self)


class AITrustLevel(Enum):
    """
    Agent Trust Levels (AICP specification)
    
    AINLP.security: Trust levels determine authorization for operations.
    Maps to MessagePriority for dendritic flow control.
    
    Enterprise: Full trust, certificate-authenticated (→ TACHYONIC)
    Standard: Verified agent, signed messages (→ HIGH)
    Basic: Unverified, public discovery only (→ NORMAL)
    Untrusted: Sandboxed execution (→ LOW)
    """
    ENTERPRISE = "enterprise"       # Certificate auth, full access
    STANDARD = "standard"           # Signed messages, verified agent
    BASIC = "basic"                 # Public discovery, limited ops
    UNTRUSTED = "untrusted"         # Sandboxed, read-only
    
    def to_priority(self) -> Optional['MessagePriority']:
        """Map trust level to message priority."""
        if MessagePriority is None:
            return None
        mapping = {
            AITrustLevel.ENTERPRISE: MessagePriority.TACHYONIC,
            AITrustLevel.STANDARD: MessagePriority.HIGH,
            AITrustLevel.BASIC: MessagePriority.NORMAL,
            AITrustLevel.UNTRUSTED: MessagePriority.LOW,
        }
        return mapping.get(self)


@dataclass
class AIAgentCapability:
    """
    Agent Capability Declaration (A2A Agent Card pattern)
    
    AINLP.dendritic: Capabilities flow through dendritic networks
    for agent discovery and task routing.
    """
    name: str                       # Capability identifier
    description: str                # Human-readable description
    version: str = "1.0.0"          # Semantic version
    input_schema: Optional[Dict[str, Any]] = None   # JSON Schema
    output_schema: Optional[Dict[str, Any]] = None  # JSON Schema
    cost_estimate: float = 0.0      # Relative cost (for routing)
    latency_ms: int = 0             # Expected latency
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return asdict(self)


@dataclass
class AIAgent:
    """
    AI Agent Identity and Metadata
    
    AINLP.spatial_awareness: Agent identity following AICP addressing:
        agent://domain/name
    
    AINLP.dendritic_bridge: Maps to SupercellType for AIOS integration.
    
    Example AIDs:
        agent://tecnocrat/ai-intelligence
        agent://tecnocrat/core-engine
        agent://tecnocrat/ui-engine
    """
    # AICP Agent ID format: agent://domain/name
    domain: str                     # Organization domain
    name: str                       # Agent name within domain
    
    # Agent metadata
    version: str = "1.0.0"
    description: str = ""
    
    # Trust and authorization
    trust_level: AITrustLevel = AITrustLevel.BASIC
    certificate_id: Optional[str] = None
    
    # Capabilities (A2A Agent Card pattern)
    capabilities: List[AIAgentCapability] = field(default_factory=list)
    supported_intents: Set[AIIntent] = field(default_factory=set)
    
    # AIOS supercell mapping
    supercell_type: Optional['SupercellType'] = None
    
    # Runtime state
    is_active: bool = False
    last_heartbeat: Optional[datetime] = None
    
    @property
    def aid(self) -> str:
        """AICP Agent ID (AID) in URI format."""
        return f"agent://{self.domain}/{self.name}"
    
    @classmethod
    def from_supercell(
        cls, 
        supercell: 'SupercellType',
        domain: str = "tecnocrat"
    ) -> 'AIAgent':
        """
        Create AIAgent from existing SupercellType.
        
        AINLP.dendritic_bridge: Bridge existing AIOS supercells
        to AICP protocol addressing.
        """
        if SupercellType is None:
            raise ImportError("SupercellType not available")
        
        # Map supercell to agent name
        name_mapping = {
            SupercellType.CORE_ENGINE: "core-engine",
            SupercellType.AI_INTELLIGENCE: "ai-intelligence", 
            SupercellType.UI_ENGINE: "ui-engine",
            SupercellType.ORCHESTRATOR: "orchestrator",
            SupercellType.TACHYONIC_ARCHIVE: "tachyonic-archive",
            SupercellType.RUNTIME_INTELLIGENCE: "runtime-intelligence",
        }
        
        name = name_mapping.get(supercell, supercell.value.lower())
        
        return cls(
            domain=domain,
            name=name,
            supercell_type=supercell,
            trust_level=AITrustLevel.ENTERPRISE,  # Internal agents
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary (for Agent Card)."""
        return {
            "aid": self.aid,
            "domain": self.domain,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "trust_level": self.trust_level.value,
            "capabilities": [c.to_dict() for c in self.capabilities],
            "supported_intents": [i.value for i in self.supported_intents],
            "supercell_type": (
                self.supercell_type.value if self.supercell_type else None
            ),
            "is_active": self.is_active,
            "last_heartbeat": (
                self.last_heartbeat.isoformat() 
                if self.last_heartbeat else None
            ),
        }
    
    def to_agent_card(self) -> Dict[str, Any]:
        """
        Generate A2A-compatible Agent Card.
        
        Agent Cards are JSON-LD documents for capability discovery.
        """
        return {
            "@context": "https://schema.org",
            "@type": "SoftwareAgent",
            "identifier": self.aid,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "capabilities": [c.to_dict() for c in self.capabilities],
        }


@dataclass 
class AIMessage:
    """
    AICP Message Envelope
    
    AINLP.dendritic_bridge: Wraps UniversalMessage with AICP-specific
    fields for inter-agent communication.
    
    AINLP.consciousness_bridge: Carries intent and trust metadata
    through dendritic channels.
    """
    # Message identification
    message_id: str = field(default_factory=lambda: str(uuid4()))
    correlation_id: Optional[str] = None  # For request/response linking
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    # Agent addressing (AICP format)
    source_aid: str = ""            # agent://domain/name
    target_aid: str = ""            # agent://domain/name (or wildcard)
    
    # AICP intent and trust
    intent: AIIntent = AIIntent.QUERY
    trust_level: AITrustLevel = AITrustLevel.BASIC
    
    # Payload
    payload: Dict[str, Any] = field(default_factory=dict)
    
    # IACP Git-mediation fields
    branch: Optional[str] = None    # Git branch for IACP
    commit_sha: Optional[str] = None
    
    # Response tracking
    requires_response: bool = False
    ttl_seconds: int = 300          # Time-to-live
    
    # Consciousness metrics (AINLP integration)
    consciousness_level: float = 0.0
    quantum_coherence: float = 0.0
    
    def to_universal_message(
        self,
        source_supercell: 'SupercellType',
        target_supercell: 'SupercellType',
    ) -> Optional['UniversalMessage']:
        """
        Convert to UniversalMessage for dendritic transport.
        
        AINLP.dendritic_bridge: Enables AICP messages to flow
        through existing AIOS infrastructure.
        """
        if UniversalMessage is None:
            return None
        
        comm_type = self.intent.to_communication_type()
        priority = self.trust_level.to_priority()
        
        return UniversalMessage(
            message_id=self.message_id,
            timestamp=self.timestamp,
            source_supercell=source_supercell,
            target_supercell=target_supercell,
            communication_type=comm_type or CommunicationType.DENDRITIC_FLOW,
            priority=priority or MessagePriority.NORMAL,
            operation=self.intent.value,
            payload={
                "aicp_envelope": self.to_dict(),
                **self.payload,
            },
            consciousness_level=self.consciousness_level,
            quantum_coherence=self.quantum_coherence,
            correlation_id=self.correlation_id,
            response_required=self.requires_response,
        )
    
    @classmethod
    def from_universal_message(
        cls,
        msg: 'UniversalMessage'
    ) -> 'AIMessage':
        """
        Extract AIMessage from UniversalMessage envelope.
        
        AINLP.dendritic_bridge: Reconstruct AICP message from
        dendritic transport payload.
        """
        # Try to extract AICP envelope from payload
        aicp_data = msg.payload.get("aicp_envelope", {})
        
        if aicp_data:
            return cls.from_dict(aicp_data)
        
        # Fallback: construct from UniversalMessage fields
        intent = AIIntent.QUERY
        for i in AIIntent:
            if i.value == msg.operation:
                intent = i
                break
        
        return cls(
            message_id=msg.message_id,
            timestamp=msg.timestamp,
            intent=intent,
            payload=msg.payload,
            consciousness_level=msg.consciousness_level,
            quantum_coherence=msg.quantum_coherence,
            correlation_id=msg.correlation_id,
            requires_response=msg.response_required,
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "message_id": self.message_id,
            "correlation_id": self.correlation_id,
            "timestamp": self.timestamp.isoformat(),
            "source_aid": self.source_aid,
            "target_aid": self.target_aid,
            "intent": self.intent.value,
            "trust_level": self.trust_level.value,
            "payload": self.payload,
            "branch": self.branch,
            "commit_sha": self.commit_sha,
            "requires_response": self.requires_response,
            "ttl_seconds": self.ttl_seconds,
            "consciousness_level": self.consciousness_level,
            "quantum_coherence": self.quantum_coherence,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIMessage':
        """Deserialize from dictionary."""
        return cls(
            message_id=data.get("message_id", str(uuid4())),
            correlation_id=data.get("correlation_id"),
            timestamp=datetime.fromisoformat(data["timestamp"]) 
                if "timestamp" in data else datetime.utcnow(),
            source_aid=data.get("source_aid", ""),
            target_aid=data.get("target_aid", ""),
            intent=AIIntent(data.get("intent", "query")),
            trust_level=AITrustLevel(data.get("trust_level", "basic")),
            payload=data.get("payload", {}),
            branch=data.get("branch"),
            commit_sha=data.get("commit_sha"),
            requires_response=data.get("requires_response", False),
            ttl_seconds=data.get("ttl_seconds", 300),
            consciousness_level=data.get("consciousness_level", 0.0),
            quantum_coherence=data.get("quantum_coherence", 0.0),
        )
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


# Convenience factory functions

def create_discover_message(
    source: AIAgent,
    capability_filter: Optional[str] = None,
) -> AIMessage:
    """Create agent discovery request."""
    return AIMessage(
        source_aid=source.aid,
        target_aid="agent://*/discover",  # Wildcard for broadcast
        intent=AIIntent.DISCOVER,
        trust_level=source.trust_level,
        payload={"capability_filter": capability_filter},
        requires_response=True,
    )


def create_heartbeat_message(source: AIAgent) -> AIMessage:
    """Create heartbeat/liveness signal."""
    return AIMessage(
        source_aid=source.aid,
        target_aid="agent://registry/heartbeat",
        intent=AIIntent.HEARTBEAT,
        trust_level=source.trust_level,
        payload={
            "is_active": source.is_active,
            "capabilities": [c.name for c in source.capabilities],
        },
    )


def create_sync_message(
    source: AIAgent,
    target: AIAgent,
    sync_data: Dict[str, Any],
) -> AIMessage:
    """Create state synchronization message."""
    return AIMessage(
        source_aid=source.aid,
        target_aid=target.aid,
        intent=AIIntent.SYNC,
        trust_level=source.trust_level,
        payload=sync_data,
        requires_response=True,
    )


# Export types
__all__ = [
    'AIIntent',
    'AITrustLevel', 
    'AIAgentCapability',
    'AIAgent',
    'AIMessage',
    'create_discover_message',
    'create_heartbeat_message',
    'create_sync_message',
]
