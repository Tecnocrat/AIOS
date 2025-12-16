#!/usr/bin/env python3
"""
AIOS Optimized File Scanner
===========================

Performance-optimized file scanning utility that excludes irrelevant directories
to prevent VSCode crashes and improve analysis speed.

AINLP COMPATIBILITY: Intelligence delimitation applied
"""

import os
from pathlib import Path
from typing import Set, Iterator, List
import logging

logger = logging.getLogger(__name__)

class OptimizedFileScanner:
    """Optimized file scanner that excludes performance-killing directories."""

    # Directories to always exclude from analysis
    EXCLUDED_DIRS = {
        # Virtual environments
        'venv', '.venv', 'env', '.env', 'ENV', 'virtualenv', 'conda-env',

        # Build directories
        'build', 'dist', '.build', 'cmake-build-debug', 'cmake-build-release',
        'cmake-build-relwithdebinfo', 'cmake-build-minsizerel', 'out', 'target',

        # Dependencies
        'node_modules', 'vendor', 'packages', '.nuget',

        # Version control
        '.git', '.svn', '.hg', '.bzr',

        # IDE and editor directories
        '.vscode', '.idea', '.vs', '.settings', '.metadata',

        # Cache directories
        '__pycache__', '.cache', '.pytest_cache', '.mypy_cache', '.tox',
        '.coverage', 'htmlcov', '.nyc_output',

        # Temporary and log directories
        'tmp', 'temp', '.tmp', '.temp', 'logs', 'log',

        # OS and system directories
        '.DS_Store', 'Thumbs.db', '$RECYCLE.BIN', 'System Volume Information',

        # Archive directories (but allow tachyonic/archive/runtime)
        'backups', '.backups', 'old', 'deprecated',

        # Documentation build
        '_build', 'docs/_build', 'site', '.doctrees',

        # CI/CD
        '.github', '.gitlab-ci', '.travis', '.circleci', '.jenkins',

        # Docker
        '.docker',

        # Specific AIOS exclusions
        'runtime/test_results',       # Test artifacts
        'runtime/logs/cache',         # Cached logs
        'evolution_lab/artifacts',    # Large experiment data
    }

    # File patterns to exclude (in addition to directories)
    EXCLUDED_PATTERNS = {
        # Compiled Python
        '*.pyc', '*.pyo', '*.pyd',

        # Backup files
        '*~', '*.bak', '*.backup', '*.orig', '*.rej',

        # OS files
        '.DS_Store', 'Thumbs.db', 'desktop.ini',

        # Large data files
        '*.zip', '*.tar.gz', '*.tar.bz2', '*.tar.xz', '*.7z', '*.rar',
        '*.iso', '*.dmg', '*.exe', '*.msi', '*.deb', '*.rpm',

        # Database files
        '*.db', '*.sqlite', '*.sqlite3',

        # Large binary files
        '*.bin', '*.dat', '*.raw',
    }

    def __init__(self, root_path: Path, max_depth: int = 10):
        self.root_path = root_path.resolve()
        self.max_depth = max_depth
        self._excluded_paths: Set[Path] = set()

        # Pre-compute excluded paths for better performance
        self._build_excluded_paths()

    def _build_excluded_paths(self):
        """Build set of paths to exclude for faster checking."""
        for parent in [self.root_path, *self.root_path.parents]:
            for excluded_dir in self.EXCLUDED_DIRS:
                excluded_path = parent / excluded_dir
                if excluded_path.exists():
                    self._excluded_paths.add(excluded_path.resolve())

    def should_exclude_path(self, path: Path) -> bool:
        """Check if a path should be excluded from analysis."""
        path = path.resolve()

        # Special allowance for tachyonic/archive/runtime (our reports directory)
        if 'tachyonic' in path.parts and 'archive' in path.parts and 'runtime' in path.parts:
            # Allow tachyonic/archive/runtime but exclude deeper archive paths
            tachyonic_index = path.parts.index('tachyonic') if 'tachyonic' in path.parts else -1
            archive_index = path.parts.index('archive') if 'archive' in path.parts else -1
            runtime_index = path.parts.index('runtime') if 'runtime' in path.parts else -1

            if (tachyonic_index >= 0 and archive_index == tachyonic_index + 1 and
                runtime_index == archive_index + 1):
                # This is the tachyonic/archive/runtime directory - allow it
                return False

        # Check if path is in excluded directories
        for excluded_path in self._excluded_paths:
            try:
                path.relative_to(excluded_path)
                return True
            except ValueError:
                continue

        # Check directory name against excluded list
        for part in path.parts:
            if part in self.EXCLUDED_DIRS:
                return True

        # Check file patterns
        for pattern in self.EXCLUDED_PATTERNS:
            if path.match(pattern):
                return True

        # Check depth limit
        try:
            relative_depth = len(path.relative_to(self.root_path).parts)
            if relative_depth > self.max_depth:
                return True
        except ValueError:
            pass

        return False

    def scan_files(self, patterns: List[str], follow_symlinks: bool = False) -> Iterator[Path]:
        """Scan for files matching patterns, excluding irrelevant directories."""
        scanned_count = 0
        excluded_count = 0

        for pattern in patterns:
            for path in self.root_path.rglob(pattern):
                scanned_count += 1

                if scanned_count % 1000 == 0:
                    logger.debug(f"Scanned {scanned_count} files, excluded {excluded_count}")

                if self.should_exclude_path(path):
                    excluded_count += 1
                    continue

                yield path

        logger.info(f"File scan complete: {scanned_count} scanned, {excluded_count} excluded")

    def scan_python_files(self, follow_symlinks: bool = False) -> Iterator[Path]:
        """Scan for Python files, excluding irrelevant directories."""
        return self.scan_files(['*.py'], follow_symlinks)

    def scan_json_files(self, follow_symlinks: bool = False) -> Iterator[Path]:
        """Scan for JSON files, excluding irrelevant directories."""
        return self.scan_files(['*.json'], follow_symlinks)

    def scan_markdown_files(self, follow_symlinks: bool = False) -> Iterator[Path]:
        """Scan for Markdown files, excluding irrelevant directories."""
        return self.scan_files(['*.md', '*.markdown'], follow_symlinks)

    def get_directory_stats(self) -> dict:
        """Get statistics about directory scanning."""
        total_dirs = 0
        excluded_dirs = 0

        for root, dirs, files in os.walk(self.root_path):
            total_dirs += 1
            root_path = Path(root)

            # Remove excluded directories from dirs list to prevent traversal
            dirs_to_remove = []
            for d in dirs:
                dir_path = root_path / d
                if self.should_exclude_path(dir_path):
                    dirs_to_remove.append(d)
                    excluded_dirs += 1

            for d in dirs_to_remove:
                dirs.remove(d)

        return {
            'total_directories': total_dirs,
            'excluded_directories': excluded_dirs,
            'analyzed_directories': total_dirs - excluded_dirs
        }

# Convenience functions for common use cases
def scan_python_files(root_path: Path, max_depth: int = 10) -> Iterator[Path]:
    """Convenience function to scan Python files."""
    scanner = OptimizedFileScanner(root_path, max_depth)
    return scanner.scan_python_files()

def scan_json_files(root_path: Path, max_depth: int = 10) -> Iterator[Path]:
    """Convenience function to scan JSON files."""
    scanner = OptimizedFileScanner(root_path, max_depth)
    return scanner.scan_json_files()

def scan_markdown_files(root_path: Path, max_depth: int = 10) -> Iterator[Path]:
    """Convenience function to scan Markdown files."""
    scanner = OptimizedFileScanner(root_path, max_depth)
    return scanner.scan_markdown_files()

if __name__ == "__main__":
    # Test the scanner
    workspace_root = Path(__file__).parent
    scanner = OptimizedFileScanner(workspace_root)

    print("Directory Statistics:")
    stats = scanner.get_directory_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\nScanning Python files...")
    python_files = list(scanner.scan_python_files())
    print(f"Found {len(python_files)} Python files")

    print("\nScanning JSON files...")
    json_files = list(scanner.scan_json_files())
    print(f"Found {len(json_files)} JSON files")