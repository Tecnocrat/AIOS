#!/usr/bin/env python3
"""AIOS Full System Validation Harness

End-to-end validation across stacks:
 1. Build C++ core (viewer target)
 2. Run tachyonic surface viewer -> PPM/BMP
 3. Reindex context (+ adjacency)
 4. Crystallize sample archive
 5. Gather artifact + DB + adjacency metrics
 6. Emit summary JSON (runtime_intelligence/context/full_system_validation.json)

Light-weight; reuses existing scripts.
"""
from __future__ import annotations
import subprocess
import json
import sqlite3
import sys
import time
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
CORE_BUILD = ROOT / "core" / "build"
RI_CONTEXT = ROOT / "runtime_intelligence" / "context"
RI_LOGS = ROOT / "runtime_intelligence" / "logs" / "tachyonic"
SUMMARY_FILE = RI_CONTEXT / "full_system_validation.json"
CRYSTAL_DB = RI_CONTEXT / "knowledge_crystals.db"
IS_WIN = sys.platform.startswith("win")
VIEWER_NAME = "aios_tachyonic_viewer.exe" if IS_WIN else "aios_tachyonic_viewer"
# Primary expected (single-config) path
VIEWER_EXE = CORE_BUILD / "bin" / VIEWER_NAME

def _resolve_viewer_path() -> Path | None:
    """Locate viewer executable handling multi-config generators.

    Search order:
      1. core/build/bin/<viewer>
      2. core/build/bin/Debug/<viewer>
      3. First match via glob core/build/**/aios_tachyonic_viewer*.exe (Windows)
    """
    if VIEWER_EXE.exists():
        return VIEWER_EXE
    debug_path = CORE_BUILD / "bin" / "Debug" / VIEWER_NAME
    if debug_path.exists():
        return debug_path
    # Broad search (limited depth)
    pattern = "aios_tachyonic_viewer.exe" if IS_WIN else "aios_tachyonic_viewer"
    for p in (CORE_BUILD / "bin").rglob(pattern):  # type: ignore[arg-type]
        return p
    return None
REINDEX_SCRIPT = ROOT / "scripts" / "context_reindex.py"
CRYSTAL_SCRIPT = ROOT / "scripts" / "context_crystallization_engine.py"


def run(
    cmd: list[str] | str,
    cwd: Path | None = None,
    timeout: int = 180,
) -> tuple[int, str, str]:
    if isinstance(cmd, str):
        shell = True
        final_cmd = cmd
    else:
        shell = False
        final_cmd = cmd
    try:
        p = subprocess.run(
            final_cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=shell,
        )
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"


def ensure_core_build():
    steps = []
    if not CORE_BUILD.exists():
        CORE_BUILD.mkdir(parents=True)
    # Configure if no cache
    if not (CORE_BUILD / "CMakeCache.txt").exists():
        code, out, err = run(
            ["cmake", "..", "-DCMAKE_BUILD_TYPE=Debug"],
            cwd=CORE_BUILD,
            timeout=300,
        )
        steps.append({"step": "cmake_config", "code": code})
    # Build viewer target only (faster)
    viewer_path = _resolve_viewer_path()
    if not viewer_path:
        code, out, err = run(
            [
                "cmake",
                "--build",
                ".",
                "--target",
                "aios_tachyonic_viewer",
                "--config",
                "Debug",
            ],
            cwd=CORE_BUILD,
            timeout=600,
        )
        steps.append({"step": "build_viewer", "code": code})
    return steps


def run_viewer():
    viewer_path = _resolve_viewer_path()
    if not viewer_path:
        return {"ran": False, "reason": "viewer_missing"}
    before = set()
    if RI_LOGS.exists():
        before = set(RI_LOGS.rglob("tachyonic_surface.*"))
    RI_LOGS.mkdir(parents=True, exist_ok=True)
    code, out, err = run([str(viewer_path)], cwd=viewer_path.parent, timeout=120)
    after = set(RI_LOGS.rglob("tachyonic_surface.*"))
    new = [str(p) for p in after - before]
    bmp = [p for p in new if p.endswith(".bmp")]
    ppm = [p for p in new if p.endswith(".ppm")]
    return {
        "ran": True,
        "code": code,
        "bmp_count": len(bmp),
        "ppm_count": len(ppm),
        "new_artifacts": new[-10:],
        "stderr_trunc": err[-400:],
    }


def reindex():
    code, out, err = run(
        [sys.executable, str(REINDEX_SCRIPT), "--emit-adjacency"], cwd=ROOT
    )
    adj_path = RI_CONTEXT / "context_adjacency.json"
    idx_path = RI_CONTEXT / "context_index.json"
    edges = None
    if adj_path.exists():
        try:
            edges = len(json.loads(adj_path.read_text()).get("edges", []))
        except Exception:
            edges = -1
    return {
        "code": code,
        "edges": edges,
        "stderr_trunc": err[-400:] if err else "",
        "indexed": idx_path.exists(),
    }


def crystallize():
    before_count = crystal_count()
    code, out, err = run(
        [
            sys.executable,
            str(CRYSTAL_SCRIPT),
            "--archive",
            "validation_archive",
        ],
        cwd=ROOT,
    )
    after_count = crystal_count()
    return {
        "code": code,
        "new_crystals": after_count - before_count,
        "total": after_count,
        "stderr_trunc": err[-400:],
    }


def crystal_count():
    if not CRYSTAL_DB.exists():
        return 0
    try:
        conn = sqlite3.connect(CRYSTAL_DB)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM knowledge_crystals")
        n = cur.fetchone()[0]
        conn.close()
        return int(n)
    except Exception:
        return -1


def main():
    start = time.time()
    RI_CONTEXT.mkdir(parents=True, exist_ok=True)
    result = {"generated_at": datetime.utcnow().isoformat() + "Z", "steps": {}}
    result["steps"]["build"] = ensure_core_build()
    result["steps"]["viewer"] = run_viewer()
    result["steps"]["reindex"] = reindex()
    result["steps"]["crystallization"] = crystallize()
    result["duration_seconds"] = round(time.time() - start, 2)
    # basic success heuristic
    result["success"] = (
        result["steps"]["viewer"].get("bmp_count", 0) >= 1
        and result["steps"]["reindex"].get("edges", 0) > 0
        and result["steps"]["crystallization"].get("new_crystals", 0) >= 1
    )
    SUMMARY_FILE.write_text(json.dumps(result, indent=2))
    print(f"[full-system] Summary -> {SUMMARY_FILE}")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
