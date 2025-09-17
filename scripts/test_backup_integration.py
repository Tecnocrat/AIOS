#!/usr/bin/env python3
"""
AIOS Backup Integration Test
Tests the integration of backup management tools within AIOS execution environment.
"""

import subprocess
import sys
from pathlib import Path

# Resolve repository root
ROOT = Path(__file__).resolve().parents[1]

def test_backup_manager_script():
    """Test backup manager PowerShell script accessibility."""
    backup_script = ROOT / "scripts" / "backup_manager.ps1"
    
    print("Testing backup manager script...")
    print(f"Script path: {backup_script}")
    
    if not backup_script.exists():
        print("❌ FAIL: Backup manager script not found")
        return False
    
    try:
        # Test status command (read-only, safe to run)
        result = subprocess.run(
            ["pwsh", "-NoLogo", "-NoProfile", "-File", str(backup_script), "-Action", "status"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            timeout=30
        )
        
        if result.returncode == 0:
            print("✓ PASS: Backup manager script executes successfully")
            print("Output preview:")
            # Show first few lines of output
            lines = result.stdout.strip().split('\n')[:5]
            for line in lines:
                print(f"  {line}")
            return True
        else:
            print(f"❌ FAIL: Backup manager script failed with exit code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: Error executing backup manager script: {e}")
        return False

def test_admin_tool_syntax():
    """Test that admin tool has valid Python syntax."""
    admin_tool = ROOT / "runtime_intelligence" / "tools" / "aios_admin.py"
    
    print("\nTesting admin tool syntax...")
    print(f"Admin tool path: {admin_tool}")
    
    if not admin_tool.exists():
        print("❌ FAIL: Admin tool not found")
        return False
    
    try:
        # Test that the admin tool has valid syntax
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(admin_tool)],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            timeout=10
        )
        
        if result.returncode == 0:
            print("✓ PASS: Admin tool has valid Python syntax")
            
            # Also test if backup functions are present
            content = admin_tool.read_text(encoding='utf-8')
            backup_functions = ["run_backup_manager", "backup_management_menu"]
            
            found_functions = []
            for func in backup_functions:
                if f"def {func}" in content:
                    found_functions.append(func)
            
            if len(found_functions) == len(backup_functions):
                print(f"✓ PASS: All backup functions found: {', '.join(found_functions)}")
                return True
            else:
                missing = set(backup_functions) - set(found_functions)
                print(f"❌ FAIL: Missing backup functions: {', '.join(missing)}")
                return False
        else:
            print(f"❌ FAIL: Admin tool syntax check failed with exit code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: Error testing admin tool syntax: {e}")
        return False

def test_vscode_tasks():
    """Test that VS Code tasks are properly configured."""
    tasks_file = ROOT / ".vscode" / "tasks.json"
    
    print("\nTesting VS Code task configuration...")
    print(f"Tasks file path: {tasks_file}")
    
    if not tasks_file.exists():
        print("❌ FAIL: VS Code tasks.json not found")
        return False
    
    try:
        content = tasks_file.read_text(encoding='utf-8')
        backup_tasks = ["backup-status", "backup-create", "backup-consolidate", "backup-cleanup"]
        
        found_tasks = []
        for task in backup_tasks:
            if f'"label": "{task}"' in content:
                found_tasks.append(task)
        
        if len(found_tasks) == len(backup_tasks):
            print("✓ PASS: All backup tasks found in VS Code configuration")
            print(f"  Tasks found: {', '.join(found_tasks)}")
            return True
        else:
            missing = set(backup_tasks) - set(found_tasks)
            print(f"❌ FAIL: Missing backup tasks: {', '.join(missing)}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: Error reading VS Code tasks file: {e}")
        return False

def main():
    """Run all integration tests."""
    print("AIOS Backup Integration Test Suite")
    print("=" * 40)
    
    tests = [
        test_backup_manager_script,
        test_admin_tool_syntax,
        test_vscode_tasks
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{'='*40}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ ALL TESTS PASSED - Backup integration successful!")
        return 0
    else:
        print("❌ SOME TESTS FAILED - Review integration issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())