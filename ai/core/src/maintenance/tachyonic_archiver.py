"""
AIOS Tachyonic Archiver - Quantum Information Storage
====================================================

This module implements the tachyonic archival system for deep storage
of redundant and fragmented documentation with perfect recall capabilities.
"""

import hashlib
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class TachyonicArchiver:
    """
    Quantum-inspired archival system for deep information storage.

    Features:
    - SQLite-based tachyonic database for temporal coherence
    - Content hashing and deduplication
    - Metadata preservation and semantic tagging
    - Holographic reconstruction capabilities
    """

    def __init__(self, workspace_root: str, db_name: str = "tachyonic_archive.db"):
        self.workspace_root = Path(workspace_root)
        self.db_path = self.workspace_root / "docs" / db_name
        self._initialize_database()

    def _initialize_database(self):
        """Initialize the tachyonic database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS archived_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    content_hash TEXT UNIQUE NOT NULL,
                    content TEXT NOT NULL,
                    file_size INTEGER,
                    archive_timestamp TEXT,
                    original_path TEXT,
                    category TEXT,
                    keywords TEXT,
                    metadata TEXT
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_content_hash
                ON archived_documents(content_hash)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_category
                ON archived_documents(category)
            """)

    def archive_file(self, file_path: Path, category: str = "general",
                    metadata: Optional[Dict] = None) -> bool:
        """
        Archive a single file into the tachyonic database.

        Args:
            file_path: Path to the file to archive
            category: Content category for organization
            metadata: Additional metadata to store

        Returns:
            bool: True if successfully archived, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            content_hash = hashlib.sha256(content.encode()).hexdigest()
            keywords = self._extract_keywords(content)

            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO archived_documents
                    (filename, content_hash, content, file_size,
                     archive_timestamp, original_path, category,
                     keywords, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    file_path.name,
                    content_hash,
                    content,
                    len(content),
                    datetime.now().isoformat(),
                    str(file_path),
                    category,
                    json.dumps(keywords),
                    json.dumps(metadata) if metadata else "{}"
                ))

            return True

        except Exception as e:
            print(f"Error archiving {file_path}: {e}")
            return False

    def archive_multiple_files(self, file_paths: List[Path],
                              category_map: Optional[Dict[str, str]] = None) -> Dict:
        """
        Archive multiple files with batch processing.

        Args:
            file_paths: List of file paths to archive
            category_map: Optional mapping of filenames to categories

        Returns:
            Dict containing archival statistics
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "total_files": len(file_paths),
            "archived_successfully": 0,
            "errors": [],
            "duplicates_skipped": 0
        }

        for file_path in file_paths:
            try:
                category = "general"
                if category_map and file_path.name in category_map:
                    category = category_map[file_path.name]

                success = self.archive_file(file_path, category)
                if success:
                    result["archived_successfully"] += 1

            except Exception as e:
                result["errors"].append(f"Error with {file_path}: {e}")

        return result

    def search_archive(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """
        Search the tachyonic archive for content.

        Args:
            query: Search query string
            category: Optional category filter

        Returns:
            List of matching documents with metadata
        """
        with sqlite3.connect(self.db_path) as conn:
            if category:
                cursor = conn.execute("""
                    SELECT filename, content_hash, archive_timestamp,
                           original_path, category, keywords
                    FROM archived_documents
                    WHERE (content LIKE ? OR keywords LIKE ?)
                    AND category = ?
                    ORDER BY archive_timestamp DESC
                """, (f"%{query}%", f"%{query}%", category))
            else:
                cursor = conn.execute("""
                    SELECT filename, content_hash, archive_timestamp,
                           original_path, category, keywords
                    FROM archived_documents
                    WHERE content LIKE ? OR keywords LIKE ?
                    ORDER BY archive_timestamp DESC
                """, (f"%{query}%", f"%{query}%"))

            return [
                {
                    "filename": row[0],
                    "content_hash": row[1],
                    "archive_timestamp": row[2],
                    "original_path": row[3],
                    "category": row[4],
                    "keywords": json.loads(row[5])
                }
                for row in cursor.fetchall()
            ]

    def retrieve_content(self, content_hash: str) -> Optional[str]:
        """
        Retrieve full content by hash for holographic reconstruction.

        Args:
            content_hash: SHA-256 hash of the content

        Returns:
            Full content string or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT content FROM archived_documents WHERE content_hash = ?",
                (content_hash,)
            )
            row = cursor.fetchone()
            return row[0] if row else None

    def get_archive_statistics(self) -> Dict:
        """Get comprehensive archive statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT
                    COUNT(*) as total_documents,
                    SUM(file_size) as total_size,
                    COUNT(DISTINCT category) as unique_categories,
                    MIN(archive_timestamp) as earliest_archive,
                    MAX(archive_timestamp) as latest_archive
                FROM archived_documents
            """)

            row = cursor.fetchone()

            # Get category breakdown
            category_cursor = conn.execute("""
                SELECT category, COUNT(*)
                FROM archived_documents
                GROUP BY category
            """)

            categories = dict(category_cursor.fetchall())

            return {
                "total_documents": row[0],
                "total_size_bytes": row[1] or 0,
                "unique_categories": row[2],
                "earliest_archive": row[3],
                "latest_archive": row[4],
                "category_breakdown": categories
            }

    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from content for indexing."""
        # Simple keyword extraction
        words = content.lower().split()
        meaningful_words = [w for w in words if len(w) > 4 and w.isalpha()]

        # Return top 10 most frequent words
        from collections import Counter
        return [word for word, count in Counter(meaningful_words).most_common(10)]
