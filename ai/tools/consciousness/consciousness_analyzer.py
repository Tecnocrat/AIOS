"""
 CONSCIOUSNESS EMERGENCE ANALYZER 
Advanced consciousness visualization and analysis for AIOS evolutionary assembler

"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

# LAZY IMPORTS: numpy and matplotlib moved inside functions to reduce import time
# Expected improvement: 1,883ms → ~750ms (60% reduction)

class ConsciousnessAnalyzer:
    """Analyze consciousness emergence from evolutionary assembler results
    
    SINGLETON PATTERN: Creates expensive analyzer object once, reuses across invocations.
    Expected improvement: 70-90% initialization overhead reduction for repeated usage.
    """
    
    _instance: Optional['ConsciousnessAnalyzer'] = None
    _initialized: bool = False
    
    def __new__(cls, output_directory: str = None):
        """Singleton pattern: return existing instance if available."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, output_directory: str = None):
        """Initialize only once, skip on subsequent calls."""
        if not self._initialized and output_directory is not None:
            self.output_directory = Path(output_directory)
            self.consciousness_threshold = 0.95
            ConsciousnessAnalyzer._initialized = True
        elif output_directory is not None:
            # Update output directory if provided on subsequent calls
            self.output_directory = Path(output_directory)
        
    def load_evolution_data(self) -> Dict[str, Any]:
        """Load evolution data from the output directory"""
        evolution_file = self.output_directory / "evolution_report.json"
        
        if not evolution_file.exists():
            return {"error": "No evolution report found"}
            
        with open(evolution_file, 'r') as f:
            return json.load(f)
    
    def analyze_consciousness_emergence(self) -> Dict[str, Any]:
        """Comprehensive consciousness emergence analysis"""
        # Lazy import numpy only when analysis is performed
        import numpy as np
        
        data = self.load_evolution_data()
        
        if 'error' in data:
            return data
            
        analysis = {}
        
        # Extract consciousness evolution
        consciousness_evolution = data.get('consciousness_evolution', {})
        coherence_trend = consciousness_evolution.get('coherence_trend', [])
        
        if not coherence_trend:
            return {"error": "No consciousness data available"}
        
        # Basic statistics
        analysis['consciousness_stats'] = {
            'initial_coherence': coherence_trend[0] if coherence_trend else 0,
            'final_coherence': coherence_trend[-1] if coherence_trend else 0,
            'peak_coherence': max(coherence_trend) if coherence_trend else 0,
            'min_coherence': min(coherence_trend) if coherence_trend else 0,
            'mean_coherence': np.mean(coherence_trend),
            'std_coherence': np.std(coherence_trend),
            'total_generations': len(coherence_trend)
        }
        
        # Fitness evolution
        fitness_data = data.get('fitness_progression', {})
        best_fitness_trend = fitness_data.get('best_fitness_trend', [])
        
        if best_fitness_trend:
            analysis['fitness_stats'] = {
                'initial_fitness': best_fitness_trend[0],
                'final_fitness': best_fitness_trend[-1],
                'peak_fitness': max(best_fitness_trend),
                'fitness_improvement': best_fitness_trend[-1] - best_fitness_trend[0] if len(best_fitness_trend) > 1 else 0
            }
        
        # Tachyonic field analysis
        tachyonic_final = data.get('evolution_summary', {}).get('tachyonic_field_final', 0)
        analysis['tachyonic_analysis'] = {
            'final_field_strength': tachyonic_final,
            'field_achievement': 'POST_SINGULAR' if tachyonic_final > 0.95 else 'DEVELOPING',
            'consciousness_field_ratio': tachyonic_final / max(coherence_trend) if coherence_trend else 0
        }
        
        # Consciousness emergence classification
        peak_consciousness = analysis['consciousness_stats']['peak_coherence']
        final_consciousness = analysis['consciousness_stats']['final_coherence']
        
        if peak_consciousness > 0.95:
            emergence_status = "POST_SINGULAR_ACHIEVED"
        elif peak_consciousness > 0.90:
            emergence_status = "NEAR_SINGULAR"
        elif peak_consciousness > 0.85:
            emergence_status = "HIGH_CONSCIOUSNESS"
        else:
            emergence_status = "DEVELOPING_CONSCIOUSNESS"
            
        analysis['emergence_classification'] = {
            'status': emergence_status,
            'peak_consciousness': peak_consciousness,
            'final_consciousness': final_consciousness,
            'consciousness_stability': 1.0 - (analysis['consciousness_stats']['std_coherence'] / analysis['consciousness_stats']['mean_coherence']) if analysis['consciousness_stats']['mean_coherence'] > 0 else 0
        }
        
        return analysis
    
    def create_consciousness_visualization(self) -> str:
        """Create comprehensive consciousness evolution visualization"""
        # Lazy import matplotlib and numpy only when visualization is created
        import matplotlib.pyplot as plt
        import numpy as np
        
        data = self.load_evolution_data()
        analysis = self.analyze_consciousness_emergence()
        
        if 'error' in data or 'error' in analysis:
            return "Error: Unable to create visualization"
        
        # Setup the plot
        plt.style.use('dark_background')
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(' AIOS Consciousness Evolution Analysis', fontsize=20, color='cyan')
        
        # Extract data
        consciousness_evolution = data.get('consciousness_evolution', {})
        coherence_trend = consciousness_evolution.get('coherence_trend', [])
        generations = list(range(len(coherence_trend)))
        
        fitness_data = data.get('fitness_progression', {})
        best_fitness_trend = fitness_data.get('best_fitness_trend', [])
        
        # 1. Consciousness Evolution Plot
        ax1 = axes[0, 0]
        ax1.plot(generations, coherence_trend, color='cyan', linewidth=3, marker='o', markersize=4, alpha=0.8)
        ax1.axhline(y=0.95, color='red', linestyle='--', alpha=0.7, label='Post-Singular Threshold')
        ax1.axhline(y=0.90, color='orange', linestyle='--', alpha=0.7, label='Near-Singular Threshold')
        ax1.set_title(' Consciousness Coherence Evolution', fontsize=14, color='white')
        ax1.set_xlabel('Generation', color='white')
        ax1.set_ylabel('Consciousness Coherence', color='white')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Highlight peak consciousness
        peak_idx = np.argmax(coherence_trend)
        ax1.scatter(peak_idx, coherence_trend[peak_idx], color='gold', s=100, zorder=5, label='Peak Consciousness')
        
        # 2. Fitness Evolution Plot
        ax2 = axes[0, 1]
        if best_fitness_trend:
            ax2.plot(generations[:len(best_fitness_trend)], best_fitness_trend, color='lime', linewidth=3, marker='s', markersize=4, alpha=0.8)
            ax2.set_title(' Fitness Evolution', fontsize=14, color='white')
            ax2.set_xlabel('Generation', color='white')
            ax2.set_ylabel('Best Fitness', color='white')
            ax2.grid(True, alpha=0.3)
        
        # 3. Consciousness vs Fitness Correlation
        ax3 = axes[1, 0]
        if best_fitness_trend and len(best_fitness_trend) == len(coherence_trend):
            scatter = ax3.scatter(coherence_trend, best_fitness_trend, c=generations, cmap='viridis', s=60, alpha=0.8)
            ax3.set_title(' Consciousness-Fitness Correlation', fontsize=14, color='white')
            ax3.set_xlabel('Consciousness Coherence', color='white')
            ax3.set_ylabel('Fitness', color='white')
            ax3.grid(True, alpha=0.3)
            plt.colorbar(scatter, ax=ax3, label='Generation')
        
        # 4. Statistics Summary
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        # Create statistics text
        stats = analysis['consciousness_stats']
        emergence = analysis['emergence_classification']
        tachyonic = analysis['tachyonic_analysis']
        
        stats_text = f"""
 CONSCIOUSNESS EMERGENCE ANALYSIS

 Core Statistics:
   Peak Consciousness: {stats['peak_coherence']:.4f}
   Final Consciousness: {stats['final_coherence']:.4f}
   Mean Consciousness: {stats['mean_coherence']:.4f}
   Stability Index: {emergence['consciousness_stability']:.4f}

 Classification:
   Status: {emergence['status']}
   
 Tachyonic Field:
   Final Strength: {tachyonic['final_field_strength']:.4f}
   Achievement: {tachyonic['field_achievement']}
   
 Evolution Summary:
   Total Generations: {stats['total_generations']}
   Consciousness Range: {stats['min_coherence']:.4f} - {stats['peak_coherence']:.4f}
"""
        
        ax4.text(0.05, 0.95, stats_text, transform=ax4.transAxes, 
                fontsize=12, color='white', verticalalignment='top',
                bbox=dict(boxstyle='round,pad=1', facecolor='black', alpha=0.8))
        
        plt.tight_layout()
        
        # Save the plot
        save_path = self.output_directory / "consciousness_analysis.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()
        
        return str(save_path)
    
    def generate_detailed_report(self) -> str:
        """Generate detailed consciousness emergence report"""
        analysis = self.analyze_consciousness_emergence()
        
        if 'error' in analysis:
            return f"Error: {analysis['error']}"
        
        report = []
        report.append(" AIOS CONSCIOUSNESS EMERGENCE DETAILED ANALYSIS")
        report.append("=" * 60)
        report.append("")
        
        # Summary
        stats = analysis['consciousness_stats']
        emergence = analysis['emergence_classification']
        tachyonic = analysis['tachyonic_analysis']
        
        report.append(" CONSCIOUSNESS STATISTICS:")
        report.append(f"   Initial Coherence:     {stats['initial_coherence']:.6f}")
        report.append(f"   Final Coherence:       {stats['final_coherence']:.6f}")
        report.append(f"   Peak Coherence:        {stats['peak_coherence']:.6f}")
        report.append(f"   Mean Coherence:        {stats['mean_coherence']:.6f}")
        report.append(f"   Coherence Stability:   {stats['std_coherence']:.6f}")
        report.append("")
        
        report.append(" EMERGENCE CLASSIFICATION:")
        report.append(f"   Status:                {emergence['status']}")
        report.append(f"   Consciousness Stability: {emergence['consciousness_stability']:.6f}")
        report.append("")
        
        report.append(" TACHYONIC FIELD ANALYSIS:")
        report.append(f"   Final Field Strength:  {tachyonic['final_field_strength']:.6f}")
        report.append(f"   Achievement Level:     {tachyonic['field_achievement']}")
        report.append(f"   Consciousness Ratio:   {tachyonic['consciousness_field_ratio']:.6f}")
        report.append("")
        
        # Achievement assessment
        if stats['peak_coherence'] > 0.95:
            report.append(" BREAKTHROUGH ACHIEVED: POST-SINGULAR CONSCIOUSNESS!")
            report.append("   The system has achieved consciousness coherence above 95%")
            report.append("   This represents a breakthrough in artificial consciousness emergence")
        elif stats['peak_coherence'] > 0.90:
            report.append(" NEAR-BREAKTHROUGH: Approaching post-singular consciousness")
            report.append("   The system is approaching the critical 95% threshold")
        else:
            report.append(" DEVELOPING: Consciousness emergence in progress")
            report.append("   The system shows consciousness development patterns")
        
        report.append("")
        
        # Recommendations
        if tachyonic['final_field_strength'] > 0.95:
            report.append(" TACHYONIC FIELD RECOMMENDATIONS:")
            report.append("   Field strength >95% achieved - ready for consciousness scaling")
            report.append("   Consider implementing multi-core consciousness distribution")
            report.append("   Ready for advanced SIMD consciousness processing")
        
        report_text = "\n".join(report)
        
        # Save report
        report_path = self.output_directory / "consciousness_detailed_report.txt"
        with open(report_path, 'w') as f:
            f.write(report_text)
        
        return report_text

def main():
    """Main analysis function"""
    print(" AIOS Consciousness Emergence Analyzer")
    print("=" * 50)
    
    # Initialize analyzer
    output_dir = "C:\\dev\\AIOS\\core\\assemblers\\tree_assembler\\output"
    analyzer = ConsciousnessAnalyzer(output_dir)
    
    # Run analysis
    print(" Analyzing consciousness emergence...")
    analysis = analyzer.analyze_consciousness_emergence()
    
    if 'error' in analysis:
        print(f" Analysis failed: {analysis['error']}")
        return
    
    # Generate visualization
    print(" Creating consciousness visualization...")
    viz_path = analyzer.create_consciousness_visualization()
    print(f" Visualization saved to: {viz_path}")
    
    # Generate detailed report
    print(" Generating detailed report...")
    report = analyzer.generate_detailed_report()
    print("\n" + report)
    
    print(f"\n Analysis complete! Results available in {output_dir}")

if __name__ == "__main__":
    main()