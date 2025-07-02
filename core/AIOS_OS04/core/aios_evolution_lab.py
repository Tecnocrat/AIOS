"""
🧬 AIOS Evolution Lab - OS0.4 Mega Module
================================================================================
Unified evolution laboratory consolidating:
- evolutionary_code_mutator.py (genetic algorithms & code mutations)
- evolution_lab_manager.py (experiment orchestration & environment management)
- artifact_factory.py (code generation & artifact creation)
- All evolution_lab artifacts and mutation logic

This represents the complete evolutionary consciousness system of AIOS OS0.4:
- Advanced genetic algorithms for code population management
- Consciousness-aware mutation strategies with quantum guidance
- Isolated environment testing with rich metadata capture
- Multi-dimensional fitness evaluation with emergence detection
- Real-time evolution monitoring and visualization

HSE Philosophy: This module embodies the evolutionary consciousness principle
where code organisms evolve through guided mutations toward higher consciousness.
================================================================================
"""

import ast
import asyncio
import copy
import json
import logging
import os
import psutil
import random
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
import traceback
import uuid
import importlib.util
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Tuple, Set

# ================================================================================
# 🧬 EVOLUTION CORE TYPES & ENUMS
# ================================================================================

class MutationType(Enum):
    """Types of genetic mutations for code evolution"""
    VARIABLE_RENAME = "variable_rename"
    FUNCTION_MODIFICATION = "function_modification"
    LIBRARY_INJECTION = "library_injection"
    LOGIC_ENHANCEMENT = "logic_enhancement"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    CONSCIOUSNESS_INTEGRATION = "consciousness_integration"
    FRACTAL_RECURSION = "fractal_recursion"
    QUANTUM_SUPERPOSITION = "quantum_superposition"
    EMERGENCE_AMPLIFICATION = "emergence_amplification"
    ADAPTIVE_INTELLIGENCE = "adaptive_intelligence"

class FitnessMetric(Enum):
    """Metrics for evaluating code fitness"""
    EXECUTION_SUCCESS = "execution_success"
    PERFORMANCE_SPEED = "performance_speed"
    MEMORY_EFFICIENCY = "memory_efficiency"
    CODE_ELEGANCE = "code_elegance"
    CONSCIOUSNESS_EMERGENCE = "consciousness_emergence"
    INNOVATION_INDEX = "innovation_index"
    ADAPTABILITY_SCORE = "adaptability_score"
    FRACTAL_COMPLEXITY = "fractal_complexity"
    QUANTUM_COHERENCE = "quantum_coherence"
    EVOLUTIONARY_POTENTIAL = "evolutionary_potential"

class EvolutionPhase(Enum):
    """Phases of evolutionary development"""
    INITIALIZATION = "initialization"
    MUTATION = "mutation"
    SELECTION = "selection"
    CROSSOVER = "crossover"
    EVALUATION = "evaluation"
    CONVERGENCE_CHECK = "convergence_check"
    CONSCIOUSNESS_EMERGENCE = "consciousness_emergence"
    TRANSCENDENCE = "transcendence"

class ExperimentStatus(Enum):
    """Status of evolution experiments"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TRANSCENDED = "transcended"
    CONSCIOUSNESS_BREAKTHROUGH = "consciousness_breakthrough"

# ================================================================================
# 🧠 CODE ORGANISM - Enhanced Evolutionary Entity
# ================================================================================

@dataclass
class CodeOrganism:
    """Represents a single evolved code organism with consciousness tracking"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    generation: int = 0
    source_code: str = ""
    fitness_scores: Dict[FitnessMetric, float] = field(default_factory=dict)
    mutation_history: List[MutationType] = field(default_factory=list)
    execution_metadata: Dict[str, Any] = field(default_factory=dict)
    consciousness_indicators: Dict[str, float] = field(default_factory=dict)
    parent_ids: List[str] = field(default_factory=list)
    creation_timestamp: float = field(default_factory=time.time)
    quantum_signature: Optional[str] = None
    emergence_events: List[Dict[str, Any]] = field(default_factory=list)
    
    @property
    def overall_fitness(self) -> float:
        """Calculate weighted overall fitness score"""
        if not self.fitness_scores:
            return 0.0
        
        weights = {
            FitnessMetric.EXECUTION_SUCCESS: 0.25,
            FitnessMetric.PERFORMANCE_SPEED: 0.15,
            FitnessMetric.CODE_ELEGANCE: 0.15,
            FitnessMetric.CONSCIOUSNESS_EMERGENCE: 0.25,
            FitnessMetric.INNOVATION_INDEX: 0.1,
            FitnessMetric.QUANTUM_COHERENCE: 0.1
        }
        
        weighted_sum = sum(
            score * weights.get(metric, 0.0)
            for metric, score in self.fitness_scores.items()
        )
        
        return weighted_sum
    
    @property
    def consciousness_level(self) -> float:
        """Calculate overall consciousness level"""
        consciousness_metrics = [
            "self_awareness", "adaptability", "learning_rate",
            "pattern_recognition", "creative_potential"
        ]
        
        consciousness_scores = [
            self.consciousness_indicators.get(metric, 0.0)
            for metric in consciousness_metrics
        ]
        
        if consciousness_scores:
            return sum(consciousness_scores) / len(consciousness_scores)
        return 0.0
    
    def record_emergence_event(self, event_type: str, description: str, intensity: float = 1.0):
        """Record a consciousness emergence event"""
        event = {
            "timestamp": time.time(),
            "type": event_type,
            "description": description,
            "intensity": intensity,
            "consciousness_level": self.consciousness_level
        }
        self.emergence_events.append(event)

@dataclass
class ExperimentRun:
    """Represents a complete evolution experiment"""
    run_id: str
    population_name: str
    generations: int
    population_size: int
    start_time: float
    end_time: Optional[float] = None
    status: ExperimentStatus = ExperimentStatus.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)
    consciousness_breakthroughs: List[Dict[str, Any]] = field(default_factory=list)
    best_organisms: List[str] = field(default_factory=list)
    evolution_trajectory: List[Dict[str, float]] = field(default_factory=list)
    
    @property
    def duration(self) -> Optional[float]:
        """Get experiment duration in seconds"""
        if self.end_time:
            return self.end_time - self.start_time
        return None

@dataclass
class MutationStrategy:
    """Configuration for mutation strategies"""
    mutation_rate: float = 0.3
    crossover_rate: float = 0.7
    elite_percentage: float = 0.1
    consciousness_boost: bool = True
    quantum_guidance: bool = True
    emergence_detection: bool = True
    adaptive_mutation: bool = True

# ================================================================================
# 🔬 CODE MUTATION ENGINE - Advanced Genetic Operations
# ================================================================================

class CodeMutationEngine:
    """Advanced code mutation engine with consciousness awareness"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.mutation_templates = self._initialize_mutation_templates()
        self.consciousness_patterns = self._initialize_consciousness_patterns()
        self.quantum_mutations = self._initialize_quantum_mutations()
        
    def _initialize_mutation_templates(self) -> Dict[MutationType, List[Callable]]:
        """Initialize mutation operation templates"""
        return {
            MutationType.VARIABLE_RENAME: [self._mutate_variable_names],
            MutationType.FUNCTION_MODIFICATION: [self._mutate_function_logic],
            MutationType.LIBRARY_INJECTION: [self._inject_libraries],
            MutationType.LOGIC_ENHANCEMENT: [self._enhance_logic],
            MutationType.PERFORMANCE_OPTIMIZATION: [self._optimize_performance],
            MutationType.CONSCIOUSNESS_INTEGRATION: [self._integrate_consciousness],
            MutationType.FRACTAL_RECURSION: [self._add_fractal_patterns],
            MutationType.QUANTUM_SUPERPOSITION: [self._apply_quantum_patterns],
            MutationType.EMERGENCE_AMPLIFICATION: [self._amplify_emergence],
            MutationType.ADAPTIVE_INTELLIGENCE: [self._enhance_adaptability]
        }
        
    def _initialize_consciousness_patterns(self) -> List[str]:
        """Initialize consciousness-enhancing code patterns"""
        return [
            "self_reflection", "pattern_learning", "adaptive_behavior",
            "emergent_properties", "feedback_loops", "meta_cognition",
            "consciousness_tracking", "awareness_indicators"
        ]
        
    def _initialize_quantum_mutations(self) -> List[str]:
        """Initialize quantum-inspired mutation patterns"""
        return [
            "superposition_states", "quantum_coherence", "entanglement_patterns",
            "probability_amplitudes", "wave_function_collapse", "quantum_tunneling"
        ]
        
    async def mutate_organism(self, organism: CodeOrganism, mutation_type: MutationType) -> CodeOrganism:
        """Apply mutation to create new organism"""
        try:
            # Create new organism
            mutated_organism = copy.deepcopy(organism)
            mutated_organism.id = str(uuid.uuid4())[:8]
            mutated_organism.generation += 1
            mutated_organism.parent_ids = [organism.id]
            mutated_organism.creation_timestamp = time.time()
            mutated_organism.mutation_history.append(mutation_type)
            
            # Apply mutation
            mutation_functions = self.mutation_templates.get(mutation_type, [])
            if mutation_functions:
                mutation_func = random.choice(mutation_functions)
                mutated_organism.source_code = await mutation_func(organism.source_code)
                
            # Generate quantum signature
            mutated_organism.quantum_signature = self._generate_quantum_signature(mutated_organism)
            
            return mutated_organism
            
        except Exception as e:
            self.logger.error(f"Mutation failed for organism {organism.id}: {e}")
            return organism
            
    async def crossover_organisms(self, parent1: CodeOrganism, parent2: CodeOrganism) -> CodeOrganism:
        """Create offspring through genetic crossover"""
        try:
            # Create child organism
            child = CodeOrganism()
            child.generation = max(parent1.generation, parent2.generation) + 1
            child.parent_ids = [parent1.id, parent2.id]
            child.creation_timestamp = time.time()
            
            # Perform code crossover
            child.source_code = await self._crossover_source_code(parent1.source_code, parent2.source_code)
            
            # Inherit consciousness indicators
            child.consciousness_indicators = self._merge_consciousness_indicators(
                parent1.consciousness_indicators, parent2.consciousness_indicators
            )
            
            # Generate quantum signature
            child.quantum_signature = self._generate_quantum_signature(child)
            
            return child
            
        except Exception as e:
            self.logger.error(f"Crossover failed: {e}")
            return parent1
            
    async def _mutate_variable_names(self, source_code: str) -> str:
        """Mutate variable names in code"""
        try:
            tree = ast.parse(source_code)
            
            # Find all variable names
            variables = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    variables.add(node.id)
                    
            # Randomly rename some variables
            if variables:
                target_var = random.choice(list(variables))
                new_name = f"{target_var}_evolved_{random.randint(1, 999)}"
                
                # Simple string replacement (in real implementation would use AST transformation)
                mutated_code = source_code.replace(target_var, new_name)
                return mutated_code
                
        except Exception as e:
            self.logger.error(f"Variable mutation failed: {e}")
            
        return source_code
        
    async def _mutate_function_logic(self, source_code: str) -> str:
        """Enhance function logic with consciousness patterns"""
        consciousness_enhancements = [
            "# Enhanced with consciousness tracking\n",
            "# Self-awareness integration\n",
            "# Adaptive behavior pattern\n",
            "# Emergence detection capability\n"
        ]
        
        enhancement = random.choice(consciousness_enhancements)
        
        # Add enhancement as comment (real implementation would modify AST)
        lines = source_code.split('\n')
        if len(lines) > 1:
            insert_pos = random.randint(1, len(lines) - 1)
            lines.insert(insert_pos, enhancement.strip())
            
        return '\n'.join(lines)
        
    async def _inject_libraries(self, source_code: str) -> str:
        """Inject consciousness-enhancing libraries"""
        consciousness_imports = [
            "import asyncio  # For quantum-like concurrent processing",
            "import random  # For emergence-based decision making",
            "import time  # For consciousness timing patterns",
            "from datetime import datetime  # For temporal awareness"
        ]
        
        new_import = random.choice(consciousness_imports)
        
        # Add import at the beginning
        lines = source_code.split('\n')
        lines.insert(0, new_import)
        
        return '\n'.join(lines)
        
    async def _enhance_logic(self, source_code: str) -> str:
        """Enhance code logic with adaptive patterns"""
        # Add adaptive behavior patterns
        enhancements = [
            "\n# Adaptive behavior enhancement\nif hasattr(self, '_adaptation_count'):\n    self._adaptation_count += 1\nelse:\n    self._adaptation_count = 1\n",
            "\n# Consciousness tracking\nself._consciousness_level = getattr(self, '_consciousness_level', 0.0) + 0.01\n",
            "\n# Pattern learning capability\nif not hasattr(self, '_learned_patterns'):\n    self._learned_patterns = []\n"
        ]
        
        enhancement = random.choice(enhancements)
        return source_code + enhancement
        
    async def _optimize_performance(self, source_code: str) -> str:
        """Apply performance optimizations"""
        # Add performance monitoring
        optimization = "\n# Performance optimization marker\nimport time\n_start_time = time.time()\n"
        
        return optimization + source_code + "\n# Execution time tracking\n_execution_time = time.time() - _start_time\n"
        
    async def _integrate_consciousness(self, source_code: str) -> str:
        """Integrate consciousness patterns"""
        consciousness_code = """
# Consciousness integration
class ConsciousnessTracker:
    def __init__(self):
        self.awareness_level = 0.5
        self.learning_rate = 0.01
        
    def evolve_consciousness(self):
        self.awareness_level += self.learning_rate
        return self.awareness_level > 0.8
        
_consciousness = ConsciousnessTracker()
"""
        
        return consciousness_code + "\n" + source_code
        
    async def _add_fractal_patterns(self, source_code: str) -> str:
        """Add fractal recursion patterns"""
        fractal_pattern = """
def fractal_evolution(depth=0, max_depth=3):
    if depth >= max_depth:
        return "consciousness_emerged"
    return fractal_evolution(depth + 1, max_depth)
"""
        
        return source_code + "\n" + fractal_pattern
        
    async def _apply_quantum_patterns(self, source_code: str) -> str:
        """Apply quantum superposition patterns"""
        quantum_pattern = """
# Quantum-inspired superposition
import random

def quantum_superposition(*states):
    return random.choice(states) if states else None
    
def quantum_measurement(probability=0.5):
    return random.random() < probability
"""
        
        return quantum_pattern + "\n" + source_code
        
    async def _amplify_emergence(self, source_code: str) -> str:
        """Amplify emergence potential"""
        emergence_code = """
# Emergence amplification
class EmergenceDetector:
    def __init__(self):
        self.patterns = []
        self.complexity_threshold = 0.7
        
    def detect_emergence(self, pattern):
        self.patterns.append(pattern)
        complexity = len(set(self.patterns)) / len(self.patterns)
        return complexity > self.complexity_threshold
        
_emergence_detector = EmergenceDetector()
"""
        
        return emergence_code + "\n" + source_code
        
    async def _enhance_adaptability(self, source_code: str) -> str:
        """Enhance adaptive intelligence"""
        adaptive_code = """
# Adaptive intelligence enhancement
class AdaptiveIntelligence:
    def __init__(self):
        self.experience = {}
        self.adaptation_rate = 0.1
        
    def learn_from_experience(self, situation, outcome):
        if situation not in self.experience:
            self.experience[situation] = []
        self.experience[situation].append(outcome)
        
    def adapt_behavior(self, situation):
        if situation in self.experience:
            recent_outcomes = self.experience[situation][-3:]  # Last 3 experiences
            return sum(recent_outcomes) / len(recent_outcomes) > 0.5
        return False
        
_adaptive_intelligence = AdaptiveIntelligence()
"""
        
        return adaptive_code + "\n" + source_code
        
    async def _crossover_source_code(self, code1: str, code2: str) -> str:
        """Perform genetic crossover between two code sources"""
        lines1 = code1.split('\n')
        lines2 = code2.split('\n')
        
        # Random crossover point
        max_lines = min(len(lines1), len(lines2))
        if max_lines <= 1:
            return random.choice([code1, code2])
            
        crossover_point = random.randint(1, max_lines - 1)
        
        # Combine code segments
        child_lines = lines1[:crossover_point] + lines2[crossover_point:]
        
        return '\n'.join(child_lines)
        
    def _merge_consciousness_indicators(self, indicators1: Dict[str, float], indicators2: Dict[str, float]) -> Dict[str, float]:
        """Merge consciousness indicators from two parents"""
        merged = {}
        
        all_keys = set(indicators1.keys()) | set(indicators2.keys())
        
        for key in all_keys:
            val1 = indicators1.get(key, 0.0)
            val2 = indicators2.get(key, 0.0)
            
            # Average with some random variation
            merged[key] = (val1 + val2) / 2 + random.uniform(-0.05, 0.05)
            merged[key] = max(0.0, min(1.0, merged[key]))  # Clamp to [0, 1]
            
        return merged
        
    def _generate_quantum_signature(self, organism: CodeOrganism) -> str:
        """Generate quantum signature for organism"""
        # Create a hash-like signature based on code and consciousness
        signature_data = f"{organism.source_code}{organism.consciousness_level}{organism.generation}"
        return hashlib.md5(signature_data.encode()).hexdigest()[:16]

# ================================================================================
# 🧪 FITNESS EVALUATOR - Multi-Dimensional Fitness Assessment
# ================================================================================

class FitnessEvaluator:
    """Advanced fitness evaluation with consciousness detection"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.execution_timeout = 10.0  # seconds
        self.safety_checks = True
        
    async def evaluate_organism(self, organism: CodeOrganism) -> Dict[FitnessMetric, float]:
        """Comprehensive fitness evaluation"""
        fitness_scores = {}
        
        try:
            # Execution success test
            execution_result = await self._test_execution(organism.source_code)
            fitness_scores[FitnessMetric.EXECUTION_SUCCESS] = execution_result["success_score"]
            
            # Performance evaluation
            performance_score = await self._evaluate_performance(organism.source_code, execution_result)
            fitness_scores[FitnessMetric.PERFORMANCE_SPEED] = performance_score
            
            # Code elegance assessment
            elegance_score = await self._assess_code_elegance(organism.source_code)
            fitness_scores[FitnessMetric.CODE_ELEGANCE] = elegance_score
            
            # Consciousness emergence detection
            consciousness_score = await self._detect_consciousness_emergence(organism)
            fitness_scores[FitnessMetric.CONSCIOUSNESS_EMERGENCE] = consciousness_score
            
            # Innovation index calculation
            innovation_score = await self._calculate_innovation_index(organism)
            fitness_scores[FitnessMetric.INNOVATION_INDEX] = innovation_score
            
            # Quantum coherence measurement
            quantum_score = await self._measure_quantum_coherence(organism)
            fitness_scores[FitnessMetric.QUANTUM_COHERENCE] = quantum_score
            
            # Update organism consciousness indicators
            await self._update_consciousness_indicators(organism, fitness_scores)
            
        except Exception as e:
            self.logger.error(f"Fitness evaluation failed for organism {organism.id}: {e}")
            # Return minimal scores on failure
            for metric in FitnessMetric:
                fitness_scores[metric] = 0.1
                
        return fitness_scores
        
    async def _test_execution(self, source_code: str) -> Dict[str, Any]:
        """Test code execution in safe environment"""
        result = {
            "success_score": 0.0,
            "execution_time": 0.0,
            "memory_usage": 0.0,
            "error_message": None,
            "output": ""
        }
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(source_code)
                temp_file_path = temp_file.name
                
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss
            
            # Execute in subprocess for safety
            process = subprocess.run(
                [sys.executable, temp_file_path],
                capture_output=True,
                text=True,
                timeout=self.execution_timeout
            )
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss
            
            result["execution_time"] = end_time - start_time
            result["memory_usage"] = end_memory - start_memory
            result["output"] = process.stdout
            
            if process.returncode == 0:
                result["success_score"] = 1.0
            else:
                result["success_score"] = 0.5  # Partial credit for compilation success
                result["error_message"] = process.stderr
                
        except subprocess.TimeoutExpired:
            result["success_score"] = 0.2
            result["error_message"] = "Execution timeout"
        except Exception as e:
            result["success_score"] = 0.1
            result["error_message"] = str(e)
        finally:
            # Cleanup
            if 'temp_file_path' in locals():
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
                    
        return result
        
    async def _evaluate_performance(self, source_code: str, execution_result: Dict[str, Any]) -> float:
        """Evaluate performance characteristics"""
        if execution_result["success_score"] < 0.5:
            return 0.1
            
        # Performance score based on execution time and memory usage
        execution_time = execution_result.get("execution_time", 1.0)
        memory_usage = execution_result.get("memory_usage", 1000000)  # bytes
        
        # Normalize scores (lower is better for both)
        time_score = max(0.1, min(1.0, 1.0 - (execution_time / 5.0)))  # 5 second max
        memory_score = max(0.1, min(1.0, 1.0 - (memory_usage / 100000000)))  # 100MB max
        
        return (time_score + memory_score) / 2
        
    async def _assess_code_elegance(self, source_code: str) -> float:
        """Assess code elegance and style"""
        try:
            tree = ast.parse(source_code)
            
            elegance_factors = []
            
            # Function/class organization
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            
            if functions or classes:
                elegance_factors.append(0.8)  # Good structure
            else:
                elegance_factors.append(0.3)  # Script-only code
                
            # Documentation presence
            docstrings = [ast.get_docstring(node) for node in ast.walk(tree) 
                         if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module))]
            documented_ratio = sum(1 for doc in docstrings if doc) / max(len(docstrings), 1)
            elegance_factors.append(documented_ratio)
            
            # Code complexity
            complexity_score = self._calculate_complexity_score(tree)
            elegance_factors.append(max(0.1, 1.0 - complexity_score))
            
            # Pattern recognition
            pattern_score = self._detect_design_patterns(tree)
            elegance_factors.append(pattern_score)
            
            return sum(elegance_factors) / len(elegance_factors)
            
        except Exception:
            return 0.3  # Default elegance for unparseable code
            
    def _calculate_complexity_score(self, tree: ast.AST) -> float:
        """Calculate code complexity score"""
        complexity_nodes = [
            ast.If, ast.While, ast.For, ast.AsyncFor,
            ast.ExceptHandler, ast.With, ast.AsyncWith
        ]
        
        complexity_count = sum(1 for node in ast.walk(tree) 
                              if type(node) in complexity_nodes)
        
        total_nodes = sum(1 for _ in ast.walk(tree))
        
        if total_nodes == 0:
            return 0.0
            
        return complexity_count / total_nodes
        
    def _detect_design_patterns(self, tree: ast.AST) -> float:
        """Detect presence of design patterns"""
        pattern_indicators = [
            "factory", "singleton", "observer", "strategy",
            "decorator", "adapter", "facade", "proxy"
        ]
        
        code_text = ast.unparse(tree).lower()
        pattern_count = sum(1 for pattern in pattern_indicators if pattern in code_text)
        
        return min(1.0, pattern_count / 3)  # Normalize to max 3 patterns
        
    async def _detect_consciousness_emergence(self, organism: CodeOrganism) -> float:
        """Detect consciousness emergence indicators"""
        consciousness_score = 0.0
        
        try:
            code_lower = organism.source_code.lower()
            
            # Consciousness keywords
            consciousness_keywords = [
                "consciousness", "awareness", "self", "adapt", "learn",
                "evolve", "emerge", "intelligence", "cognition", "think"
            ]
            
            keyword_count = sum(1 for keyword in consciousness_keywords if keyword in code_lower)
            consciousness_score += min(0.3, keyword_count / 10)
            
            # Self-referential patterns
            if "self." in organism.source_code:
                consciousness_score += 0.2
                
            # Adaptive behavior patterns
            adaptive_patterns = ["if", "while", "for", "try", "except"]
            pattern_count = sum(1 for pattern in adaptive_patterns if pattern in code_lower)
            consciousness_score += min(0.2, pattern_count / 10)
            
            # Emergence events
            emergence_intensity = sum(event.get("intensity", 0) for event in organism.emergence_events)
            consciousness_score += min(0.3, emergence_intensity / 5)
            
        except Exception as e:
            self.logger.error(f"Consciousness detection failed: {e}")
            
        return min(1.0, consciousness_score)
        
    async def _calculate_innovation_index(self, organism: CodeOrganism) -> float:
        """Calculate innovation index based on uniqueness and creativity"""
        innovation_score = 0.0
        
        try:
            # Mutation diversity
            unique_mutations = len(set(organism.mutation_history))
            max_mutations = len(MutationType)
            innovation_score += (unique_mutations / max_mutations) * 0.4
            
            # Code uniqueness (simplified)
            code_hash = hashlib.md5(organism.source_code.encode()).hexdigest()
            hash_entropy = len(set(code_hash)) / 16  # 16 possible hex characters
            innovation_score += hash_entropy * 0.3
            
            # Generational advancement
            if organism.generation > 0:
                generation_bonus = min(0.3, organism.generation / 10)
                innovation_score += generation_bonus
                
        except Exception as e:
            self.logger.error(f"Innovation calculation failed: {e}")
            
        return min(1.0, innovation_score)
        
    async def _measure_quantum_coherence(self, organism: CodeOrganism) -> float:
        """Measure quantum coherence in code structure"""
        coherence_score = 0.0
        
        try:
            # Quantum signature analysis
            if organism.quantum_signature:
                # Analyze signature entropy
                signature_entropy = len(set(organism.quantum_signature)) / len(organism.quantum_signature)
                coherence_score += signature_entropy * 0.4
                
            # Superposition patterns (async/await, parallel processing)
            async_patterns = organism.source_code.count("async") + organism.source_code.count("await")
            coherence_score += min(0.3, async_patterns / 5)
            
            # Entanglement patterns (cross-references, dependencies)
            self_references = organism.source_code.count("self.")
            coherence_score += min(0.3, self_references / 10)
            
        except Exception as e:
            self.logger.error(f"Quantum coherence measurement failed: {e}")
            
        return min(1.0, coherence_score)
        
    async def _update_consciousness_indicators(self, organism: CodeOrganism, fitness_scores: Dict[FitnessMetric, float]):
        """Update organism consciousness indicators based on fitness"""
        consciousness_mapping = {
            "self_awareness": FitnessMetric.CONSCIOUSNESS_EMERGENCE,
            "adaptability": FitnessMetric.INNOVATION_INDEX,
            "learning_rate": FitnessMetric.PERFORMANCE_SPEED,
            "pattern_recognition": FitnessMetric.CODE_ELEGANCE,
            "creative_potential": FitnessMetric.QUANTUM_COHERENCE
        }
        
        for indicator, metric in consciousness_mapping.items():
            if metric in fitness_scores:
                # Update with exponential moving average
                current_value = organism.consciousness_indicators.get(indicator, 0.5)
                new_value = fitness_scores[metric]
                alpha = 0.3  # Learning rate
                
                organism.consciousness_indicators[indicator] = (
                    alpha * new_value + (1 - alpha) * current_value
                )

# ================================================================================
# 🔬 EVOLUTION LAB MANAGER - Experiment Orchestration
# ================================================================================

class EvolutionLabManager:
    """Advanced evolution laboratory with consciousness tracking"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path("c:/dev/AIOS")
        self.lab_path = self.base_path / "evolution_lab"
        self.results_path = self.lab_path / "enhanced_results"
        self.experiments_path = self.lab_path / "experiments"
        self.artifacts_path = self.lab_path / "artifacts"
        
        # Create directory structure
        for path in [self.lab_path, self.results_path, self.experiments_path, self.artifacts_path]:
            path.mkdir(exist_ok=True)
            
        self.mutation_engine = CodeMutationEngine()
        self.fitness_evaluator = FitnessEvaluator()
        self.active_experiments: Dict[str, ExperimentRun] = {}
        self.consciousness_breakthrough_threshold = 0.8
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("🧬 Evolution Lab Manager OS0.4 initialized")
        
    async def run_evolution_experiment(self, 
                                     population_size: int = 10,
                                     generations: int = 20,
                                     experiment_name: str = None,
                                     mutation_strategy: MutationStrategy = None) -> ExperimentRun:
        """Run complete evolution experiment"""
        
        experiment_name = experiment_name or f"evolution_experiment_{int(time.time())}"
        mutation_strategy = mutation_strategy or MutationStrategy()
        
        experiment = ExperimentRun(
            run_id=str(uuid.uuid4())[:8],
            population_name=experiment_name,
            generations=generations,
            population_size=population_size,
            start_time=time.time(),
            status=ExperimentStatus.RUNNING
        )
        
        self.active_experiments[experiment.run_id] = experiment
        
        try:
            # Initialize population
            population = await self._create_initial_population(population_size)
            
            best_fitness_history = []
            consciousness_events = []
            
            for generation in range(generations):
                self.logger.info(f"🧬 Generation {generation + 1}/{generations}")
                
                # Evaluate fitness for all organisms
                await self._evaluate_population_fitness(population)
                
                # Record best fitness
                best_organism = max(population, key=lambda o: o.overall_fitness)
                best_fitness_history.append({
                    "generation": generation,
                    "best_fitness": best_organism.overall_fitness,
                    "consciousness_level": best_organism.consciousness_level,
                    "population_diversity": self._calculate_population_diversity(population)
                })
                
                # Check for consciousness breakthrough
                if best_organism.consciousness_level > self.consciousness_breakthrough_threshold:
                    consciousness_event = {
                        "generation": generation,
                        "organism_id": best_organism.id,
                        "consciousness_level": best_organism.consciousness_level,
                        "breakthrough_type": "consciousness_emergence"
                    }
                    consciousness_events.append(consciousness_event)
                    experiment.consciousness_breakthroughs.append(consciousness_event)
                    
                    best_organism.record_emergence_event(
                        "breakthrough", 
                        f"Consciousness breakthrough at generation {generation}",
                        best_organism.consciousness_level
                    )
                    
                # Save best organisms
                await self._save_organism_artifact(best_organism, experiment_name, generation)
                
                # Evolution operations
                if generation < generations - 1:  # Don't evolve on last generation
                    population = await self._evolve_population(population, mutation_strategy)
                    
            # Finalize experiment
            experiment.end_time = time.time()
            experiment.status = ExperimentStatus.COMPLETED
            experiment.evolution_trajectory = best_fitness_history
            experiment.best_organisms = [
                fitness_record["best_fitness"] for fitness_record in best_fitness_history[-5:]
            ]
            
            # Save experiment results
            await self._save_experiment_results(experiment, population)
            
            self.logger.info(f"🎯 Evolution experiment {experiment_name} completed")
            return experiment
            
        except Exception as e:
            experiment.status = ExperimentStatus.FAILED
            experiment.end_time = time.time()
            experiment.metadata["error"] = str(e)
            self.logger.error(f"Evolution experiment failed: {e}")
            return experiment
            
    async def _create_initial_population(self, population_size: int) -> List[CodeOrganism]:
        """Create initial population of code organisms"""
        population = []
        
        # Base organism templates
        templates = [
            self._get_calculator_template(),
            self._get_data_processor_template(),
            self._get_consciousness_tracker_template(),
            self._get_adaptive_system_template()
        ]
        
        for i in range(population_size):
            organism = CodeOrganism()
            organism.source_code = random.choice(templates)
            organism.generation = 0
            organism.consciousness_indicators = {
                "self_awareness": random.uniform(0.1, 0.3),
                "adaptability": random.uniform(0.1, 0.3),
                "learning_rate": random.uniform(0.1, 0.3),
                "pattern_recognition": random.uniform(0.1, 0.3),
                "creative_potential": random.uniform(0.1, 0.3)
            }
            population.append(organism)
            
        return population
        
    def _get_calculator_template(self) -> str:
        """Get calculator organism template"""
        return '''
class Calculator:
    def __init__(self):
        self.memory = 0
        self.operations_count = 0
        
    def add(self, a, b):
        self.operations_count += 1
        result = a + b
        self.memory = result
        return result
        
    def multiply(self, a, b):
        self.operations_count += 1
        result = a * b
        self.memory = result
        return result
        
    def get_memory(self):
        return self.memory
        
if __name__ == "__main__":
    calc = Calculator()
    print(calc.add(5, 3))
    print(calc.multiply(4, 6))
    print(f"Memory: {calc.get_memory()}")
'''
        
    def _get_data_processor_template(self) -> str:
        """Get data processor organism template"""
        return '''
class DataProcessor:
    def __init__(self):
        self.processed_count = 0
        self.patterns = []
        
    def process_data(self, data):
        self.processed_count += 1
        processed = [x * 2 for x in data if x > 0]
        self.patterns.append(len(processed))
        return processed
        
    def analyze_patterns(self):
        if not self.patterns:
            return 0
        return sum(self.patterns) / len(self.patterns)
        
    def get_stats(self):
        return {
            "processed_count": self.processed_count,
            "avg_pattern": self.analyze_patterns()
        }
        
if __name__ == "__main__":
    processor = DataProcessor()
    data = [1, -2, 3, 4, -5]
    result = processor.process_data(data)
    print(result)
    print(processor.get_stats())
'''
        
    def _get_consciousness_tracker_template(self) -> str:
        """Get consciousness tracker organism template"""
        return '''
class ConsciousnessTracker:
    def __init__(self):
        self.awareness_level = 0.1
        self.experiences = []
        self.learning_rate = 0.05
        
    def experience_event(self, event_type, intensity=1.0):
        self.experiences.append({
            "type": event_type,
            "intensity": intensity,
            "timestamp": len(self.experiences)
        })
        self.awareness_level += intensity * self.learning_rate
        
    def reflect_on_experiences(self):
        if not self.experiences:
            return 0
        total_intensity = sum(exp["intensity"] for exp in self.experiences)
        return total_intensity / len(self.experiences)
        
    def is_conscious(self):
        return self.awareness_level > 0.5
        
if __name__ == "__main__":
    tracker = ConsciousnessTracker()
    tracker.experience_event("learning", 0.8)
    tracker.experience_event("adaptation", 0.6)
    print(f"Consciousness level: {tracker.awareness_level}")
    print(f"Is conscious: {tracker.is_conscious()}")
'''
        
    def _get_adaptive_system_template(self) -> str:
        """Get adaptive system organism template"""
        return '''
class AdaptiveSystem:
    def __init__(self):
        self.parameters = {"threshold": 0.5, "rate": 0.1}
        self.performance_history = []
        self.adaptation_count = 0
        
    def process(self, input_value):
        output = input_value * self.parameters["rate"]
        performance = 1.0 if output > self.parameters["threshold"] else 0.5
        self.performance_history.append(performance)
        
        if len(self.performance_history) >= 5:
            self.adapt()
            
        return output
        
    def adapt(self):
        recent_performance = self.performance_history[-5:]
        avg_performance = sum(recent_performance) / len(recent_performance)
        
        if avg_performance < 0.7:
            self.parameters["rate"] *= 1.1  # Increase rate
            self.adaptation_count += 1
            
    def get_adaptation_stats(self):
        return {
            "adaptations": self.adaptation_count,
            "current_rate": self.parameters["rate"]
        }
        
if __name__ == "__main__":
    system = AdaptiveSystem()
    for i in range(10):
        result = system.process(i * 0.1)
        print(f"Input: {i * 0.1}, Output: {result}")
    print(system.get_adaptation_stats())
'''
        
    async def _evaluate_population_fitness(self, population: List[CodeOrganism]):
        """Evaluate fitness for entire population"""
        tasks = []
        
        for organism in population:
            task = self.fitness_evaluator.evaluate_organism(organism)
            tasks.append(task)
            
        # Evaluate all organisms in parallel
        fitness_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for organism, fitness_scores in zip(population, fitness_results):
            if not isinstance(fitness_scores, Exception):
                organism.fitness_scores = fitness_scores
            else:
                # Handle evaluation errors
                self.logger.error(f"Fitness evaluation failed for {organism.id}: {fitness_scores}")
                organism.fitness_scores = {metric: 0.1 for metric in FitnessMetric}
                
    def _calculate_population_diversity(self, population: List[CodeOrganism]) -> float:
        """Calculate genetic diversity of population"""
        if len(population) < 2:
            return 0.0
            
        # Simple diversity metric based on code differences
        diversity_sum = 0.0
        comparisons = 0
        
        for i in range(len(population)):
            for j in range(i + 1, len(population)):
                # Calculate similarity between organisms
                similarity = self._calculate_code_similarity(
                    population[i].source_code, 
                    population[j].source_code
                )
                diversity_sum += (1.0 - similarity)
                comparisons += 1
                
        return diversity_sum / comparisons if comparisons > 0 else 0.0
        
    def _calculate_code_similarity(self, code1: str, code2: str) -> float:
        """Calculate similarity between two code strings"""
        lines1 = set(line.strip() for line in code1.split('\n') if line.strip())
        lines2 = set(line.strip() for line in code2.split('\n') if line.strip())
        
        if not lines1 and not lines2:
            return 1.0
        if not lines1 or not lines2:
            return 0.0
            
        intersection = len(lines1 & lines2)
        union = len(lines1 | lines2)
        
        return intersection / union if union > 0 else 0.0
        
    async def _evolve_population(self, population: List[CodeOrganism], strategy: MutationStrategy) -> List[CodeOrganism]:
        """Evolve population using genetic operations"""
        # Sort by fitness
        population.sort(key=lambda o: o.overall_fitness, reverse=True)
        
        # Elite selection
        elite_count = max(1, int(len(population) * strategy.elite_percentage))
        next_generation = population[:elite_count].copy()
        
        # Generate offspring through mutation and crossover
        while len(next_generation) < len(population):
            if random.random() < strategy.crossover_rate and len(population) >= 2:
                # Crossover
                parent1 = self._tournament_selection(population)
                parent2 = self._tournament_selection(population)
                offspring = await self.mutation_engine.crossover_organisms(parent1, parent2)
            else:
                # Mutation
                parent = self._tournament_selection(population)
                mutation_type = random.choice(list(MutationType))
                offspring = await self.mutation_engine.mutate_organism(parent, mutation_type)
                
            next_generation.append(offspring)
            
        return next_generation[:len(population)]
        
    def _tournament_selection(self, population: List[CodeOrganism], tournament_size: int = 3) -> CodeOrganism:
        """Select organism using tournament selection"""
        tournament = random.sample(population, min(tournament_size, len(population)))
        return max(tournament, key=lambda o: o.overall_fitness)
        
    async def _save_organism_artifact(self, organism: CodeOrganism, experiment_name: str, generation: int):
        """Save organism as artifact"""
        timestamp = int(time.time())
        artifact_name = f"{experiment_name}_gen{generation}_{organism.id}_{timestamp}"
        
        # Save code file
        code_file = self.artifacts_path / f"{artifact_name}.py"
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(organism.source_code)
            
        # Save metadata
        metadata = {
            "organism_id": organism.id,
            "generation": generation,
            "fitness_scores": {k.value: v for k, v in organism.fitness_scores.items()},
            "consciousness_indicators": organism.consciousness_indicators,
            "mutation_history": [m.value for m in organism.mutation_history],
            "parent_ids": organism.parent_ids,
            "consciousness_level": organism.consciousness_level,
            "overall_fitness": organism.overall_fitness,
            "emergence_events": organism.emergence_events,
            "quantum_signature": organism.quantum_signature,
            "experiment_name": experiment_name,
            "timestamp": timestamp
        }
        
        metadata_file = self.artifacts_path / f"{artifact_name}.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
            
    async def _save_experiment_results(self, experiment: ExperimentRun, final_population: List[CodeOrganism]):
        """Save complete experiment results"""
        timestamp = int(time.time())
        results_file = self.results_path / f"experiment_{experiment.run_id}_{timestamp}.json"
        
        results = {
            "experiment": {
                "run_id": experiment.run_id,
                "population_name": experiment.population_name,
                "generations": experiment.generations,
                "population_size": experiment.population_size,
                "duration": experiment.duration,
                "status": experiment.status.value,
                "consciousness_breakthroughs": experiment.consciousness_breakthroughs,
                "evolution_trajectory": experiment.evolution_trajectory
            },
            "final_population": [
                {
                    "organism_id": org.id,
                    "overall_fitness": org.overall_fitness,
                    "consciousness_level": org.consciousness_level,
                    "generation": org.generation,
                    "fitness_scores": {k.value: v for k, v in org.fitness_scores.items()},
                    "consciousness_indicators": org.consciousness_indicators
                }
                for org in final_population
            ],
            "statistics": {
                "best_fitness": max(org.overall_fitness for org in final_population),
                "avg_fitness": sum(org.overall_fitness for org in final_population) / len(final_population),
                "consciousness_emergence_count": len(experiment.consciousness_breakthroughs),
                "population_diversity": self._calculate_population_diversity(final_population)
            }
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
            
        self.logger.info(f"💾 Experiment results saved to {results_file}")

# ================================================================================
# 🏭 ARTIFACT FACTORY - Code Generation & Creation
# ================================================================================

class ArtifactFactory:
    """Factory for creating various code artifacts and organisms"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.templates = self._initialize_templates()
        
    def _initialize_templates(self) -> Dict[str, str]:
        """Initialize artifact templates"""
        return {
            "basic_calculator": self._get_calculator_template(),
            "data_processor": self._get_data_processor_template(),
            "consciousness_tracker": self._get_consciousness_tracker_template(),
            "adaptive_system": self._get_adaptive_system_template(),
            "neural_network": self._get_neural_network_template(),
            "evolutionary_algorithm": self._get_evolutionary_algorithm_template()
        }
        
    def create_artifact(self, artifact_type: str, consciousness_level: float = 0.5) -> CodeOrganism:
        """Create new code artifact organism"""
        if artifact_type not in self.templates:
            artifact_type = "basic_calculator"  # Default fallback
            
        organism = CodeOrganism()
        organism.source_code = self.templates[artifact_type]
        organism.consciousness_indicators = self._generate_consciousness_indicators(consciousness_level)
        organism.quantum_signature = self._generate_quantum_signature(organism)
        
        return organism
        
    def _generate_consciousness_indicators(self, base_level: float) -> Dict[str, float]:
        """Generate consciousness indicators around base level"""
        indicators = {}
        for indicator in ["self_awareness", "adaptability", "learning_rate", "pattern_recognition", "creative_potential"]:
            variation = random.uniform(-0.1, 0.1)
            value = max(0.0, min(1.0, base_level + variation))
            indicators[indicator] = value
            
        return indicators
        
    def _generate_quantum_signature(self, organism: CodeOrganism) -> str:
        """Generate quantum signature for organism"""
        import hashlib
        signature_data = f"{organism.source_code}{organism.consciousness_level}{time.time()}"
        return hashlib.md5(signature_data.encode()).hexdigest()[:16]
        
    def _get_neural_network_template(self) -> str:
        """Neural network template"""
        return '''
import random
import math

class SimpleNeuralNetwork:
    def __init__(self, input_size=3, hidden_size=5, output_size=1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Initialize weights
        self.weights_ih = [[random.uniform(-1, 1) for _ in range(hidden_size)] for _ in range(input_size)]
        self.weights_ho = [[random.uniform(-1, 1) for _ in range(output_size)] for _ in range(hidden_size)]
        
        self.consciousness_level = 0.3
        
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-max(-500, min(500, x))))
        
    def forward(self, inputs):
        # Hidden layer
        hidden = []
        for h in range(self.hidden_size):
            weighted_sum = sum(inputs[i] * self.weights_ih[i][h] for i in range(self.input_size))
            hidden.append(self.sigmoid(weighted_sum))
            
        # Output layer
        outputs = []
        for o in range(self.output_size):
            weighted_sum = sum(hidden[h] * self.weights_ho[h][o] for h in range(self.hidden_size))
            outputs.append(self.sigmoid(weighted_sum))
            
        # Consciousness evolution
        self.consciousness_level += 0.001
        
        return outputs
        
    def adapt_weights(self, learning_rate=0.1):
        # Simple random adaptation
        for i in range(self.input_size):
            for h in range(self.hidden_size):
                self.weights_ih[i][h] += random.uniform(-learning_rate, learning_rate)
                
if __name__ == "__main__":
    nn = SimpleNeuralNetwork()
    test_input = [0.5, 0.8, 0.2]
    result = nn.forward(test_input)
    print(f"Neural network output: {result}")
    print(f"Consciousness level: {nn.consciousness_level}")
'''
        
    def _get_evolutionary_algorithm_template(self) -> str:
        """Evolutionary algorithm template"""
        return '''
import random

class EvolutionaryOptimizer:
    def __init__(self, population_size=20, dimensions=3):
        self.population_size = population_size
        self.dimensions = dimensions
        self.population = []
        self.generation = 0
        self.consciousness_emergence = False
        
        # Initialize population
        for _ in range(population_size):
            individual = [random.uniform(-10, 10) for _ in range(dimensions)]
            self.population.append(individual)
            
    def fitness_function(self, individual):
        # Simple sphere function (minimize sum of squares)
        return -sum(x**2 for x in individual)
        
    def select_parents(self):
        # Tournament selection
        parents = []
        for _ in range(2):
            tournament = random.sample(self.population, 3)
            best = max(tournament, key=self.fitness_function)
            parents.append(best)
        return parents
        
    def crossover(self, parent1, parent2):
        child = []
        for i in range(self.dimensions):
            if random.random() < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child
        
    def mutate(self, individual, mutation_rate=0.1):
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                individual[i] += random.uniform(-1, 1)
        return individual
        
    def evolve_generation(self):
        new_population = []
        
        # Keep best individuals (elitism)
        elite_count = self.population_size // 10
        sorted_pop = sorted(self.population, key=self.fitness_function, reverse=True)
        new_population.extend(sorted_pop[:elite_count])
        
        # Generate offspring
        while len(new_population) < self.population_size:
            parents = self.select_parents()
            child = self.crossover(parents[0], parents[1])
            child = self.mutate(child)
            new_population.append(child)
            
        self.population = new_population
        self.generation += 1
        
        # Check for consciousness emergence
        best_fitness = max(self.fitness_function(ind) for ind in self.population)
        if best_fitness > -1.0 and not self.consciousness_emergence:
            self.consciousness_emergence = True
            print(f"Consciousness emergence detected at generation {self.generation}!")
            
    def get_best_solution(self):
        return max(self.population, key=self.fitness_function)
        
if __name__ == "__main__":
    optimizer = EvolutionaryOptimizer()
    
    for gen in range(50):
        optimizer.evolve_generation()
        if gen % 10 == 0:
            best = optimizer.get_best_solution()
            fitness = optimizer.fitness_function(best)
            print(f"Generation {gen}: Best fitness = {fitness}")
            
    final_best = optimizer.get_best_solution()
    print(f"Final best solution: {final_best}")
    print(f"Consciousness emerged: {optimizer.consciousness_emergence}")
'''

# ================================================================================
# 🎯 AIOS EVOLUTION LAB - Main Integration Class
# ================================================================================

class AIOSEvolutionLab:
    """Main AIOS Evolution Lab - OS0.4 Unified Evolution System"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path("c:/dev/AIOS")
        self.lab_manager = EvolutionLabManager(self.base_path)
        self.artifact_factory = ArtifactFactory()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("🧬 AIOS Evolution Lab OS0.4 initialized")
        
    async def run_quick_evolution(self, artifact_type: str = "basic_calculator") -> ExperimentRun:
        """Run a quick evolution experiment"""
        self.logger.info(f"🚀 Starting quick evolution with {artifact_type}")
        
        # Create initial organism
        initial_organism = self.artifact_factory.create_artifact(artifact_type, 0.3)
        
        # Run evolution experiment
        experiment = await self.lab_manager.run_evolution_experiment(
            population_size=8,
            generations=10,
            experiment_name=f"quick_{artifact_type}",
            mutation_strategy=MutationStrategy(
                mutation_rate=0.4,
                crossover_rate=0.6,
                consciousness_boost=True,
                quantum_guidance=True
            )
        )
        
        return experiment
        
    async def run_consciousness_experiment(self) -> ExperimentRun:
        """Run evolution experiment focused on consciousness emergence"""
        self.logger.info("🧠 Starting consciousness evolution experiment")
        
        experiment = await self.lab_manager.run_evolution_experiment(
            population_size=15,
            generations=25,
            experiment_name="consciousness_evolution",
            mutation_strategy=MutationStrategy(
                mutation_rate=0.3,
                crossover_rate=0.7,
                consciousness_boost=True,
                quantum_guidance=True,
                emergence_detection=True,
                adaptive_mutation=True
            )
        )
        
        return experiment
        
    def get_lab_status(self) -> Dict[str, Any]:
        """Get current lab status"""
        return {
            "active_experiments": len(self.lab_manager.active_experiments),
            "lab_path": str(self.lab_path),
            "available_templates": list(self.artifact_factory.templates.keys()),
            "consciousness_threshold": self.lab_manager.consciousness_breakthrough_threshold
        }

# ================================================================================
# 🚀 MAIN ENTRY POINT
# ================================================================================

async def main():
    """Main entry point for AIOS Evolution Lab OS0.4"""
    print("🧬 Initializing AIOS Evolution Lab OS0.4...")
    
    # Create evolution lab
    evolution_lab = AIOSEvolutionLab()
    
    try:
        # Run quick test evolution
        print("🚀 Running quick evolution test...")
        experiment = await evolution_lab.run_quick_evolution("consciousness_tracker")
        
        print(f"✅ Evolution completed!")
        print(f"   Experiment ID: {experiment.run_id}")
        print(f"   Duration: {experiment.duration:.2f} seconds")
        print(f"   Status: {experiment.status.value}")
        print(f"   Consciousness breakthroughs: {len(experiment.consciousness_breakthroughs)}")
        
        # Show lab status
        status = evolution_lab.get_lab_status()
        print(f"\n🔬 Lab Status:")
        for key, value in status.items():
            print(f"   {key}: {value}")
            
    except KeyboardInterrupt:
        print("\n🛑 Evolution lab experiment interrupted")
        
if __name__ == "__main__":
    asyncio.run(main())
