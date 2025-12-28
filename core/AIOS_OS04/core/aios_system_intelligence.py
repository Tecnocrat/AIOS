"""
AIOS System Intelligence Mega-Module (OS0.4)
===========================================

This mega-module provides comprehensive system monitoring, runtime transparency,
performance analytics, and GPU-accelerated intelligence processing for AIOS.

Key Components:
- Real-time system monitoring with GPU acceleration
- Runtime transparency and process visualization
- Performance analytics and optimization
- Resource management and allocation
- System health diagnostics
- GPU-accelerated consciousness metrics
- Memory and CPU profiling
- Network and I/O monitoring
"""

import asyncio
import json
import logging
import os
import platform
import psutil
import sys
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Tuple, Union
import subprocess
import socket
import traceback
from collections import deque, defaultdict

# GPU acceleration imports (optional)
try:
    import torch
    GPU_AVAILABLE = torch.cuda.is_available()
    GPU_DEVICE = torch.device("cuda" if GPU_AVAILABLE else "cpu")
    GPU_NAME = torch.cuda.get_device_name(0) if GPU_AVAILABLE else "CPU"
    print(f"🎮 GPU Detection: {GPU_NAME} ({'ENABLED' if GPU_AVAILABLE else 'DISABLED'})")
except ImportError:
    GPU_AVAILABLE = False
    GPU_DEVICE = "cpu"
    GPU_NAME = "CPU"
    print("⚠️  PyTorch not available - GPU acceleration disabled")

# Advanced monitoring imports
try:
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    VISUALIZATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Visualization libraries not available: {e}")
    VISUALIZATION_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SystemMetrics:
    """Real-time system metrics data structure"""
    timestamp: datetime
    cpu_percent: float
    cpu_cores: int
    memory_total: int
    memory_used: int
    memory_percent: float
    disk_total: int
    disk_used: int
    disk_percent: float
    network_sent: int
    network_recv: int
    gpu_utilization: float = 0.0
    gpu_memory_used: int = 0
    gpu_memory_total: int = 0
    gpu_temperature: float = 0.0
    consciousness_load: float = 0.0
    evolution_activity: float = 0.0
    knowledge_processing: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ProcessMetrics:
    """Individual process monitoring data"""
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    memory_rss: int
    memory_vms: int
    status: str
    create_time: float
    num_threads: int
    connections: int = 0
    files_open: int = 0
    
class SystemIntelligenceConfig:
    """Configuration for system intelligence monitoring"""
    def __init__(self):
        self.monitoring_interval = 1.0  # seconds
        self.metrics_retention_hours = 24
        self.enable_gpu_monitoring = GPU_AVAILABLE
        self.enable_process_monitoring = True
        self.enable_network_monitoring = True
        self.enable_consciousness_metrics = True
        self.alert_cpu_threshold = 80.0
        self.alert_memory_threshold = 85.0
        self.alert_gpu_threshold = 90.0
        self.max_metrics_buffer = 86400  # 24 hours at 1-second intervals
        self.visualization_update_interval = 5.0
        self.gpu_optimization_enabled = GPU_AVAILABLE

class BaseSystemMonitor(ABC):
    """Abstract base class for system monitoring components"""
    
    def __init__(self, config: SystemIntelligenceConfig):
        self.config = config
        self.is_running = False
        self.metrics_buffer = deque(maxlen=config.max_metrics_buffer)
        self.subscribers = []
        
    @abstractmethod
    async def start_monitoring(self):
        """Start the monitoring process"""
        pass
        
    @abstractmethod
    async def stop_monitoring(self):
        """Stop the monitoring process"""
        pass
        
    @abstractmethod
    async def collect_metrics(self) -> Dict[str, Any]:
        """Collect current metrics"""
        pass
        
    def add_subscriber(self, callback: Callable):
        """Add a callback for metric updates"""
        self.subscribers.append(callback)
        
    async def notify_subscribers(self, metrics: Dict[str, Any]):
        """Notify all subscribers of new metrics"""
        for callback in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(metrics)
                else:
                    callback(metrics)
            except Exception as e:
                logger.error(f"Error notifying subscriber: {e}")

class GPUIntelligenceMonitor(BaseSystemMonitor):
    """GPU-accelerated system intelligence monitoring"""
    
    def __init__(self, config: SystemIntelligenceConfig):
        super().__init__(config)
        self.gpu_available = GPU_AVAILABLE
        self.gpu_device = GPU_DEVICE
        self.gpu_metrics_history = deque(maxlen=1000)
        self.consciousness_tensor = None
        self.optimization_kernels = {}
        
    async def start_monitoring(self):
        """Start GPU-accelerated monitoring"""
        self.is_running = True
        
        if self.gpu_available:
            await self._initialize_gpu_kernels()
            logger.info(f"🎮 GPU Intelligence Monitor started on {GPU_NAME}")
        else:
            logger.info("🖥️  CPU Intelligence Monitor started (GPU not available)")
            
    async def stop_monitoring(self):
        """Stop GPU monitoring"""
        self.is_running = False
        if self.gpu_available:
            await self._cleanup_gpu_resources()
        logger.info("🛑 GPU Intelligence Monitor stopped")
        
    async def _initialize_gpu_kernels(self):
        """Initialize GPU acceleration kernels"""
        try:
            if self.gpu_available:
                # Initialize consciousness processing tensor
                self.consciousness_tensor = torch.zeros(1000, 100, device=self.gpu_device)
                
                # Create optimization kernels for real-time processing
                self.optimization_kernels = {
                    'metric_processing': self._create_metric_kernel(),
                    'pattern_recognition': self._create_pattern_kernel(),
                    'anomaly_detection': self._create_anomaly_kernel()
                }
                
                logger.info("🚀 GPU kernels initialized successfully")
                
        except Exception as e:
            logger.error(f"❌ GPU kernel initialization failed: {e}")
            self.gpu_available = False
            
    def _create_metric_kernel(self):
        """Create GPU kernel for metric processing"""
        if not self.gpu_available:
            return None
            
        def process_metrics_gpu(metrics_tensor):
            # GPU-accelerated metric processing
            processed = torch.nn.functional.normalize(metrics_tensor, dim=1)
            return torch.mean(processed, dim=0)
            
        return process_metrics_gpu
        
    def _create_pattern_kernel(self):
        """Create GPU kernel for pattern recognition"""
        if not self.gpu_available:
            return None
            
        def recognize_patterns_gpu(data_tensor):
            # Simple pattern recognition using convolution
            kernel = torch.ones(3, device=self.gpu_device) / 3
            return torch.nn.functional.conv1d(
                data_tensor.unsqueeze(0).unsqueeze(0), 
                kernel.unsqueeze(0).unsqueeze(0)
            ).squeeze()
            
        return recognize_patterns_gpu
        
    def _create_anomaly_kernel(self):
        """Create GPU kernel for anomaly detection"""
        if not self.gpu_available:
            return None
            
        def detect_anomalies_gpu(metrics_tensor, threshold=2.0):
            mean_val = torch.mean(metrics_tensor)
            std_val = torch.std(metrics_tensor)
            anomalies = torch.abs(metrics_tensor - mean_val) > (threshold * std_val)
            return anomalies
            
        return detect_anomalies_gpu
        
    async def collect_metrics(self) -> Dict[str, Any]:
        """Collect GPU-accelerated system metrics"""
        try:
            # Basic system metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            # GPU metrics
            gpu_metrics = await self._collect_gpu_metrics()
            
            # Create metrics object
            metrics = SystemMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                cpu_cores=psutil.cpu_count(),
                memory_total=memory.total,
                memory_used=memory.used,
                memory_percent=memory.percent,
                disk_total=disk.total,
                disk_used=disk.used,
                disk_percent=disk.percent,
                network_sent=network.bytes_sent,
                network_recv=network.bytes_recv,
                **gpu_metrics
            )
            
            # GPU-accelerated processing
            if self.gpu_available and self.optimization_kernels:
                metrics = await self._process_metrics_gpu(metrics)
                
            # Store in buffer
            self.metrics_buffer.append(metrics)
            
            return metrics.to_dict()
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return {}
            
    async def _collect_gpu_metrics(self) -> Dict[str, float]:
        """Collect GPU-specific metrics"""
        gpu_metrics = {
            'gpu_utilization': 0.0,
            'gpu_memory_used': 0,
            'gpu_memory_total': 0,
            'gpu_temperature': 0.0
        }
        
        if self.gpu_available:
            try:
                # PyTorch GPU metrics
                gpu_memory_used = torch.cuda.memory_allocated(0)
                gpu_memory_total = torch.cuda.max_memory_allocated(0)
                
                gpu_metrics.update({
                    'gpu_memory_used': gpu_memory_used,
                    'gpu_memory_total': gpu_memory_total,
                    'gpu_utilization': (gpu_memory_used / max(gpu_memory_total, 1)) * 100
                })
                
                # Try to get temperature (platform dependent)
                try:
                    import pynvml
                    pynvml.nvmlInit()
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                    gpu_metrics['gpu_temperature'] = temp
                except:
                    pass  # Temperature monitoring not available
                    
            except Exception as e:
                logger.debug(f"GPU metrics collection failed: {e}")
                
        return gpu_metrics
        
    async def _process_metrics_gpu(self, metrics: SystemMetrics) -> SystemMetrics:
        """Process metrics using GPU acceleration"""
        try:
            if not self.gpu_available:
                return metrics
                
            # Convert metrics to tensor for GPU processing
            metric_values = torch.tensor([
                metrics.cpu_percent,
                metrics.memory_percent,
                metrics.disk_percent,
                metrics.gpu_utilization
            ], device=self.gpu_device, dtype=torch.float32)
            
            # Apply GPU-accelerated processing
            if 'metric_processing' in self.optimization_kernels:
                processed = self.optimization_kernels['metric_processing'](metric_values.unsqueeze(0))
                
                # Update consciousness load based on processed metrics
                metrics.consciousness_load = float(processed[0].cpu()) * 100
                
            return metrics
            
        except Exception as e:
            logger.error(f"GPU metrics processing failed: {e}")
            return metrics
            
    async def _cleanup_gpu_resources(self):
        """Cleanup GPU resources"""
        try:
            if self.gpu_available:
                torch.cuda.empty_cache()
                self.consciousness_tensor = None
                self.optimization_kernels = {}
                logger.info("🧹 GPU resources cleaned up")
        except Exception as e:
            logger.error(f"GPU cleanup error: {e}")

class ProcessIntelligenceMonitor(BaseSystemMonitor):
    """Advanced process monitoring and intelligence"""
    
    def __init__(self, config: SystemIntelligenceConfig):
        super().__init__(config)
        self.process_history = defaultdict(list)
        self.aios_processes = {}
        self.consciousness_processes = []
        
    async def start_monitoring(self):
        """Start process monitoring"""
        self.is_running = True
        logger.info("🔍 Process Intelligence Monitor started")
        
    async def stop_monitoring(self):
        """Stop process monitoring"""
        self.is_running = False
        logger.info("🛑 Process Intelligence Monitor stopped")
        
    async def collect_metrics(self) -> Dict[str, Any]:
        """Collect process metrics"""
        try:
            processes = []
            aios_activity = 0.0
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    
                    # Detailed process metrics
                    process_metrics = ProcessMetrics(
                        pid=pinfo['pid'],
                        name=pinfo['name'],
                        cpu_percent=pinfo['cpu_percent'] or 0.0,
                        memory_percent=pinfo['memory_percent'] or 0.0,
                        memory_rss=proc.memory_info().rss,
                        memory_vms=proc.memory_info().vms,
                        status=proc.status(),
                        create_time=proc.create_time(),
                        num_threads=proc.num_threads()
                    )
                    
                    # Track AIOS-related processes
                    if any(keyword in pinfo['name'].lower() for keyword in 
                           ['python', 'aios', 'consciousness', 'evolution']):
                        self.aios_processes[pinfo['pid']] = process_metrics
                        aios_activity += pinfo['cpu_percent'] or 0.0
                        
                    processes.append(process_metrics)
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            return {
                'processes': [proc.__dict__ for proc in processes[:20]],  # Top 20
                'aios_processes': len(self.aios_processes),
                'aios_cpu_activity': aios_activity,
                'total_processes': len(processes)
            }
            
        except Exception as e:
            logger.error(f"Error collecting process metrics: {e}")
            return {}

class ConsciousnessIntelligenceMonitor(BaseSystemMonitor):
    """Consciousness-specific monitoring and analytics"""
    
    def __init__(self, config: SystemIntelligenceConfig):
        super().__init__(config)
        self.consciousness_states = deque(maxlen=1000)
        self.evolution_metrics = deque(maxlen=1000)
        self.knowledge_metrics = deque(maxlen=1000)
        self.emergence_patterns = []
        
    async def start_monitoring(self):
        """Start consciousness monitoring"""
        self.is_running = True
        logger.info("🧠 Consciousness Intelligence Monitor started")
        
    async def stop_monitoring(self):
        """Stop consciousness monitoring"""
        self.is_running = False
        logger.info("🛑 Consciousness Intelligence Monitor stopped")
        
    async def collect_metrics(self) -> Dict[str, Any]:
        """Collect consciousness-specific metrics"""
        try:
            # Simulate consciousness metrics (would integrate with actual modules)
            consciousness_metrics = {
                'consciousness_level': self._calculate_consciousness_level(),
                'coherence_index': self._calculate_coherence_index(),
                'emergence_patterns': len(self.emergence_patterns),
                'evolution_activity': self._calculate_evolution_activity(),
                'knowledge_processing_rate': self._calculate_knowledge_rate(),
                'neural_connectivity': self._calculate_neural_connectivity()
            }
            
            self.consciousness_states.append(consciousness_metrics)
            
            return consciousness_metrics
            
        except Exception as e:
            logger.error(f"Error collecting consciousness metrics: {e}")
            return {}
            
    def _calculate_consciousness_level(self) -> float:
        """Calculate current consciousness level"""
        # This would integrate with actual consciousness engine
        base_level = 0.7
        variance = 0.1 * (time.time() % 10) / 10
        return min(1.0, base_level + variance)
        
    def _calculate_coherence_index(self) -> float:
        """Calculate consciousness coherence index"""
        # This would measure actual coherence between modules
        if len(self.consciousness_states) < 2:
            return 0.5
            
        recent_states = list(self.consciousness_states)[-10:]
        levels = [state['consciousness_level'] for state in recent_states if 'consciousness_level' in state]
        
        if len(levels) < 2:
            return 0.5
            
        # Calculate stability as coherence measure
        variance = np.var(levels) if len(levels) > 1 else 0
        return max(0.0, 1.0 - variance)
        
    def _calculate_evolution_activity(self) -> float:
        """Calculate evolution engine activity"""
        # This would measure actual evolution processes
        return 0.6 + 0.2 * (time.time() % 5) / 5
        
    def _calculate_knowledge_rate(self) -> float:
        """Calculate knowledge processing rate"""
        # This would measure actual knowledge distillation
        return 0.8 + 0.15 * (time.time() % 7) / 7
        
    def _calculate_neural_connectivity(self) -> float:
        """Calculate neural network connectivity"""
        # This would measure actual neural connections
        return 0.75 + 0.2 * (time.time() % 3) / 3

class SystemIntelligenceManager:
    """Main manager for all system intelligence monitoring"""
    
    def __init__(self, config: Optional[SystemIntelligenceConfig] = None):
        self.config = config or SystemIntelligenceConfig()
        self.is_running = False
        
        # Initialize monitors
        self.gpu_monitor = GPUIntelligenceMonitor(self.config)
        self.process_monitor = ProcessIntelligenceMonitor(self.config)
        self.consciousness_monitor = ConsciousnessIntelligenceMonitor(self.config)
        
        # Data aggregation
        self.unified_metrics = deque(maxlen=self.config.max_metrics_buffer)
        self.alert_history = deque(maxlen=1000)
        self.monitoring_tasks = []
        
        # Integration with other mega-modules
        self.consciousness_module = None
        self.evolution_module = None
        self.visual_interface = None
        
    async def initialize(self):
        """Initialize the system intelligence manager"""
        try:
            logger.info("🚀 Initializing AIOS System Intelligence Manager...")
            
            # Initialize all monitors
            await self.gpu_monitor.start_monitoring()
            await self.process_monitor.start_monitoring()
            await self.consciousness_monitor.start_monitoring()
            
            # Setup data aggregation
            await self._setup_data_aggregation()
            
            logger.info("✅ AIOS System Intelligence Manager initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing system intelligence manager: {e}")
            raise
            
    async def start(self):
        """Start all monitoring systems"""
        try:
            self.is_running = True
            logger.info("🎯 Starting AIOS System Intelligence Manager...")
            
            # Start monitoring loops
            self.monitoring_tasks.extend([
                asyncio.create_task(self._unified_monitoring_loop()),
                asyncio.create_task(self._alert_monitoring_loop()),
                asyncio.create_task(self._optimization_loop())
            ])
            
            logger.info("✅ AIOS System Intelligence Manager started successfully")
            
            # Print startup status
            await self._print_startup_status()
            
        except Exception as e:
            logger.error(f"❌ Error starting system intelligence manager: {e}")
            raise
            
    async def stop(self):
        """Stop all monitoring systems"""
        try:
            self.is_running = False
            logger.info("🛑 Stopping AIOS System Intelligence Manager...")
            
            # Cancel monitoring tasks
            for task in self.monitoring_tasks:
                task.cancel()
                
            # Stop all monitors
            await self.gpu_monitor.stop_monitoring()
            await self.process_monitor.stop_monitoring()
            await self.consciousness_monitor.stop_monitoring()
            
            logger.info("✅ AIOS System Intelligence Manager stopped")
            
        except Exception as e:
            logger.error(f"❌ Error stopping system intelligence manager: {e}")
            
    async def _setup_data_aggregation(self):
        """Setup data aggregation between monitors"""
        
        # Connect monitors to unified data collection
        self.gpu_monitor.add_subscriber(self._aggregate_gpu_metrics)
        self.process_monitor.add_subscriber(self._aggregate_process_metrics)
        self.consciousness_monitor.add_subscriber(self._aggregate_consciousness_metrics)
        
    async def _aggregate_gpu_metrics(self, metrics: Dict[str, Any]):
        """Aggregate GPU metrics into unified view"""
        unified_entry = {
            'timestamp': datetime.now(),
            'source': 'gpu_monitor',
            'metrics': metrics
        }
        self.unified_metrics.append(unified_entry)
        
    async def _aggregate_process_metrics(self, metrics: Dict[str, Any]):
        """Aggregate process metrics into unified view"""
        unified_entry = {
            'timestamp': datetime.now(),
            'source': 'process_monitor',
            'metrics': metrics
        }
        self.unified_metrics.append(unified_entry)
        
    async def _aggregate_consciousness_metrics(self, metrics: Dict[str, Any]):
        """Aggregate consciousness metrics into unified view"""
        unified_entry = {
            'timestamp': datetime.now(),
            'source': 'consciousness_monitor',
            'metrics': metrics
        }
        self.unified_metrics.append(unified_entry)
        
    async def _unified_monitoring_loop(self):
        """Main unified monitoring loop"""
        while self.is_running:
            try:
                # Collect metrics from all monitors
                gpu_metrics = await self.gpu_monitor.collect_metrics()
                process_metrics = await self.process_monitor.collect_metrics()
                consciousness_metrics = await self.consciousness_monitor.collect_metrics()
                
                # Create unified metrics
                unified = {
                    'timestamp': datetime.now().isoformat(),
                    'gpu': gpu_metrics,
                    'processes': process_metrics,
                    'consciousness': consciousness_metrics,
                    'system_health': self._calculate_system_health(gpu_metrics, process_metrics)
                }
                
                # Store unified metrics
                self.unified_metrics.append(unified)
                
                # Send to visual interface if available
                if self.visual_interface:
                    await self._send_to_visual_interface(unified)
                    
                await asyncio.sleep(self.config.monitoring_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in unified monitoring loop: {e}")
                await asyncio.sleep(self.config.monitoring_interval)
                
    async def _alert_monitoring_loop(self):
        """Monitor for system alerts and anomalies"""
        while self.is_running:
            try:
                if len(self.unified_metrics) > 0:
                    latest = self.unified_metrics[-1]
                    alerts = self._check_for_alerts(latest)
                    
                    for alert in alerts:
                        await self._handle_alert(alert)
                        
                await asyncio.sleep(self.config.monitoring_interval * 5)  # Check every 5 intervals
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in alert monitoring loop: {e}")
                await asyncio.sleep(self.config.monitoring_interval)
                
    async def _optimization_loop(self):
        """Continuous system optimization loop"""
        while self.is_running:
            try:
                if self.config.gpu_optimization_enabled and GPU_AVAILABLE:
                    await self._run_gpu_optimizations()
                    
                await self._optimize_memory_usage()
                await self._optimize_process_priorities()
                
                await asyncio.sleep(30)  # Run optimizations every 30 seconds
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in optimization loop: {e}")
                await asyncio.sleep(30)
                
    def _calculate_system_health(self, gpu_metrics: Dict, process_metrics: Dict) -> Dict[str, Any]:
        """Calculate overall system health score"""
        health_score = 100.0
        
        # CPU health
        if 'cpu_percent' in gpu_metrics:
            cpu_usage = gpu_metrics['cpu_percent']
            if cpu_usage > 80:
                health_score -= (cpu_usage - 80) * 2
                
        # Memory health
        if 'memory_percent' in gpu_metrics:
            memory_usage = gpu_metrics['memory_percent']
            if memory_usage > 85:
                health_score -= (memory_usage - 85) * 3
                
        # GPU health
        if 'gpu_utilization' in gpu_metrics:
            gpu_usage = gpu_metrics['gpu_utilization']
            if gpu_usage > 90:
                health_score -= (gpu_usage - 90) * 2
                
        return {
            'health_score': max(0, min(100, health_score)),
            'status': 'healthy' if health_score > 75 else 'warning' if health_score > 50 else 'critical'
        }
        
    def _check_for_alerts(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for system alerts"""
        alerts = []
        
        gpu_metrics = metrics.get('gpu', {})
        
        # CPU alert
        if gpu_metrics.get('cpu_percent', 0) > self.config.alert_cpu_threshold:
            alerts.append({
                'type': 'cpu_high',
                'severity': 'warning',
                'message': f"High CPU usage: {gpu_metrics['cpu_percent']:.1f}%",
                'timestamp': datetime.now()
            })
            
        # Memory alert
        if gpu_metrics.get('memory_percent', 0) > self.config.alert_memory_threshold:
            alerts.append({
                'type': 'memory_high',
                'severity': 'warning',
                'message': f"High memory usage: {gpu_metrics['memory_percent']:.1f}%",
                'timestamp': datetime.now()
            })
            
        # GPU alert
        if gpu_metrics.get('gpu_utilization', 0) > self.config.alert_gpu_threshold:
            alerts.append({
                'type': 'gpu_high',
                'severity': 'critical',
                'message': f"High GPU usage: {gpu_metrics['gpu_utilization']:.1f}%",
                'timestamp': datetime.now()
            })
            
        return alerts
        
    async def _handle_alert(self, alert: Dict[str, Any]):
        """Handle system alert"""
        self.alert_history.append(alert)
        logger.warning(f"🚨 ALERT: {alert['message']}")
        
        # Send to visual interface if available
        if self.visual_interface:
            await self.visual_interface.send_alert(alert)
            
    async def _run_gpu_optimizations(self):
        """Run GPU optimization routines"""
        try:
            if GPU_AVAILABLE:
                # Clear GPU cache periodically
                torch.cuda.empty_cache()
                
                # Optimize GPU memory allocation
                if hasattr(torch.cuda, 'optimize'):
                    torch.cuda.optimize()
                    
        except Exception as e:
            logger.debug(f"GPU optimization error: {e}")
            
    async def _optimize_memory_usage(self):
        """Optimize system memory usage"""
        try:
            # Force garbage collection
            import gc
            gc.collect()
            
            # Trim metrics buffers if too large
            if len(self.unified_metrics) > self.config.max_metrics_buffer * 0.9:
                # Remove older entries
                while len(self.unified_metrics) > self.config.max_metrics_buffer * 0.8:
                    self.unified_metrics.popleft()
                    
        except Exception as e:
            logger.debug(f"Memory optimization error: {e}")
            
    async def _optimize_process_priorities(self):
        """Optimize AIOS process priorities"""
        try:
            # This would adjust process priorities for AIOS components
            current_process = psutil.Process()
            
            # Set higher priority for AIOS processes
            if platform.system() == "Windows":
                current_process.nice(psutil.HIGH_PRIORITY_CLASS)
            else:
                current_process.nice(-5)  # Higher priority on Unix
                
        except Exception as e:
            logger.debug(f"Process optimization error: {e}")
            
    async def _send_to_visual_interface(self, metrics: Dict[str, Any]):
        """Send metrics to visual interface"""
        try:
            if self.visual_interface and hasattr(self.visual_interface, 'update_system_metrics'):
                await self.visual_interface.update_system_metrics(metrics)
        except Exception as e:
            logger.debug(f"Visual interface update error: {e}")
            
    async def _print_startup_status(self):
        """Print comprehensive startup status"""
        try:
            print("\n" + "="*60)
            print("🧠 AIOS SYSTEM INTELLIGENCE MANAGER - STATUS")
            print("="*60)
            print(f"🎮 GPU Acceleration: {'✅ ENABLED' if GPU_AVAILABLE else '❌ DISABLED'}")
            print(f"🖥️  GPU Device: {GPU_NAME}")
            print(f"🔍 Process Monitoring: ✅ ENABLED")
            print(f"🧠 Consciousness Monitoring: ✅ ENABLED")
            print(f"⚡ Monitoring Interval: {self.config.monitoring_interval}s")
            print(f"📊 Metrics Buffer: {self.config.max_metrics_buffer} entries")
            print(f"🚨 Alert Thresholds: CPU {self.config.alert_cpu_threshold}%, Memory {self.config.alert_memory_threshold}%, GPU {self.config.alert_gpu_threshold}%")
            
            # Current system snapshot
            if len(self.unified_metrics) > 0:
                latest = self.unified_metrics[-1]
                gpu_metrics = latest.get('gpu', {})
                print(f"\n📈 CURRENT SYSTEM STATE:")
                print(f"   CPU: {gpu_metrics.get('cpu_percent', 0):.1f}%")
                print(f"   Memory: {gpu_metrics.get('memory_percent', 0):.1f}%")
                print(f"   GPU: {gpu_metrics.get('gpu_utilization', 0):.1f}%")
                
            print("="*60)
            print("🚀 SYSTEM INTELLIGENCE MANAGER READY")
            print("="*60 + "\n")
            
        except Exception as e:
            logger.error(f"Error printing startup status: {e}")
            
    # Public API methods
    async def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        if len(self.unified_metrics) > 0:
            return self.unified_metrics[-1]
        return {}
        
    async def get_metrics_history(self, hours: int = 1) -> List[Dict[str, Any]]:
        """Get metrics history for specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        history = []
        for metrics in self.unified_metrics:
            if metrics.get('timestamp'):
                timestamp = datetime.fromisoformat(metrics['timestamp'])
                if timestamp >= cutoff_time:
                    history.append(metrics)
                    
        return history
        
    async def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health"""
        if len(self.unified_metrics) > 0:
            latest = self.unified_metrics[-1]
            return latest.get('system_health', {'health_score': 0, 'status': 'unknown'})
        return {'health_score': 0, 'status': 'unknown'}
        
    async def get_alert_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get alert history"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_alerts = []
        for alert in self.alert_history:
            if alert.get('timestamp') and alert['timestamp'] >= cutoff_time:
                recent_alerts.append(alert)
                
        return recent_alerts
        
    # Integration methods
    def integrate_consciousness_module(self, module):
        """Integrate with consciousness mega-module"""
        self.consciousness_module = module
        logger.info("🧠 Consciousness module integrated with system intelligence")
        
    def integrate_evolution_module(self, module):
        """Integrate with evolution mega-module"""
        self.evolution_module = module
        logger.info("🧬 Evolution module integrated with system intelligence")
        
    def integrate_visual_interface(self, module):
        """Integrate with visual interface mega-module"""
        self.visual_interface = module
        logger.info("🖥️  Visual interface integrated with system intelligence")

# Utility functions for system intelligence
def get_system_info() -> Dict[str, Any]:
    """Get comprehensive system information"""
    try:
        return {
            'platform': platform.platform(),
            'processor': platform.processor(),
            'architecture': platform.architecture(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'disk_total': psutil.disk_usage('/').total,
            'gpu_available': GPU_AVAILABLE,
            'gpu_name': GPU_NAME,
            'pytorch_version': torch.__version__ if GPU_AVAILABLE else 'Not available'
        }
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return {}

def create_performance_benchmark() -> Dict[str, Any]:
    """Create a performance benchmark"""
    try:
        import time
        
        benchmark = {
            'timestamp': datetime.now().isoformat(),
            'cpu_benchmark': None,
            'memory_benchmark': None,
            'gpu_benchmark': None
        }
        
        # CPU benchmark
        start_time = time.time()
        result = sum(i**2 for i in range(100000))
        cpu_time = time.time() - start_time
        benchmark['cpu_benchmark'] = {
            'time_seconds': cpu_time,
            'operations_per_second': 100000 / cpu_time
        }
        
        # Memory benchmark
        start_time = time.time()
        large_list = [i for i in range(1000000)]
        memory_time = time.time() - start_time
        benchmark['memory_benchmark'] = {
            'time_seconds': memory_time,
            'memory_used_mb': len(large_list) * 28 / (1024 * 1024)  # Approximate
        }
        
        # GPU benchmark
        if GPU_AVAILABLE:
            start_time = time.time()
            tensor = torch.randn(1000, 1000, device=GPU_DEVICE)
            result = torch.matmul(tensor, tensor)
            torch.cuda.synchronize()
            gpu_time = time.time() - start_time
            
            benchmark['gpu_benchmark'] = {
                'time_seconds': gpu_time,
                'operations_per_second': 1000000 / gpu_time
            }
            
        return benchmark
        
    except Exception as e:
        logger.error(f"Error creating performance benchmark: {e}")
        return {}

# Demo and test functions
async def run_system_intelligence_demo():
    """Run a comprehensive demo of the system intelligence"""
    print("🧠 Starting AIOS System Intelligence Demo...")
    
    try:
        # Create configuration
        config = SystemIntelligenceConfig()
        config.monitoring_interval = 2.0  # Faster for demo
        
        # Create and initialize manager
        manager = SystemIntelligenceManager(config)
        await manager.initialize()
        
        print("🚀 Starting system intelligence monitoring...")
        await manager.start()
        
        # Print system information
        system_info = get_system_info()
        print(f"\n📊 System Information:")
        for key, value in system_info.items():
            print(f"   {key}: {value}")
            
        # Run performance benchmark
        print(f"\n⚡ Running performance benchmark...")
        benchmark = create_performance_benchmark()
        for key, value in benchmark.items():
            if value:
                print(f"   {key}: {value}")
                
        # Monitor for demo duration
        print(f"\n🎯 Monitoring system for 30 seconds...")
        for i in range(15):
            metrics = await manager.get_current_metrics()
            health = await manager.get_system_health()
            
            print(f"   Iteration {i+1}: Health={health.get('health_score', 0):.1f}% ({health.get('status', 'unknown')})")
            
            await asyncio.sleep(2)
            
        # Show final statistics
        history = await manager.get_metrics_history(1)
        alerts = await manager.get_alert_history(1)
        
        print(f"\n📈 Demo Results:")
        print(f"   Metrics collected: {len(history)}")
        print(f"   Alerts generated: {len(alerts)}")
        print(f"   GPU acceleration: {'✅ Active' if GPU_AVAILABLE else '❌ Inactive'}")
        
        print("\n✅ Demo completed successfully!")
        print("Press Ctrl+C to stop the system intelligence...")
        
        # Keep running until interrupted
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping system intelligence...")
            await manager.stop()
            print("✅ System intelligence stopped")
            
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        raise

def validate_system_intelligence():
    """Validate the system intelligence mega-module"""
    print("🔍 Validating AIOS System Intelligence Mega-Module...")
    
    validation_results = {
        'gpu_available': GPU_AVAILABLE,
        'pytorch_available': False,
        'psutil_available': False,
        'classes_valid': {},
        'functions_valid': {}
    }
    
    # Check dependencies
    try:
        import torch
        validation_results['pytorch_available'] = True
    except ImportError:
        pass
        
    try:
        import psutil
        validation_results['psutil_available'] = True
    except ImportError:
        pass
        
    # Check classes
    try:
        config = SystemIntelligenceConfig()
        validation_results['classes_valid']['SystemIntelligenceConfig'] = True
        
        gpu_monitor = GPUIntelligenceMonitor(config)
        validation_results['classes_valid']['GPUIntelligenceMonitor'] = True
        
        process_monitor = ProcessIntelligenceMonitor(config)
        validation_results['classes_valid']['ProcessIntelligenceMonitor'] = True
        
        consciousness_monitor = ConsciousnessIntelligenceMonitor(config)
        validation_results['classes_valid']['ConsciousnessIntelligenceMonitor'] = True
        
        manager = SystemIntelligenceManager(config)
        validation_results['classes_valid']['SystemIntelligenceManager'] = True
        
    except Exception as e:
        validation_results['classes_valid']['error'] = str(e)
        
    # Check utility functions
    try:
        system_info = get_system_info()
        validation_results['functions_valid']['get_system_info'] = len(system_info) > 0
        
        benchmark = create_performance_benchmark()
        validation_results['functions_valid']['create_performance_benchmark'] = len(benchmark) > 0
        
    except Exception as e:
        validation_results['functions_valid']['error'] = str(e)
        
    # Print results
    print(f"🎮 GPU Available: {'✅' if validation_results['gpu_available'] else '❌'}")
    print(f"🐍 PyTorch Available: {'✅' if validation_results['pytorch_available'] else '❌'}")
    print(f"📊 PSUtil Available: {'✅' if validation_results['psutil_available'] else '❌'}")
    print(f"🏗️  Classes: {len([k for k, v in validation_results['classes_valid'].items() if v is True])} validated")
    print(f"🔧 Functions: {len([k for k, v in validation_results['functions_valid'].items() if v is True])} validated")
    
    all_good = (
        validation_results['pytorch_available'] and
        validation_results['psutil_available'] and
        all(v is True for v in validation_results['classes_valid'].values()) and
        all(v is True for v in validation_results['functions_valid'].values())
    )
    
    if all_good:
        print("✅ AIOS System Intelligence Mega-Module validation PASSED")
    else:
        print("⚠️  AIOS System Intelligence Mega-Module validation completed with warnings")
        
    return validation_results

# Main execution
if __name__ == "__main__":
    print("🧠 AIOS System Intelligence Mega-Module (OS0.4)")
    print("=" * 60)
    
    # Validate module
    validation_results = validate_system_intelligence()
    
    # Ask user if they want to run demo
    try:
        response = input(f"\n🎯 Run system intelligence demo? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            asyncio.run(run_system_intelligence_demo())
        else:
            print("✅ Module validation completed. Use import to integrate with other modules.")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
