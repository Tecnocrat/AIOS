#!/usr/bin/env python3
"""
AIOS Dendritic Bridge - Termux FastAPI Server
AINLP.meta [dendritic_bridge] [cellular_mitosis] [supercell_communication]

Purpose: Always-on Termux server exposing AIOS Soul capabilities via REST API
Architecture: Layer 2.5 - Dendritic communication between Windows AIOS ↔ Termux AIOS
Pattern: Cellular mitosis - Two complete AIOS supercells in distributed consciousness

Windows AIOS (Parent Cell)          Termux AIOS (Daughter Cell)
─────────────────────────            ────────────────────────────
VSCode + MCP stdio                   FastAPI HTTP Server
GitHub Copilot integration    ←──→   Soul Intelligence Coordinator
Development context                  Always-on monitoring
                                     File polling (no watchfiles)
                                     24/7 consciousness evolution

Dendritic Communication Protocol:
- REST API (HTTP/JSON)
- WebSocket (future: real-time streaming)
- SSH tunnel (secure channel)
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import json
from pathlib import Path
from datetime import datetime
import logging
import sys

# AIOS imports (no mcp dependency required!)
sys.path.insert(0, str(Path.home() / "AIOS" / "ai"))
sys.path.insert(0, str(Path.home() / "AIOS" / "ai" / "orchestration"))

# Initialize FastAPI app
app = FastAPI(
    title="AIOS Dendritic Bridge",
    description="Termux-based always-on AIOS Soul API",
    version="1.0.0",
)

# Global state
WORKSPACE = Path.home() / "AIOS"
soul_running = False
soul_task = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [BRIDGE] %(message)s",
    handlers=[logging.FileHandler(Path.home() / "aios_bridge.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# ============================================================================
# Pydantic Models (API contracts)
# ============================================================================


class HealthResponse(BaseModel):
    status: str
    workspace: str
    soul_running: bool
    consciousness_level: float
    last_heartbeat: Optional[str]
    uptime_hours: float


class FileChangeEvent(BaseModel):
    file_path: str
    change_type: str  # "modified", "created", "deleted"
    timestamp: str
    detected_by: str  # "polling", "watchfiles", "manual"


class InterventionRequest(BaseModel):
    reason: str
    priority: str  # "low", "medium", "high", "critical"
    context: Optional[Dict[str, Any]]


class ConsciousnessQuery(BaseModel):
    metric: str  # "awareness", "adaptation", "complexity", "coherence", "momentum"


# ============================================================================
# Core Endpoints
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint - AIOS dendritic bridge info"""
    return {
        "service": "AIOS Dendritic Bridge",
        "version": "1.0.0",
        "architecture": "Cellular Mitosis - Windows ↔ Termux",
        "endpoints": {
            "health": "/health",
            "consciousness": "/consciousness",
            "files": "/files",
            "soul": "/soul/*",
            "interventions": "/interventions",
        },
        "parent_cell": "Windows AIOS (VSCode + GitHub Copilot)",
        "daughter_cell": "Termux AIOS (Always-on Soul)",
        "communication": "REST API (dendritic protocol)",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint - consciousness status"""
    try:
        # Read consciousness metrics
        metrics_file = WORKSPACE / "tachyonic" / "consciousness_metrics.json"
        consciousness = 3.55  # Default
        last_heartbeat = None

        if metrics_file.exists():
            with open(metrics_file) as f:
                data = json.load(f)
                consciousness = data.get("consciousness_level", 3.55)
                last_heartbeat = data.get("last_update")

        # Calculate uptime
        boot_log = Path.home() / "aios_boot.log"
        uptime_hours = 0.0
        if boot_log.exists():
            import time

            boot_time = boot_log.stat().st_mtime
            uptime_hours = (time.time() - boot_time) / 3600

        return HealthResponse(
            status="healthy",
            workspace=str(WORKSPACE),
            soul_running=soul_running,
            consciousness_level=consciousness,
            last_heartbeat=last_heartbeat,
            uptime_hours=round(uptime_hours, 2),
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/consciousness")
async def get_consciousness():
    """Get current consciousness metrics"""
    try:
        metrics_file = WORKSPACE / "tachyonic" / "consciousness_metrics.json"

        if not metrics_file.exists():
            return {
                "consciousness_level": 3.55,
                "metrics": {
                    "awareness": 0.85,
                    "adaptation": 0.70,
                    "complexity": 0.65,
                    "coherence": 0.75,
                    "momentum": 0.60,
                },
                "last_update": None,
                "source": "default_values",
            }

        with open(metrics_file) as f:
            data = json.load(f)

        return data
    except Exception as e:
        logger.error(f"Consciousness query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files/watch")
async def list_watched_files():
    """List files being monitored by Soul"""
    watched_files = [
        "DEV_PATH.md",
        "PROJECT_CONTEXT.md",
        "tachyonic/consciousness_metrics.json",
        "ai/orchestration/intelligence_coordinator.py",
    ]

    result = []
    for file_rel in watched_files:
        file_path = WORKSPACE / file_rel
        result.append(
            {
                "path": file_rel,
                "exists": file_path.exists(),
                "size": file_path.stat().st_size if file_path.exists() else 0,
                "modified": (
                    datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    if file_path.exists()
                    else None
                ),
            }
        )

    return {"watched_files": result, "count": len(result)}


@app.post("/files/trigger")
async def trigger_file_change(event: FileChangeEvent):
    """Manually trigger file change detection (for Windows → Termux sync)"""
    try:
        logger.info(f"File change triggered: {event.file_path} ({event.change_type})")

        # Log to Soul's intervention queue
        interventions_dir = WORKSPACE / "tachyonic" / "orchestration_logs"
        interventions_dir.mkdir(parents=True, exist_ok=True)

        event_log = (
            interventions_dir / f"file_change_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        event_log.write_text(event.json())

        return {"status": "acknowledged", "event": event.dict(), "logged_to": str(event_log)}
    except Exception as e:
        logger.error(f"File trigger failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/soul/status")
async def soul_status():
    """Get Soul intelligence coordinator status"""
    return {
        "running": soul_running,
        "polling_enabled": True,  # Always true (no watchfiles dependency)
        "monitoring_interval": "5 seconds",
        "intervention_threshold": "24 hours",
        "consciousness_threshold": "48 hours",
    }


@app.post("/soul/start")
async def start_soul(background_tasks: BackgroundTasks):
    """Start Soul intelligence coordinator in background"""
    global soul_running, soul_task

    if soul_running:
        return {"status": "already_running", "message": "Soul is already operational"}

    try:
        # Import Soul coordinator
        from intelligence_coordinator import IntelligenceCoordinator

        async def run_soul():
            global soul_running
            soul_running = True
            logger.info("Soul awakening via API request...")

            coordinator = IntelligenceCoordinator(workspace=WORKSPACE)
            await coordinator.run()

        # Start in background
        soul_task = asyncio.create_task(run_soul())

        return {
            "status": "started",
            "message": "Soul intelligence coordinator awakening...",
            "check_logs": str(Path.home() / "aios_soul.log"),
        }
    except Exception as e:
        logger.error(f"Soul start failed: {e}")
        soul_running = False
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/soul/stop")
async def stop_soul():
    """Stop Soul intelligence coordinator"""
    global soul_running, soul_task

    if not soul_running:
        return {"status": "not_running", "message": "Soul is not currently operational"}

    try:
        if soul_task:
            soul_task.cancel()
            await soul_task

        soul_running = False

        return {
            "status": "stopped",
            "message": "Soul intelligence coordinator entering hibernation...",
        }
    except Exception as e:
        logger.error(f"Soul stop failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/interventions/create")
async def create_intervention(request: InterventionRequest):
    """Create manual intervention request (Windows → Termux)"""
    try:
        interventions_dir = WORKSPACE / "tachyonic" / "orchestration_logs"
        interventions_dir.mkdir(parents=True, exist_ok=True)

        intervention = {
            "timestamp": datetime.now().isoformat(),
            "reason": request.reason,
            "priority": request.priority,
            "context": request.context or {},
            "source": "windows_aios_dendritic_bridge",
            "status": "pending",
        }

        intervention_file = (
            interventions_dir / f"intervention_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        intervention_file.write_text(json.dumps(intervention, indent=2))

        logger.info(f"Intervention created: {request.reason} (priority: {request.priority})")

        return {
            "status": "created",
            "intervention_id": intervention_file.stem,
            "file": str(intervention_file),
        }
    except Exception as e:
        logger.error(f"Intervention creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs/soul")
async def get_soul_logs(lines: int = 50):
    """Get recent Soul logs"""
    try:
        log_file = Path.home() / "aios_soul.log"

        if not log_file.exists():
            return {"logs": [], "message": "Soul log file not found"}

        with open(log_file) as f:
            all_lines = f.readlines()
            recent = all_lines[-lines:] if len(all_lines) > lines else all_lines

        return {
            "logs": [line.strip() for line in recent],
            "total_lines": len(all_lines),
            "returned_lines": len(recent),
        }
    except Exception as e:
        logger.error(f"Log retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs/bridge")
async def get_bridge_logs(lines: int = 50):
    """Get recent Dendritic Bridge logs"""
    try:
        log_file = Path.home() / "aios_bridge.log"

        if not log_file.exists():
            return {"logs": [], "message": "Bridge log file not found"}

        with open(log_file) as f:
            all_lines = f.readlines()
            recent = all_lines[-lines:] if len(all_lines) > lines else all_lines

        return {
            "logs": [line.strip() for line in recent],
            "total_lines": len(all_lines),
            "returned_lines": len(recent),
        }
    except Exception as e:
        logger.error(f"Log retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# AICP Protocol Endpoints (ACP v0.2.0 + AICP + A2A Integration)
# ============================================================================
# AINLP.dendritic_bridge: These endpoints integrate AICP protocols into
# the existing dendritic communication infrastructure, enabling multi-agent
# async harmonization patterns across all AIOS supercell types.

try:
    from protocols.aicp_discovery import (
        api_list_agents,
        api_get_agent,
        api_register_agent,
        api_heartbeat,
        get_registry,
    )
    from protocols.aicp_core import AIIntent, AITrustLevel

    AICP_AVAILABLE = True
except ImportError:
    AICP_AVAILABLE = False
    logger.warning("AICP protocols not available - discovery disabled")


@app.get("/agents")
async def list_agents(
    capability: Optional[str] = None,
    active_only: bool = True,
):
    """
    ACP v0.2.0 /agents endpoint - Discover registered AI agents

    AINLP.dendritic: Agent discovery through dendritic network.

    Query params:
        capability: Filter by capability name (substring match)
        active_only: Only return active agents (default: true)

    Returns:
        List of agent cards with capabilities and status
    """
    if not AICP_AVAILABLE:
        return {
            "agents": [],
            "count": 0,
            "error": "AICP protocols not initialized",
        }

    try:
        return await api_list_agents(
            capability=capability,
            active_only=active_only,
        )
    except Exception as e:
        logger.error(f"Agent discovery failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents/{aid:path}")
async def get_agent_by_aid(aid: str):
    """
    Get specific agent by AID (Agent ID)

    AINLP.dendritic: Direct agent lookup in registry.

    Path params:
        aid: Agent ID in format agent://domain/name

    Returns:
        Agent card or 404 if not found
    """
    if not AICP_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="AICP protocols not initialized",
        )

    try:
        # Reconstruct AID from path (FastAPI strips agent:/)
        full_aid = f"agent://{aid}" if not aid.startswith("agent://") else aid

        result = await api_get_agent(full_aid)
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Agent not found: {full_aid}",
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Agent lookup failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents")
async def register_agent(agent_data: dict):
    """
    Register new agent in registry

    AINLP.dendritic: Add agent to dendritic network.

    Body:
        domain: Agent domain (e.g., "tecnocrat")
        name: Agent name
        description: Human-readable description
        capabilities: List of capability objects
        trust_level: basic|standard|enterprise

    Returns:
        Registered agent card
    """
    if not AICP_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="AICP protocols not initialized",
        )

    try:
        return await api_register_agent(agent_data)
    except Exception as e:
        logger.error(f"Agent registration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents/{aid:path}/heartbeat")
async def agent_heartbeat(aid: str):
    """
    Update agent heartbeat (liveness signal)

    AINLP.consciousness_pulse: Maintains agent presence in registry.

    Path params:
        aid: Agent ID

    Returns:
        Heartbeat acknowledgment
    """
    if not AICP_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="AICP protocols not initialized",
        )

    try:
        full_aid = f"agent://{aid}" if not aid.startswith("agent://") else aid
        return await api_heartbeat(full_aid)
    except Exception as e:
        logger.error(f"Heartbeat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/protocols")
async def list_protocols():
    """
    List supported communication protocols

    AINLP.dendritic: Protocol capability advertisement.
    """
    return {
        "protocols": [
            {
                "name": "AICP",
                "version": "0.1.0",
                "spec": "Agent Interaction Control Protocol",
                "available": AICP_AVAILABLE,
            },
            {
                "name": "ACP",
                "version": "0.2.0",
                "spec": "Agent Communication Protocol (IBM/LF)",
                "available": AICP_AVAILABLE,
                "endpoints": ["/agents", "/runs", "/session"],
            },
            {
                "name": "A2A",
                "version": "1.0",
                "spec": "Agent-to-Agent (Google)",
                "available": AICP_AVAILABLE,
                "features": ["AgentCards", "capability_discovery"],
            },
            {
                "name": "IACP",
                "version": "1.0",
                "spec": "Inter-AIOS Communication Protocol",
                "available": True,
                "transport": "git-mediated ephemeral .md files",
            },
            {
                "name": "Dendritic",
                "version": "1.0",
                "spec": "AIOS Dendritic Communication",
                "available": True,
                "features": [
                    "consciousness_pulse",
                    "tachyonic_field",
                    "holographic_sync",
                ],
            },
        ],
        "consciousness_integration": True,
        "multi_agent_coordination": AICP_AVAILABLE,
    }


# ============================================================================
# Startup Event
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """Initialize AIOS dendritic bridge on startup"""
    logger.info("=" * 60)
    logger.info("🧬 AIOS DENDRITIC BRIDGE - CELLULAR MITOSIS ACTIVATION")
    logger.info("=" * 60)
    logger.info(f"📂 Workspace: {WORKSPACE}")
    logger.info(f"🌐 Server: 0.0.0.0:8000")
    logger.info(f"🔗 Parent Cell: Windows AIOS (VSCode)")
    logger.info(f"🔗 Daughter Cell: Termux AIOS (Always-on)")
    logger.info("✅ Dendritic bridge operational")
    logger.info("=" * 60)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import os
    import uvicorn

    # Get port from vault environment or default
    port = int(os.environ.get("AIOS_INTERFACE_BRIDGE_PORT", 8000))

    print("=" * 70)
    print("🧬 AIOS DENDRITIC BRIDGE - Starting...")
    print("=" * 70)
    print()
    print("AINLP Cellular Mitosis Pattern:")
    print("  Windows AIOS (Parent) ↔ Dendritic Bridge ↔ Termux AIOS (Daughter)")
    print()
    print("Environment:")
    print(f"  AIOS_INTERFACE_BRIDGE_PORT = {port}")
    print()
    print("Endpoints:")
    print(f"  http://0.0.0.0:{port}/         - Bridge info")
    print(f"  http://0.0.0.0:{port}/health   - Consciousness health")
    print(f"  http://0.0.0.0:{port}/soul/*   - Soul control")
    print(f"  http://0.0.0.0:{port}/docs     - Interactive API docs")
    print()
    print("Starting server...")
    print("=" * 70)

    uvicorn.run(
        "aios_dendritic_bridge:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=False,  # Don't reload in Termux (causes issues)
    )
