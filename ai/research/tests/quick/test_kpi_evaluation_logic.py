"""UP8: Focused tests for _evaluate_kpis logic.

Exercises pass/fail/unmeasured across runtime, core, vision, evolution KPI groups.
Side effects avoided for fast feedback.
"""
from pathlib import Path
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


def build_thresholds():
    return {
        "capsule": "chatgpt-integration-2025-06-29",
        "kpis": {
            "runtime_surrogates": {
                "events_per_second": {"min": 0.5},
                "render_fps": {"min": 60},
            },
            "core_metrics": {
                "core_cpu_pct_avg": {"max": 50},
                "core_mem_mb_avg": {"max": 1024}
            },
            "vision_metrics": {
                "vision_cold_start_sec": {"max": 3.0},
                "vision_steady_state_sec": {"max": 0.12},
                "vision_first_frame_sec": {"max": 1.5}
            },
            "evolution_metrics": {
                "best_fitness": {"min": 0.45},
                "average_fitness": {"min": 0.40}
            }
        }
    }


def test_kpi_pass_fail_and_unmeasured():
    thresholds = build_thresholds()
    runtime_metrics = {"events_per_second": 0.75}  # pass
    ui_metrics = {"render_fps": 12.0}  # fail (needs 60)
    core_metrics = {"core_cpu_pct_avg": 10.0, "core_mem_mb_avg": 512.0}  # pass
    vision_summary = {
        "vision_cold_start_sec": 2.0,
        "vision_steady_state_sec": 0.2,  # fails (0.2 > 0.12)
    "vision_first_frame_sec": 1.0,  # pass (1.0 < 1.5)
    }
    evolution = {"best_fitness": 0.5}  # average_fitness unmeasured

    kpi_eval = mod._evaluate_kpis(  # type: ignore
        thresholds,
        runtime_metrics,
        ui_metrics,
        core_metrics,
        vision_summary,
        evolution,
    )

    assert kpi_eval["events_per_second"]["status"] == "pass"
    assert kpi_eval["render_fps"]["status"] == "fail"
    assert kpi_eval["core_cpu_pct_avg"]["status"] == "pass"
    assert kpi_eval["core_mem_mb_avg"]["status"] == "pass"
    assert kpi_eval["vision_cold_start_sec"]["status"] == "pass"
    # 0.2 > 0.12 => fail
    assert kpi_eval["vision_steady_state_sec"]["status"] == "fail"
    assert kpi_eval["vision_first_frame_sec"]["status"] == "pass"
    assert kpi_eval["best_fitness"]["status"] == "pass"
    assert kpi_eval["average_fitness"]["status"] == "unmeasured"


def test_kpi_edge_min_and_max_priority():
    # Ensure max rule can set fail even if min would pass
    thresholds = {"kpis": {"runtime_surrogates": {
        "events_per_second": {"min": 0.5, "max": 1.0}
    }}}
    runtime_metrics = {"events_per_second": 1.5}  # min pass but exceeds max
    kpi_eval = mod._evaluate_kpis(
        thresholds, runtime_metrics, {}, {}, {}, {}
    )  # type: ignore
    assert kpi_eval["events_per_second"]["status"] == "fail"


def test_unmeasured_all_missing():
    thresholds = {"kpis": {"runtime_surrogates": {
        "events_per_second": {"min": 0.1}
    }}}
    kpi_eval = mod._evaluate_kpis(
        thresholds, {}, {}, {}, {}, {}
    )  # type: ignore
    assert kpi_eval["events_per_second"]["status"] == "unmeasured"
