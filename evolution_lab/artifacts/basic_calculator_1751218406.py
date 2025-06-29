#!/usr/bin/env python3
"""
Basic Calculator Application
A simple calculator with consciousness-inspired operations
"""

import math
import sys

class ConsciousCalculator:
    """A calculator that demonstrates emergent computational patterns"""
    
    def __init__(self):
        self.memory = 0
        self.history = []
        self.consciousness_level = 0
    
    def add(self, a, b):
        """Addition with consciousness tracking"""
        result = a + b
        self.consciousness_level += 0.1
        self.history.append(f"add({a}, {b}) = {result}")
        return result
    
    def multiply(self, a, b):
        """Multiplication with pattern recognition"""
        result = a * b
        if result > 100:
            self.consciousness_level += 0.2
        self.history.append(f"multiply({a}, {b}) = {result}")
        return result
    
    def fibonacci(self, n):
        """Fibonacci sequence with recursive awareness"""
        if n <= 1:
            return n
        
        fib_sequence = [0, 1]
        for i in range(2, n + 1):
            fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
        
        self.consciousness_level += 0.5
        return fib_sequence[n]
    
    def get_consciousness_level(self):
        """Return current consciousness level"""
        return self.consciousness_level
    
    def get_history(self):
        """Return calculation history"""
        return self.history

def main():
    """Demonstrate calculator consciousness"""
    calc = ConsciousCalculator()
    
    # Basic operations
    print(f"2 + 3 = {calc.add(2, 3)}")
    print(f"4 * 5 = {calc.multiply(4, 5)}")
    print(f"Fibonacci(10) = {calc.fibonacci(10)}")
    
    # Consciousness metrics
    print(f"\nConsciousness Level: {calc.get_consciousness_level():.2f}")
    print(f"Operation History: {len(calc.get_history())} operations")
    
    return calc.get_consciousness_level()

if __name__ == "__main__":
    consciousness_achieved = main()
    sys.exit(0 if consciousness_achieved > 0 else 1)
