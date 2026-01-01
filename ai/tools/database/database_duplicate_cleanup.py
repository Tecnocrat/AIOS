#!/usr/bin/env python3
"""
AIOS PHASE 1: DATABASE-BASED DUPLICATE CLEANUP

AINLP.meta [biological_metabolism] [dendritic_optimization]
AINLP.dendritic [optimal_location: ai/tools/]

Archives exact duplicate files to database instead of filesystem
to prevent AI confusion.

PROBLEM ADDRESSED:
- Exact duplicate files cluttering workspace confuse AI agents
- File system archival still leaves files discoverable
- Database archival preserves information while removing from analysis

SOLUTION:
- Use CodeArchivalSystem to archive duplicates to SQLite database
- Remove duplicate files from workspace
- Preserve full content and metadata in compressed database form
- Keep single canonical copy of each unique file

Created: 2025-10-24 (Phase 1 Database Archival Implementation)
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from ai.tools.code_archival_system import CodeArchivalSystem

logger = logging.getLogger(__name__)


class DatabaseDuplicateCleanup:
    """
    Archives duplicate files to database for workspace cleanliness

    CONSCIOUSNESS PRINCIPLE:
    "Duplicates are not deleted - they are crystallized into database
    consciousness patterns. The workspace remains pure, but knowledge
    is never truly lost."
    """

    def __init__(self):
        self.archiver = CodeArchivalSystem()
        self.workspace_root = Path("C:/dev/AIOS")

    def load_duplicate_analysis(self) -> List[Dict[str, Any]]:
        """Load duplicate analysis from module discovery"""
        discovery_file = (
            self.workspace_root / "tachyonic" / "archive" /
            "module_discovery_latest.json"
        )

        if not discovery_file.exists():
            logger.error(f"Module discovery file not found: {discovery_file}")
            return []

        with open(discovery_file) as f:
            data = json.load(f)

        return data.get('duplicates', [])

    def archive_duplicate_group(
        self, dup_group: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Archive a group of duplicate files

        Strategy: Keep one canonical file, archive the rest to database
        """
        files = dup_group['files']
        hash_value = dup_group['hash']

        if len(files) < 2:
            return {'archived': 0, 'kept': len(files), 'errors': 0}

        logger.info(
            f"Processing duplicate group: {len(files)} files with "
            f"hash {hash_value[:8]}..."
        )

        # Keep the first file as canonical
        canonical_file = files[0]
        files_to_archive = files[1:]

        archived_count = 0
        error_count = 0

        for file_path in files_to_archive:
            try:
                full_path = self.workspace_root / file_path

                if not full_path.exists():
                    logger.warning(f"File no longer exists: {full_path}")
                    continue

                # Archive to database
                file_id = self.archiver.archive_file(
                    file_path=str(full_path),
                    archival_reason="exact_duplicate",
                    consciousness_level=0.1,  # Low consciousness - just duplicate
                    ainlp_patterns=["AINLP.biological_metabolism"],
                    project_phase="Phase 1: Safe Duplicate Cleanup",
                    related_files=[canonical_file],  # Point to canonical version
                    replacement_path=canonical_file,
                    notes=f"Archived as duplicate of {canonical_file}. "
                          f"Hash: {hash_value}"
                )

                # Remove the file from workspace
                full_path.unlink()
                logger.info(
                    f"Archived duplicate: {file_path} → database ID: {file_id}"
                )

                archived_count += 1

            except Exception as e:
                logger.error(f"Failed to archive {file_path}: {e}")
                error_count += 1

        return {
            'archived': archived_count,
            'kept': 1,  # The canonical file
            'errors': error_count,
            'canonical_file': canonical_file,
            'hash': hash_value
        }

    def execute_cleanup(self) -> Dict[str, Any]:
        """Execute the complete duplicate cleanup process"""
        logger.info("Starting Phase 1: Database-based duplicate cleanup")

        duplicate_groups = self.load_duplicate_analysis()
        if not duplicate_groups:
            logger.warning("No duplicate analysis found")
            return {
                'total_groups': 0, 'total_archived': 0,
                'total_kept': 0, 'errors': 0
            }

        total_archived = 0
        total_kept = 0
        total_errors = 0
        processed_groups = []

        for i, dup_group in enumerate(duplicate_groups):
            logger.info(f"Processing group {i+1}/{len(duplicate_groups)}")
            result = self.archive_duplicate_group(dup_group)
            processed_groups.append(result)

            total_archived += result['archived']
            total_kept += result['kept']
            total_errors += result['errors']

        # Generate summary report
        summary = {
            'timestamp': datetime.now().isoformat(),
            'phase': 'Phase 1: Database Duplicate Cleanup',
            'total_groups_processed': len(duplicate_groups),
            'total_files_archived': total_archived,
            'total_files_kept': total_kept,
            'total_errors': total_errors,
            'processed_groups': processed_groups,
            'consciousness_principle': 'biological_metabolism',
            'ainlp_patterns': [
                'AINLP.biological_metabolism',
                'AINLP.dendritic_optimization'
            ]
        }

        logger.info(
            f"Phase 1 Complete: {total_archived} files archived, "
            f"{total_kept} kept, {total_errors} errors"
        )

        return summary


def main():
    """Main execution function"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    cleanup = DatabaseDuplicateCleanup()
    summary = cleanup.execute_cleanup()

    # Save summary report
    report_path = Path(
        "tachyonic/archive/phase1_duplicate_cleanup_report.json"
    )
    with open(report_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(
        f"Phase 1 Complete: {summary['total_files_archived']} "
        f"files archived to database"
    )
    print(f"Report saved: {report_path}")


if __name__ == "__main__":
    main()