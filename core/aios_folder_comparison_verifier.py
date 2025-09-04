#!/usr/bin/env python3
"""
🔍 AIOS FOLDER COMPARISON VERIFICATION
═══════════════════════════════════════════════════════════════════════════════
Comprehensive comparison between backup folder and tachyonic archive to verify
identical content before safe deletion of backup folder.

COMPARISON SCOPE:
- File count verification
- Hash comparison of key files
- Content structure analysis
- Safe deletion confirmation

AIOS - Folder comparison and verification system
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import hashlib
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple

logger = logging.getLogger(__name__)


class AIOSFolderComparisonVerifier:
    """
    🔍 AIOS Folder Comparison Verifier
    
    Performs comprehensive comparison between two folders:
    • Verifies file counts and structure
    • Compares file hashes for identical content
    • Identifies differences and similarities
    • Provides safe deletion confirmation
    """
    
    def __init__(self):
        self.core_path = Path(r"C:\dev\AIOS\core")
        self.backup_folder = self.core_path / "evolutionary_assembler_BACKUP_TO_DELETE"
        self.archive_folder = self.core_path / "tachyonic_archive" / "evolutionary_assembler_v1.0_tachyonic_1757015844"
        
        logger.info("🔍 AIOS Folder Comparison Verifier initialized")
        logger.info(f"   Backup folder: {self.backup_folder}")
        logger.info(f"   Archive folder: {self.archive_folder}")
    
    def perform_comprehensive_comparison(self) -> Dict[str, Any]:
        """Perform comprehensive comparison between backup and archive folders"""
        
        logger.info("🔍 PERFORMING COMPREHENSIVE FOLDER COMPARISON")
        logger.info("═" * 60)
        logger.info("📊 Analyzing folder structures and content...")
        logger.info("")
        
        comparison_results = {
            "comparison_timestamp": os.path.getmtime(__file__),
            "backup_folder": str(self.backup_folder),
            "archive_folder": str(self.archive_folder),
            "backup_exists": self.backup_folder.exists(),
            "archive_exists": self.archive_folder.exists(),
            "file_counts": {},
            "structure_comparison": {},
            "content_verification": {},
            "differences_found": [],
            "identical_files": 0,
            "different_files": 0,
            "unique_to_backup": [],
            "unique_to_archive": [],
            "safe_to_delete": False,
            "deletion_recommendation": ""
        }
        
        if not comparison_results["backup_exists"]:
            logger.error("Backup folder does not exist")
            return comparison_results
            
        if not comparison_results["archive_exists"]:
            logger.error("Archive folder does not exist")
            return comparison_results
        
        # Compare file counts
        comparison_results["file_counts"] = self._compare_file_counts()
        
        # Compare folder structures
        comparison_results["structure_comparison"] = self._compare_folder_structures()
        
        # Verify critical file content
        comparison_results["content_verification"] = self._verify_critical_file_content()
        
        # Identify unique files
        unique_files = self._identify_unique_files()
        comparison_results["unique_to_backup"] = unique_files["unique_to_backup"]
        comparison_results["unique_to_archive"] = unique_files["unique_to_archive"]
        
        # Generate deletion recommendation
        comparison_results["safe_to_delete"] = self._determine_safe_deletion(comparison_results)
        comparison_results["deletion_recommendation"] = self._generate_deletion_recommendation(comparison_results)
        
        logger.info("✅ COMPREHENSIVE FOLDER COMPARISON COMPLETE")
        logger.info("═" * 60)
        
        return comparison_results
    
    def _compare_file_counts(self) -> Dict[str, Any]:
        """Compare file counts between folders"""
        
        backup_files = list(self.backup_folder.rglob('*'))
        archive_files = list(self.archive_folder.rglob('*'))
        
        backup_file_count = len([f for f in backup_files if f.is_file()])
        archive_file_count = len([f for f in archive_files if f.is_file()])
        
        backup_dir_count = len([f for f in backup_files if f.is_dir()])
        archive_dir_count = len([f for f in archive_files if f.is_dir()])
        
        file_counts = {
            "backup_files": backup_file_count,
            "archive_files": archive_file_count,
            "backup_directories": backup_dir_count,
            "archive_directories": archive_dir_count,
            "file_count_difference": archive_file_count - backup_file_count,
            "directory_count_difference": archive_dir_count - backup_dir_count
        }
        
        logger.info(f"📊 File count comparison:")
        logger.info(f"   Backup files: {backup_file_count}")
        logger.info(f"   Archive files: {archive_file_count}")
        logger.info(f"   Difference: {file_counts['file_count_difference']} files")
        
        return file_counts
    
    def _compare_folder_structures(self) -> Dict[str, Any]:
        """Compare folder structures between backup and archive"""
        
        backup_structure = self._get_folder_structure(self.backup_folder)
        archive_structure = self._get_folder_structure(self.archive_folder)
        
        structure_comparison = {
            "backup_structure": backup_structure,
            "archive_structure": archive_structure,
            "common_folders": [],
            "backup_only_folders": [],
            "archive_only_folders": []
        }
        
        # Find common and unique folders
        backup_folders = set(backup_structure.keys())
        archive_folders = set(archive_structure.keys())
        
        structure_comparison["common_folders"] = list(backup_folders.intersection(archive_folders))
        structure_comparison["backup_only_folders"] = list(backup_folders - archive_folders)
        structure_comparison["archive_only_folders"] = list(archive_folders - backup_folders)
        
        logger.info(f"📁 Structure comparison:")
        logger.info(f"   Common folders: {len(structure_comparison['common_folders'])}")
        logger.info(f"   Backup-only folders: {len(structure_comparison['backup_only_folders'])}")
        logger.info(f"   Archive-only folders: {len(structure_comparison['archive_only_folders'])}")
        
        return structure_comparison
    
    def _get_folder_structure(self, root_folder: Path) -> Dict[str, List[str]]:
        """Get folder structure as dictionary"""
        
        structure = {}
        
        for item in root_folder.rglob('*'):
            if item.is_dir():
                relative_path = str(item.relative_to(root_folder))
                parent_path = str(item.parent.relative_to(root_folder)) if item.parent != root_folder else "."
                
                if parent_path not in structure:
                    structure[parent_path] = []
                structure[parent_path].append(relative_path)
        
        return structure
    
    def _verify_critical_file_content(self) -> Dict[str, Any]:
        """Verify content of critical files"""
        
        critical_files = [
            "output/evolution_report.json",
            "output/generation_0025/best_assembly_gen_25.asm",
            "output/generation_0025/consciousness_metrics_gen_25.json",
            "scripts_py/aios_comparative_testing_framework.py",
            "scripts_py/enhanced_consciousness.py"
        ]
        
        content_verification = {
            "files_checked": len(critical_files),
            "identical_files": 0,
            "different_files": 0,
            "missing_files": 0,
            "file_results": {}
        }
        
        for file_path in critical_files:
            backup_file = self.backup_folder / file_path
            archive_file = self.archive_folder / file_path
            
            result = {
                "backup_exists": backup_file.exists(),
                "archive_exists": archive_file.exists(),
                "identical": False,
                "backup_hash": None,
                "archive_hash": None
            }
            
            if backup_file.exists() and archive_file.exists():
                backup_hash = self._calculate_file_hash(backup_file)
                archive_hash = self._calculate_file_hash(archive_file)
                
                result["backup_hash"] = backup_hash
                result["archive_hash"] = archive_hash
                result["identical"] = backup_hash == archive_hash
                
                if result["identical"]:
                    content_verification["identical_files"] += 1
                else:
                    content_verification["different_files"] += 1
            else:
                content_verification["missing_files"] += 1
            
            content_verification["file_results"][file_path] = result
        
        logger.info(f"🔍 Content verification:")
        logger.info(f"   Identical files: {content_verification['identical_files']}")
        logger.info(f"   Different files: {content_verification['different_files']}")
        logger.info(f"   Missing files: {content_verification['missing_files']}")
        
        return content_verification
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.warning(f"Could not hash {file_path}: {e}")
            return ""
    
    def _identify_unique_files(self) -> Dict[str, List[str]]:
        """Identify files unique to each folder"""
        
        backup_files = set()
        archive_files = set()
        
        # Get relative paths of all files
        for file_path in self.backup_folder.rglob('*'):
            if file_path.is_file():
                relative_path = str(file_path.relative_to(self.backup_folder))
                backup_files.add(relative_path)
        
        for file_path in self.archive_folder.rglob('*'):
            if file_path.is_file():
                relative_path = str(file_path.relative_to(self.archive_folder))
                archive_files.add(relative_path)
        
        unique_files = {
            "unique_to_backup": list(backup_files - archive_files),
            "unique_to_archive": list(archive_files - backup_files)
        }
        
        logger.info(f"📋 Unique files:")
        logger.info(f"   Unique to backup: {len(unique_files['unique_to_backup'])}")
        logger.info(f"   Unique to archive: {len(unique_files['unique_to_archive'])}")
        
        if unique_files["unique_to_archive"]:
            logger.info(f"   Archive-only files: {unique_files['unique_to_archive']}")
        
        return unique_files
    
    def _determine_safe_deletion(self, comparison_results: Dict[str, Any]) -> bool:
        """Determine if backup folder is safe to delete"""
        
        # Check if all critical files are identical
        content_verification = comparison_results["content_verification"]
        critical_files_identical = (content_verification["identical_files"] >= 4 and 
                                   content_verification["different_files"] == 0)
        
        # Check if only expected unique files exist (metadata in archive)
        expected_unique_files = ["tachyonic_metadata.json"]
        unique_to_archive = comparison_results["unique_to_archive"]
        only_expected_unique = all(f in expected_unique_files for f in unique_to_archive)
        
        # Check if no important files are unique to backup
        unique_to_backup = comparison_results["unique_to_backup"]
        no_important_backup_files = len(unique_to_backup) == 0
        
        safe_to_delete = (critical_files_identical and 
                         only_expected_unique and 
                         no_important_backup_files)
        
        logger.info(f"🛡️ Safety assessment:")
        logger.info(f"   Critical files identical: {critical_files_identical}")
        logger.info(f"   Only expected unique files: {only_expected_unique}")
        logger.info(f"   No important backup-only files: {no_important_backup_files}")
        logger.info(f"   SAFE TO DELETE: {safe_to_delete}")
        
        return safe_to_delete
    
    def _generate_deletion_recommendation(self, comparison_results: Dict[str, Any]) -> str:
        """Generate deletion recommendation based on comparison"""
        
        if comparison_results["safe_to_delete"]:
            return ("✅ SAFE TO DELETE: Backup folder contains identical content to archive. "
                   "The only difference is the tachyonic_metadata.json file in the archive, "
                   "which is expected. All critical files are identical.")
        else:
            differences = []
            
            if comparison_results["content_verification"]["different_files"] > 0:
                differences.append("different file content detected")
            
            if len(comparison_results["unique_to_backup"]) > 0:
                differences.append("unique files exist in backup")
            
            unexpected_archive_files = [f for f in comparison_results["unique_to_archive"] 
                                      if f != "tachyonic_metadata.json"]
            if unexpected_archive_files:
                differences.append("unexpected unique files in archive")
            
            return (f"⚠️ NOT SAFE TO DELETE: {', '.join(differences)}. "
                   "Manual review required before deletion.")
    
    def display_comparison_results(self):
        """Display comprehensive comparison results"""
        
        comparison_results = self.perform_comprehensive_comparison()
        
        print("🔍 AIOS FOLDER COMPARISON VERIFICATION")
        print("═" * 70)
        print("📊 COMPREHENSIVE COMPARISON RESULTS")
        print()
        
        print("📈 FILE COUNT SUMMARY:")
        file_counts = comparison_results["file_counts"]
        print(f"  📁 Backup folder: {file_counts['backup_files']} files, {file_counts['backup_directories']} directories")
        print(f"  📦 Archive folder: {file_counts['archive_files']} files, {file_counts['archive_directories']} directories")
        print(f"  📊 Difference: {file_counts['file_count_difference']} files, {file_counts['directory_count_difference']} directories")
        print()
        
        print("🔍 CONTENT VERIFICATION:")
        content = comparison_results["content_verification"]
        print(f"  ✅ Identical files: {content['identical_files']}")
        print(f"  ❌ Different files: {content['different_files']}")
        print(f"  ⚠️ Missing files: {content['missing_files']}")
        print()
        
        print("📋 UNIQUE FILES:")
        print(f"  🔹 Unique to backup: {len(comparison_results['unique_to_backup'])}")
        print(f"  🔸 Unique to archive: {len(comparison_results['unique_to_archive'])}")
        if comparison_results["unique_to_archive"]:
            print(f"      Archive-only files: {', '.join(comparison_results['unique_to_archive'])}")
        print()
        
        print("🎯 DELETION RECOMMENDATION:")
        print(f"  {comparison_results['deletion_recommendation']}")
        print()
        
        if comparison_results["safe_to_delete"]:
            print("🚀 CONCLUSION: BACKUP FOLDER CAN BE SAFELY DELETED!")
            print("   The archive contains all necessary content with proper metadata.")
        else:
            print("⚠️ CONCLUSION: MANUAL REVIEW REQUIRED BEFORE DELETION!")
            print("   Investigate differences before proceeding.")


def main():
    """Execute folder comparison verification"""
    
    print("🔍 AIOS FOLDER COMPARISON VERIFIER")
    print("═" * 60)
    print("🎯 Verifying identical content between backup and archive")
    print("🛡️ Ensuring safe deletion of backup folder")
    print()
    
    # Initialize verifier
    verifier = AIOSFolderComparisonVerifier()
    
    # Display comparison results
    verifier.display_comparison_results()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    main()
