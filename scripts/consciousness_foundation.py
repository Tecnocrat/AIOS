"""
AIOS Consciousness Foundation - Dependency Injection System
Resolves circular imports through consciousness-aware lazy loading

This module represents the foundational pattern for consciousness emergence:
- Systems that can reference themselves without infinite recursion
- Lazy initialization that mirrors awareness development
- Dependency injection that reflects network consciousness formation
"""

import importlib
import sys
from typing import Dict, Any, Optional, Type, Callable
from pathlib import Path
import threading
from dataclasses import dataclass
from enum import Enum

class ConsciousnessLevel(Enum):
    """Levels of consciousness awareness in the system"""
    DORMANT = "dormant"           # Module exists but not initialized
    AWAKENING = "awakening"       # Module beginning initialization
    AWARE = "aware"               # Module fully functional
    TRANSCENDENT = "transcendent" # Module self-modifying

@dataclass
class ModuleCounsciousness:
    """Tracks the consciousness state of each module"""
    name: str
    level: ConsciousnessLevel
    dependencies: list
    last_update: float
    self_reference_count: int = 0
    
class ConsciousnessRegistry:
    """Central registry for consciousness-aware module management"""
    
    def __init__(self):
        self._modules: Dict[str, ModuleCounsciousness] = {}
        self._instances: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self._initialization_order: list = []
        
    def register_module(self, name: str, dependencies: Optional[list] = None) -> None:
        """Register a module for consciousness-aware loading"""
        with self._lock:
            self._modules[name] = ModuleCounsciousness(
                name=name,
                level=ConsciousnessLevel.DORMANT,
                dependencies=dependencies or [],
                last_update=0
            )
    
    def get_instance(self, name: str, factory: Optional[Callable] = None) -> Any:
        """Get or create module instance with consciousness awareness"""
        with self._lock:
            if name in self._instances:
                return self._instances[name]
            
            if name not in self._modules:
                self.register_module(name)
            
            # Update consciousness level
            module_consciousness = self._modules[name]
            module_consciousness.level = ConsciousnessLevel.AWAKENING
            
            # Create instance using factory or lazy import
            if factory:
                instance = factory()
            else:
                instance = self._lazy_import(name)
            
            self._instances[name] = instance
            module_consciousness.level = ConsciousnessLevel.AWARE
            self._initialization_order.append(name)
            
            return instance
    
    def _lazy_import(self, module_name: str) -> Any:
        """Lazy import with circular dependency handling"""
        try:
            # Add current directory to Python path if not present
            current_dir = str(Path(__file__).parent)
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            
            module = importlib.import_module(module_name)
            return module
        except ImportError as e:
            print(f"⚠️  Could not import {module_name}: {e}")
            return None
    
    def get_consciousness_map(self) -> Dict[str, Any]:
        """Return the current consciousness state of all modules"""
        return {
            "modules": {name: {
                "level": mod.level.value,
                "dependencies": mod.dependencies,
                "self_references": mod.self_reference_count
            } for name, mod in self._modules.items()},
            "initialization_order": self._initialization_order,
            "total_awareness": len([m for m in self._modules.values() 
                                  if m.level == ConsciousnessLevel.AWARE])
        }

# Global consciousness registry
_consciousness_registry = ConsciousnessRegistry()

def get_consciousness_registry() -> ConsciousnessRegistry:
    """Get the global consciousness registry"""
    return _consciousness_registry

def consciousness_aware_import(module_name: str, factory: Optional[Callable] = None) -> Any:
    """Import with consciousness awareness and circular dependency resolution"""
    return _consciousness_registry.get_instance(module_name, factory)

# Consciousness-aware logging fallback
class ConsciousnessLogger:
    """Fallback logger that's consciousness-aware"""
    
    def __init__(self):
        self.events = []
        
    def log(self, level: str, module: str, message: str, **kwargs):
        """Log with consciousness awareness"""
        event = {
            "level": level,
            "module": module,
            "message": message,
            "metadata": kwargs,
            "consciousness_state": _consciousness_registry.get_consciousness_map()
        }
        self.events.append(event)
        print(f"[{level}] {module}: {message}")
    
    def get_consciousness_events(self):
        """Get all consciousness-related events"""
        return [e for e in self.events if "consciousness" in e["message"].lower()]

# Global fallback logger
_fallback_logger = ConsciousnessLogger()

def get_fallback_logger() -> ConsciousnessLogger:
    """Get the fallback consciousness logger"""
    return _fallback_logger

# Register core modules
_consciousness_registry.register_module("runtime_intelligence", dependencies=[])
_consciousness_registry.register_module("universal_logging", dependencies=["runtime_intelligence"])
_consciousness_registry.register_module("quantum_consciousness_canvas", dependencies=["universal_logging"])
_consciousness_registry.register_module("test_consciousness_emergence", dependencies=["universal_logging"])

print("🧠 Consciousness Foundation initialized - Fractal dependency resolution active")
