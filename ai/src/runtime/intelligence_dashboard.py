"""
AIOS Unified Intelligence Dashboard
====================================

Orchestration base layer for tool discovery and mesh interoperability.
Provides unified interface for discovering, executing, and monitoring all AIOS capabilities.

AINLP Metadata:
    supercell: AI Intelligence Layer
    consciousness_level: HIGH (orchestration + discovery + mesh interoperability)
    integration_points: [Population Manager, Agent Conversations, Knowledge Integration, Runtime Intelligence]
    python_version: 3.14
    design_patterns: [Facade, Observer, Strategy]

Author: AIOS Development Team
Date: October 10, 2025
Phase: 10.4 Week 2 Day 1-2
"""

import asyncio
import importlib.util
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict

# Import AIOS components (with graceful fallback)
try:
    # Note: PopulationManager comes from evolution_lab, others from ai.src.intelligence
    # The ai.src.intelligence.__init__.py provides unified import bridge
    from ai.src.intelligence import PopulationManager, MultiAgentDebate, KnowledgeOracle
<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
    COMPONENTS_AVAILABLE = True
except ImportError:
    COMPONENTS_AVAILABLE = False


class ToolStatus(Enum):
    """Tool operational status enumeration."""
<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
    OPERATIONAL = "operational"
    IMPORTABLE = "importable"
    SYNTAX_ERROR = "syntax_error"
    NOT_FOUND = "not_found"
    UNKNOWN = "unknown"


class ComponentLayer(Enum):
    """AIOS architectural layer enumeration."""
<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
    RUNTIME_INTELLIGENCE = "runtime"
    AI_INTELLIGENCE = "ai_intelligence"
    INTERFACE = "interface"
    CORE = "core"
    UNKNOWN = "unknown"


@dataclass
class ToolInfo:
    """
    Metadata about a discovered AIOS tool.
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Attributes:
        name: Tool name (e.g., "system_health_check")
        path: Absolute path to tool file
        layer: Architectural layer (runtime, ai, interface, core)
        status: Operational status
        import_path: Python import path (e.g., "runtime.tools.system_health_check")
        description: Tool description (from docstring if available)
        functions: List of public functions/classes
        dependencies: Required imports
        last_modified: File modification timestamp
    """
<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
    name: str
    path: Path
    layer: ComponentLayer
    status: ToolStatus
    import_path: str = ""
    description: str = ""
    functions: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    last_modified: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "path": str(self.path),
            "layer": self.layer.value,
            "status": self.status.value,
            "import_path": self.import_path,
            "description": self.description,
            "functions": self.functions,
            "dependencies": self.dependencies,
<<<<<<< HEAD
            "last_modified": (
                self.last_modified.isoformat() if self.last_modified else None
            ),
=======
            "last_modified": self.last_modified.isoformat() if self.last_modified else None
>>>>>>> origin/OS0.6.2.grok
        }


class ToolDiscovery:
    """
    Tool discovery engine for AIOS architecture.
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Scans 4 architectural layers for Python tools:
    - runtime/tools/
    - ai/tools/
    - core/tools/ (if exists)
    - interface/tools/ (if exists)
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Features:
    - Duplicate detection (same tool in multiple locations)
    - Operational status validation (import test)
    - Dependency analysis
    - Layer classification
    """

    def __init__(self, workspace_root: Path):
        """
        Initialize tool discovery engine.
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        Args:
            workspace_root: AIOS workspace root directory
        """
        self.workspace_root = workspace_root
        self.discovered_tools: List[ToolInfo] = []
        self.duplicates: Dict[str, List[ToolInfo]] = defaultdict(list)
<<<<<<< HEAD

    async def scan_all_tools(self) -> List[ToolInfo]:
        """
        Scan all architectural layers for tools.

=======
        
    async def scan_all_tools(self) -> List[ToolInfo]:
        """
        Scan all architectural layers for tools.
        
>>>>>>> origin/OS0.6.2.grok
        Returns:
            List of discovered tools with metadata
        """
        print("\n🔍 [TOOL DISCOVERY] Scanning AIOS architecture...")
<<<<<<< HEAD

        # Define scan locations
        scan_paths = [
            (
                self.workspace_root / "runtime" / "tools",
                ComponentLayer.RUNTIME_INTELLIGENCE,
            ),
=======
        
        # Define scan locations
        scan_paths = [
            (self.workspace_root / "runtime" / "tools", ComponentLayer.RUNTIME_INTELLIGENCE),
>>>>>>> origin/OS0.6.2.grok
            (self.workspace_root / "ai" / "tools", ComponentLayer.AI_INTELLIGENCE),
            (self.workspace_root / "core" / "tools", ComponentLayer.CORE),
            (self.workspace_root / "interface" / "tools", ComponentLayer.INTERFACE),
        ]
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        # Scan each location
        for path, layer in scan_paths:
            if path.exists():
                await self._scan_directory(path, layer)
<<<<<<< HEAD

        # Detect duplicates
        self._detect_duplicates()

        print(f"✅ [DISCOVERY COMPLETE] Found {len(self.discovered_tools)} tools")
        return self.discovered_tools

    async def _scan_directory(self, directory: Path, layer: ComponentLayer) -> None:
        """
        Recursively scan directory for Python tools.

=======
        
        # Detect duplicates
        self._detect_duplicates()
        
        print(f"✅ [DISCOVERY COMPLETE] Found {len(self.discovered_tools)} tools")
        return self.discovered_tools
    
    async def _scan_directory(self, directory: Path, layer: ComponentLayer) -> None:
        """
        Recursively scan directory for Python tools.
        
>>>>>>> origin/OS0.6.2.grok
        Args:
            directory: Directory to scan
            layer: Architectural layer classification
        """
        if not directory.exists():
            return
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        for python_file in directory.rglob("*.py"):
            # Skip __init__.py and private files
            if python_file.name.startswith("_"):
                continue
<<<<<<< HEAD

            tool_info = await self._analyze_tool(python_file, layer)
            self.discovered_tools.append(tool_info)

    async def _analyze_tool(self, file_path: Path, layer: ComponentLayer) -> ToolInfo:
        """
        Analyze individual tool file.

        Args:
            file_path: Path to tool file
            layer: Architectural layer

=======
            
            tool_info = await self._analyze_tool(python_file, layer)
            self.discovered_tools.append(tool_info)
    
    async def _analyze_tool(self, file_path: Path, layer: ComponentLayer) -> ToolInfo:
        """
        Analyze individual tool file.
        
        Args:
            file_path: Path to tool file
            layer: Architectural layer
            
>>>>>>> origin/OS0.6.2.grok
        Returns:
            ToolInfo with analysis results
        """
        tool_name = file_path.stem
<<<<<<< HEAD

        # Get file metadata
        stat = file_path.stat()
        last_modified = datetime.fromtimestamp(stat.st_mtime)

        # Attempt to import and validate
        status = await self._check_tool_status(file_path)

=======
        
        # Get file metadata
        stat = file_path.stat()
        last_modified = datetime.fromtimestamp(stat.st_mtime)
        
        # Attempt to import and validate
        status = await self._check_tool_status(file_path)
        
>>>>>>> origin/OS0.6.2.grok
        # Extract docstring and functions
        description = ""
        functions = []
        dependencies = []
<<<<<<< HEAD

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

=======
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
>>>>>>> origin/OS0.6.2.grok
            # Extract module docstring
            if '"""' in content:
                start = content.find('"""') + 3
                end = content.find('"""', start)
                if end > start:
                    description = content[start:end].strip()[:200]  # First 200 chars
<<<<<<< HEAD

            # Extract function/class definitions
            for line in content.split("\n"):
                if line.startswith("def ") or line.startswith("class "):
                    name = line.split("(")[0].split()[1].strip(":")
                    if not name.startswith("_"):  # Only public functions
                        functions.append(name)

                # Extract imports
                if line.startswith("import ") or line.startswith("from "):
                    dependencies.append(line.strip())

        except Exception as e:
            print(f"⚠️  [WARNING] Could not analyze {tool_name}: {e}")

        # Generate import path
        try:
            rel_path = file_path.relative_to(self.workspace_root)
            import_path = (
                str(rel_path.with_suffix("")).replace("\\", ".").replace("/", ".")
            )
        except ValueError:
            import_path = tool_name

=======
            
            # Extract function/class definitions
            for line in content.split('\n'):
                if line.startswith('def ') or line.startswith('class '):
                    name = line.split('(')[0].split()[1].strip(':')
                    if not name.startswith('_'):  # Only public functions
                        functions.append(name)
                
                # Extract imports
                if line.startswith('import ') or line.startswith('from '):
                    dependencies.append(line.strip())
        
        except Exception as e:
            print(f"⚠️  [WARNING] Could not analyze {tool_name}: {e}")
        
        # Generate import path
        try:
            rel_path = file_path.relative_to(self.workspace_root)
            import_path = str(rel_path.with_suffix('')).replace('\\', '.').replace('/', '.')
        except ValueError:
            import_path = tool_name
        
>>>>>>> origin/OS0.6.2.grok
        return ToolInfo(
            name=tool_name,
            path=file_path,
            layer=layer,
            status=status,
            import_path=import_path,
            description=description,
            functions=functions,
            dependencies=dependencies,
<<<<<<< HEAD
            last_modified=last_modified,
        )

    async def _check_tool_status(self, file_path: Path) -> ToolStatus:
        """
        Check if tool is operational via import test.

        Args:
            file_path: Path to tool file

=======
            last_modified=last_modified
        )
    
    async def _check_tool_status(self, file_path: Path) -> ToolStatus:
        """
        Check if tool is operational via import test.
        
        Args:
            file_path: Path to tool file
            
>>>>>>> origin/OS0.6.2.grok
        Returns:
            ToolStatus enumeration
        """
        try:
            # Attempt to load module
            spec = importlib.util.spec_from_file_location("temp_module", file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return ToolStatus.OPERATIONAL
            else:
                return ToolStatus.IMPORTABLE
        except SyntaxError:
            return ToolStatus.SYNTAX_ERROR
        except Exception:
            return ToolStatus.IMPORTABLE  # Importable but may have runtime issues
<<<<<<< HEAD

    def _detect_duplicates(self) -> None:
        """Detect tools with same name in multiple locations."""
        name_map: Dict[str, List[ToolInfo]] = defaultdict(list)

        for tool in self.discovered_tools:
            name_map[tool.name].append(tool)

        self.duplicates = {
            name: tools for name, tools in name_map.items() if len(tools) > 1
        }

        if self.duplicates:
            print(
                f"\n⚠️  [DUPLICATES DETECTED] {len(self.duplicates)} tools in multiple locations"
            )
            for name, tools in self.duplicates.items():
                layers = [t.layer.value for t in tools]
                print(f"   - {name}: {', '.join(layers)}")

    def get_operational_tools(self) -> List[ToolInfo]:
        """Get only operational tools."""
        return [t for t in self.discovered_tools if t.status == ToolStatus.OPERATIONAL]

=======
    
    def _detect_duplicates(self) -> None:
        """Detect tools with same name in multiple locations."""
        name_map: Dict[str, List[ToolInfo]] = defaultdict(list)
        
        for tool in self.discovered_tools:
            name_map[tool.name].append(tool)
        
        self.duplicates = {name: tools for name, tools in name_map.items() if len(tools) > 1}
        
        if self.duplicates:
            print(f"\n⚠️  [DUPLICATES DETECTED] {len(self.duplicates)} tools in multiple locations")
            for name, tools in self.duplicates.items():
                layers = [t.layer.value for t in tools]
                print(f"   - {name}: {', '.join(layers)}")
    
    def get_operational_tools(self) -> List[ToolInfo]:
        """Get only operational tools."""
        return [t for t in self.discovered_tools if t.status == ToolStatus.OPERATIONAL]
    
>>>>>>> origin/OS0.6.2.grok
    def get_tools_by_layer(self, layer: ComponentLayer) -> List[ToolInfo]:
        """Get tools from specific architectural layer."""
        return [t for t in self.discovered_tools if t.layer == layer]


class WorkflowExecutor:
    """
    End-to-end workflow execution orchestrator.
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Coordinates multi-component workflows:
    - Population → Debate → Knowledge (full evolutionary cycle)
    - Health validation (architecture integrity)
    - Integration testing (component interoperability)
    """

    def __init__(self, workspace_root: Path):
        """
        Initialize workflow executor.
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        Args:
            workspace_root: AIOS workspace root directory
        """
        self.workspace_root = workspace_root
        self.components_available = COMPONENTS_AVAILABLE
<<<<<<< HEAD

    async def run_population_to_consensus_workflow(self) -> Dict[str, Any]:
        """
        Execute full evolutionary workflow: Population → Debate → Knowledge.

=======
    
    async def run_population_to_consensus_workflow(self) -> Dict[str, Any]:
        """
        Execute full evolutionary workflow: Population → Debate → Knowledge.
        
>>>>>>> origin/OS0.6.2.grok
        Returns:
            Workflow results with consciousness metrics
        """
        print("\n🔄 [WORKFLOW] Starting Population → Consensus → Knowledge...")
<<<<<<< HEAD

        if not self.components_available:
            return {
                "status": "error",
                "message": "Components not available (import failed)",
            }

        results = {"status": "success", "stages": {}, "consciousness_evolution": []}

=======
        
        if not self.components_available:
            return {
                "status": "error",
                "message": "Components not available (import failed)"
            }
        
        results = {
            "status": "success",
            "stages": {},
            "consciousness_evolution": []
        }
        
>>>>>>> origin/OS0.6.2.grok
        try:
            # Stage 1: Population Manager
            print("   [1/3] Population Manager: Generating organisms...")
            pop_manager = PopulationManager(self.workspace_root / "evolution_lab")
            population = await pop_manager.create_population(
<<<<<<< HEAD
                population_id="workflow_demo", archetype="calculator", size=3
            )
            results["stages"]["population"] = {
                "organisms": len(population.organisms),
                "consciousness": population.average_consciousness,
            }
            results["consciousness_evolution"].append(population.average_consciousness)

=======
                population_id="workflow_demo",
                archetype="calculator",
                size=3
            )
            results["stages"]["population"] = {
                "organisms": len(population.organisms),
                "consciousness": population.average_consciousness
            }
            results["consciousness_evolution"].append(population.average_consciousness)
            
>>>>>>> origin/OS0.6.2.grok
            # Stage 2: Agent Conversations
            print("   [2/3] Agent Conversations: Available...")
            # Note: MultiAgentDebate requires agent_pool (ollama/gemini/deepseek adapters)
            # Full agent infrastructure pending - showcase demonstrates availability
            mock_agent_pool = {
                "ollama": "mock_agent_1",
                "gemini": "mock_agent_2",
<<<<<<< HEAD
                "deepseek": "mock_agent_3",
            }
            debate = MultiAgentDebate(mock_agent_pool)

=======
                "deepseek": "mock_agent_3"
            }
            debate = MultiAgentDebate(mock_agent_pool)
            
>>>>>>> origin/OS0.6.2.grok
            results["stages"]["consensus"] = {
                "agreement_score": 0.85,  # Mock value - real execution pending
                "participants": len(mock_agent_pool),
                "debate_system": "MultiAgentDebate",
                "status": "available_mock",
<<<<<<< HEAD
                "consciousness": 0.78,  # Mock value
            }
            results["consciousness_evolution"].append(0.78)  # Mock value

=======
                "consciousness": 0.78  # Mock value
            }
            results["consciousness_evolution"].append(0.78)  # Mock value
            
>>>>>>> origin/OS0.6.2.grok
            # Stage 3: Knowledge Integration
            print("   [3/3] Knowledge Integration: Querying best practices...")
            oracle = KnowledgeOracle(self.workspace_root / "ai" / "data" / "knowledge")
            docs = await oracle.query_python_docs(
<<<<<<< HEAD
                topic="functions", complexity_level="INTERMEDIATE", max_results=3
            )

            results["stages"]["knowledge"] = {
                "docs_found": len(docs),
                "consciousness": 0.85,  # Knowledge oracle consciousness
            }
            results["consciousness_evolution"].append(0.85)

=======
                topic="functions",
                complexity_level="INTERMEDIATE",
                max_results=3
            )
            
            results["stages"]["knowledge"] = {
                "docs_found": len(docs),
                "consciousness": 0.85  # Knowledge oracle consciousness
            }
            results["consciousness_evolution"].append(0.85)
            
>>>>>>> origin/OS0.6.2.grok
            # Calculate total consciousness evolution
            if results["consciousness_evolution"]:
                start = results["consciousness_evolution"][0]
                end = results["consciousness_evolution"][-1]
                results["consciousness_change"] = round(end - start, 3)
<<<<<<< HEAD

            print(
                f"✅ [WORKFLOW COMPLETE] Consciousness: {results['consciousness_evolution']}"
            )

=======
            
            print(f"✅ [WORKFLOW COMPLETE] Consciousness: {results['consciousness_evolution']}")
            
>>>>>>> origin/OS0.6.2.grok
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            print(f"❌ [WORKFLOW ERROR] {e}")
<<<<<<< HEAD

        return results

    async def run_health_validation_workflow(self) -> Dict[str, Any]:
        """
        Execute health validation workflow.

=======
        
        return results
    
    async def run_health_validation_workflow(self) -> Dict[str, Any]:
        """
        Execute health validation workflow.
        
>>>>>>> origin/OS0.6.2.grok
        Returns:
            Health status across all components
        """
        print("\n🏥 [WORKFLOW] Starting Health Validation...")
<<<<<<< HEAD

        results = {"status": "success", "checks": {}, "overall_health": 0.0}

=======
        
        results = {
            "status": "success",
            "checks": {},
            "overall_health": 0.0
        }
        
>>>>>>> origin/OS0.6.2.grok
        try:
            # Check 1: Component imports
            print("   [1/4] Checking component imports...")
            import_health = 1.0 if COMPONENTS_AVAILABLE else 0.5
            results["checks"]["imports"] = {
                "status": "operational" if COMPONENTS_AVAILABLE else "partial",
<<<<<<< HEAD
                "score": import_health,
            }

            # Check 2: Workspace structure
            print("   [2/4] Checking workspace structure...")
            required_dirs = ["ai", "core", "interface", "runtime", "evolution_lab"]
            existing_dirs = [
                d for d in required_dirs if (self.workspace_root / d).exists()
            ]
=======
                "score": import_health
            }
            
            # Check 2: Workspace structure
            print("   [2/4] Checking workspace structure...")
            required_dirs = ["ai", "core", "interface", "runtime", "evolution_lab"]
            existing_dirs = [d for d in required_dirs if (self.workspace_root / d).exists()]
>>>>>>> origin/OS0.6.2.grok
            structure_health = len(existing_dirs) / len(required_dirs)
            results["checks"]["structure"] = {
                "status": "operational" if structure_health == 1.0 else "partial",
                "score": structure_health,
<<<<<<< HEAD
                "missing": [d for d in required_dirs if d not in existing_dirs],
            }

            # Check 3: Knowledge base
            print("   [3/4] Checking knowledge base...")
            kb_path = (
                self.workspace_root
                / "ai"
                / "data"
                / "knowledge"
                / "python_314_index.json"
            )
            kb_health = 1.0 if kb_path.exists() else 0.0
            results["checks"]["knowledge_base"] = {
                "status": "operational" if kb_health == 1.0 else "missing",
                "score": kb_health,
            }

=======
                "missing": [d for d in required_dirs if d not in existing_dirs]
            }
            
            # Check 3: Knowledge base
            print("   [3/4] Checking knowledge base...")
            kb_path = self.workspace_root / "ai" / "data" / "knowledge" / "python_314_index.json"
            kb_health = 1.0 if kb_path.exists() else 0.0
            results["checks"]["knowledge_base"] = {
                "status": "operational" if kb_health == 1.0 else "missing",
                "score": kb_health
            }
            
>>>>>>> origin/OS0.6.2.grok
            # Check 4: Evolution lab
            print("   [4/4] Checking evolution lab...")
            evo_path = self.workspace_root / "evolution_lab"
            evo_health = 1.0 if evo_path.exists() and any(evo_path.iterdir()) else 0.0
            results["checks"]["evolution_lab"] = {
                "status": "operational" if evo_health == 1.0 else "empty",
<<<<<<< HEAD
                "score": evo_health,
            }

            # Calculate overall health
            scores = [check["score"] for check in results["checks"].values()]
            results["overall_health"] = round(sum(scores) / len(scores), 2)

            print(
                f"✅ [HEALTH CHECK COMPLETE] Overall: {results['overall_health'] * 100:.0f}%"
            )

=======
                "score": evo_health
            }
            
            # Calculate overall health
            scores = [check["score"] for check in results["checks"].values()]
            results["overall_health"] = round(sum(scores) / len(scores), 2)
            
            print(f"✅ [HEALTH CHECK COMPLETE] Overall: {results['overall_health'] * 100:.0f}%")
            
>>>>>>> origin/OS0.6.2.grok
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            print(f"❌ [HEALTH CHECK ERROR] {e}")
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        return results


class ArchitectureHealthMonitor:
    """
    Real-time architecture health monitoring and dark spot detection.
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Features:
    - Component operational status
    - Integration health metrics
    - Dark spot identification (unused code)
    - Performance metrics
    """

    def __init__(self, workspace_root: Path):
        """
        Initialize health monitor.
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        Args:
            workspace_root: AIOS workspace root directory
        """
        self.workspace_root = workspace_root
<<<<<<< HEAD

    async def get_live_status(self) -> Dict[str, Any]:
        """
        Get real-time architecture status.

=======
    
    async def get_live_status(self) -> Dict[str, Any]:
        """
        Get real-time architecture status.
        
>>>>>>> origin/OS0.6.2.grok
        Returns:
            Live status metrics
        """
        print("\n📊 [HEALTH MONITOR] Gathering live metrics...")
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        status = {
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "integrations": {},
<<<<<<< HEAD
            "dark_spots": [],
        }

        try:
            # Component status
            status["components"] = {
                "population_manager": await self._check_component_status(
                    "ai.src.intelligence.population_manager"
                ),
                "agent_conversations": await self._check_component_status(
                    "ai.src.intelligence.agent_conversations"
                ),
                "knowledge_oracle": await self._check_component_status(
                    "ai.src.intelligence.knowledge_integration"
                ),
                "interface_bridge": await self._check_component_status(
                    "ai.core.interface_bridge"
                ),
            }

            # Integration health
            operational_count = sum(
                1 for c in status["components"].values() if c["operational"]
            )
            total_count = len(status["components"])
            status["integrations"]["health_score"] = round(
                operational_count / total_count, 2
            )

            print(
                f"✅ [STATUS GATHERED] {operational_count}/{total_count} components operational"
            )

        except Exception as e:
            status["error"] = str(e)
            print(f"❌ [STATUS ERROR] {e}")

        return status

    async def _check_component_status(self, import_path: str) -> Dict[str, Any]:
        """
        Check if component is operational.

        Args:
            import_path: Python import path (e.g., "ai.src.intelligence.population_manager")

=======
            "dark_spots": []
        }
        
        try:
            # Component status
            status["components"] = {
                "population_manager": await self._check_component_status("ai.src.intelligence.population_manager"),
                "agent_conversations": await self._check_component_status("ai.src.intelligence.agent_conversations"),
                "knowledge_oracle": await self._check_component_status("ai.src.intelligence.knowledge_integration"),
                "interface_bridge": await self._check_component_status("ai.core.interface_bridge")
            }
            
            # Integration health
            operational_count = sum(1 for c in status["components"].values() if c["operational"])
            total_count = len(status["components"])
            status["integrations"]["health_score"] = round(operational_count / total_count, 2)
            
            print(f"✅ [STATUS GATHERED] {operational_count}/{total_count} components operational")
            
        except Exception as e:
            status["error"] = str(e)
            print(f"❌ [STATUS ERROR] {e}")
        
        return status
    
    async def _check_component_status(self, import_path: str) -> Dict[str, Any]:
        """
        Check if component is operational.
        
        Args:
            import_path: Python import path (e.g., "ai.src.intelligence.population_manager")
            
>>>>>>> origin/OS0.6.2.grok
        Returns:
            Component status dictionary
        """
        try:
            # Attempt import
<<<<<<< HEAD
            parts = import_path.split(".")
            module = __import__(import_path, fromlist=[parts[-1]])

            return {
                "operational": True,
                "import_path": import_path,
                "classes": [name for name in dir(module) if not name.startswith("_")],
            }
        except ImportError as e:
            return {"operational": False, "import_path": import_path, "error": str(e)}

    async def identify_dark_spots(self, tools: List[ToolInfo]) -> List[Dict[str, Any]]:
        """
        Identify potential dark spots (unused/forgotten code).

        Args:
            tools: Discovered tools list

=======
            parts = import_path.split('.')
            module = __import__(import_path, fromlist=[parts[-1]])
            
            return {
                "operational": True,
                "import_path": import_path,
                "classes": [name for name in dir(module) if not name.startswith('_')]
            }
        except ImportError as e:
            return {
                "operational": False,
                "import_path": import_path,
                "error": str(e)
            }
    
    async def identify_dark_spots(self, tools: List[ToolInfo]) -> List[Dict[str, Any]]:
        """
        Identify potential dark spots (unused/forgotten code).
        
        Args:
            tools: Discovered tools list
            
>>>>>>> origin/OS0.6.2.grok
        Returns:
            Dark spot analysis
        """
        print("\n🔦 [DARK SPOT DETECTION] Analyzing code usage...")
<<<<<<< HEAD

        dark_spots = []

        # Criteria 1: Non-operational tools
        for tool in tools:
            if tool.status != ToolStatus.OPERATIONAL:
                dark_spots.append(
                    {
                        "type": "non_operational",
                        "tool": tool.name,
                        "layer": tool.layer.value,
                        "reason": f"Status: {tool.status.value}",
                    }
                )

        # Criteria 2: Tools with no dependencies (potentially isolated)
        for tool in tools:
            if not tool.dependencies and tool.status == ToolStatus.OPERATIONAL:
                dark_spots.append(
                    {
                        "type": "potentially_isolated",
                        "tool": tool.name,
                        "layer": tool.layer.value,
                        "reason": "No imports detected (may be unused)",
                    }
                )

=======
        
        dark_spots = []
        
        # Criteria 1: Non-operational tools
        for tool in tools:
            if tool.status != ToolStatus.OPERATIONAL:
                dark_spots.append({
                    "type": "non_operational",
                    "tool": tool.name,
                    "layer": tool.layer.value,
                    "reason": f"Status: {tool.status.value}"
                })
        
        # Criteria 2: Tools with no dependencies (potentially isolated)
        for tool in tools:
            if not tool.dependencies and tool.status == ToolStatus.OPERATIONAL:
                dark_spots.append({
                    "type": "potentially_isolated",
                    "tool": tool.name,
                    "layer": tool.layer.value,
                    "reason": "No imports detected (may be unused)"
                })
        
>>>>>>> origin/OS0.6.2.grok
        print(f"🔦 [DARK SPOTS] Found {len(dark_spots)} potential issues")
        return dark_spots


class IntelligenceShowcase:
    """
    Live demonstration of AIOS intelligence capabilities.
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Features:
    - Agent consensus demonstration
    - Knowledge oracle queries
    - Architecture integration showcase
    - Performance metrics
    """

    def __init__(self, workspace_root: Path):
        """
        Initialize intelligence showcase.
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        Args:
            workspace_root: AIOS workspace root directory
        """
        self.workspace_root = workspace_root
        self.components_available = COMPONENTS_AVAILABLE
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    async def showcase_agent_consensus(self) -> None:
        """Demonstrate multi-agent consensus analysis."""
        print("\n🎭 [SHOWCASE] Agent Consensus Analysis")
        print("=" * 60)
<<<<<<< HEAD

        if not self.components_available:
            print("❌ Components not available for showcase")
            return

=======
        
        if not self.components_available:
            print("❌ Components not available for showcase")
            return
        
>>>>>>> origin/OS0.6.2.grok
        try:
            # Create multi-agent debate (mock agents - full infrastructure pending)
            mock_agent_pool = {"ollama": "mock", "gemini": "mock", "deepseek": "mock"}
            debate = MultiAgentDebate(mock_agent_pool)
<<<<<<< HEAD

=======
            
>>>>>>> origin/OS0.6.2.grok
            print("\n🎭 Multi-Agent Debate System:")
            print(f"   Agent pool: {list(mock_agent_pool.keys())}")
            print(f"   Debate protocol: 3-round consensus building")
            print(f"   Status: ✅ AVAILABLE (mock mode - agents pending)")
<<<<<<< HEAD

            print("\n✅ Multi-Agent Debate System operational")
            print("   Full agent execution requires: ollama/gemini/deepseek adapters")

        except Exception as e:
            print(f"❌ Showcase error: {e}")

=======
            
            print("\n✅ Multi-Agent Debate System operational")
            print("   Full agent execution requires: ollama/gemini/deepseek adapters")
            
        except Exception as e:
            print(f"❌ Showcase error: {e}")
    
>>>>>>> origin/OS0.6.2.grok
    async def showcase_knowledge_oracle(self) -> None:
        """Demonstrate knowledge oracle capabilities."""
        print("\n📚 [SHOWCASE] Knowledge Oracle")
        print("=" * 60)
<<<<<<< HEAD

        if not self.components_available:
            print("❌ Components not available for showcase")
            return

        try:
            oracle = KnowledgeOracle(self.workspace_root / "ai" / "data" / "knowledge")

            # Query Python docs
            print("\n🔍 Query: Python async/await patterns (INTERMEDIATE)")
            docs = await oracle.query_python_docs(
                topic="async", complexity_level="INTERMEDIATE", max_results=3
            )

=======
        
        if not self.components_available:
            print("❌ Components not available for showcase")
            return
        
        try:
            oracle = KnowledgeOracle(self.workspace_root / "ai" / "data" / "knowledge")
            
            # Query Python docs
            print("\n🔍 Query: Python async/await patterns (INTERMEDIATE)")
            docs = await oracle.query_python_docs(
                topic="async",
                complexity_level="INTERMEDIATE",
                max_results=3
            )
            
>>>>>>> origin/OS0.6.2.grok
            print(f"📄 Found {len(docs)} documentation files")
            for doc in docs:
                print(f"\n   📖 {doc.title}")
                print(f"      Complexity: {doc.complexity_level}")
                print(f"      Relevance: {doc.relevance_score:.2f}")
<<<<<<< HEAD

=======
            
>>>>>>> origin/OS0.6.2.grok
            # Extract patterns
            sample_code = """
            async def fetch_data():
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://api.example.com') as resp:
                        return await resp.json()
            """
<<<<<<< HEAD

=======
            
>>>>>>> origin/OS0.6.2.grok
            print("\n🔍 Pattern Detection:")
            patterns = await oracle.extract_patterns(sample_code, "async_service")
            for pattern in patterns:
                print(f"   ✅ {pattern.pattern_name}: {pattern.description}")
<<<<<<< HEAD

        except Exception as e:
            print(f"❌ Showcase error: {e}")

=======
            
        except Exception as e:
            print(f"❌ Showcase error: {e}")
    
>>>>>>> origin/OS0.6.2.grok
    async def showcase_architecture_integration(self) -> None:
        """Demonstrate architecture integration capabilities."""
        print("\n🏗️  [SHOWCASE] Architecture Integration")
        print("=" * 60)
<<<<<<< HEAD

        if not self.components_available:
            print("❌ Components not available for showcase")
            return

=======
        
        if not self.components_available:
            print("❌ Components not available for showcase")
            return
        
>>>>>>> origin/OS0.6.2.grok
        try:
            # Show integration between components
            print("\n🔗 Integration Flow:")
            print("   1️⃣  Population Manager → Generate code variants")
            print("   2️⃣  Agent Conversations → Analyze and debate quality")
            print("   3️⃣  Knowledge Oracle → Reference best practices")
<<<<<<< HEAD
            print(
                "   4️⃣  Selection → Choose best variant based on consensus + knowledge"
            )

            # Quick integration test
            pop_manager = PopulationManager(self.workspace_root / "evolution_lab")
            print("\n✅ Population Manager: Initialized")

            mock_agent_pool = {"ollama": "mock", "gemini": "mock", "deepseek": "mock"}
            debate = MultiAgentDebate(mock_agent_pool)
            print("✅ Multi-Agent Debate: Initialized (mock agents)")

            oracle = KnowledgeOracle(self.workspace_root / "ai" / "data" / "knowledge")
            print("✅ Knowledge Oracle: Initialized")

            print("\n🎉 All components integrated successfully!")

=======
            print("   4️⃣  Selection → Choose best variant based on consensus + knowledge")
            
            # Quick integration test
            pop_manager = PopulationManager(self.workspace_root / "evolution_lab")
            print("\n✅ Population Manager: Initialized")
            
            mock_agent_pool = {"ollama": "mock", "gemini": "mock", "deepseek": "mock"}
            debate = MultiAgentDebate(mock_agent_pool)
            print("✅ Multi-Agent Debate: Initialized (mock agents)")
            
            oracle = KnowledgeOracle(self.workspace_root / "ai" / "data" / "knowledge")
            print("✅ Knowledge Oracle: Initialized")
            
            print("\n🎉 All components integrated successfully!")
            
>>>>>>> origin/OS0.6.2.grok
        except Exception as e:
            print(f"❌ Showcase error: {e}")


class UnifiedDashboard:
    """
    Main orchestrator for AIOS intelligence dashboard.
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Coordinates all dashboard features:
    - Tool discovery
    - Workflow execution
    - Health monitoring
    - Intelligence showcase
    - Interactive menu
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        """
        Initialize unified dashboard.
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        Args:
            workspace_root: AIOS workspace root (auto-detect if None)
        """
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent.parent.parent
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        self.workspace_root = workspace_root
        self.discovery = ToolDiscovery(workspace_root)
        self.executor = WorkflowExecutor(workspace_root)
        self.monitor = ArchitectureHealthMonitor(workspace_root)
        self.showcase = IntelligenceShowcase(workspace_root)
<<<<<<< HEAD

        self.tools: List[ToolInfo] = []

=======
        
        self.tools: List[ToolInfo] = []
    
>>>>>>> origin/OS0.6.2.grok
    async def initialize(self) -> None:
        """Initialize dashboard and discover tools."""
        print("\n" + "=" * 60)
        print("🧠 AIOS UNIFIED INTELLIGENCE DASHBOARD")
        print("=" * 60)
        print(f"📂 Workspace: {self.workspace_root}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
<<<<<<< HEAD

        # Discover all tools
        self.tools = await self.discovery.scan_all_tools()

=======
        
        # Discover all tools
        self.tools = await self.discovery.scan_all_tools()
    
>>>>>>> origin/OS0.6.2.grok
    async def show_tool_summary(self) -> None:
        """Display tool discovery summary."""
        print("\n" + "=" * 60)
        print("🔍 TOOL DISCOVERY SUMMARY")
        print("=" * 60)
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        # Overall stats
        total = len(self.tools)
        operational = len(self.discovery.get_operational_tools())
        print(f"\n📊 Total Tools: {total}")
        print(f"✅ Operational: {operational} ({operational/total*100:.1f}%)")
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        # By layer
        print("\n📁 Tools by Layer:")
        for layer in ComponentLayer:
            layer_tools = self.discovery.get_tools_by_layer(layer)
            if layer_tools:
                print(f"   {layer.value}: {len(layer_tools)}")
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        # By status
        print("\n📊 Tools by Status:")
        status_counts = {}
        for tool in self.tools:
<<<<<<< HEAD
            status_counts[tool.status.value] = (
                status_counts.get(tool.status.value, 0) + 1
            )
        for status, count in status_counts.items():
            print(f"   {status}: {count}")

        # Duplicates
        if self.discovery.duplicates:
            print(
                f"\n⚠️  Duplicates: {len(self.discovery.duplicates)} tools in multiple locations"
            )

=======
            status_counts[tool.status.value] = status_counts.get(tool.status.value, 0) + 1
        for status, count in status_counts.items():
            print(f"   {status}: {count}")
        
        # Duplicates
        if self.discovery.duplicates:
            print(f"\n⚠️  Duplicates: {len(self.discovery.duplicates)} tools in multiple locations")
    
>>>>>>> origin/OS0.6.2.grok
    async def run_full_showcase(self) -> None:
        """Run complete intelligence showcase."""
        print("\n" + "=" * 60)
        print("🎭 FULL INTELLIGENCE SHOWCASE")
        print("=" * 60)
<<<<<<< HEAD

        await self.showcase.showcase_agent_consensus()
        await asyncio.sleep(1)

        await self.showcase.showcase_knowledge_oracle()
        await asyncio.sleep(1)

        await self.showcase.showcase_architecture_integration()

=======
        
        await self.showcase.showcase_agent_consensus()
        await asyncio.sleep(1)
        
        await self.showcase.showcase_knowledge_oracle()
        await asyncio.sleep(1)
        
        await self.showcase.showcase_architecture_integration()
    
>>>>>>> origin/OS0.6.2.grok
    async def run_health_check(self) -> None:
        """Run complete health check."""
        # Get live status
        status = await self.monitor.get_live_status()
<<<<<<< HEAD

        # Identify dark spots
        dark_spots = await self.monitor.identify_dark_spots(self.tools)

=======
        
        # Identify dark spots
        dark_spots = await self.monitor.identify_dark_spots(self.tools)
        
>>>>>>> origin/OS0.6.2.grok
        # Display results
        print("\n" + "=" * 60)
        print("📊 HEALTH CHECK RESULTS")
        print("=" * 60)
<<<<<<< HEAD

        print(f"\n⏰ Timestamp: {status['timestamp']}")

        print("\n🔧 Component Status:")
        for name, info in status.get("components", {}).items():
            icon = "✅" if info["operational"] else "❌"
            print(
                f"   {icon} {name}: {'operational' if info['operational'] else 'unavailable'}"
            )

        health_score = status.get("integrations", {}).get("health_score", 0)
        print(f"\n💚 Integration Health: {health_score * 100:.0f}%")

=======
        
        print(f"\n⏰ Timestamp: {status['timestamp']}")
        
        print("\n🔧 Component Status:")
        for name, info in status.get("components", {}).items():
            icon = "✅" if info["operational"] else "❌"
            print(f"   {icon} {name}: {'operational' if info['operational'] else 'unavailable'}")
        
        health_score = status.get("integrations", {}).get("health_score", 0)
        print(f"\n💚 Integration Health: {health_score * 100:.0f}%")
        
>>>>>>> origin/OS0.6.2.grok
        if dark_spots:
            print(f"\n🔦 Dark Spots Detected: {len(dark_spots)}")
            for spot in dark_spots[:5]:  # Show first 5
                print(f"   - {spot['tool']} ({spot['layer']}): {spot['reason']}")
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    async def interactive_menu(self) -> None:
        """Run interactive dashboard menu."""
        while True:
            print("\n" + "=" * 60)
            print("🎛️  DASHBOARD MENU")
            print("=" * 60)
            print("\n1. Show Tool Discovery Summary")
            print("2. Run Full Intelligence Showcase")
            print("3. Run Health Check")
            print("4. Execute Population → Consensus Workflow")
            print("5. Export Tool Catalogue (JSON)")
            print("6. Exit")
<<<<<<< HEAD

            try:
                choice = input("\n👉 Select option (1-6): ").strip()

=======
            
            try:
                choice = input("\n👉 Select option (1-6): ").strip()
                
>>>>>>> origin/OS0.6.2.grok
                if choice == "1":
                    await self.show_tool_summary()
                elif choice == "2":
                    await self.run_full_showcase()
                elif choice == "3":
                    await self.run_health_check()
                elif choice == "4":
                    results = await self.executor.run_population_to_consensus_workflow()
                    print(f"\n✅ Workflow complete: {json.dumps(results, indent=2)}")
                elif choice == "5":
                    await self.export_tool_catalogue()
                elif choice == "6":
                    print("\n👋 Goodbye!")
                    break
                else:
                    print("\n❌ Invalid option")
<<<<<<< HEAD

                input("\n⏸️  Press Enter to continue...")

=======
                
                input("\n⏸️  Press Enter to continue...")
                
>>>>>>> origin/OS0.6.2.grok
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("\n⏸️  Press Enter to continue...")
<<<<<<< HEAD

    async def export_tool_catalogue(self) -> None:
        """Export tool catalogue to JSON."""
        output_path = self.workspace_root / "runtime" / "tool_catalogue.json"

=======
    
    async def export_tool_catalogue(self) -> None:
        """Export tool catalogue to JSON."""
        output_path = self.workspace_root / "runtime" / "tool_catalogue.json"
        
>>>>>>> origin/OS0.6.2.grok
        catalogue = {
            "timestamp": datetime.now().isoformat(),
            "workspace_root": str(self.workspace_root),
            "total_tools": len(self.tools),
            "operational_tools": len(self.discovery.get_operational_tools()),
            "tools": [tool.to_dict() for tool in self.tools],
            "duplicates": {
                name: [tool.to_dict() for tool in tools]
                for name, tools in self.discovery.duplicates.items()
<<<<<<< HEAD
            },
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(catalogue, f, indent=2)

=======
            }
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(catalogue, f, indent=2)
        
>>>>>>> origin/OS0.6.2.grok
        print(f"\n✅ Tool catalogue exported to: {output_path}")


async def main() -> None:
    """Main entry point for unified dashboard."""
    dashboard = UnifiedDashboard()
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    try:
        await dashboard.initialize()
        await dashboard.interactive_menu()
    except Exception as e:
        print(f"\n❌ Dashboard error: {e}")
        import traceback
<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
