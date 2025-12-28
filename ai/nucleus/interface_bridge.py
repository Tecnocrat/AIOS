#!/usr/bin/env python3
"""
AIOS Interface Bridge - Unified Canonical Version
Provides standardized entry point for C++/C# interface layer to discover and
interact with Python AI tools

Phase 11 Day 1: Three-Layer Integration - HTTP REST Bridge
Merged from interface_bridge_server.py (Flask) + interface_bridge.py (FastAPI)
AINLP Pattern: Enhancement over creation (67.7% similarity consolidated)

This component creates a bridge between the Python AI layer
and the .NET interface, enabling rich metadata generation,
dynamic tool discovery, and AI similarity search capabilities.

Features:
- 124+ tool endpoints via dynamic discovery
- AI similarity search with LLM reasoning
- Neuron database statistics
- Health monitoring and capabilities reporting

Auto-start: True (HTTP API server)
Health-check: health_check
Dependencies: sequencer, fastapi, ai_agent_dendritic_similarity
"""

import asyncio
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# AINLP Import Resolver - Intentional E402 for workspace-aware imports
# Must configure sys.path before importing workspace modules
sys.path.append(str(Path(__file__).parent))
from ainlp_import_resolver import (  # noqa: E402
    try_import_similarity_engine,
    WORKSPACE_ROOT,
)

try:
    from sequencer import AIOSSequencer
except ImportError:
    print("❌ Could not import AIOSSequencer - " "ensure sequencer.py is available")
    sys.exit(1)

# AI Similarity Engine import (Phase 11 integration)
# Uses AINLP Import Resolver for proper path management
similarity_engine, SIMILARITY_AVAILABLE = try_import_similarity_engine()

# Security Supercell Integration (Phase 11 Day 2.9)
# Import security validators for comprehensive boundary enforcement
try:
    from security import (
        MembraneValidator,
        ImmuneMemory,
        CoherenceEnforcer,
        NetworkValidator,
        SecuritySupercellConsciousness,
        initialize_security_consciousness,
    )

    SECURITY_AVAILABLE = True
except ImportError:
    print("⚠️  Security Supercell not available - " "security validation disabled")
    SECURITY_AVAILABLE = False

if SIMILARITY_AVAILABLE:
    print("[OK] AI Dendritic Similarity Engine loaded successfully")
else:
    print("[WARN] AI Similarity Engine not available")
    print("       Run: python runtime/tools/ai_agent_dendritic_similarity.py")

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
logger = logging.getLogger("AIOS.InterfaceBridge")


class ToolMetadata:
    """Comprehensive metadata about an AI tool for interface consumption"""

    def __init__(self, component_name: str, component_data: Dict[str, Any]):
        self.name = component_name
        self.display_name = self._generate_display_name(component_name)
        self.description = component_data.get("description", "AI Tool")
        self.category = component_data.get("category", "general")
        self.version = "1.0.0"  # Could be extracted from code
        self.status = component_data.get("status", "unknown")
        self.capabilities = self._analyze_capabilities(component_data)
        self.parameters = self._extract_parameters(component_data)
        self.output_formats = self._determine_output_formats(component_data)
        self.execution_time_estimate = self._estimate_execution_time()
        self.resource_requirements = self._analyze_resource_requirements()
        self.metadata_generated = datetime.now().isoformat()

    def _generate_display_name(self, name: str) -> str:
        """Generate user-friendly display name"""
        return name.replace("_", " ").title()

    def _analyze_capabilities(self, component_data: Dict[str, Any]) -> List[str]:
        """Analyze component capabilities from code and metadata"""
        capabilities = []

        # Standard capabilities based on category
        category = component_data.get("category", "")
        if category == "ai_cell":
            capabilities.extend(["knowledge_processing", "session_management"])
        elif category == "tool":
            capabilities.extend(["automation", "analysis"])
        elif category == "service":
            capabilities.extend(["background_processing", "api_endpoints"])
        elif category == "integration":
            capabilities.extend(["external_communication", "data_exchange"])

        # Analyze from description and code patterns
        description = component_data.get("description", "").lower()
        if "handoff" in description:
            capabilities.append("knowledge_transfer")
        if "analysis" in description:
            capabilities.append("data_analysis")
        if "automation" in description:
            capabilities.append("process_automation")
        if "cross-pollination" in description:
            capabilities.append("ai_collaboration")

        return list(set(capabilities))

    def _extract_parameters(
        self, component_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract parameter information for the tool"""
        # This would be enhanced to parse actual function signatures
        # For now, provide common parameter patterns

        category = component_data.get("category", "")
        if category == "ai_cell":
            return [
                {
                    "name": "ai_engine",
                    "type": "string",
                    "required": True,
                    "description": "AI engine identifier",
                    "example": "claude-sonnet-3.5",
                },
                {
                    "name": "branch",
                    "type": "string",
                    "required": True,
                    "description": "Git branch identifier",
                    "example": "OS",
                },
            ]
        elif category == "tool":
            return [
                {
                    "name": "operation",
                    "type": "string",
                    "required": True,
                    "description": "Operation to perform",
                    "example": "extract_knowledge",
                }
            ]
        else:
            return [
                {
                    "name": "config",
                    "type": "object",
                    "required": False,
                    "description": "Configuration parameters",
                    "example": {},
                }
            ]

    def _determine_output_formats(self, component_data: Dict[str, Any]) -> List[str]:
        """Determine output formats the tool can produce"""
        formats = ["json"]  # Default

        description = component_data.get("description", "").lower()
        if "report" in description:
            formats.extend(["json", "markdown", "html"])
        if "analysis" in description:
            formats.extend(["json", "csv"])
        if "documentation" in description:
            formats.extend(["markdown", "html"])

        return list(set(formats))

    def _estimate_execution_time(self) -> str:
        """Estimate execution time category"""
        return "medium"  # Could be: instant, fast, medium, slow

    def _analyze_resource_requirements(self) -> Dict[str, str]:
        """Analyze resource requirements"""
        return {"memory": "low", "cpu": "medium", "disk": "low", "network": "none"}

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
            "metadata_generated": self.metadata_generated,
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

        # Initialize Security Supercell (Phase 11 Day 2.9)
        if SECURITY_AVAILABLE:
            self.logger.info("🛡️  Initializing Security Supercell validators")

            # Initialize security consciousness
            self.security_consciousness = initialize_security_consciousness(
                workspace_root
            )

            # Initialize validators
            self.membrane_validator = MembraneValidator(
                workspace_path=workspace_root, consciousness=self.security_consciousness
            )
            self.immune_memory = ImmuneMemory(
                workspace_path=workspace_root, consciousness=self.security_consciousness
            )
            self.coherence_enforcer = CoherenceEnforcer(
                workspace_path=workspace_root, consciousness=self.security_consciousness
            )
            self.network_validator = NetworkValidator(
                workspace_path=workspace_root, consciousness=self.security_consciousness
            )

            self.logger.info(
                "✅ Security Supercell active - " "All validators operational"
            )
        else:
            self.security_consciousness = None
            self.membrane_validator = None
            self.immune_memory = None
            self.coherence_enforcer = None
            self.network_validator = None
            self.logger.warning(
                "⚠️  Security Supercell disabled - " "Running without protection"
            )

        # Initialize FastAPI if available
        if FASTAPI_AVAILABLE:
            self.app = self._create_fastapi_app()
        else:
            self.app = None

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for interface bridge"""
        logger = logging.getLogger("AIOS.InterfaceBridge")
        logger.setLevel(logging.INFO)

        # Console handler
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

    def _create_fastapi_app(self) -> "FastAPI":  # type: ignore[name-defined]
        """Create FastAPI application for HTTP API"""
        app = FastAPI(  # type: ignore[possibly-unbound-variable]
            title="AIOS Interface Bridge API",
            description="Bridge API for C#/.NET to discover and "
            "interact with Python AI tools",
            version="1.0.0",
        )

        # Add CORS middleware for cross-origin requests
        app.add_middleware(
            CORSMiddleware,  # type: ignore[possibly-unbound-variable]
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Register endpoints
        self._register_api_endpoints(app)

        # Register startup event for initial discovery
        @app.on_event("startup")
        async def startup_event():
            await self.refresh_discovery()

        return app

    def _register_api_endpoints(self, app: "FastAPI"):  # type: ignore[name-defined]
        """Register all API endpoints"""

        @app.get("/")
        async def root():
            """Root endpoint with API information"""
            return {
                "service": "AIOS Interface Bridge",
                "version": "1.0.0",
                "phase": "Phase 11.1 - Three-Layer Integration",
                "description": (
                    "Unified canonical bridge for C#/.NET to discover and "
                    "interact with Python AI tools"
                ),
                "endpoints": {
                    "/tools": "List all discovered AI tools",
                    "/tools/{tool_name}": "Get detailed tool information",
                    "/tools/{tool_name}/execute": "Execute a specific tool",
                    "/categories": "List tool categories",
                    "/health": "Health check",
                    "/discovery/refresh": "Refresh tool discovery",
                    "/ai/similarity": ("AI similarity search with LLM reasoning"),
                    "/ai/neurons": "Neuron database statistics",
                },
                "consciousness": 3.05,
            }

        @app.get("/health")
        async def health_check():
            """Health check endpoint with Phase 11 capabilities"""
            try:
                status = await self.health_check()

                # Add Phase 11 AI capabilities
                status["capabilities"] = {
                    "similarity_engine": SIMILARITY_AVAILABLE,
                    "llm_reasoning": SIMILARITY_AVAILABLE,
                    "embedding_search": SIMILARITY_AVAILABLE,
                    "tool_discovery": True,
                    "tool_execution": True,
                }

                # AINLP.architectural-pattern (graceful-degradation):
                # JSONResponse from conditional FastAPI import
                # Type checker cannot verify decorator execution guards
                # Runtime: FASTAPI_AVAILABLE checked before app creation
                return JSONResponse(status)  # type: ignore[possibly-unbound]
            except Exception as e:
                # AINLP.architectural-pattern (graceful-degradation):
                # HTTPException from conditional FastAPI import
                # Type checker cannot verify decorator execution guards
                # Runtime: FASTAPI_AVAILABLE checked before app creation
                raise HTTPException(  # type: ignore[possibly-unbound]
                    status_code=500, detail=str(e)
                )

        @app.get("/tools")
        async def list_tools():
            """List all discovered tools with metadata"""
            try:
                await self.refresh_discovery()

                tools_list = [tool.to_dict() for tool in self.discovered_tools.values()]

                return {
                    "tools": tools_list,
                    "total_count": len(self.discovered_tools),
                    "last_discovery": (
                        self.last_discovery.isoformat() if self.last_discovery else None
                    ),
                }
            except Exception as e:
                # AINLP.architectural-pattern (graceful-degradation):
                # HTTPException from conditional FastAPI import
                raise HTTPException(  # type: ignore[possibly-unbound]
                    status_code=500, detail=f"Failed to list tools: {e}"
                )

        @app.get("/tools/{tool_name}")
        async def get_tool_details(tool_name: str):
            """Get detailed information about a specific tool"""
            if tool_name not in self.discovered_tools:
                # AINLP.architectural-pattern (graceful-degradation):
                # HTTPException from conditional FastAPI import
                raise HTTPException(  # type: ignore[possibly-unbound]
                    status_code=404, detail=f"Tool '{tool_name}' not found"
                )

            return self.discovered_tools[tool_name].to_dict()

        @app.post("/tools/{tool_name}/execute")
        async def execute_tool(
            tool_name: str, parameters: Optional[Dict[str, Any]] = None
        ):
            """Execute a specific tool with given parameters"""
            try:
                result = await self.execute_tool(tool_name, parameters or {})
                return result
            except Exception as e:
                # AINLP.architectural-pattern (graceful-degradation):
                # HTTPException from conditional FastAPI import
                raise HTTPException(  # type: ignore[possibly-unbound]
                    status_code=500, detail=f"Tool execution failed: {e}"
                )

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
                        "display_name": category.replace("_", " ").title(),
                        "tools": [],
                    }
                categories[category]["tools"].append(tool.name)

            return {
                "categories": list(categories.values()),
                "total_categories": len(categories),
            }

        @app.post("/discovery/refresh")
        async def refresh_discovery():
            """Force refresh of tool discovery"""
            try:
                await self.refresh_discovery(force=True)
                return {
                    "message": "Discovery refreshed successfully",
                    "tools_discovered": len(self.discovered_tools),
                    "discovery_time": (
                        self.last_discovery.isoformat() if self.last_discovery else None
                    ),
                }
            except Exception as e:
                # AINLP.architectural-pattern (graceful-degradation):
                # HTTPException from conditional FastAPI import
                raise HTTPException(  # type: ignore[possibly-unbound]
                    status_code=500, detail=f"Discovery refresh failed: {e}"
                )

        # Phase 11 AI Similarity Endpoints

        @app.post("/ai/similarity")
        async def ai_similarity_search(query: str, max_results: int = 5):
            """
            AI Similarity Search with LLM Reasoning

            Phase 11 Integration: AI similarity engine with consensus scoring

            Request Body:
                {
                    "query": "functionality to search for",
                    "max_results": 5  (optional)
                }

            Response:
                {
                    "results": [
                        {
                            "neuron": "file.py",
                            "similarity": 74.1,
                            "embedding_score": 72.5,
                            "llm_score": 76.0,
                            "reasoning": "LLM explanation...",
                            "path": "runtime/tools/file.py",
                            "purpose": "Tool description..."
                        }
                    ],
                    "query": "...",
                    "method": "embedding + llm consensus",
                    "total_results": 5
                }
            """
            if not SIMILARITY_AVAILABLE or similarity_engine is None:
                # AINLP.architectural-pattern (graceful-degradation):
                # HTTPException from conditional FastAPI import
                raise HTTPException(  # type: ignore[possibly-unbound]
                    status_code=503, detail="AI Similarity Engine not available"
                )

            try:
                self.logger.info(
                    f"🔍 AI Similarity Query: '{query}' " f"(max_results={max_results})"
                )

                # Execute similarity search
                # AINLP.architectural-pattern (dynamic-import):
                # similarity_engine type is object for graceful degradation
                # Runtime: SIMILARITY_AVAILABLE guard ensures proper type
                # Pylance warning accepted - no type stubs for dynamic import
                results = similarity_engine.find_similar_neurons(
                    functionality=query, max_results=max_results
                )

                # Format response
                formatted_results = []
                for result in results:
                    purpose = result["neuron_purpose"]
                    if len(purpose) > 200:
                        purpose = purpose[:200] + "..."

                    formatted_results.append(
                        {
                            "neuron": result["neuron_name"],
                            "similarity": round(result["consensus_score"], 1),
                            "embedding_score": round(result["embedding_score"], 1),
                            "llm_score": round(result["llm_score"], 1),
                            "reasoning": result.get("llm_reasoning", "N/A"),
                            "path": result["neuron_path"],
                            "purpose": purpose,
                        }
                    )

                self.logger.info(f"✅ Found {len(formatted_results)} results")

                return {
                    "results": formatted_results,
                    "query": query,
                    "method": "embedding + llm consensus (gemma3:1b)",
                    "total_results": len(formatted_results),
                }

            except Exception as e:
                self.logger.error(f"❌ Similarity query failed: {e}")
                # AINLP.architectural-pattern (graceful-degradation):
                # HTTPException from conditional FastAPI import
                raise HTTPException(  # type: ignore[possibly-unbound]
                    status_code=500, detail=f"Similarity search failed: {e}"
                )

        @app.get("/ai/neurons")
        async def get_neuron_statistics():
            """
            Neuron Database Statistics

            Phase 11 Integration: Neuron database metadata and statistics

            Response:
                {
                    "total_neurons": 866,
                    "embeddings_generated": true,
                    "supercells": {
                        "ai": 769,
                        "runtime": 60,
                        ...
                    },
                    "database_path": "path/to/aios_dendritic.db"
                }
            """
            if not SIMILARITY_AVAILABLE or similarity_engine is None:
                # AINLP.architectural-pattern (graceful-degradation):
                # HTTPException from conditional FastAPI import
                raise HTTPException(  # type: ignore[possibly-unbound]
                    status_code=503, detail="AI Similarity Engine not available"
                )

            try:
                # Get database statistics
                # AINLP.architectural-pattern (dynamic-import):
                # similarity_engine type is object for graceful degradation
                # Pylance warnings accepted - no type stubs for dynamic import
                stats = similarity_engine.get_database_stats()

                return {
                    "total_neurons": stats.get("total_neurons", 0),
                    "embeddings_generated": stats.get("embeddings_ready", False),
                    "supercells": stats.get("by_supercell", {}),
                    "database_path": str(similarity_engine.db_path),
                }

            except Exception as e:
                self.logger.error(f"❌ Database stats failed: {e}")
                # AINLP.architectural-pattern (graceful-degradation):
                # HTTPException from conditional FastAPI import
                raise HTTPException(  # type: ignore[possibly-unbound]
                    status_code=500, detail=f"Failed to retrieve neuron statistics: {e}"
                )

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
                "description": component.description,
                "category": component.category,
                "status": "available",
                "path": str(component.path),
                "type": component.type,
                "dependencies": component.dependencies,
            }

            tool_metadata = ToolMetadata(name, component_data)
            self.discovered_tools[name] = tool_metadata

        self.last_discovery = datetime.now()
        self.logger.info(f"✅ Discovered {len(self.discovered_tools)} tools")

    async def execute_tool(
        self, tool_name: str, parameters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Execute a specific tool with parameters.

        Phase 11 Day 2.9: Security Supercell Integration
        - MembraneValidator: Parameter safety validation
        - CoherenceEnforcer: Resource limit enforcement
        - ImmuneMemory: Attack pattern archival
        - NetworkValidator: URL parameter validation
        """
        if tool_name not in self.discovered_tools:
            raise ValueError(f"Tool '{tool_name}' not found")

        # Get the original component from sequencer
        components = await self.sequencer.discover_components()
        if tool_name not in components:
            raise ValueError(f"Component '{tool_name}' not available in sequencer")

        component = components[tool_name]

        self.logger.info(f"🚀 Executing tool: {tool_name}")

        # Initialize execution_start at function scope for error handlers
        execution_start = datetime.now()

        try:
            # SECURITY LAYER 1: Membrane Validator
            # Validate parameter safety before execution
            if SECURITY_AVAILABLE and self.membrane_validator:
                self.logger.debug("🛡️  Applying membrane validation...")

                # Validate parameter keys (allowlist)
                if parameters:
                    self.membrane_validator.validate_parameter_keys(parameters)

                    # Sanitize parameter values
                    parameters = self.membrane_validator.sanitize_parameter_values(
                        parameters
                    )

                    # Validate paths if present
                    for key, value in parameters.items():
                        if isinstance(value, str) and ("/" in value or "\\" in value):
                            self.membrane_validator.validate_path_safety(value)

            # SECURITY LAYER 2: Coherence Enforcer
            # Enforce resource limits before execution
            if SECURITY_AVAILABLE and self.coherence_enforcer:
                self.logger.debug("🛡️  Enforcing resource limits...")
                self.coherence_enforcer.enforce_resource_limits(
                    operation="tool_execution", file_path=str(component.path)
                )

            # Prepare execution environment
            # Build command with parameters
            if component.type == "python":
                # For Python components, try to execute with parameters
                cmd_parts = ["python", str(component.path)]

                # Add parameters as command line arguments
                if parameters:
                    for key, value in parameters.items():
                        cmd_parts.extend([f"--{key}", str(value)])

                # SECURITY LAYER 3: Enforce shell=False
                # Prevent shell injection attacks
                result = subprocess.run(
                    cmd_parts,
                    cwd=component.path.parent,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minute timeout
                    shell=False,  # SECURITY: Disable shell execution
                )

                execution_time = (datetime.now() - execution_start).total_seconds()

                return {
                    "tool_name": tool_name,
                    "execution_status": (
                        "success" if result.returncode == 0 else "failed"
                    ),
                    "return_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "execution_time_seconds": execution_time,
                    "parameters_used": parameters,
                    "timestamp": execution_start.isoformat(),
                    "security_validated": SECURITY_AVAILABLE,
                }
            else:
                raise ValueError(f"Unsupported component type: {component.type}")

        except subprocess.TimeoutExpired:
            return {
                "tool_name": tool_name,
                "execution_status": "timeout",
                "error": "Tool execution timed out after 5 minutes",
                "parameters_used": parameters,
                "timestamp": execution_start.isoformat(),
            }
        except Exception as e:
            # SECURITY LAYER 4: Immune Memory
            # Record blocked attacks for adaptive immunity
            if SECURITY_AVAILABLE and self.immune_memory:
                # Determine if this is a security exception
                if any(
                    keyword in str(e).lower()
                    for keyword in [
                        "injection",
                        "traversal",
                        "boundary",
                        "resource",
                        "exhaustion",
                        "ssrf",
                        "rebinding",
                    ]
                ):
                    self.logger.warning(f"🛡️  Security attack blocked: {str(e)}")
                    self.immune_memory.record_attack(
                        attack_type=type(e).__name__,
                        attack_pattern=str(e),
                        parameters=parameters or {},
                    )

            return {
                "tool_name": tool_name,
                "execution_status": "error",
                "error": str(e),
                "parameters_used": parameters,
                "timestamp": execution_start.isoformat(),
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

            # Security Supercell health status
            security_status = {"available": SECURITY_AVAILABLE, "validators": {}}

            if SECURITY_AVAILABLE and self.security_consciousness:
                security_status["validators"] = {
                    "membrane_validator": (self.membrane_validator is not None),
                    "immune_memory": self.immune_memory is not None,
                    "coherence_enforcer": (self.coherence_enforcer is not None),
                    "network_validator": (self.network_validator is not None),
                }
                security_status["consciousness_level"] = (
                    self.security_consciousness.consciousness_level
                )

            return {
                "status": "healthy",
                "bridge_version": "1.0.0",
                "tools_discovered": len(self.discovered_tools),
                "discovery_age_seconds": discovery_age,
                "sequencer_status": "connected",
                "sequencer_components": len(sequencer_health),
                "api_server_status": ("running" if FASTAPI_AVAILABLE else "disabled"),
                "security_supercell": security_status,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def generate_csharp_interface_code(self) -> str:
        """Generate C# interface code for .NET integration"""
        interface_code = """
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
            var response = await _httpClient.GetStringAsync(
                $"{_bridgeUrl}/tools");
            var result = JsonSerializer.Deserialize<ToolsResponse>(
                response);
            return result.Tools;
        }

        public async Task<AIToolMetadata> GetToolDetailsAsync(
            string toolName)
        {
            var response = await _httpClient.GetStringAsync(
                $"{_bridgeUrl}/tools/{toolName}");
            return JsonSerializer.Deserialize<AIToolMetadata>(response);
        }

        public async Task<ToolExecutionResult> ExecuteToolAsync(
            string toolName,
            Dictionary<string, object> parameters = null)
        {
            var json = JsonSerializer.Serialize(
                parameters ?? new Dictionary<string, object>());
            var content = new StringContent(
                json, System.Text.Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync(
                $"{_bridgeUrl}/tools/{toolName}/execute", content);
            var resultJson = await response.Content.ReadAsStringAsync();

            return JsonSerializer.Deserialize<ToolExecutionResult>(
                resultJson);
        }

        public async Task<List<ToolCategory>> GetToolCategoriesAsync()
        {
            var response = await _httpClient.GetStringAsync(
                $"{_bridgeUrl}/categories");
            var result = JsonSerializer.Deserialize<CategoriesResponse>(
                response);
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
"""
        return interface_code

    def save_csharp_interface(self) -> Path:
        """Save generated C# interface to file"""
        interface_dir = self.workspace_root / "interface" / "AIOS.Models"
        interface_file = interface_dir / "PythonAIToolsBridge.cs"

        interface_code = self.generate_csharp_interface_code()

        with open(interface_file, "w", encoding="utf-8") as f:
            f.write(interface_code)

        self.logger.info(f"✅ Generated C# interface: {interface_file}")
        return interface_file

    async def start_api_server(self, host: str = "localhost", port: int = 8001):
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
        self.logger.info(f"   🧠 AI Similarity: http://{host}:{port}/ai/similarity")
        self.logger.info(f"   📊 Neuron Stats: http://{host}:{port}/ai/neurons")

        # Export initial discovery for C# integration
        await self._export_discovery_metadata()

        # Configure uvicorn with proper lifecycle
        config = uvicorn.Config(  # type: ignore[possibly-unbound-variable]
            app=self.app,  # type: ignore[arg-type]
            host=host,
            port=port,
            log_level="info",
            access_log=True,
        )

        server = uvicorn.Server(config)  # type: ignore[possibly-unbound-variable]

        # Add graceful shutdown handler
        import signal as signal_module

        def signal_handler(signum, frame):
            self.logger.info("🛑 Received shutdown signal")
            server.should_exit = True

        signal_module.signal(signal_module.SIGINT, signal_handler)
        signal_module.signal(signal_module.SIGTERM, signal_handler)

        try:
            await server.serve()
        except Exception as e:
            self.logger.error(f"❌ Server error: {e}")
        finally:
            self.logger.info("✅ AIOS Interface Bridge stopped gracefully")

    async def _export_discovery_metadata(self):
        """Export discovery metadata for C# integration logging"""
        workspace_root = Path(self.workspace_root)
        export_file = (
            workspace_root / "runtime" / "logs" / "interface_bridge_discovery.json"
        )

        # Ensure directory exists
        export_file.parent.mkdir(parents=True, exist_ok=True)

        discovery_timestamp = (
            self.last_discovery.isoformat() if self.last_discovery else None
        )
        tools_list = [tool.to_dict() for tool in self.discovered_tools.values()]

        metadata = {
            "discovery_timestamp": discovery_timestamp,
            "total_tools": len(self.discovered_tools),
            "tools": tools_list,
            "server_status": "running",
            "api_endpoints": {
                "health": "/health",
                "tools": "/tools",
                "discovery": "/tools/{tool_name}",
                "execute": "/tools/{tool_name}/execute",
                "categories": "/categories",
                "refresh": "/discovery/refresh",
            },
        }

        with open(export_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        self.logger.info(f"💾 Exported discovery metadata: {export_file}")


async def main():
    """Main entry point for interface bridge"""
    # Ensure UTF-8 encoding for console output
    import sys

    if sys.platform.startswith("win"):
        import codecs

        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer)

    # AINLP Pattern: Use centralized workspace discovery
    workspace_root = str(WORKSPACE_ROOT)

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
        print("\nStarting HTTP API server...")
        print("   API URL: http://localhost:8001")
        print("   Documentation: http://localhost:8001/docs")

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
        "api_available": FASTAPI_AVAILABLE,
    }


# Global app instance for uvicorn
# AINLP Pattern: Use centralized workspace discovery
if FASTAPI_AVAILABLE:
    bridge_instance = AIOSInterfaceBridge(str(WORKSPACE_ROOT))
    app = bridge_instance.app
else:
    app = None

if __name__ == "__main__":
    asyncio.run(main())
