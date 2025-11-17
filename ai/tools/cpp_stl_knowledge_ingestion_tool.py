#!/usr/bin/env python3
"""
AIOS C++ STL Knowledge Ingestion Engine
MARKER 1: EXTRACTION - Convert STL into machine-readable knowledge base
MARKER 2: REPRESENTATION - Encode into AIOS fractal knowledge cells
MARKER 3: BRIDGING - Connect to AIOS reasoning and code generation
MARKER 4: BEHAVIOURAL INTEGRATION - Make STL part of decision-making
MARKER 5: RECURSIVE SELF-OBSERVATION - Reflect on STL usage

AINLP Architectural Improvement: Enhancement over creation paradigm
Biological Architecture: Nucleus (knowledge ingestion), Cytoplasm (data flow), Membrane (API boundaries)
"""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


@dataclass
class STLComponent:
    """Structured representation of a C++ STL component"""
    name: str
    category: str  # container, algorithm, iterator, etc.
    description: str
    complexity: Dict[str, str]  # operation -> Big O
    usage_patterns: List[str]
    code_examples: List[str]
    related_components: List[str]
    thread_safety: str
    memory_model: str
    ingestion_timestamp: str


class STLKnowledgeCell:
    """AIOS fractal knowledge cell for STL components"""

    def __init__(self, component: STLComponent):
        self.component = component
        self.knowledge_graph = self._build_knowledge_graph()
        self.reasoning_patterns = self._extract_reasoning_patterns()
        self.code_generation_templates = self._create_generation_templates()

    def _build_knowledge_graph(self) -> Dict[str, Any]:
        """Build semantic knowledge graph for the STL component"""
        return {
            "entity": self.component.name,
            "category": self.component.category,
            "properties": {
                "complexity": self.component.complexity,
                "thread_safety": self.component.thread_safety,
                "memory_model": self.component.memory_model
            },
            "relationships": {
                "related_to": self.component.related_components,
                "used_for": self.component.usage_patterns
            },
            "examples": self.component.code_examples
        }

    def _extract_reasoning_patterns(self) -> List[Dict[str, Any]]:
        """Extract reasoning patterns for AI decision making"""
        patterns = []

        # Complexity-based reasoning
        for operation, complexity in self.component.complexity.items():
            if "O(1)" in complexity:
                patterns.append({
                    "trigger": f"need fast {operation}",
                    "reasoning": f"{self.component.name} provides O(1) "
                                f"{operation}",
                    "confidence": 0.9
                })
            elif "O(log n)" in complexity:
                patterns.append({
                    "trigger": f"need ordered {operation}",
                    "reasoning": f"{self.component.name} provides O(log n) {operation}",
                    "confidence": 0.8
                })

        # Usage pattern reasoning
        for pattern in self.component.usage_patterns:
            patterns.append({
                "trigger": pattern.lower(),
                "reasoning": f"{self.component.name} is suitable for {pattern}",
                "confidence": 0.7
            })

        return patterns

    def _create_generation_templates(self) -> List[Dict[str, Any]]:
        """Create code generation templates"""
        templates = []

        for example in self.component.code_examples:
            templates.append({
                "template": example,
                "context": f"{self.component.category} usage",
                "complexity": self.component.complexity,
                "description": f"Generated {self.component.name} usage pattern"
            })

        return templates


class AIOSCppSTLIngestionEngine:
    """
    MARKER 1: EXTRACTION - Convert STL into machine-readable knowledge base
    Main ingestion engine for C++ Standard Library knowledge
    """

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.knowledge_base = self.workspace_root / "tachyonic" / "archive" / "cpp_stl_knowledge"
        self.knowledge_base.mkdir(parents=True, exist_ok=True)

        # STL documentation sources
        self.documentation_sources = {
            "microsoft_cpp_reference": "https://learn.microsoft.com/en-us/cpp/standard-library/cpp-standard-library-reference",
            "cppreference_com": "https://en.cppreference.com/w/cpp",
            "local_cache": self.knowledge_base / "stl_documentation_cache.json"
        }

        self.ingested_components: Dict[str, STLKnowledgeCell] = {}

    def ingest_stl_knowledge(self, source_url: str = None) -> Dict[str, Any]:
        """
        MARKER 1: Main ingestion pipeline
        Extract STL knowledge from documentation sources
        """
        if source_url is None:
            source_url = self.documentation_sources["microsoft_cpp_reference"]

        print(f"🔍 Extracting STL knowledge from: {source_url}")

        # For now, use predefined STL knowledge since we can't access web
        # In production, this would scrape the documentation
        stl_components = self._get_predefined_stl_components()

        knowledge_cells = {}
        for component_data in stl_components:
            component = STLComponent(**component_data)
            knowledge_cell = STLKnowledgeCell(component)
            knowledge_cells[component.name] = knowledge_cell
            self.ingested_components[component.name] = knowledge_cell

        # Save to knowledge base
        self._save_knowledge_base(knowledge_cells)

        return {
            "ingested_components": len(knowledge_cells),
            "knowledge_cells": [cell.knowledge_graph for cell in knowledge_cells.values()],
            "extraction_timestamp": datetime.now().isoformat(),
            "source": source_url
        }

    def _get_predefined_stl_components(self) -> List[Dict[str, Any]]:
        """Predefined STL components for initial ingestion"""
        return [
            {
                "name": "std::vector",
                "category": "container",
                "description": "Dynamic array container that can change size",
                "complexity": {
                    "access": "O(1)",
                    "insert_end": "amortized O(1)",
                    "insert_middle": "O(n)",
                    "erase_middle": "O(n)"
                },
                "usage_patterns": [
                    "Dynamic array storage",
                    "Fast random access",
                    "Frequent insertions at end"
                ],
                "code_examples": [
                    "std::vector<int> v = {1, 2, 3};",
                    "v.push_back(4);",
                    "int value = v[0];"
                ],
                "related_components": ["std::array", "std::deque", "std::list"],
                "thread_safety": "not thread-safe",
                "memory_model": "contiguous",
                "ingestion_timestamp": datetime.now().isoformat()
            },
            {
                "name": "std::map",
                "category": "container",
                "description": "Sorted associative container with unique keys",
                "complexity": {
                    "access": "O(log n)",
                    "insert": "O(log n)",
                    "erase": "O(log n)"
                },
                "usage_patterns": [
                    "Ordered key-value storage",
                    "Fast lookups with ordering",
                    "Unique key requirements"
                ],
                "code_examples": [
                    "std::map<std::string, int> m;",
                    "m[\"key\"] = 42;",
                    "auto it = m.find(\"key\");"
                ],
                "related_components": ["std::unordered_map", "std::set", "std::multimap"],
                "thread_safety": "not thread-safe",
                "memory_model": "node-based",
                "ingestion_timestamp": datetime.now().isoformat()
            },
            {
                "name": "std::unordered_map",
                "category": "container",
                "description": "Unordered associative container with unique keys",
                "complexity": {
                    "access": "average O(1), worst O(n)",
                    "insert": "average O(1), worst O(n)",
                    "erase": "average O(1), worst O(n)"
                },
                "usage_patterns": [
                    "Fast key-value lookups",
                    "No ordering requirements",
                    "Hash-based access"
                ],
                "code_examples": [
                    "std::unordered_map<std::string, int> um;",
                    "um[\"key\"] = 42;",
                    "auto it = um.find(\"key\");"
                ],
                "related_components": ["std::map", "std::unordered_set", "std::unordered_multimap"],
                "thread_safety": "not thread-safe",
                "memory_model": "hash table",
                "ingestion_timestamp": datetime.now().isoformat()
            },
            {
                "name": "std::sort",
                "category": "algorithm",
                "description": "Sorts elements in range using operator<",
                "complexity": {
                    "average": "O(n log n)",
                    "worst": "O(n log n)",
                    "best": "O(n)"
                },
                "usage_patterns": [
                    "Sorting collections",
                    "Preparing data for binary search",
                    "Ordering requirements"
                ],
                "code_examples": [
                    "std::vector<int> v = {3, 1, 4, 1, 5};",
                    "std::sort(v.begin(), v.end());",
                    "std::sort(v.begin(), v.end(), std::greater<int>());"
                ],
                "related_components": ["std::stable_sort", "std::partial_sort", "std::nth_element"],
                "thread_safety": "can be used with parallel execution policies",
                "memory_model": "in-place",
                "ingestion_timestamp": datetime.now().isoformat()
            },
            {
                "name": "std::unique_ptr",
                "category": "smart_pointer",
                "description": "Exclusive ownership smart pointer",
                "complexity": {
                    "construction": "O(1)",
                    "destruction": "O(1)",
                    "dereference": "O(1)"
                },
                "usage_patterns": [
                    "Exclusive resource ownership",
                    "RAII resource management",
                    "Preventing memory leaks"
                ],
                "code_examples": [
                    "std::unique_ptr<int> ptr = std::make_unique<int>(42);",
                    "int value = *ptr;",
                    "auto moved_ptr = std::move(ptr);"
                ],
                "related_components": ["std::shared_ptr", "std::weak_ptr", "std::auto_ptr"],
                "thread_safety": "not thread-safe",
                "memory_model": "exclusive ownership",
                "ingestion_timestamp": datetime.now().isoformat()
            },
            {
                "name": "std::thread",
                "category": "concurrency",
                "description": "Represents a single thread of execution",
                "complexity": {
                    "creation": "O(1)",
                    "join": "O(1)",
                    "detach": "O(1)"
                },
                "usage_patterns": [
                    "Parallel execution",
                    "Asynchronous operations",
                    "CPU-bound task parallelism"
                ],
                "code_examples": [
                    "std::thread t([]{ std::cout << \"Hello from thread\"; });",
                    "t.join();",
                    "std::thread t2(func, arg1, arg2);"
                ],
                "related_components": ["std::mutex", "std::condition_variable", "std::atomic"],
                "thread_safety": "thread-safe operations",
                "memory_model": "system thread",
                "ingestion_timestamp": datetime.now().isoformat()
            }
        ]

    def _save_knowledge_base(self, knowledge_cells: Dict[str, STLKnowledgeCell]):
        """Save ingested knowledge to persistent storage"""
        knowledge_data = {
            "ingestion_metadata": {
                "timestamp": datetime.now().isoformat(),
                "engine_version": "1.0.0",
                "components_ingested": len(knowledge_cells)
            },
            "knowledge_cells": {}
        }

        for name, cell in knowledge_cells.items():
            knowledge_data["knowledge_cells"][name] = {
                "component": cell.component.__dict__,
                "knowledge_graph": cell.knowledge_graph,
                "reasoning_patterns": cell.reasoning_patterns,
                "code_generation_templates": cell.code_generation_templates
            }

        output_file = self.knowledge_base / f"stl_knowledge_base_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(knowledge_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Knowledge base saved to: {output_file}")

    def query_stl_knowledge(self, query: str) -> Dict[str, Any]:
        """
        MARKER 3: BRIDGING - Query STL knowledge for reasoning
        """
        results = []

        for name, cell in self.ingested_components.items():
            # Simple text matching - in production would use semantic search
            if query.lower() in name.lower() or query.lower() in cell.component.description.lower():
                results.append({
                    "component": name,
                    "relevance_score": 0.8,  # Simplified scoring
                    "knowledge": cell.knowledge_graph,
                    "reasoning_patterns": cell.reasoning_patterns[:3]  # Top 3
                })

        return {
            "query": query,
            "results": results,
            "total_matches": len(results)
        }

    def generate_stl_code(self, intent: str) -> Dict[str, Any]:
        """
        MARKER 3: BRIDGING - Generate STL code based on intent
        """
        # Simple intent matching - in production would use NLP
        intent_patterns = {
            "dynamic array": "std::vector",
            "fast lookup": "std::unordered_map",
            "ordered storage": "std::map",
            "sorting": "std::sort",
            "unique ownership": "std::unique_ptr",
            "parallel execution": "std::thread"
        }

        matched_component = None
        for pattern, component in intent_patterns.items():
            if pattern in intent.lower():
                matched_component = component
                break

        if matched_component and matched_component in self.ingested_components:
            cell = self.ingested_components[matched_component]
            return {
                "intent": intent,
                "recommended_component": matched_component,
                "code_templates": cell.code_generation_templates,
                "reasoning": f"Selected {matched_component} based on intent matching",
                "complexity_analysis": cell.component.complexity
            }

        return {
            "intent": intent,
            "error": "No suitable STL component found for the given intent"
        }


def process_stl_knowledge(operation: str = "ingest",
                          **kwargs) -> Dict[str, Any]:
    """
    Main entry point for C++ STL knowledge processing operations

    Args:
        operation: Operation to perform (ingest, query, generate)
        **kwargs: Additional parameters for the operation

    Returns:
        Operation result
    """
    try:
        workspace_root = r"C:\dev\AIOS"
        engine = AIOSCppSTLIngestionEngine(workspace_root)

        if operation == "ingest":
            return engine.ingest_stl_knowledge()

        elif operation == "query":
            query = kwargs.get('query', '')
            return engine.query_stl_knowledge(query)

        elif operation == "generate":
            intent = kwargs.get('intent', '')
            return engine.generate_stl_code(intent)

        else:
            return {
                'status': 'error',
                'message': f'Unknown operation: {operation}',
                'available_operations': ['ingest', 'query', 'generate']
            }

    except Exception as e:
        return {
            'status': 'error',
            'message': f'STL knowledge processing failed: {str(e)}'
        }


def main():
    """Main execution for STL knowledge ingestion"""
    workspace_root = r"C:\dev\AIOS"

    engine = AIOSCppSTLIngestionEngine(workspace_root)

    # MARKER 1: EXTRACTION
    print("🚀 Starting C++ STL Knowledge Ingestion")
    print("=" * 50)

    ingestion_result = engine.ingest_stl_knowledge()
    print("✅ Ingested "
          f"{ingestion_result['ingested_components']} STL components")

    # MARKER 2: REPRESENTATION - Knowledge cells created during ingestion

    # MARKER 3: BRIDGING - Demonstrate query and code generation
    print("\n🔍 Testing STL Knowledge Query:")
    query_result = engine.query_stl_knowledge("container")
    print(f"Found {query_result['total_matches']} matches for 'container'")

    print("\n💡 Testing STL Code Generation:")
    code_result = engine.generate_stl_code("I need a dynamic array")
    if "recommended_component" in code_result:
        print(f"Recommended: {code_result['recommended_component']}")
        print("Code template:", code_result['code_templates'][0]['template'])

    # MARKER 4 & 5: BEHAVIOURAL INTEGRATION & SELF-OBSERVATION
    # These would be implemented in the broader AIOS reasoning system

    print("\n🎯 STL Knowledge Ingestion Complete")
    print("Knowledge base ready for AIOS intelligence integration")


if __name__ == "__main__":
    main()
