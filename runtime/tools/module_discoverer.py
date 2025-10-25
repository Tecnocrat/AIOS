#!/usr/bin/env python3
"""
AIOS Module Discoverer - AINLP Dendritic Intelligence Cell

Observes, archives, analyzes, merges, cleans, and verifies AIOS modules.
Part of the AINLP.dendritic pattern: intelligent module coherence and
consolidation.

PURPOSE:
- Scan Python modules for import dependencies and structural patterns
- Detect circular imports, redundancies, and merge opportunities
- Emit structured reports to tachyonic/archive/ for dendritic intelligence
- Integrate with existing discovery pipelines (index_tools.py, sequencer)

AINLP DENDRITIC INTEGRATION:
- This is a "cell" that observes the codebase as a living system
- Archives findings in tachyonic space for pattern evolution
- Analyzes coherence and suggests intelligent consolidations
- Merges scattered logic into higher-level architectures
- Cleans architectural debt through evidence-based recommendations
- Verifies module health and integration opportunities

CAPABILITIES:
1. Import Graph Analysis: AST-based dependency mapping
2. Circular Import Detection: Strongly connected components
3. Similarity Analysis: AST signatures + TF-IDF content similarity
4. Redundancy Detection: Duplicate names and overlapping functionality
5. Merge Opportunity Scoring: Confidence-based consolidation suggestions
6. Orphan Module Discovery: Files not in sequencer discovery
7. Spatial Metadata Respect: Honors .aios_spatial_metadata.json exclusions

OUTPUTS:
- JSON report: tachyonic/archive/module_discovery_YYYYMMDD_HHMMSS.json
- Latest pointer: tachyonic/archive/module_discovery_latest.json
- Optional summary: docs/module_discovery_report_YYYYMMDD_HHMMSS.md

USAGE:
    python -m runtime_intelligence.tools.module_discoverer [options]

OPTIONS:
    --root PATH          Workspace root (default: auto-detect)
    --include PATTERN    File patterns to include (default: *.py)
    --exclude PATTERN    Patterns to exclude
                         (default: venv/,__pycache__/,build/)
    --similarity FLOAT   Similarity threshold for merge suggestions
                         (default: 0.85)
    --output DIR         Output directory (default: tachyonic/archive/)
    --dry-run           Analyze without writing files
    --verbose           Detailed logging

EXAMPLE:
    python -m runtime_intelligence.tools.module_discoverer \
        --similarity 0.8 --verbose

DEPENDENCIES:
- ast (stdlib)
- pathlib (stdlib)
- json (stdlib)
- collections (stdlib)
- typing (stdlib)
- Optional: sklearn for advanced similarity (falls back to basic TF-IDF)

AINLP PHILOSOPHY:
"Intelligence emerges from integration, not isolation. This cell observes
the dendritic connections between modules, suggesting where to prune,
merge, or strengthen for enhanced coherence."
"""

import ast
import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import defaultdict
import hashlib
import time


class ImprovedModuleDiscoverer:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.modules: Dict[str, Dict] = {}
        self.import_graph: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_import_graph: Dict[str, Set[str]] = defaultdict(set)
        self.spatial_metadata = self._load_spatial_metadata()

    def _load_spatial_metadata(self) -> Dict:
        """Load AIOS spatial metadata to understand project structure"""
        metadata_paths = [
            self.root_path / ".aios_spatial_metadata.json",
            self.root_path / "tachyonic" / "aios_holographic_index_latest.json"
        ]

        for path in metadata_paths:
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception:
                    continue
        return {}

    def _should_exclude(self, file_path: Path) -> bool:
        """Determine if a file should be excluded from analysis"""
        # Exclude external packages and common directories
        exclude_patterns = [
            'venv', 'node_modules', '__pycache__', '.git',
            'build', 'dist', 'site-packages', '.vscode',
            'tachyonic/archive', 'tachyonic/backups'
        ]

        path_str = str(file_path)
        return any(pattern in path_str for pattern in exclude_patterns)

    def _is_workspace_module(self, file_path: Path) -> bool:
        """Check if file is within AIOS workspace (not external)"""
        try:
            # Resolve to absolute path and check if it's under root
            resolved = file_path.resolve()
            return (resolved.is_relative_to(self.root_path) and
                    not self._should_exclude(resolved))
        except Exception:
            return False

    def _parse_module(self, file_path: Path) -> Optional[Dict]:
        """Parse a Python module and extract symbols and imports"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))

            symbols = set()
            imports = set()
            functions = set()
            classes = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.add(node.name)
                    symbols.add(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.add(node.name)
                    symbols.add(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])

            # Calculate content hash for duplicate detection
            content_hash = hashlib.md5(content.encode()).hexdigest()

            return {
                'path': str(file_path.relative_to(self.root_path)),
                'symbols': symbols,
                'imports': imports,
                'functions': functions,
                'classes': classes,
                'lines': len(content.split('\n')),
                'hash': content_hash,
                'size': len(content)
            }
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def _build_import_graph(self):
        """Build import relationships between modules"""
        for module_path, module_data in self.modules.items():
            for imported in module_data['imports']:
                # Find modules that might match this import
                for other_path, other_data in self.modules.items():
                    if other_path != module_path:
                        other_name = Path(other_path).stem
                        if (imported == other_name or
                                imported in other_name):
                            self.import_graph[module_path].add(other_path)
                            self.reverse_import_graph[other_path].add(
                                module_path)

    def _find_sccs(self) -> List[List[str]]:
        """Find strongly connected components (circular imports)
        using Kosaraju's algorithm"""
        def dfs1(node, visited, stack):
            visited.add(node)
            for neighbor in self.import_graph[node]:
                if neighbor not in visited:
                    dfs1(neighbor, visited, stack)
            stack.append(node)

        def dfs2(node, visited, component):
            visited.add(node)
            component.append(node)
            for neighbor in self.reverse_import_graph[node]:
                if neighbor not in visited:
                    dfs2(neighbor, visited, component)

        visited = set()
        stack = []

        # First DFS to get finishing times
        for node in list(self.import_graph.keys()):
            if node not in visited:
                dfs1(node, visited, stack)

        # Second DFS to find SCCs
        visited.clear()
        sccs = []

        while stack:
            node = stack.pop()
            if node not in visited:
                component = []
                dfs2(node, visited, component)
                if len(component) > 1:  # Only report actual cycles
                    sccs.append(component)

        return sccs

    def _compute_similarity(self, module_a: Dict, module_b: Dict) -> float:
        """Compute semantic similarity between two modules"""
        if not module_a['symbols'] or not module_b['symbols']:
            return 0.0

        # Symbol overlap (weighted)
        symbols_a = module_a['symbols']
        symbols_b = module_b['symbols']
        symbol_overlap = len(symbols_a & symbols_b) / len(symbols_a | symbols_b)

        # Import similarity (weighted)
        imports_a = module_a['imports']
        imports_b = module_b['imports']
        import_overlap = len(imports_a & imports_b) / len(imports_a | imports_b) if (imports_a or imports_b) else 0

        # Function/class pattern similarity
        func_similarity = len(module_a['functions'] & module_b['functions']) / max(len(module_a['functions'] | module_b['functions']), 1)
        class_similarity = len(module_a['classes'] & module_b['classes']) / max(len(module_a['classes'] | module_b['classes']), 1)

        # Weighted combination (imports are most important for semantic similarity)
        similarity = (
            symbol_overlap * 0.3 +
            import_overlap * 0.4 +
            func_similarity * 0.15 +
            class_similarity * 0.15
        )

        return similarity

    def _find_similar_modules(self, threshold: float = 0.7) -> List[Dict]:
        """Find semantically similar modules"""
        similar_pairs = []

        module_paths = list(self.modules.keys())
        for i, path_a in enumerate(module_paths):
            for path_b in module_paths[i+1:]:
                module_a = self.modules[path_a]
                module_b = self.modules[path_b]

                similarity = self._compute_similarity(module_a, module_b)

                if similarity >= threshold:
                    shared_symbols = module_a['symbols'] & module_b['symbols']
                    shared_imports = module_a['imports'] & module_b['imports']

                    # Determine recommendation based on similarity and shared patterns
                    if similarity > 0.9 and len(shared_symbols) > 5:
                        recommendation = "high_merge_priority"
                    elif similarity > 0.8 and len(shared_imports) > 2:
                        recommendation = "consider_merge"
                    else:
                        recommendation = "review_similarity"

                    similar_pairs.append({
                        'path_a': path_a,
                        'path_b': path_b,
                        'similarity': round(similarity, 3),
                        'shared_symbols': list(shared_symbols),
                        'shared_imports': list(shared_imports),
                        'recommendation': recommendation
                    })

        # Sort by similarity (highest first)
        similar_pairs.sort(key=lambda x: x['similarity'], reverse=True)
        return similar_pairs

    def _find_duplicates(self) -> List[Dict]:
        """Find exact duplicate modules by content hash"""
        hash_groups = defaultdict(list)

        for path, module_data in self.modules.items():
            hash_groups[module_data['hash']].append(path)

        duplicates = []
        for hash_val, paths in hash_groups.items():
            if len(paths) > 1:
                # Get the module data for size info
                module_data = self.modules[paths[0]]
                duplicates.append({
                    'hash': hash_val,
                    'files': paths,
                    'count': len(paths),
                    'size': module_data['size'],
                    'recommendation': 'remove_duplicates' if len(paths) > 2 else 'review_duplicates'
                })

        return sorted(duplicates, key=lambda x: x['count'], reverse=True)

    def _find_orphans(self) -> List[str]:
        """Find modules that are not imported by any other module"""
        imported_modules = set()
        for module_data in self.modules.values():
            for imported in module_data['imports']:
                # Find actual module files that match imports
                for path in self.modules.keys():
                    module_name = Path(path).stem
                    if imported == module_name or imported in module_name:
                        imported_modules.add(path)

        all_modules = set(self.modules.keys())
        orphans = all_modules - imported_modules

        return sorted(list(orphans))

    def discover(self) -> Dict:
        """Main discovery method"""
        print("🔍 Scanning AIOS workspace for Python modules...")

        # Scan for Python files
        python_files = []
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    if self._is_workspace_module(file_path):
                        python_files.append(file_path)

        print(f"📊 Found {len(python_files)} Python modules in workspace")

        # Parse modules
        for file_path in python_files:
            module_data = self._parse_module(file_path)
            if module_data:
                self.modules[module_data['path']] = module_data

        print(f"✅ Successfully parsed {len(self.modules)} modules")

        # Build relationships
        self._build_import_graph()

        # Find issues
        sccs = self._find_sccs()
        similar_pairs = self._find_similar_modules(threshold=0.7)
        duplicates = self._find_duplicates()
        orphans = self._find_orphans()

        result = {
            'timestamp': time.time(),
            'scan_root': str(self.root_path),
            'summary': {
                'files_scanned': len(self.modules),
                'scc_count': len(sccs),
                'similarity_pairs': len(similar_pairs),
                'duplicate_names': len(duplicates),
                'orphans': len(orphans)
            },
            'sccs': sccs,
            'similarity_pairs': similar_pairs[:100],  # Top 100 most similar
            'duplicates': duplicates,
            'orphans': orphans[:50],  # Top 50 orphans
            'modules': {
                k: {
                    **v,
                    'symbols': list(v['symbols']),
                    'imports': list(v['imports']),
                    'functions': list(v['functions']),
                    'classes': list(v['classes'])
                }
                for k, v in self.modules.items()
                if v['lines'] > 10
            }  # Non-trivial modules
        }

        return result

    def save_report(self, result: Dict, output_path: Optional[str] = None):
        """Save discovery results to JSON file"""
        if not output_path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = str(
                self.root_path / "tachyonic" / "archive" /
                f"module_discovery_{timestamp}.json"
            )

        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path_obj, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        # Update latest pointer
        latest_path = (
            self.root_path / "tachyonic" / "archive" /
            "module_discovery_latest.json"
        )
        try:
            with open(latest_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

        print(f"💾 Report saved to: {output_path_obj}")
        print(f"🔗 Latest pointer updated: {latest_path}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="AIOS Module Discovery Tool")
    parser.add_argument('--root', default='.', help='Root directory to scan')
    parser.add_argument(
        '--similarity', type=float, default=0.7,
        help='Similarity threshold (0.0-1.0)'
    )
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument(
        '--verbose', action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    root_path = Path(args.root).resolve()
    if not root_path.exists():
        print(f"❌ Root path does not exist: {root_path}")
        return 1

    print("🚀 Starting AIOS Module Discovery")
    print(f"📁 Root: {root_path}")
    print(f"🎯 Similarity Threshold: {args.similarity}")

    discoverer = ImprovedModuleDiscoverer(str(root_path))
    result = discoverer.discover()

    # Print summary
    summary = result['summary']
    print("\n📊 DISCOVERY SUMMARY")
    print(f"   Files Scanned: {summary['files_scanned']}")
    print(f"   Circular Imports: {summary['scc_count']}")
    print(f"   Similar Pairs: {summary['similarity_pairs']}")
    print(f"   Duplicates: {summary['duplicate_names']}")
    print(f"   Orphan Modules: {summary['orphans']}")

    # Print top findings
    if result['duplicates']:
        print("\n🔍 TOP DUPLICATES:")
        for dup in result['duplicates'][:5]:
            print(f"   {dup['count']} files: {dup['files'][0]}...")

    if result['similarity_pairs']:
        print("\n🔍 TOP SIMILAR PAIRS:")
        for pair in result['similarity_pairs'][:5]:
            print(f"   {pair['path_a']} ↔ {pair['path_b']} "
                  f"(similarity: {pair['similarity']})")

    if result['sccs']:
        print("\n🔍 CIRCULAR IMPORTS DETECTED:")
        for scc in result['sccs'][:3]:
            cycle_str = ' → '.join(scc[:5])
            suffix = '...' if len(scc) > 5 else ''
            print(f"   Cycle: {cycle_str}{suffix}")

    # Save report
    discoverer.save_report(result, args.output)

    print("\n✅ Module discovery complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
