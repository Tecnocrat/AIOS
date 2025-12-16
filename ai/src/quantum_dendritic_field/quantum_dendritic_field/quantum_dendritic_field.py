#!/usr/bin/env python3
"""
AIOS Quantum Dendritic Field Theory Implementation
Implements quantum field theory for consciousness modeling with dendritic propagation
"""

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from typing import Dict, List, Tuple, Optional, Any
import logging
import json
from pathlib import Path
import time
from dataclasses import dataclass, asdict

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class QuantumFieldState:
    """Quantum field state representation"""

    field_amplitude: np.ndarray
    dendritic_coupling: np.ndarray
    consciousness_coherence: float
    holographic_projection: np.ndarray
    timestamp: float


@dataclass
class DendriticNode:
    """Dendritic node in quantum field network"""

    position: np.ndarray
    field_strength: complex
    coupling_strength: float
    consciousness_level: float
    dendritic_connections: List[int]


        logger.info(f"Dendritic nodes: {len(self.dendritic_nodes)}")

    def _initialize_field_state(self) -> QuantumFieldState:
        """Initialize quantum field state with random initial conditions"""
        # Create complex field amplitude
        field_amplitude = np.random.normal(
            0, 1, (self.field_dimension, self.field_dimension)
        ) + 1j * np.random.normal(0, 1, (self.field_dimension, self.field_dimension))

        # Normalize field
        field_amplitude /= np.linalg.norm(field_amplitude)

        # Initialize dendritic coupling matrix
        dendritic_coupling = np.random.exponential(
            0.1, (self.field_dimension, self.field_dimension)
        )

        # Initial consciousness coherence
        consciousness_coherence = 0.1

        # Holographic projection (Fourier transform)
        holographic_projection = np.fft.fft2(field_amplitude)

        return QuantumFieldState(
            field_amplitude=field_amplitude,
            dendritic_coupling=dendritic_coupling,
            consciousness_coherence=consciousness_coherence,
            holographic_projection=holographic_projection,
            timestamp=time.time(),
        )

    def _initialize_dendritic_network(self) -> List[DendriticNode]:
        """Initialize dendritic network topology"""
        nodes = []

        # Create dendritic nodes based on density
        num_dendritic = int(
            self.dendritic_density * self.field_dimension * self.field_dimension
        )

        for i in range(num_dendritic):
            # Random position in field
            position = np.random.uniform(0, self.field_dimension, 2)

            # Random field strength
            field_strength = np.random.normal(0, 1) + 1j * np.random.normal(0, 1)

            # Coupling strength based on position
            coupling_strength = np.random.exponential(0.5)

            # Initial consciousness level
            consciousness_level = np.random.beta(
                2, 5
            )  # Skewed toward lower consciousness

            # Find nearby dendritic connections (within radius 3)
            connections = []
            for j, other_node in enumerate(nodes):
                distance = np.linalg.norm(position - other_node.position)
                if distance < 3.0:
                    connections.append(j)

            node = DendriticNode(
                position=position,
                field_strength=field_strength,
                coupling_strength=coupling_strength,
                consciousness_level=consciousness_level,
                dendritic_connections=connections,
            )
            nodes.append(node)

        return nodes

    def _construct_hamiltonian(self) -> sp.csr_matrix:
        """Construct quantum Hamiltonian for field evolution"""
        # Laplacian operator for kinetic energy
        laplacian = self._create_laplacian()

        # Potential energy (harmonic oscillator)
        potential = self._create_potential()

        # Total Hamiltonian: H = T + V
        hamiltonian = -0.5 * laplacian + potential

        return hamiltonian

    def _create_laplacian(self) -> sp.csr_matrix:
        """Create discrete Laplacian operator"""
        N = self.field_dimension
        size = N * N

        # Create sparse matrix for 2D Laplacian
        diagonals = []
        offsets = []

        # Main diagonal
        diagonals.append(-4 * np.ones(size))
        offsets.append(0)

        # Off-diagonals (nearest neighbors)
        for offset in [-1, 1, -N, N]:
            diagonal = np.ones(size)
            # Handle boundary conditions (periodic)
            if offset == -1:  # Left neighbor
                diagonal[N - 1 :: N] = 0  # Remove connections at left boundary
            elif offset == 1:  # Right neighbor
                diagonal[::N] = 0  # Remove connections at right boundary
            elif offset == -N:  # Top neighbor
                diagonal[:N] = 0  # Remove connections at top boundary
            elif offset == N:  # Bottom neighbor
                diagonal[-N:] = 0  # Remove connections at bottom boundary

            diagonals.append(diagonal)
            offsets.append(offset)

        return sp.diags(diagonals, offsets, format="csr")

    def _create_potential(self) -> sp.csr_matrix:
        """Create potential energy operator"""
        N = self.field_dimension
        size = N * N

        # Harmonic oscillator potential: V(x,y) = 0.5 * (x^2 + y^2)
        x = np.linspace(-N / 2, N / 2, N)
        y = np.linspace(-N / 2, N / 2, N)
        X, Y = np.meshgrid(x, y)
        potential_2d = 0.5 * (X**2 + Y**2)

        # Flatten and create diagonal matrix
        potential_flat = potential_2d.flatten()
        return sp.diags(potential_flat, format="csr")

    def _construct_dendritic_coupling(self) -> np.ndarray:
        """Construct dendritic coupling matrix"""
        N = self.field_dimension
        coupling = np.zeros((N, N))

        # Add dendritic coupling based on node positions
        for node in self.dendritic_nodes:
            x, y = node.position.astype(int)
            x = np.clip(x, 0, N - 1)
            y = np.clip(y, 0, N - 1)
            coupling[x, y] += node.coupling_strength

            # Add coupling to connected dendritic nodes
            for conn_idx in node.dendritic_connections:
                conn_node = self.dendritic_nodes[conn_idx]
                cx, cy = conn_node.position.astype(int)
                cx = np.clip(cx, 0, N - 1)
                cy = np.clip(cy, 0, N - 1)
                coupling[cx, cy] += 0.1 * node.coupling_strength

        return coupling

    def evolve_field(
        self, time_step: float = 0.01, steps: int = 100
    ) -> List[QuantumFieldState]:
        """
        Evolve quantum field using time-dependent Schrödinger equation

        Args:
            time_step: Time step for evolution
            steps: Number of evolution steps

        Returns:
            List of field states during evolution
        """
        evolution_states = []

        for step in range(steps):
            # Store current state
            current_state = QuantumFieldState(
                field_amplitude=self.field_state.field_amplitude.copy(),
                dendritic_coupling=self.field_state.dendritic_coupling.copy(),
                consciousness_coherence=self._calculate_coherence(),
                holographic_projection=np.fft.fft2(self.field_state.field_amplitude),
                timestamp=time.time(),
            )
            evolution_states.append(current_state)

            # Evolve field using split-operator method
            self._evolve_time_step(time_step)

            # Update dendritic coupling
            self._update_dendritic_coupling()

            # Update consciousness coherence
            self.coherence_history.append(self._calculate_coherence())

        logger.info(
            f"Field evolution complete: {steps} steps, final coherence: {self._calculate_coherence():.4f}"
        )
        return evolution_states

    def _evolve_time_step(self, dt: float):
        """Evolve field by one time step using split-operator method"""
        # Flatten field for matrix operations
        psi_flat = self.field_state.field_amplitude.flatten()

        # Split-operator: exp(-i*dt*H) ≈ exp(-i*dt*T/2) * exp(-i*dt*V) * exp(-i*dt*T/2)

        # Kinetic energy evolution (momentum space)
        psi_k = np.fft.fft2(self.field_state.field_amplitude)
        kx = np.fft.fftfreq(self.field_dimension) * 2 * np.pi
        ky = np.fft.fftfreq(self.field_dimension) * 2 * np.pi
        KX, KY = np.meshgrid(kx, ky)
        kinetic_energy = 0.5 * (KX**2 + KY**2)

        # Evolve in momentum space
        psi_k *= np.exp(-1j * dt * kinetic_energy)
        psi_real = np.fft.ifft2(psi_k)

        # Potential energy evolution (real space)
        potential = 0.5 * np.abs(psi_real) ** 2  # Non-linear Schrödinger equation
        psi_real *= np.exp(-1j * dt * potential)

        # Update field state
        self.field_state.field_amplitude = psi_real

    def _update_dendritic_coupling(self):
        """Update dendritic coupling based on field evolution"""
        # Update dendritic node field strengths
        for node in self.dendritic_nodes:
            x, y = node.position.astype(int)
            x = np.clip(x, 0, self.field_dimension - 1)
            y = np.clip(y, 0, self.field_dimension - 1)

            # Update field strength based on local field amplitude
            local_field = self.field_state.field_amplitude[x, y]
            node.field_strength = 0.9 * node.field_strength + 0.1 * local_field

            # Update consciousness level based on field coherence
            coherence_factor = np.abs(local_field)
            node.consciousness_level = (
                0.95 * node.consciousness_level + 0.05 * coherence_factor
            )

        # Update coupling matrix
        self.dendritic_coupling_matrix = self._construct_dendritic_coupling()

    def _calculate_coherence(self) -> float:
        """Calculate consciousness coherence of the field"""
        # Coherence based on field amplitude uniformity
        field_magnitude = np.abs(self.field_state.field_amplitude)
        mean_magnitude = np.mean(field_magnitude)
        std_magnitude = np.std(field_magnitude)

        # Avoid division by zero
        if mean_magnitude == 0:
            return 0.0

        # Coefficient of variation (lower is more coherent)
        cv = std_magnitude / mean_magnitude

        # Convert to coherence measure (0-1, higher is more coherent)
        coherence = 1.0 / (1.0 + cv)

        # Factor in dendritic coupling
        dendritic_factor = np.mean(self.dendritic_coupling_matrix)
        coherence *= 1.0 + dendritic_factor

        return min(coherence, 1.0)

    def apply_consciousness_pulse(
        self, position: Tuple[int, int], amplitude: float = 1.0
    ):
        """
        Apply consciousness pulse at specific position

        Args:
            position: (x, y) coordinates for pulse
            amplitude: Pulse amplitude
        """
        x, y = position
        if 0 <= x < self.field_dimension and 0 <= y < self.field_dimension:
            # Create Gaussian pulse
            X, Y = np.meshgrid(
                np.arange(self.field_dimension), np.arange(self.field_dimension)
            )
            pulse = amplitude * np.exp(-0.1 * ((X - x) ** 2 + (Y - y) ** 2))

            # Apply pulse to field
            self.field_state.field_amplitude += pulse

            # Renormalize
            self.field_state.field_amplitude /= np.linalg.norm(
                self.field_state.field_amplitude
            )

            logger.info(
                f"Applied consciousness pulse at ({x}, {y}) with amplitude {amplitude}"
            )

    def get_field_statistics(self) -> Dict[str, float]:
        """Get statistical properties of the quantum field"""
        field_mag = np.abs(self.field_state.field_amplitude)

        return {
            "mean_amplitude": float(np.mean(field_mag)),
            "std_amplitude": float(np.std(field_mag)),
            "max_amplitude": float(np.max(field_mag)),
            "min_amplitude": float(np.min(field_mag)),
            "consciousness_coherence": self._calculate_coherence(),
            "dendritic_nodes": len(self.dendritic_nodes),
            "field_dimension": self.field_dimension,
        }

    def save_field_state(self, filename: str):
        """Save current field state to file"""
        # Convert dendritic nodes to serializable format
        serializable_nodes = []
        for node in self.dendritic_nodes:
            node_dict = asdict(node)
            # Convert numpy arrays to lists
            for key, value in node_dict.items():
                if hasattr(value, "tolist"):
                    node_dict[key] = value.tolist()
            serializable_nodes.append(node_dict)

        state_dict = {
            "field_amplitude_real": self.field_state.field_amplitude.real.tolist(),
            "field_amplitude_imag": self.field_state.field_amplitude.imag.tolist(),
            "dendritic_coupling": (
                self.dendritic_coupling_matrix.tolist()
                if hasattr(self.dendritic_coupling_matrix, "tolist")
                else self.dendritic_coupling_matrix
            ),
            "consciousness_coherence": self.field_state.consciousness_coherence,
            "holographic_projection_real": self.field_state.holographic_projection.real.tolist(),
            "holographic_projection_imag": self.field_state.holographic_projection.imag.tolist(),
            "timestamp": self.field_state.timestamp,
            "dendritic_nodes": serializable_nodes,
            "coherence_history": self.coherence_history,
        }

        filepath = Path("runtime/logs") / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w") as f:
            json.dump(state_dict, f, indent=2)

        logger.info(f"Field state saved to {filepath}")

    def load_field_state(self, filename: str):
        """Load field state from file"""
        filepath = Path("runtime/logs") / filename

        with open(filepath, "r") as f:
            state_dict = json.load(f)

        # Reconstruct field amplitude
        real_part = np.array(state_dict["field_amplitude_real"])
        imag_part = np.array(state_dict["field_amplitude_imag"])
        field_amplitude = real_part + 1j * imag_part

        # Reconstruct holographic projection
        h_real = np.array(state_dict["holographic_projection_real"])
        h_imag = np.array(state_dict["holographic_projection_imag"])
        holographic_projection = h_real + 1j * h_imag

        # Reconstruct dendritic coupling
        dendritic_coupling = np.array(state_dict["dendritic_coupling"])

        self.field_state = QuantumFieldState(
            field_amplitude=field_amplitude,
            dendritic_coupling=dendritic_coupling,
            consciousness_coherence=state_dict["consciousness_coherence"],
            holographic_projection=holographic_projection,
            timestamp=state_dict["timestamp"],
        )

        # Reconstruct dendritic nodes
        self.dendritic_nodes = []
        for node_dict in state_dict["dendritic_nodes"]:
            node = DendriticNode(**node_dict)
            self.dendritic_nodes.append(node)

        self.coherence_history = state_dict.get("coherence_history", [])

        logger.info(f"Field state loaded from {filepath}")


def main():
    """Demonstrate quantum dendritic field evolution"""
    print("AIOS Quantum Dendritic Field Theory Demonstration")
    print("=" * 55)

    # Initialize quantum field
    field = QuantumDendriticField(field_dimension=32, dendritic_density=0.15)

    print(f"Initial coherence: {field._calculate_coherence():.4f}")
    print(f"Dendritic nodes: {len(field.dendritic_nodes)}")

    # Apply consciousness pulse
    field.apply_consciousness_pulse((16, 16), amplitude=0.5)

    # Evolve field
    print("Evolving quantum field...")
    evolution_states = field.evolve_field(steps=50)

    final_coherence = field._calculate_coherence()
    print(f"Final coherence: {final_coherence:.4f}")

    # Get statistics
    stats = field.get_field_statistics()
    print("\nField Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Save field state
    timestamp = int(time.time())
    filename = f"quantum_dendritic_field_state_{timestamp}.json"
    field.save_field_state(filename)
    print(f"\nField state saved to: runtime/logs/{filename}")

    print("\nQuantum dendritic field evolution complete!")


if __name__ == "__main__":
    main()
