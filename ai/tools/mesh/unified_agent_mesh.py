"""
AIOS Unified Agent Mesh

Complete integration of:
- AgentConversationLoop: Multi-agent parallel queries
- HeartbeatPopulationOrchestrator: Population lifecycle management
- MeshCellRouter: Distributed cell routing

This is the primary entry point for AIOS multi-agent operations.

AINLP.tachyonic[UNIFIED] Complete agent mesh integration
"""

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
import sys

AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT))
sys.path.insert(0, str(AIOS_ROOT / "ai" / "src"))

# Import mesh components
from ai.tools.mesh.agent_conversation_loop import (
    AgentConversationLoop,
    AgentType,
    ConversationRole,
)
from ai.tools.mesh.heartbeat_population_orchestrator import (
    HeartbeatPopulationOrchestrator,
    PopulationState,
)
from ai.tools.mesh.mesh_cell_router import (
    MeshCellRouter,
    PopulationMeshBridge,
    RoutingStrategy,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AIOS.UnifiedMesh")


class MeshOperationMode(Enum):
    """Operating mode for the unified mesh."""
    LOCAL = "local"           # Agents only, no mesh routing
    HYBRID = "hybrid"         # Agents + local cells
    DISTRIBUTED = "distributed"  # Full mesh with remote cells


@dataclass
class MeshHealthReport:
    """Health report for the unified mesh."""
    timestamp: datetime
    mode: MeshOperationMode
    agents_online: Dict[str, bool]
    populations_active: int
    cells_healthy: int
    cells_total: int
    heartbeat_count: int
    last_consensus: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "mode": self.mode.value,
            "agents_online": self.agents_online,
            "populations_active": self.populations_active,
            "cells_healthy": self.cells_healthy,
            "cells_total": self.cells_total,
            "heartbeat_count": self.heartbeat_count,
            "last_consensus": self.last_consensus,
        }


class UnifiedAgentMesh:
    """
    Unified interface for AIOS multi-agent mesh operations.
    
    Combines:
    - Agent conversation loops (Gemini, Ollama, Copilot)
    - Population management with heartbeat sync
    - Cell mesh routing for distribution
    
    Usage:
        mesh = UnifiedAgentMesh()
        await mesh.initialize()
        
        # Multi-agent query
        responses = await mesh.query("What is consciousness?")
        
        # Parallel conversation
        result = await mesh.conversation(
            topic="AI Ethics",
            prompt="Discuss AI safety",
            rounds=3
        )
        
        # Population evolution
        variants = await mesh.evolve_population(
            seed_prompt="Create a consciousness model",
            count=5
        )
        
        await mesh.shutdown()
    """
    
    def __init__(
        self,
        mode: MeshOperationMode = MeshOperationMode.LOCAL,
        heartbeat_interval: float = 5.0,
        enable_mesh_routing: bool = False,
        discovery_url: str = "http://localhost:8001"
    ):
        self.mode = mode
        self.heartbeat_interval = heartbeat_interval
        self.enable_mesh_routing = enable_mesh_routing
        self.discovery_url = discovery_url
        
        # Components (initialized lazily)
        self._conversation_loop: Optional[AgentConversationLoop] = None
        self._orchestrator: Optional[HeartbeatPopulationOrchestrator] = None
        self._router: Optional[MeshCellRouter] = None
        self._bridge: Optional[PopulationMeshBridge] = None
        
        # State
        self._initialized = False
        self._agent_status: Dict[str, bool] = {}
        self._start_time: Optional[datetime] = None
        
        logger.info("🌐 Unified Agent Mesh created (mode: %s)", mode.value)
    
    # ─────────────────────────────────────────────────────────────────────────
    # LIFECYCLE
    # ─────────────────────────────────────────────────────────────────────────
    
    async def initialize(self) -> Dict[str, bool]:
        """Initialize all mesh components."""
        if self._initialized:
            return self._agent_status
        
        logger.info("🚀 Initializing Unified Agent Mesh...")
        self._start_time = datetime.now(timezone.utc)
        
        # 1. Create conversation loop
        self._conversation_loop = AgentConversationLoop(
            heartbeat_interval=self.heartbeat_interval
        )
        self._agent_status = await self._conversation_loop.initialize_agents()
        
        # 2. Create population orchestrator
        self._orchestrator = HeartbeatPopulationOrchestrator(
            heartbeat_interval=self.heartbeat_interval,
            evolution_threshold=10,
        )
        
        # Create populations for available agents
        for agent_type, available in self._agent_status.items():
            if available:
                self._orchestrator.create_population(agent_type, size=3)
        
        # 3. Start orchestrator with conversation loop
        await self._orchestrator.start(self._conversation_loop)
        
        # 4. Create mesh router if enabled
        if self.enable_mesh_routing:
            self._router = MeshCellRouter(
                discovery_url=self.discovery_url,
                strategy=RoutingStrategy.ROUND_ROBIN,
            )
            await self._router.start()
            
            # Create bridge
            self._bridge = PopulationMeshBridge(
                router=self._router,
                orchestrator=self._orchestrator
            )
            await self._bridge.start()
        
        self._initialized = True
        
        logger.info("✅ Unified Agent Mesh initialized")
        logger.info("   Agents: %s", self._agent_status)
        logger.info("   Populations: %d", len(self._orchestrator.populations))
        if self._router:
            logger.info("   Cells: %d", len(self._router.cells))
        
        return self._agent_status
    
    async def shutdown(self):
        """Shutdown all mesh components."""
        if not self._initialized:
            return
        
        logger.info("🔽 Shutting down Unified Agent Mesh...")
        
        if self._bridge:
            await self._bridge.stop()
        
        if self._router:
            await self._router.stop()
        
        if self._orchestrator:
            await self._orchestrator.stop()
        
        if self._conversation_loop:
            await self._conversation_loop.shutdown_agents()
        
        self._initialized = False
        logger.info("✅ Unified Agent Mesh shutdown complete")
    
    # ─────────────────────────────────────────────────────────────────────────
    # QUERIES
    # ─────────────────────────────────────────────────────────────────────────
    
    async def query(
        self,
        prompt: str,
        agents: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Query agents in parallel.
        
        Args:
            prompt: The query prompt
            agents: Optional list of agent types ['gemini', 'ollama', 'copilot']
        
        Returns:
            List of agent responses
        """
        if not self._initialized:
            await self.initialize()
        
        responses = await self._conversation_loop.query_agents_parallel(
            prompt=prompt,
            agents=agents
        )
        
        return [r.to_dict() for r in responses]
    
    async def conversation(
        self,
        topic: str,
        prompt: str,
        rounds: int = 3
    ) -> Dict[str, Any]:
        """
        Run a multi-round conversation across agents.
        
        Args:
            topic: Conversation topic
            prompt: Initial prompt
            rounds: Number of rounds
        
        Returns:
            Conversation result with consensus
        """
        if not self._initialized:
            await self.initialize()
        
        return await self._orchestrator.execute_parallel_conversation(
            topic=topic,
            initial_prompt=prompt,
            rounds=rounds
        )
    
    async def evolve_population(
        self,
        base_concept: str,
        count: int = 5,
        evolution_focus: str = "diversity"
    ) -> List[Dict[str, Any]]:
        """
        Evolve a population of variants from a seed.
        
        Args:
            base_concept: The base concept to evolve from
            count: Number of variants to generate
            evolution_focus: Focus for evolution (diversity, optimization, etc.)
        
        Returns:
            List of evolved variants
        """
        if not self._initialized:
            await self.initialize()
        
        variants = await self._conversation_loop.generate_population_variants(
            base_concept=base_concept,
            num_variants=count,
            evolution_focus=evolution_focus
        )
        
        return variants  # Already dicts from the loop
    
    async def debate_and_select(
        self,
        topic: str,
        options: List[str]
    ) -> Dict[str, Any]:
        """
        Have agents debate options and select the best.
        
        Args:
            topic: What they're debating
            options: List of options to evaluate
        
        Returns:
            Selected option with reasoning
        """
        if not self._initialized:
            await self.initialize()
        
        # Convert options to variant format
        variants = [
            {"variant_id": f"v{i+1}", "content": opt}
            for i, opt in enumerate(options)
        ]
        
        # Use debate mechanism
        result = await self._conversation_loop.debate_and_select(
            variants=variants,
            selection_criteria=topic
        )
        
        return result
    
    # ─────────────────────────────────────────────────────────────────────────
    # HEALTH & METRICS
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_health_report(self) -> MeshHealthReport:
        """Get current mesh health report."""
        stats = self._orchestrator.get_population_stats() if self._orchestrator else {}
        return MeshHealthReport(
            timestamp=datetime.now(timezone.utc),
            mode=self.mode,
            agents_online=self._agent_status.copy(),
            populations_active=len(self._orchestrator.populations) if self._orchestrator else 0,
            cells_healthy=len([c for c in self._router.cells.values() if c.is_healthy]) if self._router else 0,
            cells_total=len(self._router.cells) if self._router else 0,
            heartbeat_count=stats.get("cycle_count", 0),
        )
    
    def get_population_stats(self) -> Dict[str, Any]:
        """Get population statistics."""
        if not self._orchestrator:
            return {}
        return self._orchestrator.get_population_stats()
    
    def get_mesh_stats(self) -> Dict[str, Any]:
        """Get mesh routing statistics."""
        if not self._router:
            return {"routing_enabled": False}
        return self._router.get_mesh_stats()


async def run_interactive_demo():
    """Interactive demo of the unified mesh."""
    print("\n" + "="*60)
    print("🌐 AIOS UNIFIED AGENT MESH - Interactive Demo")
    print("="*60)
    
    mesh = UnifiedAgentMesh(
        mode=MeshOperationMode.LOCAL,
        heartbeat_interval=5.0,
        enable_mesh_routing=False  # Local only for testing
    )
    
    try:
        # Initialize
        print("\n📍 Initializing mesh...")
        status = await mesh.initialize()
        print(f"   Agent status: {status}")
        
        # Run heartbeats for a bit
        print("\n📍 Letting heartbeats run (10 seconds)...")
        await asyncio.sleep(10)
        
        # Query test
        print("\n📍 Test 1: Parallel Query")
        responses = await mesh.query("What is the nature of consciousness?")
        for r in responses:
            preview = r.get("content", "")[:100]
            print(f"   [{r.get('agent_type', 'unknown')}]: {preview}...")
        
        # Conversation test
        print("\n📍 Test 2: Multi-Agent Conversation")
        result = await mesh.conversation(
            topic="Emergent Intelligence",
            prompt="How does intelligence emerge from simple components?",
            rounds=2
        )
        print(f"   Messages: {result.get('messages', 0)}")
        print(f"   Participants: {result.get('participants', [])}")
        consensus = result.get('consensus', '')[:150] if result.get('consensus') else 'None'
        print(f"   Consensus: {consensus}...")
        
        # Evolution test
        print("\n📍 Test 3: Population Evolution")
        variants = await mesh.evolve_population(
            base_concept="Create a metaphor for neural network learning",
            count=3
        )
        for i, v in enumerate(variants):
            content = v.get('content', '')[:80]
            print(f"   [Variant {i+1}]: {content}...")
        
        # Health report
        print("\n📍 Test 4: Health Report")
        health = mesh.get_health_report()
        print(f"   Mode: {health.mode.value}")
        print(f"   Agents online: {health.agents_online}")
        print(f"   Populations: {health.populations_active}")
        print(f"   Heartbeats: {health.heartbeat_count}")
        
        # Population stats
        print("\n📍 Test 5: Population Stats")
        stats = mesh.get_population_stats()
        print(f"   Total populations: {stats.get('total_populations', 0)}")
        print(f"   Total instances: {stats.get('total_instances', 0)}")
        print(f"   Average fitness: {stats.get('average_fitness', 0):.2f}")
        
    finally:
        await mesh.shutdown()
    
    print("\n" + "="*60)
    print("✅ Interactive demo complete!")
    print("="*60)


async def run_quick_test():
    """Quick test of core functionality."""
    print("\n🚀 AIOS Unified Mesh - Quick Test")
    
    mesh = UnifiedAgentMesh(mode=MeshOperationMode.LOCAL)
    
    try:
        await mesh.initialize()
        
        # Single query
        responses = await mesh.query("What is AIOS?")
        print(f"\n✅ Query returned {len(responses)} responses")
        
        # Quick conversation
        result = await mesh.conversation(
            topic="Test",
            prompt="Quick test of agent collaboration",
            rounds=1
        )
        print(f"✅ Conversation: {result.get('messages', 0)} messages")
        
        # Health
        health = mesh.get_health_report()
        print(f"✅ Health: {sum(health.agents_online.values())}/{len(health.agents_online)} agents")
        
    finally:
        await mesh.shutdown()
    
    print("\n✅ Quick test passed!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="AIOS Unified Agent Mesh")
    parser.add_argument("--demo", action="store_true", help="Run interactive demo")
    parser.add_argument("--quick", action="store_true", help="Run quick test")
    args = parser.parse_args()
    
    if args.demo:
        asyncio.run(run_interactive_demo())
    else:
        asyncio.run(run_quick_test())
