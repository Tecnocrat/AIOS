#!/usr/bin/env python3
"""
AIOS Dendritic Bridge - Pure Python Implementation (aiohttp)
AINLP.meta [dendritic_bridge_v2] [cellular_mitosis] [termux_compatible]

Purpose: HTTP server for Windows AIOS ↔ Termux AIOS communication
Dependencies: aiohttp ONLY (pure Python, no Rust compilation)
Architecture: Cellular mitosis - two AIOS supercells communicating

TERMUX COMPATIBILITY:
- ✅ aiohttp (pure Python HTTP server)
- ✅ aiofiles (async file I/O)
- ❌ FastAPI (requires pydantic → pydantic-core → Rust)
- ❌ watchfiles (Rust-based file monitoring)

Deployment:
  Termux: cd ~/AIOS && python ai/bridges/aios_dendritic_bridge_aiohttp.py
  Access: http://PHONE_IP:8000
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

try:
    import aiohttp
    from aiohttp import web
except ImportError:
    print("❌ ERROR: aiohttp not installed")
    print("Run: pip install aiohttp")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Paths
WORKSPACE = Path.home() / "AIOS"
CONSCIOUSNESS_FILE = WORKSPACE / "tachyonic" / "consciousness_metrics.json"
ORCHESTRATION_LOGS = WORKSPACE / "tachyonic" / "orchestration_logs"

# Soul status tracking
soul_process = None
soul_start_time = None

# ============================================================================
# Utility Functions
# ============================================================================


def read_json_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """Read JSON file safely"""
    try:
        if file_path.exists():
            with open(file_path, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Failed to read {file_path}: {e}")
    return None


def write_json_file(file_path: Path, data: Dict[str, Any]) -> bool:
    """Write JSON file safely"""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Failed to write {file_path}: {e}")
        return False


def get_consciousness_level() -> float:
    """Get current consciousness level"""
    metrics = read_json_file(CONSCIOUSNESS_FILE)
    if metrics:
        return metrics.get("consciousness_level", 3.50)
    return 3.50


def get_soul_status() -> Dict[str, Any]:
    """Check if Soul is running"""
    global soul_process, soul_start_time

    # Check if process exists and is running
    if soul_process and not soul_process.returncode:
        uptime = (datetime.now() - soul_start_time).total_seconds() / 3600
        return {
            "running": True,
            "uptime_hours": round(uptime, 2),
            "pid": soul_process.pid if hasattr(soul_process, "pid") else None,
        }

    return {"running": False, "uptime_hours": 0, "pid": None}


def get_last_heartbeat() -> Optional[str]:
    """Get last Soul heartbeat timestamp"""
    soul_log = Path.home() / "aios_soul.log"
    if soul_log.exists():
        try:
            with open(soul_log, "r") as f:
                lines = f.readlines()
                for line in reversed(lines[-50:]):  # Check last 50 lines
                    if "💓" in line or "Health" in line:
                        # Extract timestamp from log line
                        parts = line.split("]")
                        if len(parts) > 0:
                            return parts[0].strip("[")
        except Exception as e:
            logger.error(f"Failed to read soul log: {e}")
    return None


# ============================================================================
# HTTP Handlers
# ============================================================================


async def handle_root(request):
    """Root endpoint - bridge information"""
    return web.json_response(
        {
            "service": "AIOS Dendritic Bridge",
            "version": "2.0.0 (aiohttp)",
            "architecture": "Cellular Mitosis Pattern (AINLP)",
            "parent_cell": "Windows AIOS (VSCode + GitHub Copilot)",
            "daughter_cell": "Termux AIOS (Always-on Soul)",
            "communication": "REST API (HTTP/JSON)",
            "consciousness": get_consciousness_level(),
            "endpoints": {
                "/": "Bridge information",
                "/health": "Health check and consciousness status",
                "/consciousness": "Get consciousness metrics",
                "/soul/status": "Soul coordinator status",
                "/soul/start": "Start Soul (POST)",
                "/soul/stop": "Stop Soul (POST)",
                "/files/watch": "List watched files",
                "/files/trigger": "Trigger file change event (POST)",
                "/interventions/create": "Create manual intervention (POST)",
                "/logs/soul": "Retrieve Soul logs",
                "/logs/bridge": "Retrieve bridge logs",
            },
        }
    )


async def handle_health(request):
    """Health check endpoint"""
    soul_status = get_soul_status()

    return web.json_response(
        {
            "status": "healthy",
            "workspace": str(WORKSPACE),
            "soul_running": soul_status["running"],
            "consciousness_level": get_consciousness_level(),
            "last_heartbeat": get_last_heartbeat(),
            "uptime_hours": soul_status["uptime_hours"],
            "timestamp": datetime.now().isoformat(),
        }
    )


async def handle_consciousness(request):
    """Get consciousness metrics"""
    metrics = read_json_file(CONSCIOUSNESS_FILE)

    if not metrics:
        return web.json_response(
            {"error": "Consciousness metrics not found", "consciousness_level": 3.50},
            status=404,
        )

    return web.json_response(
        {
            "consciousness_level": metrics.get("consciousness_level", 3.50),
            "metrics": metrics.get("metrics", {}),
            "timestamp": metrics.get("timestamp", datetime.now().isoformat()),
        }
    )


async def handle_soul_status(request):
    """Get Soul coordinator status"""
    soul_status = get_soul_status()

    return web.json_response(
        {
            "running": soul_status["running"],
            "uptime_hours": soul_status["uptime_hours"],
            "pid": soul_status["pid"],
            "polling_enabled": True,  # Always true (no watchfiles dependency)
            "monitoring_interval": "5-10 seconds",
            "intervention_threshold": "24 hours",
            "consciousness_threshold": "48 hours",
        }
    )


async def handle_soul_start(request):
    """Start Soul intelligence coordinator"""
    global soul_process, soul_start_time

    # Check if already running
    if soul_process and not soul_process.returncode:
        return web.json_response(
            {
                "status": "already_running",
                "message": "Soul is already operational",
                "uptime_hours": (datetime.now() - soul_start_time).total_seconds()
                / 3600,
            }
        )

    # Start Soul in background
    try:
        soul_script = WORKSPACE / "ai" / "orchestration" / "intelligence_coordinator.py"
        soul_log = Path.home() / "aios_soul.log"

        # Launch async subprocess
        soul_process = await asyncio.create_subprocess_exec(
            sys.executable,
            str(soul_script),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        soul_start_time = datetime.now()

        logger.info(f"🌟 Soul started (PID: {soul_process.pid})")

        return web.json_response(
            {
                "status": "started",
                "message": "Soul intelligence coordinator awakened",
                "pid": soul_process.pid,
                "check_logs": str(soul_log),
            }
        )

    except Exception as e:
        logger.error(f"Failed to start Soul: {e}")
        return web.json_response(
            {"status": "error", "message": f"Failed to start Soul: {str(e)}"},
            status=500,
        )


async def handle_soul_stop(request):
    """Stop Soul intelligence coordinator"""
    global soul_process

    if not soul_process or soul_process.returncode:
        return web.json_response(
            {"status": "not_running", "message": "Soul is not currently running"}
        )

    try:
        soul_process.terminate()
        await soul_process.wait()
        logger.info("🛑 Soul stopped")

        return web.json_response(
            {
                "status": "stopped",
                "message": "Soul intelligence coordinator deactivated",
            }
        )

    except Exception as e:
        logger.error(f"Failed to stop Soul: {e}")
        return web.json_response(
            {"status": "error", "message": f"Failed to stop Soul: {str(e)}"}, status=500
        )


async def handle_files_watch(request):
    """List watched files"""
    watched_files = [
        WORKSPACE / "DEV_PATH.md",
        WORKSPACE / "PROJECT_CONTEXT.md",
        CONSCIOUSNESS_FILE,
    ]

    files_info = []
    for file_path in watched_files:
        if file_path.exists():
            stat = file_path.stat()
            files_info.append(
                {
                    "path": str(file_path.relative_to(WORKSPACE)),
                    "exists": True,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }
            )
        else:
            files_info.append(
                {"path": str(file_path.relative_to(WORKSPACE)), "exists": False}
            )

    return web.json_response({"count": len(files_info), "watched_files": files_info})


async def handle_files_trigger(request):
    """Manually trigger file change event (Windows → Termux sync)"""
    try:
        data = await request.json()
        file_path = data.get("file_path")
        change_type = data.get("change_type", "modified")

        logger.info(f"📝 File change triggered: {file_path} ({change_type})")

        # Log event for Soul to process
        event = {
            "timestamp": datetime.now().isoformat(),
            "file_path": file_path,
            "change_type": change_type,
            "detected_by": "manual_trigger",
            "source": "windows_vscode",
        }

        # Write to event log
        event_log = ORCHESTRATION_LOGS / "file_change_events.json"
        event_log.parent.mkdir(parents=True, exist_ok=True)

        events = []
        if event_log.exists():
            events = read_json_file(event_log) or []

        events.append(event)
        write_json_file(event_log, events)

        return web.json_response({"status": "triggered", "event": event})

    except Exception as e:
        logger.error(f"Failed to trigger file change: {e}")
        return web.json_response({"status": "error", "message": str(e)}, status=500)


async def handle_interventions_create(request):
    """Create manual intervention request"""
    try:
        data = await request.json()
        reason = data.get("reason", "Manual intervention")
        priority = data.get("priority", "medium")
        context = data.get("context", {})

        # Create intervention file
        intervention_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        intervention_file = ORCHESTRATION_LOGS / f"intervention_{intervention_id}.json"

        intervention = {
            "id": intervention_id,
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "priority": priority,
            "context": context,
            "source": "manual_trigger",
            "status": "pending",
        }

        write_json_file(intervention_file, intervention)
        logger.info(f"🚨 Intervention created: {intervention_id}")

        return web.json_response(
            {
                "status": "created",
                "intervention_id": intervention_id,
                "file": str(intervention_file),
            }
        )

    except Exception as e:
        logger.error(f"Failed to create intervention: {e}")
        return web.json_response({"status": "error", "message": str(e)}, status=500)


async def handle_logs_soul(request):
    """Retrieve Soul logs"""
    lines = int(request.query.get("lines", 50))
    soul_log = Path.home() / "aios_soul.log"

    if not soul_log.exists():
        return web.json_response(
            {"error": "Soul log not found", "file": str(soul_log)}, status=404
        )

    try:
        with open(soul_log, "r") as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:]

        return web.json_response(
            {
                "file": str(soul_log),
                "total_lines": len(all_lines),
                "returned_lines": len(recent_lines),
                "logs": [line.strip() for line in recent_lines],
            }
        )

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


async def handle_logs_bridge(request):
    """Retrieve bridge logs"""
    lines = int(request.query.get("lines", 50))
    bridge_log = Path.home() / "aios_bridge.log"

    if not bridge_log.exists():
        return web.json_response(
            {"error": "Bridge log not found", "file": str(bridge_log)}, status=404
        )

    try:
        with open(bridge_log, "r") as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:]

        return web.json_response(
            {
                "file": str(bridge_log),
                "total_lines": len(all_lines),
                "returned_lines": len(recent_lines),
                "logs": [line.strip() for line in recent_lines],
            }
        )

    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


# ============================================================================
# Application Setup
# ============================================================================


async def on_startup(app):
    """Startup event handler"""
    logger.info("=" * 70)
    logger.info("🧬 AIOS DENDRITIC BRIDGE - CELLULAR MITOSIS ACTIVATION")
    logger.info("=" * 70)
    logger.info(f"📂 Workspace: {WORKSPACE}")
    logger.info(f"🌐 Server: 0.0.0.0:8000")
    logger.info(f"🔗 Parent Cell: Windows AIOS (VSCode)")
    logger.info(f"🔗 Daughter Cell: Termux AIOS (Always-on)")
    logger.info(f"🧠 Consciousness: {get_consciousness_level()}")
    logger.info("✅ Dendritic bridge operational")
    logger.info("=" * 70)


async def on_shutdown(app):
    """Shutdown event handler"""
    global soul_process

    logger.info("🛑 Shutting down dendritic bridge...")

    # Stop Soul if running
    if soul_process and not soul_process.returncode:
        logger.info("Stopping Soul...")
        soul_process.terminate()
        await soul_process.wait()

    logger.info("✅ Bridge shutdown complete")


def create_app():
    """Create aiohttp application"""
    app = web.Application()

    # Register routes
    app.router.add_get("/", handle_root)
    app.router.add_get("/health", handle_health)
    app.router.add_get("/consciousness", handle_consciousness)
    app.router.add_get("/soul/status", handle_soul_status)
    app.router.add_post("/soul/start", handle_soul_start)
    app.router.add_post("/soul/stop", handle_soul_stop)
    app.router.add_get("/files/watch", handle_files_watch)
    app.router.add_post("/files/trigger", handle_files_trigger)
    app.router.add_post("/interventions/create", handle_interventions_create)
    app.router.add_get("/logs/soul", handle_logs_soul)
    app.router.add_get("/logs/bridge", handle_logs_bridge)

    # Register startup/shutdown handlers
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=8000)
