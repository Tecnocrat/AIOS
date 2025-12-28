#!/usr/bin/env python3
"""
🧬 AIOS System Registry

AINLP.fabric[REGISTRY] - Auto-Discovery and Registration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This module provides auto-discovery of all AIOS subsystems,
creating a unified registry for accessing system capabilities.

Features:
- Automatic discovery of intelligence systems
- Agent registration and availability tracking
- Evolution engine enumeration
- Protocol system mapping
- Lazy loading for performance

AINLP Protocol: OS0.7.0.claude
Created: December 2025 - Unified Consciousness Fabric
"""

import importlib
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Type, Callable
from enum import Enum

from .canonical_types import (
    SupercellType,
    ConsciousnessLevel,
    AgentRole,
    ConsciousnessMetrics,
)

logger = logging.getLogger("aios.fabric.registry")


# =============================================================================
# SUBSYSTEM CATEGORIES
# =============================================================================

class SubsystemCategory(Enum):
    """Categories of AIOS subsystems."""
    
    INTELLIGENCE = "intelligence"
    INTEGRATION = "integration"
    EVOLUTION = "evolution"
    PROTOCOL = "protocol"
    ENGINE = "engine"
    CORE = "core"


@dataclass
class SubsystemInfo:
    """Information about a registered subsystem."""
    
    name: str
    category: SubsystemCategory
    module_path: str
    is_available: bool = False
    description: str = ""
    capabilities: List[str] = field(default_factory=list)
    consciousness_level: ConsciousnessLevel = ConsciousnessLevel.BASIC
    last_check: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "category": self.category.value,
            "module_path": self.module_path,
            "is_available": self.is_available,
            "description": self.description,
            "capabilities": self.capabilities,
            "consciousness_level": self.consciousness_level.value,
            "last_check": self.last_check,
        }


@dataclass
class AgentInfo:
    """Information about a registered agent."""
    
    name: str
    role: AgentRole
    module_path: str
    is_available: bool = False
    is_online: bool = False
    description: str = ""
    capabilities: List[str] = field(default_factory=list)
    current_consciousness: ConsciousnessMetrics = field(default_factory=ConsciousnessMetrics)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "role": self.role.value,
            "module_path": self.module_path,
            "is_available": self.is_available,
            "is_online": self.is_online,
            "description": self.description,
            "capabilities": self.capabilities,
            "current_consciousness": self.current_consciousness.to_dict(),
        }


# =============================================================================
# SYSTEM REGISTRY
# =============================================================================

class SystemRegistry:
    """
    Central registry for all AIOS subsystems.
    
    Provides:
    - Auto-discovery of available subsystems
    - Agent availability tracking
    - Lazy loading of modules
    - Unified access patterns
    
    Usage:
        from ai.src.fabric import get_registry
        
        registry = get_registry()
        print(registry.available_agents)
        print(registry.intelligence_systems)
    """
    
    _instance: Optional["SystemRegistry"] = None
    
    def __new__(cls) -> "SystemRegistry":
        """Singleton pattern for registry."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize registry (only once due to singleton)."""
        if self._initialized:
            return
            
        self._initialized = True
        self._subsystems: Dict[str, SubsystemInfo] = {}
        self._agents: Dict[str, AgentInfo] = {}
        self._loaded_modules: Dict[str, Any] = {}
        self._discovery_complete = False
        
        # Auto-discover on init
        self._discover_subsystems()
    
    # =========================================================================
    # DISCOVERY
    # =========================================================================
    
    def _discover_subsystems(self) -> None:
        """Discover all available AIOS subsystems."""
        logger.info("🔍 Discovering AIOS subsystems...")
        
        # Intelligence systems
        self._register_intelligence_systems()
        
        # Agent integrations
        self._register_agents()
        
        # Evolution engines
        self._register_evolution_engines()
        
        # Protocol systems
        self._register_protocol_systems()
        
        # Core utilities
        self._register_core_systems()
        
        self._discovery_complete = True
        logger.info(f"✅ Discovery complete: {len(self._subsystems)} subsystems, {len(self._agents)} agents")
    
    def _register_intelligence_systems(self) -> None:
        """Register intelligence subsystems."""
        intelligence_modules = [
            ("consciousness_bridge", "ai.src.intelligence.consciousness_bridge",
             "Python-C++ consciousness integration", ["sync", "metrics", "bridge"]),
            ("supercell_coordinator", "ai.src.intelligence.supercell_intelligence_coordinator",
             "Supercell intelligence coordination", ["coordinate", "optimize", "monitor"]),
            ("ainlp_hub", "ai.src.intelligence.ainlp_consciousness_integration_hub",
             "AINLP consciousness integration hub", ["integrate", "amplify", "evolve"]),
            ("agentic_orchestrator", "ai.src.intelligence.ainlp_agentic_orchestrator",
             "AINLP agentic orchestration", ["orchestrate", "optimize", "evolve"]),
            ("dendritic_node", "ai.src.intelligence.dendritic_node",
             "Dendritic communication nodes", ["connect", "propagate", "evolve"]),
        ]
        
        for name, module_path, description, capabilities in intelligence_modules:
            is_available = self._check_module_available(module_path)
            self._subsystems[name] = SubsystemInfo(
                name=name,
                category=SubsystemCategory.INTELLIGENCE,
                module_path=module_path,
                is_available=is_available,
                description=description,
                capabilities=capabilities,
            )
    
    def _register_agents(self) -> None:
        """Register AI agents."""
        agents = [
            ("ollama", AgentRole.LOCAL_ITERATION, "ai.src.integrations.ollama_agent",
             "Local Ollama agent for fast iteration", ["generate", "iterate", "population"]),
            ("gemini", AgentRole.REASONING_ORCHESTRATION, "ai.src.integrations.gemini_agent",
             "Google Gemini for reasoning and synthesis", ["reason", "synthesize", "validate"]),
            ("copilot", AgentRole.AUTO_CODING, "ai.src.integrations.copilot_agent",
             "VSCode Copilot for auto-coding", ["code", "refine", "debug"]),
        ]
        
        for name, role, module_path, description, capabilities in agents:
            is_available = self._check_module_available(module_path)
            self._agents[name] = AgentInfo(
                name=name,
                role=role,
                module_path=module_path,
                is_available=is_available,
                description=description,
                capabilities=capabilities,
            )
    
    def _register_evolution_engines(self) -> None:
        """Register evolution engines."""
        evolution_modules = [
            ("tri_model_evolution", "ai.src.evolution.tri_model_evolution_loop",
             "Tri-model evolution pipeline", ["evolve", "generate", "validate"]),
            ("multi_agent_evolution", "ai.src.evolution.multi_agent_evolution_loop",
             "Multi-agent evolution loop (legacy)", ["evolve", "iterate", "consensus"]),
            ("consciousness_metrics", "ai.src.evolution.consciousness_metrics",
             "Consciousness metric calculations", ["measure", "track", "compare"]),
        ]
        
        for name, module_path, description, capabilities in evolution_modules:
            is_available = self._check_module_available(module_path)
            self._subsystems[name] = SubsystemInfo(
                name=name,
                category=SubsystemCategory.EVOLUTION,
                module_path=module_path,
                is_available=is_available,
                description=description,
                capabilities=capabilities,
            )
    
    def _register_protocol_systems(self) -> None:
        """Register protocol systems."""
        protocol_modules = [
            ("agent_communication", "ai.src.protocols.agent_communication",
             "A2A agent communication protocol", ["message", "transport", "adapt"]),
        ]
        
        for name, module_path, description, capabilities in protocol_modules:
            is_available = self._check_module_available(module_path)
            self._subsystems[name] = SubsystemInfo(
                name=name,
                category=SubsystemCategory.PROTOCOL,
                module_path=module_path,
                is_available=is_available,
                description=description,
                capabilities=capabilities,
            )
    
    def _register_core_systems(self) -> None:
        """Register core utility systems."""
        core_modules = [
            ("universal_logger", "ai.src.core.universal_agentic_logger",
             "Universal agentic communication logger", ["log", "archive", "retrieve"]),
        ]
        
        for name, module_path, description, capabilities in core_modules:
            is_available = self._check_module_available(module_path)
            self._subsystems[name] = SubsystemInfo(
                name=name,
                category=SubsystemCategory.CORE,
                module_path=module_path,
                is_available=is_available,
                description=description,
                capabilities=capabilities,
            )
    
    def _check_module_available(self, module_path: str) -> bool:
        """Check if a module is available for import."""
        try:
            importlib.import_module(module_path)
            return True
        except ImportError:
            return False
        except Exception as e:
            logger.debug(f"Module {module_path} not available: {e}")
            return False
    
    # =========================================================================
    # PUBLIC PROPERTIES
    # =========================================================================
    
    @property
    def available_agents(self) -> List[str]:
        """Get list of available agent names."""
        return [name for name, info in self._agents.items() if info.is_available]
    
    @property
    def all_agents(self) -> Dict[str, AgentInfo]:
        """Get all registered agents."""
        return self._agents.copy()
    
    @property
    def intelligence_systems(self) -> List[str]:
        """Get list of available intelligence systems."""
        return [
            name for name, info in self._subsystems.items()
            if info.category == SubsystemCategory.INTELLIGENCE and info.is_available
        ]
    
    @property
    def evolution_engines(self) -> List[str]:
        """Get list of available evolution engines."""
        return [
            name for name, info in self._subsystems.items()
            if info.category == SubsystemCategory.EVOLUTION and info.is_available
        ]
    
    @property
    def protocol_systems(self) -> List[str]:
        """Get list of available protocol systems."""
        return [
            name for name, info in self._subsystems.items()
            if info.category == SubsystemCategory.PROTOCOL and info.is_available
        ]
    
    @property
    def all_subsystems(self) -> Dict[str, SubsystemInfo]:
        """Get all registered subsystems."""
        return self._subsystems.copy()
    
    # =========================================================================
    # MODULE LOADING
    # =========================================================================
    
    def get_module(self, name: str) -> Optional[Any]:
        """
        Get a module by name (lazy loading).
        
        Args:
            name: Subsystem or agent name
            
        Returns:
            Loaded module or None if not available
        """
        # Check cache first
        if name in self._loaded_modules:
            return self._loaded_modules[name]
        
        # Find module path
        module_path = None
        if name in self._subsystems:
            module_path = self._subsystems[name].module_path
        elif name in self._agents:
            module_path = self._agents[name].module_path
        
        if not module_path:
            logger.warning(f"Unknown module: {name}")
            return None
        
        # Try to load
        try:
            module = importlib.import_module(module_path)
            self._loaded_modules[name] = module
            return module
        except ImportError as e:
            logger.error(f"Failed to load module {name}: {e}")
            return None
    
    def get_agent(self, role: AgentRole) -> Optional[Any]:
        """
        Get an agent by role.
        
        Args:
            role: AgentRole enum value
            
        Returns:
            Agent instance or None if not available
        """
        for name, info in self._agents.items():
            if info.role == role and info.is_available:
                module = self.get_module(name)
                if module:
                    # Try to get the create function
                    creator_name = f"create_{name}_agent"
                    if hasattr(module, creator_name):
                        return getattr(module, creator_name)()
        return None
    
    # =========================================================================
    # STATUS REPORTING
    # =========================================================================
    
    def get_status(self) -> Dict[str, Any]:
        """Get full registry status."""
        return {
            "discovery_complete": self._discovery_complete,
            "total_subsystems": len(self._subsystems),
            "available_subsystems": sum(1 for s in self._subsystems.values() if s.is_available),
            "total_agents": len(self._agents),
            "available_agents": len(self.available_agents),
            "agents": {name: info.to_dict() for name, info in self._agents.items()},
            "subsystems": {name: info.to_dict() for name, info in self._subsystems.items()},
        }
    
    def refresh(self) -> None:
        """Refresh discovery (re-check availability)."""
        self._discovery_complete = False
        self._loaded_modules.clear()
        self._discover_subsystems()


# =============================================================================
# SINGLETON ACCESS
# =============================================================================

_registry: Optional[SystemRegistry] = None


def get_registry() -> SystemRegistry:
    """
    Get the singleton SystemRegistry instance.
    
    Returns:
        SystemRegistry: The global registry instance
    """
    global _registry
    if _registry is None:
        _registry = SystemRegistry()
    return _registry


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "SystemRegistry",
    "SubsystemCategory",
    "SubsystemInfo",
    "AgentInfo",
    "get_registry",
]
