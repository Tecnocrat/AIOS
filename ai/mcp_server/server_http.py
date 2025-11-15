#!/usr/bin/env python3
"""
AIOS MCP Server - HTTP Mode
Remote-accessible version for Termux or always-on deployment
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add AIOS paths
WORKSPACE_ROOT = Path(os.environ.get("AIOS_WORKSPACE", Path(__file__).parent.parent.parent))
sys.path.insert(0, str(WORKSPACE_ROOT / "ai" / "src"))

from aiohttp import web
import json

from mcp.server import Server
from mcp.server.stdio import stdio_server

# Import AIOS MCP components
from resources import AIOSResourceProvider
from tools import AIOSToolProvider
from prompts import AIOSPromptProvider
from diagnostics import DiagnosticsCollector

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [AIOS-MCP-HTTP] %(message)s',
    handlers=[
        logging.FileHandler(WORKSPACE_ROOT / "tachyonic" / "mcp_server_http.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AIOSMCPHTTPServer:
    """HTTP-accessible MCP server for remote deployment (Termux, cloud, etc.)"""
    
    def __init__(self, workspace_root: Path, host: str = "0.0.0.0", port: int = 8001):
        self.workspace_root = workspace_root
        self.host = host
        self.port = port
        
        # Initialize MCP components
        self.resource_provider = AIOSResourceProvider(workspace_root)
        self.tool_provider = AIOSToolProvider(workspace_root)
        self.prompt_provider = AIOSPromptProvider(workspace_root)
        self.diagnostics = DiagnosticsCollector(workspace_root)
        
        # HTTP app
        self.app = web.Application()
        self._setup_routes()
    
    def _setup_routes(self):
        """Configure HTTP API routes"""
        self.app.router.add_get("/", self.handle_info)
        self.app.router.add_get("/health", self.handle_health)
        self.app.router.add_get("/resources", self.handle_list_resources)
        self.app.router.add_get("/resources/{uri:.*}", self.handle_get_resource)
        self.app.router.add_get("/tools", self.handle_list_tools)
        self.app.router.add_post("/tools/{name}", self.handle_call_tool)
        self.app.router.add_get("/prompts", self.handle_list_prompts)
        self.app.router.add_get("/prompts/{name}", self.handle_get_prompt)
        self.app.router.add_get("/diagnostics", self.handle_diagnostics)
    
    async def handle_info(self, request: web.Request) -> web.Response:
        """Server information endpoint"""
        info = {
            "name": "AIOS MCP Server (HTTP Mode)",
            "version": "1.0.0",
            "mode": "http",
            "workspace": str(self.workspace_root),
            "endpoints": {
                "health": "/health",
                "resources": "/resources",
                "tools": "/tools",
                "prompts": "/prompts",
                "diagnostics": "/diagnostics"
            },
            "biological_architecture": "Dendritic Communication",
            "ainlp_compliant": True
        }
        return web.json_response(info)
    
    async def handle_health(self, request: web.Request) -> web.Response:
        """Health check endpoint"""
        try:
            # Quick health checks
            resources = await self.resource_provider.list_resources()
            tools = await self.tool_provider.list_tools()
            prompts = await self.prompt_provider.list_prompts()
            
            health = {
                "status": "healthy",
                "timestamp": self._get_timestamp(),
                "resources_count": len(resources),
                "tools_count": len(tools),
                "prompts_count": len(prompts),
                "workspace": str(self.workspace_root)
            }
            return web.json_response(health)
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return web.json_response(
                {"status": "unhealthy", "error": str(e)},
                status=500
            )
    
    async def handle_list_resources(self, request: web.Request) -> web.Response:
        """List available resources"""
        try:
            resources = await self.resource_provider.list_resources()
            return web.json_response({
                "resources": [
                    {
                        "uri": r.uri,
                        "name": r.name,
                        "description": r.description,
                        "mimeType": r.mimeType
                    }
                    for r in resources
                ]
            })
        except Exception as e:
            logger.error(f"Failed to list resources: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def handle_get_resource(self, request: web.Request) -> web.Response:
        """Get specific resource content"""
        try:
            uri = request.match_info['uri']
            # Reconstruct full URI
            full_uri = f"aios://{uri}"
            
            content = await self.resource_provider.read_resource(full_uri)
            return web.json_response({
                "uri": full_uri,
                "content": content,
                "timestamp": self._get_timestamp()
            })
        except Exception as e:
            logger.error(f"Failed to get resource {uri}: {e}")
            return web.json_response({"error": str(e)}, status=404)
    
    async def handle_list_tools(self, request: web.Request) -> web.Response:
        """List available tools"""
        try:
            tools = await self.tool_provider.list_tools()
            return web.json_response({
                "tools": [
                    {
                        "name": t.name,
                        "description": t.description,
                        "inputSchema": t.inputSchema
                    }
                    for t in tools
                ]
            })
        except Exception as e:
            logger.error(f"Failed to list tools: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def handle_call_tool(self, request: web.Request) -> web.Response:
        """Execute tool with arguments"""
        try:
            name = request.match_info['name']
            args = await request.json()
            
            result = await self.tool_provider.call_tool(name, args)
            return web.json_response({
                "tool": name,
                "result": result,
                "timestamp": self._get_timestamp()
            })
        except Exception as e:
            logger.error(f"Failed to call tool {name}: {e}")
            return web.json_response({"error": str(e)}, status=400)
    
    async def handle_list_prompts(self, request: web.Request) -> web.Response:
        """List available prompts"""
        try:
            prompts = await self.prompt_provider.list_prompts()
            return web.json_response({
                "prompts": [
                    {
                        "name": p.name,
                        "description": p.description,
                        "arguments": p.arguments if hasattr(p, 'arguments') else []
                    }
                    for p in prompts
                ]
            })
        except Exception as e:
            logger.error(f"Failed to list prompts: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    async def handle_get_prompt(self, request: web.Request) -> web.Response:
        """Get prompt with optional arguments"""
        try:
            name = request.match_info['name']
            # Get query parameters as arguments
            args = dict(request.query)
            
            prompt_data = await self.prompt_provider.get_prompt(name, args)
            return web.json_response({
                "prompt": name,
                "content": prompt_data,
                "timestamp": self._get_timestamp()
            })
        except Exception as e:
            logger.error(f"Failed to get prompt {name}: {e}")
            return web.json_response({"error": str(e)}, status=404)
    
    async def handle_diagnostics(self, request: web.Request) -> web.Response:
        """Get comprehensive diagnostics"""
        try:
            include_warnings = request.query.get("warnings", "true").lower() == "true"
            include_info = request.query.get("info", "false").lower() == "true"
            
            diagnostics = await self.diagnostics.collect_all(
                include_warnings=include_warnings,
                include_info=include_info
            )
            return web.json_response(diagnostics)
        except Exception as e:
            logger.error(f"Failed to collect diagnostics: {e}")
            return web.json_response({"error": str(e)}, status=500)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    async def start(self):
        """Start HTTP server"""
        logger.info("="*60)
        logger.info("AIOS Model Context Protocol Server v1.0.0 (HTTP Mode)")
        logger.info("Biological Architecture: Dendritic Communication")
        logger.info("AINLP Compliant: Enhancement Over Creation")
        logger.info("="*60)
        logger.info(f"Initializing AIOS MCP HTTP Server for workspace: {self.workspace_root}")
        logger.info(f"Server will listen on http://{self.host}:{self.port}")
        
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        
        logger.info("AIOS MCP HTTP Server started successfully")
        logger.info(f"API available at: http://{self.host}:{self.port}")
        logger.info(f"Health check: http://{self.host}:{self.port}/health")
        logger.info(f"Resources: http://{self.host}:{self.port}/resources")
        logger.info(f"Tools: http://{self.host}:{self.port}/tools")
        logger.info(f"Prompts: http://{self.host}:{self.port}/prompts")
        logger.info(f"Diagnostics: http://{self.host}:{self.port}/diagnostics")
        
        # Keep running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Shutting down AIOS MCP HTTP Server...")
            await runner.cleanup()


async def main():
    """Main entry point"""
    # Get configuration from environment
    workspace = Path(os.environ.get("AIOS_WORKSPACE", Path.cwd()))
    host = os.environ.get("AIOS_MCP_HOST", "0.0.0.0")
    port = int(os.environ.get("AIOS_MCP_PORT", "8001"))
    
    server = AIOSMCPHTTPServer(workspace, host, port)
    await server.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
