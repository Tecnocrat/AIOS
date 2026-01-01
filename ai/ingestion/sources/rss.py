"""
AIOS Knowledge Ingestion - RSS Source Adapter
=============================================

AINLP.dendritic[ai/ingestion/sources/rss]{rss,atom,feed,parsing}

Generic RSS/Atom feed adapter for knowledge ingestion.
"""

import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any
import logging

from .base import BaseSourceAdapter, SourceConfig
from ..protocol import KnowledgeItem, SourceType

logger = logging.getLogger("AIOS.KIP.RSS")

# Try to use aiohttp, fall back to urllib
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    import urllib.request
    AIOHTTP_AVAILABLE = False


def clean_html(text: str) -> str:
    """Remove HTML tags from text."""
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", clean).strip()[:500]


def parse_date(date_str: str) -> datetime | None:
    """Parse various date formats from RSS feeds."""
    if not date_str:
        return None

    formats = [
        "%a, %d %b %Y %H:%M:%S %z",      # RFC 822
        "%a, %d %b %Y %H:%M:%S %Z",      # RFC 822 with timezone name
        "%Y-%m-%dT%H:%M:%S%z",           # ISO 8601
        "%Y-%m-%dT%H:%M:%SZ",            # ISO 8601 UTC
        "%Y-%m-%d %H:%M:%S",             # Simple datetime
        "%Y-%m-%d",                       # Simple date
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue

    # Try removing timezone abbreviation
    try:
        clean_date = re.sub(r'\s+[A-Z]{3,4}$', '', date_str.strip())
        return datetime.strptime(clean_date, "%a, %d %b %Y %H:%M:%S")
    except ValueError:
        pass

    return None


class RSSSourceAdapter(BaseSourceAdapter):
    """
    RSS/Atom feed source adapter.

    Fetches and parses RSS or Atom feeds into KnowledgeItems.
    """

    @property
    def source_type(self) -> SourceType:
        return SourceType.RSS

    async def fetch(self, max_items: int | None = None, **kwargs) -> list[KnowledgeItem]:
        """
        Fetch items from RSS/Atom feed.

        Args:
            max_items: Override max items from config

        Returns:
            List of KnowledgeItem instances
        """
        max_items = max_items or self._config.max_items

        try:
            content = await self._fetch_feed_content()
            if not content:
                return []

            return self._parse_feed(content, max_items)
        except Exception as e:
            logger.error(f"Error fetching {self._config.name}: {e}")
            return []

    async def _fetch_feed_content(self) -> str:
        """Fetch raw feed content from URL."""
        url = self._config.url

        if AIOHTTP_AVAILABLE:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    if response.status == 200:
                        return await response.text()
                    logger.warning(f"HTTP {response.status} from {url}")
                    return ""
        else:
            # Fallback to synchronous urllib
            import asyncio
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._fetch_sync, url)

    def _fetch_sync(self, url: str) -> str:
        """Synchronous fallback for feed fetching."""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AIOS-KIP/1.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode("utf-8")
        except Exception as e:
            logger.error(f"Sync fetch error: {e}")
            return ""

    def _parse_feed(self, content: str, max_items: int) -> list[KnowledgeItem]:
        """Parse RSS/Atom feed content."""
        items = []

        try:
            root = ET.fromstring(content)

            # Detect feed type
            if root.tag == "rss" or root.find("channel") is not None:
                items = self._parse_rss(root, max_items)
            elif "atom" in root.tag.lower() or root.find("{http://www.w3.org/2005/Atom}entry") is not None:
                items = self._parse_atom(root, max_items)
            else:
                # Try RSS-style parsing as default
                items = self._parse_rss(root, max_items)

        except ET.ParseError as e:
            logger.error(f"XML parse error for {self._config.name}: {e}")

        return items

    def _parse_rss(self, root: ET.Element, max_items: int) -> list[KnowledgeItem]:
        """Parse RSS 2.0 feed."""
        items = []
        channel = root.find("channel") or root

        for item in channel.findall("item")[:max_items]:
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            description = clean_html(item.findtext("description", ""))
            pub_date = parse_date(item.findtext("pubDate", ""))

            if not title or not link:
                continue

            # Extract categories/tags
            tags = [cat.text for cat in item.findall("category") if cat.text]

            items.append(self.create_item(
                url=link,
                title=title,
                summary=description,
                published=pub_date,
                tags=tags or None,
            ))

        return items

    def _parse_atom(self, root: ET.Element, max_items: int) -> list[KnowledgeItem]:
        """Parse Atom feed."""
        items = []
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        entries = root.findall("atom:entry", ns) or root.findall("{http://www.w3.org/2005/Atom}entry")

        for entry in entries[:max_items]:
            # Handle namespaced elements
            title_elem = entry.find("atom:title", ns) or entry.find("{http://www.w3.org/2005/Atom}title")
            title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""

            # Get link (prefer alternate)
            link = ""
            for link_elem in entry.findall("atom:link", ns) + entry.findall("{http://www.w3.org/2005/Atom}link"):
                href = link_elem.get("href", "")
                rel = link_elem.get("rel", "alternate")
                if rel == "alternate" or not link:
                    link = href

            # Get summary/content
            summary_elem = entry.find("atom:summary", ns) or entry.find("{http://www.w3.org/2005/Atom}summary")
            summary = clean_html(summary_elem.text if summary_elem is not None and summary_elem.text else "")

            # Get published date
            pub_elem = entry.find("atom:published", ns) or entry.find("{http://www.w3.org/2005/Atom}published")
            updated_elem = entry.find("atom:updated", ns) or entry.find("{http://www.w3.org/2005/Atom}updated")
            date_str = (pub_elem.text if pub_elem is not None else None) or \
                       (updated_elem.text if updated_elem is not None else None)
            pub_date = parse_date(date_str) if date_str else None

            if not title or not link:
                continue

            items.append(self.create_item(
                url=link,
                title=title,
                summary=summary,
                published=pub_date,
            ))

        return items
