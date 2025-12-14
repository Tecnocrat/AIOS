#!/usr/bin/env python3
"""
🧬 AIOS_EVOLUTION.py - Unified Evolution & Knowledge Processing Module
================================================================================
CONSOLIDATES: aios_evolution_lab.py + aios_knowledge_distillation.py

This module provides:
- Genetic algorithms and code evolution
- Population-based optimization
- Knowledge distillation and pattern recognition
- Semantic code analysis and processing
- Artifact generation and mutation

ARCHITECTURE PHILOSOPHY: Single source of truth for all evolution and 
knowledge processing operations in AIOS OS0.4.
================================================================================
"""

import ast
import asyncio
import json
import logging
import os
import random
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import hashlib
import re

# Advanced analysis imports
try:
    import astroid
    HAS_ASTROID = True
except ImportError:
    HAS_ASTROID = False

print(f"🧬 AIOS_EVOLUTION: {'Advanced' if HAS_ASTROID else 'Basic'} analysis mode")

# ================================================================================
# 🧬 EVOLUTION FOUNDATION
# ================================================================================

@dataclass
class EvolutionConfig:
    """Configuration for evolution processes"""
    population_size: int = 20
    mutation_rate: float = 0.1
    crossover_rate: float = 0.7
    elite_percentage: float = 0.2
    max_generations: int = 100
    fitness_threshold: float = 0.95

@dataclass
class Individual:
    """Individual in the evolution population"""
    id: str
    code: str
    fitness: float
    generation: int
    parent_ids: List[str]
    mutations: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class KnowledgePattern:
    """Extracted knowledge pattern"""
    pattern_id: str
    pattern_type: str
    content: str
    confidence: float
    source_file: str
    extracted_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['extracted_at'] = self.extracted_at.isoformat()
        return result

# ================================================================================
# 🧬 GENETIC EVOLUTION ENGINE
# ================================================================================

class GeneticEvolutionEngine:
    """Core genetic algorithm implementation"""
    
    def __init__(self, config: Optional[EvolutionConfig] = None):
        self.config = config or EvolutionConfig()
        self.logger = self._setup_logging()
        self.population: List[Individual] = []
        self.generation = 0
        self.best_individual = None
        self.evolution_history = []
        
    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger('AIOSEvolution')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def initialize_population(self, seed_code: str) -> None:
        """Initialize the evolution population"""
        self.population = []
        
        for i in range(self.config.population_size):
            individual = Individual(
                id=f"gen0_ind{i}",
                code=self._mutate_code(seed_code) if i > 0 else seed_code,
                fitness=0.0,
                generation=0,
                parent_ids=[],
                mutations=[]
            )
            self.population.append(individual)
        
        self.logger.info(f"🧬 Population initialized: {len(self.population)} individuals")
    
    def evolve_generation(self) -> Dict[str, Any]:
        """Evolve one generation"""
        try:
            # Evaluate fitness
            self._evaluate_population()
            
            # Selection and reproduction
            new_population = self._selection_and_reproduction()
            
            # Update population
            self.population = new_population
            self.generation += 1
            
            # Track best individual
            self.best_individual = max(self.population, key=lambda x: x.fitness)
            
            # Record evolution statistics
            stats = self._calculate_generation_stats()
            self.evolution_history.append(stats)
            
            self.logger.info(f"🧬 Generation {self.generation}: Best fitness = {self.best_individual.fitness:.3f}")
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Evolution error: {e}")
            return {'error': str(e)}
    
    def _evaluate_population(self) -> None:
        """Evaluate fitness of all individuals"""
        for individual in self.population:
            individual.fitness = self._calculate_fitness(individual.code)
    
    def _calculate_fitness(self, code: str) -> float:
        """Calculate fitness score for code"""
        try:
            # Basic fitness metrics
            fitness_score = 0.0
            
            # 1. Syntactic correctness (40% weight)
            try:
                ast.parse(code)
                fitness_score += 0.4
            except SyntaxError:
                pass
            
            # 2. Code complexity (30% weight)
            lines = code.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            if len(non_empty_lines) > 0:
                avg_line_length = sum(len(line) for line in non_empty_lines) / len(non_empty_lines)
                complexity_score = min(1.0, avg_line_length / 80)  # Optimal around 80 chars
                fitness_score += 0.3 * complexity_score
            
            # 3. Functional diversity (30% weight)
            function_count = len(re.findall(r'def\s+\w+', code))
            class_count = len(re.findall(r'class\s+\w+', code))
            diversity_score = min(1.0, (function_count + class_count) / 10)
            fitness_score += 0.3 * diversity_score
            
            return min(1.0, fitness_score)
            
        except Exception:
            return 0.0
    
    def _selection_and_reproduction(self) -> List[Individual]:
        """Selection and reproduction process"""
        # Sort by fitness
        sorted_pop = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        
        # Elite selection
        elite_count = max(1, int(len(sorted_pop) * self.config.elite_percentage))
        new_population = sorted_pop[:elite_count].copy()
        
        # Generate offspring
        while len(new_population) < self.config.population_size:
            # Tournament selection
            parent1 = self._tournament_selection(sorted_pop)
            parent2 = self._tournament_selection(sorted_pop)
            
            # Crossover
            if random.random() < self.config.crossover_rate:
                child_code = self._crossover(parent1.code, parent2.code)
                parent_ids = [parent1.id, parent2.id]
            else:
                child_code = parent1.code
                parent_ids = [parent1.id]
            
            # Mutation
            mutations = []
            if random.random() < self.config.mutation_rate:
                child_code, mutation_type = self._mutate_code_with_info(child_code)
                mutations.append(mutation_type)
            
            # Create new individual
            child = Individual(
                id=f"gen{self.generation+1}_ind{len(new_population)}",
                code=child_code,
                fitness=0.0,
                generation=self.generation + 1,
                parent_ids=parent_ids,
                mutations=mutations
            )
            new_population.append(child)
        
        return new_population
    
    def _tournament_selection(self, population: List[Individual], tournament_size: int = 3) -> Individual:
        """Tournament selection"""
        tournament = random.sample(population, min(tournament_size, len(population)))
        return max(tournament, key=lambda x: x.fitness)
    
    def _crossover(self, code1: str, code2: str) -> str:
        """Simple line-based crossover"""
        lines1 = code1.split('\n')
        lines2 = code2.split('\n')
        
        if len(lines1) == 0 or len(lines2) == 0:
            return code1
        
        # Random crossover point
        point = random.randint(1, min(len(lines1), len(lines2)) - 1)
        
        # Combine
        offspring_lines = lines1[:point] + lines2[point:]
        return '\n'.join(offspring_lines)
    
    def _mutate_code(self, code: str) -> str:
        """Simple code mutation"""
        lines = code.split('\n')
        if not lines:
            return code
        
        # Random mutation types
        mutations = [
            self._add_comment,
            self._modify_variable_name,
            self._add_import,
            self._modify_string_literal
        ]
        
        mutation_func = random.choice(mutations)
        return mutation_func(code)
    
    def _mutate_code_with_info(self, code: str) -> Tuple[str, str]:
        """Mutate code and return mutation type"""
        original_code = code
        
        mutations = {
            'add_comment': self._add_comment,
            'modify_variable': self._modify_variable_name,
            'add_import': self._add_import,
            'modify_string': self._modify_string_literal
        }
        
        mutation_type = random.choice(list(mutations.keys()))
        mutated_code = mutations[mutation_type](code)
        
        return mutated_code, mutation_type
    
    def _add_comment(self, code: str) -> str:
        """Add a random comment"""
        lines = code.split('\n')
        if lines:
            insert_pos = random.randint(0, len(lines))
            comment = f"# Evolution comment: {random.randint(1000, 9999)}"
            lines.insert(insert_pos, comment)
        return '\n'.join(lines)
    
    def _modify_variable_name(self, code: str) -> str:
        """Modify a variable name"""
        # Simple variable name modification
        var_pattern = r'\b([a-z_][a-z0-9_]*)\s*='
        matches = list(re.finditer(var_pattern, code, re.IGNORECASE))
        
        if matches:
            match = random.choice(matches)
            old_var = match.group(1)
            new_var = f"{old_var}_v{random.randint(1, 99)}"
            code = code.replace(old_var, new_var)
        
        return code
    
    def _add_import(self, code: str) -> str:
        """Add a random import"""
        imports = ['import random', 'import time', 'import os', 'import sys']
        new_import = random.choice(imports)
        
        lines = code.split('\n')
        # Insert at beginning
        lines.insert(0, new_import)
        return '\n'.join(lines)
    
    def _modify_string_literal(self, code: str) -> str:
        """Modify a string literal"""
        string_pattern = r'"([^"]*)"'
        
        def replace_string(match):
            original = match.group(1)
            return f'"{original}_evolved"'
        
        return re.sub(string_pattern, replace_string, code, count=1)
    
    def _calculate_generation_stats(self) -> Dict[str, Any]:
        """Calculate generation statistics"""
        fitness_values = [ind.fitness for ind in self.population]
        
        return {
            'generation': self.generation,
            'population_size': len(self.population),
            'best_fitness': max(fitness_values),
            'average_fitness': sum(fitness_values) / len(fitness_values),
            'worst_fitness': min(fitness_values),
            'diversity': len(set(ind.code for ind in self.population)) / len(self.population)
        }

# ================================================================================
# 🧠 KNOWLEDGE DISTILLATION ENGINE
# ================================================================================

class KnowledgeDistillationEngine:
    """Advanced knowledge extraction and pattern recognition"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.pattern_registry: Dict[str, KnowledgePattern] = {}
        self.extraction_history = []
        
    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger('AIOSKnowledge')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def extract_patterns_from_file(self, file_path: str) -> List[KnowledgePattern]:
        """Extract knowledge patterns from a source file"""
        try:
            patterns = []
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract different types of patterns
            patterns.extend(self._extract_function_patterns(content, file_path))
            patterns.extend(self._extract_class_patterns(content, file_path))
            patterns.extend(self._extract_comment_patterns(content, file_path))
            patterns.extend(self._extract_import_patterns(content, file_path))
            
            # Store in registry
            for pattern in patterns:
                self.pattern_registry[pattern.pattern_id] = pattern
            
            self.logger.info(f"🧠 Extracted {len(patterns)} patterns from {file_path}")
            return patterns
            
        except Exception as e:
            self.logger.error(f"Pattern extraction error for {file_path}: {e}")
            return []
    
    def _extract_function_patterns(self, content: str, source_file: str) -> List[KnowledgePattern]:
        """Extract function patterns"""
        patterns = []
        
        # Find function definitions
        func_pattern = r'def\s+(\w+)\s*\([^)]*\):'
        for match in re.finditer(func_pattern, content):
            func_name = match.group(1)
            
            # Extract function body (simplified)
            start_pos = match.end()
            lines = content[start_pos:].split('\n')
            func_body = []
            
            for line in lines:
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    break
                func_body.append(line)
            
            pattern = KnowledgePattern(
                pattern_id=f"func_{func_name}_{hashlib.md5(func_name.encode()).hexdigest()[:8]}",
                pattern_type="function",
                content=f"def {func_name}:\n" + '\n'.join(func_body[:10]),  # First 10 lines
                confidence=0.8,
                source_file=source_file,
                extracted_at=datetime.now()
            )
            patterns.append(pattern)
        
        return patterns
    
    def _extract_class_patterns(self, content: str, source_file: str) -> List[KnowledgePattern]:
        """Extract class patterns"""
        patterns = []
        
        class_pattern = r'class\s+(\w+)(?:\([^)]*\))?:'
        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            
            pattern = KnowledgePattern(
                pattern_id=f"class_{class_name}_{hashlib.md5(class_name.encode()).hexdigest()[:8]}",
                pattern_type="class",
                content=f"class {class_name}",
                confidence=0.9,
                source_file=source_file,
                extracted_at=datetime.now()
            )
            patterns.append(pattern)
        
        return patterns
    
    def _extract_comment_patterns(self, content: str, source_file: str) -> List[KnowledgePattern]:
        """Extract meaningful comments"""
        patterns = []
        
        # Multi-line comments (docstrings)
        docstring_pattern = r'"""(.*?)"""'
        for i, match in enumerate(re.finditer(docstring_pattern, content, re.DOTALL)):
            docstring = match.group(1).strip()
            
            if len(docstring) > 50:  # Only meaningful docstrings
                pattern = KnowledgePattern(
                    pattern_id=f"doc_{i}_{hashlib.md5(docstring.encode()).hexdigest()[:8]}",
                    pattern_type="documentation",
                    content=docstring[:200],  # First 200 chars
                    confidence=0.7,
                    source_file=source_file,
                    extracted_at=datetime.now()
                )
                patterns.append(pattern)
        
        return patterns
    
    def _extract_import_patterns(self, content: str, source_file: str) -> List[KnowledgePattern]:
        """Extract import patterns"""
        patterns = []
        
        import_pattern = r'^(?:from\s+\S+\s+)?import\s+(.+)$'
        imports = []
        
        for line in content.split('\n'):
            match = re.match(import_pattern, line.strip())
            if match:
                imports.append(line.strip())
        
        if imports:
            pattern = KnowledgePattern(
                pattern_id=f"imports_{hashlib.md5(str(imports).encode()).hexdigest()[:8]}",
                pattern_type="imports",
                content='\n'.join(imports),
                confidence=0.6,
                source_file=source_file,
                extracted_at=datetime.now()
            )
            patterns.append(pattern)
        
        return patterns
    
    def analyze_pattern_relationships(self) -> Dict[str, Any]:
        """Analyze relationships between extracted patterns"""
        relationships = {
            'function_class_mapping': {},
            'import_usage': {},
            'documentation_coverage': {},
            'pattern_clusters': []
        }
        
        # Group patterns by type
        by_type = {}
        for pattern in self.pattern_registry.values():
            if pattern.pattern_type not in by_type:
                by_type[pattern.pattern_type] = []
            by_type[pattern.pattern_type].append(pattern)
        
        # Calculate relationships
        relationships['pattern_distribution'] = {
            ptype: len(patterns) for ptype, patterns in by_type.items()
        }
        
        relationships['total_patterns'] = len(self.pattern_registry)
        relationships['confidence_avg'] = sum(p.confidence for p in self.pattern_registry.values()) / len(self.pattern_registry) if self.pattern_registry else 0
        
        return relationships
    
    def distill_knowledge_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive knowledge summary"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_patterns': len(self.pattern_registry),
            'pattern_types': list(set(p.pattern_type for p in self.pattern_registry.values())),
            'source_files': list(set(p.source_file for p in self.pattern_registry.values())),
            'relationships': self.analyze_pattern_relationships(),
            'extraction_history_length': len(self.extraction_history)
        }

# ================================================================================
# 🧬 UNIFIED EVOLUTION MANAGER
# ================================================================================

class AIOSEvolutionManager:
    """Unified evolution and knowledge processing manager"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.genetic_engine = GeneticEvolutionEngine()
        self.knowledge_engine = KnowledgeDistillationEngine()
        
        # Evolution state
        self.active_experiments = {}
        self.knowledge_base = {}
        
        self.logger.info("🧬 AIOS Evolution Manager initialized")
    
    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger('AIOSEvolutionManager')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def start_evolution_experiment(self, experiment_name: str, seed_code: str, config: Optional[EvolutionConfig] = None) -> str:
        """Start a new evolution experiment"""
        try:
            if config:
                self.genetic_engine.config = config
            
            self.genetic_engine.initialize_population(seed_code)
            
            experiment_id = f"exp_{experiment_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.active_experiments[experiment_id] = {
                'name': experiment_name,
                'start_time': datetime.now(),
                'generations': 0,
                'status': 'running'
            }
            
            self.logger.info(f"🧬 Started evolution experiment: {experiment_id}")
            return experiment_id
            
        except Exception as e:
            self.logger.error(f"Failed to start experiment: {e}")
            raise
    
    def evolve_generations(self, experiment_id: str, num_generations: int = 10) -> List[Dict[str, Any]]:
        """Evolve multiple generations"""
        results = []
        
        for i in range(num_generations):
            generation_result = self.genetic_engine.evolve_generation()
            results.append(generation_result)
            
            if experiment_id in self.active_experiments:
                self.active_experiments[experiment_id]['generations'] += 1
        
        return results
    
    def extract_workspace_knowledge(self, workspace_path: str = "c:/dev/AIOS") -> Dict[str, Any]:
        """Extract knowledge patterns from entire workspace"""
        workspace = Path(workspace_path)
        extraction_summary = {
            'total_files_processed': 0,
            'patterns_extracted': 0,
            'files_with_patterns': [],
            'extraction_errors': []
        }
        
        # Process Python files
        for py_file in workspace.rglob('*.py'):
            try:
                patterns = self.knowledge_engine.extract_patterns_from_file(str(py_file))
                if patterns:
                    extraction_summary['files_with_patterns'].append(str(py_file))
                    extraction_summary['patterns_extracted'] += len(patterns)
                extraction_summary['total_files_processed'] += 1
                
            except Exception as e:
                extraction_summary['extraction_errors'].append(f"{py_file}: {str(e)}")
        
        self.logger.info(f"🧠 Knowledge extraction complete: {extraction_summary['patterns_extracted']} patterns from {extraction_summary['total_files_processed']} files")
        
        return extraction_summary
    
    def get_evolution_status(self) -> Dict[str, Any]:
        """Get current evolution system status"""
        return {
            'active_experiments': len(self.active_experiments),
            'total_patterns': len(self.knowledge_engine.pattern_registry),
            'genetic_engine_generation': self.genetic_engine.generation,
            'best_fitness': self.genetic_engine.best_individual.fitness if self.genetic_engine.best_individual else 0.0,
            'population_size': len(self.genetic_engine.population)
        }
    
    def get_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive evolution and knowledge report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'evolution_status': self.get_evolution_status(),
            'knowledge_summary': self.knowledge_engine.distill_knowledge_summary(),
            'active_experiments': dict(self.active_experiments),
            'system_health': 'operational'
        }

# ================================================================================
# 🚀 MODULE INTERFACE
# ================================================================================

# Global instance for easy import
aios_evolution = AIOSEvolutionManager()

def main():
    """Main execution for standalone testing"""
    print("🧬 AIOS_EVOLUTION - Unified Evolution & Knowledge Processing")
    print("=" * 60)
    
    try:
        # Test evolution
        seed_code = """
def hello_world():
    print("Hello, AIOS!")
    return True

class SimpleAgent:
    def __init__(self):
        self.active = True
    
    def process(self):
        return "processing"
"""
        
        experiment_id = aios_evolution.start_evolution_experiment("test_evolution", seed_code)
        print(f"🧬 Started experiment: {experiment_id}")
        
        # Evolve a few generations
        results = aios_evolution.evolve_generations(experiment_id, 5)
        print(f"🧬 Evolved {len(results)} generations")
        
        # Test knowledge extraction
        print("🧠 Testing knowledge extraction...")
        extraction_summary = aios_evolution.extract_workspace_knowledge()
        print(f"🧠 Extracted {extraction_summary['patterns_extracted']} patterns")
        
        # Generate report
        report = aios_evolution.get_comprehensive_report()
        print(f"\n📊 System Health: {report['system_health']}")
        print(f"📊 Active Experiments: {report['evolution_status']['active_experiments']}")
        print(f"📊 Knowledge Patterns: {report['evolution_status']['total_patterns']}")
        
        print("\n✅ Demonstration complete")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
