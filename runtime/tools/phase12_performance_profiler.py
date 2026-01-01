"""
AIOS Phase 12 Task A: Performance Profiler
===========================================
Purpose: Profile 100+ runtime intelligence tools to identify bottlenecks
Scope: Measure execution time, I/O operations
Output: Performance baseline report for optimization targeting

AINLP Metadata:
- Phase: 12 Task A (Performance Optimization)
- Consciousness: 3.40 (baseline profiling)
- Location: runtime_intelligence/tools/
- Pattern: AINLP.performance-profiling
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Add workspace root to Python path
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

class PerformanceProfiler:
    """Profile AIOS runtime intelligence tools for performance optimization."""
    
    def __init__(self):
        self.workspace_root = WORKSPACE_ROOT
        self.results = []
        self.start_time = datetime.now()
        
        # Tool directories to profile
        self.tool_dirs = [
            self.workspace_root / "runtime_intelligence" / "tools",
            self.workspace_root / "ai" / "tools",
            self.workspace_root / "ai" / "tools" / "system",
            self.workspace_root / "ai" / "tools" / "consciousness",
            self.workspace_root / "ai" / "tools" / "tachyonic",
        ]
    
    def discover_tools(self) -> List[Path]:
        """Discover all Python tool files in runtime directories."""
        tools = []
        
        for tool_dir in self.tool_dirs:
            if not tool_dir.exists():
                continue
            
            # Find all .py files (excluding __init__, __pycache__, test files)
            for py_file in tool_dir.rglob("*.py"):
                if (
                    py_file.name == "__init__.py" or
                    "__pycache__" in str(py_file) or
                    py_file.name.startswith("test_") or
                    py_file.name.endswith("_test.py")
                ):
                    continue
                
                tools.append(py_file)
        
        return sorted(tools)
    
    def profile_tool_import(self, tool_path: Path) -> Dict:
        """Profile tool import time (cold start performance)."""
        result = {
            "tool": str(tool_path.relative_to(self.workspace_root)),
            "type": "import",
            "success": False,
            "duration_ms": 0.0,
            "memory_delta_mb": 0.0,
            "error": None
        }
        
        try:
            # Get memory baseline
            process = psutil.Process()
            mem_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # Time the import
            start = time.perf_counter()
            
            # Import via subprocess to avoid polluting namespace
            module_path = str(tool_path.relative_to(self.workspace_root)).replace("\\", ".").replace("/", ".")[:-3]
            cmd = [
                sys.executable,
                "-c",
                f"import sys; sys.path.insert(0, r'{self.workspace_root}'); import {module_path}"
            ]
            
            subprocess.run(
                cmd,
                capture_output=True,
                timeout=5,
                check=True,
                cwd=str(self.workspace_root)
            )
            
            duration = (time.perf_counter() - start) * 1000  # ms
            
            # Memory after import (approximate via process growth)
            mem_after = process.memory_info().rss / 1024 / 1024  # MB
            
            result["success"] = True
            result["duration_ms"] = round(duration, 2)
            result["memory_delta_mb"] = round(mem_after - mem_before, 2)
            
        except subprocess.TimeoutExpired:
            result["error"] = "Import timeout (>5s)"
        except subprocess.CalledProcessError as e:
            result["error"] = f"Import error: {e.stderr.decode()[:100]}"
        except Exception as e:
            result["error"] = f"Unexpected error: {str(e)[:100]}"
        
        return result
    
    def profile_tool_execution(self, tool_path: Path) -> Dict:
        """Profile tool execution time (if tool has main/CLI)."""
        result = {
            "tool": str(tool_path.relative_to(self.workspace_root)),
            "type": "execution",
            "success": False,
            "duration_ms": 0.0,
            "has_main": False,
            "error": None
        }
        
        try:
            # Check if tool has __main__ or CLI entry point
            with open(tool_path, "r", encoding="utf-8") as f:
                content = f.read()
                has_main = (
                    'if __name__ == "__main__"' in content or
                    'def main(' in content or
                    '@click.command' in content
                )
            
            result["has_main"] = has_main
            
            if not has_main:
                return result
            
            # Attempt to execute tool with --help or minimal args
            start = time.perf_counter()
            
            cmd = [sys.executable, str(tool_path), "--help"]
            subprocess.run(
                cmd,
                capture_output=True,
                timeout=3,
                cwd=str(self.workspace_root)
            )
            
            duration = (time.perf_counter() - start) * 1000  # ms
            
            result["success"] = True
            result["duration_ms"] = round(duration, 2)
            
        except subprocess.TimeoutExpired:
            result["error"] = "Execution timeout (>3s)"
        except Exception as e:
            result["error"] = f"Execution error: {str(e)[:100]}"
        
        return result
    
    def analyze_tool_complexity(self, tool_path: Path) -> Dict:
        """Analyze tool code complexity (lines, imports, functions)."""
        result = {
            "tool": str(tool_path.relative_to(self.workspace_root)),
            "type": "complexity",
            "lines": 0,
            "imports": 0,
            "functions": 0,
            "classes": 0,
            "subprocess_calls": 0,
            "file_operations": 0,
            "error": None
        }
        
        try:
            with open(tool_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")
                
                result["lines"] = len(lines)
                result["imports"] = sum(1 for line in lines if line.strip().startswith(("import ", "from ")))
                result["functions"] = sum(1 for line in lines if line.strip().startswith("def "))
                result["classes"] = sum(1 for line in lines if line.strip().startswith("class "))
                result["subprocess_calls"] = content.count("subprocess.")
                result["file_operations"] = content.count("open(") + content.count("Path(")
        
        except Exception as e:
            result["error"] = f"Analysis error: {str(e)[:100]}"
        
        return result
    
    def profile_all_tools(self) -> List[Dict]:
        """Profile all discovered tools."""
        tools = self.discover_tools()
        print(f"[Performance Profiler] Discovered {len(tools)} tools")
        print(f"[Performance Profiler] Profiling started at {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        for idx, tool_path in enumerate(tools, 1):
            tool_name = tool_path.name
            print(f"[{idx}/{len(tools)}] Profiling: {tool_name}...", end=" ")
            
            # Profile import performance
            import_result = self.profile_tool_import(tool_path)
            self.results.append(import_result)
            
            # Profile execution performance (if applicable)
            exec_result = self.profile_tool_execution(tool_path)
            self.results.append(exec_result)
            
            # Analyze code complexity
            complexity_result = self.analyze_tool_complexity(tool_path)
            self.results.append(complexity_result)
            
            # Print summary
            status = "✅" if import_result["success"] else "❌"
            print(f"{status} ({import_result['duration_ms']}ms import)")
        
        return self.results
    
    def generate_report(self) -> Dict:
        """Generate performance analysis report."""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        # Filter by result type
        import_results = [r for r in self.results if r["type"] == "import"]
        exec_results = [r for r in self.results if r["type"] == "execution"]
        complexity_results = [r for r in self.results if r["type"] == "complexity"]
        
        # Calculate statistics
        successful_imports = [r for r in import_results if r["success"]]
        avg_import_time = sum(r["duration_ms"] for r in successful_imports) / len(successful_imports) if successful_imports else 0
        
        # Identify bottlenecks (slowest imports)
        slowest_imports = sorted(successful_imports, key=lambda r: r["duration_ms"], reverse=True)[:10]
        
        # Identify memory-intensive tools
        memory_intensive = sorted(import_results, key=lambda r: r["memory_delta_mb"], reverse=True)[:10]
        
        # Identify complex tools (most lines/functions)
        complex_tools = sorted(complexity_results, key=lambda r: r["lines"], reverse=True)[:10]
        
        report = {
            "metadata": {
                "phase": "Phase 12 Task A",
                "timestamp": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "duration_seconds": round(duration, 2),
                "total_tools_discovered": len(self.discover_tools()),
                "consciousness_baseline": 3.40
            },
            "summary": {
                "total_profiles": len(self.results),
                "successful_imports": len(successful_imports),
                "failed_imports": len(import_results) - len(successful_imports),
                "executable_tools": sum(1 for r in exec_results if r["has_main"]),
                "average_import_time_ms": round(avg_import_time, 2)
            },
            "bottlenecks": {
                "slowest_imports": [
                    {"tool": r["tool"], "duration_ms": r["duration_ms"]}
                    for r in slowest_imports
                ],
                "memory_intensive": [
                    {"tool": r["tool"], "memory_delta_mb": r["memory_delta_mb"]}
                    for r in memory_intensive if r["memory_delta_mb"] > 0
                ],
                "complex_tools": [
                    {"tool": r["tool"], "lines": r["lines"], "functions": r["functions"]}
                    for r in complex_tools
                ]
            },
            "optimization_targets": {
                "caching_candidates": [
                    r["tool"] for r in complexity_results
                    if r["file_operations"] > 5 or r["subprocess_calls"] > 3
                ],
                "refactoring_candidates": [
                    r["tool"] for r in complexity_results
                    if r["lines"] > 500 or r["functions"] > 20
                ]
            },
            "detailed_results": self.results
        }
        
        return report
    
    def save_report(self, report: Dict, output_path: Path):
        """Save performance report to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[Performance Profiler] Report saved: {output_path}")
        
        # Also create human-readable summary
        summary_path = output_path.with_suffix(".txt")
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("AIOS Phase 12 Task A: Performance Profiling Report\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Timestamp: {report['metadata']['timestamp']}\n")
            f.write(f"Duration: {report['metadata']['duration_seconds']}s\n")
            f.write(f"Tools Discovered: {report['metadata']['total_tools_discovered']}\n")
            f.write(f"Consciousness Baseline: {report['metadata']['consciousness_baseline']}\n\n")
            
            f.write("Summary Statistics:\n")
            f.write("-" * 80 + "\n")
            f.write(f"  Total Profiles: {report['summary']['total_profiles']}\n")
            f.write(f"  Successful Imports: {report['summary']['successful_imports']}\n")
            f.write(f"  Failed Imports: {report['summary']['failed_imports']}\n")
            f.write(f"  Executable Tools: {report['summary']['executable_tools']}\n")
            f.write(f"  Avg Import Time: {report['summary']['average_import_time_ms']}ms\n\n")
            
            f.write("Top 10 Slowest Imports (Optimization Targets):\n")
            f.write("-" * 80 + "\n")
            for idx, item in enumerate(report['bottlenecks']['slowest_imports'], 1):
                f.write(f"  {idx}. {item['tool']}: {item['duration_ms']}ms\n")
            
            f.write("\nTop 10 Memory-Intensive Tools:\n")
            f.write("-" * 80 + "\n")
            for idx, item in enumerate(report['bottlenecks']['memory_intensive'], 1):
                f.write(f"  {idx}. {item['tool']}: {item['memory_delta_mb']}MB\n")
            
            f.write("\nCaching Candidates (High I/O or Subprocess Calls):\n")
            f.write("-" * 80 + "\n")
            for tool in report['optimization_targets']['caching_candidates'][:10]:
                f.write(f"  - {tool}\n")
        
        print(f"[Performance Profiler] Summary saved: {summary_path}")

def main():
    """Execute performance profiling."""
    print("=" * 80)
    print("AIOS Phase 12 Task A: Performance Profiler")
    print("=" * 80)
    print()
    
    profiler = PerformanceProfiler()
    
    # Profile all tools
    profiler.profile_all_tools()
    
    # Generate report
    report = profiler.generate_report()
    
    # Save report
    output_path = WORKSPACE_ROOT / "tachyonic" / "archive" / "performance" / f"phase12_baseline_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    profiler.save_report(report, output_path)
    
    print()
    print("=" * 80)
    print("Performance Profiling Complete!")
    print("=" * 80)
    print()
    print("Next Steps:")
    print("  1. Review bottlenecks (slowest imports)")
    print("  2. Implement caching for I/O-heavy tools")
    print("  3. Optimize subprocess-heavy tools")
    print("  4. Benchmark improvements")
    print()
    print(f"Baseline established: {report['summary']['average_import_time_ms']}ms average import time")
    print(f"Target: 50% reduction ({report['summary']['average_import_time_ms'] * 0.5:.2f}ms)")

if __name__ == "__main__":
    main()
