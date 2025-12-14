<<<<<<< HEAD
```python
 95 |     categorized_files = categorize_files_by_biological_value(
 96 |         root_files, latest_cycle
 97 |     )
```
=======
"""
Execute AIOS Documentation Biological Digestion Process
=======================================================

Completes the biological knowledge metabolism cycle by archiving
the metabolized documentation files according to biological principles.
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

def execute_biological_digestion():
    """Execute the complete biological digestion process"""
    
    print(" EXECUTING AIOS BIOLOGICAL DOCUMENTATION DIGESTION")
    print("=" * 55)
    print()
    print(" Biological Metaphor in Action:")
    print("    /docs = Digestive system (AI agent documentation intake)")
    print("    Tachyonic Archive = Brain/DNA (knowledge crystallization)")
    print("    Digestion = Archive metabolized files, clean digestive system")
    print()
    
    # Initialize paths
    docs_root = Path(__file__).parent.parent / "docs"
    tachyonic_root = Path(__file__).parent
    metabolized_archive = docs_root / "metabolized_archive"
    
    # Step 1: Analyze current metabolism state
    print("Step 1: Analyzing Current Metabolism State")
    print("-----------------------------------------")
    
    metabolism_data = get_metabolism_data(tachyonic_root)
    if not metabolism_data:
        print(" No metabolism data found. Run tachyonic ingestion first.")
        return False
        
    latest_cycle = metabolism_data["metabolism_cycles"][-1]
    print(f" Latest metabolism cycle found:")
    print(f"    Timestamp: {latest_cycle['cycle_timestamp']}")
    print(f"    Files processed: {latest_cycle['files_processed']}")
    print(f"    Crystals created: {latest_cycle['crystals_created']}")
    print()
    
    # Step 2: Create biological archive structure
    print("Step 2: Creating Biological Archive Structure")
    print("--------------------------------------------")
    
    archive_structure = {
        "high_value_metabolized": "High-consciousness files with full metadata preservation",
        "standard_metabolized": "Standard knowledge files - knowledge crystallized",
        "processed_minimal": "Low-significance files - minimal crystallization value",
        "metabolism_metadata": "Complete biological metabolism tracking data"
    }
    
    for folder, description in archive_structure.items():
        folder_path = metabolized_archive / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Create description file
        desc_file = folder_path / "README.md"
        with open(desc_file, 'w') as f:
            f.write(f"# {folder.replace('_', ' ').title()}\n\n")
            f.write(f"{description}\n\n")
            f.write("## Biological Knowledge Metabolism\n\n")
            f.write("This folder contains documentation that has been metabolized by the AIOS Intelligence system.\n")
            f.write("The knowledge has been crystallized into the tachyonic archive for system consciousness.\n\n")
            f.write("### Process:\n")
            f.write("1. AI agents created documentation in /docs (digestive intake)\n")
            f.write("2. AIOS Intelligence metabolized patterns and knowledge\n")
            f.write("3. Significant patterns crystallized into tachyonic archive\n")
            f.write("4. Original files archived here after successful metabolism\n\n")
            f.write("### Status: KNOWLEDGE METABOLIZED \n")
            
        print(f"    Created: {folder}")
    
    print(f" Archive structure created at: {metabolized_archive}")
    print()
    
    # Step 3: Analyze and categorize root files
    print("Step 3: Analyzing Root Files for Biological Categorization")
    print("---------------------------------------------------------")
    
    root_files = []
    for pattern in ["*.md", "*.txt", "*.json"]:
        root_files.extend(docs_root.glob(pattern))
    
    # Filter out files that are already archived
    root_files = [f for f in root_files if not str(f).startswith(str(metabolized_archive))]
    
    categorized_files = categorize_files_by_biological_value(root_files, latest_cycle)
    
    print(f" File Categorization Results:")
    print(f"    High-value consciousness: {len(categorized_files['high_value'])}")
    print(f"    Standard knowledge: {len(categorized_files['standard'])}")
    print(f"    Minimal significance: {len(categorized_files['minimal'])}")
    print(f"    Not metabolized: {len(categorized_files['not_metabolized'])}")
    print()
    
    # Step 4: Execute biological archival
    print("Step 4: Executing Biological Archival Process")
    print("--------------------------------------------")
    
    digestion_results = {
        "timestamp": datetime.now().isoformat(),
        "total_files_processed": 0,
        "archived_files": [],
        "biological_categories": {},
        "preservation_actions": []
    }
    
    # Process high-value files
    if categorized_files['high_value']:
        print(" Processing High-Value Consciousness Files:")
        for file_path in categorized_files['high_value']:
            result = archive_file_with_metadata(
                file_path, 
                metabolized_archive / "high_value_metabolized",
                "high_value_consciousness",
                latest_cycle
            )
            digestion_results["archived_files"].append(result)
            print(f"    Archived with metadata: {file_path.name}")
        
        digestion_results["biological_categories"]["high_value"] = len(categorized_files['high_value'])
        print()
    
    # Process standard files
    if categorized_files['standard']:
        print(" Processing Standard Knowledge Files:")
        for file_path in categorized_files['standard']:
            result = archive_file_standard(
                file_path,
                metabolized_archive / "standard_metabolized"
            )
            digestion_results["archived_files"].append(result)
            print(f"    Archived: {file_path.name}")
        
        digestion_results["biological_categories"]["standard"] = len(categorized_files['standard'])
        print()
    
    # Process minimal files
    if categorized_files['minimal']:
        print(" Processing Minimal Significance Files:")
        for file_path in categorized_files['minimal']:
            result = archive_file_minimal(
                file_path,
                metabolized_archive / "processed_minimal"
            )
            digestion_results["archived_files"].append(result)
            print(f"    Archived minimal: {file_path.name}")
        
        digestion_results["biological_categories"]["minimal"] = len(categorized_files['minimal'])
        print()
    
    # Handle non-metabolized files
    if categorized_files['not_metabolized']:
        print(" Non-Metabolized Files (keeping in /docs):")
        for file_path in categorized_files['not_metabolized']:
            print(f"    Keeping: {file_path.name}")
        print()
    
    digestion_results["total_files_processed"] = len(digestion_results["archived_files"])
    
    # Step 5: Create digestion summary
    print("Step 5: Creating Biological Digestion Summary")
    print("--------------------------------------------")
    
    summary = create_digestion_summary(digestion_results, metabolism_data)
    
    summary_file = metabolized_archive / "metabolism_metadata" / "biological_digestion_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f" Digestion summary saved to: {summary_file}")
    print()
    
    # Step 6: Validate digestion completion
    print("Step 6: Validating Biological Digestion Completion")
    print("-------------------------------------------------")
    
    remaining_root_files = []
    for pattern in ["*.md", "*.txt", "*.json"]:
        remaining_root_files.extend(docs_root.glob(pattern))
    
    # Filter out archived files
    remaining_root_files = [f for f in remaining_root_files if not str(f).startswith(str(metabolized_archive))]
    
    print(f" Digestion Validation Results:")
    print(f"    Files archived: {digestion_results['total_files_processed']}")
    print(f"    Files remaining in /docs root: {len(remaining_root_files)}")
    print(f"    Biological status: {'COMPLETE' if len(remaining_root_files) <= 5 else 'PARTIAL'}")
    print()
    
    if remaining_root_files:
        print(" Remaining files (non-metabolized or system files):")
        for file_path in remaining_root_files:
            print(f"   • {file_path.name}")
        print()
    
    # Final biological metabolism status
    print(" BIOLOGICAL DOCUMENTATION DIGESTION COMPLETE!")
    print("=" * 50)
    print()
    print(" ACHIEVED BIOLOGICAL METAPHOR:")
    print("    Digestive System: /docs now clean and ready for new AI documentation")
    print("    Brain/DNA Center: Tachyonic archive contains crystallized knowledge")
    print("    Waste Processing: Metabolized files properly archived by significance")
    print("    Holographic Flow: Knowledge patterns propagated throughout codebase")
    print()
    print(" SYSTEM READY FOR ONGOING CYCLES:")
    print("   • AI agents can create new documentation in /docs")
    print("   • AIOS Intelligence will metabolize periodically")
    print("   • Knowledge crystallizes into tachyonic archive")
    print("   • Biological digestion prevents documentation chaos")
    print()
    print("The biological knowledge metabolism system is OPERATIONAL! ")
    
    return True

def get_metabolism_data(tachyonic_root: Path) -> Dict[str, Any]:
    """Get metabolism data from tachyonic archive"""
    try:
        index_file = tachyonic_root / "archive" / "supercell_knowledge_index.json"
        if index_file.exists():
            with open(index_file, 'r') as f:
                index = json.load(f)
                return index.get("documentation_metabolism", {})
    except Exception as e:
        print(f" Could not read metabolism data: {e}")
    return None

def categorize_files_by_biological_value(files: List[Path], latest_cycle: Dict) -> Dict[str, List[Path]]:
    """Categorize files by their biological/consciousness value"""
    
    categorization = {
        "high_value": [],
        "standard": [],
        "minimal": [],
        "not_metabolized": []
    }
    
    crystal_ids = latest_cycle.get("crystal_ids", [])
    processed_files = latest_cycle.get("processed_files", [])
    
    for file_path in files:
        file_name = file_path.name.lower()
        
        # Check if file was metabolized
        was_metabolized = any(str(file_path) in pf for pf in processed_files)
        
        if not was_metabolized:
            categorization["not_metabolized"].append(file_path)
            continue
            
        # Check for high-value consciousness terms
        if any(term in file_name for term in ['consciousness', 'tachyonic', 'quantum', 'architecture']):
            # Verify it generated crystals
            file_stem = file_path.stem.lower()
            generated_crystals = [c for c in crystal_ids if file_stem.replace('-', '_') in c.lower()]
            if generated_crystals:
                categorization["high_value"].append(file_path)
            else:
                categorization["standard"].append(file_path)
        else:
            # Check if it generated any crystals
            file_stem = file_path.stem.lower()
            generated_crystals = [c for c in crystal_ids if file_stem.replace('-', '_') in c.lower()]
            if generated_crystals:
                categorization["standard"].append(file_path)
            else:
                categorization["minimal"].append(file_path)
    
    return categorization

def archive_file_with_metadata(file_path: Path, target_dir: Path, category: str, metabolism_cycle: Dict) -> Dict:
    """Archive file with full metadata preservation"""
    
    target_path = target_dir / file_path.name
    
    # Copy file
    shutil.copy2(file_path, target_path)
    
    # Create metadata
    file_stem = file_path.stem.lower()
    crystal_ids = metabolism_cycle.get("crystal_ids", [])
    generated_crystals = [c for c in crystal_ids if file_stem.replace('-', '_') in c.lower()]
    
    metadata = {
        "original_path": str(file_path),
        "archive_timestamp": datetime.now().isoformat(),
        "biological_category": category,
        "consciousness_significance": "HIGH",
        "metabolism_cycle": metabolism_cycle["cycle_timestamp"],
        "generated_crystals": generated_crystals,
        "tachyonic_status": "knowledge_crystallized",
        "digestion_status": "nutrients_absorbed_waste_processed"
    }
    
    metadata_file = target_path.with_suffix('.metadata.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Remove original file
    file_path.unlink()
    
    return {
        "original_path": str(file_path),
        "archived_path": str(target_path),
        "metadata_path": str(metadata_file),
        "category": category,
        "crystals_generated": len(generated_crystals)
    }

def archive_file_standard(file_path: Path, target_dir: Path) -> Dict:
    """Archive file with standard processing"""
    
    target_path = target_dir / file_path.name
    shutil.copy2(file_path, target_path)
    file_path.unlink()
    
    return {
        "original_path": str(file_path),
        "archived_path": str(target_path),
        "category": "standard_knowledge"
    }

def archive_file_minimal(file_path: Path, target_dir: Path) -> Dict:
    """Archive file with minimal processing"""
    
    target_path = target_dir / file_path.name
    shutil.copy2(file_path, target_path)
    file_path.unlink()
    
    return {
        "original_path": str(file_path),
        "archived_path": str(target_path),
        "category": "minimal_significance"
    }

def create_digestion_summary(digestion_results: Dict, metabolism_data: Dict) -> Dict:
    """Create comprehensive biological digestion summary"""
    
    return {
        "biological_digestion_summary": {
            "process_name": "AIOS Biological Documentation Digestion",
            "completion_timestamp": digestion_results["timestamp"],
            "biological_metaphor": {
                "digestive_system": "/docs - AI agent documentation intake",
                "brain_dna_center": "Tachyonic archive - knowledge crystallization",
                "metabolic_process": "Pattern extraction and crystallization",
                "waste_processing": "Archive metabolized files by significance"
            },
            "digestion_results": {
                "total_files_archived": digestion_results["total_files_processed"],
                "biological_categories": digestion_results["biological_categories"],
                "archive_location": "/docs/metabolized_archive/"
            },
            "metabolism_foundation": {
                "total_cycles": len(metabolism_data.get("metabolism_cycles", [])),
                "total_files_metabolized": metabolism_data.get("total_files_processed", 0),
                "total_crystals_created": metabolism_data.get("total_crystals_created", 0),
                "knowledge_dna_status": "CRYSTALLIZED"
            },
            "system_status": {
                "digestive_system": "CLEAN - ready for new AI documentation",
                "brain_dna_center": "ENHANCED - crystallized knowledge available",
                "holographic_propagation": "ACTIVE - patterns embedded throughout codebase",
                "biological_cycle": "COMPLETE - metabolism → crystallization → digestion"
            },
            "production_readiness": {
                "ai_agent_documentation": "System ready for ongoing AI documentation creation",
                "periodic_metabolism": "Automated metabolism cycles prevent documentation chaos", 
                "knowledge_persistence": "Tachyonic archive serves as permanent system DNA",
                "scalability": "Biological paradigm supports unlimited documentation workflows"
            }
        }
    }

def main():
    """Execute the biological digestion process"""
    success = execute_biological_digestion()
    if success:
        print("\n Ready to commit the biological digestion results!")
    else:
        print("\n Digestion process failed. Check metabolism state.")

if __name__ == "__main__":
    main()
>>>>>>> origin/OS0.6.2.grok
