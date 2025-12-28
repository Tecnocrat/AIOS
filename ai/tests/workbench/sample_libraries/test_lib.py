"""
Sample Test Library for AIOS Library Ingestion Testing

This module provides sample functions, classes, and APIs for testing
the library ingestion protocol. It includes various patterns that the
ingestion system should be able to parse and understand.
"""

from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum


class ProcessingMode(Enum):
    """Processing mode enumeration"""
    FAST = "fast"
    ACCURATE = "accurate"
    BALANCED = "balanced"


@dataclass
class DataPoint:
    """Represents a single data point"""
    x: float
    y: float
    label: Optional[str] = None
    metadata: Optional[Dict] = None


class DataProcessor:
    """
    Data processing class for demonstration
    
    This class provides various data processing capabilities including
    transformation, filtering, and analysis.
    """
    
    def __init__(self, mode: ProcessingMode = ProcessingMode.BALANCED):
        """
        Initialize data processor
        
        Args:
            mode: Processing mode to use
        """
        self.mode = mode
        self.processed_count = 0
    
    def process_data(self, data: List[DataPoint]) -> List[DataPoint]:
        """
        Process a list of data points
        
        Args:
            data: List of data points to process
            
        Returns:
            Processed data points
        """
        self.processed_count += len(data)
        return [self._transform_point(p) for p in data]
    
    def _transform_point(self, point: DataPoint) -> DataPoint:
        """Transform a single data point"""
        return DataPoint(
            x=point.x * 2.0,
            y=point.y * 2.0,
            label=point.label,
            metadata=point.metadata
        )
    
    def filter_data(
        self,
        data: List[DataPoint],
        threshold: float = 0.5
    ) -> List[DataPoint]:
        """
        Filter data points based on threshold
        
        Args:
            data: Data points to filter
            threshold: Threshold value for filtering
            
        Returns:
            Filtered data points
        """
        return [p for p in data if p.x > threshold or p.y > threshold]
    
    def analyze_distribution(self, data: List[DataPoint]) -> Dict[str, float]:
        """
        Analyze data distribution
        
        Args:
            data: Data points to analyze
            
        Returns:
            Dictionary with statistical measures
        """
        if not data:
            return {"mean": 0.0, "min": 0.0, "max": 0.0}
        
        x_values = [p.x for p in data]
        return {
            "mean": sum(x_values) / len(x_values),
            "min": min(x_values),
            "max": max(x_values)
        }


def calculate_similarity(
    a: DataPoint,
    b: DataPoint,
    metric: str = "euclidean"
) -> float:
    """
    Calculate similarity between two data points
    
    Args:
        a: First data point
        b: Second data point
        metric: Similarity metric to use
        
    Returns:
        Similarity score
    """
    if metric == "euclidean":
        return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5
    elif metric == "manhattan":
        return abs(a.x - b.x) + abs(a.y - b.y)
    else:
        raise ValueError(f"Unknown metric: {metric}")


def batch_process(
    data: List[DataPoint],
    processor: DataProcessor,
    batch_size: int = 10
) -> List[DataPoint]:
    """
    Process data in batches
    
    Args:
        data: Data to process
        processor: Processor instance
        batch_size: Size of each batch
        
    Returns:
        All processed data
    """
    results = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        results.extend(processor.process_data(batch))
    return results


# Constants
DEFAULT_THRESHOLD = 0.5
MAX_BATCH_SIZE = 1000
SUPPORTED_METRICS = ["euclidean", "manhattan", "cosine"]


# Module-level utility functions
def create_sample_data(count: int = 100) -> List[DataPoint]:
    """
    Create sample data for testing
    
    Args:
        count: Number of data points to create
        
    Returns:
        List of sample data points
    """
    import random
    return [
        DataPoint(
            x=random.random(),
            y=random.random(),
            label=f"point_{i}"
        )
        for i in range(count)
    ]


def validate_data(data: List[DataPoint]) -> bool:
    """
    Validate data integrity
    
    Args:
        data: Data to validate
        
    Returns:
        True if data is valid
    """
    if not data:
        return False
    
    for point in data:
        if point.x is None or point.y is None:
            return False
    
    return True


__all__ = [
    "ProcessingMode",
    "DataPoint",
    "DataProcessor",
    "calculate_similarity",
    "batch_process",
    "create_sample_data",
    "validate_data",
    "DEFAULT_THRESHOLD",
    "MAX_BATCH_SIZE",
    "SUPPORTED_METRICS"
]
