"""
AIOS Knowledge Ingestion - Output Generation
============================================

AINLP.dendritic[ai/ingestion/output]{markdown,json,index,master}

Output generators for knowledge items.
Creates markdown indexes, JSON databases, and master catalogs.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .protocol import KnowledgeItem, IngestionResult

logger = logging.getLogger("AIOS.KIP.Output")


class OutputGenerator:
    """
    Generate output files from ingested knowledge.

    Supports:
    - Per-category JSON indexes
    - Per-category markdown READMEs
    - Master index across all providers
    - Combined JSON database
    """

    def __init__(self, output_dir: Path):
        """
        Initialize output generator.

        Args:
            output_dir: Base output directory (e.g., docs/distilled/)
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_category_index(
        self,
        provider: str,
        category: str,
        items: list[KnowledgeItem],
    ) -> Path:
        """
        Write category-specific index files.

        Creates:
        - {provider}/{category}/index.json
        - {provider}/{category}/README.md
        """
        cat_dir = self.output_dir / provider / category
        cat_dir.mkdir(parents=True, exist_ok=True)

        # JSON index
        json_path = cat_dir / "index.json"
        json_data = [item.to_dict() for item in items]
        json_path.write_text(
            json.dumps(json_data, indent=2),
            encoding="utf-8"
        )

        # Markdown README
        md_path = cat_dir / "README.md"
        md_content = self._generate_category_markdown(
            provider, category, items
        )
        md_path.write_text(md_content, encoding="utf-8")

        logger.info(f"Wrote {len(items)} items to {cat_dir}")
        return cat_dir

    def write_provider_index(
        self,
        provider: str,
        results: list[IngestionResult],
    ) -> Path:
        """
        Write provider-level index.

        Creates:
        - {provider}/KNOWLEDGE_BASE.md
        - {provider}/all_articles.json
        """
        provider_dir = self.output_dir / provider
        provider_dir.mkdir(parents=True, exist_ok=True)

        # Collect all items by category
        by_category: dict[str, list[KnowledgeItem]] = {}
        all_items: list[KnowledgeItem] = []

        for result in results:
            for item in result.items:
                cat = item.category or "uncategorized"
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(item)
                all_items.append(item)

        # Write category indexes
        for category, items in by_category.items():
            self.write_category_index(provider, category, items)

        # Combined JSON
        json_path = provider_dir / "all_articles.json"
        json_data = [item.to_dict() for item in all_items]
        json_path.write_text(
            json.dumps(json_data, indent=2),
            encoding="utf-8"
        )

        # Master markdown
        md_path = provider_dir / "KNOWLEDGE_BASE.md"
        md_content = self._generate_provider_markdown(
            provider, by_category
        )
        md_path.write_text(md_content, encoding="utf-8")

        logger.info(f"Wrote provider index: {provider_dir}")
        return provider_dir

    def write_master_index(
        self,
        all_results: dict[str, list[IngestionResult]],
    ) -> Path:
        """
        Write master index across all providers.

        Creates:
        - MASTER_INDEX.md
        - master_database.json
        """
        # Collect stats
        stats: dict[str, dict] = {}
        all_items: list[dict] = []

        for provider, results in all_results.items():
            provider_items = []
            for result in results:
                provider_items.extend(result.items)
                all_items.extend([item.to_dict() for item in result.items])

            stats[provider] = {
                "sources": len(results),
                "items": len(provider_items),
            }

        # Write master JSON
        json_path = self.output_dir / "master_database.json"
        json_path.write_text(
            json.dumps({
                "metadata": {
                    "generated": datetime.now(timezone.utc).isoformat(),
                    "total_items": len(all_items),
                    "providers": list(stats.keys()),
                },
                "items": all_items,
            }, indent=2),
            encoding="utf-8"
        )

        # Write master markdown
        md_path = self.output_dir / "MASTER_INDEX.md"
        md_content = self._generate_master_markdown(stats, all_results)
        md_path.write_text(md_content, encoding="utf-8")

        logger.info(f"Wrote master index: {len(all_items)} total items")
        return self.output_dir

    def _generate_category_markdown(
        self,
        provider: str,
        category: str,
        items: list[KnowledgeItem],
    ) -> str:
        """Generate markdown for a category."""
        title = category.replace("_", " ").title()
        lines = [
            f"# {title}",
            "",
            f"> **Provider**: {provider}",
            f"> **Articles**: {len(items)}",
            f"> **Updated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
            "",
            "---",
            "",
        ]

        for item in items:
            lines.append(f"- [{item.title}]({item.url}) - {item.source_name}")

        lines.extend([
            "",
            "---",
            "",
            "*Generated by AIOS Knowledge Ingestion Protocol*",
        ])

        return "\n".join(lines)

    def _generate_provider_markdown(
        self,
        provider: str,
        by_category: dict[str, list[KnowledgeItem]],
    ) -> str:
        """Generate markdown for a provider."""
        total = sum(len(items) for items in by_category.values())
        title = provider.title()

        lines = [
            f"# {title} Knowledge Base",
            "",
            f"> **Total Articles**: {total}",
            f"> **Categories**: {len(by_category)}",
            f"> **Updated**: {datetime.now(timezone.utc).isoformat()}",
            "> **AINLP.dendritic**: Knowledge archive",
            "",
            "---",
            "",
            "## Quick Stats",
            "",
            "| Category | Articles |",
            "|----------|----------|",
        ]

        for cat, items in sorted(by_category.items()):
            cat_name = cat.replace("_", " ").title()
            lines.append(f"| {cat_name} | {len(items)} |")

        lines.extend(["", "---", ""])

        # Category sections
        for cat, items in sorted(by_category.items()):
            cat_name = cat.replace("_", " ").title()
            lines.append(f"## {cat_name}")
            lines.append("")
            for item in items[:15]:  # Limit per category
                lines.append(f"- [{item.title}]({item.url})")
            if len(items) > 15:
                lines.append(f"- *...and {len(items) - 15} more*")
            lines.append("")

        lines.extend([
            "---",
            "",
            "*Generated by AIOS Knowledge Ingestion Protocol*",
        ])

        return "\n".join(lines)

    def _generate_master_markdown(
        self,
        stats: dict[str, dict],
        all_results: dict[str, list[IngestionResult]],
    ) -> str:
        """Generate master index markdown."""
        total_items = sum(s["items"] for s in stats.values())
        total_sources = sum(s["sources"] for s in stats.values())

        lines = [
            "# AIOS Knowledge Master Index",
            "",
            f"> **Total Items**: {total_items}",
            f"> **Providers**: {len(stats)}",
            f"> **Sources**: {total_sources}",
            f"> **Generated**: {datetime.now(timezone.utc).isoformat()}",
            "",
            "---",
            "",
            "## Providers",
            "",
            "| Provider | Sources | Items |",
            "|----------|---------|-------|",
        ]

        for provider, s in sorted(stats.items()):
            lines.append(f"| [{provider}]({provider}/) | {s['sources']} | {s['items']} |")

        lines.extend([
            "",
            "---",
            "",
            "## Recent Items",
            "",
        ])

        # Show recent items from each provider
        for provider, results in all_results.items():
            lines.append(f"### {provider.title()}")
            lines.append("")
            recent = []
            for result in results:
                recent.extend(result.items[:3])
            for item in recent[:5]:
                lines.append(f"- [{item.title}]({item.url})")
            lines.append("")

        lines.extend([
            "---",
            "",
            "*AIOS Knowledge Ingestion Protocol*",
        ])

        return "\n".join(lines)
