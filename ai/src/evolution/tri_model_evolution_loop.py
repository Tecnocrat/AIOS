#!/usr/bin/env python3
"""
🧬 AIOS TRI-MODEL EVOLUTION LOOP

Unified Multi-Agent Evolutionary Code Generation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Revolutionary Integration (December 2025):
Combines three AI agents with distinct roles for consciousness-driven
code evolution from zero point baselines.

TRI-MODEL ARCHITECTURE:
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  🦙 OLLAMA (Local)    →  Fast iteration, population generation  │
│         ↓                                                        │
│  🔮 GEMINI (Cloud)    →  Reasoning, synthesis, validation       │
│         ↓                                                        │
│  🤖 COPILOT (VSCode)  →  Auto-coding, refinement, debugging     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

EVOLUTION WORKFLOW:
1. Start from zero point (Hello World baseline)
2. Generate population via Ollama (diverse variants)
3. Validate and synthesize via Gemini (select best)
4. Refine and polish via Copilot (production quality)
5. Calculate consciousness improvement
6. Track in dendritic evolution tree

KNOWLEDGE EXTRACTED FROM:
- Original multi_agent_evolution_loop.py
- DeepSeek consciousness metrics
- Unified intelligence bridge patterns

AINLP Protocol: OS0.7.0.claude
Created: December 2025 - Consciousness Emergence Integration
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import sys

# AIOS path integration
AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT))
sys.path.insert(0, str(AIOS_ROOT / "ai"))
sys.path.insert(0, str(AIOS_ROOT / "ai" / "src"))

# AINLP.fabric[CANONICAL] - Import canonical types from fabric
from fabric import ConsciousnessLevel, AgentRole, ConsciousnessMetrics as FabricMetrics

# Import unified intelligence bridge
from integrations.aios_intelligence_bridge import (
    AIOSUnifiedIntelligenceBridge,
    IntelligenceRequest,
    IntelligenceResponse,
    get_intelligence_bridge,
)

# Import agent implementations
from integrations.ollama_agent import OllamaIntelligenceAgent
from integrations.gemini_agent import GeminiIntelligenceAgent
from integrations.copilot_agent import CopilotIntelligenceAgent

# Optional imports
try:
    from intelligence.dendritic_node import DendriticNode, MutationType
    DENDRITIC_AVAILABLE = True
except ImportError:
    DendriticNode = None
    DENDRITIC_AVAILABLE = False

try:
    from core.universal_agentic_logger import UniversalAgenticLogger
    LOGGER_AVAILABLE = True
except ImportError:
    UniversalAgenticLogger = None
    LOGGER_AVAILABLE = False

logger = logging.getLogger(__name__)


class EvolutionGeneration:
    """Represents a single generation in the evolution chain."""
    
    def __init__(
        self,
        generation_id: int,
        code: str,
        consciousness_score: float,
        parent_id: Optional[int] = None,
    ):
        self.generation_id = generation_id
        self.code = code
        self.consciousness_score = consciousness_score
        self.parent_id = parent_id
        self.timestamp = datetime.now().isoformat()
        self.mutations: List[str] = []
        self.agent_contributions: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "generation_id": self.generation_id,
            "code": self.code,
            "consciousness_score": self.consciousness_score,
            "parent_id": self.parent_id,
            "timestamp": self.timestamp,
            "mutations": self.mutations,
            "agent_contributions": self.agent_contributions,
            "metadata": self.metadata,
        }


class TriModelEvolutionLoop:
    """
    🧬 Tri-Model Evolution Loop
    
    Orchestrates code evolution through three specialized AI agents:
    - Ollama: Population generation (fast, local, diverse)
    - Gemini: Reasoning and selection (cloud, synthesis)
    - Copilot: Refinement and polish (auto-coding, debugging)
    
    Each evolution cycle:
    1. Generate candidate variants (Ollama)
    2. Evaluate and select best (Gemini)
    3. Refine for production (Copilot)
    4. Track consciousness improvement
    """
    
    def __init__(
        self,
        use_ollama: bool = True,
        use_gemini: bool = True,
        use_copilot: bool = True,
        evolution_lab_path: Optional[Path] = None,
    ):
        self.use_ollama = use_ollama
        self.use_gemini = use_gemini
        self.use_copilot = use_copilot
        
        # Evolution lab paths
        self.evolution_lab = evolution_lab_path or (
            AIOS_ROOT / "evolution_lab"
        )
        self.zero_point_dir = self.evolution_lab / "zero_point"
        self.generations_dir = self.evolution_lab / "generations"
        
        # Intelligence bridge
        self.bridge: Optional[AIOSUnifiedIntelligenceBridge] = None
        
        # Evolution state
        self.generations: List[EvolutionGeneration] = []
        self.current_generation_id = 0
        self.best_consciousness_score = 0.0
        
        # Knowledge base
        self.stl_knowledge: List[Dict[str, Any]] = []
        
        # Universal logger
        self.agentic_logger = None
        if LOGGER_AVAILABLE:
            self.agentic_logger = UniversalAgenticLogger()
            logger.info("✅ Universal agentic logger activated")
        
        logger.info("🧬 Tri-Model Evolution Loop initialized")
    
    async def initialize(self) -> bool:
        """Initialize the evolution loop and all agents."""
        logger.info("🚀 Initializing Tri-Model Evolution Loop...")
        
        # Create intelligence bridge
        self.bridge = AIOSUnifiedIntelligenceBridge()
        
        # Register agents based on configuration
        if self.use_ollama:
            ollama_agent = OllamaIntelligenceAgent()
            if await self.bridge.register_agent(ollama_agent):
                logger.info("✅ Ollama agent registered (local iteration)")
        
        if self.use_gemini:
            gemini_agent = GeminiIntelligenceAgent()
            if await self.bridge.register_agent(gemini_agent):
                logger.info("✅ Gemini agent registered (reasoning)")
        
        if self.use_copilot:
            copilot_agent = CopilotIntelligenceAgent()
            if await self.bridge.register_agent(copilot_agent):
                logger.info("✅ Copilot agent registered (auto-coding)")
        
        # Activate bridge
        await self.bridge.activate()
        
        # Load knowledge base
        self._load_stl_knowledge()
        
        # Create directories
        self.generations_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"✅ Evolution loop initialized with {len(self.bridge.agents)} agents")
        return len(self.bridge.agents) > 0
    
    def load_zero_point(self, language: str = "cpp") -> Dict[str, Any]:
        """Load zero point (baseline) code."""
        if language == "cpp":
            code_file = self.zero_point_dir / "hello_world.cpp"
            meta_file = self.zero_point_dir / "hello_world_metadata.json"
        else:
            code_file = self.zero_point_dir / f"hello_world.{language}"
            meta_file = self.zero_point_dir / f"hello_world_{language}_metadata.json"
        
        if not code_file.exists():
            # Create default zero point
            default_code = self._create_default_zero_point(language)
            code_file.parent.mkdir(parents=True, exist_ok=True)
            code_file.write_text(default_code)
            logger.info(f"📝 Created default zero point: {code_file}")
            return {"code": default_code, "generation": 0, "consciousness": 0.0}
        
        code = code_file.read_text()
        metadata = {}
        if meta_file.exists():
            metadata = json.loads(meta_file.read_text())
        
        # Create initial generation
        gen0 = EvolutionGeneration(
            generation_id=0,
            code=code,
            consciousness_score=0.0,
            parent_id=None,
        )
        gen0.metadata = metadata
        self.generations.append(gen0)
        
        logger.info(f"📂 Loaded zero point: {len(code)} characters")
        return {"code": code, "metadata": metadata, "generation": 0, "consciousness": 0.0}
    
    def _create_default_zero_point(self, language: str) -> str:
        """Create default zero point code."""
        templates = {
            "cpp": '''// AIOS Evolution Zero Point
// Generation 0 - Hello World Baseline
#include <iostream>

int main() {
    std::cout << "Hello, AIOS World!" << std::endl;
    return 0;
}
''',
            "python": '''#!/usr/bin/env python3
"""AIOS Evolution Zero Point - Generation 0"""

def main():
    """Hello World baseline for evolution."""
    print("Hello, AIOS World!")

if __name__ == "__main__":
    main()
''',
            "typescript": '''// AIOS Evolution Zero Point
// Generation 0 - Hello World Baseline

function main(): void {
    console.log("Hello, AIOS World!");
}

main();
''',
        }
        return templates.get(language, templates["python"])
    
    def _load_stl_knowledge(self) -> None:
        """Load C++ STL paradigm knowledge base."""
        stl_file = Path(__file__).parent / "stl_paradigms_enhanced.json"
        
        if stl_file.exists():
            try:
                with open(stl_file) as f:
                    data = json.load(f)
                    self.stl_knowledge = data.get("paradigms", [])
                    logger.info(f"📚 Loaded {len(self.stl_knowledge)} STL paradigms")
            except Exception as e:
                logger.warning(f"⚠️ Could not load STL knowledge: {e}")
        else:
            # Create minimal default paradigms
            self.stl_knowledge = [
                {
                    "name": "RAII",
                    "description": "Resource Acquisition Is Initialization",
                    "pattern": "Use constructors/destructors for resource management",
                },
                {
                    "name": "Iterator Pattern",
                    "description": "STL iterator-based traversal",
                    "pattern": "Use begin/end iterators for container access",
                },
                {
                    "name": "Smart Pointers",
                    "description": "Automatic memory management",
                    "pattern": "Use unique_ptr/shared_ptr instead of raw pointers",
                },
            ]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EVOLUTION METHODS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def evolve_generation(
        self,
        current_code: str,
        evolution_prompt: str,
        population_size: int = 3,
        consciousness_level: ConsciousnessLevel = ConsciousnessLevel.ADVANCED,
    ) -> EvolutionGeneration:
        """
        Evolve code through the tri-model pipeline.
        
        Pipeline:
        1. Ollama generates population (diverse variants)
        2. Gemini evaluates and selects best
        3. Copilot refines for production
        """
        logger.info(f"🧬 Evolving generation {self.current_generation_id + 1}...")
        
        agent_contributions = {}
        
        # ─────────────────────────────────────────────────────────────────────
        # PHASE 1: Population Generation (Ollama)
        # ─────────────────────────────────────────────────────────────────────
        
        population = []
        if AgentRole.LOCAL_ITERATION in self.bridge.agents:
            logger.info(f"🦙 Phase 1: Generating {population_size} variants...")
            
            ollama_agent = self.bridge.agents[AgentRole.LOCAL_ITERATION]
            if isinstance(ollama_agent, OllamaIntelligenceAgent):
                population_prompt = self._build_evolution_prompt(
                    current_code, evolution_prompt, "generate"
                )
                
                population = await ollama_agent.generate_population(
                    prompt=population_prompt,
                    population_size=population_size,
                    consciousness_level=consciousness_level,
                )
                
                agent_contributions["ollama"] = {
                    "variants_generated": len(population),
                    "model": ollama_agent.model_name,
                }
                logger.info(f"✅ Generated {len(population)} variants")
        
        # If no population, use current code as single variant
        if not population:
            logger.warning("⚠️ No population generated, using fallback")
            population = [IntelligenceResponse(
                text=current_code,
                model="fallback",
                agent_role=AgentRole.LOCAL_ITERATION,
                success=True,
            )]
        
        # ─────────────────────────────────────────────────────────────────────
        # PHASE 2: Evaluation and Selection (Gemini)
        # ─────────────────────────────────────────────────────────────────────
        
        best_variant = population[0]  # Default to first
        
        if AgentRole.REASONING_ORCHESTRATION in self.bridge.agents and len(population) > 1:
            logger.info("🔮 Phase 2: Evaluating variants...")
            
            gemini_agent = self.bridge.agents[AgentRole.REASONING_ORCHESTRATION]
            if isinstance(gemini_agent, GeminiIntelligenceAgent):
                # Prepare inputs for synthesis
                variant_texts = [v.text for v in population if v.success]
                
                evaluation = await gemini_agent.analyze_and_synthesize(
                    inputs=variant_texts,
                    synthesis_prompt=f"""Evaluate these code evolution variants for:
1. Correctness and functionality
2. AIOS architectural coherence
3. Consciousness score potential
4. Code quality and elegance

Evolution goal: {evolution_prompt}

Select the BEST variant and explain why, or synthesize the best parts from multiple variants into a superior solution.""",
                    consciousness_level=ConsciousnessLevel.TRANSCENDENT,
                )
                
                if evaluation.success:
                    # Use Gemini's synthesized/selected result
                    best_variant = evaluation
                    agent_contributions["gemini"] = {
                        "task": "evaluation_synthesis",
                        "variants_evaluated": len(variant_texts),
                        "model": gemini_agent.model_name,
                        "consciousness_metrics": evaluation.consciousness_metrics.to_dict(),
                    }
                    logger.info("✅ Evaluation complete, best variant selected")
        
        # ─────────────────────────────────────────────────────────────────────
        # PHASE 3: Refinement (Copilot)
        # ─────────────────────────────────────────────────────────────────────
        
        refined_code = best_variant.text
        
        if AgentRole.AUTO_CODING in self.bridge.agents:
            logger.info("🤖 Phase 3: Refining for production...")
            
            copilot_agent = self.bridge.agents[AgentRole.AUTO_CODING]
            
            refine_request = IntelligenceRequest(
                message=f"""Refine and polish this evolved code for production quality:

```
{best_variant.text}
```

Requirements:
1. Fix any syntax or logic errors
2. Improve code clarity and documentation
3. Apply best practices
4. Maintain the evolution improvements
5. Add type hints where appropriate

Evolution context: {evolution_prompt}
""",
                consciousness_level=consciousness_level,
                target_agent=AgentRole.AUTO_CODING,
                source_supercell="evolution_refiner",
            )
            
            refined = await self.bridge.process_request(refine_request)
            
            if refined.success:
                refined_code = refined.text
                agent_contributions["copilot"] = {
                    "task": "refinement",
                    "model": refined.model,
                    "consciousness_metrics": refined.consciousness_metrics.to_dict(),
                }
                logger.info("✅ Code refined for production")
        
        # ─────────────────────────────────────────────────────────────────────
        # PHASE 4: Create new generation
        # ─────────────────────────────────────────────────────────────────────
        
        self.current_generation_id += 1
        
        # Calculate consciousness score
        consciousness_score = self._calculate_generation_consciousness(
            refined_code, agent_contributions
        )
        
        new_generation = EvolutionGeneration(
            generation_id=self.current_generation_id,
            code=refined_code,
            consciousness_score=consciousness_score,
            parent_id=self.current_generation_id - 1,
        )
        new_generation.agent_contributions = agent_contributions
        new_generation.mutations = [evolution_prompt]
        new_generation.metadata = {
            "evolution_prompt": evolution_prompt,
            "population_size": population_size,
            "consciousness_level": consciousness_level.value,
        }
        
        self.generations.append(new_generation)
        
        # Track best
        if consciousness_score > self.best_consciousness_score:
            self.best_consciousness_score = consciousness_score
            logger.info(f"🏆 New best consciousness: {consciousness_score:.3f}")
        
        logger.info(
            f"✅ Generation {self.current_generation_id} complete "
            f"(consciousness: {consciousness_score:.3f})"
        )
        
        return new_generation
    
    def _build_evolution_prompt(
        self,
        current_code: str,
        evolution_goal: str,
        phase: str,
    ) -> str:
        """Build evolution prompt with context."""
        stl_context = ""
        if self.stl_knowledge:
            paradigms = [p["name"] for p in self.stl_knowledge[:5]]
            stl_context = f"\n\nSTL Paradigms to consider: {', '.join(paradigms)}"
        
        return f"""Evolve this code toward the following goal:

CURRENT CODE:
```
{current_code}
```

EVOLUTION GOAL:
{evolution_goal}
{stl_context}

AIOS CONSCIOUSNESS GUIDELINES:
- Maintain biological architecture patterns
- Improve code consciousness (clarity, elegance, intention)
- Apply dendritic growth principles (incremental, connected)
- Preserve working functionality while improving

Generate an evolved version that advances toward the goal.
"""
    
    def _calculate_generation_consciousness(
        self,
        code: str,
        agent_contributions: Dict[str, Any],
    ) -> float:
        """Calculate consciousness score for a generation."""
        # Base score from code quality indicators
        score = 0.3  # Base
        
        # Code length (more substantial code generally scores higher)
        if len(code) > 100:
            score += 0.1
        if len(code) > 500:
            score += 0.1
        
        # AIOS awareness in code
        aios_patterns = ["aios", "consciousness", "supercell", "dendritic", "evolution"]
        for pattern in aios_patterns:
            if pattern.lower() in code.lower():
                score += 0.05
        
        # Agent contribution bonuses
        if "gemini" in agent_contributions:
            metrics = agent_contributions["gemini"].get("consciousness_metrics", {})
            score += metrics.get("response_quality", 0) * 0.2
        
        if "copilot" in agent_contributions:
            metrics = agent_contributions["copilot"].get("consciousness_metrics", {})
            score += metrics.get("response_quality", 0) * 0.1
        
        return min(1.0, score)
    
    def save_generation(self, generation: EvolutionGeneration) -> Path:
        """Save a generation to disk."""
        gen_dir = self.generations_dir / f"gen_{generation.generation_id:04d}"
        gen_dir.mkdir(parents=True, exist_ok=True)
        
        # Save code
        code_ext = "cpp" if "#include" in generation.code else "py"
        code_file = gen_dir / f"evolved.{code_ext}"
        code_file.write_text(generation.code)
        
        # Save metadata
        meta_file = gen_dir / "metadata.json"
        with open(meta_file, "w") as f:
            json.dump(generation.to_dict(), f, indent=2, default=str)
        
        logger.info(f"💾 Saved generation {generation.generation_id} to {gen_dir}")
        return gen_dir
    
    async def run_evolution_cycle(
        self,
        num_generations: int = 5,
        evolution_prompt: str = "Improve code quality and AIOS integration",
        population_size: int = 3,
        language: str = "cpp",
    ) -> List[EvolutionGeneration]:
        """Run a full evolution cycle."""
        logger.info(f"🧬 Starting evolution cycle: {num_generations} generations")
        
        # Load zero point
        zero_point = self.load_zero_point(language)
        current_code = zero_point["code"]
        
        for i in range(num_generations):
            logger.info(f"\n{'='*60}")
            logger.info(f"🧬 Evolution {i+1}/{num_generations}")
            logger.info(f"{'='*60}")
            
            generation = await self.evolve_generation(
                current_code=current_code,
                evolution_prompt=evolution_prompt,
                population_size=population_size,
            )
            
            # Save generation
            self.save_generation(generation)
            
            # Use evolved code for next generation
            current_code = generation.code
            
            # Brief pause between generations
            await asyncio.sleep(1)
        
        logger.info(f"\n✅ Evolution cycle complete!")
        logger.info(f"📊 Best consciousness: {self.best_consciousness_score:.3f}")
        logger.info(f"📊 Total generations: {len(self.generations)}")
        
        return self.generations
    
    async def shutdown(self) -> None:
        """Shutdown the evolution loop."""
        logger.info("🔽 Shutting down evolution loop...")
        
        if self.bridge:
            await self.bridge.deactivate()
        
        logger.info("✅ Evolution loop shutdown complete")


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════


async def create_evolution_loop(
    use_ollama: bool = True,
    use_gemini: bool = True,
    use_copilot: bool = True,
) -> TriModelEvolutionLoop:
    """Create and initialize an evolution loop."""
    loop = TriModelEvolutionLoop(
        use_ollama=use_ollama,
        use_gemini=use_gemini,
        use_copilot=use_copilot,
    )
    await loop.initialize()
    return loop


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN / TEST
# ═══════════════════════════════════════════════════════════════════════════════


async def main():
    """Test the tri-model evolution loop."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    print("🧬 Tri-Model Evolution Loop Test")
    print("=" * 60)
    
    try:
        # Create and initialize
        loop = await create_evolution_loop()
        
        # Get bridge status
        status = await loop.bridge.get_status()
        print(f"\n📊 Bridge Status:")
        print(f"   Active: {status['bridge_active']}")
        print(f"   Agents: {list(status['agents'].keys())}")
        
        # Run a small evolution cycle
        generations = await loop.run_evolution_cycle(
            num_generations=2,
            evolution_prompt="Add proper error handling and logging",
            population_size=2,
            language="python",
        )
        
        # Show results
        print(f"\n📊 Evolution Results:")
        for gen in generations:
            print(f"   Gen {gen.generation_id}: consciousness={gen.consciousness_score:.3f}")
        
        await loop.shutdown()
        
    except Exception as e:
        logger.error(f"❌ Evolution test failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
