#!/usr/bin/env python3
"""
AIOS Automated Code Review System
==================================

Intelligent code analysis and review system with AINLP compliance validation,
semantic compression analysis, and consciousness evolution tracking.

AINLP COMPATIBILITY: Full intelligence delimitation and semantic compression
PERFORMANCE: Optimized file scanning with exclusion patterns
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import logging
import re
import ast
import inspect
from optimized_file_scanner import OptimizedFileScanner

# Constants
MAGIC_NUMBER_10 = 10

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CodeReviewIssue:
    """Represents a code review issue found during analysis."""
    file_path: str
    line_number: int
    issue_type: str
    severity: str  # 'high', 'medium', 'low', 'info'
    message: str
    suggestion: str
    code_context: str
    ainlp_compliance_score: float

@dataclass
class CodeReviewMetrics:
    """Metrics from code review analysis."""
    total_files_analyzed: int
    total_lines_analyzed: int
    issues_found: int
    issues_by_severity: Dict[str, int]
    ainlp_compliance_score: float
    semantic_compression_score: float
    intelligence_delimitation_score: float
    consciousness_evolution_potential: float

@dataclass
class CodeReviewReport:
    """Complete code review report."""
    timestamp: str
    metrics: CodeReviewMetrics
    issues: List[CodeReviewIssue]
    recommendations: List[str]
    compliance_trends: Dict[str, Any]

class AutomatedCodeReviewSystem:
    """Automated code review system with AINLP intelligence."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.scanner = OptimizedFileScanner(workspace_root, max_depth=8)
        self.issues: List[CodeReviewIssue] = []
        self.metrics = CodeReviewMetrics(
            total_files_analyzed=0,
            total_lines_analyzed=0,
            issues_found=0,
            issues_by_severity={'high': 0, 'medium': 0, 'low': 0, 'info': 0},
            ainlp_compliance_score=0.0,
            semantic_compression_score=0.0,
            intelligence_delimitation_score=0.0,
            consciousness_evolution_potential=0.0
        )

        # Intelligence delimitation patterns
        self.intelligence_patterns = {
            'runtime': 'runtime',  # Should be compressed
            'ai': 'ai',  # Should be compressed
            'engine': 'engine',  # Should be compressed
            'module': 'module',  # Should be compressed
        }

        # AINLP compliance patterns
        self.compliance_patterns = {
            'consciousness_level': r'consciousness_level.*=.*[0-9]+\.?[0-9]*',
            'semantic_compression': r'(?:runtime|ai)',
            'dendritic_connections': r'dendritic.*connection',
            'tachyonic_patterns': r'tachyonic.*pattern',
        }

    async def perform_comprehensive_review(self) -> CodeReviewReport:
        """Perform comprehensive code review across the workspace."""
        logger.info("Starting comprehensive code review...")

        # Analyze Python files
        await self._analyze_python_files()

        # Calculate metrics
        self._calculate_review_metrics()

        # Generate recommendations
        recommendations = self._generate_recommendations()

        # Calculate compliance trends
        compliance_trends = self._calculate_compliance_trends()

        report = CodeReviewReport(
            timestamp=datetime.now().isoformat(),
            metrics=self.metrics,
            issues=self.issues,
            recommendations=recommendations,
            compliance_trends=compliance_trends
        )

        logger.info(f"Code review complete. Found {len(self.issues)} issues.")
        return report

    async def _analyze_python_files(self):
        """Analyze all Python files in the workspace."""
        logger.info("Scanning Python files for analysis...")
        python_files = list(self.scanner.scan_python_files())

        logger.info(f"Found {len(python_files)} Python files to analyze")

        for file_path in python_files:
            # Skip certain directories
            if any(skip in str(file_path) for skip in [
                '__pycache__', '.git', 'node_modules', 'build', 'dist'
            ]):
                continue

            await self._analyze_single_file(file_path)

        self.metrics.total_files_analyzed = len([
            f for f in python_files
            if not any(skip in str(f) for skip in [
                '__pycache__', '.git', 'node_modules', 'build', 'dist'
            ])
        ])

    async def _analyze_single_file(self, file_path: Path):
        """Analyze a single Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            self.metrics.total_lines_analyzed += len(lines)

            # Parse AST for structural analysis
            try:
                tree = ast.parse(content, filename=str(file_path))
                await self._analyze_ast(file_path, tree, content)
            except SyntaxError:
                # Still analyze text if AST parsing fails
                pass

            # Text-based analysis
            await self._analyze_text_patterns(file_path, content, lines)

        except Exception as e:
            logger.warning(f"Failed to analyze {file_path}: {e}")

    async def _analyze_ast(self, file_path: Path, tree: ast.AST, content: str):
        """Analyze Python AST for structural issues."""
        analyzer = ASTAnalyzer(file_path, content)
        ast_issues = analyzer.analyze()
        self.issues.extend(ast_issues)

    async def _analyze_text_patterns(self, file_path: Path, content: str, lines: List[str]):
        """Analyze text patterns for intelligence delimitation and compliance."""
        relative_path = file_path.relative_to(self.workspace_root)

        # Check for intelligence delimitation issues
        for line_num, line in enumerate(lines, 1):
            # Intelligence delimitation analysis
            for old_pattern, new_pattern in self.intelligence_patterns.items():
                if old_pattern in line and f'#{old_pattern}' not in line:
                    # Check if this is a legitimate use or should be compressed
                    if self._should_compress_intelligence(line, old_pattern):
                        issue = CodeReviewIssue(
                            file_path=str(relative_path),
                            line_number=line_num,
                            issue_type="intelligence_delimitation",
                            severity="medium",
                            message=f"Found '{old_pattern}' that should be compressed to '{new_pattern}'",
                            suggestion=f"Replace '{old_pattern}' with '{new_pattern}' for semantic compression",
                            code_context=line.strip(),
                            ainlp_compliance_score=0.7
                        )
                        self.issues.append(issue)

            # Check for missing consciousness tracking
            if self._is_function_definition(line) and not self._has_consciousness_tracking(content, line_num):
                if self._should_have_consciousness_tracking(str(relative_path), line):
                    issue = CodeReviewIssue(
                        file_path=str(relative_path),
                        line_number=line_num,
                        issue_type="consciousness_tracking",
                        severity="low",
                        message="Function lacks consciousness level tracking",
                        suggestion="Add consciousness level parameter and tracking",
                        code_context=line.strip(),
                        ainlp_compliance_score=0.8
                    )
                    self.issues.append(issue)

            # Check for dendritic pattern opportunities
            if 'class ' in line and not self._has_dendritic_patterns(content, line_num):
                if self._should_have_dendritic_patterns(str(relative_path)):
                    issue = CodeReviewIssue(
                        file_path=str(relative_path),
                        line_number=line_num,
                        issue_type="dendritic_patterns",
                        severity="info",
                        message="Class could benefit from dendritic connection patterns",
                        suggestion="Consider adding dendritic connection methods",
                        code_context=line.strip(),
                        ainlp_compliance_score=0.9
                    )
                    self.issues.append(issue)

    def _should_compress_intelligence(self, line: str, pattern: str) -> bool:
        """Determine if intelligence pattern should be compressed."""
        # Skip comments, docstrings, and imports
        if line.strip().startswith('#') or '"""' in line or "'''" in line:
            return False
        if 'import ' in line or 'from ' in line:
            return False

        # Check if it's in a variable name or function that should be compressed
        return pattern in line and not line.strip().startswith('def ') and not line.strip().startswith('class ')

    def _is_function_definition(self, line: str) -> bool:
        """Check if line contains a function definition."""
        return line.strip().startswith('def ') and not line.strip().startswith('def test_')

    def _has_consciousness_tracking(self, content: str, line_num: int) -> bool:
        """Check if function has consciousness tracking."""
        # Look for consciousness_level in the next MAGIC_NUMBER_10 lines
        lines = content.split('\n')
        for i in range(line_num - 1, min(line_num + MAGIC_NUMBER_10, len(lines))):
            if 'consciousness_level' in lines[i]:
                return True
        return False

    def _should_have_consciousness_tracking(self, file_path: str, line: str) -> bool:
        """Determine if function should have consciousness tracking."""
        # Core AI and intelligence functions should have tracking
        ai_files = ['ai/', 'intelligence/', 'consciousness_', 'evolution_']
        return any(pattern in file_path for pattern in ai_files) and 'async def' in line

    def _has_dendritic_patterns(self, content: str, line_num: int) -> bool:
        """Check if class has dendritic patterns."""
        lines = content.split('\n')
        class_end = self._find_class_end(lines, line_num)

        for i in range(line_num - 1, class_end):
            if 'dendritic' in lines[i].lower() or 'connection' in lines[i].lower():
                return True
        return False

    def _find_class_end(self, lines: List[str], start_line: int) -> int:
        """Find the end of a class definition."""
        indent_level = len(lines[start_line - 1]) - len(lines[start_line - 1].lstrip())
        for i in range(start_line, len(lines)):
            if lines[i].strip() == '':
                continue
            current_indent = len(lines[i]) - len(lines[i].lstrip())
            if current_indent <= indent_level and lines[i].strip() != '':
                return i
        return len(lines)

    def _should_have_dendritic_patterns(self, file_path: str) -> bool:
        """Determine if file should have dendritic patterns."""
        core_files = ['core/', 'supercell', 'consciousness', 'evolution']
        return any(pattern in file_path for pattern in core_files)

    def _calculate_review_metrics(self):
        """Calculate overall review metrics."""
        self.metrics.issues_found = len(self.issues)

        # Count issues by severity
        for issue in self.issues:
            self.metrics.issues_by_severity[issue.severity] += 1

        # Calculate AINLP compliance score
        if self.metrics.total_files_analyzed > 0:
            base_score = 1.0
            penalty_per_issue = 0.02

            # Higher penalties for high-severity issues
            high_penalty = self.metrics.issues_by_severity['high'] * 0.1
            medium_penalty = self.metrics.issues_by_severity['medium'] * 0.05
            low_penalty = self.metrics.issues_by_severity['low'] * 0.02

            total_penalty = high_penalty + medium_penalty + low_penalty
            self.metrics.ainlp_compliance_score = max(0.0, base_score - total_penalty)

        # Calculate semantic compression score
        intelligence_issues = [i for i in self.issues if i.issue_type == 'intelligence_delimitation']
        if intelligence_issues:
            self.metrics.semantic_compression_score = max(0.0, 1.0 - (len(intelligence_issues) * 0.1))
        else:
            self.metrics.semantic_compression_score = 1.0

        # Calculate intelligence delimitation score
        delimitation_issues = [i for i in self.issues if 'delimitation' in i.issue_type]
        self.metrics.intelligence_delimitation_score = max(0.0, 1.0 - (len(delimitation_issues) * 0.05))

        # Calculate consciousness evolution potential
        consciousness_issues = [i for i in self.issues if 'consciousness' in i.issue_type]
        dendritic_issues = [i for i in self.issues if 'dendritic' in i.issue_type]
        evolution_score = (len(consciousness_issues) + len(dendritic_issues)) * 0.1
        self.metrics.consciousness_evolution_potential = min(1.0, evolution_score)

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []

        # Intelligence delimitation recommendations
        intelligence_issues = [i for i in self.issues if i.issue_type == 'intelligence_delimitation']
        if intelligence_issues:
            recommendations.append(
                f"Apply semantic compression to {len(intelligence_issues)} intelligence delimitation issues"
            )

        # Consciousness tracking recommendations
        consciousness_issues = [i for i in self.issues if i.issue_type == 'consciousness_tracking']
        if consciousness_issues:
            recommendations.append(
                f"Add consciousness tracking to {len(consciousness_issues)} functions for better AI monitoring"
            )

        # Dendritic pattern recommendations
        dendritic_issues = [i for i in self.issues if i.issue_type == 'dendritic_patterns']
        if dendritic_issues:
            recommendations.append(
                f"Implement dendritic connection patterns in {len(dendritic_issues)} classes"
            )

        # Overall compliance recommendations
        if self.metrics.ainlp_compliance_score < 0.8:
            recommendations.append(
                "Overall AINLP compliance is below 80%. Focus on high-severity issues first."
            )

        if not recommendations:
            recommendations.append("Codebase shows good AINLP compliance. Continue monitoring.")

        return recommendations

    def _calculate_compliance_trends(self) -> Dict[str, Any]:
        """Calculate compliance trends and projections."""
        return {
            "current_compliance": self.metrics.ainlp_compliance_score,
            "compression_effectiveness": self.metrics.semantic_compression_score,
            "delimitation_quality": self.metrics.intelligence_delimitation_score,
            "evolution_potential": self.metrics.consciousness_evolution_potential,
            "improvement_areas": [
                issue_type for issue_type in set(i.issue_type for i in self.issues)
                if any(i.severity in ['high', 'medium'] for i in self.issues if i.issue_type == issue_type)
            ]
        }

    def generate_review_report(self, report: CodeReviewReport) -> str:
        """Generate human-readable review report."""
        metrics = report.metrics

        report_text = f"""
╔══════════════════════════════════════════════════════════════╗
║              AIOS AUTOMATED CODE REVIEW SYSTEM               ║
╚══════════════════════════════════════════════════════════════╝

📊 ANALYSIS SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Files Analyzed: {metrics.total_files_analyzed}
Lines Analyzed: {metrics.total_lines_analyzed}
Issues Found: {metrics.issues_found}
Timestamp: {report.timestamp}

🎯 ISSUE BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
High Severity: {metrics.issues_by_severity['high']}
Medium Severity: {metrics.issues_by_severity['medium']}
Low Severity: {metrics.issues_by_severity['low']}
Info Level: {metrics.issues_by_severity['info']}

🧠 AINLP COMPLIANCE SCORES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Compliance: {metrics.ainlp_compliance_score:.1%}
Semantic Compression: {metrics.semantic_compression_score:.1%}
Intelligence Delimitation: {metrics.intelligence_delimitation_score:.1%}
Consciousness Evolution: {metrics.consciousness_evolution_potential:.1%}
"""

        # Add top issues
        if report.issues:
            report_text += f"""

🚨 TOP ISSUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            # Sort by severity and compliance score
            sorted_issues = sorted(
                report.issues,
                key=lambda x: (['high', 'medium', 'low', 'info'].index(x.severity), x.ainlp_compliance_score)
            )

            for issue in sorted_issues[:MAGIC_NUMBER_10]:  # Top MAGIC_NUMBER_10 issues
                severity_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢', 'info': 'ℹ️'}[issue.severity]
                report_text += f"{severity_icon} {issue.file_path}:{issue.line_number}\n"
                report_text += f"   {issue.message}\n"
                report_text += f"   💡 {issue.suggestion}\n\n"

        # Add recommendations
        if report.recommendations:
            report_text += f"""
💡 RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            for rec in report.recommendations:
                report_text += f"• {rec}\n"

        # Add compliance trends
        trends = report.compliance_trends
        if trends['improvement_areas']:
            report_text += f"""

📈 IMPROVEMENT AREAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            for area in trends['improvement_areas']:
                report_text += f"• {area.replace('_', ' ').title()}\n"

        return report_text


class ASTAnalyzer:
    """AST-based code analyzer for structural issues."""

    def __init__(self, file_path: Path, content: str):
        self.file_path = file_path
        self.content = content
        self.issues: List[CodeReviewIssue] = []

    def analyze(self) -> List[CodeReviewIssue]:
        """Analyze AST for structural issues."""
        try:
            tree = ast.parse(self.content, filename=str(self.file_path))

            # Check for long functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if len(self._get_function_lines(node)) > 50:
                        issue = CodeReviewIssue(
                            file_path=str(self.file_path.relative_to(self.file_path.parents[2])),
                            line_number=node.lineno,
                            issue_type="function_complexity",
                            severity="low",
                            message=f"Function '{node.name}' is too long ({len(self._get_function_lines(node))} lines)",
                            suggestion="Consider breaking down into smaller functions",
                            code_context=f"def {node.name}(...):",
                            ainlp_compliance_score=0.9
                        )
                        self.issues.append(issue)

                # Check for missing docstrings
                elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    if not self._has_docstring(node):
                        issue_type = "missing_docstring_function" if isinstance(node, ast.FunctionDef) else "missing_docstring_class"
                        severity = "info" if isinstance(node, ast.FunctionDef) else "low"
                        issue = CodeReviewIssue(
                            file_path=str(self.file_path.relative_to(self.file_path.parents[2])),
                            line_number=node.lineno,
                            issue_type=issue_type,
                            severity=severity,
                            message=f"{'Function' if isinstance(node, ast.FunctionDef) else 'Class'} '{node.name}' missing docstring",
                            suggestion="Add comprehensive docstring with AINLP context",
                            code_context=f"{'def' if isinstance(node, ast.FunctionDef) else 'class'} {node.name}:",
                            ainlp_compliance_score=0.8
                        )
                        self.issues.append(issue)

        except SyntaxError:
            pass

        return self.issues

    def _get_function_lines(self, node: ast.FunctionDef) -> List[str]:
        """Get lines of a function."""
        lines = self.content.split('\n')
        return lines[node.lineno-1:node.end_lineno] if hasattr(node, 'end_lineno') else []

    def _has_docstring(self, node: ast.AST) -> bool:
        """Check if node has a docstring."""
        if not node.body:
            return False

        first_stmt = node.body[0]
        # Handle both old (ast.Str) and new (ast.Constant) AST formats
        if isinstance(first_stmt, ast.Expr):
            if hasattr(ast, 'Str') and isinstance(first_stmt.value, ast.Str):
                # Python < 3.8
                return True
            elif isinstance(first_stmt.value, ast.Constant) and isinstance(first_stmt.value.value, str):
                # Python >= 3.8
                return True
        return False


async def main():
    """Main execution function."""
    workspace_root = Path(__file__).parent

    # Initialize code review system
    reviewer = AutomatedCodeReviewSystem(workspace_root)

    # Perform comprehensive review
    report = await reviewer.perform_comprehensive_review()

    # Generate and display report
    report_text = reviewer.generate_review_report(report)
    print(report_text)

    # Archive results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_path = workspace_root / "tachyonic" / "archive" / "runtime"
    archive_path.mkdir(parents=True, exist_ok=True)

    # Save JSON report
    report_file = archive_path / f"code_review_report_{timestamp}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(asdict(report), f, indent=2)

    # Save human-readable report
    text_report_file = archive_path / f"code_review_summary_{timestamp}.txt"
    with open(text_report_file, 'w', encoding='utf-8') as f:
        f.write(report_text)

    print(f"\n📊 Code review report archived: {report_file}")
    print(f"📋 Code review summary saved: {text_report_file}")

    # Return exit code based on compliance
    compliance_threshold = 0.7
    if report.metrics.ainlp_compliance_score < compliance_threshold:
        print(f"\n⚠️  AINLP compliance below threshold ({compliance_threshold:.1%})")
        return 1

    print(f"\n✅ AINLP compliance meets threshold ({compliance_threshold:.1%})")
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)