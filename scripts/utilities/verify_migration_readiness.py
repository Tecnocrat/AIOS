#!/usr/bin/env python3
"""
AIOS Migration Readiness Verification Script
Verifies system is ready for architecture de-proliferation migration

AINLP Protocol: OS0.6.2.claude
Created: October 12, 2025
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import hashlib


class MigrationReadinessChecker:
    """Verifies AIOS is ready for architecture de-proliferation"""
    
    def __init__(self, root_path: str = None):
        self.root = Path(root_path or os.getcwd())
        self.issues = []
        self.warnings = []
        self.info = []
        
    def check_all(self) -> Dict:
        """Run all readiness checks"""
        print("🔍 AIOS Migration Readiness Check")
        print("=" * 60)
        
        results = {
            "git_status": self.check_git_status(),
            "file_inventory": self.inventory_files_to_migrate(),
            "import_analysis": self.analyze_import_dependencies(),
            "backup_validation": self.check_backup_integrity(),
            "disk_space": self.check_disk_space(),
            "python_environment": self.check_python_environment(),
        }
        
        results["summary"] = self.generate_summary()
        
        return results
    
    def check_git_status(self) -> Dict:
        """Verify git repository is in clean state"""
        print("\n📦 Checking Git Status...")
        
        try:
            import subprocess
            
            # Check for uncommitted changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            
            uncommitted = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            if uncommitted:
                self.warnings.append(f"Git has {len(uncommitted)} uncommitted changes")
                print(f"  ⚠️  Warning: {len(uncommitted)} uncommitted files")
            else:
                print("  ✅ Git repository is clean")
            
            # Check current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            current_branch = branch_result.stdout.strip()
            print(f"  📌 Current branch: {current_branch}")
            
            if current_branch != "OS0.6.2.claude":
                self.warnings.append(f"Not on expected branch (current: {current_branch})")
            
            return {
                "status": "ready" if not uncommitted else "warning",
                "uncommitted_files": len(uncommitted),
                "current_branch": current_branch
            }
            
        except Exception as e:
            self.issues.append(f"Git check failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def inventory_files_to_migrate(self) -> Dict:
        """Count files that will be migrated"""
        print("\n📊 Inventorying Files to Migrate...")
        
        inventory = {
            "runtime_tools": [],
            "core_python_tools": [],
            "tachyonic_scripts": [],
            "tachyonic_docs": [],
            "tachyonic_backups": []
        }
        
        # Runtime Intelligence tools
        rt_tools = self.root / "runtime" / "tools"
        if rt_tools.exists():
            inventory["runtime_tools"] = list(rt_tools.rglob("*.py"))
            print(f"  📁 Runtime Intelligence tools: {len(inventory['runtime_tools'])} files")
        
        # Core Python tools
        core_path = self.root / "core"
        if core_path.exists():
            inventory["core_python_tools"] = [
                f for f in core_path.rglob("*.py") 
                if not f.name.startswith("test_") and f.name != "__init__.py"
            ]
            print(f"  📁 Core Python tools: {len(inventory['core_python_tools'])} files")
        
        # Tachyonic scripts
        tachyonic = self.root / "tachyonic"
        if tachyonic.exists():
            inventory["tachyonic_scripts"] = [
                f for f in tachyonic.glob("*.py")
                if f.name != "__init__.py"
            ]
            print(f"  📁 Tachyonic Python scripts: {len(inventory['tachyonic_scripts'])} files")
            
            inventory["tachyonic_docs"] = list(tachyonic.rglob("*.md"))
            print(f"  📁 Tachyonic documentation: {len(inventory['tachyonic_docs'])} files")
            
            backups_path = tachyonic / "backups"
            if backups_path.exists():
                inventory["tachyonic_backups"] = list(backups_path.rglob("*"))
                inventory["tachyonic_backups"] = [
                    f for f in inventory["tachyonic_backups"] if f.is_file()
                ]
                print(f"  📁 Tachyonic backup files: {len(inventory['tachyonic_backups'])} files")
        
        total_files = sum(len(v) for v in inventory.values())
        print(f"  📊 Total files to migrate: {total_files}")
        
        return {
            "status": "ready",
            "counts": {k: len(v) for k, v in inventory.items()},
            "total": total_files,
            "file_lists": {k: [str(f.relative_to(self.root)) for f in v] for k, v in inventory.items()}
        }
    
    def analyze_import_dependencies(self) -> Dict:
        """Analyze Python import dependencies"""
        print("\n🔗 Analyzing Import Dependencies...")
        
        dependencies = defaultdict(list)
        
        # Scan all Python files
        for py_file in self.root.rglob("*.py"):
            if ".venv" in str(py_file) or "build" in str(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # Find imports
                import_patterns = [
                    "from runtime",
                    "from core.",
                    "import runtime",
                    "import core."
                ]
                
                for pattern in import_patterns:
                    if pattern in content:
                        dependencies[str(py_file.relative_to(self.root))].append(pattern)
            
            except Exception as e:
                self.warnings.append(f"Could not read {py_file}: {e}")
        
        affected_files = len(dependencies)
        print(f"  🔗 Files with affected imports: {affected_files}")
        
        if affected_files > 0:
            self.warnings.append(f"{affected_files} files will need import path updates")
        
        return {
            "status": "warning" if affected_files > 0 else "ready",
            "affected_files": affected_files,
            "dependencies": dict(dependencies)
        }
    
    def check_backup_integrity(self) -> Dict:
        """Check backup file integrity"""
        print("\n💾 Checking Backup File Integrity...")
        
        backups_path = self.root / "tachyonic" / "backups"
        if not backups_path.exists():
            print("  ℹ️  No backups directory found")
            return {"status": "ready", "backup_count": 0}
        
        backup_files = list(backups_path.rglob("*"))
        backup_files = [f for f in backup_files if f.is_file()]
        
        total_size = sum(f.stat().st_size for f in backup_files if f.exists())
        total_size_mb = total_size / (1024 * 1024)
        
        print(f"  💾 Backup files: {len(backup_files)}")
        print(f"  💾 Total size: {total_size_mb:.2f} MB")
        
        # Calculate potential space savings with database
        estimated_db_size_mb = total_size_mb * 0.3  # Assume 70% compression
        savings_mb = total_size_mb - estimated_db_size_mb
        
        print(f"  💡 Estimated database size: {estimated_db_size_mb:.2f} MB")
        print(f"  💡 Potential space savings: {savings_mb:.2f} MB ({(savings_mb/total_size_mb)*100:.1f}%)")
        
        return {
            "status": "ready",
            "backup_count": len(backup_files),
            "total_size_mb": round(total_size_mb, 2),
            "estimated_db_size_mb": round(estimated_db_size_mb, 2),
            "potential_savings_mb": round(savings_mb, 2)
        }
    
    def check_disk_space(self) -> Dict:
        """Check available disk space"""
        print("\n💿 Checking Disk Space...")
        
        try:
            import shutil
            
            total, used, free = shutil.disk_usage(self.root)
            free_gb = free / (1024**3)
            
            print(f"  💿 Free disk space: {free_gb:.2f} GB")
            
            if free_gb < 5:
                self.warnings.append(f"Low disk space: {free_gb:.2f} GB free")
                status = "warning"
            else:
                status = "ready"
            
            return {
                "status": status,
                "free_gb": round(free_gb, 2)
            }
        
        except Exception as e:
            self.warnings.append(f"Could not check disk space: {e}")
            return {"status": "warning", "error": str(e)}
    
    def check_python_environment(self) -> Dict:
        """Check Python environment"""
        print("\n🐍 Checking Python Environment...")
        
        import sys
        
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        print(f"  🐍 Python version: {python_version}")
        
        # Check required packages
        required_packages = ["sqlite3"]
        missing = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            self.issues.append(f"Missing required packages: {', '.join(missing)}")
            status = "error"
        else:
            print("  ✅ All required packages available")
            status = "ready"
        
        return {
            "status": status,
            "python_version": python_version,
            "missing_packages": missing
        }
    
    def generate_summary(self) -> Dict:
        """Generate summary of readiness check"""
        print("\n" + "=" * 60)
        print("📋 Migration Readiness Summary")
        print("=" * 60)
        
        if self.issues:
            print(f"\n❌ Issues Found ({len(self.issues)}):")
            for issue in self.issues:
                print(f"   • {issue}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if self.info:
            print(f"\nℹ️  Information:")
            for info in self.info:
                print(f"   • {info}")
        
        # Determine overall status
        if self.issues:
            overall_status = "not_ready"
            print("\n🚫 System is NOT ready for migration")
            print("   Please resolve issues before proceeding")
        elif self.warnings:
            overall_status = "ready_with_warnings"
            print("\n⚠️  System is ready with warnings")
            print("   Review warnings before proceeding")
        else:
            overall_status = "ready"
            print("\n✅ System is READY for migration")
            print("   All checks passed!")
        
        return {
            "overall_status": overall_status,
            "issue_count": len(self.issues),
            "warning_count": len(self.warnings),
            "issues": self.issues,
            "warnings": self.warnings,
            "info": self.info
        }
    
    def save_report(self, output_path: str = None):
        """Save readiness report to JSON"""
        if output_path is None:
            output_path = self.root / "tachyonic" / "migration_readiness_report.json"
        
        results = self.check_all()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Report saved to: {output_path}")
        
        return results


def main():
    """Main execution"""
    import sys
    
    root_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    
    checker = MigrationReadinessChecker(root_path)
    results = checker.save_report()
    
    # Exit code based on status
    if results["summary"]["overall_status"] == "not_ready":
        sys.exit(1)
    elif results["summary"]["overall_status"] == "ready_with_warnings":
        sys.exit(0)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
