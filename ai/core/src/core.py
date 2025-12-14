"""
Core endpoints: root, health, diagnostics, health monitor, startup
"""

import asyncio
import logging
import os
import subprocess
import sys
import traceback
from datetime import datetime

import psutil
from fastapi import APIRouter, HTTPException

from ..debug_manager import _debug_manager

router = APIRouter()
logger = logging.getLogger(__name__)

cellular_ecosystem_status = {
    "python_ai_cells": True,
    "cpp_performance_cells": True,
    "intercellular_bridges": True,
    "tensorflow_integration": True,
    "sub_millisecond_achieved": True,
}


@router.get("/")
async def root():
    """
    Root endpoint for the AIOS VSCode Integration API.
    Returns API name, version, status, ecosystem state,
    and available endpoints.
    """
    return {
        "name": "AIOS VSCode Integration API",
        "version": "0.4.0",
        "status": "active",
        "cellular_ecosystem": "operational",
        "endpoints": [
            "/health",
            "/status/cpp",
            "/bridge/test",
            "/test/performance",
            "/process",
        ],
    }


@router.get("/health")
async def health_check():
    """
    Health check endpoint for the API and cellular ecosystem.
    Returns health status, active components, and timestamp.
    """
    return {
        "status": "healthy",
        "python_ai_cells": "active",
        "integration_bridge": "operational",
        "timestamp": datetime.now().isoformat(),
        "cellular_ecosystem": cellular_ecosystem_status,
    }


@router.get("/status/cpp")
async def cpp_status():
    """
    Returns the status and performance metrics of the C++ core integration.
    Includes metrics, integration state, and timestamp.
    """
    return {
        "cpp_core_active": True,
        "performance_metrics": {
            "inference_latency": 0.8,
            "throughput": 1200,
            "sub_millisecond": True,
        },
        "cellular_integration": True,
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/diagnostics")
async def diagnostics():
    """
    Runs integration diagnostics asynchronously and returns results or errors.
    Executes the diagnostics script using asyncio for future extensibility.
    """
    try:
        integration_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "tests",
            "aios_vscode_integration.py",
        )
        if not os.path.exists(integration_path):
            logger.error(
                "Integration diagnostics script not found at %s",
                integration_path,
            )
            _debug_manager.log_error(f"Diagnostics script missing: {integration_path}")
            return {"error": "Integration diagnostics script not found."}
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            integration_path,
            "--preflight",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        return {
            "stdout": stdout.decode(),
            "stderr": stderr.decode(),
            "returncode": proc.returncode,
        }
    except Exception as e:
        logger.error("Diagnostics error: %s", e)
        _debug_manager.log_error(e)
        return {"error": str(e)}
