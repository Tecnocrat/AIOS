#!/usr/bin/env python3
"""
AIOS Microsoft Frontier Distillation Bridge
============================================

AINLP.dendritic[MSFT→AIOS]{frontier,ingestion,distillation,agentic_windows}

Specialized bridge for ingesting Microsoft ecosystem updates and crystallizing
them into AIOS-consumable knowledge. Extends VOID Bridge patterns with:

- Microsoft-specific RSS/Atom feed parsing
- Learn.microsoft.com path extraction
- Azure AI Foundry documentation ingestion
- Windows Copilot Runtime knowledge synthesis
- Agentic Windows architecture tracking

DUAL-AGENT cascade (integrated with void_bridge.py):
    🔵 GITHUB GPT-4o-mini (Harmonizer) → 🟡 GEMINI 2.0 Flash (Creator) → 🔵 GITHUB GPT-4o (Verifier)

Priority Sources:
- Windows Dev Blog: https://blogs.windows.com/windowsdeveloper/
- Azure AI Blog: https://azure.microsoft.com/en-us/blog/
- .NET Blog: https://devblogs.microsoft.com/dotnet/
- Microsoft Learn: https://learn.microsoft.com/
- GitHub Blog: https://github.blog/

Origin: AIOS Win HP_LAB - 2025-12-08
"""

import asyncio
import hashlib
import json
import logging
import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

# Import VOID Bridge for crystallization
try:
    from void_bridge import VOIDBridge, VOIDVertex, VOIDState
    VOID_AVAILABLE = True
except ImportError:
    VOID_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("AIOS.MSFT")


# =============================================================================
# MICROSOFT FRONTIER FEED REGISTRY
# =============================================================================

MSFT_FEEDS = {
    "windows_dev": {
        "name": "Windows Developer Blog",
        "url": "https://blogs.windows.com/windowsdeveloper/feed/",
        "category": "agentic_windows",
        "priority": "high",
        "tags": ["windows", "copilot", "sdk", "winui"],
    },
    "azure_ai": {
        "name": "Azure AI Blog",
        "url": "https://azure.microsoft.com/en-us/blog/feed/",
        "category": "azure_ai_foundry",
        "priority": "high",
        "tags": ["azure", "ai", "foundry", "models"],
        "filter_keywords": ["AI", "Copilot", "GPT", "LLM", "Agent", "Foundry"],
    },
    "dotnet": {
        "name": ".NET Blog",
        "url": "https://devblogs.microsoft.com/dotnet/feed/",
        "category": "dotnet_evolution",
        "priority": "medium",
        "tags": ["dotnet", "csharp", "aspnet", "maui"],
    },
    "vscode": {
        "name": "VS Code Blog",
        "url": "https://code.visualstudio.com/feed.xml",
        "category": "developer_tools",
        "priority": "medium",
        "tags": ["vscode", "extensions", "copilot"],
    },
    "github": {
        "name": "GitHub Blog",
        "url": "https://github.blog/feed/",
        "category": "developer_tools",
        "priority": "medium",
        "tags": ["github", "copilot", "actions", "codespaces"],
        "filter_keywords": ["Copilot", "AI", "Agent", "Actions"],
    },
    "windows_insider": {
        "name": "Windows Insider Blog",
        "url": "https://blogs.windows.com/windows-insider/feed/",
        "category": "windows_internals",
        "priority": "low",
        "tags": ["windows", "insider", "preview"],
    },
}

# Microsoft Learn paths to track
MSLEARN_PATHS = {
    "agentic_windows": [
        "https://learn.microsoft.com/en-us/windows/ai/",
        "https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/",
        "https://learn.microsoft.com/en-us/windows/apps/design/",
    ],
    "azure_ai_foundry": [
        "https://learn.microsoft.com/en-us/azure/ai-services/",
        "https://learn.microsoft.com/en-us/azure/ai-studio/",
        "https://learn.microsoft.com/en-us/azure/machine-learning/",
    ],
    "copilot_sdk": [
        "https://learn.microsoft.com/en-us/copilot/",
        "https://learn.microsoft.com/en-us/microsoft-365-copilot/",
        "https://docs.github.com/en/copilot",
    ],
    "dotnet_evolution": [
        "https://learn.microsoft.com/en-us/dotnet/core/whats-new/",
        "https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/",
        "https://learn.microsoft.com/en-us/aspnet/core/release-notes/",
    ],
}


@dataclass
class MSFTUpdate:
    """A Microsoft frontier update ready for crystallization."""
    
    source: str
    title: str
    url: str
    published: str
    category: str
    tags: list[str] = field(default_factory=list)
    summary: str = ""
    content: str = ""
    priority: str = "medium"
    relevance_score: float = 0.0
    hash_id: str = ""
    
    def __post_init__(self):
        if not self.hash_id:
            self.hash_id = hashlib.sha256(self.url.encode()).hexdigest()[:12]
    
    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "title": self.title,
            "url": self.url,
            "published": self.published,
            "category": self.category,
            "tags": self.tags,
            "summary": self.summary[:500] if self.summary else "",
            "priority": self.priority,
            "relevance_score": self.relevance_score,
            "hash_id": self.hash_id,
        }


class MSFTDistillationBridge:
    """
    Microsoft Frontier Knowledge Distillation Bridge.
    
    Ingests Microsoft ecosystem updates and crystallizes them into
    AIOS-consumable knowledge patterns.
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path("docs/distilled/microsoft")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # State tracking
        self.updates: list[MSFTUpdate] = []
        self.processed_hashes: set[str] = set()
        self.state_file = self.output_dir / "ingestion_state.json"
        
        # Load previous state
        self._load_state()
        
        # Initialize VOID Bridge if available
        self.void_bridge = VOIDBridge() if VOID_AVAILABLE else None
        
        logger.info("🔷 MSFT Distillation Bridge initialized")
        logger.info(f"   Output: {self.output_dir}")
        logger.info(f"   VOID Bridge: {'✅' if self.void_bridge else '❌'}")
    
    def _load_state(self):
        """Load previous ingestion state."""
        if self.state_file.exists():
            try:
                state = json.loads(self.state_file.read_text(encoding="utf-8"))
                self.processed_hashes = set(state.get("processed_hashes", []))
                logger.info(f"   Loaded {len(self.processed_hashes)} processed hashes")
            except Exception as e:
                logger.warning(f"   Failed to load state: {e}")
    
    def _save_state(self):
        """Save ingestion state."""
        state = {
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "processed_hashes": list(self.processed_hashes),
            "total_processed": len(self.processed_hashes),
        }
        self.state_file.write_text(
            json.dumps(state, indent=2), encoding="utf-8"
        )
    
    async def fetch_rss_feed(self, feed_key: str) -> list[MSFTUpdate]:
        """Fetch and parse an RSS/Atom feed."""
        import aiohttp
        
        feed_config = MSFT_FEEDS.get(feed_key)
        if not feed_config:
            logger.error(f"Unknown feed: {feed_key}")
            return []
        
        url = feed_config["url"]
        logger.info(f"📡 Fetching {feed_config['name']}...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    if response.status != 200:
                        logger.error(f"   HTTP {response.status}")
                        return []
                    
                    content = await response.text()
        except Exception as e:
            logger.error(f"   Fetch error: {e}")
            return []
        
        # Parse RSS/Atom
        updates = self._parse_feed(content, feed_config)
        logger.info(f"   Found {len(updates)} items")
        
        return updates
    
    def _parse_feed(self, content: str, feed_config: dict) -> list[MSFTUpdate]:
        """Parse RSS/Atom feed content."""
        updates = []
        
        try:
            root = ET.fromstring(content)
        except ET.ParseError as e:
            logger.error(f"   XML parse error: {e}")
            return []
        
        # Handle RSS 2.0
        for item in root.findall(".//item"):
            update = self._parse_rss_item(item, feed_config)
            if update and self._is_relevant(update, feed_config):
                updates.append(update)
        
        # Handle Atom
        for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
            update = self._parse_atom_entry(entry, feed_config)
            if update and self._is_relevant(update, feed_config):
                updates.append(update)
        
        return updates
    
    def _parse_rss_item(self, item: ET.Element, feed_config: dict) -> Optional[MSFTUpdate]:
        """Parse RSS 2.0 item."""
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        pub_date = item.findtext("pubDate", "")
        description = item.findtext("description", "")
        
        if not title or not link:
            return None
        
        return MSFTUpdate(
            source=feed_config["name"],
            title=title,
            url=link,
            published=pub_date,
            category=feed_config["category"],
            tags=feed_config.get("tags", []),
            summary=self._clean_html(description),
            priority=feed_config.get("priority", "medium"),
        )
    
    def _parse_atom_entry(self, entry: ET.Element, feed_config: dict) -> Optional[MSFTUpdate]:
        """Parse Atom entry."""
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        
        title = entry.findtext("atom:title", "", ns)
        link_elem = entry.find("atom:link[@rel='alternate']", ns)
        if link_elem is None:
            link_elem = entry.find("atom:link", ns)
        link = link_elem.get("href", "") if link_elem is not None else ""
        published = entry.findtext("atom:published", "", ns)
        summary = entry.findtext("atom:summary", "", ns)
        
        if not title or not link:
            return None
        
        return MSFTUpdate(
            source=feed_config["name"],
            title=title,
            url=link,
            published=published,
            category=feed_config["category"],
            tags=feed_config.get("tags", []),
            summary=self._clean_html(summary),
            priority=feed_config.get("priority", "medium"),
        )
    
    def _clean_html(self, text: str) -> str:
        """Remove HTML tags from text."""
        if not text:
            return ""
        clean = re.sub(r"<[^>]+>", "", text)
        clean = re.sub(r"\s+", " ", clean).strip()
        return clean[:1000]  # Truncate for summary
    
    def _is_relevant(self, update: MSFTUpdate, feed_config: dict) -> bool:
        """Check if update matches relevance filters."""
        # Skip if already processed
        if update.hash_id in self.processed_hashes:
            return False
        
        # Apply keyword filter if present
        keywords = feed_config.get("filter_keywords", [])
        if keywords:
            text = f"{update.title} {update.summary}".lower()
            matched = any(kw.lower() in text for kw in keywords)
            if matched:
                update.relevance_score = 0.8
            else:
                update.relevance_score = 0.3
                return False  # Skip non-matching
        else:
            update.relevance_score = 0.6
        
        return True
    
    async def fetch_all_feeds(self, priority_filter: Optional[str] = None) -> list[MSFTUpdate]:
        """Fetch updates from all configured feeds."""
        all_updates = []
        
        for feed_key, config in MSFT_FEEDS.items():
            if priority_filter and config.get("priority") != priority_filter:
                continue
            
            updates = await self.fetch_rss_feed(feed_key)
            all_updates.extend(updates)
        
        # Sort by relevance and date
        all_updates.sort(
            key=lambda u: (u.relevance_score, u.published),
            reverse=True
        )
        
        self.updates = all_updates
        logger.info(f"📊 Total relevant updates: {len(all_updates)}")
        
        return all_updates
    
    async def crystallize_update(self, update: MSFTUpdate) -> Optional[Path]:
        """Crystallize a single update using VOID Bridge."""
        if not self.void_bridge:
            logger.warning("VOID Bridge not available - saving raw")
            return self._save_raw_update(update)
        
        logger.info(f"🔮 Crystallizing: {update.title[:60]}...")
        
        # Create VOID vertex from update
        vertex = VOIDVertex(
            source=update.url,
            title=update.title,
            tags=update.tags + [update.category],
            content=f"{update.summary}\n\nSource: {update.url}",
            metadata={
                "msft_source": update.source,
                "category": update.category,
                "priority": update.priority,
            }
        )
        
        # Use VOID Bridge crystallization
        try:
            # Fetch full content if needed
            if len(update.content) < 100:
                await self.void_bridge._async_fetch(vertex)
            
            # Crystallize with DUAL-AGENT cascade
            crystal = await self.void_bridge._dual_agent_crystallize(
                vertex.content,
                extraction_pattern="microsoft_frontier"
            )
            
            if crystal:
                vertex.crystallized = crystal
                vertex.state = VOIDState.CRYSTAL
                
                # Save crystal
                output_path = self._save_crystal(update, crystal)
                
                # Mark as processed
                self.processed_hashes.add(update.hash_id)
                self._save_state()
                
                return output_path
        except Exception as e:
            logger.error(f"   Crystallization error: {e}")
        
        return None
    
    def _save_raw_update(self, update: MSFTUpdate) -> Path:
        """Save raw update without crystallization."""
        category_dir = self.output_dir / update.category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{update.hash_id}_{self._slugify(update.title)}.json"
        output_path = category_dir / filename
        
        output_path.write_text(
            json.dumps(update.to_dict(), indent=2),
            encoding="utf-8"
        )
        
        return output_path
    
    def _save_crystal(self, update: MSFTUpdate, crystal: str) -> Path:
        """Save crystallized knowledge."""
        category_dir = self.output_dir / update.category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{update.hash_id}_{self._slugify(update.title)}_CRYSTAL.md"
        output_path = category_dir / filename
        
        # Build crystal document
        doc = f"""# {update.title}

> **Source**: [{update.source}]({update.url})
> **Published**: {update.published}
> **Category**: {update.category}
> **Priority**: {update.priority}
> **AINLP.dendritic[MSFT→{update.category}]{{crystallized}}**

---

{crystal}

---

*Crystallized: {datetime.now(timezone.utc).isoformat()}*
*Hash: {update.hash_id}*
"""
        
        output_path.write_text(doc, encoding="utf-8")
        logger.info(f"   ✅ Saved: {output_path.name}")
        
        return output_path
    
    def _slugify(self, text: str) -> str:
        """Convert text to filename-safe slug."""
        slug = re.sub(r"[^a-z0-9]+", "_", text.lower())
        return slug[:50].strip("_")
    
    async def ingest_learn_path(self, path_url: str, category: str = "general") -> list[Path]:
        """Ingest a Microsoft Learn path."""
        if not self.void_bridge:
            logger.error("VOID Bridge required for Learn path ingestion")
            return []
        
        logger.info(f"📚 Ingesting Learn path: {path_url}")
        
        # Use VOID Bridge's MSLearn adapter if available
        crystals = []
        
        try:
            # Create vertex for the path
            vertex = VOIDVertex(
                source=path_url,
                title=f"Microsoft Learn: {category}",
                tags=["mslearn", category],
            )
            
            # Fetch and crystallize
            await self.void_bridge._async_fetch(vertex)
            
            if vertex.content:
                crystal = await self.void_bridge._dual_agent_crystallize(
                    vertex.content,
                    extraction_pattern="microsoft_learn"
                )
                
                if crystal:
                    category_dir = self.output_dir / category
                    category_dir.mkdir(parents=True, exist_ok=True)
                    
                    slug = self._slugify(urlparse(path_url).path)
                    output_path = category_dir / f"learn_{slug}_CRYSTAL.md"
                    
                    output_path.write_text(f"""# Microsoft Learn: {category}

> **Source**: [{path_url}]({path_url})
> **AINLP.dendritic[MSLearn→{category}]{{crystallized}}**

---

{crystal}

---

*Crystallized: {datetime.now(timezone.utc).isoformat()}*
""", encoding="utf-8")
                    
                    crystals.append(output_path)
                    logger.info(f"   ✅ Saved: {output_path.name}")
        except Exception as e:
            logger.error(f"   Learn path error: {e}")
        
        return crystals
    
    def generate_summary_report(self) -> Path:
        """Generate a summary report of all ingested updates."""
        report_path = self.output_dir / "INGESTION_REPORT.md"
        
        # Group by category
        by_category: dict[str, list[MSFTUpdate]] = {}
        for update in self.updates:
            if update.category not in by_category:
                by_category[update.category] = []
            by_category[update.category].append(update)
        
        report = f"""# Microsoft Frontier Ingestion Report

> **Generated**: {datetime.now(timezone.utc).isoformat()}
> **Total Updates**: {len(self.updates)}
> **Categories**: {len(by_category)}

---

## Summary by Category

"""
        
        for category, updates in sorted(by_category.items()):
            report += f"### {category.replace('_', ' ').title()}\n\n"
            report += f"**Count**: {len(updates)}\n\n"
            
            for update in updates[:5]:  # Top 5 per category
                report += f"- [{update.title[:60]}...]({update.url}) ({update.priority})\n"
            
            if len(updates) > 5:
                report += f"- *...and {len(updates) - 5} more*\n"
            
            report += "\n"
        
        report += f"""---

## Feed Status

| Feed | Category | Priority |
|------|----------|----------|
"""
        
        for key, config in MSFT_FEEDS.items():
            report += f"| {config['name']} | {config['category']} | {config['priority']} |\n"
        
        report += f"""
---

*AIOS Microsoft Frontier Distillation Bridge*
*AINLP.dendritic[MSFT→report]{{ingestion,summary}}*
"""
        
        report_path.write_text(report, encoding="utf-8")
        logger.info(f"📋 Report saved: {report_path}")
        
        return report_path


# =============================================================================
# CLI INTERFACE
# =============================================================================

async def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AIOS Microsoft Frontier Distillation Bridge"
    )
    parser.add_argument(
        "--fetch", action="store_true",
        help="Fetch all RSS feeds"
    )
    parser.add_argument(
        "--crystallize", action="store_true",
        help="Crystallize fetched updates"
    )
    parser.add_argument(
        "--priority", choices=["high", "medium", "low"],
        help="Filter by priority level"
    )
    parser.add_argument(
        "--learn-path", type=str,
        help="Ingest a Microsoft Learn path URL"
    )
    parser.add_argument(
        "--category", type=str, default="general",
        help="Category for Learn path ingestion"
    )
    parser.add_argument(
        "--report", action="store_true",
        help="Generate summary report"
    )
    parser.add_argument(
        "--interactive", action="store_true",
        help="Interactive mode"
    )
    parser.add_argument(
        "--output", type=str,
        help="Output directory"
    )
    
    args = parser.parse_args()
    
    # Initialize bridge
    output_dir = Path(args.output) if args.output else None
    bridge = MSFTDistillationBridge(output_dir)
    
    if args.interactive:
        await interactive_mode(bridge)
        return
    
    if args.fetch or args.crystallize:
        updates = await bridge.fetch_all_feeds(args.priority)
        
        if args.crystallize and updates:
            logger.info(f"\n🔮 Crystallizing {len(updates)} updates...")
            for update in updates[:10]:  # Limit to 10 for safety
                await bridge.crystallize_update(update)
    
    if args.learn_path:
        await bridge.ingest_learn_path(args.learn_path, args.category)
    
    if args.report or args.fetch:
        bridge.generate_summary_report()


async def interactive_mode(bridge: MSFTDistillationBridge):
    """Interactive exploration mode."""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     AIOS Microsoft Frontier Distillation Bridge - Interactive     ║
╠═══════════════════════════════════════════════════════════════════╣
║  Commands:                                                        ║
║    fetch [high|medium|low]  - Fetch RSS feeds                     ║
║    crystallize [n]          - Crystallize top N updates           ║
║    learn <url>              - Ingest Microsoft Learn path         ║
║    report                   - Generate summary report             ║
║    feeds                    - List configured feeds               ║
║    status                   - Show ingestion status               ║
║    quit                     - Exit                                ║
╚═══════════════════════════════════════════════════════════════════╝
""")
    
    while True:
        try:
            cmd = input("\n🔷 MSFT> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        
        if not cmd:
            continue
        
        parts = cmd.split()
        action = parts[0]
        
        if action == "quit":
            break
        
        elif action == "fetch":
            priority = parts[1] if len(parts) > 1 else None
            await bridge.fetch_all_feeds(priority)
        
        elif action == "crystallize":
            n = int(parts[1]) if len(parts) > 1 else 5
            for update in bridge.updates[:n]:
                await bridge.crystallize_update(update)
        
        elif action == "learn":
            if len(parts) > 1:
                await bridge.ingest_learn_path(parts[1])
            else:
                print("Usage: learn <url>")
        
        elif action == "report":
            bridge.generate_summary_report()
        
        elif action == "feeds":
            print("\nConfigured feeds:")
            for key, config in MSFT_FEEDS.items():
                print(f"  [{config['priority']}] {config['name']}: {config['category']}")
        
        elif action == "status":
            print(f"\nProcessed: {len(bridge.processed_hashes)} updates")
            print(f"Pending: {len(bridge.updates)} updates")
            print(f"Output: {bridge.output_dir}")
        
        else:
            print(f"Unknown command: {action}")
    
    print("\n👋 MSFT Bridge closing...")


if __name__ == "__main__":
    asyncio.run(main())
