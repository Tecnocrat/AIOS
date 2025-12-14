"""
VOID Bridge - DEPRECATED LOCATION
=================================

This module has moved to: ai/ingestion/crystallization/void_bridge.py

This redirect exists for backward compatibility.
Please update imports to use the new location.
"""

import warnings
warnings.warn(
    "ai.tools.void_bridge is deprecated. "
    "Use ai.ingestion.crystallization.void_bridge instead.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export everything from new location
from ai.ingestion.crystallization.void_bridge import *
