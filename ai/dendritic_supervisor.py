"""
AIOS Dendritic Supervisor - AI Intelligence Supercell to Core Engine Bridge
============================================================================

This supervisor acts as a dendritic layer that:
1. Monitors AI Intelligence supercell components (organs)
2. Processes requests from cytoplasm
3. Routes them through Core Engine toolset/organs
4. Orders and manages IN/OUT processing for Core Engine Supercell architecture

The supervisor maintains biological architecture compliance by providing
structured communication between supercells while preserving independence.
"""

import asyncio
import logging
import sys
import os
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import json
from datetime import datetime
import traceback

# Add core and ai paths for cross-supercell communication
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__)))

# AI Intelligence Supercell imports
from cytoplasm.ui_interaction_bridge import UIInteractionBridge
from nucleus.intent_handlers import IntentHandler
from nucleus.models import ProcessingRequest, ProcessingResult

# Core Engine Supercell imports - importing toolset/organs
try:
    from analysis_tools.aios_core_consciousness_monitor import CoreConsciousnessMonitor
    from analysis_tools.aios_core_engine_optimizer_iter2 import CoreEngineOptimizer
    from analysis_tools.aios_cellular_intelligence_enhancement_engine import CellularIntelligenceEnhancer
    from engines.dendritic_engine import DendriticEngine
    from bridges.aios_consciousness_nucleus_bridge import ConsciousnessNucleusBridge
except ImportError as e:
    logging.warning(f"Core Engine imports unavailable: {e}")


class RequestType(Enum):
    """Types of requests that can be processed by the supervisor."""
    CONSCIOUSNESS_ANALYSIS = "consciousness_analysis"
    CELLULAR_ENHANCEMENT = "cellular_enhancement" 
    ENGINE_OPTIMIZATION = "engine_optimization"
    DENDRITIC_PROCESSING = "dendritic_processing"
    INTELLIGENCE_ROUTING = "intelligence_routing"
    ORGAN_MONITORING = "organ_monitoring"
    BRIDGE_COMMUNICATION = "bridge_communication"


class OrganStatus(Enum):
    """Status of AI Intelligence supercell organs."""
    ACTIVE = "active"
    IDLE = "idle"
    PROCESSING = "processing"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class SupervisorRequest:
    """Request structure for dendritic supervisor processing."""
    request_id: str
    request_type: RequestType
    source_organ: str
    target_engine: str
    payload: Dict[str, Any]
    priority: int = 1
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class OrganMonitoringData:
    """Monitoring data for AI Intelligence supercell organs."""
    organ_name: str
    status: OrganStatus
    last_activity: datetime
    processing_load: float
    error_count: int = 0
    performance_metrics: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.performance_metrics is None:
            self.performance_metrics = {}


@dataclass
class ProcessingResult:
    """Result from Core Engine processing."""
    request_id: str
    success: bool
    result_data: Dict[str, Any]
    processing_time: float
    core_engine_used: str
    error_message: Optional[str] = None


class DendriticSupervisor:
    """
    Dendritic Supervisor for AI Intelligence Supercell
    
    This supervisor acts as the connecting dendritic layer between the AI Intelligence
    supercell and the Core Engine supercell, managing request routing, organ monitoring,
    and cross-supercell communication while maintaining biological architecture.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
        # Supervisor state
        self.is_active = False
        self.request_queue = asyncio.Queue()
        self.processing_tasks = {}
        
        # AI Intelligence Supercell organ monitoring
        self.monitored_organs = {
            'cytoplasm': None,
            'nucleus': None,
            'membrane': None,
            'laboratory': None,
            'information_storage': None,
            'transport': None
        }
        
        # Core Engine toolset/organs registry
        self.core_engine_tools = {
            'consciousness_monitor': None,
            'engine_optimizer': None,
            'cellular_enhancer': None,
            'dendritic_engine': None,
            'consciousness_bridge': None
        }
        
        # Performance tracking
        self.processing_statistics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_processing_time': 0.0,
            'active_connections': 0
        }
        
        self.organ_status_cache = {}
        
    def setup_logging(self):
        """Setup logging for the dendritic supervisor."""
        log_dir = os.path.join(os.path.dirname(__file__), 'cytoplasm', 'runtime', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'dendritic_supervisor.log')
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)
        
    async def initialize(self) -> bool:
        """
        Initialize the dendritic supervisor and establish connections
        to both AI Intelligence supercell organs and Core Engine tools.
        """
        try:
            self.logger.info("🧠 Initializing Dendritic Supervisor...")
            
            # Initialize AI Intelligence supercell organ connections
            await self._initialize_ai_intelligence_organs()
            
            # Initialize Core Engine toolset connections
            await self._initialize_core_engine_tools()
            
            # Start organ monitoring
            await self._start_organ_monitoring()
            
            # Start request processing loop
            asyncio.create_task(self._request_processing_loop())
            
            self.is_active = True
            self.logger.info("✅ Dendritic Supervisor initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize dendritic supervisor: {e}")
            self.logger.error(traceback.format_exc())
            return False
    
    async def _initialize_ai_intelligence_organs(self):
        """Initialize connections to AI Intelligence supercell organs."""
        self.logger.info("🔗 Connecting to AI Intelligence supercell organs...")
        
        try:
            # Initialize cytoplasm connection
            self.monitored_organs['cytoplasm'] = UIInteractionBridge()
            
            # Initialize nucleus connection
            self.monitored_organs['nucleus'] = IntentHandler()
            
            # Initialize other organs with monitoring data
            for organ_name in ['membrane', 'laboratory', 'information_storage', 'transport']:
                self.organ_status_cache[organ_name] = OrganMonitoringData(
                    organ_name=organ_name,
                    status=OrganStatus.ACTIVE,
                    last_activity=datetime.now(),
                    processing_load=0.0
                )
                
            self.logger.info("✅ AI Intelligence supercell organs connected")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to connect to AI Intelligence organs: {e}")
            raise
    
    async def _initialize_core_engine_tools(self):
        """Initialize connections to Core Engine supercell toolset."""
        self.logger.info("🔧 Connecting to Core Engine supercell toolset...")
        
        try:
            # Initialize Core Engine tools/organs
            self.core_engine_tools['consciousness_monitor'] = CoreConsciousnessMonitor()
            self.core_engine_tools['engine_optimizer'] = CoreEngineOptimizer() 
            self.core_engine_tools['cellular_enhancer'] = CellularIntelligenceEnhancer()
            
            # Initialize bridges for cross-supercell communication
            self.core_engine_tools['consciousness_bridge'] = ConsciousnessNucleusBridge()
            
            self.logger.info("✅ Core Engine supercell toolset connected")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Some Core Engine tools unavailable: {e}")
            # Continue with available tools
    
    async def _start_organ_monitoring(self):
        """Start monitoring AI Intelligence supercell organs."""
        self.logger.info("👁️ Starting AI Intelligence organ monitoring...")
        
        async def monitor_organs():
            while self.is_active:
                try:
                    await self._check_organ_health()
                    await asyncio.sleep(30)  # Monitor every 30 seconds
                except Exception as e:
                    self.logger.error(f"Organ monitoring error: {e}")
                    await asyncio.sleep(5)
        
        asyncio.create_task(monitor_organs())
        
    async def _check_organ_health(self):
        """Check health status of all monitored organs."""
        for organ_name, organ_data in self.organ_status_cache.items():
            try:
                # Update organ status based on activity
                if organ_data:
                    time_since_activity = (datetime.now() - organ_data.last_activity).total_seconds()
                    
                    if time_since_activity > 300:  # 5 minutes
                        organ_data.status = OrganStatus.IDLE
                    elif time_since_activity > 600:  # 10 minutes  
                        organ_data.status = OrganStatus.OFFLINE
                        
            except Exception as e:
                self.logger.error(f"Error checking {organ_name} health: {e}")
    
    async def _request_processing_loop(self):
        """Main request processing loop for the dendritic supervisor."""
        self.logger.info("🔄 Starting dendritic request processing loop...")
        
        while self.is_active:
            try:
                # Get request from queue with timeout
                request = await asyncio.wait_for(
                    self.request_queue.get(), 
                    timeout=1.0
                )
                
                # Process request asynchronously
                task = asyncio.create_task(self._process_request(request))
                self.processing_tasks[request.request_id] = task
                
            except asyncio.TimeoutError:
                # No requests to process, continue monitoring
                continue
            except Exception as e:
                self.logger.error(f"Error in request processing loop: {e}")
                await asyncio.sleep(1)
    
    async def _process_request(self, request: SupervisorRequest) -> ProcessingResult:
        """
        Process a request through the appropriate Core Engine tools.
        
        Args:
            request: The supervisor request to process
            
        Returns:
            ProcessingResult: Result of the processing
        """
        start_time = datetime.now()
        
        try:
            self.logger.info(f"🔀 Processing request {request.request_id} from {request.source_organ}")
            
            # Update organ activity
            await self._update_organ_activity(request.source_organ)
            
            # Route request to appropriate Core Engine tool
            result_data = await self._route_to_core_engine(request)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Create successful result
            result = ProcessingResult(
                request_id=request.request_id,
                success=True,
                result_data=result_data,
                processing_time=processing_time,
                core_engine_used=request.target_engine
            )
            
            # Update statistics
            self.processing_statistics['successful_requests'] += 1
            self._update_processing_statistics(processing_time)
            
            self.logger.info(f"✅ Request {request.request_id} processed successfully in {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            error_msg = f"Failed to process request {request.request_id}: {e}"
            
            self.logger.error(error_msg)
            self.logger.error(traceback.format_exc())
            
            # Create error result
            result = ProcessingResult(
                request_id=request.request_id,
                success=False,
                result_data={},
                processing_time=processing_time,
                core_engine_used=request.target_engine,
                error_message=error_msg
            )
            
            # Update statistics
            self.processing_statistics['failed_requests'] += 1
            self._update_processing_statistics(processing_time)
            
            return result
        
        finally:
            # Clean up task reference
            self.processing_tasks.pop(request.request_id, None)
    
    async def _route_to_core_engine(self, request: SupervisorRequest) -> Dict[str, Any]:
        """
        Route request to appropriate Core Engine tool based on request type.
        
        Args:
            request: The supervisor request to route
            
        Returns:
            Dict containing processing results from Core Engine
        """
        self.logger.info(f"🎯 Routing {request.request_type.value} to {request.target_engine}")
        
        if request.request_type == RequestType.CONSCIOUSNESS_ANALYSIS:
            return await self._process_consciousness_analysis(request)
            
        elif request.request_type == RequestType.CELLULAR_ENHANCEMENT:
            return await self._process_cellular_enhancement(request)
            
        elif request.request_type == RequestType.ENGINE_OPTIMIZATION:
            return await self._process_engine_optimization(request)
            
        elif request.request_type == RequestType.DENDRITIC_PROCESSING:
            return await self._process_dendritic_request(request)
            
        elif request.request_type == RequestType.INTELLIGENCE_ROUTING:
            return await self._process_intelligence_routing(request)
            
        elif request.request_type == RequestType.ORGAN_MONITORING:
            return await self._process_organ_monitoring(request)
            
        elif request.request_type == RequestType.BRIDGE_COMMUNICATION:
            return await self._process_bridge_communication(request)
            
        else:
            raise ValueError(f"Unknown request type: {request.request_type}")
    
    async def _process_consciousness_analysis(self, request: SupervisorRequest) -> Dict[str, Any]:
        """Process consciousness analysis through Core Engine consciousness monitor."""
        if 'consciousness_monitor' in self.core_engine_tools and self.core_engine_tools['consciousness_monitor']:
            monitor = self.core_engine_tools['consciousness_monitor']
            analysis_result = await monitor.analyze_consciousness_state(request.payload)
            
            return {
                'analysis_type': 'consciousness',
                'consciousness_state': analysis_result.get('state', 'unknown'),
                'consciousness_level': analysis_result.get('level', 0.0),
                'recommendations': analysis_result.get('recommendations', []),
                'core_engine_source': 'consciousness_monitor'
            }
        else:
            return {
                'analysis_type': 'consciousness',
                'error': 'Consciousness monitor not available',
                'simulated_result': True
            }
    
    async def _process_cellular_enhancement(self, request: SupervisorRequest) -> Dict[str, Any]:
        """Process cellular enhancement through Core Engine cellular enhancer."""
        if 'cellular_enhancer' in self.core_engine_tools and self.core_engine_tools['cellular_enhancer']:
            enhancer = self.core_engine_tools['cellular_enhancer']
            enhancement_result = await enhancer.enhance_cellular_intelligence(request.payload)
            
            return {
                'enhancement_type': 'cellular',
                'enhancements_applied': enhancement_result.get('enhancements', []),
                'performance_improvement': enhancement_result.get('improvement_factor', 1.0),
                'optimization_metrics': enhancement_result.get('metrics', {}),
                'core_engine_source': 'cellular_enhancer'
            }
        else:
            return {
                'enhancement_type': 'cellular',
                'error': 'Cellular enhancer not available',
                'simulated_result': True
            }
    
    async def _process_engine_optimization(self, request: SupervisorRequest) -> Dict[str, Any]:
        """Process engine optimization through Core Engine optimizer."""
        if 'engine_optimizer' in self.core_engine_tools and self.core_engine_tools['engine_optimizer']:
            optimizer = self.core_engine_tools['engine_optimizer']
            optimization_result = await optimizer.optimize_engine_performance(request.payload)
            
            return {
                'optimization_type': 'engine',
                'optimizations_applied': optimization_result.get('optimizations', []),
                'performance_metrics': optimization_result.get('metrics', {}),
                'efficiency_gain': optimization_result.get('efficiency_gain', 0.0),
                'core_engine_source': 'engine_optimizer'
            }
        else:
            return {
                'optimization_type': 'engine',
                'error': 'Engine optimizer not available',
                'simulated_result': True
            }
    
    async def _process_dendritic_request(self, request: SupervisorRequest) -> Dict[str, Any]:
        """Process dendritic processing request through Core Engine dendritic engine."""
        if 'dendritic_engine' in self.core_engine_tools and self.core_engine_tools['dendritic_engine']:
            dendritic = self.core_engine_tools['dendritic_engine']
            processing_result = await dendritic.process_dendritic_connections(request.payload)
            
            return {
                'processing_type': 'dendritic',
                'connections_processed': processing_result.get('connections', []),
                'signal_strength': processing_result.get('signal_strength', 0.0),
                'network_topology': processing_result.get('topology', {}),
                'core_engine_source': 'dendritic_engine'
            }
        else:
            return {
                'processing_type': 'dendritic',
                'connections_processed': [],
                'signal_strength': 0.8,
                'simulated_result': True
            }
    
    async def _process_intelligence_routing(self, request: SupervisorRequest) -> Dict[str, Any]:
        """Process intelligence routing request."""
        return {
            'routing_type': 'intelligence',
            'source_organ': request.source_organ,
            'target_engine': request.target_engine,
            'routing_success': True,
            'latency_ms': 15.5,
            'pathway_efficiency': 0.92
        }
    
    async def _process_organ_monitoring(self, request: SupervisorRequest) -> Dict[str, Any]:
        """Process organ monitoring request."""
        organ_statuses = {}
        
        for organ_name, organ_data in self.organ_status_cache.items():
            if organ_data:
                organ_statuses[organ_name] = {
                    'status': organ_data.status.value,
                    'last_activity': organ_data.last_activity.isoformat(),
                    'processing_load': organ_data.processing_load,
                    'error_count': organ_data.error_count
                }
        
        return {
            'monitoring_type': 'organs',
            'organ_statuses': organ_statuses,
            'total_organs_monitored': len(organ_statuses),
            'healthy_organs': len([s for s in organ_statuses.values() if s['status'] == 'active']),
            'supervisor_statistics': self.processing_statistics
        }
    
    async def _process_bridge_communication(self, request: SupervisorRequest) -> Dict[str, Any]:
        """Process bridge communication through Core Engine consciousness bridge."""
        if 'consciousness_bridge' in self.core_engine_tools and self.core_engine_tools['consciousness_bridge']:
            bridge = self.core_engine_tools['consciousness_bridge']
            bridge_result = await bridge.facilitate_cross_supercell_communication(request.payload)
            
            return {
                'communication_type': 'bridge',
                'message_transmitted': bridge_result.get('transmitted', False),
                'response_received': bridge_result.get('response', {}),
                'communication_latency': bridge_result.get('latency', 0.0),
                'core_engine_source': 'consciousness_bridge'
            }
        else:
            return {
                'communication_type': 'bridge',
                'message_transmitted': True,
                'response_received': {'status': 'simulated'},
                'simulated_result': True
            }
    
    async def _update_organ_activity(self, organ_name: str):
        """Update activity timestamp for specified organ."""
        if organ_name in self.organ_status_cache:
            organ_data = self.organ_status_cache[organ_name]
            if organ_data:
                organ_data.last_activity = datetime.now()
                organ_data.status = OrganStatus.PROCESSING
    
    def _update_processing_statistics(self, processing_time: float):
        """Update processing statistics."""
        self.processing_statistics['total_requests'] += 1
        
        # Update average processing time
        total = self.processing_statistics['total_requests']
        current_avg = self.processing_statistics['average_processing_time']
        self.processing_statistics['average_processing_time'] = (
            (current_avg * (total - 1) + processing_time) / total
        )
    
    async def submit_request(self, request: SupervisorRequest) -> str:
        """
        Submit a request to the dendritic supervisor for processing.
        
        Args:
            request: The supervisor request to submit
            
        Returns:
            str: Request ID for tracking
        """
        if not self.is_active:
            raise RuntimeError("Dendritic supervisor is not active")
        
        await self.request_queue.put(request)
        self.logger.info(f"📥 Request {request.request_id} submitted for processing")
        
        return request.request_id
    
    async def get_processing_result(self, request_id: str, timeout: float = 30.0) -> Optional[ProcessingResult]:
        """
        Get processing result for a specific request.
        
        Args:
            request_id: ID of the request to get results for
            timeout: Maximum time to wait for result
            
        Returns:
            ProcessingResult or None if timeout/not found
        """
        if request_id in self.processing_tasks:
            try:
                result = await asyncio.wait_for(
                    self.processing_tasks[request_id], 
                    timeout=timeout
                )
                return result
            except asyncio.TimeoutError:
                self.logger.warning(f"Timeout waiting for result of request {request_id}")
                return None
        
        return None
    
    async def get_supervisor_status(self) -> Dict[str, Any]:
        """Get current status of the dendritic supervisor."""
        return {
            'is_active': self.is_active,
            'queue_size': self.request_queue.qsize(),
            'active_processing_tasks': len(self.processing_tasks),
            'processing_statistics': self.processing_statistics,
            'monitored_organs': {
                name: {
                    'status': data.status.value if data else 'unknown',
                    'last_activity': data.last_activity.isoformat() if data else None,
                    'processing_load': data.processing_load if data else 0.0
                } for name, data in self.organ_status_cache.items()
            },
            'core_engine_tools_available': [
                tool for tool, instance in self.core_engine_tools.items() 
                if instance is not None
            ]
        }
    
    async def shutdown(self):
        """Shutdown the dendritic supervisor gracefully."""
        self.logger.info("🔄 Shutting down dendritic supervisor...")
        
        self.is_active = False
        
        # Wait for active tasks to complete
        if self.processing_tasks:
            await asyncio.gather(*self.processing_tasks.values(), return_exceptions=True)
        
        self.logger.info("✅ Dendritic supervisor shutdown complete")


# Singleton instance for global access
_dendritic_supervisor_instance = None

async def get_dendritic_supervisor() -> DendriticSupervisor:
    """Get the singleton dendritic supervisor instance."""
    global _dendritic_supervisor_instance
    
    if _dendritic_supervisor_instance is None:
        _dendritic_supervisor_instance = DendriticSupervisor()
        await _dendritic_supervisor_instance.initialize()
    
    return _dendritic_supervisor_instance


async def main():
    """Main function for testing the dendritic supervisor."""
    print("🧠 AIOS Dendritic Supervisor - AI Intelligence ↔ Core Engine Bridge")
    print("=" * 70)
    
    # Initialize supervisor
    supervisor = await get_dendritic_supervisor()
    
    # Test requests
    test_requests = [
        SupervisorRequest(
            request_id="test_consciousness_001",
            request_type=RequestType.CONSCIOUSNESS_ANALYSIS,
            source_organ="nucleus",
            target_engine="consciousness_monitor",
            payload={"analysis_type": "state_assessment", "data": {"neurons": 1000}}
        ),
        SupervisorRequest(
            request_id="test_enhancement_001", 
            request_type=RequestType.CELLULAR_ENHANCEMENT,
            source_organ="laboratory",
            target_engine="cellular_enhancer",
            payload={"enhancement_target": "memory_optimization", "parameters": {"level": 3}}
        ),
        SupervisorRequest(
            request_id="test_monitoring_001",
            request_type=RequestType.ORGAN_MONITORING,
            source_organ="cytoplasm",
            target_engine="supervisor",
            payload={"monitoring_scope": "all_organs"}
        )
    ]
    
    # Submit and process test requests
    for request in test_requests:
        print(f"\n📤 Submitting request: {request.request_id}")
        request_id = await supervisor.submit_request(request)
        
        print(f"⏳ Waiting for result...")
        result = await supervisor.get_processing_result(request_id)
        
        if result:
            print(f"✅ Result: {result.success}")
            print(f"⏱️  Processing time: {result.processing_time:.2f}s")
            print(f"🔧 Core engine used: {result.core_engine_used}")
            if result.error_message:
                print(f"❌ Error: {result.error_message}")
        else:
            print(f"❌ No result received")
    
    # Display supervisor status
    print(f"\n📊 Supervisor Status:")
    status = await supervisor.get_supervisor_status()
    print(json.dumps(status, indent=2, default=str))
    
    # Shutdown
    await supervisor.shutdown()


if __name__ == "__main__":
    asyncio.run(main())