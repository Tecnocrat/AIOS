"""
VOID Compressor - Agentic Knowledge Compression Layer
======================================================

AINLP.dendritic[VOID->compress{knowledge_base}]

Transforms distilled markdown into structured knowledge:
- Semantic indexing across documents
- Cross-reference detection between concepts
- Knowledge graph generation
- AI-assisted summarization

Architecture:
    Distilled Docs → Compressor → Knowledge Graph + Index
                          ↓
                    Gemini/Ollama (optional AI layer)

Usage:
    from void_compressor import VOIDCompressor

    compressor = VOIDCompressor()
    graph = compressor.compress_directory("docs/distilled/")

    # Query the knowledge base
    results = compressor.query("shared responsibility model")
"""

import hashlib
import json
import logging
import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger("AIOS.VOID.Compressor")


@dataclass
class Concept:
    """A knowledge concept extracted from content."""

    name: str
    definition: str = ""
    source_file: str = ""
    section: str = ""
    frequency: int = 1
    related_concepts: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        """Unique ID based on name hash."""
        return hashlib.md5(self.name.lower().encode()).hexdigest()[:8]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "definition": self.definition[:500] if self.definition else "",
            "source_file": self.source_file,
            "section": self.section,
            "frequency": self.frequency,
            "related_concepts": self.related_concepts[:10],
            "tags": self.tags,
        }


@dataclass
class Document:
    """A distilled knowledge document."""

    path: str
    title: str = ""
    content: str = ""
    sections: list[str] = field(default_factory=list)
    concepts: list[str] = field(default_factory=list)
    word_count: int = 0
    source_url: str = ""

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "title": self.title,
            "sections": self.sections[:20],
            "concepts": self.concepts[:50],
            "word_count": self.word_count,
            "source_url": self.source_url,
        }


@dataclass
class KnowledgeGraph:
    """Graph structure connecting concepts and documents."""

    documents: dict[str, Document] = field(default_factory=dict)
    concepts: dict[str, Concept] = field(default_factory=dict)
    edges: list[tuple[str, str, str]] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def add_document(self, doc: Document):
        self.documents[doc.path] = doc

    def add_concept(self, concept: Concept):
        key = concept.name.lower()
        if key in self.concepts:
            # Merge with existing
            existing = self.concepts[key]
            existing.frequency += concept.frequency
            existing.related_concepts = list(
                set(existing.related_concepts + concept.related_concepts)
            )
        else:
            self.concepts[key] = concept

    def add_edge(self, source: str, target: str, relation: str):
        """Add relationship edge between concepts."""
        edge = (source.lower(), target.lower(), relation)
        if edge not in self.edges:
            self.edges.append(edge)

    def get_related(self, concept_name: str, depth: int = 1) -> list[str]:
        """Get related concepts up to depth levels."""
        related = set()
        current = {concept_name.lower()}

        for _ in range(depth):
            next_level = set()
            for c in current:
                for s, t, _ in self.edges:
                    if s == c:
                        next_level.add(t)
                    elif t == c:
                        next_level.add(s)
            related.update(next_level)
            current = next_level

        return list(related - {concept_name.lower()})

    def to_dict(self) -> dict:
        return {
            "metadata": self.metadata,
            "documents": {k: v.to_dict() for k, v in self.documents.items()},
            "concepts": {k: v.to_dict() for k, v in self.concepts.items()},
            "edges": self.edges[:500],  # Limit for serialization
            "stats": {
                "document_count": len(self.documents),
                "concept_count": len(self.concepts),
                "edge_count": len(self.edges),
            },
        }

    def save(self, path: str):
        """Save graph to JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)
        logger.info(f"Saved knowledge graph to {path}")

    @classmethod
    def load(cls, path: str) -> "KnowledgeGraph":
        """Load graph from JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        graph = cls()
        graph.metadata = data.get("metadata", {})
        graph.edges = [tuple(e) for e in data.get("edges", [])]

        # Reconstruct documents
        for k, v in data.get("documents", {}).items():
            graph.documents[k] = Document(
                path=v["path"],
                title=v.get("title", ""),
                sections=v.get("sections", []),
                concepts=v.get("concepts", []),
                word_count=v.get("word_count", 0),
                source_url=v.get("source_url", ""),
            )

        # Reconstruct concepts
        for k, v in data.get("concepts", {}).items():
            graph.concepts[k] = Concept(
                name=v["name"],
                definition=v.get("definition", ""),
                source_file=v.get("source_file", ""),
                section=v.get("section", ""),
                frequency=v.get("frequency", 1),
                related_concepts=v.get("related_concepts", []),
                tags=v.get("tags", []),
            )

        return graph


class VOIDCompressor:
    """
    Agentic knowledge compression system.

    Extracts concepts, builds relationships, enables semantic queries.
    """

    # Technical terms to extract as concepts
    CONCEPT_PATTERNS = [
        # Cloud computing
        r"\b(IaaS|PaaS|SaaS|FaaS)\b",
        r"\b(cloud computing|shared responsibility|elasticity)\b",
        r"\b(virtual machine|container|serverless)\b",
        r"\b(high availability|fault tolerance|disaster recovery)\b",
        r"\b(scalability|vertical scaling|horizontal scaling)\b",
        r"\b(load balancing|auto-scaling|CDN)\b",
        # AI/ML
        r"\b(large language model|LLM|transformer)\b",
        r"\b(multi-agent system|MAS|agent)\b",
        r"\b(neural network|deep learning|machine learning)\b",
        r"\b(reinforcement learning|supervised learning)\b",
        r"\b(embedding|vector|semantic search)\b",
        # Architecture
        r"\b(microservice|monolith|API gateway)\b",
        r"\b(message queue|event-driven|pub-sub)\b",
        r"\b(REST|GraphQL|gRPC)\b",
        # Security
        r"\b(authentication|authorization|OAuth)\b",
        r"\b(encryption|TLS|certificate)\b",
        r"\b(firewall|WAF|DDoS)\b",
    ]

    # Section header patterns
    HEADER_PATTERN = r"^(#{1,4})\s+(.+)$"

    def __init__(self, ai_enabled: bool = False):
        """
        Initialize compressor.

        Args:
            ai_enabled: Use AI for enhanced extraction (requires Gemini/Ollama)
        """
        self.ai_enabled = ai_enabled
        self.graph = KnowledgeGraph()
        self._compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.CONCEPT_PATTERNS]

    def compress_file(self, file_path: str) -> Document:
        """Extract knowledge from a single markdown file."""
        path = Path(file_path)
        if not path.exists():
            logger.warning(f"File not found: {file_path}")
            return Document(path=file_path)

        content = path.read_text(encoding="utf-8", errors="ignore")

        # Extract document metadata
        doc = Document(
            path=str(path),
            title=self._extract_title(content),
            content=content,
            word_count=len(content.split()),
            source_url=self._extract_source_url(content),
        )

        # Extract sections
        doc.sections = self._extract_sections(content)

        # Extract concepts
        concepts = self._extract_concepts(content, str(path))
        doc.concepts = [c.name for c in concepts]

        # Add to graph
        self.graph.add_document(doc)
        for concept in concepts:
            self.graph.add_concept(concept)

        # Build edges between concepts in same document
        self._build_concept_edges(concepts)

        logger.info(
            f"Compressed {path.name}: {doc.word_count} words, "
            f"{len(doc.sections)} sections, {len(concepts)} concepts"
        )

        return doc

    def compress_directory(self, dir_path: str, pattern: str = "*.md") -> KnowledgeGraph:
        """Compress all markdown files in directory."""
        path = Path(dir_path)
        if not path.exists():
            logger.error(f"Directory not found: {dir_path}")
            return self.graph

        files = list(path.rglob(pattern))
        logger.info(f"Found {len(files)} files to compress")

        for file_path in files:
            self.compress_file(str(file_path))

        # Build cross-document relationships
        self._build_cross_document_edges()

        # Update metadata
        self.graph.metadata = {
            "source_directory": str(path),
            "file_count": len(files),
            "compression_version": "1.0",
        }

        return self.graph

    def query(self, query: str, top_k: int = 10) -> list[dict]:
        """
        Query the knowledge graph for relevant concepts.

        Simple keyword matching for v1. AI-enhanced in future.
        """
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        results = []
        for name, concept in self.graph.concepts.items():
            # Score based on term overlap
            concept_terms = set(name.split()) | set(concept.definition.lower().split())
            overlap = len(query_terms & concept_terms)

            if overlap > 0 or query_lower in name:
                score = overlap + (2 if query_lower in name else 0)
                results.append(
                    {
                        "concept": concept.to_dict(),
                        "score": score,
                        "related": self.graph.get_related(name, depth=1)[:5],
                    }
                )

        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def get_summary(self) -> dict:
        """Get summary statistics of the knowledge graph."""
        # Top concepts by frequency
        top_concepts = sorted(
            self.graph.concepts.values(),
            key=lambda c: c.frequency,
            reverse=True,
        )[:20]

        # Documents by size
        docs_by_size = sorted(
            self.graph.documents.values(),
            key=lambda d: d.word_count,
            reverse=True,
        )

        return {
            "total_documents": len(self.graph.documents),
            "total_concepts": len(self.graph.concepts),
            "total_edges": len(self.graph.edges),
            "total_words": sum(d.word_count for d in docs_by_size),
            "top_concepts": [{"name": c.name, "frequency": c.frequency} for c in top_concepts],
            "documents": [
                {"title": d.title or d.path, "words": d.word_count} for d in docs_by_size[:10]
            ],
        }

    def _extract_title(self, content: str) -> str:
        """Extract document title from first H1."""
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        return match.group(1).strip() if match else ""

    def _extract_source_url(self, content: str) -> str:
        """Extract source URL from metadata."""
        match = re.search(r"\*\*Source\*\*:\s*(https?://[^\s]+)", content)
        return match.group(1).strip() if match else ""

    def _extract_sections(self, content: str) -> list[str]:
        """Extract section headers."""
        sections = []
        for match in re.finditer(self.HEADER_PATTERN, content, re.MULTILINE):
            level = len(match.group(1))
            title = match.group(2).strip()
            sections.append(f"{'#' * level} {title}")
        return sections

    def _extract_concepts(self, content: str, source_file: str) -> list[Concept]:
        """Extract technical concepts from content."""
        concepts = []
        seen = set()

        # Pattern-based extraction
        for pattern in self._compiled_patterns:
            for match in pattern.finditer(content):
                name = match.group(1) if match.lastindex else match.group(0)
                name_lower = name.lower()

                if name_lower not in seen:
                    seen.add(name_lower)

                    # Try to extract definition (sentence containing concept)
                    definition = self._extract_definition(content, name)

                    concepts.append(
                        Concept(
                            name=name,
                            definition=definition,
                            source_file=source_file,
                            frequency=len(pattern.findall(content)),
                        )
                    )

        # Extract capitalized terms (potential concepts)
        cap_pattern = r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b"
        for match in re.finditer(cap_pattern, content):
            name = match.group(1)
            name_lower = name.lower()

            # Filter common non-concepts
            skip_terms = {
                "microsoft azure",
                "azure fundamentals",
                "learning path",
                "this module",
                "you will",
                "in this",
            }
            if name_lower in seen or name_lower in skip_terms:
                continue

            # Must appear multiple times to be significant
            count = len(re.findall(re.escape(name), content, re.IGNORECASE))
            if count >= 3:
                seen.add(name_lower)
                concepts.append(
                    Concept(
                        name=name,
                        definition=self._extract_definition(content, name),
                        source_file=source_file,
                        frequency=count,
                    )
                )

        return concepts

    def _extract_definition(self, content: str, term: str) -> str:
        """Extract a sentence that defines or describes the term."""
        # Look for "X is..." pattern
        pattern = rf"{re.escape(term)}\s+(?:is|are|refers to|means)\s+([^.]+\.)"
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(0).strip()

        # Fallback: first sentence containing the term
        sentences = re.split(r"(?<=[.!?])\s+", content)
        for sentence in sentences:
            if term.lower() in sentence.lower() and len(sentence) < 500:
                return sentence.strip()

        return ""

    def _build_concept_edges(self, concepts: list[Concept]):
        """Build edges between concepts that co-occur."""
        names = [c.name.lower() for c in concepts]

        for i, c1 in enumerate(concepts):
            for c2 in concepts[i + 1 :]:
                # Co-occurrence = relationship
                self.graph.add_edge(c1.name, c2.name, "co-occurs")

                # Update related concepts
                if c2.name.lower() not in c1.related_concepts:
                    c1.related_concepts.append(c2.name)
                if c1.name.lower() not in c2.related_concepts:
                    c2.related_concepts.append(c1.name)

    def _build_cross_document_edges(self):
        """Build edges for concepts appearing in multiple documents."""
        # Group concepts by document
        concept_docs = defaultdict(list)
        for name, concept in self.graph.concepts.items():
            for doc_path, doc in self.graph.documents.items():
                if name in [c.lower() for c in doc.concepts]:
                    concept_docs[name].append(doc_path)

        # Concepts in same documents are related
        for name, docs in concept_docs.items():
            if len(docs) > 1:
                # This concept bridges multiple documents
                concept = self.graph.concepts.get(name)
                if concept:
                    concept.tags.append("cross-document")


# =============================================================================
# CLI Interface
# =============================================================================


def main():
    import argparse

    parser = argparse.ArgumentParser(description="VOID Compressor - Knowledge Graph Builder")
    parser.add_argument("path", help="File or directory to compress")
    parser.add_argument("--output", "-o", help="Output JSON file for knowledge graph")
    parser.add_argument("--query", "-q", help="Query the knowledge graph")
    parser.add_argument("--summary", "-s", action="store_true", help="Print summary statistics")

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    compressor = VOIDCompressor()
    path = Path(args.path)

    if path.is_file():
        compressor.compress_file(str(path))
    elif path.is_dir():
        compressor.compress_directory(str(path))
    else:
        print(f"❌ Path not found: {path}")
        return 1

    # Output
    if args.output:
        compressor.graph.save(args.output)
        print(f"✅ Saved to {args.output}")

    if args.query:
        results = compressor.query(args.query)
        print(f"\n🔍 Query: '{args.query}'")
        print(f"Found {len(results)} results:\n")
        for i, r in enumerate(results, 1):
            c = r["concept"]
            print(f"{i}. {c['name']} (score: {r['score']})")
            if c["definition"]:
                print(f"   {c['definition'][:100]}...")
            if r["related"]:
                print(f"   Related: {', '.join(r['related'][:3])}")
            print()

    if args.summary or (not args.output and not args.query):
        summary = compressor.get_summary()
        print("\n📊 Knowledge Graph Summary")
        print("=" * 40)
        print(f"Documents: {summary['total_documents']}")
        print(f"Concepts:  {summary['total_concepts']}")
        print(f"Edges:     {summary['total_edges']}")
        print(f"Words:     {summary['total_words']:,}")
        print("\nTop Concepts:")
        for c in summary["top_concepts"][:10]:
            print(f"  • {c['name']} ({c['frequency']})")

    return 0


if __name__ == "__main__":
    exit(main())
