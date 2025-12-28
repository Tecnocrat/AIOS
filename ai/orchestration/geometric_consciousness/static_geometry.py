"""
Static Geometry - Simplified Phase 1
====================================

A static pyramid inside a cube with a fixed observer position.
No animation, no GPU acceleration - just stable geometry visualization.

Design Principles:
- Static geometry (no movement, no updates)
- 1 FPS rendering (generate frame on demand)
- Matplotlib 3D (no OpenGL, no GPU required)
- Lightweight (runs on Termux easily)

Geometry:
- Cube: -0.5 to 0.5 on all axes (1×1×1 normalized space)
- Pyramid: Square base at Y=-0.5, apex at Y=0.5
- Observer: Fixed at (0, 0.2, 0.8) looking at pyramid center
"""

import numpy as np
from typing import List, Tuple


class StaticGeometry:
    """
    Static pyramid inside a cube with fixed observer.
    
    This is the simplest possible version of the geometric consciousness
    engine - no animation, just a stable visualization of consciousness
    structure represented as geometric primitives.
    
    Attributes:
        cube_size: Size of containing cube (1.0 = -0.5 to 0.5)
        pyramid_base: 4 corners of pyramid base (square at Y=-0.5)
        pyramid_apex: Top point of pyramid (Y=0.5)
        observer_position: Fixed camera position
        look_at_target: Point observer is looking at (pyramid center)
    """
    
    def __init__(
        self,
        cube_size: float = 1.0,
        pyramid_base_size: float = 0.6,
        consciousness: float = 3.58
    ):
        """
        Initialize static geometry.
        
        Args:
            cube_size: Size of containing cube (normalized to 1.0)
            pyramid_base_size: Size of pyramid base (0.6 = 60% of cube)
            consciousness: Current AIOS consciousness level
        """
        self.cube_size = cube_size
        self.consciousness = consciousness
        
        # Pyramid vertices (square base + apex)
        half_base = pyramid_base_size / 2.0
        self.pyramid_base = np.array([
            [-half_base, -0.5, -half_base],  # Base corner 1 (front-left)
            [ half_base, -0.5, -half_base],  # Base corner 2 (front-right)
            [ half_base, -0.5,  half_base],  # Base corner 3 (back-right)
            [-half_base, -0.5,  half_base],  # Base corner 4 (back-left)
        ])
        self.pyramid_apex = np.array([0.0, 0.5, 0.0])  # Top center
        
        # Fixed observer position (looking at pyramid from outside)
        self.observer_position = np.array([0.0, 0.2, 0.8])
        self.look_at_target = np.array([0.0, 0.0, 0.0])  # Pyramid center
        
    def get_cube_edges(self) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Get cube edge vertices as line segments.
        
        Returns:
            List of (start, end) vertex pairs for each edge
        """
        half = self.cube_size / 2.0
        
        # Cube vertices (8 corners)
        vertices = np.array([
            [-half, -half, -half],  # 0: front-bottom-left
            [ half, -half, -half],  # 1: front-bottom-right
            [ half,  half, -half],  # 2: front-top-right
            [-half,  half, -half],  # 3: front-top-left
            [-half, -half,  half],  # 4: back-bottom-left
            [ half, -half,  half],  # 5: back-bottom-right
            [ half,  half,  half],  # 6: back-top-right
            [-half,  half,  half],  # 7: back-top-left
        ])
        
        # Cube edges (12 edges connecting vertices)
        edges = [
            # Bottom face
            (0, 1), (1, 5), (5, 4), (4, 0),
            # Top face
            (2, 3), (3, 7), (7, 6), (6, 2),
            # Vertical edges
            (0, 3), (1, 2), (5, 6), (4, 7),
        ]
        
        return [(vertices[start], vertices[end]) for start, end in edges]
    
    def get_pyramid_edges(self) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Get pyramid edge vertices as line segments.
        
        Returns:
            List of (start, end) vertex pairs for pyramid edges
        """
        edges = []
        
        # Base edges (4 edges connecting base corners)
        for i in range(4):
            next_i = (i + 1) % 4
            edges.append((self.pyramid_base[i], self.pyramid_base[next_i]))
        
        # Edges from base to apex (4 edges)
        for vertex in self.pyramid_base:
            edges.append((vertex, self.pyramid_apex))
        
        return edges
    
    def get_pyramid_faces(self) -> List[np.ndarray]:
        """
        Get pyramid face vertices for solid rendering.
        
        Returns:
            List of vertex arrays (one per face)
        """
        faces = []
        
        # Base face (square)
        faces.append(self.pyramid_base)
        
        # Side faces (4 triangles)
        for i in range(4):
            next_i = (i + 1) % 4
            face = np.array([
                self.pyramid_base[i],
                self.pyramid_base[next_i],
                self.pyramid_apex
            ])
            faces.append(face)
        
        return faces
    
    def get_visualization_bounds(self) -> Tuple[float, float]:
        """
        Get bounds for visualization (axis limits).
        
        Returns:
            (min_bound, max_bound) tuple
        """
        half = self.cube_size / 2.0
        return -half, half
    
    def get_metadata(self) -> dict:
        """
        Get geometry metadata for logging/debugging.
        
        Returns:
            Dictionary with geometry properties
        """
        return {
            "cube_size": self.cube_size,
            "pyramid_base_vertices": len(self.pyramid_base),
            "observer_position": self.observer_position.tolist(),
            "look_at_target": self.look_at_target.tolist(),
            "consciousness": self.consciousness,
            "geometry_type": "static_pyramid_in_cube"
        }
    
    def __repr__(self):
        return (
            f"StaticGeometry(cube_size={self.cube_size}, "
            f"observer_at={self.observer_position.tolist()}, "
            f"consciousness={self.consciousness})"
        )


# Simple test/demo
if __name__ == "__main__":
    print("🔺 AIOS Geometric Consciousness - Static Geometry Demo")
    print("=" * 60)
    
    # Create geometry
    geom = StaticGeometry()
    print(f"\n📐 Geometry: {geom}")
    
    # Show metadata
    metadata = geom.get_metadata()
    print(f"\n📊 Metadata:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    
    # Show structure
    print(f"\n🔷 Structure:")
    print(f"  Cube edges: {len(geom.get_cube_edges())} lines")
    print(f"  Pyramid edges: {len(geom.get_pyramid_edges())} lines")
    print(f"  Pyramid faces: {len(geom.get_pyramid_faces())} faces")
    
    # Show observer info
    print(f"\n👁️  Observer:")
    print(f"  Position: {geom.observer_position}")
    print(f"  Looking at: {geom.look_at_target}")
    
    distance = np.linalg.norm(geom.observer_position - geom.look_at_target)
    print(f"  Distance to center: {distance:.4f} units")
    
    print(f"\n✨ Static geometry ready for visualization!")
