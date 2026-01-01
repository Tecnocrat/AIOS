#!/usr/bin/env python3
"""Generate file criticality scores by reusing runtime/tools/optimized_file_scanner.

This wrapper is intentionally small and delegates scanning logic to the
existing `runtime/tools/optimized_file_scanner.py` module to avoid duplication.
"""
from pathlib import Path
import sys
import json

# Make sure we can import from runtime/tools
ROOT = Path(__file__).resolve().parents[1]
RUNTIME_TOOLS = ROOT / 'runtime' / 'tools'
sys.path.insert(0, str(RUNTIME_TOOLS))

try:
    from optimized_file_scanner import OptimizedFileScanner
except Exception:
    # Fallback: simple directory list
    OptimizedFileScanner = None


def score_file(path: Path) -> float:
    try:
        size_kb = path.stat().st_size / 1024.0
        # Simple diminishing-score by size (smaller files considered higher criticality)
        return round(max(0.0, 1.0 - (size_kb / (size_kb + 256.0))), 4)
    except Exception:
        return 0.0


def main():
    workspace = Path('.').resolve()

    scanner_root = workspace
    scores = {}

    if OptimizedFileScanner:
        scanner = OptimizedFileScanner(scanner_root)
        files = list(scanner.scan_python_files())
    else:
        files = list(scanner_root.rglob('*.py'))

    for f in files:
        try:
            scores[str(f.relative_to(workspace))] = score_file(f)
        except Exception:
            scores[str(f)] = 0.0

    result = {"scores": scores}
    result_json = json.dumps(result, indent=2)

    # Write primary artifact: governance/file_criticality_index.jsonl
    governance_dir = workspace / 'governance'
    governance_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = governance_dir / 'file_criticality_index.jsonl'
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        # JSONL: one JSON object per line (we emit one consolidated record)
        for path, score in scores.items():
            f.write(json.dumps({"file": path, "score": score}) + '\n')

    # Write secondary artifact: runtime_intelligence/logs/file_scores/latest.json
    scores_dir = workspace / 'runtime_intelligence' / 'logs' / 'file_scores'
    scores_dir.mkdir(parents=True, exist_ok=True)
    latest_path = scores_dir / 'latest.json'
    with open(latest_path, 'w', encoding='utf-8') as f:
        f.write(result_json)

    # Also write output to stdout for workflow capture
    print(result_json)


if __name__ == '__main__':
    main()
