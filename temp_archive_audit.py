"""
Archive File Duplication Audit Tool
Compares files in tachyonic/archive/computational_layer_ingested_20251025/ 
against runtime/ directory to identify duplicates
"""

import os
import json
import hashlib
from pathlib import Path
from difflib import SequenceMatcher

# Base paths
ARCHIVE_BASE = r"c:\aios-supercell\aios-core\tachyonic\archive\computational_layer_ingested_20251025"
RUNTIME_BASE = r"c:\aios-supercell\aios-core\runtime"

def calculate_md5(filepath):
    """Calculate MD5 hash of file content"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        return None

def calculate_similarity(file1, file2):
    """Calculate text similarity between two files (0.0 to 1.0)"""
    try:
        with open(file1, 'r', encoding='utf-8', errors='ignore') as f1:
            content1 = f1.read()
        with open(file2, 'r', encoding='utf-8', errors='ignore') as f2:
            content2 = f2.read()
        
        # Use SequenceMatcher for similarity
        ratio = SequenceMatcher(None, content1, content2).ratio()
        return ratio
    except Exception as e:
        return 0.0

def find_runtime_equivalent(archive_file):
    """Find potential runtime equivalent for archive file"""
    archive_path = Path(archive_file)
    filename = archive_path.name
    
    # Search for matching filename in runtime directory
    runtime_path = Path(RUNTIME_BASE)
    matches = list(runtime_path.rglob(filename))
    
    if matches:
        return str(matches[0])
    return None

def analyze_file(archive_file):
    """Analyze a single archive file for duplication"""
    archive_path = Path(archive_file)
    relative_path = archive_path.relative_to(ARCHIVE_BASE)
    
    # Skip test files
    if 'test_' in archive_path.name or archive_path.name.startswith('test'):
        return {
            "file": str(relative_path),
            "runtime_equivalent": None,
            "similarity": "SKIPPED",
            "recommendation": "KEEP",
            "notes": "Test file - intentionally duplicated"
        }
    
    # Find potential runtime equivalent
    runtime_file = find_runtime_equivalent(archive_file)
    
    if runtime_file is None:
        return {
            "file": str(relative_path),
            "runtime_equivalent": None,
            "similarity": "UNIQUE",
            "recommendation": "KEEP",
            "notes": "No matching file found in runtime/"
        }
    
    # Calculate hashes and similarity
    archive_md5 = calculate_md5(archive_file)
    runtime_md5 = calculate_md5(runtime_file)
    
    if archive_md5 == runtime_md5:
        return {
            "file": str(relative_path),
            "runtime_equivalent": str(Path(runtime_file).relative_to(RUNTIME_BASE)),
            "similarity": "EXACT_DUPLICATE",
            "recommendation": "DELETE",
            "notes": "100% identical - MD5 hash match"
        }
    
    # Calculate text similarity
    similarity = calculate_similarity(archive_file, runtime_file)
    
    if similarity >= 0.90:
        return {
            "file": str(relative_path),
            "runtime_equivalent": str(Path(runtime_file).relative_to(RUNTIME_BASE)),
            "similarity": "HIGH_SIMILARITY",
            "recommendation": "REVIEW",
            "notes": f"{similarity*100:.1f}% similar - manual review required"
        }
    else:
        return {
            "file": str(relative_path),
            "runtime_equivalent": str(Path(runtime_file).relative_to(RUNTIME_BASE)),
            "similarity": "UNIQUE",
            "recommendation": "KEEP",
            "notes": f"{similarity*100:.1f}% similar - significant differences"
        }

def main():
    """Main audit function"""
    archive_base = Path(ARCHIVE_BASE)
    
    if not archive_base.exists():
        print(f"ERROR: Archive directory not found: {ARCHIVE_BASE}")
        return
    
    # Collect all Python files
    python_files = list(archive_base.rglob("*.py"))
    
    print(f"Found {len(python_files)} Python files in archive")
    print("Starting duplication analysis...\n")
    
    results = []
    
    for i, py_file in enumerate(python_files, 1):
        print(f"[{i}/{len(python_files)}] Analyzing: {py_file.name}")
        result = analyze_file(str(py_file))
        results.append(result)
    
    # Generate summary statistics
    summary = {
        "total_files": len(results),
        "exact_duplicates": sum(1 for r in results if r["similarity"] == "EXACT_DUPLICATE"),
        "high_similarity": sum(1 for r in results if r["similarity"] == "HIGH_SIMILARITY"),
        "unique": sum(1 for r in results if r["similarity"] == "UNIQUE"),
        "skipped": sum(1 for r in results if r["similarity"] == "SKIPPED")
    }
    
    # Output results
    output = {
        "audit_date": "2025-11-22",
        "archive_path": str(ARCHIVE_BASE),
        "runtime_path": str(RUNTIME_BASE),
        "summary": summary,
        "files": results
    }
    
    # Save to JSON file
    output_file = r"c:\aios-supercell\aios-core\archive_duplication_audit.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*80}")
    print("AUDIT SUMMARY")
    print(f"{'='*80}")
    print(f"Total Files Analyzed: {summary['total_files']}")
    print(f"Exact Duplicates (DELETE): {summary['exact_duplicates']}")
    print(f"High Similarity (REVIEW): {summary['high_similarity']}")
    print(f"Unique Files (KEEP): {summary['unique']}")
    print(f"Test Files (SKIPPED): {summary['skipped']}")
    print(f"\nFull report saved to: {output_file}")
    
    # Print exact duplicates for immediate action
    if summary['exact_duplicates'] > 0:
        print(f"\n{'='*80}")
        print("EXACT DUPLICATES (Safe to delete):")
        print(f"{'='*80}")
        for r in results:
            if r["similarity"] == "EXACT_DUPLICATE":
                print(f"  - {r['file']}")
                print(f"    Runtime: {r['runtime_equivalent']}")

if __name__ == "__main__":
    main()
