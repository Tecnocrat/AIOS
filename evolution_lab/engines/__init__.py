"""
AIOS Evolution Lab - Mutation Engines
AI-powered code mutation for organism evolution

Engines:
- MistralMutationEngine: Local Mistral 7B via Ollama RC1 (FREE)
"""

from .mistral_mutation_engine import (
    MistralMutationEngine,
    MutationResult,
    MutationStats
)

__all__ = [
    'MistralMutationEngine',
    'MutationResult',
    'MutationStats'
]
