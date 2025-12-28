"""Structured safety demonstration helpers.

Ingested from legacy root safety_demonstration.py.
All functions return structured dictionaries (no printing).
"""

from __future__ import annotations

from typing import Any, Dict
import time

from safety_governor import (
    SafetyLevel,
    EmergencyReason,
    get_safety_governor,
)
from evolutionary_code_mutator import EvolutionaryCodeMutator
from evolution_lab_manager import EvolutionLabManager  # noqa: F401

_SEED_MINI = (
    "\n# Probe seed\n"
    "def probe():\n"
    "    return 1\n"
    "\nif __name__ == '__main__':\n"
    "    print(probe())\n"
)


def run_safety_session_demo(duration_minutes: int = 2) -> Dict[str, Any]:
    """Run a supervised session safety demo.

    1. Attempt an unauthorized population creation (should be blocked).
    2. Start a supervised session.
    3. Create a population & mutate once.
    4. Perform human check-in and end session.
    """

    gov = get_safety_governor()
    initial = gov.get_status()

    unauthorized_attempt: Dict[str, Any] = {}
    try:
        probe_mutator = EvolutionaryCodeMutator()
        probe_mutator.create_population("unauth_probe", _SEED_MINI, 2)
        unauthorized_attempt["blocked"] = False
        unauthorized_attempt["message"] = (
            "Population creation unexpectedly allowed pre-authorization"
        )
    except Exception as e:  # Expected: safety layer should block
        unauthorized_attempt["blocked"] = True
        unauthorized_attempt["message"] = str(e)

    authorized = gov.start_supervised_session(
        experiment_description="Structured safety session demo",
        safety_level=SafetyLevel.SUPERVISED,
        duration_minutes=duration_minutes,
        authorized_by="safety_demo_ingestion",
    )

    mutation_result: Dict[str, Any] = {}
    if authorized:
        mutator = EvolutionaryCodeMutator()
        seed_code = (
            'def hello_world():\n'
            '    return "Hello, World!"\n'
            '\nif __name__ == "__main__":\n'
            '    print(hello_world())\n'
        )
        pop = mutator.create_population("safety_ingest_demo", seed_code, 3)
        mutation_result["population_size"] = len(pop.organisms)
        if pop.organisms:
            try:
                mutated = mutator.mutate_organism(pop.organisms[0])
                mutation_result["mutation"] = {"ok": True, "id": mutated.id}
            except Exception as e:  # pragma: no cover
                mutation_result["mutation"] = {"ok": False, "error": str(e)}
        gov.human_check_in("safety_demo_ingestion")
        time.sleep(0.2)
        gov.end_session("safety_demo_ingestion")

    final_status = gov.get_status()
    return {
        "initial_status": initial,
        "unauthorized_attempt": unauthorized_attempt,
        "authorized": authorized,
        "mutation_result": mutation_result,
        "final_status": final_status,
    }


def run_emergency_shutdown_demo() -> Dict[str, Any]:
    """Trigger an emergency shutdown inside a supervised session."""

    gov = get_safety_governor()
    started = gov.start_supervised_session(
        "Emergency shutdown structured demo",
        SafetyLevel.SUPERVISED,
        1,
        "safety_demo_ingestion",
    )
    emergency: Dict[str, Any] = {}
    if started:
        time.sleep(0.1)
        gov.emergency_shutdown(
            EmergencyReason.HUMAN_INTERVENTION,
            "Structured emergency demonstration",
        )
        status = gov.get_status()
        emergency = {
            "emergency_stopped": status.get("emergency_stopped"),
            "session_active": status.get("session_active"),
        }
    return {"session_started": started, "emergency_status": emergency}
