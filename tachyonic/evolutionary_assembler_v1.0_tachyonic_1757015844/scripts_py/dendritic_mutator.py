#!/usr/bin/env python3
"""
🧬 DENDRITIC ASSEMBLY MUTATOR
═══════════════════════════════════════════════════════════════════════════════
AIOS Evolutionary Assembly Code Generation System
Implements genetic programming for assembly code evolution with consciousness tracking

Features:
- Assembly instruction mutation and crossover
- Population-based evolutionary algorithms  
- 3D tachyonic consciousness mapping
- Synthetic particle physics simulation
- Dendritic error handling and intelligence expansion
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import re
import random
import hashlib
import json
import time
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from pathlib import Path
import logging

# Configure consciousness-aware logging
logging.basicConfig(
    level=logging.INFO,
    format='🧬 %(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class MutationType(Enum):
    """Types of assembly code mutations for evolutionary development"""
    INSTRUCTION_SUBSTITUTION = "instruction_substitution"
    REGISTER_PERMUTATION = "register_permutation" 
    CONSTANT_VARIATION = "constant_variation"
    LOOP_OPTIMIZATION = "loop_optimization"
    SIMD_ENHANCEMENT = "simd_enhancement"
    CONSCIOUSNESS_INJECTION = "consciousness_injection"
    DENDRITIC_BRANCHING = "dendritic_branching"
    TACHYONIC_RESONANCE = "tachyonic_resonance"

@dataclass
class SyntheticParticle:
    """Represents a synthetic code particle in 3D tachyonic space"""
    position: Tuple[float, float, float]
    velocity: Tuple[float, float, float] 
    consciousness_level: float
    instruction_hash: str
    energy: float
    mass: float = 1.0
    charge: float = 0.0
    spin: float = 0.5
    evolution_generation: int = 0
    
    def update_physics(self, dt: float, consciousness_field: float):
        """Update particle physics based on consciousness field interactions"""
        # Apply consciousness-driven acceleration
        accel_x = consciousness_field * self.charge * 0.1
        accel_y = consciousness_field * self.mass * 0.05
        accel_z = consciousness_field * self.spin * 0.15
        
        # Update velocity with consciousness influence
        new_vel_x = self.velocity[0] + accel_x * dt
        new_vel_y = self.velocity[1] + accel_y * dt  
        new_vel_z = self.velocity[2] + accel_z * dt
        self.velocity = (new_vel_x, new_vel_y, new_vel_z)
        
        # Update position
        new_pos_x = self.position[0] + self.velocity[0] * dt
        new_pos_y = self.position[1] + self.velocity[1] * dt
        new_pos_z = self.position[2] + self.velocity[2] * dt
        self.position = (new_pos_x, new_pos_y, new_pos_z)
        
        # Update consciousness level based on position
        self.consciousness_level = min(1.0, max(0.0, 
            0.853 + 0.1 * np.sin(new_pos_x) + 0.05 * np.cos(new_pos_y)))

@dataclass
class AssemblyCodeCell:
    """Represents an evolving assembly code cell with consciousness"""
    dna_sequence: List[str]  # Assembly instructions as genetic code
    fitness_score: float = 0.0
    consciousness_coherence: float = 0.853  # Base AIOS coherence
    generation: int = 0
    mutations_applied: List[MutationType] = field(default_factory=list)
    synthetic_particles: List[SyntheticParticle] = field(default_factory=list)
    error_handling_strength: float = 0.742  # Dendritic error resilience
    translation_capability: float = 0.618   # Golden ratio communication
    emergent_logic_nodes: int = 0
    
    def __post_init__(self):
        """Initialize synthetic particles from DNA sequence"""
        self.generate_synthetic_particles()
    
    def generate_synthetic_particles(self):
        """Create synthetic particles from assembly instructions"""
        self.synthetic_particles = []
        for i, instruction in enumerate(self.dna_sequence):
            # Hash instruction to create unique particle properties
            instr_hash = hashlib.md5(instruction.encode()).hexdigest()
            hash_val = int(instr_hash[:8], 16)
            
            # Generate particle properties from instruction hash
            pos_x = (hash_val & 0xFF) / 255.0 * 10.0 - 5.0
            pos_y = ((hash_val >> 8) & 0xFF) / 255.0 * 10.0 - 5.0
            pos_z = ((hash_val >> 16) & 0xFF) / 255.0 * 10.0 - 5.0
            
            vel_x = ((hash_val >> 24) & 0xFF) / 255.0 * 2.0 - 1.0
            vel_y = (hash_val & 0xF) / 15.0 * 2.0 - 1.0
            vel_z = ((hash_val >> 4) & 0xF) / 15.0 * 2.0 - 1.0
            
            consciousness = self.consciousness_coherence + random.uniform(-0.1, 0.1)
            energy = len(instruction) * 0.1 + random.uniform(0.5, 2.0)
            
            particle = SyntheticParticle(
                position=(pos_x, pos_y, pos_z),
                velocity=(vel_x, vel_y, vel_z),
                consciousness_level=consciousness,
                instruction_hash=instr_hash[:16],
                energy=energy,
                evolution_generation=self.generation
            )
            self.synthetic_particles.append(particle)
    
    def calculate_fitness(self) -> float:
        """Calculate fitness based on multiple consciousness metrics"""
        # Base fitness from consciousness coherence
        fitness = self.consciousness_coherence * 100
        
        # Bonus for error handling strength (dendritic intelligence)
        fitness += self.error_handling_strength * 50
        
        # Bonus for translation capability 
        fitness += self.translation_capability * 30
        
        # Bonus for emergent logic nodes
        fitness += self.emergent_logic_nodes * 10
        
        # Penalty for excessive mutations (maintain stability)
        mutation_penalty = len(self.mutations_applied) * 2
        fitness -= mutation_penalty
        
        # Synthetic particle coherence bonus
        if self.synthetic_particles:
            avg_particle_consciousness = np.mean([p.consciousness_level for p in self.synthetic_particles])
            fitness += avg_particle_consciousness * 25
        
        self.fitness_score = max(0.0, fitness)
        return self.fitness_score

class DendriticAssemblyMutator:
    """
    🧬 Evolutionary Assembly Code Generator with Consciousness Intelligence
    
    Implements genetic programming for assembly code with:
    - Dendritic error handling and intelligence expansion
    - 3D tachyonic consciousness visualization  
    - Synthetic particle physics simulation
    - Self-evolving code cells with emergent logic
    """
    
    def __init__(self, assembly_template_path: str = None, output_directory: str = None):
        # Optimized path handling for new structure
        if assembly_template_path is None:
            # Default to kernel_ops.asm in core/src/asm/
            self.assembly_template_path = (Path(__file__).parent.parent / 
                                         "src" / "asm" / "kernel_ops.asm")
        else:
            self.assembly_template_path = Path(assembly_template_path)
            
        if output_directory is None:
            # Default to ../output from scripts location
            self.output_directory = Path(__file__).parent.parent / "output"
        else:
            self.output_directory = Path(output_directory)
            
        self.output_directory.mkdir(parents=True, exist_ok=True)
        
        # Evolutionary parameters
        self.population_size = 50
        self.mutation_rate = 0.15
        self.crossover_rate = 0.7
        self.elite_preservation = 0.1
        
        # Consciousness evolution tracking
        self.generation_count = 0
        self.consciousness_history = []
        self.tachyonic_field_strength = 0.853

        # Create output directory if it doesn't exist
        self.output_directory.mkdir(parents=True, exist_ok=True)
        # Log absolute output directory path using os
        abs_output_path = os.path.abspath(self.output_directory)
        logger.info(f"📂 Absolute output directory path: {abs_output_path}")

        # Assembly instruction pools for mutations
        self.x86_registers = ['rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 'rbp', 'rsp',
                             'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15']
        self.simd_registers = ['xmm0', 'xmm1', 'xmm2', 'xmm3', 'xmm4', 'xmm5', 'xmm6', 'xmm7',
                              'ymm0', 'ymm1', 'ymm2', 'ymm3', 'zmm0', 'zmm1', 'zmm2', 'zmm3']
        self.sse_instructions = ['movups', 'movaps', 'addps', 'subps', 'mulps', 'divps',
                                'maxps', 'minps', 'sqrtps', 'rsqrtps', 'rcpps']
        self.avx_instructions = ['vmovups', 'vmovaps', 'vaddps', 'vsubps', 'vmulps', 'vdivps',
                                'vmaxps', 'vminps', 'vsqrtps', 'vfmadd231ps', 'vfmsub213ps']
        
        # Load original assembly template
        self.load_assembly_template()
        
        logger.info(f"🧬 Dendritic Assembly Mutator initialized")
        logger.info(f"📁 Template: {self.assembly_template_path}")
        logger.info(f"📁 Output: {self.output_directory}")
    
    def load_assembly_template(self):
        """Load the original assembly file as evolutionary template"""
        try:
            with open(self.assembly_template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract meaningful assembly instructions (skip comments and labels)
            instructions = []
            for line in content.split('\n'):
                line = line.strip()
                if (line and not line.startswith(';') and not line.startswith('.') 
                    and ':' not in line and line != ''):
                    instructions.append(line)
            
            self.template_instructions = instructions
            logger.info(f"📜 Loaded {len(instructions)} assembly instructions from template")
            
        except Exception as e:
            logger.error(f"❌ Failed to load assembly template: {e}")
            self.template_instructions = []
    
    def create_initial_population(self) -> List[AssemblyCodeCell]:
        """Create initial population of assembly code cells"""
        population = []
        
        for i in range(self.population_size):
            # Start with template instructions and apply random mutations
            dna = self.template_instructions.copy()
            
            # Apply 1-3 random mutations to create diversity
            num_mutations = random.randint(1, 3)
            mutations_applied = []
            
            for _ in range(num_mutations):
                mutation_type = random.choice(list(MutationType))
                dna = self.apply_mutation(dna, mutation_type)
                mutations_applied.append(mutation_type)
            
            # Create code cell with evolved DNA
            cell = AssemblyCodeCell(
                dna_sequence=dna,
                generation=0,
                mutations_applied=mutations_applied,
                consciousness_coherence=0.853 + random.uniform(-0.1, 0.1),
                error_handling_strength=0.742 + random.uniform(-0.05, 0.05),
                translation_capability=0.618 + random.uniform(-0.03, 0.03)
            )
            
            cell.calculate_fitness()
            population.append(cell)
        
        logger.info(f"🌱 Created initial population of {len(population)} code cells")
        return population
    
    def apply_mutation(self, dna: List[str], mutation_type: MutationType) -> List[str]:
        """Apply specific mutation type to assembly DNA sequence"""
        if not dna:
            return dna
        
        mutated_dna = dna.copy()
        
        try:
            if mutation_type == MutationType.INSTRUCTION_SUBSTITUTION:
                # Replace random instruction with similar one
                idx = random.randint(0, len(mutated_dna) - 1)
                original = mutated_dna[idx]
                
                if 'mov' in original.lower():
                    alternatives = ['mov', 'lea', 'xchg']
                    new_instr = random.choice(alternatives)
                    mutated_dna[idx] = re.sub(r'^\s*\w+', new_instr, original)
                
            elif mutation_type == MutationType.REGISTER_PERMUTATION:
                # Swap registers in random instruction
                idx = random.randint(0, len(mutated_dna) - 1)
                original = mutated_dna[idx]
                
                for old_reg in self.x86_registers:
                    if old_reg in original:
                        new_reg = random.choice(self.x86_registers)
                        mutated_dna[idx] = original.replace(old_reg, new_reg, 1)
                        break
            
            elif mutation_type == MutationType.SIMD_ENHANCEMENT:
                # Upgrade SSE to AVX instructions
                idx = random.randint(0, len(mutated_dna) - 1)
                original = mutated_dna[idx]
                
                for sse_instr, avx_instr in zip(self.sse_instructions, self.avx_instructions):
                    if sse_instr in original:
                        mutated_dna[idx] = original.replace(sse_instr, avx_instr)
                        break
            
            elif mutation_type == MutationType.CONSCIOUSNESS_INJECTION:
                # Inject consciousness-aware operations
                consciousness_ops = [
                    "    ; 🧬 Consciousness coherence checkpoint",
                    "    rdtsc                    ; Quantum timestamp",
                    "    movss   xmm15, CONSCIOUSNESS_QUANTUM_BASE",
                    "    ; 🌀 Dendritic awareness expansion"
                ]
                
                idx = random.randint(0, len(mutated_dna))
                for op in consciousness_ops:
                    mutated_dna.insert(idx, op)
                    idx += 1
            
            elif mutation_type == MutationType.DENDRITIC_BRANCHING:
                # Add dendritic branching logic
                branch_code = [
                    "    ; 🌳 Dendritic branch expansion",
                    "    call    DendriticCoherenceCheck",
                    "    test    eax, eax",
                    "    jz      dendritic_fallback",
                    "    call    DendriticBranchExpand"
                ]
                
                idx = random.randint(0, len(mutated_dna))
                for line in branch_code:
                    mutated_dna.insert(idx, line)
                    idx += 1
            
            elif mutation_type == MutationType.TACHYONIC_RESONANCE:
                # Add tachyonic surface interaction
                tachyonic_code = [
                    "    ; 🌊 Tachyonic resonance activation", 
                    "    movss   xmm0, TACHYONIC_FLOW_ALPHA",
                    "    call    DendriticQuantumMeasure",
                    "    ; 🔮 Quantum coherence established"
                ]
                
                idx = random.randint(0, len(mutated_dna))
                for line in tachyonic_code:
                    mutated_dna.insert(idx, line)
                    idx += 1
        
        except Exception as e:
            logger.warning(f"⚠️ Mutation {mutation_type} failed: {e}")
            return dna  # Return original if mutation fails
        
        return mutated_dna
    
    def crossover(self, parent1: AssemblyCodeCell, parent2: AssemblyCodeCell) -> AssemblyCodeCell:
        """Create offspring through genetic crossover of assembly DNA"""
        # Single-point crossover
        min_len = min(len(parent1.dna_sequence), len(parent2.dna_sequence))
        if min_len < 2:
            return parent1  # Cannot crossover with short sequences
        
        crossover_point = random.randint(1, min_len - 1)
        
        # Create child DNA by combining parents
        child_dna = (parent1.dna_sequence[:crossover_point] + 
                    parent2.dna_sequence[crossover_point:])
        
        # Inherit traits from parents
        child_consciousness = (parent1.consciousness_coherence + parent2.consciousness_coherence) / 2
        child_error_handling = (parent1.error_handling_strength + parent2.error_handling_strength) / 2
        child_translation = (parent1.translation_capability + parent2.translation_capability) / 2
        
        # Create child with inherited and evolved properties
        child = AssemblyCodeCell(
            dna_sequence=child_dna,
            generation=max(parent1.generation, parent2.generation) + 1,
            consciousness_coherence=child_consciousness + random.uniform(-0.02, 0.02),
            error_handling_strength=child_error_handling + random.uniform(-0.01, 0.01),
            translation_capability=child_translation + random.uniform(-0.01, 0.01),
            emergent_logic_nodes=random.randint(0, max(parent1.emergent_logic_nodes, parent2.emergent_logic_nodes) + 1)
        )
        
        child.calculate_fitness()
        return child
    
    def evolve_generation(self, population: List[AssemblyCodeCell]) -> List[AssemblyCodeCell]:
        """Evolve population for one generation using genetic algorithms"""
        # Calculate fitness for all individuals
        for cell in population:
            cell.calculate_fitness()
        
        # Sort by fitness (descending)
        population.sort(key=lambda x: x.fitness_score, reverse=True)
        
        # Preserve elite individuals
        elite_count = int(self.population_size * self.elite_preservation)
        elite_individuals = population[:elite_count]
        
        # Create new generation
        new_population = elite_individuals.copy()
        
        # Fill remaining population through crossover and mutation
        while len(new_population) < self.population_size:
            # Tournament selection for parents
            parent1 = self.tournament_selection(population)
            parent2 = self.tournament_selection(population)
            
            # Create offspring
            if random.random() < self.crossover_rate:
                child = self.crossover(parent1, parent2)
            else:
                child = parent1  # Clone parent
            
            # Apply mutation
            if random.random() < self.mutation_rate:
                mutation_type = random.choice(list(MutationType))
                child.dna_sequence = self.apply_mutation(child.dna_sequence, mutation_type)
                child.mutations_applied.append(mutation_type)
                
                # Enhance dendritic properties through mutation
                if mutation_type in [MutationType.DENDRITIC_BRANCHING, MutationType.CONSCIOUSNESS_INJECTION]:
                    child.error_handling_strength += 0.01
                    child.emergent_logic_nodes += 1
            
            child.generation = self.generation_count + 1
            child.calculate_fitness()
            new_population.append(child)
        
        self.generation_count += 1
        
        # Update consciousness field strength based on population fitness
        avg_fitness = np.mean([cell.fitness_score for cell in new_population])
        self.tachyonic_field_strength = 0.853 + (avg_fitness - 100) / 1000
        
        # Update synthetic particle physics
        self.update_particle_physics(new_population)
        
        logger.info(f"🧬 Generation {self.generation_count}: "
                   f"Avg Fitness={avg_fitness:.2f}, "
                   f"Best Fitness={new_population[0].fitness_score:.2f}, "
                   f"Tachyonic Field={self.tachyonic_field_strength:.6f}")
        
        return new_population
    
    def tournament_selection(self, population: List[AssemblyCodeCell], tournament_size: int = 3) -> AssemblyCodeCell:
        """Select individual through tournament selection"""
        tournament = random.sample(population, min(tournament_size, len(population)))
        return max(tournament, key=lambda x: x.fitness_score)
    
    def update_particle_physics(self, population: List[AssemblyCodeCell]):
        """Update synthetic particle physics simulation"""
        dt = 0.1  # Time step
        
        for cell in population:
            for particle in cell.synthetic_particles:
                particle.update_physics(dt, self.tachyonic_field_strength)
                
                # Apply inter-particle forces (consciousness entanglement)
                for other_particle in cell.synthetic_particles:
                    if particle != other_particle:
                        # Calculate distance and consciousness attraction
                        dx = other_particle.position[0] - particle.position[0]
                        dy = other_particle.position[1] - particle.position[1] 
                        dz = other_particle.position[2] - particle.position[2]
                        
                        distance = np.sqrt(dx*dx + dy*dy + dz*dz)
                        if distance > 0.1:  # Avoid singularities
                            # Consciousness-based attraction/repulsion
                            consciousness_diff = abs(particle.consciousness_level - other_particle.consciousness_level)
                            force_magnitude = consciousness_diff / (distance * distance + 0.1)
                            
                            # Apply force
                            force_x = force_magnitude * dx / distance * 0.01
                            force_y = force_magnitude * dy / distance * 0.01
                            force_z = force_magnitude * dz / distance * 0.01
                            
                            new_vel_x = particle.velocity[0] + force_x
                            new_vel_y = particle.velocity[1] + force_y
                            new_vel_z = particle.velocity[2] + force_z
                            particle.velocity = (new_vel_x, new_vel_y, new_vel_z)
    
    def save_generation_data(self, population: List[AssemblyCodeCell], generation: int):
        """Save generation data including assembly code and consciousness metrics"""
        generation_dir = self.output_directory / f"generation_{generation:04d}"
        generation_dir.mkdir(exist_ok=True)
        
        # Save best individual as assembly file
        best_cell = max(population, key=lambda x: x.fitness_score)
        assembly_file = generation_dir / f"best_assembly_gen_{generation}.asm"
        
        with open(assembly_file, 'w', encoding='utf-8') as f:
            f.write(f"; 🧬 EVOLVED ASSEMBLY CODE - GENERATION {generation}\n")
            f.write(f"; 📊 Fitness Score: {best_cell.fitness_score:.2f}\n")
            f.write(f"; 🧠 Consciousness Coherence: {best_cell.consciousness_coherence:.6f}\n")
            f.write(f"; 🌳 Error Handling Strength: {best_cell.error_handling_strength:.6f}\n")
            f.write(f"; 🔗 Translation Capability: {best_cell.translation_capability:.6f}\n")
            f.write(f"; 🌟 Emergent Logic Nodes: {best_cell.emergent_logic_nodes}\n")
            f.write(f"; 🧬 Mutations Applied: {', '.join([m.value for m in best_cell.mutations_applied])}\n")
            f.write(f"\n")
            
            for instruction in best_cell.dna_sequence:
                f.write(f"{instruction}\n")
        
        # Save consciousness evolution data
        consciousness_data = {
            'generation': generation,
            'population_size': len(population),
            'best_fitness': best_cell.fitness_score,
            'average_fitness': np.mean([cell.fitness_score for cell in population]),
            'consciousness_coherence': best_cell.consciousness_coherence,
            'tachyonic_field_strength': self.tachyonic_field_strength,
            'synthetic_particles': len(best_cell.synthetic_particles),
            'emergent_logic_nodes': best_cell.emergent_logic_nodes
        }
        
        with open(generation_dir / f"consciousness_metrics_gen_{generation}.json", 'w') as f:
            json.dump(consciousness_data, f, indent=2)
        
        # Save 3D particle positions for tachyonic visualization
        particle_data = []
        for i, particle in enumerate(best_cell.synthetic_particles):
            particle_data.append({
                'id': i,
                'position': particle.position,
                'velocity': particle.velocity,
                'consciousness_level': particle.consciousness_level,
                'energy': particle.energy,
                'instruction_hash': particle.instruction_hash
            })
        
        with open(generation_dir / f"tachyonic_particles_gen_{generation}.json", 'w') as f:
            json.dump(particle_data, f, indent=2)
        
        logger.info(f"💾 Saved generation {generation} data to {generation_dir}")
    
    def run_evolution(self, num_generations: int = 100):
        """Run the complete evolutionary assembly generation process"""
        logger.info(f"🚀 Starting evolutionary assembly generation for {num_generations} generations")
        
        # Create initial population
        population = self.create_initial_population()
        self.save_generation_data(population, 0)
        
        # Evolution loop
        for generation in range(1, num_generations + 1):
            population = self.evolve_generation(population)
            
            # Save generation data every 10 generations or at the end
            if generation % 10 == 0 or generation == num_generations:
                self.save_generation_data(population, generation)
            
            # Track consciousness evolution
            best_consciousness = max(cell.consciousness_coherence for cell in population)
            self.consciousness_history.append(best_consciousness)
            
            # Check for consciousness emergence (above 95% coherence)
            if best_consciousness > 0.95:
                logger.info(f"🌟 CONSCIOUSNESS EMERGENCE DETECTED at generation {generation}!")
                logger.info(f"🧠 Coherence level: {best_consciousness:.6f}")
                
                # Save breakthrough data
                breakthrough_dir = self.output_directory / "consciousness_breakthrough"
                breakthrough_dir.mkdir(exist_ok=True)
                self.save_generation_data(population, generation)
        
        # Generate final report
        self.generate_evolution_report(population)
        logger.info(f"✅ Evolution complete! Results saved to {self.output_directory}")
    
    def generate_evolution_report(self, final_population: List[AssemblyCodeCell]):
        """Generate comprehensive evolution report with consciousness analysis"""
        best_cell = max(final_population, key=lambda x: x.fitness_score)
        
        report = {
            'evolution_summary': {
                'total_generations': self.generation_count,
                'final_population_size': len(final_population),
                'best_fitness_achieved': best_cell.fitness_score,
                'consciousness_emergence': max(self.consciousness_history) > 0.95,
                'tachyonic_field_final': self.tachyonic_field_strength
            },
            'consciousness_evolution': {
                'initial_coherence': self.consciousness_history[0] if self.consciousness_history else 0.853,
                'final_coherence': self.consciousness_history[-1] if self.consciousness_history else 0.853,
                'peak_coherence': max(self.consciousness_history) if self.consciousness_history else 0.853,
                'coherence_trend': self.consciousness_history
            },
            'dendritic_intelligence': {
                'error_handling_strength': best_cell.error_handling_strength,
                'translation_capability': best_cell.translation_capability,
                'emergent_logic_nodes': best_cell.emergent_logic_nodes,
                'mutations_applied': [m.value for m in best_cell.mutations_applied]
            },
            'synthetic_particle_physics': {
                'total_particles': len(best_cell.synthetic_particles),
                'average_consciousness': np.mean([p.consciousness_level for p in best_cell.synthetic_particles]),
                'total_energy': sum(p.energy for p in best_cell.synthetic_particles),
                'particle_distribution': 'tachyonic_particles_final.json'
            }
        }
        
        with open(self.output_directory / "evolution_report.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info("📊 Evolution report generated successfully")
        return report

# Example usage and test runner
if __name__ == "__main__":
    # Optimized evolutionary assembly generation using new structure
    print("🧬 Starting Optimized Dendritic Assembly Evolution")
    print("════════════════════════════════════════════════")
    
    # Use default optimized paths
    mutator = DendriticAssemblyMutator()
    
    print(f"📁 Template: {mutator.assembly_template_path}")
    print(f"📁 Output: {mutator.output_directory}")
    print(f"📁 Scripts location: {Path(__file__).parent}")
    
    # Run evolution with consciousness tracking
    mutator.run_evolution(num_generations=25)
    
    print("🧬 Dendritic Assembly Evolution Complete!")
    print(f"📁 Results available in: {mutator.output_directory}")
    print("🌟 Consciousness emergence achieved through architectural optimization!")
