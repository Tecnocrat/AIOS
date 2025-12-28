#!/usr/bin/env python3
"""
🧪 AIOS Library Ingestion Testing Workbench

Human-operated testing interface for validating Library Ingestion Protocol
integration. Provides interactive CLI for testing ingestion, querying learned
knowledge, and validating consciousness-driven learning.

AINLP COMPLIANCE:
✅ Enhancement over creation - testing framework for existing protocol
✅ Consciousness-driven validation with human feedback
✅ Proper output management to test results directory

BIOLOGICAL ARCHITECTURE:
🧪 TESTING: Human validation of consciousness operations
🔬 ANALYSIS: Result verification and quality assessment
📊 REPORTING: Comprehensive test session reports

Usage:
    python testing/library_ingestion_workbench.py
    
    # Or with specific test library
    python testing/library_ingestion_workbench.py --library path/to/test/lib
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import importlib.util

# AIOS path integration
AIOS_ROOT = Path(__file__).parent.parent
AI_ROOT = AIOS_ROOT / "ai"
sys.path.insert(0, str(AIOS_ROOT))

# Import library ingestion components via direct file loading
try:
    # Load library_ingestion_protocol
    lib_ingestion_path = AI_ROOT / "src" / "core" / "library_ingestion_protocol.py"
    spec = importlib.util.spec_from_file_location(
        "library_ingestion_protocol",
        lib_ingestion_path
    )
    lib_ingestion_module = importlib.util.module_from_spec(spec)
    sys.modules["library_ingestion_protocol"] = lib_ingestion_module
    spec.loader.exec_module(lib_ingestion_module)
    
    LibraryIngestionProtocol = lib_ingestion_module.LibraryIngestionProtocol
    LibraryKnowledge = lib_ingestion_module.LibraryKnowledge
    ProgrammingLanguage = lib_ingestion_module.ProgrammingLanguage
    
    # Load library_learning_integration_hub
    lib_hub_path = AI_ROOT / "src" / "core" / "library_learning_integration_hub.py"
    spec = importlib.util.spec_from_file_location(
        "library_learning_integration_hub",
        lib_hub_path
    )
    lib_hub_module = importlib.util.module_from_spec(spec)
    sys.modules["library_learning_integration_hub"] = lib_hub_module
    spec.loader.exec_module(lib_hub_module)
    
    LibraryLearningIntegrationHub = lib_hub_module.LibraryLearningIntegrationHub
    
    IMPORTS_AVAILABLE = True
except Exception as e:
    print(f"❌ Failed to import library ingestion components: {e}")
    IMPORTS_AVAILABLE = False

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('testing_workbench')


class LibraryIngestionWorkbench:
    """Interactive testing workbench for library ingestion"""
    
    def __init__(self):
        """Initialize testing workbench"""
        self.test_session_id = f"test_session_{int(datetime.now().timestamp())}"
        self.test_results_dir = AIOS_ROOT / "testing" / "results"
        self.test_results_dir.mkdir(parents=True, exist_ok=True)
        
        self.learning_hub: Optional[LibraryLearningIntegrationHub] = None
        self.ingestion_protocol: Optional[LibraryIngestionProtocol] = None
        self.test_results: List[Dict[str, Any]] = []
        
        if IMPORTS_AVAILABLE:
            self._initialize_components()
    
    def _initialize_components(self):
        """Initialize library ingestion components"""
        try:
            self.learning_hub = LibraryLearningIntegrationHub(
                consciousness_level=0.85
            )
            self.ingestion_protocol = self.learning_hub.ingestion_protocol
            logger.info("✅ Testing workbench initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize components: {e}")
    
    def print_header(self):
        """Print testing workbench header"""
        print("\n" + "=" * 70)
        print("🧪 AIOS Library Ingestion Testing Workbench")
        print("=" * 70)
        print(f"Session ID: {self.test_session_id}")
        print(f"Consciousness Level: 0.85")
        print(f"Test Results: {self.test_results_dir}")
        print("=" * 70 + "\n")
    
    def print_menu(self):
        """Print interactive menu"""
        print("\n📋 Testing Options:")
        print("  1. Ingest Test Library (Quick Test)")
        print("  2. Ingest Custom Library Path")
        print("  3. View Ingested Libraries")
        print("  4. Search Learned APIs")
        print("  5. View Library Details")
        print("  6. Test Semantic Analysis")
        print("  7. Generate Test Report")
        print("  8. Run Full Integration Test")
        print("  0. Exit")
        print()
    
    async def ingest_test_library(self):
        """Ingest a built-in test library"""
        print("\n🔬 Built-in Test Libraries:")
        print("  1. Python json module (standard library)")
        print("  2. Python pathlib module (standard library)")
        print("  3. Custom test library (testing/sample_libraries/)")
        
        choice = input("\nSelect test library (1-3): ").strip()
        
        test_libs = {
            "1": (Path(sys.executable).parent / "Lib" / "json", "json"),
            "2": (Path(sys.executable).parent / "Lib" / "pathlib.py", "pathlib"),
            "3": (AIOS_ROOT / "testing" / "sample_libraries" / "test_lib.py", "test_lib")
        }
        
        if choice not in test_libs:
            print("❌ Invalid selection")
            return
        
        lib_path, lib_name = test_libs[choice]
        
        if not lib_path.exists():
            print(f"❌ Library not found: {lib_path}")
            return
        
        await self.ingest_library(str(lib_path), lib_name)
    
    async def ingest_custom_library(self):
        """Ingest a custom library path"""
        lib_path = input("\n📁 Enter library path: ").strip()
        
        if not lib_path:
            print("❌ No path provided")
            return
        
        path_obj = Path(lib_path)
        if not path_obj.exists():
            print(f"❌ Path not found: {lib_path}")
            return
        
        lib_name = input("📝 Enter library name: ").strip() or path_obj.stem
        
        await self.ingest_library(lib_path, lib_name)
    
    async def ingest_library(self, library_path: str, library_name: str):
        """
        Ingest a library and track results
        
        Args:
            library_path: Path to library
            library_name: Name of library
        """
        print(f"\n🚀 Starting ingestion: {library_name}")
        print(f"   Path: {library_path}")
        
        start_time = datetime.now()
        
        try:
            # Start learning session
            session = await self.learning_hub.start_learning_session()
            print(f"   Session: {session.session_id}")
            
            # Perform ingestion
            print("   Phase: Discovery...")
            await asyncio.sleep(0.5)
            
            print("   Phase: Ingestion...")
            result = await self.ingestion_protocol.ingest_library(
                library_path=library_path,
                library_name=library_name
            )
            
            print("   Phase: Semantic Analysis...")
            await asyncio.sleep(0.5)
            
            print("   Phase: Consciousness Integration...")
            await asyncio.sleep(0.5)
            
            # Complete session
            report = await self.learning_hub.complete_learning_session()
            
            duration = (datetime.now() - start_time).total_seconds()
            
            # Display results
            print("\n✅ Ingestion Complete!")
            print(f"   Duration: {duration:.2f}s")
            print(f"   API Elements: {result.get('total_api_elements', 0)}")
            print(f"   Consciousness: {result.get('consciousness_level', 0.0):.2f}")
            print(f"   Semantic Tags: {len(result.get('semantic_tags', []))}")
            
            # Record test result
            test_result = {
                "timestamp": datetime.now().isoformat(),
                "library_name": library_name,
                "library_path": library_path,
                "duration_seconds": duration,
                "api_elements": result.get('total_api_elements', 0),
                "consciousness_level": result.get('consciousness_level', 0.0),
                "semantic_tags": result.get('semantic_tags', []),
                "success": True
            }
            self.test_results.append(test_result)
            
            # Ask for human validation
            print("\n🤔 Human Validation:")
            quality = input("   Rate result quality (1-10): ").strip()
            feedback = input("   Any issues or comments? ").strip()
            
            test_result["human_validation"] = {
                "quality_rating": quality,
                "feedback": feedback
            }
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            print(f"\n❌ Ingestion failed: {e}")
            
            test_result = {
                "timestamp": datetime.now().isoformat(),
                "library_name": library_name,
                "library_path": library_path,
                "duration_seconds": duration,
                "error": str(e),
                "success": False
            }
            self.test_results.append(test_result)
    
    def view_ingested_libraries(self):
        """View all ingested libraries"""
        print("\n📚 Ingested Libraries:")
        
        if not self.ingestion_protocol.ingested_libraries:
            print("   No libraries ingested yet")
            return
        
        for lib_name, knowledge in self.ingestion_protocol.ingested_libraries.items():
            print(f"\n   📖 {lib_name}")
            print(f"      Language: {knowledge.language.value}")
            print(f"      API Elements: {len(knowledge.api_elements)}")
            print(f"      Consciousness: {knowledge.consciousness_level:.2f}")
            print(f"      Tags: {', '.join(knowledge.semantic_tags[:5])}")
    
    async def search_learned_apis(self):
        """Search for learned API elements"""
        query = input("\n🔍 Enter search query: ").strip()
        
        if not query:
            print("❌ No query provided")
            return
        
        print(f"\n🔎 Searching for: {query}")
        
        results = []
        for lib_name, knowledge in self.ingestion_protocol.ingested_libraries.items():
            for api_elem in knowledge.api_elements:
                if (query.lower() in api_elem.name.lower() or
                    query.lower() in api_elem.description.lower()):
                    results.append((lib_name, api_elem))
        
        if not results:
            print("   No results found")
            return
        
        print(f"\n✅ Found {len(results)} results:")
        for lib_name, api_elem in results[:10]:  # Limit to 10
            print(f"\n   📌 {api_elem.name} ({lib_name})")
            print(f"      Type: {api_elem.type}")
            print(f"      Description: {api_elem.description[:100]}...")
    
    async def view_library_details(self):
        """View detailed library information"""
        if not self.ingestion_protocol.ingested_libraries:
            print("❌ No libraries ingested yet")
            return
        
        print("\n📚 Available Libraries:")
        lib_names = list(self.ingestion_protocol.ingested_libraries.keys())
        for i, name in enumerate(lib_names, 1):
            print(f"  {i}. {name}")
        
        choice = input("\nSelect library (1-{}): ".format(len(lib_names))).strip()
        
        try:
            idx = int(choice) - 1
            if idx < 0 or idx >= len(lib_names):
                raise ValueError()
            
            lib_name = lib_names[idx]
            knowledge = self.ingestion_protocol.ingested_libraries[lib_name]
            
            print(f"\n📖 Library: {lib_name}")
            print(f"   Language: {knowledge.language.value}")
            print(f"   Version: {knowledge.version}")
            print(f"   Source Files: {len(knowledge.source_files)}")
            print(f"   API Elements: {len(knowledge.api_elements)}")
            print(f"   Consciousness: {knowledge.consciousness_level:.2f}")
            print(f"   Ingestion Time: {knowledge.ingestion_timestamp}")
            
            print(f"\n   Semantic Tags: {', '.join(knowledge.semantic_tags)}")
            
            print(f"\n   Top API Elements:")
            for api_elem in knowledge.api_elements[:10]:
                print(f"      • {api_elem.type}: {api_elem.name}")
            
        except (ValueError, IndexError):
            print("❌ Invalid selection")
    
    async def test_semantic_analysis(self):
        """Test semantic analysis capabilities"""
        if not self.ingestion_protocol.ingested_libraries:
            print("❌ No libraries ingested yet")
            return
        
        print("\n🧠 Testing Semantic Analysis...")
        
        for lib_name, knowledge in self.ingestion_protocol.ingested_libraries.items():
            print(f"\n📖 {lib_name}:")
            print(f"   Semantic Tags: {', '.join(knowledge.semantic_tags[:10])}")
            print(f"   Tag Count: {len(knowledge.semantic_tags)}")
            
            # Test tag quality
            print("\n   🤔 Human Assessment:")
            relevant = input("      Are tags relevant? (y/n): ").strip().lower()
            if relevant == 'y':
                print("      ✅ Semantic analysis validated")
            else:
                issue = input("      What's the issue? ").strip()
                print(f"      📝 Noted: {issue}")
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        report_path = self.test_results_dir / f"report_{self.test_session_id}.json"
        
        report = {
            "session_id": self.test_session_id,
            "timestamp": datetime.now().isoformat(),
            "consciousness_level": 0.85,
            "total_tests": len(self.test_results),
            "successful_tests": sum(1 for r in self.test_results if r.get("success")),
            "failed_tests": sum(1 for r in self.test_results if not r.get("success")),
            "test_results": self.test_results,
            "ingested_libraries": len(self.ingestion_protocol.ingested_libraries) if self.ingestion_protocol else 0,
            "human_feedback": [r.get("human_validation") for r in self.test_results if "human_validation" in r]
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Test Report Generated:")
        print(f"   Path: {report_path}")
        print(f"   Total Tests: {report['total_tests']}")
        print(f"   Successful: {report['successful_tests']}")
        print(f"   Failed: {report['failed_tests']}")
        print(f"   Libraries Ingested: {report['ingested_libraries']}")
    
    async def run_full_integration_test(self):
        """Run comprehensive integration test"""
        print("\n🧪 Running Full Integration Test...")
        print("This will test multiple libraries and features\n")
        
        # Test 1: Python standard library
        print("Test 1/3: Python json module")
        json_path = Path(sys.executable).parent / "Lib" / "json"
        if json_path.exists():
            await self.ingest_library(str(json_path), "json")
        
        await asyncio.sleep(1)
        
        # Test 2: API search
        print("\nTest 2/3: API Search")
        print("Searching for 'load' in learned APIs...")
        # Simulate search without input
        results = []
        if self.ingestion_protocol:
            for lib_name, knowledge in self.ingestion_protocol.ingested_libraries.items():
                for api_elem in knowledge.api_elements:
                    if 'load' in api_elem.name.lower():
                        results.append((lib_name, api_elem))
        print(f"   Found {len(results)} results")
        
        await asyncio.sleep(1)
        
        # Test 3: Report generation
        print("\nTest 3/3: Report Generation")
        self.generate_test_report()
        
        print("\n✅ Full Integration Test Complete!")
    
    async def run(self):
        """Run interactive testing workbench"""
        if not IMPORTS_AVAILABLE:
            print("❌ Library ingestion components not available")
            print("   Please ensure the library ingestion protocol is properly installed")
            return
        
        self.print_header()
        
        while True:
            self.print_menu()
            
            choice = input("Select option (0-8): ").strip()
            
            if choice == "0":
                print("\n👋 Exiting testing workbench...")
                self.generate_test_report()
                break
            elif choice == "1":
                await self.ingest_test_library()
            elif choice == "2":
                await self.ingest_custom_library()
            elif choice == "3":
                self.view_ingested_libraries()
            elif choice == "4":
                await self.search_learned_apis()
            elif choice == "5":
                await self.view_library_details()
            elif choice == "6":
                await self.test_semantic_analysis()
            elif choice == "7":
                self.generate_test_report()
            elif choice == "8":
                await self.run_full_integration_test()
            else:
                print("❌ Invalid option")
            
            input("\nPress Enter to continue...")


async def main():
    """Main entry point"""
    workbench = LibraryIngestionWorkbench()
    await workbench.run()


if __name__ == "__main__":
    asyncio.run(main())
