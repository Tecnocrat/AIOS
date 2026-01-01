#!/usr/bin/env python3
"""
AIOS Integrated Maintenance System
==================================

This script integrates and cleans up temporary maintenance utilities,
providing a permanent solution for the fractal/holographic development paradigm.
"""

import os
import shutil
from pathlib import Path


def main():
    """Main integration function."""
    workspace_root = Path(__file__).parent.parent.parent

    print(" Integrating AIOS Maintenance System...")
    print(f" Workspace: {workspace_root}")

    # Step 1: Clean up temporary scripts from root
    cleanup_temp_scripts(workspace_root)

    # Step 2: Verify maintenance module integrity
    verify_maintenance_module(workspace_root)

    # Step 3: Test the new system
    test_maintenance_system(workspace_root)

    print(" Integration complete!")
    print("\n Next Steps:")
    print("1. Use 'python ai/scripts/maintenance_cli.py' for maintenance operations")
    print("2. Update documentation to reference new maintenance workflow")
    print("3. Future utility scripts should be created in ai/src/maintenance/")


def cleanup_temp_scripts(workspace_root: Path):
    """Remove temporary scripts from workspace root."""
    print("\n🧹 Cleaning up temporary scripts...")

    temp_patterns = [
        "documentation_optimization_analysis.py",
        "ainlp_mega_consolidator.py",
        "aios_documentation_garbage_collector.py",
        "ainlp_optimization_verification.py",
        "ainlp_phase2_consolidator.py",
        "context_harmonization_demo.py",
        "aios_quantum_bootstrap.py",
        "MISSION_COMPLETE_*.md"
    ]

    removed_files = []

    for pattern in temp_patterns:
        files = list(workspace_root.glob(pattern))
        for file_path in files:
            try:
                if file_path.is_file():
                    file_path.unlink()
                    removed_files.append(str(file_path.name))
                    print(f"   Removed: {file_path.name}")
            except Exception as e:
                print(f"   Error removing {file_path}: {e}")

    if removed_files:
        print(f" Removed {len(removed_files)} temporary files")
    else:
        print(" No temporary files found")


def verify_maintenance_module(workspace_root: Path):
    """Verify the maintenance module is properly set up."""
    print("\n Verifying maintenance module...")

    maintenance_path = workspace_root / "ai" / "src" / "maintenance"
    required_files = [
        "__init__.py",
        "documentation_optimizer.py",
        "backup_consolidator.py",
        "tachyonic_archiver.py",
        "garbage_collector.py",
        "orchestrator.py"
    ]

    missing_files = []
    for file_name in required_files:
        file_path = maintenance_path / file_name
        if not file_path.exists():
            missing_files.append(file_name)
        else:
            print(f"   {file_name}")

    if missing_files:
        print(f" Missing files: {', '.join(missing_files)}")
        return False

    # Check CLI script
    cli_path = workspace_root / "ai" / "scripts" / "maintenance_cli.py"
    if cli_path.exists():
        print("   maintenance_cli.py")
    else:
        print("   maintenance_cli.py missing")
        return False

    print(" Maintenance module is complete")
    return True


def test_maintenance_system(workspace_root: Path):
    """Test the new maintenance system."""
    print("\n🧪 Testing maintenance system...")

    try:
        # Try to import the maintenance system
        import sys
        sys.path.insert(0, str(workspace_root / "ai" / "src"))

        from maintenance.orchestrator import MaintenanceOrchestrator

        # Create orchestrator instance (should not fail)
        orchestrator = MaintenanceOrchestrator(str(workspace_root))

        # Run quick analysis (non-destructive test)
        result = orchestrator.quick_analysis()

        if "documentation_analysis" in result:
            print(" Maintenance system is functional")

            # Print quick stats
            doc_analysis = result["documentation_analysis"]
            print(f"   Documentation files: {doc_analysis.get('total_files', 0)}")
            print(f"   Fragmentation: {doc_analysis.get('fragmentation_score', 1.0):.3f}")

            archive_stats = result["archive_status"]
            print(f"   Archived documents: {archive_stats.get('total_documents', 0)}")

            return True
        else:
            print(" Maintenance system test failed")
            return False

    except Exception as e:
        print(f" Maintenance system test error: {e}")
        return False


if __name__ == "__main__":
    main()
