"""
AIOS Knowledge Ingestion Registry
=================================

AINLP.dendritic[ai/ingestion/registry]{discovery,registration,coordination}

Central registry for knowledge providers and sources.
Enables discovery, coordination, and unified querying.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .protocol import KnowledgeItem, KnowledgeProvider, KnowledgeSource, IngestionResult

logger = logging.getLogger("AIOS.KIP.Registry")


class SourceRegistry:
    """
    Central registry for knowledge sources and providers.

    Manages registration, discovery, and coordination of all
    knowledge ingestion components.
    """

    def __init__(self, state_file: Optional[Path] = None):
        """
        Initialize registry.

        Args:
            state_file: Optional path to persist registry state
        """
        self._providers: dict[str, KnowledgeProvider] = {}
        self._sources: dict[str, KnowledgeSource] = {}
        self._state_file = state_file
        self._last_fetch: dict[str, datetime] = {}

        if state_file and state_file.exists():
            self._load_state()

    def register_provider(self, provider: KnowledgeProvider) -> None:
        """
        Register a knowledge provider.

        Args:
            provider: KnowledgeProvider instance
        """
        self._providers[provider.name] = provider
        logger.info(f"Registered provider: {provider.name} ({len(provider.get_sources())} sources)")

        # Also register individual sources
        for source in provider.get_sources():
            source_key = f"{provider.name}/{source.source_name}"
            self._sources[source_key] = source

    def register_source(self, provider_name: str, source: KnowledgeSource) -> None:
        """
        Register an individual source.

        Args:
            provider_name: Provider this source belongs to
            source: KnowledgeSource instance
        """
        source_key = f"{provider_name}/{source.source_name}"
        self._sources[source_key] = source
        logger.info(f"Registered source: {source_key}")

    def get_provider(self, name: str) -> Optional[KnowledgeProvider]:
        """Get provider by name."""
        return self._providers.get(name)

    def get_source(self, key: str) -> Optional[KnowledgeSource]:
        """Get source by key (provider/source_name)."""
        return self._sources.get(key)

    def list_providers(self) -> list[str]:
        """List all registered provider names."""
        return list(self._providers.keys())

    def list_sources(self) -> list[str]:
        """List all registered source keys."""
        return list(self._sources.keys())

    async def fetch_all(self, **kwargs) -> list[IngestionResult]:
        """
        Fetch from all registered providers.

        Returns list of IngestionResult for each source.
        """
        all_results = []

        for provider in self._providers.values():
            try:
                results = await provider.fetch_all(**kwargs)
                all_results.extend(results)

                # Update last fetch time
                for result in results:
                    source_key = f"{result.provider}/{result.source_name}"
                    self._last_fetch[source_key] = result.timestamp

            except Exception as e:
                logger.error(f"Error fetching from {provider.name}: {e}")
                all_results.append(IngestionResult(
                    provider=provider.name,
                    source_name="*",
                    errors=[str(e)],
                ))

        self._save_state()
        return all_results

    async def fetch_provider(self, provider_name: str, **kwargs) -> list[IngestionResult]:
        """Fetch from a specific provider."""
        provider = self._providers.get(provider_name)
        if not provider:
            return [IngestionResult(
                provider=provider_name,
                source_name="*",
                errors=[f"Provider not found: {provider_name}"],
            )]

        results = await provider.fetch_all(**kwargs)

        for result in results:
            source_key = f"{result.provider}/{result.source_name}"
            self._last_fetch[source_key] = result.timestamp

        self._save_state()
        return results

    async def fetch_source(self, source_key: str, **kwargs) -> IngestionResult:
        """Fetch from a specific source."""
        source = self._sources.get(source_key)
        if not source:
            return IngestionResult(
                provider=source_key.split("/")[0] if "/" in source_key else "unknown",
                source_name=source_key,
                errors=[f"Source not found: {source_key}"],
            )

        try:
            items = await source.fetch(**kwargs)
            provider_name = source_key.split("/")[0]
            result = IngestionResult(
                provider=provider_name,
                source_name=source.source_name,
                items=items,
                new_items=len(items),
            )
            self._last_fetch[source_key] = result.timestamp
            self._save_state()
            return result
        except Exception as e:
            return IngestionResult(
                provider=source_key.split("/")[0],
                source_name=source.source_name,
                errors=[str(e)],
            )

    def get_last_fetch(self, source_key: str) -> Optional[datetime]:
        """Get last fetch time for a source."""
        return self._last_fetch.get(source_key)

    def get_config(self) -> dict:
        """Get full registry configuration."""
        return {
            "providers": {
                name: provider.get_config()
                for name, provider in self._providers.items()
            },
            "last_fetch": {
                key: ts.isoformat()
                for key, ts in self._last_fetch.items()
            },
        }

    def _save_state(self) -> None:
        """Persist registry state to file."""
        if not self._state_file:
            return

        state = {
            "last_fetch": {
                key: ts.isoformat()
                for key, ts in self._last_fetch.items()
            },
            "updated": datetime.now(timezone.utc).isoformat(),
        }

        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        self._state_file.write_text(json.dumps(state, indent=2), encoding="utf-8")

    def _load_state(self) -> None:
        """Load registry state from file."""
        if not self._state_file or not self._state_file.exists():
            return

        try:
            state = json.loads(self._state_file.read_text(encoding="utf-8"))
            self._last_fetch = {
                key: datetime.fromisoformat(ts)
                for key, ts in state.get("last_fetch", {}).items()
            }
        except Exception as e:
            logger.warning(f"Failed to load registry state: {e}")


# Global registry instance
_registry: Optional[SourceRegistry] = None


def get_registry(state_file: Optional[Path] = None) -> SourceRegistry:
    """Get or create global registry instance."""
    global _registry
    if _registry is None:
        _registry = SourceRegistry(state_file)
    return _registry
