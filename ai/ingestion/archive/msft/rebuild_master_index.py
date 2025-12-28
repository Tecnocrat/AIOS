#!/usr/bin/env python3
"""Rebuild KNOWLEDGE_BASE.md from category indexes."""

import json
from pathlib import Path
from datetime import datetime

base = Path(r'c:\dev\aios\docs\distilled\microsoft\release_notes')
categories = ['agentic_windows', 'azure_ai_foundry', 'developer_tools', 'dotnet_evolution']

# Collect all articles from category indexes
all_articles = []
stats = {}

for cat in categories:
    idx_file = base / cat / 'index.json'
    if idx_file.exists():
        items = json.loads(idx_file.read_text(encoding='utf-8'))
        all_articles.extend(items)
        stats[cat] = len(items)
        print(f'{cat}: {len(items)} articles')

# Write combined JSON
(base / 'all_articles.json').write_text(json.dumps(all_articles, indent=2), encoding='utf-8')
print(f'\nTotal: {len(all_articles)} articles in all_articles.json')

# Update KNOWLEDGE_BASE.md
priority_map = {
    'agentic_windows': 'high', 
    'azure_ai_foundry': 'high', 
    'developer_tools': 'medium', 
    'dotnet_evolution': 'medium'
}

md_lines = [
    '# Microsoft Frontier Knowledge Base',
    '',
    f'> **Total Articles**: {len(all_articles)}',
    f'> **Categories**: {len(stats)}',
    f'> **Last Consolidated**: {datetime.utcnow().isoformat()}',
    '> **AINLP.dendritic**: MSFT knowledge archive',
    '',
    '---',
    '',
    '## Quick Stats',
    '',
    '| Category | Articles | Priority |',
    '|----------|----------|----------|',
]

for cat, count in stats.items():
    md_lines.append(f'| {cat.replace("_", " ").title()} | {count} | {priority_map.get(cat, "medium")} |')

md_lines.extend(['', '---', ''])

# Add article listing per category
for cat in categories:
    if cat in stats:
        md_lines.append(f'## {cat.replace("_", " ").title()}')
        md_lines.append('')
        idx_file = base / cat / 'index.json'
        items = json.loads(idx_file.read_text(encoding='utf-8'))
        for item in items:
            md_lines.append(f"- [{item['title']}]({item['url']}) - {item['source']}")
        md_lines.append('')

md_lines.extend(['---', '', '*Consolidated from AIOS Microsoft Frontier Ingestion*'])
(base / 'KNOWLEDGE_BASE.md').write_text('\n'.join(md_lines), encoding='utf-8')
print('Updated KNOWLEDGE_BASE.md')
