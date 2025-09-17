"""
AIOS Tachyonic Surface - Python Interface to C++ Core
AINLP Dendritic Paradigm: Temporal Data Layer Integration

This module provides Python bindings and extensions for the C++ tachyonic
surface implementation, enabling temporal topography and subspatial allocation
within the AIOS ecosystem.
"""

import ctypes
import hashlib
import math
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class TachyonicCoordinate(BaseModel):
    """Temporal coordinate in tachyonic space"""
    time_index: int
    distance_normalized: float
    magnitude: float
    temporal_stability: float = 0.0


class TemporalTopography(BaseModel):
    """Temporal topography data structure"""
    coordinates: List[TachyonicCoordinate]
    surface_points: List[Dict[str, float]]
    temporal_resolution: float
    created_at: str


class TachyonicSurface:
    """
    Python interface to C++ tachyonic surface implementation.

    AINLP dendritic paradigm: Tachyonic layer for temporal data processing.
    This class provides Python bindings to the existing C++ tachyonic surface
    while adding additional temporal processing capabilities.
    """

    def __init__(self, lib_path: Optional[str] = None):
        self.lib_path = lib_path or self._find_tachyonic_lib()
        self.tachyonic_lib = None
        self.temporal_topography: Dict[str, TemporalTopography] = {}
        self.subspatial_allocation: Dict[str, Dict[str, Any]] = {}
        self.temporal_resolution: float = 1.0

        # Try to load C++ library
        self._load_cpp_library()

    def build_temporal_topography(
        self,
        magnitudes: List[float],
        time_indices: List[int],
        subsystem_id: str
    ) -> TemporalTopography:
        """
        Build temporal topography from magnitude data.

        Args:
            magnitudes: List of magnitude values over time
            time_indices: Corresponding time indices
            subsystem_id: Identifier for the subsystem

        Returns:
            Temporal topography data structure
        """
        if len(magnitudes) != len(time_indices):
            raise ValueError(
                "Magnitudes and time indices must have same length"
            )

        # Create tachyonic coordinates
        coordinates = []
        surface_points = []

        for i, (mag, time_idx) in enumerate(zip(magnitudes, time_indices)):
            # Normalize magnitude to [-1, 1]
            norm_mag = max(-1.0, min(1.0, mag))

            # Calculate distance normalization (simplified)
            dist_norm = self._calculate_distance_normalization(
                i, len(magnitudes)
            )

            coord = TachyonicCoordinate(
                time_index=time_idx,
                distance_normalized=dist_norm,
                magnitude=norm_mag,
                temporal_stability=self._assess_temporal_stability(mag, i)
            )

            coordinates.append(coord)

            # Create 3D surface point
            surface_point = {
                "x": time_idx / max(time_indices) if time_indices else 0,
                "y": dist_norm,
                "z": norm_mag
            }
            surface_points.append(surface_point)

        topography = TemporalTopography(
            coordinates=coordinates,
            surface_points=surface_points,
            temporal_resolution=self.temporal_resolution,
            created_at=self._get_timestamp()
        )

        self.temporal_topography[subsystem_id] = topography
        return topography

    def register_subspatial_change(
        self, change_data: Dict[str, Any],
        spatial_coords: str,
        temporal_coords: str
    ) -> Dict[str, Any]:
        """
        Register changes in subspatial allocation with temporal coordinates.

        Args:
            change_data: The change data to register
            spatial_coords: Spatial coordinate identifier
            temporal_coords: Temporal coordinate identifier

        Returns:
            Registration confirmation with metadata
        """
        registration = {
            "change_data": change_data,
            "spatial_coords": spatial_coords,
            "temporal_coords": temporal_coords,
            "registration_time": self._get_timestamp(),
            "spatial_impact": self._calculate_spatial_impact(
                change_data
            ),
            "temporal_stability": self._assess_temporal_stability_from_data(
                change_data
            ),
            "subspatial_allocation": self._calculate_subspatial_allocation(
                change_data
            )
        }

        # Store in subspatial allocation
        key = f"{spatial_coords}_{temporal_coords}"
        self.subspatial_allocation[key] = registration

        return registration

    def query_temporal_topography(
        self, subsystem_id: str,
        time_range: Optional[tuple] = None
    ) -> Dict[str, Any]:
        """
        Query temporal topography for a specific subsystem.

        Args:
            subsystem_id: The subsystem to query
            time_range: Optional (start, end) time range

        Returns:
            Topography data within the specified range
        """
        if subsystem_id not in self.temporal_topography:
            return {"error": f"Subsystem {subsystem_id} not found"}

        topography = self.temporal_topography[subsystem_id]

        if time_range:
            start_time, end_time = time_range
            filtered_coords = [
                coord for coord in topography.coordinates
                if start_time <= coord.time_index <= end_time
            ]
            filtered_points = topography.surface_points[:len(filtered_coords)]

            return {
                "subsystem_id": subsystem_id,
                "coordinates": filtered_coords,
                "surface_points": filtered_points,
                "temporal_resolution": topography.temporal_resolution,
                "query_range": time_range,
                "total_points": len(filtered_coords)
            }

        return {
            "subsystem_id": subsystem_id,
            "coordinates": topography.coordinates,
            "surface_points": topography.surface_points,
            "temporal_resolution": topography.temporal_resolution,
            "total_points": len(topography.coordinates)
        }

    def calculate_temporal_correlation(
        self, subsystem_a: str,
        subsystem_b: str
    ) -> Dict[str, Any]:
        """
        Calculate temporal correlation between two subsystems.

        Args:
            subsystem_a: First subsystem identifier
            subsystem_b: Second subsystem identifier

        Returns:
            Correlation analysis data
        """
        if subsystem_a not in self.temporal_topography or \
           subsystem_b not in self.temporal_topography:
            return {"error": "One or both subsystems not found"}

        topo_a = self.temporal_topography[subsystem_a]
        topo_b = self.temporal_topography[subsystem_b]

        # Calculate correlation metrics
        correlation = self._calculate_correlation_coefficient(
            [coord.magnitude for coord in topo_a.coordinates],
            [coord.magnitude for coord in topo_b.coordinates]
        )

        return {
            "subsystem_a": subsystem_a,
            "subsystem_b": subsystem_b,
            "correlation_coefficient": correlation,
            "temporal_overlap": min(
                len(topo_a.coordinates), len(topo_b.coordinates)
            ),
            "analysis_timestamp": self._get_timestamp()
        }

    # Private helper methods

    def _find_tachyonic_lib(self) -> str:
        """Find the tachyonic surface C++ library"""
        # Look for the library in common locations
        possible_paths = [
            Path(__file__).parent.parent / "core" / "build" /
            "tachyonic_surface.dll",
            Path(__file__).parent.parent / "core" / "build" /
            "libtachyonic_surface.so",
            Path(__file__).parent.parent / "core" / "build" /
            "tachyonic_surface.dylib"
        ]

        for path in possible_paths:
            if path.exists():
                return str(path)

        # Return default path if library not found
        return str(
            Path(__file__).parent.parent / "core" / "build" /
            "tachyonic_surface.dll"
        )

    def _load_cpp_library(self):
        """Load the C++ tachyonic surface library"""
        try:
            if Path(self.lib_path).exists():
                self.tachyonic_lib = ctypes.CDLL(self.lib_path)
                print(f" Loaded C++ tachyonic surface library: "
                      f"{self.lib_path}")
            else:
                print(f"  C++ library not found: {self.lib_path}")
                print("   Running with Python-only implementation")
        except Exception as e:
            print(f"  Failed to load C++ library: {e}")
            print("   Running with Python-only implementation")

    def _calculate_distance_normalization(
        self, index: int, total: int
    ) -> float:
        """Calculate distance normalization for temporal coordinates"""
        if total <= 1:
            return 0.5

        # Create a gradient from core (0.0) to periphery (1.0)
        return index / (total - 1)

    def _assess_temporal_stability(
        self, magnitude: float, index: int
    ) -> float:
        """Assess temporal stability of a magnitude at given index"""
        # Simplified stability calculation based on magnitude consistency
        base_stability = 0.5

        # Magnitude closer to zero is more stable
        magnitude_factor = 1.0 - abs(magnitude)

        # Earlier indices (older data) tend to be more stable
        temporal_factor = min(1.0, index / 10)

        return (base_stability + magnitude_factor + temporal_factor) / 3

    def _assess_temporal_stability_from_data(
        self, change_data: Dict[str, Any]
    ) -> float:
        """Assess temporal stability from change data"""
        complexity = len(str(change_data))
        change_count = len(change_data)

        # More complex changes are less stable
        stability = max(0.1, 1.0 - (complexity / 1000) - (change_count / 10))
        return stability

    def _calculate_spatial_impact(
        self, change_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate spatial impact of changes"""
        return {
            "impact_radius": len(str(change_data)) / 100,
            "affected_coordinates": len(change_data),
            "spatial_propagation": self._assess_temporal_stability_from_data(
                change_data
            )
        }

    def _calculate_subspatial_allocation(
        self, change_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate subspatial allocation for changes"""
        return {
            "allocation_priority": len(change_data) / 10,
            "temporal_binding": self._assess_temporal_stability_from_data(
                change_data
            ),
            "spatial_distribution": hashlib.md5(
                str(change_data).encode()
            ).hexdigest()[:8]
        }

    def _calculate_correlation_coefficient(
        self, series_a: List[float],
        series_b: List[float]
    ) -> float:
        """Calculate Pearson correlation coefficient between two series"""
        if len(series_a) != len(series_b) or len(series_a) == 0:
            return 0.0

        n = len(series_a)
        sum_a = sum(series_a)
        sum_b = sum(series_b)
        sum_ab = sum(a * b for a, b in zip(series_a, series_b))
        sum_a_sq = sum(a * a for a in series_a)
        sum_b_sq = sum(b * b for b in series_b)

        numerator = n * sum_ab - sum_a * sum_b
        denominator = math.sqrt(
            (n * sum_a_sq - sum_a * sum_a) * (n * sum_b_sq - sum_b * sum_b)
        )

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()


# Factory function for easy instantiation
def create_tachyonic_surface(
    lib_path: Optional[str] = None
) -> TachyonicSurface:
    """
    Factory function to create a TachyonicSurface instance.

    Args:
        lib_path: Optional path to C++ library

    Returns:
        Configured TachyonicSurface instance
    """
    return TachyonicSurface(lib_path)
