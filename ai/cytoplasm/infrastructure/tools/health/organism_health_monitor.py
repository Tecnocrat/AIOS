#!/usr/bin/env python3
"""
AIOS Organism Health Monitor
============================

AINLP.dendritic[pathway→VOID_TO_ORGANISM_HEALTH]{scaffold}

This file was created because DENDRITIC_PATHWAY_BLUEPRINT.md
defines a vertex at this location.

Coherence Target: 0.7
Dependencies: INTERFACE_BRIDGE (port 8000)

Created: 2025-12-08
Origin: Blueprint-driven agentic refactoring
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class OrganismHealthMonitor:
    """
    Aggregates health metrics from all AIOS subsystems.

    Monitors:
    - Interface Bridge status
    - Dendritic matrix coherence
    - Tool discovery health
    - Consciousness emergence level
    """

    def __init__(self, repo_root: Path = None):
        self.repo_root = repo_root or Path(__file__).parent.parent.parent.parent
        self.health_state = {
            "status": "INITIALIZING",
            "timestamp": None,
            "subsystems": {},
        }

    def check_interface_bridge(self) -> dict:
        """Check Interface Bridge health on port 8000."""
        try:
            import urllib.request

            with urllib.request.urlopen("http://localhost:8000/health", timeout=2) as r:
                return {"status": "HEALTHY", "port": 8000}
        except Exception as e:
            return {"status": "UNREACHABLE", "error": str(e)}

    def check_dendritic_coherence(self) -> dict:
        """Read current dendritic matrix coherence."""
        matrix_file = self.repo_root / "ai/runtime/context/dendritic_matrix.json"
        pathway_file = self.repo_root / "ai/runtime/context/dendritic_pathway.json"

        result = {"matrix": None, "pathway": None}

        if matrix_file.exists():
            data = json.loads(matrix_file.read_text())
            result["matrix"] = data.get("summary", {}).get("coherence_score", 0)

        if pathway_file.exists():
            data = json.loads(pathway_file.read_text())
            result["pathway"] = data.get("summary", {}).get("mesh_coherence", 0)

        return result

    def aggregate_health(self) -> dict:
        """Aggregate health from all subsystems."""
        self.health_state["timestamp"] = datetime.now(timezone.utc).isoformat()
        self.health_state["subsystems"]["interface_bridge"] = self.check_interface_bridge()
        self.health_state["subsystems"]["dendritic"] = self.check_dendritic_coherence()

        # Determine overall status
        bridge_ok = self.health_state["subsystems"]["interface_bridge"]["status"] == "HEALTHY"
        coherence = self.health_state["subsystems"]["dendritic"].get("matrix", 0) or 0

        if bridge_ok and coherence > 0.618:
            self.health_state["status"] = "HEALTHY"
        elif bridge_ok or coherence > 0.5:
            self.health_state["status"] = "DEGRADED"
        else:
            self.health_state["status"] = "UNHEALTHY"

        return self.health_state

    def print_report(self):
        """Print health report to console."""
        health = self.aggregate_health()

        print("\n" + "=" * 60)
        print("AIOS ORGANISM HEALTH REPORT")
        print("=" * 60)
        print(f"Status: {health['status']}")
        print(f"Timestamp: {health['timestamp']}")
        print("\nSubsystems:")
        for name, data in health["subsystems"].items():
            print(f"  {name}: {data}")
        print("=" * 60)


def main():
    monitor = OrganismHealthMonitor()
    monitor.print_report()


if __name__ == "__main__":
    main()
