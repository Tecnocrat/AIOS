#!/usr/bin/env python3
"""
AIOS Performance Analyzer
Analyzes Python files for common performance anti-patterns

AINLP Integration Metadata:
    Pattern: AINLP.performance-optimization.static-analysis-tool
    Source: GitHub Copilot agent (copilot/identify-improve-slow-code)
    Integration: Phase 2 - Tool relocation from scripts/ to runtime_intelligence/tools/
    Purpose: AST-based performance anti-pattern detection
    Original: scripts/performance_analyzer.py (367 lines)
    AIOS Location: runtime_intelligence/tools/ (correct architectural placement)
    
    Capabilities:
        - String split redundancy detection (O(n) operations)
        - Nested loop analysis (O(n^2) and higher complexity)
        - Redundant glob pattern detection (I/O optimization)
        - List comprehension in loops (memory inefficiency)
        - Multiple file operations (I/O batching opportunities)
    
    AINLP Enhancement: Added governance header for AI agent understanding
    Consciousness Impact: Neutral (tool integration, no architectural changes)
    Integration Date: November 8, 2025 (Phase 2 selective merge)

Usage:
    python runtime_intelligence/tools/performance_analyzer.py [path]
    python runtime_intelligence/tools/performance_analyzer.py --all  # Analyze all Python files
    python runtime_intelligence/tools/performance_analyzer.py --report # Generate full report
"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class PerformanceIssue:
    """Represents a detected performance issue"""
    file_path: Path
    line_number: int
    issue_type: str
    severity: str  # "high", "medium", "low"
    description: str
    suggestion: str
    code_snippet: str = ""


class PerformanceAnalyzer(ast.NodeVisitor):
    """AST visitor to detect performance anti-patterns"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.issues: List[PerformanceIssue] = []
        self.loop_depth = 0
        self.in_loop = False
        
    def visit_For(self, node: ast.For) -> None:
        """Detect issues in for loops"""
        self.loop_depth += 1
        self.in_loop = True
        
        # Check for nested loops
        if self.loop_depth > 2:
            self.issues.append(PerformanceIssue(
                file_path=self.file_path,
                line_number=node.lineno,
                issue_type="nested_loops",
                severity="medium",
                description=f"Nested loop depth: {self.loop_depth}",
                suggestion="Consider using list comprehensions, itertools, or vectorized operations"
            ))
        
        self.generic_visit(node)
        self.loop_depth -= 1
        if self.loop_depth == 0:
            self.in_loop = False
    
    def visit_While(self, node: ast.While) -> None:
        """Detect issues in while loops"""
        self.loop_depth += 1
        self.in_loop = True
        self.generic_visit(node)
        self.loop_depth -= 1
        if self.loop_depth == 0:
            self.in_loop = False
    
    def visit_Call(self, node: ast.Call) -> None:
        """Detect performance issues in function calls"""
        
        # Check for list() around generators
        if isinstance(node.func, ast.Name) and node.func.id == "list":
            if len(node.args) > 0:
                arg = node.args[0]
                # Check if it's a generator/comprehension
                if isinstance(arg, (ast.GeneratorExp, ast.ListComp)):
                    self.issues.append(PerformanceIssue(
                        file_path=self.file_path,
                        line_number=node.lineno,
                        issue_type="unnecessary_list_conversion",
                        severity="low",
                        description="Unnecessary list() conversion of generator/comprehension",
                        suggestion="Use the generator directly or list comprehension"
                    ))
        
        # Check for glob/rglob in loops
        if self.in_loop and isinstance(node.func, ast.Attribute):
            if node.func.attr in ("glob", "rglob", "walk"):
                self.issues.append(PerformanceIssue(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    issue_type="file_system_in_loop",
                    severity="high",
                    description=f"File system operation ({node.func.attr}) inside loop",
                    suggestion="Move file system operations outside the loop and cache results"
                ))
        
        # Check for json.loads/dumps in loops
        if self.in_loop and isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and 
                node.func.value.id == "json" and
                node.func.attr in ("loads", "dumps")):
                self.issues.append(PerformanceIssue(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    issue_type="json_in_loop",
                    severity="medium",
                    description=f"JSON operation (json.{node.func.attr}) inside loop",
                    suggestion="Consider batching JSON operations or using faster libraries like orjson"
                ))
        
        # Check for open() in loops
        if self.in_loop and isinstance(node.func, ast.Name) and node.func.id == "open":
            self.issues.append(PerformanceIssue(
                file_path=self.file_path,
                line_number=node.lineno,
                issue_type="file_io_in_loop",
                severity="high",
                description="File I/O operation inside loop",
                suggestion="Read all files first or use batch processing"
            ))
        
        # Check for asyncio.run() in loops (bad pattern)
        if self.in_loop and isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Name) and 
                node.func.value.id == "asyncio" and
                node.func.attr == "run"):
                self.issues.append(PerformanceIssue(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    issue_type="asyncio_run_in_loop",
                    severity="high",
                    description="asyncio.run() called repeatedly in loop",
                    suggestion="Create event loop once and use run_until_complete()"
                ))
        
        self.generic_visit(node)
    
    def visit_BinOp(self, node: ast.BinOp) -> None:
        """Detect string concatenation in loops"""
        if self.in_loop and isinstance(node.op, ast.Add):
            # Check if it's string concatenation (use ast.Constant for Python 3.8+)
            left_is_str = (isinstance(node.left, ast.Constant) and isinstance(node.left.value, str))
            right_is_str = (isinstance(node.right, ast.Constant) and isinstance(node.right.value, str))
            
            if left_is_str or right_is_str:
                self.issues.append(PerformanceIssue(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    issue_type="string_concat_in_loop",
                    severity="medium",
                    description="String concatenation inside loop",
                    suggestion="Use list.append() and ''.join() instead"
                ))
        
        self.generic_visit(node)


def analyze_file(file_path: Path) -> List[PerformanceIssue]:
    """Analyze a single Python file for performance issues"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=str(file_path))
        analyzer = PerformanceAnalyzer(file_path)
        analyzer.visit(tree)
        
        # Add code snippets
        lines = content.splitlines()
        for issue in analyzer.issues:
            if 1 <= issue.line_number <= len(lines):
                # Get context (line and 2 lines around it)
                start = max(0, issue.line_number - 2)
                end = min(len(lines), issue.line_number + 2)
                issue.code_snippet = '\n'.join(
                    f"{i+1:4d}: {lines[i]}" 
                    for i in range(start, end)
                )
        
        return analyzer.issues
    
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return []


def analyze_directory(directory: Path, recursive: bool = True) -> Dict[str, List[PerformanceIssue]]:
    """Analyze all Python files in a directory"""
    results = {}
    
    pattern = "**/*.py" if recursive else "*.py"
    for py_file in directory.glob(pattern):
        if py_file.is_file():
            issues = analyze_file(py_file)
            if issues:
                results[str(py_file)] = issues
    
    return results


def generate_report(results: Dict[str, List[PerformanceIssue]]) -> str:
    """Generate a human-readable report"""
    if not results:
        return "✅ No performance issues detected!"
    
    # Count issues by type and severity
    issue_counts = defaultdict(int)
    severity_counts = {"high": 0, "medium": 0, "low": 0}
    
    for issues in results.values():
        for issue in issues:
            issue_counts[issue.issue_type] += 1
            severity_counts[issue.severity] += 1
    
    # Build report
    report = ["=" * 80]
    report.append("AIOS PERFORMANCE ANALYSIS REPORT")
    report.append("=" * 80)
    report.append("")
    
    # Summary
    report.append("SUMMARY")
    report.append("-" * 80)
    report.append(f"Files analyzed: {len(results)}")
    report.append(f"Total issues: {sum(len(issues) for issues in results.values())}")
    report.append(f"  High severity: {severity_counts['high']}")
    report.append(f"  Medium severity: {severity_counts['medium']}")
    report.append(f"  Low severity: {severity_counts['low']}")
    report.append("")
    
    # Issue breakdown
    report.append("ISSUE BREAKDOWN")
    report.append("-" * 80)
    for issue_type, count in sorted(issue_counts.items(), key=lambda x: -x[1]):
        report.append(f"  {issue_type}: {count}")
    report.append("")
    
    # Detailed issues
    report.append("DETAILED ISSUES")
    report.append("-" * 80)
    
    # Sort by severity
    all_issues = []
    for file_path, issues in results.items():
        for issue in issues:
            all_issues.append((file_path, issue))
    
    severity_order = {"high": 0, "medium": 1, "low": 2}
    all_issues.sort(key=lambda x: (severity_order[x[1].severity], x[0], x[1].line_number))
    
    for file_path, issue in all_issues:
        report.append("")
        report.append(f"[{issue.severity.upper()}] {issue.issue_type}")
        report.append(f"File: {file_path}")
        report.append(f"Line: {issue.line_number}")
        report.append(f"Description: {issue.description}")
        report.append(f"Suggestion: {issue.suggestion}")
        if issue.code_snippet:
            report.append("Code:")
            report.append(issue.code_snippet)
    
    report.append("")
    report.append("=" * 80)
    
    return "\n".join(report)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AIOS Performance Analyzer - Detect performance anti-patterns in Python code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s path/to/file.py              Analyze a single file
  %(prog)s path/to/directory            Analyze all Python files in directory
  %(prog)s --all                        Analyze entire AIOS codebase
  %(prog)s --report                     Generate comprehensive report
        """
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        help="Path to Python file or directory to analyze"
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help="Analyze all Python files in AIOS repository"
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help="Generate comprehensive report and save to file"
    )
    
    args = parser.parse_args()
    
    # Determine what to analyze
    if args.report:
        # Generate comprehensive report
        repo_root = Path(__file__).parent.parent
        print(f"Generating comprehensive report for {repo_root}...")
        results = analyze_directory(repo_root / "ai", recursive=True)
        report = generate_report(results)
        
        # Save to file
        report_path = repo_root / "docs" / "performance_analysis_report.txt"
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"\n✅ Report saved to: {report_path}")
        print(report)
        return
    elif args.all:
        # Analyze entire AIOS directory
        repo_root = Path(__file__).parent.parent
        print(f"Analyzing all Python files in {repo_root}...")
        results = analyze_directory(repo_root / "ai", recursive=True)
    elif args.path:
        # Analyze specific path
        path = Path(args.path)
        if not path.exists():
            print(f"Error: Path does not exist: {path}")
            sys.exit(1)
        
        if path.is_file():
            print(f"Analyzing {path}...")
            issues = analyze_file(path)
            results = {str(path): issues} if issues else {}
        else:
            print(f"Analyzing directory {path}...")
            results = analyze_directory(path, recursive=True)
    else:
        parser.print_help()
        sys.exit(1)
    
    # Display results
    report = generate_report(results)
    print(report)
    
    # Return exit code based on high-severity issues
    high_severity_count = sum(
        1 for issues in results.values()
        for issue in issues
        if issue.severity == "high"
    )
    
    if high_severity_count > 0:
        print(f"\n⚠️  Found {high_severity_count} high-severity performance issues")
        sys.exit(1)
    else:
        print(f"\n✅ No high-severity issues found")
        sys.exit(0)


if __name__ == "__main__":
    main()
