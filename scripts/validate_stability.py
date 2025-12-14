#!/usr/bin/env python3
"""
AIOS Stability Protocol Validator
Validates that the stability protocol is properly implemented
"""

import sys
import json
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Any


def load_jsonc(file_path: Path) -> Dict[str, Any]:
    """Load JSONC (JSON with comments) file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove single-line comments (// ...)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Remove multi-line comments (/* ... */)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    return json.loads(content)


def validate_stability_protocol() -> bool:
    """Validate AIOS stability protocol implementation"""
    workspace_root = Path(__file__).parent.parent
    issues: List[str] = []

    print("🔍 AIOS Stability Protocol Validation")
    print("=" * 50)

    # 1. Check Python environment pinning
    print("\n1. Python Environment Pinning:")
    workspace_file = workspace_root / "AIOS.code-workspace"
    workspace_data: Dict[str, Any] = {}

    if workspace_file.exists():
        workspace_data = load_jsonc(workspace_file)

        python_path = workspace_data.get("settings", {}).get(
            "python.defaultInterpreterPath")
        if python_path == "./aios_env/Scripts/python.exe":
            print("✅ Python pinned to aios_env")
        else:
            print(f"❌ Python not properly pinned: {python_path}")
            issues.append("Python environment not pinned to aios_env")

    # 2. Check formatter suppression
    print("\n2. Formatter Suppression:")
    format_on_save = workspace_data.get("settings", {}).get(
        "editor.formatOnSave")
    python_formatting = workspace_data.get("settings", {}).get(
        "python.formatting.provider")

    if format_on_save is False:
        print("✅ Format on save disabled")
    else:
        print(f"❌ Format on save not disabled: {format_on_save}")
        issues.append("Format on save not disabled")

    if python_formatting == "none":
        print("✅ Python formatting provider set to none")
    else:
        print(f"❌ Python formatting not disabled: {python_formatting}")
        issues.append("Python formatting not disabled")

    # 3. Check auto-restore prevention
    print("\n3. Auto-restore Prevention:")
    git_autofetch = workspace_data.get("settings", {}).get("git.autofetch")
    hot_exit = workspace_data.get("settings", {}).get("files.hotExit")
    restore_windows = workspace_data.get("settings", {}).get(
        "window.restoreWindows")

    if git_autofetch is False:
        print("✅ Git auto-fetch disabled")
    else:
        print(f"❌ Git auto-fetch not disabled: {git_autofetch}")
        issues.append("Git auto-fetch not disabled")

    if hot_exit == "off":
        print("✅ Hot exit disabled")
    else:
        print(f"❌ Hot exit not disabled: {hot_exit}")
        issues.append("Hot exit not disabled")

    if restore_windows == "none":
        print("✅ Window restore disabled")
    else:
        print(f"❌ Window restore not disabled: {restore_windows}")
        issues.append("Window restore not disabled")

    # 4. Check aios_env existence and validity
    print("\n4. AIOS Environment Validation:")
    aios_env_path = workspace_root / "aios_env"
    python_exe = aios_env_path / "Scripts" / "python.exe"

    if aios_env_path.exists():
        print("✅ aios_env directory exists")
        if python_exe.exists():
            print("✅ Python executable found in aios_env")
            try:
                result = subprocess.run(
                    [str(python_exe), "--version"],
                    capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    print(f"✅ Python executable functional: {version}")
                else:
                    error = result.stderr
                    print(f"❌ Python executable not functional: {error}")
                    issues.append("Python executable not functional")
            except Exception as e:
                print(f"❌ Error testing Python executable: {e}")
                issues.append(f"Error testing Python executable: {e}")
        else:
            print("❌ Python executable not found in aios_env")
            issues.append("Python executable not found in aios_env")
    else:
        print("❌ aios_env directory does not exist")
        issues.append("aios_env directory does not exist")

    # 5. Summary
    print("\n" + "=" * 50)
    if issues:
        print(f"❌ Stability Protocol Issues Found: {len(issues)}")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ Stability Protocol Fully Implemented")
        print("🎉 AIOS workspace is stable and ready for development")
        return True


if __name__ == "__main__":
    success = validate_stability_protocol()
    sys.exit(0 if success else 1)
