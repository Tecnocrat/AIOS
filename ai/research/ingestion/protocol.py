"""
AIOS Knowledge Ingestion Protocol - Core Abstractions
=====================================================

AINLP.dendritic[ai/ingestion/protocol]{schema,knowledge,item,source}

Defines the universal KnowledgeItem schema and KnowledgeSource interface
that all ingestion providers must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional
import hashlib
import json


class SourceType(Enum):
    """Types of knowledge sources."""
    RSS = "rss"
    DOCS = "docs"
    REPO = "repo"
    PAPER = "paper"
    API = "api"
    SCRAPE = "scrape"


class Priority(Enum):
    """Knowledge item priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class KnowledgeItem:
    """
    Universal knowledge unit across all sources.

    This is the standard schema that all ingestion providers produce.
    Enables cross-source deduplication, unified indexing, and consistent output.
    """

    # Identity
    url: str                              # Canonical source URL
    title: str                            # Item title

    # Content
    summary: str = ""                     # Brief description
    content: str = ""                     # Full text if available

    # Classification
    source_provider: str = ""             # "microsoft", "python", "arxiv"
    source_type: SourceType = SourceType.RSS
    source_name: str = ""                 # Human-readable source name
    category: str = ""                    # Provider-specific category
    tags: list[str] = field(default_factory=list)

    # Temporal
    published: Optional[datetime] = None  # When source published it
    ingested: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    first_seen: Optional[datetime] = None # When AIOS first saw it

    # Quality
    priority: Priority = Priority.MEDIUM
    relevance_score: float = 0.5          # 0.0-1.0 AIOS relevance

    # Provenance
    raw_metadata: dict = field(default_factory=dict)

    # Computed
    _id: str = field(default="", init=False)

    def __post_init__(self):
        """Compute ID hash from URL."""
        self._id = hashlib.sha256(self.url.encode()).hexdigest()[:12]
        if self.first_seen is None:
            self.first_seen = self.ingested

    @property
    def id(self) -> str:
        """Unique identifier based on URL hash."""
        return self._id

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "summary": self.summary,
            "content": self.content[:1000] if self.content else "",  # Truncate
            "source_provider": self.source_provider,
            "source_type": self.source_type.value,
            "source_name": self.source_name,
            "category": self.category,
            "tags": self.tags,
            "published": self.published.isoformat() if self.published else None,
            "ingested": self.ingested.isoformat(),
            "first_seen": self.first_seen.isoformat() if self.first_seen else None,
            "priority": self.priority.value,
            "relevance_score": self.relevance_score,
        }

    def to_markdown(self) -> str:
        """Generate markdown representation."""
        lines = [
            f"### [{self.title}]({self.url})",
            "",
            f"**Source**: {self.source_name} | **Category**: {self.category} | **Priority**: {self.priority.value}",
            "",
        ]
        if self.summary:
            lines.append(self.summary)
            lines.append("")
        if self.tags:
            lines.append(f"**Tags**: {', '.join(self.tags)}")
            lines.append("")
        return "\n".join(lines)

    @classmethod
    def from_dict(cls, data: dict) -> "KnowledgeItem":
        """Create from dictionary."""
        return cls(
            url=data["url"],
            title=data["title"],
            summary=data.get("summary", ""),
            content=data.get("content", ""),
            source_provider=data.get("source_provider", ""),
            source_type=SourceType(data.get("source_type", "rss")),
            source_name=data.get("source_name", ""),
            category=data.get("category", ""),
            tags=data.get("tags", []),
            published=datetime.fromisoformat(data["published"]) if data.get("published") else None,
            priority=Priority(data.get("priority", "medium")),
            relevance_score=data.get("relevance_score", 0.5),
        )


@dataclass
class IngestionResult:
    """Result of an ingestion operation."""

    provider: str
    source_name: str
    items: list[KnowledgeItem] = field(default_factory=list)
    new_items: int = 0
    duplicate_items: int = 0
    errors: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def success(self) -> bool:
        return len(self.errors) == 0

    @property
    def total_items(self) -> int:
        return len(self.items)


class KnowledgeSource(ABC):
    """
    Abstract base class for knowledge sources.

    All ingestion providers must implement this interface.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Provider identifier (e.g., 'microsoft', 'python')."""
        ...

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Human-readable source name."""
        ...

    @property
    @abstractmethod
    def source_type(self) -> SourceType:
        """Type of source (RSS, docs, etc.)."""
        ...

    @abstractmethod
    async def fetch(self, **kwargs) -> list[KnowledgeItem]:
        """
        Fetch knowledge items from this source.

        Returns list of KnowledgeItem instances.
        """
        ...

    @abstractmethod
    def get_config(self) -> dict:
        """Get source configuration for serialization."""
        ...

    def filter_relevant(self, items: list[KnowledgeItem], keywords: list[str] | None = None) -> list[KnowledgeItem]:
        """
        Filter items by relevance keywords.

        Default implementation checks title and summary.
        Override for source-specific filtering.
        """
        if not keywords:
            return items

        def is_relevant(item: KnowledgeItem) -> bool:
            text = f"{item.title} {item.summary}".lower()
            return any(kw.lower() in text for kw in keywords)

        return [item for item in items if is_relevant(item)]


class KnowledgeProvider(ABC):
    """
    Abstract base class for knowledge providers.

    A provider groups multiple related sources (e.g., Microsoft provider
    has Windows Dev Blog, Azure AI Blog, VS Code Blog sources).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name (e.g., 'microsoft')."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Provider description."""
        ...

    @abstractmethod
    def get_sources(self) -> list[KnowledgeSource]:
        """Get all sources for this provider."""
        ...

    async def fetch_all(self, **kwargs) -> list[IngestionResult]:
        """Fetch from all sources."""
        results = []
        for source in self.get_sources():
            try:
                items = await source.fetch(**kwargs)
                results.append(IngestionResult(
                    provider=self.name,
                    source_name=source.source_name,
                    items=items,
                    new_items=len(items),
                ))
            except Exception as e:
                results.append(IngestionResult(
                    provider=self.name,
                    source_name=source.source_name,
                    errors=[str(e)],
                ))
        return results

    def get_config(self) -> dict:
        """Get provider configuration."""
        return {
            "name": self.name,
            "description": self.description,
            "sources": [s.get_config() for s in self.get_sources()],
        }
