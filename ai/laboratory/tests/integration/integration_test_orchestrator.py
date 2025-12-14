#!/usr/bin/env python3
"""
AIOS Integration Test Orchestrator
Discovers, executes, and reports on integration tests with tachyonic metadata generation

Part of AINLP Testing Infrastructure - Phase 10 Library Ingestion Validation
"""

import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import importlib.util
import traceback

# Add AIOS paths
AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT / "ai" / "src"))


class IntegrationTestOrchestrator:
    """
    Orchestrates execution of integration tests with metadata generation.
    Follows AINLP proper output management principles.
    """
    
    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or AIOS_ROOT
        self.test_dir = Path(__file__).parent
        self.metadata_dir = self.workspace_root / "tachyonic" / "archive" / "test_results" / "integration"
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        
        self.tests = self._discover_tests()
        self.results = []
    
    def _discover_tests(self) -> List[Dict[str, Any]]:
        """Discover all integration test scripts"""
        tests = []
        
        # Pattern: test_*.py files in integration directory
        for test_file in self.test_dir.glob("test_*.py"):
            if test_file.name == "test_orchestrator.py":
                continue  # Skip self
            
            tests.append({
                "name": test_file.stem,
                "file": test_file,
                "description": self._extract_description(test_file)
            })
        
        return tests
    
    def _extract_description(self, file_path: Path) -> str:
        """Extract description from test file docstring"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract first docstring
                if '"""' in content:
                    start = content.find('"""') + 3
                    end = content.find('"""', start)
                    if end > start:
                        return content[start:end].strip().split('\n')[0]
        except:
            pass
        return "No description available"
    
    async def run_test(self, test_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single integration test and capture results.
        Generates tachyonic metadata.
        """
        test_name = test_info["name"]
        test_file = test_info["file"]
        
        print(f"\n{'='*60}")
        print(f"🧪 Running: {test_name}")
        print(f"   {test_info['description']}")
        print(f"{'='*60}")
        
        start_time = datetime.now()
        result = {
            "test_name": test_name,
            "file": str(test_file.relative_to(self.workspace_root)),
            "description": test_info["description"],
            "start_time": start_time.isoformat(),
            "success": False,
            "output": "",
            "error": None,
            "duration_seconds": 0
        }
        
        try:
            # Load and execute test module
            spec = importlib.util.spec_from_file_location(test_name, test_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[test_name] = module
                spec.loader.exec_module(module)
                
                # Execute main() if exists
                if hasattr(module, 'main'):
                    # Check if async
                    if asyncio.iscoroutinefunction(module.main):
                        output = await module.main()
                    else:
                        output = module.main()
                    
                    result["success"] = True
                    result["output"] = str(output) if output else "Test completed successfully"
                    print(f"✅ {test_name}: PASSED")
                else:
                    result["error"] = "No main() function found"
                    print(f"⚠️ {test_name}: No main() function")
            else:
                result["error"] = "Could not load test module"
                print(f"❌ {test_name}: Load failed")
        
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            result["traceback"] = traceback.format_exc()
            print(f"❌ {test_name}: FAILED - {e}")
        
        end_time = datetime.now()
        result["end_time"] = end_time.isoformat()
        result["duration_seconds"] = (end_time - start_time).total_seconds()
        
        return result
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """
        Run all discovered integration tests.
        Generates comprehensive tachyonic metadata report.
        """
        print("\n" + "="*80)
        print("🔬 AIOS INTEGRATION TEST ORCHESTRATOR")
        print("="*80)
        print(f"\n📊 Discovered {len(self.tests)} integration tests")
        print(f"📁 Test directory: {self.test_dir.relative_to(self.workspace_root)}")
        print(f"📄 Metadata output: {self.metadata_dir.relative_to(self.workspace_root)}")
        
        # Run each test
        for test_info in self.tests:
            result = await self.run_test(test_info)
            self.results.append(result)
        
        # Generate summary
        summary = self._generate_summary()
        
        # Save metadata
        self._save_metadata(summary)
        
        # Display summary
        self._display_summary(summary)
        
        return summary
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate comprehensive test summary"""
        passed = sum(1 for r in self.results if r["success"])
        failed = len(self.results) - passed
        total_duration = sum(r["duration_seconds"] for r in self.results)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "workspace_root": str(self.workspace_root),
            "test_directory": str(self.test_dir.relative_to(self.workspace_root)),
            "total_tests": len(self.results),
            "passed": passed,
            "failed": failed,
            "success_rate": passed / len(self.results) if self.results else 0,
            "total_duration_seconds": total_duration,
            "results": self.results,
            "ainlp_compliance": {
                "architectural_discovery": True,
                "proper_output_management": True,
                "integration_validation": passed == len(self.results)
            }
        }
    
    def _save_metadata(self, summary: Dict[str, Any]):
        """Save test metadata to tachyonic archive"""
        # Timestamped file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        metadata_file = self.metadata_dir / f"integration_tests_{timestamp}.json"
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        # Latest pointer
        latest_file = self.metadata_dir / "integration_tests_latest.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📄 Metadata saved:")
        print(f"   {metadata_file.relative_to(self.workspace_root)}")
        print(f"   {latest_file.relative_to(self.workspace_root)}")
    
    def _display_summary(self, summary: Dict[str, Any]):
        """Display test summary to console"""
        print("\n" + "="*80)
        print("📊 INTEGRATION TEST SUMMARY")
        print("="*80)
        
        print(f"\n✅ Passed: {summary['passed']}/{summary['total_tests']}")
        print(f"❌ Failed: {summary['failed']}/{summary['total_tests']}")
        print(f"📈 Success Rate: {summary['success_rate']:.1%}")
        print(f"⏱️  Total Duration: {summary['total_duration_seconds']:.2f}s")
        
        if summary['failed'] > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.results:
                if not result["success"]:
                    print(f"   - {result['test_name']}: {result['error']}")
        
        print("\n" + "="*80)
        print("✅ INTEGRATION TEST ORCHESTRATION COMPLETE" if summary['failed'] == 0 else "⚠️ INTEGRATION TEST ORCHESTRATION COMPLETE WITH FAILURES")
        print("="*80)
    
    async def run_specific_test(self, test_name: str) -> Optional[Dict[str, Any]]:
        """Run a specific test by name"""
        for test_info in self.tests:
            if test_info["name"] == test_name:
                return await self.run_test(test_info)
        
        print(f"❌ Test not found: {test_name}")
        print(f"Available tests: {', '.join(t['name'] for t in self.tests)}")
        return None


async def main():
    """Main entry point for test orchestration"""
    orchestrator = IntegrationTestOrchestrator()
    
    # Check command line args
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        result = await orchestrator.run_specific_test(test_name)
        return result
    else:
        # Run all tests
        summary = await orchestrator.run_all_tests()
        return summary


if __name__ == "__main__":
    result = asyncio.run(main())
    
    if result:
        success_rate = result.get("success_rate", 0) if isinstance(result, dict) else (1 if result.get("success") else 0)
        sys.exit(0 if success_rate == 1.0 else 1)
    else:
        sys.exit(1)
