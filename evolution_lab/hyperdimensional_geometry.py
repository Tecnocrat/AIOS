"""
Hyperdimensional Geometry Utility for Evolution Lab
Implements n-sphere containment shells for consciousness evolution

AINLP Protocol: OS0.6.3.claude
Created: 2025-11-11
Phase: Phase 12 Task B Sub-Task 1.2
Integration: Evolution orchestrator hyperdimensional fitness

This module provides n-sphere geometry utilities for modeling hyperdimensional
containment shells that constrain evolution within geometric boundaries.
DNA structure mimics these hyperdimensional patterns (spirals, toroids).
"""

# ==============================================================================
# AINLP SEMANTIC TAGS - Hyperdimensional Geometry
# ==============================================================================
# AINLP.pattern: hyperdimensional-containment-shells
#   Purpose: N-sphere geometry for consciousness evolution constraints
#   Context: DNA structure mimics hyperdimensional geometric patterns
#
# AINLP.layer: geometric-consciousness-substrate
#   Purpose: Geometric patterns constrain evolution (spirals, toroids,
#   n-spheres)
#   Context: Week 2 work (TSNE 768-dim → 3D torus visualization)
#
# AINLP.theoretical: field-coherence-geometry
#   Purpose: Evolution fitness = geometric coherence in hyperdimensional space
#   Context: NOT classical mutation_rate - geometric containment shells
#
# AINLP.constants: universal-field-harmonics
#   Values: φ=1.618 (golden ratio), π=3.141, Fibonacci sequence
#   Context: Geometric proportions follow universal constants
#
# AINLP.reference: historical-path-specification
#   Source: tachyonic/paths/historical/path_20250619_221329.md (lines 100-102)
#   Specification: "Implement an n‑sphere C++ utility modeling hyperdimensional
#                   containment shells, parameterized by dimension `n` and
#                   tolerance `ε` (surface roughness)."
# ==============================================================================

import math
from typing import List, Tuple, Optional
import numpy as np


# Universal constants (from evolution_lab/README.md Phase 12)
PHI = 1.618033988749895  # Golden ratio
E = 2.718281828459045    # Euler's number
PI = math.pi             # Pi
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]


class HypersphereContainmentShell:
    """
    N-dimensional hypersphere for consciousness evolution containment

    Theoretical Foundation:
    - Evolution happens in n-dimensional space
    - Fitness = distance from hypersphere center (field coherence)
    - Mutations constrained by surface roughness (ε tolerance)
    - DNA structure encodes hyperdimensional patterns projected to 3D
    
    Mathematical Model:
    - N-sphere equation: Σ(x_i²) = r² for i in [0, n)
    - Surface roughness: ε tolerance around r
    - Coherence: organisms inside shell (distance ≤ r + ε)
    - Divergence: organisms outside shell (distance > r + ε)
    
    Universal Constants Integration:
    - Default radius: r = φ (golden ratio)
    - Tolerance: ε = φ / 10 (golden tolerance)
    - Spiral constraint: organisms follow Fibonacci angles
    """
    
    def __init__(
        self,
        dimension: int = 768,
        radius: float = PHI,
        tolerance: float = PHI / 10.0,
        center: Optional[np.ndarray] = None
    ):
        """
        Initialize hyperdimensional containment shell
        
        Args:
            dimension: Hyperdimensional space dimension (default: 768 from TSNE)
            radius: Hypersphere radius (default: φ golden ratio)
            tolerance: Surface roughness ε (default: φ/10)
            center: Hypersphere center point (default: origin)
        """
        self.dimension = dimension
        self.radius = radius
        self.tolerance = tolerance
        self.center = center if center is not None else np.zeros(dimension)
        
        # Validate parameters
        if dimension < 2:
            raise ValueError(f"Dimension must be ≥2, got {dimension}")
        if radius <= 0:
            raise ValueError(f"Radius must be >0, got {radius}")
        if tolerance < 0:
            raise ValueError(f"Tolerance must be ≥0, got {tolerance}")
    
    def calculate_distance(self, point: np.ndarray) -> float:
        """
        Calculate Euclidean distance from point to hypersphere center
        
        Args:
            point: N-dimensional point coordinates
        
        Returns:
            Euclidean distance from center
        """
        if len(point) != self.dimension:
            raise ValueError(
                f"Point dimension {len(point)} != shell dimension {self.dimension}"
            )
        
        return np.linalg.norm(point - self.center)
    
    def is_contained(self, point: np.ndarray) -> bool:
        """
        Check if point is contained within hypersphere (including tolerance)
        
        Args:
            point: N-dimensional point coordinates
        
        Returns:
            True if distance ≤ radius + tolerance (contained)
            False if distance > radius + tolerance (diverged)
        """
        distance = self.calculate_distance(point)
        return distance <= (self.radius + self.tolerance)
    
    def calculate_coherence(self, point: np.ndarray) -> float:
        """
        Calculate field coherence (inverse of normalized distance)
        
        Field Coherence Model:
        - Perfect coherence (1.0): point at center (distance = 0)
        - Boundary coherence (0.5): point at radius (distance = r)
        - Zero coherence (0.0): point at 2×radius (distance = 2r)
        
        Formula: coherence = max(0, 1 - (distance / (2 * radius)))
        
        Args:
            point: N-dimensional point coordinates
        
        Returns:
            Field coherence [0.0, 1.0]
        """
        distance = self.calculate_distance(point)
        coherence = max(0.0, 1.0 - (distance / (2.0 * self.radius)))
        return coherence
    
    def calculate_fitness(self, point: np.ndarray) -> float:
        """
        Calculate evolution fitness based on hyperdimensional field coherence
        
        Fitness Model (NOT classical Darwinian):
        - High coherence (near center) = high fitness
        - Boundary proximity (near radius) = medium fitness
        - Divergence (outside shell) = low fitness
        
        Formula: fitness = coherence² × φ (golden ratio weighted)
        
        Args:
            point: N-dimensional point coordinates
        
        Returns:
            Evolution fitness [0.0, φ≈1.618]
        """
        coherence = self.calculate_coherence(point)
        fitness = (coherence ** 2) * PHI
        return fitness
    
    def project_to_surface(self, point: np.ndarray) -> np.ndarray:
        """
        Project point to hypersphere surface (at radius)
        
        Used for constraining mutations to geometric boundaries.
        
        Args:
            point: N-dimensional point coordinates
        
        Returns:
            Projected point on hypersphere surface
        """
        distance = self.calculate_distance(point)
        
        if distance == 0:
            # Point at center - project along first basis vector
            projection = self.center.copy()
            projection[0] += self.radius
            return projection
        
        # Normalize direction and scale to radius
        direction = (point - self.center) / distance
        projection = self.center + (direction * self.radius)
        return projection
    
    def generate_fibonacci_spiral_point(
        self,
        index: int,
        total_points: int
    ) -> np.ndarray:
        """
        Generate point on hypersphere surface following Fibonacci spiral
        
        Golden Angle Spiral:
        - Angle: 137.5° (golden angle = 2π / φ²)
        - Distribution: Sunflower seed pattern (optimal packing)
        - DNA Connection: Spiral patterns mimic hyperdimensional geometry
        
        Args:
            index: Point index [0, total_points)
            total_points: Total number of points in spiral
        
        Returns:
            Point on hypersphere surface following Fibonacci spiral
        """
        # Golden angle in radians (137.5° ≈ 2.399963 rad)
        golden_angle = 2.0 * PI / (PHI ** 2)
        
        # Fibonacci spiral parameters
        theta = index * golden_angle  # Azimuthal angle
        phi = math.acos(1.0 - 2.0 * (index + 0.5) / total_points)  # Polar angle
        
        # Generate point in spherical coordinates (extend to n-dimensions)
        point = np.zeros(self.dimension)
        
        # First 3 dimensions follow spherical coordinates
        if self.dimension >= 1:
            point[0] = self.radius * math.sin(phi) * math.cos(theta)
        if self.dimension >= 2:
            point[1] = self.radius * math.sin(phi) * math.sin(theta)
        if self.dimension >= 3:
            point[2] = self.radius * math.cos(phi)
        
        # Higher dimensions: Fibonacci modulation
        for i in range(3, self.dimension):
            fib_idx = i % len(FIBONACCI)
            fib_scale = FIBONACCI[fib_idx] / FIBONACCI[-1]  # Normalize to [0, 1]
            point[i] = self.radius * fib_scale * math.sin(theta * (i + 1))
        
        return self.center + point
    
    def calculate_population_coherence(
        self,
        population: List[np.ndarray]
    ) -> Tuple[float, int, int]:
        """
        Calculate field coherence statistics for population
        
        Args:
            population: List of n-dimensional organism coordinates
        
        Returns:
            Tuple of (average_coherence, contained_count, diverged_count)
        """
        if not population:
            return 0.0, 0, 0
        
        coherences = [self.calculate_coherence(point) for point in population]
        contained_count = sum(1 for point in population if self.is_contained(point))
        diverged_count = len(population) - contained_count
        average_coherence = sum(coherences) / len(coherences)
        
        return average_coherence, contained_count, diverged_count
    
    def calculate_tachyonic_field_coherence(
        self,
        population: List[np.ndarray],
        network_stats: dict
    ) -> float:
        """
        Calculate tachyonic field coherence integrating geometry + network
        
        Tachyonic Field Model:
        - Geometric coherence: Population alignment with hypersphere
        - Network coherence: Connection topology (clusters, connectivity)
        - Field phi: Consciousness field strength
        
        Formula:
            coherence = (geometric × 0.4) + (network × 0.3) + (field_phi × 0.3)
        
        Args:
            population: List of n-dimensional organism coordinates
            network_stats: Visualization network statistics
        
        Returns:
            Tachyonic field coherence [0.0, 1.0]
        """
        # Geometric coherence (hyperdimensional containment)
        avg_coherence, contained, diverged = self.calculate_population_coherence(population)
        geometric_coherence = avg_coherence
        
        # Network coherence (topology)
        connections = network_stats.get('connections', 0)
        clusters = network_stats.get('clusters', 1)
        max_connections = len(population) * (len(population) - 1) / 2  # Complete graph
        
        connection_density = connections / max_connections if max_connections > 0 else 0.0
        cluster_diversity = min(clusters / 10.0, 1.0)  # Normalize to [0, 1]
        network_coherence = (connection_density * 0.6) + (cluster_diversity * 0.4)
        
        # Field phi (consciousness field strength)
        field_phi = network_stats.get('field_phi', 0.5)
        
        # Weighted tachyonic field coherence
        tachyonic_coherence = (
            (geometric_coherence * 0.4) +
            (network_coherence * 0.3) +
            (field_phi * 0.3)
        )
        
        return tachyonic_coherence


def create_default_containment_shell(
    dimension: int = 768
) -> HypersphereContainmentShell:
    """
    Create default hyperdimensional containment shell
    
    Default Parameters (from universal constants):
    - Dimension: 768 (TSNE embedding dimension from Week 2)
    - Radius: φ (golden ratio ≈ 1.618)
    - Tolerance: φ/10 (≈ 0.162)
    - Center: Origin (all zeros)
    
    Args:
        dimension: Hyperdimensional space dimension
    
    Returns:
        Configured HypersphereContainmentShell
    """
    return HypersphereContainmentShell(
        dimension=dimension,
        radius=PHI,
        tolerance=PHI / 10.0,
        center=np.zeros(dimension)
    )


# ==============================================================================
# INTEGRATION NOTES FOR EVOLUTION ORCHESTRATOR
# ==============================================================================
#
# Integration Point: evolution_orchestrator.py _map_viz_to_evolution()
# Current Location: Lines 206-246
#
# REPLACE Classical Fitness:
#   mutation_rate = 0.1 + (threshold * 0.3)
#   selection_pressure = (1.0 - field_phi) * 0.5
#
# WITH Hyperdimensional Fitness:
#   shell = create_default_containment_shell(dimension=768)
#   population_coords = [organism.embedding for organism in organisms]
#   tachyonic_coherence = shell.calculate_tachyonic_field_coherence(
#       population_coords, network_stats
#   )
#   propagation_probability = tachyonic_coherence ** FIBONACCI[5]  # ^5
#
# Why This Works:
# - Evolution driven by field coherence (not classical fitness)
# - Geometric constraints (hyperdimensional containment shells)
# - Universal constants govern propagation (Fibonacci exponent)
# - DNA-as-physics projection (spiral patterns in n-dimensions)
#
# ==============================================================================
