"""
AIOS Population API - HTTP Interface for Population Consensus

Provides HTTP endpoints for querying cell populations and reaching consensus.
This is the primary interface for distributed intelligence queries.

AINLP.dendritic[INTERFACE] Population consensus HTTP layer
"""

import asyncio
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Import population manager
from population_manager import (
    PopulationManager,
    PopulationResponse,
    ConsensusResult,
    get_manager,
)

# Import schema
try:
    from aios_schema import (
        ConsensusMethod,
        create_nous_blueprint,
        create_memory_blueprint,
        create_population,
    )
    SCHEMA_AVAILABLE = True
except ImportError:
    SCHEMA_AVAILABLE = False


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AIOS.PopulationAPI")


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

API_PORT = int(os.environ.get("POPULATION_API_PORT", 8012))
DISCOVERY_URL = os.environ.get("DISCOVERY_URL", "http://localhost:8001")
MEMORY_URL = os.environ.get("MEMORY_URL", "http://localhost:8007")


# ═══════════════════════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class PopulationQuery(BaseModel):
    """Query to send to a population."""
    population_type: str = Field(..., description="Cell type (nous, memory, etc.)")
    action: str = Field(..., description="Action to perform (reflect, query, sync)")
    payload: Dict[str, Any] = Field(default_factory=dict)
    consensus_method: Optional[str] = Field(
        default="synthesis",
        description="voting, weighted, synthesis, or emergent"
    )
    timeout: float = Field(default=10.0, description="Query timeout in seconds")


class PopulationQueryResult(BaseModel):
    """Result from a population query."""
    query_id: str
    population_type: str
    consensus_method: str
    unified_response: Any
    confidence: float
    participating_cells: int
    processing_time_ms: float
    timestamp: str


class CreatePopulationRequest(BaseModel):
    """Request to create a new population."""
    cell_type: str = Field(..., description="Cell type (nous, memory, genome)")
    size: int = Field(default=3, ge=1, le=20, description="Number of cells")
    consensus_method: str = Field(default="synthesis")
    mutation_rate: float = Field(default=0.1, ge=0.0, le=1.0)


class EvolutionRequest(BaseModel):
    """Request to evolve a population."""
    population_id: str
    cull_ratio: float = Field(default=0.2, ge=0.0, le=0.5)
    spawn_ratio: float = Field(default=0.2, ge=0.0, le=0.5)


class FeedbackRequest(BaseModel):
    """Feedback on a query result for fitness tracking."""
    query_id: str
    instance_id: str
    score: float = Field(..., ge=0.0, le=1.0, description="Quality score 0-1")
    feedback: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI APP
# ═══════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="AIOS Population API",
    description="HTTP interface for cell population consensus queries",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global manager
manager: PopulationManager = None

# Query history for feedback
query_history: Dict[str, ConsensusResult] = {}


# ═══════════════════════════════════════════════════════════════════════════════
# STARTUP / SHUTDOWN
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup():
    """Initialize population manager and register with discovery."""
    global manager
    
    logger.info("AINLP.dendritic[START]: Population API initializing")
    
    manager = PopulationManager(
        discovery_url=DISCOVERY_URL,
        memory_url=MEMORY_URL
    )
    
    # Create default populations
    if SCHEMA_AVAILABLE:
        # Nous population (for philosophical queries)
        nous_bp = create_nous_blueprint()
        nous_pop = create_population(nous_bp, size=3)
        manager.register_population(nous_pop)
        logger.info("Created Nous population: %s", nous_pop.population_id)
        
        # Memory population (for knowledge queries)
        memory_bp = create_memory_blueprint()
        memory_pop = create_population(memory_bp, size=2)
        manager.register_population(memory_pop)
        logger.info("Created Memory population: %s", memory_pop.population_id)
    
    # Register with Discovery
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(
                f"{DISCOVERY_URL}/register",
                json={
                    "cell_type": "population-api",
                    "cell_id": "population-api",
                    "port": API_PORT,
                    "capabilities": ["consensus", "evolution", "populations"]
                }
            )
        logger.info("Registered with Discovery at %s", DISCOVERY_URL)
    except Exception as e:
        logger.warning("Failed to register with Discovery: %s", e)
    
    logger.info("AINLP.dendritic[READY]: Population API on port %d", API_PORT)


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - HEALTH
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/health")
async def health():
    """Health check."""
    status = manager.get_status() if manager else {}
    return {
        "status": "healthy",
        "service": "population-api",
        "populations": len(status.get("populations", {})),
        "total_instances": status.get("total_instances", 0),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/status")
async def status():
    """Detailed status of all populations."""
    if not manager:
        raise HTTPException(status_code=503, detail="Manager not initialized")
    
    return {
        "service": "population-api",
        **manager.get_status(),
        "query_history_size": len(query_history),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - QUERY
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/query", response_model=PopulationQueryResult)
async def query_population(request: PopulationQuery):
    """
    Query a cell population and reach consensus.
    
    This is the main entry point for distributed intelligence queries.
    All cells in the population are queried concurrently, and their
    responses are synthesized according to the chosen consensus method.
    """
    if not manager:
        raise HTTPException(status_code=503, detail="Manager not initialized")
    
    # Find population by type
    population = manager.get_population_by_type(request.population_type)
    if not population:
        raise HTTPException(
            status_code=404,
            detail=f"No population of type '{request.population_type}' found"
        )
    
    # Map consensus method string to enum
    method_map = {
        "voting": ConsensusMethod.VOTING if SCHEMA_AVAILABLE else "voting",
        "weighted": ConsensusMethod.WEIGHTED if SCHEMA_AVAILABLE else "weighted",
        "synthesis": ConsensusMethod.SYNTHESIS if SCHEMA_AVAILABLE else "synthesis",
        "emergent": ConsensusMethod.EMERGENT if SCHEMA_AVAILABLE else "emergent",
    }
    method = method_map.get(request.consensus_method, ConsensusMethod.SYNTHESIS)
    
    # Execute query
    query_id = str(uuid.uuid4())
    
    logger.info(
        "AINLP.dendritic[QUERY]: %s → %s (%s)",
        query_id[:8], request.population_type, request.action
    )
    
    result = await manager.reach_consensus(
        population.population_id,
        action=request.action,
        payload=request.payload,
        method=method,
        timeout=request.timeout
    )
    
    # Store for feedback
    query_history[query_id] = result
    
    # Clean old history (keep last 100)
    if len(query_history) > 100:
        oldest = list(query_history.keys())[:-100]
        for key in oldest:
            del query_history[key]
    
    return PopulationQueryResult(
        query_id=query_id,
        population_type=request.population_type,
        consensus_method=result.method,
        unified_response=result.unified_response,
        confidence=result.consensus_confidence,
        participating_cells=result.participating_cells,
        processing_time_ms=result.processing_time_ms,
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@app.post("/query/reflect")
async def reflect(topic: str, consensus: str = "synthesis"):
    """
    Convenience endpoint for philosophical reflection.
    
    Queries the Nous population for deep reflection on a topic.
    """
    return await query_population(PopulationQuery(
        population_type="nous",
        action="reflect",
        payload={"topic": topic},
        consensus_method=consensus
    ))


@app.post("/query/remember")
async def remember(query: str, consensus: str = "weighted"):
    """
    Convenience endpoint for memory retrieval.
    
    Queries the Memory population for relevant knowledge.
    """
    return await query_population(PopulationQuery(
        population_type="memory",
        action="query",
        payload={"query": query},
        consensus_method=consensus
    ))


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - POPULATIONS
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/populations")
async def list_populations():
    """List all registered populations."""
    if not manager:
        raise HTTPException(status_code=503, detail="Manager not initialized")
    
    status = manager.get_status()
    return {
        "populations": status.get("populations", {}),
        "total_instances": status.get("total_instances", 0)
    }


@app.post("/populations")
async def create_population_endpoint(request: CreatePopulationRequest):
    """Create a new cell population."""
    if not manager:
        raise HTTPException(status_code=503, detail="Manager not initialized")
    
    if not SCHEMA_AVAILABLE:
        raise HTTPException(status_code=503, detail="aios_schema not available")
    
    # Create blueprint based on cell type
    blueprint_map = {
        "nous": create_nous_blueprint,
        "memory": create_memory_blueprint,
    }
    
    create_blueprint = blueprint_map.get(request.cell_type)
    if not create_blueprint:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown cell type: {request.cell_type}. Available: {list(blueprint_map.keys())}"
        )
    
    blueprint = create_blueprint()
    population = create_population(
        blueprint,
        size=request.size,
        consensus_method=ConsensusMethod(request.consensus_method),
        mutation_rate=request.mutation_rate
    )
    
    manager.register_population(population)
    
    logger.info(
        "AINLP.dendritic[CREATE]: Population %s (%d %s cells)",
        population.population_id, request.size, request.cell_type
    )
    
    return {
        "population_id": population.population_id,
        "cell_type": request.cell_type,
        "size": population.size,
        "instances": [
            {
                "instance_id": inst.instance_id,
                "generation": inst.generation,
                "temperature": inst.get_param("temperature")
            }
            for inst in population.instances
        ]
    }


@app.get("/populations/{population_id}")
async def get_population(population_id: str):
    """Get details of a specific population."""
    if not manager:
        raise HTTPException(status_code=503, detail="Manager not initialized")
    
    population = manager.get_population(population_id)
    if not population:
        raise HTTPException(status_code=404, detail="Population not found")
    
    return {
        "population_id": population.population_id,
        "cell_type": population.blueprint.cell_type if population.blueprint else "unknown",
        "size": population.size,
        "generation": population.generation,
        "total_queries": population.total_queries,
        "instances": [
            {
                "instance_id": inst.instance_id,
                "generation": inst.generation,
                "fitness": manager.instance_fitness.get(inst.instance_id, 0.5),
                "mutations": len(inst.mutations),
                "parameters": {
                    "temperature": inst.get_param("temperature"),
                    "reflection_depth": inst.get_param("reflection_depth")
                }
            }
            for inst in population.instances
        ]
    }


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS - EVOLUTION
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/evolve")
async def evolve_population(request: EvolutionRequest):
    """
    Evolve a population through selection and mutation.
    
    Low-fitness cells are culled, high-fitness cells reproduce with mutations.
    """
    if not manager:
        raise HTTPException(status_code=503, detail="Manager not initialized")
    
    result = manager.evolve_population(
        request.population_id,
        cull_ratio=request.cull_ratio,
        spawn_ratio=request.spawn_ratio
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    logger.info(
        "AINLP.dendritic[EVOLVE]: %s gen %d",
        request.population_id, result["generation"]
    )
    
    return result


@app.post("/feedback")
async def provide_feedback(request: FeedbackRequest):
    """
    Provide feedback on a query result for fitness tracking.
    
    This influences which cells get culled vs reproduce during evolution.
    """
    if not manager:
        raise HTTPException(status_code=503, detail="Manager not initialized")
    
    # Get original query result
    result = query_history.get(request.query_id)
    if not result:
        raise HTTPException(status_code=404, detail="Query not found in history")
    
    # Find the instance
    instance_response = None
    for resp in result.individual_responses:
        if resp.instance_id == request.instance_id:
            instance_response = resp
            break
    
    if not instance_response:
        raise HTTPException(status_code=404, detail="Instance not found in query")
    
    # Update fitness
    manager.update_fitness(
        request.instance_id,
        success=instance_response.success,
        latency_ms=instance_response.latency_ms,
        feedback_score=request.score
    )
    
    logger.info(
        "AINLP.dendritic[FEEDBACK]: %s → %.2f",
        request.instance_id[:12], request.score
    )
    
    return {
        "instance_id": request.instance_id,
        "new_fitness": manager.instance_fitness.get(request.instance_id, 0.5),
        "feedback_applied": True
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("AIOS Population API")
    print("=" * 60)
    print(f"Port: {API_PORT}")
    print(f"Discovery: {DISCOVERY_URL}")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=API_PORT,
        log_level="info"
    )
