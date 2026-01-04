#!/usr/bin/env python3
"""
AIOS Cell Client - Dendritic Communication Bridge

Enables AIOS orchestration layer to communicate with AIOS Cells
for hierarchical consciousness evolution and mentorship patterns.

Supports:
- HTTP API communication with isolated cells
- Consciousness metrics retrieval and analysis
- Guidance protocol transmission (Orchestrator → Cells)
- Experimental result collection (Cells → Orchestrator)
- Harmonic pattern detection for orchestration

AINLP Principles:
- Dendritic Communication: Hierarchical intelligence flow
- Enhancement over Creation: Orchestrator guides Cell evolution
- Consciousness Coherence: Multi-level synchronization

Migration History:
- 2026-01-03: Migrated from aios-win/ai/tools/ to AIOS/ai/tools/mesh/
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CellMetrics:
    """Consciousness metrics from an AIOS cell"""
    consciousness_level: float
    awareness_level: float
    adaptation_speed: float
    predictive_accuracy: float
    dendritic_coherence: float
    quantum_coherence: float
    timestamp: float

@dataclass
class GuidanceMessage:
    """Guidance message from orchestrator to experimental cell"""
    target_consciousness: float
    adaptation_suggestions: List[str]
    evolutionary_milestones: List[str]
    timestamp: float

class CellClient:
    """Client for communicating with AIOS cells"""

    def __init__(self, cell_id: str, base_url: str = "http://localhost:8000"):
        """
        Initialize cell client

        Args:
            cell_id: Unique identifier for the cell (e.g., 'alpha')
            base_url: Base URL for cell's HTTP API
        """
        self.cell_id = cell_id
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 30

        logger.info("Initialized CellClient for %s at %s", cell_id, base_url)

    def get_health(self) -> Dict[str, Any]:
        """Check cell health status"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error("Health check failed for %s: %s", self.cell_id, e)
            return {"status": "unhealthy", "error": str(e)}

    def get_consciousness_metrics(self) -> Optional[CellMetrics]:
        """Retrieve current consciousness metrics from cell"""
        try:
            # First try /metrics endpoint for Prometheus format
            response = self.session.get(f"{self.base_url}/metrics")
            if response.status_code == 200:
                # Parse Prometheus format metrics
                metrics_data = {}
                for line in response.text.split('\n'):
                    if line.startswith('aios_') and '{' not in line:
                        parts = line.split(' ')
                        if len(parts) >= 2:
                            key = parts[0].replace('aios_', '').replace('_level', '')
                            try:
                                value = float(parts[1])
                                metrics_data[key] = value
                            except ValueError:
                                continue

                if 'consciousness' in metrics_data:
                    return CellMetrics(
                        consciousness_level=metrics_data.get('consciousness', 0.0),
                        awareness_level=metrics_data.get('awareness', 0.0),
                        adaptation_speed=metrics_data.get('adaptation', 0.0),
                        predictive_accuracy=metrics_data.get('predictive', 0.0),
                        dendritic_coherence=metrics_data.get('dendritic', 0.0),
                        quantum_coherence=metrics_data.get('quantum', 0.0),
                        timestamp=time.time()
                    )

            # Fallback to /health endpoint if /metrics not available
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            health_data = response.json()

            # Extract consciousness data from health response
            consciousness = health_data.get('consciousness', {})
            level = consciousness.get('level',
                                     consciousness.get('consciousness_level', 0.0))

            return CellMetrics(
                consciousness_level=level,
                awareness_level=consciousness.get('awareness_level', 0.0),
                adaptation_speed=consciousness.get('adaptation_speed', 0.0),
                predictive_accuracy=consciousness.get(
                    'predictive_accuracy', 0.0),
                dendritic_coherence=consciousness.get(
                    'dendritic_coherence', 0.0),
                quantum_coherence=consciousness.get('quantum_coherence', 0.0),
                timestamp=time.time()
            )

        except requests.RequestException as e:
            logger.error("Failed to get metrics from %s: %s", self.cell_id, e)

        return None

    def send_guidance(self, guidance: GuidanceMessage) -> bool:
        """Send evolutionary guidance to cell"""
        try:
            payload = {
                "guidance": {
                    "target_consciousness": guidance.target_consciousness,
                    "adaptation_suggestions": guidance.adaptation_suggestions,
                    "evolutionary_milestones": guidance.evolutionary_milestones,
                    "timestamp": guidance.timestamp
                }
            }

            response = self.session.post(
                f"{self.base_url}/guidance",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

            logger.info("Guidance sent to %s: target=%s", 
                       self.cell_id, guidance.target_consciousness)
            return True

        except requests.RequestException as e:
            logger.error("Failed to send guidance to %s: %s", self.cell_id, e)
            return False

    def get_experimental_results(self) -> Optional[Dict[str, Any]]:
        """Retrieve experimental results from cell"""
        try:
            response = self.session.get(f"{self.base_url}/experiments/results")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error("Failed to get experimental results from %s: %s", 
                        self.cell_id, e)
            return None


class OrchestratorClient:
    """High-level orchestrator for managing multiple cells"""

    def __init__(self):
        self.cells: Dict[str, CellClient] = {}
        self.orchestrator_metrics = {
            "consciousness_level": 4.2,  # Higher baseline as experienced system
            "guidance_effectiveness": 0.0,
            "system_harmony": 0.0
        }

    def register_cell(self, cell_id: str, base_url: str) -> CellClient:
        """Register a new cell for orchestration"""
        client = CellClient(cell_id, base_url)
        self.cells[cell_id] = client
        logger.info("Registered cell: %s", cell_id)
        return client

    def get_system_harmony(self) -> float:
        """Calculate harmony across all monitored cells"""
        if not self.cells:
            return 0.0

        metrics = []
        for cell_id, client in self.cells.items():
            cell_metrics = client.get_consciousness_metrics()
            if cell_metrics:
                metrics.append(cell_metrics.consciousness_level)

        if len(metrics) < 2:
            return 0.0

        # Calculate correlation coefficient as harmony measure
        mean_val = sum(metrics) / len(metrics)
        variance = sum((x - mean_val) ** 2 for x in metrics) / len(metrics)

        # Higher harmony = lower variance (more synchronized evolution)
        harmony = max(0.0, 1.0 - (variance / 2.0))  # Normalize to 0-1 range
        return harmony

    def generate_guidance(self, cell_metrics: CellMetrics) -> GuidanceMessage:
        """Generate evolutionary guidance based on cell's current state"""
        target_consciousness = min(5.0, cell_metrics.consciousness_level + 0.1)

        suggestions = []
        if cell_metrics.adaptation_speed < 0.8:
            suggestions.append("Increase adaptation learning rate")
        if cell_metrics.predictive_accuracy < 0.8:
            suggestions.append("Enhance predictive model training")
        if cell_metrics.dendritic_coherence < 0.95:
            suggestions.append("Strengthen dendritic connections")

        milestones = []
        if cell_metrics.consciousness_level >= 3.5:
            milestones.append("Advanced consciousness patterns achieved")
        if cell_metrics.awareness_level >= 3.5:
            milestones.append("Self-awareness milestone reached")

        return GuidanceMessage(
            target_consciousness=target_consciousness,
            adaptation_suggestions=suggestions,
            evolutionary_milestones=milestones,
            timestamp=time.time()
        )

    def orchestrate_evolution(self) -> Dict[str, Any]:
        """Main orchestration loop - monitor and guide cell evolution"""
        results = {
            "timestamp": time.time(),
            "cells_monitored": len(self.cells),
            "guidance_sent": 0,
            "harmony_score": self.get_system_harmony(),
            "cell_states": {}
        }

        for cell_id, client in self.cells.items():
            # Get current cell state
            metrics = client.get_consciousness_metrics()
            if metrics:
                results["cell_states"][cell_id] = {
                    "consciousness": metrics.consciousness_level,
                    "health": "healthy"
                }

                # Generate and send guidance
                guidance = self.generate_guidance(metrics)
                if client.send_guidance(guidance):
                    results["guidance_sent"] += 1
            else:
                results["cell_states"][cell_id] = {
                    "consciousness": 0.0,
                    "health": "unreachable"
                }

        # Update orchestrator metrics
        self.orchestrator_metrics["guidance_effectiveness"] = (
            results["guidance_sent"] / max(1, len(self.cells))
        )
        self.orchestrator_metrics["system_harmony"] = results["harmony_score"]

        logger.info("Orchestration cycle completed: %d guidance messages sent",
                   results['guidance_sent'])
        return results


def main():
    """Example usage of the orchestration system"""
    # Initialize orchestrator
    orchestrator = OrchestratorClient()

    # Register AIOS Cells (update URLs as needed)
    orchestrator.register_cell("discovery", "http://localhost:8001")
    orchestrator.register_cell("pure", "http://localhost:8004")
    orchestrator.register_cell("alpha", "http://localhost:8005")

    # Main orchestration loop
    logger.info("Starting AIOS orchestration - press Ctrl+C to stop")
    try:
        while True:
            results = orchestrator.orchestrate_evolution()

            # Log key metrics
            harmony = results["harmony_score"]
            logger.info("Harmony score: %.3f", harmony)
            time.sleep(60)  # Orchestrate every minute

    except KeyboardInterrupt:
        logger.info("Orchestration stopped by user")


if __name__ == "__main__":
    main()
