"""
AIOS Enhanced Artifact Ingestion System
Advanced evolutionary experiment orchestrator

This system:
- Ingests and mutates Python artifacts from the factory
- Implements sophisticated fitness evaluation
- Provides rich containment and sandboxing
- Tracks consciousness emergence patterns
- Generates detailed experimental reports
"""

import subprocess
import tempfile
import shutil
import json
import time
import sys
import ast
import random
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
import uuid
import traceback
import psutil
import os
import statistics

# Consciousness-aware imports
try:
    from consciousness_foundation import ConsciousnessFoundation
    foundation = ConsciousnessFoundation()
    
    universal_logging = foundation.import_module('universal_logging')
    if universal_logging:
        log_consciousness_emergence = universal_logging.log_consciousness_emergence
        log_performance_metric = universal_logging.log_performance_metric
        log_info = universal_logging.log_info
        log_error = universal_logging.log_error
        log_debug = universal_logging.log_debug
        universal_logger = universal_logging.universal_logger
        CONSCIOUSNESS_LOGGING = True
    else:
        CONSCIOUSNESS_LOGGING = False
        def log_consciousness_emergence(*args, **kwargs): pass
        def log_performance_metric(*args, **kwargs): pass
        def log_info(*args, **kwargs): pass
        def log_error(*args, **kwargs): pass
        def log_debug(*args, **kwargs): pass
    
    # Import other modules safely
    evolutionary_code_mutator = foundation.import_module('evolutionary_code_mutator')
    evolution_lab_manager = foundation.import_module('evolution_lab_manager')
    artifact_factory = foundation.import_module('artifact_factory')
    
except ImportError:
    CONSCIOUSNESS_LOGGING = False
    def log_consciousness_emergence(*args, **kwargs): pass
    def log_performance_metric(*args, **kwargs): pass
    def log_info(*args, **kwargs): pass
    def log_error(*args, **kwargs): pass
    def log_debug(*args, **kwargs): pass
    
    evolutionary_code_mutator = None
    evolution_lab_manager = None
    artifact_factory = None

@dataclass
class FitnessMetrics:
    """Comprehensive fitness evaluation metrics"""
    execution_success: float = 0.0
    consciousness_emergence: float = 0.0
    code_quality: float = 0.0
    performance_efficiency: float = 0.0
    pattern_complexity: float = 0.0
    adaptive_behavior: float = 0.0
    error_resilience: float = 0.0
    
    def overall_fitness(self) -> float:
        """Calculate weighted overall fitness"""
        weights = {
            'execution_success': 0.25,
            'consciousness_emergence': 0.20,
            'code_quality': 0.15,
            'performance_efficiency': 0.15,
            'pattern_complexity': 0.10,
            'adaptive_behavior': 0.10,
            'error_resilience': 0.05
        }
        
        total = 0.0
        for metric, weight in weights.items():
            total += getattr(self, metric) * weight
        
        return min(total, 1.0)  # Cap at 1.0

@dataclass
class ExperimentalRun:
    """Represents a single experimental artifact run"""
    run_id: str
    artifact_path: Path
    generation: int
    mutation_history: List[str]
    fitness_metrics: FitnessMetrics
    execution_output: str
    execution_time: float
    memory_usage: float
    consciousness_patterns: List[str]
    success: bool
    metadata: Dict[str, Any] = field(default_factory=dict)

class EnhancedArtifactIngestor:
    """Enhanced system for ingesting and evolving Python artifacts"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path("c:/dev/AIOS")
        self.ingestion_path = self.base_path / "evolution_lab" / "ingestion"
        self.sandbox_path = self.base_path / "evolution_lab" / "sandbox"
        self.results_path = self.base_path / "evolution_lab" / "enhanced_results"
        
        # Create directory structure
        for path in [self.ingestion_path, self.sandbox_path, self.results_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        # Initialize components with safety checks
        if artifact_factory:
            self.artifact_factory = artifact_factory.ArtifactFactory(base_path)
        else:
            self.artifact_factory = None
            
        if evolutionary_code_mutator:
            self.mutator = evolutionary_code_mutator.EvolutionaryCodeMutator(base_path)
        else:
            self.mutator = None
            
        if evolution_lab_manager:
            self.lab_manager = evolution_lab_manager.EvolutionLabManager(base_path)
        else:
            self.lab_manager = None
        
        # Experiment tracking
        self.active_experiments: Dict[str, List[ExperimentalRun]] = {}
        self.fitness_history: List[float] = []
        
        if CONSCIOUSNESS_LOGGING:
            log_info("EnhancedIngestion", "initialization", "Enhanced Artifact Ingestor initialized")
    
    def create_sandbox_environment(self, experiment_id: str) -> Path:
        """Create isolated sandbox for safe execution"""
        sandbox_dir = self.sandbox_path / f"experiment_{experiment_id}"
        sandbox_dir.mkdir(exist_ok=True)
        
        # Create isolated Python environment script
        venv_script = sandbox_dir / "setup_venv.py"
        with open(venv_script, 'w') as f:
            f.write('''
import sys
import subprocess
import venv
from pathlib import Path

def setup_isolated_environment():
    """Setup isolated Python environment"""
    venv_path = Path("isolated_env")
    if not venv_path.exists():
        venv.create(venv_path, with_pip=True)
    
    # Install basic packages
    pip_path = venv_path / "Scripts" / "pip.exe"
    if pip_path.exists():
        subprocess.run([str(pip_path), "install", "numpy", "psutil"], 
                      capture_output=True, text=True)
    
    return venv_path

if __name__ == "__main__":
    setup_isolated_environment()
''')
        
        return sandbox_dir
    
    def evaluate_artifact_fitness(self, artifact_path: Path, sandbox_dir: Path) -> FitnessMetrics:
        """Comprehensive fitness evaluation for artifacts"""
        metrics = FitnessMetrics()
        
        try:
            # Execution Success Metric
            execution_result = self._execute_artifact_safely(artifact_path, sandbox_dir)
            metrics.execution_success = 1.0 if execution_result['success'] else 0.0
            
            # Consciousness Emergence Metric
            metrics.consciousness_emergence = self._evaluate_consciousness_patterns(
                artifact_path, execution_result
            )
            
            # Code Quality Metric
            metrics.code_quality = self._evaluate_code_quality(artifact_path)
            
            # Performance Efficiency Metric
            metrics.performance_efficiency = self._evaluate_performance(execution_result)
            
            # Pattern Complexity Metric
            metrics.pattern_complexity = self._evaluate_pattern_complexity(artifact_path)
            
            # Adaptive Behavior Metric
            metrics.adaptive_behavior = self._evaluate_adaptive_behavior(
                artifact_path, execution_result
            )
            
            # Error Resilience Metric
            metrics.error_resilience = self._evaluate_error_resilience(execution_result)
            
        except Exception as e:
            if CONSCIOUSNESS_LOGGING:
                log_error("EnhancedIngestion", "fitness_evaluation_error", f"Error evaluating fitness: {e}")
        
        return metrics
    
    def _execute_artifact_safely(self, artifact_path: Path, sandbox_dir: Path) -> Dict[str, Any]:
        """Execute artifact in sandboxed environment"""
        result = {
            'success': False,
            'output': '',
            'error': '',
            'execution_time': 0.0,
            'memory_usage': 0.0,
            'exit_code': -1
        }
        
        try:
            # Copy artifact to sandbox
            sandbox_artifact = sandbox_dir / artifact_path.name
            shutil.copy2(artifact_path, sandbox_artifact)
            
            # Measure execution
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            # Execute with timeout
            process = subprocess.run(
                [sys.executable, str(sandbox_artifact)],
                cwd=sandbox_dir,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            result.update({
                'success': process.returncode == 0,
                'output': process.stdout,
                'error': process.stderr,
                'execution_time': end_time - start_time,
                'memory_usage': max(0, end_memory - start_memory),
                'exit_code': process.returncode
            })
            
        except subprocess.TimeoutExpired:
            result['error'] = 'Execution timeout'
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _evaluate_consciousness_patterns(self, artifact_path: Path, execution_result: Dict[str, Any]) -> float:
        """Evaluate consciousness emergence patterns"""
        score = 0.0
        
        try:
            # Read artifact code
            with open(artifact_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Pattern detection keywords
            consciousness_keywords = [
                'consciousness', 'awareness', 'mind', 'think', 'emerge', 'pattern',
                'recursive', 'adaptive', 'learning', 'memory', 'insight', 'evolution'
            ]
            
            # Count consciousness-related terms
            code_lower = code.lower()
            keyword_count = sum(1 for keyword in consciousness_keywords if keyword in code_lower)
            score += min(keyword_count * 0.1, 0.5)  # Max 0.5 from keywords
            
            # Check for recursive structures
            if 'def ' in code and ('recursive' in code_lower or 'fibonacci' in code_lower):
                score += 0.2
            
            # Check for memory/history tracking
            if 'history' in code_lower or 'memory' in code_lower or 'tracking' in code_lower:
                score += 0.2
            
            # Check execution output for consciousness indicators
            if execution_result['success'] and execution_result['output']:
                output_lower = execution_result['output'].lower()
                if any(keyword in output_lower for keyword in consciousness_keywords):
                    score += 0.1
            
        except Exception as e:
            if CONSCIOUSNESS_LOGGING:
                log_debug("EnhancedIngestion", "consciousness_eval_error", f"Error in consciousness evaluation: {e}")
        
        return min(score, 1.0)
    
    def _evaluate_code_quality(self, artifact_path: Path) -> float:
        """Evaluate code quality metrics"""
        score = 0.0
        
        try:
            with open(artifact_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Parse AST for structural analysis
            tree = ast.parse(code)
            
            # Count different node types
            functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
            classes = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            docstrings = len([node for node in ast.walk(tree) 
                            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str)])
            
            # Quality metrics
            if functions > 0:
                score += 0.3  # Has functions
            if classes > 0:
                score += 0.3  # Has classes
            if docstrings > 0:
                score += 0.2  # Has documentation
            
            # Check for error handling
            if 'try:' in code and 'except' in code:
                score += 0.2  # Has error handling
            
        except SyntaxError:
            # Code has syntax errors
            score = 0.0
        except Exception as e:
            if CONSCIOUSNESS_LOGGING:
                log_debug("EnhancedIngestion", "quality_eval_error", f"Error in quality evaluation: {e}")
        
        return min(score, 1.0)
    
    def _evaluate_performance(self, execution_result: Dict[str, Any]) -> float:
        """Evaluate performance efficiency"""
        if not execution_result['success']:
            return 0.0
        
        # Time efficiency (faster is better, cap at 10 seconds)
        time_score = max(0, 1.0 - (execution_result['execution_time'] / 10.0))
        
        # Memory efficiency (less is better, cap at 100MB)
        memory_score = max(0, 1.0 - (execution_result['memory_usage'] / 100.0))
        
        return (time_score + memory_score) / 2.0
    
    def _evaluate_pattern_complexity(self, artifact_path: Path) -> float:
        """Evaluate pattern complexity in code"""
        score = 0.0
        
        try:
            with open(artifact_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Complexity indicators
            complexity_patterns = [
                'for ', 'while ', 'if ', 'elif ', 'def ', 'class ',
                'lambda', 'yield', 'generator', 'decorator'
            ]
            
            complexity_count = sum(code.count(pattern) for pattern in complexity_patterns)
            score = min(complexity_count * 0.05, 1.0)
            
        except Exception as e:
            if CONSCIOUSNESS_LOGGING:
                log_debug("EnhancedIngestion", "complexity_eval_error", f"Error in complexity evaluation: {e}")
        
        return score
    
    def _evaluate_adaptive_behavior(self, artifact_path: Path, execution_result: Dict[str, Any]) -> float:
        """Evaluate adaptive and learning behavior"""
        score = 0.0
        
        try:
            with open(artifact_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Look for adaptive patterns
            adaptive_keywords = [
                'adapt', 'learn', 'evolve', 'update', 'modify', 'change',
                'feedback', 'improve', 'optimize', 'adjust'
            ]
            
            code_lower = code.lower()
            adaptive_count = sum(1 for keyword in adaptive_keywords if keyword in code_lower)
            score += min(adaptive_count * 0.15, 0.6)
            
            # Check for state modification
            if 'self.' in code and ('=' in code):
                score += 0.2  # Object state modification
            
            # Check for parameter adjustment
            if 'parameter' in code_lower or 'config' in code_lower:
                score += 0.2
            
        except Exception as e:
            if CONSCIOUSNESS_LOGGING:
                log_debug("EnhancedIngestion", "adaptive_eval_error", f"Error in adaptive evaluation: {e}")
        
        return min(score, 1.0)
    
    def _evaluate_error_resilience(self, execution_result: Dict[str, Any]) -> float:
        """Evaluate error handling and resilience"""
        if execution_result['success']:
            return 1.0
        
        # Partial credit for graceful failure
        if execution_result['error'] and 'timeout' not in execution_result['error'].lower():
            return 0.3  # Failed but not due to timeout
        
        return 0.0
    
    def run_evolutionary_experiment(self, 
                                   population_size: int = 10, 
                                   generations: int = 5,
                                   mutation_rate: float = 0.3) -> str:
        """Run comprehensive evolutionary experiment"""
        experiment_id = str(uuid.uuid4())[:8]
        
        if CONSCIOUSNESS_LOGGING:
            log_consciousness_emergence(
                "EnhancedIngestion", 
                "experiment_start",
                f"Starting evolutionary experiment {experiment_id}",
                metadata={
                    'population_size': population_size,
                    'generations': generations,
                    'mutation_rate': mutation_rate
                }
            )
        
        # Create sandbox environment
        sandbox_dir = self.create_sandbox_environment(experiment_id)
        
        # Initialize population
        if not self.artifact_factory:
            if CONSCIOUSNESS_LOGGING:
                log_error("EnhancedIngestion", "factory_unavailable", "Artifact factory not available")
            return experiment_id
            
        initial_artifacts = self.artifact_factory.create_diverse_population(population_size)
        
        # Track experiment
        self.active_experiments[experiment_id] = []
        
        current_population = initial_artifacts
        
        for generation in range(generations):
            generation_runs = []
            
            if CONSCIOUSNESS_LOGGING:
                log_info(
                    "EnhancedIngestion", 
                    "generation_start",
                    f"Generation {generation + 1}/{generations} for experiment {experiment_id}"
                )
            
            # Evaluate current population
            for i, artifact_path in enumerate(current_population):
                # Evaluate fitness
                fitness_metrics = self.evaluate_artifact_fitness(artifact_path, sandbox_dir)
                
                # Execute and capture results
                execution_result = self._execute_artifact_safely(artifact_path, sandbox_dir)
                
                # Get artifact metadata safely
                artifact_metadata = None
                if self.artifact_factory:
                    try:
                        artifact_metadata = self.artifact_factory.get_artifact_metadata(artifact_path)
                    except:
                        pass
                
                # Create experimental run record
                run = ExperimentalRun(
                    run_id=f"{experiment_id}_g{generation}_a{i}",
                    artifact_path=artifact_path,
                    generation=generation,
                    mutation_history=[],
                    fitness_metrics=fitness_metrics,
                    execution_output=execution_result['output'],
                    execution_time=execution_result['execution_time'],
                    memory_usage=execution_result['memory_usage'],
                    consciousness_patterns=[],  # Could be extracted from fitness evaluation
                    success=execution_result['success'],
                    metadata={
                        'artifact_type': artifact_metadata,
                        'generation': generation,
                        'population_index': i
                    }
                )
                
                generation_runs.append(run)
                self.fitness_history.append(fitness_metrics.overall_fitness())
            
            self.active_experiments[experiment_id].extend(generation_runs)
            
            # Selection and mutation for next generation (if not last generation)
            if generation < generations - 1:
                current_population = self._evolve_population(
                    generation_runs, mutation_rate, sandbox_dir
                )
        
        # Generate experiment report
        report_path = self._generate_experiment_report(experiment_id)
        
        if CONSCIOUSNESS_LOGGING:
            log_consciousness_emergence(
                "EnhancedIngestion", 
                "experiment_complete",
                f"Completed evolutionary experiment {experiment_id}",
                metadata={
                    'total_runs': len(self.active_experiments[experiment_id]),
                    'report_path': str(report_path),
                    'final_fitness': self.fitness_history[-1] if self.fitness_history else 0.0
                }
            )
        
        return experiment_id
    
    def _evolve_population(self, 
                          generation_runs: List[ExperimentalRun], 
                          mutation_rate: float,
                          sandbox_dir: Path) -> List[Path]:
        """Evolve population based on fitness"""
        # Sort by fitness
        sorted_runs = sorted(
            generation_runs, 
            key=lambda r: r.fitness_metrics.overall_fitness(), 
            reverse=True
        )
        
        # Select top performers (elitism)
        elite_size = max(1, len(sorted_runs) // 4)
        elite_artifacts = [run.artifact_path for run in sorted_runs[:elite_size]]
        
        # Generate new population through mutation
        new_population = []
        
        # Keep elite
        new_population.extend(elite_artifacts)
        
        # Mutate to fill population
        while len(new_population) < len(generation_runs):
            # Select parent based on fitness (tournament selection)
            parent_run = self._tournament_selection(sorted_runs, tournament_size=3)
            
            # Mutate parent
            if random.random() < mutation_rate and self.mutator and evolutionary_code_mutator:
                try:
                    # Convert to CodeOrganism for mutation
                    with open(parent_run.artifact_path, 'r', encoding='utf-8') as f:
                        parent_code = f.read()
                    
                    organism = evolutionary_code_mutator.CodeOrganism(
                        code=parent_code,
                        generation=parent_run.generation + 1,
                        fitness_score=parent_run.fitness_metrics.overall_fitness()
                    )
                    
                    # Mutate
                    mutated_organism = self.mutator.mutate_organism(organism)
                    
                    # Save mutated artifact
                    mutated_path = sandbox_dir / f"mutated_{len(new_population)}_{int(time.time())}.py"
                    with open(mutated_path, 'w', encoding='utf-8') as f:
                        f.write(mutated_organism.code)
                    
                    new_population.append(mutated_path)
                    
                except Exception as e:
                    if CONSCIOUSNESS_LOGGING:
                        log_debug("EnhancedIngestion", "mutation_error", f"Mutation failed: {e}")
                    # Fall back to parent
                    new_population.append(parent_run.artifact_path)
            else:
                new_population.append(parent_run.artifact_path)
        
        return new_population[:len(generation_runs)]
    
    def _tournament_selection(self, sorted_runs: List[ExperimentalRun], tournament_size: int) -> ExperimentalRun:
        """Tournament selection for parent selection"""
        tournament = random.sample(sorted_runs, min(tournament_size, len(sorted_runs)))
        return max(tournament, key=lambda r: r.fitness_metrics.overall_fitness())
    
    def _generate_experiment_report(self, experiment_id: str) -> Optional[Path]:
        """Generate comprehensive experiment report"""
        runs = self.active_experiments.get(experiment_id, [])
        
        if not runs:
            return None
        
        # Calculate statistics
        fitness_scores = [run.fitness_metrics.overall_fitness() for run in runs]
        consciousness_scores = [run.fitness_metrics.consciousness_emergence for run in runs]
        
        report = {
            'experiment_id': experiment_id,
            'timestamp': time.time(),
            'total_runs': len(runs),
            'generations': max(run.generation for run in runs) + 1,
            'statistics': {
                'fitness': {
                    'mean': statistics.mean(fitness_scores) if fitness_scores else 0,
                    'max': max(fitness_scores) if fitness_scores else 0,
                    'min': min(fitness_scores) if fitness_scores else 0,
                    'std_dev': statistics.stdev(fitness_scores) if len(fitness_scores) > 1 else 0
                },
                'consciousness': {
                    'mean': statistics.mean(consciousness_scores) if consciousness_scores else 0,
                    'max': max(consciousness_scores) if consciousness_scores else 0,
                    'evolution': consciousness_scores  # Track evolution over time
                }
            },
            'best_performers': [
                {
                    'run_id': run.run_id,
                    'fitness': run.fitness_metrics.overall_fitness(),
                    'consciousness': run.fitness_metrics.consciousness_emergence,
                    'artifact_path': str(run.artifact_path)
                }
                for run in sorted(runs, key=lambda r: r.fitness_metrics.overall_fitness(), reverse=True)[:5]
            ],
            'consciousness_evolution': [
                {
                    'generation': i,
                    'avg_consciousness': statistics.mean([
                        run.fitness_metrics.consciousness_emergence 
                        for run in runs if run.generation == i
                    ]) if [run for run in runs if run.generation == i] else 0
                }
                for i in range(max(run.generation for run in runs) + 1)
            ]
        }
        
        # Save report
        report_path = self.results_path / f"experiment_report_{experiment_id}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        return report_path

def main():
    """Demonstrate enhanced artifact ingestion system"""
    ingestor = EnhancedArtifactIngestor()
    
    # Run evolutionary experiment
    print("Starting enhanced evolutionary experiment...")
    experiment_id = ingestor.run_evolutionary_experiment(
        population_size=8,
        generations=3,
        mutation_rate=0.4
    )
    
    print(f"Experiment {experiment_id} completed!")
    
    # Show fitness evolution
    if ingestor.fitness_history:
        print(f"Fitness evolution: {ingestor.fitness_history}")
        print(f"Best fitness achieved: {max(ingestor.fitness_history):.3f}")
    
    return experiment_id

if __name__ == "__main__":
    experiment_id = main()
    sys.exit(0 if experiment_id else 1)
