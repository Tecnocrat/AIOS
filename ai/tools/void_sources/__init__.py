"""
AIOS VOID Source Adapters
=========================

Multi-dimensional knowledge ingestion from diverse source types.

AINLP.dendritic[VOID->source{type}]

Each adapter handles domain-specific extraction patterns:
- arxiv: Scientific papers (physics, CS, math, biology)
- github: Code repositories and documentation
- docs: Technical documentation sites
- blog: Technical blog posts
- news: News articles
- video: Transcripts/summaries

Source Library Pattern:
    AINLP.dendritic[void->arxiv{"Search for AIOS related papers"}]
    → Multi-agent ingestion pipeline
    → Dendritic vertex discovery at focused location

Usage:
    from void_sources import SourceLibrary, ArxivAdapter, ainlp_pattern

    # Generate AINLP pattern
    pattern = ainlp_pattern("multi-agent coordination", "arxiv-ai")

    # Detect source type
    library = SourceLibrary()
    source = library.detect("https://arxiv.org/abs/2303.08774")

    # Multi-agent ingestion
    from void_sources.multi_agent_pipeline import void_multi_agent_ingest
    result = void_multi_agent_ingest(
        "https://arxiv.org/abs/2303.08774",
        topic="GPT-4 architecture"
    )
"""

from .base import (
    ContentDimension,
    SourceAdapter,
    SourceMetadata,
    SourceType,
)
from .arxiv_adapter import ArxivAdapter, process_arxiv_url
from .source_library import (
    SourceCategory,
    SourceLibrary,
    SourcePattern,
    ainlp_pattern,
    detect_source,
    get_library,
)

__all__ = [
    # Base classes
    "SourceAdapter",
    "SourceMetadata",
    "SourceType",
    "ContentDimension",
    # ArXiv adapter
    "ArxivAdapter",
    "process_arxiv_url",
    # Source library
    "SourceCategory",
    "SourceLibrary",
    "SourcePattern",
    "ainlp_pattern",
    "detect_source",
    "get_library",
]
