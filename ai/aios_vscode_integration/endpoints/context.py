"""
Context endpoints: /context/health, /context/logs
"""

from datetime import datetime

from fastapi import APIRouter

from ..debug_manager import _debug_manager

router = APIRouter()


@router.get("/context/health")
async def context_health():
    """
    Returns the current health status of the context subsystem, including
    persistence, history size, encryption, backup time,
    and self-healing features.
    """
    health_status = {
        "context_persistence": True,
        "max_history_size": 1000,
        "encryption": True,
        "last_backup": datetime.now().isoformat(),
        "self_healing": "enabled",
        "auto_restart": "enabled",
    }
    return {
        "health_status": health_status,
        "timestamp": datetime.now().isoformat(),
        "note": "Replace with real context health and self-healing logic.",
    }


@router.get("/context/logs")
async def context_logs():
    """
    Retrieves debug logs and diagnostic information from the debug manager.
    Returns logs, timestamp, and a note about diagnostics.
    """
    debug_info = _debug_manager.get_debug_info()
    return {
        "logs": debug_info,
        "timestamp": datetime.now().isoformat(),
        "note": "Replace with real diagnostics and performance analysis.",
    }
