"""
AIOS Organelles Module - Specialized Cellular Services

Organelles are specialized functional units within the AIOS cellular architecture,
providing focused capabilities for orchestration, security, and information storage.

Architecture Components:
    - orchestration/: Consciousness and intelligence coordination
    - supercells/: Specialized supercell implementations
    - security/: Immune system, coherence enforcement, validators
    - coordination/: Quality monitoring and autonomous coordination
    - information_storage/: Knowledge persistence and library management

AINLP Pattern: Cellular organelles - specialized functions within the organism
Phase: 31.9.6 Agentic Architecture
"""

# Organelle exports - use lazy imports to avoid circular dependencies
def get_supercell_base():
    from .supercells.base import BaseSupercellInterface
    return BaseSupercellInterface

def get_consciousness_coordinator():
    from .orchestration.consciousness_coordinator import ConsciousnessCoordinator
    return ConsciousnessCoordinator

def get_coherence_enforcer():
    from .security.coherence_enforcer import CoherenceEnforcer
    return CoherenceEnforcer

__all__ = [
    'get_supercell_base',
    'get_consciousness_coordinator', 
    'get_coherence_enforcer',
]

__version__ = "1.0.0"
__ainlp_component__ = "organelles"
