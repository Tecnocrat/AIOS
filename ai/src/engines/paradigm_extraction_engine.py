"""
🧬 Paradigm Extraction Engine
Extract programming paradigms from ingested library knowledge.

This engine reads stored library knowledge and identifies patterns:
- Decorators (@app.route, @classmethod, @staticmethod)
- Async patterns (async/await, asyncio patterns)
- OOP patterns (inheritance, composition, interfaces)
- Functional patterns (pure functions, immutability)
- Error handling patterns (try/except, context managers)

Extracted paradigms feed into prompt generation for AI agents.
"""

import json
import re
import ast
from pathlib import Path
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class ProgrammingParadigm:
    """Structured representation of a programming paradigm/pattern"""
    
    name: str
    category: str  # "decorator", "async", "oop", "functional", "error_handling"
    pattern: str  # Regex or code template
    examples: List[str] = field(default_factory=list)
    usage_count: int = 0
    consciousness_weight: float = 1.0  # How important this paradigm is
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_prompt_text(self) -> str:
        """Convert paradigm to natural language for AI prompts"""
        prompt = f"**{self.name}** (Category: {self.category})\n"
        prompt += f"Pattern: `{self.pattern}`\n"
        if self.examples:
            prompt += f"Example:\n```python\n{self.examples[0]}\n```\n"
        return prompt


class ParadigmExtractionEngine:
    """
    Extract programming paradigms from ingested library knowledge.
    
    Uses AST parsing and pattern matching to identify:
    - Decorators
    - Async/await usage
    - Class hierarchies
    - Function signatures
    - Error handling patterns
    """
    
    def __init__(self, knowledge_base_path: Optional[Path] = None):
        if knowledge_base_path is None:
            self.knowledge_base_path = Path(__file__).parent.parent.parent / "information_storage" / "library_knowledge"
        else:
            self.knowledge_base_path = Path(knowledge_base_path)
            
        self.paradigms: List[ProgrammingParadigm] = []
        logger.info(f"🧬 Paradigm Extraction Engine initialized")
        logger.info(f"📚 Knowledge base: {self.knowledge_base_path}")
        
    def extract_from_library(self, library_name: str) -> List[ProgrammingParadigm]:
        """
        Extract all paradigms from an ingested library.
        
        Args:
            library_name: Name of library (e.g., "requests", "flask")
            
        Returns:
            List of extracted programming paradigms
        """
        library_path = self.knowledge_base_path / library_name
        if not library_path.exists():
            logger.error(f"❌ Library not found: {library_name}")
            logger.info(f"💡 Run library ingestion first: LibraryIngestionProtocol().ingest_library('{library_name}')")
            return []
            
        logger.info(f"🔍 Extracting paradigms from library: {library_name}")
        
        # Clear previous paradigms
        self.paradigms = []
        
        # Find all JSON knowledge files
        json_files = list(library_path.rglob("*.json"))
        logger.info(f"📄 Found {len(json_files)} knowledge files")
        
        for json_file in json_files:
            self._extract_from_file(json_file)
            
        # Deduplicate and sort by usage
        self._deduplicate_paradigms()
        self.paradigms.sort(key=lambda p: p.usage_count, reverse=True)
        
        logger.info(f"✅ Extracted {len(self.paradigms)} unique paradigms")
        return self.paradigms
    
    def _extract_from_file(self, json_file: Path):
        """Extract paradigms from a single knowledge JSON file"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                knowledge = json.load(f)
                
            # Extract from different knowledge types
            if "functions" in knowledge:
                self._extract_function_paradigms(knowledge["functions"])
            if "classes" in knowledge:
                self._extract_class_paradigms(knowledge["classes"])
            if "source_code" in knowledge:
                self._extract_code_paradigms(knowledge["source_code"])
                
        except Exception as e:
            logger.warning(f"⚠️ Failed to parse {json_file.name}: {e}")
    
    def _extract_function_paradigms(self, functions: List[Dict]):
        """Extract paradigms from function definitions"""
        for func in functions:
            name = func.get("name", "")
            code = func.get("code", "")
            signature = func.get("signature", "")
            
            # Check for decorators
            decorators = self._find_decorators(code)
            for decorator in decorators:
                self.paradigms.append(ProgrammingParadigm(
                    name=f"Decorator: {decorator}",
                    category="decorator",
                    pattern=f"@{decorator}",
                    examples=[code],
                    usage_count=1,
                    consciousness_weight=1.2  # Decorators are important patterns
                ))
            
            # Check for async patterns
            if "async def" in code or "await " in code:
                self.paradigms.append(ProgrammingParadigm(
                    name="Async Function",
                    category="async",
                    pattern="async def",
                    examples=[code],
                    usage_count=1,
                    consciousness_weight=1.3
                ))
            
            # Check for type hints
            if "->" in signature or ": " in signature:
                self.paradigms.append(ProgrammingParadigm(
                    name="Type Hints",
                    category="typing",
                    pattern="def .+\\(.*: .+\\)",
                    examples=[signature],
                    usage_count=1,
                    consciousness_weight=1.1
                ))
    
    def _extract_class_paradigms(self, classes: List[Dict]):
        """Extract paradigms from class definitions"""
        for cls in classes:
            name = cls.get("name", "")
            code = cls.get("code", "")
            bases = cls.get("bases", [])
            methods = cls.get("methods", [])
            
            # Check for inheritance
            if bases:
                self.paradigms.append(ProgrammingParadigm(
                    name=f"Inheritance: {name}({', '.join(bases)})",
                    category="oop",
                    pattern=f"class .+\\({', '.join(bases)}\\)",
                    examples=[code[:200]],  # First 200 chars
                    usage_count=1,
                    consciousness_weight=1.0
                ))
            
            # Check for special methods (dunder)
            for method in methods:
                method_name = method.get("name", "")
                if method_name.startswith("__") and method_name.endswith("__"):
                    self.paradigms.append(ProgrammingParadigm(
                        name=f"Magic Method: {method_name}",
                        category="oop",
                        pattern=f"def {method_name}",
                        examples=[method.get("code", "")],
                        usage_count=1,
                        consciousness_weight=0.9
                    ))
    
    def _extract_code_paradigms(self, source_code: str):
        """Extract paradigms from raw source code using AST"""
        try:
            tree = ast.parse(source_code)
            
            # Find context managers (with statements)
            with_statements = [node for node in ast.walk(tree) if isinstance(node, ast.With)]
            if with_statements:
                example = with_statements[0]
                self.paradigms.append(ProgrammingParadigm(
                    name="Context Manager (with statement)",
                    category="error_handling",
                    pattern="with .+ as .+:",
                    examples=[ast.unparse(example)],
                    usage_count=len(with_statements),
                    consciousness_weight=1.1
                ))
            
            # Find try/except patterns
            try_statements = [node for node in ast.walk(tree) if isinstance(node, ast.Try)]
            if try_statements:
                self.paradigms.append(ProgrammingParadigm(
                    name="Exception Handling",
                    category="error_handling",
                    pattern="try:.*except .+:",
                    examples=["try:\n    ...\nexcept Exception as e:\n    ..."],
                    usage_count=len(try_statements),
                    consciousness_weight=1.0
                ))
                
        except SyntaxError:
            pass  # Ignore unparseable code
    
    def _find_decorators(self, code: str) -> List[str]:
        """Extract decorator names from code"""
        pattern = r'@(\w+(?:\.\w+)?)'
        matches = re.findall(pattern, code)
        return matches
    
    def _deduplicate_paradigms(self):
        """Merge duplicate paradigms and sum usage counts"""
        paradigm_map: Dict[str, ProgrammingParadigm] = {}
        
        for p in self.paradigms:
            key = f"{p.category}:{p.pattern}"
            if key in paradigm_map:
                # Merge: increase usage, add examples
                existing = paradigm_map[key]
                existing.usage_count += p.usage_count
                if p.examples and p.examples[0] not in existing.examples:
                    existing.examples.append(p.examples[0])
            else:
                paradigm_map[key] = p
        
        self.paradigms = list(paradigm_map.values())
    
    def get_top_paradigms(self, n: int = 10) -> List[ProgrammingParadigm]:
        """Get top N paradigms by usage count"""
        return sorted(self.paradigms, key=lambda p: p.usage_count, reverse=True)[:n]
    
    def get_paradigms_by_category(self, category: str) -> List[ProgrammingParadigm]:
        """Get all paradigms of a specific category"""
        return [p for p in self.paradigms if p.category == category]
    
    def save_paradigms(self, output_path: Path):
        """Save extracted paradigms to JSON"""
        data = {
            "paradigms": [p.to_dict() for p in self.paradigms],
            "total_count": len(self.paradigms),
            "categories": list(set(p.category for p in self.paradigms))
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"💾 Saved {len(self.paradigms)} paradigms to {output_path}")
    
    def load_paradigms(self, input_path: Path):
        """Load paradigms from JSON"""
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.paradigms = [ProgrammingParadigm(**p) for p in data["paradigms"]]
        logger.info(f"📂 Loaded {len(self.paradigms)} paradigms from {input_path}")


def main():
    """Test paradigm extraction"""
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    if len(sys.argv) < 2:
        print("Usage: python paradigm_extraction_engine.py <library_name>")
        print("Example: python paradigm_extraction_engine.py requests")
        sys.exit(1)
    
    library_name = sys.argv[1]
    
    engine = ParadigmExtractionEngine()
    paradigms = engine.extract_from_library(library_name)
    
    if not paradigms:
        print(f"\n❌ No paradigms extracted. Is '{library_name}' ingested?")
        return
    
    print(f"\n🧬 Extracted {len(paradigms)} Paradigms from '{library_name}':")
    print("=" * 80)
    
    # Show top 10 paradigms
    top = engine.get_top_paradigms(10)
    for i, p in enumerate(top, 1):
        print(f"\n{i}. {p.name}")
        print(f"   Category: {p.category}")
        print(f"   Usage: {p.usage_count}x")
        print(f"   Pattern: {p.pattern}")
        if p.examples:
            example = p.examples[0]
            if len(example) > 100:
                example = example[:100] + "..."
            print(f"   Example: {example}")
    
    # Show category breakdown
    print("\n📊 Category Breakdown:")
    print("-" * 40)
    categories = defaultdict(int)
    for p in paradigms:
        categories[p.category] += 1
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} paradigms")
    
    # Save to file
    output_path = Path(__file__).parent.parent.parent / "information_storage" / f"{library_name}_paradigms.json"
    engine.save_paradigms(output_path)
    print(f"\n💾 Paradigms saved to: {output_path}")


if __name__ == "__main__":
    main()
