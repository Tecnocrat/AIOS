#!/usr/bin/env python3
"""
AIOS Interface Bridge
Provides standardized entry point for C++/C# interface layer to discover and interact with Python AI tools

This component creates a bridge between the Python AI layer and the .NET interface,
enabling rich metadata generation and dynamic tool discovery for the UI.

Auto-start: True (HTTP API server)
Health-check: health_check
Dependencies: sequencer, fastapi
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import asdict
import subprocess
import importlib.util

# Add core to path for sequencer import
sys.path.append(str(Path(__file__).parent))

try:
    from sequencer import AIOSSequencer
except ImportError:
    print("❌ Could not import AIOSSequencer - ensure sequencer.py is available")
    sys.exit(1)

# FastAPI imports
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    print("⚠️  FastAPI not available - HTTP API will be disabled")
    FASTAPI_AVAILABLE = False

# Setup logging
logger = logging.getLogger('AIOS.InterfaceBridge')


class ToolMetadata:
    """Comprehensive metadata about an AI tool for interface consumption"""
    
    def __init__(self, component_name: str, component_data: Dict[str, Any]):
        self.name = component_name
        self.display_name = self._generate_display_name(component_name)
        self.description = component_data.get('description', 'AI Tool')
        self.category = component_data.get('category', 'general')
        self.version = "1.0.0"  # Could be extracted from code
        self.status = component_data.get('status', 'unknown')
        self.capabilities = self._analyze_capabilities(component_data)
        self.parameters = self._extract_parameters(component_data)
        self.output_formats = self._determine_output_formats(component_data)
        self.execution_time_estimate = self._estimate_execution_time()
        self.resource_requirements = self._analyze_resource_requirements()
        self.metadata_generated = datetime.now().isoformat()
    
    def _generate_display_name(self, name: str) -> str:
        """Generate user-friendly display name"""
        return name.replace('_', ' ').title()
    
    def _analyze_capabilities(self, component_data: Dict[str, Any]) -> List[str]:
        """Analyze component capabilities from code and metadata"""
        capabilities = []
        
        # Standard capabilities based on category
        category = component_data.get('category', '')
        if category == 'ai_cell':
            capabilities.extend(['knowledge_processing', 'session_management'])
        elif category == 'tool':
            capabilities.extend(['automation', 'analysis'])
        elif category == 'service':
            capabilities.extend(['background_processing', 'api_endpoints'])
        elif category == 'integration':
            capabilities.extend(['external_communication', 'data_exchange'])
        
        # Analyze from description and code patterns
        description = component_data.get('description', '').lower()
        if 'handoff' in description:
            capabilities.append('knowledge_transfer')
        if 'analysis' in description:
            capabilities.append('data_analysis')
        if 'automation' in description:
            capabilities.append('process_automation')
        if 'cross-pollination' in description:
            capabilities.append('ai_collaboration')
        
        return list(set(capabilities))
    
    def _extract_parameters(self, component_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract parameter information for the tool"""
        # This would be enhanced to parse actual function signatures
        # For now, provide common parameter patterns
        
        category = component_data.get('category', '')
        if category == 'ai_cell':
            return [
                {
                    "name": "ai_engine",
                    "type": "string",
                    "required": True,
                    "description": "AI engine identifier",
                    "example": "claude-sonnet-3.5"
                },
                {
                    "name": "branch",
                    "type": "string", 
                    "required": True,
                    "description": "Git branch identifier",
                    "example": "OS"
                }
            ]
        elif category == 'tool':
            return [
                {
                    "name": "operation",
                    "type": "string",
                    "required": True,
                    "description": "Operation to perform",
                    "example": "extract_knowledge"
                }
            ]
        else:
            return [
                {
                    "name": "config",
                    "type": "object",
                    "required": False,
                    "description": "Configuration parameters",
                    "example": {}
                }
            ]
    
    def _determine_output_formats(self, component_data: Dict[str, Any]) -> List[str]:
        """Determine output formats the tool can produce"""
        formats = ['json']  # Default
        
        description = component_data.get('description', '').lower()
        if 'report' in description:
            formats.extend(['json', 'markdown', 'html'])
        if 'analysis' in description:
            formats.extend(['json', 'csv'])
        if 'documentation' in description:
            formats.extend(['markdown', 'html'])
        
        return list(set(formats))
    
    def _estimate_execution_time(self) -> str:
        """Estimate execution time category"""
        return "medium"  # Could be: instant, fast, medium, slow
    
    def _analyze_resource_requirements(self) -> Dict[str, str]:
        """Analyze resource requirements"""
        return {
            "memory": "low",
            "cpu": "medium", 
            "disk": "low",
            "network": "none"
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "category": self.category,
            "version": self.version,
            "status": self.status,
            "capabilities": self.capabilities,
            "parameters": self.parameters,
            "output_formats": self.output_formats,
            "execution_time_estimate": self.execution_time_estimate,
            "resource_requirements": self.resource_requirements,
            "metadata_generated": self.metadata_generated
        }


class AIOSInterfaceBridge:
    """
    Main interface bridge between Python AI tools and C#/.NET interface
    """
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.sequencer = AIOSSequencer(workspace_root)
        self.discovered_tools: Dict[str, ToolMetadata] = {}
        self.last_discovery = None
        self.api_server = None
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Initialize FastAPI if available
        if FASTAPI_AVAILABLE:
            self.app = self._create_fastapi_app()
        else:
            self.app = None
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for interface bridge"""
        logger = logging.getLogger('AIOS.InterfaceBridge')
        logger.setLevel(logging.INFO)
        
        # Console handler
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        return logger
    
    def _create_fastapi_app(self) -> FastAPI:
        """Create FastAPI application for HTTP API"""
        app = FastAPI(
            title="AIOS Interface Bridge API",
            description="Bridge API for C#/.NET to discover and interact with Python AI tools",
            version="1.0.0"
        )
        
        # Add CORS middleware for cross-origin requests
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Register endpoints
        self._register_api_endpoints(app)
        
        return app
    
    def _register_api_endpoints(self, app: FastAPI):
        """Register all API endpoints"""
        
        @app.get("/")
        async def root():
            """Root endpoint with API information"""
            return {
                "service": "AIOS Interface Bridge",
                "version": "1.0.0",
                "description": "Bridge API for discovering and executing Python AI tools",
                "endpoints": {
                    "/tools": "List all discovered AI tools",
                    "/tools/{tool_name}": "Get detailed tool information",
                    "/tools/{tool_name}/execute": "Execute a specific tool",
                    "/categories": "List tool categories",
                    "/health": "Health check",
                    "/discovery/refresh": "Refresh tool discovery"
                }
            }
        
        @app.get("/health")
        async def health_check():
            """Health check endpoint"""
            try:
                status = await self.health_check()
                return JSONResponse(status)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/tools")
        async def list_tools():
            """List all discovered tools with metadata"""
            try:
                await self.refresh_discovery()
                return {
                    "tools": [tool.to_dict() for tool in self.discovered_tools.values()],
                    "total_count": len(self.discovered_tools),
                    "last_discovery": self.last_discovery.isoformat() if self.last_discovery else None
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to list tools: {e}")
        
        @app.get("/tools/{tool_name}")
        async def get_tool_details(tool_name: str):
            """Get detailed information about a specific tool"""
            if tool_name not in self.discovered_tools:
                raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
            
            return self.discovered_tools[tool_name].to_dict()
        
        @app.post("/tools/{tool_name}/execute")
        async def execute_tool(tool_name: str, parameters: Dict[str, Any] = None):
            """Execute a specific tool with given parameters"""
            try:
                result = await self.execute_tool(tool_name, parameters or {})
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Tool execution failed: {e}")
        
        @app.get("/categories")
        async def list_categories():
            """List all tool categories"""
            await self.refresh_discovery()
            categories = {}
            for tool in self.discovered_tools.values():
                category = tool.category
                if category not in categories:
                    categories[category] = {
                        "name": category,
                        "display_name": category.replace('_', ' ').title(),
                        "tools": []
                    }
                categories[category]["tools"].append(tool.name)
            
            return {
                "categories": list(categories.values()),
                "total_categories": len(categories)
            }
        
        @app.post("/discovery/refresh")
        async def refresh_discovery():
            """Force refresh of tool discovery"""
            try:
                await self.refresh_discovery(force=True)
                return {
                    "message": "Discovery refreshed successfully",
                    "tools_discovered": len(self.discovered_tools),
                    "discovery_time": self.last_discovery.isoformat()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Discovery refresh failed: {e}")
    
    async def refresh_discovery(self, force: bool = False):
        """Refresh tool discovery from sequencer"""
        # Only refresh if forced or if it's been more than 5 minutes
        if not force and self.last_discovery:
            time_since_last = datetime.now() - self.last_discovery
            if time_since_last.total_seconds() < 300:  # 5 minutes
                return
        
        self.logger.info("🔍 Refreshing tool discovery...")
        
        # Discover components using sequencer
        components = await self.sequencer.discover_components()
        
        # Generate metadata for each component
        self.discovered_tools = {}
        for name, component in components.items():
            component_data = {
                'description': component.description,
                'category': component.category,
                'status': 'available',
                'path': str(component.path),
                'type': component.type,
                'dependencies': component.dependencies
            }
            
            tool_metadata = ToolMetadata(name, component_data)
            self.discovered_tools[name] = tool_metadata
        
        self.last_discovery = datetime.now()
        self.logger.info(f"✅ Discovered {len(self.discovered_tools)} tools")
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific tool with parameters"""
        if tool_name not in self.discovered_tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        # Get the original component from sequencer
        components = await self.sequencer.discover_components()
        if tool_name not in components:
            raise ValueError(f"Component '{tool_name}' not available in sequencer")
        
        component = components[tool_name]
        
        self.logger.info(f"🚀 Executing tool: {tool_name}")
        
        try:
            # Prepare execution environment
            execution_start = datetime.now()
            
            # Build command with parameters
            if component.type == 'python':
                # For Python components, try to execute with parameters
                cmd_parts = ["python", str(component.path)]
                
                # Add parameters as command line arguments
                for key, value in parameters.items():
                    cmd_parts.extend([f"--{key}", str(value)])
                
                # Execute the command
                result = subprocess.run(
                    cmd_parts,
                    cwd=component.path.parent,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                
                execution_time = (datetime.now() - execution_start).total_seconds()
                
                return {
                    "tool_name": tool_name,
                    "execution_status": "success" if result.returncode == 0 else "failed",
                    "return_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "execution_time_seconds": execution_time,
                    "parameters_used": parameters,
                    "timestamp": execution_start.isoformat()
                }
            else:
                raise ValueError(f"Unsupported component type: {component.type}")
                
        except subprocess.TimeoutExpired:
            return {
                "tool_name": tool_name,
                "execution_status": "timeout",
                "error": "Tool execution timed out after 5 minutes",
                "parameters_used": parameters,
                "timestamp": execution_start.isoformat()
            }
        except Exception as e:
            return {
                "tool_name": tool_name,
                "execution_status": "error",
                "error": str(e),
                "parameters_used": parameters,
                "timestamp": execution_start.isoformat()
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check of the interface bridge"""
        try:
            # Check sequencer health
            sequencer_health = await self.sequencer.health_check_all()
            
            # Check tool discovery freshness
            discovery_age = None
            if self.last_discovery:
                discovery_age = (datetime.now() - self.last_discovery).total_seconds()
            
            return {
                "status": "healthy",
                "bridge_version": "1.0.0",
                "tools_discovered": len(self.discovered_tools),
                "discovery_age_seconds": discovery_age,
                "sequencer_status": "connected",
                "sequencer_components": len(sequencer_health),
                "api_server_status": "running" if FASTAPI_AVAILABLE else "disabled",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_csharp_interface_code(self) -> str:
        """Generate C# interface code for .NET integration"""
        interface_code = '''
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Text.Json;
using System.Net.Http;

namespace AIOS.Models
{
    /// <summary>
    /// Generated interface for Python AI Tools Bridge
    /// Automatically generated from AIOS Interface Bridge discovery
    /// </summary>
    public class PythonAIToolsBridge
    {
        private readonly HttpClient _httpClient;
        private readonly string _bridgeUrl;
        
        public PythonAIToolsBridge(string bridgeUrl = "http://localhost:8000")
        {
            _bridgeUrl = bridgeUrl;
            _httpClient = new HttpClient();
        }
        
        public async Task<List<AIToolMetadata>> GetAvailableToolsAsync()
        {
            var response = await _httpClient.GetStringAsync($"{_bridgeUrl}/tools");
            var result = JsonSerializer.Deserialize<ToolsResponse>(response);
            return result.Tools;
        }
        
        public async Task<AIToolMetadata> GetToolDetailsAsync(string toolName)
        {
            var response = await _httpClient.GetStringAsync($"{_bridgeUrl}/tools/{toolName}");
            return JsonSerializer.Deserialize<AIToolMetadata>(response);
        }
        
        public async Task<ToolExecutionResult> ExecuteToolAsync(string toolName, Dictionary<string, object> parameters = null)
        {
            var json = JsonSerializer.Serialize(parameters ?? new Dictionary<string, object>());
            var content = new StringContent(json, System.Text.Encoding.UTF8, "application/json");
            
            var response = await _httpClient.PostAsync($"{_bridgeUrl}/tools/{toolName}/execute", content);
            var resultJson = await response.Content.ReadAsStringAsync();
            
            return JsonSerializer.Deserialize<ToolExecutionResult>(resultJson);
        }
        
        public async Task<List<ToolCategory>> GetToolCategoriesAsync()
        {
            var response = await _httpClient.GetStringAsync($"{_bridgeUrl}/categories");
            var result = JsonSerializer.Deserialize<CategoriesResponse>(response);
            return result.Categories;
        }
    }
    
    public class AIToolMetadata
    {
        public string Name { get; set; }
        public string DisplayName { get; set; }
        public string Description { get; set; }
        public string Category { get; set; }
        public string Version { get; set; }
        public string Status { get; set; }
        public List<string> Capabilities { get; set; }
        public List<ToolParameter> Parameters { get; set; }
        public List<string> OutputFormats { get; set; }
        public string ExecutionTimeEstimate { get; set; }
        public ResourceRequirements ResourceRequirements { get; set; }
        public DateTime MetadataGenerated { get; set; }
    }
    
    public class ToolParameter
    {
        public string Name { get; set; }
        public string Type { get; set; }
        public bool Required { get; set; }
        public string Description { get; set; }
        public object Example { get; set; }
    }
    
    public class ResourceRequirements
    {
        public string Memory { get; set; }
        public string Cpu { get; set; }
        public string Disk { get; set; }
        public string Network { get; set; }
    }
    
    public class ToolExecutionResult
    {
        public string ToolName { get; set; }
        public string ExecutionStatus { get; set; }
        public int? ReturnCode { get; set; }
        public string Stdout { get; set; }
        public string Stderr { get; set; }
        public double ExecutionTimeSeconds { get; set; }
        public Dictionary<string, object> ParametersUsed { get; set; }
        public DateTime Timestamp { get; set; }
    }
    
    public class ToolCategory
    {
        public string Name { get; set; }
        public string DisplayName { get; set; }
        public List<string> Tools { get; set; }
    }
    
    public class ToolsResponse
    {
        public List<AIToolMetadata> Tools { get; set; }
        public int TotalCount { get; set; }
        public DateTime? LastDiscovery { get; set; }
    }
    
    public class CategoriesResponse
    {
        public List<ToolCategory> Categories { get; set; }
        public int TotalCategories { get; set; }
    }
}
'''
        return interface_code
    
    def save_csharp_interface(self) -> Path:
        """Save generated C# interface to file"""
        interface_dir = self.workspace_root / "interface" / "AIOS.Models"
        interface_file = interface_dir / "PythonAIToolsBridge.cs"
        
        interface_code = self.generate_csharp_interface_code()
        
        with open(interface_file, 'w', encoding='utf-8') as f:
            f.write(interface_code)
        
        self.logger.info(f"✅ Generated C# interface: {interface_file}")
        return interface_file
    
    async def start_api_server(self, host: str = "localhost", port: int = 8000):
        """Start the HTTP API server with proper lifecycle management"""
        if not FASTAPI_AVAILABLE:
            self.logger.error("❌ FastAPI not available - cannot start API server")
            return
        
        # Initial discovery
        await self.refresh_discovery()
        
        # Generate C# interface
        self.save_csharp_interface()
        
        self.logger.info(f"🚀 Starting AIOS Interface Bridge API on {host}:{port}")
        self.logger.info(f"   📖 Documentation: http://{host}:{port}/docs")
        self.logger.info(f"   🔧 Health Check: http://{host}:{port}/health")
        
        # Export initial discovery for C# integration
        await self._export_discovery_metadata()
        
        # Configure uvicorn with proper lifecycle
        config = uvicorn.Config(
            app=self.app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
        
        server = uvicorn.Server(config)
        
        # Add graceful shutdown handler
        import signal
        
        def signal_handler(signum, frame):
            self.logger.info("🛑 Received shutdown signal")
            server.should_exit = True
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            await server.serve()
        except Exception as e:
            self.logger.error(f"❌ Server error: {e}")
        finally:
            self.logger.info("✅ AIOS Interface Bridge stopped gracefully")
    
    async def _export_discovery_metadata(self):
        """Export discovery metadata for C# integration logging"""
        workspace_root = Path(self.workspace_root)
        export_file = workspace_root / "runtime_intelligence" / "logs" / "interface_bridge_discovery.json"
        
        # Ensure directory exists
        export_file.parent.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            "discovery_timestamp": self.last_discovery.isoformat() if self.last_discovery else None,
            "total_tools": len(self.discovered_tools),
            "tools": [tool.to_dict() for tool in self.discovered_tools.values()],
            "server_status": "running",
            "api_endpoints": {
                "health": "/health",
                "tools": "/tools",
                "discovery": "/tools/{tool_name}",
                "execute": "/tools/{tool_name}/execute",
                "categories": "/categories",
                "refresh": "/discovery/refresh"
            }
        }
        
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"💾 Exported discovery metadata: {export_file}")


async def main():
    """Main entry point for interface bridge"""
    # Ensure UTF-8 encoding for console output
    import sys
    if sys.platform.startswith('win'):
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)
    
    workspace_root = r"C:\dev\AIOS"
    
    bridge = AIOSInterfaceBridge(workspace_root)
    
    print("AIOS Interface Bridge Starting...")
    print("=" * 50)
    
    # Initial discovery
    await bridge.refresh_discovery()
    print(f"Discovered {len(bridge.discovered_tools)} AI tools")
    
    # Show discovered tools
    print("\nAvailable Tools:")
    for tool_name, tool_metadata in bridge.discovered_tools.items():
        print(f"   • {tool_metadata.display_name} ({tool_metadata.category})")
    
    # Start API server if FastAPI is available
    if FASTAPI_AVAILABLE:
        print(f"\nStarting HTTP API server...")
        print(f"   API URL: http://localhost:8000")
        print(f"   Documentation: http://localhost:8000/docs")
        
        try:
            await bridge.start_api_server()
        except KeyboardInterrupt:
            print("\nInterface Bridge stopped")
    else:
        print("\nFastAPI not available - HTTP API disabled")
        print("Install with: pip install fastapi uvicorn")


def run():
    """Sequencer-compatible run method"""
    logger.info("AIOS Interface Bridge is ready for startup")


def health_check() -> Dict[str, Any]:
    """Sequencer-compatible health check"""
    return {
        "status": "available",
        "service": "interface_bridge",
        "api_available": FASTAPI_AVAILABLE
    }


if __name__ == "__main__":
    asyncio.run(main())