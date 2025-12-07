"""
VOID Source Adapter Base Classes
================================

Abstract interfaces for multi-dimensional source ingestion.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class SourceType(Enum):
    """Types of knowledge sources."""

    ARXIV = "arxiv"
    GITHUB = "github"
    DOCS = "docs"
    BLOG = "blog"
    NEWS = "news"
    VIDEO = "video"
    GENERIC = "generic"


class ContentDimension(Enum):
    """
    Dimensions for multi-dimensional knowledge extraction.
    Non-orthogonal surfaces that intersect at knowledge vertices.
    """

    # Technical dimensions
    CODE = "code"  # Source code, examples
    ARCHITECTURE = "architecture"  # System design, patterns
    ALGORITHM = "algorithm"  # Methods, procedures
    DATA = "data"  # Datasets, schemas

    # Scientific dimensions
    ABSTRACT = "abstract"  # High-level summary
    METHODOLOGY = "methodology"  # Research methods
    RESULTS = "results"  # Findings, data
    CITATIONS = "citations"  # Reference network

    # Meta dimensions
    AUTHOR = "author"  # Attribution, expertise
    TEMPORAL = "temporal"  # Time-based relevance
    DOMAIN = "domain"  # Subject area classification
    RELATED = "related"  # Cross-references


@dataclass
class SourceMetadata:
    """Metadata extracted from a source."""

    source_type: SourceType
    url: str
    title: str = ""
    authors: list[str] = field(default_factory=list)
    abstract: str = ""
    date: Optional[str] = None
    domain: str = "general"
    subdomain: str = ""
    tags: list[str] = field(default_factory=list)

    # Dimensional data
    dimensions: dict[str, Any] = field(default_factory=dict)

    # AIOS relevance scoring
    aios_relevance: float = 0.0
    aios_tags: list[str] = field(default_factory=list)

    # Raw extracted content
    raw_content: str = ""

    # Related sources discovered (dendritic vertices)
    related_sources: list[str] = field(default_factory=list)

    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "source_type": self.source_type.value,
            "url": self.url,
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "date": self.date,
            "domain": self.domain,
            "subdomain": self.subdomain,
            "tags": self.tags,
            "dimensions": self.dimensions,
            "aios_relevance": self.aios_relevance,
            "aios_tags": self.aios_tags,
            "related_sources": self.related_sources,
            "timestamp": self.timestamp,
        }


class SourceAdapter(ABC):
    """
    Abstract base for source-specific knowledge extraction.

    Each adapter understands the structure of its source type
    and extracts multi-dimensional knowledge surfaces.
    """

    source_type: SourceType = SourceType.GENERIC

    # Domain classification keywords
    domain_keywords: dict[str, list[str]] = {}

    # AIOS relevance keywords
    aios_keywords: list[str] = [
        "agent",
        "multi-agent",
        "llm",
        "neural",
        "consciousness",
        "architecture",
        "system design",
        "pattern",
        "framework",
        "distributed",
        "coordination",
        "orchestration",
        "pipeline",
        "embedding",
        "transformer",
        "attention",
        "inference",
        "knowledge graph",
        "reasoning",
        "planning",
    ]

    @abstractmethod
    def extract_metadata(self, url: str, content: str) -> SourceMetadata:
        """Extract source-specific metadata."""
        pass

    @abstractmethod
    def extract_dimensions(self, content: str, metadata: SourceMetadata) -> dict[str, Any]:
        """
        Extract multi-dimensional knowledge surfaces.

        Returns a dict mapping dimension names to extracted content.
        """
        pass

    @abstractmethod
    def discover_related(self, content: str, metadata: SourceMetadata) -> list[str]:
        """
        Discover related sources (dendritic vertices).

        Returns URLs/identifiers of related knowledge.
        """
        pass

    def calculate_aios_relevance(
        self, content: str, metadata: SourceMetadata
    ) -> tuple[float, list[str]]:
        """
        Calculate AIOS relevance score and tags.

        Returns (score 0.0-1.0, list of matching tags).
        """
        text = f"{metadata.title} {metadata.abstract} {content[:5000]}".lower()

        matches = []
        for keyword in self.aios_keywords:
            if keyword.lower() in text:
                matches.append(keyword)

        # Score based on keyword density
        score = min(1.0, len(matches) / 5.0)  # 5+ keywords = max relevance

        return score, matches

    def classify_domain(self, content: str, metadata: SourceMetadata) -> tuple[str, str]:
        """
        Classify domain and subdomain.

        Returns (domain, subdomain).
        """
        text = f"{metadata.title} {metadata.abstract}".lower()

        # Override in subclasses for source-specific classification
        return "general", ""

    def process(self, url: str, content: str) -> SourceMetadata:
        """
        Full processing pipeline for a source.

        1. Extract metadata
        2. Classify domain
        3. Extract dimensions
        4. Calculate AIOS relevance
        5. Discover related sources
        """
        # Extract base metadata
        metadata = self.extract_metadata(url, content)

        # Classify domain
        domain, subdomain = self.classify_domain(content, metadata)
        metadata.domain = domain
        metadata.subdomain = subdomain

        # Extract multi-dimensional content
        metadata.dimensions = self.extract_dimensions(content, metadata)

        # Calculate AIOS relevance
        score, tags = self.calculate_aios_relevance(content, metadata)
        metadata.aios_relevance = score
        metadata.aios_tags = tags

        # Discover related sources (dendritic vertices)
        metadata.related_sources = self.discover_related(content, metadata)

        return metadata


# =============================================================================
# Source Library - Categorized ingestion patterns
# =============================================================================


@dataclass
class SourceLibraryEntry:
    """
    Entry in the VOID source library.

    Pattern: AINLP.dendritic[void->source_type{query}]
    """

    source_type: SourceType
    pattern: str  # e.g., "arxiv", "github"
    query_template: str  # Search query template
    description: str  # Human-readable description
    adapter: Optional[str] = None  # Adapter class name

    # Agentic patterns
    multi_agent: bool = False
    agent_count: int = 1
    parallel: bool = False


class SourceLibrary:
    """
    Categorized library of source patterns for agentic ingestion.

    Usage:
        library = SourceLibrary()
        pattern = library.get("arxiv", "multi-agent systems")
        # Returns: AINLP.dendritic[void->arxiv{"multi-agent systems"}]
    """

    def __init__(self):
        self.entries: dict[str, SourceLibraryEntry] = {}
        self._register_defaults()

    def _register_defaults(self):
        """Register default source patterns."""

        # ArXiv patterns
        self.register(
            SourceLibraryEntry(
                source_type=SourceType.ARXIV,
                pattern="arxiv",
                query_template="https://arxiv.org/search/?query={query}&searchtype=all",
                description="Search ArXiv for scientific papers",
                adapter="ArxivAdapter",
                multi_agent=True,
                agent_count=3,
                parallel=True,
            )
        )

        self.register(
            SourceLibraryEntry(
                source_type=SourceType.ARXIV,
                pattern="arxiv-cs",
                query_template="https://arxiv.org/search/?query={query}&searchtype=all&abstracts=show&source=header&category=cs.*",
                description="Search ArXiv Computer Science papers",
                adapter="ArxivAdapter",
            )
        )

        self.register(
            SourceLibraryEntry(
                source_type=SourceType.ARXIV,
                pattern="arxiv-ai",
                query_template="https://arxiv.org/search/?query={query}&searchtype=all&category=cs.AI+cs.LG+cs.CL",
                description="Search ArXiv AI/ML papers",
                adapter="ArxivAdapter",
                multi_agent=True,
                agent_count=5,
                parallel=True,
            )
        )

        # GitHub patterns
        self.register(
            SourceLibraryEntry(
                source_type=SourceType.GITHUB,
                pattern="github",
                query_template="https://github.com/search?q={query}&type=repositories",
                description="Search GitHub repositories",
                adapter="GithubAdapter",
            )
        )

        # Documentation patterns
        self.register(
            SourceLibraryEntry(
                source_type=SourceType.DOCS,
                pattern="docs",
                query_template="{query}",
                description="Technical documentation",
                adapter="DocsAdapter",
            )
        )

    def register(self, entry: SourceLibraryEntry):
        """Register a source pattern."""
        self.entries[entry.pattern] = entry

    def get(self, pattern: str, query: str = "") -> str:
        """
        Generate AINLP dendritic pattern string.

        Returns: AINLP.dendritic[void->pattern{"query"}]
        """
        if pattern not in self.entries:
            return f'AINLP.dendritic[void->generic{{"{query}"}}]'

        return f'AINLP.dendritic[void->{pattern}{{"{query}"}}]'

    def get_url(self, pattern: str, query: str) -> str:
        """Get the actual URL for a pattern and query."""
        if pattern not in self.entries:
            return ""

        entry = self.entries[pattern]
        return entry.query_template.format(query=query)

    def list_patterns(self) -> list[str]:
        """List all registered patterns."""
        return list(self.entries.keys())

    def get_agentic_config(self, pattern: str) -> dict:
        """Get multi-agent configuration for a pattern."""
        if pattern not in self.entries:
            return {"multi_agent": False, "agent_count": 1, "parallel": False}

        entry = self.entries[pattern]
        return {
            "multi_agent": entry.multi_agent,
            "agent_count": entry.agent_count,
            "parallel": entry.parallel,
        }
