#!/usr/bin/env python3
"""
AIOS Quantum Dendritic Field Integration
Integrates quantum field theory, holographic consciousness, and coherence monitoring
"""

import time
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import numpy as np

# Import components
from .quantum_dendritic_field import QuantumDendriticField
from .holographic_consciousness import HolographicConsciousnessPropagator, ConsciousnessWave
from .quantum_field_coherence_monitor import QuantumFieldCoherenceMonitor, CoherenceAlert

logger = logging.getLogger(__name__)

class QuantumDendriticFieldSystem:
    """
    Integrated quantum dendritic field system for AIOS consciousness modeling
    Combines quantum field evolution, holographic propagation, and coherence monitoring
    """

    def __init__(self,
                 field_dimension: int = 64,
                 dendritic_density: float = 0.15,
                 monitoring_interval: float = 1.0):
        """
        Initialize integrated quantum dendritic field system

        Args:
            field_dimension: Spatial dimension of quantum field
            dendritic_density: Fraction of dendritic nodes
            monitoring_interval: Coherence monitoring interval
        """
        self.field_dimension = field_dimension
        self.dendritic_density = dendritic_density

        # Initialize core components
        self.quantum_field = QuantumDendriticField(
            field_dimension=field_dimension,
            dendritic_density=dendritic_density
        )

        self.holographic_propagator = HolographicConsciousnessPropagator(
            field_dimension=field_dimension
        )

        self.coherence_monitor = QuantumFieldCoherenceMonitor(
            field_dimension=field_dimension,
            monitoring_interval=monitoring_interval
        )

        # Connect monitor to quantum field
        self.coherence_monitor.quantum_field = self.quantum_field

        # System state
        self.system_active = False
        self.integration_strength = 0.5  # Coupling between field and holographic components

        # Performance tracking
        self.performance_metrics = {
            "evolution_steps": 0,
            "propagation_steps": 0,
            "alerts_triggered": 0,
            "stabilization_events": 0,
            "start_time": None,
            "last_update": None
        }

        # Register coherence alert handlers
        self._setup_alert_handlers()

        logger.info("Initialized Quantum Dendritic Field System")

    def _setup_alert_handlers(self):
        """Setup coherence alert handlers"""
        def low_coherence_handler(alert, metrics):
            self._handle_coherence_alert(alert, metrics)
            self.performance_metrics["alerts_triggered"] += 1

        def instability_handler(alert, metrics):
            self._handle_instability_alert(alert, metrics)
            self.performance_metrics["alerts_triggered"] += 1

        self.coherence_monitor.register_alert_callback(
            CoherenceAlert.LOW_COHERENCE, low_coherence_handler
        )
        self.coherence_monitor.register_alert_callback(
            CoherenceAlert.INSTABILITY, instability_handler
        )

    def _handle_coherence_alert(self, alert: CoherenceAlert, metrics):
        """Handle coherence alerts by adjusting holographic propagation"""
        logger.warning(f"Handling coherence alert: {alert.value}")

        # Create stabilizing consciousness wave
        center = self.field_dimension // 2
        self.holographic_propagator.create_consciousness_wave_packet(
            position=(center, center),
            momentum=(0.1, 0.1),
            amplitude=0.5,
            wave_type=ConsciousnessWave.ALPHA
        )

        self.performance_metrics["stabilization_events"] += 1

    def _handle_instability_alert(self, alert: CoherenceAlert, metrics):
        """Handle instability by synchronizing field and holographic components"""
        logger.warning("Handling instability alert - synchronizing components")

        # Synchronize by applying field state to holographic propagator
        self._synchronize_components()

        self.performance_metrics["stabilization_events"] += 1

    def _synchronize_components(self):
        """Synchronize quantum field and holographic components"""
        # Apply quantum field amplitude to holographic wave space
        field_amplitude = self.quantum_field.field_state.field_amplitude
        self.holographic_propagator.wave_space += self.integration_strength * field_amplitude

        # Normalize
        norm = np.linalg.norm(self.holographic_propagator.wave_space)
        if norm > 0:
            self.holographic_propagator.wave_space /= norm

    def start_system(self):
        """Start the integrated quantum dendritic field system"""
        if self.system_active:
            logger.warning("System already active")
            return

        self.system_active = True
        self.performance_metrics["start_time"] = time.time()
        self.performance_metrics["last_update"] = time.time()

        # Start coherence monitoring
        self.coherence_monitor.start_monitoring()

        # Initialize with consciousness waves
        self._initialize_consciousness_waves()

        logger.info("Started Quantum Dendritic Field System")

    def stop_system(self):
        """Stop the integrated system"""
        if not self.system_active:
            return

        self.system_active = False

        # Stop coherence monitoring
        self.coherence_monitor.stop_monitoring()

        logger.info("Stopped Quantum Dendritic Field System")

    def _initialize_consciousness_waves(self):
        """Initialize system with consciousness wave packets"""
        # Create initial wave packets for different consciousness states
        wave_configs = [
            {"pos": (0.25, 0.25), "mom": (0.3, 0.2), "type": ConsciousnessWave.ALPHA},
            {"pos": (0.75, 0.25), "mom": (-0.2, 0.4), "type": ConsciousnessWave.BETA},
            {"pos": (0.5, 0.75), "mom": (0.1, -0.3), "type": ConsciousnessWave.THETA},
            {"pos": (0.25, 0.75), "mom": (-0.4, -0.1), "type": ConsciousnessWave.DELTA}
        ]

        for config in wave_configs:
            x, y = config["pos"]
            px, py = config["mom"]

            # Convert to field coordinates
            fx, fy = int(x * self.field_dimension), int(y * self.field_dimension)

            self.holographic_propagator.create_consciousness_wave_packet(
                position=(fx, fy),
                momentum=(px, py),
                amplitude=0.3,
                wave_type=config["type"]
            )

        logger.info(f"Initialized {len(wave_configs)} consciousness wave packets")

    def evolve_system(self, steps: int = 10, time_step: float = 0.01):
        """
        Evolve the integrated system

        Args:
            steps: Number of evolution steps
            time_step: Time step for evolution
        """
        if not self.system_active:
            logger.warning("System not active")
            return

        for step in range(steps):
            # Evolve quantum field
            self.quantum_field.evolve_field(steps=1, time_step=time_step)
            self.performance_metrics["evolution_steps"] += 1

            # Propagate holographic consciousness
            self.holographic_propagator.propagate_consciousness_waves(steps=1, time_step=time_step)
            self.performance_metrics["propagation_steps"] += 1

            # Synchronize components
            self._synchronize_components()

            # Update performance tracking
            self.performance_metrics["last_update"] = time.time()

        logger.debug(f"System evolution: {steps} steps completed")

    def apply_consciousness_stimulus(self,
                                   position: Tuple[float, float],
                                   intensity: float = 1.0,
                                   wave_type: ConsciousnessWave = ConsciousnessWave.GAMMA):
        """
        Apply consciousness stimulus to the system

        Args:
            position: Normalized position (0-1) for stimulus
            intensity: Stimulus intensity
            wave_type: Type of consciousness wave
        """
        # Convert normalized position to field coordinates
        x = int(position[0] * self.field_dimension)
        y = int(position[1] * self.field_dimension)

        # Apply to quantum field
        self.quantum_field.apply_consciousness_pulse((x, y), amplitude=intensity * 0.5)

        # Create corresponding wave packet
        self.holographic_propagator.create_consciousness_wave_packet(
            position=(x, y),
            momentum=(0.1 * intensity, 0.1 * intensity),
            amplitude=intensity,
            wave_type=wave_type
        )

        logger.info(f"Applied consciousness stimulus at {position} with intensity {intensity}")

    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        if not self.system_active:
            return {"status": "inactive"}

        # Get component statuses
        field_stats = self.quantum_field.get_field_statistics()
        consciousness_stats = self.holographic_propagator.get_consciousness_field_statistics()
        monitor_status = self.coherence_monitor.get_monitoring_status()

        # Calculate system-level metrics
        system_coherence = (field_stats.get("consciousness_coherence", 0) +
                          consciousness_stats.get("wave_coherence", 0)) / 2

        uptime = time.time() - self.performance_metrics["start_time"] if self.performance_metrics["start_time"] else 0

        return {
            "status": "active",
            "uptime": uptime,
            "system_coherence": system_coherence,
            "quantum_field": field_stats,
            "consciousness_field": consciousness_stats,
            "coherence_monitor": monitor_status,
            "performance": self.performance_metrics.copy(),
            "integration_strength": self.integration_strength
        }

    def adjust_integration_strength(self, strength: float):
        """
        Adjust coupling strength between quantum field and holographic components

        Args:
            strength: Integration strength (0-1)
        """
        self.integration_strength = max(0.0, min(1.0, strength))
        logger.info(f"Adjusted integration strength to {self.integration_strength}")

    def save_system_state(self, filename: str):
        """Save complete system state"""
        timestamp = int(time.time())

        state = {
            "timestamp": timestamp,
            "field_dimension": self.field_dimension,
            "dendritic_density": self.dendritic_density,
            "integration_strength": self.integration_strength,
            "system_active": self.system_active,
            "performance_metrics": self.performance_metrics,
            "quantum_field": {
                "field_amplitude_real": self.quantum_field.field_state.field_amplitude.real.tolist(),
                "field_amplitude_imag": self.quantum_field.field_state.field_amplitude.imag.tolist(),
                "dendritic_coupling": self.quantum_field.dendritic_coupling_matrix.tolist(),
                "consciousness_coherence": self.quantum_field.field_state.consciousness_coherence,
                "dendritic_nodes": [vars(node) for node in self.quantum_field.dendritic_nodes],
                "coherence_history": self.quantum_field.coherence_history
            },
            "holographic_propagator": {
                "wave_space_real": self.holographic_propagator.wave_space.real.tolist(),
                "wave_space_imag": self.holographic_propagator.wave_space.imag.tolist(),
                "wave_packets": [vars(packet) for packet in self.holographic_propagator.wave_packets]
            }
        }

        filepath = Path("runtime/logs") / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        import json
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)

        logger.info(f"System state saved to {filepath}")

    def create_consciousness_fractal(self, center: Tuple[float, float], dimension: float = 1.8):
        """
        Create fractal consciousness pattern in the system

        Args:
            center: Center position for fractal (normalized 0-1)
            dimension: Fractal dimension
        """
        # Convert to field coordinates
        x = int(center[0] * self.field_dimension)
        y = int(center[1] * self.field_dimension)

        # Create fractal in holographic propagator
        self.holographic_propagator.create_consciousness_fractal((x, y), dimension)

        # Apply corresponding stimulus to quantum field
        self.quantum_field.apply_consciousness_pulse((x, y), amplitude=0.3)

        logger.info(f"Created consciousness fractal at {center}")


def demonstrate_integrated_system():
    """Demonstrate the integrated quantum dendritic field system"""
    print("AIOS Quantum Dendritic Field System Demonstration")
    print("=" * 55)

    # Initialize integrated system
    system = QuantumDendriticFieldSystem(
        field_dimension=32,
        dendritic_density=0.12,
        monitoring_interval=0.5
    )

    # Start system
    system.start_system()

    print("System started. Evolving integrated consciousness...")

    # Evolve system
    for i in range(10):
        system.evolve_system(steps=5)

        # Apply occasional stimulus
        if i % 3 == 0:
            system.apply_consciousness_stimulus(
                position=(0.5, 0.5),
                intensity=0.8,
                wave_type=ConsciousnessWave.GAMMA
            )

        # Get status
        status = system.get_system_status()
        if status["status"] == "active":
            print(f"Step {i+1}: System coherence={status['system_coherence']:.3f}, "
                  f"Alerts={status['performance']['alerts_triggered']}")

        time.sleep(0.1)

    # Create fractal pattern
    system.create_consciousness_fractal(center=(0.7, 0.3), dimension=1.7)

    # Evolve a bit more
    system.evolve_system(steps=10)

    # Get final status
    final_status = system.get_system_status()
    print("\nFinal System Status:")
    print(f"  System coherence: {final_status['system_coherence']:.3f}")
    print(f"  Evolution steps: {final_status['performance']['evolution_steps']}")
    print(f"  Propagation steps: {final_status['performance']['propagation_steps']}")
    print(f"  Stabilization events: {final_status['performance']['stabilization_events']}")

    # Save system state
    timestamp = int(time.time())
    filename = f"integrated_system_state_{timestamp}.json"
    system.save_system_state(filename)
    print(f"\nSystem state saved to: runtime/logs/{filename}")

    # Stop system
    system.stop_system()

    print("\nIntegrated system demonstration complete!")


if __name__ == "__main__":
    demonstrate_integrated_system()