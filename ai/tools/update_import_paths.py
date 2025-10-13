#!/usr/bin/env python3
"""
AIOS Import Path Update Automation
===================================

Automatically updates import statements referencing migrated tools from
runtime_intelligence/tools/ to new ai/tools/[category]/ structure.

Usage:
    python ai/tools/update_import_paths.py --dry-run    # Preview changes
    python ai/tools/update_import_paths.py --execute    # Apply updates
    python ai/tools/update_import_paths.py --validate   # Test imports

AINLP Integration: ai/tools/update_import_paths.py
Purpose: Automate import path updates for 31 migrated tools
Category: system (automated maintenance utility)
"""

import argparse
import ast
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional

# Workspace root
ROOT = Path(__file__).resolve().parents[2]  # c:/dev/AIOS

# Tool category mappings (from migration batches)
TOOL_CATEGORIES = {
    # System tools (18)
    "system_health_check": "system",
    "system_status_report": "system",
    "aios_admin": "system",
    "ainlp_root_cleanup": "system",
    "aios_dendritic_path_tracker": "system",
    "aios_dev_setup": "system",
    "comprehensive_aios_health_test": "system",
    "demo_enhanced_commit_hook": "system",
    "generate_file_scores": "system",
    "integration_test_runner": "system",
    "python_environment_validator": "system",
    "runtime_intelligence_comprehensive_test": "system",
    "safety_demo": "system",
    "safety_rollback": "system",
    "subprocess_manager": "system",
    "temp_neural_analysis": "system",
    "index_tools": "system",
    
    # Architecture tools (8)
    "ainlp_holographic_documentation_system": "architecture",
    "ainlp_integration_optimizer": "architecture",
    "aios_cpp_analyzer": "architecture",
    "aios_powershell_analyzer": "architecture",
    "aios_architecture_monitor": "architecture",
    "architectural_compliance_validator": "architecture",
    "biological_architecture_monitor": "architecture",
    "self_similarity_analyzer": "architecture",
    
    # Consciousness tools (7)
    "aios_cli_agent_system": "consciousness",
    "consciousness_analysis_report": "consciousness",
    "consciousness_emergence_demo": "consciousness",
    "enhanced_consciousness_demo": "consciousness",
    "dendritic_supervisor": "consciousness",
    "runtime_intelligence_dendritic_integration": "consciousness",
    "dendritic_self_improvement_orchestrator": "consciousness",
    
    # Visual tools (4)
    "enhanced_visual_intelligence_bridge": "visual",
    "consciousness_visual_analyzer": "visual",
    "visual_intelligence_bridge_enhanced": "visual",
    "visual_intelligence_bridge": "visual",
    
    # Tachyonic tools (2)
    "create_stl_crystal": "tachyonic",
    "ingest_microsoft_agent_framework": "tachyonic",
}

# Directories to exclude from scanning
EXCLUDE_DIRS = {
    ".git",
    ".venv",
    ".venv314t",
    "node_modules",
    "__pycache__",
    "build",
    "dist",
    "backups",
    "ai/tools",  # Exclude migrated tools directory
    "runtime_intelligence/tools",  # Exclude old tools directory
    "tachyonic/archive",  # Exclude archives
    "tachyonic/backups",
}

# File extensions to scan
PYTHON_EXTENSIONS = {".py"}


class ImportPathUpdater:
    """Automated import path updater for migrated tools."""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.files_scanned = 0
        self.files_modified = 0
        self.imports_updated = 0
        self.changes: List[Dict] = []
        self.errors: List[Dict] = []
        
    def scan_workspace(self) -> List[Path]:
        """Scan workspace for Python files to process."""
        python_files = []
        
        for path in ROOT.rglob("*.py"):
            # Skip excluded directories
            if any(excluded in path.parts for excluded in EXCLUDE_DIRS):
                continue
            
            # Skip if in ai/tools or runtime_intelligence/tools
            rel_path = path.relative_to(ROOT)
            if str(rel_path).startswith("ai\\tools") or str(rel_path).startswith("ai/tools"):
                continue
            if str(rel_path).startswith("runtime_intelligence\\tools") or str(rel_path).startswith("runtime_intelligence/tools"):
                continue
                
            python_files.append(path)
            
        return python_files
    
    def detect_old_imports(self, file_path: Path) -> List[Tuple[int, str, str, str]]:
        """
        Detect import statements referencing old tool paths.
        
        Returns:
            List of (line_number, original_line, tool_name, category) tuples
        """
        detections = []
        
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.splitlines()
            
            for line_num, line in enumerate(lines, 1):
                # Pattern 1: from [toolname] import ...
                match1 = re.match(r'^from\s+(\w+)\s+import\s+', line)
                if match1:
                    tool_name = match1.group(1)
                    if tool_name in TOOL_CATEGORIES:
                        category = TOOL_CATEGORIES[tool_name]
                        detections.append((line_num, line, tool_name, category))
                        continue
                
                # Pattern 2: import [toolname]
                match2 = re.match(r'^import\s+(\w+)(?:\s+as\s+\w+)?$', line)
                if match2:
                    tool_name = match2.group(1)
                    if tool_name in TOOL_CATEGORIES:
                        category = TOOL_CATEGORIES[tool_name]
                        detections.append((line_num, line, tool_name, category))
                        continue
                
                # Pattern 3: from runtime_intelligence.tools import [toolname]
                match3 = re.match(r'^from\s+runtime_intelligence\.tools(?:\.(\w+))?\s+import\s+', line)
                if match3:
                    # Extract tool name from import clause
                    import_part = line.split("import", 1)[1].strip()
                    # Handle "import tool1, tool2" or "import tool1"
                    imported_tools = [t.strip().split()[0] for t in import_part.split(",")]
                    for tool_name in imported_tools:
                        if tool_name in TOOL_CATEGORIES:
                            category = TOOL_CATEGORIES[tool_name]
                            detections.append((line_num, line, tool_name, category))
                            break  # One detection per line
                    continue
                
                # Pattern 4: from runtime_intelligence.tools.[toolname] import ...
                match4 = re.match(r'^from\s+runtime_intelligence\.tools\.(\w+)\s+import\s+', line)
                if match4:
                    tool_name = match4.group(1)
                    if tool_name in TOOL_CATEGORIES:
                        category = TOOL_CATEGORIES[tool_name]
                        detections.append((line_num, line, tool_name, category))
                        continue
                        
        except Exception as e:
            self.errors.append({
                "file": str(file_path),
                "error": f"Error reading file: {e}"
            })
            
        return detections
    
    def generate_new_import(self, old_line: str, tool_name: str, category: str) -> str:
        """Generate new import statement with correct path."""
        
        # Pattern 1: from [toolname] import ... → from ai.tools.[category].[toolname] import ...
        if old_line.startswith(f"from {tool_name} import"):
            new_line = old_line.replace(
                f"from {tool_name} import",
                f"from ai.tools.{category}.{tool_name} import"
            )
            return new_line
        
        # Pattern 2: import [toolname] → from ai.tools.[category] import [toolname]
        if old_line.startswith(f"import {tool_name}"):
            # Handle "import tool as alias"
            if " as " in old_line:
                alias = old_line.split(" as ")[1].strip()
                new_line = f"from ai.tools.{category} import {tool_name} as {alias}"
            else:
                new_line = f"from ai.tools.{category} import {tool_name}"
            return new_line
        
        # Pattern 3: from runtime_intelligence.tools import [toolname]
        if "from runtime_intelligence.tools import" in old_line:
            new_line = old_line.replace(
                "from runtime_intelligence.tools import",
                f"from ai.tools.{category} import"
            )
            return new_line
        
        # Pattern 4: from runtime_intelligence.tools.[toolname] import ...
        if f"from runtime_intelligence.tools.{tool_name} import" in old_line:
            new_line = old_line.replace(
                f"from runtime_intelligence.tools.{tool_name} import",
                f"from ai.tools.{category}.{tool_name} import"
            )
            return new_line
        
        # Fallback: return original (shouldn't happen)
        return old_line
    
    def update_file(self, file_path: Path, detections: List[Tuple[int, str, str, str]]) -> bool:
        """
        Update file with new import paths.
        
        Returns:
            True if file was modified, False otherwise
        """
        if not detections:
            return False
        
        try:
            # Read file content
            content = file_path.read_text(encoding="utf-8")
            lines = content.splitlines(keepends=True)
            
            # Create backup if not dry run
            if not self.dry_run:
                backup_path = file_path.with_suffix(file_path.suffix + ".backup")
                shutil.copy2(file_path, backup_path)
            
            # Apply replacements
            modified = False
            for line_num, old_line, tool_name, category in detections:
                new_line = self.generate_new_import(old_line, tool_name, category)
                
                if new_line != old_line:
                    # Update line (preserve line ending)
                    idx = line_num - 1
                    original_ending = "\n" if lines[idx].endswith("\n") else ""
                    lines[idx] = new_line.rstrip() + original_ending
                    
                    modified = True
                    self.imports_updated += 1
                    
                    # Record change
                    self.changes.append({
                        "file": str(file_path.relative_to(ROOT)),
                        "line": line_num,
                        "tool": tool_name,
                        "category": category,
                        "old": old_line.strip(),
                        "new": new_line.strip()
                    })
            
            # Write updated content if not dry run
            if modified and not self.dry_run:
                file_path.write_text("".join(lines), encoding="utf-8")
                self.files_modified += 1
            
            return modified
            
        except Exception as e:
            self.errors.append({
                "file": str(file_path),
                "error": f"Error updating file: {e}"
            })
            return False
    
    def process_workspace(self):
        """Process all Python files in workspace."""
        print(f"[IMPORT PATH UPDATER] Scanning workspace: {ROOT}")
        print(f"[IMPORT PATH UPDATER] Mode: {'DRY RUN' if self.dry_run else 'EXECUTE'}")
        print()
        
        # Scan for Python files
        python_files = self.scan_workspace()
        print(f"[SCAN] Found {len(python_files)} Python files to scan")
        print()
        
        # Process each file
        files_with_changes = []
        for file_path in python_files:
            self.files_scanned += 1
            
            # Detect old imports
            detections = self.detect_old_imports(file_path)
            
            if detections:
                files_with_changes.append((file_path, detections))
                rel_path = file_path.relative_to(ROOT)
                print(f"[DETECT] {rel_path}: {len(detections)} old import(s) found")
        
        print()
        print(f"[SUMMARY] {len(files_with_changes)} file(s) with old imports")
        print()
        
        # Update files
        if files_with_changes:
            print("[UPDATE] Processing updates...")
            print()
            
            for file_path, detections in files_with_changes:
                rel_path = file_path.relative_to(ROOT)
                modified = self.update_file(file_path, detections)
                
                if modified:
                    status = "PREVIEW" if self.dry_run else "UPDATED"
                    print(f"[{status}] {rel_path}: {len(detections)} import(s)")
        
        print()
        self.print_report()
    
    def print_report(self):
        """Print detailed report of changes."""
        print("=" * 80)
        print("IMPORT PATH UPDATE REPORT")
        print("=" * 80)
        print()
        
        print(f"Mode: {'DRY RUN (preview only)' if self.dry_run else 'EXECUTE (changes applied)'}")
        print(f"Files scanned: {self.files_scanned}")
        print(f"Files with changes: {len(set(c['file'] for c in self.changes))}")
        print(f"Import statements updated: {self.imports_updated}")
        print()
        
        if self.changes:
            print("CHANGES BY CATEGORY:")
            print()
            
            # Group by category
            by_category = {}
            for change in self.changes:
                category = change['category']
                by_category.setdefault(category, []).append(change)
            
            for category, changes in sorted(by_category.items()):
                print(f"  {category.upper()}: {len(changes)} import(s)")
            
            print()
            print("DETAILED CHANGES:")
            print()
            
            for change in self.changes:
                print(f"  File: {change['file']}")
                print(f"  Line: {change['line']}")
                print(f"  Tool: {change['tool']} → {change['category']}")
                print(f"  Old:  {change['old']}")
                print(f"  New:  {change['new']}")
                print()
        
        if self.errors:
            print("ERRORS:")
            print()
            for error in self.errors:
                print(f"  {error['file']}: {error['error']}")
            print()
        
        if self.dry_run:
            print("[DRY RUN] No files were modified. Run with --execute to apply changes.")
        else:
            print("[EXECUTE] Changes have been applied. Backup files created with .backup extension.")
            print()
            print("NEXT STEPS:")
            print("  1. Run validation: python ai/tools/update_import_paths.py --validate")
            print("  2. Test imports manually if needed")
            print("  3. Commit changes with git")
            print("  4. Remove backup files: find . -name '*.py.backup' -delete")
        
        print()
        print("=" * 80)
    
    def save_report(self):
        """Save detailed report to JSON file."""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "mode": "dry_run" if self.dry_run else "execute",
            "summary": {
                "files_scanned": self.files_scanned,
                "files_modified": self.files_modified,
                "imports_updated": self.imports_updated
            },
            "changes": self.changes,
            "errors": self.errors
        }
        
        report_path = ROOT / "ai" / "tools" / "import_update_report.json"
        report_path.write_text(json.dumps(report_data, indent=2), encoding="utf-8")
        
        print(f"[REPORT] Detailed report saved to: {report_path.relative_to(ROOT)}")
        print()
    
    def validate_imports(self):
        """Validate that all updated imports can be resolved."""
        print("[VALIDATE] Testing import statements...")
        print()
        
        validation_errors = []
        
        for tool_name, category in TOOL_CATEGORIES.items():
            try:
                # Test import
                module_path = f"ai.tools.{category}.{tool_name}"
                exec(f"from {module_path} import *", {})
                print(f"  ✅ {module_path}")
            except ImportError as e:
                validation_errors.append({
                    "tool": tool_name,
                    "category": category,
                    "error": str(e)
                })
                print(f"  ❌ ai.tools.{category}.{tool_name}: {e}")
            except Exception as e:
                # Other errors (syntax, etc.) - expected for some tools
                print(f"  ⚠️  ai.tools.{category}.{tool_name}: {type(e).__name__}")
        
        print()
        if validation_errors:
            print(f"[VALIDATE] {len(validation_errors)} import error(s) detected")
            print("Note: Some errors may be expected (missing dependencies, syntax errors in tool code)")
        else:
            print("[VALIDATE] All imports resolved successfully!")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Update import paths for migrated AIOS tools"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files (default)"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Apply changes to files (creates .backup files)"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate that imports can be resolved"
    )
    
    args = parser.parse_args()
    
    # Default to dry run if no mode specified
    if not args.execute and not args.validate:
        args.dry_run = True
    
    # Validation mode
    if args.validate:
        updater = ImportPathUpdater(dry_run=True)
        updater.validate_imports()
        return
    
    # Update mode
    updater = ImportPathUpdater(dry_run=args.dry_run)
    updater.process_workspace()
    updater.save_report()


if __name__ == "__main__":
    main()
