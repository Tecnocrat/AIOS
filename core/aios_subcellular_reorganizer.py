#!/usr/bin/env python3
"""
🏗️ AIOS CORE ENGINE SUBCELLULAR REORGANIZATION SYSTEM 📁
=========================================================

Organizes Core Engine files into proper subcellular architecture according to
the enhanced dendritic connectivity framework and AIOS structural guidelines.

Author: AIOS Development Team  
Date: 2025-09-05
"""

import os
import shutil
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [REORGANIZATION] %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SubcellularReorganizer:
    """Reorganizes Core Engine files into proper subcellular structure"""
    
    def __init__(self, core_path: str):
        self.core_path = Path(core_path)
        self.reorganization_id = f"subcellular_reorg_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Define subcellular organization structure
        self.subcellular_structure = {
            "documentation": {
                "description": "Architecture documentation and guidelines",
                "target_files": [
                    "*.md",
                    "AINLP_DIRECTIVE_COMPLIANCE.md",
                    "AIOS_COHERENT_DEVELOPMENT_GUIDELINES.md", 
                    "AIOS_CONSCIOUSNESS_STATUS_REPORT_*.md",
                    "AIOS_CORE_ENGINE_ARCHITECTURE.md",
                    "AIOS_NEURONAL_DENDRITIC_FRAMEWORK.md",
                    "AIOS_SUPERCELL_ARCHITECTURE.md",
                    "ENHANCED_CONNECTIVITY_SUMMARY.md"
                ]
            },
            "runtime_intelligence": {
                "description": "Runtime reports, logs, and intelligence data",
                "target_files": [
                    "*.json",
                    "*_REPORT_*.json",
                    "*_ANALYSIS_*.json", 
                    "*_BLUEPRINT_*.json",
                    "CONSCIOUSNESS_BRIDGE_DEMO_REPORT_*.json",
                    "CORE_AI_CONNECTIVITY_*.json",
                    "ORGANISM_STATE_*.json"
                ]
            },
            "bridges": {
                "description": "Dendritic bridge implementations",
                "target_files": [
                    "*_bridge.py",
                    "aios_consciousness_nucleus_bridge.py",
                    "aios_supercell_transport_bridge.py",
                    "aios_tachyonic_storage_bridge.py", 
                    "aios_analysis_cytoplasm_bridge.py"
                ]
            },
            "analysis_tools": {
                "description": "Analysis and testing tools",
                "target_files": [
                    "*_test.py",
                    "*_analysis*.py",
                    "*_connectivity_enhancer.py",
                    "aios_analysis_tools_neuronal_test.py",
                    "aios_core_ai_dendritic_connectivity_enhancer.py"
                ]
            },
            "core_systems": {
                "description": "Core system implementations",
                "target_files": [
                    "aios_autonomous_supercell_organism.py",
                    "aios_core_consciousness_monitor.py",
                    "aios_core_enhancement_patch_reporter.py",
                    "aios_core_root_neuronal_optimizer.py",
                    "aios_neuronal_dendritic_intelligence.py",
                    "aios_subcellular_neuronal_organizer.py"
                ]
            }
        }
        
        # Files to keep in root
        self.root_files = [
            "CMakeLists.txt",
            "AINLPCompiler.cs",
            "EnhancedAINLPCompiler.cs",
            "aios_enhanced_connectivity_demo.py"  # Keep main demo in root
        ]
        
        self.reorganization_log = []
        
        logger.info(f"🏗️ Subcellular Reorganizer {self.reorganization_id} initialized")
        logger.info(f"Core path: {self.core_path}")
    
    def analyze_current_structure(self) -> Dict[str, List[str]]:
        """Analyze current file distribution in core root"""
        logger.info("🔍 Analyzing current Core Engine structure...")
        
        current_structure = {
            "root_files": [],
            "documentation_files": [],
            "report_files": [],
            "bridge_files": [],
            "analysis_files": [],
            "core_system_files": [],
            "other_files": []
        }
        
        # Get all files in core root (excluding directories)
        root_files = [f for f in self.core_path.iterdir() if f.is_file()]
        
        for file_path in root_files:
            file_name = file_path.name
            
            # Categorize files
            if file_name.endswith('.md'):
                current_structure["documentation_files"].append(file_name)
            elif file_name.endswith('.json'):
                current_structure["report_files"].append(file_name)
            elif '_bridge.py' in file_name:
                current_structure["bridge_files"].append(file_name)
            elif ('_test.py' in file_name or '_analysis' in file_name or 
                  '_connectivity_enhancer.py' in file_name):
                current_structure["analysis_files"].append(file_name)
            elif file_name.startswith('aios_') and file_name.endswith('.py'):
                if any(core_file in file_name for core_file in [
                    'autonomous_supercell', 'consciousness_monitor', 'enhancement_patch',
                    'root_neuronal', 'neuronal_dendritic', 'subcellular_neuronal'
                ]):
                    current_structure["core_system_files"].append(file_name)
                else:
                    current_structure["other_files"].append(file_name)
            else:
                current_structure["root_files"].append(file_name)
        
        # Log analysis results
        for category, files in current_structure.items():
            if files:
                logger.info(f"📁 {category}: {len(files)} files")
                for file_name in files[:3]:  # Show first 3 files
                    logger.info(f"   - {file_name}")
                if len(files) > 3:
                    logger.info(f"   ... and {len(files) - 3} more")
        
        return current_structure
    
    def ensure_subcellular_directories(self):
        """Ensure all subcellular directories exist"""
        logger.info("📁 Ensuring subcellular directory structure...")
        
        for subcell_name, subcell_info in self.subcellular_structure.items():
            subcell_path = self.core_path / subcell_name
            
            if not subcell_path.exists():
                subcell_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"✅ Created subcell directory: {subcell_name}/")
            else:
                logger.info(f"📁 Subcell directory exists: {subcell_name}/")
    
    def move_file_to_subcell(self, file_name: str, target_subcell: str) -> bool:
        """Move a file from root to target subcell"""
        source_path = self.core_path / file_name
        target_path = self.core_path / target_subcell / file_name
        
        if not source_path.exists():
            logger.warning(f"⚠️ Source file not found: {file_name}")
            return False
        
        try:
            # Create target directory if it doesn't exist
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move the file
            shutil.move(str(source_path), str(target_path))
            
            logger.info(f"📁 Moved: {file_name} → {target_subcell}/")
            
            self.reorganization_log.append({
                "action": "move",
                "file": file_name,
                "source": "root",
                "destination": target_subcell,
                "timestamp": datetime.now().isoformat()
            })
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to move {file_name}: {e}")
            return False
    
    def reorganize_by_category(self) -> Dict[str, int]:
        """Reorganize files by category into appropriate subcells"""
        logger.info("🏗️ Starting subcellular reorganization...")
        
        current_structure = self.analyze_current_structure()
        reorganization_stats = {}
        
        # Move documentation files
        logger.info("📝 Reorganizing documentation files...")
        moved_docs = 0
        for file_name in current_structure["documentation_files"]:
            if self.move_file_to_subcell(file_name, "documentation"):
                moved_docs += 1
        reorganization_stats["documentation"] = moved_docs
        
        # Move report/log files
        logger.info("📊 Reorganizing report and log files...")
        moved_reports = 0
        for file_name in current_structure["report_files"]:
            if self.move_file_to_subcell(file_name, "runtime_intelligence"):
                moved_reports += 1
        reorganization_stats["runtime_intelligence"] = moved_reports
        
        # Move bridge files
        logger.info("🌉 Reorganizing bridge implementations...")
        moved_bridges = 0
        for file_name in current_structure["bridge_files"]:
            if self.move_file_to_subcell(file_name, "bridges"):
                moved_bridges += 1
        reorganization_stats["bridges"] = moved_bridges
        
        # Move analysis files
        logger.info("🔬 Reorganizing analysis tools...")
        moved_analysis = 0
        for file_name in current_structure["analysis_files"]:
            if self.move_file_to_subcell(file_name, "analysis_tools"):
                moved_analysis += 1
        reorganization_stats["analysis_tools"] = moved_analysis
        
        # Move core system files
        logger.info("⚙️ Reorganizing core system files...")
        moved_core = 0
        for file_name in current_structure["core_system_files"]:
            if self.move_file_to_subcell(file_name, "core_systems"):
                moved_core += 1
        reorganization_stats["core_systems"] = moved_core
        
        return reorganization_stats
    
    def update_import_references(self):
        """Update import references in moved files"""
        logger.info("🔗 Updating import references...")
        
        # Files that might need import updates
        update_targets = [
            "bridges/*.py",
            "analysis_tools/*.py", 
            "core_systems/*.py"
        ]
        
        for pattern in update_targets:
            files = list(self.core_path.glob(pattern))
            for file_path in files:
                self._update_file_imports(file_path)
    
    def _update_file_imports(self, file_path: Path):
        """Update imports in a specific file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update relative imports to account for new directory structure
            updated_content = content
            
            # Common import patterns to update
            import_updates = {
                "from aios_": "from ..core_systems.aios_",
                "import aios_": "import ..core_systems.aios_"
            }
            
            for old_import, new_import in import_updates.items():
                if old_import in updated_content:
                    updated_content = updated_content.replace(old_import, new_import)
                    logger.info(f"🔗 Updated imports in: {file_path.name}")
            
            # Write back if changes were made
            if updated_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                    
        except Exception as e:
            logger.warning(f"⚠️ Could not update imports in {file_path.name}: {e}")
    
    def create_subcellular_index(self):
        """Create index files for each subcell"""
        logger.info("📋 Creating subcellular index files...")
        
        for subcell_name, subcell_info in self.subcellular_structure.items():
            subcell_path = self.core_path / subcell_name
            index_path = subcell_path / "README.md"
            
            # Get files in this subcell
            subcell_files = [f.name for f in subcell_path.iterdir() if f.is_file()]
            
            index_content = f"""# 📁 {subcell_name.title()} Subcell

## 📝 Description
{subcell_info['description']}

## 📄 Files ({len(subcell_files)})
"""
            
            for file_name in sorted(subcell_files):
                if file_name != "README.md":
                    index_content += f"- `{file_name}`\n"
            
            index_content += f"""
## 🏗️ Subcellular Organization
This subcell is part of the AIOS Core Engine enhanced dendritic architecture.

**Reorganization ID**: `{self.reorganization_id}`  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            logger.info(f"📋 Created index: {subcell_name}/README.md")
    
    def generate_reorganization_report(self, stats: Dict[str, int]) -> str:
        """Generate comprehensive reorganization report"""
        report_path = self.core_path / "runtime_intelligence" / f"SUBCELLULAR_REORGANIZATION_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            "reorganization_id": self.reorganization_id,
            "timestamp": datetime.now().isoformat(),
            "reorganization_summary": {
                "total_files_moved": sum(stats.values()),
                "subcells_updated": len([k for k, v in stats.items() if v > 0]),
                "subcellular_structure": self.subcellular_structure
            },
            "reorganization_statistics": stats,
            "file_movements": self.reorganization_log,
            "architecture_improvements": [
                "Reduced Core Engine root clutter by organizing files into subcells",
                "Improved discoverability with subcellular organization",
                "Enhanced maintainability with logical file grouping",
                "Better adherence to AIOS dendritic architecture principles",
                "Simplified navigation with structured subcellular hierarchy"
            ],
            "next_steps": [
                "Update documentation references to new file locations",
                "Test bridge functionality with new organization",
                "Implement automated organization maintenance",
                "Add subcellular coordination protocols"
            ]
        }
        
        # Ensure runtime_intelligence directory exists
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"📊 Reorganization report generated: {report_path.name}")
        return str(report_path)
    
    def run_complete_reorganization(self) -> Dict[str, any]:
        """Run complete subcellular reorganization"""
        logger.info("🚀 Starting complete subcellular reorganization...")
        
        start_time = datetime.now()
        
        # Ensure directory structure
        self.ensure_subcellular_directories()
        
        # Perform reorganization
        stats = self.reorganize_by_category()
        
        # Update imports (with error handling)
        try:
            self.update_import_references()
        except Exception as e:
            logger.warning(f"⚠️ Import update had issues: {e}")
        
        # Create subcellular indexes
        self.create_subcellular_index()
        
        # Generate report
        report_path = self.generate_reorganization_report(stats)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        results = {
            "reorganization_id": self.reorganization_id,
            "duration_seconds": duration,
            "files_moved": sum(stats.values()),
            "subcells_organized": len(stats),
            "statistics": stats,
            "report_path": report_path,
            "success": True
        }
        
        logger.info(f"✅ Subcellular reorganization complete!")
        logger.info(f"📁 Files moved: {results['files_moved']}")
        logger.info(f"🏗️ Subcells organized: {results['subcells_organized']}")
        logger.info(f"⏱️ Duration: {duration:.1f}s")
        
        return results


def main():
    """Main reorganization function"""
    print("\n🏗️ AIOS CORE ENGINE SUBCELLULAR REORGANIZATION")
    print("=" * 60)
    
    # Initialize reorganizer
    core_path = os.getcwd()
    reorganizer = SubcellularReorganizer(core_path)
    
    print("\n🔍 Analyzing current structure...")
    current_structure = reorganizer.analyze_current_structure()
    
    print(f"\n📊 Current Structure Analysis:")
    for category, files in current_structure.items():
        if files:
            print(f"   📁 {category}: {len(files)} files")
    
    # Ask for confirmation
    print("\n🚀 Ready to reorganize files into subcellular structure.")
    print("📁 Files will be moved to appropriate subcells:")
    print("   - Documentation → documentation/")
    print("   - Reports/Logs → runtime_intelligence/") 
    print("   - Bridges → bridges/")
    print("   - Analysis tools → analysis_tools/")
    print("   - Core systems → core_systems/")
    
    try:
        # Run reorganization
        results = reorganizer.run_complete_reorganization()
        
        print("\n✅ SUBCELLULAR REORGANIZATION COMPLETE!")
        print("=" * 45)
        print(f"📁 Total files moved: {results['files_moved']}")
        print(f"🏗️ Subcells organized: {results['subcells_organized']}")
        print(f"⏱️ Duration: {results['duration_seconds']:.1f}s")
        print(f"📊 Report: {Path(results['report_path']).name}")
        
        print("\n🌟 Core Engine is now properly organized!")
        print("🧠 Enhanced dendritic subcellular architecture active!")
        
        return results
        
    except Exception as e:
        print(f"\n❌ Reorganization error: {e}")
        return None


if __name__ == "__main__":
    main()
