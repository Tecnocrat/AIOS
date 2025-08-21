"""Generate per-file criticality scores.

Outputs:
  - governance/file_criticality_index.jsonl (authoritative index)
  - runtime_intelligence/logs/file_scores/latest.json (telemetry snapshot)

Scoring references agent-mode instructions file_criticality.* keys.
Initial scaffold: structure only; fan-in/out & coverage placeholders.
"""
from __future__ import annotations

import json
import time
import pathlib
import subprocess
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
INDEX_PATH = REPO_ROOT / 'governance' / 'file_criticality_index.jsonl'
TELEMETRY_OUT = (
    REPO_ROOT / 'runtime_intelligence' / 'logs' / 'file_scores' / 'latest.json'
)
OWNERSHIP_MAP_PATH = REPO_ROOT / 'governance' / 'file_ownership_map.json'

# Weights (must mirror file_criticality.weights.v1)
WEIGHTS = dict(
    w1=0.18,
    w2=0.15,
    w3=0.20,
    w4=0.12,
    w5=0.15,
    w6=0.12,
    w7=0.08,
)


@dataclass
class FileMetrics:
    path: str
    fan_in: float = 0.0
    fan_out: float = 0.0
    churn_90d: float = 0.0
    blast_radius: float = 0.0
    coverage_pct: float = 0.0
    security_flag: int = 0
    runtime_touch_freq: float = 0.0
    stability_weight: float = 1.0
    refactor_confidence: float = 0.0
    criticality_score: float = 0.0
    tier: str = 'low'
    last_reviewed: Optional[str] = None
    deprecation_stage: Optional[str] = None
    ownership: Optional[str] = None
    coupling_degree: Optional[float] = None
    coverage_band: Optional[str] = None
    synthetic_precision: Optional[str] = None


def discover_files() -> List[pathlib.Path]:
    include_roots = ['ai', 'interface', 'core', 'runtime_intelligence']
    exts = {'.py', '.cs', '.cpp', '.h', '.hpp'}
    results: List[pathlib.Path] = []
    for root in include_roots:
        base = REPO_ROOT / root
        if not base.exists():
            continue
        for path in base.rglob('*'):
            if not path.is_file():
                continue
            if path.suffix not in exts:
                continue
            if 'build' in path.parts or path.name.endswith('.pyc'):
                continue
            results.append(path)
    return results


def git_churn(path: pathlib.Path) -> float:
    rel = path.relative_to(REPO_ROOT).as_posix()
    try:
        out = subprocess.check_output(
            ['git', 'log', '--since=90.days', '--pretty=oneline', '--', rel],
            cwd=REPO_ROOT,
            text=True,
        )
        lines = [line for line in out.splitlines() if line.strip()]
        return float(len(lines))
    except Exception:
        return 0.0


def naive_fan_out(path: pathlib.Path) -> float:
    # Count basic import/include statements (rough heuristic)
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return 0.0
    count = 0
    if path.suffix == '.py':
        for line in text.splitlines():
            if line.startswith('import ') or line.startswith('from '):
                count += 1
    elif path.suffix == '.cs':
        count += sum(
            1
            for line in text.splitlines()
            if line.strip().startswith('using ')
        )
    elif path.suffix in {'.cpp', '.h', '.hpp'}:
        count += sum(
            1
            for line in text.splitlines()
            if line.strip().startswith('#include')
        )
    return float(count)


def naive_fan_in(all_files: List[pathlib.Path], target: pathlib.Path) -> float:
    stem = target.stem
    count = 0
    for candidate in all_files:
        if candidate == target:
            continue
        try:
            text = candidate.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        if target.suffix == '.py':
            if (
                candidate.suffix == '.py'
                and (f"import {stem}" in text or f"from {stem}" in text)
            ):
                count += 1
        else:
            if stem in text:
                count += 1
    return float(count)


def normalize(values: List[float]) -> List[float]:
    if not values:
        return values
    max_val = max(values)
    if max_val <= 0:
        return [0.0 for _ in values]
    return [v / max_val for v in values]


def assign_tier(score: float) -> str:
    if score >= 90:
        return 'core'
    if score >= 75:
        return 'high'
    if score >= 40:
        return 'medium'
    return 'low'


def load_coverage_map() -> Dict[str, float]:
    """Attempt to load coverage data (coverage.json) else return empty map."""
    cov_map: Dict[str, float] = {}
    cov_json = REPO_ROOT / 'coverage.json'
    if cov_json.exists():
        try:
            data = json.loads(cov_json.read_text(encoding='utf-8'))
            files = data.get('files', {})
            for path_str, meta in files.items():
                p_rel = pathlib.Path(path_str).as_posix()
                if p_rel.startswith('./'):
                    p_rel = p_rel[2:]
                cov = meta.get('summary', {}).get('percent_covered')
                if cov is not None:
                    cov_map[p_rel] = float(cov)
        except Exception:
            pass
    return cov_map


def heuristic_runtime_touch(path: pathlib.Path) -> float:
    """Proxy runtime touch frequency via git blame line count (log scaled)."""
    try:
        rel = path.relative_to(REPO_ROOT).as_posix()
        out = subprocess.check_output(
            ['git', 'blame', '--line-porcelain', '-l', rel],
            cwd=REPO_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        lines = [
            ln for ln in out.splitlines()
            if ln and not ln.startswith('#')
        ]
        import math
        return round(math.log(len(lines) + 1, 10), 4)
    except Exception:
        return 0.0


def load_previous_index() -> Dict[str, Dict[str, float]]:
    prev: Dict[str, Dict[str, float]] = {}
    if not INDEX_PATH.exists():
        return prev
    try:
        for line in INDEX_PATH.read_text(encoding='utf-8').splitlines():
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            path = obj.get('path')
            if not path:
                continue
            prev[path] = {
                'score': float(obj.get('criticality_score', 0.0)),
                'precision': obj.get('synthetic_precision'),
            }
    except Exception:
        pass
    return prev


def load_ownership_map() -> Dict[str, str]:
    """Load ownership prefix map; keys are path prefixes (posix style)."""
    if not OWNERSHIP_MAP_PATH.exists():
        return {}
    try:
        data = json.loads(OWNERSHIP_MAP_PATH.read_text(encoding='utf-8'))
        return {k: v for k, v in data.items() if not k.startswith('_')}
    except Exception:
        return {}


def resolve_owner(path: str, ownership_map: Dict[str, str]) -> Optional[str]:
    if not ownership_map:
        return None
    best_prefix = ''
    best_owner = None
    for prefix, owner in ownership_map.items():
        if path.startswith(prefix) and len(prefix) > len(best_prefix):
            best_prefix = prefix
            best_owner = owner
    return best_owner


def main() -> None:
    files = discover_files()
    metrics: Dict[str, FileMetrics] = {}
    coverage_map = load_coverage_map()
    prev_index = load_previous_index()
    ownership_map = load_ownership_map()
    for path in files:
        fm = FileMetrics(path=path.relative_to(REPO_ROOT).as_posix())
        fm.fan_out = naive_fan_out(path)
        fm.churn_90d = git_churn(path)
        if path.suffix == '.py':
            fm.coverage_pct = coverage_map.get(fm.path, 0.0)
        fm.runtime_touch_freq = heuristic_runtime_touch(path)
        fm.ownership = resolve_owner(fm.path, ownership_map)
        metrics[fm.path] = fm
    for path in files:
        rel = path.relative_to(REPO_ROOT).as_posix()
        metrics[rel].fan_in = naive_fan_in(files, path)
    for fm in metrics.values():
        fm.blast_radius = fm.fan_in
    fan_in_norm = normalize([m.fan_in for m in metrics.values()])
    blast_norm = normalize([m.blast_radius for m in metrics.values()])
    for (fm, fi_n, br_n) in zip(metrics.values(), fan_in_norm, blast_norm):
        coverage_n = (fm.coverage_pct / 100.0) if fm.coverage_pct else 0.0
        refactor_confidence_n = 0.0
        raw_score = (
            WEIGHTS['w1'] * fi_n
            + WEIGHTS['w2'] * br_n
            + WEIGHTS['w3'] * fm.security_flag
            + WEIGHTS['w4'] * (1 - coverage_n)
            + WEIGHTS['w5'] * fm.runtime_touch_freq
            + WEIGHTS['w6'] * fm.stability_weight
            - WEIGHTS['w7'] * refactor_confidence_n
        ) * 100.0
        prev = prev_index.get(fm.path)
        prev_score = prev['score'] if prev else None
        delta = None
        if prev_score is not None:
            delta = raw_score - prev_score
        # Determine precision mode
        # Boundary proximity thresholds
        boundaries = (40, 75, 90)
        dist_to_boundary = min(
            (abs(raw_score - b) for b in boundaries), default=999
        )
        # Base precision selection
        if delta is None:
            # First observation
            precision_mode: str = 'int'
        else:
            abs_delta = abs(delta)
            if abs_delta >= 2:
                precision_mode = 'int'
            elif abs_delta >= 0.5:
                precision_mode = 'tenths'
            elif abs_delta > 0:
                precision_mode = 'hundredths'
            else:
                prev_prec = 'int'
                if prev and prev.get('precision'):
                    prev_prec = str(prev.get('precision'))
                precision_mode = prev_prec
        # Escalate if near boundary
        if dist_to_boundary < 1 and precision_mode == 'int':
            precision_mode = 'tenths'
        if dist_to_boundary < 0.4 and precision_mode in ('int', 'tenths'):
            precision_mode = 'hundredths'
        # Apply rounding per precision mode
        if precision_mode == 'int':
            score = round(raw_score)
        elif precision_mode == 'tenths':
            score = round(raw_score, 1)
        elif precision_mode == 'hundredths':
            score = round(raw_score, 2)
        else:  # synthetic_quantum future
            score = round(raw_score, 3)
            precision_mode = 'synthetic_quantum'
        fm.criticality_score = score
        fm.synthetic_precision = str(precision_mode)
        fm.tier = assign_tier(fm.criticality_score)
        if fm.coverage_pct >= 80:
            fm.coverage_band = 'high'
        elif fm.coverage_pct >= 50:
            fm.coverage_band = 'medium'
        else:
            fm.coverage_band = 'low'
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with INDEX_PATH.open('w', encoding='utf-8') as handle:
        for fm in sorted(metrics.values(), key=lambda x: -x.criticality_score):
            handle.write(json.dumps(asdict(fm), ensure_ascii=False) + '\n')
    TELEMETRY_OUT.parent.mkdir(parents=True, exist_ok=True)
    snapshot = {
        'generated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'file_count': len(metrics),
        'top10': [
            asdict(fm)
            for fm in sorted(
                metrics.values(), key=lambda x: -x.criticality_score
            )[:10]
        ],
    }
    TELEMETRY_OUT.write_text(json.dumps(snapshot, indent=2), encoding='utf-8')
    print(
        f"Generated scores for {len(metrics)} files; index at {INDEX_PATH}"
    )


if __name__ == '__main__':
    main()
