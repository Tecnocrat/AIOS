"""
AIOS Knowledge Ingestion - Microsoft Provider (Extended Tools)
=============================================================

AINLP.dendritic[ai/ingestion/providers/microsoft]{msft,rss,distillation}

Extended Microsoft tools for feed fetching and distillation.

Components:
- msft_feed_fetcher.py - GitHub Actions workflow fetcher
- msft_distillation_bridge.py - VOID Bridge integration

Usage:
    # For KIP-based provider:
    from ai.ingestion.providers import MicrosoftProvider

    # For extended workflow tools:
    from ai.ingestion.providers.microsoft import msft_feed_fetcher
    from ai.ingestion.providers.microsoft import msft_distillation_bridge
"""

# These are standalone scripts, not modules to import
# Use them directly: python -m ai.ingestion.providers.microsoft.msft_feed_fetcher

__all__ = []
