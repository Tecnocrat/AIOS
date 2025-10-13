#!/usr/bin/env python3
"""
 AIOS FILE TRACKING & DEPENDENCY MANAGEMENT SYSTEM 
=======================================================

Core infrastructure for tracking file locations, imports, dependencies, and structural changes.
Solves the fundamental AI context retention challenge: "Where are the files at every point?"

Author: AIOS Development Team
Date: 2025-09-06
"""

import ast
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class FileRecord:
    """Record of a file's current state and metadata"""
    file_path: str
    relative_path: str
    file_hash: str
    size_bytes: int
    last_modified: str
    imports: List[str]
    exports: List[str]
    dependencies: List[str]
    subcell: str
    purpose: str


@dataclass
class DependencyChange:
    """Record of a dependency change between files"""
    timestamp: str
    change_type: str  # 'added', 'removed', 'modified'
    source_file: str
    target_file: str
    import_statement: str
    context: str


@dataclass
class StructuralChange:
    """Record of structural changes (file moves, renames, etc.)"""
    timestamp: str
    change_type: str  # 'moved', 'renamed', 'created', 'deleted'
    old_path: Optional[str]
    new_path: Optional[str]
    file_hash: str
    subcell_change: bool


class FileTracker:
    """Tracks file locations, contents, and structural changes"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.tracking_data = {
            "files": {},  # file_path -> FileRecord
            "dependency_graph": {},  # file_path -> [dependent_files]
            "reverse_dependencies": {},  # file_path -> [files_that_depend_on_this]
            "structural_changes": [],
            "dependency_changes": [],
            "last_scan": None
        }
        
        # Initialize tracking database
        self.tracking_file = self.workspace_root / "runtime_intelligence" / "file_tracking_database.json"
        self.load_tracking_data()
    
    def load_tracking_data(self):
        """Load existing tracking data"""
        if self.tracking_file.exists():
            try:
                with open(self.tracking_file, 'r') as f:
                    data = json.load(f)
                    self.tracking_data.update(data)
                    print(f" Loaded tracking data from {self.tracking_file}")
            except Exception as e:
                print(f" Could not load tracking data: {e}")
    
    def save_tracking_data(self):
        """Save tracking data to persistent storage"""
        # Ensure directory exists
        self.tracking_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert dataclasses to dicts for JSON serialization
        serializable_data = {
            "files": {path: asdict(record) if hasattr(record, '__dataclass_fields__') else record 
                     for path, record in self.tracking_data["files"].items()},
            "dependency_graph": self.tracking_data["dependency_graph"],
            "reverse_dependencies": self.tracking_data["reverse_dependencies"],
            "structural_changes": [asdict(change) if hasattr(change, '__dataclass_fields__') else change 
                                  for change in self.tracking_data["structural_changes"]],
            "dependency_changes": [asdict(change) if hasattr(change, '__dataclass_fields__') else change 
                                  for change in self.tracking_data["dependency_changes"]],
            "last_scan": datetime.now().isoformat(),
            "metadata": {
                "total_files": len(self.tracking_data["files"]),
                "total_dependencies": sum(len(deps) for deps in self.tracking_data["dependency_graph"].values()),
                "last_updated": datetime.now().isoformat()
            }
        }
        
        with open(self.tracking_file, 'w') as f:
            json.dump(serializable_data, f, indent=2)
        
        print(f" Saved tracking data to {self.tracking_file}")
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file contents"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return "unknown"
    
    def extract_python_imports(self, file_path: Path) -> tuple[List[str], List[str]]:
        """Extract imports and exports from Python file"""
        imports = []
        exports = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Extract imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}" if module else alias.name)
                
                # Extract function and class definitions (exports)
                elif isinstance(node, ast.FunctionDef):
                    exports.append(f"function:{node.name}")
                elif isinstance(node, ast.ClassDef):
                    exports.append(f"class:{node.name}")
                elif isinstance(node, ast.Assign):
                    # Extract variable assignments at module level
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            exports.append(f"variable:{target.id}")
        
        except Exception as e:
            print(f" Could not parse {file_path}: {e}")
        
        return imports, exports
    
    def determine_subcell(self, file_path: Path) -> str:
        """Determine which subcell a file belongs to"""
        relative = file_path.relative_to(self.workspace_root)
        parts = relative.parts
        
        if len(parts) == 1:
            return "root"
        else:
            return parts[0]
    
    def determine_file_purpose(self, file_path: Path, imports: List[str], exports: List[str]) -> str:
        """Determine the purpose/role of a file"""
        name = file_path.name.lower()
        
        # Analyze filename patterns
        if "_test" in name or name.startswith("test_"):
            return "testing"
        elif "_bridge" in name:
            return "integration_bridge"
        elif "_analyzer" in name or "_analysis" in name:
            return "analysis_tool"
        elif "_monitor" in name or "_tracker" in name:
            return "monitoring"
        elif "_organizer" in name or "_optimizer" in name:
            return "organization"
        elif name.endswith(".md"):
            return "documentation"
        elif name.endswith(".json"):
            return "data_storage"
        elif "main" in name or name.startswith("aios_enhanced"):
            return "main_executable"
        
        # Analyze exports to infer purpose
        has_classes = any(exp.startswith("class:") for exp in exports)
        has_functions = any(exp.startswith("function:") for exp in exports)
        
        if has_classes and "Manager" in str(exports):
            return "system_manager"
        elif has_classes and ("Bridge" in str(exports) or "Interface" in str(exports)):
            return "interface_layer"
        elif has_functions and len(exports) > 5:
            return "utility_library"
        elif "main" in exports:
            return "executable_script"
        
        return "general_module"
    
    def scan_file(self, file_path: Path) -> FileRecord:
        """Scan a single file and create tracking record"""
        try:
            # Basic file info
            stat = file_path.stat()
            file_hash = self.calculate_file_hash(file_path)
            relative_path = str(file_path.relative_to(self.workspace_root))
            
            # Extract imports/exports for Python files
            imports, exports = [], []
            if file_path.suffix == '.py':
                imports, exports = self.extract_python_imports(file_path)
            
            # Determine dependencies (files this file imports from workspace)
            dependencies = []
            for imp in imports:
                # Check if import refers to a local file
                if imp.startswith('aios_') or imp.startswith('.'):
                    dependencies.append(imp)
            
            # Create record
            record = FileRecord(
                file_path=str(file_path),
                relative_path=relative_path,
                file_hash=file_hash,
                size_bytes=stat.st_size,
                last_modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
                imports=imports,
                exports=exports,
                dependencies=dependencies,
                subcell=self.determine_subcell(file_path),
                purpose=self.determine_file_purpose(file_path, imports, exports)
            )
            
            return record
            
        except Exception as e:
            print(f" Error scanning {file_path}: {e}")
            return None
    
    def full_workspace_scan(self) -> Dict[str, Any]:
        """Perform complete scan of workspace"""
        print(" Starting full workspace scan...")
        
        # Find all relevant files
        file_patterns = ['*.py', '*.md', '*.json', '*.cs', '*.txt']
        all_files = []
        
        for pattern in file_patterns:
            all_files.extend(self.workspace_root.rglob(pattern))
        
        # Filter out unwanted directories
        filtered_files = []
        skip_dirs = {'__pycache__', '.git', 'node_modules', 'build', 'obj', '.vs'}
        
        for file_path in all_files:
            if not any(skip_dir in file_path.parts for skip_dir in skip_dirs):
                filtered_files.append(file_path)
        
        print(f" Found {len(filtered_files)} files to scan")
        
        # Scan each file
        new_files = {}
        changed_files = []
        
        for file_path in filtered_files:
            record = self.scan_file(file_path)
            if record:
                rel_path = record.relative_path
                
                # Check if file changed
                if rel_path in self.tracking_data["files"]:
                    old_record_data = self.tracking_data["files"][rel_path]
                    # Handle both dict and FileRecord objects
                    old_hash = old_record_data.get('file_hash') if isinstance(old_record_data, dict) else old_record_data.file_hash
                    if old_hash != record.file_hash:
                        changed_files.append(rel_path)
                        # Only track dependency changes if we have proper record objects
                        if not isinstance(old_record_data, dict):
                            self.track_dependency_changes(old_record_data, record)
                
                new_files[rel_path] = record
        
        # Update tracking data
        old_files = set(self.tracking_data["files"].keys())
        new_file_paths = set(new_files.keys())
        
        # Detect structural changes
        deleted_files = old_files - new_file_paths
        added_files = new_file_paths - old_files
        
        for deleted_file in deleted_files:
            self.track_structural_change("deleted", deleted_file, None)
        
        for added_file in added_files:
            self.track_structural_change("created", None, added_file)
        
        # Update files and rebuild dependency graph
        self.tracking_data["files"] = new_files
        self.rebuild_dependency_graph()
        
        # Save results
        self.save_tracking_data()
        
        scan_results = {
            "total_files": len(new_files),
            "changed_files": len(changed_files),
            "added_files": len(added_files),
            "deleted_files": len(deleted_files),
            "total_dependencies": sum(len(deps) for deps in self.tracking_data["dependency_graph"].values())
        }
        
        print(f" Workspace scan complete: {scan_results}")
        return scan_results
    
    def track_structural_change(self, change_type: str, old_path: Optional[str], new_path: Optional[str]):
        """Track structural changes like file moves, renames, etc."""
        change = StructuralChange(
            timestamp=datetime.now().isoformat(),
            change_type=change_type,
            old_path=old_path,
            new_path=new_path,
            file_hash="unknown",
            subcell_change=True
        )
        
        self.tracking_data["structural_changes"].append(change)
        print(f" Tracked structural change: {change_type} {old_path} -> {new_path}")
    
    def track_dependency_changes(self, old_record: FileRecord, new_record: FileRecord):
        """Track changes in file dependencies"""
        old_deps = set(old_record.dependencies)
        new_deps = set(new_record.dependencies)
        
        added_deps = new_deps - old_deps
        removed_deps = old_deps - new_deps
        
        for dep in added_deps:
            change = DependencyChange(
                timestamp=datetime.now().isoformat(),
                change_type="added",
                source_file=new_record.relative_path,
                target_file=dep,
                import_statement=dep,
                context="dependency_scan"
            )
            self.tracking_data["dependency_changes"].append(change)
        
        for dep in removed_deps:
            change = DependencyChange(
                timestamp=datetime.now().isoformat(),
                change_type="removed",
                source_file=new_record.relative_path,
                target_file=dep,
                import_statement=dep,
                context="dependency_scan"
            )
            self.tracking_data["dependency_changes"].append(change)
    
    def rebuild_dependency_graph(self):
        """Rebuild the dependency graph from current file records"""
        dependency_graph = {}
        reverse_dependencies = {}
        
        for file_path, record in self.tracking_data["files"].items():
            dependency_graph[file_path] = record.dependencies
            
            # Build reverse dependencies
            for dep in record.dependencies:
                if dep not in reverse_dependencies:
                    reverse_dependencies[dep] = []
                reverse_dependencies[dep].append(file_path)
        
        self.tracking_data["dependency_graph"] = dependency_graph
        self.tracking_data["reverse_dependencies"] = reverse_dependencies
    
    def get_file_location(self, filename: str) -> Optional[str]:
        """Answer: Where is this file now?"""
        for file_path, record in self.tracking_data["files"].items():
            if filename in file_path:
                return record.file_path
        return None
    
    def get_file_dependencies(self, filename: str) -> List[str]:
        """Answer: What does this file depend on?"""
        for file_path, record in self.tracking_data["files"].items():
            if filename in file_path:
                return record.dependencies
        return []
    
    def get_dependent_files(self, filename: str) -> List[str]:
        """Answer: What files depend on this file?"""
        result = []
        for file_path, deps in self.tracking_data["dependency_graph"].items():
            if any(filename in dep for dep in deps):
                result.append(file_path)
        return result
    
    def generate_dependency_report(self) -> str:
        """Generate comprehensive dependency and structure report"""
        report_path = self.workspace_root / "runtime_intelligence" / f"dependency_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        # Analyze subcells
        subcell_stats = {}
        for record in self.tracking_data["files"].values():
            subcell = record.subcell
            if subcell not in subcell_stats:
                subcell_stats[subcell] = {"count": 0, "purposes": {}}
            subcell_stats[subcell]["count"] += 1
            
            purpose = record.purpose
            if purpose not in subcell_stats[subcell]["purposes"]:
                subcell_stats[subcell]["purposes"][purpose] = 0
            subcell_stats[subcell]["purposes"][purpose] += 1
        
        # Generate report
        report_content = f"""#  AIOS File Tracking & Dependency Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Files**: {len(self.tracking_data["files"])}
**Total Dependencies**: {sum(len(deps) for deps in self.tracking_data["dependency_graph"].values())}

##  Subcellular Organization

"""
        
        for subcell, stats in subcell_stats.items():
            report_content += f"###  {subcell}/ ({stats['count']} files)\n"
            for purpose, count in stats["purposes"].items():
                report_content += f"- **{purpose}**: {count} files\n"
            report_content += "\n"
        
        report_content += """##  Recent Changes

### Structural Changes
"""
        
        recent_structural = self.tracking_data["structural_changes"][-10:]  # Last 10 changes
        for change in recent_structural:
            # Handle both dict and dataclass objects
            if isinstance(change, dict):
                change_type = change.get('change_type', 'unknown')
                old_path = change.get('old_path', 'None')
                new_path = change.get('new_path', 'None')
                timestamp = change.get('timestamp', '')[:10]
            else:
                change_type = change.change_type
                old_path = change.old_path or 'None'
                new_path = change.new_path or 'None'
                timestamp = change.timestamp[:10]
            
            report_content += f"- **{change_type}**: {old_path} → {new_path} ({timestamp})\n"
        
        report_content += "\n### Dependency Changes\n"
        
        recent_deps = self.tracking_data["dependency_changes"][-10:]  # Last 10 changes
        for change in recent_deps:
            # Handle both dict and dataclass objects
            if isinstance(change, dict):
                change_type = change.get('change_type', 'unknown')
                source_file = change.get('source_file', 'unknown')
                target_file = change.get('target_file', 'unknown')
                timestamp = change.get('timestamp', '')[:10]
            else:
                change_type = change.change_type
                source_file = change.source_file
                target_file = change.target_file
                timestamp = change.timestamp[:10]
                
            report_content += f"- **{change_type}**: {source_file} → {target_file} ({timestamp})\n"
        
        report_content += f"""

##  Key Insights

- **Most Active Subcell**: {max(subcell_stats.items(), key=lambda x: x[1]["count"])[0]}/
- **Total Structural Changes**: {len(self.tracking_data["structural_changes"])}
- **Total Dependency Changes**: {len(self.tracking_data["dependency_changes"])}
- **Most Common Purpose**: {max([p for stats in subcell_stats.values() for p in stats["purposes"]], key=lambda x: sum(stats["purposes"].get(x, 0) for stats in subcell_stats.values()))}

---
*Generated by AIOS File Tracking System*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f" Dependency report generated: {report_path}")
        return str(report_path)


def main():
    """Main tracking system function"""
    print(" AIOS FILE TRACKING & DEPENDENCY MANAGEMENT SYSTEM")
    print("=" * 60)
    
    # Initialize tracker
    workspace_root = os.getcwd()
    tracker = FileTracker(workspace_root)
    
    # Perform full scan
    print(" Performing full workspace scan...")
    results = tracker.full_workspace_scan()
    
    # Generate report
    print(" Generating dependency report...")
    report_path = tracker.generate_dependency_report()
    
    print("\n FILE TRACKING COMPLETE!")
    print("=" * 30)
    print(f" Files tracked: {results['total_files']}")
    print(f" Dependencies mapped: {results['total_dependencies']}")
    print(f" Changes detected: {results['changed_files']}")
    print(f" Report: {Path(report_path).name}")
    
    print("\n Key Questions Now Answered:")
    print("• Where are the files at every point? ")
    print("• Which module imports which files? ") 
    print("• How do dependencies change over time? ")
    print("• What's the current subcellular structure? ")
    
    return tracker


if __name__ == "__main__":
    main()
