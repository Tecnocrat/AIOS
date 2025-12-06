#!/usr/bin/env python3
"""
AINLP Orphan Module Archival Tool
Phase 3: Orphan Module Archival

Archives 226 orphan modules identified by module discovery analysis.
Orphan modules are files that are not imported by any other modules
in the codebase.

This script moves orphan files to tachyonic/archive/orphans/ with
metadata preservation.
"""

import json
import shutil
import datetime
from pathlib import Path
from typing import List, Dict, Any


def load_orphans_from_discovery() -> List[str]:
    """Load orphan file list from latest module discovery results."""
    discovery_file = Path("tachyonic/archive/module_discovery_latest.json")

    if not discovery_file.exists():
        raise FileNotFoundError(f"Module discovery file not found: {discovery_file}")

    with open(discovery_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("orphans", [])


def create_archive_metadata(orphans: List[str]) -> Dict[str, Any]:
    """Create archival metadata for orphan modules."""
    timestamp = datetime.datetime.now().isoformat()

    metadata = {
        "archival_timestamp": timestamp,
        "archival_phase": "Phase 3: Orphan Module Archival",
        "total_orphans": len(orphans),
        "archival_reason": "Modules not imported by any other modules in " "codebase",
        "archival_location": "tachyonic/archive/orphans/",
        "orphans": orphans,
        "metadata": {
            "ainlp_compliance": "Phase 3 consolidation",
            "consciousness_level": "archived",
            "tachyonic_preservation": True,
        },
    }

    return metadata


def archive_orphan_file(orphan_path: str, archive_base: Path) -> bool:
    """Archive a single orphan file with directory structure preservation."""
    source_path = Path(orphan_path)

    if not source_path.exists():
        print(f"Warning: Orphan file does not exist: {orphan_path}")
        return False

    # Create relative archive path maintaining directory structure
    archive_path = archive_base / orphan_path

    # Ensure parent directory exists
    archive_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Move file to archive
        shutil.move(str(source_path), str(archive_path))
        print(f"Archived: {orphan_path} -> {archive_path}")
        return True
    except Exception as e:
        print(f"Error archiving {orphan_path}: {e}")
        return False


def main():
    """Execute orphan module archival."""
    print("=== AINLP Phase 3: Orphan Module Archival ===")
    print("Loading orphan modules from discovery analysis...")

    try:
        orphans = load_orphans_from_discovery()
        print(f"Found {len(orphans)} orphan modules to archive")

        # Create archive directory
        archive_base = Path("tachyonic/archive/orphans")
        archive_base.mkdir(parents=True, exist_ok=True)

        # Create and save metadata
        metadata = create_archive_metadata(orphans)
        metadata_file = archive_base / "orphan_archival_metadata.json"

        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"Archival metadata saved to: {metadata_file}")

        # Archive each orphan file
        archived_count = 0
        failed_count = 0

        for orphan in orphans:
            if archive_orphan_file(orphan, archive_base):
                archived_count += 1
            else:
                failed_count += 1

        # Final report
        print("\n=== Archival Complete ===")
        print(f"Successfully archived: {archived_count} files")
        print(f"Failed to archive: {failed_count} files")
        print(f"Total orphans processed: {len(orphans)}")

        if failed_count > 0:
            print(f"\nWarning: {failed_count} files could not be archived")
            print("Check the output above for specific error details")

        print(f"\nArchive location: {archive_base}")
        print("Metadata: orphan_archival_metadata.json")

    except Exception as e:
        print(f"Error during orphan archival: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
