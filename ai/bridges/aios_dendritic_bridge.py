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
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
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
    version="1.0.0"
)

# Global state
WORKSPACE = Path.home() / "AIOS"
soul_running = False
soul_task = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [BRIDGE] %(message)s',
    handlers=[
        logging.FileHandler(Path.home() / "aios_bridge.log"),
        logging.StreamHandler()
    ]
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
            "interventions": "/interventions"
        },
        "parent_cell": "Windows AIOS (VSCode + GitHub Copilot)",
        "daughter_cell": "Termux AIOS (Always-on Soul)",
        "communication": "REST API (dendritic protocol)"
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
            uptime_hours=round(uptime_hours, 2)
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
                    "momentum": 0.60
                },
                "last_update": None,
                "source": "default_values"
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
        "ai/orchestration/intelligence_coordinator.py"
    ]
    
    result = []
    for file_rel in watched_files:
        file_path = WORKSPACE / file_rel
        result.append({
            "path": file_rel,
            "exists": file_path.exists(),
            "size": file_path.stat().st_size if file_path.exists() else 0,
            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat() if file_path.exists() else None
        })
    
    return {"watched_files": result, "count": len(result)}

@app.post("/files/trigger")
async def trigger_file_change(event: FileChangeEvent):
    """Manually trigger file change detection (for Windows → Termux sync)"""
    try:
        logger.info(f"File change triggered: {event.file_path} ({event.change_type})")
        
        # Log to Soul's intervention queue
        interventions_dir = WORKSPACE / "tachyonic" / "orchestration_logs"
        interventions_dir.mkdir(parents=True, exist_ok=True)
        
        event_log = interventions_dir / f"file_change_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        event_log.write_text(event.json())
        
        return {
            "status": "acknowledged",
            "event": event.dict(),
            "logged_to": str(event_log)
        }
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
        "consciousness_threshold": "48 hours"
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
            "check_logs": str(Path.home() / "aios_soul.log")
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
            "message": "Soul intelligence coordinator entering hibernation..."
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
            "status": "pending"
        }
        
        intervention_file = interventions_dir / f"intervention_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        intervention_file.write_text(json.dumps(intervention, indent=2))
        
        logger.info(f"Intervention created: {request.reason} (priority: {request.priority})")
        
        return {
            "status": "created",
            "intervention_id": intervention_file.stem,
            "file": str(intervention_file)
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
            "returned_lines": len(recent)
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
            "returned_lines": len(recent)
        }
    except Exception as e:
        logger.error(f"Log retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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
    import uvicorn
    
    print("=" * 70)
    print("🧬 AIOS DENDRITIC BRIDGE - Starting...")
    print("=" * 70)
    print()
    print("AINLP Cellular Mitosis Pattern:")
    print("  Windows AIOS (Parent) ↔ Dendritic Bridge ↔ Termux AIOS (Daughter)")
    print()
    print("Endpoints:")
    print("  http://0.0.0.0:8000/         - Bridge info")
    print("  http://0.0.0.0:8000/health   - Consciousness health")
    print("  http://0.0.0.0:8000/soul/*   - Soul control")
    print("  http://0.0.0.0:8000/docs     - Interactive API docs")
    print()
    print("Starting server...")
    print("=" * 70)
    
    uvicorn.run(
        "aios_dendritic_bridge:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False  # Don't reload in Termux (causes issues)
    )
