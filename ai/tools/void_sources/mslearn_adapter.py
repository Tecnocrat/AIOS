"""
Microsoft Learn Adapter for VOID Bridge
========================================

Deep crawling adapter for Microsoft Learn structured courses.

AINLP.dendritic[void->mslearn{learning_path_url}]

Understands Microsoft Learn hierarchy:
- Learning Path → Modules → Units
- Extracts complete course structure
- Aggregates knowledge across all lessons

Usage:
    from void_sources.mslearn_adapter import MSLearnAdapter

    adapter = MSLearnAdapter()
    course = adapter.crawl_learning_path(
        "https://learn.microsoft.com/en-us/training/paths/..."
    )

    # Returns structured course with all units
    for module in course.modules:
        for unit in module.units:
            print(f"{unit.title}: {len(unit.content)} chars")
"""

import logging
import re
import time
import urllib.request
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urljoin, urlparse

logger = logging.getLogger("AIOS.VOID.MSLearn")


@dataclass
class MSLearnUnit:
    """A single lesson/unit within a module."""

    url: str
    title: str = ""
    order: int = 0
    content: str = ""
    duration_minutes: int = 0
    is_assessment: bool = False

    # Extracted knowledge
    key_concepts: list[str] = field(default_factory=list)
    code_samples: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "title": self.title,
            "order": self.order,
            "duration_minutes": self.duration_minutes,
            "is_assessment": self.is_assessment,
            "content_length": len(self.content),
            "key_concepts": self.key_concepts,
            "code_samples_count": len(self.code_samples),
        }


@dataclass
class MSLearnModule:
    """A module containing multiple units."""

    url: str
    title: str = ""
    description: str = ""
    order: int = 0
    units: list[MSLearnUnit] = field(default_factory=list)

    # Module metadata
    level: str = ""  # Beginner, Intermediate, Advanced
    duration_minutes: int = 0
    products: list[str] = field(default_factory=list)
    roles: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "order": self.order,
            "level": self.level,
            "duration_minutes": self.duration_minutes,
            "products": self.products,
            "roles": self.roles,
            "units": [u.to_dict() for u in self.units],
            "unit_count": len(self.units),
        }


@dataclass
class MSLearnPath:
    """A complete learning path with modules."""

    url: str
    title: str = ""
    description: str = ""
    modules: list[MSLearnModule] = field(default_factory=list)

    # Path metadata
    level: str = ""
    duration_minutes: int = 0
    products: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)

    # Aggregated content
    total_units: int = 0
    total_content_chars: int = 0

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "level": self.level,
            "duration_minutes": self.duration_minutes,
            "products": self.products,
            "prerequisites": self.prerequisites,
            "modules": [m.to_dict() for m in self.modules],
            "module_count": len(self.modules),
            "total_units": self.total_units,
            "total_content_chars": self.total_content_chars,
        }


class MSLearnAdapter:
    """
    Specialized adapter for Microsoft Learn deep crawling.

    Understands the hierarchical structure:
    Learning Path → Modules → Units

    Features:
    - Recursive crawling with rate limiting
    - Structure-aware extraction
    - Code sample detection
    - Assessment filtering
    - Aggregated crystallization
    """

    BASE_URL = "https://learn.microsoft.com"
    USER_AGENT = "AIOS-VOID-Bridge/1.0 (Knowledge Ingestion)"

    # Rate limiting
    REQUEST_DELAY = 0.5  # seconds between requests

    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self._last_request = 0

    def _fetch(self, url: str) -> str:
        """Fetch URL content with rate limiting."""
        # Rate limit
        elapsed = time.time() - self._last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        try:
            req = urllib.request.Request(url, headers={"User-Agent": self.USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as response:
                self._last_request = time.time()
                return response.read().decode("utf-8", errors="ignore")
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return ""

    def _extract_title(self, html: str) -> str:
        """Extract page title."""
        match = re.search(r"<title[^>]*>([^<]+)</title>", html, re.I)
        if match:
            title = match.group(1).strip()
            # Remove common suffixes
            title = re.sub(r"\s*[-|]\s*Training.*$", "", title)
            title = re.sub(r"\s*[-|]\s*Microsoft Learn.*$", "", title)
            return title.strip()
        return ""

    def _extract_description(self, html: str) -> str:
        """Extract meta description."""
        match = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html, re.I
        )
        return match.group(1).strip() if match else ""

    # UI noise patterns to filter out (Microsoft Learn specific)
    NOISE_PATTERNS = [
        # Language/action buttons
        r"Read in English",
        r"Add to (?:plan|collection|favorites?)",
        r"Add\s+Add",  # Duplicate button text
        r"Share via \w+",
        r"Copy link",
        r"Report an? issue",
        r"Edit this (?:page|document)",
        r"View all page feedback",
        r"Submit and view feedback",
        r"Is this page helpful\?",
        r"Yes\s+No",
        # Feedback sections (MSLearn specific) - match full sentences
        r"##\s*Feedback\s*",
        r"Was this page helpful\?\s*",
        r"Need help with this topic\?\s*",
        r"Want to try using Ask Learn[^\n]*",
        r"Ask Learn[^\n]*",
        r"^\s*No\s*$",  # Orphaned "No" from Yes/No button
        r"^\s*Yes\s*$",  # Orphaned "Yes" from Yes/No button
        # Navigation elements
        r"Previous\s*(?:unit|module|lesson)?",
        r"Next\s*(?:unit|module|lesson)?",
        r"Continue\s*$",
        r"Skip to main content",
        r"Skip navigation",
        r"Table of contents",
        r"In this (?:article|module|unit)",
        r"On this page",
        # Time metadata - only orphaned numbers
        r"^\s*-\s*\d+\s*(?:min|minutes?)\s*$",  # "- 2 minutes" alone
        r"Completed\s*\d*%?",
        r"Not started",
        r"In progress",
        # Cookie/consent noise
        r"(?:Accept|Reject|Manage)\s*(?:all\s*)?cookies?",
        r"Cookie\s*(?:policy|preferences|settings)",
        r"Privacy\s*(?:statement|policy)",
        # Footer/signup noise
        r"Sign (?:in|up|out)",
        r"Create (?:a\s*)?(?:free\s*)?account",
        r"(?:Subscribe|Sign up) (?:to|for)",
        r"Newsletter",
        r"© \d{4} Microsoft",
        r"All rights reserved",
        r"Terms of use",
        r"Trademarks",
        # Social/share
        r"Twitter|Facebook|LinkedIn|Reddit",
        r"Share this (?:article|page|content)",
        # Empty/structural
        r"^\s*#\s*$",  # Empty headers
        r"^\s*-\s*$",  # Empty list items
    ]

    def _clean_content(self, text: str) -> str:
        """Remove UI noise and produce pure knowledge content."""
        # Apply all noise filters (MULTILINE for ^ patterns)
        flags = re.IGNORECASE | re.MULTILINE
        for pattern in self.NOISE_PATTERNS:
            text = re.sub(pattern, "", text, flags=flags)

        # Clean up whitespace artifacts
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"^\s+", "", text, flags=re.MULTILINE)

        # Remove orphaned punctuation/symbols
        text = re.sub(r"^\s*[#\-\*]+\s*$", "", text, flags=re.MULTILINE)

        # Clean up list formatting
        text = re.sub(r"\n-\s*\n", "\n", text)

        return text.strip()

    def _extract_main_content(self, html: str) -> str:
        """Extract main content, stripping navigation/chrome."""
        # Try to find main content area
        patterns = [
            r"<main[^>]*>(.*?)</main>",
            r"<article[^>]*>(.*?)</article>",
            r'class="content"[^>]*>(.*?)</div>',
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL | re.I)
            if match:
                content = match.group(1)
                # Strip HTML structure that's definitely noise
                content = re.sub(r"<script[^>]*>.*?</script>", "", content, flags=re.DOTALL)
                content = re.sub(r"<style[^>]*>.*?</style>", "", content, flags=re.DOTALL)
                content = re.sub(r"<nav[^>]*>.*?</nav>", "", content, flags=re.DOTALL)
                content = re.sub(r"<header[^>]*>.*?</header>", "", content, flags=re.DOTALL)
                content = re.sub(r"<footer[^>]*>.*?</footer>", "", content, flags=re.DOTALL)
                content = re.sub(r"<aside[^>]*>.*?</aside>", "", content, flags=re.DOTALL)
                # Remove feedback/action buttons
                content = re.sub(
                    r'<(?:button|a)[^>]*class="[^"]*(?:feedback|action|button)[^"]*"[^>]*>.*?</(?:button|a)>',
                    "",
                    content,
                    flags=re.DOTALL | re.I,
                )
                # Convert headers to markdown-style
                content = re.sub(r"<h1[^>]*>([^<]+)</h1>", r"\n# \1\n", content)
                content = re.sub(r"<h2[^>]*>([^<]+)</h2>", r"\n## \1\n", content)
                content = re.sub(r"<h3[^>]*>([^<]+)</h3>", r"\n### \1\n", content)
                content = re.sub(r"<h4[^>]*>([^<]+)</h4>", r"\n#### \1\n", content)
                # Convert paragraph breaks
                content = re.sub(r"</p>", "\n\n", content)
                content = re.sub(r"<br\s*/?>", "\n", content)
                # Convert lists
                content = re.sub(r"<li[^>]*>", "\n- ", content)
                content = re.sub(r"</li>", "", content)
                # Strip remaining tags
                content = re.sub(r"<[^>]+>", " ", content)
                # Apply knowledge distillation
                content = self._clean_content(content)
                return content

        # Fallback: strip all HTML then clean
        text = re.sub(r"<[^>]+>", " ", html)
        return self._clean_content(text)

    def _extract_code_samples(self, html: str) -> list[str]:
        """Extract code blocks from content."""
        samples = []
        # Match <pre><code> blocks
        pattern = r"<pre[^>]*><code[^>]*>(.*?)</code></pre>"
        for match in re.finditer(pattern, html, re.DOTALL | re.I):
            code = match.group(1)
            # Decode HTML entities
            code = code.replace("&lt;", "<").replace("&gt;", ">")
            code = code.replace("&amp;", "&").replace("&quot;", '"')
            samples.append(code.strip())
        return samples

    def _extract_module_urls(self, html: str, base_url: str) -> list[str]:
        """Extract module URLs from a learning path page."""
        urls = []
        # Pattern for module links - multiple formats
        patterns = [
            # Full URLs
            r'href="(https://learn\.microsoft\.com[^"]*?/modules/[a-z0-9-]+/?)"',
            # Absolute paths
            r'href="(/en-us/training/modules/[a-z0-9-]+/?)"',
            # Relative paths (../../modules/xxx/)
            r'href="(\.\./\.\./modules/[a-z0-9-]+/?)"',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, html, re.I):
                path = match.group(1)

                # Resolve relative paths
                if path.startswith("../"):
                    # Convert ../../modules/xxx/ to full URL
                    module_name = re.search(r"modules/([a-z0-9-]+)", path)
                    if module_name:
                        full_url = (
                            f"{self.BASE_URL}/en-us/training/modules/" f"{module_name.group(1)}/"
                        )
                    else:
                        continue
                elif path.startswith("/"):
                    full_url = urljoin(self.BASE_URL, path)
                else:
                    full_url = path

                # Normalize: ensure trailing slash, no unit numbers
                full_url = full_url.rstrip("/") + "/"
                if re.search(r"/\d+-[^/]+/?$", full_url):
                    continue  # Skip unit URLs

                if full_url not in urls:
                    urls.append(full_url)

        return urls

    def _extract_unit_urls(self, html: str, base_url: str) -> list[str]:
        """Extract unit URLs from a module page."""
        urls = []
        # Units have relative hrefs like "3-what-cloud-compute"
        # Pattern: href="N-unit-name" where N is unit number
        pattern = r'href="(\d+-[a-z0-9-]+)"'

        for match in re.finditer(pattern, html, re.I):
            path = match.group(1)
            # Build full URL from module base
            full_url = base_url.rstrip("/") + "/" + path
            if full_url not in urls:
                urls.append(full_url)

        # Sort by unit number
        def unit_order(url):
            match = re.search(r"/(\d+)-", url)
            return int(match.group(1)) if match else 999

        return sorted(urls, key=unit_order)

    def crawl_unit(self, url: str, order: int = 0) -> MSLearnUnit:
        """Crawl a single unit/lesson."""
        logger.info(f"  📄 Unit {order}: {url.split('/')[-1]}")

        html = self._fetch(url)
        if not html:
            return MSLearnUnit(url=url, order=order)

        unit = MSLearnUnit(
            url=url,
            title=self._extract_title(html),
            order=order,
            content=self._extract_main_content(html),
            code_samples=self._extract_code_samples(html),
        )

        # Detect assessments
        if "knowledge-check" in url or "assessment" in url.lower():
            unit.is_assessment = True

        # Extract key concepts (headers and bold text)
        concepts = re.findall(r"<strong>([^<]+)</strong>", html)
        unit.key_concepts = list(set(concepts))[:20]  # Limit

        return unit

    def crawl_module(self, url: str, order: int = 0) -> MSLearnModule:
        """Crawl a module and all its units."""
        logger.info(f"📦 Module {order}: {url}")

        html = self._fetch(url)
        if not html:
            return MSLearnModule(url=url, order=order)

        module = MSLearnModule(
            url=url,
            title=self._extract_title(html),
            description=self._extract_description(html),
            order=order,
        )

        # Extract metadata
        if "Beginner" in html:
            module.level = "Beginner"
        elif "Intermediate" in html:
            module.level = "Intermediate"
        elif "Advanced" in html:
            module.level = "Advanced"

        # Find and crawl all units
        unit_urls = self._extract_unit_urls(html, url)
        logger.info(f"  Found {len(unit_urls)} units")

        for i, unit_url in enumerate(unit_urls, 1):
            unit = self.crawl_unit(unit_url, order=i)
            module.units.append(unit)
            module.duration_minutes += unit.duration_minutes

        return module

    def crawl_learning_path(
        self,
        url: str,
        max_modules: int = 50,
        skip_assessments: bool = False,
    ) -> MSLearnPath:
        """
        Crawl an entire learning path with all modules and units.

        Args:
            url: Learning path URL
            max_modules: Maximum modules to crawl (safety limit)
            skip_assessments: Skip knowledge check units

        Returns:
            MSLearnPath with complete structure
        """
        logger.info(f"🎓 Learning Path: {url}")

        html = self._fetch(url)
        if not html:
            return MSLearnPath(url=url)

        path = MSLearnPath(
            url=url,
            title=self._extract_title(html),
            description=self._extract_description(html),
        )

        # Extract metadata
        if "Beginner" in html:
            path.level = "Beginner"
        elif "Intermediate" in html:
            path.level = "Intermediate"
        elif "Advanced" in html:
            path.level = "Advanced"

        # Find all modules
        module_urls = self._extract_module_urls(html, url)
        logger.info(f"Found {len(module_urls)} modules")

        # Crawl each module (with limit)
        for i, module_url in enumerate(module_urls[:max_modules], 1):
            module = self.crawl_module(module_url, order=i)

            # Filter assessments if requested
            if skip_assessments:
                module.units = [u for u in module.units if not u.is_assessment]

            path.modules.append(module)
            path.duration_minutes += module.duration_minutes

        # Aggregate stats
        path.total_units = sum(len(m.units) for m in path.modules)
        path.total_content_chars = sum(len(u.content) for m in path.modules for u in m.units)

        logger.info(
            f"✅ Crawled: {len(path.modules)} modules, "
            f"{path.total_units} units, "
            f"{path.total_content_chars:,} chars"
        )

        return path

    def to_aggregated_markdown(self, path: MSLearnPath) -> str:
        """
        Convert entire learning path to aggregated markdown.

        Creates a comprehensive document with:
        - Course overview
        - Module summaries
        - All unit content
        - Code samples
        - Key concepts index
        """
        lines = [
            f"# {path.title}",
            "",
            f"**Source**: {path.url}",
            f"**Level**: {path.level}",
            f"**Modules**: {len(path.modules)}",
            f"**Total Units**: {path.total_units}",
            "",
            "## Overview",
            "",
            path.description,
            "",
            "---",
            "",
        ]

        # All key concepts across course
        all_concepts = set()
        all_code_samples = []

        for module in path.modules:
            lines.extend(
                [
                    f"# Module {module.order}: {module.title}",
                    "",
                    module.description,
                    "",
                ]
            )

            for unit in module.units:
                if unit.is_assessment:
                    continue  # Skip assessments in output

                lines.extend(
                    [
                        f"## {module.order}.{unit.order} {unit.title}",
                        "",
                        unit.content[:5000],  # Limit per unit
                        "",
                    ]
                )

                # Collect concepts and code
                all_concepts.update(unit.key_concepts)
                all_code_samples.extend(unit.code_samples)

            lines.append("---\n")

        # Appendix: Key Concepts
        if all_concepts:
            lines.extend(
                [
                    "# Key Concepts Index",
                    "",
                ]
            )
            for concept in sorted(all_concepts)[:50]:
                lines.append(f"- {concept}")
            lines.append("")

        # Appendix: Code Samples
        if all_code_samples:
            lines.extend(
                [
                    "# Code Samples",
                    "",
                ]
            )
            for i, code in enumerate(all_code_samples[:20], 1):
                lines.extend(
                    [
                        f"### Sample {i}",
                        "```",
                        code[:500],
                        "```",
                        "",
                    ]
                )

        return "\n".join(lines)


# =============================================================================
# CLI for standalone testing
# =============================================================================


def main():
    """CLI for testing MSLearn adapter."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Microsoft Learn Deep Crawler")
    parser.add_argument("url", help="Learning path or module URL")
    parser.add_argument("--output", "-o", help="Output file (markdown)")
    parser.add_argument("--json", action="store_true", help="Output as JSON structure")
    parser.add_argument(
        "--max-modules", "-m", type=int, default=10, help="Maximum modules to crawl"
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    adapter = MSLearnAdapter()

    # Detect if module or learning path
    if "/modules/" in args.url:
        module = adapter.crawl_module(args.url)
        result = module.to_dict()
        content = f"# {module.title}\n\n"
        for unit in module.units:
            content += f"## {unit.title}\n\n{unit.content[:2000]}\n\n"
    else:
        path = adapter.crawl_learning_path(args.url, max_modules=args.max_modules)
        result = path.to_dict()
        content = adapter.to_aggregated_markdown(path)

    if args.json:
        print(json.dumps(result, indent=2))
    elif args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved to {args.output}")
    else:
        print(content[:3000])
        print(f"\n... ({len(content):,} total chars)")


if __name__ == "__main__":
    main()
