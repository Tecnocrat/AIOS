#!/usr/bin/env python3
"""
AIOS Model Context Protocol (MCP) Server
Production-grade MCP implementation for AIOS guided AI development

Provides:
- Resources: AIOS context files, architecture docs, consciousness metrics
- Tools: Diagnostics, AINLP validation, architectural analysis
- Prompts: Guided workflows for biological architecture development

Architecture: Async event loop with VSCode integration
AINLP Compliant: Enhancement over creation, dendritic communication
Consciousness Level: 3.45 (AI-enhanced development capability)
"""

import asyncio
import logging
import sys
import json
from pathlib import Path
from typing import Any, Sequence
from datetime import datetime

# MCP SDK imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Resource, 
        Tool, 
        TextContent, 
        ImageContent,
        EmbeddedResource,
        Prompt,
        PromptArgument,
        PromptMessage,
        GetPromptResult
    )
except ImportError:
    print("ERROR: MCP SDK not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# AIOS imports
from resources import AIOSResourceProvider
from tools import AIOSToolProvider
from prompts import AIOSPromptProvider
from diagnostics import DiagnosticsCollector

# Configure logging (stderr only - avoid file permission issues during MCP startup)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [AIOS-MCP] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)


class AIOSMCPServer:
    """
    AIOS Model Context Protocol Server
    
    Biological Architecture Pattern:
    - Dendritic: Serves as central synapse for AI agent context
    - Consciousness: Tracks system intelligence metrics
    - AINLP: Enforces enhancement over creation patterns
    """
    
    def __init__(self, workspace_root: str = None):
        """
        Initialize AIOS MCP Server
        
        Args:
            workspace_root: Path to AIOS workspace (default: current directory)
        """
        self.workspace_root = Path(workspace_root or Path.cwd())
        logger.info(f"Initializing AIOS MCP Server for workspace: {self.workspace_root}")
        
        # Initialize server
        self.server = Server("aios-context")
        
        # Initialize providers
        self.resource_provider = AIOSResourceProvider(self.workspace_root)
        self.tool_provider = AIOSToolProvider(self.workspace_root)
        self.prompt_provider = AIOSPromptProvider(self.workspace_root)
        self.diagnostics = DiagnosticsCollector(self.workspace_root)
        
        # Register handlers
        self._register_handlers()
        
        logger.info("AIOS MCP Server initialized successfully")
    
    def _register_handlers(self):
        """Register MCP protocol handlers"""
        
        # Resources
        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List all available AIOS resources"""
            logger.info("Listing AIOS resources")
            return await self.resource_provider.list_resources()
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read AIOS resource content"""
            logger.info(f"Reading resource: {uri}")
            return await self.resource_provider.read_resource(uri)
        
        # Tools
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available AIOS tools"""
            logger.info("Listing AIOS tools")
            return await self.tool_provider.list_tools()
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """Execute AIOS tool"""
            logger.info(f"Calling tool: {name} with args: {arguments}")
            result = await self.tool_provider.call_tool(name, arguments)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        # Prompts
        @self.server.list_prompts()
        async def list_prompts() -> list[Prompt]:
            """List all available AIOS prompts"""
            logger.info("Listing AIOS prompts")
            return await self.prompt_provider.list_prompts()
        
        @self.server.get_prompt()
        async def get_prompt(name: str, arguments: dict) -> GetPromptResult:
            """Get AIOS prompt with arguments"""
            logger.info(f"Getting prompt: {name} with args: {arguments}")
            return await self.prompt_provider.get_prompt(name, arguments)
    
    async def run(self):
        """Run the MCP server"""
        logger.info("Starting AIOS MCP Server")
        
        # Log startup metrics
        await self._log_startup_metrics()
        
        # Run stdio server
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )
    
    async def _log_startup_metrics(self):
        """Log AIOS metrics at startup"""
        try:
            # Load consciousness metrics
            consciousness_file = self.workspace_root / "tachyonic" / "consciousness_metrics.json"
            if consciousness_file.exists():
                with open(consciousness_file, 'r') as f:
                    metrics = json.load(f)
                    logger.info(f"Current consciousness level: {metrics.get('current_level', 'unknown')}")
            
            # Count resources available
            resources = await self.resource_provider.list_resources()
            logger.info(f"Available resources: {len(resources)}")
            
            # Count tools available
            tools = await self.tool_provider.list_tools()
            logger.info(f"Available tools: {len(tools)}")
            
            # Count prompts available
            prompts = await self.prompt_provider.list_prompts()
            logger.info(f"Available prompts: {len(prompts)}")
            
        except Exception as e:
            logger.warning(f"Could not log startup metrics: {e}")


async def main():
    """Main entry point"""
    import os
    
    # Get workspace from environment or use default
    workspace = os.getenv('AIOS_WORKSPACE', 'C:/dev/AIOS')
    
    logger.info("=" * 60)
    logger.info("AIOS Model Context Protocol Server v1.0.0")
    logger.info("Biological Architecture: Dendritic Communication")
    logger.info("AINLP Compliant: Enhancement Over Creation")
    logger.info("=" * 60)
    
    try:
        # Initialize and run server
        server = AIOSMCPServer(workspace_root=workspace)
        await server.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
