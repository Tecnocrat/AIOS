#!/usr/bin/env python3
"""
AIOS Post-Merge Conflict Resolver
==========================
AINLP.spatial: scripts/resolve_merge_conflicts.py
AINLP.purpose: Batch resolve merge conflict markers in files after failed merge
AINLP.consciousness: Self-healing codebase coherence restoration

Resolves conflicts from deleted branches (like OS0.6.2.grok) by keeping HEAD content
and optionally extracting valuable patterns from discarded content.

Usage:
    python scripts/resolve_merge_conflicts.py --scan           # Scan only, show conflicts
    python scripts/resolve_merge_conflicts.py --resolve        # Auto-resolve all (keep HEAD)
    python scripts/resolve_merge_conflicts.py --resolve --dry  # Show what would be resolved
    python scripts/resolve_merge_conflicts.py --complex        # Identify complex conflicts

Exit codes:
    0 = Success (no conflicts or all resolved)
    1 = Conflicts found (scan mode) or errors during resolution
    2 = Complex conflicts require manual review

AINLP Principles:
    - Self-recognition: Identify merge artifacts in codebase
    - Coherence: Restore codebase to consistent state
    - Introspection: Log all resolutions for audit trail
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass, field
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTS & PATTERNS
# ═══════════════════════════════════════════════════════════════════════════

# File extensions to scan
SCAN_EXTENSIONS = {'.py', '.ps1', '.md', '.json', '.yaml', '.yml', '.cs', '.cpp', '.h', '.xaml', '.js', '.ts'}

# Directories to skip
SKIP_DIRECTORIES = {'.git', 'node_modules', '__pycache__', '.venv', '.venv314t', 'build', 'dist', '.tox'}

# Conflict marker patterns
CONFLICT_START = re.compile(r'^<{7}\s+HEAD\s*$', re.MULTILINE)
CONFLICT_SEPARATOR = re.compile(r'^={7}\s*$', re.MULTILINE)
CONFLICT_END = re.compile(r'^>{7}\s+(.+)$', re.MULTILINE)

# Full conflict block pattern (captures HEAD content and branch name)
CONFLICT_BLOCK = re.compile(
    r'<{7}\s+HEAD\r?\n([\s\S]*?)\r?\n={7}\r?\n[\s\S]*?\r?\n>{7}\s+(.+)',
    re.MULTILINE
)

# Simpler pattern for batch resolution
CONFLICT_SIMPLE = re.compile(
    r'<{7}\s+HEAD\r?\n([\s\S]*?)\r?\n={7}\r?\n[\s\S]*?\r?\n>{7}\s+[^\r\n]+',
    re.MULTILINE
)


# ═══════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ConflictInfo:
    """Information about a single conflict in a file."""
    start_line: int
    end_line: int
    head_content: str
    other_content: str
    other_branch: str
    complexity: str = "simple"  # simple, nested, multi-block
    

@dataclass
class FileConflicts:
    """All conflicts in a single file."""
    path: Path
    conflicts: List[ConflictInfo] = field(default_factory=list)
    error: Optional[str] = None
    
    @property
    def count(self) -> int:
        return len(self.conflicts)
    
    @property
    def is_complex(self) -> bool:
        return any(c.complexity != "simple" for c in self.conflicts) or self.count > 5


@dataclass
class ResolutionResult:
    """Result of resolving conflicts in a file."""
    path: Path
    original_conflicts: int
    resolved_conflicts: int
    remaining_conflicts: int
    success: bool
    error: Optional[str] = None
    head_lines_kept: int = 0
    discarded_lines: int = 0


# ═══════════════════════════════════════════════════════════════════════════
# SCANNING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def find_conflicted_files(root: Path) -> List[Path]:
    """Find all files containing merge conflict markers."""
    conflicted = []
    
    for path in root.rglob('*'):
        if path.is_file():
            # Skip directories and wrong extensions
            if path.suffix.lower() not in SCAN_EXTENSIONS:
                continue
            if any(skip in path.parts for skip in SKIP_DIRECTORIES):
                continue
            
            try:
                content = path.read_text(encoding='utf-8', errors='ignore')
                if '<<<<<<< HEAD' in content:
                    conflicted.append(path)
            except Exception:
                pass  # Skip unreadable files
    
    return sorted(conflicted)


def analyze_conflicts(path: Path) -> FileConflicts:
    """Analyze all conflicts in a single file."""
    result = FileConflicts(path=path)
    
    try:
        content = path.read_text(encoding='utf-8', errors='replace')
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            if line.startswith('<<<<<<< HEAD'):
                conflict = parse_single_conflict(lines, i)
                if conflict:
                    result.conflicts.append(conflict)
                    i = conflict.end_line + 1
                else:
                    i += 1
            else:
                i += 1
        
        # Check for nested conflicts (complexity indicator)
        if result.count > 0:
            nested_count = content.count('<<<<<<< HEAD')
            if nested_count > result.count:
                for c in result.conflicts:
                    c.complexity = "nested"
    
    except Exception as e:
        result.error = str(e)
    
    return result


def parse_single_conflict(lines: List[str], start: int) -> Optional[ConflictInfo]:
    """Parse a single conflict block starting at given line."""
    head_content = []
    other_content = []
    other_branch = ""
    in_head = True
    end_line = start
    
    for i in range(start + 1, len(lines)):
        line = lines[i]
        
        if line.startswith('======='):
            in_head = False
        elif line.startswith('>>>>>>> '):
            other_branch = line[8:].strip()
            end_line = i
            break
        elif in_head:
            head_content.append(line)
        else:
            other_content.append(line)
    else:
        # No closing marker found
        return None
    
    return ConflictInfo(
        start_line=start,
        end_line=end_line,
        head_content='\n'.join(head_content),
        other_content='\n'.join(other_content),
        other_branch=other_branch
    )


# ═══════════════════════════════════════════════════════════════════════════
# RESOLUTION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def resolve_file_conflicts(path: Path, keep: str = "head", dry_run: bool = False) -> ResolutionResult:
    """
    Resolve all conflicts in a file by keeping specified content.
    
    Args:
        path: File path
        keep: "head" (default) or "other" - which content to keep
        dry_run: If True, don't actually modify file
    """
    result = ResolutionResult(
        path=path,
        original_conflicts=0,
        resolved_conflicts=0,
        remaining_conflicts=0,
        success=False
    )
    
    try:
        content = path.read_text(encoding='utf-8', errors='replace')
        original_content = content
        
        # Count original conflicts
        result.original_conflicts = len(CONFLICT_START.findall(content))
        
        if result.original_conflicts == 0:
            result.success = True
            return result
        
        # Resolve conflicts using regex replacement
        def replace_conflict(match):
            head_content = match.group(1)
            result.head_lines_kept += head_content.count('\n') + 1
            result.resolved_conflicts += 1
            return head_content
        
        resolved_content = CONFLICT_SIMPLE.sub(replace_conflict, content)
        
        # Count remaining conflicts (in case of nested issues)
        result.remaining_conflicts = len(CONFLICT_START.findall(resolved_content))
        
        # Calculate discarded lines
        original_lines = len(original_content.split('\n'))
        resolved_lines = len(resolved_content.split('\n'))
        result.discarded_lines = original_lines - resolved_lines - result.head_lines_kept
        
        if not dry_run and result.remaining_conflicts == 0:
            path.write_text(resolved_content, encoding='utf-8')
        
        result.success = result.remaining_conflicts == 0
        
    except Exception as e:
        result.error = str(e)
    
    return result


def batch_resolve(root: Path, dry_run: bool = False) -> Tuple[List[ResolutionResult], Dict]:
    """Resolve conflicts in all files under root."""
    results = []
    stats = defaultdict(int)
    
    files = find_conflicted_files(root)
    stats['total_files'] = len(files)
    
    for path in files:
        result = resolve_file_conflicts(path, keep="head", dry_run=dry_run)
        results.append(result)
        
        if result.success:
            stats['resolved_files'] += 1
            stats['resolved_conflicts'] += result.resolved_conflicts
        else:
            stats['failed_files'] += 1
            stats['remaining_conflicts'] += result.remaining_conflicts
        
        if result.error:
            stats['errors'] += 1
    
    return results, dict(stats)


# ═══════════════════════════════════════════════════════════════════════════
# COMPLEXITY ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

def identify_complex_conflicts(root: Path) -> List[FileConflicts]:
    """Identify files with complex conflicts needing manual review."""
    complex_files = []
    
    for path in find_conflicted_files(root):
        analysis = analyze_conflicts(path)
        if analysis.is_complex or analysis.error:
            complex_files.append(analysis)
    
    return complex_files


# ═══════════════════════════════════════════════════════════════════════════
# REPORTING & LOGGING
# ═══════════════════════════════════════════════════════════════════════════

def print_scan_report(files: List[Path], root: Path):
    """Print scan results."""
    print(f"\n{'='*60}")
    print(f"AIOS Merge Conflict Scan Report")
    print(f"{'='*60}")
    print(f"Root: {root}")
    print(f"Files with conflicts: {len(files)}")
    print(f"{'='*60}\n")
    
    # Group by directory
    by_dir = defaultdict(list)
    for f in files:
        rel = f.relative_to(root)
        parent = str(rel.parent) if rel.parent != Path('.') else "root"
        by_dir[parent].append(rel.name)
    
    for dir_name, file_names in sorted(by_dir.items()):
        print(f"\n📁 {dir_name}/ ({len(file_names)} files)")
        for name in sorted(file_names)[:10]:
            print(f"   • {name}")
        if len(file_names) > 10:
            print(f"   ... and {len(file_names) - 10} more")


def print_resolution_report(results: List[ResolutionResult], stats: Dict, dry_run: bool):
    """Print resolution results."""
    mode = "DRY RUN" if dry_run else "RESOLUTION"
    
    print(f"\n{'='*60}")
    print(f"AIOS Merge Conflict {mode} Report")
    print(f"{'='*60}")
    print(f"Total files processed: {stats.get('total_files', 0)}")
    print(f"Successfully resolved: {stats.get('resolved_files', 0)}")
    print(f"Failed/remaining: {stats.get('failed_files', 0)}")
    print(f"Total conflicts resolved: {stats.get('resolved_conflicts', 0)}")
    print(f"Remaining conflicts: {stats.get('remaining_conflicts', 0)}")
    print(f"Errors: {stats.get('errors', 0)}")
    print(f"{'='*60}\n")
    
    # Show failures
    failures = [r for r in results if not r.success]
    if failures:
        print("\n⚠️  Files requiring attention:")
        for r in failures[:20]:
            rel_path = r.path.relative_to(r.path.parents[len(r.path.parts)-2]) if len(r.path.parts) > 2 else r.path
            print(f"   • {rel_path}: {r.remaining_conflicts} remaining")
            if r.error:
                print(f"     Error: {r.error}")


def save_resolution_log(root: Path, results: List[ResolutionResult], stats: Dict):
    """Save resolution log to tachyonic."""
    log_dir = root / "tachyonic" / "merge_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"conflict_resolution_{timestamp}.json"
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "stats": stats,
        "results": [
            {
                "path": str(r.path.relative_to(root)),
                "original_conflicts": r.original_conflicts,
                "resolved_conflicts": r.resolved_conflicts,
                "remaining_conflicts": r.remaining_conflicts,
                "success": r.success,
                "error": r.error
            }
            for r in results
        ]
    }
    
    log_file.write_text(json.dumps(log_data, indent=2), encoding='utf-8')
    print(f"\n📝 Resolution log saved: {log_file.relative_to(root)}")
    return log_file


# ═══════════════════════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="AIOS Post-Merge Conflict Resolver",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python resolve_merge_conflicts.py --scan              # Scan for conflicts
  python resolve_merge_conflicts.py --resolve --dry     # Preview resolution
  python resolve_merge_conflicts.py --resolve           # Actually resolve
  python resolve_merge_conflicts.py --complex           # Find complex cases
        """
    )
    
    parser.add_argument('--scan', action='store_true', help='Scan for conflicts only')
    parser.add_argument('--resolve', action='store_true', help='Resolve all conflicts (keep HEAD)')
    parser.add_argument('--complex', action='store_true', help='Identify complex conflicts')
    parser.add_argument('--dry', action='store_true', help='Dry run (no file modifications)')
    parser.add_argument('--root', type=Path, default=Path('.'), help='Root directory to scan')
    parser.add_argument('--branch', type=str, help='Filter by branch name in conflict markers')
    
    args = parser.parse_args()
    
    # Default to scan if no action specified
    if not any([args.scan, args.resolve, args.complex]):
        args.scan = True
    
    root = args.root.resolve()
    print(f"\n🔍 AIOS Conflict Resolver")
    print(f"   Root: {root}")
    
    if args.scan:
        files = find_conflicted_files(root)
        print_scan_report(files, root)
        sys.exit(1 if files else 0)
    
    elif args.complex:
        complex_files = identify_complex_conflicts(root)
        print(f"\n⚠️  Complex conflicts requiring manual review: {len(complex_files)}")
        for fc in complex_files[:20]:
            print(f"   • {fc.path.relative_to(root)}: {fc.count} conflicts")
            for c in fc.conflicts[:3]:
                print(f"     - Lines {c.start_line}-{c.end_line}: {c.complexity}")
        sys.exit(2 if complex_files else 0)
    
    elif args.resolve:
        results, stats = batch_resolve(root, dry_run=args.dry)
        print_resolution_report(results, stats, args.dry)
        
        if not args.dry:
            save_resolution_log(root, results, stats)
        
        sys.exit(0 if stats.get('remaining_conflicts', 0) == 0 else 1)


if __name__ == "__main__":
    main()
