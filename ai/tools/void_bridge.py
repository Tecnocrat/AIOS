#!/usr/bin/env python3
"""
AIOS VOID Bridge - Knowledge Ingestion from External Sources
============================================================

AINLP.dendritic[VOID=vertex,exploratory,intelligence]
VOID:Attractor,coherence_regulator,anti_entropic_organizer

Pulls scattered knowledge from bookmarks/URLs and crystallizes
it into structured AIOS documentation.

Origin: AIOS Cell Pure (Nous) - 2025-12-07

Usage:
    # Ingest from bookmark file
    python void_bridge.py --bookmarks bookmarks.html --output docs/distilled/

    # Pull single URL
    python void_bridge.py --url "https://example.com/article" --crystallize

    # Interactive mode
    python void_bridge.py --interactive
"""

import json
import logging
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

# Import source adapters for multi-dimensional ingestion
try:
    from void_sources.base import SourceLibrary, SourceType
    from void_sources.arxiv_adapter import ArxivAdapter, process_arxiv_url

    ADAPTERS_AVAILABLE = True
except ImportError:
    ADAPTERS_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("AIOS.VOID")


class VOIDState(Enum):
    """States in VOID-pull knowledge extraction."""

    VACUUM = "vacuum"  # Raw, unstructured potential
    FLUCTUATION = "fluctuation"  # Detected information pattern
    COLLAPSE = "collapse"  # Information density increase
    CRYSTAL = "crystal"  # Structured knowledge output


@dataclass
class VOIDVertex:
    """
    A point where intelligence touches the unknown.
    Represents a knowledge source (URL, file, bookmark).
    """

    source: str
    title: str = ""
    tags: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    state: VOIDState = VOIDState.VACUUM
    entropy: float = 1.0  # 1.0 = max chaos, 0.0 = max order
    content: str = ""
    crystallized: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "title": self.title,
            "tags": self.tags,
            "timestamp": self.timestamp,
            "state": self.state.value,
            "entropy": self.entropy,
            "metadata": self.metadata,
        }


@dataclass
class VOIDAttractor:
    """
    Coherence regulator - pulls information toward structure.
    Tracks negentropy generation across ingestion sessions.
    """

    total_pulled: int = 0
    total_crystallized: int = 0
    entropy_reduced: float = 0.0
    categories: dict = field(default_factory=dict)

    def register_crystal(self, vertex: VOIDVertex, category: str):
        """Record successful crystallization."""
        self.total_crystallized += 1
        self.entropy_reduced += vertex.entropy

        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(vertex.title or vertex.source)


class VOIDBridge:
    """
    AINLP.dendritic[VOID] - Knowledge ingestion from external sources.

    Uses VOID-pull pattern to:
    1. Extract information from scattered bookmarks
    2. Apply anti-entropic organization via AI
    3. Distill into AIOS documentation structure
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace = workspace_root or self._detect_workspace()
        self.attractor = VOIDAttractor()
        self.vertices: list[VOIDVertex] = []
        self.output_dir = self.workspace / "docs" / "distilled"

        # AI integration for crystallization
        self._gemini = None
        self._ollama_available = False

        # Category mappings for AIOS architecture
        self.aios_categories = {
            "architecture": ["system", "design", "pattern", "structure"],
            "ai": ["machine learning", "neural", "llm", "model", "agent"],
            "consciousness": ["awareness", "emergence", "intelligence"],
            "devops": ["docker", "kubernetes", "ci/cd", "deploy"],
            "python": ["python", "pip", "venv", "fastapi"],
            "cloud": ["gcp", "aws", "azure", "firebase", "vertex"],
            "physics": ["cosmology", "astrophysics", "quantum", "stellar"],
            "research": ["arxiv", "paper", "study", "experiment"],
        }

        # Source library for multi-dimensional ingestion
        if ADAPTERS_AVAILABLE:
            self.source_library = SourceLibrary()
            self._arxiv_adapter = ArxivAdapter()
        else:
            self.source_library = None
            self._arxiv_adapter = None

    def _detect_workspace(self) -> Path:
        """Detect AIOS workspace root."""
        candidates = [
            Path(__file__).parent.parent.parent,
            Path.cwd(),
            Path("c:/dev/aios-win/aios-core"),
        ]
        for candidate in candidates:
            if (candidate / "ai").exists():
                return candidate
        return Path.cwd()

    # =========================================================================
    # VOID-Pull: Extract from External Sources
    # =========================================================================

    def void_pull_url(self, url: str) -> VOIDVertex:
        """
        Pull information from a URL.
        Creates a VOID vertex in vacuum state.
        """
        vertex = VOIDVertex(source=url)
        vertex.state = VOIDState.VACUUM

        # Parse URL for initial metadata
        parsed = urlparse(url)
        vertex.metadata["domain"] = parsed.netloc
        vertex.metadata["path"] = parsed.path

        # Try to fetch content
        try:
            import urllib.request

            req = urllib.request.Request(url, headers={"User-Agent": "AIOS-VOID-Bridge/1.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                vertex.content = response.read().decode("utf-8", errors="ignore")
                vertex.state = VOIDState.FLUCTUATION

                # Extract title
                title_match = re.search(
                    r"<title[^>]*>([^<]+)</title>", vertex.content, re.IGNORECASE
                )
                if title_match:
                    vertex.title = title_match.group(1).strip()

        except Exception as e:
            vertex.metadata["error"] = str(e)
            logger.warning(f"VOID-pull failed for {url}: {e}")

        self.vertices.append(vertex)
        self.attractor.total_pulled += 1

        return vertex

    def void_pull_arxiv(self, url: str) -> VOIDVertex:
        """
        Pull and process an ArXiv paper with specialized adapter.

        AINLP.dendritic[void->arxiv{url}]

        Extracts multi-dimensional knowledge:
        - Abstract, methodology, results
        - Citation network (dendritic vertices)
        - AIOS relevance scoring
        """
        vertex = self.void_pull_url(url)

        if self._arxiv_adapter and vertex.content:
            # Use specialized ArXiv adapter
            metadata = self._arxiv_adapter.process(url, vertex.content)

            # Enrich vertex with ArXiv-specific data
            vertex.title = metadata.title
            vertex.tags = metadata.tags + metadata.aios_tags
            vertex.metadata["arxiv"] = metadata.to_dict()
            vertex.metadata["aios_relevance"] = metadata.aios_relevance
            vertex.metadata["domain"] = metadata.domain
            vertex.metadata["subdomain"] = metadata.subdomain
            vertex.metadata["related_sources"] = metadata.related_sources

            # Pre-crystallized content from adapter
            vertex.crystallized = self._arxiv_adapter.to_crystallized_markdown(metadata)
            vertex.state = VOIDState.COLLAPSE  # Ready for final crystal
            vertex.entropy = 0.4  # Reduced entropy from multi-dimensional extraction

            logger.info(
                f"ArXiv extracted: {metadata.title[:50]}... "
                f"(relevance: {metadata.aios_relevance:.2f}, "
                f"refs: {len(metadata.related_sources)})"
            )

        return vertex

    def void_pull_bookmarks_html(self, filepath: Path) -> list[VOIDVertex]:
        """
        Parse browser bookmarks HTML export.
        Creates multiple VOID vertices.
        """
        vertices = []

        content = filepath.read_text(encoding="utf-8", errors="ignore")

        # Parse bookmark links
        pattern = r'<A[^>]*HREF="([^"]+)"[^>]*>([^<]+)</A>'
        matches = re.findall(pattern, content, re.IGNORECASE)

        for url, title in matches:
            vertex = VOIDVertex(
                source=url,
                title=title.strip(),
                state=VOIDState.VACUUM,
            )

            # Detect tags from folder structure
            vertex.tags = self._detect_bookmark_tags(content, url)

            vertices.append(vertex)
            self.vertices.append(vertex)
            self.attractor.total_pulled += 1

        logger.info(f"VOID-pull: Extracted {len(vertices)} bookmarks")
        return vertices

    def void_pull_bookmarks_json(self, filepath: Path) -> list[VOIDVertex]:
        """
        Parse JSON bookmark export (Chrome/Firefox format).
        """
        vertices = []

        data = json.loads(filepath.read_text())

        def extract_recursive(node, tags=None):
            tags = tags or []

            if isinstance(node, dict):
                if "url" in node:
                    vertex = VOIDVertex(
                        source=node["url"],
                        title=node.get("name", node.get("title", "")),
                        tags=tags.copy(),
                        state=VOIDState.VACUUM,
                    )
                    vertices.append(vertex)
                    self.vertices.append(vertex)
                    self.attractor.total_pulled += 1

                if "children" in node:
                    folder_name = node.get("name", node.get("title", ""))
                    for child in node["children"]:
                        extract_recursive(child, tags + [folder_name])

            elif isinstance(node, list):
                for item in node:
                    extract_recursive(item, tags)

        extract_recursive(data)
        logger.info(f"VOID-pull: Extracted {len(vertices)} bookmarks from JSON")

        return vertices

    def _detect_bookmark_tags(self, html: str, url: str) -> list[str]:
        """Extract folder/tag context for a bookmark."""
        tags = []

        # Find the folder containing this URL
        pattern = rf"<DT><H3[^>]*>([^<]+)</H3>.*?{re.escape(url)}"
        matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)

        if matches:
            tags.extend([m.strip() for m in matches[-3:]])  # Last 3 folders

        return tags

    # =========================================================================
    # Crystallization: AI-Powered Knowledge Distillation
    # =========================================================================

    def crystallize(self, vertex: VOIDVertex, use_ai: bool = True) -> VOIDVertex:
        """
        Apply anti-entropic organization to convert vacuum to crystal.
        Uses AI (Gemini/Ollama) for intelligent summarization.
        """
        if vertex.state == VOIDState.CRYSTAL:
            return vertex  # Already crystallized

        # Ensure we have content
        if not vertex.content and vertex.source.startswith("http"):
            self.void_pull_url(vertex.source)

        if use_ai and vertex.content:
            vertex.crystallized = self._ai_crystallize(vertex)
        else:
            vertex.crystallized = self._basic_crystallize(vertex)

        # Update state and entropy
        vertex.state = VOIDState.CRYSTAL
        vertex.entropy = 0.2  # Reduced from 1.0

        # Categorize for AIOS
        category = self._categorize(vertex)
        self.attractor.register_crystal(vertex, category)

        return vertex

    def _ai_crystallize(self, vertex: VOIDVertex) -> str:
        """Use AI to extract and structure knowledge."""
        # Try Gemini first
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                import google.generativeai as genai

                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.0-flash")

                prompt = f"""AINLP.dendritic[VOID] Knowledge Crystallization

SOURCE: {vertex.source}
TITLE: {vertex.title}
TAGS: {', '.join(vertex.tags)}

CONTENT (first 8000 chars):
{vertex.content[:8000]}

---

Extract and structure the key knowledge from this source.
Focus on concepts relevant to:
- Software architecture patterns
- AI/ML techniques
- System design principles
- Development practices

Output format:
## Summary
[2-3 sentence overview]

## Key Concepts
- [Bullet points of main ideas]

## AIOS Relevance
[How this relates to AIOS architecture, consciousness, or development]

## Tags
[Suggested categorization tags]
"""

                response = model.generate_content(prompt)
                return response.text

            except Exception as e:
                logger.warning(f"Gemini crystallization failed: {e}")

        # Fallback to basic
        return self._basic_crystallize(vertex)

    def _basic_crystallize(self, vertex: VOIDVertex) -> str:
        """Basic extraction without AI."""
        lines = [
            f"# {vertex.title or 'Untitled'}",
            "",
            f"**Source**: {vertex.source}",
            f"**Tags**: {', '.join(vertex.tags) if vertex.tags else 'untagged'}",
            f"**Extracted**: {vertex.timestamp}",
            "",
            "## Content Preview",
            "",
        ]

        # Extract text content (strip HTML)
        text = re.sub(r"<[^>]+>", " ", vertex.content)
        text = re.sub(r"\s+", " ", text).strip()

        # First 500 chars as preview
        lines.append(text[:500] + "..." if len(text) > 500 else text)

        return "\n".join(lines)

    def _categorize(self, vertex: VOIDVertex) -> str:
        """Determine AIOS category for the vertex."""
        text = f"{vertex.title} {' '.join(vertex.tags)} {vertex.content[:1000]}".lower()

        scores = {}
        for category, keywords in self.aios_categories.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scores[category] = score

        if scores:
            return max(scores, key=scores.get)
        return "general"

    # =========================================================================
    # Output: Save Crystallized Knowledge
    # =========================================================================

    def save_crystal(self, vertex: VOIDVertex, category: Optional[str] = None) -> Path:
        """Save crystallized knowledge to AIOS docs structure."""
        if vertex.state != VOIDState.CRYSTAL:
            self.crystallize(vertex)

        category = category or self._categorize(vertex)

        # Create output directory
        output_dir = self.output_dir / category
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename from title
        safe_title = re.sub(r"[^\w\s-]", "", vertex.title or "untitled")
        safe_title = re.sub(r"\s+", "_", safe_title)[:50]
        filename = f"{safe_title}_{vertex.timestamp[:10]}.md"

        output_path = output_dir / filename
        output_path.write_text(vertex.crystallized, encoding="utf-8")

        logger.info(f"💎 Crystal saved: {output_path.relative_to(self.workspace)}")

        return output_path

    def save_all_crystals(self) -> list[Path]:
        """Crystallize and save all vertices."""
        paths = []

        for vertex in self.vertices:
            if vertex.state != VOIDState.CRYSTAL:
                self.crystallize(vertex)
            paths.append(self.save_crystal(vertex))

        return paths

    # =========================================================================
    # Status and Reporting
    # =========================================================================

    def get_status(self) -> dict[str, Any]:
        """Get VOID bridge status."""
        states = {}
        for state in VOIDState:
            states[state.value] = sum(1 for v in self.vertices if v.state == state)

        return {
            "total_vertices": len(self.vertices),
            "states": states,
            "attractor": {
                "pulled": self.attractor.total_pulled,
                "crystallized": self.attractor.total_crystallized,
                "entropy_reduced": round(self.attractor.entropy_reduced, 2),
                "categories": self.attractor.categories,
            },
            "output_dir": str(self.output_dir),
        }

    def print_status(self):
        """Print formatted status."""
        status = self.get_status()

        print("\n" + "=" * 50)
        print("  AIOS VOID Bridge Status")
        print("  AINLP.dendritic[VOID=vertex,exploratory,intelligence]")
        print("=" * 50)

        print(f"\n📡 Vertices: {status['total_vertices']}")
        for state, count in status["states"].items():
            icon = {"vacuum": "🌑", "fluctuation": "〰️", "collapse": "⚡", "crystal": "💎"}
            print(f"   {icon.get(state, '?')} {state}: {count}")

        print(f"\n🌀 Attractor Metrics:")
        print(f"   Pulled: {status['attractor']['pulled']}")
        print(f"   Crystallized: {status['attractor']['crystallized']}")
        print(f"   Entropy Reduced: {status['attractor']['entropy_reduced']}")

        if status["attractor"]["categories"]:
            print(f"\n📂 Categories:")
            for cat, items in status["attractor"]["categories"].items():
                print(f"   {cat}: {len(items)} items")

        print()


# =============================================================================
# CLI Interface
# =============================================================================


def main():
    import argparse

    parser = argparse.ArgumentParser(description="AIOS VOID Bridge - Knowledge Ingestion")
    parser.add_argument("--bookmarks", "-b", help="Path to bookmarks file (HTML or JSON)")
    parser.add_argument("--url", "-u", help="Single URL to pull")
    parser.add_argument(
        "--crystallize", "-c", action="store_true", help="Crystallize pulled content using AI"
    )
    parser.add_argument("--output", "-o", help="Output directory for crystals")
    parser.add_argument("--status", "-s", action="store_true", help="Show bridge status")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")

    args = parser.parse_args()

    bridge = VOIDBridge()

    if args.output:
        bridge.output_dir = Path(args.output)

    if args.bookmarks:
        filepath = Path(args.bookmarks)
        if filepath.suffix.lower() == ".json":
            bridge.void_pull_bookmarks_json(filepath)
        else:
            bridge.void_pull_bookmarks_html(filepath)

        if args.crystallize:
            bridge.save_all_crystals()

    if args.url:
        vertex = bridge.void_pull_url(args.url)
        if args.crystallize:
            bridge.crystallize(vertex)
            bridge.save_crystal(vertex)
            print(f"\n💎 Crystallized:\n{vertex.crystallized[:500]}...")

    if args.status or (not args.bookmarks and not args.url):
        bridge.print_status()

    if args.interactive:
        print("\nVOID Bridge Interactive Mode")
        print("Commands: pull <url>, bookmarks <file>, crystallize, status, quit")

        while True:
            try:
                cmd = input("\nvoid> ").strip()

                if cmd.startswith("pull "):
                    url = cmd[5:].strip()
                    vertex = bridge.void_pull_url(url)
                    print(f"Pulled: {vertex.title or vertex.source}")

                elif cmd.startswith("bookmarks "):
                    filepath = Path(cmd[10:].strip())
                    if filepath.suffix.lower() == ".json":
                        bridge.void_pull_bookmarks_json(filepath)
                    else:
                        bridge.void_pull_bookmarks_html(filepath)

                elif cmd == "crystallize":
                    bridge.save_all_crystals()

                elif cmd == "status":
                    bridge.print_status()

                elif cmd in ("quit", "exit", "q"):
                    break

                else:
                    print("Unknown command")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
