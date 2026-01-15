"""
AIOS Knowledge Ingestion - Base Source Adapter
==============================================

AINLP.dendritic[ai/ingestion/sources/base]{adapter,abstract,interface}

Abstract base class for all source adapters.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional
import logging

from ..protocol import KnowledgeItem, KnowledgeSource, SourceType

logger = logging.getLogger("AIOS.KIP.Adapter")


@dataclass
class SourceConfig:
    """Configuration for a knowledge source."""

    name: str                              # Human-readable name
    url: str                               # Source URL or endpoint
    category: str = ""                     # Category classification
    priority: str = "medium"               # Priority level
    tags: list[str] = field(default_factory=list)
    filter_keywords: list[str] | None = None  # Relevance filters
    max_items: int = 50                    # Max items per fetch
    enabled: bool = True                   # Whether source is active

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "url": self.url,
            "category": self.category,
            "priority": self.priority,
            "tags": self.tags,
            "filter_keywords": self.filter_keywords,
            "max_items": self.max_items,
            "enabled": self.enabled,
        }


class BaseSourceAdapter(KnowledgeSource, ABC):
    """
    Base class for source adapters.

    Provides common functionality for all source types.
    Subclasses implement the actual fetching logic.
    """

    def __init__(
        self,
        provider_name: str,
        config: SourceConfig,
    ):
        self._provider_name = provider_name
        self._config = config

    @property
    def provider_name(self) -> str:
        return self._provider_name

    @property
    def source_name(self) -> str:
        return self._config.name

    @property
    def source_type(self) -> SourceType:
        """Override in subclass."""
        return SourceType.RSS

    @property
    def config(self) -> SourceConfig:
        return self._config

    def get_config(self) -> dict:
        return {
            "provider": self._provider_name,
            "type": self.source_type.value,
            **self._config.to_dict(),
        }

    def create_item(
        self,
        url: str,
        title: str,
        summary: str = "",
        content: str = "",
        published: Any = None,
        tags: list[str] | None = None,
        **kwargs,
    ) -> KnowledgeItem:
        """
        Create a KnowledgeItem with source metadata.

        Convenience method for adapters to create properly
        attributed knowledge items.
        """
        from ..protocol import Priority

        return KnowledgeItem(
            url=url,
            title=title,
            summary=summary,
            content=content,
            source_provider=self._provider_name,
            source_type=self.source_type,
            source_name=self._config.name,
            category=self._config.category,
            tags=tags or self._config.tags.copy(),
            published=published,
            priority=Priority(self._config.priority),
            **kwargs,
        )

    @abstractmethod
    async def fetch(self, **kwargs) -> list[KnowledgeItem]:
        """
        Fetch knowledge items from this source.

        Must be implemented by subclasses.
        """
        ...

    async def fetch_filtered(self, **kwargs) -> list[KnowledgeItem]:
        """
        Fetch and filter by relevance keywords.

        Uses filter_keywords from config if set.
        """
        items = await self.fetch(**kwargs)
        return self.filter_relevant(items, self._config.filter_keywords)
