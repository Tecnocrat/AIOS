#!/usr/bin/env python3
"""
AIOS Evolution Lab - First Mistral Mutation
Organism: org_utility_gen1_mistral_001
Parent: org_utility_gen0_original
Engine: aios-mistral (Mistral 7B Instruct)
Date: 2025-12-05
Fitness: 0.725 (+0.225 from parent)

Improvements applied by Mistral:
- Added type hints (List -> int)
- Added error handling (try/except)
- Added exception chaining (from e)

Known issues (for next mutation):
- import exceptions is unused/incorrect (removed here)
- List should be List[int] or List[float] (fixed here)
"""

from typing import List


def calculate_sum(numbers: List[int]) -> int:
    """
    Calculate the sum of a list of numbers.
    
    Args:
        numbers: List of integers to sum
        
    Returns:
        Sum of all numbers in the list
        
    Raises:
        ValueError: If list contains non-numeric values
    """
    try:
        total = 0
        for n in numbers:
            total = total + n
        return total
    except TypeError as e:
        raise ValueError(
            "Invalid input. Ensure the provided list contains only numeric values."
        ) from e


# Test the organism
if __name__ == "__main__":
    # Basic test
    result = calculate_sum([1, 2, 3, 4, 5])
    print(f"Sum of [1,2,3,4,5]: {result}")
    assert result == 15, f"Expected 15, got {result}"
    
    # Empty list
    result = calculate_sum([])
    print(f"Sum of []: {result}")
    assert result == 0, f"Expected 0, got {result}"
    
    # Error handling test
    try:
        calculate_sum(["a", "b"])
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    print("✅ All tests passed - Organism is viable!")
