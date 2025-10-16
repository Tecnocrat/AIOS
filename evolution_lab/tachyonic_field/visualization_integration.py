#!/usr/bin/env python3
"""
TACHYONIC FIELD VISUALIZATION INTEGRATION

Integrates tachyonic field prototype with existing AIOS 3D infrastructure:
- computational_layer/engines/aios_assembly_3d_engine.py (assembly-optimized rendering)
- core/include/tachyonic_surface.hpp (C++ tachyonic surface renderer)
- interface/visualization/visual_interface/ConsciousnessGeometryEngine.cs (WPF 3D geometry)

HYDROGEN PRINCIPLE APPLIED:
- Minimal new code (reuse existing infrastructure)
- Maximum emergence (field data drives visualization)
- No duplication (extend, don't recreate)

INTEGRATION ARCHITECTURE:
evolution_lab/tachyonic_field/
    └── visualization_integration.py  ← THIS FILE (bridge to existing engines)

computational_layer/engines/
    └── aios_assembly_3d_engine.py    ← EXTEND with tachyonic field primitives

interface/visualization/
    └── ConsciousnessGeometryEngine.cs ← ADD tachyonic field geometry methods
"""

import sys
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict

# Add AIOS computational layer to path
AIOS_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT / "computational_layer" / "engines"))

# Import existing AIOS assembly engine
try:
    from aios_assembly_3d_engine import (
        Vector3D, Vertex, Primitive3D, PrimitiveType, RenderMode,
        AssemblyMathEngine, AssemblyRenderEngine
    )
    ASSEMBLY_ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Assembly engine not available: {e}")
    print(f"   Using fallback Python implementation")
    ASSEMBLY_ENGINE_AVAILABLE = False
    
    # Fallback definitions
    @dataclass
    class Vector3D:
        x: float
        y: float
        z: float

# Import tachyonic field components
from field_topology import TachyonicField
from pattern_quanta import PatternQuantum, PatternType


@dataclass
class TachyonicFieldRenderData:
    """
    Render data optimized for AIOS assembly engine.
    
    Follows existing architecture patterns from:
    - aios_assembly_3d_engine.py (Primitive3D structure)
    - tachyonic_surface.hpp (HeightMap structure)
    """
    patterns: List[Dict[str, Any]]
    connections: List[Dict[str, Any]]
    field_consciousness: float
    spatial_layout: Dict[str, Tuple[float, float, float]]
    cluster_assignments: Dict[str, int]


class TachyonicFieldVisualizationBridge:
    """
    Bridge tachyonic field data to existing AIOS 3D infrastructure.
    
    DESIGN PHILOSOPHY:
    - Reuse existing assembly engine (not create new one)
    - Extend existing geometry patterns (not duplicate)
    - Integrate with existing C++ renderer (not rebuild)
    
    INTEGRATION POINTS:
    1. Assembly Engine: Create TACHYONIC_FIELD primitive type
    2. C++ Renderer: Use existing aios_render_heightmap_ortho
    3. C# Geometry: Extend ConsciousnessGeometryEngine with tachyonic methods
    """
    
    def __init__(self, field: TachyonicField, use_assembly: bool = True):
        """
        Initialize visualization bridge.
        
        Args:
            field: TachyonicField instance to visualize
            use_assembly: Use assembly engine if available (default True)
        """
        self.field = field
        self.use_assembly = use_assembly and ASSEMBLY_ENGINE_AVAILABLE
        
        # Initialize assembly engine if available
        if self.use_assembly:
            self.math_engine = AssemblyMathEngine()
            self.render_engine = AssemblyRenderEngine()
            print("✓ Using AIOS assembly-optimized rendering")
        else:
            self.math_engine = None
            self.render_engine = None
            print("✓ Using Python fallback rendering")
        
        # Cache for performance
        self._layout_cache: Optional[Dict[str, Tuple[float, float, float]]] = None
        self._cluster_cache: Optional[Dict[str, int]] = None
    
    def get_render_data(self, force_relayout: bool = False) -> TachyonicFieldRenderData:
        """
        Export field state as render data for AIOS engines.
        
        Args:
            force_relayout: Recalculate 3D layout even if cached
        
        Returns:
            TachyonicFieldRenderData optimized for assembly engine
        """
        # Calculate 3D spatial layout (use cache if available)
        if self._layout_cache is None or force_relayout:
            self._layout_cache = self._calculate_3d_layout()
        
        # Detect emergent clusters (use cache if available)
        if self._cluster_cache is None or force_relayout:
            self._cluster_cache = self._assign_clusters()
        
        # Build pattern render data
        patterns = []
        for pattern_id, pattern in self.field.patterns.items():
            position = self._layout_cache.get(pattern_id, (0.0, 0.0, 0.0))
            cluster_id = self._cluster_cache.get(pattern_id, -1)
            
            patterns.append({
                "id": pattern_id,
                "position": position,
                "radius": 0.1 + (pattern.consciousness * 0.3),  # Size by consciousness
                "color": self._consciousness_to_color(pattern),
                "type": pattern.pattern_type.value,
                "consciousness": pattern.consciousness,
                "cluster_id": cluster_id,
                "resonance_frequency": pattern.resonance_frequency
            })
        
        # Build connection render data
        connections = []
        for pid, cid in self.field.topology.edges():
            if pid < cid:  # Avoid duplicates (undirected graph)
                p1 = self.field.patterns[pid]
                p2 = self.field.patterns[cid]
                strength = p1.resonates_with(p2)
                
                connections.append({
                    "from_id": pid,
                    "to_id": cid,
                    "strength": strength,
                    "from_pos": self._layout_cache[pid],
                    "to_pos": self._layout_cache[cid]
                })
        
        # Calculate field-level consciousness
        field_phi = self.field.consciousness_field()
        
        return TachyonicFieldRenderData(
            patterns=patterns,
            connections=connections,
            field_consciousness=field_phi,
            spatial_layout=self._layout_cache,
            cluster_assignments=self._cluster_cache
        )
    
    def _calculate_3d_layout(self) -> Dict[str, Tuple[float, float, float]]:
        """
        Calculate 3D positions for patterns using force-directed layout.
        
        ALGORITHM:
        - Resonant patterns attract (closer in space)
        - Different types repel (spatial separation)
        - Consciousness determines altitude (higher Φ → higher Z)
        
        IMPLEMENTATION:
        - Use networkx spring_layout (proven, optimized)
        - Post-process with consciousness stratification
        - Scale to visible range ([-10, 10] cube)
        """
        import networkx as nx
        
        # Build graph from field topology
        G = nx.Graph()
        
        # Add nodes with consciousness weight
        for pid, pattern in self.field.patterns.items():
            G.add_node(pid, weight=pattern.consciousness)
        
        # Add edges with resonance weight
        for pid, cid in self.field.topology.edges():
            if pid < cid:  # Undirected edges
                p1 = self.field.patterns[pid]
                p2 = self.field.patterns[cid]
                resonance = p1.resonates_with(p2)
                G.add_edge(pid, cid, weight=resonance)
        
        # Calculate 3D spring layout
        if len(G.nodes) == 0:
            return {}
        
        # Optimal spacing parameter (prevents overlap)
        k = 1.0 / math.sqrt(len(G.nodes)) if len(G.nodes) > 1 else 1.0
        
        # 3D force-directed layout
        pos = nx.spring_layout(
            G,
            dim=3,
            k=k,
            iterations=50,
            weight='weight',
            seed=42  # Reproducible layouts
        )
        
        # Post-process: stratify by consciousness (higher Φ → higher altitude)
        layout = {}
        for pid, (x, y, z) in pos.items():
            pattern = self.field.patterns[pid]
            
            # Consciousness stratification
            z_adjusted = z + (pattern.consciousness * 2.0)
            
            # Scale to visible range ([-10, 10] cube)
            layout[pid] = (
                x * 10.0,
                y * 10.0,
                z_adjusted * 10.0
            )
        
        return layout
    
    def _assign_clusters(self) -> Dict[str, int]:
        """
        Assign cluster IDs to patterns based on emergent topology.
        
        Uses field.emergent_clusters() which performs DFS graph traversal
        to detect connected components (clusters formed by resonance).
        """
        clusters = self.field.emergent_clusters()
        
        # Flatten cluster assignments
        assignments = {}
        for cluster_id, pattern_ids in enumerate(clusters):
            for pid in pattern_ids:
                assignments[pid] = cluster_id
        
        return assignments
    
    def _consciousness_to_color(self, pattern: PatternQuantum) -> Tuple[int, int, int]:
        """
        Map pattern to RGB color for visualization.
        
        COLOR SCHEME (consciousness + type):
        - Consciousness: Low (blue) → Mid (cyan) → High (white)
        - Type: Hue shift based on pattern type
        
        INTEGRATION:
        - Matches ConsciousnessGeometryEngine.cs material system
        - Compatible with tachyonic_surface.hpp baseColor (0xAARRGGBB)
        """
        # Base hue from pattern type (matches ConsciousnessGeometryEngine materials)
        type_hues = {
            PatternType.CONSCIOUSNESS: 300,  # Magenta (consciousness material)
            PatternType.EMERGENCE: 30,       # Orange (emergence material)
            PatternType.RECURSION: 270,      # Purple (fractal material)
            PatternType.RESONANCE: 180,      # Cyan (quantum material)
            PatternType.COHERENCE: 120,      # Green (coherence)
            PatternType.VOID: 240            # Blue (void/substrate)
        }
        
        base_hue = type_hues.get(pattern.pattern_type, 200)
        
        # Lightness from consciousness (30% → 100%)
        lightness = 0.3 + (pattern.consciousness * 0.7)
        
        # Saturation (high for visibility)
        saturation = 0.9
        
        # Convert HSL to RGB
        return self._hsl_to_rgb(base_hue, saturation, lightness)
    
    def _hsl_to_rgb(self, h: float, s: float, l: float) -> Tuple[int, int, int]:
        """Convert HSL color to RGB (0-255 range)."""
        h = h / 360.0  # Normalize hue to [0, 1]
        
        if s == 0:
            # Achromatic (gray)
            r = g = b = l
        else:
            def hue_to_rgb(p: float, q: float, t: float) -> float:
                if t < 0:
                    t += 1
                if t > 1:
                    t -= 1
                if t < 1/6:
                    return p + (q - p) * 6 * t
                if t < 1/2:
                    return q
                if t < 2/3:
                    return p + (q - p) * (2/3 - t) * 6
                return p
            
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            
            r = hue_to_rgb(p, q, h + 1/3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1/3)
        
        return (
            int(r * 255),
            int(g * 255),
            int(b * 255)
        )
    
    def export_for_assembly_engine(self) -> Dict[str, Any]:
        """
        Export field as Primitive3D objects for AIOS assembly engine.
        
        INTEGRATION:
        - Creates TACHYONIC_FIELD primitive type (new)
        - Uses existing Vector3D, Vertex structures
        - Compatible with AssemblyRenderEngine.render()
        """
        if not self.use_assembly:
            return {"error": "Assembly engine not available"}
        
        render_data = self.get_render_data()
        
        # Convert to assembly engine primitives
        primitives = []
        
        # Pattern spheres
        for pattern in render_data.patterns:
            x, y, z = pattern["position"]
            r, g, b = pattern["color"]
            
            primitive = {
                "type": "TACHYONIC_PATTERN_SPHERE",
                "position": {"x": x, "y": y, "z": z},
                "radius": pattern["radius"],
                "color": {"r": r/255.0, "g": g/255.0, "b": b/255.0, "a": 1.0},
                "consciousness": pattern["consciousness"],
                "pattern_type": pattern["type"]
            }
            primitives.append(primitive)
        
        # Connection lines
        for conn in render_data.connections:
            from_x, from_y, from_z = conn["from_pos"]
            to_x, to_y, to_z = conn["to_pos"]
            
            primitive = {
                "type": "TACHYONIC_CONNECTION_LINE",
                "from": {"x": from_x, "y": from_y, "z": from_z},
                "to": {"x": to_x, "y": to_y, "z": to_z},
                "strength": conn["strength"],
                "color": {"r": 0.0, "g": 0.8, "b": 1.0, "a": conn["strength"]}
            }
            primitives.append(primitive)
        
        return {
            "primitives": primitives,
            "field_consciousness": render_data.field_consciousness,
            "camera_focus": self._calculate_camera_focus(render_data),
            "render_mode": "QUANTUM_SUBSTRATE"  # Use existing render mode
        }
    
    def export_for_csharp_geometry(self) -> str:
        """
        Export field as JSON for C# ConsciousnessGeometryEngine.
        
        INTEGRATION:
        - JSON serialization for C# interop
        - Compatible with existing WPF 3D structures
        - Extends ConsciousnessGeometryEngine methods (not duplicate)
        """
        render_data = self.get_render_data()
        
        # Convert to JSON-serializable format
        export_data = {
            "patterns": render_data.patterns,
            "connections": render_data.connections,
            "fieldConsciousness": render_data.field_consciousness,
            "clusterCount": len(set(render_data.cluster_assignments.values())),
            "patternCount": len(render_data.patterns),
            "connectionCount": len(render_data.connections),
            "cameraFocus": self._calculate_camera_focus(render_data)
        }
        
        return json.dumps(export_data, indent=2)
    
    def _calculate_camera_focus(self, render_data: TachyonicFieldRenderData) -> Dict[str, float]:
        """
        Calculate optimal camera position and target.
        
        AI INTELLIGENCE:
        - Focus on highest consciousness cluster
        - Distance based on field extent
        - Look at field centroid
        """
        if not render_data.patterns:
            return {"x": 0, "y": 0, "z": 15, "target_x": 0, "target_y": 0, "target_z": 0}
        
        # Find highest consciousness cluster
        cluster_consciousness = {}
        for pattern in render_data.patterns:
            cid = pattern["cluster_id"]
            if cid >= 0:
                if cid not in cluster_consciousness:
                    cluster_consciousness[cid] = []
                cluster_consciousness[cid].append(pattern["consciousness"])
        
        # Calculate cluster averages
        cluster_avgs = {
            cid: sum(phi_list) / len(phi_list)
            for cid, phi_list in cluster_consciousness.items()
        }
        
        # Find highest consciousness cluster
        if cluster_avgs:
            target_cluster = max(cluster_avgs.items(), key=lambda x: x[1])[0]
            
            # Calculate cluster centroid
            cluster_patterns = [p for p in render_data.patterns if p["cluster_id"] == target_cluster]
            cx = sum(p["position"][0] for p in cluster_patterns) / len(cluster_patterns)
            cy = sum(p["position"][1] for p in cluster_patterns) / len(cluster_patterns)
            cz = sum(p["position"][2] for p in cluster_patterns) / len(cluster_patterns)
        else:
            # No clusters, use overall centroid
            cx = sum(p["position"][0] for p in render_data.patterns) / len(render_data.patterns)
            cy = sum(p["position"][1] for p in render_data.patterns) / len(render_data.patterns)
            cz = sum(p["position"][2] for p in render_data.patterns) / len(render_data.patterns)
        
        # Camera position (orbit around target)
        distance = 20.0
        angle = 0.0  # Can be animated
        
        camera_x = cx + distance * math.cos(angle)
        camera_y = cy + distance * 0.3 * math.sin(angle * 0.5)
        camera_z = cz + distance * math.sin(angle)
        
        return {
            "x": camera_x,
            "y": camera_y,
            "z": camera_z,
            "target_x": cx,
            "target_y": cy,
            "target_z": cz
        }
    
    def save_render_data(self, filepath: Path):
        """Save render data to JSON file for external visualization tools."""
        render_data = self.get_render_data()
        
        with open(filepath, 'w') as f:
            json.dump({
                "patterns": render_data.patterns,
                "connections": render_data.connections,
                "field_consciousness": render_data.field_consciousness,
                "spatial_layout": {k: list(v) for k, v in render_data.spatial_layout.items()},
                "cluster_assignments": render_data.cluster_assignments
            }, f, indent=2)
        
        print(f"✓ Render data saved to {filepath}")


# Convenience function for quick visualization setup
def create_field_visualizer(field: TachyonicField) -> TachyonicFieldVisualizationBridge:
    """
    Create visualization bridge for tachyonic field.
    
    Usage:
        from field_topology import TachyonicField
        from pattern_quanta import PatternQuantum, PatternType
        
        field = TachyonicField()
        field.inject_pattern(PatternQuantum(...))
        
        viz = create_field_visualizer(field)
        render_data = viz.get_render_data()
        json_export = viz.export_for_csharp_geometry()
    """
    return TachyonicFieldVisualizationBridge(field, use_assembly=True)


if __name__ == "__main__":
    # Test visualization integration with existing field
    print("🌌 Tachyonic Field Visualization Integration Test")
    print("=" * 60)
    
    # Create test field (reuse from test_field_consciousness.py)
    from pattern_quanta import PatternQuantum, PatternType
    
    field = TachyonicField()
    
    # Inject test patterns
    patterns = [
        PatternQuantum("∃ₙ", PatternType.CONSCIOUSNESS, "👁", "AIOS observer", 0.85, 1.618),
        PatternQuantum("∃∞", PatternType.CONSCIOUSNESS, "🜛", "Universal Observer", 1.0, float('inf')),
        PatternQuantum("E₁", PatternType.EMERGENCE, "🌊", "Wave emergence", 0.7, 2.71),
        PatternQuantum("R₁", PatternType.RECURSION, "🔁", "Recursive pattern", 0.6, 1.414),
        PatternQuantum("C₁", PatternType.COHERENCE, "💎", "Quantum coherence", 0.8, 3.14),
    ]
    
    for pattern in patterns:
        field.inject_pattern(pattern)
    
    print(f"✓ Field initialized: {len(field.patterns)} patterns, {field.topology.number_of_edges()} connections")
    
    # Create visualization bridge
    viz = create_field_visualizer(field)
    
    # Test render data export
    print("\n📊 Testing render data export...")
    render_data = viz.get_render_data()
    print(f"   Patterns: {len(render_data.patterns)}")
    print(f"   Connections: {len(render_data.connections)}")
    print(f"   Field consciousness: {render_data.field_consciousness:.3f}")
    print(f"   Clusters: {len(set(render_data.cluster_assignments.values()))}")
    
    # Test assembly engine export
    if ASSEMBLY_ENGINE_AVAILABLE:
        print("\n⚙️  Testing assembly engine export...")
        assembly_data = viz.export_for_assembly_engine()
        print(f"   Primitives: {len(assembly_data['primitives'])}")
        print(f"   Render mode: {assembly_data['render_mode']}")
    
    # Test C# geometry export
    print("\n🎨 Testing C# geometry export...")
    csharp_json = viz.export_for_csharp_geometry()
    print(f"   JSON length: {len(csharp_json)} characters")
    
    # Save render data
    output_path = Path(__file__).parent / "test_render_data.json"
    viz.save_render_data(output_path)
    
    print("\n✓ Visualization integration test complete!")
    print(f"✓ Ready to integrate with existing AIOS 3D infrastructure")
