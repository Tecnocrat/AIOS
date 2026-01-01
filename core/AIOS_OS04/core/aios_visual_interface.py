"""
AIOS Visual Interface Mega-Module (OS0.4)
========================================

This mega-module serves as the Python-side orchestrator and bridge for AIOS visual interfaces,
including real-time visualization, C# visual interface coordination, web-based dashboards,
and consciousness state visualization.

Key Components:
- Real-time visualization engine
- C# visual interface bridge/coordinator
- Web dashboard server
- Consciousness state rendering
- Data visualization utilities
- Interactive analytics dashboard
"""

import asyncio
import json
import logging
import os
import sys
import threading
import time
import webbrowser
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Tuple, Union
import subprocess
import socket

# Third-party imports (will need to be installed)
try:
    import websockets
    import aiofiles
    from flask import Flask, render_template, jsonify, request
    from flask_socketio import SocketIO, emit
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import numpy as np
    import plotly.graph_objects as go
    import plotly.offline as pyo
    from plotly.subplots import make_subplots
except ImportError as e:
    print(f"Warning: Some visualization dependencies not available: {e}")
    print("Run: pip install websockets aiofiles flask flask-socketio matplotlib numpy plotly")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VisualizationConfig:
    """Configuration for visualization components"""
    def __init__(self):
        self.web_port = 8080
        self.websocket_port = 8081
        self.cs_bridge_port = 8082
        self.update_interval = 1.0  # seconds
        self.enable_web_dashboard = True
        self.enable_cs_bridge = True
        self.enable_real_time_plots = True
        self.data_retention_hours = 24
        self.visualization_themes = {
            'consciousness': 'viridis',
            'evolution': 'plasma',
            'knowledge': 'cool',
            'system': 'warm'
        }

@dataclass
class VisualizationData:
    """Data structure for visualization content"""
    timestamp: datetime
    data_type: str
    content: Dict[str, Any]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'data_type': self.data_type,
            'content': self.content,
            'metadata': self.metadata
        }

class BaseVisualizationEngine(ABC):
    """Abstract base class for all visualization engines"""
    
    def __init__(self, config: VisualizationConfig):
        self.config = config
        self.is_running = False
        self.data_buffer: List[VisualizationData] = []
        self.subscribers: List[Callable] = []
        
    @abstractmethod
    async def start(self):
        """Start the visualization engine"""
        pass
        
    @abstractmethod
    async def stop(self):
        """Stop the visualization engine"""
        pass
        
    @abstractmethod
    async def render(self, data: VisualizationData) -> Any:
        """Render visualization data"""
        pass
        
    def add_subscriber(self, callback: Callable):
        """Add a callback for data updates"""
        self.subscribers.append(callback)
        
    def remove_subscriber(self, callback: Callable):
        """Remove a callback"""
        if callback in self.subscribers:
            self.subscribers.remove(callback)
            
    async def notify_subscribers(self, data: VisualizationData):
        """Notify all subscribers of new data"""
        for callback in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                logger.error(f"Error notifying subscriber: {e}")

class ConsciousnessVisualizationEngine(BaseVisualizationEngine):
    """Specialized engine for consciousness state visualization"""
    
    def __init__(self, config: VisualizationConfig):
        super().__init__(config)
        self.consciousness_states = {}
        self.evolution_history = []
        self.current_plots = {}
        
    async def start(self):
        """Start consciousness visualization"""
        self.is_running = True
        logger.info("Consciousness Visualization Engine started")
        
    async def stop(self):
        """Stop consciousness visualization"""
        self.is_running = False
        logger.info("Consciousness Visualization Engine stopped")
        
    async def render(self, data: VisualizationData) -> Dict[str, Any]:
        """Render consciousness visualization"""
        if data.data_type == 'consciousness_state':
            return await self._render_consciousness_state(data)
        elif data.data_type == 'evolution_progress':
            return await self._render_evolution_progress(data)
        elif data.data_type == 'knowledge_graph':
            return await self._render_knowledge_graph(data)
        else:
            return {'error': f'Unknown data type: {data.data_type}'}
            
    async def _render_consciousness_state(self, data: VisualizationData) -> Dict[str, Any]:
        """Render consciousness state visualization"""
        try:
            state_data = data.content
            
            # Create consciousness state plot
            fig = go.Figure()
            
            # Add consciousness levels
            if 'levels' in state_data:
                levels = state_data['levels']
                fig.add_trace(go.Scatter(
                    x=list(range(len(levels))),
                    y=levels,
                    mode='lines+markers',
                    name='Consciousness Levels',
                    line=dict(color='cyan', width=3)
                ))
            
            # Add coherence metrics
            if 'coherence' in state_data:
                coherence = state_data['coherence']
                fig.add_trace(go.Scatter(
                    x=list(range(len(coherence))),
                    y=coherence,
                    mode='lines+markers',
                    name='Coherence',
                    line=dict(color='magenta', width=2)
                ))
            
            fig.update_layout(
                title='AIOS Consciousness State',
                xaxis_title='Time Steps',
                yaxis_title='Activation Level',
                template='plotly_dark',
                showlegend=True
            )
            
            # Convert to HTML
            html_plot = pyo.plot(fig, output_type='div', include_plotlyjs=False)
            
            return {
                'type': 'consciousness_state',
                'html': html_plot,
                'metadata': data.metadata,
                'timestamp': data.timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error rendering consciousness state: {e}")
            return {'error': str(e)}
            
    async def _render_evolution_progress(self, data: VisualizationData) -> Dict[str, Any]:
        """Render evolution progress visualization"""
        # Implementation stub - will expand in next step
        return {'type': 'evolution_progress', 'status': 'rendering'}
        
    async def _render_knowledge_graph(self, data: VisualizationData) -> Dict[str, Any]:
        """Render knowledge graph visualization"""
        # Implementation stub - will expand in next step
        return {'type': 'knowledge_graph', 'status': 'rendering'}

class CSharpVisualInterfaceBridge:
    """Bridge for coordinating with C# visual interface components"""
    
    def __init__(self, config: VisualizationConfig):
        self.config = config
        self.is_running = False
        self.process = None
        self.websocket_server = None
        self.connected_clients = set()
        self.data_queue = asyncio.Queue()
        
    async def start(self):
        """Start the C# bridge"""
        try:
            self.is_running = True
            
            # Start WebSocket server for C# communication
            await self._start_websocket_server()
            
            # Launch C# visual interface if configured
            if self.config.enable_cs_bridge:
                await self._launch_cs_interface()
                
            logger.info("C# Visual Interface Bridge started")
            
        except Exception as e:
            logger.error(f"Error starting C# bridge: {e}")
            
    async def stop(self):
        """Stop the C# bridge"""
        self.is_running = False
        
        # Stop WebSocket server
        if self.websocket_server:
            self.websocket_server.close()
            await self.websocket_server.wait_closed()
            
        # Terminate C# process
        if self.process:
            self.process.terminate()
            
        logger.info("C# Visual Interface Bridge stopped")
        
    async def _start_websocket_server(self):
        """Start WebSocket server for C# communication"""
        async def handle_client(websocket, path):
            self.connected_clients.add(websocket)
            logger.info(f"C# client connected: {websocket.remote_address}")
            
            try:
                async for message in websocket:
                    data = json.loads(message)
                    await self._handle_cs_message(data, websocket)
            except websockets.exceptions.ConnectionClosed:
                logger.info("C# client disconnected")
            finally:
                self.connected_clients.discard(websocket)
                
        self.websocket_server = await websockets.serve(
            handle_client,
            "localhost",
            self.config.cs_bridge_port
        )
        
    async def _handle_cs_message(self, data: Dict[str, Any], websocket):
        """Handle messages from C# interface"""
        try:
            message_type = data.get('type')
            
            if message_type == 'consciousness_update':
                # Forward consciousness data to Python visualization
                viz_data = VisualizationData(
                    timestamp=datetime.now(),
                    data_type='consciousness_state',
                    content=data.get('content', {}),
                    metadata={'source': 'cs_interface'}
                )
                await self.data_queue.put(viz_data)
                
            elif message_type == 'request_data':
                # C# requesting data from Python
                response = await self._get_data_for_cs(data.get('data_type'))
                await websocket.send(json.dumps(response))
                
            elif message_type == 'configuration_update':
                # C# updating configuration
                await self._update_configuration(data.get('config', {}))
                
        except Exception as e:
            logger.error(f"Error handling C# message: {e}")
            
    async def _launch_cs_interface(self):
        """Launch the C# visual interface application"""
        try:
            cs_exe_path = Path("../visual_interface/bin/Debug/AIOS.VisualInterface.exe")
            
            if cs_exe_path.exists():
                self.process = subprocess.Popen([str(cs_exe_path)])
                logger.info("C# Visual Interface launched")
            else:
                logger.warning(f"C# executable not found at {cs_exe_path}")
                
        except Exception as e:
            logger.error(f"Error launching C# interface: {e}")
            
    async def _get_data_for_cs(self, data_type: str) -> Dict[str, Any]:
        """Get data to send to C# interface"""
        # This would integrate with other mega-modules
        return {
            'type': 'data_response',
            'data_type': data_type,
            'content': {},
            'timestamp': datetime.now().isoformat()
        }
        
    async def _update_configuration(self, config_data: Dict[str, Any]):
        """Update configuration based on C# requests"""
        # Update visualization configuration
        pass
        
    async def send_to_cs_clients(self, data: Dict[str, Any]):
        """Send data to all connected C# clients"""
        if not self.connected_clients:
            return
            
        message = json.dumps(data)
        disconnected = set()
        
        for client in self.connected_clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
                
        # Remove disconnected clients
        self.connected_clients -= disconnected

class WebDashboardServer:
    """Flask-based web dashboard for AIOS visualization"""
    
    def __init__(self, config: VisualizationConfig):
        self.config = config
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.is_running = False
        self.setup_routes()
        self.setup_socketio_events()
        
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def dashboard():
            return render_template('dashboard.html')
            
        @self.app.route('/api/consciousness')
        def get_consciousness_data():
            # This would integrate with consciousness engine
            return jsonify({
                'status': 'active',
                'levels': [0.8, 0.9, 0.85, 0.92],
                'coherence': [0.75, 0.82, 0.78, 0.88],
                'timestamp': datetime.now().isoformat()
            })
            
        @self.app.route('/api/evolution')
        def get_evolution_data():
            # This would integrate with evolution lab
            return jsonify({
                'generations': 42,
                'fitness': 0.87,
                'mutations': 156,
                'timestamp': datetime.now().isoformat()
            })
            
        @self.app.route('/api/system')
        def get_system_data():
            # This would integrate with system intelligence
            return jsonify({
                'cpu_usage': 45.2,
                'memory_usage': 67.8,
                'active_processes': 8,
                'timestamp': datetime.now().isoformat()
            })
            
    def setup_socketio_events(self):
        """Setup SocketIO events for real-time updates"""
        
        @self.socketio.on('connect')
        def handle_connect():
            logger.info('Web client connected')
            
        @self.socketio.on('disconnect')
        def handle_disconnect():
            logger.info('Web client disconnected')
            
        @self.socketio.on('request_update')
        def handle_request_update(data):
            # Send real-time updates to web client
            self.socketio.emit('data_update', {
                'type': data.get('type', 'all'),
                'timestamp': datetime.now().isoformat()
            })
            
    async def start(self):
        """Start the web dashboard server"""
        try:
            self.is_running = True
            
            # Run Flask app in a separate thread
            def run_app():
                self.socketio.run(
                    self.app,
                    host='0.0.0.0',
                    port=self.config.web_port,
                    debug=False
                )
                
            self.server_thread = threading.Thread(target=run_app, daemon=True)
            self.server_thread.start()
            
            logger.info(f"Web Dashboard started on port {self.config.web_port}")
            
        except Exception as e:
            logger.error(f"Error starting web dashboard: {e}")
            
    async def stop(self):
        """Stop the web dashboard server"""
        self.is_running = False
        logger.info("Web Dashboard stopped")
        
    def emit_real_time_update(self, data: Dict[str, Any]):
        """Emit real-time update to web clients"""
        self.socketio.emit('real_time_update', data)

class AIOSVisualInterfaceManager:
    """Main manager for all AIOS visual interface components"""
    
    def __init__(self, config: Optional[VisualizationConfig] = None):
        self.config = config or VisualizationConfig()
        self.is_running = False
        
        # Initialize components
        self.consciousness_engine = ConsciousnessVisualizationEngine(self.config)
        self.cs_bridge = CSharpVisualInterfaceBridge(self.config)
        self.web_dashboard = WebDashboardServer(self.config)
        
        # Data coordination
        self.data_processors = {}
        self.active_visualizations = {}
        self.update_tasks = []
        
        # Integration with other mega-modules (will be injected)
        self.consciousness_module = None
        self.evolution_module = None
        self.knowledge_module = None
        self.admin_module = None
        
    async def initialize(self):
        """Initialize the visual interface manager"""
        try:
            logger.info("Initializing AIOS Visual Interface Manager...")
            
            # Setup data processors
            await self._setup_data_processors()
            
            # Initialize component connections
            await self._setup_component_connections()
            
            logger.info("AIOS Visual Interface Manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing visual interface manager: {e}")
            raise
            
    async def start(self):
        """Start all visual interface components"""
        try:
            self.is_running = True
            logger.info("Starting AIOS Visual Interface Manager...")
            
            # Start consciousness visualization engine
            await self.consciousness_engine.start()
            
            # Start C# bridge if enabled
            if self.config.enable_cs_bridge:
                await self.cs_bridge.start()
                
            # Start web dashboard if enabled
            if self.config.enable_web_dashboard:
                await self.web_dashboard.start()
                
            # Start data update loop
            self.update_tasks.append(
                asyncio.create_task(self._data_update_loop())
            )
            
            # Start integration bridges
            self.update_tasks.append(
                asyncio.create_task(self._integration_bridge_loop())
            )
            
            logger.info("AIOS Visual Interface Manager started successfully")
            
            # Open web dashboard in browser
            if self.config.enable_web_dashboard:
                await asyncio.sleep(2)  # Wait for server to be ready
                webbrowser.open(f"http://localhost:{self.config.web_port}")
                
        except Exception as e:
            logger.error(f"Error starting visual interface manager: {e}")
            raise
            
    async def stop(self):
        """Stop all visual interface components"""
        try:
            self.is_running = False
            logger.info("Stopping AIOS Visual Interface Manager...")
            
            # Cancel update tasks
            for task in self.update_tasks:
                task.cancel()
                
            # Stop components
            await self.consciousness_engine.stop()
            await self.cs_bridge.stop()
            await self.web_dashboard.stop()
            
            logger.info("AIOS Visual Interface Manager stopped")
            
        except Exception as e:
            logger.error(f"Error stopping visual interface manager: {e}")
            
    async def _setup_data_processors(self):
        """Setup data processing pipelines"""
        
        # Consciousness data processor
        async def process_consciousness_data(data):
            viz_data = VisualizationData(
                timestamp=datetime.now(),
                data_type='consciousness_state',
                content=data,
                metadata={'processor': 'consciousness'}
            )
            
            # Render visualization
            rendered = await self.consciousness_engine.render(viz_data)
            
            # Send to web dashboard
            self.web_dashboard.emit_real_time_update({
                'type': 'consciousness_update',
                'data': rendered
            })
            
            # Send to C# clients
            await self.cs_bridge.send_to_cs_clients({
                'type': 'consciousness_visualization',
                'data': rendered
            })
            
        self.data_processors['consciousness'] = process_consciousness_data
        
        # Evolution data processor
        async def process_evolution_data(data):
            viz_data = VisualizationData(
                timestamp=datetime.now(),
                data_type='evolution_progress',
                content=data,
                metadata={'processor': 'evolution'}
            )
            
            rendered = await self.consciousness_engine.render(viz_data)
            
            self.web_dashboard.emit_real_time_update({
                'type': 'evolution_update',
                'data': rendered
            })
            
        self.data_processors['evolution'] = process_evolution_data
        
        # Knowledge data processor
        async def process_knowledge_data(data):
            viz_data = VisualizationData(
                timestamp=datetime.now(),
                data_type='knowledge_graph',
                content=data,
                metadata={'processor': 'knowledge'}
            )
            
            rendered = await self.consciousness_engine.render(viz_data)
            
            self.web_dashboard.emit_real_time_update({
                'type': 'knowledge_update',
                'data': rendered
            })
            
        self.data_processors['knowledge'] = process_knowledge_data
        
    async def _setup_component_connections(self):
        """Setup connections between components"""
        
        # Connect consciousness engine to bridges
        self.consciousness_engine.add_subscriber(
            lambda data: self._forward_to_bridges(data, 'consciousness')
        )
        
    async def _forward_to_bridges(self, data: VisualizationData, source: str):
        """Forward data to appropriate bridges"""
        try:
            # Forward to web dashboard
            self.web_dashboard.emit_real_time_update({
                'type': f'{source}_data',
                'data': data.to_dict()
            })
            
            # Forward to C# bridge
            await self.cs_bridge.send_to_cs_clients({
                'type': f'{source}_data',
                'data': data.to_dict()
            })
            
        except Exception as e:
            logger.error(f"Error forwarding data to bridges: {e}")
            
    async def _data_update_loop(self):
        """Main data update loop"""
        while self.is_running:
            try:
                # Check for data from C# bridge
                if not self.cs_bridge.data_queue.empty():
                    data = await self.cs_bridge.data_queue.get()
                    
                    # Process data based on type
                    processor = self.data_processors.get(data.data_type)
                    if processor:
                        await processor(data.content)
                        
                # Collect data from integrated modules (if available)
                await self._collect_module_data()
                
                await asyncio.sleep(self.config.update_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in data update loop: {e}")
                await asyncio.sleep(self.config.update_interval)
                
    async def _integration_bridge_loop(self):
        """Integration bridge with other mega-modules"""
        while self.is_running:
            try:
                # Try to collect data from consciousness module
                if self.consciousness_module:
                    try:
                        consciousness_data = await self._get_consciousness_data()
                        if consciousness_data:
                            processor = self.data_processors.get('consciousness')
                            if processor:
                                await processor(consciousness_data)
                    except Exception as e:
                        logger.debug(f"Could not get consciousness data: {e}")
                
                # Try to collect data from evolution module
                if self.evolution_module:
                    try:
                        evolution_data = await self._get_evolution_data()
                        if evolution_data:
                            processor = self.data_processors.get('evolution')
                            if processor:
                                await processor(evolution_data)
                    except Exception as e:
                        logger.debug(f"Could not get evolution data: {e}")
                
                await asyncio.sleep(self.config.update_interval * 2)  # Less frequent
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in integration bridge loop: {e}")
                await asyncio.sleep(self.config.update_interval)
                
    async def _collect_module_data(self):
        """Collect data from integrated mega-modules"""
        # This will be implemented when modules are integrated
        pass
        
    async def _get_consciousness_data(self) -> Optional[Dict[str, Any]]:
        """Get consciousness data from consciousness module"""
        if not self.consciousness_module:
            return None
            
        # This will call methods from the consciousness mega-module
        # For now, return mock data
        return {
            'levels': [0.8, 0.85, 0.9, 0.88],
            'coherence': [0.75, 0.8, 0.82, 0.79],
            'active_patterns': 12,
            'emergence_level': 0.73
        }
        
    async def _get_evolution_data(self) -> Optional[Dict[str, Any]]:
        """Get evolution data from evolution module"""
        if not self.evolution_module:
            return None
            
        # This will call methods from the evolution mega-module
        # For now, return mock data
        return {
            'current_generation': 45,
            'fitness_score': 0.87,
            'mutation_rate': 0.15,
            'population_size': 100,
            'best_individuals': 5
        }
        
    # Integration methods for other mega-modules
    def integrate_consciousness_module(self, module):
        """Integrate with consciousness mega-module"""
        self.consciousness_module = module
        logger.info("Consciousness module integrated with visual interface")
        
    def integrate_evolution_module(self, module):
        """Integrate with evolution mega-module"""
        self.evolution_module = module
        logger.info("Evolution module integrated with visual interface")
        
    def integrate_knowledge_module(self, module):
        """Integrate with knowledge mega-module"""
        self.knowledge_module = module
        logger.info("Knowledge module integrated with visual interface")
        
    def integrate_admin_module(self, module):
        """Integrate with admin mega-module"""
        self.admin_module = module
        logger.info("Admin module integrated with visual interface")
        
    # Public API methods
    async def visualize_consciousness_state(self, state_data: Dict[str, Any]):
        """Manually trigger consciousness visualization"""
        processor = self.data_processors.get('consciousness')
        if processor:
            await processor(state_data)
            
    async def visualize_evolution_progress(self, evolution_data: Dict[str, Any]):
        """Manually trigger evolution visualization"""
        processor = self.data_processors.get('evolution')
        if processor:
            await processor(evolution_data)
            
    async def get_visualization_status(self) -> Dict[str, Any]:
        """Get status of all visualization components"""
        return {
            'manager_running': self.is_running,
            'consciousness_engine': self.consciousness_engine.is_running,
            'cs_bridge_running': self.cs_bridge.is_running,
            'web_dashboard_running': self.web_dashboard.is_running,
            'connected_cs_clients': len(self.cs_bridge.connected_clients),
            'active_visualizations': len(self.active_visualizations),
            'config': {
                'web_port': self.config.web_port,
                'websocket_port': self.config.websocket_port,
                'cs_bridge_port': self.config.cs_bridge_port,
                'update_interval': self.config.update_interval
            }
        }

# Utility Functions
def create_sample_consciousness_data() -> Dict[str, Any]:
    """Create sample consciousness data for testing"""
    import random
    
    return {
        'levels': [random.uniform(0.5, 1.0) for _ in range(10)],
        'coherence': [random.uniform(0.3, 0.9) for _ in range(10)],
        'active_patterns': random.randint(5, 20),
        'emergence_level': random.uniform(0.4, 0.95),
        'neural_connectivity': random.uniform(0.6, 0.98),
        'consciousness_index': random.uniform(0.5, 1.0)
    }

def create_sample_evolution_data() -> Dict[str, Any]:
    """Create sample evolution data for testing"""
    import random
    
    return {
        'current_generation': random.randint(20, 100),
        'fitness_score': random.uniform(0.5, 1.0),
        'mutation_rate': random.uniform(0.05, 0.25),
        'population_size': random.randint(50, 200),
        'best_individuals': random.randint(3, 10),
        'diversity_index': random.uniform(0.3, 0.8),
        'convergence_rate': random.uniform(0.1, 0.9)
    }

def validate_visualization_dependencies() -> Dict[str, bool]:
    """Validate that all required dependencies are available"""
    dependencies = {
        'websockets': False,
        'aiofiles': False,
        'flask': False,
        'flask_socketio': False,
        'matplotlib': False,
        'numpy': False,
        'plotly': False
    }
    
    for dep in dependencies:
        try:
            __import__(dep)
            dependencies[dep] = True
        except ImportError:
            dependencies[dep] = False
            
    return dependencies

def get_available_ports(start_port: int = 8080, count: int = 10) -> List[int]:
    """Get a list of available ports starting from start_port"""
    available_ports = []
    
    for port in range(start_port, start_port + count * 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                available_ports.append(port)
                if len(available_ports) >= count:
                    break
            except OSError:
                continue
                
    return available_ports

def create_dashboard_template() -> str:
    """Create a basic HTML template for the web dashboard"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AIOS Visual Interface Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: #ffffff;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
        }
        .header { 
            text-align: center; 
            margin-bottom: 30px; 
        }
        .dashboard-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); 
            gap: 20px; 
        }
        .chart-container { 
            background: rgba(255, 255, 255, 0.1); 
            border-radius: 10px; 
            padding: 20px; 
            backdrop-filter: blur(10px);
        }
        .status-indicator { 
            display: inline-block; 
            width: 12px; 
            height: 12px; 
            border-radius: 50%; 
            margin-right: 8px; 
        }
        .status-active { background-color: #00ff00; }
        .status-inactive { background-color: #ff0000; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 AIOS Visual Interface Dashboard</h1>
            <p>Real-time Consciousness & Evolution Monitoring</p>
            <div id="connection-status">
                <span class="status-indicator status-inactive" id="connection-indicator"></span>
                <span id="connection-text">Connecting...</span>
            </div>
        </div>
        
        <div class="dashboard-grid">
            <div class="chart-container">
                <h3>Consciousness State</h3>
                <div id="consciousness-chart"></div>
            </div>
            
            <div class="chart-container">
                <h3>Evolution Progress</h3>
                <div id="evolution-chart"></div>
            </div>
            
            <div class="chart-container">
                <h3>System Metrics</h3>
                <div id="system-chart"></div>
            </div>
            
            <div class="chart-container">
                <h3>Real-time Log</h3>
                <div id="log-container" style="height: 300px; overflow-y: auto; font-family: monospace; font-size: 12px;"></div>
            </div>
        </div>
    </div>

    <script>
        // Initialize Socket.IO connection
        const socket = io();
        
        socket.on('connect', function() {
            document.getElementById('connection-indicator').className = 'status-indicator status-active';
            document.getElementById('connection-text').textContent = 'Connected';
            addLog('Connected to AIOS Visual Interface');
        });
        
        socket.on('disconnect', function() {
            document.getElementById('connection-indicator').className = 'status-indicator status-inactive';
            document.getElementById('connection-text').textContent = 'Disconnected';
            addLog('Disconnected from AIOS Visual Interface');
        });
        
        socket.on('real_time_update', function(data) {
            handleRealtimeUpdate(data);
        });
        
        function handleRealtimeUpdate(data) {
            addLog(`Received ${data.type} update`);
            
            if (data.type === 'consciousness_update') {
                updateConsciousnessChart(data.data);
            } else if (data.type === 'evolution_update') {
                updateEvolutionChart(data.data);
            }
        }
        
        function updateConsciousnessChart(data) {
            // Placeholder for consciousness chart updates
            addLog('Updated consciousness visualization');
        }
        
        function updateEvolutionChart(data) {
            // Placeholder for evolution chart updates
            addLog('Updated evolution visualization');
        }
        
        function addLog(message) {
            const logContainer = document.getElementById('log-container');
            const timestamp = new Date().toLocaleTimeString();
            logContainer.innerHTML += `<div>[${timestamp}] ${message}</div>`;
            logContainer.scrollTop = logContainer.scrollHeight;
        }
        
        // Initialize with placeholder charts
        window.onload = function() {
            initializePlaceholderCharts();
        };
        
        function initializePlaceholderCharts() {
            // Consciousness chart
            Plotly.newPlot('consciousness-chart', [{
                x: [1, 2, 3, 4, 5],
                y: [0.8, 0.85, 0.9, 0.88, 0.92],
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Consciousness Level',
                line: {color: 'cyan'}
            }], {
                title: 'Consciousness Levels',
                plot_bgcolor: 'rgba(0,0,0,0)',
                paper_bgcolor: 'rgba(0,0,0,0)',
                font: {color: 'white'}
            });
            
            // Evolution chart
            Plotly.newPlot('evolution-chart', [{
                x: ['Gen 1', 'Gen 2', 'Gen 3', 'Gen 4', 'Gen 5'],
                y: [0.6, 0.7, 0.75, 0.82, 0.87],
                type: 'bar',
                name: 'Fitness Score',
                marker: {color: 'magenta'}
            }], {
                title: 'Evolution Progress',
                plot_bgcolor: 'rgba(0,0,0,0)',
                paper_bgcolor: 'rgba(0,0,0,0)',
                font: {color: 'white'}
            });
            
            // System chart
            Plotly.newPlot('system-chart', [{
                values: [45, 55],
                labels: ['Used', 'Free'],
                type: 'pie',
                name: 'CPU Usage',
                hole: 0.4,
                marker: {colors: ['#ff6b6b', '#4ecdc4']}
            }], {
                title: 'System Resources',
                plot_bgcolor: 'rgba(0,0,0,0)',
                paper_bgcolor: 'rgba(0,0,0,0)',
                font: {color: 'white'}
            });
        }
    </script>
</body>
</html>
    """

# Demo and Test Functions
async def run_visual_interface_demo():
    """Run a comprehensive demo of the visual interface system"""
    print("🧠 Starting AIOS Visual Interface Demo...")
    
    try:
        # Validate dependencies
        deps = validate_visualization_dependencies()
        missing_deps = [dep for dep, available in deps.items() if not available]
        
        if missing_deps:
            print(f"⚠️  Missing dependencies: {', '.join(missing_deps)}")
            print("Please install with: pip install websockets aiofiles flask flask-socketio matplotlib numpy plotly")
            return
            
        # Create configuration with available ports
        available_ports = get_available_ports(8080, 3)
        if len(available_ports) < 3:
            print("❌ Not enough available ports for demo")
            return
            
        config = VisualizationConfig()
        config.web_port = available_ports[0]
        config.websocket_port = available_ports[1]
        config.cs_bridge_port = available_ports[2]
        
        print(f"📊 Using ports: Web={config.web_port}, WebSocket={config.websocket_port}, C#={config.cs_bridge_port}")
        
        # Create and save dashboard template
        dashboard_dir = Path("templates")
        dashboard_dir.mkdir(exist_ok=True)
        
        dashboard_path = dashboard_dir / "dashboard.html"
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(create_dashboard_template())
            
        print(f"📄 Dashboard template created at {dashboard_path}")
        
        # Initialize visual interface manager
        manager = AIOSVisualInterfaceManager(config)
        await manager.initialize()
        
        print("🚀 Starting visual interface components...")
        await manager.start()
        
        print(f"🌐 Web dashboard available at: http://localhost:{config.web_port}")
        print(f"🔗 WebSocket server: ws://localhost:{config.websocket_port}")
        print(f"🖥️  C# bridge: ws://localhost:{config.cs_bridge_port}")
        
        # Run demo simulation
        print("\n🎯 Running demo simulation...")
        for i in range(10):
            # Generate sample data
            consciousness_data = create_sample_consciousness_data()
            evolution_data = create_sample_evolution_data()
            
            # Visualize data
            await manager.visualize_consciousness_state(consciousness_data)
            await manager.visualize_evolution_progress(evolution_data)
            
            print(f"📈 Iteration {i+1}: Consciousness={consciousness_data['consciousness_index']:.2f}, Evolution={evolution_data['fitness_score']:.2f}")
            
            await asyncio.sleep(2)
            
        # Show status
        status = await manager.get_visualization_status()
        print(f"\n📊 Final Status: {json.dumps(status, indent=2)}")
        
        print("\n✅ Demo completed successfully!")
        print("Press Ctrl+C to stop the visual interface...")
        
        # Keep running until interrupted
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping visual interface...")
            await manager.stop()
            print("✅ Visual interface stopped")
            
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        raise

def validate_mega_module():
    """Validate the visual interface mega-module"""
    print("🔍 Validating AIOS Visual Interface Mega-Module...")
    
    validation_results = {
        'dependencies': validate_visualization_dependencies(),
        'classes': {},
        'functions': {},
        'config': True
    }
    
    # Check classes
    try:
        config = VisualizationConfig()
        validation_results['classes']['VisualizationConfig'] = True
        
        data = VisualizationData(
            timestamp=datetime.now(),
            data_type='test',
            content={},
            metadata={}
        )
        validation_results['classes']['VisualizationData'] = True
        
        engine = ConsciousnessVisualizationEngine(config)
        validation_results['classes']['ConsciousnessVisualizationEngine'] = True
        
        bridge = CSharpVisualInterfaceBridge(config)
        validation_results['classes']['CSharpVisualInterfaceBridge'] = True
        
        dashboard = WebDashboardServer(config)
        validation_results['classes']['WebDashboardServer'] = True
        
        manager = AIOSVisualInterfaceManager(config)
        validation_results['classes']['AIOSVisualInterfaceManager'] = True
        
    except Exception as e:
        validation_results['classes']['error'] = str(e)
        
    # Check utility functions
    try:
        sample_consciousness = create_sample_consciousness_data()
        validation_results['functions']['create_sample_consciousness_data'] = bool(sample_consciousness)
        
        sample_evolution = create_sample_evolution_data()
        validation_results['functions']['create_sample_evolution_data'] = bool(sample_evolution)
        
        ports = get_available_ports(9000, 3)
        validation_results['functions']['get_available_ports'] = len(ports) > 0
        
        template = create_dashboard_template()
        validation_results['functions']['create_dashboard_template'] = len(template) > 1000
        
    except Exception as e:
        validation_results['functions']['error'] = str(e)
        
    # Print results
    print(f"📦 Dependencies: {sum(validation_results['dependencies'].values())}/{len(validation_results['dependencies'])} available")
    print(f"🏗️  Classes: {len([k for k, v in validation_results['classes'].items() if v is True])} validated")
    print(f"🔧 Functions: {len([k for k, v in validation_results['functions'].items() if v is True])} validated")
    
    all_good = (
        all(validation_results['dependencies'].values()) and
        all(v is True for v in validation_results['classes'].values()) and
        all(v is True for v in validation_results['functions'].values())
    )
    
    if all_good:
        print("✅ AIOS Visual Interface Mega-Module validation PASSED")
    else:
        print("⚠️  AIOS Visual Interface Mega-Module validation completed with warnings")
        
    return validation_results

# Main execution
if __name__ == "__main__":
    print("🧠 AIOS Visual Interface Mega-Module (OS0.4)")
    print("=" * 50)
    
    # Validate module
    validation_results = validate_mega_module()
    
    # Ask user if they want to run demo
    try:
        response = input("\n🎯 Run visual interface demo? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            asyncio.run(run_visual_interface_demo())
        else:
            print("✅ Module validation completed. Use import to integrate with other modules.")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")