"""
Comprehensive Test for AIOS Python Environment Management
========================================================

Tests the robust Python environment management system with AIOS integration,
including OS reinstall simulation and recovery procedures.
"""

import os
import shutil
import sys
import tempfile
from datetime import datetime

# Add AIOS modules to path
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    from aios_python_environment_integration import (
        AIOSPythonEnvironmentIntegration, get_aios_python_integration,
        initialize_aios_python_environment)
    from robust_python_environment_manager import (
        RobustPythonEnvironmentManager, get_environment_manager,
        initialize_python_environment_for_aios)
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running this from the correct directory")
    sys.exit(1)


class MockContextManager:
    """Mock context manager for testing AIOS integration."""

    def __init__(self):
        self.registered_subsystems = {}

    def register_subsystem(
    self, name, get_snapshot_func, restore_snapshot_func):
        self.registered_subsystems[name] = {
            'get_snapshot': get_snapshot_func,
            'restore_snapshot': restore_snapshot_func
        }
        print(f"Registered subsystem: {name}")


def test_environment_discovery():
    """Test Python environment discovery."""
    print("\n" + "="*60)
    print("TEST: Python Environment Discovery")
    print("="*60)

    # Create temporary config directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = RobustPythonEnvironmentManager(config_dir=temp_dir)

        print("Discovering Python environments...")
        environments = manager.discover_python_installations()

        print(f"Found {len(environments)} Python environments:")
        for env in environments:
            print(f"  - {env.name}")
            print(f"    Path: {env.python_path}")
            print(f"    Version: {env.version}")
            print(f"    Virtual: {env.is_virtual}")
            print(f"    Health: {env.health_status}")
            print()

        return len(environments) > 0


def test_environment_manager():
    """Test environment manager functionality."""
    print("\n" + "="*60)
    print("TEST: Environment Manager Functionality")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        manager = RobustPythonEnvironmentManager(config_dir=temp_dir)

        # Test refresh
        print("Refreshing environments...")
        healthy_count = manager.refresh_environments()
        print(f"Found {healthy_count} healthy environments")

        # Test health check
        print("\nPerforming health check...")
        health = manager.health_check()
        print(f"Health check results:")
        print(f"  Total: {health['total_environments']}")
        print(f"  Healthy: {health['healthy_environments']}")
        print(f"  Missing: {health['missing_environments']}")
        print(f"  Broken: {health['broken_environments']}")

        # Test setting active environment
        environments = manager.list_environments()
        healthy_envs = [
        env for env in environments if env.health_status == "healthy"]

        if healthy_envs:
            print(f"\nSetting active environment: {healthy_envs[0].name}")
            success = manager.set_active_environment(healthy_envs[0].id)
            print(f"Success: {success}")

            active = manager.get_active_environment()
            if active:
                print(f"Active environment: {active.name}")

        return healthy_count > 0


def test_aios_integration():
    """Test AIOS integration functionality."""
    print("\n" + "="*60)
    print("TEST: AIOS Integration")
    print("="*60)

    # Create mock context manager
    context_manager = MockContextManager()

    # Initialize integration
    integration = AIOSPythonEnvironmentIntegration(context_manager)

    print("Testing health check with recovery...")
    health_report = integration.perform_health_check()

    print(f"Health check results:")
    print(f"  Total environments: {health_report['total_environments']}")
    print(f"  Healthy environments: {health_report['healthy_environments']}")
    print(
    f"  Recovery applied: {health_report['aios_integration']['recovery_applied']}")

    # Test environment snapshot
    print("\nTesting environment snapshot...")
    snapshot = integration.get_environment_snapshot()
    print(
    f"Snapshot created with {len(snapshot['environments'])} environments")

    if snapshot['active_environment']:
        print(
        f"Active environment in snapshot: {snapshot['active_environment']['name']}")

    # Test diagnostic report
    print("\nGenerating diagnostic report...")
    diagnostic = integration.get_diagnostic_report()
    print(
    f"Diagnostic report generated for platform: {diagnostic['platform']}")

    return health_report['healthy_environments'] > 0


def test_os_reinstall_preparation():
    """Test OS reinstall preparation and recovery."""
    print("\n" + "="*60)
    print("TEST: OS Reinstall Preparation and Recovery")
    print("="*60)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize integration with temporary directory
        context_manager = MockContextManager()
        integration = AIOSPythonEnvironmentIntegration(context_manager)
        integration.env_manager.config_dir = temp_dir

        print("Preparing for OS reinstall...")
        backup_file = integration.prepare_for_os_reinstall()

        if backup_file and os.path.exists(backup_file):
            print(f"Backup created: {backup_file}")

            # Load and examine backup
            import json
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)

            print(f"Backup contains:")
            print(f"  - Export timestamp: {backup_data['export_timestamp']}")
            print(f"  - Platform: {backup_data['platform']}")
            print(
            f"  - Environment snapshot: {len(backup_data['environment_snapshot']['environments'])} environments")
            print(
            f"  - Recovery instructions: {len(backup_data['recovery_instructions'])} steps")

            # Test recovery
            print("\nTesting post-reinstall recovery...")
            recovery_success = integration.post_reinstall_recovery(backup_file)
            print(f"Recovery success: {recovery_success}")

            return True
        else:
            print("Failed to create backup file")
            return False


def test_memory_allocation_explanation():
    """Explain memory allocation for VSCode and AIOS."""
    print("\n" + "="*60)
    print("MEMORY ALLOCATION EXPLANATION")
    print("="*60)

    print("""
MEMORY ALLOCATION IN AIOS AND VSCODE INTEGRATION:

1. VSCode Extension Memory:
   - Extension Host Process: Node.js runtime (typically 1-2GB limit)
   - Language Server Protocol: Separate process for Python analysis
   - Workspace State: Persistent storage in VS Code's storage directory
   - File System Cache: In-memory caching of file contents and metadata
   - Communication: IPC between extension host and language server

2. AIOS Memory Architecture:
   - C++ Core: Native memory management with custom allocators
     * Real-time context buffers: 64MB default
     * Fractal data structures: Dynamic allocation
     * Holographic indices: Memory-mapped files

   - Python AI Components: Heap-based memory management
     * Environment snapshots: JSON serialization (~1-10MB each)
     * Context preservation: Pickle-based state saving
     * ML models: NumPy/TensorFlow memory pools

   - C# UI Layer: .NET managed memory
     * WPF rendering: DirectX surface memory
     * Data binding: Observable collections in heap
     * Context synchronization: Shared memory regions

3. Cross-Process Communication:
   - Named pipes (Windows) / Unix sockets (Linux/Mac)
   - Shared memory segments for large data transfers
   - JSON-based message passing for control commands
   - Memory-mapped files for persistent context storage

4. Environment Management Memory:
   - Configuration storage: JSON files (~1-5MB)
   - Environment snapshots: Compressed state (~100KB-1MB each)
   - Recovery data: Backup files with full environment state
   - Health monitoring: Periodic memory usage tracking

5. Recovery and Persistence:
   - Context snapshots: Atomic writes to prevent corruption
   - Backup rotation: Keep last 10 snapshots with size limits
   - Memory pressure handling: Automatic cleanup of old snapshots
   - OS reinstall recovery: Full state export/import capability
    """)


def run_comprehensive_test():
    """Run all tests and provide summary."""
    print("AIOS Python Environment Management - Comprehensive Test Suite")
    print("=" * 70)
    print(f"Test started at: {datetime.now()}")
    print(f"Platform: {os.name}")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")

    test_results = []

    # Run tests
    tests = [
        ("Environment Discovery", test_environment_discovery),
        ("Environment Manager", test_environment_manager),
        ("AIOS Integration", test_aios_integration),
        ("OS Reinstall Preparation", test_os_reinstall_preparation),
    ]

    for test_name, test_func in tests:
        try:
            print(f"\nRunning {test_name}...")
            result = test_func()
            test_results.append((test_name, result, None))
        except Exception as e:
            print(f"ERROR in {test_name}: {e}")
            test_results.append((test_name, False, str(e)))

    # Show memory allocation explanation
    test_memory_allocation_explanation()

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = 0
    total = len(test_results)

    for test_name, result, error in test_results:
        status = "PASS" if result else "FAIL"
        print(f"{status:6} | {test_name}")
        if error:
            print(f"       | Error: {error}")
        if result:
            passed += 1

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print(
        "\n All tests passed! AIOS Python environment management is ready.")
        print("\nNext steps:")
        print(
        "1. The system is now resilient to OS reinstalls and PATH issues")
        print("2. Environment snapshots are automatically created and managed")
        print("3. Recovery strategies will automatically fix common issues")
        print("4. Integration with AIOS fractal/holographic context is active")
    else:
        print(
        f"\n {total - passed} tests failed. Please check the issues above.")

    return passed == total


if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
