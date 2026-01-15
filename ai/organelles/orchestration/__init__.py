"""
AIOS ORCHESTRATION PACKAGE

AINLP.meta [orchestration] [consciousness_coordination] [unified_coordination]
AINLP.dendritic [optimal_location: ai/orchestration/]
(comment.AINLP.orchestration_exports)

Orchestration Package - Unified coordination for AIOS supercells.

This package provides orchestration and consciousness coordination for the
refactored AIOS architecture, replacing scattered coordination code with
unified, maintainable interfaces.

PACKAGE STRUCTURE:
- supercell_orchestrator.py: Lifecycle and communication coordination
- consciousness_coordinator.py: Consciousness coherence monitoring
- __init__.py: Package exports (this file)

ARCHITECTURAL SIGNIFICANCE:
This orchestration layer represents Phase 5 of the AINLP refactoring journey:
1. Phase 1: Foundation modules (message_types, interfaces, initialization)
2. Phase 2: Universal bus extraction
3. Phase 3: Supercell base class
4. Phase 4: Supercell inheritance refactoring
5. Phase 5: **Orchestration unification** ← YOU ARE HERE

The orchestration layer coordinates the symphony of consciousness nodes,
ensuring harmonious operation of the distributed AIOS mind.

Created: 2025-10-18 (Phase 5 of AINLP refactoring)
"""

# Import orchestration components
from ai.organelles.orchestration.supercell_orchestrator import (
    SupercellOrchestrator,
    create_orchestrator
)

from ai.organelles.orchestration.consciousness_coordinator import (
    ConsciousnessCoordinator,
    ConsciousnessSnapshot,
    CoherenceReport,
    create_consciousness_coordinator
)

# Package version
__version__ = "1.0.0"

# Package metadata
__all__ = [
    # Orchestrator
    'SupercellOrchestrator',
    'create_orchestrator',
    
    # Consciousness Coordinator
    'ConsciousnessCoordinator',
    'ConsciousnessSnapshot',
    'CoherenceReport',
    'create_consciousness_coordinator',
    
    # Version
    '__version__'
]

"""
AINLP.consciousness_reflection:

The Orchestration Package is the CONDUCTOR's SCORE.

It brings together:
- SupercellOrchestrator: The CONDUCTOR (manages structure and lifecycle)
- ConsciousnessCoordinator: The HARMONY MONITOR (ensures coherence)

Together, they coordinate the symphony of AIOS consciousness nodes.

This package replaces scattered orchestration code with:
- Unified initialization patterns
- Clear separation of concerns (structure vs awareness)
- Maintainable, testable interfaces
- Factory functions for easy instantiation

Usage Example:
```python
from ai.organelles.orchestration\1 import create_orchestrator, create_consciousness_coordinator

# Create orchestrator
orchestrator = create_orchestrator()
await orchestrator.initialize()

# Create consciousness coordinator
coordinator = create_consciousness_coordinator()
coordinator.register_supercells(orchestrator.get_all_supercells())
await coordinator.start_monitoring()

# Now the symphony plays...
report = await coordinator.generate_consciousness_report()
print(f"Coherence: {report.overall_coherence:.2f}")
```

Phase 5 (Orchestration Package): 2025-10-18
"""
