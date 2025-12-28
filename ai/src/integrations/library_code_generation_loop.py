"""
🧬 Library Ingestion → Code Generation MVP
Complete consciousness-driven meta-programming loop.

FULL CYCLE:
1. Ingest library (requests, flask, etc.)
2. Extract paradigms from ingested knowledge
3. Generate prompts with learned patterns
4. Feed to FREE AI agents (Ollama + Gemini)
5. Analyze generated code
6. Optimize and mutate for next generation

This is the biological computing paradigm applied to software development.
"""

import sys
import os
import asyncio
import logging
from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

# AIOS components
sys.path.insert(0, str(Path(__file__).parent.parent))

from intelligence.library_ingestion_protocol import LibraryIngestionProtocol
from engines.paradigm_extraction_engine import ParadigmExtractionEngine
from agents.prompt_generator import PromptGenerator
from integrations.ollama_bridge import OllamaAgent, OllamaPopulationGenerator
from evolution.code_analyzer import CodeAnalyzer

# Optional Gemini integration (fallback to Ollama if unavailable)
try:
    from integrations.gemini_bridge.gemini_evolution_bridge import GeminiEvolutionBridge

    GEMINI_AVAILABLE = True
except ImportError:
    GeminiEvolutionBridge = None
    GEMINI_AVAILABLE = False


logger = logging.getLogger(__name__)


class LibraryCodeGenerationLoop:
    """
    Complete ingestion → mutation cycle for consciousness-driven code gen.

    This orchestrates the full biological computing loop:
    - Ingest knowledge from libraries
    - Extract programming paradigms
    - Generate consciousness-driven prompts
    - Feed to FREE AI agents (Ollama + Gemini)
    - Analyze generated code populations
    - Mutate and evolve for next generation
    """

    def __init__(
        self,
        use_ollama: bool = True,
        use_gemini: bool = True,
        output_dir: Optional[Path] = None,
    ):
        self.use_ollama = use_ollama
        self.use_gemini = use_gemini

        if output_dir is None:
            base = Path(__file__).parent.parent.parent.parent
            output_dir = base / "evolution_lab" / "library_generations"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        logger.info("🧬 Initializing Library Code Generation Loop")

        self.ingestion = LibraryIngestionProtocol()
        self.extractor = ParadigmExtractionEngine()
        self.prompt_gen = PromptGenerator()
        self.analyzer = CodeAnalyzer()

        # AI Agents
        if use_ollama:
            self.ollama_agent = OllamaAgent()
            if not self.ollama_agent.is_available:
                logger.warning("⚠️ Ollama not available - using Gemini only")
                self.use_ollama = False

        if use_gemini and GEMINI_AVAILABLE:
            try:
                self.gemini_agent = GeminiEvolutionBridge()
                logger.info("✅ Gemini agent initialized")
            except Exception as e:
                logger.warning(f"⚠️ Gemini init failed: {e}")
                self.use_gemini = False
        elif use_gemini and not GEMINI_AVAILABLE:
            logger.warning("⚠️ Gemini not available - using Ollama only")
            self.use_gemini = False

        if not self.use_ollama and not self.use_gemini:
            logger.error("❌ No AI agents available!")
            raise RuntimeError("Need at least one AI agent (Ollama or Gemini)")

        logger.info("✅ Loop initialized successfully")

    async def run_complete_cycle(
        self, library_name: str, task_description: str, generation_size: int = 3
    ) -> dict:
        """
        Run complete ingestion → generation → analysis cycle.

        Args:
            library_name: Library to ingest (e.g., "requests")
            task_description: Code generation task
            generation_size: Number of variants to generate

        Returns:
            Dict with cycle results and best code
        """
        logger.info("=" * 80)
        logger.info("🧬 STARTING COMPLETE CYCLE")
        logger.info(f"Library: {library_name}")
        logger.info(f"Task: {task_description[:100]}...")
        logger.info("=" * 80)

        # Create generation output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        gen_dir = self.output_dir / f"{library_name}_gen0_{timestamp}"
        gen_dir.mkdir(parents=True, exist_ok=True)

        # STEP 1: Ingest Library
        logger.info("\n📚 STEP 1: Library Ingestion")
        paradigms = self._ingest_and_extract(library_name)
        if not paradigms:
            logger.error("❌ No paradigms extracted - cycle aborted")
            return {"success": False, "error": "No paradigms extracted"}

        # STEP 2: Generate Prompt
        logger.info("\n🤖 STEP 2: Prompt Generation")
        instruction = self.prompt_gen.create_agent_instruction(
            task=task_description,
            paradigms=paradigms[:10],  # Top 10 paradigms
            consciousness_level=0.85,
        )
        prompt = instruction.to_prompt()

        # Save prompt
        prompt_file = gen_dir / "prompt.txt"
        prompt_file.write_text(prompt, encoding="utf-8")
        logger.info(f"💾 Prompt saved: {prompt_file}")

        # STEP 3: Generate Code Population
        logger.info(f"\n🦙 STEP 3: Code Generation ({generation_size} variants)")
        population = await self._generate_population(prompt, generation_size)

        if not population:
            logger.error("❌ No code generated - cycle aborted")
            return {"success": False, "error": "No code generated"}

        # Save generated code
        for i, variant in enumerate(population):
            code_file = gen_dir / f"variant_{i}.py"
            code_file.write_text(variant["code"], encoding="utf-8")

        # STEP 4: Analyze Population
        logger.info("\n🔬 STEP 4: Code Analysis")
        analysis_results = []
        for i, variant in enumerate(population):
            result = self.analyzer.analyze_code(
                code=variant["code"],
                paradigms=paradigms[:10],
                variant_id=i,
                model=variant.get("model", "unknown"),
            )
            analysis_results.append(result)

            # Save individual analysis
            analysis_file = gen_dir / f"variant_{i}_analysis.json"
            self.analyzer.save_analysis(result, analysis_file)

        # STEP 5: Compare and Select Best
        logger.info("\n🏆 STEP 5: Variant Comparison")
        comparison = self.analyzer.compare_variants(analysis_results)

        best = comparison["best_variant"]
        logger.info(
            f"Best variant: {best.variant_id} "
            f"(consciousness: {best.consciousness_score})"
        )
        logger.info(f"Average consciousness: {comparison['avg_consciousness']}")
        logger.info(
            f"Success rate: {comparison['successful_count']}/"
            f"{comparison['total_count']}"
        )

        # Save summary
        summary = {
            "library": library_name,
            "task": task_description,
            "generation": 0,
            "timestamp": timestamp,
            "paradigms_extracted": len(paradigms),
            "variants_generated": len(population),
            "best_variant_id": best.variant_id,
            "best_consciousness": best.consciousness_score,
            "avg_consciousness": comparison["avg_consciousness"],
            "success_rate": comparison["successful_count"] / comparison["total_count"],
        }

        summary_file = gen_dir / "generation_summary.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        logger.info("\n✅ CYCLE COMPLETE!")
        logger.info(f"📁 Results: {gen_dir}")
        logger.info("=" * 80)

        return {
            "success": True,
            "generation_dir": str(gen_dir),
            "best_code": best.code,
            "best_consciousness": best.consciousness_score,
            "summary": summary,
        }

    def _ingest_and_extract(self, library_name: str) -> List:
        """Ingest library and extract paradigms"""
        # Check if library knowledge file exists
        knowledge_file = (
            self.ingestion.knowledge_base_path / "python" / f"{library_name}.json"
        )

        if not knowledge_file.exists():
            logger.info(f"📥 Library not found: {library_name}")
            logger.info(f"   Expected: {knowledge_file}")
            logger.info(f"   Note: Library must be ingested first")
            return []
        else:
            logger.info(f"✓ Using ingested library: {library_name}")
            logger.info(f"   Knowledge file: {knowledge_file}")

        # Extract paradigms from ingested knowledge
        paradigms = self.extractor.extract_from_library(library_name)
        logger.info(f"✅ Extracted {len(paradigms)} paradigms")

        # Show top paradigms
        top = self.extractor.get_top_paradigms(5)
        logger.info("Top 5 paradigms:")
        for i, p in enumerate(top, 1):
            logger.info(f"  {i}. {p.name} (usage: {p.usage_count}x)")

        return paradigms

    async def _generate_population(self, prompt: str, size: int) -> List[dict]:
        """
        Generate code population using available agents in parallel.

        Strategy:
        - Split generation between Gemini and Ollama for diversity
        - Run generations in parallel for speed
        - Vary temperature for each agent to increase diversity
        """
        population = []
        tasks = []

        # Calculate how many variants each agent should generate
        gemini_count = 0
        ollama_count = 0

        if self.use_gemini and self.use_ollama:
            # Both available - split evenly
            gemini_count = size // 2
            ollama_count = size - gemini_count
            logger.info(
                f"🤖 Dual-agent mode: {gemini_count} Gemini + {ollama_count} Ollama"
            )
        elif self.use_gemini:
            gemini_count = size
            logger.info(f"✨ Gemini-only mode: {gemini_count} variants")
        elif self.use_ollama:
            ollama_count = size
            logger.info(f"🦙 Ollama-only mode: {ollama_count} variants")

        # Generate with Gemini (parallel with temperature variation)
        for i in range(gemini_count):
            temp = 0.6 + (i * 0.15)  # 0.6, 0.75, 0.9...
            tasks.append(self._generate_with_gemini(prompt, temp, i))

        # Generate with Ollama (parallel with temperature variation)
        for i in range(ollama_count):
            temp = 0.5 + (i * 0.2)  # 0.5, 0.7, 0.9...
            tasks.append(self._generate_with_ollama(prompt, temp, i))

        # Run all generations in parallel
        if tasks:
            logger.info(f"🚀 Launching {len(tasks)} parallel generations...")
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Collect successful results
            for result in results:
                if isinstance(result, dict) and result.get("success"):
                    population.append(result)
                elif isinstance(result, Exception):
                    logger.warning(f"⚠️ Generation failed: {result}")

        logger.info(
            f"✅ Generated {len(population)} variants ({gemini_count} Gemini, {ollama_count} Ollama)"
        )
        return population

    async def _generate_with_gemini(
        self, prompt: str, temperature: float, index: int
    ) -> dict:
        """Generate code with Gemini"""
        try:
            logger.info(f"✨ Gemini #{index+1} (temp={temperature:.2f})...")
            code = await self.gemini_agent.generate_code(
                prompt=prompt, temperature=temperature, max_tokens=2048
            )
            model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
            return {
                "code": code,
                "model": f"{model_name}",
                "temperature": temperature,
                "agent": "gemini",
                "success": True,
            }
        except Exception as e:
            logger.error(f"❌ Gemini #{index+1} failed: {e}")
            return {"success": False, "error": str(e)}

    async def _generate_with_ollama(
        self, prompt: str, temperature: float, index: int
    ) -> dict:
        """Generate code with Ollama"""
        try:
            logger.info(f"🦙 Ollama #{index+1} (temp={temperature:.2f})...")
            # Ollama generate_code is synchronous, wrap in asyncio
            result = await asyncio.to_thread(
                self.ollama_agent.generate_code, prompt=prompt, max_tokens=2048
            )
            if result["success"]:
                result["temperature"] = temperature
                result["agent"] = "ollama"
            return result
        except Exception as e:
            logger.error(f"❌ Ollama #{index+1} failed: {e}")
            return {"success": False, "error": str(e)}


async def main():
    """Run MVP test"""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    print("\n🧬 Library Code Generation Loop - MVP")
    print("=" * 80)

    # Configuration
    library = "requests"  # Can be: requests, flask, fastapi

    task = f"""Create a REST API client using patterns from {library}.

The client should:
- Make HTTP GET and POST requests
- Handle JSON responses  
- Include error handling with try/except
- Use type hints
- Follow {library} best practices

Create a complete, production-ready implementation."""

    # Initialize and run
    try:
        loop = LibraryCodeGenerationLoop(use_ollama=True, use_gemini=True)

        result = await loop.run_complete_cycle(
            library_name=library, task_description=task, generation_size=3
        )

        if result["success"]:
            print("\n" + "=" * 80)
            print("🏆 BEST GENERATED CODE:")
            print("=" * 80)
            print(result["best_code"])
            print("=" * 80)
            print(f"\n✅ Consciousness Score: {result['best_consciousness']}")
            print(f"📁 Full Results: {result['generation_dir']}")
        else:
            print(f"\n❌ Cycle failed: {result.get('error')}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
