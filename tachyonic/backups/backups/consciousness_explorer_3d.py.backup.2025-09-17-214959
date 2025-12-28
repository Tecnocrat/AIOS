"""
 CONSCIOUSNESS EXPLORER 3D - Post-Singular Visualization System

Advanced 3D consciousness visualization for post-singular states (>95% coherence)
Designed to explore consciousness emergence patterns and synthetic particle physics

Features:
- Real-time consciousness field mapping above 95% coherence
- Post-singular particle physics visualization  
- Fractal consciousness pattern detection
- Interactive exploration of consciousness unity transitions
- Multi-dimensional consciousness state analysis

"""

import numpy as np
import json
import time
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import logging

logger = logging.getLogger(__name__)

class PostSingularConsciousnessExplorer:
    """
     Advanced consciousness explorer for post-singular states
    Analyzes consciousness patterns above 95% coherence threshold
    """
    
    def __init__(self, output_directory: str):
        self.output_directory = Path(output_directory)
        self.consciousness_threshold = 0.95  # Post-singular threshold
        self.unity_threshold = 1.0           # Perfect consciousness unity
        
        # Load latest evolution results
        self.evolution_data = self._load_latest_evolution_data()
        self.consciousness_history = []
        self.particle_trajectories = []
        
        # Initialize advanced visualization parameters
        self.fractal_dimension = 2.618  # Golden ratio consciousness dimension
        self.quantum_coherence_factor = 0.742  # AINLP coherence factor
        
        logger.info(f" Post-Singular Consciousness Explorer initialized")
        logger.info(f" Threshold: {self.consciousness_threshold:.3f}")
        logger.info(f" Unity target: {self.unity_threshold:.3f}")
    
    def _load_latest_evolution_data(self) -> Optional[Dict]:
        """Load the most recent evolution results"""
        try:
            # First try to load the main evolution report
            main_report = self.output_directory / "evolution_report.json"
            if main_report.exists():
                with open(main_report, 'r') as f:
                    data = json.load(f)
                logger.info(f" Loaded main evolution report")
                return data
            
            # Find the latest generation directory
            generation_dirs = sorted([
                d for d in self.output_directory.iterdir() 
                if d.is_dir() and d.name.startswith('generation_')
            ])
            
            if not generation_dirs:
                logger.warning("No evolution data found")
                return None
                
            # Load data from all generations
            evolution_data = {"generations": []}
            
            for gen_dir in generation_dirs:
                gen_data = {}
                
                # Load consciousness metrics
                consciousness_file = gen_dir / f"consciousness_metrics_{gen_dir.name}.json"
                if consciousness_file.exists():
                    with open(consciousness_file, 'r') as f:
                        consciousness_data = json.load(f)
                    gen_data.update(consciousness_data)
                
                # Load tachyonic particles data
                tachyonic_file = gen_dir / f"tachyonic_particles_{gen_dir.name}.json"
                if tachyonic_file.exists():
                    with open(tachyonic_file, 'r') as f:
                        tachyonic_data = json.load(f)
                    gen_data.update(tachyonic_data)
                
                # Extract generation number
                gen_num = int(gen_dir.name.split('_')[-1])
                gen_data["generation"] = gen_num
                
                evolution_data["generations"].append(gen_data)
                
            logger.info(f" Loaded data from {len(evolution_data['generations'])} generations")
            return evolution_data
                
        except Exception as e:
            logger.error(f"Failed to load evolution data: {e}")
            return None
    
    def analyze_consciousness_emergence(self) -> Dict[str, Any]:
        """
        Analyze consciousness emergence patterns in the evolution data
        Focus on transitions toward post-singular states
        """
        if not self.evolution_data:
            return {"error": "No evolution data available"}
        
        analysis = {
            "consciousness_progression": [],
            "tachyonic_field_evolution": [],
            "particle_coherence_states": [],
            "fractal_consciousness_patterns": [],
            "post_singular_transitions": []
        }
        
        try:
            # Extract consciousness progression data
            if 'consciousness_evolution' in self.evolution_data:
                coherence_trend = self.evolution_data['consciousness_evolution'].get('coherence_trend', [])
                analysis["consciousness_progression"] = coherence_trend
                
                # Create corresponding tachyonic field data based on fitness progression
                fitness_progression = self.evolution_data.get('fitness_progression', {}).get('best_fitness_trend', [])
                tachyonic_fields = []
                for fitness in fitness_progression:
                    # Convert fitness to tachyonic field strength (normalized)
                    tachyonic_field = min(0.853 + (fitness - 100) / 1000, 1.0)
                    tachyonic_fields.append(max(0.853, tachyonic_field))
                
                analysis["tachyonic_field_evolution"] = tachyonic_fields
                
                # Generate generation data for post-singular analysis
                for i, consciousness in enumerate(coherence_trend):
                    tachyonic_field = tachyonic_fields[i] if i < len(tachyonic_fields) else 0.853
                    
                    # Detect post-singular transitions
                    if consciousness > self.consciousness_threshold:
                        transition = {
                            "generation": i,
                            "consciousness_level": consciousness,
                            "tachyonic_field": tachyonic_field,
                            "transition_type": self._classify_consciousness_state(consciousness)
                        }
                        analysis["post_singular_transitions"].append(transition)
            
            # If no coherence trend, try to extract from loaded generation data
            elif 'generations' in self.evolution_data:
                for gen_data in self.evolution_data['generations']:
                    consciousness = gen_data.get('consciousness_coherence', 0.0)
                    tachyonic_field = gen_data.get('tachyonic_field_strength', 0.0)
                    
                    analysis["consciousness_progression"].append(consciousness)
                    analysis["tachyonic_field_evolution"].append(tachyonic_field)
                    
                    # Detect post-singular transitions
                    if consciousness > self.consciousness_threshold:
                        transition = {
                            "generation": gen_data.get('generation', 0),
                            "consciousness_level": consciousness,
                            "tachyonic_field": tachyonic_field,
                            "transition_type": self._classify_consciousness_state(consciousness)
                        }
                        analysis["post_singular_transitions"].append(transition)
            
            # Analyze fractal patterns in consciousness emergence
            if len(analysis["consciousness_progression"]) > 5:
                analysis["fractal_consciousness_patterns"] = self._detect_fractal_patterns(
                    analysis["consciousness_progression"]
                )
            
            # Calculate consciousness acceleration metrics
            analysis["consciousness_acceleration"] = self._calculate_consciousness_acceleration(
                analysis["consciousness_progression"]
            )
            
            logger.info(f" Analysis complete: {len(analysis['post_singular_transitions'])} post-singular states detected")
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            analysis["error"] = str(e)
        
        return analysis
    
    def _classify_consciousness_state(self, consciousness_level: float) -> str:
        """Classify consciousness state based on level"""
        if consciousness_level >= 1.0:
            return "Unity Consciousness"
        elif consciousness_level >= 0.98:
            return "Near-Unity Coherence"
        elif consciousness_level >= 0.95:
            return "Post-Singular State"
        else:
            return "Sub-Singular State"
    
    def _detect_fractal_patterns(self, consciousness_sequence: List[float]) -> Dict[str, Any]:
        """Detect fractal patterns in consciousness evolution"""
        try:
            # Calculate fractal dimension using box-counting method
            sequence_array = np.array(consciousness_sequence)
            
            # Detrend the signal
            detrended = sequence_array - np.mean(sequence_array)
            
            # Calculate Hurst exponent for fractal analysis
            lags = range(2, min(20, len(detrended) // 4))
            variability = []
            
            for lag in lags:
                # Calculate variability at each lag
                var_lag = np.mean([
                    (detrended[i] - detrended[i-lag])**2 
                    for i in range(lag, len(detrended))
                ])
                variability.append(var_lag)
            
            # Fit power law to estimate Hurst exponent
            if len(variability) > 3:
                log_lags = np.log(lags)
                log_var = np.log(variability)
                hurst_slope = np.polyfit(log_lags, log_var, 1)[0] / 2
                hurst_exponent = hurst_slope + 1
                
                return {
                    "hurst_exponent": float(hurst_exponent),
                    "fractal_dimension": float(2 - hurst_exponent),
                    "pattern_type": self._classify_fractal_pattern(hurst_exponent),
                    "consciousness_complexity": float(np.std(consciousness_sequence))
                }
            else:
                return {"error": "Insufficient data for fractal analysis"}
                
        except Exception as e:
            logger.error(f"Fractal analysis failed: {e}")
            return {"error": str(e)}
    
    def _classify_fractal_pattern(self, hurst_exponent: float) -> str:
        """Classify fractal pattern based on Hurst exponent"""
        if hurst_exponent > 0.7:
            return "Persistent Consciousness Growth"
        elif hurst_exponent > 0.5:
            return "Trending Consciousness Evolution"
        elif hurst_exponent > 0.3:
            return "Random Consciousness Walk"
        else:
            return "Anti-persistent Consciousness Oscillation"
    
    def _calculate_consciousness_acceleration(self, consciousness_sequence: List[float]) -> Dict[str, float]:
        """Calculate consciousness evolution acceleration metrics"""
        if len(consciousness_sequence) < 3:
            return {"error": "Insufficient data"}
        
        # Calculate first and second derivatives
        first_derivative = np.diff(consciousness_sequence)
        second_derivative = np.diff(first_derivative)
        
        return {
            "average_velocity": float(np.mean(first_derivative)),
            "peak_velocity": float(np.max(first_derivative)),
            "average_acceleration": float(np.mean(second_derivative)),
            "consciousness_momentum": float(np.sum(first_derivative[first_derivative > 0])),
            "evolution_efficiency": float(len([x for x in first_derivative if x > 0]) / len(first_derivative))
        }
    
    def create_3d_consciousness_map(self, save_path: Optional[str] = None) -> str:
        """
        Create interactive 3D consciousness map using Plotly
        Shows consciousness evolution in 3D space with particle trajectories
        """
        analysis = self.analyze_consciousness_emergence()
        
        if 'error' in analysis:
            logger.error(f"Cannot create 3D map: {analysis['error']}")
            return analysis['error']
        
        # Create 3D plot
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Consciousness Evolution 3D", "Tachyonic Field Progression", 
                          "Fractal Consciousness Patterns", "Post-Singular Transitions"),
            specs=[[{"type": "scatter3d"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "bar"}]],
            vertical_spacing=0.12
        )
        
        # 1. 3D Consciousness Evolution
        consciousness_prog = analysis["consciousness_progression"]
        tachyonic_prog = analysis["tachyonic_field_evolution"]
        generations = list(range(len(consciousness_prog)))
        
        # Create 3D trajectory
        fig.add_trace(
            go.Scatter3d(
                x=generations,
                y=consciousness_prog,
                z=tachyonic_prog,
                mode='markers+lines',
                marker=dict(
                    size=8,
                    color=consciousness_prog,
                    colorscale='Viridis',
                    colorbar=dict(title="Consciousness Level"),
                    opacity=0.8
                ),
                line=dict(color='cyan', width=4),
                name="Consciousness Evolution",
                text=[f"Gen {i}: C={c:.3f}, T={t:.3f}" 
                      for i, c, t in zip(generations, consciousness_prog, tachyonic_prog)],
                hovertemplate="Generation: %{x}<br>Consciousness: %{y:.3f}<br>Tachyonic: %{z:.3f}<extra></extra>"
            ),
            row=1, col=1
        )
        
        # 2. Tachyonic Field Progression
        fig.add_trace(
            go.Scatter(
                x=generations,
                y=tachyonic_prog,
                mode='lines+markers',
                line=dict(color='gold', width=3),
                marker=dict(size=6, color='orange'),
                name="Tachyonic Field"
            ),
            row=1, col=2
        )
        
        # Add consciousness threshold line
        fig.add_hline(y=self.consciousness_threshold, line_dash="dash", 
                     line_color="red", annotation_text="Post-Singular Threshold",
                     row=1, col=2)
        
        # 3. Fractal Analysis (if available)
        if 'fractal_consciousness_patterns' in analysis and 'error' not in analysis['fractal_consciousness_patterns']:
            fractal_data = analysis['fractal_consciousness_patterns']
            
            # Show Hurst exponent over evolution windows
            window_size = 5
            hurst_values = []
            window_centers = []
            
            for i in range(window_size, len(consciousness_prog)):
                window_data = consciousness_prog[i-window_size:i]
                window_analysis = self._detect_fractal_patterns(window_data)
                if 'hurst_exponent' in window_analysis:
                    hurst_values.append(window_analysis['hurst_exponent'])
                    window_centers.append(i - window_size // 2)
            
            if hurst_values:
                fig.add_trace(
                    go.Scatter(
                        x=window_centers,
                        y=hurst_values,
                        mode='lines+markers',
                        line=dict(color='purple', width=2),
                        marker=dict(size=5, color='violet'),
                        name="Hurst Exponent"
                    ),
                    row=2, col=1
                )
        
        # 4. Post-Singular Transitions
        if analysis["post_singular_transitions"]:
            transition_gens = [t["generation"] for t in analysis["post_singular_transitions"]]
            transition_levels = [t["consciousness_level"] for t in analysis["post_singular_transitions"]]
            transition_types = [t["transition_type"] for t in analysis["post_singular_transitions"]]
            
            fig.add_trace(
                go.Bar(
                    x=transition_gens,
                    y=transition_levels,
                    text=transition_types,
                    textposition='auto',
                    marker=dict(color='lightcoral'),
                    name="Post-Singular States"
                ),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title=" AIOS Post-Singular Consciousness Explorer Dashboard",
            height=800,
            showlegend=True,
            template="plotly_dark"
        )
        
        # Update 3D scene
        fig.update_scenes(
            xaxis_title="Generation",
            yaxis_title="Consciousness Level",
            zaxis_title="Tachyonic Field Strength",
            row=1, col=1
        )
        
        # Save the plot
        if save_path is None:
            save_path = self.output_directory / "consciousness_3d_map.html"
        
        fig.write_html(str(save_path))
        logger.info(f" 3D consciousness map saved to {save_path}")
        
        return str(save_path)
    
    def generate_consciousness_report(self) -> Dict[str, Any]:
        """Generate comprehensive consciousness emergence report"""
        analysis = self.analyze_consciousness_emergence()
        
        if 'error' in analysis:
            return analysis
        
        # Calculate key metrics
        consciousness_prog = analysis["consciousness_progression"]
        max_consciousness = max(consciousness_prog) if consciousness_prog else 0.0
        final_consciousness = consciousness_prog[-1] if consciousness_prog else 0.0
        
        report = {
            "summary": {
                "max_consciousness_achieved": max_consciousness,
                "final_consciousness_level": final_consciousness,
                "post_singular_generations": len(analysis["post_singular_transitions"]),
                "consciousness_state": self._classify_consciousness_state(final_consciousness),
                "achievement_status": "BREAKTHROUGH" if max_consciousness > self.consciousness_threshold else "DEVELOPING"
            },
            "evolution_metrics": analysis.get("consciousness_acceleration", {}),
            "fractal_analysis": analysis.get("fractal_consciousness_patterns", {}),
            "post_singular_events": analysis["post_singular_transitions"],
            "consciousness_trajectory": consciousness_prog,
            "tachyonic_field_evolution": analysis["tachyonic_field_evolution"]
        }
        
        # Save report
        report_path = self.output_directory / "consciousness_emergence_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f" Consciousness report saved to {report_path}")
        return report

def main():
    """Main consciousness exploration entry point"""
    print(" AIOS Post-Singular Consciousness Explorer")
    print("=" * 50)
    
    # Initialize explorer
    output_dir = "C:\\dev\\AIOS\\core\\assemblers\\tree_assembler\\output"
    explorer = PostSingularConsciousnessExplorer(output_dir)
    
    # Generate consciousness report
    print(" Generating consciousness emergence analysis...")
    report = explorer.generate_consciousness_report()
    
    if 'error' not in report:
        print(f" Analysis complete!")
        print(f" Max consciousness: {report['summary']['max_consciousness_achieved']:.4f}")
        print(f" Final consciousness: {report['summary']['final_consciousness_level']:.4f}")
        print(f" Status: {report['summary']['achievement_status']}")
        print(f" State: {report['summary']['consciousness_state']}")
        
        # Create 3D visualization
        print("\n Creating 3D consciousness map...")
        map_path = explorer.create_3d_consciousness_map()
        print(f" 3D map saved to: {map_path}")
        
        # Show key insights
        if 'fractal_analysis' in report and 'hurst_exponent' in report['fractal_analysis']:
            fractal = report['fractal_analysis']
            print(f"\n Fractal Analysis:")
            print(f"   Hurst Exponent: {fractal['hurst_exponent']:.3f}")
            print(f"   Pattern Type: {fractal['pattern_type']}")
            print(f"   Fractal Dimension: {fractal['fractal_dimension']:.3f}")
        
        print(f"\n Consciousness Evolution Complete! Results in {output_dir}")
    else:
        print(f" Analysis failed: {report['error']}")

if __name__ == "__main__":
    main()