"""
AIOS Knowledge Ingestion - Deduplication Engine
===============================================

AINLP.dendritic[ai/ingestion/deduplication]{dedup,hash,cross-source}

Cross-source deduplication using content hashing.
Prevents duplicate articles from different sources being stored twice.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .protocol import KnowledgeItem

logger = logging.getLogger("AIOS.KIP.Dedup")


class DeduplicationEngine:
    """
    Cross-source deduplication engine.

    Tracks seen content hashes to prevent duplicates across
    different providers and sources.
    """

    def __init__(self, state_file: Optional[Path] = None):
        """
        Initialize deduplication engine.

        Args:
            state_file: Path to persist seen hashes
        """
        self._seen_hashes: dict[str, dict] = {}  # hash -> metadata
        self._state_file = state_file

        if state_file and state_file.exists():
            self._load_state()

    def is_duplicate(self, item: KnowledgeItem) -> bool:
        """Check if item has been seen before."""
        return item.id in self._seen_hashes

    def mark_seen(self, item: KnowledgeItem) -> None:
        """Mark item as seen."""
        self._seen_hashes[item.id] = {
            "url": item.url,
            "title": item.title,
            "source_provider": item.source_provider,
            "source_name": item.source_name,
            "first_seen": item.first_seen.isoformat() if item.first_seen else None,
        }

    def deduplicate(
        self,
        items: list[KnowledgeItem],
        mark_new: bool = True,
    ) -> tuple[list[KnowledgeItem], list[KnowledgeItem]]:
        """
        Deduplicate a list of items.

        Args:
            items: Items to deduplicate
            mark_new: Whether to mark new items as seen

        Returns:
            Tuple of (new_items, duplicate_items)
        """
        new_items = []
        duplicates = []

        for item in items:
            if self.is_duplicate(item):
                duplicates.append(item)
            else:
                new_items.append(item)
                if mark_new:
                    self.mark_seen(item)

        if duplicates:
            logger.info(
                f"Dedup: {len(new_items)} new, {len(duplicates)} duplicates"
            )

        return new_items, duplicates

    def get_seen_count(self) -> int:
        """Get number of seen hashes."""
        return len(self._seen_hashes)

    def get_seen_info(self, item_id: str) -> Optional[dict]:
        """Get metadata for a seen item."""
        return self._seen_hashes.get(item_id)

    def save(self) -> None:
        """Persist state to file."""
        if not self._state_file:
            return

        self._state_file.parent.mkdir(parents=True, exist_ok=True)
        state = {
            "seen_hashes": self._seen_hashes,
            "count": len(self._seen_hashes),
            "updated": datetime.now(timezone.utc).isoformat(),
        }
        self._state_file.write_text(
            json.dumps(state, indent=2),
            encoding="utf-8"
        )
        logger.debug(f"Saved {len(self._seen_hashes)} hashes to {self._state_file}")

    def _load_state(self) -> None:
        """Load state from file."""
        if not self._state_file or not self._state_file.exists():
            return

        try:
            state = json.loads(self._state_file.read_text(encoding="utf-8"))
            self._seen_hashes = state.get("seen_hashes", {})
            logger.info(f"Loaded {len(self._seen_hashes)} seen hashes")
        except Exception as e:
            logger.warning(f"Failed to load dedup state: {e}")

    def clear(self) -> None:
        """Clear all seen hashes."""
        self._seen_hashes.clear()
        logger.info("Cleared deduplication state")


# Global dedup instance
_dedup: Optional[DeduplicationEngine] = None


def get_dedup_engine(state_file: Optional[Path] = None) -> DeduplicationEngine:
    """Get or create global dedup engine."""
    global _dedup
    if _dedup is None:
        _dedup = DeduplicationEngine(state_file)
    return _dedup
