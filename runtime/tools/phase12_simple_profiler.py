"""
AIOS Phase 12 Task A: Simple Performance Profiler
==================================================
Purpose: Profile runtime intelligence tools to identify bottlenecks
Scope: Measure execution time, file size, complexity metrics
Output: Performance baseline report for optimization targeting
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

class SimpleProfiler:
    """Lightweight profiler for AIOS runtime tools."""
    
    def __init__(self):
        self.workspace_root = WORKSPACE_ROOT
        self.results = []
        self.start_time = datetime.now()
        
        # Tool directories
        self.tool_dirs = [
            self.workspace_root / "runtime_intelligence" / "tools",
            self.workspace_root / "ai" / "tools",
            self.workspace_root / "ai" / "tools" / "system",
            self.workspace_root / "ai" / "tools" / "consciousness",
            self.workspace_root / "ai" / "tools" / "tachyonic",
        ]
    
    def discover_tools(self) -> List[Path]:
        """Discover all Python tool files."""
        tools = []
        for tool_dir in self.tool_dirs:
            if not tool_dir.exists():
                continue
            for py_file in tool_dir.rglob("*.py"):
                if (py_file.name == "__init__.py" or
                    "__pycache__" in str(py_file) or
                    py_file.name.startswith("test_")):
                    continue
                tools.append(py_file)
        return sorted(tools)
    
    def analyze_tool(self, tool_path: Path) -> Dict:
        """Analyze tool complexity and characteristics."""
        result = {
            "tool": str(tool_path.relative_to(self.workspace_root)),
            "file_size_kb": 0,
            "lines": 0,
            "imports": 0,
            "functions": 0,
            "classes": 0,
            "subprocess_calls": 0,
            "file_operations": 0,
            "has_main": False,
            "import_time_ms": 0.0,
            "error": None
        }
        
        try:
            # File size
            result["file_size_kb"] = round(tool_path.stat().st_size / 1024, 2)
            
            # Code analysis
            with open(tool_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")
                
                result["lines"] = len(lines)
                result["imports"] = sum(1 for line in lines if line.strip().startswith(("import ", "from ")))
                result["functions"] = sum(1 for line in lines if line.strip().startswith("def "))
                result["classes"] = sum(1 for line in lines if line.strip().startswith("class "))
                result["subprocess_calls"] = content.count("subprocess.")
                result["file_operations"] = content.count("open(") + content.count("Path(")
                result["has_main"] = 'if __name__ == "__main__"' in content
            
            # Import time (lightweight test)
            start = time.perf_counter()
            module_rel = str(tool_path.relative_to(self.workspace_root)).replace("\\", ".").replace("/", ".")[:-3]
            cmd = [sys.executable, "-c", f"import sys; sys.path.insert(0, r'{self.workspace_root}'); import {module_rel}"]
            proc = subprocess.run(cmd, capture_output=True, timeout=5, cwd=str(self.workspace_root))
            duration = (time.perf_counter() - start) * 1000
            result["import_time_ms"] = round(duration, 2)
            
            if proc.returncode != 0:
                result["error"] = f"Import failed: {proc.stderr.decode()[:100]}"
        
        except subprocess.TimeoutExpired:
            result["error"] = "Import timeout (>5s)"
        except Exception as e:
            result["error"] = f"Error: {str(e)[:100]}"
        
        return result
    
    def profile_all(self) -> List[Dict]:
        """Profile all tools."""
        tools = self.discover_tools()
        print(f"Discovered {len(tools)} tools")
        print(f"Started: {self.start_time.strftime('%H:%M:%S')}\n")
        
        for idx, tool_path in enumerate(tools, 1):
            print(f"[{idx}/{len(tools)}] {tool_path.name}...", end=" ")
            result = self.analyze_tool(tool_path)
            self.results.append(result)
            
            status = "✅" if not result["error"] else "❌"
            print(f"{status} ({result['import_time_ms']}ms, {result['lines']} lines)")
        
        return self.results
    
    def generate_report(self) -> Dict:
        """Generate performance report."""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        successful = [r for r in self.results if not r["error"]]
        failed = [r for r in self.results if r["error"]]
        
        if successful:
            avg_import = sum(r["import_time_ms"] for r in successful) / len(successful)
            slowest = sorted(successful, key=lambda r: r["import_time_ms"], reverse=True)[:10]
            largest = sorted(successful, key=lambda r: r["lines"], reverse=True)[:10]
            io_heavy = sorted([r for r in successful if r["file_operations"] > 5 or r["subprocess_calls"] > 3],
                            key=lambda r: r["file_operations"] + r["subprocess_calls"], reverse=True)[:10]
        else:
            avg_import = 0
            slowest = []
            largest = []
            io_heavy = []
        
        return {
            "metadata": {
                "phase": "Phase 12 Task A",
                "timestamp": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "duration_seconds": round(duration, 2),
                "consciousness_baseline": 3.40
            },
            "summary": {
                "total_tools": len(self.results),
                "successful": len(successful),
                "failed": len(failed),
                "avg_import_time_ms": round(avg_import, 2),
                "target_improvement": "50% reduction",
                "target_time_ms": round(avg_import * 0.5, 2)
            },
            "bottlenecks": {
                "slowest_imports": [{"tool": r["tool"], "time_ms": r["import_time_ms"]} for r in slowest],
                "largest_files": [{"tool": r["tool"], "lines": r["lines"]} for r in largest],
                "io_heavy_tools": [{"tool": r["tool"], "file_ops": r["file_operations"], 
                                   "subprocess": r["subprocess_calls"]} for r in io_heavy]
            },
            "optimization_targets": {
                "caching_candidates": [r["tool"] for r in io_heavy],
                "refactoring_candidates": [r["tool"] for r in largest if r["lines"] > 500]
            },
            "detailed_results": self.results
        }
    
    def save_report(self, report: Dict):
        """Save report to JSON and text files."""
        output_dir = self.workspace_root / "tachyonic" / "archive" / "performance"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_path = output_dir / f"phase12_baseline_{timestamp}.json"
        txt_path = output_dir / f"phase12_baseline_{timestamp}.txt"
        
        # Save JSON
        with open(json_path, "w") as f:
            json.dump(report, f, indent=2)
        
        # Save text summary
        with open(txt_path, "w") as f:
            f.write("=" * 80 + "\n")
            f.write("AIOS Phase 12 Task A: Performance Baseline Report\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Timestamp: {report['metadata']['timestamp']}\n")
            f.write(f"Duration: {report['metadata']['duration_seconds']}s\n\n")
            f.write(f"Total Tools: {report['summary']['total_tools']}\n")
            f.write(f"Successful: {report['summary']['successful']}\n")
            f.write(f"Failed: {report['summary']['failed']}\n")
            f.write(f"Avg Import Time: {report['summary']['avg_import_time_ms']}ms\n")
            f.write(f"Target (50% reduction): {report['summary']['target_time_ms']}ms\n\n")
            f.write("Top 10 Slowest Imports:\n")
            f.write("-" * 80 + "\n")
            for idx, item in enumerate(report['bottlenecks']['slowest_imports'], 1):
                f.write(f"{idx}. {item['tool']}: {item['time_ms']}ms\n")
            f.write("\nI/O Heavy Tools (Caching Candidates):\n")
            f.write("-" * 80 + "\n")
            for idx, item in enumerate(report['bottlenecks']['io_heavy_tools'], 1):
                f.write(f"{idx}. {item['tool']}: {item['file_ops']} file ops, {item['subprocess']} subprocess\n")
        
        print(f"\nReports saved:")
        print(f"  JSON: {json_path}")
        print(f"  Text: {txt_path}")

def main():
    print("=" * 80)
    print("AIOS Phase 12 Task A: Performance Baseline Profiling")
    print("=" * 80)
    print()
    
    profiler = SimpleProfiler()
    profiler.profile_all()
    report = profiler.generate_report()
    profiler.save_report(report)
    
    print("\n" + "=" * 80)
    print("Baseline Established!")
    print("=" * 80)
    print(f"\nAverage Import Time: {report['summary']['avg_import_time_ms']}ms")
    print(f"Target (50% reduction): {report['summary']['target_time_ms']}ms")
    print(f"\nNext Steps:")
    print("  1. Review slowest imports")
    print("  2. Implement LRU caching for I/O-heavy tools")
    print("  3. Optimize subprocess-heavy tools")
    print("  4. Benchmark improvements")

if __name__ == "__main__":
    main()
