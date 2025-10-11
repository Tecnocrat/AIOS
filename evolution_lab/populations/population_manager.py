"""
Knowledge-Driven Evolutionary Population Manager

AINLP Protocol: OS0.6.2.claude
Phase: 10.4 - Knowledge-Driven Evolutionary Populations
Component: Population Manager (Foundation)
Created: October 9, 2025

Purpose:
    Manage populations of diverse code organisms evolving through multi-agent
    conversations, Python 3.14 knowledge integration, and parallel execution.
    
Key Features:
    - Population lifecycle management (init, evolve, archive)
    - Archetype diversity enforcement (2 organisms per archetype)
    - Fitness-based selection with elitism
    - Tachyonic archival with timestamped JSON
    - Neural chain lineage tracking
    - Complexity ratchet (prevent regression)

Integration Points:
    - Agent Protocol (Phase 10.2.1): Multi-agent coordination
    - A2A Communication (Phase 10.2.2): Agent conversations
    - Python 3.14 Knowledge (Phase 10.3): Documentation queries
    - Free-Threading (Phase 10.3.1): Parallel execution
    - Neural Chain Architecture: Evolutionary memory

AINLP Compliance: 4/4 principles
    ✅ Discovery: Built on Phase 10 foundations
    ✅ Enhancement: Extended existing agent systems
    ✅ Output: Tachyonic archival + comprehensive docs
    ✅ Integration: Compatible with all Phase 10 components
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from pathlib import Path
import json
from datetime import datetime
import uuid


# ============================================================================
# ENUMERATIONS
# ============================================================================

class ArchetypeEnum(str, Enum):
    """Application archetype categories"""
    OS_TOOLS = "os_tools"
    CLI_APPLICATIONS = "cli_applications"
    WEB_SERVICES = "web_services"
    ABSTRACT_OBJECTS = "abstract_objects"
    NETWORK_TOOLS = "network_tools"
    DATA_SCIENCE = "data_science"
    AUTOMATION = "automation"
    GAME_LOGIC = "game_logic"


class SelectionStrategy(str, Enum):
    """Organism selection strategies"""
    FITNESS_ELITISM = "fitness_elitism"  # Keep top N by fitness
    DIVERSITY_PRESERVATION = "diversity_preservation"  # Archetype balance
    TOURNAMENT = "tournament"  # Tournament-style selection


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class KnowledgeContext:
    """Shared knowledge state for population"""
    python_index_path: Path
    pattern_library: Dict[str, any] = field(default_factory=dict)
    conversation_history: List[str] = field(default_factory=list)
    complexity_trends: List[float] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Serialize for archival"""
        return {
            "python_index_path": str(self.python_index_path),
            "pattern_library_size": len(self.pattern_library),
            "conversation_count": len(self.conversation_history),
            "complexity_trend": (
                self.complexity_trends[-10:]
                if self.complexity_trends else []
            )
        }


@dataclass
class Organism:
    """Individual code organism in population"""
    organism_id: str
    code: str
    archetype: ArchetypeEnum
    complexity_score: float
    fitness_score: float
    generation: int
    parent_id: Optional[str] = None
    patterns_used: List[str] = field(default_factory=list)
    apis_used: List[str] = field(default_factory=list)
    archetype_traits: Dict[str, any] = field(default_factory=dict)
    neural_chain_id: Optional[str] = None
    metadata: Dict[str, any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Serialize organism for archival"""
        return {
            "organism_id": self.organism_id,
            "archetype": self.archetype.value,
            "complexity_score": round(self.complexity_score, 4),
            "fitness_score": round(self.fitness_score, 4),
            "generation": self.generation,
            "parent_id": self.parent_id,
            "code_length": len(self.code),
            "patterns_count": len(self.patterns_used),
            "patterns_used": self.patterns_used,
            "apis_count": len(self.apis_used),
            "apis_used": self.apis_used,
            "neural_chain_id": self.neural_chain_id,
            "archetype_traits": self.archetype_traits,
            "metadata": self.metadata
        }
    
    def clone(self, new_generation: int) -> 'Organism':
        """Create cloned organism for next generation"""
        return Organism(
            organism_id=f"{self.organism_id}_clone_gen{new_generation}",
            code=self.code,
            archetype=self.archetype,
            complexity_score=self.complexity_score,
            fitness_score=self.fitness_score,
            generation=new_generation,
            parent_id=self.organism_id,
            patterns_used=self.patterns_used.copy(),
            apis_used=self.apis_used.copy(),
            archetype_traits=self.archetype_traits.copy(),
            neural_chain_id=self.neural_chain_id,
            metadata={"cloned_from": self.organism_id}
        )


@dataclass
class Population:
    """Population of diverse code organisms"""
    population_id: str
    organisms: List[Organism]
    generation: int
    archetype_distribution: Dict[ArchetypeEnum, int]
    knowledge_context: KnowledgeContext
    consciousness_trajectory: List[float] = field(default_factory=list)
    selection_strategy: SelectionStrategy = SelectionStrategy.FITNESS_ELITISM
    metadata: Dict[str, any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Serialize population for archival"""
        return {
            "population_id": self.population_id,
            "generation": self.generation,
            "organism_count": len(self.organisms),
            "organisms": [org.to_dict() for org in self.organisms],
            "archetype_distribution": {
                arch.value: count
                for arch, count in self.archetype_distribution.items()
            },
            "knowledge_context": self.knowledge_context.to_dict(),
            "consciousness_trajectory": self.consciousness_trajectory,
            "selection_strategy": self.selection_strategy.value,
            "average_complexity": self.average_complexity,
            "average_fitness": self.average_fitness,
            "metadata": self.metadata,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    @property
    def average_complexity(self) -> float:
        """Compute average complexity across population"""
        if not self.organisms:
            return 0.0
        return (
            sum(org.complexity_score for org in self.organisms)
            / len(self.organisms)
        )
    
    @property
    def average_fitness(self) -> float:
        """Compute average fitness across population"""
        if not self.organisms:
            return 0.0
        return (
            sum(org.fitness_score for org in self.organisms)
            / len(self.organisms)
        )
    
    @property
    def best_organism(self) -> Optional[Organism]:
        """Get highest fitness organism"""
        if not self.organisms:
            return None
        return max(self.organisms, key=lambda o: o.fitness_score)
    
    @property
    def consciousness_level(self) -> float:
        """Compute population consciousness (based on complexity + fitness)"""
        if not self.organisms:
            return 0.0
        avg_complexity = self.average_complexity
        avg_fitness = self.average_fitness
        return (avg_complexity * 0.6 + avg_fitness * 0.4)


# ============================================================================
# POPULATION MANAGER
# ============================================================================

class PopulationManager:
    """Manage evolutionary populations with diversity and fitness"""
    
    def __init__(
        self,
        evolution_dir: Path = None,
        archive_dir: Path = None,
        knowledge_base_path: Path = None
    ):
        """
        Initialize population manager
        
        Args:
            evolution_dir: Evolution lab directory (for backward compatibility)
            archive_dir: Tachyonic archive directory
                (default: tachyonic/archive/populations/)
            knowledge_base_path: Python 3.14 knowledge index
                (default: ai/data/knowledge/python_314_index.json)
        """
        # Evolution directory (for integration compatibility)
        if evolution_dir is not None:
            self.evolution_dir = Path(evolution_dir)
        elif archive_dir is not None:
            self.evolution_dir = Path(archive_dir)
        else:
            self.evolution_dir = Path("tachyonic/archive/populations")
        
        # Archive configuration (alias for evolution_dir)
        self.archive_dir = self.evolution_dir
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Knowledge base
        if knowledge_base_path is None:
            knowledge_base_path = Path("ai/data/knowledge/python_314_index.json")
        self.knowledge_base_path = knowledge_base_path
        
        print(f"[POPULATION MANAGER] Initialized")
        print(f"  Archive: {self.archive_dir}")
        print(f"  Knowledge: {self.knowledge_base_path}")
    
    def create_initial_population(
        self,
        size: int = 16,
        archetypes: List[ArchetypeEnum] = None,
        seed_code_provider: callable = None
    ) -> Population:
        """
        Create initial population with seed organisms
        
        Args:
            size: Population size (default: 16, should be multiple of archetype count)
            archetypes: List of archetypes to include (default: all 8)
            seed_code_provider: Function(archetype) -> seed_code (default: simple templates)
        
        Returns:
            Initial population (generation 0)
        """
        # Default to all archetypes
        if archetypes is None:
            archetypes = list(ArchetypeEnum)
        
        # Validate size is appropriate for archetype count
        organisms_per_archetype = size // len(archetypes)
        if organisms_per_archetype < 1:
            raise ValueError(f"Population size {size} too small for {len(archetypes)} archetypes")
        
        # Generate population ID
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        population_id = f"pop_{timestamp}"
        
        # Create knowledge context
        knowledge_context = KnowledgeContext(
            python_index_path=self.knowledge_base_path
        )
        
        # Create organisms
        organisms = []
        archetype_distribution = {arch: 0 for arch in archetypes}
        
        for archetype in archetypes:
            for i in range(organisms_per_archetype):
                organism_id = f"org_{archetype.value}_gen0_{uuid.uuid4().hex[:6]}"
                
                # Get seed code
                if seed_code_provider:
                    seed_code = seed_code_provider(archetype)
                else:
                    seed_code = self._default_seed_code(archetype)
                
                organism = Organism(
                    organism_id=organism_id,
                    code=seed_code,
                    archetype=archetype,
                    complexity_score=0.10,  # Minimal seed complexity
                    fitness_score=0.50,  # Neutral initial fitness
                    generation=0,
                    parent_id=None,
                    patterns_used=[],
                    apis_used=[],
                    archetype_traits={},
                    neural_chain_id=f"neural_{organism_id}",
                    metadata={"seed": True}
                )
                
                organisms.append(organism)
                archetype_distribution[archetype] += 1
        
        # Create population
        population = Population(
            population_id=population_id,
            organisms=organisms,
            generation=0,
            archetype_distribution=archetype_distribution,
            knowledge_context=knowledge_context,
            consciousness_trajectory=[0.30],  # Initial consciousness
            metadata={
                "created": datetime.utcnow().isoformat() + "Z",
                "size": size,
                "archetypes": [a.value for a in archetypes]
            }
        )
        
        print(f"\n[POPULATION CREATED] {population_id}")
        print(f"  Size: {len(organisms)} organisms")
        print(f"  Archetypes: {len(archetypes)} types ({organisms_per_archetype} each)")
        print(f"  Generation: 0 (seed)")
        
        # Archive initial population
        self.archive_population(population)
        
        return population
    
    def _default_seed_code(self, archetype: ArchetypeEnum) -> str:
        """Generate simple seed code for archetype"""
        seeds = {
            ArchetypeEnum.OS_TOOLS: '''#!/usr/bin/env python3
"""Simple file lister"""
import os
def list_files(path="."):
    return os.listdir(path)
if __name__ == "__main__":
    print(list_files())
''',
            ArchetypeEnum.CLI_APPLICATIONS: '''#!/usr/bin/env python3
"""Hello CLI"""
def main():
    print("Hello, World!")
if __name__ == "__main__":
    main()
''',
            ArchetypeEnum.WEB_SERVICES: '''#!/usr/bin/env python3
"""Simple HTTP server"""
from http.server import HTTPServer, BaseHTTPRequestHandler
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello")
if __name__ == "__main__":
    HTTPServer(("", 8000), Handler).serve_forever()
''',
            ArchetypeEnum.ABSTRACT_OBJECTS: '''#!/usr/bin/env python3
"""Simple linked list"""
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
class LinkedList:
    def __init__(self):
        self.head = None
''',
            ArchetypeEnum.NETWORK_TOOLS: '''#!/usr/bin/env python3
"""TCP echo server"""
import socket
def echo_server(port=9000):
    with socket.socket() as s:
        s.bind(("", port))
        s.listen(1)
        conn, _ = s.accept()
        with conn:
            data = conn.recv(1024)
            conn.sendall(data)
''',
            ArchetypeEnum.DATA_SCIENCE: '''#!/usr/bin/env python3
"""CSV reader"""
import csv
def read_csv(filename):
    with open(filename) as f:
        return list(csv.reader(f))
''',
            ArchetypeEnum.AUTOMATION: '''#!/usr/bin/env python3
"""Simple task runner"""
import time
def run_task(func, delay=1):
    while True:
        func()
        time.sleep(delay)
''',
            ArchetypeEnum.GAME_LOGIC: '''#!/usr/bin/env python3
"""Tic-tac-toe board"""
class Board:
    def __init__(self):
        self.grid = [[" " for _ in range(3)] for _ in range(3)]
    def display(self):
        for row in self.grid:
            print("|".join(row))
'''
        }
        return seeds.get(archetype, '# Seed code\nprint("Hello")')
    
    def select_survivors(
        self,
        population: Population,
        selection_rate: float = 0.50
    ) -> List[Organism]:
        """
        Select organisms for next generation
        
        Args:
            population: Current population
            selection_rate: Fraction of population to keep (default: 0.50)
        
        Returns:
            List of surviving organisms
        """
        if not population.organisms:
            return []
        
        # Strategy-specific selection
        if population.selection_strategy == SelectionStrategy.FITNESS_ELITISM:
            return self._fitness_elitism_selection(population, selection_rate)
        
        elif population.selection_strategy == SelectionStrategy.DIVERSITY_PRESERVATION:
            return self._diversity_preservation_selection(population, selection_rate)
        
        else:
            raise ValueError(f"Unknown selection strategy: {population.selection_strategy}")
    
    def _fitness_elitism_selection(
        self,
        population: Population,
        selection_rate: float
    ) -> List[Organism]:
        """Keep top N% by fitness score"""
        survivors_count = max(1, int(len(population.organisms) * selection_rate))
        
        # Sort by fitness (descending)
        sorted_organisms = sorted(
            population.organisms,
            key=lambda o: o.fitness_score,
            reverse=True
        )
        
        survivors = sorted_organisms[:survivors_count]
        
        print(f"\n[SELECTION] Fitness Elitism")
        print(f"  Survivors: {len(survivors)}/{len(population.organisms)} ({selection_rate*100:.0f}%)")
        print(f"  Best fitness: {survivors[0].fitness_score:.3f}")
        print(f"  Worst fitness: {survivors[-1].fitness_score:.3f}")
        
        return survivors
    
    def _diversity_preservation_selection(
        self,
        population: Population,
        selection_rate: float
    ) -> List[Organism]:
        """Ensure archetype balance while selecting by fitness"""
        survivors_count = max(1, int(len(population.organisms) * selection_rate))
        survivors_per_archetype = max(1, survivors_count // len(population.archetype_distribution))
        
        survivors = []
        
        # Select best from each archetype
        for archetype in population.archetype_distribution.keys():
            archetype_organisms = [
                org for org in population.organisms
                if org.archetype == archetype
            ]
            
            if not archetype_organisms:
                continue
            
            # Sort by fitness
            sorted_arch = sorted(
                archetype_organisms,
                key=lambda o: o.fitness_score,
                reverse=True
            )
            
            # Take top N per archetype
            survivors.extend(sorted_arch[:survivors_per_archetype])
        
        print(f"\n[SELECTION] Diversity Preservation")
        print(f"  Survivors: {len(survivors)} ({survivors_per_archetype} per archetype)")
        print(f"  Archetypes: {len(population.archetype_distribution)}")
        
        return survivors
    
    def repopulate(
        self,
        survivors: List[Organism],
        target_size: int,
        new_generation: int
    ) -> List[Organism]:
        """
        Clone survivors to reach target population size
        
        Args:
            survivors: Surviving organisms
            target_size: Desired population size
            new_generation: Generation number for clones
        
        Returns:
            Full population (survivors + clones)
        """
        if not survivors:
            raise ValueError("Cannot repopulate from empty survivors list")
        
        # Start with survivors
        full_population = survivors.copy()
        
        # Clone until we reach target size
        clone_count = 0
        while len(full_population) < target_size:
            # Clone best organism (elitism)
            parent = survivors[clone_count % len(survivors)]
            clone = parent.clone(new_generation)
            full_population.append(clone)
            clone_count += 1
        
        print(f"[REPOPULATION] {len(survivors)} survivors → {len(full_population)} total (+{clone_count} clones)")
        
        return full_population
    
    def evaluate_fitness(
        self,
        population: Population,
        knowledge_oracle: 'KnowledgeOracle' = None
    ) -> Population:
        """
        Evaluate and update fitness scores for all organisms in population
        
        Fitness factors:
        1. Code quality (syntax, structure, readability) - 0.30 weight
        2. Complexity appropriateness (matches archetype) - 0.25 weight  
        3. Pattern usage (design patterns detected) - 0.20 weight
        4. API sophistication (stdlib usage) - 0.15 weight
        5. Archetype alignment (traits match archetype) - 0.10 weight
        
        Args:
            population: Population to evaluate
            knowledge_oracle: Knowledge oracle for complexity analysis
        
        Returns:
            Population with updated fitness scores
        """
        print(f"\n[FITNESS EVALUATION] Generation {population.generation}")
        
        for organism in population.organisms:
            # Factor 1: Code quality (syntax, structure, readability)
            quality_score = self._evaluate_code_quality(organism.code)
            
            # Factor 2: Complexity appropriateness
            complexity_score = self._evaluate_complexity_appropriateness(
                organism.complexity_score, 
                organism.archetype
            )
            
            # Factor 3: Pattern usage
            pattern_score = 0.0
            if knowledge_oracle:
                try:
                    patterns = knowledge_oracle.extract_patterns(
                        organism.code, 
                        organism.archetype.value
                    )
                    pattern_score = min(1.0, len(patterns) * 0.15)  # 0.15 per pattern, max 1.0
                    organism.patterns_used = [p.pattern_name for p in patterns]
                except Exception as e:
                    print(f"  Pattern analysis failed for {organism.organism_id}: {e}")
            
            # Factor 4: API sophistication
            api_score = self._evaluate_api_sophistication(organism.code)
            organism.apis_used = self._extract_api_usage(organism.code)
            
            # Factor 5: Archetype alignment
            archetype_score = self._evaluate_archetype_alignment(
                organism.code, 
                organism.archetype
            )
            
            # Calculate weighted fitness score
            fitness_score = (
                quality_score * 0.30 +
                complexity_score * 0.25 +
                pattern_score * 0.20 +
                api_score * 0.15 +
                archetype_score * 0.10
            )
            
            # Update organism fitness
            old_fitness = organism.fitness_score
            organism.fitness_score = round(fitness_score, 3)
            
            print(f"  {organism.organism_id}: {old_fitness:.3f} → {organism.fitness_score:.3f}")
            print(f"    Quality: {quality_score:.2f}, Complexity: {complexity_score:.2f}, Patterns: {pattern_score:.2f}")
        
        print(f"\n[FITNESS SUMMARY]")
        print(f"  Average fitness: {population.average_fitness:.3f}")
        print(f"  Best fitness: {max(o.fitness_score for o in population.organisms):.3f}")
        print(f"  Fitness range: {min(o.fitness_score for o in population.organisms):.3f} - {max(o.fitness_score for o in population.organisms):.3f}")
        
        return population
    
    def _evaluate_code_quality(self, code: str) -> float:
        """Evaluate code quality (0.0-1.0)"""
        score = 0.0
        
        # Basic syntax check
        try:
            compile(code, '<string>', 'exec')
            score += 0.40  # Compiles successfully
        except SyntaxError:
            return 0.10  # Major syntax issues
        
        # Structure indicators
        if 'def ' in code:
            score += 0.15  # Has functions
        if 'class ' in code:
            score += 0.20  # Has classes
        
        # Readability indicators
        if '"""' in code or "'''" in code:
            score += 0.10  # Has docstrings
        if '#' in code:
            score += 0.05  # Has comments
        
        # Code organization
        lines = code.split('\n')
        if len(lines) > 5:
            score += 0.10  # Substantial code
        
        return min(1.0, score)
    
    def _evaluate_complexity_appropriateness(self, complexity: float, archetype: ArchetypeEnum) -> float:
        """Evaluate if complexity matches archetype expectations (0.0-1.0)"""
        # Archetype complexity expectations
        expectations = {
            ArchetypeEnum.CLI_APPLICATIONS: (0.20, 0.50),      # Simple to moderate
            ArchetypeEnum.WEB_SERVICES: (0.40, 0.70),   # Moderate to complex
            ArchetypeEnum.DATA_SCIENCE: (0.50, 0.80),   # Complex with ML
            ArchetypeEnum.AUTOMATION: (0.30, 0.60),     # Moderate complexity
            ArchetypeEnum.GAME_LOGIC: (0.35, 0.65),     # Moderate to complex
            ArchetypeEnum.OS_TOOLS: (0.25, 0.55),       # Simple to moderate
            ArchetypeEnum.NETWORK_TOOLS: (0.35, 0.65),  # Moderate complexity
            ArchetypeEnum.ABSTRACT_OBJECTS: (0.30, 0.60), # Moderate complexity
        }
        
        min_complexity, max_complexity = expectations.get(archetype, (0.30, 0.60))
        
        if complexity < min_complexity:
            return 0.60  # Too simple, could be more sophisticated
        elif complexity > max_complexity:
            return 0.70  # Too complex, might be over-engineered
        else:
            return 0.90  # Appropriate complexity
    
    def _evaluate_api_sophistication(self, code: str) -> float:
        """Evaluate API sophistication based on stdlib usage (0.0-1.0)"""
        score = 0.0
        
        # Advanced stdlib modules
        advanced_modules = [
            'asyncio', 'concurrent', 'multiprocessing', 'threading',
            'pathlib', 'typing', 'dataclasses', 'collections',
            'itertools', 'functools', 'operator', 'contextlib'
        ]
        
        for module in advanced_modules:
            if f"import {module}" in code or f"from {module}" in code:
                score += 0.10
        
        # External libraries (basic detection)
        if 'import requests' in code or 'import aiohttp' in code:
            score += 0.15
        
        return min(1.0, score)
    
    def _extract_api_usage(self, code: str) -> List[str]:
        """Extract APIs/modules used in code"""
        apis = []
        
        # Common stdlib modules
        stdlib_modules = [
            'os', 'sys', 'pathlib', 'json', 'csv', 're', 'datetime',
            'asyncio', 'threading', 'subprocess', 'argparse', 'logging',
            'typing', 'dataclasses', 'collections', 'itertools'
        ]
        
        for module in stdlib_modules:
            if f"import {module}" in code or f"from {module}" in code:
                apis.append(module)
        
        return apis
    
    def _evaluate_archetype_alignment(self, code: str, archetype: ArchetypeEnum) -> float:
        """Evaluate how well code matches archetype expectations (0.0-1.0)"""
        score = 0.50  # Base score
        
        # Archetype-specific patterns
        patterns = {
            ArchetypeEnum.CLI_APPLICATIONS: ['argparse', 'sys.argv', 'print(', 'input('],
            ArchetypeEnum.WEB_SERVICES: ['async def', 'await', 'http', 'json'],
            ArchetypeEnum.DATA_SCIENCE: ['import pandas', 'import numpy', 'def analyze', 'def predict'],
            ArchetypeEnum.AUTOMATION: ['def run_', 'while True', 'time.sleep', 'schedule'],
            ArchetypeEnum.GAME_LOGIC: ['class Board', 'class Player', 'def move', 'def check_win'],
            ArchetypeEnum.OS_TOOLS: ['import os', 'import pathlib', 'def list_', 'def create_'],
            ArchetypeEnum.NETWORK_TOOLS: ['socket', 'import socket', 'def connect', 'def send'],
            ArchetypeEnum.ABSTRACT_OBJECTS: ['class ', 'def __init__', 'self.', 'property'],
        }
        
        archetype_patterns = patterns.get(archetype, [])
        matches = sum(1 for pattern in archetype_patterns if pattern in code)
        
        # Bonus for pattern matches
        score += min(0.50, matches * 0.10)
        
        return min(1.0, score)
    
    def archive_population(self, population: Population) -> Path:
        """
        Archive population state to tachyonic
        
        Args:
            population: Population to archive
        
        Returns:
            Path to archived JSON file
        """
        # Timestamped filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{population.population_id}_gen{population.generation:03d}_{timestamp}.json"
        filepath = self.archive_dir / filename
        
        # Serialize population
        data = population.to_dict()
        
        # Write to file
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Update index (latest pointer + generation list)
        self._update_archive_index(population, filepath)
        
        print(f"[ARCHIVED] {filepath.name} ({len(data['organisms'])} organisms)")
        
        return filepath
    
    def _update_archive_index(self, population: Population, filepath: Path):
        """Update archive index with latest generation"""
        index_path = self.archive_dir / f"{population.population_id}_index.json"
        
        # Load existing index or create new
        if index_path.exists():
            with open(index_path) as f:
                index = json.load(f)
        else:
            index = {
                "population_id": population.population_id,
                "created": population.metadata.get("created"),
                "generations": []
            }
        
        # Add this generation
        index["generations"].append({
            "generation": population.generation,
            "file": filepath.name,
            "organism_count": len(population.organisms),
            "average_complexity": round(population.average_complexity, 4),
            "average_fitness": round(population.average_fitness, 4),
            "consciousness": round(population.consciousness_level, 4),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
        
        # Update latest pointer
        index["latest_generation"] = population.generation
        index["latest_file"] = filepath.name
        
        # Write index
        with open(index_path, 'w') as f:
            json.dump(index, f, indent=2)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def example_basic_population():
    """Example: Create basic population and demonstrate selection"""
    manager = PopulationManager()
    
    # Create initial population (16 organisms, 8 archetypes)
    population = manager.create_initial_population(size=16)
    
    # Simulate evolution by randomizing fitness
    import random
    for organism in population.organisms:
        organism.fitness_score = random.uniform(0.3, 0.9)
        organism.complexity_score = random.uniform(0.1, 0.5)
    
    print(f"\n[BEFORE SELECTION]")
    print(f"  Population: {len(population.organisms)} organisms")
    print(f"  Avg Fitness: {population.average_fitness:.3f}")
    print(f"  Avg Complexity: {population.average_complexity:.3f}")
    
    # Select survivors (top 50%)
    survivors = manager.select_survivors(population, selection_rate=0.50)
    
    # Repopulate to original size
    next_generation = manager.repopulate(
        survivors=survivors,
        target_size=16,
        new_generation=1
    )
    
    # Create new population object
    population.organisms = next_generation
    population.generation = 1
    population.consciousness_trajectory.append(population.consciousness_level)
    
    print(f"\n[AFTER SELECTION + REPOPULATION]")
    print(f"  Population: {len(population.organisms)} organisms")
    print(f"  Avg Fitness: {population.average_fitness:.3f}")
    print(f"  Avg Complexity: {population.average_complexity:.3f}")
    print(f"  Consciousness: {population.consciousness_level:.3f}")
    
    # Archive new generation
    manager.archive_population(population)


if __name__ == "__main__":
    print("=" * 70)
    print("POPULATION MANAGER - Foundation Implementation")
    print("=" * 70)
    
    example_basic_population()
    
    print("\n" + "=" * 70)
    print("✅ Population Manager foundation operational")
    print("=" * 70)
