#!/usr/bin/env python3
"""
AIOS Runtime Sequencer
Orchestrates and manages all executable components in AIOS at startup and runtime
"""

import os
import sys
import json
import asyncio
import importlib
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

<<<<<<< HEAD

@dataclass
class ExecutableComponent:
    """Represents a discoverable executable component in AIOS"""

=======
@dataclass
class ExecutableComponent:
    """Represents a discoverable executable component in AIOS"""
>>>>>>> origin/OS0.6.2.grok
    name: str
    path: Path
    type: str  # 'python', 'script', 'service', 'tool'
    category: str  # 'ai_cell', 'tool', 'service', 'integration'
    dependencies: List[str]
    description: str
    entry_point: str
    auto_start: bool = False
    health_check: Optional[str] = None
<<<<<<< HEAD


@dataclass
class SequencerState:
    """Current state of the sequencer and all components"""

=======
    
@dataclass
class SequencerState:
    """Current state of the sequencer and all components"""
>>>>>>> origin/OS0.6.2.grok
    startup_time: datetime
    components_discovered: int
    components_active: int
    components_failed: int
    execution_order: List[str]
    health_status: Dict[str, str]


class AIOSSequencer:
    """
    AIOS Runtime Sequencer - Orchestrates all executable components
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Responsibilities:
    1. Discover all executable components in AIOS
    2. Validate dependencies and execution order
    3. Start components in proper sequence
    4. Monitor component health and status
    5. Provide runtime information and control
    """
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.ai_root = self.workspace_root / "ai"
        self.components: Dict[str, ExecutableComponent] = {}
        self.state = SequencerState(
            startup_time=datetime.now(),
            components_discovered=0,
            components_active=0,
            components_failed=0,
            execution_order=[],
<<<<<<< HEAD
            health_status={},
        )

        # Setup logging
        self.logger = self._setup_logging()

        # Discovery patterns for different component types
        self.discovery_patterns = {
            "python": ["**/*.py"],
            "script": ["**/*.ps1", "**/*.bat", "**/*.sh"],
            "config": ["**/*.json", "**/*.yaml", "**/*.yml"],
            "service": ["**/start_*.py", "**/*_server.py"],
        }

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for sequencer operations"""
        logger = logging.getLogger("AIOS.Sequencer")
        logger.setLevel(logging.INFO)

=======
            health_status={}
        )
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Discovery patterns for different component types
        self.discovery_patterns = {
            'python': ['**/*.py'],
            'script': ['**/*.ps1', '**/*.bat', '**/*.sh'],
            'config': ['**/*.json', '**/*.yaml', '**/*.yml'],
            'service': ['**/start_*.py', '**/*_server.py']
        }
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for sequencer operations"""
        logger = logging.getLogger('AIOS.Sequencer')
        logger.setLevel(logging.INFO)
        
>>>>>>> origin/OS0.6.2.grok
        # Console handler with UTF-8 encoding for Windows
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
<<<<<<< HEAD
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        # Fix encoding issues on Windows
        if hasattr(console_handler.stream, "reconfigure"):
            console_handler.stream.reconfigure(encoding="utf-8")

        logger.addHandler(console_handler)

        # File handler
        log_dir = self.workspace_root / "ai" / "infrastructure" / "runtime"
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "sequencer.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    async def discover_components(self) -> Dict[str, ExecutableComponent]:
        """Discover all executable components in AIOS"""
        self.logger.info("🔍 Starting component discovery...")

        discovered = {}

        # Discover AI cells
        ai_cells = await self._discover_ai_cells()
        discovered.update(ai_cells)

        # Discover tools from ai/tools/ (primary location after migration)
        ai_tools = await self._discover_ai_tools()
        discovered.update(ai_tools)

        # Discover tools and utilities (infrastructure)
        tools = await self._discover_tools()
        discovered.update(tools)

        # Discover services and servers
        services = await self._discover_services()
        discovered.update(services)

        # Discover integration components
        integrations = await self._discover_integrations()
        discovered.update(integrations)

        # Discover runtime intelligence tools (legacy location)
        runtime = await self._discover_runtime()
        discovered.update(runtime)

        self.components = discovered
        self.state.components_discovered = len(discovered)

        self.logger.info(f"✅ Discovered {len(discovered)} components")
        return discovered

=======
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Fix encoding issues on Windows
        if hasattr(console_handler.stream, 'reconfigure'):
            console_handler.stream.reconfigure(encoding='utf-8')
        
        logger.addHandler(console_handler)
        
        # File handler
        log_dir = self.workspace_root / "ai" / "infrastructure" / "runtime"
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / "sequencer.log", 
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    async def discover_components(self) -> Dict[str, ExecutableComponent]:
        """Discover all executable components in AIOS"""
        self.logger.info("🔍 Starting component discovery...")
        
        discovered = {}
        
        # Discover AI cells
        ai_cells = await self._discover_ai_cells()
        discovered.update(ai_cells)
        
        # Discover tools from ai/tools/ (primary location after migration)
        ai_tools = await self._discover_ai_tools()
        discovered.update(ai_tools)
        
        # Discover tools and utilities (infrastructure)
        tools = await self._discover_tools()
        discovered.update(tools)
        
        # Discover services and servers
        services = await self._discover_services()
        discovered.update(services)
        
        # Discover integration components
        integrations = await self._discover_integrations()
        discovered.update(integrations)
        
        # Discover runtime intelligence tools (legacy location)
        runtime = await self._discover_runtime()
        discovered.update(runtime)
        
        self.components = discovered
        self.state.components_discovered = len(discovered)
        
        self.logger.info(f"✅ Discovered {len(discovered)} components")
        return discovered
    
>>>>>>> origin/OS0.6.2.grok
    async def _discover_ai_cells(self) -> Dict[str, ExecutableComponent]:
        """Discover AI cell components"""
        ai_cells = {}
        ai_cells_dir = self.ai_root / "core" / "ai_cells"
<<<<<<< HEAD

        if ai_cells_dir.exists():
            for py_file in ai_cells_dir.glob("*.py"):
                if py_file.name != "__init__.py":
                    component = await self._analyze_python_component(py_file, "ai_cell")
                    if component:
                        ai_cells[component.name] = component

        return ai_cells

    async def _discover_ai_tools(self) -> Dict[str, ExecutableComponent]:
        """
        Discover AI tools from ai/tools/ structure (post-migration primary location)

=======
        
        if ai_cells_dir.exists():
            for py_file in ai_cells_dir.glob("*.py"):
                if py_file.name != "__init__.py":
                    component = await self._analyze_python_component(
                        py_file, "ai_cell"
                    )
                    if component:
                        ai_cells[component.name] = component
        
        return ai_cells
    
    async def _discover_ai_tools(self) -> Dict[str, ExecutableComponent]:
        """
        Discover AI tools from ai/tools/ structure (post-migration primary location)
        
>>>>>>> origin/OS0.6.2.grok
        Discovers tools across 6 categories:
        - consciousness: Consciousness analysis and evolution tools
        - system: System health, admin, and development tools
        - architecture: Architecture monitoring and analysis tools
        - visual: Visual processing and cognition tools
        - tachyonic: Tachyonic metadata and intelligence tools
        - database: Database transformation and management tools
        """
        ai_tools = {}
        ai_tools_dir = self.ai_root / "tools"
<<<<<<< HEAD

        if not ai_tools_dir.exists():
            self.logger.warning(f"ai/tools directory not found: {ai_tools_dir}")
            return ai_tools

        # Discover tools in all category subdirectories
        categories = [
            "consciousness",
            "system",
            "architecture",
            "visual",
            "tachyonic",
            "database",
        ]

=======
        
        if not ai_tools_dir.exists():
            self.logger.warning(f"ai/tools directory not found: {ai_tools_dir}")
            return ai_tools
        
        # Discover tools in all category subdirectories
        categories = ['consciousness', 'system', 'architecture', 'visual', 'tachyonic', 'database']
        
>>>>>>> origin/OS0.6.2.grok
        for category in categories:
            category_dir = ai_tools_dir / category
            if category_dir.exists() and category_dir.is_dir():
                for py_file in category_dir.glob("*.py"):
                    if py_file.name != "__init__.py":
                        component = await self._analyze_python_component(
                            py_file, "tool"
                        )
                        if component:
                            # Enhance component with category metadata
                            component.category = f"tool/{category}"
                            ai_tools[component.name] = component
<<<<<<< HEAD
                            self.logger.debug(
                                f"Discovered {category} tool: {component.name}"
                            )

        self.logger.info(f"✅ Discovered {len(ai_tools)} tools from ai/tools/")
        return ai_tools

    async def _discover_tools(self) -> Dict[str, ExecutableComponent]:
        """Discover tool components"""
        tools = {}

=======
                            self.logger.debug(f"Discovered {category} tool: {component.name}")
        
        self.logger.info(f"✅ Discovered {len(ai_tools)} tools from ai/tools/")
        return ai_tools
    
    async def _discover_tools(self) -> Dict[str, ExecutableComponent]:
        """Discover tool components"""
        tools = {}
        
>>>>>>> origin/OS0.6.2.grok
        # Infrastructure tools
        tools_dir = self.ai_root / "infrastructure" / "tools"
        if tools_dir.exists():
            for tool_file in tools_dir.glob("*.py"):
                if tool_file.name != "__init__.py":
<<<<<<< HEAD
                    component = await self._analyze_python_component(tool_file, "tool")
                    if component:
                        tools[component.name] = component

        # Core tools
        for py_file in self.ai_root.glob("**/*tool*.py"):
            if not any(part.startswith(".") for part in py_file.parts):
                component = await self._analyze_python_component(py_file, "tool")
                if component and component.name not in tools:
                    tools[component.name] = component

        return tools

    async def _discover_services(self) -> Dict[str, ExecutableComponent]:
        """Discover service components"""
        services = {}

        # Look for server files
        for server_file in self.ai_root.glob("**/start_*.py"):
            component = await self._analyze_python_component(server_file, "service")
            if component:
                services[component.name] = component

        for server_file in self.ai_root.glob("**/*_server.py"):
            component = await self._analyze_python_component(server_file, "service")
            if component and component.name not in services:
                services[component.name] = component

        return services

=======
                    component = await self._analyze_python_component(
                        tool_file, "tool"
                    )
                    if component:
                        tools[component.name] = component
        
        # Core tools
        for py_file in self.ai_root.glob("**/*tool*.py"):
            if not any(part.startswith('.') for part in py_file.parts):
                component = await self._analyze_python_component(
                    py_file, "tool"
                )
                if component and component.name not in tools:
                    tools[component.name] = component
        
        return tools
    
    async def _discover_services(self) -> Dict[str, ExecutableComponent]:
        """Discover service components"""
        services = {}
        
        # Look for server files
        for server_file in self.ai_root.glob("**/start_*.py"):
            component = await self._analyze_python_component(
                server_file, "service"
            )
            if component:
                services[component.name] = component
        
        for server_file in self.ai_root.glob("**/*_server.py"):
            component = await self._analyze_python_component(
                server_file, "service"
            )
            if component and component.name not in services:
                services[component.name] = component
        
        return services
    
>>>>>>> origin/OS0.6.2.grok
    async def _discover_integrations(self) -> Dict[str, ExecutableComponent]:
        """Discover integration components"""
        integrations = {}
        interfaces_dir = self.ai_root / "interfaces"
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        if interfaces_dir.exists():
            for py_file in interfaces_dir.glob("*.py"):
                if py_file.name != "__init__.py":
                    component = await self._analyze_python_component(
                        py_file, "integration"
                    )
                    if component:
                        integrations[component.name] = component
<<<<<<< HEAD

        return integrations

=======
        
        return integrations
    
>>>>>>> origin/OS0.6.2.grok
    async def _discover_runtime(self) -> Dict[str, ExecutableComponent]:
        """Discover runtime intelligence tools and components"""
        runtime_tools = {}
        # Get path relative to this sequencer.py file location
        sequencer_dir = Path(__file__).parent
        runtime_dir = (sequencer_dir / "../../runtime").resolve()
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        if runtime_dir.exists():
            # Discover tools in runtime/tools/
            tools_dir = runtime_dir / "tools"
            if tools_dir.exists():
                for py_file in tools_dir.glob("*.py"):
                    if py_file.name != "__init__.py":
                        component = await self._analyze_python_component(
                            py_file, "tool"
                        )
                        if component:
                            runtime_tools[component.name] = component
<<<<<<< HEAD

            # Discover other runtime intelligence components
            for py_file in runtime_dir.glob("*.py"):
                if py_file.name != "__init__.py":
                    component = await self._analyze_python_component(py_file, "tool")
                    if component and component.name not in runtime_tools:
                        runtime_tools[component.name] = component

        return runtime_tools

    async def _analyze_python_component(
        self, file_path: Path, category: str
    ) -> Optional[ExecutableComponent]:
        """Analyze a Python file to create component metadata"""
        try:
            content = file_path.read_text(encoding="utf-8")

=======
            
            # Discover other runtime intelligence components
            for py_file in runtime_dir.glob("*.py"):
                if py_file.name != "__init__.py":
                    component = await self._analyze_python_component(
                        py_file, "tool"
                    )
                    if component and component.name not in runtime_tools:
                        runtime_tools[component.name] = component
        
        return runtime_tools
    
    async def _analyze_python_component(
        self, 
        file_path: Path, 
        category: str
    ) -> Optional[ExecutableComponent]:
        """Analyze a Python file to create component metadata"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
>>>>>>> origin/OS0.6.2.grok
            # Extract metadata from docstring and code
            name = file_path.stem
            description = self._extract_description(content)
            dependencies = self._extract_dependencies(content)
            entry_point = self._determine_entry_point(content, file_path)
            auto_start = self._should_auto_start(content, category)
<<<<<<< HEAD

            return ExecutableComponent(
                name=name,
                path=file_path,
                type="python",
=======
            
            return ExecutableComponent(
                name=name,
                path=file_path,
                type='python',
>>>>>>> origin/OS0.6.2.grok
                category=category,
                dependencies=dependencies,
                description=description,
                entry_point=entry_point,
                auto_start=auto_start,
<<<<<<< HEAD
                health_check=self._extract_health_check(content),
            )

        except Exception as e:
            self.logger.warning(f"Could not analyze {file_path}: {e}")
            return None

    def _extract_description(self, content: str) -> str:
        """Extract description from docstring"""
        lines = content.split("\n")
        in_docstring = False
        description_lines = []

=======
                health_check=self._extract_health_check(content)
            )
            
        except Exception as e:
            self.logger.warning(f"Could not analyze {file_path}: {e}")
            return None
    
    def _extract_description(self, content: str) -> str:
        """Extract description from docstring"""
        lines = content.split('\n')
        in_docstring = False
        description_lines = []
        
>>>>>>> origin/OS0.6.2.grok
        for line in lines:
            stripped = line.strip()
            if '"""' in stripped:
                if in_docstring:
                    break
                in_docstring = True
                # Extract text after opening quotes
                after_quotes = stripped.split('"""', 1)
                if len(after_quotes) > 1 and after_quotes[1]:
                    description_lines.append(after_quotes[1])
            elif in_docstring and stripped:
                description_lines.append(stripped)
<<<<<<< HEAD

        return " ".join(description_lines[:3])  # First 3 lines max

    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract dependencies from imports and code"""
        dependencies = []
        lines = content.split("\n")

        for line in lines:
            stripped = line.strip()
            # Look for imports that might be dependencies
            if stripped.startswith("import ") or stripped.startswith("from "):
                # Extract module names
                if " import " in stripped:
                    module = stripped.split(" import ")[0].replace("from ", "")
                    if "." in module:
                        dependencies.append(module.split(".")[0])
                    else:
                        dependencies.append(module)

        # Remove standard library modules
        stdlib_modules = {
            "os",
            "sys",
            "json",
            "asyncio",
            "subprocess",
            "pathlib",
            "typing",
            "dataclasses",
            "datetime",
            "logging",
            "importlib",
        }

        return [dep for dep in set(dependencies) if dep not in stdlib_modules]

    def _determine_entry_point(self, content: str, file_path: Path) -> str:
        """Determine the entry point for execution"""
        # Look for main function
        if "def main(" in content or 'if __name__ == "__main__"' in content:
            return f"python {file_path}"

        # Look for class with run method
        if "def run(" in content or "async def run(" in content:
            return f'python -c "from {file_path.stem} import *; run()"'

        # Default to module execution
        return f"python {file_path}"

    def _should_auto_start(self, content: str, category: str) -> bool:
        """Determine if component should auto-start"""
        # Services typically auto-start
        if category == "service":
            return True

        # Look for auto-start indicators in code
        auto_indicators = ["auto_start", "startup", "background"]
        return any(indicator in content.lower() for indicator in auto_indicators)

    def _extract_health_check(self, content: str) -> Optional[str]:
        """Extract health check method if available"""
        if "def health_check(" in content:
            return "health_check"
        if "def status(" in content:
            return "status"
        return None

    async def validate_dependencies(self) -> Tuple[bool, List[str]]:
        """Validate all component dependencies"""
        self.logger.info("🔍 Validating component dependencies...")

        missing_deps = []
        all_component_names = set(self.components.keys())

=======
        
        return ' '.join(description_lines[:3])  # First 3 lines max
    
    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract dependencies from imports and code"""
        dependencies = []
        lines = content.split('\n')
        
        for line in lines:
            stripped = line.strip()
            # Look for imports that might be dependencies
            if stripped.startswith('import ') or stripped.startswith('from '):
                # Extract module names
                if ' import ' in stripped:
                    module = stripped.split(' import ')[0].replace('from ', '')
                    if '.' in module:
                        dependencies.append(module.split('.')[0])
                    else:
                        dependencies.append(module)
        
        # Remove standard library modules
        stdlib_modules = {
            'os', 'sys', 'json', 'asyncio', 'subprocess', 'pathlib',
            'typing', 'dataclasses', 'datetime', 'logging', 'importlib'
        }
        
        return [dep for dep in set(dependencies) if dep not in stdlib_modules]
    
    def _determine_entry_point(self, content: str, file_path: Path) -> str:
        """Determine the entry point for execution"""
        # Look for main function
        if 'def main(' in content or 'if __name__ == "__main__"' in content:
            return f"python {file_path}"
        
        # Look for class with run method
        if 'def run(' in content or 'async def run(' in content:
            return f"python -c \"from {file_path.stem} import *; run()\""
        
        # Default to module execution
        return f"python {file_path}"
    
    def _should_auto_start(self, content: str, category: str) -> bool:
        """Determine if component should auto-start"""
        # Services typically auto-start
        if category == 'service':
            return True
        
        # Look for auto-start indicators in code
        auto_indicators = ['auto_start', 'startup', 'background']
        return any(indicator in content.lower() for indicator in auto_indicators)
    
    def _extract_health_check(self, content: str) -> Optional[str]:
        """Extract health check method if available"""
        if 'def health_check(' in content:
            return 'health_check'
        if 'def status(' in content:
            return 'status'
        return None
    
    async def validate_dependencies(self) -> Tuple[bool, List[str]]:
        """Validate all component dependencies"""
        self.logger.info("🔍 Validating component dependencies...")
        
        missing_deps = []
        all_component_names = set(self.components.keys())
        
>>>>>>> origin/OS0.6.2.grok
        for name, component in self.components.items():
            for dep in component.dependencies:
                if dep not in all_component_names:
                    missing_deps.append(f"{name} → {dep}")
<<<<<<< HEAD

        if missing_deps:
            self.logger.warning(f"⚠️  Missing dependencies: {missing_deps}")
            return False, missing_deps

        self.logger.info("✅ All dependencies validated")
        return True, []

    async def calculate_execution_order(self) -> List[str]:
        """Calculate optimal execution order based on dependencies"""
        self.logger.info("📋 Calculating execution order...")

=======
        
        if missing_deps:
            self.logger.warning(f"⚠️  Missing dependencies: {missing_deps}")
            return False, missing_deps
        
        self.logger.info("✅ All dependencies validated")
        return True, []
    
    async def calculate_execution_order(self) -> List[str]:
        """Calculate optimal execution order based on dependencies"""
        self.logger.info("📋 Calculating execution order...")
        
>>>>>>> origin/OS0.6.2.grok
        # Topological sort for dependency resolution
        visited = set()
        temp_visited = set()
        order = []
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        def visit(component_name: str):
            if component_name in temp_visited:
                raise ValueError(f"Circular dependency detected: {component_name}")
            if component_name in visited:
                return
<<<<<<< HEAD

            temp_visited.add(component_name)

=======
            
            temp_visited.add(component_name)
            
>>>>>>> origin/OS0.6.2.grok
            component = self.components.get(component_name)
            if component:
                for dep in component.dependencies:
                    if dep in self.components:
                        visit(dep)
<<<<<<< HEAD

            temp_visited.remove(component_name)
            visited.add(component_name)
            order.append(component_name)

=======
            
            temp_visited.remove(component_name)
            visited.add(component_name)
            order.append(component_name)
        
>>>>>>> origin/OS0.6.2.grok
        # Visit all components
        for name in self.components.keys():
            if name not in visited:
                visit(name)
<<<<<<< HEAD

        self.state.execution_order = order
        self.logger.info(f"✅ Execution order: {' → '.join(order[:5])}...")
        return order

    async def start_components(self, auto_start_only: bool = True) -> Dict[str, bool]:
        """Start components in calculated order"""
        self.logger.info("🚀 Starting components...")

        results = {}
        order = await self.calculate_execution_order()

        for component_name in order:
            component = self.components[component_name]

            if auto_start_only and not component.auto_start:
                continue

            try:
                success = await self._start_component(component)
                results[component_name] = success

=======
        
        self.state.execution_order = order
        self.logger.info(f"✅ Execution order: {' → '.join(order[:5])}...")
        return order
    
    async def start_components(self, auto_start_only: bool = True) -> Dict[str, bool]:
        """Start components in calculated order"""
        self.logger.info("🚀 Starting components...")
        
        results = {}
        order = await self.calculate_execution_order()
        
        for component_name in order:
            component = self.components[component_name]
            
            if auto_start_only and not component.auto_start:
                continue
            
            try:
                success = await self._start_component(component)
                results[component_name] = success
                
>>>>>>> origin/OS0.6.2.grok
                if success:
                    self.state.components_active += 1
                    self.state.health_status[component_name] = "running"
                else:
                    self.state.components_failed += 1
                    self.state.health_status[component_name] = "failed"
<<<<<<< HEAD

=======
                    
>>>>>>> origin/OS0.6.2.grok
            except Exception as e:
                self.logger.error(f"❌ Failed to start {component_name}: {e}")
                results[component_name] = False
                self.state.components_failed += 1
                self.state.health_status[component_name] = "error"
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        self.logger.info(
            f"✅ Started {self.state.components_active} components, "
            f"{self.state.components_failed} failed"
        )
        return results
<<<<<<< HEAD

    async def _start_component(self, component: ExecutableComponent) -> bool:
        """Start a single component"""
        self.logger.info(f"Starting {component.name}...")

        try:
            if component.type == "python":
=======
    
    async def _start_component(self, component: ExecutableComponent) -> bool:
        """Start a single component"""
        self.logger.info(f"Starting {component.name}...")
        
        try:
            if component.type == 'python':
>>>>>>> origin/OS0.6.2.grok
                # For Python components, we might want to import and initialize
                # rather than subprocess for better integration
                return await self._start_python_component(component)
            else:
                # For scripts, use subprocess
                result = subprocess.run(
                    component.entry_point.split(),
                    cwd=component.path.parent,
                    capture_output=True,
                    text=True,
<<<<<<< HEAD
                    timeout=30,
                )
                return result.returncode == 0

        except Exception as e:
            self.logger.error(f"Error starting {component.name}: {e}")
            return False

=======
                    timeout=30
                )
                return result.returncode == 0
                
        except Exception as e:
            self.logger.error(f"Error starting {component.name}: {e}")
            return False
    
>>>>>>> origin/OS0.6.2.grok
    async def _start_python_component(self, component: ExecutableComponent) -> bool:
        """Start a Python component by importing and initializing"""
        try:
            # Add path to sys.path temporarily
            component_dir = str(component.path.parent)
            if component_dir not in sys.path:
                sys.path.insert(0, component_dir)
<<<<<<< HEAD

            # Import module
            module_name = component.path.stem
            module = importlib.import_module(module_name)

            # Look for initialization patterns
            if hasattr(module, "main"):
=======
            
            # Import module
            module_name = component.path.stem
            module = importlib.import_module(module_name)
            
            # Look for initialization patterns
            if hasattr(module, 'main'):
>>>>>>> origin/OS0.6.2.grok
                if asyncio.iscoroutinefunction(module.main):
                    await module.main()
                else:
                    module.main()
                return True
<<<<<<< HEAD
            elif hasattr(module, "run"):
=======
            elif hasattr(module, 'run'):
>>>>>>> origin/OS0.6.2.grok
                if asyncio.iscoroutinefunction(module.run):
                    await module.run()
                else:
                    module.run()
                return True
            else:
                # Module imported successfully but no clear entry point
                return True
<<<<<<< HEAD

        except Exception as e:
            self.logger.error(f"Error importing {component.name}: {e}")
            return False

    async def health_check_all(self) -> Dict[str, str]:
        """Perform health check on all components"""
        health_status = {}

=======
                
        except Exception as e:
            self.logger.error(f"Error importing {component.name}: {e}")
            return False
    
    async def health_check_all(self) -> Dict[str, str]:
        """Perform health check on all components"""
        health_status = {}
        
>>>>>>> origin/OS0.6.2.grok
        for name, component in self.components.items():
            if component.health_check:
                try:
                    # Attempt to run health check
                    status = await self._check_component_health(component)
                    health_status[name] = status
                except Exception as e:
                    health_status[name] = f"health_check_failed: {e}"
            else:
                # Basic status check
                health_status[name] = self.state.health_status.get(name, "unknown")
<<<<<<< HEAD

        self.state.health_status = health_status
        return health_status

=======
        
        self.state.health_status = health_status
        return health_status
    
>>>>>>> origin/OS0.6.2.grok
    async def _check_component_health(self, component: ExecutableComponent) -> str:
        """Check health of a specific component"""
        # This would be implemented based on component type
        # For now, return basic status
        return self.state.health_status.get(component.name, "unknown")
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    def get_runtime_info(self) -> Dict[str, Any]:
        """Get comprehensive runtime information"""
        return {
            "sequencer_state": {
                "startup_time": self.state.startup_time.isoformat(),
<<<<<<< HEAD
                "uptime_seconds": (
                    datetime.now() - self.state.startup_time
                ).total_seconds(),
                "components_discovered": self.state.components_discovered,
                "components_active": self.state.components_active,
                "components_failed": self.state.components_failed,
                "execution_order": self.state.execution_order,
=======
                "uptime_seconds": (datetime.now() - self.state.startup_time).total_seconds(),
                "components_discovered": self.state.components_discovered,
                "components_active": self.state.components_active,
                "components_failed": self.state.components_failed,
                "execution_order": self.state.execution_order
>>>>>>> origin/OS0.6.2.grok
            },
            "components": {
                name: {
                    "type": comp.type,
                    "category": comp.category,
                    "path": str(comp.path),
                    "auto_start": comp.auto_start,
                    "dependencies": comp.dependencies,
                    "description": comp.description,
                    "status": self.state.health_status.get(name, "unknown"),
                    "entry_point": comp.entry_point,
<<<<<<< HEAD
                    "health_check": comp.health_check,
=======
                    "health_check": comp.health_check
>>>>>>> origin/OS0.6.2.grok
                }
                for name, comp in self.components.items()
            },
            "health_summary": {
                "total": len(self.components),
<<<<<<< HEAD
                "running": len(
                    [s for s in self.state.health_status.values() if s == "running"]
                ),
                "failed": len(
                    [s for s in self.state.health_status.values() if s == "failed"]
                ),
                "unknown": len(
                    [s for s in self.state.health_status.values() if s == "unknown"]
                ),
=======
                "running": len([s for s in self.state.health_status.values() if s == "running"]),
                "failed": len([s for s in self.state.health_status.values() if s == "failed"]),
                "unknown": len([s for s in self.state.health_status.values() if s == "unknown"])
>>>>>>> origin/OS0.6.2.grok
            },
            "interface_bridge": {
                "api_endpoint": "http://localhost:8000",
                "documentation": "http://localhost:8000/docs",
<<<<<<< HEAD
                "csharp_interface": "interface/AIOS.Models/PythonAIToolsBridge.cs",
            },
        }

    def save_runtime_state(self, output_path: Optional[Path] = None) -> Path:
        """Save current runtime state to file"""
        if output_path is None:
            output_path = (
                self.workspace_root
                / "ai"
                / "infrastructure"
                / "runtime"
                / "sequencer_state.json"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        runtime_info = self.get_runtime_info()
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(runtime_info, f, indent=2, ensure_ascii=False)

=======
                "csharp_interface": "interface/AIOS.Models/PythonAIToolsBridge.cs"
            }
        }
    
    def save_runtime_state(self, output_path: Optional[Path] = None) -> Path:
        """Save current runtime state to file"""
        if output_path is None:
            output_path = (self.workspace_root / "ai" / "infrastructure" / 
                          "runtime" / "sequencer_state.json")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        runtime_info = self.get_runtime_info()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(runtime_info, f, indent=2, ensure_ascii=False)
        
>>>>>>> origin/OS0.6.2.grok
        return output_path


async def main():
    """Main sequencer execution"""
    workspace_root = r"C:\dev\AIOS"
    sequencer = AIOSSequencer(workspace_root)
<<<<<<< HEAD

    print("🎯 AIOS Runtime Sequencer Starting...")
    print("=" * 50)

    # Discovery phase
    components = await sequencer.discover_components()
    print(f"📊 Discovery Complete: {len(components)} components found")

=======
    
    print("🎯 AIOS Runtime Sequencer Starting...")
    print("=" * 50)
    
    # Discovery phase
    components = await sequencer.discover_components()
    print(f"📊 Discovery Complete: {len(components)} components found")
    
>>>>>>> origin/OS0.6.2.grok
    # Validation phase
    valid, missing = await sequencer.validate_dependencies()
    if not valid:
        print(f"⚠️  Dependency issues: {len(missing)} missing")
        for issue in missing[:5]:  # Show first 5
            print(f"   • {issue}")
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    # Execution phase
    results = await sequencer.start_components(auto_start_only=True)
    active = len([r for r in results.values() if r])
    print(f"🚀 Startup Complete: {active}/{len(results)} components active")
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    # Health check
    health = await sequencer.health_check_all()
    print("🏥 Health Status:")
    for name, status in list(health.items())[:5]:  # Show first 5
        emoji = "✅" if status == "running" else "❌" if "failed" in status else "❓"
        print(f"   {emoji} {name}: {status}")
<<<<<<< HEAD

    # Save state
    state_file = sequencer.save_runtime_state()
    print(f"💾 Runtime state saved: {state_file}")

=======
    
    # Save state
    state_file = sequencer.save_runtime_state()
    print(f"💾 Runtime state saved: {state_file}")
    
>>>>>>> origin/OS0.6.2.grok
    # Display summary
    info = sequencer.get_runtime_info()
    print("\n📋 AIOS Runtime Summary:")
    print(f"   • Total Components: {info['sequencer_state']['components_discovered']}")
    print(f"   • Active: {info['sequencer_state']['components_active']}")
    print(f"   • Failed: {info['sequencer_state']['components_failed']}")
    print(f"   • Uptime: {info['sequencer_state']['uptime_seconds']:.1f}s")
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    return sequencer


if __name__ == "__main__":
<<<<<<< HEAD
    asyncio.run(main())
=======
    asyncio.run(main())
>>>>>>> origin/OS0.6.2.grok
