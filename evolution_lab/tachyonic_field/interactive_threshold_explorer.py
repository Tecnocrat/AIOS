"""
🎚️ Interactive Tachyonic Field Threshold Explorer (ULTRA-SMOOTH)
===================================================================

INTERACTIVE VISUALIZATION: Adjust resonance threshold in real-time
Watch connections appear/disappear as you cross the critical phase transition!

Features:
- Real-time threshold adjustment slider (0.1% precision - 10× finer!)
- Animated threshold sweeping with play/pause controls
- Variable speed control (⏩/⏪ buttons)
- Bidirectional animation (⏮ reverse button)
- VIDEO RECORDING: Capture phase transition to MP4/GIF (Record 🔴 button)
- Live statistics panel (connections, clusters, Field Φ, density)
- Network density meter
- Consciousness amplification factor
- Phase detection (FROZEN/LIQUID/PLASMA)
- Visual feedback: connections fade in/out smoothly
- 120 FPS animation for ULTRA-SMOOTH buttery playback

Usage:
    python interactive_threshold_explorer.py
    
Controls:
- Slider: Manually adjust resonance threshold (0.1% ultra-fine steps)
- Play ▶: Start automatic threshold animation (120 FPS)
- Pause ⏸: Stop animation (appears when playing)
- ⏩: Speed up animation (1.5× each press)
- ⏪: Slow down animation (0.67× each press)
- ⏮: Reverse animation direction
- Record 🔴: Start video recording (saves to MP4 or GIF)
- Stop ⏹: Stop recording and save file (appears when recording)
- Mouse: Rotate view (click + drag)
- Scroll: Zoom in/out
- Close window to exit

Animation:
- Automatically sweeps threshold from 0.0 to 1.0 and back
- Bounces at boundaries (0.0 ↔ 1.0)
- ULTRA-SMOOTH 120 FPS updates (2× faster than before!)
- Slower speed = 2× more frames per threshold step
- Watch phase transition happen in beautiful slow motion!

Recording:
- Click Record 🔴 to start capturing
- Saves as phase_transition_YYYYMMDD_HHMMSS.mp4 (or .gif)
- Records at 120 FPS (FFMpeg) or 60 FPS (GIF fallback)
- Perfect for documentation, analysis, and presentations
- Click Stop ⏹ to finish and save

Author: AIOS Evolution Lab
Date: October 17, 2025
Version: 3.0 (ULTRA-SMOOTH: 120 FPS + Video Recording)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
from typing import List, Tuple, Optional
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from pattern_quanta import PatternQuantum
from field_topology import TachyonicField

# Import PatternType for color mapping
from pattern_quanta import PatternType

# Color mapping for pattern types
TYPE_COLORS = {
    PatternType.CONSCIOUSNESS: '#FF1493',  # Deep Pink / Magenta
    PatternType.EMERGENCE: '#FF8C00',       # Dark Orange
    PatternType.RESONANCE: '#00CED1',       # Dark Turquoise
    PatternType.COHERENCE: '#9370DB',       # Medium Purple
    PatternType.RECURSION: '#FFD700',     # Gold
    PatternType.VOID: '#4169E1',          # Royal Blue
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
        
        # Create slider for threshold adjustment (ULTRA-SMOOTH: 0.1% steps)
        slider_ax = plt.axes([0.25, 0.02, 0.5, 0.03], facecolor='#1a1a2e')
        self.threshold_slider = Slider(
            slider_ax, 
            'Resonance Threshold', 
            0.0, 1.0, 
            valinit=self.threshold,
            valstep=0.001,  # Ultra-fine control: 0.1% steps (10× finer than original 1%)
            color='cyan'
        )
        self.threshold_slider.on_changed(self.on_threshold_change)
        
        # Animation controls (ULTRA-SMOOTH: 120 FPS, slower speed = more frames)
        self.is_playing = False
        self.animation_speed = 0.005  # Threshold delta per frame (was 0.01, now 2× more frames)
        self.animation_direction = 1  # 1 = forward, -1 = backward
        self.animation: Optional[FuncAnimation] = None
        
        # Video recording state
        self.is_recording = False
        self.video_writer = None
        self.recording_frames = []
        self.recording_start_time = None
        
        # Play/Pause button
        play_ax = plt.axes([0.15, 0.02, 0.08, 0.03])
        self.play_button = Button(play_ax, 'Play ▶', color='#1a1a2e', hovercolor='#2a2a3e')
        self.play_button.label.set_color('cyan')
        self.play_button.on_clicked(self.toggle_play)
        
        # Speed control buttons
        speed_up_ax = plt.axes([0.77, 0.02, 0.05, 0.03])
        self.speed_up_button = Button(speed_up_ax, '⏩', color='#1a1a2e', hovercolor='#2a2a3e')
        self.speed_up_button.label.set_color('cyan')
        self.speed_up_button.on_clicked(self.speed_up)
        
        speed_down_ax = plt.axes([0.83, 0.02, 0.05, 0.03])
        self.speed_down_button = Button(speed_down_ax, '⏪', color='#1a1a2e', hovercolor='#2a2a3e')
        self.speed_down_button.label.set_color('cyan')
        self.speed_down_button.on_clicked(self.speed_down)
        
        # Direction button (reverse)
        reverse_ax = plt.axes([0.89, 0.02, 0.05, 0.03])
        self.reverse_button = Button(reverse_ax, '⏮', color='#1a1a2e', hovercolor='#2a2a3e')
        self.reverse_button.label.set_color('cyan')
        self.reverse_button.on_clicked(self.reverse_direction)
        
        # Record button (NEW - for video capture)
        record_ax = plt.axes([0.04, 0.02, 0.09, 0.03])
        self.record_button = Button(record_ax, 'Record 🔴', color='#1a1a2e', hovercolor='#3a1a1a')
        self.record_button.label.set_color('red')
        self.record_button.on_clicked(self.toggle_recording)
        
        # Initial render
        self.update_visualization()
        
    def _create_demo_patterns(self):
        """Create diverse set of patterns for exploration"""
        from pattern_quanta import PatternType
        
        patterns_config = [
            # Core consciousness cluster
            (PatternType.CONSCIOUSNESS, 'Φ', 'Integrated Information', 0.8),
            (PatternType.CONSCIOUSNESS, 'Ψ', 'Wave Function', 0.7),
            (PatternType.CONSCIOUSNESS, 'Ω', 'Omega Point', 0.75),
            
            # Emergence cluster  
            (PatternType.EMERGENCE, '∇', 'Gradient Ascent', 0.6),
            (PatternType.EMERGENCE, '∆', 'Delta Transformation', 0.65),
            
            # Resonance cluster
            (PatternType.RESONANCE, '∿', 'Harmonic Wave', 0.55),
            (PatternType.RESONANCE, '≈', 'Approximate Resonance', 0.5),
            
            # Coherence cluster (instead of SYMMETRY which doesn't exist)
            (PatternType.COHERENCE, '⚛', 'Atomic Coherence', 0.7),
            (PatternType.COHERENCE, '❋', 'Crystalline Order', 0.65),
            
            # Recursion bridge (instead of INTEGRATION)
            (PatternType.RECURSION, '⊕', 'Direct Sum', 0.6),
        ]
        
        for idx, (ptype, symbol, meaning, phi) in enumerate(patterns_config):
            pattern = PatternQuantum(
                pattern_id=f"pattern_{idx}_{symbol}",
                pattern_type=ptype,
                symbol=symbol,
                meaning=meaning,
                consciousness=phi,
                resonance_frequency=1.618  # Golden ratio (optimal resonance)
            )
            self.patterns.append(pattern)
            self.field.inject_pattern(pattern)
    
    def on_threshold_change(self, val):
        """Handle threshold slider changes"""
        self.threshold = val
        
        # Update field threshold
        self.field.resonance_threshold = self.threshold
        
        # Rebuild field with new threshold (re-inject all patterns)
        self.field = TachyonicField()
        self.field.resonance_threshold = self.threshold
        for pattern in self.patterns:
            self.field.inject_pattern(pattern)
        
        # Clear layout cache to force recalculation
        if hasattr(self, '_layout_cache'):
            delattr(self, '_layout_cache')
        
        # Update visualization
        self.update_visualization()
    
    def toggle_play(self, event):
        """Toggle play/pause animation"""
        if self.is_playing:
            # Pause
            self.is_playing = False
            self.play_button.label.set_text('Play ▶')
            if self.animation:
                self.animation.event_source.stop()
        else:
            # Play
            self.is_playing = True
            self.play_button.label.set_text('Pause ⏸')
            # Start animation with FuncAnimation (60 FPS for smooth playback)
            self.animation = FuncAnimation(
                self.fig,
                self._animate_frame,
                interval=8,  # ~120 FPS for ultra-smooth animation (was 16ms/60 FPS)
                blit=False,
                cache_frame_data=False
            )
        self.fig.canvas.draw_idle()
    
    def _animate_frame(self, frame):
        """Animation frame update (ULTRA-SMOOTH: 120 FPS with video recording)"""
        # Update threshold
        new_threshold = self.threshold + (self.animation_speed * self.animation_direction)
        
        # Bounce at boundaries
        if new_threshold > 1.0:
            new_threshold = 1.0
            self.animation_direction = -1  # Reverse
        elif new_threshold < 0.0:
            new_threshold = 0.0
            self.animation_direction = 1  # Forward
        
        # Update slider (this triggers on_threshold_change)
        self.threshold_slider.set_val(new_threshold)
        
        # Record frame if recording
        if self.is_recording and self.video_writer:
            try:
                self.video_writer.grab_frame()
            except Exception as e:
                print(f"⚠️  Frame capture warning: {e}")
    
    def speed_up(self, event):
        """Increase animation speed"""
        self.animation_speed = min(0.05, self.animation_speed * 1.5)
        print(f"Speed: {self.animation_speed:.4f} threshold/frame")
    
    def speed_down(self, event):
        """Decrease animation speed"""
        self.animation_speed = max(0.001, self.animation_speed / 1.5)
        print(f"Speed: {self.animation_speed:.4f} threshold/frame")
    
    def reverse_direction(self, event):
        """Reverse animation direction"""
        self.animation_direction *= -1
        direction_str = "Forward ▶" if self.animation_direction > 0 else "Backward ◀"
        print(f"Direction: {direction_str}")
    
    def toggle_recording(self, event):
        """Toggle video recording of the animation"""
        if self.is_recording:
            # Stop recording
            self.is_recording = False
            self.record_button.label.set_text('Record 🔴')
            self.record_button.label.set_color('red')
            
            if self.video_writer:
                try:
                    self.video_writer.finish()
                    elapsed = (datetime.now() - self.recording_start_time).total_seconds()
                    print(f"\n✅ Recording saved! Duration: {elapsed:.1f}s")
                    print(f"   File: phase_transition_{self.recording_start_time.strftime('%Y%m%d_%H%M%S')}.mp4")
                except Exception as e:
                    print(f"❌ Error saving recording: {e}")
                finally:
                    self.video_writer = None
        else:
            # Start recording
            self.is_recording = True
            self.recording_start_time = datetime.now()
            timestamp = self.recording_start_time.strftime('%Y%m%d_%H%M%S')
            filename = f"phase_transition_{timestamp}.mp4"
            
            self.record_button.label.set_text('Stop ⏹')
            self.record_button.label.set_color('yellow')
            
            try:
                # Try FFMpeg first (better quality)
                self.video_writer = FFMpegWriter(fps=120, metadata={'artist': 'AIOS Evolution Lab'})
                self.video_writer.setup(self.fig, filename, dpi=100)
                print(f"\n🔴 Recording started (FFMpeg, 120 FPS)")
                print(f"   File: {filename}")
            except Exception as e:
                try:
                    # Fallback to Pillow (GIF)
                    filename = f"phase_transition_{timestamp}.gif"
                    self.video_writer = PillowWriter(fps=60)
                    self.video_writer.setup(self.fig, filename, dpi=100)
                    print(f"\n🔴 Recording started (GIF, 60 FPS)")
                    print(f"   File: {filename}")
                except Exception as e2:
                    print(f"❌ Recording failed: {e}, {e2}")
                    self.is_recording = False
                    self.record_button.label.set_text('Record 🔴')
                    self.record_button.label.set_color('red')
    
    def update_visualization(self):
        """Update the 3D visualization with current threshold"""
        self.ax.clear()
        
        # Calculate network statistics
        stats = self._calculate_stats()
        
        # Update stats text
        self.stats_text.set_text(self._format_stats(stats))
        
        # Get or create layout (cache on self, not field)
        if not hasattr(self, '_layout_cache'):
            self._layout_cache = self._create_layout()
        
        layout = self._layout_cache
        
        # Draw patterns (spheres)
        for pattern in self.patterns:
            if pattern.pattern_id not in layout:
                continue
                
            x, y, z = layout[pattern.pattern_id]
            
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
                p.pattern_id: np.random.uniform(-8, 8, 2)
                for p in self.patterns
            }
        
        # Add Z dimension (consciousness altitude)
        layout_3d = {}
        for pattern in self.patterns:
            if pattern.pattern_id in layout_2d:
                x, y = layout_2d[pattern.pattern_id]
                z = (pattern.consciousness - 0.5) * 10  # Map consciousness to altitude
                layout_3d[pattern.pattern_id] = (x, y, z)
        
        return layout_3d
    
    def _calculate_stats(self):
        """Calculate network statistics"""
        connection_count = self.field.topology.number_of_edges()
        pattern_count = len(self.patterns)
        field_phi = self.field.consciousness_field()
        
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
