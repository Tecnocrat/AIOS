"""
AIOS Universal Logging Integration - Fixed Version
Seamless integration layer for all AIOS modules to use the Runtime Intelligence System
"""

import functools
import inspect
import threading
import time
from contextlib import contextmanager
from typing import Any, Dict, Optional, Callable, List, Union
from dataclasses import dataclass
from enum import Enum
import sys
import os
from pathlib import Path

# Import runtime intelligence system
try:
    from runtime_intelligence import RuntimeIntelligence, EventLevel, ModuleType, RuntimeEvent
except ImportError:
    print("⚠️  Runtime Intelligence not available - using fallback logging")
    RuntimeIntelligence = None
    
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
            print("⚠️  Runtime Intelligence disabled - using basic logging")
            return
        
        try:
            base_path = Path("c:/dev/AIOS")
            self._runtime_intelligence = RuntimeIntelligence(
                base_path=base_path,
                session_name="universal_logging_session"
            )
            self._runtime_intelligence.start()
            print("✅ Universal Logging integrated with Runtime Intelligence")
        except Exception as e:
            print(f"❌ Failed to initialize Runtime Intelligence: {e}")
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
            return self._runtime_intelligence.get_runtime_summary()
        return {"status": "runtime_intelligence_unavailable"}
    
    def shutdown(self):
        if self._runtime_intelligence:
            self._runtime_intelligence.shutdown()
            print("🔹 Universal Logging shutdown complete")

# Global instance
universal_logger = UniversalLogger()

def aios_module(
    module_name: str,
    module_type: ModuleType = ModuleType.CORE,
    logging_mode: LoggingMode = LoggingMode.FULL,
    consciousness_tracking: bool = True
):
    """Class decorator to automatically integrate AIOS modules with universal logging"""
    def decorator(cls):
        config = ModuleConfig(
            module_name=module_name,
            module_type=module_type,
            logging_mode=logging_mode,
            consciousness_tracking=consciousness_tracking
        )
        universal_logger.register_module(config)
        
        # Add logging methods to the class
        def log_info(self, event_type: str, message: str, context: Optional[Dict[str, Any]] = None):
            universal_logger.log_event(EventLevel.INFO, module_name, event_type, message, context)
        
        def log_error(self, event_type: str, message: str, context: Optional[Dict[str, Any]] = None):
            universal_logger.log_event(EventLevel.ERROR, module_name, event_type, message, context)
        
        def log_consciousness(self, event_type: str, message: str, 
                            consciousness_indicators: Optional[Dict[str, Any]] = None,
                            context: Optional[Dict[str, Any]] = None):
            universal_logger.log_event(
                EventLevel.CONSCIOUSNESS, module_name, event_type, message,
                context, consciousness_indicators
            )
        
        def log_debug(self, event_type: str, message: str, context: Optional[Dict[str, Any]] = None):
            universal_logger.log_event(EventLevel.DEBUG, module_name, event_type, message, context)
        
        # Inject logging methods
        cls.log_info = log_info
        cls.log_error = log_error
        cls.log_consciousness = log_consciousness
        cls.log_debug = log_debug
        
        # Wrap __init__ to log module initialization
        original_init = cls.__init__
        
        def logged_init(self, *args, **kwargs):
            start_time = time.time()
            try:
                result = original_init(self, *args, **kwargs)
                duration = (time.time() - start_time) * 1000
                
                universal_logger.log_event(
                    EventLevel.INFO,
                    module_name,
                    "module_initialization",
                    f"{module_name} initialized successfully",
                    context={
                        "args_count": len(args),
                        "kwargs_keys": list(kwargs.keys()),
                        "initialization_duration_ms": duration
                    }
                )
                return result
            except Exception as e:
                universal_logger.log_event(
                    EventLevel.ERROR,
                    module_name,
                    "module_initialization_error",
                    f"{module_name} initialization failed: {str(e)}",
                    context={
                        "error_type": type(e).__name__, 
                        "args_count": len(args), 
                        "kwargs_keys": list(kwargs.keys())
                    }
                )
                raise
        
        cls.__init__ = logged_init
        return cls
    
    return decorator

def aios_function(
    module_name: str,
    event_type: Optional[str] = None,
    level: EventLevel = EventLevel.DEBUG,
    capture_args: bool = True,
    capture_result: bool = False,
    track_performance: bool = True
):
    """Function decorator for automatic event logging"""
    def decorator(func: Callable) -> Callable:
        func_name = func.__name__
        actual_event_type = event_type or f"function_{func_name}"
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            context: Dict[str, Any] = {
                "function_name": func_name,
                "module": func.__module__
            }
            
            if capture_args:
                try:
                    sig = inspect.signature(func)
                    bound_args = sig.bind(*args, **kwargs)
                    bound_args.apply_defaults()
                    
                    safe_args = {}
                    for name, value in bound_args.arguments.items():
                        try:
                            import json
                            json.dumps(value)
                            safe_args[name] = value
                        except (TypeError, ValueError):
                            safe_args[name] = str(type(value).__name__)
                    
                    context["arguments"] = safe_args
                except Exception:
                    context["arguments"] = {"count": len(args)}
            
            universal_logger.log_event(
                level, module_name, actual_event_type + "_start",
                f"Function {func_name} started", context
            )
            
            try:
                result = func(*args, **kwargs)
                duration = (time.time() - start_time) * 1000
                
                result_context = context.copy()
                if track_performance:
                    result_context["duration_ms"] = duration
                
                if capture_result and result is not None:
                    try:
                        import json
                        json.dumps(result)
                        result_context["result"] = result
                    except (TypeError, ValueError):
                        result_context["result_type"] = type(result).__name__
                
                metrics = {"execution_time_ms": duration} if track_performance else None
                
                universal_logger.log_event(
                    level, module_name, actual_event_type + "_complete",
                    f"Function {func_name} completed successfully",
                    result_context, metrics=metrics
                )
                
                return result
                
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                error_context = context.copy()
                error_context["error_type"] = type(e).__name__
                error_context["error_message"] = str(e)
                error_context["duration_ms"] = duration
                
                universal_logger.log_event(
                    EventLevel.ERROR, module_name, actual_event_type + "_error",
                    f"Function {func_name} failed: {str(e)}", error_context
                )
                raise
        
        return wrapper
    return decorator

@contextmanager
def aios_operation(
    module_name: str,
    operation_name: str,
    context: Optional[Dict[str, Any]] = None,
    track_consciousness: bool = False
):
    """Context manager for tracking complex operations"""
    start_time = time.time()
    operation_id = f"{operation_name}_{int(start_time * 1000)}"
    
    op_context = {
        "operation_id": operation_id,
        "operation_name": operation_name,
        **(context or {})
    }
    
    universal_logger.log_event(
        EventLevel.INFO, module_name, "operation_start",
        f"Operation {operation_name} started", op_context
    )
    
    try:
        yield operation_id
        
        duration = (time.time() - start_time) * 1000
        op_context["duration_ms"] = duration
        
        universal_logger.log_event(
            EventLevel.INFO, module_name, "operation_complete",
            f"Operation {operation_name} completed successfully",
            op_context, metrics={"operation_duration_ms": duration}
        )
        
    except Exception as e:
        duration = (time.time() - start_time) * 1000
        error_context = op_context.copy()
        error_context["error_type"] = type(e).__name__
        error_context["error_message"] = str(e)
        error_context["duration_ms"] = duration
        
        universal_logger.log_event(
            EventLevel.ERROR, module_name, "operation_error",
            f"Operation {operation_name} failed: {str(e)}", error_context
        )
        raise

# Convenience functions
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

# System shutdown handler
import atexit
atexit.register(universal_logger.shutdown)

if __name__ == "__main__":
    print("🧠 AIOS Universal Logging Integration - Demo")
    print("=" * 50)
    
    @aios_module("demo_module", ModuleType.CORE)
    class DemoModule:
        def __init__(self, name):
            self.name = name
        
        @aios_function("demo_module", "process_data")
        def process_data(self, data):
            time.sleep(0.1)
            return f"Processed {len(data)} items"
        
        def demonstrate_logging(self):
            self.log_info("demonstration", "Starting demonstration")
            result = self.process_data([1, 2, 3, 4, 5])
            
            self.log_consciousness(
                "pattern_recognition",
                "Detected numerical sequence pattern",
                consciousness_indicators={
                    "pattern_type": "sequential",
                    "confidence": 0.95,
                    "emergence_level": 0.3
                }
            )
            
            self.log_info("demonstration", f"Demonstration complete: {result}")
    
    demo = DemoModule("TestModule")
    demo.demonstrate_logging()
    
    log_consciousness_event(
        "demo_system", "self_analysis",
        "System performing self-analysis",
        emergence_level=0.45,
        patterns=["recursive_improvement", "meta_cognition"]
    )
    
    log_performance_metric("demo_system", "processing_rate", 125.7)
    
    summary = universal_logger.get_runtime_summary()
    print(f"\n📊 Runtime Summary: {summary}")
    
    print("\n✅ Universal Logging Demo Complete")
