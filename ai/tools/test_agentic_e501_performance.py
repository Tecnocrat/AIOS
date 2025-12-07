#!/usr/bin/env python3
"""
Test Agentic E501 Fixer Performance on Attached File
Using AIOS Integrated Architecture
"""

import sys
import os
from pathlib import Path

# Add AIOS paths
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from ai.nucleus.communication.ai_intelligence_supercell_interface import (
    AIIntelligenceSupercellInterface,
)


def test_agentic_e501_performance():
    """Test the agentic E501 fixer on the attached holographic metadata file."""

    # Initialize the supercell interface
    interface = AIIntelligenceSupercellInterface()

    # Target file with E501 violations
    target_file = Path(__file__).parent / "aios_holographic_metadata_system.py"

    print(f"Testing agentic E501 fixer on: {target_file}")
    print("=" * 60)

    # Run the fixer in dry-run mode first to see performance
    result = interface.execute_analysis_tool(
        "agentic_e501_fixer", {"file_path": str(target_file), "dry_run": True}
    )

    print("Fixer Result:")
    print(f"- File: {result.get('file', 'N/A')}")
    print(f"- Fixes Applied: {result.get('fixes_applied', 0)}")
    print(f"- Dry Run: {result.get('dry_run', True)}")

    # Show agent usage stats
    if "stats" in result:
        stats = result["stats"]
        print("\nAgent Usage Statistics:")
        print(f"- Files Processed: {stats.get('files_processed', 0)}")
        print(f"- Lines Fixed: {stats.get('lines_fixed', 0)}")
        print("- Agents Used:")
        for agent, count in stats.get("agents_used", {}).items():
            print(f"  - {agent}: {count}")

    # Show some example fixes if available
    if "fixes" in result and result["fixes"]:
        print("\nExample Fixes:")
        for i, fix in enumerate(result["fixes"][:3]):  # Show first 3
            print(f"Line {fix['line_number']}: {fix['original_line'][:50]}...")
            print(f"  -> {fix['fixed_lines']}")

    return result


if __name__ == "__main__":
    test_agentic_e501_performance()
