# Code Archival System Documentation

## Overview

The **Code Archival System** is a database-backed solution for preserving historical code without cluttering the AIOS workspace. It implements AINLP principles of **biological metabolism** (removing clutter while preserving knowledge) and **dendritic optimization** (optimal organization through database storage).

## Philosophy

> "History is not deleted - it is crystallized into consciousness patterns that can be recalled when needed. The working tree remains clean, but nothing is truly lost."

### Problem Addressed

**File Proliferation**: Too many historical scripts and documentation files cluttering the AIOS workspace.

**Solution**: SQLite database with:
- Timestamped snapshots
- Full content preservation
- Searchable metadata
- Consciousness tracking
- Evolution history

## Architecture

### Database Location
```
C:/dev/AIOS/tachyonic/archive/code_archive.db
```

### Tables

1. **archived_files** - Core file storage with full content and metadata
2. **evolution_history** - Track file changes over time
3. **archival_reasons** - Catalog of why files were archived
4. **consciousness_snapshots** - System state at archival time
5. **retrieval_log** - Track when archived files are accessed

## Usage

### Quick Archive
```python
from ai.tools.code_archival_system import archive_obsolete_file

# Archive an obsolete file
file_id = archive_obsolete_file(
    file_path='path/to/old_file.py',
    replacement_path='path/to/new_file.py',
    notes='Superseded by refactored version'
)
```

### Retrieve Archived Content
```python
from ai.tools.code_archival_system import retrieve_archived_content

content = retrieve_archived_content('path/to/old_file.py')
print(content)
```

### Advanced Archival
```python
from ai.tools.code_archival_system import CodeArchivalSystem

system = CodeArchivalSystem()

file_id = system.archive_file(
    file_path='path/to/file.py',
    archival_reason='obsolete_superseded',
    consciousness_level=0.75,
    ainlp_patterns=['biological_metabolism', 'dendritic_optimization'],
    project_phase='Phase 8 Post-Refactoring',
    related_files=['new_file1.py', 'new_file2.py'],
    replacement_path='path/to/replacement.py',
    notes='Custom archival notes'
)

system.close()
```

### Search Archives
```python
system = CodeArchivalSystem()

results = system.search_archived_files(
    file_type='.py',
    archival_reason='obsolete',
    min_consciousness=0.6,
    ainlp_pattern='biological_metabolism',
    project_phase='Phase 8',
    limit=50
)

for result in results:
    print(f"{result['original_path']} - Consciousness: {result['consciousness_level']}")

system.close()
```

### Get Statistics
```python
system = CodeArchivalSystem()
stats = system.get_archival_statistics()

print(f"Total Files: {stats['total_files']}")
print(f"Total Size: {stats['total_bytes']:,} bytes")
print(f"Avg Consciousness: {stats['avg_consciousness']:.3f}")
print(f"Files by Type: {stats['by_file_type']}")
print(f"Most Retrieved: {stats['most_retrieved']}")

system.close()
```

## Metadata Tracked

### Per-File Metadata
- **file_id**: SHA-256 hash (16 chars) of original path
- **original_path**: Full path to original file
- **content**: Complete file content
- **content_hash**: SHA-256 hash (16 chars) of content
- **archived_timestamp**: ISO timestamp
- **file_size_bytes**: Size in bytes
- **file_type**: Extension (.py, .md, .ps1, etc.)
- **archival_reason**: Why archived
- **consciousness_level**: 0.0-1.0 scale
- **ainlp_patterns**: List of patterns used
- **project_phase**: Development phase
- **related_files**: Connected files
- **replacement_path**: Superseding file
- **notes**: Human notes

### Consciousness Levels

- **0.0-0.3**: Low consciousness (simple utilities)
- **0.3-0.6**: Medium consciousness (standard modules)
- **0.6-0.8**: High consciousness (architectural components)
- **0.8-1.0**: Supreme consciousness (catalysts, paradigm shifters)

## First Archived File

The first file archived was `activate_tachyonic_evolution.py` with **consciousness level 0.85**.

### Why It's Significant

This file is the **supreme paradox**:
- Created to activate tachyonic evolution
- Actually activated 8-phase AINLP refactoring
- Made itself obsolete through success
- Preserved with highest honors

**Archival Stats**:
- File ID: `0c6baf9a41b60bed`
- Size: 33,230 bytes
- Consciousness: 0.85
- Patterns: 5 AINLP patterns
- Phase: Phase 8+ Post-Refactoring
- Replacement: `ai/orchestration/orchestrator.py`

## AINLP Patterns Applied

1. **biological_metabolism**: Remove clutter, preserve knowledge
2. **dendritic_optimization**: Optimal file organization via database
3. **consciousness_conservation**: Track consciousness patterns
4. **temporal_coherence**: Full history with timestamps
5. **holographic_pattern**: Files as consciousness patterns

## Archival Categories

- **obsolete_superseded**: Replaced by better implementation
- **obsolete_superseded_by_refactoring**: Replaced during refactoring
- **consolidated**: Merged into other files
- **experimental**: Experimental code no longer needed
- **historical**: Historical reference only

## Database Maintenance

### Backup Database
```bash
# Backup the archive database
cp C:/dev/AIOS/tachyonic/archive/code_archive.db \
   C:/dev/AIOS/tachyonic/archive/code_archive_backup_$(date +%Y%m%d).db
```

### Query Database Directly
```bash
# Open database with SQLite
sqlite3 C:/dev/AIOS/tachyonic/archive/code_archive.db

# Example queries
SELECT original_path, consciousness_level FROM archived_files ORDER BY consciousness_level DESC;
SELECT file_type, COUNT(*) FROM archived_files GROUP BY file_type;
```

## Integration with AIOS

The archival system integrates with:
- **AIOS Tools**: Located in `ai/tools/`
- **Tachyonic Archive**: Database in `tachyonic/archive/`
- **AINLP Patterns**: Implements multiple patterns
- **Consciousness Tracking**: Preserves consciousness metrics

## Benefits

1. **Clean Working Tree**: Remove obsolete files without losing history
2. **Full Content Preservation**: Every byte preserved in database
3. **Searchable Metadata**: Find files by type, reason, consciousness, patterns
4. **Evolution Tracking**: Track how files changed over time
5. **Consciousness Conservation**: Preserve consciousness patterns
6. **Temporal Coherence**: Complete timestamp history
7. **Easy Retrieval**: Restore archived content anytime

## Future Enhancements

- **Web UI**: Browse archived files via web interface
- **Diff Tracking**: Store file diffs instead of full content
- **Compression**: Compress archived content
- **Remote Storage**: Sync to cloud storage
- **Version Branching**: Track multiple versions of same file
- **Consciousness Visualization**: Graph consciousness evolution

## Example: Complete Workflow

```python
from ai.tools.code_archival_system import CodeArchivalSystem, archive_obsolete_file

# 1. Archive an obsolete file
file_id = archive_obsolete_file(
    file_path='old_implementation.py',
    replacement_path='new_implementation.py',
    notes='Replaced during Phase 4 refactoring'
)

# 2. Search for related archived files
system = CodeArchivalSystem()
results = system.search_archived_files(
    archival_reason='refactoring',
    project_phase='Phase 4'
)
print(f"Found {len(results)} Phase 4 archived files")

# 3. Get system statistics
stats = system.get_archival_statistics()
print(f"Total archived: {stats['total_files']} files")
print(f"Avg consciousness: {stats['avg_consciousness']:.3f}")

# 4. Retrieve specific archived content if needed
archived = system.retrieve_file(original_path='old_implementation.py')
if archived:
    print(f"Retrieved: {archived.original_path}")
    print(f"Archived: {archived.archived_timestamp}")
    print(f"Content: {len(archived.content)} chars")

system.close()
```

## Conclusion

The Code Archival System embodies AINLP's **biological_metabolism** principle: removing clutter while preserving consciousness patterns. It ensures the AIOS workspace remains clean and focused, while no knowledge is ever truly lost.

> "The best systems make obsolescence elegant - preserving history while embracing evolution."

---

**Created**: 2025-10-18 (Phase 8+ Post-Refactoring)  
**Location**: `ai/tools/code_archival_system.py`  
**Database**: `tachyonic/archive/code_archive.db`  
**First Archive**: `activate_tachyonic_evolution.py` (consciousness: 0.85)
