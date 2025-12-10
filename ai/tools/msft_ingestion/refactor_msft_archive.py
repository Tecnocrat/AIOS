#!/usr/bin/env python3
"""
MSFT Ingestion Refactoring Tool
================================

Consolidates duplicate daily files into a clean archive structure:
- Creates a master index with all unique articles
- Archives by month instead of day (reduces file proliferation)
- Generates clean category summaries

Usage:
    python scripts/refactor_msft_archive.py
"""
import json
import shutil
from datetime import datetime
from pathlib import Path
from collections import defaultdict

BASE = Path('c:/dev/aios/docs/distilled/microsoft/release_notes')
ARCHIVE_DIR = BASE / 'archive'
CATEGORIES = ['agentic_windows', 'azure_ai_foundry', 'developer_tools', 'dotnet_evolution']


def collect_all_unique_items():
    """Collect all unique items across all files."""
    unique_items = {}  # hash -> item data
    
    for cat in CATEGORIES:
        cat_dir = BASE / cat
        if not cat_dir.exists():
            continue
            
        for f in cat_dir.glob('*_index.json'):
            items = json.loads(f.read_text())
            for item in items:
                h = item['hash']
                if h not in unique_items:
                    # Add metadata about when first seen
                    date_str = f.stem.replace('_index', '')
                    item['first_seen'] = date_str
                    item['ingestion_file'] = f.name
                    unique_items[h] = item
    
    return unique_items


def create_master_index(unique_items: dict):
    """Create a single master index of all articles."""
    # Group by category
    by_category = defaultdict(list)
    for item in unique_items.values():
        by_category[item['category']].append(item)
    
    # Sort each category by published date (newest first)
    for cat in by_category:
        by_category[cat].sort(key=lambda x: x.get('published', ''), reverse=True)
    
    return dict(by_category)


def generate_master_markdown(by_category: dict) -> str:
    """Generate consolidated master markdown."""
    total = sum(len(items) for items in by_category.values())
    timestamp = datetime.utcnow().isoformat()
    
    md = f"""# Microsoft Frontier Knowledge Base

> **Total Articles**: {total}
> **Categories**: {len(by_category)}
> **Last Consolidated**: {timestamp}
> **AINLP.dendritic**: MSFT knowledge archive

---

## Quick Stats

| Category | Articles | Priority |
|----------|----------|----------|
"""
    
    for cat, items in sorted(by_category.items()):
        high_priority = len([i for i in items if i.get('priority') == 'high'])
        md += f"| {cat.replace('_', ' ').title()} | {len(items)} | {high_priority} high |\n"
    
    md += "\n---\n\n"
    
    # Category sections
    for cat, items in sorted(by_category.items()):
        md += f"## {cat.replace('_', ' ').title()}\n\n"
        
        for item in items[:10]:  # Top 10 per category
            title = item['title']
            url = item['url']
            source = item['source']
            summary = item.get('summary', '')[:200]
            
            md += f"### [{title}]({url})\n\n"
            md += f"**Source**: {source} | **First Seen**: {item.get('first_seen', 'unknown')}\n\n"
            if summary:
                md += f"{summary}...\n\n"
            md += "---\n\n"
        
        if len(items) > 10:
            md += f"*...and {len(items) - 10} more articles in this category*\n\n"
    
    md += f"\n---\n\n*Consolidated from AIOS Microsoft Frontier Ingestion*\n"
    
    return md


def archive_old_files():
    """Move old daily files to archive directory."""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    archived = 0
    for cat in CATEGORIES:
        cat_dir = BASE / cat
        if not cat_dir.exists():
            continue
        
        archive_cat = ARCHIVE_DIR / cat
        archive_cat.mkdir(parents=True, exist_ok=True)
        
        for f in list(cat_dir.glob('2025-*')):  # Archive all dated files
            dest = archive_cat / f.name
            shutil.move(str(f), str(dest))
            archived += 1
    
    return archived


def create_category_summaries(by_category: dict):
    """Create clean per-category summary files."""
    for cat, items in by_category.items():
        cat_dir = BASE / cat
        cat_dir.mkdir(parents=True, exist_ok=True)
        
        # JSON index (all items)
        index_file = cat_dir / 'index.json'
        index_file.write_text(json.dumps(items, indent=2))
        
        # Markdown summary
        md_file = cat_dir / 'README.md'
        md_content = f"""# {cat.replace('_', ' ').title()}

> **Articles**: {len(items)}
> **Source**: Microsoft Frontier Ingestion

---

"""
        for item in items:
            md_content += f"- [{item['title']}]({item['url']}) - {item['source']}\n"
        
        md_file.write_text(md_content, encoding='utf-8')
        
        print(f"  ✓ {cat}: {len(items)} articles")


def main():
    print("=" * 60)
    print("MSFT INGESTION REFACTORING")
    print("=" * 60)
    
    # Step 1: Collect unique items
    print("\n📥 Collecting unique articles...")
    unique_items = collect_all_unique_items()
    print(f"   Found {len(unique_items)} unique articles")
    
    # Step 2: Create master index
    print("\n📊 Creating master index...")
    by_category = create_master_index(unique_items)
    
    # Step 3: Archive old files
    print("\n📦 Archiving old daily files...")
    archived = archive_old_files()
    print(f"   Archived {archived} files to {ARCHIVE_DIR}")
    
    # Step 4: Generate new structure
    print("\n📝 Generating consolidated structure...")
    create_category_summaries(by_category)
    
    # Step 5: Create master markdown
    master_md = generate_master_markdown(by_category)
    master_file = BASE / 'KNOWLEDGE_BASE.md'
    master_file.write_text(master_md, encoding='utf-8')
    print(f"\n✓ Master index: {master_file}")
    
    # Step 6: Create combined JSON
    combined_json = BASE / 'all_articles.json'
    combined_json.write_text(json.dumps(list(unique_items.values()), indent=2))
    print(f"✓ Combined JSON: {combined_json}")
    
    print("\n" + "=" * 60)
    print("REFACTORING COMPLETE")
    print("=" * 60)
    print(f"""
New structure:
  {BASE}/
  ├── KNOWLEDGE_BASE.md      # Master human-readable index
  ├── LATEST_UPDATES.md      # Daily updates (workflow maintains this)
  ├── all_articles.json      # All articles in one file
  ├── archive/               # Historical daily files
  │   ├── agentic_windows/
  │   ├── azure_ai_foundry/
  │   └── ...
  └── [category]/
      ├── index.json         # Category articles
      └── README.md          # Category summary
""")


if __name__ == "__main__":
    main()
