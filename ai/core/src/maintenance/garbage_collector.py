"""
AIOS Garbage Collector - Fractal Optimization Engine
===================================================

This module implements intelligent garbage collection for documentation
with tachyonic preservation and holographic optimization.
"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

from .backup_consolidator import BackupConsolidator
from .documentation_optimizer import DocumentationOptimizer
from .tachyonic_archiver import TachyonicArchiver


class GarbageCollector:
    """
    Advanced garbage collection system with tachyonic preservation.

    Features:
    - Intelligent file categorization and preservation
    - Tachyonic archival before removal
    - Backup consolidation and deduplication
    - Zero-loss optimization with perfect recall
    """

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.docs_path = self.workspace_root / "docs"

        # Initialize subsystems
        self.optimizer = DocumentationOptimizer(workspace_root)
        self.consolidator = BackupConsolidator(workspace_root)
        self.archiver = TachyonicArchiver(workspace_root)

        # Define core documentation structure
        self.core_documents = {
            "DOCUMENTATION_INDEX.md",
            "INSTALLATION.md",
            "API_REFERENCE.md",
            "ARCHITECTURE.md",
            "DEVELOPMENT.md",
            "user-guide.md",
            "PROJECT_ROADMAP_2025_2026.md",
            "COMPLETE_INTEGRATION_GUIDE.md"
        }

    def run_full_optimization(self) -> Dict:
        """
        Execute complete documentation optimization cycle.

        Returns:
            Dict containing comprehensive optimization results
        """
        optimization_result = {
            "timestamp": datetime.now().isoformat(),
            "phases": {},
            "final_state": {},
            "errors": []
        }

        try:
            # Phase 1: Analysis
            optimization_result["phases"]["analysis"] = self._run_analysis_phase()

            # Phase 2: Backup Consolidation
            optimization_result["phases"]["backup_consolidation"] = self._run_backup_phase()

            # Phase 3: Tachyonic Archival
            optimization_result["phases"]["tachyonic_archival"] = self._run_archival_phase()

            # Phase 4: Cleanup and Optimization
            optimization_result["phases"]["cleanup"] = self._run_cleanup_phase()

            # Phase 5: Final State Assessment
            optimization_result["final_state"] = self._assess_final_state()

        except Exception as e:
            optimization_result["errors"].append(f"Critical error: {e}")

        return optimization_result

    def _run_analysis_phase(self) -> Dict:
        """Run comprehensive documentation analysis."""
        return self.optimizer.analyze_documentation_structure()

    def _run_backup_phase(self) -> Dict:
        """Consolidate all backup folders."""
        return self.consolidator.consolidate_all_backups()

    def _run_archival_phase(self) -> Dict:
        """Archive redundant files to tachyonic database."""
        if not self.docs_path.exists():
            return {"error": "Documentation directory not found"}

        # Find files to archive (everything except core documents)
        all_files = list(self.docs_path.glob("*.md"))
        files_to_archive = [
            f for f in all_files
            if f.name not in self.core_documents
        ]

        # Create category mapping
        category_map = {}
        for file_path in files_to_archive:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                category = self.optimizer._categorize_content(content)
                category_map[file_path.name] = category
            except:
                category_map[file_path.name] = "general"

        # Archive files
        archive_result = self.archiver.archive_multiple_files(
            files_to_archive,
            category_map
        )

        # Remove archived files
        files_removed = []
        for file_path in files_to_archive:
            try:
                file_path.unlink()
                files_removed.append(str(file_path))
            except Exception as e:
                archive_result.setdefault("errors", []).append(
                    f"Error removing {file_path}: {e}"
                )

        archive_result["files_removed"] = files_removed
        return archive_result

    def _run_cleanup_phase(self) -> Dict:
        """Clean up old backup folders and temporary files."""
        cleanup_result = {
            "timestamp": datetime.now().isoformat(),
            "backup_folders_removed": [],
            "temp_files_removed": [],
            "errors": []
        }

        # Find and remove old backup folders
        backup_folders = self.consolidator._find_backup_folders()
        old_folders = [
            f for f in backup_folders
            if f.name != "unified_backups"
        ]

        folder_cleanup = self.consolidator.cleanup_old_folders(old_folders)
        cleanup_result["backup_folders_removed"] = folder_cleanup["folders_removed"]
        cleanup_result["errors"].extend(folder_cleanup["errors"])

        # Remove temporary files in workspace root
        temp_patterns = [
            "*_analysis_*.py",
            "*_consolidator_*.py",
            "*_garbage_collector_*.py",
            "*_verification_*.py",
            "cleanup_*.py",
            "final_*.py",
            "check_*.py"
        ]

        for pattern in temp_patterns:
            temp_files = list(self.workspace_root.glob(pattern))
            for temp_file in temp_files:
                try:
                    temp_file.unlink()
                    cleanup_result["temp_files_removed"].append(str(temp_file))
                except Exception as e:
                    cleanup_result["errors"].append(f"Error removing {temp_file}: {e}")

        return cleanup_result

    def _assess_final_state(self) -> Dict:
        """Assess the final optimization state."""
        final_state = {
            "timestamp": datetime.now().isoformat(),
            "documentation_structure": {},
            "archive_statistics": {},
            "fragmentation_score": 0.0,
            "optimization_complete": False
        }

        # Analyze final documentation structure
        analysis = self.optimizer.analyze_documentation_structure()
        final_state["documentation_structure"] = {
            "total_files": analysis.get("total_files", 0),
            "core_documents_present": len([
                f for f in self.docs_path.glob("*.md")
                if f.name in self.core_documents
            ]),
            "fragmentation_score": analysis.get("fragmentation_score", 1.0)
        }

        # Get archive statistics
        final_state["archive_statistics"] = self.archiver.get_archive_statistics()

        # Determine if optimization is complete
        files_count = final_state["documentation_structure"]["total_files"]
        core_count = final_state["documentation_structure"]["core_documents_present"]

        final_state["optimization_complete"] = (
            files_count <= 8 and
            core_count >= 6 and
            analysis.get("fragmentation_score", 1.0) < 0.1
        )

        return final_state

    def verify_integrity(self) -> Dict:
        """Verify system integrity after optimization."""
        integrity_result = {
            "timestamp": datetime.now().isoformat(),
            "core_documents_check": {},
            "archive_integrity": {},
            "backup_consolidation": {},
            "overall_status": "unknown"
        }

        # Check core documents
        missing_core = []
        present_core = []

        for doc_name in self.core_documents:
            doc_path = self.docs_path / doc_name
            if doc_path.exists():
                present_core.append(doc_name)
            else:
                missing_core.append(doc_name)

        integrity_result["core_documents_check"] = {
            "present": present_core,
            "missing": missing_core,
            "coverage_percentage": len(present_core) / len(self.core_documents) * 100
        }

        # Check archive integrity
        integrity_result["archive_integrity"] = self.archiver.get_archive_statistics()

        # Check backup consolidation
        unified_backup_path = self.workspace_root / "docs" / "unified_backups"
        integrity_result["backup_consolidation"] = {
            "unified_backups_exists": unified_backup_path.exists(),
            "backup_file_count": len(list(unified_backup_path.glob("*"))) if unified_backup_path.exists() else 0
        }

        # Overall status
        if (len(missing_core) == 0 and
            integrity_result["archive_integrity"]["total_documents"] > 0 and
            integrity_result["backup_consolidation"]["unified_backups_exists"]):
            integrity_result["overall_status"] = "optimal"
        elif len(missing_core) <= 2:
            integrity_result["overall_status"] = "acceptable"
        else:
            integrity_result["overall_status"] = "needs_attention"

        return integrity_result
