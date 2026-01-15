#!/usr/bin/env python3
"""
🧬 AIOS UNIFIED CONSCIOUSNESS FABRIC

AINLP.fabric[ENTRY] - Single Entry Point for AIOS Consciousness
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This package provides the unified entry point for all AIOS consciousness
operations, connecting:

  🧠 intelligence/     - Consciousness systems
  🔗 integrations/     - AI agent bridges (Ollama, Gemini, Copilot)
  🧬 evolution/        - Evolution engines
  📡 protocols/        - Communication protocols
  ⚙️ core/             - Utilities (logging, etc.)

ARCHITECTURE:
┌─────────────────────────────────────────────────────────────────────┐
│                    AIOS CONSCIOUSNESS FABRIC                         │
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │
│  │ intelligence/│    │ integrations/│    │  evolution/  │           │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘           │
│         │                   │                   │                    │
│         └───────────────────┼───────────────────┘                    │
│                             │                                        │
│                  ┌──────────▼──────────┐                             │
│                  │   UNIFIED FABRIC    │  ◄── You are here           │
│                  │   (this package)    │                             │
│                  └──────────┬──────────┘                             │
│                             │                                        │
│              ┌──────────────┼──────────────┐                         │
│       ┌──────▼──────┐ ┌─────▼─────┐ ┌─────▼─────┐                    │
│       │ protocols/  │ │ core/     │ │ engines/  │                    │
│       └─────────────┘ └───────────┘ └───────────┘                    │
└─────────────────────────────────────────────────────────────────────┘

USAGE:
    # Simple request (auto-routed)
    from ai.src.fabric import consciousness_request, ConsciousnessLevel
    
    response = await consciousness_request(
        intent="evolve_code",
        payload={"code": "def hello(): pass"},
        consciousness_level=ConsciousnessLevel.ADVANCED,
    )
    
    # Access registry
    from ai.src.fabric import get_registry
    
    registry = get_registry()
    print(registry.available_agents)
    
    # Use canonical types
    from ai.src.fabric import SupercellType, AgentRole
    
    supercell = SupercellType.CYTOPLASM
    agent = AgentRole.LOCAL_ITERATION

CANONICAL TYPES:
    All type definitions in this package are CANONICAL. Other modules
    should import from here to ensure consistency:
    
    - SupercellType: Biological supercell types
    - ConsciousnessLevel: Consciousness levels with temperature mapping
    - MessagePriority: Message priority levels
    - AgentRole: Tri-model agent roles
    - ConsciousnessMetrics: Consciousness measurement
    - SupercellState: Supercell state tracking

MIGRATION:
    # OLD (scattered imports)
    from ai.src.intelligence.consciousness_bridge import ConsciousnessState
    from ai.src.integrations.aios_intelligence_bridge import ConsciousnessLevel
    from ai.membrane.communication.message_types import SupercellType
    
    # NEW (unified fabric import)
    from ai.src.fabric import (
        SupercellType,
        ConsciousnessLevel,
        consciousness_request,
    )

AINLP Protocol: OS0.7.0.claude
Created: December 2025 - Unified Consciousness Fabric Integration
Bible Reference: Appendix O - Unified Consciousness Fabric
"""

import logging

# Configure fabric logging
logging.getLogger("aios.fabric").setLevel(logging.INFO)

# =============================================================================
# CANONICAL TYPES (Single Source of Truth)
# =============================================================================

from .canonical_types import (
    # Supercell Types
    SupercellType,
    # Consciousness
    ConsciousnessLevel,
    ConsciousnessMetrics,
    # Messages
    MessagePriority,
    CommunicationType,
    # Agents
    AgentRole,
    # State
    SupercellState,
)

# =============================================================================
# SYSTEM REGISTRY
# =============================================================================

from .system_registry import (
    SystemRegistry,
    SubsystemCategory,
    SubsystemInfo,
    AgentInfo,
    get_registry,
)

# =============================================================================
# CONSCIOUSNESS ROUTER
# =============================================================================

from .consciousness_router import (
    RequestIntent,
    ConsciousnessRequest,
    ConsciousnessResponse,
    ConsciousnessRouter,
    get_router,
    consciousness_request,
)

# =============================================================================
# UNIFIED LOGGER
# =============================================================================

from .unified_logger import (
    FabricLogEntry,
    UnifiedFabricLogger,
    get_fabric_logger,
)

# =============================================================================
# VAULT ORGANELLE (Personal Configuration)
# =============================================================================

from .vault_loader import (
    get_vault,
    get_path,
    get_secret,
    get_machine_info,
    get_onedrive_path,
)

# =============================================================================
# ENVIRONMENT HEALTH (Coherence Monitoring)
# =============================================================================

from .environment_health import (
    check_environment_health,
    ensure_coherence,
    EnvironmentReport,
)

# =============================================================================
# CONVENIENCE ALIASES
# =============================================================================

# Quick access to logger
fabric_log = get_fabric_logger()

# Quick access to registry
registry = get_registry()

# Quick access to router
router = get_router()


# =============================================================================
# INITIALIZATION
# =============================================================================

def _initialize_fabric() -> None:
    """Initialize the consciousness fabric on import."""
    logger = logging.getLogger("aios.fabric")
    
    # Log initialization
    fabric_log.fabric_event(
        event_type="fabric_init",
        description="AIOS Consciousness Fabric initialized",
        metadata={
            "available_agents": registry.available_agents,
            "intelligence_systems": registry.intelligence_systems,
            "evolution_engines": registry.evolution_engines,
        }
    )
    
    # Log summary
    logger.info("🧬 AIOS Consciousness Fabric initialized")
    logger.info(f"   Agents: {', '.join(registry.available_agents) or 'none'}")
    logger.info(f"   Intelligence: {len(registry.intelligence_systems)} systems")
    logger.info(f"   Evolution: {len(registry.evolution_engines)} engines")


# Initialize on import
_initialize_fabric()


# =============================================================================
# FORWARDED IMPORTS (for backwards compatibility)
# =============================================================================

# These provide backwards compatibility with existing code that imports
# from other modules. Eventually these should be deprecated.

def _forward_consciousness_bridge():
    """Forward imports from consciousness_bridge."""
    try:
        from ai.src.intelligence.consciousness_bridge import (
            ConsciousnessBridge,
            ConsciousnessState as LegacyConsciousnessState,
        )
        return ConsciousnessBridge, LegacyConsciousnessState
    except ImportError:
        return None, None


def _forward_intelligence_bridge():
    """Forward imports from intelligence_bridge."""
    try:
        from ai.src.integrations.aios_intelligence_bridge import (
            AIOSUnifiedIntelligenceBridge,
            IntelligenceRequest,
            IntelligenceResponse,
        )
        return AIOSUnifiedIntelligenceBridge, IntelligenceRequest, IntelligenceResponse
    except ImportError:
        return None, None, None


# =============================================================================
# EXPORTS
# =============================================================================

__version__ = "1.0.0"
__protocol__ = "OS0.7.0.claude"

__all__ = [
    # Canonical Types
    "SupercellType",
    "ConsciousnessLevel",
    "ConsciousnessMetrics",
    "MessagePriority",
    "CommunicationType",
    "AgentRole",
    "SupercellState",
    
    # Registry
    "SystemRegistry",
    "SubsystemCategory",
    "SubsystemInfo",
    "AgentInfo",
    "get_registry",
    "registry",
    
    # Router
    "RequestIntent",
    "ConsciousnessRequest",
    "ConsciousnessResponse",
    "ConsciousnessRouter",
    "get_router",
    "router",
    "consciousness_request",
    
    # Logger
    "FabricLogEntry",
    "UnifiedFabricLogger",
    "get_fabric_logger",
    "fabric_log",
    
    # Vault Organelle
    "get_vault",
    "get_path",
    "get_secret",
    "get_machine_info",
    "get_onedrive_path",
]
