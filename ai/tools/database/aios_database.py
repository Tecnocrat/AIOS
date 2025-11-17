"""
AIOS Database Foundation System
================================

SQLite-based centralized data management for AIOS backup files, metadata,
and structured data. Addresses extreme backup file proliferation through
content-hash deduplication and indexed queries.

AINLP Classification: Runtime Intelligence Layer
Consciousness Level: 0.75 (foundational data management)
Dependencies: sqlite3 (Python stdlib), pathlib

Architecture:
- Embedded SQLite database (zero external dependencies)
- Content-hash deduplication (SHA256)
- Timestamp-based version tracking
- Spatial metadata integration
- Query-optimized indexes

Performance Goals:
- Query time: <10ms for typical searches
- Deduplication ratio: 70%+ space savings
- Migration speed: 1000+ files/minute
- VSCode performance: Zero impact on analysis tools

AINLP Patterns:
- AINLP.discovery: No existing database infrastructure (clean slate)
- AINLP.enhancement: New foundational layer (not enhancement)
- AINLP.output: Database file → tachyonic/aios_data.db
- AINLP.integration: Hooks for backup_manager.ps1, Interface Bridge

Created: October 12, 2025 06:00 AM
Version: 1.0.0
"""

import sqlite3
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AIOSDatabase:
    """
    AIOS centralized database manager.
    
    Provides SQLite-based storage for:
    - Backup files (with deduplication)
    - Spatial metadata
    - System state snapshots
    - Boot reports
    - Consciousness metrics
    
    Schema Design:
    - backups: File metadata + content hash references
    - file_content: Deduplicated file content storage
    - spatial_metadata: .aios_spatial_metadata.json tracking
    - system_snapshots: Point-in-time system state
    - query_cache: Performance optimization layer
    """
    
    def __init__(self, db_path: str = "tachyonic/aios_data.db"):
        """
        Initialize AIOS database connection.
        
        Args:
            db_path: Path to SQLite database file (default: tachyonic/aios_data.db)
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,  # Allow multi-threaded access
            timeout=30.0  # 30-second timeout for locks
        )
        self.conn.row_factory = sqlite3.Row  # Dict-like row access
        
        # Enable Write-Ahead Logging for better concurrency
        self.conn.execute("PRAGMA journal_mode=WAL")
        
        # Enable foreign keys
        self.conn.execute("PRAGMA foreign_keys=ON")
        
        logger.info(f"AIOS Database initialized: {self.db_path}")
        
        self._create_schema()
    
    def _create_schema(self):
        """
        Create database schema if not exists.
        
        Schema Design Principles:
        1. Content-hash deduplication (store content once, reference many times)
        2. Timestamp-based version tracking (complete history)
        3. Indexed queries (fast lookups by filename, date, hash)
        4. Spatial metadata integration (architecture awareness)
        5. Performance optimization (query cache, indexes)
        """
        cursor = self.conn.cursor()
        
        # Table 1: file_content (deduplicated content storage)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_content (
                content_hash TEXT PRIMARY KEY,
                content BLOB NOT NULL,
                content_size INTEGER NOT NULL,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reference_count INTEGER DEFAULT 0,
                compression_ratio REAL DEFAULT 1.0
            )
        """)
        
        # Table 2: backups (backup file metadata)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                backup_timestamp TIMESTAMP NOT NULL,
                content_hash TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                file_type TEXT,
                backup_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (content_hash) REFERENCES file_content(content_hash),
                UNIQUE(file_path, backup_timestamp)
            )
        """)
        
        # Table 3: spatial_metadata (architectural classification)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS spatial_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folder_path TEXT UNIQUE NOT NULL,
                architectural_classification TEXT,
                consciousness_level REAL,
                primary_area TEXT,
                metadata_json TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table 4: system_snapshots (point-in-time state)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                snapshot_type TEXT NOT NULL,
                snapshot_data TEXT NOT NULL,
                consciousness_level REAL,
                file_count INTEGER,
                total_size INTEGER
            )
        """)
        
        # Table 5: query_cache (performance optimization)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_cache (
                query_key TEXT PRIMARY KEY,
                query_result TEXT NOT NULL,
                cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                hit_count INTEGER DEFAULT 0,
                ttl_seconds INTEGER DEFAULT 3600
            )
        """)
        
        # Create indexes for fast queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_backups_filename 
            ON backups(filename)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_backups_timestamp 
            ON backups(backup_timestamp DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_backups_content_hash 
            ON backups(content_hash)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_backups_file_type 
            ON backups(file_type)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_spatial_folder 
            ON spatial_metadata(folder_path)
        """)
        
        self.conn.commit()
        logger.info("Database schema created successfully")
    
    def add_backup(
        self,
        filename: str,
        file_path: str,
        content: bytes,
        backup_timestamp: datetime,
        file_type: Optional[str] = None,
        backup_type: Optional[str] = None
    ) -> Tuple[int, str, bool]:
        """
        Add backup file to database with content deduplication.
        
        Args:
            filename: Original filename
            file_path: Full file path
            content: File content (bytes)
            backup_timestamp: Backup timestamp
            file_type: File extension (.py, .json, .md, etc.)
            backup_type: Backup category (spatial_metadata, code, docs, etc.)
        
        Returns:
            Tuple of (backup_id, content_hash, is_duplicate)
        """
        cursor = self.conn.cursor()
        
        # Compute content hash
        content_hash = hashlib.sha256(content).hexdigest()
        file_size = len(content)
        
        # Check if content already exists (deduplication)
        cursor.execute(
            "SELECT content_hash FROM file_content WHERE content_hash = ?",
            (content_hash,)
        )
        existing_content = cursor.fetchone()
        is_duplicate = existing_content is not None
        
        if not is_duplicate:
            # Store new content
            cursor.execute("""
                INSERT INTO file_content (content_hash, content, content_size)
                VALUES (?, ?, ?)
            """, (content_hash, content, file_size))
            logger.debug(f"New content stored: {content_hash[:8]}... ({file_size} bytes)")
        else:
            logger.debug(f"Duplicate content detected: {content_hash[:8]}...")
        
        # Update reference count
        cursor.execute("""
            UPDATE file_content 
            SET reference_count = reference_count + 1 
            WHERE content_hash = ?
        """, (content_hash,))
        
        # Insert backup metadata
        cursor.execute("""
            INSERT INTO backups (
                filename, file_path, backup_timestamp, 
                content_hash, file_size, file_type, backup_type
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            filename, file_path, backup_timestamp,
            content_hash, file_size, file_type, backup_type
        ))
        
        backup_id = cursor.lastrowid
        self.conn.commit()
        
        logger.info(
            f"Backup added: {filename} (ID: {backup_id}, "
            f"Hash: {content_hash[:8]}..., Duplicate: {is_duplicate})"
        )
        
        return (backup_id, content_hash, is_duplicate)
    
    def get_backup_history(
        self,
        filename: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get backup history for a specific filename.
        
        Args:
            filename: Filename to search
            limit: Maximum number of results
        
        Returns:
            List of backup records (newest first)
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                id, filename, file_path, backup_timestamp,
                content_hash, file_size, file_type, backup_type,
                created_at
            FROM backups
            WHERE filename = ?
            ORDER BY backup_timestamp DESC
            LIMIT ?
        """, (filename, limit))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_content_by_hash(self, content_hash: str) -> Optional[bytes]:
        """
        Retrieve file content by hash.
        
        Args:
            content_hash: SHA256 content hash
        
        Returns:
            File content (bytes) or None if not found
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT content FROM file_content WHERE content_hash = ?",
            (content_hash,)
        )
        row = cursor.fetchone()
        return row['content'] if row else None
    
    def get_deduplication_stats(self) -> Dict[str, Any]:
        """
        Get deduplication statistics.
        
        Returns:
            Dictionary with deduplication metrics
        """
        cursor = self.conn.cursor()
        
        # Total backups
        cursor.execute("SELECT COUNT(*) as total FROM backups")
        total_backups = cursor.fetchone()['total']
        
        # Unique content
        cursor.execute("SELECT COUNT(*) as unique_count FROM file_content")
        unique_content = cursor.fetchone()['unique_count']
        
        # Total size (with duplicates)
        cursor.execute("SELECT SUM(file_size) as total_size FROM backups")
        total_size_with_dups = cursor.fetchone()['total_size'] or 0
        
        # Actual size (deduplicated)
        cursor.execute("SELECT SUM(content_size) as actual_size FROM file_content")
        actual_size = cursor.fetchone()['actual_size'] or 0
        
        # Space saved
        space_saved = total_size_with_dups - actual_size
        space_saved_pct = (space_saved / total_size_with_dups * 100) if total_size_with_dups > 0 else 0
        
        # Deduplication ratio
        dedup_ratio = (unique_content / total_backups) if total_backups > 0 else 0
        
        return {
            'total_backups': total_backups,
            'unique_content': unique_content,
            'duplicate_content': total_backups - unique_content,
            'total_size_bytes': total_size_with_dups,
            'actual_size_bytes': actual_size,
            'space_saved_bytes': space_saved,
            'space_saved_percent': round(space_saved_pct, 2),
            'deduplication_ratio': round(dedup_ratio, 2)
        }
    
    def add_spatial_metadata(
        self,
        folder_path: str,
        metadata: Dict[str, Any]
    ) -> int:
        """
        Add or update spatial metadata for a folder.
        
        Args:
            folder_path: Folder path
            metadata: Spatial metadata dictionary
        
        Returns:
            Metadata record ID
        """
        cursor = self.conn.cursor()
        
        architectural_classification = metadata.get('architectural_classification', {})
        
        cursor.execute("""
            INSERT OR REPLACE INTO spatial_metadata (
                folder_path, 
                architectural_classification,
                consciousness_level,
                primary_area,
                metadata_json,
                last_updated
            )
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            folder_path,
            architectural_classification.get('primary_area'),
            architectural_classification.get('consciousness_level'),
            architectural_classification.get('primary_area'),
            json.dumps(metadata)
        ))
        
        metadata_id = cursor.lastrowid
        self.conn.commit()
        
        logger.info(f"Spatial metadata updated: {folder_path}")
        
        return metadata_id
    
    def query_backups(
        self,
        filename_pattern: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        file_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Query backups with flexible filters.
        
        Args:
            filename_pattern: SQL LIKE pattern (e.g., '%.json')
            start_date: Start of date range
            end_date: End of date range
            file_type: File extension filter
            limit: Maximum results
        
        Returns:
            List of matching backup records
        """
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM backups WHERE 1=1"
        params = []
        
        if filename_pattern:
            query += " AND filename LIKE ?"
            params.append(filename_pattern)
        
        if start_date:
            query += " AND backup_timestamp >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND backup_timestamp <= ?"
            params.append(end_date)
        
        if file_type:
            query += " AND file_type = ?"
            params.append(file_type)
        
        query += " ORDER BY backup_timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Example usage
if __name__ == "__main__":
    # Initialize database
    db = AIOSDatabase()
    
    # Example: Add a backup
    sample_content = b"Sample file content"
    backup_id, content_hash, is_dup = db.add_backup(
        filename="test.json",
        file_path="tachyonic/backups/test.json",
        content=sample_content,
        backup_timestamp=datetime.now(),
        file_type=".json",
        backup_type="test"
    )
    
    print(f"Backup ID: {backup_id}")
    print(f"Content Hash: {content_hash}")
    print(f"Is Duplicate: {is_dup}")
    
    # Get deduplication stats
    stats = db.get_deduplication_stats()
    print(f"\nDeduplication Stats:")
    print(f"  Total Backups: {stats['total_backups']}")
    print(f"  Unique Content: {stats['unique_content']}")
    print(f"  Space Saved: {stats['space_saved_percent']}%")
    
    db.close()
