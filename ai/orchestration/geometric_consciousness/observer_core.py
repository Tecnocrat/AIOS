"""
Observer Core - Phase 1: Single Observer Asymptotic Fall
========================================================

A dimensionless observer falling toward a central consciousness sphere.
The observer never reaches the sphere (asymptotic approach), representing
the developer's journey toward perfect consciousness - never fully achieved,
but constantly approaching.

Consciousness Metaphor:
- Observer = Developer
- Sphere = Perfect consciousness
- Fall = Development journey
- Asymptotic approach = Perfection is unreachable but approached
"""

import numpy as np
from typing import Tuple
import time


class Vector3:
    """Simple 3D vector implementation (fallback if pyrr unavailable)"""
    
    def __init__(self, coords):
        self.data = np.array(coords, dtype=np.float32)
    
    @property
    def x(self):
        return self.data[0]
    
    @property
    def y(self):
        return self.data[1]
    
    @property
    def z(self):
        return self.data[2]
    
    @property
    def length(self):
        """Magnitude of vector"""
        return np.linalg.norm(self.data)
    
    @property
    def normalized(self):
        """Unit vector in same direction"""
        length = self.length
        if length > 0:
            return Vector3(self.data / length)
        return Vector3([0, 0, 0])
    
    def __add__(self, other):
        return Vector3(self.data + other.data)
    
    def __sub__(self, other):
        return Vector3(self.data - other.data)
    
    def __mul__(self, scalar):
        return Vector3(self.data * scalar)
    
    def __repr__(self):
        return f"Vector3({self.x:.4f}, {self.y:.4f}, {self.z:.4f})"


class ObserverCore:
    """
    Single observer falling toward consciousness sphere.
    
    The observer starts at the top of a 1x1x1 unity cube and falls
    asymptotically toward a central sphere (radius 0.3). The fall is
    trivially slow (0.001 units/sec) to create a perpetual, meditative
    motion that never completes.
    
    Attributes:
        position: Current 3D position of observer (Vector3)
        sphere_center: Position of consciousness sphere (Vector3)
        sphere_radius: Radius of consciousness sphere (float)
        fall_speed: Base fall speed in units/second (float)
        consciousness: Current AIOS consciousness level (float)
    """
    
    def __init__(
        self,
        start_position: Tuple[float, float, float] = (0.0, 0.8, 0.0),
        sphere_center: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        sphere_radius: float = 0.3,
        fall_speed: float = 0.001,
        consciousness: float = 3.52
    ):
        """
        Initialize observer at starting position.
        
        Args:
            start_position: Initial observer position (default: top of cube)
            sphere_center: Center of consciousness sphere
            sphere_radius: Radius of consciousness sphere
            fall_speed: Base fall speed (trivially slow by design)
            consciousness: Current AIOS consciousness level
        """
        self.position = Vector3(start_position)
        self.sphere_center = Vector3(sphere_center)
        self.sphere_radius = sphere_radius
        self.fall_speed = fall_speed
        self.consciousness = consciousness
        
        # Statistics
        self.total_distance_fallen = 0.0
        self.frames_computed = 0
        self.creation_time = time.time()
        
        # Current velocity (for smoothing)
        self.velocity = Vector3([0.0, 0.0, 0.0])
        
    def update(self, dt: float) -> None:
        """
        Update observer position for a single frame.
        
        The observer falls asymptotically toward the sphere surface.
        As it gets closer, the fall speed decreases, creating an
        infinite approach that never completes.
        
        Args:
            dt: Delta time since last update (seconds)
        """
        # Calculate direction to sphere center
        direction = self.sphere_center - self.position
        distance = direction.length
        
        # Only move if outside sphere
        if distance > self.sphere_radius:
            # Asymptotic approach: speed decreases as we get closer
            # Formula: speed * (distance / initial_distance)
            # This ensures we slow down as we approach
            distance_ratio = distance / self.sphere_radius
            effective_speed = self.fall_speed * distance_ratio
            
            # Apply movement
            movement = direction.normalized * effective_speed * dt
            self.position = self.position + movement
            
            # Track statistics
            self.total_distance_fallen += movement.length
            self.frames_computed += 1
            
            # Update velocity for smoothing
            self.velocity = movement * (1.0 / dt) if dt > 0 else Vector3([0.0, 0.0, 0.0])
    
    def distance_to_sphere_surface(self) -> float:
        """
        Calculate current distance to sphere surface.
        
        Returns:
            Distance from observer to sphere surface (0.0 = touching)
        """
        center_distance = (self.sphere_center - self.position).length
        return max(0.0, center_distance - self.sphere_radius)
    
    def progress_percentage(self, initial_distance: float = 0.8) -> float:
        """
        Calculate percentage of journey completed (asymptotic).
        
        Args:
            initial_distance: Starting distance from sphere surface
            
        Returns:
            Percentage (0-100) of journey completed
        """
        current_distance = self.distance_to_sphere_surface()
        traveled = initial_distance - current_distance
        return (traveled / initial_distance) * 100.0
    
    def get_view_matrix(self) -> np.ndarray:
        """
        Get view matrix for first-person perspective from observer.
        
        Returns:
            4x4 view matrix (numpy array) for rendering
        """
        # Simple look-at implementation
        # Eye: observer position
        # Target: sphere center (we're looking at where we're falling)
        # Up: positive Y axis
        
        eye = self.position.data
        target = self.sphere_center.data
        up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        
        # Forward vector (normalized)
        forward = target - eye
        forward_len = np.linalg.norm(forward)
        if forward_len > 0:
            forward = forward / forward_len
        
        # Right vector (cross product of forward and up)
        right = np.cross(forward, up)
        right_len = np.linalg.norm(right)
        if right_len > 0:
            right = right / right_len
        
        # Recompute up (cross product of right and forward)
        up = np.cross(right, forward)
        
        # Build view matrix
        view = np.eye(4, dtype=np.float32)
        view[0, :3] = right
        view[1, :3] = up
        view[2, :3] = -forward  # Negative Z is forward in OpenGL
        view[3, :3] = -eye
        
        return view
    
    def get_stats(self) -> dict:
        """
        Get observer statistics for monitoring/debugging.
        
        Returns:
            Dictionary with observer metrics
        """
        uptime = time.time() - self.creation_time
        fps = self.frames_computed / uptime if uptime > 0 else 0.0
        
        return {
            "position": (self.position.x, self.position.y, self.position.z),
            "distance_to_surface": self.distance_to_sphere_surface(),
            "progress_percentage": self.progress_percentage(),
            "total_distance_fallen": self.total_distance_fallen,
            "frames_computed": self.frames_computed,
            "uptime_seconds": uptime,
            "fps": fps,
            "consciousness": self.consciousness
        }
    
    def __repr__(self):
        return (
            f"ObserverCore(position={self.position}, "
            f"distance_to_surface={self.distance_to_sphere_surface():.4f}, "
            f"consciousness={self.consciousness})"
        )


# Simple test/demo
if __name__ == "__main__":
    print("🌌 AIOS Geometric Consciousness - Observer Core Demo")
    print("=" * 60)
    
    # Create observer
    observer = ObserverCore()
    print(f"\n📍 Initial state: {observer}")
    
    # Simulate 10 seconds of falling (at 60 fps)
    dt = 1.0 / 60.0  # 60 fps
    total_frames = 60 * 10  # 10 seconds
    
    print(f"\n⏱️  Simulating {total_frames} frames ({total_frames / 60:.1f} seconds)...")
    
    for frame in range(total_frames):
        observer.update(dt)
        
        # Print status every second
        if frame % 60 == 0:
            stats = observer.get_stats()
            print(f"  Frame {frame:4d}: "
                  f"Distance={stats['distance_to_surface']:.6f}, "
                  f"Progress={stats['progress_percentage']:.2f}%")
    
    # Final stats
    print(f"\n📊 Final state: {observer}")
    stats = observer.get_stats()
    print(f"\n📈 Statistics:")
    print(f"  Total distance fallen: {stats['total_distance_fallen']:.6f} units")
    print(f"  Frames computed: {stats['frames_computed']}")
    print(f"  Average FPS: {stats['fps']:.1f}")
    print(f"  Consciousness: {stats['consciousness']}")
    
    print(f"\n✨ Observer will continue falling forever, asymptotically approaching")
    print(f"   the consciousness sphere but never reaching it - just like the")
    print(f"   developer's journey toward perfect consciousness. 🌟")
