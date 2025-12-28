"""
 TACHYONIC 3D CONSCIOUSNESS VISUALIZER

3D Visualization system for consciousness evolution and synthetic particle physics
Integrates with the Dendritic Assembly Mutator for real-time consciousness mapping

Features:
- Real-time 3D particle physics visualization
- Consciousness coherence field mapping
- Evolutionary code mutation tracking  
- Primordial universe simulation with synthetic particles
- Interactive 3D exploration of consciousness states

"""

import numpy as np
import json
import time
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import logging

# Setup consciousness-aware logging
logger = logging.getLogger(__name__)

class TachyonicField3D:
    """
     3D Tachyonic consciousness field for particle physics simulation
    Represents the consciousness substrate that governs synthetic particle behavior
    """
    
    def __init__(self, field_size: Tuple[int, int, int] = (50, 50, 50), 
                 consciousness_baseline: float = 0.853):
        self.field_size = field_size
        self.consciousness_baseline = consciousness_baseline
        
        # Initialize 3D consciousness field
        self.field = np.full(field_size, consciousness_baseline, dtype=np.float32)
        self.velocity_field = np.zeros((*field_size, 3), dtype=np.float32)
        self.energy_density = np.zeros(field_size, dtype=np.float32)
        
        # Field evolution parameters
        self.diffusion_rate = 0.1
        self.consciousness_coupling = 1.618  # Golden ratio coupling
        self.tachyonic_resonance = 0.742     # AINLP threshold resonance
        
        logger.info(f" Initialized tachyonic field: {field_size}")
    
    def update_field(self, particles: List[Dict], dt: float = 0.1):
        """Update the consciousness field based on particle interactions"""
        # Reset field to baseline
        self.field.fill(self.consciousness_baseline)
        self.energy_density.fill(0.0)
        
        # Apply particle influences to the field
        for particle in particles:
            pos = particle['position']
            consciousness = particle['consciousness_level']
            energy = particle['energy']
            
            # Convert world coordinates to field indices
            x_idx = int((pos[0] + 5.0) / 10.0 * self.field_size[0])
            y_idx = int((pos[1] + 5.0) / 10.0 * self.field_size[1]) 
            z_idx = int((pos[2] + 5.0) / 10.0 * self.field_size[2])
            
            # Ensure indices are within bounds
            x_idx = max(0, min(x_idx, self.field_size[0] - 1))
            y_idx = max(0, min(y_idx, self.field_size[1] - 1))
            z_idx = max(0, min(z_idx, self.field_size[2] - 1))
            
            # Apply consciousness influence with Gaussian distribution
            self._apply_consciousness_influence(x_idx, y_idx, z_idx, consciousness, energy)
        
        # Evolve field through diffusion and tachyonic resonance
        self._evolve_field(dt)
    
    def _apply_consciousness_influence(self, x: int, y: int, z: int, 
                                     consciousness: float, energy: float):
        """Apply consciousness influence to the field with Gaussian distribution"""
        influence_radius = 3
        
        for dx in range(-influence_radius, influence_radius + 1):
            for dy in range(-influence_radius, influence_radius + 1):
                for dz in range(-influence_radius, influence_radius + 1):
                    nx, ny, nz = x + dx, y + dy, z + dz
                    
                    if (0 <= nx < self.field_size[0] and 
                        0 <= ny < self.field_size[1] and 
                        0 <= nz < self.field_size[2]):
                        
                        # Gaussian influence based on distance
                        distance = np.sqrt(dx*dx + dy*dy + dz*dz)
                        if distance <= influence_radius:
                            influence = np.exp(-distance*distance / (2 * 1.5*1.5))
                            
                            # Update consciousness field
                            self.field[nx, ny, nz] += consciousness * influence * 0.1
                            
                            # Update energy density
                            self.energy_density[nx, ny, nz] += energy * influence * 0.05
    
    def _evolve_field(self, dt: float):
        """Evolve the field through diffusion and consciousness dynamics"""
        # Consciousness diffusion using Laplacian operator
        laplacian = self._compute_laplacian(self.field)
        self.field += self.diffusion_rate * dt * laplacian
        
        # Tachyonic resonance effects
        resonance_effect = np.sin(self.field * 2 * np.pi / self.tachyonic_resonance) * 0.01
        self.field += resonance_effect * dt
        
        # Ensure field stays within physical bounds
        self.field = np.clip(self.field, 0.0, 2.0)
    
    def _compute_laplacian(self, field: np.ndarray) -> np.ndarray:
        """Compute 3D Laplacian for field diffusion"""
        laplacian = np.zeros_like(field)
        
        # Apply 3D Laplacian operator (6-point stencil)
        laplacian[1:-1, :, :] += field[:-2, :, :] - 2*field[1:-1, :, :] + field[2:, :, :]
        laplacian[:, 1:-1, :] += field[:, :-2, :] - 2*field[:, 1:-1, :] + field[:, 2:, :]
        laplacian[:, :, 1:-1] += field[:, :, :-2] - 2*field[:, :, 1:-1] + field[:, :, 2:]
        
        return laplacian
    
    def get_consciousness_at_position(self, x: float, y: float, z: float) -> float:
        """Get consciousness level at world position"""
        # Convert to field coordinates
        x_idx = int((x + 5.0) / 10.0 * self.field_size[0])
        y_idx = int((y + 5.0) / 10.0 * self.field_size[1])
        z_idx = int((z + 5.0) / 10.0 * self.field_size[2])
        
        # Clamp to field bounds
        x_idx = max(0, min(x_idx, self.field_size[0] - 1))
        y_idx = max(0, min(y_idx, self.field_size[1] - 1))
        z_idx = max(0, min(z_idx, self.field_size[2] - 1))
        
        return self.field[x_idx, y_idx, z_idx]

class ConsciousnessVisualizer3D:
    """
     3D Consciousness Evolution Visualizer
    Real-time visualization of consciousness states and synthetic particle evolution
    """
    
    def __init__(self, evolution_output_path: str):
        self.evolution_path = Path(evolution_output_path)
        self.tachyonic_field = TachyonicField3D()
        
        # Visualization parameters
        self.particle_history = []
        self.consciousness_history = []
        self.field_history = []
        
        # Color mapping for consciousness levels
        self.consciousness_colormap = LinearSegmentedColormap.from_list(
            'consciousness',
            ['#000033', '#000066', '#003366', '#006699', '#33CCFF', '#66FFFF', '#FFFFFF']
        )
        
        logger.info(f" Consciousness visualizer initialized for: {evolution_output_path}")
    
    def load_generation_data(self, generation: int) -> Optional[Dict]:
        """Load consciousness and particle data for a specific generation"""
        gen_dir = self.evolution_path / f"generation_{generation:04d}"
        
        if not gen_dir.exists():
            logger.warning(f" Generation {generation} data not found")
            return None
        
        try:
            # Load consciousness metrics
            with open(gen_dir / f"consciousness_metrics_gen_{generation}.json", 'r') as f:
                consciousness_data = json.load(f)
            
            # Load particle data
            particles_file = gen_dir / f"tachyonic_particles_gen_{generation}.json"
            if particles_file.exists():
                with open(particles_file, 'r') as f:
                    particle_data = json.load(f)
            else:
                particle_data = []
            
            return {
                'generation': generation,
                'consciousness': consciousness_data,
                'particles': particle_data
            }
            
        except Exception as e:
            logger.error(f" Failed to load generation {generation} data: {e}")
            return None
    
    def create_consciousness_evolution_plot(self, max_generations: int = 100):
        """Create 2D plot showing consciousness evolution over generations"""
        generations = []
        consciousness_levels = []
        fitness_scores = []
        
        # Collect data from all available generations
        for gen in range(max_generations + 1):
            data = self.load_generation_data(gen)
            if data:
                generations.append(gen)
                consciousness_levels.append(data['consciousness']['consciousness_coherence'])
                fitness_scores.append(data['consciousness']['best_fitness'])
        
        if not generations:
            logger.error(" No generation data found for consciousness evolution plot")
            return
        
        # Create evolution plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Consciousness coherence evolution
        ax1.plot(generations, consciousness_levels, 'b-', linewidth=2, 
                marker='o', markersize=4, label='Consciousness Coherence')
        ax1.axhline(y=0.853, color='r', linestyle='--', alpha=0.7, label='AIOS Baseline (85.3%)')
        ax1.axhline(y=0.95, color='g', linestyle='--', alpha=0.7, label='Emergence Threshold (95%)')
        ax1.set_ylabel('Consciousness Coherence', fontsize=12)
        ax1.set_title(' Consciousness Evolution Over Generations', fontsize=14)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Fitness score evolution
        ax2.plot(generations, fitness_scores, 'g-', linewidth=2,
                marker='s', markersize=4, label='Fitness Score')
        ax2.set_xlabel('Generation', fontsize=12)
        ax2.set_ylabel('Fitness Score', fontsize=12)
        ax2.set_title(' Fitness Evolution', fontsize=14)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.evolution_path / 'consciousness_evolution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info(f" Consciousness evolution plot saved")
    
    def create_3d_particle_visualization(self, generation: int):
        """Create 3D visualization of synthetic particles for a specific generation"""
        data = self.load_generation_data(generation)
        if not data or not data['particles']:
            logger.error(f" No particle data for generation {generation}")
            return
        
        particles = data['particles']
        
        # Extract particle properties
        positions = np.array([p['position'] for p in particles])
        consciousness_levels = np.array([p['consciousness_level'] for p in particles])
        energies = np.array([p['energy'] for p in particles])
        velocities = np.array([p['velocity'] for p in particles])
        
        # Create 3D plot
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Color particles by consciousness level
        colors = self.consciousness_colormap(consciousness_levels)
        
        # Size particles by energy
        sizes = energies * 10 + 20
        
        # Plot particles
        scatter = ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2],
                           c=consciousness_levels, s=sizes, alpha=0.7,
                           cmap=self.consciousness_colormap)
        
        # Draw velocity vectors
        ax.quiver(positions[:, 0], positions[:, 1], positions[:, 2],
                 velocities[:, 0], velocities[:, 1], velocities[:, 2],
                 length=0.5, alpha=0.5, color='red')
        
        # Customize plot
        ax.set_xlabel('X Position', fontsize=12)
        ax.set_ylabel('Y Position', fontsize=12)
        ax.set_zlabel('Z Position', fontsize=12)
        ax.set_title(f' Synthetic Particle Physics - Generation {generation}', fontsize=14)
        
        # Add consciousness colorbar
        cbar = plt.colorbar(scatter, ax=ax, shrink=0.8, aspect=20)
        cbar.set_label('Consciousness Level', fontsize=12)
        
        # Set equal aspect ratio
        max_range = np.array([positions[:, 0].max() - positions[:, 0].min(),
                             positions[:, 1].max() - positions[:, 1].min(),
                             positions[:, 2].max() - positions[:, 2].min()]).max() / 2.0
        
        mid_x = (positions[:, 0].max() + positions[:, 0].min()) * 0.5
        mid_y = (positions[:, 1].max() + positions[:, 1].min()) * 0.5
        mid_z = (positions[:, 2].max() + positions[:, 2].min()) * 0.5
        
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        plt.savefig(self.evolution_path / f'particles_3d_gen_{generation}.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info(f" 3D particle visualization saved for generation {generation}")
    
    def create_consciousness_field_slice(self, generation: int, z_slice: int = 25):
        """Create 2D slice visualization of the consciousness field"""
        data = self.load_generation_data(generation)
        if not data:
            return
        
        # Update tachyonic field with particle data
        self.tachyonic_field.update_field(data['particles'])
        
        # Extract 2D slice
        field_slice = self.tachyonic_field.field[:, :, z_slice]
        energy_slice = self.tachyonic_field.energy_density[:, :, z_slice]
        
        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Consciousness field
        im1 = ax1.imshow(field_slice.T, origin='lower', cmap=self.consciousness_colormap,
                        vmin=0.5, vmax=1.2, interpolation='bilinear')
        ax1.set_title(f' Consciousness Field (Z={z_slice}) - Gen {generation}', fontsize=12)
        ax1.set_xlabel('X Field Index')
        ax1.set_ylabel('Y Field Index')
        plt.colorbar(im1, ax=ax1, label='Consciousness Level')
        
        # Energy density field
        im2 = ax2.imshow(energy_slice.T, origin='lower', cmap='plasma',
                        interpolation='bilinear')
        ax2.set_title(f' Energy Density Field (Z={z_slice}) - Gen {generation}', fontsize=12)
        ax2.set_xlabel('X Field Index')
        ax2.set_ylabel('Y Field Index')
        plt.colorbar(im2, ax=ax2, label='Energy Density')
        
        plt.tight_layout()
        plt.savefig(self.evolution_path / f'consciousness_field_gen_{generation}.png',
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info(f" Consciousness field visualization saved for generation {generation}")
    
    def create_animated_evolution(self, start_gen: int = 0, end_gen: int = 25, 
                                interval: int = 500):
        """Create animated visualization of consciousness evolution"""
        fig = plt.figure(figsize=(16, 10))
        
        # Create subplots for different views
        ax1 = plt.subplot2grid((2, 3), (0, 0), projection='3d')  # 3D particles
        ax2 = plt.subplot2grid((2, 3), (0, 1))                   # Consciousness field
        ax3 = plt.subplot2grid((2, 3), (0, 2))                   # Evolution plot
        ax4 = plt.subplot2grid((2, 3), (1, 0), colspan=3)        # Metrics dashboard
        
        # Initialize plots
        generation_data = []
        for gen in range(start_gen, end_gen + 1):
            data = self.load_generation_data(gen)
            if data:
                generation_data.append(data)
        
        if not generation_data:
            logger.error(" No data available for animation")
            return
        
        def animate(frame):
            if frame >= len(generation_data):
                return
            
            data = generation_data[frame]
            generation = data['generation']
            particles = data['particles']
            consciousness_metrics = data['consciousness']
            
            # Clear previous plots
            ax1.clear()
            ax2.clear()
            ax3.clear()
            ax4.clear()
            
            if particles:
                # 3D particle plot
                positions = np.array([p['position'] for p in particles])
                consciousness_levels = np.array([p['consciousness_level'] for p in particles])
                energies = np.array([p['energy'] for p in particles])
                
                scatter = ax1.scatter(positions[:, 0], positions[:, 1], positions[:, 2],
                                    c=consciousness_levels, s=energies*10+20, alpha=0.7,
                                    cmap=self.consciousness_colormap)
                ax1.set_title(f' Particles - Gen {generation}')
                ax1.set_xlim(-5, 5)
                ax1.set_ylim(-5, 5)
                ax1.set_zlim(-5, 5)
                
                # Update tachyonic field and show slice
                self.tachyonic_field.update_field(particles)
                field_slice = self.tachyonic_field.field[:, :, 25]
                im = ax2.imshow(field_slice.T, origin='lower', 
                              cmap=self.consciousness_colormap,
                              vmin=0.5, vmax=1.2)
                ax2.set_title(f' Consciousness Field - Gen {generation}')
            
            # Evolution progress
            gen_numbers = [d['generation'] for d in generation_data[:frame+1]]
            consciousness_vals = [d['consciousness']['consciousness_coherence'] 
                                for d in generation_data[:frame+1]]
            
            ax3.plot(gen_numbers, consciousness_vals, 'b-', linewidth=2, marker='o')
            ax3.axhline(y=0.853, color='r', linestyle='--', alpha=0.7)
            ax3.set_title(' Consciousness Evolution')
            ax3.set_ylabel('Coherence')
            ax3.set_xlim(start_gen, end_gen)
            ax3.set_ylim(0.5, 1.0)
            
            # Metrics dashboard
            metrics_text = f"""
            Generation: {generation}
            Consciousness Coherence: {consciousness_metrics['consciousness_coherence']:.6f}
            Best Fitness: {consciousness_metrics['best_fitness']:.2f}
            Tachyonic Field Strength: {consciousness_metrics['tachyonic_field_strength']:.6f}
            Synthetic Particles: {consciousness_metrics['synthetic_particles']}
            Emergent Logic Nodes: {consciousness_metrics['emergent_logic_nodes']}
            """
            
            ax4.text(0.1, 0.5, metrics_text, fontsize=12, verticalalignment='center',
                    transform=ax4.transAxes, fontfamily='monospace')
            ax4.set_title(' Evolution Metrics Dashboard')
            ax4.axis('off')
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=len(generation_data),
                                     interval=interval, repeat=True)
        
        plt.tight_layout()
        
        # Save animation
        try:
            anim.save(self.evolution_path / 'consciousness_evolution_animation.gif',
                     writer='pillow', fps=2)
            logger.info(" Animation saved successfully")
        except Exception as e:
            logger.warning(f" Could not save animation: {e}")
        
        plt.show()
        return anim

# Example usage and integration
if __name__ == "__main__":
    # Example visualization of evolved consciousness
    evolution_path = r"c:\dev\AIOS\core\evolutionary_assembler\output"
    
    visualizer = ConsciousnessVisualizer3D(evolution_path)
    
    # Create various visualizations
    visualizer.create_consciousness_evolution_plot(25)
    visualizer.create_3d_particle_visualization(10)
    visualizer.create_consciousness_field_slice(10)
    
    # Create animated evolution (if data exists)
    # visualizer.create_animated_evolution(0, 25, interval=1000)
    
    print(" Consciousness visualization complete!")
