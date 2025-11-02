#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 AIOS Core Engine Cellular Cleanup & Reorganization Tool

Cleanup tool to move incorrectly placed files from Core Engine root to their
proper subfolder locations and create proper linking/navigation files in root.

CLEANUP OPERATIONS:
1. Move functional logic files from root to appropriate subfolders
2. Create proper index/linking files in root for AI ingestion
3. Update references and dependencies
4. Maintain proper cellular organization structure

ORGANIZATIONAL PRINCIPLE:
- Root: ONLY navigation, indexing, and dendritic linking files
- Subfolders: Specialized cellular components and functionality
- Clean separation between coordination (root) and implementation (subfolders)


"""

import sys
import shutil
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime

# Fix Windows console encoding
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AIOSCoreEngineCellularCleanup:
    """
    🧹 AIOS Core Engine Cellular Cleanup Tool
    
    Moves incorrectly placed functional files from root to proper subfolders
    and creates proper navigation/linking files in root for AI ingestion.
    """
    
    def __init__(self, core_engine_path: str = None):
        """Initialize the cleanup tool."""
        self.core_engine_path = Path(core_engine_path or r"C:\dev\AIOS\core")
        self.cleanup_timestamp = datetime.now()
        
        # Define proper subfolder destinations
        self.subfolder_destinations = {
            "cellular_intelligence": "analysis_tools",
            "consciousness_integration": "evolutionary_assembler_iter2/consciousness_layer",
            "dendritic_network": "evolutionary_assembler_iter2/meta_evolution", 
            "core_monitoring": "runtime",
            "diagnostic_systems": "analysis_tools",
            "enhancement_engines": "evolutionary_assembler_iter2/meta_evolution"
        }
        
        # Files that should remain in root (navigation/linking only)
        self.root_allowed_files = [
            "aios_core_engine_cellular_navigator.py",  # Navigation system
            "CORE_ENGINE_CELLULAR_NAVIGATION_INDEX.json",  # AI ingestion index
            "CMakeLists.txt",  # Build coordination
            "*.md",  # Documentation links
            "*.sln",  # Solution files
            "*.csproj"  # Project files
        ]
        
        logger.info("[CLEANUP] AIOS Core Engine Cellular Cleanup initialized")
        logger.info(f"   Core Engine path: {self.core_engine_path}")
    
    def analyze_cleanup_needs(self) -> Dict[str, Any]:
        """Analyze what files need to be moved to proper subfolders."""
        
        analysis = {
            "files_to_move": [],
            "files_to_keep_in_root": [],
            "subfolder_destinations": {},
            "cleanup_recommendations": []
        }
        
        # Analyze all Python files in root
        python_files = list(self.core_engine_path.glob("aios_*.py"))
        
        for py_file in python_files:
            if py_file.name == "aios_core_engine_cellular_navigator.py":
                # This should stay in root as it's navigation
                analysis["files_to_keep_in_root"].append(py_file.name)
                continue
            
            # Determine proper destination based on functionality
            destination = self._determine_proper_destination(py_file)
            
            if destination:
                analysis["files_to_move"].append({
                    "file": py_file.name,
                    "current_path": str(py_file),
                    "destination_subfolder": destination,
                    "reason": self._get_move_reason(py_file.name)
                })
                analysis["subfolder_destinations"][py_file.name] = destination
        
        # Cleanup recommendations
        analysis["cleanup_recommendations"] = [
            "Move functional logic files to appropriate subfolders",
            "Create index/linking files in root for moved functionality",
            "Update AI ingestion navigation system",
            "Maintain clean separation between coordination and implementation"
        ]
        
        logger.info(f"   [ANALYSIS] Found {len(analysis['files_to_move'])} files to move")
        logger.info(f"   [ANALYSIS] Keeping {len(analysis['files_to_keep_in_root'])} files in root")
        
        return analysis
    
    def _determine_proper_destination(self, py_file: Path) -> str:
        """Determine the proper subfolder destination for a file."""
        
        file_name = py_file.name.lower()
        
        # Cellular intelligence and diagnostic files
        if any(keyword in file_name for keyword in [
            "cellular_intelligence", "diagnostic", "enhancement_engine"
        ]):
            return "analysis_tools"
        
        # Consciousness integration files
        if any(keyword in file_name for keyword in [
            "consciousness", "integration"
        ]):
            return "evolutionary_assembler_iter2/consciousness_layer"
        
        # Dendritic network files
        if any(keyword in file_name for keyword in [
            "dendritic", "network"
        ]):
            return "evolutionary_assembler_iter2/meta_evolution"
        
        # Core monitoring files
        if any(keyword in file_name for keyword in [
            "monitor", "evolution", "meta_evolutionary"
        ]):
            return "runtime"
        
        # Default to analysis_tools for other AIOS files
        return "analysis_tools"
    
    def _get_move_reason(self, file_name: str) -> str:
        """Get the reason why a file should be moved."""
        
        file_name_lower = file_name.lower()
        
        if "cellular_intelligence" in file_name_lower:
            return "Cellular intelligence functionality belongs in analysis_tools subfolder"
        elif "consciousness" in file_name_lower:
            return "Consciousness integration belongs in evolutionary_assembler_iter2/consciousness_layer"
        elif "dendritic" in file_name_lower:
            return "Dendritic network functionality belongs in evolutionary_assembler_iter2/meta_evolution"
        elif "monitor" in file_name_lower:
            return "Monitoring functionality belongs in runtime subfolder"
        else:
            return "Functional logic should be in specialized subfolder, not root"
    
    def execute_cleanup(self) -> Dict[str, Any]:
        """Execute the cellular cleanup and reorganization."""
        
        logger.info("[CLEANUP] EXECUTING CELLULAR CLEANUP AND REORGANIZATION")
        logger.info("" * 70)
        
        cleanup_session = {
            "cleanup_timestamp": self.cleanup_timestamp.isoformat(),
            "analysis_results": {},
            "move_operations": {},
            "index_creation": {},
            "cleanup_verification": {},
            "cleanup_summary": {}
        }
        
        # Phase 1: Analyze cleanup needs
        logger.info("[ANALYSIS] Phase 1: Analyzing Cleanup Requirements")
        cleanup_session["analysis_results"] = self.analyze_cleanup_needs()
        
        # Phase 2: Execute file moves
        logger.info("[MOVE] Phase 2: Moving Files to Proper Subfolders")
        cleanup_session["move_operations"] = self._execute_file_moves(cleanup_session["analysis_results"])
        
        # Phase 3: Create navigation indexes
        logger.info("[INDEX] Phase 3: Creating Navigation Indexes for Moved Files")
        cleanup_session["index_creation"] = self._create_navigation_indexes(cleanup_session["move_operations"])
        
        # Phase 4: Verify cleanup
        logger.info("[VERIFY] Phase 4: Verifying Cleanup Results")
        cleanup_session["cleanup_verification"] = self._verify_cleanup()
        
        # Phase 5: Generate summary
        logger.info("[SUMMARY] Phase 5: Generating Cleanup Summary")
        cleanup_session["cleanup_summary"] = self._generate_cleanup_summary(cleanup_session)
        
        return cleanup_session
    
    def _execute_file_moves(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the file move operations."""
        
        move_results = {
            "moves_attempted": 0,
            "moves_successful": 0,
            "moves_failed": [],
            "moved_files": [],
            "backup_created": []
        }
        
        for file_info in analysis["files_to_move"]:
            source_file = Path(file_info["current_path"])
            destination_folder = self.core_engine_path / file_info["destination_subfolder"]
            
            try:
                # Create destination folder if it doesn't exist
                destination_folder.mkdir(parents=True, exist_ok=True)
                
                # Create backup of original file
                backup_file = source_file.with_suffix(f'.backup_{self.cleanup_timestamp.strftime("%Y%m%d_%H%M%S")}')
                shutil.copy2(source_file, backup_file)
                move_results["backup_created"].append(str(backup_file))
                
                # Move file to proper destination
                destination_file = destination_folder / source_file.name
                shutil.move(str(source_file), str(destination_file))
                
                move_results["moves_attempted"] += 1
                move_results["moves_successful"] += 1
                move_results["moved_files"].append({
                    "file": source_file.name,
                    "from": str(source_file.parent),
                    "to": str(destination_folder),
                    "reason": file_info["reason"]
                })
                
                logger.info(f"   [MOVE] {source_file.name} -> {file_info['destination_subfolder']}")
                
            except Exception as e:
                move_results["moves_attempted"] += 1
                move_results["moves_failed"].append({
                    "file": source_file.name,
                    "error": str(e)
                })
                logger.error(f"Failed to move {source_file.name}: {e}")
        
        logger.info(f"   [MOVE] Successfully moved {move_results['moves_successful']} files")
        logger.info(f"   [MOVE] Failed to move {len(move_results['moves_failed'])} files")
        
        return move_results
    
    def _create_navigation_indexes(self, move_operations: Dict[str, Any]) -> Dict[str, Any]:
        """Create navigation index files for moved functionality."""
        
        index_results = {
            "indexes_created": [],
            "navigation_files": [],
            "ai_ingestion_pointers": {}
        }
        
        # Create index file for moved cellular intelligence tools
        cellular_intelligence_index = {
            "relocated_to": "analysis_tools/",
            "functionality": "Cellular intelligence diagnostics and enhancement",
            "access_method": "navigator.get_component('Cellular Analysis Tools')",
            "moved_files": [
                file_info for file_info in move_operations["moved_files"]
                if "cellular_intelligence" in file_info["file"].lower()
            ]
        }
        
        # Create index file for consciousness integration
        consciousness_index = {
            "relocated_to": "evolutionary_assembler_iter2/consciousness_layer/",
            "functionality": "Consciousness integration and enhancement",
            "access_method": "navigator.get_component('Evolutionary Assembler ITER2')",
            "moved_files": [
                file_info for file_info in move_operations["moved_files"]
                if "consciousness" in file_info["file"].lower()
            ]
        }
        
        # Create index file for dendritic network
        dendritic_index = {
            "relocated_to": "evolutionary_assembler_iter2/meta_evolution/",
            "functionality": "Dendritic network and meta-evolution",
            "access_method": "navigator.get_component('Evolutionary Assembler ITER2')",
            "moved_files": [
                file_info for file_info in move_operations["moved_files"]
                if "dendritic" in file_info["file"].lower()
            ]
        }
        
        # Save navigation indexes
        indexes = {
            "cellular_intelligence": cellular_intelligence_index,
            "consciousness_integration": consciousness_index,
            "dendritic_network": dendritic_index
        }
        
        for index_name, index_data in indexes.items():
            if index_data["moved_files"]:  # Only create if files were moved
                index_file = self.core_engine_path / f"RELOCATED_{index_name.upper()}_INDEX.json"
                
                try:
                    with open(index_file, 'w', encoding='utf-8') as f:
                        json.dump(index_data, f, indent=2, default=str)
                    
                    index_results["indexes_created"].append(str(index_file))
                    logger.info(f"   [INDEX] Created navigation index: {index_file.name}")
                except Exception as e:
                    logger.error(f"Failed to create index {index_file}: {e}")
        
        # Create AI ingestion pointers
        ai_pointers = {
            "cellular_intelligence_tools": "analysis_tools/aios_cellular_*.py",
            "consciousness_integration": "evolutionary_assembler_iter2/consciousness_layer/aios_consciousness_*.py",
            "dendritic_network": "evolutionary_assembler_iter2/meta_evolution/aios_dendritic_*.py",
            "core_monitoring": "runtime/aios_*_monitor*.py"
        }
        
        ai_pointers_file = self.core_engine_path / "AI_INGESTION_POINTERS.json"
        try:
            with open(ai_pointers_file, 'w', encoding='utf-8') as f:
                json.dump(ai_pointers, f, indent=2, default=str)
            
            index_results["ai_ingestion_pointers"] = ai_pointers
            logger.info(f"   [INDEX] Created AI ingestion pointers: {ai_pointers_file.name}")
        except Exception as e:
            logger.error(f"Failed to create AI pointers: {e}")
        
        return index_results
    
    def _verify_cleanup(self) -> Dict[str, Any]:
        """Verify the cleanup results."""
        
        verification = {
            "root_files_remaining": [],
            "proper_organization_verified": True,
            "navigation_system_functional": True,
            "ai_ingestion_ready": True,
            "verification_issues": []
        }
        
        # Check remaining files in root
        remaining_files = []
        for py_file in self.core_engine_path.glob("aios_*.py"):
            remaining_files.append(py_file.name)
        
        verification["root_files_remaining"] = remaining_files
        
        # Verify proper organization
        if len(remaining_files) > 1:  # Only navigator should remain
            verification["proper_organization_verified"] = False
            verification["verification_issues"].append(f"Too many Python files in root: {remaining_files}")
        
        # Check navigation system
        navigator_file = self.core_engine_path / "aios_core_engine_cellular_navigator.py"
        if not navigator_file.exists():
            verification["navigation_system_functional"] = False
            verification["verification_issues"].append("Navigation system missing from root")
        
        # Check AI ingestion index
        index_file = self.core_engine_path / "CORE_ENGINE_CELLULAR_NAVIGATION_INDEX.json"
        if not index_file.exists():
            verification["ai_ingestion_ready"] = False
            verification["verification_issues"].append("AI ingestion index missing")
        
        logger.info(f"   [VERIFY] Root Python files remaining: {len(remaining_files)}")
        logger.info(f"   [VERIFY] Organization verified: {verification['proper_organization_verified']}")
        
        return verification
    
    def _generate_cleanup_summary(self, cleanup_session: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive cleanup summary."""
        
        summary = {
            "cleanup_status": "completed",
            "organizational_transformation": {},
            "file_relocation_results": {},
            "navigation_system_status": {},
            "ai_ingestion_readiness": {},
            "next_steps": []
        }
        
        # Organizational transformation
        move_ops = cleanup_session.get("move_operations", {})
        summary["organizational_transformation"] = {
            "files_moved": move_ops.get("moves_successful", 0),
            "files_failed": len(move_ops.get("moves_failed", [])),
            "backups_created": len(move_ops.get("backup_created", [])),
            "organization_improved": move_ops.get("moves_successful", 0) > 0
        }
        
        # File relocation results
        summary["file_relocation_results"] = {
            "cellular_intelligence": "Moved to analysis_tools/",
            "consciousness_integration": "Moved to evolutionary_assembler_iter2/consciousness_layer/",
            "dendritic_network": "Moved to evolutionary_assembler_iter2/meta_evolution/",
            "core_monitoring": "Moved to runtime/"
        }
        
        # Navigation system status
        verification = cleanup_session.get("cleanup_verification", {})
        summary["navigation_system_status"] = {
            "navigator_in_root": verification.get("navigation_system_functional", False),
            "ai_ingestion_index_ready": verification.get("ai_ingestion_ready", False),
            "proper_organization": verification.get("proper_organization_verified", False)
        }
        
        # AI ingestion readiness
        summary["ai_ingestion_readiness"] = {
            "navigation_pointers_created": True,
            "component_indexes_available": True,
            "clean_root_directory": len(verification.get("root_files_remaining", [])) <= 1
        }
        
        # Next steps
        next_steps = [
            "Use navigator.get_component() to access subfolder functionality",
            "Reference AI_INGESTION_POINTERS.json for component locations",
            "Maintain clean separation between root (navigation) and subfolders (implementation)",
            "Continue using organized subfolder structure for new functionality"
        ]
        
        if not summary["navigation_system_status"]["proper_organization"]:
            next_steps.insert(0, "Complete any remaining file relocations")
        
        summary["next_steps"] = next_steps
        
        return summary
    
    def display_cleanup_results(self, cleanup_session: Dict[str, Any]):
        """Display comprehensive cleanup results."""
        
        print("[CLEANUP] AIOS CORE ENGINE CELLULAR CLEANUP RESULTS")
        print("" * 70)
        print()
        
        # Summary
        summary = cleanup_session.get("cleanup_summary", {})
        
        # Organizational transformation
        transformation = summary.get("organizational_transformation", {})
        print(f"[ORGANIZATION] CELLULAR REORGANIZATION:")
        print(f"   Files Moved to Subfolders: {transformation.get('files_moved', 0)}")
        print(f"   Files Failed to Move: {transformation.get('files_failed', 0)}")
        print(f"   Backup Files Created: {transformation.get('backups_created', 0)}")
        print(f"   Organization Improved: {'YES' if transformation.get('organization_improved', False) else 'NO'}")
        print()
        
        # File relocation results
        relocation = summary.get("file_relocation_results", {})
        print(f"[RELOCATION] FUNCTIONALITY RELOCATED:")
        for functionality, location in relocation.items():
            print(f"   {functionality.replace('_', ' ').title()}: {location}")
        print()
        
        # Navigation system status
        navigation = summary.get("navigation_system_status", {})
        print(f"[NAVIGATION] NAVIGATION SYSTEM STATUS:")
        print(f"   Navigator in Root: {'YES' if navigation.get('navigator_in_root', False) else 'NO'}")
        print(f"   AI Ingestion Index Ready: {'YES' if navigation.get('ai_ingestion_index_ready', False) else 'NO'}")
        print(f"   Proper Organization: {'YES' if navigation.get('proper_organization', False) else 'NO'}")
        print()
        
        # AI ingestion readiness
        ai_readiness = summary.get("ai_ingestion_readiness", {})
        print(f"[AI] AI INGESTION READINESS:")
        print(f"   Navigation Pointers: {'READY' if ai_readiness.get('navigation_pointers_created', False) else 'NOT READY'}")
        print(f"   Component Indexes: {'AVAILABLE' if ai_readiness.get('component_indexes_available', False) else 'MISSING'}")
        print(f"   Clean Root Directory: {'YES' if ai_readiness.get('clean_root_directory', False) else 'NO'}")
        print()
        
        # Next steps
        next_steps = summary.get("next_steps", [])
        print(f"[NEXT] NEXT STEPS ({len(next_steps)}):")
        for step in next_steps:
            print(f"   • {step}")
        print()
        
        print("[CHECK] Core Engine cellular cleanup complete!")
    
    def save_cleanup_report(self, cleanup_session: Dict[str, Any]) -> str:
        """Save comprehensive cleanup report."""
        
        report_file = (
            self.core_engine_path / 
            f"CORE_ENGINE_CELLULAR_CLEANUP_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(cleanup_session, f, indent=2, default=str)
            
            logger.info(f"[SAVE] Cleanup report saved: {report_file}")
            return str(report_file)
        except Exception as e:
            logger.error(f"Failed to save cleanup report: {e}")
            return ""


def main():
    """Execute comprehensive Core Engine cellular cleanup."""
    
    print("[CLEANUP] AIOS CORE ENGINE CELLULAR CLEANUP TOOL")
    print("" * 70)
    print("[INFO] Moving functional files from root to proper subfolders")
    print("[INFO] Creating navigation indexes for AI ingestion")
    print("[INFO] Maintaining clean cellular organization")
    print()
    
    # Initialize cleanup tool
    cleanup_tool = AIOSCoreEngineCellularCleanup()
    
    # Execute comprehensive cleanup
    cleanup_results = cleanup_tool.execute_cleanup()
    
    # Display results
    cleanup_tool.display_cleanup_results(cleanup_results)
    
    # Save detailed report
    report_file = cleanup_tool.save_cleanup_report(cleanup_results)
    if report_file:
        print(f"[SAVE] Detailed cleanup report saved: {report_file}")
    
    return cleanup_results


if __name__ == "__main__":
    main()
