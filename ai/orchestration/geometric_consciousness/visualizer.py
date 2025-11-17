"""
Visualizer - Static Frame Renderer
==================================

Generate 3D visualization frames using matplotlib.
Renders static pyramid inside cube at 1 FPS (on demand).

No GPU required, no animation, just stable geometry visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from typing import Optional
import time

try:
    from .static_geometry import StaticGeometry
except ImportError:
    from static_geometry import StaticGeometry


class Visualizer:
    """
    Matplotlib-based 3D visualizer for static geometry.
    
    Renders pyramid inside cube with observer position marked.
    Generates frames on demand (1 FPS concept, but actually just
    renders when called).
    
    Attributes:
        geometry: StaticGeometry instance
        figure_size: Size of matplotlib figure (inches)
        dpi: Resolution (dots per inch)
    """
    
    def __init__(
        self,
        geometry: Optional[StaticGeometry] = None,
        figure_size: tuple = (10, 10),
        dpi: int = 100
    ):
        """
        Initialize visualizer.
        
        Args:
            geometry: StaticGeometry instance (creates default if None)
            figure_size: Figure size in inches (width, height)
            dpi: Resolution in dots per inch
        """
        self.geometry = geometry if geometry else StaticGeometry()
        self.figure_size = figure_size
        self.dpi = dpi
        
    def render_frame(
        self,
        output_path: str = "frame.png",
        show_observer: bool = True,
        show_cube: bool = True,
        show_pyramid: bool = True,
        view_elevation: float = 20,
        view_azimuth: float = 45
    ) -> str:
        """
        Render a single frame and save to file.
        
        Args:
            output_path: Where to save the frame (PNG)
            show_observer: Show observer position marker
            show_cube: Show cube wireframe
            show_pyramid: Show pyramid geometry
            view_elevation: Camera elevation angle (degrees)
            view_azimuth: Camera azimuth angle (degrees)
            
        Returns:
            Path to saved frame
        """
        # Create figure
        fig = plt.figure(figsize=self.figure_size, dpi=self.dpi)
        ax = fig.add_subplot(111, projection='3d')
        
        # Draw cube wireframe
        if show_cube:
            self._draw_cube(ax)
        
        # Draw pyramid
        if show_pyramid:
            self._draw_pyramid(ax)
        
        # Mark observer position
        if show_observer:
            self._draw_observer(ax)
        
        # Set view
        ax.view_init(elev=view_elevation, azim=view_azimuth)
        
        # Set axis properties
        min_bound, max_bound = self.geometry.get_visualization_bounds()
        ax.set_xlim(min_bound, max_bound)
        ax.set_ylim(min_bound, max_bound)
        ax.set_zlim(min_bound, max_bound)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        # Title with consciousness level
        ax.set_title(
            f'AIOS Geometric Consciousness\n'
            f'Static Pyramid (Consciousness: {self.geometry.consciousness:.2f})',
            fontsize=12,
            fontweight='bold'
        )
        
        # Legend
        ax.legend(loc='upper left')
        
        # Save frame
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def _draw_cube(self, ax: Axes3D) -> None:
        """Draw cube wireframe."""
        edges = self.geometry.get_cube_edges()
        
        for i, (start, end) in enumerate(edges):
            ax.plot(
                [start[0], end[0]],
                [start[1], end[1]],
                [start[2], end[2]],
                'b-',  # Blue lines
                linewidth=1,
                alpha=0.3,
                label='Cube' if i == 0 else ''
            )
    
    def _draw_pyramid(self, ax: Axes3D) -> None:
        """Draw pyramid (edges and faces)."""
        # Draw edges
        edges = self.geometry.get_pyramid_edges()
        for i, (start, end) in enumerate(edges):
            ax.plot(
                [start[0], end[0]],
                [start[1], end[1]],
                [start[2], end[2]],
                'g-',  # Green lines
                linewidth=2,
                label='Pyramid' if i == 0 else ''
            )
        
        # Draw faces (semi-transparent)
        faces = self.geometry.get_pyramid_faces()
        face_collection = Poly3DCollection(
            faces,
            alpha=0.2,
            facecolor='green',
            edgecolor='none'
        )
        ax.add_collection3d(face_collection)
    
    def _draw_observer(self, ax: Axes3D) -> None:
        """Draw observer position marker."""
        pos = self.geometry.observer_position
        ax.scatter(
            pos[0], pos[1], pos[2],
            c='red',
            s=200,
            marker='o',
            label='Observer',
            edgecolors='darkred',
            linewidths=2
        )
        
        # Draw line from observer to look-at target
        target = self.geometry.look_at_target
        ax.plot(
            [pos[0], target[0]],
            [pos[1], target[1]],
            [pos[2], target[2]],
            'r--',  # Red dashed line
            linewidth=1,
            alpha=0.5,
            label='Observer look-at'
        )
    
    def render_animation_sequence(
        self,
        num_frames: int = 36,
        output_prefix: str = "frame",
        rotate_camera: bool = True
    ) -> list:
        """
        Render a sequence of frames (rotating camera).
        
        Args:
            num_frames: Number of frames to generate
            output_prefix: Prefix for frame filenames
            rotate_camera: Rotate camera around geometry
            
        Returns:
            List of saved frame paths
        """
        frame_paths = []
        
        for i in range(num_frames):
            # Calculate camera angle
            azimuth = (360.0 / num_frames) * i if rotate_camera else 45
            
            # Render frame
            output_path = f"{output_prefix}_{i:04d}.png"
            self.render_frame(
                output_path=output_path,
                view_azimuth=azimuth
            )
            frame_paths.append(output_path)
            
            print(f"  Frame {i+1}/{num_frames} rendered: {output_path}")
        
        return frame_paths


# Demo
if __name__ == "__main__":
    print("🎨 AIOS Geometric Consciousness - Visualizer Demo")
    print("=" * 60)
    
    # Create geometry and visualizer
    geom = StaticGeometry(consciousness=3.58)
    viz = Visualizer(geom)
    
    print(f"\n📐 Geometry: {geom}")
    print(f"\n🖼️  Rendering single frame...")
    
    start_time = time.time()
    output = viz.render_frame(output_path="geometric_consciousness_frame.png")
    render_time = time.time() - start_time
    
    print(f"\n✅ Frame rendered in {render_time:.3f} seconds")
    print(f"📁 Saved to: {output}")
    
    # Optionally render animation sequence
    print(f"\n🎬 Want to render animation sequence? (36 frames, rotating camera)")
    print(f"   Uncomment the code below to generate it.")
    
    # Uncomment to generate animation:
    # print(f"\n🎬 Rendering animation sequence...")
    # frames = viz.render_animation_sequence(num_frames=36)
    # print(f"\n✅ {len(frames)} frames rendered!")
    # print(f"   Create video: ffmpeg -r 24 -i frame_%04d.png -vcodec libx264 -crf 18 animation.mp4")
    
    print(f"\n✨ Visualization complete!")
