#!/usr/bin/env python3
"""AIOS Tachyonic Context Surface Reindexer

Parses AIOS_PROJECT_CONTEXT.md and generates:
    runtime_intelligence/context/context_index.json

Schema Version: 1

Design Goals:
- Zero external dependencies (stdlib only)
- Append-only friendly (does not mutate source)
- Deterministic hashing & canonicalization
- Graceful degradation: continue indexing after malformed capsule
"""
from __future__ import annotations
import re
import json
import hashlib
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple, Set, Dict, Any

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "AIOS_PROJECT_CONTEXT.md"
OUTPUT_DIR = ROOT / "runtime_intelligence" / "context"
OUTPUT = OUTPUT_DIR / "context_index.json"
SCHEMA_VERSION = 1

CAPSULE_HEADING_RE = re.compile(r"^## +(.+?)(?:\s+|$)")
DATE_RE = re.compile(r"(20[2-5][0-9]-[01][0-9]-[0-3][0-9])")
REVISION_RE = re.compile(
    r"^### +Revision.*?(\d{4}-\d{2}-\d{2})?",
    re.IGNORECASE,
)
TOKEN_SPLIT_RE = re.compile(r"\s+")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{4,}")
STOPLIST = {
    "added",
    "ingested",
    "phase",
    "guide",
    "note",
    "status",
    "report",
    "capsule",
    "revision",
    "summary",
}
TAG_KEYWORDS = {
    "reorganization": ["reorganization"],
    "environment": ["environment", "registry", "python system"],
    "orchestrator": ["orchestrator"],
    "quick-context": ["quick context", "quick-context"],
    "optimization": ["optimization", "optimiz"],
    "dual-interface": ["dual-interface", "dual interface", "quantum visor"],
    "consciousness": ["consciousness", "emergence"],
    "phase": ["phase 1", "phase 2"],
    "dependency": ["dependency", "requirements", "pyproject"],
    "strategy": ["strategy"],
    "recovery": ["recovery", "cleanup"],
}

@dataclass
class RevisionInfo:
    heading: str
    line: int
    date: Optional[str]
    hash: str

@dataclass
class CapsuleInfo:
    id: str
    title: str
    type: str
    ingested_date: Optional[str]
    start_line: int
    end_line: int
    content_hash: str
    semantic_tags: List[str]
    revision_chain: List[RevisionInfo]
    dates_all: List[str]
    token_estimate: int
    jaccard_overlap_prev: Optional[float]
    similarity_alert: bool


def slugify(title: str, existing: Set[str]) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip('-')
    slug = base or "capsule"
    i = 2
    while slug in existing:
        slug = f"{base}-{i}"
        i += 1
    existing.add(slug)
    return slug


def canonical_lines(lines: List[str]) -> List[str]:
    return [ln.rstrip() for ln in lines]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def extract_tags(text_lower: str) -> List[str]:
    tags: List[str] = []
    for tag, patterns in TAG_KEYWORDS.items():
        if any(p in text_lower for p in patterns):
            tags.append(tag)
    return sorted(set(tags))


def keyphrases(text_lower: str) -> set[str]:
    return {
        w for w in WORD_RE.findall(text_lower)
        if w.lower() not in STOPLIST
    }


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def classify_type(title: str) -> str:
    tl = title.lower()
    if "transition" in tl or "strategy" in tl:
        return "note"
    if "capsule" in tl:
        return "capsule"
    return "note"


def parse_source() -> List[CapsuleInfo]:
    text: List[str] = SOURCE.read_text(encoding='utf-8').splitlines()
    headings: List[Tuple[int, str]] = []
    for idx, line in enumerate(text, start=1):
        m = CAPSULE_HEADING_RE.match(line)
        if m:
            headings.append((idx, m.group(1).strip()))
    capsules: List[CapsuleInfo] = []
    used_slugs: Set[str] = set()

    for i, (line_no, title) in enumerate(headings):
        end_line = (
            headings[i + 1][0] - 1
            if i + 1 < len(headings) else len(text)
        )
        slice_lines = text[line_no - 1:end_line]
        canon = canonical_lines(slice_lines)
        normalized = "\n".join(canon)
        content_hash = sha256_text(normalized)
        dates = sorted(set(DATE_RE.findall(normalized)))
        ingested_date = None
        # heuristics: first 15 lines for any date marker
        for probe in canon[:15]:
            dm = DATE_RE.search(probe)
            if dm:
                ingested_date = dm.group(1)
                break
        revs: List[RevisionInfo] = []
        for rel_idx, raw in enumerate(slice_lines, start=0):
            rm = REVISION_RE.match(raw)
            if rm:
                r_start = rel_idx
                # find end of revision subsection (next ### or end of slice)
                r_end = None
                for inner in range(rel_idx + 1, len(slice_lines)):
                    if slice_lines[inner].startswith('### '):
                        r_end = inner
                        break
                r_end = r_end or len(slice_lines)
                rev_block = "\n".join(
                    canonical_lines(slice_lines[r_start:r_end])
                )
                rev_hash = sha256_text(rev_block)
                revs.append(
                    RevisionInfo(
                        heading=slice_lines[rel_idx].strip(),
                        line=line_no + rel_idx,
                        date=rm.group(1),
                        hash=rev_hash,
                    )
                )
        tag_list = extract_tags(normalized.lower())
        tokens = (
            len(TOKEN_SPLIT_RE.split(normalized.strip()))
            if normalized.strip() else 0
        )
        capsule = CapsuleInfo(
            id=slugify(title, used_slugs),
            title=title,
            type=classify_type(title),
            ingested_date=ingested_date,
            start_line=line_no,
            end_line=end_line,
            content_hash=content_hash,
            semantic_tags=tag_list,
            revision_chain=revs,
            dates_all=dates,
            token_estimate=tokens,
            jaccard_overlap_prev=None,  # update later
            similarity_alert=False,
        )
        capsules.append(capsule)

    # Similarity metrics
    prev_phrases: Optional[Set[str]] = None
    # Re-parse slices for full-text keyphrase extraction
    # (avoid storing full raw text inside index)
    full_text = SOURCE.read_text(encoding='utf-8').splitlines()
    for cap in capsules:
        slice_lines = full_text[cap.start_line - 1: cap.end_line]
        normalized = "\n".join(canonical_lines(slice_lines)).lower()
        phrases = keyphrases(normalized)
        if prev_phrases is not None:
            overlap = jaccard(prev_phrases, phrases)
            cap.jaccard_overlap_prev = round(overlap, 4)
            cap.similarity_alert = (overlap < 0.08) or (overlap > 0.90)
        prev_phrases = phrases
    return capsules


def generate_index():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Source context file not found: {SOURCE}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    capsules = parse_source()
    stats = {
        "capsule_count": len(capsules),
        "total_lines_indexed": sum(
            c.end_line - c.start_line + 1 for c in capsules
        ),
        "aggregate_token_estimate": sum(c.token_estimate for c in capsules),
    }
    data: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "source_file": SOURCE.name,
        "capsules": [asdict(c) for c in capsules],
        "stats": stats,
        "errors": [],
    }
    tmp = OUTPUT.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(data, indent=2), encoding='utf-8')
    tmp.replace(OUTPUT)
    return data


if __name__ == "__main__":
    try:
        result = generate_index()
        count = result['stats']['capsule_count']
        print(
            f"[context-reindex] Indexed {count} capsules -> {OUTPUT}"
        )
    except Exception as e:
        print(f"[context-reindex][ERROR] {e}")
        raise
