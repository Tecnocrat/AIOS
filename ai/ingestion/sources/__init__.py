"""
AIOS Knowledge Ingestion - Source Adapters
==========================================

Generic source adapters for various knowledge source types.

Adapters:
- base.py - BaseSourceAdapter ABC
- rss.py - RSS/Atom feed adapter
- arxiv_adapter.py - arXiv paper adapter
- mslearn_adapter.py - Microsoft Learn adapter
"""

from .base import BaseSourceAdapter, SourceConfig
from .rss import RSSSourceAdapter

# Optional adapters (may have additional dependencies)
try:
    from .arxiv_adapter import ArxivAdapter
except ImportError:
    ArxivAdapter = None

try:
    from .mslearn_adapter import MSLearnAdapter
except ImportError:
    MSLearnAdapter = None

__all__ = [
    "BaseSourceAdapter",
    "SourceConfig",
    "RSSSourceAdapter",
    "ArxivAdapter",
    "MSLearnAdapter",
]
