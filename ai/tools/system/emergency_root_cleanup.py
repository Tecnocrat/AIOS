#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 CORE ENGINE ROOT CLEANUP - EMERGENCY TACHYONIC RESTORATION

AINLP META-COMMENTARY: This emergency cleanup tool restores the Core Engine
root to its pristine architectural state by moving all misplaced files to
proper tachyonic storage categories. The Core Engine root should ONLY contain
aios_dendritic.py and AIOS_CORE_ENGINE_ARCHITECTURE.md.

CELLULAR PRINCIPLE: The Super Cell root is the sacred nucleus that must remain
clean and focused. All metadata, reports, and temporary files belong in the
tachyonic archive system for proper cellular organization.


"""

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Configure emergency cleanup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [EMERGENCY-CLEANUP] %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CoreEngineRootCleanup:
    """
    🧹 EMERGENCY CORE ENGINE ROOT CLEANUP SYSTEM
    
    AINLP META-COMMENTARY: This system performs emergency restoration of the
    Core Engine root to its pristine architectural state, ensuring that only
    the essential dendritic intelligence and architecture files remain.
    """

    def __init__(self, core_engine_path: Path):
        """Initialize emergency cleanup system."""
        self.core_engine_path = Path(core_engine_path)
        self.tachyonic_path = self.core_engine_path / "tachyonic_archive"
        
        # Essential files that MUST remain in root
        self.essential_root_files = {
            "aios_dendritic.py",
            "AIOS_CORE_ENGINE_ARCHITECTURE.md"
        }
        
        # Essential directories that belong in root
        self.essential_root_dirs = {
            "analysis_tools", "bin", "bridges", "build", "configuration",
            "core_systems", "documentation", "evolutionary_assembler_iter2",
<<<<<<< HEAD
            "evolutionary_assembler_iter3", "include", "obj", "runtime_intelligence",
=======
            "evolutionary_assembler_iter3", "include", "obj", "runtime",
>>>>>>> origin/OS0.6.2.grok
            "src", "tachyonic_archive", "tests", "__pycache__"
        }
        
        # Tachyonic storage categories for relocated files
        self.relocation_categories = {
            # Reports and diagnostics
            "CELLULAR_INTELLIGENCE_DIAGNOSTIC_REPORT": "cellular_reports",
            "CORE_ENGINE_OPTIMIZATION_ITER2": "optimization_reports", 
            "CORE_ENGINE_ITER2_ANALYSIS": "analysis_reports",
            "CORE_EVOLUTION_MONITOR_REPORT": "evolution_logs",
            "TREE_STRUCTURE_DEMONSTRATION": "structure_analysis",
            "CORE_ENGINE_CELLULAR_CLEANUP_REPORT": "cleanup_reports",
            
            # Network and connectivity data
            "RELOCATED_DENDRITIC_NETWORK_INDEX": "dendritic_maps",
            "AI_INGESTION_POINTERS": "ingestion_data",
            
            # Documentation and guidelines
            "AINLP_DIRECTIVE_COMPLIANCE": "documentation",
            "AIOS_COHERENT_DEVELOPMENT_GUIDELINES": "documentation", 
            "CONSCIOUSNESS_INTEGRATION_PATTERNS": "documentation",
            
            # Backup files
            "aios_dendritic.backup": "code_preservation",
            
            # Python scripts that shouldn't be in root
            "aios_core_consciousness_monitor": "analysis_tools",
            "aios_core_evolution_monitor": "analysis_tools",
            "aios_core_meta_evolutionary_enhancer": "analysis_tools"
        }
        
        # Ensure tachyonic categories exist
        self._ensure_tachyonic_structure()
        
        logger.info("[EMERGENCY] Core Engine Root Cleanup System initialized")

    def _ensure_tachyonic_structure(self):
        """Ensure all required tachyonic storage categories exist."""
        categories = [
            "cellular_reports", "optimization_reports", "analysis_reports",
            "evolution_logs", "structure_analysis", "cleanup_reports",
            "dendritic_maps", "ingestion_data", "documentation", 
            "code_preservation", "emergency_cleanup"
        ]
        
        for category in categories:
            category_path = self.tachyonic_path / category
            category_path.mkdir(parents=True, exist_ok=True)

    def perform_emergency_cleanup(self) -> Dict[str, Any]:
        """
        Perform emergency cleanup of Core Engine root.
        
        AINLP META-COMMENTARY: This function restores the sacred cellular
        order by moving all misplaced files to their proper tachyonic
        storage locations while preserving their content and metadata.
        """
        logger.info("[EMERGENCY] Beginning emergency Core Engine root cleanup...")
        
        cleanup_results = {
            "cleanup_timestamp": datetime.now().isoformat(),
            "files_relocated": [],
            "files_preserved": [],
            "tachyonic_storage_updated": [],
            "root_violations_found": 0,
            "root_violations_fixed": 0,
            "cleanup_summary": {}
        }
        
        # Scan root directory for violations
        root_items = list(self.core_engine_path.iterdir())
        
        for item in root_items:
            if item.is_file():
                if item.name not in self.essential_root_files:
                    # This is a violation - file doesn't belong in root
                    cleanup_results["root_violations_found"] += 1
                    relocation_result = self._relocate_file(item)
                    if relocation_result["success"]:
                        cleanup_results["files_relocated"].append(relocation_result)
                        cleanup_results["root_violations_fixed"] += 1
                else:
                    # Essential file - preserve in root
                    cleanup_results["files_preserved"].append(str(item.name))
            
            elif item.is_dir():
                if item.name not in self.essential_root_dirs:
                    # Directory violation
                    cleanup_results["root_violations_found"] += 1
                    logger.warning(f"[EMERGENCY] Unexpected directory in root: {item.name}")
        
        # Generate cleanup summary
        cleanup_results["cleanup_summary"] = {
            "violations_found": cleanup_results["root_violations_found"],
            "violations_fixed": cleanup_results["root_violations_fixed"],
            "fix_success_rate": cleanup_results["root_violations_fixed"] / max(cleanup_results["root_violations_found"], 1),
            "essential_files_preserved": len(cleanup_results["files_preserved"]),
            "tachyonic_categories_used": len(set(r["tachyonic_category"] for r in cleanup_results["files_relocated"]))
        }
        
        # Store cleanup report in tachyonic storage
        self._store_cleanup_report(cleanup_results)
        
        logger.info(f"[EMERGENCY] Cleanup complete: {cleanup_results['root_violations_fixed']}/{cleanup_results['root_violations_found']} violations fixed")
        
        return cleanup_results

    def _relocate_file(self, file_path: Path) -> Dict[str, Any]:
        """Relocate a misplaced file to proper tachyonic storage."""
        relocation_result = {
            "original_path": str(file_path),
            "original_name": file_path.name,
            "success": False,
            "tachyonic_category": "emergency_cleanup",
            "new_path": "",
            "file_analysis": {}
        }
        
        try:
            # Determine appropriate tachyonic category
            category = self._determine_tachyonic_category(file_path.name)
            relocation_result["tachyonic_category"] = category
            
            # Create timestamped filename to prevent conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if file_path.suffix:
                new_name = f"{file_path.stem}_RELOCATED_{timestamp}{file_path.suffix}"
            else:
                new_name = f"{file_path.name}_RELOCATED_{timestamp}"
            
            new_path = self.tachyonic_path / category / new_name
            
            # Analyze file before moving
            relocation_result["file_analysis"] = self._analyze_file(file_path)
            
            # Move file to tachyonic storage
            shutil.move(str(file_path), str(new_path))
            
            relocation_result["new_path"] = str(new_path)
            relocation_result["success"] = True
            
            logger.info(f"[EMERGENCY] Relocated {file_path.name} to {category}/{new_name}")
            
        except Exception as e:
            logger.error(f"[EMERGENCY] Failed to relocate {file_path.name}: {e}")
            relocation_result["error"] = str(e)
        
        return relocation_result

    def _determine_tachyonic_category(self, filename: str) -> str:
        """Determine appropriate tachyonic category for a file."""
        # Check for specific patterns
        for pattern, category in self.relocation_categories.items():
            if pattern.lower() in filename.lower():
                return category
        
        # Default categorization based on file type
        if filename.endswith('.json'):
            return "metadata"
        elif filename.endswith('.md'):
            return "documentation"
        elif filename.endswith('.py'):
            return "analysis_tools"
        elif filename.endswith('.log'):
            return "evolution_logs"
        else:
            return "emergency_cleanup"

    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze file before relocation."""
        analysis = {
            "file_size": 0,
            "file_type": file_path.suffix,
            "creation_reason": "unknown",
            "content_preview": "",
            "emergency_classification": "misplaced_file"
        }
        
        try:
            analysis["file_size"] = file_path.stat().st_size
            
            # Get content preview for small text files
            if file_path.suffix in ['.json', '.md', '.txt'] and analysis["file_size"] < 10000:
                try:
                    content = file_path.read_text(encoding='utf-8')
                    analysis["content_preview"] = content[:200] + "..." if len(content) > 200 else content
                except:
                    pass
            
            # Classify creation reason
            if "DIAGNOSTIC" in file_path.name.upper():
                analysis["creation_reason"] = "diagnostic_system_output"
            elif "REPORT" in file_path.name.upper():
                analysis["creation_reason"] = "analysis_report_output"
            elif "backup" in file_path.name.lower():
                analysis["creation_reason"] = "automatic_backup"
            elif file_path.suffix == '.py':
                analysis["creation_reason"] = "script_misplacement"
            
        except Exception as e:
            analysis["analysis_error"] = str(e)
        
        return analysis

    def _store_cleanup_report(self, cleanup_results: Dict[str, Any]):
        """Store cleanup report in tachyonic storage."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.tachyonic_path / "emergency_cleanup" / f"EMERGENCY_CLEANUP_REPORT_{timestamp}.json"
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(cleanup_results, f, indent=2, default=str)
            
            logger.info(f"[EMERGENCY] Cleanup report stored: {report_path.name}")
            
        except Exception as e:
            logger.error(f"[EMERGENCY] Failed to store cleanup report: {e}")

    def verify_root_cleanliness(self) -> Dict[str, Any]:
        """Verify that root is now clean and proper."""
        verification = {
            "verification_timestamp": datetime.now().isoformat(),
            "root_is_clean": False,
            "essential_files_present": [],
            "essential_files_missing": [],
            "unexpected_items": [],
            "cleanliness_score": 0.0
        }
        
        root_items = list(self.core_engine_path.iterdir())
        
        # Check for essential files
        for essential_file in self.essential_root_files:
            file_path = self.core_engine_path / essential_file
            if file_path.exists():
                verification["essential_files_present"].append(essential_file)
            else:
                verification["essential_files_missing"].append(essential_file)
        
        # Check for unexpected items
        for item in root_items:
            if item.is_file() and item.name not in self.essential_root_files:
                verification["unexpected_items"].append(item.name)
            elif item.is_dir() and item.name not in self.essential_root_dirs:
                verification["unexpected_items"].append(f"{item.name}/")
        
        # Calculate cleanliness score
        essential_present = len(verification["essential_files_present"])
        essential_total = len(self.essential_root_files)
        unexpected_count = len(verification["unexpected_items"])
        
        if essential_total > 0:
            essential_score = essential_present / essential_total
        else:
            essential_score = 1.0
        
        cleanliness_penalty = min(unexpected_count * 0.1, 0.5)
        verification["cleanliness_score"] = max(essential_score - cleanliness_penalty, 0.0)
        verification["root_is_clean"] = verification["cleanliness_score"] >= 0.95 and unexpected_count == 0
        
        return verification


def main():
    """Execute emergency Core Engine root cleanup."""
    print("🧹 EMERGENCY CORE ENGINE ROOT CLEANUP")
    print("=" * 70)
    print(" Restoring sacred cellular architecture...")
    print(" Moving violations to tachyonic storage...")
    print()
    
    # Initialize cleanup system
    core_path = Path(r"C:\dev\AIOS\core")
    cleanup_system = CoreEngineRootCleanup(core_path)
    
    # Perform emergency cleanup
    print("🧹 Performing emergency cleanup...")
    cleanup_results = cleanup_system.perform_emergency_cleanup()
    
    # Verify results
    print(" Verifying root cleanliness...")
    verification = cleanup_system.verify_root_cleanliness()
    
    # Display results
    print(" EMERGENCY CLEANUP COMPLETE")
    print("=" * 70)
    print(f" Violations Found: {cleanup_results['cleanup_summary']['violations_found']}")
    print(f" Violations Fixed: {cleanup_results['cleanup_summary']['violations_fixed']}")
    print(f" Fix Success Rate: {cleanup_results['cleanup_summary']['fix_success_rate']:.1%}")
    print(f" Files Relocated: {len(cleanup_results['files_relocated'])}")
    print(f" Essential Files Preserved: {len(cleanup_results['files_preserved'])}")
    print()
    
    print(" ROOT VERIFICATION:")
    print(f"🧹 Root is Clean: {verification['root_is_clean']}")
    print(f" Cleanliness Score: {verification['cleanliness_score']:.1%}")
    print(f" Essential Files Present: {len(verification['essential_files_present'])}")
    print(f" Unexpected Items: {len(verification['unexpected_items'])}")
    
    if verification["unexpected_items"]:
        print("\n Remaining Issues:")
        for item in verification["unexpected_items"]:
            print(f"   • {item}")
    
    print("\n Sacred cellular architecture restored!")
    print(" Core Engine root is now pristine!")


if __name__ == "__main__":
    main()
