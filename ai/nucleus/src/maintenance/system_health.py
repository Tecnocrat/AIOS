"""
AIOS Maintenance - System Health Runner

AINLP provenance:
- Purpose: bridge AI Core to the runtime system health tool without
  coupling tests or core logic to side effects
- Origin: integrates runtime_intelligence/tools/system_health_check.py
  as an ops/diagnostics callable
"""

from __future__ import annotations

import asyncio
import subprocess
import sys
from pathlib import Path
from typing import Optional


def _health_tool_path() -> str:
    root = Path(__file__).resolve().parents[3]  # .../AIOS/ai/src/maintenance
    return str(
        root / "runtime_intelligence" / "tools" / "system_health_check.py"
    )


def run_system_health_check(timeout: Optional[int] = 180) -> int:
    """Run the system health tool synchronously; return exit code."""
    cmd = [sys.executable, _health_tool_path()]
    try:
        completed = subprocess.run(
            cmd, cwd=Path(__file__).resolve().parents[3], timeout=timeout
        )
        return completed.returncode
    except Exception:
        return 2


async def run_system_health_check_async(timeout: Optional[int] = 180) -> int:
    """Run the system health tool in a thread to avoid blocking the loop."""
    return await asyncio.to_thread(run_system_health_check, timeout)
