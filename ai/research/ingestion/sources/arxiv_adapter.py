"""
ArXiv Source Adapter
====================

Multi-dimensional knowledge extraction from ArXiv papers.

AINLP.dendritic[void->arxiv{query}]

Handles:
- Paper metadata extraction
- Domain classification (cs, physics, math, bio, etc.)
- Citation network discovery (dendritic vertices)
- AIOS relevance scoring
"""

import json
import re
from dataclasses import dataclass, field
from typing import Any, Optional
from urllib.parse import urlparse

from .base import (
    ContentDimension,
    SourceAdapter,
    SourceMetadata,
    SourceType,
)


@dataclass
class ArxivPaper:
    """Structured representation of an ArXiv paper."""

    arxiv_id: str
    title: str
    authors: list[str] = field(default_factory=list)
    abstract: str = ""
    categories: list[str] = field(default_factory=list)
    primary_category: str = ""
    submitted_date: str = ""
    updated_date: str = ""
    doi: str = ""
    journal_ref: str = ""

    # Extracted content
    introduction: str = ""
    methodology: str = ""
    results: str = ""
    conclusion: str = ""

    # References (dendritic vertices)
    references: list[str] = field(default_factory=list)
    cited_arxiv_ids: list[str] = field(default_factory=list)


class ArxivAdapter(SourceAdapter):
    """
    Adapter for ArXiv paper ingestion.

    Extracts multi-dimensional knowledge from scientific papers:
    - Abstract dimension: High-level summary
    - Methodology dimension: Research methods
    - Results dimension: Findings
    - Citations dimension: Reference network
    """

    source_type = SourceType.ARXIV

    # ArXiv category to domain mapping
    domain_mapping = {
        # Computer Science
        "cs.AI": ("ai", "artificial_intelligence"),
        "cs.LG": ("ai", "machine_learning"),
        "cs.CL": ("ai", "natural_language"),
        "cs.CV": ("ai", "computer_vision"),
        "cs.MA": ("ai", "multi_agent"),
        "cs.NE": ("ai", "neural_evolution"),
        "cs.RO": ("ai", "robotics"),
        "cs.SE": ("software", "engineering"),
        "cs.DC": ("systems", "distributed"),
        "cs.PL": ("software", "programming_languages"),
        "cs.DB": ("data", "databases"),
        "cs.IR": ("data", "information_retrieval"),
        # Physics / Astronomy
        "astro-ph": ("physics", "astrophysics"),
        "astro-ph.GA": ("physics", "galaxies"),
        "astro-ph.CO": ("physics", "cosmology"),
        "cond-mat": ("physics", "condensed_matter"),
        "quant-ph": ("physics", "quantum"),
        "gr-qc": ("physics", "general_relativity"),
        "hep-th": ("physics", "high_energy_theory"),
        # Mathematics
        "math": ("mathematics", "general"),
        "math.CO": ("mathematics", "combinatorics"),
        "math.OC": ("mathematics", "optimization"),
        "stat.ML": ("statistics", "machine_learning"),
        # Biology
        "q-bio": ("biology", "general"),
        "q-bio.NC": ("biology", "neural_computation"),
    }

    # AIOS-relevant ArXiv keywords
    aios_arxiv_keywords = [
        # Multi-agent systems
        "multi-agent",
        "agent coordination",
        "agent communication",
        "emergent behavior",
        "swarm intelligence",
        "collective intelligence",
        # LLM/AI architecture
        "large language model",
        "transformer",
        "attention mechanism",
        "neural network architecture",
        "deep learning",
        "foundation model",
        # System design
        "distributed system",
        "microservices",
        "orchestration",
        "pipeline",
        "workflow",
        "architecture pattern",
        # Consciousness/Cognition (relevant to AIOS philosophy)
        "consciousness",
        "cognition",
        "self-organization",
        "emergence",
        "complexity",
        "information theory",
    ]

    def __init__(self):
        # Extend base AIOS keywords
        self.aios_keywords = self.aios_keywords + self.aios_arxiv_keywords

    def extract_arxiv_id(self, url: str) -> str:
        """Extract ArXiv ID from URL."""
        # Handle various ArXiv URL formats
        patterns = [
            r"arxiv\.org/abs/(\d+\.\d+)",
            r"arxiv\.org/html/(\d+\.\d+)",
            r"arxiv\.org/pdf/(\d+\.\d+)",
            r"arxiv:(\d+\.\d+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return ""

    def extract_metadata(self, url: str, content: str) -> SourceMetadata:
        """Extract paper metadata from ArXiv page."""

        arxiv_id = self.extract_arxiv_id(url)

        metadata = SourceMetadata(
            source_type=SourceType.ARXIV,
            url=url,
        )

        # Extract title
        title_match = re.search(
            r"<h1[^>]*class=\"[^\"]*title[^\"]*\"[^>]*>([^<]+)</h1>", content, re.IGNORECASE
        )
        if not title_match:
            title_match = re.search(r"<title[^>]*>([^<]+)</title>", content, re.IGNORECASE)

        if title_match:
            metadata.title = title_match.group(1).strip()
            # Clean up title
            metadata.title = re.sub(r"\s+", " ", metadata.title)
            metadata.title = metadata.title.replace(" - arXiv", "").strip()

        # Extract authors
        author_matches = re.findall(
            r'class="[^"]*author[^"]*"[^>]*>([^<]+)</a>', content, re.IGNORECASE
        )
        if author_matches:
            metadata.authors = [a.strip() for a in author_matches]

        # Extract abstract
        abstract_match = re.search(
            r'<blockquote[^>]*class="[^"]*abstract[^"]*"[^>]*>(.*?)</blockquote>',
            content,
            re.DOTALL | re.IGNORECASE,
        )
        if abstract_match:
            abstract = abstract_match.group(1)
            # Clean HTML
            abstract = re.sub(r"<[^>]+>", " ", abstract)
            abstract = re.sub(r"\s+", " ", abstract).strip()
            metadata.abstract = abstract

        # Extract categories/tags
        category_matches = re.findall(
            r'class="[^"]*primary-subject[^"]*"[^>]*>([^<]+)</span>', content, re.IGNORECASE
        )
        if not category_matches:
            category_matches = re.findall(r"\[([a-z-]+\.[A-Z]+)\]", content)

        if category_matches:
            metadata.tags = category_matches

        # Store arxiv_id in dimensions
        metadata.dimensions["arxiv_id"] = arxiv_id
        metadata.raw_content = content

        return metadata

    def extract_dimensions(self, content: str, metadata: SourceMetadata) -> dict[str, Any]:
        """
        Extract multi-dimensional knowledge surfaces from paper.

        Dimensions:
        - abstract: Paper summary
        - sections: Key sections (intro, methods, results, discussion)
        - figures: Figure/table information
        - equations: Mathematical formulations
        - code: Any code snippets
        - citations: Reference information
        """

        dimensions = metadata.dimensions.copy()

        # Abstract dimension
        dimensions[ContentDimension.ABSTRACT.value] = metadata.abstract

        # Try to extract sections
        sections = self._extract_sections(content)
        dimensions["sections"] = sections

        # Extract methodology keywords
        methodology_keywords = [
            "method",
            "approach",
            "algorithm",
            "model",
            "framework",
            "architecture",
            "design",
            "implementation",
            "technique",
        ]
        methodology_text = self._extract_section_by_keywords(content, methodology_keywords)
        dimensions[ContentDimension.METHODOLOGY.value] = methodology_text

        # Extract results/findings
        results_keywords = [
            "result",
            "finding",
            "performance",
            "evaluation",
            "experiment",
            "analysis",
            "comparison",
            "benchmark",
        ]
        results_text = self._extract_section_by_keywords(content, results_keywords)
        dimensions[ContentDimension.RESULTS.value] = results_text

        # Extract code snippets (if any)
        code_blocks = re.findall(r"<pre[^>]*>(.*?)</pre>", content, re.DOTALL | re.IGNORECASE)
        if code_blocks:
            dimensions[ContentDimension.CODE.value] = code_blocks[:5]  # Max 5

        # Key figures mentioned
        figure_refs = re.findall(r"Figure\s+(\d+)", content, re.IGNORECASE)
        if figure_refs:
            dimensions["figure_count"] = len(set(figure_refs))

        # Key equations mentioned
        equation_count = len(re.findall(r"\$[^$]+\$|\\\[.*?\\\]", content, re.DOTALL))
        dimensions["equation_count"] = equation_count

        return dimensions

    def _extract_sections(self, content: str) -> dict[str, str]:
        """Extract major sections from paper."""
        sections = {}

        # Try to find section headers
        section_patterns = [
            (r"##\s*(Introduction|Background)[^\n]*\n(.*?)(?=##|\Z)", "introduction"),
            (r"##\s*(Method|Approach|Model)[^\n]*\n(.*?)(?=##|\Z)", "methodology"),
            (r"##\s*(Result|Experiment|Evaluation)[^\n]*\n(.*?)(?=##|\Z)", "results"),
            (r"##\s*(Discussion|Analysis)[^\n]*\n(.*?)(?=##|\Z)", "discussion"),
            (r"##\s*(Conclusion|Summary)[^\n]*\n(.*?)(?=##|\Z)", "conclusion"),
        ]

        for pattern, section_name in section_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                text = match.group(2)
                # Clean HTML
                text = re.sub(r"<[^>]+>", " ", text)
                text = re.sub(r"\s+", " ", text).strip()
                sections[section_name] = text[:2000]  # Limit length

        return sections

    def _extract_section_by_keywords(self, content: str, keywords: list[str]) -> str:
        """Extract text around keyword occurrences."""
        extracted = []

        # Clean content for searching
        clean_content = re.sub(r"<[^>]+>", " ", content)
        clean_content = re.sub(r"\s+", " ", clean_content)

        for keyword in keywords:
            # Find sentences containing keyword
            pattern = rf"[^.]*\b{keyword}\b[^.]*\."
            matches = re.findall(pattern, clean_content, re.IGNORECASE)
            extracted.extend(matches[:3])  # Max 3 per keyword

        return " ".join(set(extracted))[:3000]  # Dedupe and limit

    def discover_related(self, content: str, metadata: SourceMetadata) -> list[str]:
        """
        Discover related papers (dendritic vertices).

        Extracts:
        - ArXiv IDs from references
        - Related paper links
        - Citation network
        """
        related = []

        # Find ArXiv references in content
        arxiv_refs = re.findall(r"arxiv[:\s]*(\d{4}\.\d{4,5})", content, re.IGNORECASE)
        for ref in arxiv_refs:
            related.append(f"https://arxiv.org/abs/{ref}")

        # Find explicit arxiv.org links
        arxiv_links = re.findall(r"https?://arxiv\.org/abs/(\d{4}\.\d{4,5})", content)
        for link in arxiv_links:
            url = f"https://arxiv.org/abs/{link}"
            if url not in related:
                related.append(url)

        # Extract DOI references (for cross-reference)
        doi_refs = re.findall(r"doi[:\s]*(10\.\d{4,}/[^\s<>\"]+)", content, re.IGNORECASE)
        for doi in doi_refs[:10]:  # Limit
            related.append(f"https://doi.org/{doi}")

        return list(set(related))[:20]  # Dedupe, limit to 20

    def classify_domain(self, content: str, metadata: SourceMetadata) -> tuple[str, str]:
        """Classify paper domain from ArXiv categories."""

        # Check tags first
        for tag in metadata.tags:
            for category, (domain, subdomain) in self.domain_mapping.items():
                if tag.startswith(category) or category in tag:
                    return domain, subdomain

        # Fallback: keyword-based classification
        text = f"{metadata.title} {metadata.abstract}".lower()

        # AI/ML detection
        ai_keywords = ["neural", "learning", "agent", "model", "transformer", "llm"]
        if any(kw in text for kw in ai_keywords):
            return "ai", "machine_learning"

        # Physics detection
        physics_keywords = ["galaxy", "stellar", "cosmic", "quantum", "particle"]
        if any(kw in text for kw in physics_keywords):
            return "physics", "general"

        return "general", ""

    def to_crystallized_markdown(self, metadata: SourceMetadata) -> str:
        """
        Convert extracted metadata to crystallized markdown.

        Enhanced format for ArXiv papers.
        """

        lines = [
            f"# {metadata.title}",
            "",
            f"**ArXiv ID**: {metadata.dimensions.get('arxiv_id', 'N/A')}",
            f"**Source**: {metadata.url}",
            f"**Authors**: {', '.join(metadata.authors) if metadata.authors else 'Unknown'}",
            f"**Domain**: {metadata.domain}/{metadata.subdomain}",
            f"**Tags**: {', '.join(metadata.tags) if metadata.tags else 'untagged'}",
            f"**AIOS Relevance**: {metadata.aios_relevance:.2f}",
            f"**Extracted**: {metadata.timestamp}",
            "",
            "---",
            "",
            "## Abstract",
            "",
            metadata.abstract or "No abstract available.",
            "",
        ]

        # Add methodology if available
        methodology = metadata.dimensions.get(ContentDimension.METHODOLOGY.value, "")
        if methodology:
            lines.extend(
                [
                    "## Methodology Highlights",
                    "",
                    methodology[:1500] + "..." if len(methodology) > 1500 else methodology,
                    "",
                ]
            )

        # Add results if available
        results = metadata.dimensions.get(ContentDimension.RESULTS.value, "")
        if results:
            lines.extend(
                [
                    "## Key Results",
                    "",
                    results[:1500] + "..." if len(results) > 1500 else results,
                    "",
                ]
            )

        # AIOS relevance analysis
        if metadata.aios_tags:
            lines.extend(
                [
                    "## AIOS Relevance Analysis",
                    "",
                    f"Matching concepts: {', '.join(metadata.aios_tags)}",
                    "",
                ]
            )

        # Related sources (dendritic vertices)
        if metadata.related_sources:
            lines.extend(
                [
                    "## Related Sources (Dendritic Vertices)",
                    "",
                ]
            )
            for ref in metadata.related_sources[:10]:
                lines.append(f"- {ref}")
            lines.append("")

        return "\n".join(lines)


# =============================================================================
# Utility Functions
# =============================================================================


def process_arxiv_url(url: str, content: str) -> tuple[SourceMetadata, str]:
    """
    Process an ArXiv URL and return metadata + crystallized content.

    Convenience function for VOID bridge integration.
    """
    adapter = ArxivAdapter()
    metadata = adapter.process(url, content)
    crystallized = adapter.to_crystallized_markdown(metadata)

    return metadata, crystallized
