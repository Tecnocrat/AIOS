#!/usr/bin/env python3
"""Analyze MSFT ingestion content for refactoring."""
import json
from pathlib import Path
from collections import defaultdict

base = Path('c:/dev/aios/docs/distilled/microsoft/release_notes')
categories = ['agentic_windows', 'azure_ai_foundry', 'developer_tools', 'dotnet_evolution']

# Collect all items across all dates
all_items = {}
items_by_category = defaultdict(list)
files_by_category = defaultdict(list)

for cat in categories:
    cat_dir = base / cat
    if not cat_dir.exists():
        print(f"Category {cat}: NOT FOUND")
        continue
    
    json_files = list(cat_dir.glob('*_index.json'))
    md_files = list(cat_dir.glob('*_updates.md'))
    files_by_category[cat] = {'json': len(json_files), 'md': len(md_files)}
    
    for f in json_files:
        items = json.loads(f.read_text())
        for item in items:
            h = item['hash']
            if h not in all_items:
                all_items[h] = {'item': item, 'files': [str(f.name)], 'category': cat}
            else:
                all_items[h]['files'].append(str(f.name))
            items_by_category[cat].append(h)

print("=" * 60)
print("MSFT INGESTION ANALYSIS REPORT")
print("=" * 60)

print(f"\n📊 SUMMARY")
print(f"   Total unique articles: {len(all_items)}")
print(f"   Categories: {len([c for c in categories if (base/c).exists()])}")

print(f"\n📁 FILES PER CATEGORY")
for cat, counts in files_by_category.items():
    print(f"   {cat}: {counts['json']} JSON, {counts['md']} MD files")

print(f"\n🔄 DUPLICATION ANALYSIS")
duplicated = [(h, data) for h, data in all_items.items() if len(data['files']) > 1]
print(f"   Items appearing in multiple files: {len(duplicated)}/{len(all_items)}")

if duplicated:
    print(f"\n   Duplicated items:")
    for h, data in duplicated[:10]:
        title = data['item']['title'][:45]
        print(f"   - '{title}...' in {len(data['files'])} files")

print(f"\n📰 UNIQUE ARTICLES BY CATEGORY")
for cat in categories:
    unique_in_cat = set(items_by_category[cat])
    print(f"   {cat}: {len(unique_in_cat)} unique articles")

print(f"\n📅 CONTENT BY DATE")
dates = set()
for cat in categories:
    cat_dir = base / cat
    if cat_dir.exists():
        for f in cat_dir.glob('*_index.json'):
            date = f.stem.replace('_index', '')
            dates.add(date)

for date in sorted(dates):
    count = 0
    for cat in categories:
        f = base / cat / f"{date}_index.json"
        if f.exists():
            count += len(json.loads(f.read_text()))
    print(f"   {date}: {count} items")

print("\n" + "=" * 60)
