"""Baseline test for taxonomy_extraction.

Validates that running taxonomy_extraction:
 - Produces taxonomy_baseline.json
 - Produces at least one phase1b_taxonomy_baseline_* crystal
 - Inserts signature_dictionary_size into Phase 1B revision placeholder
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
CTX = ROOT / 'AIOS_PROJECT_CONTEXT.md'
OUT = ROOT / 'runtime' / 'context'
CRYSTALS = OUT / 'crystals'


def run_script() -> None:
    subprocess.check_call([
        sys.executable,
        str(ROOT / 'scripts' / 'taxonomy_extraction.py')
    ])


def assert_file(path: Path) -> None:
    if not path.exists():
        raise AssertionError(f'Missing expected file: {path}')


def test_taxonomy_baseline():  # simple invocation style
    run_script()
    baseline = OUT / 'taxonomy_baseline.json'
    assert_file(baseline)
    # crystal presence with regex validation (timestamp pattern)
    crystals = list(CRYSTALS.glob('phase1b_taxonomy_baseline_*.json'))
    assert crystals, 'No taxonomy baseline crystals created'
    crystal_names = [c.name for c in crystals]
    timestamp_re = re.compile(r'^phase1b_taxonomy_baseline_\d{8}_\d{6}\.json$')
    assert any(
        timestamp_re.match(n) for n in crystal_names
    ), 'Crystal filename pattern mismatch'
    # revision metrics inserted
    text = CTX.read_text(encoding='utf-8')
    assert (
        'signature_dictionary_size:' in text
    ), 'Revision metrics not inserted'
    # sanity: pattern_count key present
    import json
    data = json.loads(baseline.read_text(encoding='utf-8'))
    assert 'pattern_count' in data and isinstance(data['pattern_count'], int)
    # Extended metrics present
    assert 'taxonomy_coverage_pct' in data, 'Missing taxonomy_coverage_pct'
    assert (
        'predictive_precision_baseline_pct' in data
    ), 'Missing predictive precision baseline'
    assert data['taxonomy_coverage_pct'] >= 0.0
    assert 0.0 <= data['predictive_precision_baseline_pct'] <= 100.0
    print('[test] taxonomy baseline OK patterns=', data['pattern_count'])


if __name__ == '__main__':
    test_taxonomy_baseline()
