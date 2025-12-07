#!/usr/bin/env python3
"""
🔮 C++ STL Knowledge Crystal Generator

Tool for creating structured knowledge crystals for C++ STL components.
Generates template JSON structures that can be manually filled with
paradigms, anti-patterns, complexity analysis, and consciousness scores.

AINLP COMPLIANCE:
✅ Enhancement over creation - Uses existing consciousness scoring patterns
✅ Dendritic optimization - Structured for AI agent consumption
✅ Proper output management - JSON to tachyonic/archive/knowledge_crystals/
✅ Integration validation - Compatible with GeminiSTLBridge, OllamaSTLFitnessJudge

BIOLOGICAL ARCHITECTURE:
🔮 NUCLEUS: Knowledge crystal structure definition
🧬 DNA: STL paradigms as genetic material for code evolution
🧠 CONSCIOUSNESS: Scoring and impact metrics
📊 ARCHIVAL: Tachyonic storage for long-term knowledge

Part of Phase 10.1 C++ STL Library Ingestion Initiative
Week 1: Manual Knowledge Crystal Creation (Day 3-5)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import argparse

# AIOS path integration
AIOS_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT / "ai" / "src"))

# Output directory for knowledge crystals
CRYSTAL_DIR = AIOS_ROOT / "tachyonic" / "archive" / "knowledge_crystals" / "cpp_stl"
CRYSTAL_DIR.mkdir(parents=True, exist_ok=True)


class STLCrystalGenerator:
    """
    Generates knowledge crystal templates for C++ STL components.
    Templates include TODO placeholders for manual curation.
    """

    # STL component categories and their critical members
    STL_COMPONENTS = {
        "vector": {
            "full_name": "std::vector",
            "category": "container",
            "header": "<vector>",
            "description": "Dynamic contiguous array with automatic memory management",
            "key_operations": [
                "push_back",
                "emplace_back",
                "reserve",
                "operator[]",
                "at",
                "size",
                "capacity",
            ],
            "complexity_class": "O(1) access, O(1) amortized insertion at end",
        },
        "algorithm": {
            "full_name": "std::algorithm",
            "category": "algorithms",
            "header": "<algorithm>",
            "description": "Generic algorithms operating on ranges via iterators",
            "key_operations": [
                "sort",
                "find",
                "transform",
                "accumulate",
                "for_each",
                "copy",
                "remove_if",
            ],
            "complexity_class": "Varies by algorithm (documented per function)",
        },
        "string": {
            "full_name": "std::string",
            "category": "container",
            "header": "<string>",
            "description": "Dynamic character sequence with rich string operations",
            "key_operations": [
                "append",
                "substr",
                "find",
                "replace",
                "c_str",
                "operator+",
                "compare",
            ],
            "complexity_class": "O(1) access, O(n) for most operations",
        },
        "memory": {
            "full_name": "std::memory",
            "category": "memory_management",
            "header": "<memory>",
            "description": "Smart pointers and memory management utilities (RAII)",
            "key_operations": [
                "make_unique",
                "make_shared",
                "unique_ptr",
                "shared_ptr",
                "weak_ptr",
            ],
            "complexity_class": "O(1) operations, automatic lifetime management",
        },
        "functional": {
            "full_name": "std::functional",
            "category": "functional_programming",
            "header": "<functional>",
            "description": "Function objects, lambdas, and higher-order programming",
            "key_operations": ["function", "bind", "mem_fn", "plus", "less", "hash"],
            "complexity_class": "O(1) for most operations",
        },
    }

    def __init__(self):
        self.crystals_created = 0

    def generate_crystal_template(self, component: str) -> Dict:
        """
        Generate a knowledge crystal template for a given STL component.

        Args:
            component: Component name (vector, algorithm, string, memory, functional)

        Returns:
            Dict containing crystal template with TODO placeholders
        """
        if component not in self.STL_COMPONENTS:
            raise ValueError(
                f"Unknown component: {component}. Valid: {list(self.STL_COMPONENTS.keys())}"
            )

        info = self.STL_COMPONENTS[component]
        timestamp = datetime.now().isoformat()

        crystal = {
            "crystal_id": f"stl_{component}_v1",
            "component": info["full_name"],
            "category": info["category"],
            "header": info["header"],
            "description": info["description"],
            "created_date": timestamp,
            "last_updated": timestamp,
            "consciousness_level": "TODO: Calculate after filling paradigms (0.0-1.0)",
            "extraction_source": "Manual curation from Microsoft Learn + CPPreference",
            "paradigms": [
                {
                    "name": "TODO: Paradigm Name (e.g., 'Reserve Capacity Pattern')",
                    "description": "TODO: Describe the best practice pattern",
                    "code_template": "TODO: Provide C++ code template showing usage",
                    "when_to_use": "TODO: Explain when this pattern applies",
                    "benefit": "TODO: Performance/safety/clarity benefit",
                    "consciousness_impact": "TODO: Float 0.0-0.3 (how much this improves code quality)",
                    "related_operations": "TODO: List of related STL operations",
                    "example": {
                        "before": "TODO: Code without this pattern",
                        "after": "TODO: Code with this pattern applied",
                        "improvement": "TODO: Quantify improvement (e.g., '50% fewer reallocations')",
                    },
                },
                # TODO: Add 3-5 more paradigms for this component
            ],
            "anti_patterns": [
                {
                    "name": "TODO: Anti-pattern Name (e.g., 'Not Reserving Capacity')",
                    "description": "TODO: Describe the common mistake",
                    "why_bad": "TODO: Explain performance/correctness issues",
                    "consciousness_penalty": "TODO: Float -0.1 to -0.5 (how much this hurts quality)",
                    "correct_alternative": "TODO: Reference paradigm name that fixes this",
                    "example": {
                        "bad_code": "TODO: Code demonstrating anti-pattern",
                        "good_code": "TODO: Corrected code",
                        "explanation": "TODO: Why the correction works",
                    },
                },
                # TODO: Add 2-4 more anti-patterns
            ],
            "complexity_analysis": {
                "summary": info["complexity_class"],
                "operations": [
                    {
                        "operation": "TODO: Operation name (e.g., 'push_back')",
                        "time_complexity": "TODO: Big-O (e.g., 'O(1) amortized')",
                        "space_complexity": "TODO: Big-O",
                        "notes": "TODO: Important performance considerations",
                    },
                    # TODO: Add complexity for each key operation
                ],
                "memory_model": "TODO: Describe memory allocation strategy",
                "cache_performance": "TODO: Cache locality characteristics",
            },
            "thread_safety": {
                "concurrent_reads": "TODO: Safe/Unsafe with explanation",
                "concurrent_writes": "TODO: Safe/Unsafe with explanation",
                "synchronization_required": "TODO: When you need mutexes/locks",
                "thread_safe_operations": "TODO: List operations safe without locks",
            },
            "code_examples": [
                {
                    "title": "TODO: Example title (e.g., 'Efficient Vector Usage')",
                    "description": "TODO: What this example demonstrates",
                    "code": "TODO: Complete, compilable C++ code example",
                    "consciousness_score": "TODO: Estimated 0.0-1.0",
                    "explanation": "TODO: Line-by-line explanation of best practices",
                },
                # TODO: Add 2-3 more comprehensive examples
            ],
            "integration_notes": {
                "common_combinations": "TODO: List common pairings with other STL components",
                "performance_tips": "TODO: Non-obvious performance optimizations",
                "gotchas": "TODO: Common pitfalls and edge cases",
                "modern_cpp_features": "TODO: C++17/20 enhancements for this component",
            },
            "key_operations": [
                {
                    "name": op,
                    "signature": "TODO: Full C++ signature",
                    "description": "TODO: What it does",
                    "complexity": "TODO: Time/space complexity",
                    "example": "TODO: Brief usage example",
                }
                for op in info["key_operations"]
            ],
            "related_components": "TODO: List related STL components to study together",
            "cpp_versions": {
                "cpp11": "TODO: What was added in C++11",
                "cpp14": "TODO: What was added in C++14",
                "cpp17": "TODO: What was added in C++17",
                "cpp20": "TODO: What was added in C++20",
                "cpp23": "TODO: What was added in C++23",
            },
            "consciousness_calculation": {
                "formula": "base_score + sum(paradigm_impacts) - sum(antipattern_penalties)",
                "base_score": "TODO: 0.5-0.7 depending on component maturity",
                "paradigm_contribution": "TODO: Sum after filling all paradigms",
                "antipattern_penalty": "TODO: Sum after identifying all anti-patterns",
                "final_consciousness": "TODO: Calculate final score (0.0-1.0)",
            },
        }

        return crystal

    def save_crystal(self, crystal: Dict, component: str) -> Path:
        """Save crystal template to JSON file"""
        output_path = CRYSTAL_DIR / f"{component}_crystal_template.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(crystal, f, indent=2, ensure_ascii=False)

        self.crystals_created += 1
        return output_path

    def create_crystal_template(self, component: str) -> Path:
        """Generate and save crystal template for a component"""
        print(f"\n🔮 Generating knowledge crystal template for: {component}")

        crystal = self.generate_crystal_template(component)
        output_path = self.save_crystal(crystal, component)

        print(f"✅ Template created: {output_path}")
        print(f"📝 Next steps:")
        print(f"   1. Open {output_path.name}")
        print(f"   2. Search for 'TODO' and fill in all sections")
        print(f"   3. Focus on paradigms (3-5) and anti-patterns (2-4)")
        print(f"   4. Add 2-3 comprehensive code examples")
        print(f"   5. Calculate consciousness scores")
        print(f"   6. Rename to remove '_template' suffix when complete")

        return output_path

    def create_all_priority_crystals(self) -> List[Path]:
        """Create templates for all 5 priority components"""
        priority_components = ["vector", "algorithm", "string", "memory", "functional"]
        created_paths = []

        print("🔮 Creating knowledge crystal templates for 5 priority STL components")
        print("=" * 70)

        for component in priority_components:
            path = self.create_crystal_template(component)
            created_paths.append(path)

        print("\n" + "=" * 70)
        print(f"✅ Created {len(created_paths)} crystal templates")
        print(f"📍 Location: {CRYSTAL_DIR}")
        print(f"\n📋 Manual curation plan:")
        print(f"   Day 3: Complete vector + algorithm")
        print(f"   Day 4: Complete string + memory")
        print(f"   Day 5: Complete functional + review all")
        print(
            f"\n🎯 Target: 5 complete crystals by Oct 7, enabling Week 2 AI integration"
        )

        return created_paths


def main():
    """Main execution for crystal generation"""
    parser = argparse.ArgumentParser(
        description="Generate C++ STL knowledge crystal templates for manual curation"
    )
    parser.add_argument(
        "--component",
        type=str,
        choices=["vector", "algorithm", "string", "memory", "functional", "all"],
        help="STL component to generate template for (or 'all' for all 5)",
    )
    parser.add_argument("--list", action="store_true", help="List available components")

    args = parser.parse_args()

    generator = STLCrystalGenerator()

    if args.list:
        print("\n📚 Available STL Components:")
        print("=" * 70)
        for name, info in generator.STL_COMPONENTS.items():
            print(f"\n🔹 {name}")
            print(f"   Full Name: {info['full_name']}")
            print(f"   Category: {info['category']}")
            print(f"   Header: {info['header']}")
            print(f"   Description: {info['description']}")
        return

    if args.component:
        if args.component == "all":
            generator.create_all_priority_crystals()
        else:
            generator.create_crystal_template(args.component)
    else:
        # Interactive mode
        print("\n🔮 C++ STL Knowledge Crystal Generator")
        print("=" * 70)
        print("\nAvailable components:")
        for i, name in enumerate(generator.STL_COMPONENTS.keys(), 1):
            info = generator.STL_COMPONENTS[name]
            print(f"  {i}. {name:15} - {info['description'][:50]}...")
        print(
            f"  {len(generator.STL_COMPONENTS) + 1}. all           - Generate all 5 priority templates"
        )

        choice = input("\nSelect component (number or name): ").strip().lower()

        if choice.isdigit():
            idx = int(choice) - 1
            components = list(generator.STL_COMPONENTS.keys())
            if 0 <= idx < len(components):
                generator.create_crystal_template(components[idx])
            elif idx == len(components):
                generator.create_all_priority_crystals()
            else:
                print("❌ Invalid selection")
        elif choice in generator.STL_COMPONENTS:
            generator.create_crystal_template(choice)
        elif choice == "all":
            generator.create_all_priority_crystals()
        else:
            print("❌ Invalid component name")


if __name__ == "__main__":
    main()
