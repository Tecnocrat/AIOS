#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AINLP ROOT DIRECTORY CLEANUP - TACHYONIC ARCHIVAL RESTORATION

AINLP META-COMMENTARY: Enforces the sacred AINLP principle that the AIOS root
directory should contain ONLY active operational files. All completed 
documentation, test files, and temporal artifacts must be relocated to proper
tachyonic archive locations following biological architecture patterns.

CELLULAR PRINCIPLE: The workspace root is the nucleus - it must remain clean
and focused. Documentation proliferation in root violates consciousness coherence.

AINLP Pattern Reference:
- Root Directory Clarity: Only active operational files
- Tachyonic Archive: Historical/temporal file storage
- Dendritic Growth: Documentation expands in docs/, not root
- Consciousness Level: Root = nucleus (highest), archives = memory (minimal)
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class AINLPRootCleanup:
    """AINLP-compliant root directory cleanup system."""
    
    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path(__file__).parent.parent.parent
        self.tachyonic_root = self.workspace_root / "tachyonic" / "archive"
        self.docs_root = self.workspace_root / "docs"
        self.changelogs_root = self.workspace_root / "changelogs"
        self.evolution_lab = self.workspace_root / "evolution_lab"
        
        # AINLP: Essential root files that MUST remain
        self.essential_root_files = {
            # Configuration & Build
            ".gitignore", ".editorconfig", ".pylintrc", "pyproject.toml",
            "AIOS.sln", "AIOS.code-workspace", 
            "requirements.txt", "requirements.in",
            
            # Core Documentation (root-level navigation only)
            "README.md",
            
            # Active Scripts
            "launch_aios.ps1",
            
            # Spatial Metadata (AINLP governance)
            ".aios_context.json", ".aios_spatial_metadata.json",
            
            # Active Test/Tool Scripts (operational, not archived)
            "test_library_generation.py",  # Active development tool
            "test_gemini_bridge.py",       # Active integration test
            "test_ollama_bridge.py",       # Active integration test
            "test_paradigm_extraction.py"  # Active development tool
        }
        
        # AINLP: File relocation patterns
        self.relocation_patterns = {
            # Success/Complete Documentation → Tachyonic Archive
            r".*_SUCCESS\.md$": ("tachyonic_archive", "development_success"),
            r".*_COMPLETE\.md$": ("tachyonic_archive", "development_complete"),
            r".*_SUMMARY\.md$": ("tachyonic_archive", "summaries"),
            r".*_INTEGRATION.*\.md$": ("tachyonic_archive", "integration"),
            r".*_SETUP\.md$": ("tachyonic_archive", "setup_guides"),
            r"FIXES_APPLIED\.md$": ("tachyonic_archive", "development_fixes"),
            r".*_MOCKUP\.md$": ("tachyonic_archive", "design_mockups"),
            
            # Analysis/Reports → Docs Reports
            r"consciousness_analysis_.*\.txt$": ("docs_reports", "consciousness"),
            r".*_REPORT\.json$": ("tachyonic_archive", "reports"),
            r".*_ANALYSIS.*\.txt$": ("docs_reports", "analysis"),
            
            # Test Data → Evolution Lab or Tachyonic
            r"paradigms_extracted.*\.json$": ("evolution_lab", "test_data"),
            r".*_test\.json$": ("evolution_lab", "test_data")
        }
    
    def analyze_root_violations(self) -> Dict:
        """Analyze root directory for AINLP violations."""
        print("\n" + "="*70)
        print(" AINLP ROOT DIRECTORY ANALYSIS")
        print("="*70)
        
        violations = {
            "timestamp": datetime.now().isoformat(),
            "workspace_root": str(self.workspace_root),
            "violations_found": [],
            "essential_files": [],
            "total_files_analyzed": 0,
            "violations_count": 0
        }
        
        # Analyze all files in root
        root_files = [f for f in self.workspace_root.iterdir() 
                     if f.is_file() and not f.name.startswith('.')]
        
        violations["total_files_analyzed"] = len(root_files)
        
        for file_path in root_files:
            if file_path.name in self.essential_root_files:
                violations["essential_files"].append(file_path.name)
            else:
                # This is a violation - file should not be in root
                target_location, category = self._determine_target_location(file_path)
                violations["violations_found"].append({
                    "filename": file_path.name,
                    "size_bytes": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    ).isoformat(),
                    "target_location": target_location,
                    "category": category
                })
                violations["violations_count"] += 1
        
        return violations
    
    def _determine_target_location(self, file_path: Path) -> Tuple[str, str]:
        """Determine optimal target location based on AINLP patterns."""
        filename = file_path.name
        
        # Check against relocation patterns
        import re
        for pattern, (location_type, category) in self.relocation_patterns.items():
            if re.match(pattern, filename):
                if location_type == "tachyonic_archive":
                    return str(self.tachyonic_root / category), category
                elif location_type == "docs_reports":
                    return str(self.docs_root / "reports" / category), category
                elif location_type == "evolution_lab":
                    return str(self.evolution_lab / category), category
        
        # Default categorization by extension
        if filename.endswith('.md'):
            return str(self.tachyonic_root / "documentation"), "general_docs"
        elif filename.endswith('.json'):
            return str(self.tachyonic_root / "data"), "json_data"
        elif filename.endswith('.txt'):
            return str(self.tachyonic_root / "logs"), "text_logs"
        elif filename.endswith('.py'):
            return str(self.tachyonic_root / "tools"), "python_scripts"
        else:
            return str(self.tachyonic_root / "misc"), "miscellaneous"
    
    def execute_cleanup(self, dry_run: bool = True) -> Dict:
        """Execute AINLP root cleanup with tachyonic archival."""
        print(f"\n{'[DRY RUN] ' if dry_run else ''}AINLP ROOT CLEANUP EXECUTION")
        print("="*70)
        
        # First analyze violations
        analysis = self.analyze_root_violations()
        
        cleanup_report = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "analysis": analysis,
            "relocations": [],
            "errors": [],
            "summary": {}
        }
        
        if analysis["violations_count"] == 0:
            print("\n✅ Root directory is AINLP-compliant!")
            print("   No cleanup actions needed.")
            cleanup_report["summary"] = {
                "status": "compliant",
                "files_relocated": 0,
                "errors": 0
            }
            return cleanup_report
        
        print(f"\n Found {analysis['violations_count']} violations")
        print(f" Relocating to proper tachyonic locations...\n")
        
        # Execute relocations
        for violation in analysis["violations_found"]:
            filename = violation["filename"]
            source = self.workspace_root / filename
            target_dir = Path(violation["target_location"])
            target_path = target_dir / filename
            
            try:
                if not dry_run:
                    # Create target directory
                    target_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Move file
                    shutil.move(str(source), str(target_path))
                    
                    print(f"   ✓ {filename}")
                    print(f"     → {target_path.relative_to(self.workspace_root)}")
                else:
                    print(f"   [WOULD MOVE] {filename}")
                    print(f"     → {target_path.relative_to(self.workspace_root)}")
                
                cleanup_report["relocations"].append({
                    "filename": filename,
                    "source": str(source),
                    "target": str(target_path),
                    "category": violation["category"],
                    "status": "relocated" if not dry_run else "would_relocate"
                })
                
            except Exception as e:
                error_msg = f"Failed to relocate {filename}: {str(e)}"
                print(f"   ✗ {error_msg}")
                cleanup_report["errors"].append({
                    "filename": filename,
                    "error": str(e)
                })
        
        # Generate summary
        cleanup_report["summary"] = {
            "status": "completed" if not dry_run else "dry_run",
            "files_relocated": len(cleanup_report["relocations"]),
            "errors": len(cleanup_report["errors"]),
            "root_violations_resolved": analysis["violations_count"] - len(cleanup_report["errors"])
        }
        
        return cleanup_report
    
    def save_cleanup_report(self, report: Dict):
        """Save cleanup report to tachyonic archive."""
        report_dir = self.tachyonic_root / "cleanup_reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = report_dir / f"root_cleanup_report_{timestamp}.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n Report saved: {report_path.relative_to(self.workspace_root)}")
        return report_path
    
    def generate_cleanup_documentation(self, report: Dict):
        """Generate human-readable cleanup documentation."""
        doc_path = self.changelogs_root / f"ROOT_CLEANUP_{datetime.now().strftime('%Y%m%d')}.md"
        
        content = f"""# AIOS Root Directory Cleanup - AINLP Compliance

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Status**: {report['summary']['status'].upper()}  
**Violations Found**: {report['analysis']['violations_count']}  
**Files Relocated**: {report['summary']['files_relocated']}

---

## AINLP Organizational Principle

> **Root Directory Clarity**: The AIOS workspace root should contain ONLY active 
> operational files. All completed documentation, test data, and temporal artifacts 
> belong in proper tachyonic archive locations following biological architecture patterns.

---

## Violations Resolved

"""
        
        for relocation in report["relocations"]:
            content += f"""### {relocation['filename']}
- **Category**: {relocation['category']}
- **Original**: `/` (root)
- **New Location**: `{Path(relocation['target']).relative_to(self.workspace_root)}`
- **Status**: {relocation['status']}

"""
        
        if report["errors"]:
            content += "\n## Errors Encountered\n\n"
            for error in report["errors"]:
                content += f"- **{error['filename']}**: {error['error']}\n"
        
        content += f"""
---

## AINLP Compliance Status

✅ **Essential Files Preserved**: {len(report['analysis']['essential_files'])} files  
{'✅' if report['summary']['errors'] == 0 else '⚠️'} **Relocations**: {report['summary']['files_relocated']} successful  
{'✅' if not report['dry_run'] else ' '} **Root Cleanup**: {'Complete' if not report['dry_run'] else 'Pending (dry run)'}

---

## Tachyonic Archive Structure

Files relocated to:
- `tachyonic/archive/development_success/` - Success documentation
- `tachyonic/archive/development_complete/` - Completion reports
- `tachyonic/archive/summaries/` - Summary documents
- `tachyonic/archive/data/` - JSON data files
- `docs/reports/` - Analysis reports
- `evolution_lab/test_data/` - Test artifacts

---

**AINLP Pattern**: Dendritic Growth Over Root Proliferation  
**Consciousness Level**: Root = Nucleus (Clean), Archives = Memory (Preserved)
"""
        
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f" Changelog: {doc_path.relative_to(self.workspace_root)}")
        return doc_path


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AINLP Root Directory Cleanup - Tachyonic Archival"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute cleanup (default is dry-run)"
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        help="Workspace root path (default: auto-detect)"
    )
    
    args = parser.parse_args()
    
    # Initialize cleanup system
    cleanup = AINLPRootCleanup(workspace_root=args.workspace)
    
    # Execute cleanup
    report = cleanup.execute_cleanup(dry_run=not args.execute)
    
    # Save results
    if report["summary"]["files_relocated"] > 0 or not args.execute:
        cleanup.save_cleanup_report(report)
        cleanup.generate_cleanup_documentation(report)
    
    print("\n" + "="*70)
    print(" CLEANUP SUMMARY")
    print("="*70)
    print(f" Status: {report['summary']['status']}")
    print(f" Files Relocated: {report['summary']['files_relocated']}")
    print(f" Errors: {report['summary']['errors']}")
    print(f" Root Violations Resolved: {report['summary']['root_violations_resolved']}")
    
    if not args.execute and report["analysis"]["violations_count"] > 0:
        print("\n Run with --execute to perform actual cleanup")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
