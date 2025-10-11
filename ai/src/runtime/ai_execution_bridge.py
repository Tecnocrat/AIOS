"""
AIOS AI Execution Bridge
========================

AI-executable runtime bridge providing programmatic access to all AIOS capabilities.
Enables natural language → AIOS function execution without menu navigation.

Key Features:
- Natural language command parsing
- Async execution with result streaming
- Structured JSON responses for AI consumption
- Real-time progress tracking
- Comprehensive error handling

Usage (via AI assistant):
    bridge = AIExecutionBridge()
    await bridge.initialize()
    
    # Natural language: "Check system health"
    results = await bridge.execute("health_check")
    
    # Natural language: "Discover all tools"
    tools = await bridge.execute("discover_tools")
    
    # Streaming: "Test Week 1 integration"
    async for progress in bridge.execute_streaming("test_integration", scope="week1"):
        print(progress)

AINLP Metadata:
    supercell: AI Intelligence Layer
    consciousness_level: HIGH (AI-executable API + natural language interface)
    integration_points: [Unified Dashboard, All AIOS Tools, Runtime Monitor]
    python_version: 3.14
    design_patterns: [Facade, Command, Strategy, Observer]

Author: AIOS Development Team
Date: October 11, 2025
Phase: 10.4 Week 2 Day 3-4
"""

import asyncio
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Tuple

# Import unified dashboard
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.runtime.intelligence_dashboard import (
    UnifiedDashboard,
    ToolDiscovery,
    ComponentLayer,
    ToolStatus
)


class CommandStatus(Enum):
    """Command execution status."""
    SUCCESS = "success"
    ERROR = "error"
    RUNNING = "running"
    CANCELLED = "cancelled"


@dataclass
class BridgeResult:
    """
    Structured result from bridge execution.
    
    Attributes:
        command: Command name executed
        status: Execution status (success/error)
        result: Command result data
        metadata: Additional execution metadata
    """
    command: str
    status: CommandStatus
    result: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            "command": self.command,
            "status": self.status.value,
            "result": self._serialize_result(self.result),
            "metadata": {
                "duration": self.metadata.get("duration", 0),
                "timestamp": self.metadata.get("timestamp", datetime.now().isoformat()),
                "consciousness_impact": self.metadata.get("consciousness_impact", 0.0)
            }
        }
    
    def _serialize_result(self, obj: Any) -> Any:
        """Make result JSON-serializable."""
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, (list, tuple)):
            return [self._serialize_result(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self._serialize_result(v) for k, v in obj.items()}
        elif hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif hasattr(obj, '__dict__'):
            return self._serialize_result(obj.__dict__)
        else:
            return str(obj)


@dataclass
class StreamingProgress:
    """
    Real-time progress update during streaming execution.
    
    Attributes:
        type: Update type (progress/result/error)
        data: Update data payload
        progress: Progress percentage (0.0 to 1.0)
        message: Human-readable status message
        timestamp: Update timestamp
    """
    type: str  # "progress" | "result" | "error"
    data: Any
    progress: float  # 0.0 to 1.0
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            "type": self.type,
            "data": self.data,
            "progress": self.progress,
            "message": self.message,
            "timestamp": self.timestamp.isoformat()
        }


class BridgeError(Exception):
    """Base exception for bridge errors."""
    def __init__(self, command: str, message: str, details: Dict[str, Any] = None):
        self.command = command
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON error response."""
        return {
            "command": self.command,
            "status": "error",
            "error": {
                "message": self.message,
                "type": self.__class__.__name__,
                "details": self.details
            }
        }


class CommandNotFoundError(BridgeError):
    """Command not recognized."""
    pass


class ExecutionError(BridgeError):
    """Command execution failed."""
    pass


class InitializationError(BridgeError):
    """Bridge initialization failed."""
    pass


class AIExecutionBridge:
    """
    AI-executable runtime bridge for AIOS.
    
    Provides programmatic access to all AIOS runtime capabilities:
    - Tool discovery and cataloguing
    - Component execution and orchestration
    - Health monitoring and validation
    - Integration testing
    - Real-time result streaming
    
    Designed for AI assistant consumption via natural language commands.
    """
    
    # Natural language command patterns
    NATURAL_LANGUAGE_MAP = {
        # Health patterns
        "check health": "health_check",
        "system health": "health_check",
        "health status": "health_check",
        "how healthy": "health_check",
        
        # Discovery patterns
        "discover tools": "discover_tools",
        "list tools": "discover_tools",
        "what tools": "discover_tools",
        "find tools": "discover_tools",
        "show me tools": "discover_tools",
        "tool catalogue": "discover_tools",
        
        # Operational patterns
        "operational tools": "list_operational",
        "working tools": "list_operational",
        "what works": "list_operational",
        "active tools": "list_operational",
        
        # Integration patterns
        "test integration": "test_integration",
        "run tests": "test_integration",
        "validate integration": "test_integration",
        "integration tests": "test_integration",
        
        # Dark spots patterns
        "find dark spots": "identify_dark_spots",
        "what's broken": "identify_dark_spots",
        "unused code": "identify_dark_spots",
        "dark spots": "identify_dark_spots",
        
        # Workflow patterns
        "run workflow": "run_workflow",
        "execute workflow": "run_workflow",
        "full cycle": "run_workflow",
        "population workflow": "run_workflow",
        
        # Showcase patterns
        "showcase agents": "showcase_agents",
        "show agents": "showcase_agents",
        "agent demo": "showcase_agents",
        "showcase knowledge": "showcase_knowledge",
        "show knowledge": "showcase_knowledge",
        "knowledge demo": "showcase_knowledge",
        
        # Export patterns
        "export catalogue": "export_catalogue",
        "save catalogue": "export_catalogue",
        "export tools": "export_catalogue",
        
        # Status patterns
        "live status": "get_live_status",
        "system status": "get_live_status",
        "current status": "get_live_status",
    }
    
    def __init__(self, workspace_root: Path = None):
        """
        Initialize AI execution bridge.
        
        Args:
            workspace_root: AIOS workspace root directory
        """
        self.workspace_root = workspace_root or Path.cwd()
        self.dashboard: Optional[UnifiedDashboard] = None
        self.initialized = False
        self.command_map: Dict[str, Callable] = {}
        self._tools_cache: Optional[List[Any]] = None
    
    async def initialize(self) -> Dict[str, Any]:
        """
        Initialize bridge and underlying dashboard.
        
        Returns:
            {
                "status": "initialized",
                "workspace": str,
                "tools_discovered": int,
                "components_available": bool
            }
        """
        try:
            # Initialize dashboard
            self.dashboard = UnifiedDashboard(workspace_root=self.workspace_root)
            await self.dashboard.initialize()
            
            # Build command map
            self._build_command_map()
            
            self.initialized = True
            
            return {
                "status": "initialized",
                "workspace": str(self.workspace_root),
                "tools_discovered": len(self.dashboard.tools),
                "components_available": True,
                "available_commands": len(self.command_map)
            }
            
        except Exception as e:
            raise InitializationError(
                command="initialize",
                message=f"Failed to initialize bridge: {e}",
                details={"workspace": str(self.workspace_root)}
            )
    
    def _build_command_map(self) -> None:
        """Build command name → function mapping."""
        self.command_map = {
            # Discovery commands
            "discover_tools": self._cmd_discover_tools,
            "get_tool_summary": self._cmd_tool_summary,
            "list_operational": self._cmd_list_operational,
            "list_by_layer": self._cmd_list_by_layer,
            
            # Execution commands
            "run_workflow": self._cmd_run_workflow,
            "test_integration": self._cmd_test_integration,
            
            # Monitoring commands
            "health_check": self._cmd_health_check,
            "get_live_status": self._cmd_live_status,
            "identify_dark_spots": self._cmd_identify_dark_spots,
            
            # Showcase commands
            "showcase_agents": self._cmd_showcase_agents,
            "showcase_knowledge": self._cmd_showcase_knowledge,
            "showcase_architecture": self._cmd_showcase_architecture,
            
            # Export commands
            "export_catalogue": self._cmd_export_catalogue,
        }
    
    async def execute(
        self,
        command: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute AIOS command with structured result.
        
        Args:
            command: Natural language or function name
                Examples: "health_check", "check health", "discover_tools"
            **kwargs: Command-specific parameters
            
        Returns:
            {
                "command": str,
                "status": "success" | "error",
                "result": Any,
                "metadata": {...}
            }
        """
        if not self.initialized:
            raise InitializationError(
                command=command,
                message="Bridge not initialized. Call initialize() first."
            )
        
        start_time = datetime.now()
        
        try:
            # Parse natural language → function name
            func_name, parsed_kwargs = self._parse_command(command)
            
            # Merge parsed kwargs with provided kwargs
            merged_kwargs = {**parsed_kwargs, **kwargs}
            
            # Get function
            func = self.command_map.get(func_name)
            if not func:
                raise CommandNotFoundError(
                    command=command,
                    message=f"Command '{func_name}' not found",
                    details={
                        "available_commands": list(self.command_map.keys()),
                        "natural_language_patterns": list(self.NATURAL_LANGUAGE_MAP.keys())
                    }
                )
            
            # Execute function
            result = await func(**merged_kwargs)
            
            # Calculate duration
            duration = (datetime.now() - start_time).total_seconds()
            
            # Create result
            bridge_result = BridgeResult(
                command=func_name,
                status=CommandStatus.SUCCESS,
                result=result,
                metadata={
                    "duration": duration,
                    "timestamp": datetime.now().isoformat(),
                    "consciousness_impact": 0.0  # TODO: Calculate based on operation
                }
            )
            
            return bridge_result.to_dict()
            
        except BridgeError:
            raise
        except Exception as e:
            raise ExecutionError(
                command=command,
                message=f"Command execution failed: {e}",
                details={"kwargs": kwargs}
            )
    
    async def execute_streaming(
        self,
        command: str,
        **kwargs
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Execute command with real-time progress streaming.
        
        Args:
            command: Natural language or function name
            **kwargs: Command-specific parameters
            
        Yields:
            {
                "type": "progress" | "result" | "error",
                "data": Any,
                "progress": float,  # 0.0 to 1.0
                "message": str
            }
        """
        if not self.initialized:
            raise InitializationError(
                command=command,
                message="Bridge not initialized. Call initialize() first."
            )
        
        try:
            # Initial progress
            yield StreamingProgress(
                type="progress",
                data=None,
                progress=0.0,
                message=f"Starting execution of '{command}'..."
            ).to_dict()
            
            # Execute command
            result = await self.execute(command, **kwargs)
            
            # Final result
            yield StreamingProgress(
                type="result",
                data=result,
                progress=1.0,
                message="Execution complete"
            ).to_dict()
            
        except Exception as e:
            yield StreamingProgress(
                type="error",
                data=str(e),
                progress=0.0,
                message=f"Execution failed: {e}"
            ).to_dict()
    
    def _parse_command(self, command: str) -> Tuple[str, Dict[str, Any]]:
        """
        Parse natural language command into function name + parameters.
        
        Args:
            command: Natural language or function name
            
        Returns:
            (function_name, parameters)
        """
        command_lower = command.lower().strip()
        
        # Direct match in natural language map
        if command_lower in self.NATURAL_LANGUAGE_MAP:
            return self.NATURAL_LANGUAGE_MAP[command_lower], {}
        
        # Pattern matching with parameter extraction
        for pattern, func_name in self.NATURAL_LANGUAGE_MAP.items():
            if pattern in command_lower:
                params = self._extract_parameters(command_lower, pattern)
                return func_name, params
        
        # Fallback: assume exact function name
        return command_lower, {}
    
    def _extract_parameters(self, command: str, pattern: str) -> Dict[str, Any]:
        """
        Extract parameters from natural language command.
        
        Args:
            command: Full natural language command
            pattern: Matched pattern
            
        Returns:
            Dictionary of extracted parameters
        """
        params = {}
        
        # Extract layer filter: "in runtime intelligence layer"
        layer_match = re.search(r'in (\w+(?:\s+\w+)*) layer', command)
        if layer_match:
            layer_text = layer_match.group(1).replace(' ', '_').upper()
            # Map to ComponentLayer enum
            layer_mapping = {
                "RUNTIME_INTELLIGENCE": "runtime_intelligence",
                "AI_INTELLIGENCE": "ai_intelligence",
                "INTERFACE": "interface",
                "CORE": "core"
            }
            if layer_text in layer_mapping:
                params["layer"] = layer_mapping[layer_text]
        
        # Extract scope: "Week 1 integration"
        if "week 1" in command or "week1" in command:
            params["scope"] = "week1"
        
        # Extract status filter: "operational tools"
        if "operational" in command:
            params["status"] = "operational"
        
        return params
    
    async def get_available_commands(self) -> List[Dict[str, Any]]:
        """
        List all available commands with descriptions.
        
        Returns:
            [
                {
                    "name": "health_check",
                    "description": "Run system health validation",
                    "parameters": [],
                    "estimated_duration": "5-10s",
                    "natural_language": ["check health", "system health"]
                },
                ...
            ]
        """
        commands = []
        
        # Build natural language reverse map
        nl_reverse_map = {}
        for nl, func in self.NATURAL_LANGUAGE_MAP.items():
            if func not in nl_reverse_map:
                nl_reverse_map[func] = []
            nl_reverse_map[func].append(nl)
        
        for cmd_name, cmd_func in self.command_map.items():
            commands.append({
                "name": cmd_name,
                "description": cmd_func.__doc__.strip() if cmd_func.__doc__ else "",
                "parameters": [],  # TODO: Extract from function signature
                "estimated_duration": "1-10s",
                "natural_language": nl_reverse_map.get(cmd_name, [])
            })
        
        return commands
    
    # ==================== Command Implementations ====================
    
    async def _cmd_discover_tools(self, **kwargs) -> Dict[str, Any]:
        """Discover all AIOS tools with optional filtering."""
        tools = self.dashboard.tools
        
        # Apply filters
        if "layer" in kwargs:
            layer = ComponentLayer(kwargs["layer"])
            tools = [t for t in tools if t.layer == layer]
        
        if "status" in kwargs:
            status = ToolStatus(kwargs["status"])
            tools = [t for t in tools if t.status == status]
        
        return {
            "total": len(tools),
            "tools": [tool.to_dict() for tool in tools]
        }
    
    async def _cmd_tool_summary(self, **kwargs) -> Dict[str, Any]:
        """Get tool discovery summary statistics."""
        tools = self.dashboard.tools
        operational = self.dashboard.discovery.get_operational_tools()
        
        # Count by layer
        by_layer = {}
        for layer in ComponentLayer:
            layer_tools = [t for t in tools if t.layer == layer]
            if layer_tools:
                by_layer[layer.value] = len(layer_tools)
        
        # Count by status
        by_status = {}
        for status in ToolStatus:
            status_tools = [t for t in tools if t.status == status]
            if status_tools:
                by_status[status.value] = len(status_tools)
        
        return {
            "total_tools": len(tools),
            "operational_tools": len(operational),
            "operational_percentage": len(operational) / len(tools) * 100 if tools else 0,
            "by_layer": by_layer,
            "by_status": by_status,
            "duplicates": len(self.dashboard.discovery.duplicates)
        }
    
    async def _cmd_list_operational(self, **kwargs) -> Dict[str, Any]:
        """List only operational tools."""
        operational = self.dashboard.discovery.get_operational_tools()
        
        return {
            "total": len(operational),
            "tools": [tool.to_dict() for tool in operational]
        }
    
    async def _cmd_list_by_layer(self, layer: str = None, **kwargs) -> Dict[str, Any]:
        """List tools by architectural layer."""
        if not layer:
            raise ExecutionError(
                command="list_by_layer",
                message="Parameter 'layer' is required",
                details={"available_layers": [l.value for l in ComponentLayer]}
            )
        
        layer_enum = ComponentLayer(layer)
        layer_tools = self.dashboard.discovery.get_tools_by_layer(layer_enum)
        
        return {
            "layer": layer,
            "total": len(layer_tools),
            "tools": [tool.to_dict() for tool in layer_tools]
        }
    
    async def _cmd_run_workflow(self, **kwargs) -> Dict[str, Any]:
        """Execute full population to consensus workflow."""
        results = await self.dashboard.executor.run_population_to_consensus_workflow()
        return results
    
    async def _cmd_test_integration(self, scope: str = "all", **kwargs) -> Dict[str, Any]:
        """Run integration tests with optional scope filtering."""
        # TODO: Implement integration testing
        # For now, return placeholder
        return {
            "scope": scope,
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "message": "Integration testing not yet implemented"
        }
    
    async def _cmd_health_check(self, **kwargs) -> Dict[str, Any]:
        """Run comprehensive system health check."""
        # Get live status
        status = await self.dashboard.monitor.get_live_status()
        
        # Get dark spots
        dark_spots = await self.dashboard.monitor.identify_dark_spots(self.dashboard.tools)
        
        return {
            "timestamp": status.get("timestamp"),
            "health_score": status.get("integrations", {}).get("health_score", 0),
            "components": status.get("components", {}),
            "dark_spots": len(dark_spots),
            "dark_spot_details": dark_spots[:5]  # First 5
        }
    
    async def _cmd_live_status(self, **kwargs) -> Dict[str, Any]:
        """Get current live system status."""
        return await self.dashboard.monitor.get_live_status()
    
    async def _cmd_identify_dark_spots(self, **kwargs) -> Dict[str, Any]:
        """Identify dark spots (unused/broken components)."""
        dark_spots = await self.dashboard.monitor.identify_dark_spots(self.dashboard.tools)
        
        return {
            "total": len(dark_spots),
            "dark_spots": dark_spots
        }
    
    async def _cmd_showcase_agents(self, **kwargs) -> Dict[str, Any]:
        """Run agent consensus showcase."""
        await self.dashboard.showcase.showcase_agent_consensus()
        return {"status": "showcase_complete", "component": "multi_agent_debate"}
    
    async def _cmd_showcase_knowledge(self, **kwargs) -> Dict[str, Any]:
        """Run knowledge oracle showcase."""
        await self.dashboard.showcase.showcase_knowledge_oracle()
        return {"status": "showcase_complete", "component": "knowledge_oracle"}
    
    async def _cmd_showcase_architecture(self, **kwargs) -> Dict[str, Any]:
        """Run architecture integration showcase."""
        await self.dashboard.showcase.showcase_architecture_integration()
        return {"status": "showcase_complete", "component": "full_architecture"}
    
    async def _cmd_export_catalogue(self, **kwargs) -> Dict[str, Any]:
        """Export tool catalogue to JSON."""
        await self.dashboard.export_tool_catalogue()
        
        output_path = self.workspace_root / "runtime_intelligence" / "tool_catalogue.json"
        
        return {
            "status": "exported",
            "path": str(output_path),
            "total_tools": len(self.dashboard.tools)
        }


async def main():
    """Test bridge functionality."""
    bridge = AIExecutionBridge()
    
    print("=" * 60)
    print("🌉 AI EXECUTION BRIDGE - TEST MODE")
    print("=" * 60)
    
    # Initialize
    print("\n1. Initializing bridge...")
    init_result = await bridge.initialize()
    print(f"✅ {json.dumps(init_result, indent=2)}")
    
    # Test natural language command
    print("\n2. Testing natural language: 'check health'")
    health_result = await bridge.execute("check health")
    print(f"✅ Health Score: {health_result['result']['health_score']}")
    
    # Test tool discovery
    print("\n3. Testing: 'discover tools'")
    tools_result = await bridge.execute("discover tools")
    print(f"✅ Found {tools_result['result']['total']} tools")
    
    # Test tool summary
    print("\n4. Getting tool summary...")
    summary_result = await bridge.execute("get_tool_summary")
    print(f"✅ {summary_result['result']['operational_tools']}/{summary_result['result']['total_tools']} operational ({summary_result['result']['operational_percentage']:.1f}%)")
    
    # Test available commands
    print("\n5. Listing available commands...")
    commands = await bridge.get_available_commands()
    print(f"✅ {len(commands)} commands available")
    for cmd in commands[:5]:  # Show first 5
        print(f"   - {cmd['name']}: {cmd['description'][:50]}...")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
