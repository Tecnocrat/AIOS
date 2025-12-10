"""
AIOS Microsoft Frontier Ingestion Module
=========================================

AINLP.dendritic[ai/tools/msft_ingestion]{frontier,microsoft,rss,distillation}

Unified module for Microsoft ecosystem knowledge ingestion:
- RSS/Atom feed fetching from Windows Dev, Azure AI, .NET, VS Code, GitHub blogs
- Content distillation and crystallization
- Archive refactoring and deduplication
- Master index generation

Components:
-----------
- msft_feed_fetcher.py     : GitHub Actions feed fetcher (scheduled daily)
- msft_distillation_bridge.py : Full distillation with VOID Bridge integration
- analyze_msft_ingestion.py   : Content analysis and duplication detection
- refactor_msft_archive.py    : Archive consolidation tool
- rebuild_master_index.py     : Regenerate KNOWLEDGE_BASE.md from indexes

Output Location:
----------------
docs/distilled/microsoft/release_notes/
├── KNOWLEDGE_BASE.md      # Master human-readable index
├── all_articles.json      # Combined article database
├── archive/               # Historical daily files
└── [category]/
    ├── index.json         # Category articles
    └── README.md          # Category summary

GitHub Workflow:
----------------
.github/workflows/msft-frontier-ingestion.yml
- Schedule: Daily at 6 AM UTC
- Trigger: Manual dispatch available
"""

__version__ = "1.0.0"
__author__ = "AIOS"
