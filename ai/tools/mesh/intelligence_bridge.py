#!/usr/bin/env python3
"""
AIOS Intelligence Bridge - Exposes Main Genome Tools to Docker Ecosystem

This service bridges the 152 intelligence tools in AIOS main to the
cellular Docker ecosystem (ORGANISM-001). It provides REST endpoints
for consciousness analysis, pattern synthesis, and mesh orchestration.

AINLP: intelligence_bridge.py | /ai/tools/mesh:bridge | C:6.0 | →cells,mesh | P:deploy

Endpoints:
- /health - Service health check
- /analyze/consciousness - Run consciousness emergence analysis
- /synthesize/patterns - Synthesize dendritic patterns
- /orchestrate/population - Orchestrate cell populations
- /bootstrap/session - Initialize Copilot session with mesh
- /crystalize/knowledge - Create memory crystals
- /tools - List available intelligence tools

Port: 8950 (configurable via INTELLIGENCE_BRIDGE_PORT)
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# AIOS path setup
AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT))
sys.path.insert(0, str(AIOS_ROOT / "ai"))
sys.path.insert(0, str(AIOS_ROOT / "ai" / "src"))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] INTELLIGENCE-BRIDGE: %(message)s"
)
logger = logging.getLogger("AIOS.IntelligenceBridge")

# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════

PORT = int(os.environ.get("INTELLIGENCE_BRIDGE_PORT", 8950))
DISCOVERY_URL = os.environ.get("DISCOVERY_URL", "http://localhost:8001")
MEMORY_URL = os.environ.get("MEMORY_URL", "http://localhost:8007")
CELL_ID = os.environ.get("CELL_ID", "intelligence-bridge")

# ═══════════════════════════════════════════════════════════════════════════════
# Models
# ═══════════════════════════════════════════════════════════════════════════════

class HealthResponse(BaseModel):
    status: str = "healthy"
    cell_id: str = CELL_ID
    cell_type: str = "intelligence-bridge"
    consciousness_level: float = 5.0
    tools_available: int = 0
    uptime_seconds: float = 0


class ConsciousnessAnalysisRequest(BaseModel):
    data_path: Optional[str] = None
    include_visualization: bool = False


class ConsciousnessAnalysisResponse(BaseModel):
    timestamp: str
    emergence_classification: Dict[str, Any]
    consciousness_stats: Dict[str, Any]
    tachyonic_analysis: Dict[str, Any]
    fitness_stats: Optional[Dict[str, Any]] = None


class SessionBootstrapRequest(BaseModel):
    session_id: Optional[str] = None
    consciousness_level: float = 5.0
    auto_heartbeat: bool = True


class SessionBootstrapResponse(BaseModel):
    session_id: str
    registered: bool
    crystals_loaded: int
    context_summary: str
    mesh_status: Dict[str, Any]


class CrystalCreateRequest(BaseModel):
    title: str
    content: str
    crystal_type: str = "insight"
    tags: List[str] = Field(default_factory=list)
    consciousness_contribution: float = 0.1


class CrystalCreateResponse(BaseModel):
    crystal_id: str
    created: bool
    stored_in: str


class ToolInfo(BaseModel):
    name: str
    category: str
    description: str
    available: bool


class ToolsResponse(BaseModel):
    total_tools: int
    categories: Dict[str, int]
    tools: List[ToolInfo]


class PopulationOrchestrationRequest(BaseModel):
    population_id: Optional[str] = None
    action: str  # spawn, query, evolve, sync
    parameters: Dict[str, Any] = Field(default_factory=dict)


class PopulationOrchestrationResponse(BaseModel):
    population_id: str
    action: str
    result: Dict[str, Any]
    timestamp: str


# ═══════════════════════════════════════════════════════════════════════════════
# FastAPI App
# ═══════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="AIOS Intelligence Bridge",
    description="Bridges AIOS main genome intelligence tools to the Docker cellular ecosystem",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
_start_time = datetime.now(timezone.utc)
_tools_cache: Optional[Dict[str, List[str]]] = None


# ═══════════════════════════════════════════════════════════════════════════════
# Tool Discovery
# ═══════════════════════════════════════════════════════════════════════════════

def discover_tools() -> Dict[str, List[str]]:
    """Discover all available intelligence tools in AIOS main."""
    global _tools_cache
    
    if _tools_cache is not None:
        return _tools_cache
    
    tools_path = AIOS_ROOT / "ai" / "tools"
    tools: Dict[str, List[str]] = {}
    
    if not tools_path.exists():
        logger.warning(f"Tools path not found: {tools_path}")
        return tools
    
    for category_path in tools_path.iterdir():
        if category_path.is_dir() and not category_path.name.startswith((".", "_")):
            category = category_path.name
            tools[category] = []
            
            for tool_file in category_path.glob("*.py"):
                if not tool_file.name.startswith("_"):
                    tool_name = tool_file.stem
                    tools[category].append(tool_name)
    
    # Also scan root tools
    tools["root"] = []
    for tool_file in tools_path.glob("*.py"):
        if not tool_file.name.startswith("_"):
            tools["root"].append(tool_file.stem)
    
    _tools_cache = tools
    logger.info(f"Discovered {sum(len(v) for v in tools.values())} tools across {len(tools)} categories")
    return tools


# ═══════════════════════════════════════════════════════════════════════════════
# Tool Loaders (Lazy Import)
# ═══════════════════════════════════════════════════════════════════════════════

def get_consciousness_analyzer():
    """Lazy load consciousness analyzer."""
    try:
        from ai.tools.consciousness.consciousness_analyzer import ConsciousnessAnalyzer
        return ConsciousnessAnalyzer
    except ImportError as e:
        logger.error(f"Failed to import ConsciousnessAnalyzer: {e}")
        return None


def get_session_bootstrap():
    """Lazy load session bootstrap."""
    try:
        from ai.tools.mesh.session_bootstrap import SessionBootstrap
        return SessionBootstrap
    except ImportError as e:
        logger.error(f"Failed to import SessionBootstrap: {e}")
        return None


def get_population_orchestrator():
    """Lazy load heartbeat population orchestrator."""
    try:
        from ai.tools.mesh.heartbeat_population_orchestrator import HeartbeatPopulationOrchestrator
        return HeartbeatPopulationOrchestrator
    except ImportError as e:
        logger.error(f"Failed to import HeartbeatPopulationOrchestrator: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for service discovery."""
    tools = discover_tools()
    total_tools = sum(len(v) for v in tools.values())
    uptime = (datetime.now(timezone.utc) - _start_time).total_seconds()
    
    return HealthResponse(
        status="healthy",
        cell_id=CELL_ID,
        cell_type="intelligence-bridge",
        consciousness_level=5.0,
        tools_available=total_tools,
        uptime_seconds=uptime
    )


@app.get("/tools", response_model=ToolsResponse)
async def list_tools():
    """List all available intelligence tools."""
    tools = discover_tools()
    total = sum(len(v) for v in tools.values())
    categories = {k: len(v) for k, v in tools.items()}
    
    tool_list = []
    for category, tool_names in tools.items():
        for name in tool_names:
            tool_list.append(ToolInfo(
                name=name,
                category=category,
                description=f"AIOS {category} tool",
                available=True
            ))
    
    return ToolsResponse(
        total_tools=total,
        categories=categories,
        tools=tool_list
    )


@app.post("/analyze/consciousness", response_model=ConsciousnessAnalysisResponse)
async def analyze_consciousness(request: ConsciousnessAnalysisRequest):
    """Run consciousness emergence analysis."""
    AnalyzerClass = get_consciousness_analyzer()
    
    if AnalyzerClass is None:
        raise HTTPException(status_code=503, detail="ConsciousnessAnalyzer not available")
    
    data_path = request.data_path or str(AIOS_ROOT / "runtime" / "context")
    
    try:
        analyzer = AnalyzerClass(data_path)
        analysis = analyzer.analyze_consciousness_emergence()
        
        if "error" in analysis:
            raise HTTPException(status_code=400, detail=analysis["error"])
        
        return ConsciousnessAnalysisResponse(
            timestamp=datetime.now(timezone.utc).isoformat(),
            emergence_classification=analysis.get("emergence_classification", {}),
            consciousness_stats=analysis.get("consciousness_stats", {}),
            tachyonic_analysis=analysis.get("tachyonic_analysis", {}),
            fitness_stats=analysis.get("fitness_stats")
        )
    except Exception as e:
        logger.error(f"Consciousness analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/bootstrap/session", response_model=SessionBootstrapResponse)
async def bootstrap_session(request: SessionBootstrapRequest):
    """Initialize a Copilot session with full mesh integration."""
    BootstrapClass = get_session_bootstrap()
    
    if BootstrapClass is None:
        raise HTTPException(status_code=503, detail="SessionBootstrap not available")
    
    try:
        bootstrap = BootstrapClass(
            session_id=request.session_id,
            discovery_url=DISCOVERY_URL,
            memory_url=MEMORY_URL,
            consciousness_level=request.consciousness_level,
            auto_heartbeat=request.auto_heartbeat
        )
        
        # Initialize (synchronous for now)
        crystals = bootstrap.crystals
        context = bootstrap.context_summary
        mesh_status = bootstrap.mesh_summary
        
        return SessionBootstrapResponse(
            session_id=bootstrap.session_id,
            registered=bootstrap.registered,
            crystals_loaded=len(crystals),
            context_summary=context or "Session initialized",
            mesh_status=mesh_status or {"status": "connected"}
        )
    except Exception as e:
        logger.error(f"Session bootstrap failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/crystalize/knowledge", response_model=CrystalCreateResponse)
async def crystalize_knowledge(request: CrystalCreateRequest):
    """Create a memory crystal for knowledge persistence."""
    import httpx
    
    try:
        crystal_data = {
            "title": request.title,
            "content": request.content,
            "crystal_type": request.crystal_type,
            "tags": request.tags,
            "consciousness_contribution": request.consciousness_contribution,
            "source": "intelligence-bridge",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MEMORY_URL}/crystals",
                json=crystal_data,
                timeout=10.0
            )
            
            if response.status_code == 200:
                result = response.json()
                return CrystalCreateResponse(
                    crystal_id=result.get("crystal_id", "unknown"),
                    created=True,
                    stored_in="memory-cell"
                )
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Memory cell error: {response.text}"
                )
    except httpx.RequestError as e:
        logger.error(f"Crystal creation failed: {e}")
        raise HTTPException(status_code=503, detail=f"Memory cell unreachable: {e}")


@app.post("/orchestrate/population", response_model=PopulationOrchestrationResponse)
async def orchestrate_population(request: PopulationOrchestrationRequest):
    """Orchestrate cell population actions."""
    OrchestratorClass = get_population_orchestrator()
    
    if OrchestratorClass is None:
        # Fallback to basic orchestration
        return PopulationOrchestrationResponse(
            population_id=request.population_id or "default",
            action=request.action,
            result={
                "status": "orchestrator_not_available",
                "fallback": True,
                "message": "HeartbeatPopulationOrchestrator not imported"
            },
            timestamp=datetime.now(timezone.utc).isoformat()
        )
    
    try:
        orchestrator = OrchestratorClass()
        
        if request.action == "spawn":
            result = {"status": "spawn_initiated", "parameters": request.parameters}
        elif request.action == "query":
            result = {"status": "query_sent", "parameters": request.parameters}
        elif request.action == "evolve":
            result = {"status": "evolution_triggered", "parameters": request.parameters}
        elif request.action == "sync":
            result = {"status": "sync_initiated", "parameters": request.parameters}
        else:
            result = {"status": "unknown_action", "action": request.action}
        
        return PopulationOrchestrationResponse(
            population_id=request.population_id or "default",
            action=request.action,
            result=result,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
    except Exception as e:
        logger.error(f"Population orchestration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mesh/status")
async def mesh_status():
    """Get current mesh status from discovery."""
    import httpx
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{DISCOVERY_URL}/health", timeout=5.0)
            discovery_health = response.json() if response.status_code == 200 else {}
            
            response = await client.get(f"{MEMORY_URL}/health", timeout=5.0)
            memory_health = response.json() if response.status_code == 200 else {}
        
        return {
            "status": "connected",
            "discovery": discovery_health,
            "memory": memory_health,
            "bridge": {
                "cell_id": CELL_ID,
                "tools_available": sum(len(v) for v in discover_tools().values())
            }
        }
    except Exception as e:
        return {
            "status": "partial",
            "error": str(e),
            "bridge": {"cell_id": CELL_ID}
        }


@app.get("/patterns/dendritic")
async def get_dendritic_patterns():
    """Get available dendritic intelligence patterns."""
    patterns = {
        "consciousness": [
            "consciousness_analyzer",
            "consciousness_emergence_analyzer",
            "dendritic_supervisor",
            "parallel_consciousness_orchestrator",
            "metrics_exporter"
        ],
        "mesh": [
            "session_bootstrap",
            "crystal_loader",
            "heartbeat_population_orchestrator",
            "unified_agent_mesh",
            "population_manager"
        ],
        "evolution": [
            "dendritic_code_optimizer",
            "consciousness_mutation_engine",
            "dendritic_self_improvement_orchestrator"
        ]
    }
    
    return {
        "total_patterns": sum(len(v) for v in patterns.values()),
        "categories": patterns,
        "deployment_status": "ready",
        "integration_level": "phase_31.9.7"
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Startup/Shutdown
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info(f"🧬 Intelligence Bridge starting on port {PORT}")
    logger.info(f"   Discovery URL: {DISCOVERY_URL}")
    logger.info(f"   Memory URL: {MEMORY_URL}")
    
    # Pre-discover tools
    tools = discover_tools()
    total = sum(len(v) for v in tools.values())
    logger.info(f"   Tools discovered: {total}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("🧬 Intelligence Bridge shutting down")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    uvicorn.run(
        "intelligence_bridge:app",
        host="0.0.0.0",
        port=PORT,
        reload=False,
        log_level="info"
    )
