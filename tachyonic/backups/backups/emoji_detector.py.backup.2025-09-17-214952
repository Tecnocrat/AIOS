#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AIOS Emoji Detection Utility
============================
Location: ai/laboratory/scripts/emoji_detector.py
Purpose: Detect and report Unicode emoji characters in text files
Architecture: LABORATORY supercell (Analysis & Experimentation)

This utility scans files for Unicode emoji characters that can cause
Windows terminal encoding issues. Designed to integrate with the
AIOS GitHooks governance system.
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

# Emoji detection patterns
EMOJI_PATTERNS = [
    # Basic emoji ranges
    r"[\U0001F600-\U0001F64F]",  # Emoticons
    r"[\U0001F300-\U0001F5FF]",  # Misc Symbols and Pictographs
    r"[\U0001F680-\U0001F6FF]",  # Transport and Map
    r"[\U0001F1E0-\U0001F1FF]",  # Regional indicators
    r"[\U00002600-\U000026FF]",  # Misc symbols
    r"[\U00002700-\U000027BF]",  # Dingbats
    r"[\U0001F900-\U0001F9FF]",  # Supplemental Symbols and Pictographs
    # Common checkmarks and symbols
    r"[]",  # Check marks
    r"[]",  # Common AIOS emojis
    r"[]",  # Architecture emojis
]

# Compile regex for efficiency
EMOJI_REGEX = re.compile("|".join(EMOJI_PATTERNS))


@dataclass
class EmojiMatch:
    """Single emoji detection result"""

    file_path: str
    line_number: int
    column: int
    emoji: str
    unicode_name: str
    context: str


class EmojiDetector:
    """Main emoji detection engine"""

    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path.cwd()
        self.results: List[EmojiMatch] = []

    def scan_file(self, file_path: Path) -> List[EmojiMatch]:
        """Scan a single file for emojis"""
        matches = []

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line_num, line in enumerate(f, 1):
                    for match in EMOJI_REGEX.finditer(line):
                        emoji = match.group()
                        context = line.strip()

                        # Get Unicode name
                        try:
                            unicode_name = f"U+{ord(emoji):04X}"
                        except:
                            unicode_name = "Unknown"

                        matches.append(
                            EmojiMatch(
                                file_path=str(file_path),
                                line_number=line_num,
                                column=match.start() + 1,
                                emoji=emoji,
                                unicode_name=unicode_name,
                                context=context,
                            )
                        )

        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")

        return matches

    def scan_directory(
        self, directory: Path, extensions: List[str] = None
    ) -> List[EmojiMatch]:
        """Scan directory for emoji usage"""
        if extensions is None:
            extensions = [
                ".md",
                ".py",
                ".ps1",
                ".txt",
                ".json",
                ".yaml",
                ".yml",
            ]

        all_matches = []

        for ext in extensions:
            for file_path in directory.rglob(f"*{ext}"):
                if file_path.is_file():
                    matches = self.scan_file(file_path)
                    all_matches.extend(matches)

        return all_matches

    def generate_report(
        self, matches: List[EmojiMatch], output_format: str = "console"
    ) -> str:
        """Generate detection report"""
        if not matches:
            return "No emoji characters detected."

        if output_format == "console":
            return self._console_report(matches)
        elif output_format == "json":
            return self._json_report(matches)
        else:
            return self._detailed_report(matches)

    def _console_report(self, matches: List[EmojiMatch]) -> str:
        """Console-friendly report"""
        report = []
        report.append(f"\nEMOJI DETECTION REPORT")
        report.append(f"======================")
        report.append(f"Total emojis found: {len(matches)}")
        report.append("")

        # Group by file
        by_file = {}
        for match in matches:
            if match.file_path not in by_file:
                by_file[match.file_path] = []
            by_file[match.file_path].append(match)

        for file_path, file_matches in by_file.items():
            rel_path = os.path.relpath(file_path, self.workspace_root)
            report.append(f"File: {rel_path}")
            for match in file_matches:
                report.append(
                    f"  Line {match.line_number}: '{match.emoji}' ({match.unicode_name})"
                )
                report.append(f"    Context: {match.context}")
            report.append("")

        return "\n".join(report)

    def _json_report(self, matches: List[EmojiMatch]) -> str:
        """JSON report for programmatic use"""
        import json

        data = {
            "total_matches": len(matches),
            "scan_timestamp": str(datetime.now()),
            "matches": [
                {
                    "file": match.file_path,
                    "line": match.line_number,
                    "column": match.column,
                    "emoji": match.emoji,
                    "unicode": match.unicode_name,
                    "context": match.context,
                }
                for match in matches
            ],
        }
        return json.dumps(data, indent=2)

    def _detailed_report(self, matches: List[EmojiMatch]) -> str:
        """Detailed analysis report"""
        report = []
        report.append("EMOJI DETECTION ANALYSIS")
        report.append("========================")

        # Statistics
        emoji_counts = {}
        file_counts = {}

        for match in matches:
            emoji_counts[match.emoji] = emoji_counts.get(match.emoji, 0) + 1
            file_counts[match.file_path] = (
                file_counts.get(match.file_path, 0) + 1
            )

        report.append(f"\nMost common emojis:")
        for emoji, count in sorted(
            emoji_counts.items(), key=lambda x: x[1], reverse=True
        ):
            try:
                name = f"U+{ord(emoji):04X}"
            except:
                name = "Unknown"
            report.append(f"  {emoji} ({name}): {count} occurrences")

        report.append(f"\nFiles with most emojis:")
        for file_path, count in sorted(
            file_counts.items(), key=lambda x: x[1], reverse=True
        )[:10]:
            rel_path = os.path.relpath(file_path, self.workspace_root)
            report.append(f"  {rel_path}: {count} emojis")

        return "\n".join(report)


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AIOS Emoji Detection Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python emoji_detector.py                    # Scan current directory
  python emoji_detector.py --target ../docs  # Scan specific directory
  python emoji_detector.py --format json     # JSON output
  python emoji_detector.py --extensions .md .py  # Specific file types
        """,
    )

    parser.add_argument(
        "--target",
        "-t",
        type=Path,
        default=Path.cwd(),
        help="Directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["console", "json", "detailed"],
        default="console",
        help="Output format",
    )
    parser.add_argument(
        "--extensions",
        "-e",
        nargs="+",
        default=[".md", ".py", ".ps1", ".txt", ".json"],
        help="File extensions to scan",
    )
    parser.add_argument(
        "--output", "-o", type=Path, help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    # Initialize detector
    detector = EmojiDetector(workspace_root=args.target)

    # Scan for emojis
    print(f"Scanning {args.target} for emoji characters...")
    matches = detector.scan_directory(args.target, args.extensions)

    # Generate report
    report = detector.generate_report(matches, args.format)

    # Output report
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to {args.output}")
    else:
        print(report)

    # Exit code
    return len(matches)


if __name__ == "__main__":
    from datetime import datetime

    sys.exit(main())
