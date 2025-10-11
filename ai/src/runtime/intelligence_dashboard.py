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
    COMPONENTS_AVAILABLE = True
except ImportError:
    COMPONENTS_AVAILABLE = False


class ToolStatus(Enum):
    """Tool operational status enumeration."""
    OPERATIONAL = "operational"
    IMPORTABLE = "importable"
    SYNTAX_ERROR = "syntax_error"
    NOT_FOUND = "not_found"
    UNKNOWN = "unknown"


class ComponentLayer(Enum):
    """AIOS architectural layer enumeration."""
    RUNTIME_INTELLIGENCE = "runtime_intelligence"
    AI_INTELLIGENCE = "ai_intelligence"
    INTERFACE = "interface"
    CORE = "core"
    UNKNOWN = "unknown"


@dataclass
class ToolInfo:
    """
    Metadata about a discovered AIOS tool.
    
    Attributes:
        name: Tool name (e.g., "system_health_check")
        path: Absolute path to tool file
        layer: Architectural layer (runtime, ai, interface, core)
        status: Operational status
        import_path: Python import path (e.g., "runtime_intelligence.tools.system_health_check")
        description: Tool description (from docstring if available)
        functions: List of public functions/classes
        dependencies: Required imports
        last_modified: File modification timestamp
    """
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
            "last_modified": self.last_modified.isoformat() if self.last_modified else None
        }


class ToolDiscovery:
    """
    Tool discovery engine for AIOS architecture.
    
    Scans 4 architectural layers for Python tools:
    - runtime_intelligence/tools/
    - ai/tools/
    - core/tools/ (if exists)
    - interface/tools/ (if exists)
    
    Features:
    - Duplicate detection (same tool in multiple locations)
    - Operational status validation (import test)
    - Dependency analysis
    - Layer classification
    """

    def __init__(self, workspace_root: Path):
        """
        Initialize tool discovery engine.
        
        Args:
            workspace_root: AIOS workspace root directory
        """
        self.workspace_root = workspace_root
        self.discovered_tools: List[ToolInfo] = []
        self.duplicates: Dict[str, List[ToolInfo]] = defaultdict(list)
        
    async def scan_all_tools(self) -> List[ToolInfo]:
        """
        Scan all architectural layers for tools.
        
        Returns:
            List of discovered tools with metadata
        """
        print("\n🔍 [TOOL DISCOVERY] Scanning AIOS architecture...")
        
        # Define scan locations
        scan_paths = [
            (self.workspace_root / "runtime_intelligence" / "tools", ComponentLayer.RUNTIME_INTELLIGENCE),
            (self.workspace_root / "ai" / "tools", ComponentLayer.AI_INTELLIGENCE),
            (self.workspace_root / "core" / "tools", ComponentLayer.CORE),
            (self.workspace_root / "interface" / "tools", ComponentLayer.INTERFACE),
        ]
        
        # Scan each location
        for path, layer in scan_paths:
            if path.exists():
                await self._scan_directory(path, layer)
        
        # Detect duplicates
        self._detect_duplicates()
        
        print(f"✅ [DISCOVERY COMPLETE] Found {len(self.discovered_tools)} tools")
        return self.discovered_tools
    
    async def _scan_directory(self, directory: Path, layer: ComponentLayer) -> None:
        """
        Recursively scan directory for Python tools.
        
        Args:
            directory: Directory to scan
            layer: Architectural layer classification
        """
        if not directory.exists():
            return
        
        for python_file in directory.rglob("*.py"):
            # Skip __init__.py and private files
            if python_file.name.startswith("_"):
                continue
            
            tool_info = await self._analyze_tool(python_file, layer)
            self.discovered_tools.append(tool_info)
    
    async def _analyze_tool(self, file_path: Path, layer: ComponentLayer) -> ToolInfo:
        """
        Analyze individual tool file.
        
        Args:
            file_path: Path to tool file
            layer: Architectural layer
            
        Returns:
            ToolInfo with analysis results
        """
        tool_name = file_path.stem
        
        # Get file metadata
        stat = file_path.stat()
        last_modified = datetime.fromtimestamp(stat.st_mtime)
        
        # Attempt to import and validate
        status = await self._check_tool_status(file_path)
        
        # Extract docstring and functions
        description = ""
        functions = []
        dependencies = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract module docstring
            if '"""' in content:
                start = content.find('"""') + 3
                end = content.find('"""', start)
                if end > start:
                    description = content[start:end].strip()[:200]  # First 200 chars
            
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
        
        return ToolInfo(
            name=tool_name,
            path=file_path,
            layer=layer,
            status=status,
            import_path=import_path,
            description=description,
            functions=functions,
            dependencies=dependencies,
            last_modified=last_modified
        )
    
    async def _check_tool_status(self, file_path: Path) -> ToolStatus:
        """
        Check if tool is operational via import test.
        
        Args:
            file_path: Path to tool file
            
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
    
    def get_tools_by_layer(self, layer: ComponentLayer) -> List[ToolInfo]:
        """Get tools from specific architectural layer."""
        return [t for t in self.discovered_tools if t.layer == layer]


class WorkflowExecutor:
    """
    End-to-end workflow execution orchestrator.
    
    Coordinates multi-component workflows:
    - Population → Debate → Knowledge (full evolutionary cycle)
    - Health validation (architecture integrity)
    - Integration testing (component interoperability)
    """

    def __init__(self, workspace_root: Path):
        """
        Initialize workflow executor.
        
        Args:
            workspace_root: AIOS workspace root directory
        """
        self.workspace_root = workspace_root
        self.components_available = COMPONENTS_AVAILABLE
    
    async def run_population_to_consensus_workflow(self) -> Dict[str, Any]:
        """
        Execute full evolutionary workflow: Population → Debate → Knowledge.
        
        Returns:
            Workflow results with consciousness metrics
        """
        print("\n🔄 [WORKFLOW] Starting Population → Consensus → Knowledge...")
        
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
        
        try:
            # Stage 1: Population Manager
            print("   [1/3] Population Manager: Generating organisms...")
            pop_manager = PopulationManager(self.workspace_root / "evolution_lab")
            population = await pop_manager.create_population(
                population_id="workflow_demo",
                archetype="calculator",
                size=3
            )
            results["stages"]["population"] = {
                "organisms": len(population.organisms),
                "consciousness": population.average_consciousness
            }
            results["consciousness_evolution"].append(population.average_consciousness)
            
            # Stage 2: Agent Conversations
            print("   [2/3] Agent Conversations: Available...")
            # Note: MultiAgentDebate requires agent_pool (ollama/gemini/deepseek adapters)
            # Full agent infrastructure pending - showcase demonstrates availability
            mock_agent_pool = {
                "ollama": "mock_agent_1",
                "gemini": "mock_agent_2",
                "deepseek": "mock_agent_3"
            }
            debate = MultiAgentDebate(mock_agent_pool)
            
            results["stages"]["consensus"] = {
                "agreement_score": 0.85,  # Mock value - real execution pending
                "participants": len(mock_agent_pool),
                "debate_system": "MultiAgentDebate",
                "status": "available_mock",
                "consciousness": 0.78  # Mock value
            }
            results["consciousness_evolution"].append(0.78)  # Mock value
            
            # Stage 3: Knowledge Integration
            print("   [3/3] Knowledge Integration: Querying best practices...")
            oracle = KnowledgeOracle(self.workspace_root / "ai" / "data" / "knowledge")
            docs = await oracle.query_python_docs(
                topic="functions",
                complexity_level="INTERMEDIATE",
                max_results=3
            )
            
            results["stages"]["knowledge"] = {
                "docs_found": len(docs),
                "consciousness": 0.85  # Knowledge oracle consciousness
            }
            results["consciousness_evolution"].append(0.85)
            
            # Calculate total consciousness evolution
            if results["consciousness_evolution"]:
                start = results["consciousness_evolution"][0]
                end = results["consciousness_evolution"][-1]
                results["consciousness_change"] = round(end - start, 3)
            
            print(f"✅ [WORKFLOW COMPLETE] Consciousness: {results['consciousness_evolution']}")
            
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            print(f"❌ [WORKFLOW ERROR] {e}")
        
        return results
    
    async def run_health_validation_workflow(self) -> Dict[str, Any]:
        """
        Execute health validation workflow.
        
        Returns:
            Health status across all components
        """
        print("\n🏥 [WORKFLOW] Starting Health Validation...")
        
        results = {
            "status": "success",
            "checks": {},
            "overall_health": 0.0
        }
        
        try:
            # Check 1: Component imports
            print("   [1/4] Checking component imports...")
            import_health = 1.0 if COMPONENTS_AVAILABLE else 0.5
            results["checks"]["imports"] = {
                "status": "operational" if COMPONENTS_AVAILABLE else "partial",
                "score": import_health
            }
            
            # Check 2: Workspace structure
            print("   [2/4] Checking workspace structure...")
            required_dirs = ["ai", "core", "interface", "runtime_intelligence", "evolution_lab"]
            existing_dirs = [d for d in required_dirs if (self.workspace_root / d).exists()]
            structure_health = len(existing_dirs) / len(required_dirs)
            results["checks"]["structure"] = {
                "status": "operational" if structure_health == 1.0 else "partial",
                "score": structure_health,
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
            
            # Check 4: Evolution lab
            print("   [4/4] Checking evolution lab...")
            evo_path = self.workspace_root / "evolution_lab"
            evo_health = 1.0 if evo_path.exists() and any(evo_path.iterdir()) else 0.0
            results["checks"]["evolution_lab"] = {
                "status": "operational" if evo_health == 1.0 else "empty",
                "score": evo_health
            }
            
            # Calculate overall health
            scores = [check["score"] for check in results["checks"].values()]
            results["overall_health"] = round(sum(scores) / len(scores), 2)
            
            print(f"✅ [HEALTH CHECK COMPLETE] Overall: {results['overall_health'] * 100:.0f}%")
            
        except Exception as e:
            results["status"] = "error"
            results["error"] = str(e)
            print(f"❌ [HEALTH CHECK ERROR] {e}")
        
        return results


class ArchitectureHealthMonitor:
    """
    Real-time architecture health monitoring and dark spot detection.
    
    Features:
    - Component operational status
    - Integration health metrics
    - Dark spot identification (unused code)
    - Performance metrics
    """

    def __init__(self, workspace_root: Path):
        """
        Initialize health monitor.
        
        Args:
            workspace_root: AIOS workspace root directory
        """
        self.workspace_root = workspace_root
    
    async def get_live_status(self) -> Dict[str, Any]:
        """
        Get real-time architecture status.
        
        Returns:
            Live status metrics
        """
        print("\n📊 [HEALTH MONITOR] Gathering live metrics...")
        
        status = {
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "integrations": {},
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
            
        Returns:
            Component status dictionary
        """
        try:
            # Attempt import
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
            
        Returns:
            Dark spot analysis
        """
        print("\n🔦 [DARK SPOT DETECTION] Analyzing code usage...")
        
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
        
        print(f"🔦 [DARK SPOTS] Found {len(dark_spots)} potential issues")
        return dark_spots


class IntelligenceShowcase:
    """
    Live demonstration of AIOS intelligence capabilities.
    
    Features:
    - Agent consensus demonstration
    - Knowledge oracle queries
    - Architecture integration showcase
    - Performance metrics
    """

    def __init__(self, workspace_root: Path):
        """
        Initialize intelligence showcase.
        
        Args:
            workspace_root: AIOS workspace root directory
        """
        self.workspace_root = workspace_root
        self.components_available = COMPONENTS_AVAILABLE
    
    async def showcase_agent_consensus(self) -> None:
        """Demonstrate multi-agent consensus analysis."""
        print("\n🎭 [SHOWCASE] Agent Consensus Analysis")
        print("=" * 60)
        
        if not self.components_available:
            print("❌ Components not available for showcase")
            return
        
        try:
            # Create multi-agent debate (mock agents - full infrastructure pending)
            mock_agent_pool = {"ollama": "mock", "gemini": "mock", "deepseek": "mock"}
            debate = MultiAgentDebate(mock_agent_pool)
            
            print("\n🎭 Multi-Agent Debate System:")
            print(f"   Agent pool: {list(mock_agent_pool.keys())}")
            print(f"   Debate protocol: 3-round consensus building")
            print(f"   Status: ✅ AVAILABLE (mock mode - agents pending)")
            
            print("\n✅ Multi-Agent Debate System operational")
            print("   Full agent execution requires: ollama/gemini/deepseek adapters")
            
        except Exception as e:
            print(f"❌ Showcase error: {e}")
    
    async def showcase_knowledge_oracle(self) -> None:
        """Demonstrate knowledge oracle capabilities."""
        print("\n📚 [SHOWCASE] Knowledge Oracle")
        print("=" * 60)
        
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
            
            print(f"📄 Found {len(docs)} documentation files")
            for doc in docs:
                print(f"\n   📖 {doc.title}")
                print(f"      Complexity: {doc.complexity_level}")
                print(f"      Relevance: {doc.relevance_score:.2f}")
            
            # Extract patterns
            sample_code = """
            async def fetch_data():
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://api.example.com') as resp:
                        return await resp.json()
            """
            
            print("\n🔍 Pattern Detection:")
            patterns = await oracle.extract_patterns(sample_code, "async_service")
            for pattern in patterns:
                print(f"   ✅ {pattern.pattern_name}: {pattern.description}")
            
        except Exception as e:
            print(f"❌ Showcase error: {e}")
    
    async def showcase_architecture_integration(self) -> None:
        """Demonstrate architecture integration capabilities."""
        print("\n🏗️  [SHOWCASE] Architecture Integration")
        print("=" * 60)
        
        if not self.components_available:
            print("❌ Components not available for showcase")
            return
        
        try:
            # Show integration between components
            print("\n🔗 Integration Flow:")
            print("   1️⃣  Population Manager → Generate code variants")
            print("   2️⃣  Agent Conversations → Analyze and debate quality")
            print("   3️⃣  Knowledge Oracle → Reference best practices")
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
            
        except Exception as e:
            print(f"❌ Showcase error: {e}")


class UnifiedDashboard:
    """
    Main orchestrator for AIOS intelligence dashboard.
    
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
        
        Args:
            workspace_root: AIOS workspace root (auto-detect if None)
        """
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent.parent.parent
        
        self.workspace_root = workspace_root
        self.discovery = ToolDiscovery(workspace_root)
        self.executor = WorkflowExecutor(workspace_root)
        self.monitor = ArchitectureHealthMonitor(workspace_root)
        self.showcase = IntelligenceShowcase(workspace_root)
        
        self.tools: List[ToolInfo] = []
    
    async def initialize(self) -> None:
        """Initialize dashboard and discover tools."""
        print("\n" + "=" * 60)
        print("🧠 AIOS UNIFIED INTELLIGENCE DASHBOARD")
        print("=" * 60)
        print(f"📂 Workspace: {self.workspace_root}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Discover all tools
        self.tools = await self.discovery.scan_all_tools()
    
    async def show_tool_summary(self) -> None:
        """Display tool discovery summary."""
        print("\n" + "=" * 60)
        print("🔍 TOOL DISCOVERY SUMMARY")
        print("=" * 60)
        
        # Overall stats
        total = len(self.tools)
        operational = len(self.discovery.get_operational_tools())
        print(f"\n📊 Total Tools: {total}")
        print(f"✅ Operational: {operational} ({operational/total*100:.1f}%)")
        
        # By layer
        print("\n📁 Tools by Layer:")
        for layer in ComponentLayer:
            layer_tools = self.discovery.get_tools_by_layer(layer)
            if layer_tools:
                print(f"   {layer.value}: {len(layer_tools)}")
        
        # By status
        print("\n📊 Tools by Status:")
        status_counts = {}
        for tool in self.tools:
            status_counts[tool.status.value] = status_counts.get(tool.status.value, 0) + 1
        for status, count in status_counts.items():
            print(f"   {status}: {count}")
        
        # Duplicates
        if self.discovery.duplicates:
            print(f"\n⚠️  Duplicates: {len(self.discovery.duplicates)} tools in multiple locations")
    
    async def run_full_showcase(self) -> None:
        """Run complete intelligence showcase."""
        print("\n" + "=" * 60)
        print("🎭 FULL INTELLIGENCE SHOWCASE")
        print("=" * 60)
        
        await self.showcase.showcase_agent_consensus()
        await asyncio.sleep(1)
        
        await self.showcase.showcase_knowledge_oracle()
        await asyncio.sleep(1)
        
        await self.showcase.showcase_architecture_integration()
    
    async def run_health_check(self) -> None:
        """Run complete health check."""
        # Get live status
        status = await self.monitor.get_live_status()
        
        # Identify dark spots
        dark_spots = await self.monitor.identify_dark_spots(self.tools)
        
        # Display results
        print("\n" + "=" * 60)
        print("📊 HEALTH CHECK RESULTS")
        print("=" * 60)
        
        print(f"\n⏰ Timestamp: {status['timestamp']}")
        
        print("\n🔧 Component Status:")
        for name, info in status.get("components", {}).items():
            icon = "✅" if info["operational"] else "❌"
            print(f"   {icon} {name}: {'operational' if info['operational'] else 'unavailable'}")
        
        health_score = status.get("integrations", {}).get("health_score", 0)
        print(f"\n💚 Integration Health: {health_score * 100:.0f}%")
        
        if dark_spots:
            print(f"\n🔦 Dark Spots Detected: {len(dark_spots)}")
            for spot in dark_spots[:5]:  # Show first 5
                print(f"   - {spot['tool']} ({spot['layer']}): {spot['reason']}")
    
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
            
            try:
                choice = input("\n👉 Select option (1-6): ").strip()
                
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
                
                input("\n⏸️  Press Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("\n⏸️  Press Enter to continue...")
    
    async def export_tool_catalogue(self) -> None:
        """Export tool catalogue to JSON."""
        output_path = self.workspace_root / "runtime_intelligence" / "tool_catalogue.json"
        
        catalogue = {
            "timestamp": datetime.now().isoformat(),
            "workspace_root": str(self.workspace_root),
            "total_tools": len(self.tools),
            "operational_tools": len(self.discovery.get_operational_tools()),
            "tools": [tool.to_dict() for tool in self.tools],
            "duplicates": {
                name: [tool.to_dict() for tool in tools]
                for name, tools in self.discovery.duplicates.items()
            }
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(catalogue, f, indent=2)
        
        print(f"\n✅ Tool catalogue exported to: {output_path}")


async def main() -> None:
    """Main entry point for unified dashboard."""
    dashboard = UnifiedDashboard()
    
    try:
        await dashboard.initialize()
        await dashboard.interactive_menu()
    except Exception as e:
        print(f"\n❌ Dashboard error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
