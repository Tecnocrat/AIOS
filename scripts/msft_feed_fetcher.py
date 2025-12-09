#!/usr/bin/env python3
"""
AIOS Microsoft Feed Fetcher
===========================

AINLP.dendritic[MSFT→AIOS]{feed,fetcher,automation}

Standalone feed fetcher for GitHub Actions workflow.
Fetches Microsoft ecosystem RSS feeds and saves as Markdown.

Usage:
    python scripts/msft_feed_fetcher.py

Environment Variables:
    MAX_ITEMS: Maximum items per feed (default: 10)
    PRIORITY_FILTER: Filter by priority (high, medium, low, all)
    OUTPUT_DIR: Output directory (default: docs/distilled/microsoft/release_notes)
"""

import asyncio
import hashlib
import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

# Try to use aiohttp, fall back to urllib
try:
    import aiohttp

    AIOHTTP_AVAILABLE = True
except ImportError:
    import urllib.request

    AIOHTTP_AVAILABLE = False

# =============================================================================
# FEED CONFIGURATION
# =============================================================================

FEEDS = {
    "windows_dev": {
        "name": "Windows Developer Blog",
        "url": "https://blogs.windows.com/windowsdeveloper/feed/",
        "category": "agentic_windows",
        "priority": "high",
        "filter": None,
    },
    "azure_ai": {
        "name": "Azure AI Blog",
        "url": "https://azure.microsoft.com/en-us/blog/feed/",
        "category": "azure_ai_foundry",
        "priority": "high",
        "filter": ["AI", "Copilot", "GPT", "LLM", "Agent", "Foundry", "OpenAI", "Machine Learning"],
    },
    "dotnet": {
        "name": ".NET Blog",
        "url": "https://devblogs.microsoft.com/dotnet/feed/",
        "category": "dotnet_evolution",
        "priority": "medium",
        "filter": None,
    },
    "vscode": {
        "name": "VS Code Blog",
        "url": "https://code.visualstudio.com/feed.xml",
        "category": "developer_tools",
        "priority": "medium",
        "filter": None,
    },
    "github": {
        "name": "GitHub Blog",
        "url": "https://github.blog/feed/",
        "category": "developer_tools",
        "priority": "medium",
        "filter": ["Copilot", "AI", "Agent", "Actions", "Codespaces"],
    },
}


def clean_html(text: str) -> str:
    """Remove HTML tags from text."""
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", clean).strip()[:500]


def is_relevant(title: str, summary: str, filters: list | None) -> bool:
    """Check if content matches relevance filters."""
    if not filters:
        return True
    text = f"{title} {summary}".lower()
    return any(f.lower() in text for f in filters)


def parse_feed(content: str, config: dict, max_items: int) -> list[dict]:
    """Parse RSS/Atom feed content."""
    items = []

    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        print(f"❌ {config['name']}: Parse error - {e}")
        return []

    # RSS 2.0 format
    for item in root.findall(".//item")[:max_items]:
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        pub = item.findtext("pubDate", "")
        desc = clean_html(item.findtext("description", ""))

        if link and is_relevant(title, desc, config.get("filter")):
            items.append(
                {
                    "source": config["name"],
                    "category": config["category"],
                    "priority": config["priority"],
                    "title": title,
                    "url": link,
                    "published": pub,
                    "summary": desc,
                    "hash": hashlib.sha256(link.encode()).hexdigest()[:12],
                }
            )

    # Atom format
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall(".//atom:entry", ns)[:max_items]:
        title = entry.findtext("atom:title", "", ns)
        link_el = entry.find("atom:link[@rel='alternate']", ns)
        if link_el is None:
            link_el = entry.find("atom:link", ns)
        link = link_el.get("href", "") if link_el is not None else ""
        pub = entry.findtext("atom:published", "", ns)
        desc = clean_html(entry.findtext("atom:summary", "", ns))

        if link and is_relevant(title, desc, config.get("filter")):
            items.append(
                {
                    "source": config["name"],
                    "category": config["category"],
                    "priority": config["priority"],
                    "title": title,
                    "url": link,
                    "published": pub,
                    "summary": desc,
                    "hash": hashlib.sha256(link.encode()).hexdigest()[:12],
                }
            )

    return items


# User-Agent to avoid 403 errors on some feeds
HEADERS = {"User-Agent": "AIOS-Feed-Fetcher/1.0 (https://github.com/Tecnocrat/aios-win)"}


async def fetch_feed_async(session, config: dict, max_items: int) -> list[dict]:
    """Fetch feed using aiohttp."""
    try:
        async with session.get(config["url"], timeout=30, headers=HEADERS) as resp:
            if resp.status != 200:
                print(f"X {config['name']}: HTTP {resp.status}")
                return []
            content = await resp.text()
    except Exception as e:
        print(f"X {config['name']}: {e}")
        return []

    items = parse_feed(content, config, max_items)
    print(f"OK {config['name']}: {len(items)} items")
    return items


def fetch_feed_sync(config: dict, max_items: int) -> list[dict]:
    """Fetch feed using urllib (fallback)."""
    try:
        req = urllib.request.Request(config["url"], headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8")
    except Exception as e:
        print(f"X {config['name']}: {e}")
        return []

    items = parse_feed(content, config, max_items)
    print(f"OK {config['name']}: {len(items)} items")
    return items


async def fetch_all_feeds(max_items: int, priority_filter: str) -> list[dict]:
    """Fetch all configured feeds."""
    all_items = []

    if AIOHTTP_AVAILABLE:
        async with aiohttp.ClientSession() as session:
            for key, config in FEEDS.items():
                if priority_filter != "all" and config["priority"] != priority_filter:
                    continue
                items = await fetch_feed_async(session, config, max_items)
                all_items.extend(items)
    else:
        for key, config in FEEDS.items():
            if priority_filter != "all" and config["priority"] != priority_filter:
                continue
            items = fetch_feed_sync(config, max_items)
            all_items.extend(items)

    return all_items


def save_updates(items: list[dict], output_dir: Path):
    """Save updates to Markdown files."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Group by category
    by_category: dict[str, list] = {}
    for item in items:
        cat = item["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(item)

    # Save category files
    for category, cat_items in by_category.items():
        cat_dir = output_dir / category
        cat_dir.mkdir(parents=True, exist_ok=True)

        # Save JSON index
        index_file = cat_dir / f"{timestamp}_index.json"
        index_file.write_text(json.dumps(cat_items, indent=2))

        # Save Markdown summary
        md_file = cat_dir / f"{timestamp}_updates.md"
        md_content = f"# {category.replace('_', ' ').title()} Updates - {timestamp}\n\n"
        md_content += f"> **Count**: {len(cat_items)} | **Generated**: {datetime.now(timezone.utc).isoformat()}\n\n"
        md_content += "---\n\n"

        for item in cat_items:
            md_content += f"## [{item['title']}]({item['url']})\n\n"
            md_content += f"**Source**: {item['source']} | **Priority**: {item['priority']}\n\n"
            if item["summary"]:
                md_content += f"{item['summary']}\n\n"
            md_content += f"*Hash: {item['hash']}*\n\n---\n\n"

        md_file.write_text(md_content, encoding="utf-8")
        print(f"Saved: {cat_dir.name}/{timestamp}_updates.md")

    # Generate master index
    master_index = output_dir / "LATEST_UPDATES.md"
    master_content = f"""# Microsoft Frontier Updates - {timestamp}

> **Generated**: {datetime.now(timezone.utc).isoformat()}
> **Total Items**: {len(items)}
> **AINLP.dendritic**: MSFT ingestion automated

---

## Categories

"""
    for category, cat_items in sorted(by_category.items()):
        master_content += f"### {category.replace('_', ' ').title()} ({len(cat_items)} items)\n\n"
        for item in cat_items[:3]:
            title_short = item["title"][:60] + "..." if len(item["title"]) > 60 else item["title"]
            master_content += f"- [{title_short}]({item['url']})\n"
        if len(cat_items) > 3:
            master_content += (
                f"- *...and {len(cat_items) - 3} more in {category}/{timestamp}_updates.md*\n"
            )
        master_content += "\n"

    master_content += """---

## Feed Sources

| Source | Category | Priority |
|--------|----------|----------|
"""
    for key, config in FEEDS.items():
        master_content += f"| {config['name']} | {config['category']} | {config['priority']} |\n"

    master_content += f"\n---\n\n*AIOS Microsoft Frontier Ingestion*\n"

    master_index.write_text(master_content, encoding="utf-8")
    print(f"\nMaster index: {master_index}")

    return by_category


async def main():
    """Main entry point."""
    # Configuration from environment
    max_items = int(os.environ.get("MAX_ITEMS", "10"))
    priority_filter = os.environ.get("PRIORITY_FILTER", "high")
    output_dir = Path(os.environ.get("OUTPUT_DIR", "docs/distilled/microsoft/release_notes"))

    print(f"🔷 AIOS Microsoft Feed Fetcher")
    print(f"   Max items: {max_items}")
    print(f"   Priority: {priority_filter}")
    print(f"   Output: {output_dir}")
    print()

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Fetch all feeds
    items = await fetch_all_feeds(max_items, priority_filter)
    print(f"\n📊 Total: {len(items)} items")

    if items:
        # Save updates
        by_category = save_updates(items, output_dir)

        # Output for GitHub Actions
        print(f"\n::set-output name=items_count::{len(items)}")
        print(f"::set-output name=categories::{','.join(by_category.keys())}")
    else:
        print("\n⚠️ No items fetched")


if __name__ == "__main__":
    asyncio.run(main())
