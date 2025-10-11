#!/usr/bin/env python3
"""
AIOS Integration Test Runner - Interface Bridge Tool
Exposes integration tests via HTTP API for AIOS component access

Part of AINLP Runtime Intelligence - Test Infrastructure
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Add AIOS paths
AIOS_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT / "ai" / "src"))
sys.path.insert(0, str(AIOS_ROOT / "ai" / "tests" / "integration"))

try:
    from integration_test_orchestrator import IntegrationTestOrchestrator
except ImportError:
    print("Error: Could not import IntegrationTestOrchestrator")
    print("Ensure ai/tests/integration/integration_test_orchestrator.py exists")
    sys.exit(1)


class IntegrationTestRunner:
    """
    Interface Bridge Tool: Run AIOS integration tests on demand
    
    Enables AIOS components to discover and execute integration tests
    via HTTP API with full metadata generation.
    """
    
    # Interface Bridge tool metadata
    name = "integration_test_runner"
    description = "Run AIOS integration tests with metadata generation"
    version = "1.0.0"
    
    def __init__(self):
        self.orchestrator = IntegrationTestOrchestrator()
        self.last_run = None
    
    async def run(self, test_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Run integration tests with metadata generation.
        
        Args:
            test_name: Specific test to run, or None for all tests
        
        Returns:
            Test results with tachyonic metadata
        """
        if test_name:
            # Run specific test
            result = await self.orchestrator.run_specific_test(test_name)
            if result:
                self.last_run = {
                    "timestamp": datetime.now().isoformat(),
                    "test_name": test_name,
                    "result": result
                }
                return result
            else:
                return {
                    "error": f"Test not found: {test_name}",
                    "available_tests": self.get_available_tests()
                }
        else:
            # Run all tests
            summary = await self.orchestrator.run_all_tests()
            self.last_run = {
                "timestamp": datetime.now().isoformat(),
                "test_name": "all",
                "summary": summary
            }
            return summary
    
    def get_available_tests(self) -> List[str]:
        """Get list of available integration tests"""
        return [test["name"] for test in self.orchestrator.tests]
    
    def get_test_info(self) -> List[Dict[str, str]]:
        """Get detailed info about available tests"""
        return [{
            "name": test["name"],
            "description": test["description"],
            "file": str(test["file"].name)
        } for test in self.orchestrator.tests]
    
    def get_last_run(self) -> Optional[Dict[str, Any]]:
        """Get results of last test run"""
        return self.last_run
    
    def get_metadata_location(self) -> str:
        """Get location of test metadata files"""
        return str(self.orchestrator.metadata_dir.relative_to(
            self.orchestrator.workspace_root
        ))
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of test infrastructure"""
        return {
            "status": "healthy",
            "discovered_tests": len(self.orchestrator.tests),
            "test_directory": str(self.orchestrator.test_dir.relative_to(
                self.orchestrator.workspace_root
            )),
            "metadata_directory": self.get_metadata_location(),
            "tests_available": self.get_available_tests()
        }


async def main():
    """CLI entry point for test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AIOS Integration Test Runner"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="run",
        choices=["run", "list", "info", "health"],
        help="Command to execute"
    )
    parser.add_argument(
        "--test",
        "-t",
        help="Specific test to run (for 'run' command)"
    )
    
    args = parser.parse_args()
    
    runner = IntegrationTestRunner()
    
    if args.command == "run":
        # Run tests
        result = await runner.run(args.test)
        print("\n" + "="*80)
        print("TEST EXECUTION RESULT")
        print("="*80)
        import json
        print(json.dumps(result, indent=2))
        return result
    
    elif args.command == "list":
        # List available tests
        tests = runner.get_available_tests()
        print("\n" + "="*80)
        print("AVAILABLE INTEGRATION TESTS")
        print("="*80)
        for test_name in tests:
            print(f"  - {test_name}")
        print(f"\nTotal: {len(tests)} tests")
        return tests
    
    elif args.command == "info":
        # Get detailed test info
        info = runner.get_test_info()
        print("\n" + "="*80)
        print("INTEGRATION TEST INFORMATION")
        print("="*80)
        for test in info:
            print(f"\n📝 {test['name']}")
            print(f"   File: {test['file']}")
            print(f"   Description: {test['description']}")
        return info
    
    elif args.command == "health":
        # Health check
        health = runner.health_check()
        print("\n" + "="*80)
        print("TEST INFRASTRUCTURE HEALTH CHECK")
        print("="*80)
        import json
        print(json.dumps(health, indent=2))
        return health


if __name__ == "__main__":
    result = asyncio.run(main())
    
    # Exit with appropriate code
    if isinstance(result, dict):
        if result.get("success_rate") == 1.0:
            sys.exit(0)
        elif "error" in result:
            sys.exit(1)
        else:
            sys.exit(0 if result.get("passed") == result.get("total_tests") else 1)
    else:
        sys.exit(0)
