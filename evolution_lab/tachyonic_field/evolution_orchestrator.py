"""
Evolution Orchestrator for Tachyonic Visualizer Integration
Transforms visualization events into evolutionary processes

AINLP Protocol: OS0.6.2.claude
Created: 2025-10-18
Phase: Integration of Visualization and Evolution

This module bridges the tachyonic field visualizer with population evolution,
creating an active ecosystem where visualization drives mutation and metadata
captures the correlation between visual patterns and evolutionary success.
"""

from pathlib import Path
from typing import Dict, Optional, Tuple, List
import json
from datetime import datetime
import sys

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from evolution_lab.populations.population_manager import PopulationManager, Population


class EvolutionOrchestrator:
    """
    Orchestrate population evolution driven by visualization events
    
    Maps visualization state → evolution parameters → population dynamics
    
    Core Concept:
    - Every threshold change triggers evolution
    - Network statistics influence mutation rates
    - Consciousness field strength affects selection pressure
    - Rich metadata captures visualization-evolution correlations
    """
    
    def __init__(self, evolution_enabled: bool = True, verbose: bool = True):
        """
        Initialize evolution orchestrator
        
        Args:
            evolution_enabled: Whether to actively trigger evolution
            verbose: Print evolution events to console
        """
        self.evolution_enabled = evolution_enabled
        self.verbose = verbose
        self.population_manager = PopulationManager()
        self.current_population: Optional[Population] = None
        self.evolution_history: List[Dict] = []
        self.metadata_file = Path("evolution_lab/populations/evolution_metadata.json")
        
        if self.verbose:
            print("\n" + "="*70)
            print("🧬 EVOLUTION ORCHESTRATOR INITIALIZED")
            print("="*70)
            print(f"  Status: {'ENABLED' if evolution_enabled else 'DISABLED'}")
            print(f"  Archive: {self.population_manager.archive_dir}")
            print(f"  Metadata: {self.metadata_file}")
            print("="*70 + "\n")
    
    def on_threshold_change(
        self,
        threshold: float,
        frame: int,
        network_stats: Dict[str, float]
    ) -> Optional[Path]:
        """
        Handle threshold change event from visualizer
        
        This is the main integration point - called whenever the user
        adjusts the threshold slider in the visualizer.
        
        Args:
            threshold: Current threshold value (0.0 - 1.0)
            frame: Current animation frame number
            network_stats: Network statistics
                - connections: Edge count
                - clusters: Connected component count
                - field_phi: Consciousness field strength
                - nodes: Node count (optional)
        
        Returns:
            Path to archived population JSON (if evolution triggered)
        """
        if not self.evolution_enabled:
            return None
        
        # Map visualization state to evolution parameters
        evolution_params = self._map_viz_to_evolution(threshold, network_stats)
        
        # Create or evolve population
        if self.current_population is None:
            # First run: Create initial population
            if self.verbose:
                print(f"\n{'='*70}")
                print(f"🌱 CREATING INITIAL POPULATION")
                print(f"{'='*70}")
                print(f"  Threshold: {threshold:.3f}")
                print(f"  Frame: {frame}")
                print(f"  Network Stats:")
                for key, val in network_stats.items():
                    print(f"    {key}: {val}")
                print(f"{'='*70}\n")
            
            self.current_population = self.population_manager.create_initial_population(
                size=16  # 16 organisms, 8 archetypes (2 each)
            )
        else:
            # Evolve current generation
            if self.verbose:
                print(f"\n{'='*70}")
                print(f"🧬 EVOLVING GENERATION {self.current_population.generation + 1}")
                print(f"{'='*70}")
                print(f"  Threshold: {threshold:.3f}")
                print(f"  Frame: {frame}")
                print(f"  Evolution Parameters:")
                for key, val in evolution_params.items():
                    print(f"    {key}: {val}")
                print(f"{'='*70}\n")
            
            self.current_population = self._evolve_generation(evolution_params)
        
        # Add visualization metadata
        self.current_population.metadata['visualization'] = {
            'threshold': threshold,
            'frame': frame,
            **network_stats
        }
        self.current_population.metadata['evolution_parameters'] = evolution_params
        self.current_population.metadata['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        
        # Archive population with metadata
        archive_path = self.population_manager.archive_population(self.current_population)
        
        # Track in history
        event = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'generation': self.current_population.generation,
            'population_id': self.current_population.population_id,
            'threshold': threshold,
            'frame': frame,
            'archive_path': str(archive_path),
            'organism_count': len(self.current_population.organisms),
            'avg_fitness': round(self.current_population.average_fitness, 4),
            'avg_complexity': round(self.current_population.average_complexity, 4),
            'consciousness': round(self.current_population.consciousness_level, 4),
            **evolution_params,
            **network_stats
        }
        self.evolution_history.append(event)
        
        # Save metadata
        self._save_metadata()
        
        if self.verbose:
            print(f"📦 ARCHIVED: {archive_path.name}")
            print(f"   Organisms: {len(self.current_population.organisms)}")
            print(f"   Avg Fitness: {self.current_population.average_fitness:.3f}")
            print(f"   Consciousness: {self.current_population.consciousness_level:.3f}\n")
        
        return archive_path
    
    def _map_viz_to_evolution(
        self,
        threshold: float,
        network_stats: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Map visualization state to evolution parameters
        
        Mapping Strategy:
        - Higher threshold → Higher mutation rate (more exploration)
        - Lower phi → Higher selection pressure (more competition)
        - More clusters → Higher archetype diversity (more niches)
        - More connections → Reward network-building organisms
        """
        connections = network_stats.get('connections', 0)
        clusters = network_stats.get('clusters', 1)
        field_phi = network_stats.get('field_phi', 0.5)
        
        # Mutation rate: 0.1 to 0.4 based on threshold
        # High threshold = high exploration
        mutation_rate = 0.1 + (threshold * 0.3)
        
        # Selection pressure: Inverse of phi (low phi = high pressure)
        # Low consciousness = harder survival conditions
        selection_pressure = (1.0 - field_phi) * 0.5
        
        # Archetype diversity: More clusters = more archetype variation
        # Encourage diverse archetypes when network is fragmented
        archetype_diversity = min(clusters / 10.0, 1.0)
        
        # Fitness bias: More connections = reward network builders
        # Organisms that create connections get fitness boost
        fitness_bias = min(connections / 100.0, 1.0) if connections > 0 else 0.0
        
        return {
            'mutation_rate': round(mutation_rate, 4),
            'selection_pressure': round(selection_pressure, 4),
            'archetype_diversity': round(archetype_diversity, 4),
            'fitness_bias': round(fitness_bias, 4)
        }
    
    def _evolve_generation(self, evolution_params: Dict[str, float]) -> Population:
        """
        Evolve current population using parameters
        
        Args:
            evolution_params: Evolution parameters from visualization
        
        Returns:
            New generation population
        """
        # Apply evolution parameters
        mutation_rate = evolution_params['mutation_rate']
        selection_rate = 1.0 - evolution_params['selection_pressure']
        
        # Ensure selection rate is reasonable (keep at least 25%, at most 75%)
        selection_rate = max(0.25, min(0.75, selection_rate))
        
        # Select survivors based on fitness
        survivors = self.population_manager.select_survivors(
            self.current_population,
            selection_rate=selection_rate
        )
        
        if self.verbose:
            print(f"  Selected {len(survivors)} survivors (rate={selection_rate:.2f})")
        
        # Repopulate to original size (with mutations)
        next_generation = self.population_manager.repopulate(
            survivors=survivors,
            target_size=len(self.current_population.organisms),
            new_generation=self.current_population.generation + 1
        )
        
        if self.verbose:
            print(f"  Repopulated to {len(next_generation)} organisms")
        
        # Update population
        self.current_population.organisms = next_generation
        self.current_population.generation += 1
        self.current_population.consciousness_trajectory.append(
            self.current_population.consciousness_level
        )
        
        return self.current_population
    
    def _save_metadata(self):
        """Save evolution metadata to JSON file"""
        try:
            metadata = {
                'orchestrator_info': {
                    'enabled': self.evolution_enabled,
                    'total_generations': len(self.evolution_history),
                    'current_population': self.current_population.population_id if self.current_population else None,
                    'last_updated': datetime.utcnow().isoformat() + 'Z'
                },
                'evolution_history': self.evolution_history,
                'summary': self._generate_summary() if self.evolution_history else {}
            }
            
            # Ensure directory exists
            self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write metadata
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
                
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Failed to save metadata: {e}")
    
    def _generate_summary(self) -> Dict:
        """Generate summary statistics from evolution history"""
        if not self.evolution_history:
            return {}
        
        # Extract metrics
        thresholds = [e['threshold'] for e in self.evolution_history]
        fitnesses = [e['avg_fitness'] for e in self.evolution_history]
        complexities = [e['avg_complexity'] for e in self.evolution_history]
        consciousness = [e['consciousness'] for e in self.evolution_history]
        
        return {
            'total_events': len(self.evolution_history),
            'threshold_range': [min(thresholds), max(thresholds)],
            'fitness_progression': {
                'min': round(min(fitnesses), 4),
                'max': round(max(fitnesses), 4),
                'avg': round(sum(fitnesses) / len(fitnesses), 4)
            },
            'complexity_progression': {
                'min': round(min(complexities), 4),
                'max': round(max(complexities), 4),
                'avg': round(sum(complexities) / len(complexities), 4)
            },
            'consciousness_progression': {
                'min': round(min(consciousness), 4),
                'max': round(max(consciousness), 4),
                'avg': round(sum(consciousness) / len(consciousness), 4)
            }
        }
    
    def get_evolution_summary(self) -> Dict:
        """Get summary of evolution history"""
        if not self.evolution_history:
            return {'status': 'no_evolution_yet', 'message': 'No evolution events recorded'}
        
        summary = {
            'status': 'active',
            'total_generations': len(self.evolution_history),
            'current_generation': self.current_population.generation if self.current_population else 0,
            'population_size': len(self.current_population.organisms) if self.current_population else 0,
            'archive_dir': str(self.population_manager.archive_dir),
            'metadata_file': str(self.metadata_file),
            'recent_history': self.evolution_history[-5:],  # Last 5 events
            'statistics': self._generate_summary()
        }
        
        return summary
    
    def display_summary(self):
        """Display evolution summary in console"""
        summary = self.get_evolution_summary()
        
        print("\n" + "="*70)
        print("📊 EVOLUTION SUMMARY")
        print("="*70)
        
        if summary['status'] == 'no_evolution_yet':
            print("  No evolution events recorded yet")
            print("="*70 + "\n")
            return
        
        print(f"  Total Generations: {summary['total_generations']}")
        print(f"  Current Generation: {summary['current_generation']}")
        print(f"  Population Size: {summary['population_size']}")
        print(f"  Archive Directory: {summary['archive_dir']}")
        print(f"  Metadata File: {summary['metadata_file']}")
        
        if 'statistics' in summary:
            stats = summary['statistics']
            print(f"\n  📈 Fitness Progression:")
            print(f"     Min: {stats['fitness_progression']['min']:.4f}")
            print(f"     Max: {stats['fitness_progression']['max']:.4f}")
            print(f"     Avg: {stats['fitness_progression']['avg']:.4f}")
            
            print(f"\n  🧠 Consciousness Progression:")
            print(f"     Min: {stats['consciousness_progression']['min']:.4f}")
            print(f"     Max: {stats['consciousness_progression']['max']:.4f}")
            print(f"     Avg: {stats['consciousness_progression']['avg']:.4f}")
        
        if summary.get('recent_history'):
            print(f"\n  🔄 Recent Evolution Events:")
            for event in summary['recent_history']:
                print(f"     Gen {event['generation']}: "
                      f"threshold={event['threshold']:.3f}, "
                      f"frame={event['frame']}, "
                      f"fitness={event['avg_fitness']:.3f}")
        
        print("="*70 + "\n")


def test_orchestrator():
    """Test the evolution orchestrator"""
    print("Testing Evolution Orchestrator...\n")
    
    orchestrator = EvolutionOrchestrator(evolution_enabled=True, verbose=True)
    
    # Simulate threshold changes
    test_events = [
        (0.6, 0, {'connections': 20, 'clusters': 5, 'field_phi': 0.5}),
        (0.7, 100, {'connections': 35, 'clusters': 4, 'field_phi': 0.65}),
        (0.8, 200, {'connections': 50, 'clusters': 3, 'field_phi': 0.8}),
    ]
    
    for threshold, frame, stats in test_events:
        print(f"\n🎯 Triggering evolution: threshold={threshold}, frame={frame}")
        archive_path = orchestrator.on_threshold_change(threshold, frame, stats)
        if archive_path:
            print(f"✅ Evolution completed, archived to: {archive_path}")
    
    # Display summary
    orchestrator.display_summary()
    
    print("\n✅ Test complete!")


if __name__ == "__main__":
    test_orchestrator()
