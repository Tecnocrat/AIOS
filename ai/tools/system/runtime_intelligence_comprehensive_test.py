#!/usr/bin/env python3
"""
AIOS Runtime Intelligence Comprehensive Testing Suite
=====================================================

Systematic testing of all runtime intelligence tools to:
1. Validate functionality and integration
2. Document tool capabilities and connections
3. Identify redundancies and optimization opportunities
4. Ensure all tools are accessible through Interface Bridge

AINLP Protocol: Architectural Discovery First → Enhancement over Creation
"""

import json
import subprocess
import sys
import time
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests
import importlib.util

class RuntimeIntelligenceTester:
    """Comprehensive tester for AIOS runtime intelligence ecosystem"""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.results = {
            "timestamp": datetime.now().isoformat(),
<<<<<<< HEAD
            "phase": "9.2.5_runtime_intelligence_validation",
=======
            "phase": "9.2.5_runtime_validation",
>>>>>>> origin/OS0.6.2.grok
            "tools_tested": [],
            "integration_status": {},
            "redundancy_analysis": {},
            "optimization_opportunities": [],
            "interface_bridge_coverage": {},
            "execution_summary": {}
        }
        self.interface_bridge_url = "http://localhost:8000"

    def test_interface_bridge_connectivity(self) -> bool:
        """Test Interface Bridge connectivity and tool discovery"""
        try:
            response = requests.get(f"{self.interface_bridge_url}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                self.results["interface_bridge_status"] = {
                    "connected": True,
                    "health": health_data,
                    "tools_discovered": health_data.get("tools_discovered", 0)
                }
                return True
            else:
                self.results["interface_bridge_status"] = {
                    "connected": False,
                    "error": f"HTTP {response.status_code}"
                }
                return False
        except Exception as e:
            self.results["interface_bridge_status"] = {
                "connected": False,
                "error": str(e)
            }
            return False

    def get_interface_bridge_tools(self) -> List[Dict[str, Any]]:
        """Get all tools available through Interface Bridge"""
        try:
            response = requests.get(f"{self.interface_bridge_url}/tools", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("tools", [])
            return []
        except Exception as e:
            print(f"Error getting Interface Bridge tools: {e}")
            return []

    def test_tool_execution(self, tool_path: Path, tool_name: str) -> Dict[str, Any]:
        """Test individual tool execution and capture results"""
        result = {
            "tool_name": tool_name,
            "tool_path": str(tool_path),
            "execution_success": False,
            "execution_time": None,
            "output": None,
            "error": None,
            "capabilities_detected": [],
            "integration_points": [],
            "dependencies": []
        }

        start_time = time.time()

        try:
            # Test basic import first
            if tool_name.endswith('.py'):
                module_name = tool_name[:-3]  # Remove .py extension
                try:
                    # Try to import the module
                    spec = importlib.util.spec_from_file_location(module_name, tool_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        result["import_success"] = True

                        # Analyze module for capabilities
                        if hasattr(module, '__doc__') and module.__doc__:
                            result["documentation"] = module.__doc__.strip()

                        # Check for main functions/classes
                        if hasattr(module, 'main'):
                            result["capabilities_detected"].append("has_main_function")
                        if hasattr(module, 'run'):
                            result["capabilities_detected"].append("has_run_function")

                        # Check for classes
                        classes = [name for name in dir(module) if isinstance(getattr(module, name), type)]
                        if classes:
                            result["capabilities_detected"].append(f"classes: {classes}")

                    else:
                        result["import_success"] = False
                        result["import_error"] = "Could not create module spec"

                except Exception as e:
                    result["import_success"] = False
                    result["import_error"] = str(e)

            # Test command-line execution
            try:
                cmd = [sys.executable, str(tool_path), "--help"]
                process = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=self.workspace_root
                )

                if process.returncode == 0:
                    result["cli_success"] = True
                    result["cli_help_output"] = process.stdout[:1000]  # Truncate long output
                else:
                    result["cli_success"] = False
                    result["cli_error"] = process.stderr[:500]

            except subprocess.TimeoutExpired:
                result["cli_success"] = False
                result["cli_error"] = "Command timed out"
            except Exception as e:
                result["cli_success"] = False
                result["cli_error"] = str(e)

            result["execution_success"] = result.get("import_success", False) or result.get("cli_success", False)

        except Exception as e:
            result["error"] = str(e)

        result["execution_time"] = time.time() - start_time
        return result

    def analyze_tool_capabilities(self, tool_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze tool capabilities and identify patterns/redundancies"""
        analysis = {
            "capability_clusters": {},
            "redundant_functionality": [],
            "unique_capabilities": [],
            "integration_opportunities": [],
            "optimization_candidates": []
        }

        # Group tools by capabilities
        for tool in tool_results:
            capabilities = tool.get("capabilities_detected", [])
            for cap in capabilities:
                if cap not in analysis["capability_clusters"]:
                    analysis["capability_clusters"][cap] = []
                analysis["capability_clusters"][cap].append(tool["tool_name"])

        # Identify redundant functionality
        for cap, tools in analysis["capability_clusters"].items():
            if len(tools) > 1:
                analysis["redundant_functionality"].append({
                    "capability": cap,
                    "tools": tools,
                    "recommendation": f"Consider consolidating {cap} functionality"
                })

        return analysis

    def check_interface_bridge_coverage(self, tool_results: List[Dict[str, Any]], bridge_tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Check which tools are accessible through Interface Bridge"""
        coverage = {
            "bridge_tools": [t["name"] for t in bridge_tools],
            "local_tools": [t["tool_name"] for t in tool_results],
            "covered_tools": [],
            "uncovered_tools": [],
            "coverage_percentage": 0.0
        }

        bridge_tool_names = set(coverage["bridge_tools"])
        local_tool_names = set(coverage["local_tools"])

        coverage["covered_tools"] = list(bridge_tool_names & local_tool_names)
        coverage["uncovered_tools"] = list(local_tool_names - bridge_tool_names)

        if local_tool_names:
            coverage["coverage_percentage"] = (len(coverage["covered_tools"]) / len(local_tool_names)) * 100

        return coverage

    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive testing of all runtime intelligence tools"""
        print("🔍 AIOS Runtime Intelligence Comprehensive Testing")
        print("=" * 60)

        # Test Interface Bridge connectivity
        print("Testing Interface Bridge connectivity...")
        bridge_connected = self.test_interface_bridge_connectivity()
        if not bridge_connected:
            print("❌ Interface Bridge not available - some tests may be limited")
        else:
            print("✅ Interface Bridge connected")

        # Get Interface Bridge tools
        bridge_tools = self.get_interface_bridge_tools()
        print(f"📋 Interface Bridge reports {len(bridge_tools)} tools available")

<<<<<<< HEAD
        # Find all Python files in runtime_intelligence
        runtime_intelligence_dir = self.workspace_root / "runtime_intelligence"
        
        print(f"Searching in directory: {runtime_intelligence_dir}")
        print(f"Directory exists: {runtime_intelligence_dir.exists()}")
        
        # Check if we're in the right place
        if not runtime_intelligence_dir.exists():
            print(f"Directory not found, trying parent: {self.workspace_root}")
            runtime_intelligence_dir = self.workspace_root
        
        python_files = []
        
        for root, dirs, files in os.walk(runtime_intelligence_dir):
=======
        # Find all Python files in runtime
        runtime_dir = self.workspace_root / "runtime"
        
        print(f"Searching in directory: {runtime_dir}")
        print(f"Directory exists: {runtime_dir.exists()}")
        
        # Check if we're in the right place
        if not runtime_dir.exists():
            print(f"Directory not found, trying parent: {self.workspace_root}")
            runtime_dir = self.workspace_root
        
        python_files = []
        
        for root, dirs, files in os.walk(runtime_dir):
>>>>>>> origin/OS0.6.2.grok
            print(f"Walking: {root} - {len(files)} files")
            for file in files:
                if file.endswith('.py'):
                    full_path = Path(root) / file
                    python_files.append(full_path)
                    print(f"Found Python file: {full_path}")

<<<<<<< HEAD
        print(f"🔧 Found {len(python_files)} Python files in runtime_intelligence")
=======
        print(f"🔧 Found {len(python_files)} Python files in runtime")
>>>>>>> origin/OS0.6.2.grok

        # Test each tool
        tool_results = []
        for i, py_file in enumerate(python_files, 1):
            tool_name = py_file.name
            print(f"Testing {i}/{len(python_files)}: {tool_name}")

            result = self.test_tool_execution(py_file, tool_name)
            tool_results.append(result)

            status = "✅" if result["execution_success"] else "❌"
            print(f"  {status} {tool_name}")

        # Analyze results
        print("\n📊 Analyzing results...")

        # Capability analysis
        capability_analysis = self.analyze_tool_capabilities(tool_results)
        self.results["capability_analysis"] = capability_analysis

        # Interface Bridge coverage
        coverage_analysis = self.check_interface_bridge_coverage(tool_results, bridge_tools)
        self.results["interface_bridge_coverage"] = coverage_analysis

        # Generate optimization recommendations
        self.generate_optimization_recommendations(tool_results, capability_analysis, coverage_analysis)

        self.results["tools_tested"] = tool_results
        self.results["execution_summary"] = {
            "total_tools": len(tool_results),
            "successful_tools": len([t for t in tool_results if t["execution_success"]]),
            "failed_tools": len([t for t in tool_results if not t["execution_success"]]),
            "bridge_coverage": coverage_analysis["coverage_percentage"],
            "redundancy_opportunities": len(capability_analysis["redundant_functionality"])
        }

        return self.results

    def generate_optimization_recommendations(self, tool_results: List[Dict[str, Any]],
                                            capability_analysis: Dict[str, Any],
                                            coverage_analysis: Dict[str, Any]):
        """Generate optimization recommendations based on analysis"""

        recommendations = []

        # Bridge coverage recommendations
        if coverage_analysis["coverage_percentage"] < 80:
            recommendations.append({
                "type": "interface_bridge_coverage",
                "priority": "high",
                "description": f"Only {coverage_analysis['coverage_percentage']:.1f}% of tools are accessible via Interface Bridge",
                "action": "Add missing tools to Interface Bridge discovery",
                "affected_tools": coverage_analysis["uncovered_tools"]
            })

        # Redundancy recommendations
        for redundant in capability_analysis["redundant_functionality"]:
            if len(redundant["tools"]) > 2:  # Only flag significant redundancy
                recommendations.append({
                    "type": "redundancy_consolidation",
                    "priority": "medium",
                    "description": f"Multiple tools provide {redundant['capability']}",
                    "action": "Consider consolidating functionality",
                    "affected_tools": redundant["tools"]
                })

        # Failed tool recommendations
        failed_tools = [t["tool_name"] for t in tool_results if not t["execution_success"]]
        if failed_tools:
            recommendations.append({
                "type": "tool_failure_resolution",
                "priority": "high",
                "description": f"{len(failed_tools)} tools failed to execute",
                "action": "Fix import/execution issues",
                "affected_tools": failed_tools
            })

        self.results["optimization_opportunities"] = recommendations

    def save_results(self, output_path: Optional[Path] = None) -> Path:
        """Save comprehensive test results"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
<<<<<<< HEAD
            output_path = self.workspace_root / "tachyonic" / "archive" / f"runtime_intelligence_test_{timestamp}.json"
=======
            output_path = self.workspace_root / "tachyonic" / "archive" / f"runtime_test_{timestamp}.json"
>>>>>>> origin/OS0.6.2.grok

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

        return output_path

def main():
    """Main execution function"""
    workspace_root = Path(__file__).parent.parent

    tester = RuntimeIntelligenceTester(workspace_root)
    results = tester.run_comprehensive_test()

    # Save results
    output_path = tester.save_results()
    print(f"\n💾 Results saved to: {output_path}")

    # Print summary
    summary = results["execution_summary"]
    print("\n📈 EXECUTION SUMMARY")
    print(f"Total Tools Tested: {summary['total_tools']}")
    print(f"Successful: {summary['successful_tools']}")
    print(f"Failed: {summary['failed_tools']}")
    print(f"Bridge Coverage: {summary['bridge_coverage']:.1f}%")
    print(f"Redundancy Opportunities: {summary['redundancy_opportunities']}")

    if results["optimization_opportunities"]:
        print("\n🎯 OPTIMIZATION OPPORTUNITIES:")
        for i, opp in enumerate(results["optimization_opportunities"], 1):
            print(f"{i}. [{opp['priority'].upper()}] {opp['description']}")
            print(f"   Action: {opp['action']}")

if __name__ == "__main__":
    main()