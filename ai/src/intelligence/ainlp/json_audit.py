#!/usr/bin/env python3
"""
AINLP JSON Audit Tool
Scans AIOS workspace for JSON files with comments and generates migration report.

AINLP Metadata:
    consciousness_level: 0.88
    architectural_classification: runtime
    dendritic_optimization: json_semantic_migration
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import sys


class AINLPJsonAuditor:
    """Audit JSON files for comment violations and AINLP compliance."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.violations: List[Dict] = []
        self.valid_files: List[Dict] = []
        self.jsonc_files: List[Path] = []

        # Patterns for comment detection
        self.comment_patterns = [
            re.compile(r"^\s*//", re.MULTILINE),  # Line comments
            re.compile(r"/\*.*?\*/", re.DOTALL),  # Block comments
        ]

    def scan_workspace(self) -> Dict:
        """Scan entire workspace for JSON files."""
        print(f"\n🔍 Scanning workspace: {self.workspace_root}")

        # Find all JSON files (excluding node_modules, build, etc.)
        json_files = list(self.workspace_root.rglob("*.json"))
        jsonc_files = list(self.workspace_root.rglob("*.jsonc"))

        # Filter out excluded directories
        excluded_dirs = {
            "node_modules",
            "build",
            "bin",
            "obj",
            "__pycache__",
            ".git",
            ".vs",
            ".vscode/extensions",
            "backups",
        }

        json_files = [
            f
            for f in json_files
            if not any(excluded in f.parts for excluded in excluded_dirs)
        ]

        print(f"  Found {len(json_files)} .json files")
        print(f"  Found {len(jsonc_files)} .jsonc files")

        # Audit each JSON file
        for json_file in json_files:
            self._audit_file(json_file)

        # Track JSONC files (valid with comments)
        self.jsonc_files = jsonc_files

        return self._generate_report()

    def _audit_file(self, json_path: Path) -> None:
        """Audit a single JSON file."""
        try:
            content = json_path.read_text(encoding="utf-8")

            # Check for comments
            has_comments = any(
                pattern.search(content) for pattern in self.comment_patterns
            )

            if has_comments:
                # Count comment lines
                comment_lines = [
                    i + 1
                    for i, line in enumerate(content.split("\n"))
                    if line.strip().startswith("//")
                ]

                self.violations.append(
                    {
                        "path": json_path.relative_to(self.workspace_root),
                        "comment_lines": len(comment_lines),
                        "line_numbers": comment_lines[:10],  # First 10
                        "size_kb": json_path.stat().st_size / 1024,
                    }
                )
            else:
                # Try to parse as valid JSON
                try:
                    data = json.loads(content)
                    has_ainlp = "_ainlp_integration" in data

                    self.valid_files.append(
                        {
                            "path": json_path.relative_to(self.workspace_root),
                            "has_ainlp_metadata": has_ainlp,
                            "size_kb": json_path.stat().st_size / 1024,
                        }
                    )
                except json.JSONDecodeError as e:
                    self.violations.append(
                        {
                            "path": json_path.relative_to(self.workspace_root),
                            "error": f"Invalid JSON: {str(e)}",
                            "size_kb": json_path.stat().st_size / 1024,
                        }
                    )

        except Exception as e:
            print(f"  ⚠️  Error reading {json_path}: {e}")

    def _generate_report(self) -> Dict:
        """Generate comprehensive audit report."""
        total_files = len(self.violations) + len(self.valid_files)
        violation_rate = len(self.violations) / total_files if total_files > 0 else 0

        report = {
            "timestamp": datetime.now().isoformat(),
            "workspace": str(self.workspace_root),
            "summary": {
                "total_json_files": total_files,
                "total_jsonc_files": len(self.jsonc_files),
                "violations": len(self.violations),
                "valid_files": len(self.valid_files),
                "violation_rate": f"{violation_rate * 100:.1f}%",
                "ainlp_compliant": sum(
                    1 for f in self.valid_files if f["has_ainlp_metadata"]
                ),
            },
            "violations": self.violations,
            "valid_files": self.valid_files[:20],  # Top 20
            "recommendations": self._generate_recommendations(),
        }

        return report

    def _generate_recommendations(self) -> List[str]:
        """Generate migration recommendations."""
        recommendations = []

        if self.violations:
            recommendations.append(
                f"🔧 Fix {len(self.violations)} JSON files with comments:"
            )
            recommendations.append("   1. VS Code configs → Rename .json to .jsonc")
            recommendations.append(
                "   2. Data files → Convert comments to semantic metadata"
            )

        ainlp_missing = len(
            [f for f in self.valid_files if not f["has_ainlp_metadata"]]
        )

        if ainlp_missing > 0:
            recommendations.append(
                f"\n📋 Add AINLP metadata to {ainlp_missing} valid JSON files"
            )
            recommendations.append("   Use: runtime/tools/ainlp_json_metadata.py")

        if not self.violations and ainlp_missing == 0:
            recommendations.append("✅ All JSON files are compliant! No action needed.")

        return recommendations

    def print_report(self, report: Dict) -> None:
        """Print human-readable report."""
        print("\n" + "=" * 70)
        print("📊 AINLP JSON Audit Report")
        print("=" * 70)

        summary = report["summary"]
        print(f"\n📈 Summary:")
        print(f"  Total .json files:     {summary['total_json_files']}")
        print(f"  Total .jsonc files:    {summary['total_jsonc_files']}")
        print(
            f"  Files with violations: {summary['violations']} ({summary['violation_rate']})"
        )
        print(f"  Valid JSON files:      {summary['valid_files']}")
        print(f"  AINLP-compliant:       {summary['ainlp_compliant']}")

        if report["violations"]:
            print(f"\n⚠️  Violations Found ({len(report['violations'])} files):")
            for v in report["violations"][:10]:  # Show first 10
                path = v["path"]
                if "comment_lines" in v:
                    print(f"  • {path}")
                    print(
                        f"    {v['comment_lines']} comment lines at: {v['line_numbers']}"
                    )
                elif "error" in v:
                    print(f"  • {path}")
                    print(f"    {v['error']}")

        print(f"\n💡 Recommendations:")
        for rec in report["recommendations"]:
            print(rec)

        # Consciousness calculation
        total = summary["total_json_files"]
        valid = summary["valid_files"]
        ainlp = summary["ainlp_compliant"]

        consciousness = 0.5  # Base
        if total > 0:
            consciousness += 0.3 * (valid / total)  # Validity
            consciousness += 0.2 * (ainlp / total)  # AINLP compliance

        print(f"\n🧬 Workspace JSON Consciousness: {consciousness:.2f}")
        print("=" * 70 + "\n")

    def save_report(self, report: Dict, output_path: Path) -> None:
        """Save detailed report to JSON."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, default=str)

        print(f"📄 Detailed report saved: {output_path}")


def main():
    """Main execution."""
    workspace = Path(__file__).resolve().parents[2]  # Go up to AIOS root

    print("\n🔮 AINLP JSON Audit Tool")
    print("Semantic Metadata Over Syntactic Comments")
    print(f"Workspace: {workspace}\n")

    auditor = AINLPJsonAuditor(workspace)
    report = auditor.scan_workspace()
    auditor.print_report(report)

    # Save detailed report
    report_path = (
        workspace
        / "tachyonic"
        / "archive"
        / f"json_audit_{datetime.now():%Y%m%d_%H%M%S}.json"
    )
    auditor.save_report(report, report_path)

    # Exit code based on violations
    violations = report["summary"]["violations"]
    if violations > 0:
        print(f"⚠️  Found {violations} violations - migration recommended")
        return 1
    else:
        print("✅ All JSON files compliant!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
