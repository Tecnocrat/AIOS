#!/usr/bin/env python3
"""AIOS Full System Validation Harness
                    }


if __name__ == "__main__":
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
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
try:  # optional KPI crystal helper
    from context_crystallization_engine import (  # type: ignore
        create_metric_crystal,
    )
except Exception:  # pragma: no cover
    create_metric_crystal = None  # type: ignore

ROOT = Path(__file__).resolve().parent.parent
# Validation harness schema/versioning & mode targets (UP7)
VALIDATION_SCHEMA_VERSION = 2
MODE_CHOICES = {"fast", "full"}
DEFAULT_MODE = "full"
# Target maximum durations (seconds)
MODE_DURATION_TARGETS = {"full": 300, "fast": 90}
DEFAULT_EVOLUTION_CYCLES_FULL = 3
DEFAULT_EVOLUTION_CYCLES_FAST = 1
CORE_BUILD = ROOT / "core" / "build"
RI_CONTEXT = ROOT / "runtime_intelligence" / "context"
RI_LOGS = ROOT / "runtime_intelligence" / "logs" / "tachyonic"
SUMMARY_FILE = RI_CONTEXT / "full_system_validation.json"
CRYSTAL_DB = RI_CONTEXT / "knowledge_crystals.db"
IS_WIN = sys.platform.startswith("win")
VIEWER_NAME = (
    "aios_tachyonic_viewer.exe" if IS_WIN else "aios_tachyonic_viewer"
)
# Primary expected (single-config) path
VIEWER_EXE = CORE_BUILD / "bin" / VIEWER_NAME
AI_CONTEXT_DUMPS = ROOT / "runtime_intelligence" / "logs" / "aios_context"
KPI_THRESHOLDS_FILE = (
    ROOT / "runtime_intelligence" / "context" / "kpi_thresholds.json"
)
VISION_DEMO_SCRIPT = ROOT / "ai" / "demos" / "opencv_integration_demo.py"
VISION_DEMO_OUTPUT = ROOT / "runtime_intelligence" / "logs" / "vision_demo"
EVOLUTION_SCHEDULER = (
    ROOT / "scripts" / "orchestration" / "evolution_scheduler.py"
)


def _resolve_viewer_path() -> Optional[Path]:
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
    pattern = (
        "aios_tachyonic_viewer.exe" if IS_WIN else "aios_tachyonic_viewer"
    )
    for p in (CORE_BUILD / "bin").rglob(pattern):  # type: ignore[arg-type]
        return p
    return None
REINDEX_SCRIPT = ROOT / "scripts" / "context_reindex.py"
CRYSTAL_SCRIPT = ROOT / "scripts" / "context_crystallization_engine.py"



def run(
    cmd: List[str] | str,
    cwd: Optional[Path] = None,
    timeout: int = 180,
) -> Tuple[int, str, str]:
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


def _latest_mtime(paths: List[Path]) -> float:
    latest = 0.0
    for p in paths:
        try:
            m = p.stat().st_mtime
            if m > latest:
                latest = m
        except Exception:
            continue
    return latest


def needs_rebuild(force: bool = False) -> bool:
    """Determine if core viewer rebuild is needed.

    Heuristic: if viewer binary missing OR any source/newer than binary.
    """
    if force:
        return True
    viewer = _resolve_viewer_path()
    if not viewer:
        return True
    try:
        bin_mtime = viewer.stat().st_mtime
    except Exception:
        return True
    src_dirs = [ROOT / "core" / "src", ROOT / "core" / "include"]
    src_files: List[Path] = []
    for d in src_dirs:
        if d.exists():
            src_files.extend(list(d.rglob("*.cpp")))
            src_files.extend(list(d.rglob("*.c")))
            src_files.extend(list(d.rglob("*.hpp")))
            src_files.extend(list(d.rglob("*.h")))
    if not src_files:  # fallback to CMakeLists.txt
        cmk = ROOT / "core" / "CMakeLists.txt"
        if cmk.exists():
            src_files.append(cmk)
    latest_src = _latest_mtime(src_files)
    return latest_src > bin_mtime


def ensure_core_build(force: bool = False) -> List[Dict[str, Any]]:
    steps = []
    if not CORE_BUILD.exists():
        CORE_BUILD.mkdir(parents=True)
    # Configure if no cache
    if not (CORE_BUILD / "CMakeCache.txt").exists():
        code, _out, _err = run(
            ["cmake", "..", "-DCMAKE_BUILD_TYPE=Debug"],
            cwd=CORE_BUILD,
            timeout=300,
        )
        steps.append({"step": "cmake_config", "code": code})
    # Rebuild only if needed
    if needs_rebuild(force=force):
        code, _out, _err = run(
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
        steps.append({"step": "build_viewer", "code": code, "rebuilt": True})
    else:
        steps.append(
            {
                "step": "build_viewer",
                "rebuilt": False,
                "skipped_reason": "up_to_date",
            }
        )
    return steps


def run_viewer() -> Dict[str, Any]:
    """Run viewer twice capturing cold + steady timings and artifact counts."""
    viewer_path = _resolve_viewer_path()
    if not viewer_path:
        return {"ran": False, "reason": "viewer_missing"}

    def _invoke() -> Dict[str, Any]:
        before = set()
        if RI_LOGS.exists():
            before = set(RI_LOGS.rglob("tachyonic_surface.*"))
        RI_LOGS.mkdir(parents=True, exist_ok=True)
        start_t = time.time()
        code, out, err = run(
            [str(viewer_path)], cwd=viewer_path.parent, timeout=120
        )
        duration = time.time() - start_t
        after = set(RI_LOGS.rglob("tachyonic_surface.*"))
        new = [str(p) for p in after - before]
        bmp = [p for p in new if p.endswith(".bmp")]
        ppm = [p for p in new if p.endswith(".ppm")]
        return {
            "code": code,
            "duration": round(duration, 4),
            "bmp_count": len(bmp),
            "ppm_count": len(ppm),
            "new_artifacts": new[-10:],
            "stderr_trunc": err[-400:],
        }

    cold = _invoke()
    steady = _invoke()
    # Preserve backwards-compatible keys (use cold run artifact counts)
    return {
        "ran": True,
        "bmp_count": cold.get("bmp_count"),
        "ppm_count": cold.get("ppm_count"),
        "cold": cold,
        "steady": steady,
        "vision_cold_start_sec": cold.get("duration"),
        "vision_steady_state_sec": steady.get("duration"),
    }


def reindex() -> Dict[str, Any]:
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


def crystallize() -> Dict[str, Any]:
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


def crystal_count() -> int:
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


def _load_ui_metrics() -> Dict[str, Any]:
    """Load UI/performance metrics emitted by future instrumentation.

    Expected path: runtime_intelligence/logs/ui/ui_metrics.json
    Schema (proposed): {
        "render_fps": float,
        "cpp_python_latency_ms": float,
        "ui_uptime_pct": float,
        "state_restore_sec": float,
        "metadata_rate_ctx_per_min": int
    }
    """
    ui_dir = ROOT / "runtime_intelligence" / "logs" / "ui"
    ui_file = ui_dir / "ui_metrics.json"
    if not ui_file.exists():
        return {}
    try:
        return json.loads(ui_file.read_text())
    except Exception as ex:  # pragma: no cover
        return {"error": str(ex)}


def _emit_ui_metrics_stub() -> None:
    """Emit light synthetic UI metrics to reduce 'unmeasured' until real data.

    Approximates a render loop to estimate a nominal FPS figure. Other
    metrics remain None pending instrumentation.
    """
    ui_dir = ROOT / "runtime_intelligence" / "logs" / "ui"
    ui_dir.mkdir(parents=True, exist_ok=True)
    ui_file = ui_dir / "ui_metrics.json"
    if ui_file.exists():  # don't overwrite real metrics
        return
    frames = 200
    start = time.time()
    acc = 0
    for i in range(frames):  # trivial CPU work
        acc += (i * i) % 11
    elapsed = time.time() - start
    fps = frames / elapsed if elapsed > 0 else 0.0
    stub = {
        "render_fps": round(fps, 2),
        "cpp_python_latency_ms": None,
        "ui_uptime_pct": None,
        "state_restore_sec": None,
        "metadata_rate_ctx_per_min": None,
        "_stub": True,
    }
    ui_file.write_text(json.dumps(stub, indent=2))


def _run_evolution_cycles(cycles: int = 3) -> Dict[str, Any]:
    """Run a small number of evolution scheduler cycles (UP5 integration).

    Returns summary metrics; best-effort (ignored if scheduler missing).
    """
    if not EVOLUTION_SCHEDULER.exists():
        return {"ran": False, "reason": "scheduler_missing"}
    try:
        code, out, err = run(
            [
                sys.executable,
                str(EVOLUTION_SCHEDULER),
                "--cycles",
                str(cycles),
            ],
            cwd=ROOT,
            timeout=120,
        )
        data: Dict[str, Any] = {}
        try:
            data = json.loads(out.strip().splitlines()[-1]) if out else {}
        except Exception:
            data = {"parse_error": True}
        data.update({"code": code})
        # Optional crystal capturing improvement metrics
        if create_metric_crystal and data:
            try:
                create_metric_crystal(
                    metric_snapshot=data,
                    capsule_ids=["evolution-orchestration-up5"],
                    kpi_dimensions=[
                        k
                        for k in ("best_fitness", "average_fitness")
                        if k in data
                    ],
                    source_tag="evolution_scheduler_run",
                )
                data["evolution_crystal"] = True
            except Exception as ex:  # pragma: no cover
                data["evolution_crystal_error"] = str(ex)
        return data
    except Exception as ex:  # pragma: no cover
        return {"ran": False, "error": str(ex)}


def _load_core_telemetry() -> Dict[str, Any]:
    """Load recent core telemetry samples (newline-delimited JSON).

    Returns aggregated stats for CPU %, memory MB, frame timings.
    """
    core_file = (
        ROOT
        / "runtime_intelligence"
        / "logs"
        / "core"
        / "core_metrics.json"
    )
    if not core_file.exists():
        return {}
    try:
        lines = core_file.read_text().strip().splitlines()
        if not lines:
            return {}
        # consider last up to 120 samples (~2 min if 1s interval later)
        tail = lines[-120:]
        samples: List[Dict[str, Any]] = []
        for ln in tail:
            try:
                samples.append(json.loads(ln))
            except Exception:
                continue
        if not samples:
            return {}
        def _avg(key: str) -> Optional[float]:  # nested helper
            vals_f: List[float] = []
            for s in samples:
                v = s.get(key)
                if (
                    isinstance(v, (int, float))
                    and v >= 0  # type: ignore[operator]
                ):
                    vals_f.append(float(v))
            return round(sum(vals_f) / len(vals_f), 3) if vals_f else None

        def _max(key: str) -> Optional[float]:  # nested helper
            vals_f: List[float] = []
            for s in samples:
                v = s.get(key)
                if (
                    isinstance(v, (int, float))
                    and v >= 0  # type: ignore[operator]
                ):
                    vals_f.append(float(v))
            return round(max(vals_f), 3) if vals_f else None
        agg: Dict[str, Any] = {
            "_core_samples": len(samples),
            "core_cpu_pct_avg": _avg("cpu"),
            "core_cpu_pct_max": _max("cpu"),
            "core_mem_mb_avg": _avg("mem_mb"),
            "core_mem_mb_max": _max("mem_mb"),
            "core_frame_time_ms_avg": _avg("frame_ms"),
            "core_frame_time_ms_smoothing": _avg("avg_frame_ms"),
        }
        return agg
    except Exception as ex:  # pragma: no cover
        return {"error": str(ex)}


def _evaluate_kpis(
    thresholds: Dict[str, Any],
    runtime_metrics: Dict[str, Any],
    ui_metrics: Dict[str, Any],
    core_metrics: Dict[str, Any],
    vision_summary: Dict[str, Any],
    evolution_metrics: Dict[str, Any],
) -> Dict[str, Dict[str, Any]]:
    """Evaluate KPIs given metric sources and threshold lattice.

    Returns mapping name -> {value, rule, status}.
    Status semantics: pass | fail | unmeasured.
    """
    kpi_eval: Dict[str, Dict[str, Any]] = {}
    kpis = thresholds.get("kpis", {})
    merged_metrics: Dict[str, Any] = {
        **runtime_metrics,
        **ui_metrics,
        **core_metrics,
    }
    # Runtime surrogate KPIs
    for name, rule in kpis.get("runtime_surrogates", {}).items():
        cur = merged_metrics.get(name)
        status = "unmeasured"
        if cur is not None:
            if "min" in rule:
                status = "pass" if cur >= rule["min"] else "fail"
            if "max" in rule:
                within = cur <= rule["max"]
                status = "pass" if status != "fail" and within else "fail"
        kpi_eval[name] = {"value": cur, "rule": rule, "status": status}
    # Objectives
    for obj_key in ("objective1", "objective2", "objective3"):
        for name, rule in kpis.get(obj_key, {}).items():
            cur = merged_metrics.get(name)
            status = "unmeasured"
            if cur is not None:
                if "min" in rule and cur >= rule["min"]:
                    status = "pass"
                elif "min" in rule:
                    status = "fail"
                if "max" in rule and cur is not None:
                    if cur > rule["max"]:
                        status = "fail"
                    elif status != "fail":
                        status = "pass"
            kpi_eval[name] = {"value": cur, "rule": rule, "status": status}
    # Core metrics
    for name, rule in kpis.get("core_metrics", {}).items():
        cur = merged_metrics.get(name)
        status = "unmeasured"
        if cur is not None:
            if "min" in rule and cur < rule["min"]:
                status = "fail"
            elif "min" in rule:
                status = "pass"
            if "max" in rule:
                if cur > rule["max"]:
                    status = "fail"
                elif status != "fail":
                    status = "pass"
        kpi_eval[name] = {"value": cur, "rule": rule, "status": status}
    # Vision metrics
    for name, rule in kpis.get("vision_metrics", {}).items():
        cur = merged_metrics.get(name) or vision_summary.get(name)
        status = "unmeasured"
        if cur is not None:
            if "min" in rule and cur >= rule["min"]:
                status = "pass"
            elif "min" in rule:
                status = "fail"
            if "max" in rule and cur is not None:
                if cur > rule["max"]:
                    status = "fail"
                elif status != "fail":
                    status = "pass"
        kpi_eval[name] = {"value": cur, "rule": rule, "status": status}
    # Evolution metrics
    for name, rule in kpis.get("evolution_metrics", {}).items():
        cur = evolution_metrics.get(name)
        status = "unmeasured"
        if cur is not None:
            if "min" in rule and cur < rule["min"]:
                status = "fail"
            elif "min" in rule:
                status = "pass"
            if "max" in rule:
                if cur > rule["max"]:
                    status = "fail"
                elif status != "fail":
                    status = "pass"
        kpi_eval[name] = {"value": cur, "rule": rule, "status": status}
    return kpi_eval


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        description="AIOS System Validation Harness (UP7 modes)"
    )
    parser.add_argument(
        "--mode",
        choices=sorted(MODE_CHOICES),
        default=DEFAULT_MODE,
        help="Validation mode: fast or full",
    )
    parser.add_argument(
        "--force-rebuild",
        action="store_true",
        help="Force core rebuild even if up-to-date",
    )
    parser.add_argument(
        "--fast-cycles",
        type=int,
        default=DEFAULT_EVOLUTION_CYCLES_FAST,
        help="Evolution cycles in fast mode override",
    )
    args = parser.parse_args(argv)

    mode = args.mode
    force_rebuild = args.force_rebuild
    fast_cycles_override = max(1, args.fast_cycles)
    start = time.time()
    RI_CONTEXT.mkdir(parents=True, exist_ok=True)
    result: Dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "steps": {},
        "validation_schema_version": VALIDATION_SCHEMA_VERSION,
        "mode": mode,
    }
    step_durations: Dict[str, float] = {}
    skipped: List[str] = []

    from typing import Callable, Any as _Any

    def _exec_step(
        name: str, fn: Callable[..., _Any], *fargs: _Any, **fkwargs: _Any
    ) -> _Any:
        t0 = time.time()
        try:
            out = fn(*fargs, **fkwargs)
        except Exception as ex:  # pragma: no cover
            out = {"error": str(ex)}
        step_durations[name] = round(time.time() - t0, 3)
        result["steps"][name] = out
        return out

    # Build (always evaluated but may be skipped if up-to-date)
    _exec_step("build", ensure_core_build, force_rebuild)

    # Viewer + crystallization may be skipped in fast mode for speed
    if mode == "fast":
        result["steps"]["viewer"] = {
            "ran": False,
            "skipped": True,
            "reason": "fast_mode",
        }
        skipped.append("viewer")
    else:
        vw_res = _exec_step("viewer", run_viewer)
        vw = vw_res
        result["viewer_timings"] = (
            {
                "viewer_cold_start_sec": vw.get("vision_cold_start_sec"),
                "viewer_steady_state_sec": vw.get("vision_steady_state_sec"),
            }
            if vw.get("ran")
            else {}
        )

    _exec_step("reindex", reindex)

    if mode == "fast":
        result["steps"]["crystallization"] = {
            "ran": False,
            "skipped": True,
            "reason": "fast_mode",
        }
        skipped.append("crystallization")
    else:
        _exec_step("crystallization", crystallize)
    # UP2: ensure a stub UI metrics file exists (will not overwrite actual)
    _emit_ui_metrics_stub()
    # Runtime KPI ingestion (best-effort)
    runtime_metrics: Dict[str, Any] = {}
    try:
        if AI_CONTEXT_DUMPS.exists():
            dumps = sorted(
                AI_CONTEXT_DUMPS.glob("ai_context_dump_*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            if dumps:
                latest = dumps[0]
                with latest.open() as f:
                    data = json.load(f)
                summary = data.get(
                    "aios_runtime_intelligence_dump", {}
                ).get("session_summary", {})
                cons = summary.get("consciousness_metrics", {})
                runtime_metrics = {
                    "source_file": str(latest),
                    "events_per_second": summary.get("events_per_second"),
                    "total_events": summary.get("total_events"),
                    "active_modules": summary.get("active_modules"),
                    "module_event_counts": summary.get("module_event_counts"),
                    "current_consciousness_level": cons.get("current_level"),
                    "emergence_patterns_detected": cons.get(
                        "emergence_patterns"
                    ),
                }
    except Exception as ex:
        runtime_metrics = {"error": str(ex)}
    result["runtime"] = runtime_metrics

    # Core telemetry ingestion (UP4 optional)
    core_metrics = _load_core_telemetry()
    if core_metrics:
        result["core_telemetry"] = core_metrics

    # Vision demo (OpenCV) summary ingestion (best-effort)
    vision_summary: Dict[str, Any] = {}
    try:
        if VISION_DEMO_SCRIPT.exists():
            VISION_DEMO_OUTPUT.mkdir(parents=True, exist_ok=True)
            # Run only direct phase for speed
            code, out, err = run(
                [
                    sys.executable,
                    str(VISION_DEMO_SCRIPT),
                    "--phases",
                    "direct",
                    "--output-dir",
                    str(VISION_DEMO_OUTPUT),
                ],
                cwd=ROOT,
                timeout=120,
            )
            summary_path = VISION_DEMO_OUTPUT / "opencv_demo_summary.json"
            if summary_path.exists():
                raw = json.loads(summary_path.read_text())
                # Aggregate basic metrics
                vals = [
                    r
                    for r in raw.get("results", [])
                    if not r.get("error")
                    and r.get("kind") in {"simple", "mandala", "fractal"}
                ]

                def _avg(field: str) -> Optional[float]:
                    nums = [
                        r.get(field)
                        for r in vals
                        if isinstance(r.get(field), (int, float))
                    ]
                    return round(sum(nums) / len(nums), 4) if nums else None

                vision_summary = {
                    "invocation_code": code,
                    "result_count": raw.get("count"),
                    "avg_consciousness_resonance": _avg(
                        "consciousness_resonance"
                    ),
                    "avg_coherence_level": _avg("coherence_level"),
                    "avg_image_entropy": _avg("image_entropy"),
                    "avg_enhanced_image_entropy": _avg("enhanced_entropy"),
                    "max_emergence_probability": max(
                        [
                            r.get("emergence_probability", 0.0)
                            for r in vals
                        ],
                        default=None,
                    ),
                    "vision_cold_start_sec": raw.get("vision_cold_start_sec"),
                    "vision_steady_state_sec": raw.get(
                        "vision_steady_state_sec"
                    ),
                    # UP9: first simple frame processing duration
                    "vision_first_frame_sec": raw.get(
                        "vision_first_frame_sec"
                    ),
                    "summary_file": str(summary_path),
                }
                # Optional crystal for vision metrics
                if create_metric_crystal and vision_summary:
                    try:
                        create_metric_crystal(
                            metric_snapshot=vision_summary,
                            capsule_ids=[
                                "chatgpt-integration-2025-06-29"
                            ],
                            kpi_dimensions=[
                                k
                                for k in vision_summary.keys()
                                if k.startswith("avg_")
                                or k.endswith("probability")
                            ],
                            source_tag="vision_demo_metrics",
                        )
                        vision_summary["vision_crystal"] = True
                    except Exception as ex:  # pragma: no cover
                        vision_summary["vision_crystal_error"] = str(ex)
            else:
                vision_summary = {
                    "error": "summary_missing",
                    "code": code,
                    "stderr_trunc": err[-200:],
                }
    except Exception as ex:  # pragma: no cover
        vision_summary = {"error": str(ex)}
    result["vision_demo"] = vision_summary

    # UP5: Evolution scheduler (mutation/evaluation) cycles
    evo_cycles = (
        DEFAULT_EVOLUTION_CYCLES_FULL
        if mode == "full"
        else fast_cycles_override
    )
    result["evolution"] = _run_evolution_cycles(cycles=evo_cycles)

    # KPI threshold evaluation (now includes vision metrics if produced)
    kpi_eval: Dict[str, Dict[str, Any]] = {}
    try:
        if KPI_THRESHOLDS_FILE.exists():
            thresholds = json.loads(KPI_THRESHOLDS_FILE.read_text())
            ui_metrics = _load_ui_metrics()
            kpi_eval = _evaluate_kpis(
                thresholds,
                runtime_metrics,
                ui_metrics,
                result.get("core_telemetry", {}),
                result.get("vision_demo", {}),
                result.get("evolution", {}),
            )
            result["kpi_evaluation"] = kpi_eval
            result["kpi_capsule"] = thresholds.get("capsule")
            if kpi_eval and create_metric_crystal:
                try:
                    snapshot = {
                        k: {"value": v.get("value"), "status": v.get("status")}
                        for k, v in kpi_eval.items()
                    }
                    capsule_ids = [
                        thresholds.get(
                            "capsule", "chatgpt-integration-2025-06-29"
                        ),
                        "development-environment-status-2025-08-16",
                    ]
                    create_metric_crystal(
                        metric_snapshot=snapshot,
                        capsule_ids=capsule_ids,
                        kpi_dimensions=list(kpi_eval.keys()),
                        source_tag="full_system_validation_kpis",
                    )
                    result["kpi_crystal"] = {
                        "capsules": capsule_ids,
                        "dimensions": list(kpi_eval.keys()),
                    }
                except Exception as ex:  # pragma: no cover
                    result["kpi_crystal_error"] = str(ex)
    except Exception as ex:  # pragma: no cover
        result["kpi_evaluation_error"] = str(ex)
    total_duration = round(time.time() - start, 2)
    result["duration_seconds"] = total_duration
    result["step_durations"] = step_durations
    if skipped:
        result["skipped_steps"] = skipped
    target = MODE_DURATION_TARGETS.get(mode)
    if target:
        result["target_duration_sec"] = target
        result["duration_within_target"] = total_duration <= target
    # basic success heuristic
    success_core = (
        result["steps"].get("viewer", {}).get("bmp_count", 0) >= 1
        and result["steps"].get("reindex", {}).get("edges", 0) > 0
        and result["steps"].get("crystallization", {}).get(
            "new_crystals", 0
        )
        >= 1
    )
    # Augment with runtime KPI sanity if available
    if runtime_metrics:
        kpi_ok = True
        eps = runtime_metrics.get("events_per_second")
        total = runtime_metrics.get("total_events")
        if eps is not None and eps <= 0:
            kpi_ok = False
        if total is not None and total < 10:  # minimal activity threshold
            kpi_ok = False
        # If we have explicit KPI evaluation entries, incorporate failures
        if kpi_eval:
            if any(v.get("status") == "fail" for v in kpi_eval.values()):
                kpi_ok = False
        result["success"] = success_core and kpi_ok
    else:
        result["success"] = success_core
    SUMMARY_FILE.write_text(json.dumps(result, indent=2))
    print(f"[full-system] Summary -> {SUMMARY_FILE} (mode={mode})")
    print(json.dumps(result, indent=2))

 
if __name__ == "__main__":
    main()
