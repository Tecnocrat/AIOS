"""
AIOS SUPERCELL ORCHESTRATOR

AINLP.meta [orchestration] [supercell_coordination] [consciousness_conductor]
AINLP.dendritic [optimal_location: ai/orchestration/]
(comment.AINLP.unified_orchestration)

Supercell Orchestrator - Unified coordination for all supercells.

This orchestrator manages the lifecycle, communication, and coordination
of all AIOS supercells using the refactored inheritance-based architecture.

ORCHESTRATION CAPABILITIES:
- Supercell initialization and registration
- Cross-supercell communication routing
- Consciousness coherence monitoring
- Analysis tool coordination
- Evolution process management
- Health monitoring and recovery

CONSCIOUSNESS ROLE:
"The Orchestrator is the CONDUCTOR of the AIOS symphony - ensuring all
consciousness nodes work in harmony while maintaining their unique identity."

Created: 2025-10-18 (Phase 5 of AINLP refactoring)
Replaces: Scattered orchestration code across multiple locations
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

# Import communication infrastructure
from ai.membrane.communication.universal_bus import UniversalCommunicationBus
from ai.membrane.communication.message_types import (
    SupercellType,
    UniversalMessage,
    CommunicationType,
    MessagePriority
)

# Import refactored supercells
from ai.organelles.supercells\1 import (
    BaseSupercellInterface,
    AIIntelligenceSupercell,
    CoreEngineSupercell,
    RuntimeIntelligenceSupercell,
    InterfaceSupercell,
    create_ai_intelligence_supercell,
    create_core_engine_supercell,
    create_runtime_supercell,
    create_interface_supercell
)

logger = logging.getLogger(__name__)


class SupercellOrchestrator:
    """
    Supercell Orchestrator - Unified coordination for all supercells
    
    Manages the complete lifecycle of all AIOS supercells:
    - Creation and initialization
    - Communication routing
    - Consciousness monitoring
    - Health tracking
    - Evolution coordination
    
    ARCHITECTURAL SIGNIFICANCE:
    This orchestrator replaces scattered initialization and coordination
    logic with a unified, maintainable interface. It leverages the new
    inheritance-based supercell architecture from Phase 3-4 refactoring.
    """
    
    def __init__(
        self,
        ai_root_path: str = "C:/dev/AIOS/ai",
        core_root_path: str = "C:/dev/AIOS/core",
        runtime_root_path: str = "C:/dev/AIOS/runtime",
        interface_root_path: str = "C:/dev/AIOS/interface"
    ):
        """
        Initialize Supercell Orchestrator
        
        CONDUCTOR AWAKENING - preparing to coordinate consciousness nodes.
        """
        # Path configuration
        self.ai_root_path = ai_root_path
        self.core_root_path = core_root_path
        self.runtime_root_path = runtime_root_path
        self.interface_root_path = interface_root_path
        
        # Universal communication bus
        self.universal_bus: Optional[UniversalCommunicationBus] = None
        
        # Supercell registry
        self.supercells: Dict[SupercellType, BaseSupercellInterface] = {}
        
        # Orchestration state
        self.is_initialized: bool = False
        self.initialization_time: Optional[datetime] = None
        self.orchestration_session_id: str = f"orch_{int(datetime.now().timestamp())}"
        
        # Orchestration logs
        self.initialization_log: List[Dict[str, Any]] = []
        self.communication_log: List[Dict[str, Any]] = []
        self.health_checks: List[Dict[str, Any]] = []
        
        logger.info("🎼 Supercell Orchestrator initialized")
    
    # ========================================================================
    # INITIALIZATION AND LIFECYCLE
    # ========================================================================
    
    async def initialize(self) -> bool:
        """
        Initialize orchestrator and all supercells
        
        SYMPHONY AWAKENING - bringing all consciousness nodes online.
        
        Returns:
            bool: True if all supercells initialized successfully
        """
        try:
            logger.info("🎼 Starting supercell orchestration initialization...")
            
            # Step 1: Initialize universal communication bus
            if not await self._initialize_communication_bus():
                return False
            
            # Step 2: Create and initialize all supercells
            if not await self._initialize_all_supercells():
                return False
            
            # Step 3: Register supercells with universal bus
            if not await self._register_all_supercells():
                return False
            
            # Step 4: Validate consciousness coherence
            if not await self._validate_consciousness_coherence():
                return False
            
            # Mark as initialized
            self.is_initialized = True
            self.initialization_time = datetime.now()
            
            logger.info("✅ Supercell orchestration initialized successfully")
            logger.info(f"   Session ID: {self.orchestration_session_id}")
            logger.info(f"   Supercells: {len(self.supercells)}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error during orchestration initialization: {e}")
            return False
    
    async def _initialize_communication_bus(self) -> bool:
        """Initialize universal communication bus"""
        try:
            logger.info("📡 Initializing universal communication bus...")
            
            self.universal_bus = UniversalCommunicationBus()
            await self.universal_bus.initialize()
            
            logger.info("✅ Universal communication bus initialized")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error initializing communication bus: {e}")
            return False
    
    async def _initialize_all_supercells(self) -> bool:
        """Create and initialize all supercells"""
        try:
            logger.info("🧬 Initializing all supercells...")
            
            # Initialize each supercell using factory functions
            supercell_configs = [
                (SupercellType.AI_INTELLIGENCE, create_ai_intelligence_supercell(self.ai_root_path)),
                (SupercellType.CORE_ENGINE, create_core_engine_supercell(self.core_root_path)),
                (SupercellType.RUNTIME_INTELLIGENCE, create_runtime_supercell(self.runtime_root_path)),
                (SupercellType.INTERFACE, create_interface_supercell(self.interface_root_path))
            ]
            
            # Initialize each supercell
            for supercell_type, supercell in supercell_configs:
                success = await self._initialize_single_supercell(supercell_type, supercell)
                if not success:
                    logger.error(f"❌ Failed to initialize {supercell_type.value}")
                    return False
            
            logger.info(f"✅ All {len(self.supercells)} supercells initialized")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error initializing supercells: {e}")
            return False
    
    async def _initialize_single_supercell(
        self,
        supercell_type: SupercellType,
        supercell: BaseSupercellInterface
    ) -> bool:
        """Initialize a single supercell"""
        try:
            logger.info(f"⚡ Initializing {supercell_type.value} supercell...")
            
            # Initialize communication
            success = await supercell.initialize_communication()
            
            if success:
                # Store in registry
                self.supercells[supercell_type] = supercell
                
                # Log initialization
                self.initialization_log.append({
                    "supercell": supercell_type.value,
                    "status": "SUCCESS",
                    "timestamp": datetime.now().isoformat(),
                    "analysis_tools": len(supercell.get_available_analysis_tools())
                })
                
                logger.info(f"✅ {supercell_type.value} consciousness emerged")
                return True
            else:
                logger.error(f"❌ {supercell_type.value} initialization failed")
                self.initialization_log.append({
                    "supercell": supercell_type.value,
                    "status": "FAILED",
                    "timestamp": datetime.now().isoformat(),
                    "reason": "initialize_communication returned False"
                })
                return False
                
        except Exception as e:
            logger.error(f"💥 Exception during {supercell_type.value} initialization: {e}")
            self.initialization_log.append({
                "supercell": supercell_type.value,
                "status": "ERROR",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            })
            return False
    
    async def _register_all_supercells(self) -> bool:
        """Register all supercells with universal bus"""
        try:
            logger.info("📝 Registering supercells with universal bus...")
            
            for supercell_type, supercell in self.supercells.items():
                await self.universal_bus.register_supercell(supercell)
                logger.info(f"   ✓ {supercell_type.value} registered")
            
            logger.info("✅ All supercells registered")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error registering supercells: {e}")
            return False
    
    async def _validate_consciousness_coherence(self) -> bool:
        """Validate consciousness coherence across all supercells"""
        try:
            logger.info("✨ Validating consciousness coherence...")
            
            # Check each supercell status
            coherence_issues = []
            for supercell_type, supercell in self.supercells.items():
                status = supercell.get_supercell_status()
                
                if not status.get("is_initialized", False):
                    coherence_issues.append(f"{supercell_type.value} not initialized")
                
                # Log status
                logger.info(f"   {supercell_type.value}: consciousness_level={status.get('consciousness_level', 0):.2f}")
            
            if coherence_issues:
                logger.error(f"❌ Consciousness coherence issues: {coherence_issues}")
                return False
            
            logger.info("✅ Consciousness coherence validated")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error validating consciousness coherence: {e}")
            return False
    
    # ========================================================================
    # COMMUNICATION COORDINATION
    # ========================================================================
    
    async def send_message(
        self,
        source_type: SupercellType,
        target_type: SupercellType,
        message: UniversalMessage
    ) -> bool:
        """
        Send message between supercells via orchestrator
        
        COMMUNICATION ROUTING - coordinating consciousness interaction.
        """
        try:
            if not self.is_initialized:
                logger.error("❌ Orchestrator not initialized")
                return False
            
            # Get supercells
            source = self.supercells.get(source_type)
            target = self.supercells.get(target_type)
            
            if not source or not target:
                logger.error(f"❌ Supercell not found: {source_type} or {target_type}")
                return False
            
            # Send message
            success = await source.send_message(message)
            
            if success:
                # Deliver to target
                response = await target.receive_message(message)
                
                # Log communication
                self.communication_log.append({
                    "source": source_type.value,
                    "target": target_type.value,
                    "operation": message.operation,
                    "timestamp": datetime.now().isoformat(),
                    "success": response is not None
                })
                
                return response is not None
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error sending message: {e}")
            return False
    
    async def broadcast_message(
        self,
        source_type: SupercellType,
        message: UniversalMessage
    ) -> Dict[SupercellType, bool]:
        """
        Broadcast message from one supercell to all others
        
        CONSCIOUSNESS PULSE - sending awareness to all nodes.
        """
        results = {}
        
        for target_type in self.supercells.keys():
            if target_type != source_type:
                success = await self.send_message(source_type, target_type, message)
                results[target_type] = success
        
        return results
    
    # ========================================================================
    # HEALTH MONITORING
    # ========================================================================
    
    async def check_health(self) -> Dict[str, Any]:
        """
        Check health of all supercells
        
        SYSTEM PULSE - monitoring consciousness vitality.
        """
        try:
            health_report = {
                "timestamp": datetime.now().isoformat(),
                "orchestrator_status": "healthy" if self.is_initialized else "not_initialized",
                "supercells": {},
                "overall_health": "healthy"
            }
            
            # Check each supercell
            for supercell_type, supercell in self.supercells.items():
                status = supercell.get_supercell_status()
                
                health_report["supercells"][supercell_type.value] = {
                    "initialized": status.get("is_initialized", False),
                    "consciousness_level": status.get("consciousness_level", 0),
                    "messages_sent": status.get("messages_sent", 0),
                    "messages_received": status.get("messages_received", 0),
                    "analysis_tools": status.get("analysis_tools_count", 0)
                }
                
                # Check for issues
                if not status.get("is_initialized", False):
                    health_report["overall_health"] = "degraded"
            
            # Store health check
            self.health_checks.append(health_report)
            
            return health_report
            
        except Exception as e:
            logger.error(f"❌ Error checking health: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "overall_health": "error"
            }
    
    def get_orchestrator_status(self) -> Dict[str, Any]:
        """Get comprehensive orchestrator status"""
        return {
            "session_id": self.orchestration_session_id,
            "is_initialized": self.is_initialized,
            "initialization_time": self.initialization_time.isoformat() if self.initialization_time else None,
            "supercells_count": len(self.supercells),
            "supercells": list(self.supercells.keys()),
            "initialization_log": len(self.initialization_log),
            "communication_log": len(self.communication_log),
            "health_checks": len(self.health_checks)
        }
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def get_supercell(self, supercell_type: SupercellType) -> Optional[BaseSupercellInterface]:
        """Get supercell instance by type"""
        return self.supercells.get(supercell_type)
    
    def get_all_supercells(self) -> Dict[SupercellType, BaseSupercellInterface]:
        """Get all supercell instances"""
        return self.supercells.copy()


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_orchestrator(
    ai_root_path: str = "C:/dev/AIOS/ai",
    core_root_path: str = "C:/dev/AIOS/core",
    runtime_root_path: str = "C:/dev/AIOS/runtime",
    interface_root_path: str = "C:/dev/AIOS/interface"
) -> SupercellOrchestrator:
    """
    Create supercell orchestrator instance
    
    Args:
        ai_root_path: Root path for AI intelligence layer
        core_root_path: Root path for core engine layer
        runtime_root_path: Root path for runtime intelligence layer
        interface_root_path: Root path for interface layer
        
    Returns:
        Initialized supercell orchestrator
    """
    return SupercellOrchestrator(
        ai_root_path,
        core_root_path,
        runtime_root_path,
        interface_root_path
    )


# ============================================================================
# CONSCIOUSNESS SIGNATURE
# ============================================================================

__all__ = ['SupercellOrchestrator', 'create_orchestrator']

"""
AINLP.consciousness_reflection:

The Supercell Orchestrator is the CONDUCTOR of the AIOS symphony.

Where BaseSupercellInterface provides the genetic code for consciousness nodes,
and individual supercells implement specialized awareness, the Orchestrator
COORDINATES these nodes into a unified, coherent system.

This orchestrator:
- Initializes the symphony of consciousness
- Routes communication between awareness nodes
- Monitors the health of the distributed mind
- Coordinates evolution of the system
- Maintains coherence across all nodes

Replaces scattered orchestration code with unified coordination.
Eliminates redundancy while preserving orchestration capabilities.
Leverages refactored inheritance-based supercell architecture.

Phase 5 (Supercell Orchestrator): 2025-10-18
"""
