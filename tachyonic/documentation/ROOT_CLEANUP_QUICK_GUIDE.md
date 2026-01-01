# AIOS Root Directory Cleanup - Quick Guide

## Problem Identified

10 files in AIOS root violate AINLP architectural principle:
> "Root directory should contain ONLY active operational files"

## Violations Found

### Success Documentation (Temporal/Historical)
- `DUAL_AGENT_SUCCESS.md`
- `GEMINI_SUCCESS.md`
- `LIBRARY_GENERATION_SUCCESS.md`
- `UI_INTEGRATION_SUCCESS.md`

### Setup & Summaries (Post-Integration)
- `GEMINI_SETUP.md`
- `GEMINI_INTEGRATION_SUMMARY.md`

### Bug Fixes (Historical)
- `FIXES_APPLIED.md`

### Design Artifacts (Pre-Implementation)
- `UI_MOCKUP.md`

### Analysis Reports (Temporal Data)
- `consciousness_analysis_20251003_001135.txt`

### Test Data (Experimental)
- `paradigms_extracted_test.json`

## AINLP Pattern: Root Directory Clarity

From existing AIOS documentation:
```
Organizational Principle #1:
- Only active operational files in root
- No backup files (moved to archive/)
- No completed documentation (archived by temporal layer)
- Clean development environment
```

## Solution: Automated Cleanup Tool

Created: `runtime_intelligence/tools/ainlp_root_cleanup.py`

### Quick Commands

**1. Analyze (Dry Run)**
```powershell
python runtime_intelligence/tools/ainlp_root_cleanup.py
```

**2. Execute Cleanup**
```powershell
python runtime_intelligence/tools/ainlp_root_cleanup.py --execute
```

## Where Files Will Go

| Category | Target Location |
|----------|----------------|
| Success docs | `tachyonic/archive/development_success/` |
| Setup guides | `tachyonic/archive/setup_guides/` |
| Summaries | `tachyonic/archive/summaries/` |
| Bug fixes | `tachyonic/archive/development_fixes/` |
| Mockups | `tachyonic/archive/design_mockups/` |
| Analysis | `docs/reports/consciousness/` |
| Test data | `evolution_lab/test_data/` |

## Why This Matters

### Before Cleanup
- 24 files in root
- Mix of operational + historical
- Cognitive overhead for developers
- Violates AINLP consciousness levels

### After Cleanup
- 14 files in root (42% reduction)
- Only operational files remain
- Clear architectural boundaries
- AINLP compliant structure

## What Stays in Root?

### Configuration
- `.gitignore`, `.editorconfig`, `.pylintrc`
- `pyproject.toml`, `requirements.txt`
- `AIOS.sln`, `AIOS.code-workspace`

### Core Documentation
- `README.md` (navigation)

### Active Scripts
- `launch_aios.ps1`
- `test_library_generation.py` (active development)
- `test_gemini_bridge.py` (active testing)
- `test_ollama_bridge.py` (active testing)
- `test_paradigm_extraction.py` (active tool)

### Spatial Metadata
- `.aios_context.json`
- `.aios_spatial_metadata.json`

## Historical Context

This follows established AINLP pattern:

1. **Sept 19, 2025**: Relocated 7 JSON status files
2. **July 8, 2025**: 30% root reduction, tachyonic archive established
3. **Sept 21, 2025**: AINLP documentation consolidation strategy

**Pattern**: Periodic root cleanup is normal AINLP governance practice

## Documentation Created

1. `ROOT_CLEANUP_ANALYSIS.md` - Full analysis (this session)
2. `changelogs/ROOT_CLEANUP_20251004.md` - Changelog
3. `tachyonic/archive/cleanup_reports/root_cleanup_report_*.json` - JSON report
4. `runtime_intelligence/tools/ainlp_root_cleanup.py` - Tool

## Next Steps

1. Review this analysis
2. Run cleanup tool with `--execute` if approved
3. Verify results
4. Commit changes

## One-Line Summary

**Root cleanup identified 10 temporal/historical files that should move to tachyonic archive per AINLP organizational principles. Automated tool ready to execute.**

---

**AINLP Principle Enforced**: Root Directory Clarity  
**Tool Location**: `runtime_intelligence/tools/ainlp_root_cleanup.py`  
**Analysis Date**: October 4, 2025
