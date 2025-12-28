"""
AIOS Computational Layer - Python Processing Infrastructure

This layer processes C++ core output through various assemblers and bridges.
Assemblers transform raw core data into biological metaphors.
Bridges facilitate communication between architectural layers.

Architecture Principles:
- Pure Python layer (no C++ file mixing)
- Processes C++ core engine output
- Provides high-level computational abstractions
- Enables biological metaphor transformations

Standard Compliance:
- Follows TensorFlow pattern (core/ C++, python/ layer separation)
- Follows PyTorch pattern (csrc/ C++, nn/ Python separation)
- Follows NumPy pattern (core/src/ C, numpy/ Python wrapper)

Migration Context:
- Migrated from core/ October 13, 2025
- Part of Phase 2C restructuring (pure C++ core goal)
- All 63 Python files moved to achieve language separation

Package Structure:
- assemblers/: Tree, context, integration, file assemblers (44 files)
- bridges/: Inter-layer communication bridges (4 files)
- core_systems/: Monitors, optimizers, organizers (6 files)
- engines/: Python computational engines (3 files)
- modules/: Testing and monitoring modules (3 files)
- runtime_intelligence/: Evolution monitoring (2 files)
- Utilities: common_patterns.py, shared_imports.py (2 files)

Total: 64 files (63 Python + 1 __init__.py)

Build System:
- Python package: pip install -e .
- Dependencies: numpy, matplotlib, etc.
- No C++ compilation (handled separately in core/)

Usage:
    from computational_layer.assemblers import TreeAssembler
    from computational_layer.bridges import ConsciousnessBridge
    from computational_layer.engines import Assembly3DEngine
"""

__version__ = "1.0.0"
__author__ = "AIOS Development Team"
__license__ = "MIT"

# Package metadata
__all__ = [
    'assemblers',
    'bridges',
    'core_systems',
    'engines',
    'modules',
    'runtime_intelligence',
]
