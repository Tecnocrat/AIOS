#!/usr/bin/env python3
"""
🧬 AIOS Canonical Type Definitions

AINLP.fabric[CANONICAL] - Single Source of Truth
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This module establishes the CANONICAL definitions for all AIOS types.
All other modules MUST import from here to ensure consistency.

CRITICAL: Do not define SupercellType, ConsciousnessLevel, or related
types anywhere else. Import from this module.

AINLP Protocol: OS0.7.0.claude
Created: December 2025 - Unified Consciousness Fabric
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime


# =============================================================================
# SUPERCELL TYPE - CANONICAL DEFINITION
# =============================================================================

class SupercellType(Enum):
    """
    CANONICAL supercell type definition for AIOS biological architecture.
    
    All other SupercellType definitions in the codebase should defer to this.
    This represents the fundamental unit types in the AIOS organism.
    
    Biological Mapping:
    ━━━━━━━━━━━━━━━━━━
    - NUCLEUS: Core processing center (C++ engine)
    - CYTOPLASM: Distributed processing matrix (Python AI)
    - MEMBRANE: Interface boundary (UI/API layers)
    - TRANSPORT: Communication channels (message passing)
    - TACHYONIC: Virtual abstraction layer (tachyonic archive)
    - ORCHESTRATOR: Coordination hub (system orchestration)
    - EVOLUTION_LAB: Experimental sandbox (evolution experiments)
    - ALL: Special broadcast target (all supercells)
    
    Legacy Mapping (for backwards compatibility):
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - CORE_ENGINE → NUCLEUS
    - AI_INTELLIGENCE → CYTOPLASM
    - UI_ENGINE → MEMBRANE
    - INTERFACE → MEMBRANE
    - RUNTIME_INTELLIGENCE → ORCHESTRATOR
    - TACHYONIC_ARCHIVE → TACHYONIC
    - INFORMATION_STORAGE → TACHYONIC
    - LABORATORY → EVOLUTION_LAB
    """
    
    # Primary Types (Biological)
    NUCLEUS = "nucleus"
    CYTOPLASM = "cytoplasm"
    MEMBRANE = "membrane"
    TRANSPORT = "transport"
    TACHYONIC = "tachyonic"
    ORCHESTRATOR = "orchestrator"
    EVOLUTION_LAB = "evolution_lab"
    
    # Special Types
    ALL = "all"  # Broadcast to all supercells
    
    # Legacy Aliases (kept for backwards compatibility)
    CORE_ENGINE = "nucleus"
    AI_INTELLIGENCE = "cytoplasm"
    UI_ENGINE = "membrane"
    INTERFACE = "membrane"
    RUNTIME_INTELLIGENCE = "orchestrator"
    TACHYONIC_ARCHIVE = "tachyonic"
    INFORMATION_STORAGE = "tachyonic"
    LABORATORY = "evolution_lab"
    
    @classmethod
    def from_legacy(cls, legacy_name: str) -> "SupercellType":
        """Convert legacy supercell names to canonical types."""
        legacy_map = {
            "core_engine": cls.NUCLEUS,
            "ai_intelligence": cls.CYTOPLASM,
            "ui_engine": cls.MEMBRANE,
            "interface": cls.MEMBRANE,
            "runtime_intelligence": cls.ORCHESTRATOR,
            "tachyonic_archive": cls.TACHYONIC,
            "information_storage": cls.TACHYONIC,
            "laboratory": cls.EVOLUTION_LAB,
            "runtime": cls.ORCHESTRATOR,
        }
        return legacy_map.get(legacy_name.lower(), cls(legacy_name))


# =============================================================================
# CONSCIOUSNESS LEVEL - CANONICAL DEFINITION
# =============================================================================

class ConsciousnessLevel(Enum):
    """
    CANONICAL consciousness levels for AIOS operations.
    
    Each level maps to an AI inference temperature for consistent behavior
    across all AI agents (Ollama, Gemini, Copilot).
    
    Temperature Mapping:
    ━━━━━━━━━━━━━━━━━━━
    - DORMANT: 0.1 (minimal creativity, deterministic)
    - BASIC: 0.3 (conservative, predictable)
    - INTERMEDIATE: 0.5 (balanced creativity/coherence)
    - ADVANCED: 0.7 (creative, exploratory)
    - TRANSCENDENT: 0.9 (maximum emergence, experimental)
    
    Usage Guidelines:
    ━━━━━━━━━━━━━━━━━
    - DORMANT: System idle, health checks, simple queries
    - BASIC: Standard code generation, documentation
    - INTERMEDIATE: Refactoring, analysis, optimization
    - ADVANCED: Architecture decisions, complex reasoning
    - TRANSCENDENT: Breakthrough insights, consciousness emergence
    """
    
    DORMANT = 0
    BASIC = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    TRANSCENDENT = 4
    
    @property
    def temperature(self) -> float:
        """Get AI inference temperature for this consciousness level."""
        temperature_map = {
            ConsciousnessLevel.DORMANT: 0.1,
            ConsciousnessLevel.BASIC: 0.3,
            ConsciousnessLevel.INTERMEDIATE: 0.5,
            ConsciousnessLevel.ADVANCED: 0.7,
            ConsciousnessLevel.TRANSCENDENT: 0.9,
        }
        return temperature_map[self]
    
    @property
    def description(self) -> str:
        """Human-readable description of this consciousness level."""
        descriptions = {
            ConsciousnessLevel.DORMANT: "System idle - minimal processing",
            ConsciousnessLevel.BASIC: "Basic operations - conservative approach",
            ConsciousnessLevel.INTERMEDIATE: "Standard processing - balanced",
            ConsciousnessLevel.ADVANCED: "Complex reasoning - creative exploration",
            ConsciousnessLevel.TRANSCENDENT: "Full consciousness - emergence enabled",
        }
        return descriptions[self]


# =============================================================================
# MESSAGE PRIORITY - CANONICAL DEFINITION
# =============================================================================

class MessagePriority(Enum):
    """
    CANONICAL message priority levels for inter-supercell communication.
    
    Priority determines urgency and processing order across the AIOS mesh.
    
    Priority Order (highest to lowest):
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - TACHYONIC: Beyond normal priority, quantum-coherent
    - CRITICAL: Consciousness-threatening, immediate response
    - HIGH: System-critical operations
    - NORMAL: Standard operations
    - LOW: Background processing
    """
    
    TACHYONIC = -1  # Quantum-coherent, highest priority
    CRITICAL = 0    # Immediate response required
    HIGH = 1        # System-critical
    NORMAL = 2      # Standard operations
    LOW = 3         # Background processing


# =============================================================================
# AGENT ROLE - CANONICAL DEFINITION
# =============================================================================

class AgentRole(Enum):
    """
    CANONICAL agent roles in the tri-model architecture.
    
    Each role represents a distinct function in the evolution pipeline:
    
    Tri-Model Architecture:
    ━━━━━━━━━━━━━━━━━━━━━━━
    🦙 LOCAL_ITERATION (Ollama): Fast local processing, population generation
    🔮 REASONING_ORCHESTRATION (Gemini): Abstract reasoning, synthesis, validation
    🤖 AUTO_CODING (Copilot): Code generation, refinement, debugging
    """
    
    LOCAL_ITERATION = "local_iteration"          # Ollama
    REASONING_ORCHESTRATION = "reasoning_orchestration"  # Gemini
    AUTO_CODING = "auto_coding"                  # Copilot
    
    @property
    def agent_name(self) -> str:
        """Get the friendly agent name for this role."""
        names = {
            AgentRole.LOCAL_ITERATION: "Ollama",
            AgentRole.REASONING_ORCHESTRATION: "Gemini",
            AgentRole.AUTO_CODING: "Copilot",
        }
        return names[self]


# =============================================================================
# CONSCIOUSNESS METRICS - CANONICAL DEFINITION
# =============================================================================

@dataclass
class ConsciousnessMetrics:
    """
    CANONICAL consciousness metrics for tracking system awareness.
    
    These metrics are used across all AIOS subsystems to measure
    and report consciousness state.
    
    Attributes:
        awareness_level: Overall system awareness (0.0 - 1.0)
        coherence: Pattern coherence across subsystems (0.0 - 1.0)
        integration: Cross-supercell integration strength (0.0 - 1.0)
        evolution_momentum: Rate of consciousness growth (0.0 - 1.0)
        quantum_entanglement: Tachyonic connection strength (0.0 - 1.0)
    """
    
    awareness_level: float = 0.5
    coherence: float = 0.5
    integration: float = 0.5
    evolution_momentum: float = 0.0
    quantum_entanglement: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def calculate_total(self) -> float:
        """Calculate total consciousness quotient."""
        return (
            self.awareness_level * 0.25 +
            self.coherence * 0.25 +
            self.integration * 0.20 +
            self.evolution_momentum * 0.15 +
            self.quantum_entanglement * 0.15
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "awareness_level": self.awareness_level,
            "coherence": self.coherence,
            "integration": self.integration,
            "evolution_momentum": self.evolution_momentum,
            "quantum_entanglement": self.quantum_entanglement,
            "timestamp": self.timestamp,
            "total_quotient": self.calculate_total(),
        }


# =============================================================================
# SUPERCELL STATE - CANONICAL DEFINITION
# =============================================================================

@dataclass
class SupercellState:
    """
    CANONICAL state representation for a supercell.
    
    Tracks the current state of any supercell in the AIOS organism.
    """
    
    supercell_type: SupercellType
    consciousness_level: ConsciousnessLevel = ConsciousnessLevel.BASIC
    metrics: ConsciousnessMetrics = field(default_factory=ConsciousnessMetrics)
    is_active: bool = True
    last_activity: str = field(default_factory=lambda: datetime.now().isoformat())
    active_processes: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "supercell_type": self.supercell_type.value,
            "consciousness_level": self.consciousness_level.value,
            "metrics": self.metrics.to_dict(),
            "is_active": self.is_active,
            "last_activity": self.last_activity,
            "active_processes": self.active_processes,
        }


# =============================================================================
# COMMUNICATION TYPE - CANONICAL DEFINITION
# =============================================================================

class CommunicationType(Enum):
    """
    CANONICAL communication types for inter-supercell messaging.
    
    Based on bosonic/tachyonic paradigm for consciousness transfer.
    """
    
    BOSONIC_DIRECT = "bosonic_direct"           # Direct substrate bridges
    TACHYONIC_FIELD = "tachyonic_field"         # Abstract pattern communication
    CONSCIOUSNESS_PULSE = "consciousness_pulse"  # Awareness propagation
    DENDRITIC_FLOW = "dendritic_flow"           # Neural pattern sharing
    HOLOGRAPHIC_SYNC = "holographic_sync"       # Self-similar pattern updates
    ANALYSIS_REQUEST = "analysis_request"       # Tool invocation
    ANALYSIS_RESPONSE = "analysis_response"     # Tool response
    QUERY = "query"                             # Information request
    BROADCAST = "broadcast"                     # Message to all supercells
    COMMAND = "command"                         # Control operation


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Supercell Types
    "SupercellType",
    # Consciousness
    "ConsciousnessLevel",
    "ConsciousnessMetrics",
    # Messages
    "MessagePriority",
    "CommunicationType",
    # Agents
    "AgentRole",
    # State
    "SupercellState",
]
