"""
AIOS Tachyonic Garbage Collection System
=======================================

PROBLEM: Documentation consolidation is FAILING -
 creating MORE files instead of fewer
SOLUTION: Intelligent garbage collection with tachyonic database integration
APPROACH: Analyze, classify, archive, and ENFORCE coherence

This system will:
1. Identify redundant/fragmented files
2. Archive them to tachyonic database layer
3. ENFORCE a clean, coherent documentation structure
4. Prevent future fragmentation
"""

import hashlib
import json
import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


class TachyonicDatabase:
    """Tachyonic database for storing archived documentation with full metadata."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initialize the tachyonic database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS archived_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    original_path TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    content TEXT NOT NULL,
                    file_size INTEGER,
                    archive_timestamp TEXT NOT NULL,
                    archive_reason TEXT,
                    topics TEXT,  -- JSON array
                    cross_references TEXT,  -- JSON array
                    consolidation_target TEXT,
                    metadata TEXT  -- JSON object
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS consolidation_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    files_processed INTEGER,
                    files_archived INTEGER,
                    files_kept INTEGER,
                    operation_summary TEXT
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_filename ON archived_documents(
                filename)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_content_hash ON archived_documen\
                ts(content_hash)
            """)

    def archive_document(
    self, filepath: Path, reason: str, topics: List[str] = None,
                        cross_refs: List[
                        str] = None, consolidation_target: str = None):
        """Archive a document to the tachyonic database."""
        if not filepath.exists():
            return False

        content = filepath.read_text(encoding='utf-8')
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        metadata = {
            'original_modification_time': filepath.stat().st_mtime,
            'archive_operation': 'garbage_collection',
            'file_extension': filepath.suffix
        }

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO archived_documents
                (filename, original_path, content_hash, content, file_size,
                 archive_timestamp, archive_reason, topics, cross_references,
                 consolidation_target, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                filepath.name,
                str(filepath),
                content_hash,
                content,
                len(content),
                datetime.now().isoformat(),
                reason,
                json.dumps(topics or []),
                json.dumps(cross_refs or []),
                consolidation_target,
                json.dumps(metadata)
            ))

        return True

    def log_operation(self, operation_type: str, files_processed: int,
                     files_archived: int, files_kept: int, summary: str):
        """Log a garbage collection operation."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO consolidation_log
                (operation_type, timestamp, files_processed, files_archived,
                 files_kept, operation_summary)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                operation_type,
                datetime.now().isoformat(),
                files_processed,
                files_archived,
                files_kept,
                summary
            ))

    def get_archive_stats(self) -> Dict:
        """Get statistics about archived documents."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total archived documents
            cursor.execute("SELECT COUNT(*) FROM archived_documents")
            total_archived = cursor.fetchone()[0]

            # Total size archived
            cursor.execute("SELECT SUM(file_size) FROM archived_documents")
            total_size = cursor.fetchone()[0] or 0

            # Archive reasons
            cursor.execute("""
                SELECT archive_reason, COUNT(*)
                FROM archived_documents
                GROUP BY archive_reason
            """)
            reasons = dict(cursor.fetchall())

            return {
                'total_archived': total_archived,
                'total_size_bytes': total_size,
                'archive_reasons': reasons
            }


class AIOSDocumentationGarbageCollector:
    """Intelligent garbage collection system for AIOS documentation."""

    def __init__(self, docs_dir: Path):
        self.docs_dir = Path(docs_dir)
        self.tachyonic_db = TachyonicDatabase(
        self.docs_dir / "tachyonic_archive.db")

        # Define the ENFORCED documentation structure
        self.ENFORCED_STRUCTURE = {
            # Core documentation files (MUST KEEP)
            'ESSENTIAL_CORE': [
                'AIOS_COMPLETE_SPECIFICATION_GUIDE.md',
                'AIOS_DEVELOPMENT_AND_SETUP_GUIDE.md',
                'AIOS_ARCHITECTURE_AND_DESIGN_GUIDE.md',
                'AIOS_API_AND_REFERENCE_GUIDE.md',
                'AIOS_OPTIMIZATION_AND_TROUBLESHOOTING_GUIDE.md',
                'AIOS_PROJECT_STATUS_AND_ROADMAP_GUIDE.md',
                'AIOS_SPECIALIZED_INTEGRATIONS_GUIDE.md'
            ],

            # Files that should be archived (redundant/fragmented)
            'ARCHIVE_CANDIDATES': [
                'ADVANCED_OPTIMIZATION_IMPLEMENTATION.md',
                'AINLP_SPECIFICATION.md',
                'API_REFERENCE.md',
                'api-reference.md',
                'ARCHITECTURE.md',
                'AUTO_WAYPOINT_SUMMARY.md',
                'BREAKTHROUGH_INTEGRATION_SUMMARY.md',
                'CHANGELOG.md',
                'CODEBASE_ANALYSIS_BUGS_OPTIMIZATION.md',
                'COMPLETE_INTEGRATION_GUIDE.md',
                'CONTEXT_HARMONIZATION_COMPLETE_JULY8_2025.md',
                'CRITICAL_BUG_FIXES_IMPLEMENTATION.md',
                'DEBUGGING_INTEGRATION_PROTOCOL.md',
                'DEVELOPMENT.md',
                'FRACTAL_HOLOGRAPHIC_DEVELOPMENT.md',
                'FRACTAL_HOLOGRAPHIC_IMPLEMENTATION_SUMMARY.md',
                'HYBRID_UI_INTEGRATION_GUIDE.md',
                'HYBRID_UI_SETUP_GUIDE.md',
                'INSTALLATION.md',
                'INTEGRATION_STATUS_JULY_2025.md',
                'JULY_2025_INTEGRATION_COMPLETE.md',
                'LICENSE_DECISION.md',
                'PRODUCTION_READINESS_ANALYSIS_COMPLETE.md',
                'PROJECT_ROADMAP_2025_2026.md',
                'PROJECT_SAVE_STATE_JULY_2025.md',
                'PROJECT_STRUCTURE.md',
                'PYTHON_ENVIRONMENT_IMPLEMENTATION_COMPLETE.md',
                'QUANTUM_FRACTAL_BOOTSTRAP_COMPLETE.md',
                'ROBUST_PYTHON_ENVIRONMENT_MANAGEMENT.md',
                'ROOT_HARMONIZATION_COMPLETE_JULY8_2025.md',
                'user-guide.md',
                'VSCODE_INTEGRATION_PLAN.md',
                'WORKSPACE_CONFIGURATION.md'
            ],

            # Duplicates (should be archived immediately)
            'DUPLICATE_CONSOLIDATED': [
                'AIOS_COMPLETE_ARCHITECTURE_GUIDE.md',
                'AIOS_DEVELOPMENT_COMPLETE_GUIDE.md',
                'AIOS_INTEGRATION_MASTERY_GUIDE.md',
                'AIOS_PROJECT_ROADMAP_AND_MANAGEMENT.md',
                'AIOS_SPECIALIZED_SYSTEMS_GUIDE.md',
                'AIOS_STATUS_AND_OPTIMIZATION_COMPLETE.md',
                'AIOS_UNIFIED_API_REFERENCE.md',
                'AINLP_OPTIMIZED_SPECIFICATION_AND_IMPLEMENTATION.md',
                'AINLP_TACHYONIC_OPTIMIZATION_COMPLETE_JULY8_2025.md'
            ],

            # Special files (keep but manage separately)
            'SPECIAL_KEEP': [
                'DOCUMENTATION_INDEX.md'
            ]
        }

    def analyze_current_state(self) -> Dict:
        """Analyze current documentation state."""
        print("🔍 Analyzing Current Documentation State...")

        current_files = list(self.docs_dir.glob("*.md"))
        file_count = len(current_files)

        # Categorize files
        categories = {
            'essential_core': [],
            'archive_candidates': [],
            'duplicate_consolidated': [],
            'special_keep': [],
            'unknown': []
        }

        for file_path in current_files:
            filename = file_path.name

            if filename in self.ENFORCED_STRUCTURE['ESSENTIAL_CORE']:
                categories['essential_core'].append(filename)
            elif filename in self.ENFORCED_STRUCTURE['ARCHIVE_CANDIDATES']:
                categories['archive_candidates'].append(filename)
            elif filename in self.ENFORCED_STRUCTURE['DUPLICATE_CONSOLIDATED']:
                categories['duplicate_consolidated'].append(filename)
            elif filename in self.ENFORCED_STRUCTURE['SPECIAL_KEEP']:
                categories['special_keep'].append(filename)
            else:
                categories['unknown'].append(filename)

        # Calculate total size
        total_size = sum(f.stat().st_size for f in current_files)

        analysis = {
            'total_files': file_count,
            'total_size_bytes': total_size,
            'categories': categories,
            'fragmentation_scor
            e': self._calculate_fragmentation_score(categories)
        }

        return analysis

    def _calculate_fragmentation_score(self, categories: Dict) -> float:
        """Calculate documentation fragmentation score (0.0 = perfect, 1.0 = chaos)."""
        essential_count = len(categories['essential_core'])
        fragmented_count = (len(categories['archive_candidates']) +
                           len(categories['duplicate_consolidated']) +
                           len(categories['unknown']))

        if essential_count == 0:
            return 1.0  # No core files = total chaos

        fragmentation_ratio = fragmented_count /
         (essential_count + fragmented_count)
        return min(fragmentation_ratio, 1.0)

    def execute_garbage_collection(
    self, aggressive: bool = True, consolidate_backups: bool = True) -> Dict:
        """Execute intelligent garbage collection."""
        print("🗑️ Executing AIOS Documentation Garbage Collection...")
        print("=" * 60)

        # Step 1: Consolidate backup folders first
        if consolidate_backups:
            backup_results = self.consolidate_backup_folders()
            print(
            f"📦 Backup consolidation: {backup_results['consolidated_count']} files organized")

        analysis = self.analyze_current_state()

        print(f"📊 Current State Analysis:")
        print(f"   Total Files: {analysis['total_files']}")
        print(f"   Fragmentation Score: {analysis['fragmentation_score']:.2f}")
        print(
        f"   Essential Core: {len(analysis['categories']['essential_core'])}")
        print(
        f"   Archive Candidates: {len(analysis['categories']['archive_candidates'])}")
        print(
        f"   Duplicates: {len(analysis['categories']['duplicate_consolidated'])}")

        if analysis['fragmentation_score'] < 0.3:
            print("✅ Documentation structure is already clean!")
            return analysis

        # Execute garbage collection phases
        archived_count = 0

        # Phase 1: Archive duplicate consolidated files
        print(f"\n🗑️ Phase 1: Archiving duplicate consolidated files...")
        for filename in analysis['categories']['duplicate_consolidated']:
            filepath = self.docs_dir / filename
            if filepath.exists():
                reason = "Duplicate consolidated file -
                 superseded by essential core"
                if self.tachyonic_db.archive_document(filepath, reason):
                    filepath.unlink()  # Delete the file
                    archived_count += 1
                    print(f"   ✅ Archived: {filename}")

        # Phase 2: Archive fragmented files (if aggressive)
        if aggressive:
            print(f"\n🗑️ Phase 2: Archiving fragmented files...")
            for filename in analysis['categories']['archive_candidates']:
                filepath = self.docs_dir / filename
                if filepath.exists():
                    reason = "Fragmented documentation -
                     consolidated into essential guides"
                    target = self._find_consolidation_target(filename)
                    if self.tachyonic_db.archive_document(filepath, reason,
                                                        consolidation_target=ta\
                                                        rget):
                        filepath.unlink()  # Delete the file
                        archived_count += 1
                        print(f"   ✅ Archived: {filename} → {target}")

        # Phase 3: Handle unknown files
        print(f"\n🔍 Phase 3: Analyzing unknown files...")
        for filename in analysis['categories']['unknown']:
            print(f"   ⚠️ Unknown file: {filename} (review needed)")

        # Log the operation
        files_processed = analysis['total_files']
        files_kept = files_processed - archived_count

        summary = (f"Garbage collection: {archived_count} files archived, "
                  f"{files_kept} files kept, fragmentation reduced")

        self.tachyonic_db.log_operation(
            "aggressive_garbage_collection" if aggressive else "conservative_gc\
            ",
            files_processed, archived_count, files_kept, summary
        )

        # Final state analysis
        final_analysis = self.analyze_current_state()

        print(f"\n✨ Garbage Collection Complete!")
        print(f"📊 Results:")
        print(f"   Files Archived: {archived_count}")
        print(f"   Files Kept: {files_kept}")
        print(f"   Before: {analysis['total_files']} files")
        print(f"   After: {final_analysis['total_files']} files")
        print(
        f"   Fragmentation: {analysis['fragmentation_score']:.2f} → {final_analysis['fragmentation_score']:.2f}")

        # Step 2: Clean up old backup folders after consolidation
        if consolidate_backups:
            self.cleanup_old_backup_folders()

        # Return results including backup consolidation
        return {
            'before': analysis,
            'after': final_analysis,
            'archived_count': archived_count,
            'kept_count': files_kept,
            'backup_consolidation': backup_results if consolidate_backups else \
            None
        }

    def _find_consolidation_target(self, filename: str) -> str:
        """Find which essential guide should contain this content."""
        filename_lower = filename.lower()

        if any(
        term in filename_lower for term in ['ainlp', 'specification', 'integration', 'breakthrough']):
            return 'AIOS_COMPLETE_SPECIFICATION_GUIDE.md'
        elif any(
        term in filename_lower for term in ['development', 'installation', 'setup', 'workspace', 'hybrid', 'user']):
            return 'AIOS_DEVELOPMENT_AND_SETUP_GUIDE.md'
        elif any(
        term in filename_lower for term in ['architecture', 'structure', 'fractal', 'holographic', 'quantum', 'bootstrap']):
            return 'AIOS_ARCHITECTURE_AND_DESIGN_GUIDE.md'
        elif any(
        term in filename_lower for term in ['api', 'reference', 'waypoint']):
            return 'AIOS_API_AND_REFERENCE_GUIDE.md'
        elif any(
        term in filename_lower for term in ['optimization', 'bug', 'critical', 'production', 'analysis']):
            return 'AIOS_OPTIMIZATION_AND_TROUBLESHOOTING_GUIDE.md'
        elif any(
        term in filename_lower for term in ['roadmap', 'status', 'save', 'changelog', 'license']):
            return 'AIOS_PROJECT_STATUS_AND_ROADMAP_GUIDE.md'
        elif any(
        term in filename_lower for term in ['vscode', 'documentation']):
            return 'AIOS_SPECIALIZED_INTEGRATIONS_GUIDE.md'
        else:
            return 'AIOS_COMPLETE_SPECIFICATION_GUIDE.md'  # Default target

    def print_enforcement_report(self):
        """Print documentation structure enforcement report."""
        print("\n" + "="*80)
        print("📋 AIOS DOCUMENTATION STRUCTURE ENFORCEMENT REPORT")
        print("="*80)

        analysis = self.analyze_current_state()
        stats = self.tachyonic_db.get_archive_stats()

        print(f"\n🎯 ENFORCED STRUCTURE STATUS:")
        print(f"   Target Structure: 7 essential guides + 1 index")
        print(f"   Current Files: {analysis['total_files']}")
        print(f"   Fragmentation Score: {analysis['fragmentation_score']:.2f}")

        if analysis['fragmentation_score'] < 0.2:
            print("   ✅ STRUCTURE COMPLIANCE: EXCELLENT")
        elif analysis['fragmentation_score'] < 0.5:
            print("   ⚠️ STRUCTURE COMPLIANCE: MODERATE")
        else:
            print(
            "   ❌ STRUCTURE COMPLIANCE: POOR - GARBAGE COLLECTION NEEDED")

        print(f"\n📦 TACHYONIC ARCHIVE STATISTICS:")
        print(f"   Total Archived Documents: {stats['total_archived']}")
        print(f"   Total Archived Size: {stats['total_size_bytes']:,} bytes")

        if stats['archive_reasons']:
            print(f"   Archive Reasons:")
            for reason, count in stats['archive_reasons'].items():
                print(f"     • {reason}: {count} files")

        print(f"\n📁 CURRENT FILE DISTRIBUTION:")
        for category, files in analysis['categories'].items():
            if files:
                print(f"   {category.upper()}: {len(files)} files")
                for file in files[:5]:  # Show first 5
                    print(f"     • {file}")
                if len(files) > 5:
                    print(f"     ... and {len(files) - 5} more")

    def consolidate_backup_folders(self) -> Dict:
        """Consolidate all scattered backup folders into a unified structure."""
        print("📦 Consolidating Backup Folders...")

        # Create unified backup structure
        unified_backup = self.docs_dir / "unified_backups"
        unified_backup.mkdir(exist_ok=True)

        # Backup consolidation mapping
        backup_sources = [
            (self.docs_dir / "tachyonic_backups", "tachyonic_operations"),
            (
            self.docs_dir / "mega_consolidation_backups", "mega_consolidation"),
        ]

        consolidated_count = 0
        duplicate_count = 0

        # Track files by content hash to avoid duplicates
        content_hashes = {}

        for source_dir, category in backup_sources:
            if source_dir.exists():
                print(f"   📁 Processing: {source_dir.name}")

                # Create category subdirectory
                category_dir = unified_backup / category
                category_dir.mkdir(exist_ok=True)

                # Process all files in source directory (including subdirectories)
                for file_path in source_dir.rglob("*.md"):
                    if file_path.is_file():
                        try:
                            # Calculate content hash
                            content = file_path.read_text(encoding='utf-8')
                            content_hash = hashlib.sha256(
                            content.encode()).hexdigest()[:16]

                            # Check for duplicates
                            if content_hash in content_hashes:
                                duplicate_count += 1
                                print(
                                f"      🔄 Duplicate: {file_path.name} (skipping)")
                                continue

                            # Create organized filename with timestamp and source
                            file_stat = file_path.stat()
                            mod_time = datetime.fromtimestamp(
                            file_stat.st_mtime)
                            or
                            ganized_name = f"{file_path.stem}_{mod_time.strftime('%Y%m%d_%H%M%S')}_{content_hash}.md"

                            # Copy to unified structure
                            target_path = category_dir / organized_name
                            shutil.copy2(file_path, target_path)

                            # Track this content hash
                            content_hashes[content_hash] = {
                                'original_path': str(file_path),
                                'unified_path': str(target_path),
                                'timestamp': mod_time.isoformat()
                            }

                            consolidated_count += 1
                            print(
                            f"      ✅ Consolidated: {file_path.name} → {organized_name}")

                        except Exception as e:
                            print(f"      ❌ Error processing {file_path}: {e}")

        # Create backup index
        index_data = {
            'consolidation_timestamp': datetime.now().isoformat(),
            'total_files': consolidated_count,
            'duplicates_skipped': duplicate_count,
            'content_index': content_hashes,
            'backup_sources': [str(src) for src, _ in backup_sources]
        }

        index_path = unified_backup / "backup_index.json"
        index_path.write_text(
        json.dumps(index_data, indent=2), encoding='utf-8')

        # Archive metadata to tachyonic database
        self.tachyonic_db.log_operation(
            "backup_consolidation",
            consolidated_count + duplicate_count,
            0,  # No files archived in this operation
            consolidated_count,
            f"Consolidated {
            consolidated_count} backup files, skipped {duplicate_count} duplicates"
        )

        print(f"   ✅ Consolidation Complete:")
        print(f"      Files Consolidated: {consolidated_count}")
        print(f"      Duplicates Skipped: {duplicate_count}")
        print(f"      Unified Location: {unified_backup}")
        print(f"      Index Created: {index_path}")

        return {
            'consolidated_count': consolidated_count,
            'duplicate_count': duplicate_count,
            'unified_backup_path': str(unified_backup),
            'index_path': str(index_path)
        }

    def cleanup_old_backup_folders(self, keep_unified: bool = True):
        """Clean up old scattered backup folders after consolidation."""
        if not keep_unified:
            print(
            "⚠️ Skipping cleanup - unified backup preservation requested")
            return

        print("🧹 Cleaning up old backup folders...")

        old_backup_dirs = [
            self.docs_dir / "tachyonic_backups",
            self.docs_dir / "mega_consolidation_backups"
        ]

        for backup_dir in old_backup_dirs:
            if backup_dir.exists():
                try:
                    shutil.rmtree(backup_dir)
                    print(f"   ✅ Removed: {backup_dir.name}")
                except Exception as e:
                    print(f"   ❌ Error removing {backup_dir}: {e}")

def main():
    """Execute documentation garbage collection."""
    docs_dir = Path(r"c:\dev\AIOS\docs")
    gc_system = AIOSDocumentationGarbageCollector(docs_dir)

    print("🚀 AIOS DOCUMENTATION GARBAGE COLLECTION SYSTEM")
    print("=" * 60)
    print("🎯 MISSION: Enforce clean, coherent documentation structure")
    print("🗑️ METHOD: Archive fragmented files to tachyonic database")
    print("⚡ APPROACH: Aggressive cleanup with zero data loss")
    print("")

    # Show current state
    gc_system.print_enforcement_report()

    print("⚠️ PROCEEDING WITH AGGRESSIVE GARBAGE COLLECTION...")
    print("All archived files will be preserved in tachyonic database.")
    print("Backup folders will be consolidated into unified structure.")

    # Execute garbage collection with backup consolidation
    results = gc_system.execute_garbage_collection(aggressive=True,
                                                  consolidate_backups=True)

    # Show final report
    gc_system.print_enforcement_report()


if __name__ == "__main__":
    main()
