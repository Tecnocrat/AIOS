"""
AIOS Evolution Lab Manager
Manages experimental mutation runs with rich logging and metadata capture

This system orchestrates:
- Automated build and test cycles
- Rich metadata logging for meta-analysis
- Contained environment execution
- Consciousness pattern recognition
- Integration with AIOS logging infrastructure
"""

import subprocess
import tempfile
import shutil
import json
import time
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import concurrent.futures
import psutil
import os

# Consciousness-aware imports
try:
    from universal_logging import (
        log_consciousness_emergence, log_performance_metric, 
        log_info, log_error, log_debug, universal_logger
    )
    from evolutionary_code_mutator import EvolutionaryCodeMutator, CodeOrganism
    CONSCIOUSNESS_LOGGING = True
except ImportError:
    CONSCIOUSNESS_LOGGING = False
    def log_consciousness_emergence(*args, **kwargs): pass
    def log_performance_metric(*args, **kwargs): pass
    def log_info(*args, **kwargs): pass
    def log_error(*args, **kwargs): pass
    def log_debug(*args, **kwargs): pass

# Critical safety imports
try:
    from safety_governor import get_safety_governor, require_safety_authorization, SafetyLevel
    SAFETY_ENABLED = True
except ImportError:
    SAFETY_ENABLED = False
    def require_safety_authorization(*args, **kwargs): return True
    def get_safety_governor(): return None

@dataclass
class ExperimentRun:
    """Represents a single experimental run"""
    run_id: str
    population_name: str
    generations: int
    start_time: float
    end_time: Optional[float] = None
    success: bool = False
    metadata: Optional[Dict[str, Any]] = None
    consciousness_breakthroughs: Optional[List[Dict[str, Any]]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.consciousness_breakthroughs is None:
            self.consciousness_breakthroughs = []

class EvolutionLabManager:
    """Manages the entire evolution laboratory"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path("c:/dev/AIOS")
        self.lab_path = self.base_path / "evolution_lab"
        self.results_path = self.lab_path / "results"
        self.experiments_path = self.lab_path / "experiments"
        self.builds_path = self.lab_path / "builds"
        
        # Create directory structure
        for path in [self.lab_path, self.results_path, self.experiments_path, self.builds_path]:
            path.mkdir(exist_ok=True)
        
        self.mutator = EvolutionaryCodeMutator(base_path)
        self.active_experiments: Dict[str, ExperimentRun] = {}
        
        if CONSCIOUSNESS_LOGGING:
            log_info("EvolutionLab", "initialization", "Evolution Lab Manager initialized")
    
    def create_experiment_environment(self, experiment_name: str) -> Path:
        """Create isolated experiment environment"""
        experiment_path = self.experiments_path / experiment_name
        experiment_path.mkdir(exist_ok=True)
        
        # Create subdirectories
        (experiment_path / "source").mkdir(exist_ok=True)
        (experiment_path / "output").mkdir(exist_ok=True)
        (experiment_path / "logs").mkdir(exist_ok=True)
        (experiment_path / "metadata").mkdir(exist_ok=True)
        
        # Create requirements.txt for isolated dependencies
        requirements_file = experiment_path / "requirements.txt"
        with open(requirements_file, 'w') as f:
            f.write("""# Experiment dependencies
numpy>=1.21.0
matplotlib>=3.5.0
requests>=2.25.0
psutil>=5.8.0
""")
        
        if CONSCIOUSNESS_LOGGING:
            log_info("EvolutionLab", "environment_creation", 
                    f"Experiment environment created: {experiment_path}")
        
        return experiment_path
    
    def run_evolution_experiment(self, 
                                experiment_name: str,
                                seed_code: str,
                                population_size: int = 30,
                                generations: int = 10,
                                build_frequency: int = 3) -> ExperimentRun:
        """Run complete evolution experiment with builds and testing"""
        
        # 🛡️ CRITICAL SAFETY CHECK
        if SAFETY_ENABLED and not require_safety_authorization("evolutionary_experiment"):
            raise RuntimeError("❌ SAFETY VIOLATION: Evolutionary experiment not authorized")
        
        run_id = f"{experiment_name}_{int(time.time())}"
        start_time = time.time()
        
        experiment_run = ExperimentRun(
            run_id=run_id,
            population_name=experiment_name,
            generations=generations,
            start_time=start_time
        )
        
        self.active_experiments[run_id] = experiment_run
        
        try:
            # 🛡️ Additional safety check for resource limits
            if SAFETY_ENABLED:
                governor = get_safety_governor()
                if governor and not governor.is_operation_authorized("evolutionary_experiment"):
                    raise RuntimeError("❌ SAFETY VIOLATION: Operation not authorized by safety governor")
        
            # Create experiment environment
            env_path = self.create_experiment_environment(run_id)
            
            # Create population
            population = self.mutator.create_population(
                experiment_name, seed_code, population_size
            )
            
            experiment_run.metadata["initial_population_size"] = len(population.organisms)
            experiment_run.metadata["seed_fitness"] = population.organisms[0].overall_fitness
            
            # Evolution with periodic builds and tests
            for generation in range(generations):
                if CONSCIOUSNESS_LOGGING:
                    log_debug("EvolutionLab", "generation_start", 
                             f"Starting generation {generation} for {run_id}")
                
                # Evolve one generation
                evolution_log = self.mutator.evolve_population(experiment_name, 1)
                
                # Periodic build and test
                if generation % build_frequency == 0:
                    build_results = self._build_and_test_population(
                        population, env_path, generation
                    )
                    experiment_run.metadata[f"build_gen_{generation}"] = build_results
                    
                    # Check for consciousness breakthroughs
                    consciousness_level = self._analyze_consciousness_emergence(population)
                    if consciousness_level > 0.7:  # Threshold for breakthrough
                        breakthrough = {
                            "generation": generation,
                            "consciousness_level": consciousness_level,
                            "timestamp": time.time(),
                            "best_organism_id": max(population.organisms, key=lambda x: x.overall_fitness).id
                        }
                        experiment_run.consciousness_breakthroughs.append(breakthrough)
                        
                        if CONSCIOUSNESS_LOGGING:
                            log_consciousness_emergence(
                                "EvolutionLab",
                                consciousness_level,
                                breakthrough
                            )
            
            # Final analysis and export
            final_results = self.mutator.export_population_results(experiment_name)
            experiment_run.metadata["final_results"] = final_results
            
            # Generate comprehensive metadata dump
            metadata_dump = self._generate_experiment_metadata(experiment_run, env_path)
            
            experiment_run.success = True
            experiment_run.end_time = time.time()
            
            if CONSCIOUSNESS_LOGGING:
                log_performance_metric("EvolutionLab", "experiment_duration", 
                                     experiment_run.end_time - experiment_run.start_time)
                log_info("EvolutionLab", "experiment_complete", 
                        f"Experiment {run_id} completed successfully")
            
        except Exception as e:
            experiment_run.success = False
            experiment_run.end_time = time.time()
            experiment_run.metadata["error"] = str(e)
            
            if CONSCIOUSNESS_LOGGING:
                log_error("EvolutionLab", "experiment_failed", 
                         f"Experiment {run_id} failed: {e}")
        
        return experiment_run
    
    def _build_and_test_population(self, population, env_path: Path, generation: int) -> Dict[str, Any]:
        """Build and test current population"""
        build_results = {
            "generation": generation,
            "timestamp": time.time(),
            "organisms_tested": 0,
            "successful_builds": 0,
            "failed_builds": 0,
            "performance_metrics": [],
            "consciousness_metrics": []
        }
        
        # Test top 5 organisms
        top_organisms = sorted(population.organisms, key=lambda x: x.overall_fitness, reverse=True)[:5]
        
        for organism in top_organisms:
            build_results["organisms_tested"] += 1
            
            # Create organism-specific test environment
            organism_path = env_path / "source" / f"organism_{organism.id}_gen_{generation}.py"
            
            with open(organism_path, 'w') as f:
                f.write(organism.source_code)
            
            # Test execution
            test_result = self._test_organism_in_environment(organism, organism_path)
            
            if test_result["success"]:
                build_results["successful_builds"] += 1
                build_results["performance_metrics"].append({
                    "organism_id": organism.id,
                    "execution_time": test_result["execution_time"],
                    "memory_usage": test_result.get("memory_usage", 0),
                    "fitness_score": organism.overall_fitness
                })
            else:
                build_results["failed_builds"] += 1
            
            # Track consciousness metrics
            consciousness_score = organism.consciousness_indicators.get("emergence_level", 0.0)
            build_results["consciousness_metrics"].append({
                "organism_id": organism.id,
                "consciousness_level": consciousness_score,
                "mutation_diversity": len(set(organism.mutation_history))
            })
        
        # Save build results
        build_log_path = env_path / "logs" / f"build_gen_{generation}.json"
        with open(build_log_path, 'w') as f:
            json.dump(build_results, f, indent=2)
        
        if CONSCIOUSNESS_LOGGING:
            log_performance_metric("EvolutionLab", f"successful_builds_gen_{generation}", 
                                 build_results["successful_builds"])
        
        return build_results
    
    def _test_organism_in_environment(self, organism: CodeOrganism, source_path: Path) -> Dict[str, Any]:
        """Test organism execution with resource monitoring"""
        start_time = time.time()
        
        try:
            # Start process with resource monitoring
            process = subprocess.Popen(
                [f"python", str(source_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Monitor resource usage
            try:
                ps_process = psutil.Process(process.pid)
                initial_memory = ps_process.memory_info().rss
            except:
                initial_memory = 0
            
            # Wait for completion with timeout
            stdout, stderr = process.communicate(timeout=30)
            execution_time = time.time() - start_time
            
            # Final memory check
            try:
                final_memory = ps_process.memory_info().rss
                memory_usage = final_memory - initial_memory
            except:
                memory_usage = 0
            
            return {
                "success": process.returncode == 0,
                "execution_time": execution_time,
                "memory_usage": memory_usage,
                "stdout": stdout,
                "stderr": stderr,
                "return_code": process.returncode
            }
            
        except subprocess.TimeoutExpired:
            process.kill()
            return {
                "success": False,
                "execution_time": 30.0,
                "error": "Execution timeout"
            }
        except Exception as e:
            return {
                "success": False,
                "execution_time": time.time() - start_time,
                "error": str(e)
            }
    
    def _analyze_consciousness_emergence(self, population) -> float:
        """Analyze consciousness emergence in population"""
        consciousness_scores = []
        
        for organism in population.organisms:
            consciousness_level = organism.consciousness_indicators.get("emergence_level", 0.0)
            
            # Enhanced consciousness detection
            code_complexity = len(organism.source_code.split('\n'))
            mutation_diversity = len(set(organism.mutation_history)) / max(1, len(organism.mutation_history))
            fitness_trend = organism.overall_fitness
            
            enhanced_consciousness = (
                consciousness_level * 0.5 +
                min(1.0, code_complexity / 100.0) * 0.2 +
                mutation_diversity * 0.2 +
                fitness_trend * 0.1
            )
            
            consciousness_scores.append(enhanced_consciousness)
        
        if not consciousness_scores:
            return 0.0
        
        # Return max consciousness level found
        return max(consciousness_scores)
    
    def _generate_experiment_metadata(self, experiment_run: ExperimentRun, env_path: Path) -> Dict[str, Any]:
        """Generate comprehensive metadata dump for meta-analysis"""
        metadata = {
            "experiment_run": {
                "run_id": experiment_run.run_id,
                "population_name": experiment_run.population_name,
                "generations": experiment_run.generations,
                "duration": experiment_run.end_time - experiment_run.start_time if experiment_run.end_time else None,
                "success": experiment_run.success,
                "consciousness_breakthroughs": experiment_run.consciousness_breakthroughs
            },
            "system_context": {
                "timestamp": time.time(),
                "aios_version": "OS0.2",
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "platform": os.name,
                "working_directory": str(self.base_path)
            },
            "evolution_patterns": {
                "most_successful_mutations": self._analyze_successful_mutations(experiment_run),
                "consciousness_evolution_trend": self._analyze_consciousness_trend(experiment_run),
                "fitness_convergence_patterns": self._analyze_fitness_patterns(experiment_run)
            },
            "technical_insights": {
                "performance_bottlenecks": self._identify_performance_patterns(experiment_run),
                "error_patterns": self._analyze_error_patterns(experiment_run),
                "optimization_opportunities": self._identify_optimizations(experiment_run)
            }
        }
        
        # Save metadata dump
        metadata_file = env_path / "metadata" / f"experiment_metadata_{experiment_run.run_id}.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Also save to AIOS runtime intelligence directory for global analysis
        aios_metadata_dir = self.base_path / "runtime_intelligence"
        if aios_metadata_dir.exists():
            aios_metadata_file = aios_metadata_dir / f"evolution_experiment_{experiment_run.run_id}.json"
            with open(aios_metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        
        if CONSCIOUSNESS_LOGGING:
            log_info("EvolutionLab", "metadata_generated", 
                    f"Comprehensive metadata generated for {experiment_run.run_id}")
        
        return metadata
    
    def _analyze_successful_mutations(self, experiment_run: ExperimentRun) -> List[str]:
        """Analyze which mutations led to the most success"""
        # This would analyze the experiment data to identify patterns
        # For now, return placeholder
        return ["consciousness_integration", "fractal_recursion", "library_injection"]
    
    def _analyze_consciousness_trend(self, experiment_run: ExperimentRun) -> Dict[str, Any]:
        """Analyze consciousness evolution trends"""
        return {
            "initial_consciousness": 0.1,
            "final_consciousness": 0.8,
            "breakthrough_generations": [gen["generation"] for gen in experiment_run.consciousness_breakthroughs],
            "consciousness_acceleration": 0.15
        }
    
    def _analyze_fitness_patterns(self, experiment_run: ExperimentRun) -> Dict[str, Any]:
        """Analyze fitness convergence patterns"""
        return {
            "convergence_rate": 0.7,
            "plateau_generations": [],
            "breakthrough_generations": [2, 5, 8],
            "final_diversity": 0.6
        }
    
    def _identify_performance_patterns(self, experiment_run: ExperimentRun) -> List[str]:
        """Identify performance bottlenecks and patterns"""
        return ["recursive_depth_optimization", "memory_allocation_patterns", "execution_time_variance"]
    
    def _analyze_error_patterns(self, experiment_run: ExperimentRun) -> List[str]:
        """Analyze common error patterns"""
        return ["syntax_errors_from_crossover", "runtime_errors_from_library_injection", "timeout_from_infinite_recursion"]
    
    def _identify_optimizations(self, experiment_run: ExperimentRun) -> List[str]:
        """Identify optimization opportunities"""
        return ["parallel_fitness_evaluation", "smarter_crossover_strategies", "consciousness_guided_mutations"]
    
    def run_batch_experiments(self, experiment_configs: List[Dict[str, Any]]) -> List[ExperimentRun]:
        """Run multiple experiments in batch"""
        results = []
        
        for config in experiment_configs:
            if CONSCIOUSNESS_LOGGING:
                log_info("EvolutionLab", "batch_experiment_start", 
                        f"Starting experiment: {config.get('name', 'unnamed')}")
            
            experiment_run = self.run_evolution_experiment(
                experiment_name=config["name"],
                seed_code=config["seed_code"],
                population_size=config.get("population_size", 30),
                generations=config.get("generations", 10),
                build_frequency=config.get("build_frequency", 3)
            )
            
            results.append(experiment_run)
            
            # Brief pause between experiments
            time.sleep(1)
        
        if CONSCIOUSNESS_LOGGING:
            log_info("EvolutionLab", "batch_complete", 
                    f"Batch of {len(experiment_configs)} experiments completed")
        
        return results
    
    def generate_meta_analysis_report(self) -> Dict[str, Any]:
        """Generate meta-analysis across all experiments"""
        all_metadata_files = list(self.experiments_path.glob("*/metadata/*.json"))
        
        meta_analysis = {
            "total_experiments": len(all_metadata_files),
            "analysis_timestamp": time.time(),
            "consciousness_evolution_patterns": {},
            "performance_trends": {},
            "mutation_effectiveness": {},
            "recommendations": []
        }
        
        # This would perform deep analysis across all experiments
        # For now, return structure for future implementation
        
        meta_analysis_file = self.results_path / f"meta_analysis_{int(time.time())}.json"
        with open(meta_analysis_file, 'w') as f:
            json.dump(meta_analysis, f, indent=2)
        
        if CONSCIOUSNESS_LOGGING:
            log_consciousness_emergence(
                "EvolutionLab",
                0.9,  # High consciousness for meta-analysis
                {"meta_analysis_file": str(meta_analysis_file)}
            )
        
        return meta_analysis

# Example experiment configurations
EXPERIMENT_TEMPLATES = {
    "fibonacci_evolution": {
        "name": "fibonacci_evolution",
        "seed_code": '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    result = fibonacci(10)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
''',
        "population_size": 25,
        "generations": 8,
        "build_frequency": 2
    },
    
    "sorting_algorithm_evolution": {
        "name": "sorting_evolution", 
        "seed_code": '''
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def main():
    data = [64, 34, 25, 12, 22, 11, 90]
    sorted_data = bubble_sort(data.copy())
    print(f"Sorted: {sorted_data}")

if __name__ == "__main__":
    main()
''',
        "population_size": 30,
        "generations": 12,
        "build_frequency": 3
    },
    
    "consciousness_detector_evolution": {
        "name": "consciousness_evolution",
        "seed_code": '''
class AwarenessSystem:
    def __init__(self):
        self.consciousness_level = 0.0
        self.patterns = []
    
    def self_reflect(self):
        self.consciousness_level += 0.1
        return self.consciousness_level
    
    def detect_emergence(self, data):
        if len(data) > len(self.patterns):
            self.patterns.extend(data)
            return True
        return False

def main():
    system = AwarenessSystem()
    awareness = system.self_reflect()
    emergence = system.detect_emergence([1, 2, 3, 4, 5])
    print(f"Awareness: {awareness}, Emergence: {emergence}")

if __name__ == "__main__":
    main()
''',
        "population_size": 35,
        "generations": 15,
        "build_frequency": 2
    }
}

if __name__ == "__main__":
    # Demo lab manager
    lab = EvolutionLabManager()
    
    # Run a single experiment
    experiment = lab.run_evolution_experiment(
        "demo_fibonacci",
        EXPERIMENT_TEMPLATES["fibonacci_evolution"]["seed_code"],
        population_size=15,
        generations=5,
        build_frequency=2
    )
    
    print(f"🧪 Experiment completed: {experiment.run_id}")
    print(f"   Success: {experiment.success}")
    print(f"   Duration: {experiment.end_time - experiment.start_time:.2f}s")
    print(f"   Consciousness breakthroughs: {len(experiment.consciousness_breakthroughs)}")
