#!/usr/bin/env python3
"""
AIOS VOID Bridge - Knowledge Ingestion from External Sources
============================================================

AINLP.dendritic[VOID=vertex,exploratory,intelligence]
VOID:Attractor,coherence_regulator,anti_entropic_organizer

Pulls scattered knowledge from bookmarks/URLs and crystallizes
it into structured AIOS documentation using TRI-AGENT INTELLIGENCE:

    🔷 OLLAMA (Harmonizer) - Initial coherence layer
       Local Mistral for fast, private preprocessing
       Entry/middle/exit point validation

    🟡 GEMINI (Creator) - Main reasoning engine
       Advanced distillation and knowledge extraction
       Primary crystallization worker

    🔵 GITHUB MODELS (Verifier) - Intelligent student
       Verification via Microsoft Cloud AI infrastructure
       Multi-model validation using GPT-4o/4.1

Origin: AIOS Cell Pure (Nous) - 2025-12-07
Enhanced: TRI-AGENT Pattern - 2025-12-08

Usage:
    # Ingest from bookmark file
    python void_bridge.py --bookmarks bookmarks.html --output docs/distilled/

    # Pull single URL with tri-agent crystallization
    python void_bridge.py --url "https://example.com/article" --crystallize

    # Multi-version distillation (stochastic-resistant)
    python void_bridge.py --url "..." --crystallize --multi-version 3

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
    VERIFIED = "verified"  # Multi-agent verification complete


class AgentRole(Enum):
    """Roles in the tri-agent crystallization cascade."""

    HARMONIZER = "harmonizer"  # OLLAMA - Initial coherence
    CREATOR = "creator"  # GEMINI - Main reasoning engine
    VERIFIER = "verifier"  # GITHUB - Intelligent verification


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

        # AI integration for crystallization (lazy initialization)
        self._gemini_model = None
        self._gemini_api_key = os.getenv("GEMINI_API_KEY")
        self._ai_provider = None  # Track which provider is active

        # Ollama local (ARCHIVED - hardware limitations)
        # Kept for future use when better hardware available
        self._ollama_available = False  # Disabled - timeout issues
        self._ollama_model = os.getenv("OLLAMA_MODEL", "aios-mistral:latest")

        # GitHub Models API (Microsoft Cloud AI - uses existing subscription)
        self._github_token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
        self._github_models_url = "https://models.github.ai/inference/chat/completions"
        self._github_model = os.getenv("GITHUB_MODEL", "openai/gpt-4o")

        # DUAL-AGENT cascade configuration (Cloud-only, fast)
        # OLLAMA archived - local hardware insufficient for timely responses
        self.tri_agent_enabled = True
        self.agent_cascade = {
            AgentRole.HARMONIZER: "github",   # GitHub GPT-4o-mini (fast)
            AgentRole.CREATOR: "gemini",       # Gemini 2.0 Flash (reasoning)
            AgentRole.VERIFIER: "github",      # GitHub GPT-4o (verification)
        }

        # Default crystallization patterns (canonical extraction templates)
        self.crystallization_patterns = self._load_default_patterns()

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

    def _check_ollama(self) -> bool:
        """Check if Ollama is available locally."""
        try:
            import subprocess

            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _load_default_patterns(self) -> dict:
        """Load canonical crystallization patterns for AI-guided distillation."""
        return {
            "standard": {
                "name": "Standard Knowledge Crystal",
                "template": """## Summary
{summary}

## Key Concepts
{concepts}

## Technical Details
{technical}

## AIOS Relevance
{aios_relevance}

## Tags
{tags}""",
                "instructions": """Extract structured knowledge focusing on:
1. Core concepts and definitions
2. Technical implementation details
3. Architectural patterns
4. Relationships to AIOS consciousness framework""",
            },
            "research": {
                "name": "Research Paper Crystal",
                "template": """## Abstract
{abstract}

## Key Findings
{findings}

## Methodology
{methodology}

## AIOS Applications
{applications}

## Citation Network
{citations}""",
                "instructions": """Extract academic knowledge focusing on:
1. Research objectives and conclusions
2. Novel contributions
3. Experimental methodology
4. Potential AIOS integration points""",
            },
            "architecture": {
                "name": "Architecture Pattern Crystal",
                "template": """## Pattern Name
{pattern_name}

## Problem Context
{problem}

## Solution
{solution}

## Implementation
{implementation}

## Trade-offs
{tradeoffs}

## AIOS Integration
{integration}""",
                "instructions": """Extract architectural knowledge focusing on:
1. Design pattern classification
2. Problem-solution mapping
3. Implementation considerations
4. AIOS dendritic intelligence alignment""",
            },
            "verification": {
                "name": "Verification Crystal",
                "template": """## Original Claim
{claim}

## Evidence
{evidence}

## Verification Status
{status}

## Confidence Level
{confidence}

## Issues Found
{issues}

## Recommendations
{recommendations}""",
                "instructions": """Critically analyze the knowledge extract:
1. Verify factual accuracy
2. Identify logical inconsistencies
3. Check for missing context
4. Assess confidence level (0.0-1.0)""",
            },
        }

    def _github_generate(self, prompt: str, model: str = None) -> Optional[str]:
        """Generate response using GitHub Models API (Microsoft Cloud AI).

        Uses GPT-4o or other models via Microsoft's GitHub infrastructure.
        Requires GITHUB_TOKEN with 'models' scope.

        Guide to create PAT with models scope:
        1. Go to https://github.com/settings/tokens
        2. Generate new token (classic)
        3. Select 'models' scope
        4. Copy token to GITHUB_TOKEN environment variable
        """
        if not self._github_token:
            logger.debug("GitHub Models: No GITHUB_TOKEN set")
            return None

        model = model or self._github_model
        try:
            import urllib.request
            import json as json_module

            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self._github_token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "Content-Type": "application/json",
            }

            data = json_module.dumps(
                {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt[:12000]}],
                    "temperature": 0.7,
                }
            ).encode()

            req = urllib.request.Request(
                self._github_models_url, data=data, headers=headers, method="POST"
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                result = json_module.loads(response.read().decode())
                content = result["choices"][0]["message"]["content"]
                return content

        except Exception as e:
            logger.warning(f"GitHub Models generation failed: {e}")
            return None

    def _get_gemini_model(self):
        """Lazy initialization of Gemini model (cached)."""
        if self._gemini_model is None and self._gemini_api_key:
            try:
                import google.generativeai as genai

                genai.configure(api_key=self._gemini_api_key)
                self._gemini_model = genai.GenerativeModel("gemini-2.0-flash")
                logger.info("🔮 Gemini 2.0 Flash initialized")
            except Exception as e:
                logger.warning(f"Gemini initialization failed: {e}")
        return self._gemini_model

    def _ollama_generate(self, prompt: str) -> Optional[str]:
        """Generate response using local Ollama."""
        if not self._ollama_available:
            return None
        try:
            import subprocess

            # Use ollama API via subprocess with UTF-8 encoding
            result = subprocess.run(
                [
                    "ollama",
                    "run",
                    self._ollama_model,
                    prompt[:4000],  # Limit prompt size for local models
                ],
                capture_output=True,
                text=True,
                timeout=120,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as e:
            logger.warning(f"Ollama generation failed: {e}")
        return None

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
                title_pattern = r"<title[^>]*>([^<]+)</title>"
                title_match = re.search(title_pattern, vertex.content, re.IGNORECASE)
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
        """Use AI to extract and structure knowledge.

        TRI-AGENT CASCADE (when enabled):
        1. OLLAMA (Harmonizer) - Initial coherence, noise filtering
        2. GEMINI (Creator) - Main reasoning, knowledge extraction
        3. GITHUB (Verifier) - Intelligent verification, quality check

        Single-agent fallback cascade:
        1. Gemini 2.0 Flash (cloud, high quality)
        2. GitHub Models GPT-4o (Microsoft Cloud)
        3. Ollama local (aios-mistral, offline capable)
        4. Basic extraction (no AI fallback)
        """
        if self.tri_agent_enabled:
            return self._tri_agent_crystallize(vertex)

        # Single agent cascade (original behavior)
        prompt = self._build_crystallize_prompt(vertex)

        # Try Gemini first (cached model)
        gemini = self._get_gemini_model()
        if gemini:
            try:
                response = gemini.generate_content(prompt)
                self._ai_provider = "gemini"
                logger.debug("Crystallized via Gemini 2.0 Flash")
                return response.text
            except Exception as e:
                logger.warning(f"Gemini crystallization failed: {e}")

        # Try GitHub Models (Microsoft Cloud AI)
        result = self._github_generate(prompt)
        if result:
            self._ai_provider = "github"
            logger.debug(f"Crystallized via GitHub Models ({self._github_model})")
            return result

        # Fallback to Ollama local
        if self._ollama_available:
            result = self._ollama_generate(prompt)
            if result:
                self._ai_provider = "ollama"
                logger.debug(f"Crystallized via Ollama ({self._ollama_model})")
                return result

        # Final fallback to basic extraction
        self._ai_provider = "basic"
        logger.debug("Crystallized via basic extraction (no AI)")
        return self._basic_crystallize(vertex)

    def _tri_agent_crystallize(self, vertex: VOIDVertex) -> str:
        """Tri-agent cascade crystallization for maximum quality.

        Stage 1 - HARMONIZER (Ollama/local):
            - Initial content preprocessing
            - Noise filtering and structure detection
            - Entry point coherence check

        Stage 2 - CREATOR (Gemini):
            - Main knowledge extraction
            - Concept identification
            - Relationship mapping
            - Primary crystallization

        Stage 3 - VERIFIER (GitHub/Microsoft Cloud):
            - Quality verification
            - Factual consistency check
            - Gap identification
            - Exit point validation
        """
        logger.info("🔷 DUAL-AGENT: Starting cloud cascade...")

        # Stage 1: HARMONIZER (GitHub GPT-4o-mini - fast cloud preprocessing)
        harmonized_content = vertex.content
        if self._github_token:
            logger.info("   🔵 Stage 1: HARMONIZER (GitHub GPT-4o-mini)")
            harmonize_prompt = f"""Preprocess this content for knowledge extraction.
Remove noise, identify structure, extract key sections.
Keep technical details intact. Be concise.

CONTENT:
{vertex.content[:6000]}

OUTPUT: Clean, structured content ready for deep analysis."""

            result = self._github_generate(harmonize_prompt, "openai/gpt-4o-mini")
            if result:
                harmonized_content = result
                logger.info("      ✓ Content harmonized")

        # Stage 2: CREATOR (Gemini - main reasoning engine)
        crystal = None
        gemini = self._get_gemini_model()
        if gemini:
            logger.info("   🟡 Stage 2: CREATOR (Gemini)")
            pattern = self.crystallization_patterns.get("standard", {})
            create_prompt = f"""AINLP.dendritic[VOID] Knowledge Crystallization

SOURCE: {vertex.source}
TITLE: {vertex.title}

{pattern.get('instructions', 'Extract key knowledge.')}

PREPROCESSED CONTENT:
{harmonized_content[:8000]}

OUTPUT FORMAT:
{pattern.get('template', 'Structured knowledge summary.')}"""

            try:
                response = gemini.generate_content(create_prompt)
                crystal = response.text
                self._ai_provider = "gemini+tri-agent"
                logger.info("      ✓ Crystal created")
            except Exception as e:
                logger.warning(f"      Creator failed: {e}")

        # Fallback to GitHub if Gemini failed
        if not crystal:
            result = self._github_generate(self._build_crystallize_prompt(vertex))
            if result:
                crystal = result
                self._ai_provider = "github+tri-agent"

        # Final fallback
        if not crystal:
            crystal = self._basic_crystallize(vertex)
            self._ai_provider = "basic"
            return crystal

        # Stage 3: VERIFIER (GitHub Models - intelligent student)
        if self._github_token:
            logger.info("   🔵 Stage 3: VERIFIER (GitHub/Microsoft)")
            verify_pattern = self.crystallization_patterns.get("verification", {})
            verify_prompt = f"""You are an intelligent verification agent.
Analyze this knowledge crystal for quality and accuracy.

{verify_pattern.get('instructions', 'Verify the knowledge extract.')}

CRYSTAL TO VERIFY:
{crystal[:6000]}

ORIGINAL SOURCE: {vertex.source}

Provide brief verification notes (keep the crystal, add verification footer):
- Confidence score (0.0-1.0)
- Any concerns or gaps
- Verification status: VERIFIED/NEEDS_REVIEW/UNVERIFIED"""

            verification = self._github_generate(verify_prompt, "openai/gpt-4o-mini")
            if verification:
                crystal += f"\n\n---\n## 🔵 Verification Notes\n{verification}"
                vertex.state = VOIDState.VERIFIED
                logger.info("      ✓ Crystal verified")

        logger.info("🔷 DUAL-AGENT: Cascade complete")
        return crystal

    def crystallize_multi_version(self, vertex: VOIDVertex, num_versions: int = 3) -> list[str]:
        """Generate multiple crystallization versions for comparison.

        Produces stochastic-resistant knowledge extraction by:
        1. Running multiple independent crystallizations
        2. Using different models/temperatures
        3. Enabling cross-comparison verification

        Returns list of crystallized versions for agent comparison.
        """
        logger.info(f"🔮 Multi-version crystallization: {num_versions} versions")
        versions = []

        # Version configs: (provider, model, temperature_hint)
        configs = [
            ("gemini", None, "balanced"),
            ("github", "openai/gpt-4o", "creative"),
            ("github", "openai/gpt-4o-mini", "concise"),
            ("ollama", None, "local"),
        ][:num_versions]

        for i, (provider, model, style) in enumerate(configs):
            logger.info(f"   Version {i+1}/{num_versions}: {provider} ({style})")

            prompt = self._build_crystallize_prompt(vertex)
            prompt = f"[Style: {style}]\n{prompt}"
            result = None

            if provider == "gemini":
                gemini = self._get_gemini_model()
                if gemini:
                    try:
                        response = gemini.generate_content(prompt)
                        result = response.text
                    except Exception:
                        pass

            elif provider == "github":
                result = self._github_generate(prompt, model)

            elif provider == "ollama" and self._ollama_available:
                result = self._ollama_generate(prompt)

            if result:
                versions.append(
                    {
                        "version": i + 1,
                        "provider": provider,
                        "model": model,
                        "style": style,
                        "content": result,
                    }
                )

        # Store versions in vertex metadata
        vertex.metadata["multi_versions"] = len(versions)
        vertex.metadata["versions"] = versions

        logger.info(f"   Generated {len(versions)} versions")
        return versions

    def compare_versions(self, versions: list[dict]) -> str:
        """Use an agent to compare multiple distillation versions.

        Leverages GitHub Models as the comparison agent to:
        1. Identify common knowledge across versions
        2. Flag discrepancies
        3. Synthesize best elements
        4. Produce consensus crystal
        """
        if not versions or len(versions) < 2:
            return versions[0]["content"] if versions else ""

        logger.info("🔄 Comparing versions with agent...")

        version_text = "\n\n---\n\n".join(
            [
                f"VERSION {v['version']} ({v['provider']}, {v['style']}):\n{v['content'][:3000]}"
                for v in versions
            ]
        )

        compare_prompt = f"""You are a knowledge synthesis agent.
Compare these {len(versions)} crystallization versions of the same source.

{version_text}

TASK:
1. Identify CONSENSUS knowledge (present in all versions)
2. Note UNIQUE insights (only in one version)
3. Flag DISCREPANCIES (conflicting information)
4. Produce SYNTHESIZED CRYSTAL combining best elements

OUTPUT: Final synthesized knowledge crystal with confidence notes."""

        # Use GitHub Models for comparison (neutral third party)
        result = self._github_generate(compare_prompt, "openai/gpt-4o")
        if result:
            return result

        # Fallback to Gemini
        gemini = self._get_gemini_model()
        if gemini:
            try:
                response = gemini.generate_content(compare_prompt)
                return response.text
            except Exception:
                pass

        # Final fallback: return first version
        return versions[0]["content"]

    def _build_crystallize_prompt(self, vertex: VOIDVertex) -> str:
        """Build the crystallization prompt for AI models."""
        return f"""AINLP.dendritic[VOID] Knowledge Crystallization

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
    parser.add_argument(
        "--multi-version",
        "-m",
        type=int,
        default=0,
        help="Generate N crystallization versions for comparison",
    )
    parser.add_argument(
        "--tri-agent",
        "-t",
        action="store_true",
        help="Enable tri-agent cascade (OLLAMA→GEMINI→GITHUB)",
    )
    parser.add_argument("--output", "-o", help="Output directory for crystals")
    parser.add_argument("--status", "-s", action="store_true", help="Show bridge status")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")

    args = parser.parse_args()

    bridge = VOIDBridge()

    # Configure tri-agent mode
    if args.tri_agent:
        bridge.tri_agent_enabled = True
        logger.info("🔷 Tri-agent cascade enabled")
    elif hasattr(args, "multi_version") and args.multi_version > 0:
        bridge.tri_agent_enabled = False  # Multi-version uses separate agents

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

        if args.multi_version > 0:
            # Multi-version distillation mode
            versions = bridge.crystallize_multi_version(vertex, args.multi_version)
            synthesized = bridge.compare_versions(versions)
            vertex.crystallized = synthesized
            vertex.state = VOIDState.VERIFIED
            bridge.save_crystal(vertex)
            print(f"\n💎 Multi-version crystal ({args.multi_version} versions):")
            print(synthesized[:500] + "...")

        elif args.crystallize:
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
