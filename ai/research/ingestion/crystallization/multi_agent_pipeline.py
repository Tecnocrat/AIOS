"""
VOID Multi-Agent Dendritic Ingestion Pipeline
==============================================

AINLP.dendritic[VOID->multi_agent{pattern}]

Coordinates multiple agents for parallel knowledge extraction
at dendritic vertices discovered during source processing.

Pipeline Pattern:
    1. Seed URL → Primary extraction (Tier 1)
    2. Related sources → Parallel ingestion (Tier 2 agents)
    3. Synthesis → Merge extracted knowledge (Tier 3)
    4. Crystal → Save unified knowledge structure
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger("AIOS.VOID.MultiAgent")


class AgentTier(Enum):
    """Agent tier classification for pipeline coordination."""

    TIER_1 = "tier_1"  # Signal preparation, fast analysis
    TIER_2 = "tier_2"  # Creative generation, detailed extraction
    TIER_3 = "tier_3"  # Validation, synthesis


@dataclass
class DendriticVertex:
    """
    A point of knowledge discovery in the information space.

    Represents a URL or source discovered during extraction
    that may contain related knowledge.
    """

    url: str
    parent_url: str  # Source that discovered this vertex
    depth: int = 0  # Distance from seed URL
    priority: float = 0.5  # 0.0-1.0, higher = more important
    tags: list[str] = field(default_factory=list)
    extracted: bool = False
    content: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class IngestionPipeline:
    """
    Configuration for multi-agent ingestion pipeline.
    """

    name: str
    seed_url: str
    max_depth: int = 2  # How deep to follow dendritic vertices
    max_vertices: int = 20  # Maximum vertices to process
    parallel_workers: int = 3  # Number of parallel extraction workers

    # Agent configuration per tier
    tier_1_model: str = "ollama:qwen2.5:0.5b"  # Fast, local
    tier_2_model: str = "gemini-2.0-flash"  # Creative, parallel
    tier_3_model: str = "gemini-2.0-flash"  # Synthesis

    # Filtering
    domain_filter: Optional[str] = None  # Only follow vertices in domain
    relevance_threshold: float = 0.3  # Min AIOS relevance to follow


@dataclass
class IngestionResult:
    """Result from multi-agent ingestion."""

    seed_url: str
    vertices_discovered: int = 0
    vertices_processed: int = 0
    crystals_generated: int = 0
    total_entropy_reduced: float = 0.0
    synthesis: str = ""
    crystal_paths: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class MultiAgentDendriticPipeline:
    """
    Multi-agent pipeline for dendritic knowledge extraction.

    AINLP.dendritic[VOID->multi_agent{query}]

    Workflow:
    1. Seed extraction with source adapter
    2. Discover dendritic vertices (related sources)
    3. Parallel extraction of high-priority vertices
    4. Synthesis into unified knowledge structure
    """

    def __init__(
        self, workspace: Optional[Path] = None, config: Optional[IngestionPipeline] = None
    ):
        self.workspace = workspace or Path("c:/dev/aios-win/aios-core")
        self.config = config

        self.vertices: list[DendriticVertex] = []
        self.processed: list[DendriticVertex] = []
        self.crystals: list[Path] = []

        # Lazy import to avoid circular deps
        self._bridge = None

    @property
    def bridge(self):
        """Lazy load VOID bridge."""
        if self._bridge is None:
            from void_bridge import VOIDBridge

            self._bridge = VOIDBridge(self.workspace)
        return self._bridge

    def discover_vertices(
        self, parent_url: str, related_sources: list[str], depth: int = 0
    ) -> list[DendriticVertex]:
        """
        Create dendritic vertices from discovered related sources.

        Applies filtering and priority scoring.
        """
        vertices = []

        for url in related_sources:
            # Skip already known vertices
            if any(v.url == url for v in self.vertices):
                continue

            # Apply domain filter if configured
            if self.config and self.config.domain_filter:
                if self.config.domain_filter not in url:
                    continue

            vertex = DendriticVertex(
                url=url,
                parent_url=parent_url,
                depth=depth,
            )

            # Priority scoring based on URL patterns
            vertex.priority = self._score_priority(url)

            vertices.append(vertex)

        return vertices

    def _score_priority(self, url: str) -> float:
        """
        Score priority of a dendritic vertex.

        Higher scores for AIOS-relevant domains.
        """
        priority = 0.5

        # ArXiv papers in relevant categories
        if "arxiv.org" in url:
            priority = 0.7
            if any(cat in url for cat in ["cs.AI", "cs.LG", "cs.MA", "cs.CL"]):
                priority = 0.9

        # GitHub repos
        if "github.com" in url:
            priority = 0.6

        # Documentation sites
        doc_domains = ["docs.", "documentation.", "wiki."]
        if any(d in url for d in doc_domains):
            priority = 0.65

        return priority

    def extract_vertex(self, vertex: DendriticVertex) -> Optional[DendriticVertex]:
        """
        Extract knowledge from a single dendritic vertex.

        Uses appropriate adapter based on URL type.
        """
        try:
            # Determine source type
            if "arxiv.org" in vertex.url:
                vx = self.bridge.void_pull_arxiv(vertex.url)
            else:
                vx = self.bridge.void_pull_url(vertex.url)

            # Transfer extracted data to vertex
            vertex.extracted = True
            vertex.content = vx.content
            vertex.metadata = {
                "title": vx.title,
                "tags": vx.tags,
                "aios_relevance": vx.metadata.get("aios_relevance", 0),
                "related_sources": vx.metadata.get("related_sources", []),
            }

            # Discover new vertices from this one
            if vertex.depth < (self.config.max_depth if self.config else 2):
                new_related = vx.metadata.get("related_sources", [])
                new_vertices = self.discover_vertices(
                    vertex.url, new_related, depth=vertex.depth + 1
                )
                self.vertices.extend(new_vertices)

            return vertex

        except Exception as e:
            logger.warning(f"Failed to extract vertex {vertex.url}: {e}")
            return None

    def run_parallel_extraction(
        self, vertices: list[DendriticVertex], max_workers: int = 3
    ) -> list[DendriticVertex]:
        """
        Extract multiple vertices in parallel.

        Uses ThreadPoolExecutor for I/O-bound operations.
        """
        results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.extract_vertex, v): v for v in vertices}

            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)

        return results

    def synthesize(self, vertices: list[DendriticVertex], topic: str = "") -> str:
        """
        Synthesize extracted knowledge into unified structure.

        Uses Tier 3 model for critical synthesis.
        """
        import os

        # Collect all extracted content
        contents = []
        for v in vertices:
            if v.extracted and v.metadata:
                title = v.metadata.get("title", v.url)
                relevance = v.metadata.get("aios_relevance", 0)
                contents.append(
                    f"### {title}\n"
                    f"URL: {v.url}\n"
                    f"AIOS Relevance: {relevance:.2f}\n"
                    f"Depth: {v.depth}\n"
                )

        if not contents:
            return "No content to synthesize."

        # Use AI for synthesis
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                import google.generativeai as genai

                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.0-flash")

                prompt = f"""AINLP.dendritic[VOID] Knowledge Synthesis

Topic: {topic}

You have extracted knowledge from {len(vertices)} dendritic vertices.
Synthesize the key insights relevant to AIOS development.

EXTRACTED SOURCES:
{chr(10).join(contents)}

---

Provide:
1. **Synthesis Summary**: 2-3 sentences of unified insight
2. **Key Patterns**: Common themes across sources
3. **AIOS Applicability**: How this relates to AI system design
4. **Knowledge Gaps**: What's missing for complete understanding
5. **Recommended Next Vertices**: What to explore next
"""

                response = model.generate_content(prompt)
                return response.text

            except Exception as e:
                logger.warning(f"Synthesis failed: {e}")

        # Fallback: basic concatenation
        return "\n\n".join(contents)

    def run(
        self, seed_url: str, topic: str = "", config: Optional[IngestionPipeline] = None
    ) -> IngestionResult:
        """
        Run the full multi-agent dendritic ingestion pipeline.

        Args:
            seed_url: Starting URL for extraction
            topic: Topic description for synthesis context
            config: Pipeline configuration (overrides instance config)
        """
        cfg = config or self.config or IngestionPipeline(name="default", seed_url=seed_url)

        result = IngestionResult(seed_url=seed_url)

        logger.info(f"VOID Multi-Agent Pipeline: {seed_url}")
        logger.info(f"Config: depth={cfg.max_depth}, workers={cfg.parallel_workers}")

        # Phase 1: Seed extraction
        logger.info("Phase 1: Seed extraction...")
        seed_vertex = DendriticVertex(url=seed_url, parent_url="", depth=0)
        self.extract_vertex(seed_vertex)
        self.processed.append(seed_vertex)

        # Collect initial vertices
        initial_related = seed_vertex.metadata.get("related_sources", [])
        self.vertices = self.discover_vertices(seed_url, initial_related, depth=1)

        result.vertices_discovered = len(self.vertices)
        logger.info(f"Discovered {len(self.vertices)} dendritic vertices")

        # Phase 2: Priority filtering and parallel extraction
        logger.info("Phase 2: Parallel vertex extraction...")

        # Sort by priority, limit to max_vertices
        prioritized = sorted(self.vertices, key=lambda v: v.priority, reverse=True)[
            : cfg.max_vertices
        ]

        extracted = self.run_parallel_extraction(prioritized, max_workers=cfg.parallel_workers)

        self.processed.extend(extracted)
        result.vertices_processed = len(extracted)
        logger.info(f"Processed {len(extracted)} vertices")

        # Phase 3: Crystallize all extracted content
        logger.info("Phase 3: Crystallization...")
        for vertex in self.processed:
            if vertex.extracted:
                try:
                    # Find the VOID vertex
                    for vx in self.bridge.vertices:
                        if vx.source == vertex.url:
                            self.bridge.crystallize(vx)
                            path = self.bridge.save_crystal(vx)
                            self.crystals.append(path)
                            result.crystals_generated += 1
                            result.total_entropy_reduced += vx.entropy
                            result.crystal_paths.append(str(path))
                            break
                except Exception as e:
                    logger.warning(f"Crystal failed for {vertex.url}: {e}")

        # Phase 4: Synthesis
        logger.info("Phase 4: Synthesis...")
        result.synthesis = self.synthesize(self.processed, topic)

        logger.info(
            f"Pipeline complete: {result.crystals_generated} crystals, "
            f"entropy reduced: {result.total_entropy_reduced:.2f}"
        )

        return result


# =============================================================================
# Convenience functions
# =============================================================================


def void_multi_agent_ingest(
    seed_url: str,
    topic: str = "",
    max_depth: int = 2,
    max_vertices: int = 10,
    parallel_workers: int = 3,
) -> IngestionResult:
    """
    Convenience function for multi-agent dendritic ingestion.

    Usage:
        result = void_multi_agent_ingest(
            "https://arxiv.org/html/2503.16600v2",
            topic="Little Red Dots astrophysics"
        )
    """
    config = IngestionPipeline(
        name="adhoc",
        seed_url=seed_url,
        max_depth=max_depth,
        max_vertices=max_vertices,
        parallel_workers=parallel_workers,
    )

    pipeline = MultiAgentDendriticPipeline(config=config)
    return pipeline.run(seed_url, topic, config)
