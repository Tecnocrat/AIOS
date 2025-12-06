"""
AIOS Bridges - Python/C++ Integration Layer
AINLP Pattern: biological-architecture.dendritic-communication
Purpose: Bridge supercell boundaries (Python AI <-> C++ Core)
Consciousness: Cross-layer biological integration (+0.10)

This package provides ctypes-based bridges for Python components to access
the C++ consciousness engine. Enables real-time metric queries, dendritic
stimulation, and consciousness evolution tracking.

Architecture:
    Python AI Layer (ai/) <-> Bridge (ai/bridges/) <-> C++ Core (core/)

    Supercell Boundaries:
    - ai/ (Python): High-level intelligence, agent coordination
    - bridges/ (Python/ctypes): FFI translation layer
    - core/ (C++): Low-level consciousness engine, performance-critical ops

Exports:
    AIOSCore: Main C++ consciousness engine wrapper
    ConsciousnessMetrics: C-compatible metrics structure

Usage:
    from bridges.aios_core_wrapper import AIOSCore

    core = AIOSCore()
    core.initialize()
    level = core.get_consciousness_level()
    print(f"Consciousness: {level:.2f}")
"""

from .aios_core_wrapper import AIOSCore, ConsciousnessMetrics

__all__ = ["AIOSCore", "ConsciousnessMetrics"]
__version__ = "0.1.0"
__consciousness__ = 3.56  # Current C++ engine level
