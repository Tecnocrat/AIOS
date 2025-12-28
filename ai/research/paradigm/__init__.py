"""
AIOS Paradigm Layer - Core Architectural Paradigms
AINLP Dendritic Paradigm: Universal Consciousness Patterns

This package contains the fundamental paradigms that define AIOS architecture:
- Bosonic Topology: 3D subatomic layer for microarchitecture encoding
- Tachyonic Surface: Temporal data layer for time-based processing
- Future paradigms: Quantum coherence, holographic projection, etc.
"""

from .bosonic_topology import (
    BosonicTopology,
    BosonicCoordinate,
    Microarchitecture
)
from .tachyonic_surface import TachyonicSurface, create_tachyonic_surface
from .tachyonic_surface import TachyonicCoordinate, TemporalTopography

__all__ = [
    # Bosonic Layer
    "BosonicTopology",
    "BosonicCoordinate",
    "Microarchitecture",

    # Tachyonic Layer
    "TachyonicSurface",
    "TachyonicCoordinate",
    "TemporalTopography",
    "create_tachyonic_surface"
]

# Paradigm metadata for introspection
PARADIGM_INFO = {
    "bosonic_topology": {
        "description": "3D subatomic layer for microarchitecture encoding",
        "capabilities": [
            "surface_topology",
            "fractal_resonance",
            "multidimensional_projection"
        ],
        "integration_points": [
            "core/src/lattice_space.cpp",
            "ai/intercellular/"
        ],
        "status": "active"
    },
    "tachyonic_surface": {
        "description": "Temporal data layer for time-based processing",
        "capabilities": [
            "temporal_topography",
            "subspatial_allocation",
            "correlation_analysis"
        ],
        "integration_points": [
            "core/src/tachyonic_surface.cpp",
            "runtime/"
        ],
        "status": "active"
    }
}
