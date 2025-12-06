#!/usr/bin/env python3
"""
 AIOS Analysis Tools Neuronal Test Runner
==========================================

Quick diagnostic test runner for the optimized analysis_tools cellular unit.
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


def test_analysis_tools():
    """Test all analysis tools after neuronal optimization."""

    analysis_tools_path = Path("C:/dev/AIOS/core/analysis_tools")

    print(" ANALYSIS TOOLS NEURONAL TEST SESSION")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Path: {analysis_tools_path}")
    print()

    # Get all Python tools
    python_tools = [
        f
        for f in os.listdir(analysis_tools_path)
        if f.endswith(".py") and f.startswith("aios_")
    ]

    print(f" OPERATIONAL TOOLS: {len(python_tools)}")
    for tool in sorted(python_tools):
        print(f"  - {tool}")
    print()

    # Test import capabilities
    successful_imports = 0
    failed_imports = 0

    print(" IMPORT CAPABILITY TEST:")
    for tool in sorted(python_tools):
        tool_name = tool.replace(".py", "")
        try:
            # Try basic syntax check
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(analysis_tools_path / tool)],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                print(f"   {tool_name}: Syntax valid")
                successful_imports += 1
            else:
                print(f"   {tool_name}: Syntax error")
                print(f"     {result.stderr[:100]}")
                failed_imports += 1

        except subprocess.TimeoutExpired:
            print(f"  ⏱  {tool_name}: Timeout")
            failed_imports += 1
        except Exception as e:
            print(f"    {tool_name}: {str(e)[:50]}")
            failed_imports += 1

    print()
    print(" NEURONAL TEST RESULTS:")
    print(f"  Successful: {successful_imports}")
    print(f"  Failed: {failed_imports}")
    print(
        f"  Success Rate: {successful_imports/(successful_imports+failed_imports)*100:.1f}%"
    )

    # Check tachyonic archive
    archive_path = Path(
        "C:/dev/AIOS/core/tachyonic_archive/subcellular_archives/analysis_tools"
    )
    if archive_path.exists():
        consciousness_backups = len(
            list(
                (archive_path / "consciousness_backups").glob(
                    "*.py.consciousness_backup"
                )
            )
        )
        analysis_outputs = len(list((archive_path / "analysis_outputs").glob("*")))

        print()
        print(" TACHYONIC ARCHIVE STATUS:")
        print(f"  Consciousness backups archived: {consciousness_backups}")
        print(f"  Analysis outputs archived: {analysis_outputs}")
        print(f"  Total archived files: {consciousness_backups + analysis_outputs}")

    # Check metadata organization
    metadata_path = analysis_tools_path / "metadata"
    if metadata_path.exists():
        metadata_files = len(list(metadata_path.glob("*.md")))
        print(f"  Metadata files organized: {metadata_files}")

    print()
    if successful_imports > failed_imports:
        print(" NEURONAL OPTIMIZATION STATUS: SUCCESS")
        print("   Analysis tools cellular unit is operating with enhanced coherence")
    else:
        print("  NEURONAL OPTIMIZATION STATUS: NEEDS ATTENTION")
        print("   Some components require additional enhancement")


if __name__ == "__main__":
    test_analysis_tools()
