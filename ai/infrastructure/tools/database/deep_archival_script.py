#!/usr/bin/env python3
"""
AINLP Deep Archival Script
==========================

Stores semantic validator in AIOS database using database interface bridge
for permanent deep archival, then removes local file to unclutter.

AINLP Standards:
- Intelligence delimitation: Contextually bound archival
- Semantic compression: Efficient storage patterns
- Tachyonic archival: Hyperdimensional database storage
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add AI tools to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from aios_database import AIOSDatabase


def deep_archive_semantic_validator():
    """Perform deep archival of semantic validator to AIOS database"""

    print("🔮 Starting Deep Archival Process...")

    # Initialize database connection
    db = AIOSDatabase("tachyonic/aios_data.db")

    # File paths
    source_file = Path(
        "../../../tachyonic/database/" "semantic_validator_20251025_210000.py"
    )
    cleanup_record = Path(
        "../../../tachyonic/database/" "cleanup_semantic_validator_20251025_210000.json"
    )

    if not source_file.exists():
        print(f"❌ Source file not found: {source_file}")
        return False

    # Read file content
    print(f"📖 Reading semantic validator: {source_file}")
    content = source_file.read_bytes()

    # Read cleanup metadata
    cleanup_metadata = {}
    if cleanup_record.exists():
        cleanup_metadata = json.loads(cleanup_record.read_text())

    # Prepare archival metadata
    archival_timestamp = datetime.now()

    # Store in database with deep archival
    print("💾 Storing in AIOS database...")
    backup_id, content_hash, is_duplicate = db.add_backup(
        filename="semantic_validator_20251025_210000.py",
        file_path=str(source_file),
        content=content,
        backup_timestamp=archival_timestamp,
        file_type="python",
        backup_type="deep_archival_validation_tools",
    )

    # Store cleanup metadata as separate backup
    if cleanup_metadata:
        cleanup_content = json.dumps(cleanup_metadata, indent=2).encode("utf-8")
        cleanup_id, cleanup_hash, cleanup_duplicate = db.add_backup(
            filename="cleanup_semantic_validator_20251025_210000.json",
            file_path=str(cleanup_record),
            content=cleanup_content,
            backup_timestamp=archival_timestamp,
            file_type="json",
            backup_type="deep_archival_metadata",
        )

    # Get deduplication stats
    stats = db.get_deduplication_stats()

    print("✅ Deep Archival Complete!")
    print(f"   📊 Backup ID: {backup_id}")
    print(f"   🔐 Content Hash: {content_hash[:16]}...")
    print(f"   🔄 Duplicate: {is_duplicate}")
    print(
        f"   💾 Database Stats: {stats['total_backups']} backups, "
        f"{stats['space_saved_percent']}% space saved"
    )

    # Remove local files to unclutter
    print("🧹 Removing local files...")
    source_file.unlink()
    if cleanup_record.exists():
        cleanup_record.unlink()

    print("✨ Deep archival complete - workspace uncluttered!")
    print("   📁 Files permanently stored in: tachyonic/aios_data.db")
    print(
        "   🔍 Query with: SELECT * FROM backups WHERE filename "
        "LIKE 'semantic_validator%'"
    )

    return True


if __name__ == "__main__":
    success = deep_archive_semantic_validator()
    sys.exit(0 if success else 1)
