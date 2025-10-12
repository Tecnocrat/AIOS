#!/usr/bin/env python3
"""
AIOS Development Environment Setup
Phase 9.2: System Optimization and Debugging Pass

Sets up Python environment for AIOS development:
- Adds AIOS workspace paths to PYTHONPATH
- Validates environment configuration
- Provides development environment activation

AINLP Integration: runtime_intelligence/tools/aios_dev_setup.py
Purpose: Ensure consistent Python environment for AIOS development
"""

import os
import sys
from pathlib import Path


def setup_aios_environment():
    """
    Set up AIOS development environment paths and configuration
    """
    workspace_root = Path(__file__).parent.parent.parent

    # AIOS paths to add to Python path
    aios_paths = [
        str(workspace_root),                    # Main workspace
        str(workspace_root / "ai"),            # AI Intelligence Layer
        str(workspace_root / "runtime_intelligence"),  # Runtime Intelligence
        str(workspace_root / "core"),          # Core Engine
        str(workspace_root / "interface"),     # Interface Layer
    ]

    # Add paths to sys.path if not already present
    for path in aios_paths:
        if path not in sys.path:
            sys.path.insert(0, path)

    # Set environment variables for development
    existing_pythonpath = os.environ.get('PYTHONPATH', '')
    if existing_pythonpath:
        all_paths = aios_paths + existing_pythonpath.split(os.pathsep)
    else:
        all_paths = aios_paths

    os.environ['PYTHONPATH'] = os.pathsep.join(all_paths)
    os.environ.setdefault('AIOS_WORKSPACE_ROOT', str(workspace_root))

    return {
        'workspace_root': str(workspace_root),
        'paths_added': aios_paths,
        'pythonpath_set': os.environ.get('PYTHONPATH', ''),
        'success': True
    }


def validate_environment():
    """
    Validate that the environment is properly configured
    """
    issues = []

    # Check if AIOS paths are in sys.path
    workspace_root = Path(__file__).parent.parent.parent
    required_paths = [
        str(workspace_root),
        str(workspace_root / "ai"),
        str(workspace_root / "runtime_intelligence"),
    ]

    for path in required_paths:
        if path not in sys.path:
            issues.append(f"Missing path in sys.path: {path}")

    # Check if key modules can be imported
    test_imports = [
        ('ai.nucleus.interface_bridge', 'AIOSInterfaceBridge'),
        ('runtime_intelligence.tools.biological_architecture_monitor',
         'AIOSArchitectureMonitor'),
    ]

    for module_name, class_name in test_imports:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            issues.append(f"Import failed: {module_name}.{class_name} - {e}")

    return {
        'issues': issues,
        'valid': len(issues) == 0
    }


def main():
    """Main setup execution"""
    print("🔧 AIOS Development Environment Setup")
    print("=" * 40)

    # Setup environment
    setup_result = setup_aios_environment()
    print(f"✅ Workspace root: {setup_result['workspace_root']}")
    print(f"✅ Added {len(setup_result['paths_added'])} paths to sys.path")

    # Validate environment
    validation = validate_environment()

    if validation['valid']:
        print("✅ Environment validation: PASSED")
        print("\n🎉 AIOS development environment is ready!")
    else:
        print("❌ Environment validation: FAILED")
        print("\nIssues found:")
        for issue in validation['issues']:
            print(f"  • {issue}")

        print("\n💡 Try running this script again or check your "
              "Python environment.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())