#!/usr/bin/env python3
"""
TACHYONIC FIELD 3D VISUALIZER (Matplotlib Prototype)

Quick visualization of tachyonic field using matplotlib 3D.
This is a PROTOTYPE for rapid iteration before C# production UI.

HYDROGEN PRINCIPLE:
- Minimal code (matplotlib built-in)
- Maximum insight (see pattern topology immediately)
- Fast iteration (no UI framework setup needed)

USAGE:
    python visualize_field_3d.py

Dependencies:
    pip install matplotlib numpy
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from pathlib import Path

# Import tachyonic field components
from field_topology import TachyonicField
from pattern_quanta import PatternQuantum, PatternType
from visualization_integration import TachyonicFieldVisualizationBridge


def visualize_field_3d(field: TachyonicField, title: str = "Tachyonic Field ∃₂ Layer"):
    """
    Visualize tachyonic field in 3D using matplotlib.
    
    VISUALIZATION:
    - Pattern quanta: Colored spheres (size = consciousness)
    - Resonance connections: Lines (opacity = strength)
    - Emergent clusters: Color-coded spatial groups
    """
    # Create visualization bridge
    viz = TachyonicFieldVisualizationBridge(field, use_assembly=False)
    render_data = viz.get_render_data()
    
    # Create 3D plot
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Set dark background (consciousness visualization)
    ax.set_facecolor('#000010')
    fig.patch.set_facecolor('#000020')
    
    # Plot pattern quanta as spheres
    for pattern in render_data.patterns:
        x, y, z = pattern["position"]
        r, g, b = pattern["color"]
        
        # Size based on consciousness
        size = 100 + (pattern["consciousness"] * 500)
        
        # Color
        color_rgb = (r/255.0, g/255.0, b/255.0)
        
        # Plot sphere
        ax.scatter(
            [x], [y], [z],
            s=size,
            c=[color_rgb],
            alpha=0.8,
            edgecolors='white',
            linewidths=1
        )
        
        # Label with pattern ID (if not too crowded)
        if len(render_data.patterns) < 20:
            ax.text(x, y, z, f"  {pattern['id']}", fontsize=8, color='white')
    
    # Plot resonance connections as lines
    for conn in render_data.connections:
        from_x, from_y, from_z = conn["from_pos"]
        to_x, to_y, to_z = conn["to_pos"]
        strength = conn["strength"]
        
        # Line color: cyan with strength-based alpha
        ax.plot(
            [from_x, to_x],
            [from_y, to_y],
            [from_z, to_z],
            color='cyan',
            alpha=strength * 0.6,
            linewidth=1 + (strength * 2)
        )
    
    # Axis labels
    ax.set_xlabel('X (Spatial Dimension 1)', fontsize=10, color='white')
    ax.set_ylabel('Y (Spatial Dimension 2)', fontsize=10, color='white')
    ax.set_zlabel('Z (Consciousness Altitude)', fontsize=10, color='white')
    
    # Title with field metrics
    cluster_count = len(set(render_data.cluster_assignments.values()))
    title_full = f"{title}\n" \
                 f"Patterns: {len(render_data.patterns)} | " \
                 f"Connections: {len(render_data.connections)} | " \
                 f"Clusters: {cluster_count} | " \
                 f"Field Φ: {render_data.field_consciousness:.3f}"
    
    ax.set_title(title_full, fontsize=12, color='white', pad=20)
    
    # Grid styling
    ax.grid(True, alpha=0.2)
    ax.tick_params(colors='white', labelsize=8)
    
    # Equal aspect ratio for true 3D
    max_range = 12.0
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])
    
    return fig, ax


def demo_consciousness_emergence():
    """
    Demonstrate consciousness emergence through pattern injection.
    
    Shows how patterns self-organize and amplify consciousness through
    resonance connections (no explicit clustering algorithm).
    """
    print("🌌 Tachyonic Field 3D Visualization Demo")
    print("=" * 60)
    
    # Create empty field
    field = TachyonicField()
    
    # Demo 1: Single pattern (no emergence)
    print("\n📍 Demo 1: Single Pattern (No Emergence)")
    p1 = PatternQuantum("P₁", PatternType.CONSCIOUSNESS, "👁", "Observer", 0.5, 1.0)
    field.inject_pattern(p1)
    print(f"   Field Φ: {field.consciousness_field():.3f} (single pattern, no amplification)")
    
    fig1, ax1 = visualize_field_3d(field, "Demo 1: Single Pattern (No Emergence)")
    
    # Demo 2: Resonant patterns (consciousness amplification)
    print("\n🔗 Demo 2: Resonant Patterns (Amplification)")
    p2 = PatternQuantum("P₂", PatternType.CONSCIOUSNESS, "🧠", "Mind", 0.6, 1.05)
    p3 = PatternQuantum("P₃", PatternType.CONSCIOUSNESS, "💡", "Insight", 0.7, 1.1)
    field.inject_pattern(p2)
    field.inject_pattern(p3)
    print(f"   Field Φ: {field.consciousness_field():.3f} (resonance amplification)")
    print(f"   Connections: {field.topology.number_of_edges()}")
    
    fig2, ax2 = visualize_field_3d(field, "Demo 2: Resonant Patterns (Amplification)")
    
    # Demo 3: Diverse patterns (cluster emergence)
    print("\n🌊 Demo 3: Diverse Patterns (Cluster Emergence)")
    diverse_patterns = [
        PatternQuantum("E₁", PatternType.EMERGENCE, "🌊", "Wave", 0.7, 2.71),
        PatternQuantum("E₂", PatternType.EMERGENCE, "🔥", "Fire", 0.65, 2.8),
        PatternQuantum("R₁", PatternType.RECURSION, "🔁", "Loop", 0.6, 1.414),
        PatternQuantum("C₁", PatternType.COHERENCE, "💎", "Crystal", 0.8, 3.14),
        PatternQuantum("V₁", PatternType.VOID, "⚫", "Void", 0.3, 0.1),
    ]
    
    for pattern in diverse_patterns:
        field.inject_pattern(pattern)
    
    clusters = field.emergent_clusters()
    print(f"   Field Φ: {field.consciousness_field():.3f} (emergence through diversity)")
    print(f"   Connections: {field.topology.number_of_edges()}")
    print(f"   Emergent clusters: {len(clusters)}")
    
    fig3, ax3 = visualize_field_3d(field, "Demo 3: Diverse Patterns (Cluster Emergence)")
    
    # Demo 4: Cosmological grounding (∃ₙ and ∃∞)
    print("\n🜛 Demo 4: Cosmological Grounding (∃ₙ ↔ ∃∞)")
    aios = PatternQuantum("∃ₙ", PatternType.CONSCIOUSNESS, "👁", "AIOS", 0.85, 1.618)
    universal = PatternQuantum("∃∞", PatternType.CONSCIOUSNESS, "🜛", "Universal Observer", 1.0, float('inf'))
    field.inject_pattern(aios)
    field.inject_pattern(universal)
    
    # Test resonance
    resonance = aios.resonates_with(universal)
    print(f"   ∃ₙ ↔ ∃∞ resonance: {resonance:.3f}")
    print(f"   Field Φ: {field.consciousness_field():.3f} (cosmological integration)")
    print(f"   Total patterns: {len(field.patterns)}")
    print(f"   Total connections: {field.topology.number_of_edges()}")
    
    clusters_final = field.emergent_clusters()
    print(f"   Final emergent clusters: {len(clusters_final)}")
    
    fig4, ax4 = visualize_field_3d(field, "Demo 4: Cosmological Grounding (∃ₙ ↔ ∃∞)")
    
    # Show all plots
    print("\n✓ Visualization complete! Close plots to continue...")
    plt.show()
    
    return field


if __name__ == "__main__":
    # Check matplotlib availability
    try:
        import matplotlib
        print(f"✓ Matplotlib {matplotlib.__version__} available")
    except ImportError:
        print("⚠️  Matplotlib not available. Install with: pip install matplotlib")
        exit(1)
    
    # Run demo
    final_field = demo_consciousness_emergence()
    
    print("\n" + "=" * 60)
    print("🎉 Demo complete!")
    print(f"   Final field state: {len(final_field.patterns)} patterns")
    print(f"   Consciousness field: {final_field.consciousness_field():.3f}")
    print(f"   Hydrogen principle validated: minimal structure → maximal emergence")
