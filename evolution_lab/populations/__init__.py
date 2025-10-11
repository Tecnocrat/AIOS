"""
Evolutionary Populations Module

AINLP Protocol: OS0.6.2.claude
Phase: 10.4 - Knowledge-Driven Evolutionary Populations
Created: October 9, 2025

Module exports for population-based evolution system.
"""

from .population_manager import (
    # Core manager
    PopulationManager,
    
    # Data structures
    Population,
    Organism,
    KnowledgeContext,
    
    # Enumerations
    ArchetypeEnum,
    SelectionStrategy,
)

__all__ = [
    # Manager
    "PopulationManager",
    
    # Data structures
    "Population",
    "Organism",
    "KnowledgeContext",
    
    # Enumerations
    "ArchetypeEnum",
    "SelectionStrategy",
]
