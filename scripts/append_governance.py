#!/usr/bin/env python3
"""
append_governance.py

Append a governance entry to docs/GOVERNANCE_CHANGELOG.md using CLI args.

Usage:
  python scripts/append_governance.py --title "Title" --author "@me" --files "path1,path2" --owner "@team" --affected "fileA,fileB" --alternatives "explain" --benefits "one;two" --risks "one;two" --effort "1h" --expiry "2026-01-01" --approval "# APPROVED: reason" --notes "any notes"

The script appends a formatted block to the changelog.
"""
import argparse
from pathlib import Path
from datetime import datetime


TEMPLATE = """
---
Date: {date}
Author: {author}
Title: {title}
Files: {files}
Owner: {owner}
Affected: {affected}
Alternatives: {alternatives}
Benefits:
{benefits}
Risks:
{risks}
Estimated Effort: {effort}
Expiry (if experimental): {expiry}
Approval: {approval}
Notes: {notes}
---

"""


def format_list_field(s, sep=';'):
    if not s:
        return ''
    parts = [p.strip() for p in s.split(sep) if p.strip()]
    return '\n'.join([f'- {p}' for p in parts])


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--title', required=True)
    p.add_argument('--author', required=True)
    p.add_argument('--files', default='')
    p.add_argument('--owner', default='')
    p.add_argument('--affected', default='')
    p.add_argument('--alternatives', default='')
    p.add_argument('--benefits', default='')
    p.add_argument('--risks', default='')
    p.add_argument('--effort', default='')
    p.add_argument('--expiry', default='')
    p.add_argument('--approval', default='')
    p.add_argument('--notes', default='')
    args = p.parse_args()

    changelog = Path('docs') / 'GOVERNANCE_CHANGELOG.md'
    if not changelog.exists():
        print('ERROR: docs/GOVERNANCE_CHANGELOG.md not found')
        raise SystemExit(2)

    entry = TEMPLATE.format(
        date=datetime.utcnow().date().isoformat(),
        author=args.author,
        title=args.title,
        files=args.files,
        owner=args.owner,
        affected=args.affected,
        alternatives=args.alternatives,
        benefits=format_list_field(args.benefits, sep=';') or '- None',
        risks=format_list_field(args.risks, sep=';') or '- None',
        effort=args.effort,
        expiry=args.expiry,
        approval=args.approval,
        notes=args.notes,
    )

    with changelog.open('a', encoding='utf-8') as fh:
        fh.write('\n')
        fh.write(entry)

    print('Appended governance entry to', changelog)


if __name__ == '__main__':
    main()
