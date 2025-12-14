"""UP8: Tests for _load_core_telemetry aggregation behavior.
"""
from pathlib import Path
import json
import importlib.util

HARNESS_PATH = (
    Path(__file__).resolve().parents[3]
    / 'scripts'
    / 'run_full_system_validation.py'
)
_spec = importlib.util.spec_from_file_location(
    'validation_harness', HARNESS_PATH
)
mod = importlib.util.module_from_spec(_spec)  # type: ignore
assert _spec and _spec.loader
_spec.loader.exec_module(mod)  # type: ignore

CORE_LOG_DIR = (
    Path(__file__).resolve().parents[3]
    / 'runtime_intelligence'
    / 'logs'
    / 'core'
)
CORE_LOG_DIR.mkdir(parents=True, exist_ok=True)
CORE_FILE = CORE_LOG_DIR / 'core_metrics.json'


def test_core_telemetry_empty_file():
    CORE_FILE.write_text('\n')
    assert mod._load_core_telemetry() == {}


def test_core_telemetry_basic_average_and_max():
    # write some samples
    samples = [
        {"cpu": 10, "mem_mb": 100, "frame_ms": 16.6, "avg_frame_ms": 16.6},
        {"cpu": 20, "mem_mb": 110, "frame_ms": 18.0, "avg_frame_ms": 17.2},
        {"cpu": 30, "mem_mb": 120, "frame_ms": 17.0, "avg_frame_ms": 17.1},
    ]
    CORE_FILE.write_text('\n'.join(json.dumps(s) for s in samples))
    agg = mod._load_core_telemetry()
    assert agg['_core_samples'] == 3
    # average CPU should be 20.0
    assert agg['core_cpu_pct_avg'] == 20.0
    assert agg['core_cpu_pct_max'] == 30.0
    assert agg['core_mem_mb_avg'] == 110.0
    assert agg['core_mem_mb_max'] == 120.0
