"""
Cytoplasm-Dendritic Supervisor Bridge
====================================

This bridge integrates the Dendritic Supervisor with the cytoplasm system,
providing seamless communication between the AI Intelligence supercell organs
and the Core Engine supercell architecture through dendritic processing.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json

from .dendritic_supervisor import (
    DendriticSupervisor, 
    SupervisorRequest, 
    RequestType,
    get_dendritic_supervisor
)
from .ui_interaction_bridge import UIInteractionBridge


class CytoplasmDendriticBridge:
    """
    Bridge between cytoplasm and dendritic supervisor for AI Intelligence ↔ Core Engine communication.
    
    This bridge:
    1. Receives requests from cytoplasm/UI interactions
    2. Translates them into dendritic supervisor requests
    3. Routes them through Core Engine tools
    4. Returns processed results back to cytoplasm
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.dendritic_supervisor: Optional[DendriticSupervisor] = None
        self.ui_bridge: Optional[UIInteractionBridge] = None
        self.is_initialized = False
        
        # Request routing configuration
        self.request_routing_map = {
            'consciousness_analysis': RequestType.CONSCIOUSNESS_ANALYSIS,
            'cellular_enhancement': RequestType.CELLULAR_ENHANCEMENT,
            'engine_optimization': RequestType.ENGINE_OPTIMIZATION,
            'dendritic_processing': RequestType.DENDRITIC_PROCESSING,
            'intelligence_routing': RequestType.INTELLIGENCE_ROUTING,
            'organ_monitoring': RequestType.ORGAN_MONITORING,
            'bridge_communication': RequestType.BRIDGE_COMMUNICATION
        }
        
        # Engine mapping for different request types
        self.engine_mapping = {
            RequestType.CONSCIOUSNESS_ANALYSIS: 'consciousness_monitor',
            RequestType.CELLULAR_ENHANCEMENT: 'cellular_enhancer',
            RequestType.ENGINE_OPTIMIZATION: 'engine_optimizer',
            RequestType.DENDRITIC_PROCESSING: 'dendritic_engine',
            RequestType.INTELLIGENCE_ROUTING: 'supervisor',
            RequestType.ORGAN_MONITORING: 'supervisor',
            RequestType.BRIDGE_COMMUNICATION: 'consciousness_bridge'
        }
    
    async def initialize(self) -> bool:
        """Initialize the cytoplasm-dendritic bridge."""
        try:
            self.logger.info(" Initializing Cytoplasm-Dendritic Bridge...")
            
            # Initialize dendritic supervisor
            self.dendritic_supervisor = await get_dendritic_supervisor()
            
            # Initialize UI bridge for cytoplasm communication
            self.ui_bridge = UIInteractionBridge()
            
            self.is_initialized = True
            self.logger.info(" Cytoplasm-Dendritic Bridge initialized successfully")
            
            return True
            
        except Exception as e:
            self.logger.error(f" Failed to initialize bridge: {e}")
            return False
    
    async def process_cytoplasm_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a request from the cytoplasm through the dendritic supervisor.
        
        Args:
            request_data: Request data from cytoplasm containing:
                - request_type: Type of processing requested
                - source_organ: Origin organ in AI Intelligence supercell
                - payload: Data to be processed
                - priority: Request priority (optional)
        
        Returns:
            Dict containing processing results from Core Engine
        """
        if not self.is_initialized:
            raise RuntimeError("Bridge not initialized")
        
        try:
            # Extract request information
            request_type_str = request_data.get('request_type', 'intelligence_routing')
            source_organ = request_data.get('source_organ', 'cytoplasm')
            payload = request_data.get('payload', {})
            priority = request_data.get('priority', 1)
            
            # Map request type to supervisor enum
            request_type = self.request_routing_map.get(request_type_str, RequestType.INTELLIGENCE_ROUTING)
            
            # Determine target engine
            target_engine = self.engine_mapping.get(request_type, 'supervisor')
            
            # Generate unique request ID
            request_id = f"{source_organ}_{request_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            
            # Create supervisor request
            supervisor_request = SupervisorRequest(
                request_id=request_id,
                request_type=request_type,
                source_organ=source_organ,
                target_engine=target_engine,
                payload=payload,
                priority=priority
            )
            
            self.logger.info(f" Processing cytoplasm request {request_id} via dendritic supervisor")
            
            # Submit request to dendritic supervisor
            await self.dendritic_supervisor.submit_request(supervisor_request)
            
            # Wait for processing result
            result = await self.dendritic_supervisor.get_processing_result(request_id, timeout=60.0)
            
            if result:
                # Format result for cytoplasm
                return {
                    'success': result.success,
                    'request_id': result.request_id,
                    'processing_time': result.processing_time,
                    'core_engine_used': result.core_engine_used,
                    'result_data': result.result_data,
                    'error_message': result.error_message,
                    'timestamp': datetime.now().isoformat(),
                    'bridge_source': 'cytoplasm_dendritic_bridge'
                }
            else:
                return {
                    'success': False,
                    'request_id': request_id,
                    'error_message': 'Processing timeout or result not available',
                    'timestamp': datetime.now().isoformat(),
                    'bridge_source': 'cytoplasm_dendritic_bridge'
                }
                
        except Exception as e:
            error_msg = f"Error processing cytoplasm request: {e}"
            self.logger.error(error_msg)
            
            return {
                'success': False,
                'error_message': error_msg,
                'timestamp': datetime.now().isoformat(),
                'bridge_source': 'cytoplasm_dendritic_bridge'
            }
    
    async def get_ai_intelligence_status(self) -> Dict[str, Any]:
        """
        Get comprehensive status of AI Intelligence supercell through dendritic supervisor.
        
        Returns:
            Dict containing status of all AI Intelligence organs and Core Engine connections
        """
        if not self.is_initialized:
            raise RuntimeError("Bridge not initialized")
        
        try:
            # Get supervisor status
            supervisor_status = await self.dendritic_supervisor.get_supervisor_status()
            
            # Enhanced with bridge-specific information
            return {
                'ai_intelligence_supercell': {
                    'status': 'active' if supervisor_status['is_active'] else 'inactive',
                    'monitored_organs': supervisor_status['monitored_organs'],
                    'processing_queue_size': supervisor_status['queue_size'],
                    'active_processing_tasks': supervisor_status['active_processing_tasks']
                },
                'core_engine_connectivity': {
                    'available_tools': supervisor_status['core_engine_tools_available'],
                    'total_tools': len(supervisor_status['core_engine_tools_available'])
                },
                'dendritic_processing': {
                    'statistics': supervisor_status['processing_statistics']
                },
                'bridge_status': {
                    'is_initialized': self.is_initialized,
                    'ui_bridge_active': self.ui_bridge is not None,
                    'supervisor_active': self.dendritic_supervisor is not None
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting AI Intelligence status: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def monitor_organ_health(self, organ_name: str) -> Dict[str, Any]:
        """
        Monitor specific AI Intelligence organ health through dendritic supervisor.
        
        Args:
            organ_name: Name of the organ to monitor
            
        Returns:
            Dict containing health information for the specified organ
        """
        request_data = {
            'request_type': 'organ_monitoring',
            'source_organ': 'cytoplasm',
            'payload': {
                'monitoring_scope': 'single_organ',
                'target_organ': organ_name
            }
        }
        
        return await self.process_cytoplasm_request(request_data)
    
    async def enhance_organ_performance(self, organ_name: str, enhancement_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request performance enhancement for specific AI Intelligence organ.
        
        Args:
            organ_name: Name of the organ to enhance
            enhancement_params: Parameters for enhancement
            
        Returns:
            Dict containing enhancement results
        """
        request_data = {
            'request_type': 'cellular_enhancement',
            'source_organ': organ_name,
            'payload': {
                'enhancement_target': organ_name,
                'parameters': enhancement_params
            }
        }
        
        return await self.process_cytoplasm_request(request_data)
    
    async def analyze_consciousness_state(self, analysis_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request consciousness analysis through Core Engine.
        
        Args:
            analysis_params: Parameters for consciousness analysis
            
        Returns:
            Dict containing consciousness analysis results
        """
        request_data = {
            'request_type': 'consciousness_analysis',
            'source_organ': 'nucleus',
            'payload': analysis_params
        }
        
        return await self.process_cytoplasm_request(request_data)
    
    async def optimize_core_engine(self, optimization_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request Core Engine optimization.
        
        Args:
            optimization_params: Parameters for optimization
            
        Returns:
            Dict containing optimization results
        """
        request_data = {
            'request_type': 'engine_optimization',
            'source_organ': 'cytoplasm',
            'payload': optimization_params
        }
        
        return await self.process_cytoplasm_request(request_data)
    
    async def facilitate_cross_supercell_communication(self, communication_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Facilitate communication between AI Intelligence and Core Engine supercells.
        
        Args:
            communication_data: Data for cross-supercell communication
            
        Returns:
            Dict containing communication results
        """
        request_data = {
            'request_type': 'bridge_communication',
            'source_organ': 'transport',
            'payload': communication_data
        }
        
        return await self.process_cytoplasm_request(request_data)
    
    async def shutdown(self):
        """Shutdown the cytoplasm-dendritic bridge."""
        self.logger.info(" Shutting down Cytoplasm-Dendritic Bridge...")
        
        if self.dendritic_supervisor:
            await self.dendritic_supervisor.shutdown()
        
        self.is_initialized = False
        self.logger.info(" Cytoplasm-Dendritic Bridge shutdown complete")


# Singleton instance for global access
_cytoplasm_dendritic_bridge_instance = None

async def get_cytoplasm_dendritic_bridge() -> CytoplasmDendriticBridge:
    """Get the singleton cytoplasm-dendritic bridge instance."""
    global _cytoplasm_dendritic_bridge_instance
    
    if _cytoplasm_dendritic_bridge_instance is None:
        _cytoplasm_dendritic_bridge_instance = CytoplasmDendriticBridge()
        await _cytoplasm_dendritic_bridge_instance.initialize()
    
    return _cytoplasm_dendritic_bridge_instance