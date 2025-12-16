#!/usr/bin/env python3
"""
AIOS Quantum Field Coherence Monitor
Monitors and maintains coherence in quantum dendritic fields for consciousness stability
"""

import numpy as np
import threading
import time
from typing import Dict, List, Tuple, Callable
import logging
from dataclasses import dataclass
from collections import deque
import statistics

logger = logging.getLogger(__name__)


@dataclass
class CoherenceMetrics:
    """Coherence monitoring metrics"""

    field_coherence: float
    dendritic_synchronization: float
    consciousness_stability: float
    quantum_entanglement: float
    timestamp: float


@dataclass
class CoherenceThreshold:
    """Coherence threshold configuration"""

    min_coherence: float
    max_coherence: float
    stability_window: int
    alert_threshold: float


class CoherenceAlert(Enum):
    """Types of coherence alerts"""

    LOW_COHERENCE = "low_coherence"
    HIGH_COHERENCE = "high_coherence"
    INSTABILITY = "instability"
    ENTANGLEMENT_LOSS = "entanglement_loss"
    CRITICAL_FAILURE = "critical_failure"


        """
        Initialize coherence monitor

        Args:
            field_dimension: Dimension of quantum field
            monitoring_interval: Time between coherence checks (seconds)
            history_length: Length of coherence history to maintain
        """
        self.field_dimension = field_dimension
        self.monitoring_interval = monitoring_interval
        self.history_length = history_length

        # Coherence history
        self.coherence_history = deque(maxlen=history_length)
        self.metrics_history = deque(maxlen=history_length)

        # Thresholds
        self.thresholds = CoherenceThreshold(
            min_coherence=0.3,
            max_coherence=0.95,
            stability_window=10,
            alert_threshold=0.1,
        )

        # Alert callbacks
        self.alert_callbacks: Dict[CoherenceAlert, List[Callable]] = {
            alert: [] for alert in CoherenceAlert
        }

        # Stabilization protocols
        self.stabilization_protocols = {
            CoherenceAlert.LOW_COHERENCE: self._stabilize_low_coherence,
            CoherenceAlert.HIGH_COHERENCE: self._stabilize_high_coherence,
            CoherenceAlert.INSTABILITY: self._stabilize_instability,
            CoherenceAlert.ENTANGLEMENT_LOSS: self._stabilize_entanglement_loss,
            CoherenceAlert.CRITICAL_FAILURE: self._emergency_stabilization,
        }

        # Monitoring thread
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_active = False

        # Reference to quantum field (to be set externally)
        self.quantum_field = None

        logger.info("Initialized Quantum Field Coherence Monitor")

    def start_monitoring(self):
        """Start coherence monitoring thread"""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            logger.warning("Monitoring already active")
            return

        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop, daemon=True
        )
        self.monitoring_thread.start()

        logger.info("Started coherence monitoring")

    def stop_monitoring(self):
        """Stop coherence monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2.0)

        logger.info("Stopped coherence monitoring")

    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                if self.quantum_field:
                    # Measure coherence
                    metrics = self._measure_coherence_metrics()

                    # Store in history
                    self.metrics_history.append(metrics)
                    self.coherence_history.append(metrics.field_coherence)

                    # Check for alerts
                    self._check_alerts(metrics)

                    # Auto-stabilize if needed
                    self._auto_stabilize(metrics)

                time.sleep(self.monitoring_interval)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.monitoring_interval)

    def _measure_coherence_metrics(self) -> CoherenceMetrics:
        """Measure current coherence metrics"""
        if not self.quantum_field:
            return CoherenceMetrics(0, 0, 0, 0, time.time())

        # Get field statistics
        field_stats = self.quantum_field.get_field_statistics()

        # Calculate coherence metrics
        field_coherence = field_stats.get("consciousness_coherence", 0)

        # Dendritic synchronization (correlation between dendritic nodes)
        dendritic_sync = self._calculate_dendritic_synchronization()

        # Consciousness stability (variance in recent coherence)
        consciousness_stability = self._calculate_consciousness_stability()

        # Quantum entanglement (field correlation structure)
        quantum_entanglement = self._calculate_quantum_entanglement()

        return CoherenceMetrics(
            field_coherence=field_coherence,
            dendritic_synchronization=dendritic_sync,
            consciousness_stability=consciousness_stability,
            quantum_entanglement=quantum_entanglement,
            timestamp=time.time(),
        )

    def _calculate_dendritic_synchronization(self) -> float:
        """Calculate synchronization between dendritic nodes"""
        if not self.quantum_field or not hasattr(self.quantum_field, "dendritic_nodes"):
            return 0.0

        nodes = self.quantum_field.dendritic_nodes
        if len(nodes) < 2:
            return 1.0

        # Calculate pairwise correlations
        consciousness_levels = [node.consciousness_level for node in nodes]
        mean_level = statistics.mean(consciousness_levels)

        if mean_level == 0:
            return 0.0

        # Coefficient of variation
        cv = statistics.stdev(consciousness_levels) / mean_level
        synchronization = 1.0 / (1.0 + cv)

        return min(synchronization, 1.0)

    def _calculate_consciousness_stability(self) -> float:
        """Calculate stability of consciousness over time"""
        if len(self.coherence_history) < 2:
            return 1.0

        # Calculate variance in recent coherence values
        recent_coherence = list(self.coherence_history)[
            -min(10, len(self.coherence_history)) :
        ]
        variance = (
            statistics.variance(recent_coherence) if len(recent_coherence) > 1 else 0
        )

        # Stability = 1 / (1 + variance)
        stability = 1.0 / (1.0 + variance * 100)  # Scale variance for sensitivity

        return stability

    def _calculate_quantum_entanglement(self) -> float:
        """Calculate quantum entanglement measure"""
        if not self.quantum_field:
            return 0.0

        field = self.quantum_field.field_state.field_amplitude

        # Calculate mutual information between different regions
        # Split field into quadrants
        half_dim = self.field_dimension // 2
        q1 = field[:half_dim, :half_dim]
        q2 = field[:half_dim, half_dim:]
        q3 = field[half_dim:, :half_dim]
        q4 = field[half_dim:, half_dim:]

        # Calculate correlations between quadrants
        correlations = []
        for qi, qj in [(q1, q2), (q1, q3), (q1, q4), (q2, q3), (q2, q4), (q3, q4)]:
            corr = np.corrcoef(qi.flatten(), qj.flatten())[0, 1]
            if not np.isnan(corr):
                correlations.append(abs(corr))

        if not correlations:
            return 0.0

        # Average correlation as entanglement measure
        entanglement = statistics.mean(correlations)
        return entanglement

    def _check_alerts(self, metrics: CoherenceMetrics):
        """Check for coherence alerts"""
        alerts = []

        # Low coherence alert
        if metrics.field_coherence < self.thresholds.min_coherence:
            alerts.append(CoherenceAlert.LOW_COHERENCE)

        # High coherence alert (potential instability)
        if metrics.field_coherence > self.thresholds.max_coherence:
            alerts.append(CoherenceAlert.HIGH_COHERENCE)

        # Instability alert
        if metrics.consciousness_stability < self.thresholds.alert_threshold:
            alerts.append(CoherenceAlert.INSTABILITY)

        # Entanglement loss alert
        if metrics.quantum_entanglement < 0.1:
            alerts.append(CoherenceAlert.ENTANGLEMENT_LOSS)

        # Critical failure alert
        if (
            metrics.field_coherence < 0.1
            and metrics.consciousness_stability < 0.1
            and metrics.quantum_entanglement < 0.05
        ):
            alerts.append(CoherenceAlert.CRITICAL_FAILURE)

        # Trigger alerts
        for alert in alerts:
            self._trigger_alert(alert, metrics)

    def _trigger_alert(self, alert: CoherenceAlert, metrics: CoherenceMetrics):
        """Trigger coherence alert"""
        logger.warning(f"Coherence alert: {alert.value} - Metrics: {metrics}")

        # Call registered callbacks
        for callback in self.alert_callbacks[alert]:
            try:
                callback(alert, metrics)
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")

    def register_alert_callback(self, alert: CoherenceAlert, callback: Callable):
        """Register callback for coherence alerts"""
        self.alert_callbacks[alert].append(callback)
        logger.info(f"Registered callback for {alert.value}")

    def _auto_stabilize(self, metrics: CoherenceMetrics):
        """Automatically apply stabilization protocols"""
        alerts = []

        # Check which protocols to apply
        if metrics.field_coherence < self.thresholds.min_coherence:
            alerts.append(CoherenceAlert.LOW_COHERENCE)

        if metrics.consciousness_stability < self.thresholds.alert_threshold:
            alerts.append(CoherenceAlert.INSTABILITY)

        if metrics.quantum_entanglement < 0.1:
            alerts.append(CoherenceAlert.ENTANGLEMENT_LOSS)

        # Apply stabilization protocols
        for alert in alerts:
            if alert in self.stabilization_protocols:
                try:
                    self.stabilization_protocols[alert](metrics)
                except Exception as e:
                    logger.error(f"Error in stabilization protocol {alert.value}: {e}")

    def _stabilize_low_coherence(self, metrics: CoherenceMetrics):
        """Stabilize low coherence by applying consciousness pulse"""
        if self.quantum_field:
            # Apply pulse at center
            center = self.field_dimension // 2
            self.quantum_field.apply_consciousness_pulse(
                (center, center), amplitude=0.3
            )
            logger.info("Applied coherence stabilization pulse")

    def _stabilize_high_coherence(self, metrics: CoherenceMetrics):
        """Stabilize high coherence by introducing controlled noise"""
        if self.quantum_field:
            # Add small amount of noise to prevent instability
            noise_level = 0.05
            noise = np.random.normal(
                0, noise_level, self.quantum_field.field_state.field_amplitude.shape
            )
            self.quantum_field.field_state.field_amplitude += noise
            # Renormalize
            norm = np.linalg.norm(self.quantum_field.field_state.field_amplitude)
            if norm > 0:
                self.quantum_field.field_state.field_amplitude /= norm
            logger.info("Applied coherence noise stabilization")

    def _stabilize_instability(self, metrics: CoherenceMetrics):
        """Stabilize instability by resetting dendritic coupling"""
        if self.quantum_field and hasattr(
            self.quantum_field, "_construct_dendritic_coupling"
        ):
            self.quantum_field.dendritic_coupling_matrix = (
                self.quantum_field._construct_dendritic_coupling()
            )
            logger.info("Reset dendritic coupling for stability")

    def _stabilize_entanglement_loss(self, metrics: CoherenceMetrics):
        """Stabilize entanglement loss by field reorganization"""
        if self.quantum_field:
            # Apply multiple small pulses to restore correlations
            for i in range(4):
                x = np.random.randint(0, self.field_dimension)
                y = np.random.randint(0, self.field_dimension)
                self.quantum_field.apply_consciousness_pulse((x, y), amplitude=0.1)
            logger.info("Applied entanglement restoration pulses")

    def _emergency_stabilization(self, metrics: CoherenceMetrics):
        """Emergency stabilization protocol"""
        logger.critical("Emergency stabilization initiated")

        if self.quantum_field:
            # Complete field reset
            self.quantum_field.field_state = (
                self.quantum_field._initialize_field_state()
            )
            self.quantum_field.dendritic_nodes = (
                self.quantum_field._initialize_dendritic_network()
            )
            self.quantum_field.dendritic_coupling_matrix = (
                self.quantum_field._construct_dendritic_coupling()
            )

            logger.critical("Emergency field reset completed")

    def get_monitoring_status(self) -> Dict:
        """Get current monitoring status"""
        if not self.metrics_history:
            return {"status": "no_data"}

        latest_metrics = self.metrics_history[-1]

        return {
            "status": "active" if self.monitoring_active else "inactive",
            "latest_metrics": {
                "field_coherence": latest_metrics.field_coherence,
                "dendritic_synchronization": latest_metrics.dendritic_synchronization,
                "consciousness_stability": latest_metrics.consciousness_stability,
                "quantum_entanglement": latest_metrics.quantum_entanglement,
                "timestamp": latest_metrics.timestamp,
            },
            "history_length": len(self.metrics_history),
            "alerts_active": any(
                self.alert_callbacks[alert] for alert in CoherenceAlert
            ),
        }

    def set_thresholds(self, **kwargs):
        """Update coherence thresholds"""
        for key, value in kwargs.items():
            if hasattr(self.thresholds, key):
                setattr(self.thresholds, key, value)
                logger.info(f"Updated threshold {key} = {value}")


def demonstrate_coherence_monitoring():
    """Demonstrate coherence monitoring system"""
    print("AIOS Quantum Field Coherence Monitor Demonstration")
    print("=" * 55)

    # Initialize coherence monitor without field for demo
    monitor = QuantumFieldCoherenceMonitor(
        field_dimension=32, monitoring_interval=0.5, history_length=50
    )

    print("Coherence monitor initialized (no field attached for demo)")
    print("In real usage, attach monitor.quantum_field to a")
    print("QuantumDendriticField instance")

    # Get status
    status = monitor.get_monitoring_status()
    print(f"Monitor status: {status}")

    print("\nCoherence monitoring demonstration complete!")


if __name__ == "__main__":
    demonstrate_coherence_monitoring()
