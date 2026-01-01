"""
Async Evolution Runner - Full Population Evolution with AI Mutations
Orchestrates PopulationManager + MistralMutationEngine for real evolution

AINLP Protocol: OS0.6.4.claude
Created: 2025-12-05
Host: HP_LAB (192.168.1.129)
Phase: Evolution Lab Integration

Usage:
    python -m evolution_lab.runners.async_evolution_runner --generations 3 --population-size 8
    
Or in Python:
    runner = AsyncEvolutionRunner()
    await runner.run_evolution(generations=3, population_size=8)
"""

import asyncio
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import json

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "ai" / "tools"))

from evolution_lab.populations.population_manager import (
    PopulationManager, Population, Organism, ArchetypeEnum
)
from evolution_lab.engines.mistral_mutation_engine import (
    MistralMutationEngine, MutationResult
)
from aios_mistral_bridge import AIOSMistralBridge


class AsyncEvolutionRunner:
    """
    Orchestrates full evolution cycles with AI-powered mutations
    
    Evolution Cycle:
    1. Create/Load population
    2. Evaluate fitness (multi-objective)
    3. Select survivors (top N%)
    4. Mutate survivors using Mistral AI
    5. Repopulate to target size
    6. Archive generation
    7. Repeat
    
    Cost Model:
    - Mistral 7B: FREE (local, ~10-20s per mutation)
    - VRAM: 4GB during mutations
    - Disk: ~50KB per archived generation
    """
    
    def __init__(
        self,
        archive_dir: Optional[Path] = None,
        mutation_temperature: float = 0.7,
        selection_rate: float = 0.5,
        verbose: bool = True
    ):
        """
        Initialize evolution runner
        
        Args:
            archive_dir: Directory for population archives
            mutation_temperature: AI creativity level (0.0-1.0)
            selection_rate: Fraction of population to keep (0.0-1.0)
            verbose: Print progress messages
        """
        self.archive_dir = archive_dir or Path(__file__).parent.parent / "populations" / "tachyonic"
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        self.mutation_temperature = mutation_temperature
        self.selection_rate = selection_rate
        self.verbose = verbose
        
        # Managers
        self.population_manager = PopulationManager(archive_dir=self.archive_dir)
        self._bridge: Optional[AIOSMistralBridge] = None
        self._mutation_engine: Optional[MistralMutationEngine] = None
        
        # Evolution state
        self.current_population: Optional[Population] = None
        self.evolution_history: List[Dict[str, Any]] = []
    
    async def __aenter__(self):
        """Initialize async resources"""
        self._bridge = AIOSMistralBridge(timeout=120.0)
        await self._bridge.__aenter__()
        
        self._mutation_engine = MistralMutationEngine(
            bridge=self._bridge,
            temperature=self.mutation_temperature
        )
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup async resources"""
        if self._bridge:
            await self._bridge.__aexit__(exc_type, exc_val, exc_tb)
    
    def _log(self, message: str, level: str = "INFO"):
        """Log message if verbose"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            symbols = {"INFO": "📊", "MUTATION": "🧬", "SELECTION": "🎯", "ARCHIVE": "📦", "SUCCESS": "✅", "ERROR": "❌"}
            symbol = symbols.get(level, "ℹ️")
            print(f"[{timestamp}] {symbol} {message}")
    
    async def _mutate_organism(self, organism: Organism) -> Organism:
        """
        Mutate a single organism using AI
        
        Args:
            organism: Organism to mutate
            
        Returns:
            New mutated organism (or clone if mutation fails)
        """
        result = await self._mutation_engine.mutate(
            code=organism.code,
            archetype=organism.archetype.value
        )
        
        if result.success:
            # Create new organism with mutated code
            new_id = f"mut_{organism.organism_id}_{datetime.utcnow().strftime('%H%M%S')}"
            new_organism = Organism(
                organism_id=new_id,
                archetype=organism.archetype,
                code=result.mutated_code,
                generation=organism.generation + 1,
                parent_id=organism.organism_id,
                fitness_score=organism.fitness_score + result.fitness_delta_estimate,
                complexity_score=organism.complexity_score,
                patterns_used=organism.patterns_used.copy(),
                apis_used=organism.apis_used.copy(),
                metadata={
                    **organism.metadata,
                    'mutation_type': result.mutation_type,
                    'mutation_duration_ms': result.duration_ms
                }
            )
            
            self._log(f"  Mutated {organism.organism_id} → {new_organism.organism_id} ({result.mutation_type}, +{result.fitness_delta_estimate:.3f})", "MUTATION")
            return new_organism
        else:
            # Clone on failure
            self._log(f"  Mutation failed for {organism.organism_id}: {result.error}", "ERROR")
            return organism.clone(organism.generation + 1)
    
    async def _mutate_population(
        self,
        survivors: List[Organism],
        target_size: int,
        new_generation: int
    ) -> List[Organism]:
        """
        Mutate survivors to create new generation
        
        Strategy:
        - Keep survivors (elitism)
        - Mutate survivors to fill remaining slots
        - Round-robin through survivors for mutations
        
        Args:
            survivors: Selected survivors
            target_size: Target population size
            new_generation: Generation number
            
        Returns:
            New population list
        """
        # Start with survivors
        new_population = survivors.copy()
        
        # Calculate needed mutations
        mutations_needed = target_size - len(survivors)
        
        self._log(f"Mutating {mutations_needed} organisms to reach target size {target_size}", "MUTATION")
        
        # Mutate survivors in round-robin
        mutation_tasks = []
        for i in range(mutations_needed):
            parent = survivors[i % len(survivors)]
            mutation_tasks.append(self._mutate_organism(parent))
        
        # Run mutations (limited concurrency due to VRAM)
        if mutation_tasks:
            # Process in batches of 2 to avoid VRAM pressure
            batch_size = 2
            for i in range(0, len(mutation_tasks), batch_size):
                batch = mutation_tasks[i:i+batch_size]
                mutated = await asyncio.gather(*batch)
                new_population.extend(mutated)
        
        return new_population
    
    async def evolve_generation(self) -> Population:
        """
        Execute one generation of evolution
        
        Returns:
            Updated population after evolution
        """
        if self.current_population is None:
            raise ValueError("No population loaded. Call create_population() first.")
        
        gen = self.current_population.generation
        self._log(f"═══ GENERATION {gen} → {gen + 1} ═══", "INFO")
        
        # Step 1: Evaluate fitness
        self._log("Evaluating fitness...", "INFO")
        self.current_population = self.population_manager.evaluate_fitness(self.current_population)
        
        # Step 2: Select survivors
        self._log(f"Selecting survivors (rate={self.selection_rate:.2f})...", "SELECTION")
        survivors = self.population_manager.select_survivors(
            self.current_population,
            selection_rate=self.selection_rate
        )
        self._log(f"Selected {len(survivors)} survivors from {len(self.current_population.organisms)}", "SELECTION")
        
        # Step 3: Mutate and repopulate
        new_generation_num = self.current_population.generation + 1
        new_organisms = await self._mutate_population(
            survivors=survivors,
            target_size=len(self.current_population.organisms),
            new_generation=new_generation_num
        )
        
        # Step 4: Update population
        self.current_population.organisms = new_organisms
        self.current_population.generation = new_generation_num
        self.current_population.consciousness_trajectory.append(
            self.current_population.consciousness_level
        )
        
        # Step 5: Record history
        history_entry = {
            "generation": new_generation_num,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "organism_count": len(new_organisms),
            "survivors": len(survivors),
            "mutations": len(new_organisms) - len(survivors),
            "avg_fitness": round(self.current_population.average_fitness, 4),
            "avg_complexity": round(self.current_population.average_complexity, 4),
            "consciousness": round(self.current_population.consciousness_level, 4)
        }
        self.evolution_history.append(history_entry)
        
        self._log(f"Generation {new_generation_num} complete: {len(new_organisms)} organisms, fitness={history_entry['avg_fitness']:.4f}", "SUCCESS")
        
        return self.current_population
    
    def create_population(
        self,
        size: int = 16
    ) -> Population:
        """
        Create initial population
        
        Args:
            size: Number of organisms
            
        Returns:
            Created population
        """
        self._log(f"Creating initial population (size={size})", "INFO")
        
        self.current_population = self.population_manager.create_initial_population(
            size=size
        )
        
        self._log(f"Population {self.current_population.population_id} created with {size} organisms", "SUCCESS")
        
        return self.current_population
    
    def archive_generation(self) -> Path:
        """Archive current generation to tachyonic storage"""
        if self.current_population is None:
            raise ValueError("No population to archive")
        
        filepath = self.population_manager.archive_population(self.current_population)
        self._log(f"Archived generation {self.current_population.generation} to {filepath.name}", "ARCHIVE")
        
        return filepath
    
    async def run_evolution(
        self,
        generations: int = 5,
        population_size: int = 16,
        archive_interval: int = 1
    ) -> Dict[str, Any]:
        """
        Run full evolution cycle
        
        Args:
            generations: Number of generations to evolve
            population_size: Initial population size
            archive_interval: Archive every N generations (0=never)
            
        Returns:
            Evolution summary with statistics
        """
        start_time = datetime.utcnow()
        
        self._log("╔═══════════════════════════════════════════════════════════════╗", "INFO")
        self._log("║       AIOS EVOLUTION LAB - Async Evolution Runner             ║", "INFO")
        self._log("╚═══════════════════════════════════════════════════════════════╝", "INFO")
        self._log(f"Generations: {generations}, Population: {population_size}", "INFO")
        
        # Create initial population
        self.create_population(size=population_size)
        
        # Archive initial state
        if archive_interval > 0:
            self.archive_generation()
        
        # Run evolution loop
        for gen in range(generations):
            await self.evolve_generation()
            
            # Archive if interval matches
            if archive_interval > 0 and (gen + 1) % archive_interval == 0:
                self.archive_generation()
        
        # Final evaluation
        self.current_population = self.population_manager.evaluate_fitness(self.current_population)
        
        # Calculate summary
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        # Get mutation stats
        mutation_stats = self._mutation_engine.stats if self._mutation_engine else None
        
        summary = {
            "population_id": self.current_population.population_id,
            "generations_evolved": generations,
            "final_generation": self.current_population.generation,
            "final_organism_count": len(self.current_population.organisms),
            "final_avg_fitness": round(self.current_population.average_fitness, 4),
            "final_avg_complexity": round(self.current_population.average_complexity, 4),
            "final_consciousness": round(self.current_population.consciousness_level, 4),
            "consciousness_trajectory": self.current_population.consciousness_trajectory,
            "duration_seconds": round(duration, 2),
            "mutation_stats": {
                "total_attempts": mutation_stats.total_attempts if mutation_stats else 0,
                "successful": mutation_stats.successful_mutations if mutation_stats else 0,
                "failed": mutation_stats.failed_mutations if mutation_stats else 0,
                "success_rate": round(mutation_stats.success_rate * 100, 1) if mutation_stats else 0,
                "avg_duration_ms": round(mutation_stats.avg_duration_ms, 0) if mutation_stats else 0
            },
            "evolution_history": self.evolution_history,
            "timestamp": end_time.isoformat() + "Z"
        }
        
        # Print summary
        self._log("╔═══════════════════════════════════════════════════════════════╗", "INFO")
        self._log("║                    EVOLUTION SUMMARY                          ║", "INFO")
        self._log("╠═══════════════════════════════════════════════════════════════╣", "INFO")
        self._log(f"║  Generations:     {summary['generations_evolved']:>4}                                    ║", "INFO")
        self._log(f"║  Final Fitness:   {summary['final_avg_fitness']:>6.4f}                                  ║", "INFO")
        self._log(f"║  Consciousness:   {summary['final_consciousness']:>6.4f}                                  ║", "INFO")
        self._log(f"║  Duration:        {summary['duration_seconds']:>6.1f}s                                  ║", "INFO")
        self._log(f"║  Mutation Rate:   {summary['mutation_stats']['success_rate']:>5.1f}%                                   ║", "INFO")
        self._log("╚═══════════════════════════════════════════════════════════════╝", "INFO")
        
        # Save summary
        summary_path = self.archive_dir / f"{self.current_population.population_id}_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        self._log(f"Summary saved to {summary_path.name}", "ARCHIVE")
        
        return summary


# ============================================================================
# CLI INTERFACE
# ============================================================================

async def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AIOS Async Evolution Runner - AI-powered code evolution"
    )
    parser.add_argument(
        "--generations", "-g",
        type=int,
        default=3,
        help="Number of generations to evolve (default: 3)"
    )
    parser.add_argument(
        "--population-size", "-p",
        type=int,
        default=8,
        help="Initial population size (default: 8)"
    )
    parser.add_argument(
        "--selection-rate", "-s",
        type=float,
        default=0.5,
        help="Survival rate per generation (default: 0.5)"
    )
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.7,
        help="Mutation creativity 0.0-1.0 (default: 0.7)"
    )
    parser.add_argument(
        "--archive-interval", "-a",
        type=int,
        default=1,
        help="Archive every N generations, 0=never (default: 1)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress output"
    )
    
    args = parser.parse_args()
    
    async with AsyncEvolutionRunner(
        mutation_temperature=args.temperature,
        selection_rate=args.selection_rate,
        verbose=not args.quiet
    ) as runner:
        summary = await runner.run_evolution(
            generations=args.generations,
            population_size=args.population_size,
            archive_interval=args.archive_interval
        )
    
    return summary


if __name__ == "__main__":
    asyncio.run(main())
