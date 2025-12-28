"""
Simple Biological Digestion Executor
====================================

Execute the biological digestion process with proper encoding handling.
"""

import shutil
import json
from pathlib import Path
from datetime import datetime

def execute_simple_digestion():
    """Execute biological digestion with robust encoding"""
    
    print("EXECUTING AIOS BIOLOGICAL DOCUMENTATION DIGESTION")
    print("=" * 50)
    print()
    
    # Initialize paths
    docs_root = Path(__file__).parent.parent / "docs"
    metabolized_archive = docs_root / "metabolized_archive"
    
    # Create archive structure
    print("Step 1: Creating Archive Structure")
    print("-" * 35)
    
    archive_folders = [
        "high_value_metabolized",
        "standard_metabolized", 
        "processed_minimal",
        "metabolism_metadata"
    ]
    
    for folder in archive_folders:
        folder_path = metabolized_archive / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Create simple README
        readme_file = folder_path / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(f"# {folder.replace('_', ' ').title()}\n\n")
            f.write("Files metabolized by AIOS Intelligence system.\n")
            f.write("Knowledge crystallized into tachyonic archive.\n")
            
        print(f"   Created: {folder}")
    
    print(f"Archive structure created at: {metabolized_archive}")
    print()
    
    # Get root files to process
    print("Step 2: Processing Root Documentation Files")
    print("-" * 40)
    
    root_files = []
    for pattern in ["*.md", "*.txt"]:
        root_files.extend(docs_root.glob(pattern))
    
    # Filter out already archived files
    root_files = [f for f in root_files if not str(f).startswith(str(metabolized_archive))]
    
    print(f"Found {len(root_files)} root files to process")
    
    # Categorize and archive files
    digestion_results = {
        "timestamp": datetime.now().isoformat(),
        "archived_files": [],
        "high_value_count": 0,
        "standard_count": 0,
        "minimal_count": 0
    }
    
    for file_path in root_files:
        file_name = file_path.name.lower()
        
        # Determine category based on filename content
        if any(term in file_name for term in ['consciousness', 'tachyonic', 'quantum', 'architecture']):
            # High value - preserve with metadata
            target_dir = metabolized_archive / "high_value_metabolized"
            category = "high_value"
            digestion_results["high_value_count"] += 1
        elif any(term in file_name for term in ['integration', 'ui', 'system', 'intelligence']):
            # Standard value
            target_dir = metabolized_archive / "standard_metabolized"
            category = "standard"
            digestion_results["standard_count"] += 1
        else:
            # Minimal value
            target_dir = metabolized_archive / "processed_minimal"
            category = "minimal"
            digestion_results["minimal_count"] += 1
        
        # Archive the file
        target_path = target_dir / file_path.name
        try:
            shutil.copy2(file_path, target_path)
            
            # Create simple metadata for high-value files
            if category == "high_value":
                metadata = {
                    "original_path": str(file_path),
                    "archive_timestamp": datetime.now().isoformat(),
                    "category": "high_value_consciousness",
                    "status": "knowledge_crystallized"
                }
                metadata_file = target_path.with_suffix('.metadata.json')
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2)
            
            # Remove original file
            file_path.unlink()
            
            digestion_results["archived_files"].append({
                "file": file_path.name,
                "category": category,
                "archived_to": str(target_path)
            })
            
            print(f"   Archived ({category}): {file_path.name}")
            
        except Exception as e:
            print(f"   ERROR archiving {file_path.name}: {e}")
    
    # Create digestion summary
    print()
    print("Step 3: Creating Digestion Summary")
    print("-" * 35)
    
    summary = {
        "biological_digestion_complete": {
            "timestamp": digestion_results["timestamp"],
            "total_files_archived": len(digestion_results["archived_files"]),
            "categories": {
                "high_value_consciousness": digestion_results["high_value_count"],
                "standard_knowledge": digestion_results["standard_count"],
                "minimal_significance": digestion_results["minimal_count"]
            },
            "biological_status": "nutrients_absorbed_waste_processed",
            "system_ready": "digestive_system_clean_for_new_documentation"
        }
    }
    
    summary_file = metabolized_archive / "metabolism_metadata" / "digestion_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Digestion summary saved to: {summary_file}")
    print()
    
    # Final status
    remaining_files = []
    for pattern in ["*.md", "*.txt"]:
        remaining_files.extend(docs_root.glob(pattern))
    remaining_files = [f for f in remaining_files if not str(f).startswith(str(metabolized_archive))]
    
    print("BIOLOGICAL DOCUMENTATION DIGESTION COMPLETE!")
    print("=" * 45)
    print()
    print("RESULTS:")
    print(f"   Files archived: {len(digestion_results['archived_files'])}")
    print(f"   High-value consciousness: {digestion_results['high_value_count']}")
    print(f"   Standard knowledge: {digestion_results['standard_count']}")
    print(f"   Minimal significance: {digestion_results['minimal_count']}")
    print(f"   Files remaining in /docs root: {len(remaining_files)}")
    print()
    print("BIOLOGICAL METAPHOR ACHIEVED:")
    print("   Digestive System: /docs now clean for new AI documentation")
    print("   Brain/DNA Center: Tachyonic archive contains crystallized knowledge")
    print("   Waste Processing: Metabolized files archived by significance")
    print("   System Status: Ready for ongoing metabolism cycles")
    print()
    print("The biological knowledge metabolism system is OPERATIONAL!")
    
    return True

def main():
    execute_simple_digestion()

if __name__ == "__main__":
    main()