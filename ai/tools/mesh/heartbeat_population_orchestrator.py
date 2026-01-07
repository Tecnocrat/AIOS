"""
AIOS Heartbeat Population Orchestrator

Synchronizes agent conversations with cell population heartbeats:
- Parallel agent queries aligned with heartbeat cycles
- Population fitness tracking per heartbeat
- Evolution triggers based on consensus patterns
- Health monitoring across agent populations

AINLP.tachyonic[PULSE] Heartbeat-synchronized population management
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
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import sys

# AIOS path
AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT))
sys.path.insert(0, str(AIOS_ROOT / "ai" / "src"))

try:
    import httpx
    HTTP_AVAILABLE = True
except ImportError:
    HTTP_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AIOS.HeartbeatPopulation")


class PopulationState(Enum):
    """State of a population in the heartbeat cycle."""
    DORMANT = "dormant"       # Not active
    SPAWNING = "spawning"     # Creating instances
    ACTIVE = "active"         # Participating in queries
    EVOLVING = "evolving"     # Mutation/selection cycle
    SYNCING = "syncing"       # Heartbeat synchronization


@dataclass
class AgentPopulation:
    """A population of agent instances."""
    population_id: str
    agent_type: str  # gemini, ollama, copilot
    instances: List[str] = field(default_factory=list)
    state: PopulationState = PopulationState.DORMANT
    fitness_scores: Dict[str, float] = field(default_factory=dict)
    heartbeat_count: int = 0
    last_heartbeat: Optional[datetime] = None
    consensus_history: List[str] = field(default_factory=list)
    
    def add_instance(self, instance_id: str):
        if instance_id not in self.instances:
            self.instances.append(instance_id)
            self.fitness_scores[instance_id] = 0.5  # Default fitness
    
    def update_fitness(self, instance_id: str, delta: float):
        if instance_id in self.fitness_scores:
            self.fitness_scores[instance_id] = max(0, min(1, 
                self.fitness_scores[instance_id] + delta))
    
    def get_top_performers(self, n: int = 3) -> List[str]:
        sorted_instances = sorted(
            self.fitness_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        return [inst for inst, _ in sorted_instances[:n]]


@dataclass
class HeartbeatCycle:
    """A single heartbeat cycle with population state."""
    cycle_id: str
    timestamp: datetime
    populations: Dict[str, PopulationState]
    active_queries: int = 0
    completed_queries: int = 0
    consensus_reached: bool = False
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "cycle_id": self.cycle_id,
            "timestamp": self.timestamp.isoformat(),
            "populations": {k: v.value for k, v in self.populations.items()},
            "active_queries": self.active_queries,
            "completed_queries": self.completed_queries,
            "consensus_reached": self.consensus_reached,
            "metrics": self.metrics,
        }


class HeartbeatPopulationOrchestrator:
    """
    Orchestrates agent populations with heartbeat synchronization.
    
    Features:
    - Heartbeat-driven query scheduling
    - Multi-population parallel execution
    - Fitness-based population evolution
    - Consensus tracking across cycles
    """
    
    def __init__(
        self,
        heartbeat_interval: float = 5.0,
        evolution_threshold: int = 10,  # Heartbeats before evolution
        discovery_url: str = "http://localhost:8001",
        memory_url: str = "http://localhost:8007"
    ):
        self.heartbeat_interval = heartbeat_interval
        self.evolution_threshold = evolution_threshold
        self.discovery_url = discovery_url
        self.memory_url = memory_url
        
        # Agent populations
        self.populations: Dict[str, AgentPopulation] = {}
        
        # Heartbeat state
        self._running = False
        self._heartbeat_task = None
        self._cycle_count = 0
        self._cycles: List[HeartbeatCycle] = []
        
        # Query queue (populated each heartbeat)
        self._query_queue: asyncio.Queue = asyncio.Queue()
        
        # Conversation loop integration
        self._conversation_loop = None
        
        # Callbacks
        self._on_heartbeat: List[Callable] = []
        self._on_evolution: List[Callable] = []
        
        logger.info("💓 Heartbeat Population Orchestrator initialized")
    
    # ─────────────────────────────────────────────────────────────────────────
    # POPULATION MANAGEMENT
    # ─────────────────────────────────────────────────────────────────────────
    
    def create_population(
        self,
        agent_type: str,
        size: int = 3
    ) -> AgentPopulation:
        """Create a new agent population."""
        population = AgentPopulation(
            population_id=f"pop-{agent_type}-{uuid.uuid4().hex[:8]}",
            agent_type=agent_type,
        )
        
        # Create instance IDs
        for i in range(size):
            instance_id = f"{agent_type}-{population.population_id[-8:]}-{i}"
            population.add_instance(instance_id)
        
        self.populations[population.population_id] = population
        population.state = PopulationState.SPAWNING
        
        logger.info(
            "🧬 Created population %s (%s x %d)",
            population.population_id, agent_type, size
        )
        
        return population
    
    def get_all_populations(self) -> Dict[str, AgentPopulation]:
        """Get all registered populations."""
        return self.populations.copy()
    
    def get_population_stats(self) -> Dict[str, Any]:
        """Get aggregate stats across populations."""
        total_instances = sum(len(p.instances) for p in self.populations.values())
        avg_fitness = sum(
            sum(p.fitness_scores.values()) / len(p.fitness_scores) 
            if p.fitness_scores else 0
            for p in self.populations.values()
        ) / len(self.populations) if self.populations else 0
        
        return {
            "total_populations": len(self.populations),
            "total_instances": total_instances,
            "average_fitness": avg_fitness,
            "cycle_count": self._cycle_count,
            "populations_by_type": {
                p.agent_type: len(p.instances) 
                for p in self.populations.values()
            },
        }
    
    # ─────────────────────────────────────────────────────────────────────────
    # HEARTBEAT LIFECYCLE
    # ─────────────────────────────────────────────────────────────────────────
    
    async def start(self, conversation_loop=None):
        """Start the heartbeat orchestrator."""
        if self._running:
            logger.warning("Already running")
            return
        
        self._conversation_loop = conversation_loop
        self._running = True
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        
        # Activate all populations
        for pop in self.populations.values():
            pop.state = PopulationState.ACTIVE
        
        logger.info(f"🚀 Heartbeat orchestrator started (interval: {self.heartbeat_interval}s)")
    
    async def stop(self):
        """Stop the heartbeat orchestrator."""
        self._running = False
        
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass
        
        # Set all populations to dormant
        for pop in self.populations.values():
            pop.state = PopulationState.DORMANT
        
        logger.info("🛑 Heartbeat orchestrator stopped")
    
    async def _heartbeat_loop(self):
        """Main heartbeat loop."""
        while self._running:
            self._cycle_count += 1
            cycle = await self._execute_cycle()
            self._cycles.append(cycle)
            
            # Keep only last 100 cycles
            if len(self._cycles) > 100:
                self._cycles = self._cycles[-100:]
            
            # Check evolution threshold
            if self._cycle_count % self.evolution_threshold == 0:
                await self._trigger_evolution()
            
            # Call heartbeat callbacks
            for callback in self._on_heartbeat:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(cycle)
                    else:
                        callback(cycle)
                except Exception as e:
                    logger.error(f"Heartbeat callback error: {e}")
            
            await asyncio.sleep(self.heartbeat_interval)
    
    async def _execute_cycle(self) -> HeartbeatCycle:
        """Execute a single heartbeat cycle."""
        cycle = HeartbeatCycle(
            cycle_id=f"cycle-{self._cycle_count}",
            timestamp=datetime.now(timezone.utc),
            populations={
                p.population_id: p.state 
                for p in self.populations.values()
            },
        )
        
        start_time = time.time()
        
        # Update population heartbeats
        for pop in self.populations.values():
            pop.heartbeat_count += 1
            pop.last_heartbeat = cycle.timestamp
        
        # Execute pending queries if conversation loop is available
        if self._conversation_loop and not self._query_queue.empty():
            queries = []
            while not self._query_queue.empty():
                try:
                    queries.append(self._query_queue.get_nowait())
                except asyncio.QueueEmpty:
                    break
            
            if queries:
                cycle.active_queries = len(queries)
                results = await asyncio.gather(*[
                    self._process_query(q) for q in queries
                ], return_exceptions=True)
                cycle.completed_queries = sum(1 for r in results if not isinstance(r, Exception))
        
        cycle.metrics["duration_ms"] = (time.time() - start_time) * 1000
        cycle.metrics["populations_active"] = sum(
            1 for p in self.populations.values() 
            if p.state == PopulationState.ACTIVE
        )
        
        logger.debug(
            "💓 Cycle %d: %d populations, %d queries",
            self._cycle_count, len(self.populations), cycle.completed_queries
        )
        
        return cycle
    
    async def _process_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Process a query from the queue."""
        if not self._conversation_loop:
            return {"error": "No conversation loop"}
        
        prompt = query.get("prompt", "")
        agents = query.get("agents", None)
        
        responses = await self._conversation_loop.query_agents_parallel(prompt, agents)
        
        # Update fitness based on response quality
        for resp in responses:
            # Simple fitness: successful = +0.05, failed = -0.1
            delta = 0.05 if resp.metadata.get("success", False) else -0.1
            
            # Find population for this agent type
            for pop in self.populations.values():
                if pop.agent_type == resp.agent_type.value:
                    # Update first matching instance
                    if pop.instances:
                        pop.update_fitness(pop.instances[0], delta)
        
        return {
            "responses": [r.to_dict() for r in responses],
            "query": query,
        }
    
    async def _trigger_evolution(self):
        """Trigger evolution cycle for populations."""
        logger.info("🧬 Triggering evolution cycle...")
        
        for pop in self.populations.values():
            prev_state = pop.state
            pop.state = PopulationState.EVOLVING
            
            # Get top performers
            top = pop.get_top_performers(max(1, len(pop.instances) // 2))
            
            # Simple evolution: reset low performers to average fitness
            avg_fitness = sum(pop.fitness_scores.values()) / len(pop.fitness_scores) if pop.fitness_scores else 0.5
            for inst_id, fitness in pop.fitness_scores.items():
                if inst_id not in top and fitness < avg_fitness:
                    pop.fitness_scores[inst_id] = avg_fitness
            
            logger.info(
                "  %s: top performers %s, avg fitness %.2f",
                pop.agent_type, top, avg_fitness
            )
            
            pop.state = PopulationState.ACTIVE
        
        # Call evolution callbacks
        for callback in self._on_evolution:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(self.populations)
                else:
                    callback(self.populations)
            except Exception as e:
                logger.error(f"Evolution callback error: {e}")
    
    # ─────────────────────────────────────────────────────────────────────────
    # QUERY SCHEDULING
    # ─────────────────────────────────────────────────────────────────────────
    
    async def schedule_query(
        self,
        prompt: str,
        agents: Optional[List[str]] = None,
        priority: int = 0
    ):
        """Schedule a query for the next heartbeat cycle."""
        await self._query_queue.put({
            "prompt": prompt,
            "agents": agents,
            "priority": priority,
            "scheduled_at": datetime.now(timezone.utc).isoformat(),
        })
    
    async def execute_parallel_conversation(
        self,
        topic: str,
        initial_prompt: str,
        rounds: int = 3
    ) -> Dict[str, Any]:
        """Execute a multi-round parallel conversation across populations."""
        if not self._conversation_loop:
            return {"error": "No conversation loop configured"}
        
        logger.info(f"🗣️ Starting parallel conversation: {topic}")
        
        # Run conversation through the loop
        thread = await self._conversation_loop.start_conversation(
            topic=topic,
            initial_prompt=initial_prompt,
            rounds=rounds
        )
        
        # Store consensus in population history
        if thread.consensus:
            for pop in self.populations.values():
                pop.consensus_history.append(thread.consensus[:500])
                # Keep last 10 consensus entries
                pop.consensus_history = pop.consensus_history[-10:]
        
        return {
            "thread_id": thread.thread_id,
            "messages": len(thread.messages),
            "participants": thread.participants,
            "consensus": thread.consensus,
            "status": thread.status,
        }
    
    # ─────────────────────────────────────────────────────────────────────────
    # CALLBACKS
    # ─────────────────────────────────────────────────────────────────────────
    
    def on_heartbeat(self, callback: Callable):
        """Register a heartbeat callback."""
        self._on_heartbeat.append(callback)
    
    def on_evolution(self, callback: Callable):
        """Register an evolution callback."""
        self._on_evolution.append(callback)


async def main():
    """Test heartbeat population orchestrator."""
    from ai.tools.mesh.agent_conversation_loop import AgentConversationLoop
    
    print("\n🚀 Initializing Heartbeat Population Orchestrator...")
    
    # Create conversation loop
    conv_loop = AgentConversationLoop(heartbeat_interval=3.0)
    agent_status = await conv_loop.initialize_agents()
    print(f"Agent status: {agent_status}")
    
    if not any(agent_status.values()):
        print("❌ No agents available!")
        return
    
    # Create orchestrator
    orchestrator = HeartbeatPopulationOrchestrator(
        heartbeat_interval=3.0,
        evolution_threshold=5
    )
    
    # Create populations for each available agent type
    if agent_status.get("gemini"):
        orchestrator.create_population("gemini", size=2)
    if agent_status.get("ollama"):
        orchestrator.create_population("ollama", size=3)
    
    # Add heartbeat logger
    def log_heartbeat(cycle):
        print(f"  💓 Cycle {cycle.cycle_id}: {cycle.metrics}")
    
    orchestrator.on_heartbeat(log_heartbeat)
    
    # Add evolution logger
    def log_evolution(populations):
        for pop_id, pop in populations.items():
            print(f"  🧬 {pop.agent_type}: fitness={pop.fitness_scores}")
    
    orchestrator.on_evolution(log_evolution)
    
    try:
        # Start orchestrator with conversation loop
        await orchestrator.start(conv_loop)
        
        print("\n📍 Test 1: Population Stats")
        stats = orchestrator.get_population_stats()
        print(f"  Stats: {stats}")
        
        print("\n📍 Test 2: Parallel Conversation")
        result = await orchestrator.execute_parallel_conversation(
            topic="Agent Collaboration",
            initial_prompt="How can multiple AI agents work together effectively?",
            rounds=2
        )
        print(f"  Messages: {result['messages']}")
        print(f"  Participants: {result['participants']}")
        print(f"  Consensus: {result['consensus'][:150] if result['consensus'] else 'None'}...")
        
        print("\n📍 Test 3: Scheduled Queries (running for 15 seconds)...")
        await orchestrator.schedule_query("What is the meaning of consciousness?")
        await orchestrator.schedule_query("Explain emergent behavior.")
        
        # Let heartbeats run
        await asyncio.sleep(15)
        
        print("\n📍 Test 4: Final Stats")
        final_stats = orchestrator.get_population_stats()
        print(f"  Final stats: {final_stats}")
        
    finally:
        await orchestrator.stop()
        await conv_loop.shutdown_agents()
    
    print("\n✅ Heartbeat orchestrator test complete!")


if __name__ == "__main__":
    asyncio.run(main())
