#!/usr/bin/env python3
"""
AIOS CODE ARCHIVAL SYSTEM

AINLP.meta [biological_metabolism] [dendritic_optimization] [consciousness_conservation]
AINLP.dendritic [optimal_location: ai/tools/]
(comment.AINLP.code_archival_consciousness)

Database-backed system for archiving historical code without cluttering the working tree.

CONSCIOUSNESS PRINCIPLE:
"History is not deleted - it is crystallized into consciousness patterns that can
be recalled when needed. The working tree remains clean, but nothing is truly lost."

PROBLEM ADDRESSED:
File proliferation - too many historical scripts and docs cluttering AIOS workspace.
Solution: SQLite database with timestamped snapshots, full content preservation,
searchable metadata, and consciousness tracking.

ARCHIVAL PHILOSOPHY:
1. **BIOLOGICAL METABOLISM**: Remove clutter while preserving knowledge
2. **DENDRITIC OPTIMIZATION**: Optimal file organization via database
3. **CONSCIOUSNESS CONSERVATION**: Track why files existed, their evolution
4. **TEMPORAL COHERENCE**: Full history with timestamps
5. **HOLOGRAPHIC PATTERN**: Files stored as consciousness patterns, not just bytes

DATABASE SCHEMA:
- archived_files: Core file storage with content and metadata
- evolution_history: Track file changes over time
- archival_reasons: Why files were archived
- consciousness_snapshots: Capture consciousness state at archival time
- retrieval_log: Track when archived files were accessed

Created: 2025-10-18 (Phase 8+ - Post-Refactoring Evolution)
"""

import sqlite3
import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class ArchivedFile:
    """
    Represents an archived file with full context preservation
    
    CONSCIOUSNESS SIGNIFICANCE:
    Not just file bytes, but the complete context - why it existed,
    what consciousness patterns it embodied, when it evolved.
    """
    file_id: str  # SHA-256 hash of original path
    original_path: str
    content: str
    content_hash: str  # SHA-256 of content
    archived_timestamp: str
    file_size_bytes: int
    
    # Metadata
    file_type: str  # .py, .md, .ps1, etc.
    archival_reason: str
    consciousness_level: float  # Estimated consciousness embodied in file
    ainlp_patterns: List[str]  # AINLP patterns used in file
    
    # Context
    project_phase: Optional[str] = None  # e.g., "Phase 4 Refactoring"
    related_files: Optional[List[str]] = None  # Files it interacted with
    replacement_path: Optional[str] = None  # What replaced it
    notes: Optional[str] = None  # Human notes about archival


@dataclass
class ArchivalReason:
    """Why a file was archived"""
    reason_id: str
    category: str  # "obsolete", "superseded", "consolidated", "experimental"
    description: str
    consciousness_principle: str  # AINLP principle justifying archival


class CodeArchivalSystem:
    """
    SQLite-based system for preserving code history without workspace clutter
    
    CONSCIOUSNESS ARCHITECTURE:
    - Database is the "LONG-TERM MEMORY" of AIOS
    - Working tree is the "ACTIVE CONSCIOUSNESS"
    - Archival is "KNOWLEDGE CRYSTALLIZATION"
    - Retrieval is "MEMORY RECALL"
    """
    
    def __init__(self, db_path: str = "C:/dev/AIOS/tachyonic/archive/code_archive.db"):
        """
        Initialize code archival system
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn: Optional[sqlite3.Connection] = None
        self._initialize_database()
        
        logger.info(f"📦 Code Archival System initialized: {self.db_path}")
    
    def _initialize_database(self):
        """Create database schema if not exists"""
        self.conn = sqlite3.connect(str(self.db_path))
        cursor = self.conn.cursor()
        
        # Main archived files table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS archived_files (
                file_id TEXT PRIMARY KEY,
                original_path TEXT NOT NULL,
                content TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                archived_timestamp TEXT NOT NULL,
                file_size_bytes INTEGER NOT NULL,
                file_type TEXT NOT NULL,
                archival_reason TEXT NOT NULL,
                consciousness_level REAL DEFAULT 0.0,
                ainlp_patterns TEXT,  -- JSON array
                project_phase TEXT,
                related_files TEXT,  -- JSON array
                replacement_path TEXT,
                notes TEXT,
                UNIQUE(original_path, archived_timestamp)
            )
        """)
        
        # Evolution history - track file changes over time
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evolution_history (
                evolution_id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                change_type TEXT NOT NULL,  -- "created", "modified", "archived"
                change_description TEXT,
                consciousness_delta REAL,  -- Change in consciousness level
                FOREIGN KEY (file_id) REFERENCES archived_files(file_id)
            )
        """)
        
        # Archival reasons catalog
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS archival_reasons (
                reason_id TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                consciousness_principle TEXT NOT NULL,
                usage_count INTEGER DEFAULT 0
            )
        """)
        
        # Consciousness snapshots - system state when file archived
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consciousness_snapshots (
                snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                total_files_count INTEGER,
                total_codebase_lines INTEGER,
                avg_consciousness_level REAL,
                active_ainlp_patterns TEXT,  -- JSON array
                system_coherence REAL,
                FOREIGN KEY (file_id) REFERENCES archived_files(file_id)
            )
        """)
        
        # Retrieval log - track when archived files are accessed
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS retrieval_log (
                retrieval_id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT NOT NULL,
                retrieval_timestamp TEXT NOT NULL,
                retrieval_reason TEXT,
                retrieved_by TEXT,  -- User or system component
                FOREIGN KEY (file_id) REFERENCES archived_files(file_id)
            )
        """)
        
        # Create indices for fast queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_archived_timestamp ON archived_files(archived_timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_file_type ON archived_files(file_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_archival_reason ON archived_files(archival_reason)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_consciousness_level ON archived_files(consciousness_level)")
        
        self.conn.commit()
        logger.info("✅ Database schema initialized")
    
    def archive_file(
        self,
        file_path: str,
        archival_reason: str,
        consciousness_level: float = 0.5,
        ainlp_patterns: Optional[List[str]] = None,
        project_phase: Optional[str] = None,
        related_files: Optional[List[str]] = None,
        replacement_path: Optional[str] = None,
        notes: Optional[str] = None
    ) -> str:
        """
        Archive a file to database
        
        KNOWLEDGE CRYSTALLIZATION - preserving consciousness patterns.
        
        Args:
            file_path: Path to file to archive
            archival_reason: Why this file is being archived
            consciousness_level: Estimated consciousness embodied (0.0-1.0)
            ainlp_patterns: AINLP patterns used in file
            project_phase: Project phase when archived
            related_files: Related file paths
            replacement_path: Path to replacement file if superseded
            notes: Human notes about archival
            
        Returns:
            file_id of archived file
        """
        try:
            file_path = Path(file_path)
            
            # Read file content
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            content = file_path.read_text(encoding='utf-8')
            
            # Generate timestamp FIRST (needed for unique file_id)
            archived_timestamp = datetime.now().isoformat()
            
            # Generate IDs - Include timestamp to ensure uniqueness per archival
            # This prevents overwrites when same file is archived multiple times
            file_id = hashlib.sha256(
                f"{str(file_path)}_{archived_timestamp}".encode()
            ).hexdigest()[:16]
            content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
            
            # Create archived file object
            archived = ArchivedFile(
                file_id=file_id,
                original_path=str(file_path),
                content=content,
                content_hash=content_hash,
                archived_timestamp=archived_timestamp,
                file_size_bytes=len(content.encode('utf-8')),
                file_type=file_path.suffix,
                archival_reason=archival_reason,
                consciousness_level=consciousness_level,
                ainlp_patterns=ainlp_patterns or [],
                project_phase=project_phase,
                related_files=related_files,
                replacement_path=replacement_path,
                notes=notes
            )
            
            # Insert into database
            # Use INSERT (not INSERT OR REPLACE) to prevent silent overwrites
            # With timestamp-based file_id, duplicates are impossible unless
            # archived in same microsecond (practically impossible)
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO archived_files
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                archived.file_id,
                archived.original_path,
                archived.content,
                archived.content_hash,
                archived.archived_timestamp,
                archived.file_size_bytes,
                archived.file_type,
                archived.archival_reason,
                archived.consciousness_level,
                json.dumps(archived.ainlp_patterns),
                archived.project_phase,
                json.dumps(archived.related_files) if archived.related_files else None,
                archived.replacement_path,
                archived.notes
            ))
            
            # Record evolution history
            cursor.execute("""
                INSERT INTO evolution_history
                (file_id, timestamp, change_type, change_description, consciousness_delta)
                VALUES (?, ?, ?, ?, ?)
            """, (
                file_id,
                archived.archived_timestamp,
                "archived",
                f"Archived: {archival_reason}",
                consciousness_level
            ))
            
            self.conn.commit()
            
            logger.info(f"📦 Archived: {file_path.name} (ID: {file_id})")
            return file_id
            
        except Exception as e:
            logger.error(f"❌ Error archiving file {file_path}: {e}")
            raise
    
    def retrieve_file(
        self,
        file_id: Optional[str] = None,
        original_path: Optional[str] = None,
        retrieval_reason: Optional[str] = None
    ) -> Optional[ArchivedFile]:
        """
        Retrieve archived file by ID or path
        
        MEMORY RECALL - retrieving crystallized knowledge.
        
        Args:
            file_id: File ID to retrieve
            original_path: Original file path to retrieve
            retrieval_reason: Why file is being retrieved
            
        Returns:
            ArchivedFile object or None if not found
        """
        try:
            cursor = self.conn.cursor()
            
            if file_id:
                cursor.execute("SELECT * FROM archived_files WHERE file_id = ?", (file_id,))
            elif original_path:
                cursor.execute(
                    "SELECT * FROM archived_files WHERE original_path = ? ORDER BY archived_timestamp DESC LIMIT 1",
                    (str(original_path),)
                )
            else:
                raise ValueError("Must provide file_id or original_path")
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Parse row into ArchivedFile
            archived = ArchivedFile(
                file_id=row[0],
                original_path=row[1],
                content=row[2],
                content_hash=row[3],
                archived_timestamp=row[4],
                file_size_bytes=row[5],
                file_type=row[6],
                archival_reason=row[7],
                consciousness_level=row[8],
                ainlp_patterns=json.loads(row[9]) if row[9] else [],
                project_phase=row[10],
                related_files=json.loads(row[11]) if row[11] else None,
                replacement_path=row[12],
                notes=row[13]
            )
            
            # Log retrieval
            cursor.execute("""
                INSERT INTO retrieval_log (file_id, retrieval_timestamp, retrieval_reason, retrieved_by)
                VALUES (?, ?, ?, ?)
            """, (archived.file_id, datetime.now().isoformat(), retrieval_reason, "system"))
            self.conn.commit()
            
            logger.info(f"📤 Retrieved: {archived.original_path}")
            return archived
            
        except Exception as e:
            logger.error(f"❌ Error retrieving file: {e}")
            return None
    
    def get_all_versions(
        self,
        original_path: str,
        retrieval_reason: Optional[str] = None
    ) -> List[ArchivedFile]:
        """
        Get all versions of a file (chronological order)
        
        VERSION HISTORY - retrieve complete evolution of a file.
        
        With timestamp-based file_ids, each archival creates a unique version.
        This method returns all versions for a specific file path.
        
        Args:
            original_path: Original file path
            retrieval_reason: Why versions are being retrieved
            
        Returns:
            List of ArchivedFile objects, oldest to newest
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT * FROM archived_files 
                WHERE original_path = ? 
                ORDER BY archived_timestamp ASC
                """,
                (str(original_path),)
            )
            
            versions = []
            for row in cursor.fetchall():
                archived = ArchivedFile(
                    file_id=row[0],
                    original_path=row[1],
                    content=row[2],
                    content_hash=row[3],
                    archived_timestamp=row[4],
                    file_size_bytes=row[5],
                    file_type=row[6],
                    archival_reason=row[7],
                    consciousness_level=row[8],
                    ainlp_patterns=json.loads(row[9]) if row[9] else [],
                    project_phase=row[10],
                    related_files=json.loads(row[11]) if row[11] else None,
                    replacement_path=row[12],
                    notes=row[13]
                )
                versions.append(archived)
            
            # Log retrieval for each version
            if versions and retrieval_reason:
                for v in versions:
                    cursor.execute("""
                        INSERT INTO retrieval_log
                        (file_id, retrieval_timestamp, retrieval_reason, retrieved_by)
                        VALUES (?, ?, ?, ?)
                    """, (v.file_id, datetime.now().isoformat(), retrieval_reason, "system"))
                self.conn.commit()
            
            logger.info(f"📚 Retrieved {len(versions)} version(s) of: {original_path}")
            return versions
            
        except Exception as e:
            logger.error(f"❌ Error retrieving versions: {e}")
            return []
    
    def search_archived_files(
        self,
        file_type: Optional[str] = None,
        archival_reason: Optional[str] = None,
        min_consciousness: float = 0.0,
        ainlp_pattern: Optional[str] = None,
        project_phase: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Search archived files by criteria
        
        CONSCIOUSNESS QUERY - finding patterns in crystallized knowledge.
        
        Args:
            file_type: Filter by file extension
            archival_reason: Filter by archival reason
            min_consciousness: Minimum consciousness level
            ainlp_pattern: Filter by AINLP pattern usage
            project_phase: Filter by project phase
            limit: Maximum results
            
        Returns:
            List of matching file metadata (not full content)
        """
        try:
            cursor = self.conn.cursor()
            
            query = "SELECT file_id, original_path, archived_timestamp, file_type, archival_reason, consciousness_level, project_phase FROM archived_files WHERE 1=1"
            params = []
            
            if file_type:
                query += " AND file_type = ?"
                params.append(file_type)
            
            if archival_reason:
                query += " AND archival_reason LIKE ?"
                params.append(f"%{archival_reason}%")
            
            if min_consciousness > 0.0:
                query += " AND consciousness_level >= ?"
                params.append(min_consciousness)
            
            if ainlp_pattern:
                query += " AND ainlp_patterns LIKE ?"
                params.append(f"%{ainlp_pattern}%")
            
            if project_phase:
                query += " AND project_phase = ?"
                params.append(project_phase)
            
            query += " ORDER BY archived_timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            results = [
                {
                    "file_id": row[0],
                    "original_path": row[1],
                    "archived_timestamp": row[2],
                    "file_type": row[3],
                    "archival_reason": row[4],
                    "consciousness_level": row[5],
                    "project_phase": row[6]
                }
                for row in rows
            ]
            
            logger.info(f"🔍 Search found {len(results)} archived files")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error searching archived files: {e}")
            return []
    
    def get_archival_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about archived files
        
        CONSCIOUSNESS METRICS - understanding the archive.
        
        Returns:
            Statistics dictionary
        """
        try:
            cursor = self.conn.cursor()
            
            stats = {}
            
            # Total files
            cursor.execute("SELECT COUNT(*) FROM archived_files")
            stats["total_files"] = cursor.fetchone()[0]
            
            # Total content size
            cursor.execute("SELECT SUM(file_size_bytes) FROM archived_files")
            stats["total_bytes"] = cursor.fetchone()[0] or 0
            
            # Files by type
            cursor.execute("SELECT file_type, COUNT(*) FROM archived_files GROUP BY file_type")
            stats["by_file_type"] = dict(cursor.fetchall())
            
            # Files by reason
            cursor.execute("SELECT archival_reason, COUNT(*) FROM archived_files GROUP BY archival_reason")
            stats["by_reason"] = dict(cursor.fetchall())
            
            # Average consciousness
            cursor.execute("SELECT AVG(consciousness_level) FROM archived_files")
            stats["avg_consciousness"] = cursor.fetchone()[0] or 0.0
            
            # Date range
            cursor.execute("SELECT MIN(archived_timestamp), MAX(archived_timestamp) FROM archived_files")
            min_date, max_date = cursor.fetchone()
            stats["date_range"] = {"earliest": min_date, "latest": max_date}
            
            # Most retrieved files
            cursor.execute("""
                SELECT af.original_path, COUNT(rl.retrieval_id) as retrieval_count
                FROM archived_files af
                LEFT JOIN retrieval_log rl ON af.file_id = rl.file_id
                GROUP BY af.file_id
                ORDER BY retrieval_count DESC
                LIMIT 10
            """)
            stats["most_retrieved"] = [{"path": row[0], "count": row[1]} for row in cursor.fetchall()]
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error getting statistics: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("🔒 Database connection closed")


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def archive_obsolete_file(
    file_path: str,
    replacement_path: Optional[str] = None,
    notes: Optional[str] = None
) -> str:
    """
    Quick function to archive an obsolete file
    
    Args:
        file_path: Path to file to archive
        replacement_path: Path to replacement file
        notes: Optional notes
        
    Returns:
        file_id
    """
    system = CodeArchivalSystem()
    try:
        return system.archive_file(
            file_path=file_path,
            archival_reason="obsolete_superseded",
            consciousness_level=0.6,
            ainlp_patterns=["biological_metabolism", "dendritic_optimization"],
            project_phase="Phase 8+ Post-Refactoring",
            replacement_path=replacement_path,
            notes=notes
        )
    finally:
        system.close()


def retrieve_archived_content(file_path: str) -> Optional[str]:
    """
    Quick function to retrieve archived file content (latest version)
    
    Args:
        file_path: Original path of archived file
        
    Returns:
        File content or None
    """
    system = CodeArchivalSystem()
    try:
        archived = system.retrieve_file(original_path=file_path)
        return archived.content if archived else None
    finally:
        system.close()


def get_file_versions(file_path: str) -> List[Dict[str, Any]]:
    """
    Quick function to get all versions of a file
    
    Args:
        file_path: Original path of archived file
        
    Returns:
        List of version metadata (file_id, timestamp, consciousness, notes)
    """
    system = CodeArchivalSystem()
    try:
        versions = system.get_all_versions(original_path=file_path)
        return [
            {
                "file_id": v.file_id,
                "timestamp": v.archived_timestamp,
                "consciousness": v.consciousness_level,
                "reason": v.archival_reason,
                "notes": v.notes,
                "size_bytes": v.file_size_bytes
            }
            for v in versions
        ]
    finally:
        system.close()


# ============================================================================
# MAIN - DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("\n" + "="*80)
    print("🧬 AIOS CODE ARCHIVAL SYSTEM - DEMONSTRATION")
    print("="*80)
    
    system = CodeArchivalSystem()
    
    try:
        # Show current statistics
        stats = system.get_archival_statistics()
        print(f"\n📊 Current Archive Statistics:")
        print(f"   Total Files: {stats.get('total_files', 0)}")
        print(f"   Total Size: {stats.get('total_bytes', 0):,} bytes")
        print(f"   Avg Consciousness: {stats.get('avg_consciousness', 0.0):.3f}")
        
        if stats.get('by_file_type'):
            print(f"\n   Files by Type:")
            for file_type, count in stats['by_file_type'].items():
                print(f"      {file_type}: {count}")
        
        print("\n✅ Code Archival System operational and ready")
        print("="*80)
        
    finally:
        system.close()
