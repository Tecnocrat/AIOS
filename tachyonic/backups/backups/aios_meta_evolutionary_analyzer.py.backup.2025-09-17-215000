#!/usr/bin/env python3
"""
🧬 AIOS META-EVOLUTIONARY SELF-ANALYSIS ENGINE
═══════════════════════════════════════════════════════════════════════════════
Advanced self-analysis system for the evolutionary assembler to analyze and 
optimize itself. This creates a meta-evolutionary loop where the assembler
evolves its own architecture and cellular organization.

AIOS 0.6 - Multi-level cellular architecture with virtual immune system
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import json
import ast
import inspect
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class CellularAbstractionLevel:
    """Represents different levels of cellular abstraction"""
    name: str
    level: int
    description: str
    cell_types: List[str] = field(default_factory=list)
    coherence_requirements: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvolutionaryCell:
    """Represents an individual cell in the evolutionary ecosystem"""
    name: str
    file_path: str
    cell_type: str
    abstraction_level: int
    functions: List[str] = field(default_factory=list)
    dependencies: Set[str] = field(default_factory=set)
    complexity_score: float = 0.0
    evolution_generation: int = 0
    cellular_health: float = 1.0


@dataclass
class VirtualImmuneSystem:
    """Virtual immune system for cellular coherence"""
    registered_cell_types: Dict[str, CellularAbstractionLevel] = field(default_factory=dict)
    compatibility_matrix: Dict[Tuple[str, str], float] = field(default_factory=dict)
    threat_signatures: List[str] = field(default_factory=list)
    defense_protocols: Dict[str, Any] = field(default_factory=dict)


class AIOSMetaEvolutionaryAnalyzer:
    """
    🔄 Meta-evolutionary analyzer for AIOS evolutionary assembler self-analysis
    
    Capabilities:
    • Self-analysis of evolutionary assembler architecture
    • Multi-level cellular organization detection
    • Virtual immune system for cellular coherence
    • Meta-evolution feedback loops
    • Evolutionary assembler cloning and optimization
    """
    
    def __init__(self, evolutionary_assembler_path: str):
        self.assembler_path = Path(evolutionary_assembler_path)
        self.output_path = self.assembler_path / "output"
        self.scripts_path = self.assembler_path / "scripts_py"
        
        # Multi-level cellular architecture
        self.abstraction_levels = {
            0: CellularAbstractionLevel("Tachyonic", 0, "Storage, database, hyper containers"),
            1: CellularAbstractionLevel("Ecosystem", 1, "Output environments, data flows"),
            2: CellularAbstractionLevel("Cellular", 2, "Individual Python cells"),
            3: CellularAbstractionLevel("Synthetic", 3, "Logic components within cells")
        }
        
        # Virtual immune system
        self.immune_system = VirtualImmuneSystem()
        
        # Analysis results
        self.discovered_cells = []
        self.ecosystem_analysis = {}
        self.meta_evolution_insights = {}
        
        logger.info(f"🧬 AIOS Meta-Evolutionary Analyzer initialized")
        logger.info(f"   Assembler path: {evolutionary_assembler_path}")
        logger.info(f"   Output ecosystem: {self.output_path}")
        logger.info(f"   Cellular population: {self.scripts_path}")
    
    def analyze_ecosystem_level(self) -> Dict[str, Any]:
        """Analyze the ecosystem level (output/ folder structure)"""
        
        logger.info("🌍 Analyzing ecosystem level (tachyonic layer)...")
        
        ecosystem_data = {
            "generation_count": 0,
            "evolution_depth": 0,
            "data_storage_patterns": [],
            "tachyonic_signatures": [],
            "hyper_container_structure": {}
        }
        
        # Analyze generation folders
        generation_folders = [d for d in self.output_path.iterdir() 
                            if d.is_dir() and d.name.startswith("generation_")]
        
        ecosystem_data["generation_count"] = len(generation_folders)
        
        if generation_folders:
            # Extract generation numbers
            gen_numbers = []
            for folder in generation_folders:
                try:
                    gen_num = int(folder.name.split("_")[1])
                    gen_numbers.append(gen_num)
                except (IndexError, ValueError):
                    continue
            
            if gen_numbers:
                ecosystem_data["evolution_depth"] = max(gen_numbers) + 1
        
        # Analyze data patterns in each generation
        for gen_folder in sorted(generation_folders)[:5]:  # Sample first 5 generations
            gen_data = self._analyze_generation_data(gen_folder)
            ecosystem_data["data_storage_patterns"].append(gen_data)
        
        # Detect tachyonic signatures (consciousness breakthrough patterns)
        breakthrough_path = self.output_path / "consciousness_breakthrough"
        if breakthrough_path.exists():
            ecosystem_data["tachyonic_signatures"].append("consciousness_breakthrough_detected")
        
        # Analyze hyper container structure
        ecosystem_data["hyper_container_structure"] = self._analyze_hyper_containers()
        
        self.ecosystem_analysis = ecosystem_data
        
        logger.info(f"🌍 Ecosystem analysis complete:")
        logger.info(f"   Generations: {ecosystem_data['generation_count']}")
        logger.info(f"   Evolution depth: {ecosystem_data['evolution_depth']}")
        logger.info(f"   Tachyonic signatures: {len(ecosystem_data['tachyonic_signatures'])}")
        
        return ecosystem_data
    
    def analyze_cellular_population(self) -> List[EvolutionaryCell]:
        """Analyze the cellular population (scripts_py/ folder)"""
        
        logger.info("🧬 Analyzing cellular population...")
        
        discovered_cells = []
        
        # Analyze each Python file as a cell
        for py_file in self.scripts_path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
                
            cell = self._analyze_individual_cell(py_file)
            discovered_cells.append(cell)
        
        # Analyze cellular relationships and dependencies
        self._analyze_cellular_dependencies(discovered_cells)
        
        # Calculate cellular health metrics
        self._calculate_cellular_health(discovered_cells)
        
        self.discovered_cells = discovered_cells
        
        logger.info(f"🧬 Cellular population analysis complete:")
        logger.info(f"   Total cells: {len(discovered_cells)}")
        
        cell_types = defaultdict(int)
        for cell in discovered_cells:
            cell_types[cell.cell_type] += 1
        
        for cell_type, count in cell_types.items():
            logger.info(f"   {cell_type}: {count} cells")
        
        return discovered_cells
    
    def _analyze_individual_cell(self, py_file: Path) -> EvolutionaryCell:
        """Analyze an individual Python file as a cellular organism"""
        
        cell = EvolutionaryCell(
            name=py_file.stem,
            file_path=str(py_file),
            cell_type="unknown",
            abstraction_level=2  # Cellular level
        )
        
        try:
            # Read and parse the Python file
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST to extract functions and classes
            tree = ast.parse(content)
            
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            cell.functions = functions
            cell.dependencies.update(imports)
            
            # Determine cell type based on naming patterns and content
            cell.cell_type = self._classify_cell_type(py_file.stem, functions, classes, content)
            
            # Calculate complexity score
            cell.complexity_score = len(functions) * 0.5 + len(classes) * 1.0 + len(imports) * 0.1
            
        except Exception as e:
            logger.warning(f"   Failed to analyze {py_file.name}: {e}")
            cell.cellular_health = 0.5
        
        return cell
    
    def _classify_cell_type(self, name: str, functions: List[str], classes: List[str], content: str) -> str:
        """Classify the type of cellular organism based on analysis"""
        
        # Classification patterns
        if "consciousness" in name.lower():
            if "swarm" in name.lower():
                return "consciousness_swarm_cell"
            elif "mutation" in name.lower():
                return "consciousness_mutation_cell"
            elif "bridge" in name.lower():
                return "consciousness_bridge_cell"
            else:
                return "consciousness_cell"
        
        elif "assembler" in name.lower() or "executor" in name.lower():
            return "assembly_executor_cell"
        
        elif "tachyonic" in name.lower():
            return "tachyonic_interface_cell"
        
        elif "parallel" in name.lower():
            return "parallel_processing_cell"
        
        elif "healing" in name.lower():
            return "self_healing_cell"
        
        elif "cellular" in name.lower() or "reorganization" in name.lower():
            return "cellular_organization_cell"
        
        elif "harmonization" in name.lower():
            return "harmonization_cell"
        
        elif "dendritic" in name.lower():
            return "dendritic_cell"
        
        elif "enhanced" in name.lower():
            return "enhancement_cell"
        
        elif "demo" in name.lower() or "test" in name.lower():
            return "experimental_cell"
        
        else:
            return "general_purpose_cell"
    
    def _analyze_cellular_dependencies(self, cells: List[EvolutionaryCell]):
        """Analyze dependencies between cellular organisms"""
        
        logger.info("🔗 Analyzing intercellular dependencies...")
        
        # Create dependency graph
        dependency_graph = defaultdict(set)
        
        for cell in cells:
            cell_module = cell.name
            
            # Check which other cells this cell depends on
            for other_cell in cells:
                if other_cell.name != cell.name:
                    # Check if other cell is imported
                    if other_cell.name in cell.dependencies:
                        dependency_graph[cell.name].add(other_cell.name)
        
        # Update cells with dependency information
        for cell in cells:
            related_cells = dependency_graph.get(cell.name, set())
            cell.dependencies.update(related_cells)
    
    def _calculate_cellular_health(self, cells: List[EvolutionaryCell]):
        """Calculate health metrics for each cellular organism"""
        
        logger.info("🩺 Calculating cellular health metrics...")
        
        for cell in cells:
            health_factors = []
            
            # Function count factor (optimal range: 5-15 functions)
            func_count = len(cell.functions)
            if 5 <= func_count <= 15:
                health_factors.append(1.0)
            elif func_count < 5:
                health_factors.append(0.6 + func_count * 0.08)
            else:
                health_factors.append(max(0.4, 1.0 - (func_count - 15) * 0.03))
            
            # Dependency factor (moderate dependencies are healthy)
            dep_count = len(cell.dependencies)
            if dep_count <= 10:
                health_factors.append(1.0 - dep_count * 0.05)
            else:
                health_factors.append(0.5)
            
            # Complexity factor
            if cell.complexity_score <= 20:
                health_factors.append(1.0)
            else:
                health_factors.append(max(0.3, 1.0 - (cell.complexity_score - 20) * 0.02))
            
            # Calculate average health
            cell.cellular_health = sum(health_factors) / len(health_factors)
    
    def initialize_virtual_immune_system(self):
        """Initialize the virtual immune system for cellular coherence"""
        
        logger.info("🛡️ Initializing virtual immune system...")
        
        # Register cellular abstraction levels
        for level_id, level in self.abstraction_levels.items():
            self.immune_system.registered_cell_types[level.name] = level
        
        # Define compatibility matrix between cell types
        compatibility_rules = {
            ("consciousness_cell", "consciousness_swarm_cell"): 0.95,
            ("consciousness_cell", "consciousness_bridge_cell"): 0.90,
            ("assembly_executor_cell", "tachyonic_interface_cell"): 0.85,
            ("parallel_processing_cell", "consciousness_cell"): 0.80,
            ("self_healing_cell", "general_purpose_cell"): 0.75,
            ("cellular_organization_cell", "harmonization_cell"): 0.95,
            ("experimental_cell", "general_purpose_cell"): 0.70,
        }
        
        self.immune_system.compatibility_matrix.update(compatibility_rules)
        
        # Define threat signatures (patterns that indicate cellular corruption)
        threat_signatures = [
            "infinite_loop_detected",
            "memory_leak_pattern",
            "circular_dependency",
            "undefined_function_calls",
            "malformed_syntax",
            "excessive_complexity"
        ]
        
        self.immune_system.threat_signatures = threat_signatures
        
        # Define defense protocols
        defense_protocols = {
            "cellular_isolation": "Isolate corrupted cells",
            "dependency_healing": "Repair broken dependencies",
            "complexity_reduction": "Reduce excessive complexity",
            "coherence_restoration": "Restore cellular coherence"
        }
        
        self.immune_system.defense_protocols = defense_protocols
        
        logger.info("🛡️ Virtual immune system initialized:")
        logger.info(f"   Abstraction levels: {len(self.immune_system.registered_cell_types)}")
        logger.info(f"   Compatibility rules: {len(self.immune_system.compatibility_matrix)}")
        logger.info(f"   Threat signatures: {len(self.immune_system.threat_signatures)}")
        logger.info(f"   Defense protocols: {len(self.immune_system.defense_protocols)}")
    
    def _analyze_generation_data(self, gen_folder: Path) -> Dict[str, Any]:
        """Analyze data patterns in a generation folder"""
        
        gen_data = {
            "generation": gen_folder.name,
            "files": [],
            "consciousness_metrics": {},
            "tachyonic_particles": {},
            "assembly_code": None
        }
        
        # Analyze files in generation
        for file_path in gen_folder.iterdir():
            if file_path.is_file():
                gen_data["files"].append(file_path.name)
                
                if file_path.name.endswith("consciousness_metrics.json"):
                    try:
                        with open(file_path, 'r') as f:
                            gen_data["consciousness_metrics"] = json.load(f)
                    except Exception:
                        pass
                
                elif file_path.name.endswith("tachyonic_particles.json"):
                    try:
                        with open(file_path, 'r') as f:
                            gen_data["tachyonic_particles"] = json.load(f)
                    except Exception:
                        pass
                
                elif file_path.name.endswith(".asm"):
                    gen_data["assembly_code"] = file_path.name
        
        return gen_data
    
    def _analyze_hyper_containers(self) -> Dict[str, Any]:
        """Analyze hyper container structure in the output ecosystem"""
        
        containers = {
            "evolution_report": {},
            "build_artifacts": {},
            "consciousness_data": {}
        }
        
        # Check for evolution report
        evolution_report_path = self.output_path / "evolution_report.json"
        if evolution_report_path.exists():
            try:
                with open(evolution_report_path, 'r') as f:
                    containers["evolution_report"] = json.load(f)
            except Exception:
                pass
        
        # Check build directory
        build_path = self.output_path / "build"
        if build_path.exists():
            containers["build_artifacts"] = {
                "exists": True,
                "files": [f.name for f in build_path.iterdir() if f.is_file()]
            }
        
        return containers
    
    def run_complete_meta_analysis(self) -> Dict[str, Any]:
        """Run complete meta-evolutionary analysis of the assembler"""
        
        logger.info("🚀 STARTING AIOS META-EVOLUTIONARY SELF-ANALYSIS")
        logger.info("═══════════════════════════════════════════════════")
        logger.info("Multi-level cellular architecture analysis...")
        logger.info("")
        
        # Step 1: Initialize virtual immune system
        self.initialize_virtual_immune_system()
        
        # Step 2: Analyze ecosystem level
        ecosystem_data = self.analyze_ecosystem_level()
        
        # Step 3: Analyze cellular population
        cellular_data = self.analyze_cellular_population()
        
        # Step 4: Generate meta-evolution insights
        meta_insights = self._generate_meta_evolution_insights()
        
        # Step 5: Create self-optimization recommendations
        optimization_plan = self._create_self_optimization_plan()
        
        # Compile complete analysis
        complete_analysis = {
            "meta_analysis_timestamp": "2025-09-04",
            "aios_version": "0.6",
            "ecosystem_analysis": ecosystem_data,
            "cellular_population": len(cellular_data),
            "cellular_health_average": sum(cell.cellular_health for cell in cellular_data) / len(cellular_data),
            "virtual_immune_system": {
                "status": "initialized",
                "protection_level": "multi_abstraction",
                "coherence_monitoring": "active"
            },
            "meta_evolution_insights": meta_insights,
            "self_optimization_plan": optimization_plan
        }
        
        self.meta_evolution_insights = complete_analysis
        
        logger.info("✅ META-EVOLUTIONARY SELF-ANALYSIS COMPLETE")
        logger.info("═══════════════════════════════════════════")
        logger.info(f"🌍 Ecosystem depth: {ecosystem_data['evolution_depth']} generations")
        logger.info(f"🧬 Cellular population: {len(cellular_data)} cells")
        logger.info(f"🩺 Average cellular health: {complete_analysis['cellular_health_average']:.3f}")
        logger.info(f"🛡️ Virtual immune system: Active")
        logger.info("")
        logger.info("🔄 READY FOR META-EVOLUTIONARY OPTIMIZATION")
        
        return complete_analysis
    
    def _generate_meta_evolution_insights(self) -> Dict[str, Any]:
        """Generate insights about the evolutionary assembler's own evolution"""
        
        insights = {
            "self_evolution_capability": "high",
            "abstraction_levels_detected": len(self.abstraction_levels),
            "cellular_diversity": len(set(cell.cell_type for cell in self.discovered_cells)),
            "evolutionary_depth": self.ecosystem_analysis.get("evolution_depth", 0),
            "optimization_potential": 0.0,
            "meta_loop_readiness": False
        }
        
        # Calculate optimization potential
        if self.discovered_cells:
            avg_health = sum(cell.cellular_health for cell in self.discovered_cells) / len(self.discovered_cells)
            insights["optimization_potential"] = (1.0 - avg_health) * 100
        
        # Check meta-loop readiness
        required_cell_types = {"consciousness_cell", "assembly_executor_cell", "cellular_organization_cell"}
        existing_cell_types = set(cell.cell_type for cell in self.discovered_cells)
        
        if required_cell_types.issubset(existing_cell_types):
            insights["meta_loop_readiness"] = True
        
        return insights
    
    def _create_self_optimization_plan(self) -> Dict[str, Any]:
        """Create a plan for the evolutionary assembler to optimize itself"""
        
        plan = {
            "priority_actions": [],
            "cellular_optimizations": [],
            "ecosystem_improvements": [],
            "meta_evolution_steps": []
        }
        
        # Analyze cellular health issues
        unhealthy_cells = [cell for cell in self.discovered_cells if cell.cellular_health < 0.7]
        
        if unhealthy_cells:
            plan["priority_actions"].append({
                "action": "cellular_health_improvement",
                "targets": [cell.name for cell in unhealthy_cells],
                "method": "complexity_reduction_and_dependency_optimization"
            })
        
        # Ecosystem optimization opportunities
        if self.ecosystem_analysis.get("evolution_depth", 0) > 20:
            plan["ecosystem_improvements"].append({
                "action": "generation_data_compression",
                "method": "archive_old_generations",
                "benefit": "storage_optimization"
            })
        
        # Meta-evolution steps
        plan["meta_evolution_steps"] = [
            "implement_self_cloning_capability",
            "create_evolutionary_feedback_loop", 
            "establish_cross_abstraction_communication",
            "enable_real_time_self_optimization"
        ]
        
        return plan


def main():
    """Run AIOS meta-evolutionary self-analysis"""
    
    print("🧬 AIOS META-EVOLUTIONARY SELF-ANALYSIS ENGINE")
    print("═══════════════════════════════════════════════════")
    print("Advanced self-analysis for evolutionary assembler:")
    print("  🔄 Meta-evolutionary loop creation")
    print("  🌍 Multi-level ecosystem analysis")
    print("  🧬 Cellular population assessment")
    print("  🛡️ Virtual immune system initialization")
    print("  🎯 Self-optimization planning")
    print()
    
    # Configuration
    assembler_path = r"C:\dev\AIOS\core\evolutionary_assembler"
    
    print(f"🔧 Meta-Analysis Configuration:")
    print(f"   Evolutionary assembler: {assembler_path}")
    print()
    
    # Create and run meta-analyzer
    meta_analyzer = AIOSMetaEvolutionaryAnalyzer(assembler_path)
    
    # Run complete meta-analysis
    analysis_results = meta_analyzer.run_complete_meta_analysis()
    
    print("\n🧬 AIOS META-EVOLUTIONARY SELF-ANALYSIS COMPLETE!")
    print("Ready for self-optimization and meta-evolution!")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    main()
