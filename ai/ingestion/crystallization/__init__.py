"""
AIOS Knowledge Ingestion - Crystallization (VOID Bridge)
========================================================

AINLP.dendritic[ai/ingestion/crystallization]{void,bridge,multi-agent}

VOID Bridge integration for knowledge crystallization.
Transforms raw knowledge into AIOS-consumable patterns.

Components:
- void_bridge.py - Main VOID Bridge for URL crystallization
- source_library.py - Source pattern library
- multi_agent_pipeline.py - Multi-agent ingestion orchestration
"""

from .void_bridge import VOIDBridge, VOIDVertex

__all__ = [
    "VOIDBridge",
    "VOIDVertex",
]
