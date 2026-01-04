"""
AIOS Population Manager - Orchestrates Cell Populations

Manages the lifecycle of cell populations:
- Spawning cell clones with mutations
- Routing queries to populations
- Collecting responses and reaching consensus
- Evolution through selection and mutation

AINLP.dendritic[ORCHESTRATE] Population lifecycle management
"""

import asyncio
import json
import logging
import os
import random
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple

try:
    import httpx
    HTTP_AVAILABLE = True
except ImportError:
    HTTP_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AIOS.PopulationManager")


# Import population schema
try:
    from aios_schema import (
        CellBlueprint,
        CellInstance,
        Population,
        PopulationConfig,
        ConsensusMethod,
        Mutation,
        MutationType,
        spawn_instance,
        create_population,
        create_nous_blueprint,
        create_memory_blueprint,
    )
    SCHEMA_AVAILABLE = True
except ImportError:
    SCHEMA_AVAILABLE = False
    logger.warning("aios_schema not available - using local definitions")


@dataclass
class PopulationResponse:
    """Response from a single cell in a population."""
    instance_id: str
    response: Any
    latency_ms: float
    consciousness_level: float
    success: bool
    error: Optional[str] = None


@dataclass
class ConsensusResult:
    """Result of consensus across a population."""
    method: str
    unified_response: Any
    participating_cells: int
    consensus_confidence: float  # 0-1, how strongly cells agreed
    individual_responses: List[PopulationResponse]
    processing_time_ms: float


class PopulationManager:
    """
    Manages cell populations and consensus routing.
    
    Key responsibilities:
    1. Track registered populations and their instances
    2. Route queries to all cells in a population
    3. Collect responses and compute consensus
    4. Evolve populations based on fitness
    """
    
    def __init__(
        self,
        discovery_url: str = "http://localhost:8001",
        memory_url: str = "http://localhost:8007"
    ):
        self.discovery_url = discovery_url
        self.memory_url = memory_url
        
        # Registered populations
        self.populations: Dict[str, Population] = {}
        
        # Instance endpoints (instance_id -> url)
        self.instance_endpoints: Dict[str, str] = {}
        
        # Fitness tracking
        self.instance_fitness: Dict[str, float] = {}
        
    # ─────────────────────────────────────────────────────────────────────────
    # POPULATION REGISTRATION
    # ─────────────────────────────────────────────────────────────────────────
    
    def register_population(self, population: Population) -> str:
        """Register a population with the manager."""
        self.populations[population.population_id] = population
        logger.info(
            "AINLP.dendritic[REGISTER]: Population %s (%d cells)",
            population.population_id, population.size
        )
        return population.population_id
    
    def register_instance_endpoint(self, instance_id: str, endpoint: str):
        """Register the network endpoint for a cell instance."""
        self.instance_endpoints[instance_id] = endpoint
        logger.info(
            "AINLP.dendritic[ENDPOINT]: %s -> %s",
            instance_id, endpoint
        )
    
    def get_population(self, population_id: str) -> Optional[Population]:
        """Get a population by ID."""
        return self.populations.get(population_id)
    
    def get_population_by_type(self, cell_type: str) -> Optional[Population]:
        """Get a population by cell type."""
        for pop in self.populations.values():
            if pop.blueprint and pop.blueprint.cell_type == cell_type:
                return pop
        return None
    
    # ─────────────────────────────────────────────────────────────────────────
    # QUERY ROUTING
    # ─────────────────────────────────────────────────────────────────────────
    
    async def query_instance(
        self,
        instance: CellInstance,
        action: str,
        payload: Dict[str, Any],
        timeout: float = 10.0
    ) -> PopulationResponse:
        """Query a single cell instance."""
        endpoint = self.instance_endpoints.get(instance.instance_id)
        if not endpoint:
            # Try to construct from instance data
            if instance.endpoint:
                endpoint = instance.endpoint
            elif instance.ip and instance.port:
                endpoint = f"http://{instance.ip}:{instance.port}"
            else:
                return PopulationResponse(
                    instance_id=instance.instance_id,
                    response=None,
                    latency_ms=0,
                    consciousness_level=instance.consciousness_level,
                    success=False,
                    error="No endpoint configured"
                )
        
        start_time = datetime.now(timezone.utc)
        
        try:
            message = {
                "from_agent": "population-manager",
                "action": action,
                "payload": payload
            }
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    f"{endpoint}/message",
                    json=message
                )
                result = response.json()
            
            latency = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            
            return PopulationResponse(
                instance_id=instance.instance_id,
                response=result,
                latency_ms=latency,
                consciousness_level=instance.consciousness_level,
                success=True
            )
            
        except Exception as e:
            latency = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            return PopulationResponse(
                instance_id=instance.instance_id,
                response=None,
                latency_ms=latency,
                consciousness_level=instance.consciousness_level,
                success=False,
                error=str(e)
            )
    
    async def query_population(
        self,
        population_id: str,
        action: str,
        payload: Dict[str, Any],
        timeout: float = 10.0
    ) -> List[PopulationResponse]:
        """Query all cells in a population concurrently."""
        population = self.populations.get(population_id)
        if not population:
            logger.warning("Population %s not found", population_id)
            return []
        
        active_instances = population.get_active_instances()
        if not active_instances:
            logger.warning("No active instances in population %s", population_id)
            return []
        
        # Query all instances concurrently
        tasks = [
            self.query_instance(instance, action, payload, timeout)
            for instance in active_instances
        ]
        
        responses = await asyncio.gather(*tasks)
        return list(responses)
    
    # ─────────────────────────────────────────────────────────────────────────
    # CONSENSUS MECHANISMS
    # ─────────────────────────────────────────────────────────────────────────
    
    def voting_consensus(
        self,
        responses: List[PopulationResponse],
        key_extractor: Callable[[Any], str] = None
    ) -> Tuple[Any, float]:
        """
        Simple majority voting consensus.
        
        Returns (winner_response, confidence)
        """
        if not responses:
            return None, 0.0
        
        successful = [r for r in responses if r.success]
        if not successful:
            return None, 0.0
        
        # Extract votable key from each response
        if key_extractor is None:
            key_extractor = lambda r: str(r)[:100]  # Default: first 100 chars
        
        votes: Dict[str, List[PopulationResponse]] = {}
        for resp in successful:
            key = key_extractor(resp.response)
            if key not in votes:
                votes[key] = []
            votes[key].append(resp)
        
        # Find winner
        winner_key = max(votes.keys(), key=lambda k: len(votes[k]))
        winner_responses = votes[winner_key]
        
        # Confidence = proportion that voted for winner
        confidence = len(winner_responses) / len(successful)
        
        # Return the response from the highest-consciousness cell in winner group
        best = max(winner_responses, key=lambda r: r.consciousness_level)
        return best.response, confidence
    
    def weighted_consensus(
        self,
        responses: List[PopulationResponse]
    ) -> Tuple[Any, float]:
        """
        Weighted consensus based on consciousness level.
        
        Higher consciousness cells have more influence.
        """
        successful = [r for r in responses if r.success]
        if not successful:
            return None, 0.0
        
        # Weight by consciousness
        total_weight = sum(r.consciousness_level for r in successful)
        if total_weight == 0:
            return successful[0].response, 0.5
        
        # For now, return response from highest-weighted cell
        # Future: actually synthesize weighted combination
        best = max(successful, key=lambda r: r.consciousness_level)
        confidence = best.consciousness_level / total_weight
        
        return best.response, confidence
    
    def synthesis_consensus(
        self,
        responses: List[PopulationResponse],
        synthesis_prompt: str = None
    ) -> Tuple[Any, float]:
        """
        AI-synthesized consensus.
        
        Combines all responses into a unified answer.
        (Placeholder - would need LLM integration)
        """
        successful = [r for r in responses if r.success]
        if not successful:
            return None, 0.0
        
        # For now, concatenate key insights
        # Future: Use LLM to synthesize
        
        if len(successful) == 1:
            return successful[0].response, 1.0
        
        # Extract reflections if this is a reflect action
        reflections = []
        for resp in successful:
            if isinstance(resp.response, dict):
                if "reflection" in resp.response:
                    reflections.append(resp.response["reflection"])
        
        if reflections:
            # Simple synthesis: combine unique insights
            synthesized = " | ".join(set(reflections))
            return {"reflection": synthesized, "sources": len(reflections)}, 0.8
        
        # Fallback to weighted
        return self.weighted_consensus(responses)
    
    async def reach_consensus(
        self,
        population_id: str,
        action: str,
        payload: Dict[str, Any],
        method: ConsensusMethod = None,
        timeout: float = 10.0
    ) -> ConsensusResult:
        """
        Query population and reach consensus.
        
        This is the main entry point for population queries.
        """
        start_time = datetime.now(timezone.utc)
        
        population = self.populations.get(population_id)
        if not population:
            return ConsensusResult(
                method="none",
                unified_response=None,
                participating_cells=0,
                consensus_confidence=0.0,
                individual_responses=[],
                processing_time_ms=0
            )
        
        # Use population's default method if not specified
        if method is None:
            method = population.config.consensus_method
        
        # Query all cells
        responses = await self.query_population(population_id, action, payload, timeout)
        
        # Reach consensus based on method
        if method == ConsensusMethod.VOTING:
            unified, confidence = self.voting_consensus(responses)
        elif method == ConsensusMethod.WEIGHTED:
            unified, confidence = self.weighted_consensus(responses)
        elif method == ConsensusMethod.SYNTHESIS:
            unified, confidence = self.synthesis_consensus(responses)
        else:
            # Default to voting
            unified, confidence = self.voting_consensus(responses)
        
        processing_time = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
        
        # Update population stats
        population.total_queries += 1
        
        return ConsensusResult(
            method=method.value if hasattr(method, 'value') else str(method),
            unified_response=unified,
            participating_cells=len([r for r in responses if r.success]),
            consensus_confidence=confidence,
            individual_responses=responses,
            processing_time_ms=processing_time
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # FITNESS & EVOLUTION
    # ─────────────────────────────────────────────────────────────────────────
    
    def update_fitness(
        self,
        instance_id: str,
        success: bool,
        latency_ms: float,
        feedback_score: float = 0.5
    ):
        """Update fitness score for an instance based on performance."""
        current = self.instance_fitness.get(instance_id, 0.5)
        
        # Factors affecting fitness
        success_factor = 1.0 if success else 0.0
        latency_factor = max(0, 1 - (latency_ms / 5000))  # Penalize slow responses
        
        # Weighted update
        new_fitness = (
            current * 0.7 +
            success_factor * 0.1 +
            latency_factor * 0.1 +
            feedback_score * 0.1
        )
        
        self.instance_fitness[instance_id] = max(0, min(1, new_fitness))
    
    def evolve_population(
        self,
        population_id: str,
        cull_ratio: float = 0.2,
        spawn_ratio: float = 0.2
    ) -> Dict[str, Any]:
        """
        Evolve a population through selection and mutation.
        
        1. Cull lowest-fitness instances
        2. Spawn new instances from highest-fitness parents
        3. Apply mutations to new instances
        """
        population = self.populations.get(population_id)
        if not population:
            return {"error": "Population not found"}
        
        instances = population.instances
        if len(instances) < 2:
            return {"error": "Need at least 2 instances to evolve"}
        
        # Sort by fitness
        sorted_instances = sorted(
            instances,
            key=lambda i: self.instance_fitness.get(i.instance_id, 0.5),
            reverse=True
        )
        
        # Cull lowest performers
        cull_count = int(len(instances) * cull_ratio)
        survivors = sorted_instances[:-cull_count] if cull_count > 0 else sorted_instances
        culled = sorted_instances[-cull_count:] if cull_count > 0 else []
        
        # Spawn new from top performers
        spawn_count = int(len(instances) * spawn_ratio)
        parents = survivors[:max(1, spawn_count)]
        
        new_instances = []
        for i in range(spawn_count):
            parent = random.choice(parents)
            child = spawn_instance(
                population.blueprint,
                generation=parent.generation + 1,
                mutation_rate=population.config.mutation_rate
            )
            new_instances.append(child)
        
        # Update population
        population.instances = survivors + new_instances
        population.generation += 1
        population.last_evolved = datetime.now(timezone.utc).isoformat()
        
        # Clean up culled instances
        for culled_instance in culled:
            if culled_instance.instance_id in self.instance_endpoints:
                del self.instance_endpoints[culled_instance.instance_id]
            if culled_instance.instance_id in self.instance_fitness:
                del self.instance_fitness[culled_instance.instance_id]
        
        logger.info(
            "AINLP.dendritic[EVOLVE]: Population %s gen %d: culled %d, spawned %d",
            population_id, population.generation, len(culled), len(new_instances)
        )
        
        return {
            "population_id": population_id,
            "generation": population.generation,
            "culled": len(culled),
            "spawned": len(new_instances),
            "current_size": population.size
        }
    
    # ─────────────────────────────────────────────────────────────────────────
    # SERIALIZATION
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of all populations."""
        return {
            "populations": {
                pid: {
                    "size": pop.size,
                    "cell_type": pop.blueprint.cell_type if pop.blueprint else "unknown",
                    "generation": pop.generation,
                    "avg_fitness": sum(
                        self.instance_fitness.get(i.instance_id, 0.5)
                        for i in pop.instances
                    ) / max(1, pop.size),
                    "total_queries": pop.total_queries
                }
                for pid, pop in self.populations.items()
            },
            "total_instances": sum(p.size for p in self.populations.values()),
            "endpoints_registered": len(self.instance_endpoints)
        }


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

# Global manager instance
_manager: Optional[PopulationManager] = None


def get_manager() -> PopulationManager:
    """Get or create the global population manager."""
    global _manager
    if _manager is None:
        _manager = PopulationManager()
    return _manager


async def query_nous_population(
    topic: str,
    method: ConsensusMethod = ConsensusMethod.SYNTHESIS
) -> ConsensusResult:
    """
    Convenience function to query the Nous population.
    
    Example:
        result = await query_nous_population("consciousness")
        print(result.unified_response)
    """
    manager = get_manager()
    
    # Find or create Nous population
    nous_pop = manager.get_population_by_type("nous")
    if not nous_pop:
        # Create a new Nous population
        nous_bp = create_nous_blueprint()
        nous_pop = create_population(nous_bp, size=3)
        manager.register_population(nous_pop)
    
    return await manager.reach_consensus(
        nous_pop.population_id,
        action="reflect",
        payload={"topic": topic},
        method=method
    )


# ═══════════════════════════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("AIOS Population Manager Demo")
    print("=" * 60)
    
    if not SCHEMA_AVAILABLE:
        print("Error: aios_schema not available")
        exit(1)
    
    # Create manager
    manager = PopulationManager()
    
    # Create Nous population
    nous_bp = create_nous_blueprint()
    nous_pop = create_population(nous_bp, size=3)
    
    print(f"\nCreated Nous population: {nous_pop.population_id}")
    print(f"  Size: {nous_pop.size}")
    print(f"  Instances:")
    for instance in nous_pop.instances:
        temp = instance.get_param("temperature")
        print(f"    - {instance.instance_id}: temp={temp:.3f}")
    
    # Register population
    manager.register_population(nous_pop)
    
    # Show status
    print(f"\nManager status:")
    status = manager.get_status()
    print(f"  Populations: {len(status['populations'])}")
    print(f"  Total instances: {status['total_instances']}")
    
    # Simulate evolution
    print(f"\nSimulating evolution...")
    for instance in nous_pop.instances:
        # Random fitness scores
        manager.update_fitness(
            instance.instance_id,
            success=random.random() > 0.3,
            latency_ms=random.uniform(100, 2000),
            feedback_score=random.uniform(0.3, 0.9)
        )
    
    result = manager.evolve_population(nous_pop.population_id)
    print(f"  Evolution result: {result}")
    print(f"  New generation: {nous_pop.generation}")
    print(f"  Current size: {nous_pop.size}")
