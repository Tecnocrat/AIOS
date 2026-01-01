#!/usr/bin/env python3
"""
AINLP System Knowledge Graph Builder
Creates comprehensive knowledge graph of codebase relationships and semantics.

PERFORMANCE: Optimized file scanning with exclusion patterns
"""

import json
import ast
import networkx as nx
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict
import argparse
from optimized_file_scanner import OptimizedFileScanner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SystemKnowledgeGraph:
    """Builds comprehensive knowledge graph of the AIOS system."""

    def __init__(self, codebase_root: str):
        self.codebase_root = Path(codebase_root)
        self.scanner = OptimizedFileScanner(self.codebase_root, max_depth=8)
        self.knowledge_graph = nx.MultiDiGraph()
        self.semantic_index = {}
        self.relationship_types = set()

    def build_knowledge_graph(self) -> Dict:
        """Build comprehensive system knowledge graph."""
        logger.info("Building system knowledge graph...")

        # Phase 1: Structural Analysis
        self._analyze_code_structure()

        # Phase 2: Semantic Analysis
        self._analyze_semantic_relationships()

        # Phase 3: Dependency Analysis
        self._analyze_dependencies()

        # Phase 4: Pattern Recognition
        self._recognize_patterns()

        # Phase 5: Consciousness Mapping
        self._map_consciousness_layers()

        return {
            'timestamp': datetime.now().isoformat(),
            'graph_builder_version': '1.0.0',
            'codebase_root': str(self.codebase_root),
            'graph_statistics': self._get_graph_statistics(),
            'relationship_types': list(self.relationship_types),
            'semantic_index': self.semantic_index,
            'graph_data': self._export_graph_data()
        }

    def _analyze_code_structure(self):
        """Analyze basic code structure and create nodes."""
        logger.info("Analyzing code structure...")

        python_files = list(self.scanner.scan_python_files())

        for file_path in python_files:
            self._process_python_file(file_path)

    def _process_python_file(self, file_path: Path):
        """Process a single Python file for structural analysis."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))

            # Create file node
            file_node = str(file_path.relative_to(self.codebase_root))
            self.knowledge_graph.add_node(file_node, **{
                'type': 'file',
                'path': file_node,
                'size': len(content.splitlines()),
                'language': 'python'
            })

            # Extract and create nodes for classes, functions, etc.
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    self._process_class_node(file_node, node)
                elif isinstance(node, ast.FunctionDef):
                    self._process_function_node(file_node, node)
                elif isinstance(node, ast.Import):
                    self._process_import_node(file_node, node)
                elif isinstance(node, ast.ImportFrom):
                    self._process_import_from_node(file_path, node)

        except Exception as e:
            logger.warning(f"Error processing {file_path}: {e}")

    def _process_class_node(self, file_node: str, class_node: ast.ClassDef):
        """Process a class definition."""
        class_id = f"{file_node}::{class_node.name}"

        self.knowledge_graph.add_node(class_id, **{
            'type': 'class',
            'name': class_node.name,
            'file': file_node,
            'line': class_node.lineno,
            'bases': [base.id if hasattr(base, 'id') else str(base)
                     for base in class_node.bases]
        })

        # Add relationship to file
        self.knowledge_graph.add_edge(file_node, class_id,
                                    relationship='contains')
        self.relationship_types.add('contains')

        # Add inheritance relationships
        for base in class_node.bases:
            base_name = base.id if hasattr(base, 'id') else str(base)
            self.knowledge_graph.add_edge(class_id, base_name,
                                        relationship='inherits_from')
            self.relationship_types.add('inherits_from')

    def _process_function_node(self, file_node: str,
                             func_node: ast.FunctionDef):
        """Process a function definition."""
        func_id = f"{file_node}::{func_node.name}"

        self.knowledge_graph.add_node(func_id, **{
            'type': 'function',
            'name': func_node.name,
            'file': file_node,
            'line': func_node.lineno,
            'args': len(func_node.args.args),
            'is_async': isinstance(func_node, ast.AsyncFunctionDef)
        })

        # Add relationship to file
        self.knowledge_graph.add_edge(file_node, func_id,
                                    relationship='contains')
        self.relationship_types.add('contains')

        # Add relationship to class if method
        # This would require more sophisticated analysis

    def _process_import_node(self, file_node: str, import_node: ast.Import):
        """Process import statements."""
        for alias in import_node.names:
            module_name = alias.name
            import_id = f"import::{module_name}"

            self.knowledge_graph.add_node(import_id, **{
                'type': 'import',
                'module': module_name,
                'alias': alias.asname
            })

            self.knowledge_graph.add_edge(file_node, import_id,
                                        relationship='imports')
            self.relationship_types.add('imports')

    def _process_import_from_node(self, file_node: str,
                                import_node: ast.ImportFrom):
        """Process from import statements."""
        module = import_node.module or ''
        for alias in import_node.names:
            import_id = f"import_from::{module}::{alias.name}"

            self.knowledge_graph.add_node(import_id, **{
                'type': 'import_from',
                'module': module,
                'name': alias.name,
                'alias': alias.asname
            })

            self.knowledge_graph.add_edge(file_node, import_id,
                                        relationship='imports_from')
            self.relationship_types.add('imports_from')

    def _analyze_semantic_relationships(self):
        """Analyze semantic relationships between components."""
        logger.info("Analyzing semantic relationships...")

        # Find related components by naming patterns
        self._find_naming_relationships()

        # Find related components by content similarity
        self._find_content_relationships()

    def _find_naming_relationships(self):
        """Find relationships based on naming patterns."""
        nodes_by_type = {}
        for node, attrs in self.knowledge_graph.nodes(data=True):
            node_type = attrs.get('type', 'unknown')
            if node_type not in nodes_by_type:
                nodes_by_type[node_type] = []
            nodes_by_type[node_type].append((node, attrs))

        # Find class-function relationships
        if 'class' in nodes_by_type and 'function' in nodes_by_type:
            for class_node, class_attrs in nodes_by_type['class']:
                class_name = class_attrs['name'].lower()
                for func_node, func_attrs in nodes_by_type['function']:
                    if class_name in func_attrs['name'].lower():
                        self.knowledge_graph.add_edge(
                            class_node, func_node,
                            relationship='potentially_related')
                        self.relationship_types.add('potentially_related')

    def _find_content_relationships(self):
        """Find relationships based on content analysis."""
        # This would analyze docstrings, comments, and code patterns
        # Simplified implementation
        pass

    def _analyze_dependencies(self):
        """Analyze dependency relationships."""
        logger.info("Analyzing dependencies...")

        # Build dependency graph from imports
        import_nodes = [n for n, attrs in self.knowledge_graph.nodes(data=True)
                       if attrs.get('type') in ['import', 'import_from']]

        for import_node in import_nodes:
            attrs = self.knowledge_graph.nodes[import_node]
            module_name = attrs.get('module', '')

            # Find potential target files
            for node, node_attrs in self.knowledge_graph.nodes(data=True):
                if node_attrs.get('type') == 'file':
                    if module_name and module_name.replace('.', '/') in node:
                        self.knowledge_graph.add_edge(
                            import_node, node, relationship='depends_on')
                        self.relationship_types.add('depends_on')

    def _recognize_patterns(self):
        """Recognize architectural and design patterns."""
        logger.info("Recognizing patterns...")

        # Find singleton patterns
        self._find_singleton_patterns()

        # Find factory patterns
        self._find_factory_patterns()

        # Find observer patterns
        self._find_observer_patterns()

    def _find_singleton_patterns(self):
        """Find singleton pattern implementations."""
        for node, attrs in self.knowledge_graph.nodes(data=True):
            if attrs.get('type') == 'class':
                # Look for singleton indicators in class name or structure
                class_name = attrs.get('name', '').lower()
                if 'singleton' in class_name or 'manager' in class_name:
                    self.knowledge_graph.nodes[node]['pattern'] = 'singleton'
                    self.relationship_types.add('pattern_singleton')

    def _find_factory_patterns(self):
        """Find factory pattern implementations."""
        for node, attrs in self.knowledge_graph.nodes(data=True):
            if attrs.get('type') == 'class':
                class_name = attrs.get('name', '').lower()
                if 'factory' in class_name or 'creator' in class_name:
                    self.knowledge_graph.nodes[node]['pattern'] = 'factory'
                    self.relationship_types.add('pattern_factory')

    def _find_observer_patterns(self):
        """Find observer pattern implementations."""
        for node, attrs in self.knowledge_graph.nodes(data=True):
            if attrs.get('type') == 'class':
                class_name = attrs.get('name', '').lower()
                if 'observer' in class_name or 'listener' in class_name:
                    self.knowledge_graph.nodes[node]['pattern'] = 'observer'
                    self.relationship_types.add('pattern_observer')

    def _map_consciousness_layers(self):
        """Map consciousness layers and dendritic relationships."""
        logger.info("Mapping consciousness layers...")

        consciousness_keywords = ['consciousness', 'dendritic', 'tachyonic',
                                'neuronal', 'supercell']

        for node, attrs in self.knowledge_graph.nodes(data=True):
            node_name = attrs.get('name', '').lower() if 'name' in attrs \
                       else str(node).lower()

            for keyword in consciousness_keywords:
                if keyword in node_name:
                    self.knowledge_graph.nodes[node]['consciousness_layer'] \
                        = keyword
                    break

        # Create consciousness relationship edges
        consciousness_nodes = [n for n, attrs in
                              self.knowledge_graph.nodes(data=True)
                              if 'consciousness_layer' in attrs]

        for i, node1 in enumerate(consciousness_nodes):
            for node2 in consciousness_nodes[i+1:]:
                layer1 = self.knowledge_graph.nodes[node1]['consciousness_layer']
                layer2 = self.knowledge_graph.nodes[node2]['consciousness_layer']
                if layer1 != layer2:
                    self.knowledge_graph.add_edge(
                        node1, node2, relationship='consciousness_bridge')
                    self.relationship_types.add('consciousness_bridge')

    def _get_graph_statistics(self) -> Dict:
        """Get comprehensive graph statistics."""
        return {
            'total_nodes': len(self.knowledge_graph.nodes),
            'total_edges': len(self.knowledge_graph.edges),
            'node_types': self._count_node_types(),
            'edge_types': self._count_edge_types(),
            'density': nx.density(self.knowledge_graph) \
                      if len(self.knowledge_graph.nodes) > 1 else 0,
            'connected_components': nx.number_connected_components(
                self.knowledge_graph.to_undirected())
        }

    def _count_node_types(self) -> Dict[str, int]:
        """Count nodes by type."""
        types = {}
        for node, attrs in self.knowledge_graph.nodes(data=True):
            node_type = attrs.get('type', 'unknown')
            types[node_type] = types.get(node_type, 0) + 1
        return types

    def _count_edge_types(self) -> Dict[str, int]:
        """Count edges by relationship type."""
        relationships = {}
        for edge in self.knowledge_graph.edges(data=True):
            rel_type = edge[2].get('relationship', 'unknown')
            relationships[rel_type] = relationships.get(rel_type, 0) + 1
        return relationships

    def _export_graph_data(self) -> Dict:
        """Export graph data for serialization."""
        def make_serializable(obj):
            """Convert objects to JSON-serializable types."""
            if isinstance(obj, Path):
                return str(obj)
            elif isinstance(obj, dict):
                return {k: make_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [make_serializable(item) for item in obj]
            else:
                return obj

        return {
            'nodes': [
                make_serializable({'id': node, **attrs})
                for node, attrs in self.knowledge_graph.nodes(data=True)
            ],
            'edges': [
                make_serializable({'source': edge[0], 'target': edge[1], **edge[2]})
                for edge in self.knowledge_graph.edges(data=True)
            ]
        }


def main():
    parser = argparse.ArgumentParser(
        description='AINLP System Knowledge Graph Builder')
    parser.add_argument('--codebase-root', required=True,
                       help='Root directory of codebase')
    parser.add_argument('--output-dir',
                       default='tachyonic/archive/runtime',
                       help='Output directory for reports')

    args = parser.parse_args()

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build knowledge graph
    builder = SystemKnowledgeGraph(args.codebase_root)
    results = builder.build_knowledge_graph()

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = output_dir / f"system_knowledge_graph_{timestamp}.json"

    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Print summary
    stats = results['graph_statistics']
    print("=" * 70)
    print("AINLP SYSTEM KNOWLEDGE GRAPH COMPLETE")
    print("=" * 70)
    print(f"Total Nodes: {stats['total_nodes']}")
    print(f"Total Edges: {stats['total_edges']}")
    print(f"Node Types: {stats['node_types']}")
    print(f"Edge Types: {stats['edge_types']}")
    print(f"Connected Components: {stats['connected_components']}")
    print(f"Graph Density: {stats['density']:.4f}")
    print(f"Report: {report_path}")
    print("=" * 70)


if __name__ == '__main__':
    main()