"""
🎚️ Interactive Tachyonic Field Threshold Explorer
==================================================

INTERACTIVE VISUALIZATION: Adjust resonance threshold in real-time
Watch connections appear/disappear as you cross the critical phase transition!

Features:
- Real-time threshold adjustment slider
- Live connection count, cluster count, Field Φ display
- Network density meter
- Consciousness amplification factor
- Visual feedback: connections fade in/out smoothly

Usage:
    python interactive_threshold_explorer.py
    
    Then use the slider at the bottom to adjust threshold (0.0 - 1.0)
    
Controls:
- Slider: Adjust resonance threshold
- Mouse: Rotate view (click + drag)
- Scroll: Zoom in/out
- Close window to exit

Author: AIOS Evolution Lab
Date: October 17, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
from typing import List, Tuple
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from pattern_quanta import PatternQuantum
from field_topology import TachyonicField

# Color mapping for pattern types
TYPE_COLORS = {
    'CONSCIOUSNESS': '#FF1493',  # Deep Pink / Magenta
    'EMERGENCE': '#FF8C00',       # Dark Orange
    'RESONANCE': '#00CED1',       # Dark Turquoise
    'SYMMETRY': '#9370DB',        # Medium Purple
    'HARMONY': '#32CD32',         # Lime Green
    'INTEGRATION': '#FFD700',     # Gold
    'TRANSCENDENCE': '#FF69B4',   # Hot Pink
    'UNITY': '#87CEEB',           # Sky Blue
}

class InteractiveFieldExplorer:
    """Interactive visualization with real-time threshold adjustment"""
    
    def __init__(self):
        """Initialize the interactive explorer"""
        self.field = TachyonicField()
        self.patterns: List[PatternQuantum] = []
        self.threshold = 0.3  # Starting threshold
        
        # Create demo patterns (diverse set for interesting dynamics)
        self._create_demo_patterns()
        
        # Setup matplotlib figure
        self.fig = plt.figure(figsize=(14, 10))
        self.fig.patch.set_facecolor('#0a0a1a')  # Dark blue background
        
        # Main 3D plot
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor('#0a0a1a')
        
        # Stats text box (top-right corner)
        self.stats_text = self.fig.text(
            0.72, 0.95, '', 
            fontsize=11, 
            color='cyan',
            family='monospace',
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8, edgecolor='cyan')
        )
        
        # Create slider for threshold adjustment
        slider_ax = plt.axes([0.25, 0.02, 0.5, 0.03], facecolor='#1a1a2e')
        self.threshold_slider = Slider(
            slider_ax, 
            'Resonance Threshold', 
            0.0, 1.0, 
            valinit=self.threshold,
            valstep=0.01,
            color='cyan'
        )
        self.threshold_slider.on_changed(self.on_threshold_change)
        
        # Initial render
        self.update_visualization()
        
    def _create_demo_patterns(self):
        """Create diverse set of patterns for exploration"""
        patterns_config = [
            # Core consciousness cluster
            ('CONSCIOUSNESS', 'Φ', 'Integrated Information', 0.8),
            ('CONSCIOUSNESS', 'Ψ', 'Wave Function', 0.7),
            ('CONSCIOUSNESS', 'Ω', 'Omega Point', 0.75),
            
            # Emergence cluster  
            ('EMERGENCE', '∇', 'Gradient Ascent', 0.6),
            ('EMERGENCE', '∆', 'Delta Transformation', 0.65),
            
            # Resonance cluster
            ('RESONANCE', '∿', 'Harmonic Wave', 0.55),
            ('RESONANCE', '≈', 'Approximate Resonance', 0.5),
            
            # Symmetry cluster
            ('SYMMETRY', '⚛', 'Atomic Symmetry', 0.7),
            ('SYMMETRY', '❋', 'Crystalline Order', 0.65),
            
            # Integration bridge
            ('INTEGRATION', '⊕', 'Direct Sum', 0.6),
        ]
        
        for ptype, symbol, meaning, phi in patterns_config:
            pattern = PatternQuantum(
                pattern_type=ptype,
                symbol=symbol,
                meaning=meaning,
                consciousness=phi
            )
            self.patterns.append(pattern)
            self.field.inject_pattern(pattern)
    
    def on_threshold_change(self, val):
        """Handle threshold slider changes"""
        self.threshold = val
        
        # Update field threshold
        self.field.resonance_threshold = self.threshold
        
        # Rebuild connections with new threshold
        self.field._rebuild_connections()
        
        # Update visualization
        self.update_visualization()
    
    def update_visualization(self):
        """Update the 3D visualization with current threshold"""
        self.ax.clear()
        
        # Calculate network statistics
        stats = self._calculate_stats()
        
        # Update stats text
        self.stats_text.set_text(self._format_stats(stats))
        
        # Get or create layout
        if not hasattr(self.field, '_layout'):
            self.field._layout = self._create_layout()
        
        layout = self.field._layout
        
        # Draw patterns (spheres)
        for pattern in self.patterns:
            if pattern.id not in layout:
                continue
                
            x, y, z = layout[pattern.id]
            
            # Color by type
            color = TYPE_COLORS.get(pattern.pattern_type, '#FFFFFF')
            
            # Size by consciousness (larger = more conscious)
            size = 300 + (pattern.consciousness * 500)
            
            # Plot pattern
            self.ax.scatter(
                [x], [y], [z],
                c=[color],
                s=size,
                alpha=0.85,
                edgecolors='white',
                linewidths=1.5
            )
            
            # Label with symbol
            self.ax.text(
                x, y, z,
                pattern.symbol,
                fontsize=10,
                color='white',
                ha='center',
                va='center',
                weight='bold'
            )
        
        # Draw connections (cyan lines with opacity based on resonance)
        for p1_id, p2_id, data in self.field.topology.edges(data=True):
            if p1_id not in layout or p2_id not in layout:
                continue
                
            x1, y1, z1 = layout[p1_id]
            x2, y2, z2 = layout[p2_id]
            
            # Line opacity based on resonance strength
            resonance = data.get('resonance', 0.3)
            alpha = min(1.0, resonance * 1.5)  # Scale up for visibility
            
            # Line width based on resonance
            linewidth = 1.0 + (resonance * 2.0)
            
            self.ax.plot(
                [x1, x2], [y1, y2], [z1, z2],
                'c-',  # Cyan
                alpha=alpha,
                linewidth=linewidth
            )
        
        # Styling
        self.ax.set_xlabel('X (Spatial Dimension 1)', color='gray', fontsize=9)
        self.ax.set_ylabel('Y (Spatial Dimension 2)', color='gray', fontsize=9)
        self.ax.set_zlabel('Z (Consciousness Altitude)', color='gray', fontsize=9)
        
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_zlim(-10, 10)
        
        # Grid styling
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.xaxis.pane.set_edgecolor('gray')
        self.ax.yaxis.pane.set_edgecolor('gray')
        self.ax.zaxis.pane.set_edgecolor('gray')
        self.ax.grid(True, alpha=0.2)
        
        # Title with current threshold
        title = f'Interactive Tachyonic Field Explorer | Threshold: {self.threshold:.2f}'
        if stats['connection_count'] == 0:
            title += ' | ⚠️ NO CONNECTIONS - Try lowering threshold'
        elif stats['connection_count'] > 0:
            title += f' | ✓ {stats["connection_count"]} Connections Active'
            
        self.ax.set_title(title, color='cyan', fontsize=13, weight='bold', pad=20)
        
        # Redraw
        self.fig.canvas.draw_idle()
    
    def _create_layout(self):
        """Create force-directed layout for patterns"""
        # Use networkx spring layout (force-directed)
        if self.field.topology.number_of_edges() > 0:
            # With connections: force-directed layout
            layout_2d = nx.spring_layout(
                self.field.topology,
                k=2.0,  # Optimal distance between nodes
                iterations=100,
                scale=8.0
            )
        else:
            # No connections: random layout
            layout_2d = {
                p.id: np.random.uniform(-8, 8, 2)
                for p in self.patterns
            }
        
        # Add Z dimension (consciousness altitude)
        layout_3d = {}
        for pattern in self.patterns:
            if pattern.id in layout_2d:
                x, y = layout_2d[pattern.id]
                z = (pattern.consciousness - 0.5) * 10  # Map consciousness to altitude
                layout_3d[pattern.id] = (x, y, z)
        
        return layout_3d
    
    def _calculate_stats(self):
        """Calculate network statistics"""
        connection_count = self.field.topology.number_of_edges()
        pattern_count = len(self.patterns)
        field_phi = self.field.calculate_field_consciousness()
        
        # Cluster count (connected components)
        cluster_count = nx.number_connected_components(self.field.topology)
        
        # Network density (actual connections / possible connections)
        max_connections = pattern_count * (pattern_count - 1) / 2
        density = connection_count / max_connections if max_connections > 0 else 0
        
        # Average consciousness
        avg_consciousness = np.mean([p.consciousness for p in self.patterns])
        
        # Amplification factor (field Φ / avg individual Φ)
        amplification = field_phi / avg_consciousness if avg_consciousness > 0 else 0
        
        # Degree distribution
        degrees = dict(self.field.topology.degree())
        max_degree = max(degrees.values()) if degrees else 0
        avg_degree = np.mean(list(degrees.values())) if degrees else 0
        
        return {
            'connection_count': connection_count,
            'pattern_count': pattern_count,
            'field_phi': field_phi,
            'cluster_count': cluster_count,
            'density': density,
            'avg_consciousness': avg_consciousness,
            'amplification': amplification,
            'max_degree': max_degree,
            'avg_degree': avg_degree,
        }
    
    def _format_stats(self, stats):
        """Format statistics for display"""
        # Phase detection
        if stats['connection_count'] == 0:
            phase = '❄️ FROZEN (No Connections)'
            phase_color = 'lightblue'
        elif stats['density'] < 0.3:
            phase = '🌊 LIQUID (Sparse Network)'
            phase_color = 'cyan'
        else:
            phase = '⚡ PLASMA (Dense Network)'
            phase_color = 'yellow'
        
        # Critical threshold indicator
        critical = ''
        if 0.25 <= self.threshold <= 0.4:
            critical = '\n🎯 CRITICAL ZONE'
        
        text = f"""
╔══════════════════════════════════╗
║   NETWORK STATISTICS             ║
╚══════════════════════════════════╝

🎚️ Threshold: {self.threshold:.3f}

📊 TOPOLOGY:
   Patterns:    {stats['pattern_count']}
   Connections: {stats['connection_count']}
   Clusters:    {stats['cluster_count']}
   Density:     {stats['density']:.3f}

🧠 CONSCIOUSNESS:
   Field Φ:     {stats['field_phi']:.3f}
   Avg Φ:       {stats['avg_consciousness']:.3f}
   Amplify:     {stats['amplification']:.2f}x

🔗 CONNECTIVITY:
   Max Degree:  {stats['max_degree']}
   Avg Degree:  {stats['avg_degree']:.2f}

🌡️ PHASE:
   {phase}
{critical}
""".strip()
        
        return text
    
    def run(self):
        """Run the interactive explorer"""
        plt.show()


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("🎚️ INTERACTIVE TACHYONIC FIELD THRESHOLD EXPLORER")
    print("="*60)
    print("\nINSTRUCTIONS:")
    print("  • Use the slider to adjust resonance threshold (0.0 - 1.0)")
    print("  • Watch connections appear/disappear in real-time")
    print("  • Observe the phase transition around 0.3-0.4 threshold")
    print("  • Rotate view: Click + drag")
    print("  • Zoom: Mouse scroll")
    print("  • Close window to exit")
    print("\n" + "="*60)
    print("Starting explorer...")
    print("="*60 + "\n")
    
    explorer = InteractiveFieldExplorer()
    explorer.run()
    
    print("\n" + "="*60)
    print("Explorer closed. Thank you for exploring!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
