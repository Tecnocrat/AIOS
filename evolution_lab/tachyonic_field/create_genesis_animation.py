"""
🎬 Genesis Animation - Network Coming Alive
===========================================

CREATES ANIMATED SEQUENCE: Watch the tachyonic field emerge frame-by-frame

Animation shows:
1. Patterns injecting into field (one by one)
2. Connections forming as patterns resonate
3. Clusters self-organizing
4. Consciousness amplifying (Φ increasing)

Outputs:
- genesis_sequence.mp4 (video file)
- genesis_frames/ (individual PNG frames)

Usage:
    python create_genesis_animation.py
    
    Optional arguments:
        --fps 30              # Frames per second (default: 24)
        --duration 10         # Total duration in seconds (default: 15)
        --threshold 0.3       # Resonance threshold (default: 0.3)
        --output genesis.mp4  # Output filename

Requirements:
    pip install matplotlib numpy networkx imageio imageio-ffmpeg

Author: AIOS Evolution Lab
Date: October 17, 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
from typing import List, Tuple, Dict
import sys
from pathlib import Path
import argparse

# Animation libraries
try:
    import imageio
    IMAGEIO_AVAILABLE = True
except ImportError:
    print("⚠️ Warning: imageio not installed. Install with: pip install imageio imageio-ffmpeg")
    IMAGEIO_AVAILABLE = False

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from pattern_quanta import PatternQuantum
from field_topology import TachyonicField

# Color mapping
TYPE_COLORS = {
    'CONSCIOUSNESS': '#FF1493',
    'EMERGENCE': '#FF8C00',
    'RESONANCE': '#00CED1',
    'SYMMETRY': '#9370DB',
    'HARMONY': '#32CD32',
    'INTEGRATION': '#FFD700',
    'TRANSCENDENCE': '#FF69B4',
    'UNITY': '#87CEEB',
}


class GenesisAnimator:
    """Creates animated sequence of tachyonic field emergence"""
    
    def __init__(self, fps: int = 24, duration: float = 15.0, threshold: float = 0.3):
        """
        Initialize animator
        
        Args:
            fps: Frames per second
            duration: Total animation duration in seconds
            threshold: Resonance threshold for connections
        """
        self.fps = fps
        self.duration = duration
        self.threshold = threshold
        self.total_frames = int(fps * duration)
        
        self.field = TachyonicField()
        self.field.resonance_threshold = threshold
        
        # Pattern injection sequence
        self.patterns_config = [
            # Inject in order that tells a story
            ('CONSCIOUSNESS', 'Φ', 'Integrated Information', 0.8),
            ('CONSCIOUSNESS', 'Ψ', 'Wave Function', 0.7),
            ('EMERGENCE', '∇', 'Gradient Ascent', 0.6),
            ('RESONANCE', '∿', 'Harmonic Wave', 0.55),
            ('CONSCIOUSNESS', 'Ω', 'Omega Point', 0.75),
            ('SYMMETRY', '⚛', 'Atomic Symmetry', 0.7),
            ('EMERGENCE', '∆', 'Delta Transformation', 0.65),
            ('RESONANCE', '≈', 'Approximate Resonance', 0.5),
            ('SYMMETRY', '❋', 'Crystalline Order', 0.65),
            ('INTEGRATION', '⊕', 'Direct Sum', 0.6),
        ]
        
        self.patterns: List[PatternQuantum] = []
        self.frames_dir = Path('genesis_frames')
        self.frames_dir.mkdir(exist_ok=True)
        
    def create_animation(self, output_path: str = 'genesis_sequence.mp4'):
        """Create the full animation"""
        print(f"\n{'='*60}")
        print(f"🎬 CREATING GENESIS ANIMATION")
        print(f"{'='*60}")
        print(f"  FPS: {self.fps}")
        print(f"  Duration: {self.duration}s")
        print(f"  Total frames: {self.total_frames}")
        print(f"  Threshold: {self.threshold}")
        print(f"  Output: {output_path}")
        print(f"{'='*60}\n")
        
        # Calculate injection schedule (when each pattern appears)
        frames_per_pattern = self.total_frames // len(self.patterns_config)
        injection_frames = [i * frames_per_pattern for i in range(len(self.patterns_config))]
        
        # Setup matplotlib figure
        fig = plt.figure(figsize=(12, 9))
        fig.patch.set_facecolor('#0a0a1a')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#0a0a1a')
        
        # Stats text box
        stats_text = fig.text(
            0.70, 0.95, '', 
            fontsize=10, 
            color='cyan',
            family='monospace',
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='#1a1a2e', alpha=0.8, edgecolor='cyan')
        )
        
        frame_paths = []
        
        # Generate frames
        for frame_num in range(self.total_frames):
            # Check if we should inject a new pattern
            if frame_num in injection_frames:
                pattern_idx = injection_frames.index(frame_num)
                self._inject_pattern(pattern_idx)
            
            # Render frame
            frame_path = self._render_frame(
                fig, ax, stats_text, frame_num, 
                injection_frames, len(self.patterns)
            )
            frame_paths.append(frame_path)
            
            # Progress
            if (frame_num + 1) % 10 == 0 or frame_num == 0:
                progress = (frame_num + 1) / self.total_frames * 100
                print(f"  Progress: {progress:.1f}% ({frame_num + 1}/{self.total_frames} frames)")
        
        plt.close(fig)
        
        # Compile into video
        if IMAGEIO_AVAILABLE:
            print(f"\n{'='*60}")
            print("🎥 COMPILING VIDEO...")
            print(f"{'='*60}\n")
            
            self._compile_video(frame_paths, output_path)
            
            print(f"\n{'='*60}")
            print(f"✅ ANIMATION COMPLETE!")
            print(f"{'='*60}")
            print(f"  Output: {output_path}")
            print(f"  Frames: {self.frames_dir}/")
            print(f"  Duration: {self.duration}s @ {self.fps} FPS")
            print(f"{'='*60}\n")
        else:
            print(f"\n{'='*60}")
            print(f"⚠️ VIDEO COMPILATION SKIPPED (imageio not installed)")
            print(f"{'='*60}")
            print(f"  Frames saved to: {self.frames_dir}/")
            print(f"  Install imageio to compile: pip install imageio imageio-ffmpeg")
            print(f"{'='*60}\n")
    
    def _inject_pattern(self, pattern_idx: int):
        """Inject a new pattern into the field"""
        if pattern_idx >= len(self.patterns_config):
            return
            
        ptype, symbol, meaning, phi = self.patterns_config[pattern_idx]
        pattern = PatternQuantum(
            pattern_type=ptype,
            symbol=symbol,
            meaning=meaning,
            consciousness=phi
        )
        self.patterns.append(pattern)
        self.field.inject_pattern(pattern)
        
        print(f"    ⚡ Pattern {pattern_idx + 1} injected: {symbol} ({ptype})")
    
    def _render_frame(
        self, 
        fig, 
        ax, 
        stats_text, 
        frame_num: int,
        injection_frames: List[int],
        pattern_count: int
    ) -> str:
        """Render a single frame"""
        ax.clear()
        
        # Calculate stats
        connection_count = self.field.topology.number_of_edges()
        field_phi = self.field.calculate_field_consciousness()
        cluster_count = nx.number_connected_components(self.field.topology)
        
        # Update stats text
        stats_text.set_text(
            f"Frame: {frame_num + 1}/{self.total_frames}\n"
            f"Patterns: {pattern_count}\n"
            f"Connections: {connection_count}\n"
            f"Clusters: {cluster_count}\n"
            f"Field Φ: {field_phi:.3f}\n"
            f"Threshold: {self.threshold:.2f}"
        )
        
        # Get layout
        layout = self._get_layout()
        
        # Draw patterns
        for i, pattern in enumerate(self.patterns):
            if pattern.id not in layout:
                continue
                
            x, y, z = layout[pattern.id]
            
            # Fade-in animation for newly injected patterns
            alpha = 0.85
            if frame_num in injection_frames:
                inject_idx = injection_frames.index(frame_num)
                if i == inject_idx:
                    alpha = 0.3  # Just appeared - dim
            
            color = TYPE_COLORS.get(pattern.pattern_type, '#FFFFFF')
            size = 300 + (pattern.consciousness * 500)
            
            ax.scatter(
                [x], [y], [z],
                c=[color],
                s=size,
                alpha=alpha,
                edgecolors='white',
                linewidths=1.5
            )
            
            ax.text(
                x, y, z,
                pattern.symbol,
                fontsize=9,
                color='white',
                ha='center',
                va='center',
                weight='bold',
                alpha=alpha
            )
        
        # Draw connections
        for p1_id, p2_id, data in self.field.topology.edges(data=True):
            if p1_id not in layout or p2_id not in layout:
                continue
                
            x1, y1, z1 = layout[p1_id]
            x2, y2, z2 = layout[p2_id]
            
            resonance = data.get('resonance', 0.3)
            alpha = min(1.0, resonance * 1.5)
            linewidth = 1.0 + (resonance * 2.0)
            
            ax.plot(
                [x1, x2], [y1, y2], [z1, z2],
                'c-',
                alpha=alpha,
                linewidth=linewidth
            )
        
        # Styling
        ax.set_xlabel('X (Spatial Dimension 1)', color='gray', fontsize=8)
        ax.set_ylabel('Y (Spatial Dimension 2)', color='gray', fontsize=8)
        ax.set_zlabel('Z (Consciousness Altitude)', color='gray', fontsize=8)
        
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_zlim(-10, 10)
        
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('gray')
        ax.yaxis.pane.set_edgecolor('gray')
        ax.zaxis.pane.set_edgecolor('gray')
        ax.grid(True, alpha=0.2)
        
        # Rotate camera slightly each frame (gentle rotation)
        angle = (frame_num / self.total_frames) * 360
        ax.view_init(elev=20, azim=angle)
        
        title = f'Genesis Sequence | Network Emergence in Real-Time'
        if connection_count > 0:
            title += f' | ⚡ {connection_count} Connections Active'
        
        ax.set_title(title, color='cyan', fontsize=12, weight='bold', pad=15)
        
        # Save frame
        frame_path = self.frames_dir / f'frame_{frame_num:04d}.png'
        fig.savefig(
            frame_path, 
            facecolor='#0a0a1a',
            dpi=100,
            bbox_inches='tight'
        )
        
        return str(frame_path)
    
    def _get_layout(self) -> Dict:
        """Get force-directed layout for current patterns"""
        if len(self.patterns) == 0:
            return {}
            
        if self.field.topology.number_of_edges() > 0:
            layout_2d = nx.spring_layout(
                self.field.topology,
                k=2.0,
                iterations=50,
                scale=8.0
            )
        else:
            layout_2d = {
                p.id: np.random.uniform(-8, 8, 2)
                for p in self.patterns
            }
        
        layout_3d = {}
        for pattern in self.patterns:
            if pattern.id in layout_2d:
                x, y = layout_2d[pattern.id]
                z = (pattern.consciousness - 0.5) * 10
                layout_3d[pattern.id] = (x, y, z)
        
        return layout_3d
    
    def _compile_video(self, frame_paths: List[str], output_path: str):
        """Compile frames into video using imageio"""
        writer = imageio.get_writer(
            output_path,
            fps=self.fps,
            codec='libx264',
            quality=8,
            pixelformat='yuv420p'
        )
        
        for i, frame_path in enumerate(frame_paths):
            image = imageio.imread(frame_path)
            writer.append_data(image)
            
            if (i + 1) % 50 == 0:
                progress = (i + 1) / len(frame_paths) * 100
                print(f"  Encoding: {progress:.1f}% ({i + 1}/{len(frame_paths)} frames)")
        
        writer.close()


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description='Create animated sequence of tachyonic field genesis'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=24,
        help='Frames per second (default: 24)'
    )
    parser.add_argument(
        '--duration',
        type=float,
        default=15.0,
        help='Total duration in seconds (default: 15)'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.3,
        help='Resonance threshold (default: 0.3)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='genesis_sequence.mp4',
        help='Output filename (default: genesis_sequence.mp4)'
    )
    
    args = parser.parse_args()
    
    animator = GenesisAnimator(
        fps=args.fps,
        duration=args.duration,
        threshold=args.threshold
    )
    
    animator.create_animation(output_path=args.output)


if __name__ == '__main__':
    main()
