"""
AIOS Knowledge Ingestion Protocol (KIP)
=======================================

AINLP.dendritic[ai/ingestion]{knowledge,learning,sources,crystallization}

Unified framework for ingesting external knowledge into AIOS:
- Standardized KnowledgeItem schema across all sources
- Plugin-based source adapters (RSS, docs, repos, papers)
- Cross-source deduplication
- Automated scheduling and archival

Architecture:
------------
ai/ingestion/
├── protocol.py        # Core abstractions (KnowledgeItem, KnowledgeSource)
├── registry.py        # Source registration and discovery
├── scheduler.py       # Cron/trigger coordination
├── deduplication.py   # Hash-based cross-source dedup
│
├── sources/           # Generic source adapters
│   ├── base.py        # BaseSourceAdapter ABC
│   ├── rss.py         # RSS/Atom feed adapter
│   ├── docs.py        # Documentation site scraper
│   └── repo.py        # Git repository cloning
│
└── providers/         # Concrete implementations
    ├── microsoft/     # MSFT ecosystem
    ├── python/        # Python docs, PyPI
    ├── cpp/           # C++ STL
    └── arxiv/         # Research papers

Output:
-------
docs/distilled/
├── MASTER_INDEX.md    # All sources unified
├── microsoft/
├── python/
└── arxiv/

Usage:
------
from ai.ingestion import KnowledgeItem, SourceRegistry

# Register a provider
registry = SourceRegistry()
registry.register("microsoft", MicrosoftProvider())

# Fetch knowledge
items = await registry.fetch_all()

# Query
recent = registry.query(since="2025-12-01", provider="microsoft")
"""

__version__ = "1.0.0"
__author__ = "AIOS"

from .protocol import KnowledgeItem, KnowledgeSource, IngestionResult
from .registry import SourceRegistry
from .deduplication import DeduplicationEngine, get_dedup_engine
from .output import OutputGenerator

__all__ = [
    "KnowledgeItem",
    "KnowledgeSource",
    "IngestionResult",
    "SourceRegistry",
    "DeduplicationEngine",
    "get_dedup_engine",
    "OutputGenerator",
]
