#!/usr/bin/env python3
"""
🧪 Tests for AIOS Library Ingestion Protocol

Comprehensive test suite for library ingestion protocol system,
validating multi-language parsing, semantic analysis, consciousness
integration, and AINLP compliance.
"""

import asyncio
import json
import tempfile
import shutil
from pathlib import Path
import sys

# Add src/core to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from library_ingestion_protocol import (
    LibraryIngestionProtocol,
    ProgrammingLanguage,
    APIElementType,
    LibraryKnowledge,
    APIElement,
)


class TestLibraryIngestionProtocol:
    """Test suite for Library Ingestion Protocol"""

    def __init__(self):
        self.test_results = []
        self.temp_dir = None
        self.protocol = None

    def setup(self):
        """Set up test environment"""
        print("🔧 Setting up test environment...")
        self.temp_dir = Path(tempfile.mkdtemp())
        self.protocol = LibraryIngestionProtocol(
            knowledge_base_path=self.temp_dir / "knowledge_base",
            consciousness_level=0.8,
        )
        print(f"   Test directory: {self.temp_dir}")

    def teardown(self):
        """Clean up test environment"""
        print("🧹 Cleaning up test environment...")
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def assert_true(self, condition: bool, message: str):
        """Assert condition is true"""
        if condition:
            self.test_results.append(("PASS", message))
            print(f"   ✅ {message}")
        else:
            self.test_results.append(("FAIL", message))
            print(f"   ❌ {message}")

    def assert_equal(self, actual, expected, message: str):
        """Assert values are equal"""
        if actual == expected:
            self.test_results.append(("PASS", message))
            print(f"   ✅ {message}")
        else:
            self.test_results.append(
                ("FAIL", f"{message} (got {actual}, expected {expected})")
            )
            print(f"   ❌ {message} (got {actual}, expected {expected})")

    def test_language_detection(self):
        """Test programming language detection from file extensions"""
        print("\n🧪 Test: Language Detection")

        test_cases = [
            ("test.py", ProgrammingLanguage.PYTHON),
            ("test.cpp", ProgrammingLanguage.CPP),
            ("test.java", ProgrammingLanguage.JAVA),
            ("test.js", ProgrammingLanguage.JAVASCRIPT),
            ("test.c", ProgrammingLanguage.C),
            ("test.php", ProgrammingLanguage.PHP),
            ("test.asm", ProgrammingLanguage.ASSEMBLY),
            ("test.unknown", ProgrammingLanguage.UNKNOWN),
        ]

        for filename, expected_lang in test_cases:
            detected = self.protocol.detect_language(filename)
            self.assert_equal(
                detected, expected_lang, f"Detected {detected.value} for {filename}"
            )

    async def test_python_parsing(self):
        """Test Python library parsing"""
        print("\n🧪 Test: Python Parsing")

        # Create test Python file
        test_file = self.temp_dir / "test_module.py"
        test_content = '''
"""Test module for library ingestion"""

def calculate_sum(a: int, b: int) -> int:
    """Calculate sum of two numbers"""
    return a + b

class DataProcessor:
    """Process data with AI capabilities"""
    
    def process(self, data):
        """Process the data"""
        pass
    
    def train_model(self, dataset):
        """Train AI model on dataset"""
        pass
'''

        test_file.write_text(test_content)

        # Parse the file
        api_elements = await self.protocol._parse_source_file(
            test_file, ProgrammingLanguage.PYTHON
        )

        self.assert_true(
            len(api_elements) > 0,
            f"Parsed {len(api_elements)} API elements from Python file",
        )

        # Check for specific elements
        func_names = [
            elem.name
            for elem in api_elements
            if elem.element_type == APIElementType.FUNCTION
        ]
        class_names = [
            elem.name
            for elem in api_elements
            if elem.element_type == APIElementType.CLASS
        ]

        self.assert_true(
            "calculate_sum" in func_names, "Found function 'calculate_sum'"
        )

        self.assert_true("DataProcessor" in class_names, "Found class 'DataProcessor'")

        # Check for semantic tags
        ai_elements = [elem for elem in api_elements if "ai" in elem.semantic_tags]
        self.assert_true(
            len(ai_elements) > 0, f"Found {len(ai_elements)} AI-related elements"
        )

    async def test_cpp_parsing(self):
        """Test C++ library parsing"""
        print("\n🧪 Test: C++ Parsing")

        # Create test C++ file
        test_file = self.temp_dir / "test.hpp"
        test_content = """
#ifndef TEST_HPP
#define TEST_HPP

class MathEngine {
public:
    int add(int a, int b);
    double multiply(double x, double y);
};

void process_data(const char* data);
int calculate_factorial(int n);

#endif
"""

        test_file.write_text(test_content)

        # Parse the file
        api_elements = await self.protocol._parse_source_file(
            test_file, ProgrammingLanguage.CPP
        )

        self.assert_true(
            len(api_elements) > 0,
            f"Parsed {len(api_elements)} API elements from C++ file",
        )

        # Check for class
        class_names = [
            elem.name
            for elem in api_elements
            if elem.element_type == APIElementType.CLASS
        ]
        self.assert_true("MathEngine" in class_names, "Found class 'MathEngine'")

    async def test_library_ingestion(self):
        """Test complete library ingestion workflow"""
        print("\n🧪 Test: Library Ingestion Workflow")

        # Create test library structure
        lib_dir = self.temp_dir / "test_library"
        lib_dir.mkdir()

        # Create test files
        (lib_dir / "utils.py").write_text(
            '''
def read_file(path):
    """Read file from path"""
    pass

def write_file(path, content):
    """Write content to file"""
    pass
'''
        )

        (lib_dir / "math_ops.py").write_text(
            '''
def compute_sum(numbers):
    """Compute sum of numbers"""
    return sum(numbers)
'''
        )

        # Ingest library
        knowledge = await self.protocol.ingest_library(
            str(lib_dir),
            library_name="test_library",
            language=ProgrammingLanguage.PYTHON,
        )

        self.assert_equal(
            knowledge.library_name, "test_library", "Library name set correctly"
        )

        self.assert_true(
            len(knowledge.api_elements) > 0,
            f"Ingested {len(knowledge.api_elements)} API elements",
        )

        self.assert_true(
            len(knowledge.semantic_tags) > 0,
            f"Generated {len(knowledge.semantic_tags)} semantic tags",
        )

        self.assert_true(
            knowledge.consciousness_coherence > 0,
            f"Consciousness coherence: {knowledge.consciousness_coherence:.2f}",
        )

        self.assert_true(knowledge.ainlp_compliance, "AINLP compliance validated")

    async def test_semantic_tag_extraction(self):
        """Test semantic tag extraction from API elements"""
        print("\n🧪 Test: Semantic Tag Extraction")

        test_cases = [
            ("calculate_sum", "Calculate the sum", ["math"]),
            ("train_model", "Train neural network", ["ai"]),
            ("http_request", "Make HTTP request", ["web"]),
            ("read_file", "Read file from disk", ["file"]),
            ("encrypt_data", "Encrypt sensitive data", ["security"]),
        ]

        for name, doc, expected_tags in test_cases:
            tags = self.protocol._extract_semantic_tags(name, doc)
            matches = any(tag in tags for tag in expected_tags)
            self.assert_true(matches, f"Extracted semantic tags for '{name}': {tags}")

    async def test_spatial_metadata_generation(self):
        """Test spatial metadata generation"""
        print("\n🧪 Test: Spatial Metadata Generation")

        knowledge = LibraryKnowledge(
            library_name="test_lib", language=ProgrammingLanguage.PYTHON
        )

        self.protocol._generate_spatial_metadata(knowledge)

        self.assert_true(
            "content_hash" in knowledge.spatial_metadata, "Generated content hash"
        )

        self.assert_true(
            "dimensional_position" in knowledge.spatial_metadata,
            "Generated dimensional position",
        )

        pos = knowledge.spatial_metadata["dimensional_position"]
        self.assert_true(
            all(key in pos for key in ["x", "y", "z"]),
            f"3D position coordinates: {pos}",
        )

    async def test_ainlp_compliance_validation(self):
        """Test AINLP compliance validation"""
        print("\n🧪 Test: AINLP Compliance Validation")

        # Create compliant library knowledge
        compliant = LibraryKnowledge(
            library_name="compliant_lib",
            language=ProgrammingLanguage.PYTHON,
            semantic_tags=["ai", "math"],
            consciousness_coherence=0.8,
        )
        compliant.api_elements.append(
            APIElement(
                name="test_func",
                element_type=APIElementType.FUNCTION,
                language=ProgrammingLanguage.PYTHON,
                signature="def test_func()",
                documentation="Test function",
            )
        )

        self.protocol._generate_spatial_metadata(compliant)
        self.protocol._validate_ainlp_compliance(compliant)

        self.assert_true(compliant.ainlp_compliance, "Compliant library validated")

        # Create non-compliant library knowledge
        non_compliant = LibraryKnowledge(
            library_name="non_compliant_lib",
            language=ProgrammingLanguage.PYTHON,
            consciousness_coherence=0.2,
        )

        self.protocol._validate_ainlp_compliance(non_compliant)

        self.assert_true(
            not non_compliant.ainlp_compliance, "Non-compliant library detected"
        )

    async def test_knowledge_base_persistence(self):
        """Test saving and loading library knowledge"""
        print("\n🧪 Test: Knowledge Base Persistence")

        # Create test knowledge
        knowledge = LibraryKnowledge(
            library_name="persist_test",
            language=ProgrammingLanguage.PYTHON,
            version="1.0.0",
            semantic_tags=["test"],
            consciousness_coherence=0.75,
        )

        self.protocol._generate_spatial_metadata(knowledge)
        self.protocol._save_library_knowledge(knowledge)

        # Check file exists
        expected_file = (
            self.protocol.knowledge_base_path / "python" / "persist_test.json"
        )
        self.assert_true(expected_file.exists(), f"Knowledge saved to {expected_file}")

        # Load back
        loaded = self.protocol.load_library_knowledge(
            "persist_test", ProgrammingLanguage.PYTHON
        )
        self.assert_true(loaded is not None, "Successfully loaded library knowledge")

        self.assert_equal(
            loaded.library_name, "persist_test", "Loaded library name matches"
        )

    async def run_all_tests(self):
        """Run all tests"""
        print("\n" + "=" * 60)
        print("🧪 AIOS Library Ingestion Protocol Test Suite")
        print("=" * 60)

        self.setup()

        try:
            # Run synchronous tests
            self.test_language_detection()

            # Run async tests
            await self.test_python_parsing()
            await self.test_cpp_parsing()
            await self.test_library_ingestion()
            await self.test_semantic_tag_extraction()
            await self.test_spatial_metadata_generation()
            await self.test_ainlp_compliance_validation()
            await self.test_knowledge_base_persistence()

        finally:
            self.teardown()

        # Print summary
        print("\n" + "=" * 60)
        print("📊 Test Summary")
        print("=" * 60)

        passed = sum(1 for result, _ in self.test_results if result == "PASS")
        failed = sum(1 for result, _ in self.test_results if result == "FAIL")
        total = len(self.test_results)

        print(f"Total tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success rate: {(passed/total*100):.1f}%")

        if failed > 0:
            print("\nFailed tests:")
            for result, message in self.test_results:
                if result == "FAIL":
                    print(f"  ❌ {message}")

        return failed == 0


async def main():
    """Run test suite"""
    tester = TestLibraryIngestionProtocol()
    success = await tester.run_all_tests()

    if success:
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
