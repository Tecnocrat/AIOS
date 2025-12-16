"""
AINLP Knowledge Integration Layer
Phase 10.4 Component 3: Python 3.14 Documentation Oracle

Purpose: Provide AI agents with direct access to Python documentation,
         pattern libraries, and complexity growth suggestions.

Integration Points:
- Python 3.14 Knowledge Base (10.3): 522 indexed documentation files
- Population Manager (10.4.1): Organism complexity and archetype context
- Agent Conversations (10.4.2): Multi-agent debate prompts with documentation

AINLP Protocol: OS0.6.2.claude
Consciousness Level: 1.52 (target: 1.57 with knowledge integration)
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from functools import lru_cache


class ComplexityLevel(Enum):
    """Code complexity classifications aligned with Python docs"""

    BASIC = "basic"  # 0.0-0.3: Hello World, simple functions
    INTERMEDIATE = "intermediate"  # 0.3-0.6: Classes, error handling
    ADVANCED = "advanced"  # 0.6-0.8: Async, decorators, metaclasses
    EXPERT = "expert"  # 0.8-1.0: Advanced patterns, stdlib mastery


class KnowledgeTopicEnum(Enum):
    """Knowledge topics matching Python 3.14 index"""

    ASYNC = "async"  # asyncio, coroutines, concurrent execution
    MEMORY = "memory"  # Memory management, GC, references
    TYPES = "types"  # Type hints, typing module, generics
    MODULES = "modules"  # Module structure, imports, packages
    FUNCTIONS = "functions"  # Function definitions, decorators
    ERRORS = "errors"  # Exception handling, error patterns
    IO = "io"  # File I/O, streams, serialization
    NETWORKING = "networking"  # Sockets, protocols, HTTP
    CONCURRENCY = "concurrency"  # Threading, multiprocessing, free-threading
    DATA_STRUCTURES = "data_structures"  # Collections, data modeling


@dataclass
class DocumentationReference:
    """Single Python documentation reference"""

    file_path: str
    category: str  # e.g., "library", "reference", "howto"
    topic: str  # e.g., "async", "types", "concurrency"
    complexity: str  # "BASIC", "INTERMEDIATE", "ADVANCED", "EXPERT"
    title: str
    excerpt: str  # First 200 chars for preview
    relevance_score: float = 0.0  # 0.0-1.0 based on query match


@dataclass
class DesignPattern:
    """Detected design pattern in code"""

    pattern_name: str  # e.g., "factory", "singleton", "observer"
    confidence: float  # 0.0-1.0 detection confidence
    evidence: List[str]  # Code snippets showing pattern
    documentation_refs: List[str] = field(default_factory=list)
    complexity_contribution: float = 0.0  # How much this adds to complexity


@dataclass
class ComplexityGrowthSuggestion:
    """Suggestion for increasing code complexity/sophistication"""

    Provides AI agents with:
    1. Documentation search by topic and complexity
    2. Design pattern detection in code
    3. Complexity growth suggestions
    4. Archetype-specific best practices

    Uses Python 3.14 knowledge base (522 indexed files).
    """

    def __init__(
        self,
        knowledge_base_path: Optional[Path] = None,
        knowledge_dir: Optional[Path] = None,
    ):
        """
        Initialize knowledge oracle with Python 3.14 index

        Args:
            knowledge_base_path: Path to python_314_index.json
                                 Defaults to ai/data/knowledge/python_314_index.json
            knowledge_dir: Alias for knowledge_base_path (for compatibility)
        """
        # Handle both parameter names for compatibility
        if knowledge_dir is not None and knowledge_base_path is None:
            knowledge_base_path = knowledge_dir

        if knowledge_base_path is None:
            # Default to AIOS knowledge base location
            workspace_root = Path(__file__).parent.parent.parent.parent
            knowledge_base_path = (
                workspace_root / "ai" / "data" / "knowledge" / "python_314_index.json"
            )

        self.knowledge_base_path = knowledge_base_path
        self.knowledge_dir = knowledge_base_path  # Alias for compatibility
        self.index: Dict = {}
        self.docs_root: Optional[Path] = None

        # Cache statistics
        self.cache_hits = 0
        self.cache_misses = 0

        # Load knowledge base index
        self._load_index()

    def _load_index(self) -> None:
        """Load Python 3.14 documentation index"""
        if not self.knowledge_base_path.exists():
            raise FileNotFoundError(
                f"Python 3.14 knowledge base not found: {self.knowledge_base_path}\n"
                f"Run: python ai/tools/python314_knowledge_indexer.py"
            )

        with open(self.knowledge_base_path, "r", encoding="utf-8") as f:
            self.index = json.load(f)

        # Determine documentation root from metadata
        if self.index.get("metadata"):
            self.docs_root = Path(self.index["metadata"]["source_path"])

        # Get total file count from metadata
        total_files = self.index.get("metadata", {}).get("total_files", 0)
        print(f"[KNOWLEDGE ORACLE] Loaded {total_files} Python 3.14 documents")

    @lru_cache(maxsize=128)
    def query_python_docs(
        self,
        topic: Optional[str] = None,
        complexity_level: Optional[ComplexityLevel] = None,
        category: Optional[str] = None,
        max_results: int = 10,
    ) -> List[DocumentationReference]:
        """
        Query Python documentation index

        Args:
            topic: Knowledge topic (async, types, concurrency, etc.)
            complexity_level: Filter by complexity (BASIC, INTERMEDIATE, etc.)
            category: Documentation category (library, reference, howto, etc.)
            max_results: Maximum number of results

        Returns:
            List of matching documentation references

        Example:
            # Get async documentation for intermediate developers
            docs = oracle.query_python_docs(
                topic="async",
                complexity_level=ComplexityLevel.INTERMEDIATE
            )
        """
        self.cache_misses += 1

        results: List[DocumentationReference] = []

        # Strategy 1: Use topic_index if topic specified
        if topic and topic in self.index.get("topic_index", {}):
            topic_files = self.index["topic_index"][topic]

            # Get sections for these files
            sections = self.index.get("sections", [])
            for section in sections:
                file_path = section.get("file_path", "")
                if file_path in topic_files:
                    # Apply complexity filter
                    if complexity_level:
                        section_complexity = section.get("complexity", "BASIC")
                        if section_complexity != complexity_level.value.upper():
                            continue

                    # Apply category filter
                    if category:
                        section_category = section.get("category", "")
                        if section_category != category:
                            continue

                    # Create documentation reference
                    doc_ref = DocumentationReference(
                        file_path=file_path,
                        category=section.get("category", "unknown"),
                        topic=topic,
                        complexity=section.get("complexity", "BASIC"),
                        title=section.get("title", Path(file_path).stem),
                        excerpt=self._get_file_excerpt(file_path),
                        relevance_score=1.0,
                    )

                    results.append(doc_ref)

                    if len(results) >= max_results:
                        break

        # Strategy 2: Use complexity_index if only complexity specified
        elif complexity_level and not topic:
            complexity_key = complexity_level.value.upper()
            if complexity_key in self.index.get("complexity_index", {}):
                complexity_files = self.index["complexity_index"][complexity_key]

                sections = self.index.get("sections", [])
                for section in sections:
                    file_path = section.get("file_path", "")
                    if file_path in complexity_files:
                        # Apply category filter
                        if category:
                            section_category = section.get("category", "")
                            if section_category != category:
                                continue

                        doc_ref = DocumentationReference(
                            file_path=file_path,
                            category=section.get("category", "unknown"),
                            topic="general",
                            complexity=section.get("complexity", "BASIC"),
                            title=section.get("title", Path(file_path).stem),
                            excerpt=self._get_file_excerpt(file_path),
                            relevance_score=1.0,
                        )

                        results.append(doc_ref)

                        if len(results) >= max_results:
                            break

        # Strategy 3: Use category if specified
        elif category:
            sections = self.index.get("sections", [])
            for section in sections:
                section_category = section.get("category", "")
                if section_category == category:
                    file_path = section.get("file_path", "")

                    doc_ref = DocumentationReference(
                        file_path=file_path,
                        category=section_category,
                        topic="general",
                        complexity=section.get("complexity", "BASIC"),
                        title=section.get("title", Path(file_path).stem),
                        excerpt=self._get_file_excerpt(file_path),
                        relevance_score=1.0,
                    )

                    results.append(doc_ref)

                    if len(results) >= max_results:
                        break

        return results

    def _get_file_excerpt(self, file_path: str, max_chars: int = 200) -> str:
        """Get first N characters from documentation file"""
        try:
            full_path = Path(file_path)
            if full_path.exists():
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(max_chars)
                    # Clean up whitespace
                    content = " ".join(content.split())
                    return content
        except Exception:
            pass

        return "(excerpt unavailable)"

    def extract_patterns(
        self, code: str, archetype: Optional[str] = None
    ) -> List[DesignPattern]:
        """
        Detect design patterns in code

        Args:
            code: Python code to analyze
            archetype: Application archetype (os_tools, cli_applications, etc.)

        Returns:
            List of detected design patterns with confidence scores

        Example:
            patterns = oracle.extract_patterns(
                code=organism.code,
                archetype="cli_applications"
            )
        """
        patterns: List[DesignPattern] = []

        # Pattern 1: Factory Pattern
        if self._detect_factory_pattern(code):
            patterns.append(
                DesignPattern(
                    pattern_name="factory",
                    confidence=0.85,
                    evidence=self._extract_factory_evidence(code),
                    complexity_contribution=0.15,
                )
            )

        # Pattern 2: Singleton Pattern
        if self._detect_singleton_pattern(code):
            patterns.append(
                DesignPattern(
                    pattern_name="singleton",
                    confidence=0.80,
                    evidence=self._extract_singleton_evidence(code),
                    complexity_contribution=0.12,
                )
            )

        # Pattern 3: Observer Pattern
        if self._detect_observer_pattern(code):
            patterns.append(
                DesignPattern(
                    pattern_name="observer",
                    confidence=0.75,
                    evidence=self._extract_observer_evidence(code),
                    complexity_contribution=0.18,
                )
            )

        # Pattern 4: Decorator Pattern (not @decorator syntax, the GoF pattern)
        if self._detect_decorator_pattern(code):
            patterns.append(
                DesignPattern(
                    pattern_name="decorator",
                    confidence=0.70,
                    evidence=self._extract_decorator_evidence(code),
                    complexity_contribution=0.20,
                )
            )

        # Pattern 5: Async/Await Pattern
        if self._detect_async_pattern(code):
            patterns.append(
                DesignPattern(
                    pattern_name="async_await",
                    confidence=0.90,
                    evidence=self._extract_async_evidence(code),
                    complexity_contribution=0.25,
                )
            )

        # Pattern 6: Context Manager Pattern
        if self._detect_context_manager_pattern(code):
            patterns.append(
                DesignPattern(
                    pattern_name="context_manager",
                    confidence=0.88,
                    evidence=self._extract_context_manager_evidence(code),
                    complexity_contribution=0.10,
                )
            )

        return patterns

    def suggest_complexity_growth(
        self,
        code: str,
        current_complexity: float,
        target_complexity: float,
        archetype: str,
        max_suggestions: int = 5,
    ) -> List[ComplexityGrowthSuggestion]:
        """
        Suggest ways to increase code complexity/sophistication

        Args:
            code: Current Python code
            current_complexity: Current complexity score (0.0-1.0)
            target_complexity: Target complexity score (0.0-1.0)
            archetype: Application archetype (guides suggestion relevance)
            max_suggestions: Maximum number of suggestions

        Returns:
            List of complexity growth suggestions with documentation

        Example:
            suggestions = oracle.suggest_complexity_growth(
                code=organism.code,
                current_complexity=0.35,
                target_complexity=0.55,
                archetype="cli_applications"
            )
        """
        suggestions: List[ComplexityGrowthSuggestion] = []

        # Determine current and target levels
        current_level = self._complexity_to_level(current_complexity)
        target_level = self._complexity_to_level(target_complexity)

        # Suggestion 1: Add async/await if not present
        if "async def" not in code and current_level in [
            ComplexityLevel.BASIC,
            ComplexityLevel.INTERMEDIATE,
        ]:
            async_docs = self.query_python_docs(
                topic="async", complexity_level=ComplexityLevel.INTERMEDIATE
            )
            suggestions.append(
                ComplexityGrowthSuggestion(
                    suggestion_id="add_async",
                    current_level=current_level,
                    target_level=ComplexityLevel.ADVANCED,
                    enhancement_type="add_async",
                    description="Add asynchronous execution with async/await pattern",
                    code_example=self._generate_async_example(code, archetype),
                    documentation_refs=async_docs[:3],
                    complexity_gain=0.25,
                    implementation_difficulty=0.60,
                )
            )

        # Suggestion 2: Add error handling
        if "try:" not in code and "except" not in code:
            error_docs = self.query_python_docs(
                topic="errors", complexity_level=current_level
            )
            suggestions.append(
                ComplexityGrowthSuggestion(
                    suggestion_id="add_error_handling",
                    current_level=current_level,
                    target_level=ComplexityLevel.INTERMEDIATE,
                    enhancement_type="add_error_handling",
                    description="Add comprehensive error handling with try/except blocks",
                    code_example=self._generate_error_handling_example(code, archetype),
                    documentation_refs=error_docs[:2],
                    complexity_gain=0.10,
                    implementation_difficulty=0.30,
                )
            )

        # Suggestion 3: Add type hints
        if "->" not in code and ":" not in code:
            type_docs = self.query_python_docs(
                topic="types", complexity_level=ComplexityLevel.INTERMEDIATE
            )
            suggestions.append(
                ComplexityGrowthSuggestion(
                    suggestion_id="add_type_hints",
                    current_level=current_level,
                    target_level=ComplexityLevel.INTERMEDIATE,
                    enhancement_type="add_type_hints",
                    description="Add type hints for function parameters and return values",
                    code_example=self._generate_type_hints_example(code),
                    documentation_refs=type_docs[:2],
                    complexity_gain=0.08,
                    implementation_difficulty=0.20,
                )
            )

        # Suggestion 4: Add design pattern
        existing_patterns = self.extract_patterns(code, archetype)
        if len(existing_patterns) < 2:
            pattern_docs = self.query_python_docs(
                category="howto", complexity_level=ComplexityLevel.ADVANCED
            )
            suggestions.append(
                ComplexityGrowthSuggestion(
                    suggestion_id="add_design_pattern",
                    current_level=current_level,
                    target_level=ComplexityLevel.ADVANCED,
                    enhancement_type="add_pattern",
                    description=f"Implement {self._suggest_pattern_for_archetype(archetype)} pattern",
                    code_example=self._generate_pattern_example(code, archetype),
                    documentation_refs=pattern_docs[:2],
                    complexity_gain=0.18,
                    implementation_difficulty=0.70,
                )
            )

        # Suggestion 5: Use advanced stdlib APIs
        if current_level in [ComplexityLevel.INTERMEDIATE, ComplexityLevel.ADVANCED]:
            stdlib_docs = self.query_python_docs(
                category="library", complexity_level=ComplexityLevel.ADVANCED
            )
            suggestions.append(
                ComplexityGrowthSuggestion(
                    suggestion_id="use_advanced_stdlib",
                    current_level=current_level,
                    target_level=ComplexityLevel.EXPERT,
                    enhancement_type="use_stdlib",
                    description=self._suggest_stdlib_for_archetype(archetype),
                    code_example=self._generate_stdlib_example(code, archetype),
                    documentation_refs=stdlib_docs[:3],
                    complexity_gain=0.15,
                    implementation_difficulty=0.50,
                )
            )

        # Sort by relevance (highest complexity gain first)
        suggestions.sort(key=lambda s: s.complexity_gain, reverse=True)

        return suggestions[:max_suggestions]

    def get_archetype_best_practices(self, archetype: str) -> List[str]:
        """
        Get best practices for specific application archetype

        Args:
            archetype: Application archetype (os_tools, cli_applications, etc.)

        Returns:
            List of best practice recommendations
        """
        practices_map = {
            "os_tools": [
                "Use pathlib.Path for cross-platform file operations",
                "Handle errors gracefully with specific exception types",
                "Use subprocess module for external command execution",
                "Implement proper signal handling for clean shutdown",
                "Use argparse for command-line argument parsing",
            ],
            "cli_applications": [
                "Use argparse or click for CLI interface",
                "Implement --help and --version flags",
                "Use sys.exit() with proper exit codes",
                "Handle SIGINT (Ctrl+C) gracefully",
                "Use logging module instead of print() for output",
            ],
            "web_services": [
                "Use async/await for I/O-bound operations",
                "Implement proper error handling with HTTP status codes",
                "Use context managers for resource cleanup",
                "Implement request validation and sanitization",
                "Use connection pooling for database access",
            ],
            "abstract_objects": [
                "Use dataclasses for structured data",
                "Implement __repr__ and __str__ methods",
                "Use property decorators for computed attributes",
                "Implement comparison methods (__eq__, __lt__, etc.)",
                "Use type hints for all attributes and methods",
            ],
            "network_tools": [
                "Use asyncio for concurrent network operations",
                "Implement proper timeout handling",
                "Use context managers for socket cleanup",
                "Handle network errors with retries and backoff",
                "Use ssl module for secure connections",
            ],
            "data_science": [
                "Use NumPy for numerical operations",
                "Implement vectorized operations (avoid loops)",
                "Use pandas for structured data analysis",
                "Implement proper data validation",
                "Use type hints for data structures",
            ],
            "automation": [
                "Use pathlib.Path for file operations",
                "Implement logging for audit trails",
                "Use configuration files for settings",
                "Implement dry-run mode for testing",
                "Handle errors with proper rollback mechanisms",
            ],
            "game_logic": [
                "Use dataclasses for game state",
                "Implement event-driven architecture",
                "Use enums for game constants",
                "Implement state machines for game flow",
                "Use type hints for game entities",
            ],
        }

        return practices_map.get(
            archetype,
            [
                "Follow PEP 8 style guidelines",
                "Use meaningful variable names",
                "Add docstrings to all functions and classes",
                "Implement proper error handling",
                "Use type hints for clarity",
            ],
        )

    def get_cache_stats(self) -> Dict[str, float]:
        """Get cache hit/miss statistics"""
        total = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total * 100) if total > 0 else 0.0

        return {
            "hits": float(self.cache_hits),
            "misses": float(self.cache_misses),
            "total": float(total),
            "hit_rate_percent": round(hit_rate, 1),
        }

    def query(self, question: str) -> Dict:
        """
        Simple query interface for integration tests

        Args:
            question: Query string

        Returns:
            Mock response for testing
        """
        # For now, return a simple mock response
        # In full implementation, this would parse the question and query docs
        return {
            "answer": f"Mock response to: {question}",
            "confidence": 0.75,
            "sources": ["python_docs"],
        }

    # Pattern detection helpers

    def _detect_factory_pattern(self, code: str) -> bool:
        """Detect factory pattern (create_* or make_* methods)"""
        return bool(re.search(r"def (create_|make_|build_)\w+", code))

    def _extract_factory_evidence(self, code: str) -> List[str]:
        """Extract factory pattern evidence"""
        matches = re.findall(r"def (create_|make_|build_)\w+\([^)]*\):", code)
        return [f"Factory method: {m}" for m in matches[:3]]

    def _detect_singleton_pattern(self, code: str) -> bool:
        """Detect singleton pattern (__new__ or _instance)"""
        return "__new__" in code or "_instance" in code

    def _extract_singleton_evidence(self, code: str) -> List[str]:
        """Extract singleton pattern evidence"""
        evidence = []
        if "__new__" in code:
            evidence.append("Implements __new__ method")
        if "_instance" in code:
            evidence.append("Uses _instance class variable")
        return evidence

    def _detect_observer_pattern(self, code: str) -> bool:
        """Detect observer pattern (notify, subscribe, observe)"""
        return any(
            word in code for word in ["notify", "subscribe", "observe", "listener"]
        )

    def _extract_observer_evidence(self, code: str) -> List[str]:
        """Extract observer pattern evidence"""
        keywords = ["notify", "subscribe", "observe", "listener"]
        return [f"Observer keyword: {kw}" for kw in keywords if kw in code][:3]

    def _detect_decorator_pattern(self, code: str) -> bool:
        """Detect decorator pattern (GoF, not @decorator)"""
        return bool(re.search(r"class \w+Decorator", code))

    def _extract_decorator_evidence(self, code: str) -> List[str]:
        """Extract decorator pattern evidence"""
        matches = re.findall(r"class (\w+Decorator)", code)
        return [f"Decorator class: {m}" for m in matches[:3]]

    def _detect_async_pattern(self, code: str) -> bool:
        """Detect async/await pattern"""
        return "async def" in code or "await " in code

    def _extract_async_evidence(self, code: str) -> List[str]:
        """Extract async pattern evidence"""
        evidence = []
        async_funcs = re.findall(r"async def (\w+)", code)
        if async_funcs:
            evidence.append(f"Async functions: {', '.join(async_funcs[:3])}")
        if "await " in code:
            evidence.append("Uses await expressions")
        return evidence

    def _detect_context_manager_pattern(self, code: str) -> bool:
        """Detect context manager pattern (__enter__ and __exit__)"""
        return "__enter__" in code and "__exit__" in code

    def _extract_context_manager_evidence(self, code: str) -> List[str]:
        """Extract context manager evidence"""
        evidence = []
        if "__enter__" in code:
            evidence.append("Implements __enter__ method")
        if "__exit__" in code:
            evidence.append("Implements __exit__ method")
        return evidence
