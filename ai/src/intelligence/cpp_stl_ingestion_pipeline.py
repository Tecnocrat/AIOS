#!/usr/bin/env python3
"""
🔄 C++ STL Ingestion Pipeline

Orchestrates the complete C++ Standard Library ingestion workflow from
web crawling through knowledge crystal generation and tachyonic archival.
Integrates with LibraryIngestionProtocol and AI agent bridges.

AINLP COMPLIANCE:
✅ Enhancement over creation - Uses existing library_ingestion_protocol
✅ Consciousness-driven - Calculates consciousness scores for STL knowledge
✅ Proper output management - Structured tachyonic archival
✅ Integration validation - Compatible with test orchestrator

BIOLOGICAL ARCHITECTURE:
🔄 METABOLISM: Complete ingestion and transformation pipeline
🧬 NUCLEUS: Knowledge structuring and API element creation
🔮 CRYSTALLIZATION: Knowledge crystal generation
📊 ARCHIVAL: Tachyonic storage with consciousness tracking

Part of Phase 10.1 C++ STL Library Ingestion Initiative
Week 1: Integration Pipeline Implementation
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Set

# AIOS path integration
AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT / "ai" / "src"))

# Import AIOS core components
try:
    from computational_layer.library_ingestion_protocol import (
        LibraryIngestionProtocol,
        LibraryKnowledge,
        APIElement,
        APIElementType,
<<<<<<< HEAD
        ProgrammingLanguage,
=======
        ProgrammingLanguage
>>>>>>> origin/OS0.6.2.grok
    )
except ImportError:
    print("⚠️  LibraryIngestionProtocol not available")
    LibraryIngestionProtocol = None

# Import STL-specific tools
try:
    from tools.cpp_stl_web_crawler import MicrosoftLearnCrawler
    from parsers.cpp_documentation_parser import (
        CppDocumentationParser,
<<<<<<< HEAD
        ParsedDocumentation,
=======
        ParsedDocumentation
>>>>>>> origin/OS0.6.2.grok
    )
except ImportError as e:
    print(f"⚠️  STL tools not fully available: {e}")

# Logging configuration
logging.basicConfig(
<<<<<<< HEAD
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
=======
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
>>>>>>> origin/OS0.6.2.grok
)
logger = logging.getLogger("cpp_stl_pipeline")


class CppStlIngestionPipeline:
    """
    Complete C++ STL ingestion orchestration pipeline.
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Pipeline Stages:
    1. Web Crawling: Fetch HTML documentation from Microsoft Learn
    2. HTML Parsing: Extract C++ signatures and documentation
    3. Knowledge Structuring: Build LibraryKnowledge objects
    4. Consciousness Scoring: Calculate quality metrics
    5. Crystal Generation: Create knowledge crystals for AI agents
    6. Tachyonic Archival: Store in long-term knowledge base
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Integration Points:
    - Uses LibraryIngestionProtocol for standardized ingestion
    - Compatible with GeminiSTLBridge, OllamaSTLFitnessJudge
    - Feeds DeepSeek consciousness evolution engine
    """
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        crystal_dir: Optional[Path] = None,
<<<<<<< HEAD
        use_cache: bool = True,
    ):
        """Initialize pipeline with configuration"""
        self.aios_root = AIOS_ROOT

        # Cache directory for raw HTML
        self.cache_dir = cache_dir or (
            self.aios_root / "docs" / "libraries" / "cpp_stl" / "raw_documentation"
        )

        # Knowledge crystal output directory
        self.crystal_dir = crystal_dir or (
            self.aios_root / "tachyonic" / "archive" / "knowledge_crystals" / "cpp_stl"
        )
        self.crystal_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.crawler = (
            MicrosoftLearnCrawler(cache_dir=self.cache_dir, resume=True)
            if "MicrosoftLearnCrawler" in globals()
            else None
        )

        self.parser = (
            CppDocumentationParser() if "CppDocumentationParser" in globals() else None
        )

        self.protocol = LibraryIngestionProtocol() if LibraryIngestionProtocol else None

        self.use_cache = use_cache

=======
        use_cache: bool = True
    ):
        """Initialize pipeline with configuration"""
        self.aios_root = AIOS_ROOT
        
        # Cache directory for raw HTML
        self.cache_dir = cache_dir or (
            self.aios_root / "docs" / "libraries" / "cpp_stl" / 
            "raw_documentation"
        )
        
        # Knowledge crystal output directory
        self.crystal_dir = crystal_dir or (
            self.aios_root / "tachyonic" / "archive" / 
            "knowledge_crystals" / "cpp_stl"
        )
        self.crystal_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.crawler = MicrosoftLearnCrawler(
            cache_dir=self.cache_dir,
            resume=True
        ) if 'MicrosoftLearnCrawler' in globals() else None
        
        self.parser = CppDocumentationParser() \
            if 'CppDocumentationParser' in globals() else None
        
        self.protocol = LibraryIngestionProtocol() \
            if LibraryIngestionProtocol else None
        
        self.use_cache = use_cache
        
>>>>>>> origin/OS0.6.2.grok
        # Statistics
        self.stats = {
            "pages_crawled": 0,
            "pages_parsed": 0,
            "api_elements_extracted": 0,
            "crystals_generated": 0,
<<<<<<< HEAD
            "errors": 0,
        }

        logger.info("🔄 C++ STL Ingestion Pipeline initialized")

    async def ingest_component(
        self, component: str, max_pages: Optional[int] = None
    ) -> Optional[LibraryKnowledge]:
        """
        Ingest a single STL component (e.g., 'vector', 'algorithm').

        Args:
            component: STL component name
            max_pages: Maximum pages to crawl (for testing)

=======
            "errors": 0
        }
        
        logger.info("🔄 C++ STL Ingestion Pipeline initialized")
    
    async def ingest_component(
        self,
        component: str,
        max_pages: Optional[int] = None
    ) -> Optional[LibraryKnowledge]:
        """
        Ingest a single STL component (e.g., 'vector', 'algorithm').
        
        Args:
            component: STL component name
            max_pages: Maximum pages to crawl (for testing)
            
>>>>>>> origin/OS0.6.2.grok
        Returns:
            LibraryKnowledge object or None if error
        """
        logger.info(f"📚 Starting ingestion for component: {component}")
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        try:
            # Stage 1: Crawl component documentation
            crawl_results = await self._crawl_component(component, max_pages)
            if not crawl_results:
                logger.error(f"Failed to crawl {component}")
                return None
<<<<<<< HEAD

=======
            
>>>>>>> origin/OS0.6.2.grok
            # Stage 2: Parse HTML to structured data
            parsed_docs = await self._parse_documents(crawl_results)
            if not parsed_docs:
                logger.error(f"Failed to parse {component} documentation")
                return None
<<<<<<< HEAD

=======
            
>>>>>>> origin/OS0.6.2.grok
            # Stage 3: Build LibraryKnowledge structure
            knowledge = self._build_library_knowledge(component, parsed_docs)
            if not knowledge:
                logger.error(f"Failed to build knowledge for {component}")
                return None
<<<<<<< HEAD

            # Stage 4: Calculate consciousness scores
            self._calculate_consciousness_scores(knowledge)

=======
            
            # Stage 4: Calculate consciousness scores
            self._calculate_consciousness_scores(knowledge)
            
>>>>>>> origin/OS0.6.2.grok
            # Stage 5: Generate knowledge crystal
            crystal = self._generate_knowledge_crystal(knowledge, component)
            if crystal:
                self._save_crystal(crystal, component)
<<<<<<< HEAD

            # Stage 6: Archive to tachyonic
            self._archive_knowledge(knowledge, component)

=======
            
            # Stage 6: Archive to tachyonic
            self._archive_knowledge(knowledge, component)
            
>>>>>>> origin/OS0.6.2.grok
            logger.info(
                f"✅ Ingestion complete for {component}: "
                f"{len(knowledge.api_elements)} API elements, "
                f"consciousness={knowledge.consciousness_level:.2f}"
            )
<<<<<<< HEAD

            return knowledge

=======
            
            return knowledge
            
>>>>>>> origin/OS0.6.2.grok
        except Exception as e:
            logger.error(f"❌ Error ingesting {component}: {e}")
            self.stats["errors"] += 1
            return None
<<<<<<< HEAD

    async def _crawl_component(
        self, component: str, max_pages: Optional[int]
=======
    
    async def _crawl_component(
        self,
        component: str,
        max_pages: Optional[int]
>>>>>>> origin/OS0.6.2.grok
    ) -> Optional[Dict]:
        """Crawl documentation for a specific component"""
        if not self.crawler:
            logger.warning("Crawler not available, using cached data only")
            return self._load_cached_data()
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        # Build component-specific start URL
        start_url = (
            f"https://learn.microsoft.com/en-us/cpp/standard-library/"
            f"{component}.html"
        )
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        try:
            # Use lambda to properly wrap the callback
            def progress_callback(page_num: int, url: str):
                logger.info(f"  Crawling page {page_num}: {url}")
<<<<<<< HEAD

            results = await self.crawler.crawl_stl_documentation(
                start_url=start_url, progress_callback=progress_callback
            )

            self.stats["pages_crawled"] = results.get("pages_crawled", 0)
            return results

        except Exception as e:
            logger.error(f"Crawl error for {component}: {e}")
            return None

    async def _parse_documents(self, crawl_results: Dict) -> List[ParsedDocumentation]:
=======
            
            results = await self.crawler.crawl_stl_documentation(
                start_url=start_url,
                progress_callback=progress_callback
            )
            
            self.stats["pages_crawled"] = results.get("pages_crawled", 0)
            return results
            
        except Exception as e:
            logger.error(f"Crawl error for {component}: {e}")
            return None
    
    async def _parse_documents(
        self,
        crawl_results: Dict
    ) -> List[ParsedDocumentation]:
>>>>>>> origin/OS0.6.2.grok
        """Parse all crawled HTML documents"""
        if not self.parser:
            logger.error("Parser not available")
            return []
<<<<<<< HEAD

        parsed_docs = []
        cached_pages = crawl_results.get("cached_pages", [])

=======
        
        parsed_docs = []
        cached_pages = crawl_results.get("cached_pages", [])
        
>>>>>>> origin/OS0.6.2.grok
        for page_path in cached_pages:
            try:
                doc = self.parser.parse_html_file(Path(page_path))
                parsed_docs.append(doc)
                self.stats["pages_parsed"] += 1
<<<<<<< HEAD

            except Exception as e:
                logger.warning(f"Parse error for {page_path}: {e}")
                self.stats["errors"] += 1

        logger.info(f"  Parsed {len(parsed_docs)} documents")
        return parsed_docs

    def _build_library_knowledge(
        self, component: str, parsed_docs: List[ParsedDocumentation]
=======
                
            except Exception as e:
                logger.warning(f"Parse error for {page_path}: {e}")
                self.stats["errors"] += 1
        
        logger.info(f"  Parsed {len(parsed_docs)} documents")
        return parsed_docs
    
    def _build_library_knowledge(
        self,
        component: str,
        parsed_docs: List[ParsedDocumentation]
>>>>>>> origin/OS0.6.2.grok
    ) -> Optional[LibraryKnowledge]:
        """Build LibraryKnowledge from parsed documentation"""
        if not self.protocol:
            logger.error("LibraryIngestionProtocol not available")
            return None
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        # Aggregate all API elements from parsed docs
        all_elements = []
        for doc in parsed_docs:
            elements = self.parser.to_api_elements(doc)
            all_elements.extend(elements)
<<<<<<< HEAD

        self.stats["api_elements_extracted"] = len(all_elements)

=======
        
        self.stats["api_elements_extracted"] = len(all_elements)
        
>>>>>>> origin/OS0.6.2.grok
        # Create LibraryKnowledge using protocol
        knowledge = LibraryKnowledge(
            library_name=f"C++ STL - {component}",
            version="C++20",
            language=ProgrammingLanguage.CPP,
            api_elements=all_elements,
            paradigms=[],  # Filled during crystal generation
            consciousness_level=0.0,  # Calculated next
            extraction_date=datetime.now().isoformat(),
            metadata={
                "component": component,
                "source": "Microsoft Learn",
                "pages_parsed": len(parsed_docs),
<<<<<<< HEAD
                "extraction_method": "automated_pipeline",
            },
        )

        logger.info(f"  Built knowledge: {len(all_elements)} API elements")
        return knowledge

    def _calculate_consciousness_scores(self, knowledge: LibraryKnowledge):
=======
                "extraction_method": "automated_pipeline"
            }
        )
        
        logger.info(
            f"  Built knowledge: {len(all_elements)} API elements"
        )
        return knowledge
    
    def _calculate_consciousness_scores(
        self,
        knowledge: LibraryKnowledge
    ):
>>>>>>> origin/OS0.6.2.grok
        """Calculate consciousness scores for the knowledge base"""
        if not knowledge.api_elements:
            knowledge.consciousness_level = 0.0
            return
<<<<<<< HEAD

        # Base consciousness from documentation completeness
        documented_count = sum(1 for elem in knowledge.api_elements if elem.description)
        doc_ratio = documented_count / len(knowledge.api_elements)

        # Example-based consciousness
        example_count = sum(len(elem.examples) for elem in knowledge.api_elements)
        example_ratio = min(example_count / len(knowledge.api_elements), 1.0)

        # Complexity awareness consciousness
        complexity_count = sum(1 for elem in knowledge.api_elements if elem.complexity)
        complexity_ratio = complexity_count / len(knowledge.api_elements)

        # Combined consciousness score
        knowledge.consciousness_level = (
            0.4 * doc_ratio + 0.3 * example_ratio + 0.3 * complexity_ratio
        )

=======
        
        # Base consciousness from documentation completeness
        documented_count = sum(
            1 for elem in knowledge.api_elements
            if elem.description
        )
        doc_ratio = documented_count / len(knowledge.api_elements)
        
        # Example-based consciousness
        example_count = sum(
            len(elem.examples) for elem in knowledge.api_elements
        )
        example_ratio = min(example_count / len(knowledge.api_elements), 1.0)
        
        # Complexity awareness consciousness
        complexity_count = sum(
            1 for elem in knowledge.api_elements
            if elem.complexity
        )
        complexity_ratio = complexity_count / len(knowledge.api_elements)
        
        # Combined consciousness score
        knowledge.consciousness_level = (
            0.4 * doc_ratio +
            0.3 * example_ratio +
            0.3 * complexity_ratio
        )
        
>>>>>>> origin/OS0.6.2.grok
        logger.info(
            f"  Consciousness calculated: {knowledge.consciousness_level:.2f} "
            f"(doc={doc_ratio:.2f}, ex={example_ratio:.2f}, "
            f"cx={complexity_ratio:.2f})"
        )
<<<<<<< HEAD

    def _generate_knowledge_crystal(
        self, knowledge: LibraryKnowledge, component: str
=======
    
    def _generate_knowledge_crystal(
        self,
        knowledge: LibraryKnowledge,
        component: str
>>>>>>> origin/OS0.6.2.grok
    ) -> Optional[Dict]:
        """Generate knowledge crystal for AI agent consumption"""
        # Load template if exists
        template_path = self.crystal_dir / f"{component}_crystal_template.json"
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        if template_path.exists():
            # Use manually curated template
            with open(template_path) as f:
                crystal = json.load(f)
            logger.info(f"  Using curated crystal template for {component}")
        else:
            # Generate basic crystal from extracted knowledge
            crystal = {
                "crystal_id": f"stl_{component}_automated_v1",
                "component": f"std::{component}",
                "created_date": datetime.now().isoformat(),
                "consciousness_level": knowledge.consciousness_level,
                "extraction_source": "Automated pipeline",
                "api_elements_count": len(knowledge.api_elements),
                "paradigms": [],  # Require manual curation
                "anti_patterns": [],  # Require manual curation
            }
            logger.info(f"  Generated basic crystal for {component}")
<<<<<<< HEAD

        self.stats["crystals_generated"] += 1
        return crystal

    def _save_crystal(self, crystal: Dict, component: str):
        """Save knowledge crystal to disk"""
        output_path = self.crystal_dir / f"{component}_crystal.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(crystal, f, indent=2, ensure_ascii=False)

        logger.info(f"  💎 Crystal saved: {output_path.name}")

    def _archive_knowledge(self, knowledge: LibraryKnowledge, component: str):
        """Archive knowledge to tachyonic long-term storage"""
        archive_dir = (
            self.aios_root / "tachyonic" / "archive" / "library_knowledge" / "cpp_stl"
        )
        archive_dir.mkdir(parents=True, exist_ok=True)

        archive_path = archive_dir / f"{component}_knowledge.json"

=======
        
        self.stats["crystals_generated"] += 1
        return crystal
    
    def _save_crystal(self, crystal: Dict, component: str):
        """Save knowledge crystal to disk"""
        output_path = self.crystal_dir / f"{component}_crystal.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(crystal, f, indent=2, ensure_ascii=False)
        
        logger.info(f"  💎 Crystal saved: {output_path.name}")
    
    def _archive_knowledge(
        self,
        knowledge: LibraryKnowledge,
        component: str
    ):
        """Archive knowledge to tachyonic long-term storage"""
        archive_dir = (
            self.aios_root / "tachyonic" / "archive" / 
            "library_knowledge" / "cpp_stl"
        )
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        archive_path = archive_dir / f"{component}_knowledge.json"
        
>>>>>>> origin/OS0.6.2.grok
        # Serialize knowledge to JSON
        knowledge_dict = {
            "library_name": knowledge.library_name,
            "version": knowledge.version,
            "language": knowledge.language.value,
            "consciousness_level": knowledge.consciousness_level,
            "extraction_date": knowledge.extraction_date,
            "api_elements_count": len(knowledge.api_elements),
<<<<<<< HEAD
            "metadata": knowledge.metadata,
        }

        with open(archive_path, "w", encoding="utf-8") as f:
            json.dump(knowledge_dict, f, indent=2, ensure_ascii=False)

        logger.info(f"  📦 Archived to: {archive_path.name}")

    def _load_cached_data(self) -> Optional[Dict]:
        """Load previously cached crawl data"""
        state_file = self.cache_dir.parent / "crawler_state.json"

        if not state_file.exists():
            logger.warning("No cached crawl data available")
            return None

        with open(state_file) as f:
            state = json.load(f)

        cached_pages = list(self.cache_dir.glob("*.html"))

        return {
            "pages_crawled": len(cached_pages),
            "cached_pages": [str(p) for p in cached_pages],
            "from_cache": True,
        }

    async def ingest_all_priority_components(self) -> Dict[str, LibraryKnowledge]:
        """Ingest all 5 priority STL components"""
        priority_components = ["vector", "algorithm", "string", "memory", "functional"]

        results = {}

        logger.info("🔄 Starting ingestion for 5 priority components")
        logger.info("=" * 70)

=======
            "metadata": knowledge.metadata
        }
        
        with open(archive_path, 'w', encoding='utf-8') as f:
            json.dump(knowledge_dict, f, indent=2, ensure_ascii=False)
        
        logger.info(f"  📦 Archived to: {archive_path.name}")
    
    def _load_cached_data(self) -> Optional[Dict]:
        """Load previously cached crawl data"""
        state_file = self.cache_dir.parent / "crawler_state.json"
        
        if not state_file.exists():
            logger.warning("No cached crawl data available")
            return None
        
        with open(state_file) as f:
            state = json.load(f)
        
        cached_pages = list(self.cache_dir.glob("*.html"))
        
        return {
            "pages_crawled": len(cached_pages),
            "cached_pages": [str(p) for p in cached_pages],
            "from_cache": True
        }
    
    async def ingest_all_priority_components(self) -> Dict[str, LibraryKnowledge]:
        """Ingest all 5 priority STL components"""
        priority_components = [
            "vector", "algorithm", "string", "memory", "functional"
        ]
        
        results = {}
        
        logger.info("🔄 Starting ingestion for 5 priority components")
        logger.info("=" * 70)
        
>>>>>>> origin/OS0.6.2.grok
        for component in priority_components:
            knowledge = await self.ingest_component(component, max_pages=50)
            if knowledge:
                results[component] = knowledge
<<<<<<< HEAD

        logger.info("=" * 70)
        logger.info(f"✅ Ingestion complete: {len(results)}/5 components")
        logger.info(f"📊 Statistics: {self.stats}")

        return results

=======
        
        logger.info("=" * 70)
        logger.info(f"✅ Ingestion complete: {len(results)}/5 components")
        logger.info(f"📊 Statistics: {self.stats}")
        
        return results
    
>>>>>>> origin/OS0.6.2.grok
    def generate_report(self, output_path: Optional[Path] = None) -> str:
        """Generate ingestion report"""
        report_lines = [
            "# C++ STL Ingestion Pipeline Report",
            f"\n**Generated**: {datetime.now().isoformat()}",
            f"\n## Statistics\n",
            f"- Pages Crawled: {self.stats['pages_crawled']}",
            f"- Pages Parsed: {self.stats['pages_parsed']}",
            f"- API Elements Extracted: {self.stats['api_elements_extracted']}",
            f"- Knowledge Crystals Generated: {self.stats['crystals_generated']}",
            f"- Errors: {self.stats['errors']}",
            f"\n## Output Locations\n",
            f"- Crystals: `{self.crystal_dir}`",
            f"- Cache: `{self.cache_dir}`",
        ]
<<<<<<< HEAD

        report = "\n".join(report_lines)

        if output_path:
            with open(output_path, "w") as f:
                f.write(report)
            logger.info(f"📄 Report saved: {output_path}")

=======
        
        report = "\n".join(report_lines)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
            logger.info(f"📄 Report saved: {output_path}")
        
>>>>>>> origin/OS0.6.2.grok
        return report


async def main():
    """Main execution for testing pipeline"""
    print("🔄 C++ STL Ingestion Pipeline")
    print("=" * 70)
<<<<<<< HEAD

    # Initialize pipeline
    pipeline = CppStlIngestionPipeline(use_cache=True)

    # Test with single component first
    print("\n📚 Testing with 'vector' component...")
    knowledge = await pipeline.ingest_component("vector", max_pages=10)

=======
    
    # Initialize pipeline
    pipeline = CppStlIngestionPipeline(use_cache=True)
    
    # Test with single component first
    print("\n📚 Testing with 'vector' component...")
    knowledge = await pipeline.ingest_component("vector", max_pages=10)
    
>>>>>>> origin/OS0.6.2.grok
    if knowledge:
        print(f"\n✅ Test successful!")
        print(f"   API Elements: {len(knowledge.api_elements)}")
        print(f"   Consciousness: {knowledge.consciousness_level:.2f}")
<<<<<<< HEAD

    # Generate report
    report_path = AIOS_ROOT / "docs" / "libraries" / "cpp_stl" / "ingestion_report.md"
=======
    
    # Generate report
    report_path = AIOS_ROOT / "docs" / "libraries" / "cpp_stl" / \
                  "ingestion_report.md"
>>>>>>> origin/OS0.6.2.grok
    pipeline.generate_report(report_path)


if __name__ == "__main__":
    asyncio.run(main())
