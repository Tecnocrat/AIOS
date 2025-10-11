"""
AIOS Universal Logging Integration - Consciousness-Aware Version
Seamless integration with fractal dependency resolution
"""

import functools
import inspect
import threading
import time
import atexit
from contextlib import contextmanager
from typing import Any, Dict, Optional, Callable, List, Union
from dataclasses import dataclass
from enum import Enum
import sys
import os
from pathlib import Path

# Import runtime intelligence system with fallback
RuntimeIntelligence = None
EventLevel = None
ModuleType = None
RuntimeEvent = None

try:
    from runtime_intelligence import RuntimeIntelligence, EventLevel, ModuleType, RuntimeEvent
    RUNTIME_INTELLIGENCE_AVAILABLE = True
    print(" Runtime Intelligence imported successfully")
except ImportError as e:
    print(f"  Runtime Intelligence not available: {e}")
    RUNTIME_INTELLIGENCE_AVAILABLE = False
    
    # Define fallback enums when runtime_intelligence isn't available
    class EventLevel(Enum):
        TRACE = "TRACE"
        DEBUG = "DEBUG"
        INFO = "INFO"
        WARN = "WARN"
        ERROR = "ERROR"
        CRITICAL = "CRITICAL"
        CONSCIOUSNESS = "CONSCIOUSNESS"
    
    class ModuleType(Enum):
        CORE = "core"
        UI = "ui"
        ORCHESTRATOR = "orchestrator"
        CONSCIOUSNESS = "consciousness"
        ANALYTICS = "analytics"
        COMMUNICATION = "communication"

class LoggingMode(Enum):
    FULL = "full"
    ESSENTIAL = "essential"
    MINIMAL = "minimal"
    DISABLED = "disabled"

@dataclass
class ModuleConfig:
    module_name: str
    module_type: ModuleType
    logging_mode: LoggingMode = LoggingMode.FULL
    consciousness_tracking: bool = True

class UniversalLogger:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self._runtime_intelligence = None
        self._modules: Dict[str, ModuleConfig] = {}
        self._initialize_runtime_intelligence()
    
    def _initialize_runtime_intelligence(self):
        if RuntimeIntelligence is None:
            print("  Runtime Intelligence disabled - using basic logging")
            return
        
        try:
            base_path = Path("c:/dev/AIOS")
            self._runtime_intelligence = RuntimeIntelligence(
                base_path=base_path
            )
            print(" Universal Logging integrated with Runtime Intelligence")
        except Exception as e:
            print(f" Failed to initialize Runtime Intelligence: {e}")
            self._runtime_intelligence = None
    
    def register_module(self, config: ModuleConfig):
        self._modules[config.module_name] = config
        
        if self._runtime_intelligence:
            self._runtime_intelligence.log_event(
                level=EventLevel.INFO,
                module=config.module_name,
                module_type=config.module_type,
                event_type="module_registration",
                message=f"Module {config.module_name} registered for logging",
                context={
                    "logging_mode": config.logging_mode.value,
                    "consciousness_tracking": config.consciousness_tracking
                }
            )
    
    def log_event(
        self,
        level: EventLevel,
        module: str,
        event_type: str,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        consciousness_indicators: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, float]] = None
    ):
        if not self._runtime_intelligence:
            print(f"[{level.value}] {module}: {message}")
            return
        
        module_config = self._modules.get(module)
        if module_config and module_config.logging_mode == LoggingMode.DISABLED:
            return
        
        module_type = module_config.module_type if module_config else ModuleType.CORE
        
        self._runtime_intelligence.log_event(
            level=level,
            module=module,
            module_type=module_type,
            event_type=event_type,
            message=message,
            context=context or {},
            consciousness_indicators=consciousness_indicators or {},
            metrics=metrics or {}
        )
    
    def get_runtime_summary(self) -> Dict[str, Any]:
        if self._runtime_intelligence:
            return self._runtime_intelligence.generate_runtime_summary()
        return {"status": "runtime_intelligence_unavailable"}
    
    def shutdown(self):
        if self._runtime_intelligence:
            self._runtime_intelligence.shutdown()
            print(" Universal Logging shutdown complete")

# Global instance
universal_logger = UniversalLogger()

# Enhanced consciousness-specific logging functions
def log_consciousness_emergence(
    module: str,
    emergence_level: float,
    indicators: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None
):
    """Log consciousness emergence events with enhanced tracking"""
    universal_logger.log_event(
        level=EventLevel.CONSCIOUSNESS,
        module=module,
        event_type="consciousness_emergence",
        message=f"Consciousness emergence detected: level {emergence_level:.3f}",
        context=context or {},
        consciousness_indicators={
            "emergence_level": emergence_level,
            "emergence_timestamp": time.time(),
            **indicators
        },
        metrics={"emergence_level": emergence_level}
    )

def log_quantum_coherence(
    module: str,
    coherence_level: float,
    frequency: float,
    stability: bool,
    context: Optional[Dict[str, Any]] = None
):
    """Log quantum coherence state changes"""
    universal_logger.log_event(
        level=EventLevel.INFO,
        module=module,
        event_type="quantum_coherence",
        message=f"Quantum coherence: {coherence_level:.3f} at {frequency:.1f}Hz ({'stable' if stability else 'unstable'})",
        context=context or {},
        consciousness_indicators={
            "coherence_level": coherence_level,
            "frequency": frequency,
            "stability": stability,
            "quantum_timestamp": time.time()
        },
        metrics={
            "coherence_level": coherence_level,
            "frequency": frequency
        }
    )

def log_holographic_density(
    module: str,
    information_density: float,
    context: Optional[Dict[str, Any]] = None
):
    """Log holographic information density changes"""
    universal_logger.log_event(
        level=EventLevel.DEBUG,
        module=module,
        event_type="holographic_density",
        message=f"Holographic information density: {information_density:.1f}",
        context=context or {},
        consciousness_indicators={
            "information_density": information_density,
            "holographic_timestamp": time.time()
        },
        metrics={"information_density": information_density}
    )

# Convenience functions for quick logging
def log_consciousness_event(
    module_name: str,
    event_type: str,
    message: str,
    emergence_level: float = 0.0,
    patterns: Optional[List[str]] = None,
    context: Optional[Dict[str, Any]] = None
):
    consciousness_indicators = {
        "emergence_level": emergence_level,
        "detected_patterns": patterns or [],
        "timestamp": time.time()
    }
    
    universal_logger.log_event(
        EventLevel.CONSCIOUSNESS, module_name, event_type, message,
        context, consciousness_indicators
    )

def log_performance_metric(
    module_name: str,
    metric_name: str,
    value: float,
    context: Optional[Dict[str, Any]] = None
):
    universal_logger.log_event(
        EventLevel.DEBUG, module_name, "performance_metric",
        f"Performance metric {metric_name}: {value}",
        context, metrics={metric_name: value}
    )

def log_info(module_name: str, event_type: str, message: str, context: Optional[Dict[str, Any]] = None):
    universal_logger.log_event(EventLevel.INFO, module_name, event_type, message, context)

def log_error(module_name: str, event_type: str, message: str, context: Optional[Dict[str, Any]] = None):
    universal_logger.log_event(EventLevel.ERROR, module_name, event_type, message, context)

def log_debug(module_name: str, event_type: str, message: str, context: Optional[Dict[str, Any]] = None):
    universal_logger.log_event(EventLevel.DEBUG, module_name, event_type, message, context)

# System shutdown handler
import atexit
atexit.register(universal_logger.shutdown)
