#!/usr/bin/env python3
"""
AIOS Context Index Regeneration Script

AINLP.dendritic[context→index]{regeneration,freshness}

This script regenerates the context_index.json from AIOS_PROJECT_CONTEXT.md
to ensure context freshness across the system.

Location: scripts/context_reindex.py
Output: runtime/context/context_index.json

Usage:
    python scripts/context_reindex.py [--emit-adjacency]

Standard library only - no external dependencies required.
"""

import json
import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Resolve paths relative to script location
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
# Context source can be in root or docs/ - check both locations
CONTEXT_SOURCE_ROOT = REPO_ROOT / "AIOS_PROJECT_CONTEXT.md"
CONTEXT_SOURCE_DOCS = REPO_ROOT / "docs" / "AIOS_PROJECT_CONTEXT.md"
CONTEXT_SOURCE = CONTEXT_SOURCE_ROOT if CONTEXT_SOURCE_ROOT.exists() else CONTEXT_SOURCE_DOCS
CONTEXT_INDEX_OUTPUT = REPO_ROOT / "runtime" / "context" / "context_index.json"
ADJACENCY_OUTPUT = REPO_ROOT / "runtime" / "context" / "adjacency_graph.json"


def compute_hash(content: str) -> str:
    """Compute SHA-256 hash of content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def estimate_tokens(text: str) -> int:
    """Rough token estimate (chars / 4)."""
    return len(text) // 4


def extract_semantic_tags(content: str) -> list[str]:
    """Extract semantic tags from content based on key terms."""
    tags = set()
    tag_patterns = {
        "consciousness": r"\bconsciousness\b",
        "ainlp": r"\bAINLP\b",
        "dendritic": r"\bdendritic\b",
        "supercell": r"\bsupercell\b",
        "tachyonic": r"\btachyonic\b",
        "evolution": r"\bevolution\b",
        "bridge": r"\bbridge\b",
        "transport": r"\btransport\b",
        "security": r"\bsecurity\b",
        "nucleus": r"\bnucleus\b",
        "orchestration": r"\borchestration\b",
        "environment": r"\benvironment\b",
        "architecture": r"\barchitecture\b",
        "protocol": r"\bprotocol\b",
        "integration": r"\bintegration\b",
    }
    for tag, pattern in tag_patterns.items():
        if re.search(pattern, content, re.IGNORECASE):
            tags.add(tag)
    return sorted(tags)


def extract_dates(content: str) -> list[str]:
    """Extract dates from content in YYYY-MM-DD format."""
    dates = set()
    # Match YYYY-MM-DD patterns
    for match in re.finditer(r"\b(20\d{2}-\d{2}-\d{2})\b", content):
        dates.add(match.group(1))
    return sorted(dates)


def jaccard_similarity(set1: set, set2: set) -> float:
    """Compute Jaccard similarity between two sets."""
    if not set1 and not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0


def parse_context_file(filepath: Path) -> list[dict]:
    """
    Parse the PROJECT_CONTEXT.md file into capsules.

    Capsules are sections delimited by ## headers.
    """
    if not filepath.exists():
        print(f"Warning: Context source file not found: {filepath}")
        return []

    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    capsules = []
    current_capsule = None
    current_content_lines = []
    current_start_line = 1

    for i, line in enumerate(lines, start=1):
        # Detect section headers (## level)
        header_match = re.match(r"^##\s+(.+)$", line)

        if header_match:
            # Save previous capsule if exists
            if current_capsule:
                content_text = "\n".join(current_content_lines)
                current_capsule["end_line"] = i - 1
                current_capsule["content_hash"] = compute_hash(content_text)
                current_capsule["token_estimate"] = estimate_tokens(content_text)
                current_capsule["semantic_tags"] = extract_semantic_tags(content_text)
                current_capsule["dates_all"] = extract_dates(content_text)
                capsules.append(current_capsule)

            # Start new capsule
            title = header_match.group(1).strip()
            capsule_id = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            current_capsule = {
                "id": capsule_id,
                "title": title,
                "type": "note",
                "ingested_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "start_line": i,
                "end_line": None,
                "content_hash": None,
                "semantic_tags": [],
                "revision_chain": [],
                "dates_all": [],
                "token_estimate": 0,
                "jaccard_overlap_prev": None,
                "similarity_alert": False,
            }
            current_content_lines = [line]
            current_start_line = i
        elif current_capsule:
            current_content_lines.append(line)
        elif not current_capsule and i == 1:
            # Handle content before first header as "root" capsule
            current_capsule = {
                "id": "root",
                "title": "Root",
                "type": "note",
                "ingested_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "start_line": 1,
                "end_line": None,
                "content_hash": None,
                "semantic_tags": [],
                "revision_chain": [],
                "dates_all": [],
                "token_estimate": 0,
                "jaccard_overlap_prev": None,
                "similarity_alert": False,
            }
            current_content_lines = [line]

    # Save final capsule
    if current_capsule:
        content_text = "\n".join(current_content_lines)
        current_capsule["end_line"] = len(lines)
        current_capsule["content_hash"] = compute_hash(content_text)
        current_capsule["token_estimate"] = estimate_tokens(content_text)
        current_capsule["semantic_tags"] = extract_semantic_tags(content_text)
        current_capsule["dates_all"] = extract_dates(content_text)
        capsules.append(current_capsule)

    # Compute Jaccard overlap with previous capsule
    for i, capsule in enumerate(capsules):
        if i > 0:
            prev_tags = set(capsules[i - 1]["semantic_tags"])
            curr_tags = set(capsule["semantic_tags"])
            overlap = jaccard_similarity(prev_tags, curr_tags)
            capsule["jaccard_overlap_prev"] = round(overlap, 4)
            capsule["similarity_alert"] = overlap > 0.8  # High similarity warning

    return capsules


def build_adjacency_graph(capsules: list[dict]) -> dict:
    """
    Build adjacency graph based on semantic tag overlap.
    """
    adjacency = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "nodes": [],
        "edges": [],
    }

    # Create nodes
    for capsule in capsules:
        adjacency["nodes"].append(
            {"id": capsule["id"], "title": capsule["title"], "tags": capsule["semantic_tags"]}
        )

    # Create edges based on shared tags
    for i, cap1 in enumerate(capsules):
        tags1 = set(cap1["semantic_tags"])
        for j, cap2 in enumerate(capsules[i + 1 :], start=i + 1):
            tags2 = set(cap2["semantic_tags"])
            shared = tags1 & tags2
            if shared:
                adjacency["edges"].append(
                    {
                        "source": cap1["id"],
                        "target": cap2["id"],
                        "weight": len(shared),
                        "shared_tags": list(shared),
                    }
                )

    return adjacency


def generate_index(emit_adjacency: bool = False) -> None:
    """
    Generate the context index and optionally the adjacency graph.
    """
    print(f"[context_reindex] Parsing {CONTEXT_SOURCE}...")

    capsules = parse_context_file(CONTEXT_SOURCE)

    if not capsules:
        print("[context_reindex] Warning: No capsules extracted")
        # Create minimal index
        capsules = [
            {
                "id": "empty",
                "title": "Empty Index",
                "type": "note",
                "ingested_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "start_line": 1,
                "end_line": 1,
                "content_hash": compute_hash(""),
                "semantic_tags": [],
                "revision_chain": [],
                "dates_all": [],
                "token_estimate": 0,
                "jaccard_overlap_prev": None,
                "similarity_alert": False,
            }
        ]

    # Build index structure
    index = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_file": str(CONTEXT_SOURCE.name),
        "capsules": capsules,
    }

    # Ensure output directory exists
    CONTEXT_INDEX_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # Write index
    CONTEXT_INDEX_OUTPUT.write_text(
        json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"[context_reindex] Wrote {len(capsules)} capsules to {CONTEXT_INDEX_OUTPUT}")

    # Optionally emit adjacency graph
    if emit_adjacency:
        adjacency = build_adjacency_graph(capsules)
        ADJACENCY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        ADJACENCY_OUTPUT.write_text(
            json.dumps(adjacency, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"[context_reindex] Wrote adjacency graph to {ADJACENCY_OUTPUT}")


def main():
    """Entry point."""
    emit_adjacency = "--emit-adjacency" in sys.argv

    print("[context_reindex] AIOS Context Index Regeneration")
    print(f"[context_reindex] Source: {CONTEXT_SOURCE}")
    print(f"[context_reindex] Output: {CONTEXT_INDEX_OUTPUT}")

    try:
        generate_index(emit_adjacency=emit_adjacency)
        print("[context_reindex] Success!")
        return 0
    except Exception as e:
        print(f"[context_reindex] Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
