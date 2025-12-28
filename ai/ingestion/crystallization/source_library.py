"""
VOID Source Classification Library
===================================

Categorized website patterns for agentic ingestion.

Pattern: AINLP.dendritic[void->source_type{query}]

Examples:
    AINLP.dendritic[void->arxiv{"multi-agent systems"}]
    AINLP.dendritic[void->github{"llm orchestration"}]
    AINLP.dendritic[void->docs{"fastapi tutorial"}]
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("AIOS.VOID.Library")


class SourceCategory(Enum):
    """High-level source categories."""

    SCIENTIFIC = "scientific"  # Academic papers, research
    CODE = "code"  # Repositories, snippets
    DOCUMENTATION = "documentation"  # Technical docs
    NEWS = "news"  # News, blogs
    REFERENCE = "reference"  # Wikipedia, encyclopedias
    MEDIA = "media"  # Videos, podcasts


@dataclass
class SourcePattern:
    """
    A source pattern definition for VOID ingestion.

    Defines how to detect, extract, and categorize a source type.
    """

    # Pattern identification
    pattern_id: str  # e.g., "arxiv", "github", "pytorch-docs"
    name: str  # Human-readable name
    category: SourceCategory

    # URL detection
    url_patterns: list[str]  # Regex patterns to match URLs
    domain_patterns: list[str]  # Domain patterns (e.g., "arxiv.org")

    # Search/query patterns
    search_url_template: str = ""  # Template for search queries
    api_endpoint: str = ""  # API endpoint if available

    # Extraction configuration
    adapter_class: str = ""  # Adapter class name
    requires_auth: bool = False  # Needs API key
    rate_limit: int = 10  # Requests per minute

    # Multi-agent configuration
    supports_multi_agent: bool = False
    recommended_workers: int = 1
    max_depth: int = 1

    # AIOS relevance hints
    aios_relevant_keywords: list[str] = field(default_factory=list)
    default_relevance: float = 0.5

    # Metadata
    description: str = ""
    examples: list[str] = field(default_factory=list)

    def matches_url(self, url: str) -> bool:
        """Check if URL matches this pattern."""
        import re

        for pattern in self.url_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return True

        for domain in self.domain_patterns:
            if domain in url:
                return True

        return False

    def get_search_url(self, query: str) -> str:
        """Generate search URL from query."""
        if not self.search_url_template:
            return ""
        return self.search_url_template.format(query=query)

    def to_ainlp_pattern(self, query: str = "") -> str:
        """Generate AINLP dendritic pattern string."""
        return f'AINLP.dendritic[void->{self.pattern_id}{{"{query}"}}]'


class SourceLibrary:
    """
    Library of source patterns for intelligent ingestion.

    Provides:
    - Pattern matching: Detect source type from URL
    - Search generation: Create search URLs for queries
    - Multi-agent config: Get ingestion configuration
    - AINLP patterns: Generate dendritic pattern strings
    """

    def __init__(self, library_path: Optional[Path] = None):
        self.patterns: dict[str, SourcePattern] = {}
        self.library_path = library_path

        # Register built-in patterns
        self._register_builtins()

        # Load custom patterns from file if provided
        if library_path and library_path.exists():
            self._load_from_file(library_path)

    def _register_builtins(self):
        """Register built-in source patterns."""

        # =====================================================================
        # SCIENTIFIC SOURCES
        # =====================================================================

        self.register(
            SourcePattern(
                pattern_id="arxiv",
                name="ArXiv Papers",
                category=SourceCategory.SCIENTIFIC,
                url_patterns=[r"arxiv\.org/(abs|html|pdf)/\d+\.\d+"],
                domain_patterns=["arxiv.org"],
                search_url_template="https://arxiv.org/search/?query={query}&searchtype=all",
                adapter_class="ArxivAdapter",
                supports_multi_agent=True,
                recommended_workers=3,
                max_depth=2,
                aios_relevant_keywords=[
                    "agent",
                    "multi-agent",
                    "llm",
                    "transformer",
                    "neural",
                    "architecture",
                    "system",
                    "distributed",
                    "coordination",
                ],
                default_relevance=0.6,
                description="ArXiv preprint server for scientific papers",
                examples=[
                    "https://arxiv.org/abs/2303.08774",  # GPT-4 paper
                    "https://arxiv.org/abs/2305.10601",  # Gorilla
                ],
            )
        )

        self.register(
            SourcePattern(
                pattern_id="arxiv-cs",
                name="ArXiv Computer Science",
                category=SourceCategory.SCIENTIFIC,
                url_patterns=[r"arxiv\.org.*cs\.\w+"],
                domain_patterns=[],
                search_url_template="https://arxiv.org/search/?query={query}&searchtype=all&abstracts=show&source=header&category=cs.*",
                adapter_class="ArxivAdapter",
                supports_multi_agent=True,
                recommended_workers=5,
                max_depth=2,
                aios_relevant_keywords=["algorithm", "machine learning", "deep learning"],
                default_relevance=0.8,
                description="ArXiv Computer Science papers",
            )
        )

        self.register(
            SourcePattern(
                pattern_id="arxiv-ai",
                name="ArXiv AI/ML Papers",
                category=SourceCategory.SCIENTIFIC,
                url_patterns=[r"arxiv\.org.*(cs\.AI|cs\.LG|cs\.CL|cs\.MA)"],
                domain_patterns=[],
                search_url_template="https://arxiv.org/search/?query={query}&searchtype=all&abstracts=show&category=cs.AI+cs.LG+cs.CL+cs.MA",
                adapter_class="ArxivAdapter",
                supports_multi_agent=True,
                recommended_workers=5,
                max_depth=3,
                aios_relevant_keywords=[
                    "large language model",
                    "agent",
                    "reasoning",
                    "planning",
                    "multi-agent",
                    "coordination",
                    "emergence",
                ],
                default_relevance=0.95,
                description="ArXiv AI and Machine Learning papers",
            )
        )

        self.register(
            SourcePattern(
                pattern_id="semantic-scholar",
                name="Semantic Scholar",
                category=SourceCategory.SCIENTIFIC,
                url_patterns=[r"semanticscholar\.org/paper"],
                domain_patterns=["semanticscholar.org"],
                api_endpoint="https://api.semanticscholar.org/v1/paper/",
                description="Academic paper search with citation graph",
            )
        )

        # =====================================================================
        # CODE SOURCES
        # =====================================================================

        self.register(
            SourcePattern(
                pattern_id="github",
                name="GitHub",
                category=SourceCategory.CODE,
                url_patterns=[r"github\.com/[\w-]+/[\w-]+"],
                domain_patterns=["github.com"],
                search_url_template="https://github.com/search?q={query}&type=repositories",
                adapter_class="GithubAdapter",
                supports_multi_agent=True,
                recommended_workers=3,
                max_depth=1,
                aios_relevant_keywords=[
                    "agent",
                    "llm",
                    "framework",
                    "orchestration",
                    "pipeline",
                    "langchain",
                    "autogen",
                    "crewai",
                ],
                default_relevance=0.7,
                description="GitHub repositories and code",
            )
        )

        self.register(
            SourcePattern(
                pattern_id="huggingface",
                name="Hugging Face",
                category=SourceCategory.CODE,
                url_patterns=[r"huggingface\.co/([\w-]+/)?[\w-]+"],
                domain_patterns=["huggingface.co"],
                search_url_template="https://huggingface.co/models?search={query}",
                aios_relevant_keywords=["model", "transformer", "embedding", "tokenizer"],
                default_relevance=0.85,
                description="Hugging Face models and datasets",
            )
        )

        # =====================================================================
        # DOCUMENTATION SOURCES
        # =====================================================================

        self.register(
            SourcePattern(
                pattern_id="mslearn",
                name="Microsoft Learn",
                category=SourceCategory.DOCUMENTATION,
                url_patterns=[
                    r"learn\.microsoft\.com/en-us/training/paths/",
                    r"learn\.microsoft\.com/en-us/training/modules/",
                ],
                domain_patterns=["learn.microsoft.com"],
                search_url_template="https://learn.microsoft.com/en-us/search/?terms={query}&category=Learn",
                adapter_class="MSLearnAdapter",
                supports_multi_agent=True,
                recommended_workers=3,
                max_depth=3,  # Path → Module → Unit
                aios_relevant_keywords=[
                    "azure",
                    "cloud",
                    "architecture",
                    "devops",
                    "ai",
                    "machine learning",
                    "container",
                    "kubernetes",
                    "serverless",
                ],
                default_relevance=0.8,
                description="Microsoft Learn training paths and modules",
                examples=[
                    "https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/",
                    "https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/",
                ],
            )
        )

        self.register(
            SourcePattern(
                pattern_id="azure-docs",
                name="Azure Documentation",
                category=SourceCategory.DOCUMENTATION,
                url_patterns=[r"learn\.microsoft\.com/en-us/azure/"],
                domain_patterns=[],
                search_url_template="https://learn.microsoft.com/en-us/search/?terms={query}&scope=Azure",
                adapter_class="MSLearnAdapter",
                supports_multi_agent=True,
                max_depth=2,
                aios_relevant_keywords=[
                    "azure",
                    "cloud",
                    "service",
                    "deployment",
                    "resource",
                ],
                default_relevance=0.75,
                description="Azure technical documentation",
            )
        )

        self.register(
            SourcePattern(
                pattern_id="python-docs",
                name="Python Documentation",
                category=SourceCategory.DOCUMENTATION,
                url_patterns=[r"docs\.python\.org"],
                domain_patterns=["docs.python.org"],
                search_url_template="https://docs.python.org/3/search.html?q={query}",
                description="Official Python documentation",
            )
        )

        self.register(
            SourcePattern(
                pattern_id="pytorch-docs",
                name="PyTorch Documentation",
                category=SourceCategory.DOCUMENTATION,
                url_patterns=[r"pytorch\.org/docs"],
                domain_patterns=["pytorch.org/docs"],
                search_url_template="https://pytorch.org/docs/stable/search.html?q={query}",
                aios_relevant_keywords=["tensor", "neural", "training", "model"],
                default_relevance=0.75,
                description="PyTorch deep learning documentation",
            )
        )

        self.register(
            SourcePattern(
                pattern_id="langchain-docs",
                name="LangChain Documentation",
                category=SourceCategory.DOCUMENTATION,
                url_patterns=[r"python\.langchain\.com"],
                domain_patterns=["python.langchain.com"],
                aios_relevant_keywords=[
                    "agent",
                    "chain",
                    "llm",
                    "retrieval",
                    "tool",
                    "memory",
                    "prompt",
                    "callback",
                ],
                default_relevance=0.95,
                description="LangChain framework documentation",
            )
        )

        self.register(
            SourcePattern(
                pattern_id="openai-docs",
                name="OpenAI Documentation",
                category=SourceCategory.DOCUMENTATION,
                url_patterns=[r"platform\.openai\.com"],
                domain_patterns=["platform.openai.com"],
                aios_relevant_keywords=["api", "gpt", "chat", "completion", "embedding"],
                default_relevance=0.9,
                description="OpenAI API documentation",
            )
        )

        # =====================================================================
        # REFERENCE SOURCES
        # =====================================================================

        self.register(
            SourcePattern(
                pattern_id="wikipedia",
                name="Wikipedia",
                category=SourceCategory.REFERENCE,
                url_patterns=[r"(en\.)?wikipedia\.org/wiki/"],
                domain_patterns=["wikipedia.org"],
                search_url_template="https://en.wikipedia.org/w/index.php?search={query}",
                supports_multi_agent=True,
                recommended_workers=2,
                max_depth=2,
                description="Wikipedia encyclopedia",
            )
        )

        # =====================================================================
        # NEWS/BLOG SOURCES
        # =====================================================================

        self.register(
            SourcePattern(
                pattern_id="medium",
                name="Medium",
                category=SourceCategory.NEWS,
                url_patterns=[r"medium\.com/@?[\w-]+/[\w-]+"],
                domain_patterns=["medium.com", "towardsdatascience.com"],
                description="Medium blog posts",
            )
        )

        self.register(
            SourcePattern(
                pattern_id="hacker-news",
                name="Hacker News",
                category=SourceCategory.NEWS,
                url_patterns=[r"news\.ycombinator\.com"],
                domain_patterns=["news.ycombinator.com"],
                search_url_template="https://hn.algolia.com/?q={query}",
                description="Hacker News discussions",
            )
        )

    def register(self, pattern: SourcePattern):
        """Register a source pattern."""
        self.patterns[pattern.pattern_id] = pattern

    def detect(self, url: str) -> Optional[SourcePattern]:
        """Detect source type from URL."""
        for pattern in self.patterns.values():
            if pattern.matches_url(url):
                return pattern
        return None

    def get(self, pattern_id: str) -> Optional[SourcePattern]:
        """Get pattern by ID."""
        return self.patterns.get(pattern_id)

    def search(self, query: str, pattern_id: str = "arxiv-ai") -> str:
        """
        Generate AINLP dendritic pattern for search.

        Returns: AINLP.dendritic[void->pattern{"query"}]
        """
        pattern = self.get(pattern_id)
        if pattern:
            return pattern.to_ainlp_pattern(query)
        return f'AINLP.dendritic[void->generic{{"{query}"}}]'

    def get_search_url(self, query: str, pattern_id: str) -> str:
        """Get actual search URL for a query."""
        pattern = self.get(pattern_id)
        if pattern:
            return pattern.get_search_url(query)
        return ""

    def list_patterns(self, category: Optional[SourceCategory] = None) -> list[str]:
        """List registered patterns, optionally filtered by category."""
        if category:
            return [p.pattern_id for p in self.patterns.values() if p.category == category]
        return list(self.patterns.keys())

    def get_multi_agent_config(self, pattern_id: str) -> dict:
        """Get multi-agent configuration for a pattern."""
        pattern = self.get(pattern_id)
        if not pattern:
            return {"supports_multi_agent": False, "recommended_workers": 1, "max_depth": 1}

        return {
            "supports_multi_agent": pattern.supports_multi_agent,
            "recommended_workers": pattern.recommended_workers,
            "max_depth": pattern.max_depth,
            "aios_relevant_keywords": pattern.aios_relevant_keywords,
            "default_relevance": pattern.default_relevance,
        }

    def _load_from_file(self, path: Path):
        """Load custom patterns from JSON file."""
        try:
            data = json.loads(path.read_text())
            for item in data.get("patterns", []):
                pattern = SourcePattern(
                    pattern_id=item["pattern_id"],
                    name=item["name"],
                    category=SourceCategory(item["category"]),
                    url_patterns=item.get("url_patterns", []),
                    domain_patterns=item.get("domain_patterns", []),
                    search_url_template=item.get("search_url_template", ""),
                    adapter_class=item.get("adapter_class", ""),
                    supports_multi_agent=item.get("supports_multi_agent", False),
                    recommended_workers=item.get("recommended_workers", 1),
                    max_depth=item.get("max_depth", 1),
                    aios_relevant_keywords=item.get("aios_relevant_keywords", []),
                    default_relevance=item.get("default_relevance", 0.5),
                    description=item.get("description", ""),
                )
                self.register(pattern)
        except Exception as e:
            logger.warning(f"Failed to load custom patterns: {e}")

    def save_to_file(self, path: Path):
        """Save patterns to JSON file."""
        data = {
            "patterns": [
                {
                    "pattern_id": p.pattern_id,
                    "name": p.name,
                    "category": p.category.value,
                    "url_patterns": p.url_patterns,
                    "domain_patterns": p.domain_patterns,
                    "search_url_template": p.search_url_template,
                    "adapter_class": p.adapter_class,
                    "supports_multi_agent": p.supports_multi_agent,
                    "recommended_workers": p.recommended_workers,
                    "max_depth": p.max_depth,
                    "aios_relevant_keywords": p.aios_relevant_keywords,
                    "default_relevance": p.default_relevance,
                    "description": p.description,
                }
                for p in self.patterns.values()
            ]
        }
        path.write_text(json.dumps(data, indent=2))


# =============================================================================
# Global library instance
# =============================================================================

_library: Optional[SourceLibrary] = None


def get_library() -> SourceLibrary:
    """Get the global source library instance."""
    global _library
    if _library is None:
        _library = SourceLibrary()
    return _library


def detect_source(url: str) -> Optional[SourcePattern]:
    """Detect source type from URL."""
    return get_library().detect(url)


def ainlp_pattern(query: str, source: str = "arxiv-ai") -> str:
    """
    Generate AINLP dendritic pattern.

    Usage:
        pattern = ainlp_pattern("multi-agent systems", "arxiv-ai")
        # Returns: AINLP.dendritic[void->arxiv-ai{"multi-agent systems"}]
    """
    return get_library().search(query, source)
