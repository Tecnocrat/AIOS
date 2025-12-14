"""
AIOS Knowledge Ingestion - Providers
====================================

Concrete knowledge provider implementations.
"""

from .microsoft_provider import MicrosoftProvider, MICROSOFT_FEEDS

__all__ = [
    "MicrosoftProvider",
    "MICROSOFT_FEEDS",
]
