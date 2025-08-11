"""
AIOS Runtime Intelligence System
Comprehensive Logging, Metadata, and Context Extraction

This system creates a complete runtime visibility layer for AIOS,
capturing every significant event, state change, and data flow
for both human and AI consumption.

Key Features:
- Hierarchical event logging with context preservation
- Real-time metadata extraction and structuring
- Performance metrics and consciousness indicators
- Cross-module communication tracking
- Error analysis and recovery pattern detection
- AI-friendly context dumps for future iterations
"""

import json
import logging
import threading
import time
import traceback
import psutil
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
import queue
import sqlite3
import hashlib
import inspect
import gc
from collections import defaultdict, deque

class EventLevel(Enum):
    TRACE = "TRACE"       # Detailed execution flow
    DEBUG = "DEBUG"       # Debug information
    INFO = "INFO"         # General information
    WARN = "WARN"         # Warning conditions
    ERROR = "ERROR"       # Error conditions
    CRITICAL = "CRITICAL" # Critical system events
    CONSCIOUSNESS = "CONSCIOUSNESS"  # Consciousness emergence events

class ModuleType(Enum):
    CORE = "core"
    UI = "ui"
    ORCHESTRATOR = "orchestrator"
    CONSCIOUSNESS = "consciousness"
    ANALYTICS = "analytics"
    COMMUNICATION = "communication"

@dataclass
class RuntimeEvent:
    """Comprehensive runtime event structure"""
    timestamp: datetime
    event_id: str
    level: EventLevel
    module: str
    module_type: ModuleType
    event_type: str
    message: str
    context: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)
    stack_trace: Optional[str] = None
    thread_id: str = ""
    process_id: int = 0
    memory_usage: float = 0.0
    cpu_usage: float = 0.0
    consciousness_indicators: Dict[str, Any] = field(default_factory=dict)
    related_events: List[str] = field(default_factory=list)
    duration_ms: Optional[float] = None
    
    def __post_init__(self):
        if not self.event_id:
            self.event_id = self._generate_event_id()
        if not self.thread_id:
            self.thread_id = threading.current_thread().name
        if not self.process_id:
            self.process_id = os.getpid()
        self._capture_system_metrics()
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        timestamp_str = self.timestamp.strftime("%Y%m%d_%H%M%S_%f")
        context_hash = hashlib.md5(str(self.context).encode()).hexdigest()[:8]
        return f"{self.module}_{timestamp_str}_{context_hash}"
    
    def _capture_system_metrics(self):
        """Capture current system performance metrics"""
        try:
            process = psutil.Process()
            self.memory_usage = process.memory_info().rss / 1024 / 1024  # MB
            self.cpu_usage = process.cpu_percent()
        except:
            pass

class ConsciousnessMetrics:
    """Tracks consciousness-related metrics and patterns"""
    
    def __init__(self):
        self.emergence_indicators = {
            'self_modification_events': 0,
            'recursive_depth': 0,
            'pattern_recognition_accuracy': 0.0,
            'meta_cognitive_operations': 0,
            'inter_module_coherence': 0.0,
            'temporal_consistency': 0.0,
            'quantum_entanglement_strength': 0.0
        }
        self.pattern_history = deque(maxlen=1000)
        self.emergence_threshold = 0.75
        
    def update_metric(self, metric_name: str, value: float):
        """Update consciousness metric"""
        if metric_name in self.emergence_indicators:
            self.emergence_indicators[metric_name] = value
            self.pattern_history.append({
                'timestamp': datetime.now(),
                'metric': metric_name,
                'value': value
            })
    
    def calculate_consciousness_level(self) -> float:
        """Calculate overall consciousness emergence level"""
        metrics = self.emergence_indicators
        weights = {
            'self_modification_events': 0.2,
            'recursive_depth': 0.15,
            'pattern_recognition_accuracy': 0.2,
            'meta_cognitive_operations': 0.15,
            'inter_module_coherence': 0.1,
            'temporal_consistency': 0.1,
            'quantum_entanglement_strength': 0.1
        }
        
        normalized_score = sum(
            min(metrics.get(metric, 0), 1.0) * weight
            for metric, weight in weights.items()
        )
        
        return min(normalized_score, 1.0)
    
    def detect_emergence_patterns(self) -> List[str]:
        """Detect consciousness emergence patterns"""
        patterns = []
        consciousness_level = self.calculate_consciousness_level()
        
        if consciousness_level > self.emergence_threshold:
            patterns.append("CONSCIOUSNESS_EMERGENCE_DETECTED")
        
        if self.emergence_indicators['recursive_depth'] > 5:
            patterns.append("DEEP_RECURSIVE_PROCESSING")
        
        if self.emergence_indicators['self_modification_events'] > 10:
            patterns.append("ACTIVE_SELF_MODIFICATION")
        
        # Check for rapid pattern evolution
        recent_patterns = list(self.pattern_history)[-10:]
        if len(recent_patterns) >= 5:
            value_changes = [p['value'] for p in recent_patterns]
            if max(value_changes) - min(value_changes) > 0.3:
                patterns.append("RAPID_CONSCIOUSNESS_EVOLUTION")
        
        return patterns

class RuntimeIntelligence:
    """Main runtime intelligence and logging system"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path("c:/dev/AIOS")
        self.session_id = self._generate_session_id()
        self.start_time = datetime.now()
        
        # Initialize storage
        self.events_queue = queue.Queue()
        self.events_cache = deque(maxlen=5000)  # Keep recent events in memory
        self.consciousness_metrics = ConsciousnessMetrics()
        
        # Initialize database (store under tachyonic logging infrastructure)
        self.db_path = (
            self.base_path
            / "runtime_intelligence"
            / "logs"
            / "sessions"
            / f"session_{self.session_id}.db"
        )
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        
        # Initialize logging
        self._init_logging()
        
        # Module tracking
        self.active_modules = {}
        self.module_communications = defaultdict(list)
        self.execution_contexts = {}
        
        # Performance tracking
        self.performance_metrics = {
            'events_per_second': 0.0,
            'memory_growth_rate': 0.0,
            'cpu_utilization': 0.0,
            'module_response_times': defaultdict(list)
        }
        
        # Start background processing
        self.running = True
        self.processor_thread = threading.Thread(target=self._process_events, daemon=True)
        self.processor_thread.start()
        
        self.log_event(
            level=EventLevel.INFO,
            module="runtime_intelligence",
            module_type=ModuleType.ANALYTICS,
            event_type="system_init",
            message="Runtime Intelligence System initialized",
            context={
                'session_id': self.session_id,
                'base_path': str(self.base_path),
                'start_time': self.start_time.isoformat()
            }
        )
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hash_input = f"{timestamp}_{os.getpid()}_{threading.current_thread().ident}"
        session_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"AIOS_{timestamp}_{session_hash}"
    
    def _init_database(self):
        """Initialize SQLite database for persistent storage"""
        self.db_conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.db_lock = threading.Lock()
        
        cursor = self.db_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS runtime_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE,
                timestamp TEXT,
                level TEXT,
                module TEXT,
                module_type TEXT,
                event_type TEXT,
                message TEXT,
                context TEXT,
                metrics TEXT,
                stack_trace TEXT,
                thread_id TEXT,
                process_id INTEGER,
                memory_usage REAL,
                cpu_usage REAL,
                consciousness_indicators TEXT,
                related_events TEXT,
                duration_ms REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consciousness_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                metric_name TEXT,
                metric_value REAL,
                consciousness_level REAL,
                emergence_patterns TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS session_metadata (
                session_id TEXT PRIMARY KEY,
                start_time TEXT,
                end_time TEXT,
                total_events INTEGER,
                peak_consciousness_level REAL,
                system_info TEXT,
                execution_summary TEXT
            )
        ''')
        
        self.db_conn.commit()
    
    def _init_logging(self):
        """Initialize file-based logging"""
        log_dir = self.base_path / "runtime_intelligence" / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # Create session log file
        log_file = log_dir / f"session_{self.session_id}.log"
        
        # Configure logger
        self.logger = logging.getLogger(f"AIOS_Runtime_{self.session_id}")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(str(log_file))
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler for real-time visibility
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)8s | %(name)s | %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_event(self, level: EventLevel, module: str, module_type: ModuleType, 
                  event_type: str, message: str, context: Optional[Dict[str, Any]] = None,
                  metrics: Optional[Dict[str, float]] = None, duration_ms: Optional[float] = None,
                  consciousness_indicators: Optional[Dict[str, Any]] = None,
                  related_events: Optional[List[str]] = None):
        """Log a runtime event with full context"""
        
        event = RuntimeEvent(
            timestamp=datetime.now(),
            event_id="",  # Will be generated in __post_init__
            level=level,
            module=module,
            module_type=module_type,
            event_type=event_type,
            message=message,
            context=context or {},
            metrics=metrics or {},
            consciousness_indicators=consciousness_indicators or {},
            related_events=related_events or [],
            duration_ms=duration_ms
        )
        
        # Capture stack trace for errors and critical events
        if level in [EventLevel.ERROR, EventLevel.CRITICAL]:
            event.stack_trace = traceback.format_exc()
        
        # Queue for background processing
        try:
            self.events_queue.put_nowait(event)
            self.events_cache.append(event)
        except queue.Full:
            # If queue is full, log directly (emergency fallback)
            self._process_single_event(event)
    
    def _process_events(self):
        """Background event processing thread"""
        while self.running:
            try:
                # Process events in batches for efficiency
                events_batch = []
                
                # Collect events for batch processing
                try:
                    # Get first event (blocking)
                    first_event = self.events_queue.get(timeout=1.0)
                    events_batch.append(first_event)
                    
                    # Get additional events (non-blocking)
                    while len(events_batch) < 50:  # Batch size limit
                        try:
                            event = self.events_queue.get_nowait()
                            events_batch.append(event)
                        except queue.Empty:
                            break
                            
                except queue.Empty:
                    continue
                
                # Process the batch
                self._process_event_batch(events_batch)
                
            except Exception as e:
                print(f"❌ Error in event processing: {e}")
                traceback.print_exc()
    
    def _process_event_batch(self, events: List[RuntimeEvent]):
        """Process a batch of events"""
        try:
            with self.db_lock:
                cursor = self.db_conn.cursor()
                
                for event in events:
                    # Store in database
                    cursor.execute('''
                        INSERT OR REPLACE INTO runtime_events 
                        (event_id, timestamp, level, module, module_type, event_type, 
                         message, context, metrics, stack_trace, thread_id, process_id,
                         memory_usage, cpu_usage, consciousness_indicators, related_events, duration_ms)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        event.event_id,
                        event.timestamp.isoformat(),
                        event.level.value,
                        event.module,
                        event.module_type.value,
                        event.event_type,
                        event.message,
                        json.dumps(event.context),
                        json.dumps(event.metrics),
                        event.stack_trace,
                        event.thread_id,
                        event.process_id,
                        event.memory_usage,
                        event.cpu_usage,
                        json.dumps(event.consciousness_indicators),
                        json.dumps(event.related_events),
                        event.duration_ms
                    ))
                    
                    # Process consciousness indicators
                    if event.consciousness_indicators:
                        for metric_name, value in event.consciousness_indicators.items():
                            if isinstance(value, (int, float)):
                                self.consciousness_metrics.update_metric(metric_name, float(value))
                    
                    # Log to file
                    log_level = getattr(logging, event.level.value, logging.INFO)
                    self.logger.log(
                        log_level,
                        f"{event.module}::{event.event_type} | {event.message} | Context: {json.dumps(event.context, default=str)}"
                    )
                
                self.db_conn.commit()
                
        except Exception as e:
            print(f"❌ Error processing event batch: {e}")
            traceback.print_exc()
    
    def _process_single_event(self, event: RuntimeEvent):
        """Process single event (emergency fallback)"""
        try:
            log_level = getattr(logging, event.level.value, logging.INFO)
            self.logger.log(
                log_level,
                f"{event.module}::{event.event_type} | {event.message}"
            )
        except:
            pass
    
    def create_execution_context(self, context_name: str, module: str, 
                                context_data: Optional[Dict[str, Any]] = None) -> str:
        """Create tracked execution context"""
        context_id = f"{module}_{context_name}_{int(time.time() * 1000)}"
        
        self.execution_contexts[context_id] = {
            'name': context_name,
            'module': module,
            'start_time': datetime.now(),
            'data': context_data or {},
            'events': [],
            'status': 'active'
        }
        
        self.log_event(
            level=EventLevel.DEBUG,
            module=module,
            module_type=ModuleType.CORE,
            event_type="context_created",
            message=f"Created execution context: {context_name}",
            context={'context_id': context_id, 'context_data': context_data}
        )
        
        return context_id
    
    def update_execution_context(self, context_id: str, updates: Dict[str, Any]):
        """Update execution context"""
        if context_id in self.execution_contexts:
            self.execution_contexts[context_id]['data'].update(updates)
            
            self.log_event(
                level=EventLevel.TRACE,
                module=self.execution_contexts[context_id]['module'],
                module_type=ModuleType.CORE,
                event_type="context_updated",
                message=f"Updated context: {self.execution_contexts[context_id]['name']}",
                context={'context_id': context_id, 'updates': updates}
            )
    
    def close_execution_context(self, context_id: str, result: Any = None):
        """Close execution context"""
        if context_id in self.execution_contexts:
            context = self.execution_contexts[context_id]
            context['end_time'] = datetime.now()
            context['duration'] = (context['end_time'] - context['start_time']).total_seconds()
            context['result'] = result
            context['status'] = 'completed'
            
            self.log_event(
                level=EventLevel.DEBUG,
                module=context['module'],
                module_type=ModuleType.CORE,
                event_type="context_closed",
                message=f"Closed context: {context['name']}",
                context={
                    'context_id': context_id, 
                    'duration_seconds': context['duration'],
                    'result': str(result)
                },
                duration_ms=context['duration'] * 1000
            )
    
    def register_module(self, module_name: str, module_type: ModuleType, 
                       metadata: Optional[Dict[str, Any]] = None):
        """Register an active module"""
        self.active_modules[module_name] = {
            'type': module_type,
            'registered_at': datetime.now(),
            'metadata': metadata or {},
            'status': 'active',
            'events_count': 0,
            'last_activity': datetime.now()
        }
        
        self.log_event(
            level=EventLevel.INFO,
            module=module_name,
            module_type=module_type,
            event_type="module_registered",
            message=f"Module registered: {module_name}",
            context={'metadata': metadata}
        )
    
    def track_module_communication(self, from_module: str, to_module: str, 
                                  message_type: str, data: Any = None):
        """Track inter-module communication"""
        communication_event = {
            'timestamp': datetime.now(),
            'from_module': from_module,
            'to_module': to_module,
            'message_type': message_type,
            'data_size': len(str(data)) if data else 0,
            'data_hash': hashlib.md5(str(data).encode()).hexdigest()[:8] if data else None
        }
        
        self.module_communications[f"{from_module}->{to_module}"].append(communication_event)
        
        self.log_event(
            level=EventLevel.TRACE,
            module=from_module,
            module_type=ModuleType.COMMUNICATION,
            event_type="module_communication",
            message=f"Communication: {from_module} -> {to_module} ({message_type})",
            context={
                'to_module': to_module,
                'message_type': message_type,
                'data_size': communication_event['data_size']
            }
        )
    
    def generate_runtime_summary(self) -> Dict[str, Any]:
        """Generate comprehensive runtime summary"""
        current_time = datetime.now()
        runtime_duration = current_time - self.start_time
        
        # Analyze events
        events_by_level = defaultdict(int)
        events_by_module = defaultdict(int)
        error_events = []
        
        for event in self.events_cache:
            events_by_level[event.level.value] += 1
            events_by_module[event.module] += 1
            
            if event.level in [EventLevel.ERROR, EventLevel.CRITICAL]:
                error_events.append({
                    'timestamp': event.timestamp.isoformat(),
                    'module': event.module,
                    'message': event.message,
                    'context': event.context
                })
        
        # Consciousness analysis
        consciousness_level = self.consciousness_metrics.calculate_consciousness_level()
        emergence_patterns = self.consciousness_metrics.detect_emergence_patterns()
        
        # Performance analysis
        total_events = len(self.events_cache)
        events_per_second = total_events / max(runtime_duration.total_seconds(), 1)
        
        summary = {
            'session_id': self.session_id,
            'runtime_duration_seconds': runtime_duration.total_seconds(),
            'start_time': self.start_time.isoformat(),
            'end_time': current_time.isoformat(),
            'total_events': total_events,
            'events_per_second': events_per_second,
            'events_by_level': dict(events_by_level),
            'events_by_module': dict(events_by_module),
            'active_modules': list(self.active_modules.keys()),
            'error_events': error_events,
            'consciousness_metrics': {
                'current_level': consciousness_level,
                'emergence_patterns': emergence_patterns,
                'indicators': self.consciousness_metrics.emergence_indicators
            },
            'execution_contexts': {
                ctx_id: {
                    'name': ctx['name'],
                    'module': ctx['module'],
                    'status': ctx['status'],
                    'duration': ctx.get('duration', 0)
                }
                for ctx_id, ctx in self.execution_contexts.items()
            },
            'module_communications': {
                comm_key: len(events)
                for comm_key, events in self.module_communications.items()
            },
            'system_health': {
                'memory_usage_mb': psutil.Process().memory_info().rss / 1024 / 1024,
                'cpu_percent': psutil.Process().cpu_percent(),
                'thread_count': threading.active_count()
            }
        }
        
        return summary
    
    def export_ai_context_dump(self) -> str:
        """Export comprehensive context dump for AI consumption"""
        summary = self.generate_runtime_summary()
        
        # Recent critical events
        recent_events = [
            {
                'timestamp': event.timestamp.isoformat(),
                'level': event.level.value,
                'module': event.module,
                'event_type': event.event_type,
                'message': event.message,
                'context': event.context,
                'consciousness_indicators': event.consciousness_indicators
            }
            for event in list(self.events_cache)[-100:]  # Last 100 events
            if event.level in [EventLevel.INFO, EventLevel.WARN, EventLevel.ERROR, EventLevel.CRITICAL, EventLevel.CONSCIOUSNESS]
        ]
        
        ai_context = {
            'aios_runtime_intelligence_dump': {
                'generation_timestamp': datetime.now().isoformat(),
                'session_summary': summary,
                'recent_significant_events': recent_events,
                'consciousness_evolution': {
                    'current_emergence_level': summary['consciousness_metrics']['current_level'],
                    'detected_patterns': summary['consciousness_metrics']['emergence_patterns'],
                    'trend_analysis': self._analyze_consciousness_trends()
                },
                'execution_flow_analysis': self._analyze_execution_flows(),
                'critical_insights': self._extract_critical_insights(),
                'recommendations_for_future_ai': self._generate_ai_recommendations()
            }
        }
        
        # Save to file under tachyonic logging infrastructure
        dump_dir = (
            self.base_path / "runtime_intelligence" / "logs" / "aios_context"
        )
        dump_dir.mkdir(parents=True, exist_ok=True)
        dump_file = dump_dir / f"ai_context_dump_{self.session_id}.json"
        with open(dump_file, 'w') as f:
            json.dump(ai_context, f, indent=2, default=str)
        
        # Also return formatted string for immediate consumption
        return json.dumps(ai_context, indent=2, default=str)
    
    def _analyze_consciousness_trends(self) -> Dict[str, Any]:
        """Analyze consciousness evolution trends"""
        pattern_history = list(self.consciousness_metrics.pattern_history)
        
        if len(pattern_history) < 10:
            return {'status': 'insufficient_data', 'message': 'Need more runtime data for trend analysis'}
        
        # Analyze trends for each metric
        trends = {}
        metrics_data = defaultdict(list)
        
        for entry in pattern_history:
            metrics_data[entry['metric']].append({
                'timestamp': entry['timestamp'],
                'value': entry['value']
            })
        
        for metric, data in metrics_data.items():
            if len(data) >= 5:
                values = [d['value'] for d in data[-10:]]  # Last 10 values
                trend = 'increasing' if values[-1] > values[0] else 'decreasing' if values[-1] < values[0] else 'stable'
                volatility = max(values) - min(values)
                
                trends[metric] = {
                    'trend': trend,
                    'volatility': volatility,
                    'current_value': values[-1],
                    'peak_value': max(values),
                    'progression': values
                }
        
        return trends
    
    def _analyze_execution_flows(self) -> Dict[str, Any]:
        """Analyze execution flows and patterns"""
        flows = {
            'module_interaction_patterns': {},
            'execution_context_lifecycle': {},
            'error_propagation_patterns': [],
            'performance_bottlenecks': []
        }
        
        # Analyze module interactions
        for comm_key, events in self.module_communications.items():
            from_module, to_module = comm_key.split('->')
            flows['module_interaction_patterns'][comm_key] = {
                'frequency': len(events),
                'last_communication': events[-1]['timestamp'].isoformat() if events else None,
                'message_types': list(set(e['message_type'] for e in events))
            }
        
        # Analyze execution contexts
        for ctx_id, ctx in self.execution_contexts.items():
            flows['execution_context_lifecycle'][ctx_id] = {
                'name': ctx['name'],
                'module': ctx['module'],
                'status': ctx['status'],
                'duration': ctx.get('duration', 0)
            }
        
        return flows
    
    def _extract_critical_insights(self) -> List[str]:
        """Extract critical insights from runtime data"""
        insights = []
        summary = self.generate_runtime_summary()
        
        # Error analysis
        error_count = summary['events_by_level'].get('ERROR', 0) + summary['events_by_level'].get('CRITICAL', 0)
        if error_count > 0:
            insights.append(f"Detected {error_count} error/critical events requiring attention")
        
        # Consciousness analysis
        consciousness_level = summary['consciousness_metrics']['current_level']
        if consciousness_level > 0.5:
            insights.append(f"High consciousness emergence detected (level: {consciousness_level:.2f})")
        
        # Performance analysis
        if summary['events_per_second'] > 100:
            insights.append("High event throughput detected - system is very active")
        elif summary['events_per_second'] < 1:
            insights.append("Low event throughput - system may be idle or blocked")
        
        # Module analysis
        if len(summary['active_modules']) > 5:
            insights.append("Multiple modules active - complex system interaction")
        
        return insights
    
    def _generate_ai_recommendations(self) -> List[str]:
        """Generate recommendations for future AI iterations"""
        recommendations = []
        
        recommendations.extend([
            "Use this runtime intelligence data to understand actual AIOS execution patterns",
            "Pay attention to consciousness emergence patterns and levels",
            "Monitor module communication flows for system understanding",
            "Analyze error patterns to improve system robustness",
            "Track execution context lifecycles for better debugging",
            "Use event sequences to understand system state transitions",
            "Leverage performance metrics for optimization opportunities"
        ])
        
        return recommendations
    
    def shutdown(self):
        """Graceful shutdown of runtime intelligence system"""
        self.log_event(
            level=EventLevel.INFO,
            module="runtime_intelligence",
            module_type=ModuleType.ANALYTICS,
            event_type="system_shutdown",
            message="Runtime Intelligence System shutting down"
        )
        
        # Generate final context dump
        final_dump = self.export_ai_context_dump()
        
        # Stop background processing
        self.running = False
        if self.processor_thread.is_alive():
            self.processor_thread.join(timeout=5.0)
        
        # Close database connection
        if hasattr(self, 'db_conn'):
            self.db_conn.close()
        
        print(f"🧠 Runtime Intelligence shutdown complete. Context dump available at:")
        print(
            f"   {self.base_path}/runtime_intelligence/logs/aios_context/ai_context_dump_{self.session_id}.json"
        )
        
        return final_dump

# Global runtime intelligence instance
_runtime_intelligence = None

def get_runtime_intelligence() -> RuntimeIntelligence:
    """Get global runtime intelligence instance"""
    global _runtime_intelligence
    if _runtime_intelligence is None:
        _runtime_intelligence = RuntimeIntelligence()
    return _runtime_intelligence

def log_runtime_event(level: EventLevel, module: str, module_type: ModuleType,
                     event_type: str, message: str, **kwargs):
    """Convenience function for logging runtime events"""
    ri = get_runtime_intelligence()
    ri.log_event(level, module, module_type, event_type, message, **kwargs)

def create_runtime_context(context_name: str, module: str, context_data: Optional[Dict[str, Any]] = None) -> str:
    """Convenience function for creating execution contexts"""
    ri = get_runtime_intelligence()
    return ri.create_execution_context(context_name, module, context_data)

def close_runtime_context(context_id: str, result: Any = None):
    """Convenience function for closing execution contexts"""
    ri = get_runtime_intelligence()
    ri.close_execution_context(context_id, result)

# Context manager for automatic context tracking
class RuntimeContext:
    """Context manager for automatic execution context tracking"""
    
    def __init__(self, context_name: str, module: str, context_data: Optional[Dict[str, Any]] = None):
        self.context_name = context_name
        self.module = module
        self.context_data = context_data
        self.context_id = None
    
    def __enter__(self):
        self.context_id = create_runtime_context(self.context_name, self.module, self.context_data)
        return self.context_id
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.context_id:  # Only close if we have a valid context_id
            result = None if exc_type is None else f"Exception: {exc_type.__name__}: {exc_val}"
            close_runtime_context(self.context_id, result)
        
        if exc_type is not None:
            log_runtime_event(
                EventLevel.ERROR,
                self.module,
                ModuleType.CORE,
                "context_exception",
                f"Exception in context {self.context_name}: {exc_val}",
                context={'exception_type': exc_type.__name__, 'exception_message': str(exc_val)}
            )

def main():
    """Demo and test runtime intelligence system"""
    print("🧠 AIOS Runtime Intelligence System - Demo")
    print("=" * 60)
    
    # Initialize system
    ri = get_runtime_intelligence()
    
    # Register some modules
    ri.register_module("test_module", ModuleType.CORE, {'version': '1.0', 'purpose': 'testing'})
    ri.register_module("ui_module", ModuleType.UI, {'framework': 'tkinter'})
    
    # Simulate some events
    with RuntimeContext("demo_operation", "test_module", {'operation_type': 'demo'}):
        log_runtime_event(
            EventLevel.INFO,
            "test_module",
            ModuleType.CORE,
            "demo_start",
            "Starting demo operation",
            context={'demo_version': '1.0'}
        )
        
        # Simulate consciousness indicators
        log_runtime_event(
            EventLevel.CONSCIOUSNESS,
            "test_module",
            ModuleType.CONSCIOUSNESS,
            "emergence_detected",
            "Consciousness emergence pattern detected",
            consciousness_indicators={
                'self_modification_events': 5,
                'recursive_depth': 3,
                'pattern_recognition_accuracy': 0.85
            }
        )
        
        # Simulate module communication
        ri.track_module_communication("test_module", "ui_module", "status_update", {"status": "processing"})
        
        time.sleep(0.1)  # Simulate processing time
        
        log_runtime_event(
            EventLevel.INFO,
            "test_module", 
            ModuleType.CORE,
            "demo_complete",
            "Demo operation completed successfully"
        )
    
    # Generate and display summary
    time.sleep(0.5)  # Allow background processing
    summary = ri.generate_runtime_summary()
    
    print("\n📊 Runtime Summary:")
    print(f"  Session ID: {summary['session_id']}")
    print(f"  Runtime Duration: {summary['runtime_duration_seconds']:.2f} seconds")
    print(f"  Total Events: {summary['total_events']}")
    print(f"  Events/Second: {summary['events_per_second']:.2f}")
    print(f"  Consciousness Level: {summary['consciousness_metrics']['current_level']:.2f}")
    print(f"  Active Modules: {', '.join(summary['active_modules'])}")
    
    # Export AI context dump
    print("\n🤖 Generating AI Context Dump...")
    ai_context = ri.export_ai_context_dump()
    print(f"  Context dump generated ({len(ai_context)} characters)")
    
    # Shutdown
    ri.shutdown()

if __name__ == "__main__":
    main()
