#!/usr/bin/env python3
"""
AIOS Documentation Tachyonic Cleanup and Optimization Script
==========================================================

This script implements tachyonic paradigm-based documentation cleanup:
- Identifies redundant and fragmented documentation
- Archives legacy content using quantum-inspired storage
- Maintains unified backup structure with perfect recall
- Optimizes logical organization following tachyonic principles

Usage:
    python docs_tachyonic_cleanup.py [--dry-run] [--verbose]
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Add the AIOS AI source path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "ai" / "src"))

from maintenance.tachyonic_archiver import TachyonicArchiver


class TachyonicDocumentationOptimizer:
    """
    Implements tachyonic-paradigm based documentation optimization.

    Tachyonic Principles:
    1. Information coherence across time dimensions
    2. Quantum superposition of document states
    3. Holographic reconstruction capabilities
    4. Temporal optimization through archival
    """

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.docs_path = self.workspace_root / "docs"
        self.archiver = TachyonicArchiver(workspace_root)
        self.backup_path = self.docs_path / "unified_backups"
        self.backup_path.mkdir(exist_ok=True)

        # Tachyonic document categories
        self.categories = {
            "core": ["ARCHITECTURE", "DEVELOPMENT", "API", "INSTALLATION"],
            "status": ["STATUS", "INTEGRATION", "COMPLETE", "INFRASTRUCTURE"],
            "guides": ["GUIDE", "SPECIFICATION", "REFERENCE"],
            "vscode": ["VSCODE", "EXTENSION"],
            "legacy": ["CHANGELOG", "ROADMAP", "TROUBLESHOOTING"],
            "ai_context": ["AI_", "CONTEXT", "QUICK_REFERENCE"]
        }

    def analyze_documentation_structure(self) -> Dict:
        """Analyze current documentation structure using tachyonic principles."""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_files": 0,
            "redundant_patterns": [],
            "fragmented_content": [],
            "optimization_candidates": [],
            "tachyonic_coherence_score": 0.0
        }

        md_files = list(self.docs_path.glob("*.md"))
        analysis["total_files"] = len(md_files)

        # Detect redundant patterns
        filename_groups = self._group_by_similarity(md_files)
        for group, files in filename_groups.items():
            if len(files) > 1:
                analysis["redundant_patterns"].append({
                    "pattern": group,
                    "files": [f.name for f in files],
                    "count": len(files)
                })

        # Detect fragmented content
        content_analysis = self._analyze_content_fragmentation(md_files)
        analysis["fragmented_content"] = content_analysis

        # Calculate tachyonic coherence score
        analysis["tachyonic_coherence_score"] = self._calculate_coherence_score(md_files)

        return analysis

    def _group_by_similarity(self, files: List[Path]) -> Dict[str, List[Path]]:
        """Group files by name similarity patterns."""
        groups = {}

        for file in files:
            # Extract base pattern (remove dates, numbers, modifiers)
            base_name = file.stem

            # Remove common suffixes
            suffixes = ["_COMPLETE", "_GUIDE", "_2025", "_JULY", "_STATUS"]
            for suffix in suffixes:
                base_name = base_name.replace(suffix, "")

            # Group by prefix
            if base_name.startswith("AIOS_"):
                prefix = base_name.split("_")[0] + "_" + base_name.split("_")[1]
            else:
                prefix = base_name.split("_")[0]

            if prefix not in groups:
                groups[prefix] = []
            groups[prefix].append(file)

        return groups

    def _analyze_content_fragmentation(self, files: List[Path]) -> List[Dict]:
        """Analyze content fragmentation using tachyonic principles."""
        fragmentation = []

        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Analyze content structure
                lines = content.split('\n')
                headers = [line for line in lines if line.startswith('#')]

                fragmentation.append({
                    "filename": file.name,
                    "size": len(content),
                    "lines": len(lines),
                    "headers": len(headers),
                    "fragmentation_score": self._calculate_fragmentation_score(content)
                })

            except Exception as e:
                fragmentation.append({
                    "filename": file.name,
                    "error": str(e),
                    "fragmentation_score": 1.0
                })

        return fragmentation

    def _calculate_fragmentation_score(self, content: str) -> float:
        """Calculate content fragmentation score (0.0 = coherent, 1.0 = fragmented)."""
        lines = content.split('\n')

        # Factors indicating fragmentation
        empty_lines = len([line for line in lines if not line.strip()])
        short_lines = len([line for line in lines if len(line.strip()) < 20])
        todo_markers = content.count('TODO') + content.count('FIXME')

        # Calculate score
        total_lines = len(lines)
        if total_lines == 0:
            return 1.0

        fragmentation_score = (empty_lines * 0.1 + short_lines * 0.2 + todo_markers * 0.3) / total_lines
        return min(fragmentation_score, 1.0)

    def _calculate_coherence_score(self, files: List[Path]) -> float:
        """Calculate overall tachyonic coherence score."""
        if not files:
            return 0.0

        coherence_factors = []

        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Coherence indicators
                has_structure = bool(content.count('##') > 2)
                has_toc = 'table of contents' in content.lower() or '## contents' in content.lower()
                has_clear_title = content.startswith('#')
                appropriate_length = 1000 < len(content) < 10000

                coherence = sum([has_structure, has_toc, has_clear_title, appropriate_length]) / 4
                coherence_factors.append(coherence)

            except:
                coherence_factors.append(0.0)

        return sum(coherence_factors) / len(coherence_factors)

    def optimize_documentation(self, dry_run: bool = False) -> Dict:
        """Execute tachyonic optimization of documentation."""
        optimization_result = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "operations": [],
            "archived_files": [],
            "unified_files": [],
            "errors": []
        }

        # Step 1: Analyze current state
        analysis = self.analyze_documentation_structure()
        optimization_result["initial_analysis"] = analysis

        # Step 2: Identify optimization candidates
        candidates = self._identify_optimization_candidates()

        # Step 3: Archive redundant files
        archive_result = self._archive_redundant_files(candidates["archive"], dry_run)
        optimization_result["archived_files"] = archive_result

        # Step 4: Consolidate fragmented content
        consolidation_result = self._consolidate_fragmented_content(candidates["consolidate"], dry_run)
        optimization_result["unified_files"] = consolidation_result

        # Step 5: Update documentation index
        if not dry_run:
            self._update_documentation_index()

        return optimization_result

    def _identify_optimization_candidates(self) -> Dict:
        """Identify files for archival and consolidation."""
        candidates = {
            "archive": [],
            "consolidate": [],
            "preserve": []
        }

        md_files = list(self.docs_path.glob("*.md"))

        # Categorize files
        for file in md_files:
            filename = file.name.upper()

            # Check if file should be archived
            if self._should_archive_file(filename):
                candidates["archive"].append(file)
            # Check if file should be consolidated
            elif self._should_consolidate_file(filename):
                candidates["consolidate"].append(file)
            else:
                candidates["preserve"].append(file)

        return candidates

    def _should_archive_file(self, filename: str) -> bool:
        """Determine if file should be archived based on tachyonic principles."""
        archive_patterns = [
            "CHANGELOG",
            "ROADMAP",
            "TROUBLESHOOTING",
            "_OLD",
            "_BACKUP",
            "_DEPRECATED",
            "JULY_2025" if datetime.now().month > 7 else "NEVER_MATCH"
        ]

        return any(pattern in filename for pattern in archive_patterns)

    def _should_consolidate_file(self, filename: str) -> bool:
        """Determine if file should be consolidated."""
        consolidation_patterns = [
            "AIOS_COMPLETE_SPECIFICATION",
            "AIOS_DEVELOPMENT_AND_SETUP",
            "AIOS_ARCHITECTURE_AND_DESIGN",
            "AIOS_API_AND_REFERENCE",
            "AIOS_OPTIMIZATION_AND_TROUBLESHOOTING",
            "AIOS_PROJECT_STATUS_AND_ROADMAP",
            "AIOS_SPECIALIZED_INTEGRATIONS"
        ]

        return any(pattern in filename for pattern in consolidation_patterns)

    def _archive_redundant_files(self, files: List[Path], dry_run: bool) -> List[Dict]:
        """Archive redundant files using tachyonic archiver."""
        archive_results = []

        for file in files:
            try:
                category = self._determine_category(file.name)

                if not dry_run:
                    success = self.archiver.archive_file(file, category)
                    if success:
                        file.unlink()  # Remove original file
                        archive_results.append({
                            "file": file.name,
                            "category": category,
                            "status": "archived",
                            "timestamp": datetime.now().isoformat()
                        })
                    else:
                        archive_results.append({
                            "file": file.name,
                            "status": "failed",
                            "error": "Archive operation failed"
                        })
                else:
                    archive_results.append({
                        "file": file.name,
                        "category": category,
                        "status": "would_archive",
                        "dry_run": True
                    })

            except Exception as e:
                archive_results.append({
                    "file": file.name,
                    "status": "error",
                    "error": str(e)
                })

        return archive_results

    def _consolidate_fragmented_content(self, files: List[Path], dry_run: bool) -> List[Dict]:
        """Consolidate fragmented content into unified documents."""
        consolidation_results = []

        # Group files by consolidation target
        consolidation_groups = self._group_for_consolidation(files)

        for target_name, source_files in consolidation_groups.items():
            try:
                if not dry_run:
                    consolidated_content = self._merge_content(source_files)
                    target_path = self.docs_path / f"{target_name}.md"

                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write(consolidated_content)

                    # Archive source files
                    for source_file in source_files:
                        self.archiver.archive_file(source_file, "consolidated")
                        source_file.unlink()

                    consolidation_results.append({
                        "target": target_name,
                        "source_files": [f.name for f in source_files],
                        "status": "consolidated",
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    consolidation_results.append({
                        "target": target_name,
                        "source_files": [f.name for f in source_files],
                        "status": "would_consolidate",
                        "dry_run": True
                    })

            except Exception as e:
                consolidation_results.append({
                    "target": target_name,
                    "status": "error",
                    "error": str(e)
                })

        return consolidation_results

    def _group_for_consolidation(self, files: List[Path]) -> Dict[str, List[Path]]:
        """Group files for consolidation based on semantic similarity."""
        groups = {}

        for file in files:
            filename = file.name.upper()

            # Determine consolidation target
            if "SPECIFICATION" in filename or "GUIDE" in filename:
                target = "AIOS_MASTER_SPECIFICATION"
            elif "DEVELOPMENT" in filename or "SETUP" in filename:
                target = "AIOS_DEVELOPER_GUIDE"
            elif "ARCHITECTURE" in filename or "DESIGN" in filename:
                target = "AIOS_ARCHITECTURE_GUIDE"
            elif "API" in filename or "REFERENCE" in filename:
                target = "AIOS_API_REFERENCE"
            elif "STATUS" in filename or "ROADMAP" in filename:
                target = "AIOS_PROJECT_STATUS"
            else:
                target = "AIOS_MISCELLANEOUS"

            if target not in groups:
                groups[target] = []
            groups[target].append(file)

        return groups

    def _merge_content(self, files: List[Path]) -> str:
        """Merge multiple files into unified content."""
        merged_content = []

        # Add header
        merged_content.append("# AIOS Unified Documentation")
        merged_content.append("")
        merged_content.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        merged_content.append("")
        merged_content.append("## Table of Contents")
        merged_content.append("")

        # Collect all content
        sections = []
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract title
                title = file.stem.replace('_', ' ').title()
                sections.append({
                    "title": title,
                    "content": content,
                    "filename": file.name
                })

                # Add to TOC
                merged_content.append(f"- [{title}](#{title.lower().replace(' ', '-')})")

            except Exception as e:
                merged_content.append(f"- Error reading {file.name}: {e}")

        merged_content.append("")
        merged_content.append("---")
        merged_content.append("")

        # Add all sections
        for section in sections:
            merged_content.append(f"## {section['title']}")
            merged_content.append("")
            merged_content.append(f"*Source: {section['filename']}*")
            merged_content.append("")
            merged_content.append(section['content'])
            merged_content.append("")
            merged_content.append("---")
            merged_content.append("")

        return "\n".join(merged_content)

    def _determine_category(self, filename: str) -> str:
        """Determine category for archival."""
        filename_upper = filename.upper()

        for category, patterns in self.categories.items():
            if any(pattern in filename_upper for pattern in patterns):
                return category

        return "general"

    def _update_documentation_index(self):
        """Update the documentation index after optimization."""
        index_path = self.docs_path / "DOCUMENTATION_INDEX.md"

        # This would update the index with new structure
        # Implementation depends on current index format
        pass

    def generate_optimization_report(self, results: Dict) -> str:
        """Generate a comprehensive optimization report."""
        report = []

        report.append("# AIOS Documentation Tachyonic Optimization Report")
        report.append("")
        report.append(f"**Generated:** {results['timestamp']}")
        report.append(f"**Mode:** {'Dry Run' if results['dry_run'] else 'Live Execution'}")
        report.append("")

        # Initial analysis
        if "initial_analysis" in results:
            analysis = results["initial_analysis"]
            report.append("## Initial Analysis")
            report.append("")
            report.append(f"- **Total Files:** {analysis['total_files']}")
            report.append(f"- **Tachyonic Coherence Score:** {analysis['tachyonic_coherence_score']:.2f}")
            report.append(f"- **Redundant Patterns:** {len(analysis['redundant_patterns'])}")
            report.append(f"- **Fragmented Content:** {len(analysis['fragmented_content'])}")
            report.append("")

        # Archival results
        if results["archived_files"]:
            report.append("## Archived Files")
            report.append("")
            for item in results["archived_files"]:
                status = item["status"]
                report.append(f"- **{item['file']}** → {status}")
            report.append("")

        # Consolidation results
        if results["unified_files"]:
            report.append("## Unified Files")
            report.append("")
            for item in results["unified_files"]:
                report.append(f"- **{item['target']}** ← {len(item['source_files'])} files")
            report.append("")

        return "\n".join(report)


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(description="AIOS Documentation Tachyonic Optimizer")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without executing")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    parser.add_argument("--workspace", default=".", help="Workspace root directory")

    args = parser.parse_args()

    # Initialize optimizer
    optimizer = TachyonicDocumentationOptimizer(args.workspace)

    print("🚀 AIOS Documentation Tachyonic Optimizer")
    print("=" * 50)

    # Run optimization
    results = optimizer.optimize_documentation(dry_run=args.dry_run)

    # Generate report
    report = optimizer.generate_optimization_report(results)

    if args.verbose:
        print("\n" + report)

    # Save report
    report_path = Path(args.workspace) / "docs" / "unified_backups" / f"optimization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✅ Optimization complete! Report saved to: {report_path}")


if __name__ == "__main__":
    main()
