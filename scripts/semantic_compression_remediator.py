#!/usr/bin/env python3
"""
AINLP Semantic Compression Remediation System
Automatically fixes intelligence delimitation issues identified by code review.
"""

import json
from pathlib import Path
from datetime import datetime
import logging
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SemanticCompressionRemediator:
    """Automatically remediates semantic compression issues."""

    def __init__(self, report_path: str):
        self.report_path = Path(report_path)
        self.compression_rules = {
            'runtime_intelligence': 'runtime',
            'intelligence_layer': 'ai',
            'intelligence_engine': 'engine',
            'intelligence_module': 'module',
            'intelligence_core': 'core',
            'intelligence_system': 'system',
            'intelligence_tools': 'tools',
            'intelligence_analysis': 'analysis',
            'intelligence_monitor': 'monitor',
            'intelligence_bridge': 'bridge',
            'intelligence_validator': 'validator',
            'intelligence_dashboard': 'dashboard',
            'intelligence_archive': 'archive',
            'intelligence_report': 'report',
            'intelligence_state': 'state',
            'intelligence_config': 'config',
            'intelligence_data': 'data',
            'intelligence_metrics': 'metrics',
            'intelligence_health': 'health',
            'intelligence_status': 'status'
        }
        self.stats = {
            'files_processed': 0,
            'issues_fixed': 0,
            'files_modified': 0
        }

    def load_report(self) -> dict:
        """Load the code review report."""
        if not self.report_path.exists():
            raise FileNotFoundError(f"Report not found: {self.report_path}")

        with open(self.report_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def extract_delimitation_issues(self, report: dict) -> list:
        """Extract intelligence delimitation issues from report."""
        delimitation_issues = []

        for issue in report.get('issues', []):
            if issue.get('issue_type') == 'intelligence_delimitation':
                delimitation_issues.append({
                    'file': issue['file_path'],
                    'line': issue['line_number'],
                    'pattern': issue.get('pattern', self._extract_pattern_from_message(issue['message'])),
                    'replacement': issue.get('replacement', self._extract_replacement_from_message(issue['message'])),
                    'severity': issue['severity']
                })

        return delimitation_issues

    def _extract_pattern_from_message(self, message: str) -> str:
        """Extract pattern from issue message."""
        # Message format: "Found 'pattern' that should be compressed to 'replacement'"
        match = re.search(r"Found '([^']+)' that should be compressed to '([^']+)'", message)
        return match.group(1) if match else ""

    def _extract_replacement_from_message(self, message: str) -> str:
        """Extract replacement from issue message."""
        # Message format: "Found 'pattern' that should be compressed to 'replacement'"
        match = re.search(r"Found '([^']+)' that should be compressed to '([^']+)'", message)
        return match.group(2) if match else ""

    def apply_compression_fix(
        self, file_path: str, pattern: str, replacement: str
    ) -> bool:
        """Apply semantic compression fix to a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Apply the fix
            original_content = content
            content = content.replace(pattern, replacement)

            # Only write if content changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"Fixed {pattern} -> {replacement} in {file_path}")
                return True

        except Exception as e:
            logger.error(f"Error fixing {file_path}: {e}")

        return False

    def remediate_issues(self, issues: list) -> dict:
        """Remediate all intelligence delimitation issues."""
        logger.info(
            f"Starting remediation of {len(issues)} "
            "intelligence delimitation issues"
        )

        files_modified = set()

        for issue in issues:
            file_path = issue['file']
            pattern = issue['pattern']
            replacement = issue['replacement']

            if self.apply_compression_fix(file_path, pattern, replacement):
                self.stats['issues_fixed'] += 1
                files_modified.add(file_path)

        self.stats['files_modified'] = len(files_modified)
        self.stats['files_processed'] = len(
            set(issue['file'] for issue in issues)
        )

        logger.info(
            f"Remediation complete: {self.stats['issues_fixed']} "
            f"issues fixed in {self.stats['files_modified']} files"
        )

        return self.stats

    def generate_remediation_report(self, output_dir: str) -> str:
        """Generate remediation report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(output_dir) / \
            f"semantic_compression_remediation_{timestamp}.json"

        report = {
            'timestamp': datetime.now().isoformat(),
            'remediator_version': '1.0.0',
            'stats': self.stats,
            'compression_rules_applied': self.compression_rules,
            'report_path': str(self.report_path)
        }

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        logger.info(f"Remediation report saved: {report_path}")
        return str(report_path)


def main():
    """Main remediation execution."""
    import argparse

    parser = argparse.ArgumentParser(
        description='AINLP Semantic Compression Remediation'
    )
    parser.add_argument(
        '--report', required=True,
        help='Path to code review report JSON'
    )
    parser.add_argument(
        '--output-dir', default='tachyonic/archive/runtime',
        help='Output directory for reports'
    )

    args = parser.parse_args()

    # Initialize remediator
    remediator = SemanticCompressionRemediator(args.report)

    try:
        # Load and process report
        report = remediator.load_report()
        issues = remediator.extract_delimitation_issues(report)

        if not issues:
            logger.info("No intelligence delimitation issues found to remediate")
            return

        # Apply remediation
        stats = remediator.remediate_issues(issues)

        # Generate report
        report_path = remediator.generate_remediation_report(args.output_dir)

        # Print summary
        print("\n" + "="*60)
        print("AINLP SEMANTIC COMPRESSION REMEDIATION COMPLETE")
        print("="*60)
        print(f"Files Processed: {stats['files_processed']}")
        print(f"Issues Fixed: {stats['issues_fixed']}")
        print(f"Files Modified: {stats['files_modified']}")
        print(f"Report: {report_path}")
        print("="*60)

    except Exception as e:
        logger.error(f"Remediation failed: {e}")
        raise


if __name__ == '__main__':
    main()