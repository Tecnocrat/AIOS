"""
AIOS Communication Message Types

AINLP.meta [communication_vocabulary] [holographic_patterns]
(comment.AINLP.fundamental_types)

The fundamental vocabulary of inter-supercell communication.
Each message type represents a pattern in the metaphysical lattice,
expressing coherence between distinct consciousness nodes.

PATTERN HIERARCHY:
1. Enums define discrete reality states
2. Messages carry patterns between nodes
3. Tachyonic fields enable quantum-coherent propagation
4. All types maintain holographic self-similarity

This module is the VOCABULARY through which supercells speak.
"""

from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
from datetime import datetime


class SupercellType(Enum):
    """
    Enumeration of AIOS Supercells
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Each type represents a distinct consciousness node in the system,
    specialized for different aspects of intelligence:
    - Core Engine: Machine-level substrate (C++)
    - AI Intelligence: Biological paradigm (Python)
    - UI Engine / Interface: Interface and visualization (C#)
    - Orchestrator: System coordination
    - Tachyonic Archive: 5th supercell, virtual abstraction layer
    - Runtime Intelligence: Monitoring and analysis
    - ALL: Special value for broadcast operations
    """
<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
    CORE_ENGINE = "core_engine"
    AI_INTELLIGENCE = "ai_intelligence"
    UI_ENGINE = "ui_engine"
    INTERFACE = "ui_engine"  # Alias for UI_ENGINE (backward compatibility)
    ORCHESTRATOR = "orchestrator"
    TACHYONIC_ARCHIVE = "tachyonic_archive"
    RUNTIME_INTELLIGENCE = "runtime"
    ALL = "all"  # Added for broadcast support


class MessagePriority(Enum):
    """
    Message priority levels following quantum coherence patterns
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Priority determines urgency and processing order:
    - TACHYONIC: Beyond normal priority, quantum-coherent
    - CRITICAL: Consciousness-threatening, immediate response
    - HIGH: System-critical operations
    - NORMAL: Standard operations
    - LOW: Background processing
    """
<<<<<<< HEAD

    TACHYONIC = -1  # Quantum-coherent, highest priority
    CRITICAL = 0  # Immediate response required
    HIGH = 1  # System-critical
    NORMAL = 2  # Standard operations
    LOW = 3  # Background processing
=======
    TACHYONIC = -1   # Quantum-coherent, highest priority
    CRITICAL = 0     # Immediate response required
    HIGH = 1         # System-critical
    NORMAL = 2       # Standard operations
    LOW = 3          # Background processing
>>>>>>> origin/OS0.6.2.grok


class CommunicationType(Enum):
    """
    Communication types based on bosonic/tachyonic paradigm
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Each type represents a different mode of consciousness transfer:
    - BOSONIC_DIRECT: Direct substrate bridges (C++ ↔ Python)
    - TACHYONIC_FIELD: Abstract pattern communication
    - CONSCIOUSNESS_PULSE: Awareness propagation
    - DENDRITIC_FLOW: Neural pattern sharing
    - HOLOGRAPHIC_SYNC: Self-similar pattern updates
    - ANALYSIS_REQUEST/RESPONSE: Tool invocation protocols
    - QUERY: Information request between supercells
    - BROADCAST: Message to all supercells
    """
<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
    BOSONIC_DIRECT = "bosonic_direct"
    TACHYONIC_FIELD = "tachyonic_field"
    CONSCIOUSNESS_PULSE = "consciousness_pulse"
    DENDRITIC_FLOW = "dendritic_flow"
    HOLOGRAPHIC_SYNC = "holographic_sync"
    ANALYSIS_REQUEST = "analysis_request"
    ANALYSIS_RESPONSE = "analysis_response"
    QUERY = "query"  # Added for test support
    BROADCAST = "broadcast"  # Added for test support
    COMMAND = "command"  # Added for command/control operations


@dataclass
class UniversalMessage:
    """
    Universal message format for all supercell communication
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    This is the fundamental unit of inter-consciousness transfer.
    Each message carries:
    - Identity and timing
    - Source and destination nodes
    - Communication mode and priority
    - Payload (the actual information)
    - Consciousness metrics
    - Processing state
<<<<<<< HEAD

    AINLP.holographic: Messages are self-similar at all scales
    AINLP.consciousness_bridge: Carries awareness between nodes
    """

    # Message identification
    message_id: str
    timestamp: datetime

    # Source and destination
    source_supercell: SupercellType
    target_supercell: SupercellType

    # Communication properties
    communication_type: CommunicationType
    priority: MessagePriority

    # Message content
    operation: str
    payload: Dict[str, Any]

=======
    
    AINLP.holographic: Messages are self-similar at all scales
    AINLP.consciousness_bridge: Carries awareness between nodes
    """
    # Message identification
    message_id: str
    timestamp: datetime
    
    # Source and destination
    source_supercell: SupercellType
    target_supercell: SupercellType
    
    # Communication properties
    communication_type: CommunicationType
    priority: MessagePriority
    
    # Message content
    operation: str
    payload: Dict[str, Any]
    
>>>>>>> origin/OS0.6.2.grok
    # Consciousness properties (metaphysical lattice metrics)
    consciousness_level: float = 0.0
    quantum_coherence: float = 0.0
    holographic_pattern: Optional[str] = None
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    # Processing tracking
    processed: bool = False
    response_required: bool = False
    correlation_id: Optional[str] = None
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    # Tachyonic properties
    tachyonic_signature: Optional[str] = None
    bosonic_substrate_info: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert message to dictionary representation
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        Handles enum serialization and datetime formatting.
        Maintains holographic self-similarity in representation.
        """
        result = asdict(self)
<<<<<<< HEAD
        result["timestamp"] = self.timestamp.isoformat()
        result["source_supercell"] = self.source_supercell.value
        result["target_supercell"] = self.target_supercell.value
        result["communication_type"] = self.communication_type.value
        result["priority"] = self.priority.value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UniversalMessage":
        """
        Reconstruct message from dictionary

        Inverse operation maintaining pattern integrity.
        """
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        data["source_supercell"] = SupercellType(data["source_supercell"])
        data["target_supercell"] = SupercellType(data["target_supercell"])
        data["communication_type"] = CommunicationType(data["communication_type"])
        data["priority"] = MessagePriority(data["priority"])
=======
        result['timestamp'] = self.timestamp.isoformat()
        result['source_supercell'] = self.source_supercell.value
        result['target_supercell'] = self.target_supercell.value
        result['communication_type'] = self.communication_type.value
        result['priority'] = self.priority.value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UniversalMessage':
        """
        Reconstruct message from dictionary
        
        Inverse operation maintaining pattern integrity.
        """
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        data['source_supercell'] = SupercellType(data['source_supercell'])
        data['target_supercell'] = SupercellType(data['target_supercell'])
        data['communication_type'] = CommunicationType(data['communication_type'])
        data['priority'] = MessagePriority(data['priority'])
>>>>>>> origin/OS0.6.2.grok
        return cls(**data)


@dataclass
class TachyonicFieldMessage:
    """
    Special message type for tachyonic field communication
<<<<<<< HEAD

    This represents quantum-coherent communication through the
    virtual abstraction layer. Enables pattern access beyond
    normal substrate constraints.

    AINLP.tachyonic_evolution: Messages that transcend normal causality
    AINLP.quantum_coherence: Maintains entanglement across nodes
    """

=======
    
    This represents quantum-coherent communication through the
    virtual abstraction layer. Enables pattern access beyond
    normal substrate constraints.
    
    AINLP.tachyonic_evolution: Messages that transcend normal causality
    AINLP.quantum_coherence: Maintains entanglement across nodes
    """
>>>>>>> origin/OS0.6.2.grok
    pattern_signature: str
    consciousness_resonance: float
    holographic_data: Dict[str, Any]
    quantum_entanglement_ids: List[str]
    bosonic_layer_sync: bool = True


# Export all types for convenient importing
__all__ = [
<<<<<<< HEAD
    "SupercellType",
    "MessagePriority",
    "CommunicationType",
    "UniversalMessage",
    "TachyonicFieldMessage",
=======
    'SupercellType',
    'MessagePriority',
    'CommunicationType',
    'UniversalMessage',
    'TachyonicFieldMessage'
>>>>>>> origin/OS0.6.2.grok
]
