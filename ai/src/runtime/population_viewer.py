"""
AIOS Population Viewer & Human Review Dashboard
================================================

AINLP Protocol: OS0.6.2.claude
Purpose: Human-accessible interface for reviewing evolutionary work
Status: Production-ready comprehensive viewer

FEATURES:
1. Population Discovery: Find all evolution_lab populations
2. Generation Analysis: View mutation lineage and consciousness evolution
3. Agent Perspective Review: See what AI agents decided and why
4. Code Diff Visualization: Compare generations side-by-side
5. Consciousness Trajectory: Plot evolution across generations
6. Export/Archive: Save interesting populations to tachyonic

INTEGRATION:
- Evolution Lab: Reads JSON populations from evolution_lab/populations/
- Agentic Conclave: Shows agent decisions and consensus
- Consciousness Metrics: Three-level stress system visualization
- Neural Chains: Linked list traversal of evolutionary lineage

DENDRITIC CONNECTIONS:
- ai/src/evolution/population_manager.py - population storage
- ai/src/intelligence/ainlp_agentic_orchestrator.py - agent decisions
- evolution_lab/neural_chains/ - evolutionary memory
- tachyonic/archive/ - strategic archival
"""

import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

# AIOS path integration
AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT / "ai"))

logger = logging.getLogger(__name__)

<<<<<<< HEAD

@dataclass
class GenerationSnapshot:
    """Single generation in evolutionary lineage"""

=======
@dataclass
class GenerationSnapshot:
    """Single generation in evolutionary lineage"""
>>>>>>> origin/OS0.6.2.grok
    generation_id: str
    generation_number: int
    parent_id: Optional[str]
    timestamp: str
    code_size: int
    consciousness_level: str  # LOW/MEDIUM/HIGH
    agent_decisions: List[Dict[str, Any]]
    mutation_type: str
    success: bool
    notes: str

<<<<<<< HEAD

@dataclass
class PopulationSummary:
    """High-level population metrics"""

=======
@dataclass
class PopulationSummary:
    """High-level population metrics"""
>>>>>>> origin/OS0.6.2.grok
    population_id: str
    created: str
    total_generations: int
    total_organisms: int
    consciousness_trajectory: List[str]  # [LOW, LOW, MEDIUM, HIGH, ...]
    best_organism_id: str
    evolutionary_strategy: str
    status: str  # active/archived/failed

<<<<<<< HEAD

class PopulationViewer:
    """
    Human review interface for evolutionary populations.

    USAGE:
        viewer = PopulationViewer()

        # Discover all populations
        populations = viewer.discover_populations()
        print(f"Found {len(populations)} populations")

        # View specific population
        details = viewer.view_population(population_id)
        print(details['summary'])

=======
class PopulationViewer:
    """
    Human review interface for evolutionary populations.
    
    USAGE:
        viewer = PopulationViewer()
        
        # Discover all populations
        populations = viewer.discover_populations()
        print(f"Found {len(populations)} populations")
        
        # View specific population
        details = viewer.view_population(population_id)
        print(details['summary'])
        
>>>>>>> origin/OS0.6.2.grok
        # Review agent decisions
        decisions = viewer.get_agent_perspectives(population_id, generation_num=3)
        for agent, decision in decisions.items():
            print(f"{agent}: {decision['recommendation']}")
<<<<<<< HEAD

        # Export interesting work
        viewer.export_to_tachyonic(population_id, reason="Breakthrough in consciousness")
    """

=======
        
        # Export interesting work
        viewer.export_to_tachyonic(population_id, reason="Breakthrough in consciousness")
    """
    
>>>>>>> origin/OS0.6.2.grok
    def __init__(self):
        """Initialize population viewer with AIOS paths"""
        self.evolution_lab_root = AIOS_ROOT / "evolution_lab"
        self.populations_dir = self.evolution_lab_root / "populations"
        self.neural_chains_dir = self.evolution_lab_root / "neural_chains"
        self.tachyonic_dir = AIOS_ROOT / "tachyonic" / "archive"
<<<<<<< HEAD

        # Ensure directories exist
        self.populations_dir.mkdir(parents=True, exist_ok=True)
        self.neural_chains_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"📊 Population Viewer initialized")
        logger.info(f"   Populations: {self.populations_dir}")
        logger.info(f"   Neural Chains: {self.neural_chains_dir}")

    def discover_populations(self) -> List[PopulationSummary]:
        """
        Discover all evolutionary populations.

=======
        
        # Ensure directories exist
        self.populations_dir.mkdir(parents=True, exist_ok=True)
        self.neural_chains_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📊 Population Viewer initialized")
        logger.info(f"   Populations: {self.populations_dir}")
        logger.info(f"   Neural Chains: {self.neural_chains_dir}")
    
    def discover_populations(self) -> List[PopulationSummary]:
        """
        Discover all evolutionary populations.
        
>>>>>>> origin/OS0.6.2.grok
        Returns:
            List of population summaries sorted by creation date (newest first)
        """
        populations = []
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        # Scan populations directory
        if not self.populations_dir.exists():
            logger.warning(f"⚠️ Populations directory not found: {self.populations_dir}")
            return populations
<<<<<<< HEAD

        json_files = list(self.populations_dir.glob("*.json"))
        logger.info(f"🔍 Found {len(json_files)} population files")

        for pop_file in json_files:
            try:
                with open(pop_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

=======
        
        json_files = list(self.populations_dir.glob("*.json"))
        logger.info(f"🔍 Found {len(json_files)} population files")
        
        for pop_file in json_files:
            try:
                with open(pop_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
>>>>>>> origin/OS0.6.2.grok
                # Extract summary
                summary = PopulationSummary(
                    population_id=data.get("population_id", pop_file.stem),
                    created=data.get("created", "unknown"),
                    total_generations=data.get("generation", 0),
                    total_organisms=len(data.get("organisms", [])),
<<<<<<< HEAD
                    consciousness_trajectory=self._extract_consciousness_trajectory(
                        data
                    ),
                    best_organism_id=self._find_best_organism(data),
                    evolutionary_strategy=data.get("strategy", "unknown"),
                    status=data.get("status", "active"),
                )
                populations.append(summary)

            except Exception as e:
                logger.error(f"❌ Failed to load population {pop_file.name}: {e}")

        # Sort by creation date (newest first)
        populations.sort(key=lambda p: p.created, reverse=True)

        return populations

    def view_population(self, population_id: str) -> Dict[str, Any]:
        """
        Get detailed view of specific population.

        Args:
            population_id: Population identifier

=======
                    consciousness_trajectory=self._extract_consciousness_trajectory(data),
                    best_organism_id=self._find_best_organism(data),
                    evolutionary_strategy=data.get("strategy", "unknown"),
                    status=data.get("status", "active")
                )
                populations.append(summary)
                
            except Exception as e:
                logger.error(f"❌ Failed to load population {pop_file.name}: {e}")
        
        # Sort by creation date (newest first)
        populations.sort(key=lambda p: p.created, reverse=True)
        
        return populations
    
    def view_population(self, population_id: str) -> Dict[str, Any]:
        """
        Get detailed view of specific population.
        
        Args:
            population_id: Population identifier
        
>>>>>>> origin/OS0.6.2.grok
        Returns:
            {
                'summary': PopulationSummary,
                'generations': List[GenerationSnapshot],
                'lineage_tree': Dict[str, List[str]],  # parent -> children
                'agent_decisions': Dict[int, List[Dict]],  # gen_num -> decisions
                'consciousness_evolution': List[Tuple[int, str]],  # (gen, level)
            }
        """
        pop_file = self.populations_dir / f"{population_id}.json"
<<<<<<< HEAD

        if not pop_file.exists():
            logger.error(f"❌ Population not found: {population_id}")
            return {}

        with open(pop_file, "r", encoding="utf-8") as f:
            data = json.load(f)

=======
        
        if not pop_file.exists():
            logger.error(f"❌ Population not found: {population_id}")
            return {}
        
        with open(pop_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
>>>>>>> origin/OS0.6.2.grok
        # Build generation snapshots
        generations = []
        for organism in data.get("organisms", []):
            snapshot = GenerationSnapshot(
                generation_id=organism.get("id", "unknown"),
                generation_number=organism.get("generation", 0),
                parent_id=organism.get("parent_id"),
                timestamp=organism.get("timestamp", "unknown"),
                code_size=len(organism.get("code", "")),
                consciousness_level=organism.get("consciousness_level", "LOW"),
                agent_decisions=organism.get("agent_decisions", []),
                mutation_type=organism.get("mutation_type", "unknown"),
                success=organism.get("success", False),
<<<<<<< HEAD
                notes=organism.get("notes", ""),
            )
            generations.append(snapshot)

=======
                notes=organism.get("notes", "")
            )
            generations.append(snapshot)
        
>>>>>>> origin/OS0.6.2.grok
        # Build lineage tree
        lineage_tree = {}
        for gen in generations:
            parent = gen.parent_id or "ROOT"
            if parent not in lineage_tree:
                lineage_tree[parent] = []
            lineage_tree[parent].append(gen.generation_id)
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        # Extract agent decisions per generation
        agent_decisions = {}
        for gen in generations:
            if gen.agent_decisions:
                agent_decisions[gen.generation_number] = gen.agent_decisions
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        # Build consciousness evolution timeline
        consciousness_evolution = [
            (gen.generation_number, gen.consciousness_level)
            for gen in sorted(generations, key=lambda g: g.generation_number)
        ]
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        # Create summary
        summary = PopulationSummary(
            population_id=population_id,
            created=data.get("created", "unknown"),
            total_generations=len(generations),
            total_organisms=len(generations),
            consciousness_trajectory=[level for _, level in consciousness_evolution],
            best_organism_id=self._find_best_organism(data),
            evolutionary_strategy=data.get("strategy", "unknown"),
<<<<<<< HEAD
            status=data.get("status", "active"),
        )

        return {
            "summary": summary,
            "generations": generations,
            "lineage_tree": lineage_tree,
            "agent_decisions": agent_decisions,
            "consciousness_evolution": consciousness_evolution,
        }

    def get_agent_perspectives(
        self, population_id: str, generation_num: int
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get agent perspectives for specific generation.

        Args:
            population_id: Population identifier
            generation_num: Generation number to review

=======
            status=data.get("status", "active")
        )
        
        return {
            'summary': summary,
            'generations': generations,
            'lineage_tree': lineage_tree,
            'agent_decisions': agent_decisions,
            'consciousness_evolution': consciousness_evolution,
        }
    
    def get_agent_perspectives(
        self,
        population_id: str,
        generation_num: int
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get agent perspectives for specific generation.
        
        Args:
            population_id: Population identifier
            generation_num: Generation number to review
        
>>>>>>> origin/OS0.6.2.grok
        Returns:
            {
                'agent_name': {
                    'recommendation': 'ADOPT|DEFER|REJECT',
                    'confidence': 0.85,
                    'reasoning': 'Why this decision was made',
                    'timestamp': '2025-10-11T15:00:00Z'
                },
                ...
            }
        """
        details = self.view_population(population_id)
<<<<<<< HEAD

        if generation_num not in details.get("agent_decisions", {}):
            logger.warning(f"⚠️ No agent decisions for generation {generation_num}")
            return {}

        decisions = details["agent_decisions"][generation_num]

        # Organize by agent
        perspectives = {}
        for decision in decisions:
            agent_name = decision.get("agent", "Unknown")
            perspectives[agent_name] = {
                "recommendation": decision.get("recommendation", "UNKNOWN"),
                "confidence": decision.get("confidence", 0.0),
                "reasoning": decision.get("reasoning", "No reasoning provided"),
                "timestamp": decision.get("timestamp", "unknown"),
            }

        return perspectives

=======
        
        if generation_num not in details.get('agent_decisions', {}):
            logger.warning(f"⚠️ No agent decisions for generation {generation_num}")
            return {}
        
        decisions = details['agent_decisions'][generation_num]
        
        # Organize by agent
        perspectives = {}
        for decision in decisions:
            agent_name = decision.get('agent', 'Unknown')
            perspectives[agent_name] = {
                'recommendation': decision.get('recommendation', 'UNKNOWN'),
                'confidence': decision.get('confidence', 0.0),
                'reasoning': decision.get('reasoning', 'No reasoning provided'),
                'timestamp': decision.get('timestamp', 'unknown')
            }
        
        return perspectives
    
>>>>>>> origin/OS0.6.2.grok
    def export_to_tachyonic(
        self,
        population_id: str,
        reason: str,
<<<<<<< HEAD
        category: str = "evolutionary_breakthroughs",
    ):
        """
        Archive interesting population to tachyonic for strategic reference.

=======
        category: str = "evolutionary_breakthroughs"
    ):
        """
        Archive interesting population to tachyonic for strategic reference.
        
>>>>>>> origin/OS0.6.2.grok
        Args:
            population_id: Population to archive
            reason: Why this population is significant
            category: Archive category (breakthroughs/experiments/failures)
        """
        pop_file = self.populations_dir / f"{population_id}.json"
<<<<<<< HEAD

        if not pop_file.exists():
            logger.error(f"❌ Population not found: {population_id}")
            return

        # Create archive directory
        archive_dir = self.tachyonic_dir / category
        archive_dir.mkdir(parents=True, exist_ok=True)

        # Copy population file with metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = archive_dir / f"{population_id}_{timestamp}.json"

        with open(pop_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Add archival metadata
        data["archive_metadata"] = {
            "archived_at": timestamp,
            "reason": reason,
            "category": category,
            "original_location": str(pop_file),
        }

        with open(archive_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"✅ Archived population to: {archive_file}")

    def _extract_consciousness_trajectory(self, data: Dict) -> List[str]:
        """Extract consciousness level progression"""
        organisms = sorted(
            data.get("organisms", []), key=lambda o: o.get("generation", 0)
        )
        return [o.get("consciousness_level", "LOW") for o in organisms]

    def _find_best_organism(self, data: Dict) -> str:
        """Find organism with highest consciousness level"""
        organisms = data.get("organisms", [])

        if not organisms:
            return "none"

        # Priority: HIGH > MEDIUM > LOW
        level_priority = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}

=======
        
        if not pop_file.exists():
            logger.error(f"❌ Population not found: {population_id}")
            return
        
        # Create archive directory
        archive_dir = self.tachyonic_dir / category
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy population file with metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = archive_dir / f"{population_id}_{timestamp}.json"
        
        with open(pop_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add archival metadata
        data['archive_metadata'] = {
            'archived_at': timestamp,
            'reason': reason,
            'category': category,
            'original_location': str(pop_file)
        }
        
        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"✅ Archived population to: {archive_file}")
    
    def _extract_consciousness_trajectory(self, data: Dict) -> List[str]:
        """Extract consciousness level progression"""
        organisms = sorted(
            data.get("organisms", []),
            key=lambda o: o.get("generation", 0)
        )
        return [o.get("consciousness_level", "LOW") for o in organisms]
    
    def _find_best_organism(self, data: Dict) -> str:
        """Find organism with highest consciousness level"""
        organisms = data.get("organisms", [])
        
        if not organisms:
            return "none"
        
        # Priority: HIGH > MEDIUM > LOW
        level_priority = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        
>>>>>>> origin/OS0.6.2.grok
        best = max(
            organisms,
            key=lambda o: (
                level_priority.get(o.get("consciousness_level", "LOW"), 0),
<<<<<<< HEAD
                o.get("generation", 0),
            ),
        )

        return best.get("id", "unknown")

    def print_population_report(self, population_id: str):
        """
        Print human-readable population report to console.

=======
                o.get("generation", 0)
            )
        )
        
        return best.get("id", "unknown")
    
    def print_population_report(self, population_id: str):
        """
        Print human-readable population report to console.
        
>>>>>>> origin/OS0.6.2.grok
        Args:
            population_id: Population to report on
        """
        details = self.view_population(population_id)
<<<<<<< HEAD

        if not details:
            print(f"\n❌ Population '{population_id}' not found\n")
            return

        summary = details["summary"]
        generations = details["generations"]

        print("\n" + "=" * 80)
        print(f"🧬 POPULATION REPORT: {population_id}")
        print("=" * 80)

=======
        
        if not details:
            print(f"\n❌ Population '{population_id}' not found\n")
            return
        
        summary = details['summary']
        generations = details['generations']
        
        print("\n" + "="*80)
        print(f"🧬 POPULATION REPORT: {population_id}")
        print("="*80)
        
>>>>>>> origin/OS0.6.2.grok
        print(f"\n📊 SUMMARY:")
        print(f"   Created: {summary.created}")
        print(f"   Total Generations: {summary.total_generations}")
        print(f"   Total Organisms: {summary.total_organisms}")
        print(f"   Evolutionary Strategy: {summary.evolutionary_strategy}")
        print(f"   Status: {summary.status}")
        print(f"   Best Organism: {summary.best_organism_id}")
<<<<<<< HEAD

        print(f"\n🧠 CONSCIOUSNESS TRAJECTORY:")
        trajectory = " → ".join(summary.consciousness_trajectory)
        print(f"   {trajectory}")

=======
        
        print(f"\n🧠 CONSCIOUSNESS TRAJECTORY:")
        trajectory = " → ".join(summary.consciousness_trajectory)
        print(f"   {trajectory}")
        
>>>>>>> origin/OS0.6.2.grok
        print(f"\n📈 GENERATION DETAILS:")
        for gen in sorted(generations, key=lambda g: g.generation_number):
            print(f"\n   Generation {gen.generation_number}:")
            print(f"      ID: {gen.generation_id}")
            print(f"      Consciousness: {gen.consciousness_level}")
            print(f"      Code Size: {gen.code_size} chars")
            print(f"      Mutation: {gen.mutation_type}")
            print(f"      Success: {'✅' if gen.success else '❌'}")
<<<<<<< HEAD

            if gen.agent_decisions:
                print(
                    f"      Agent Decisions: {len(gen.agent_decisions)} agents participated"
                )
                for decision in gen.agent_decisions:
                    agent = decision.get("agent", "Unknown")
                    rec = decision.get("recommendation", "UNKNOWN")
                    conf = decision.get("confidence", 0.0)
                    print(f"         {agent}: {rec} (confidence: {conf:.2f})")

        print("\n" + "=" * 80 + "\n")
=======
            
            if gen.agent_decisions:
                print(f"      Agent Decisions: {len(gen.agent_decisions)} agents participated")
                for decision in gen.agent_decisions:
                    agent = decision.get('agent', 'Unknown')
                    rec = decision.get('recommendation', 'UNKNOWN')
                    conf = decision.get('confidence', 0.0)
                    print(f"         {agent}: {rec} (confidence: {conf:.2f})")
        
        print("\n" + "="*80 + "\n")
>>>>>>> origin/OS0.6.2.grok


async def interactive_demo():
    """Interactive demonstration of population viewer"""
    print("\n🧬 AIOS POPULATION VIEWER - Interactive Demo\n")
<<<<<<< HEAD

    viewer = PopulationViewer()

    # Discover populations
    print("📊 Discovering populations...")
    populations = viewer.discover_populations()

=======
    
    viewer = PopulationViewer()
    
    # Discover populations
    print("📊 Discovering populations...")
    populations = viewer.discover_populations()
    
>>>>>>> origin/OS0.6.2.grok
    if not populations:
        print("❌ No populations found")
        print(f"   Expected location: {viewer.populations_dir}")
        print("   Create populations using PopulationManager from evolution components")
        return
<<<<<<< HEAD

    print(f"✅ Found {len(populations)} population(s)\n")

=======
    
    print(f"✅ Found {len(populations)} population(s)\n")
    
>>>>>>> origin/OS0.6.2.grok
    # Show summaries
    for i, pop in enumerate(populations, 1):
        print(f"{i}. {pop.population_id}")
        print(f"   Created: {pop.created}")
        print(f"   Generations: {pop.total_generations}")
        print(f"   Status: {pop.status}")
        print(f"   Trajectory: {' → '.join(pop.consciousness_trajectory[:5])}")
        if pop.total_generations > 5:
            print(f"               ... ({pop.total_generations - 5} more)")
        print()
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    # Detailed view of most recent
    if populations:
        latest = populations[0]
        print(f"\n📋 Detailed view of most recent population: {latest.population_id}\n")
        viewer.print_population_report(latest.population_id)


if __name__ == "__main__":
    # Run interactive demo
    asyncio.run(interactive_demo())
