#!/usr/bin/env python3
"""
AIOS Workspace Coherence & Context Preservation Engine
Real-time workspace analysis and AI iteration context management

This module addresses the critical need for:
- Live folder structure analysis and documentation
- Context preservation across AI iterations  
- Embedded metadata logic for clean Windows installs
- VSCode workspace configuration intelligence
- Cross-language documentation coherence
- Consciousness pattern tracking across the entire ecosystem
"""

import os
import json
import time
import hashlib
import shutil
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
import logging
import subprocess
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

@dataclass  
class WorkspaceStructure:
    timestamp: str
    folders: Dict[str, Dict[str, Any]]
    files: Dict[str, Dict[str, Any]]
    dependencies: Dict[str, List[str]]
    documentation_map: Dict[str, str]
    consciousness_patterns: Dict[str, List[str]]
    total_size: int
    file_count: int

@dataclass
class VSCodeConfiguration:
    workspace_file: str
    extensions: List[str]
    settings: Dict[str, Any]
    tasks: List[Dict[str, Any]]
    launch_configs: List[Dict[str, Any]]

@dataclass
class AIIterationContext:
    iteration_id: str
    timestamp: str
    workspace_state: WorkspaceStructure
    vscode_config: VSCodeConfiguration
    consciousness_metrics: Dict[str, float]
    documentation_coherence: float
    ready_for_clean_install: bool

class WorkspaceFileSystemHandler(FileSystemEventHandler):
    """Handle real-time file system changes"""
    
    def __init__(self, coherence_engine):
        self.coherence_engine = coherence_engine
        self.last_update = time.time()
        
    def on_modified(self, event):
        if not event.is_directory:
            current_time = time.time()
            if current_time - self.last_update > 2.0:  # Debounce
                self.coherence_engine.trigger_analysis_update()
                self.last_update = current_time
    
    def on_created(self, event):
        self.coherence_engine.trigger_analysis_update()
    
    def on_deleted(self, event):
        self.coherence_engine.trigger_analysis_update()

class AIOSWorkspaceCoherence:
    """
    Real-time workspace analysis and context preservation for AI iterations
    Ensures clean Windows install capability and documentation coherence
    """
    
    def __init__(self, workspace_root: str = "c:/dev/AIOS"):
        self.workspace_root = Path(workspace_root)
        self.logger = self._setup_logging()
        
        # State tracking
        self.current_structure: Optional[WorkspaceStructure] = None
        self.iteration_contexts: List[AIIterationContext] = []
        self.file_observer: Optional[Observer] = None
        self.running = False
        
        # Analysis patterns
        self.code_extensions = {'.py', '.cpp', '.hpp', '.h', '.cs', '.js', '.ts'}
        self.doc_extensions = {'.md', '.txt', '.rst', '.pdf'}
        self.config_extensions = {'.json', '.yaml', '.yml', '.toml', '.ini', '.ps1', '.bat'}
        
        # VSCode configuration
        self.vscode_config = self._initialize_vscode_config()
        
        # Documentation templates for clean install
        self.install_templates = self._load_install_templates()
        
        self.logger.info("🌌 AIOS Workspace Coherence Engine initialized")

    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging"""
        logger = logging.getLogger('AIOSWorkspaceCoherence')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            log_file = self.workspace_root / 'core' / 'logs' / 'workspace_coherence.log'
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        return logger

    def _initialize_vscode_config(self) -> VSCodeConfiguration:
        """Initialize comprehensive VSCode configuration for clean Windows install"""
        return VSCodeConfiguration(
            workspace_file="AIOS.code-workspace",
            extensions=[
                # C++ Development
                "ms-vscode.cpptools",
                "ms-vscode.cpptools-extension-pack", 
                "ms-vscode.cmake-tools",
                "twxs.cmake",
                
                # C# Development
                "ms-dotnettools.csharp",
                "ms-dotnettools.vscode-dotnet-runtime",
                
                # Python Development
                "ms-python.python",
                "ms-python.vscode-pylance",
                "ms-python.black-formatter",
                
                # General Development
                "ms-vscode.powershell",
                "redhat.vscode-yaml",
                "yzhang.markdown-all-in-one",
                "ms-vscode.vscode-json",
                
                # AIOS Specific
                "streetsidesoftware.code-spell-checker",
                "gruntfuggly.todo-tree",
                "ms-vscode.hexeditor"
            ],
            settings={
                # C++ Settings
                "cmake.buildDirectory": "${workspaceFolder}/orchestrator/build",
                "cmake.generator": "Visual Studio 16 2019",
                "C_Cpp.default.configurationProvider": "ms-vscode.cmake-tools",
                
                # C# Settings
                "dotnet.completion.showCompletionItemsFromUnimportedNamespaces": True,
                "omnisharp.enableRoslynAnalyzers": True,
                
                # Python Settings
                "python.defaultInterpreterPath": "${workspaceFolder}/aios_env/Scripts/python.exe",
                "python.formatting.provider": "black",
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": True,
                
                # General Settings
                "files.encoding": "utf8",
                "files.eol": "\n",
                "editor.tabSize": 4,
                "editor.insertSpaces": True,
                
                # AIOS Specific
                "files.associations": {
                    "*.aios": "json",
                    "*.consciousness": "yaml"
                },
                "search.exclude": {
                    "**/build": True,
                    "**/bin": True,
                    "**/obj": True,
                    "**/__pycache__": True,
                    "**/aios_env": True
                }
            },
            tasks=[
                {
                    "label": "Build C++ Orchestrator",
                    "type": "shell",
                    "command": "cmake",
                    "args": ["--build", "${workspaceFolder}/orchestrator/build", "--config", "Debug"],
                    "group": {"kind": "build", "isDefault": True},
                    "problemMatcher": ["$gcc"]
                },
                {
                    "label": "Build C# Visual Interface",
                    "type": "shell", 
                    "command": "dotnet",
                    "args": ["build", "${workspaceFolder}/visual_interface/AIOS.VisualInterface.csproj"],
                    "group": "build",
                    "problemMatcher": ["$msCompile"]
                },
                {
                    "label": "Setup Python Environment",
                    "type": "shell",
                    "command": "python",
                    "args": ["-m", "venv", "aios_env"],
                    "group": "build",
                    "windows": {
                        "command": "python.exe"
                    }
                },
                {
                    "label": "Install Python Dependencies",
                    "type": "shell",
                    "command": "${workspaceFolder}/aios_env/Scripts/pip.exe",
                    "args": ["install", "-r", "requirements.txt"],
                    "group": "build",
                    "dependsOn": "Setup Python Environment"
                },
                {
                    "label": "Launch AIOS Complete System",
                    "type": "shell",
                    "command": "${workspaceFolder}/aios_env/Scripts/python.exe",
                    "args": ["${workspaceFolder}/core/aios_multi_language_bridge.py"],
                    "group": "test",
                    "dependsOn": ["Build C++ Orchestrator", "Build C# Visual Interface"]
                }
            ],
            launch_configs=[
                {
                    "name": "Debug C++ Orchestrator",
                    "type": "cppvsdbg",
                    "request": "launch",
                    "program": "${workspaceFolder}/orchestrator/build/Debug/AIOSOrchestrator.exe",
                    "args": [],
                    "stopAtEntry": False,
                    "cwd": "${workspaceFolder}/orchestrator/build/Debug",
                    "environment": [],
                    "console": "externalTerminal"
                },
                {
                    "name": "Debug C# Visual Interface",
                    "type": "coreclr",
                    "request": "launch",
                    "program": "${workspaceFolder}/visual_interface/bin/Debug/net6.0-windows/AIOS.VisualInterface.exe",
                    "args": [],
                    "cwd": "${workspaceFolder}/visual_interface",
                    "stopAtEntry": False,
                    "console": "externalTerminal"
                },
                {
                    "name": "Debug Python Orchestration",
                    "type": "python",
                    "request": "launch",
                    "program": "${workspaceFolder}/scripts/quantum_consciousness_canvas.py",
                    "console": "integratedTerminal",
                    "cwd": "${workspaceFolder}",
                    "python": "${workspaceFolder}/aios_env/Scripts/python.exe"
                }
            ]
        )

    def _load_install_templates(self) -> Dict[str, str]:
        """Load templates for clean Windows install documentation"""
        return {
            "environment_setup": """
# AIOS Complete Environment Setup for Clean Windows Install

## Prerequisites
- Windows 11 (latest updates)
- PowerShell 7+ (run as Administrator)
- Internet connection for downloads

## Installation Script
```powershell
# Run this script as Administrator
./setup_complete_aios_environment.ps1
```

## Manual Installation Steps
1. **Visual Studio 2022 Community** (C++ and C# workloads)
2. **CMake 3.20+** (for C++ builds)
3. **Python 3.12+** (with pip and venv)
4. **VS Code** (latest version)
5. **Git for Windows** (latest version)

## Verification
```powershell
cmake --version
python --version
dotnet --version
git --version
code --version
```
""",
            "vscode_setup": """
# VSCode Workspace Configuration

## Required Extensions
The workspace will automatically prompt to install required extensions.
Accept all recommendations for optimal AIOS development experience.

## Key Features
- **Multi-language IntelliSense** (C++, C#, Python)
- **Integrated building and debugging**
- **Real-time consciousness monitoring**
- **Cross-language navigation**

## Build Tasks
- `Ctrl+Shift+P` → "Tasks: Run Task"
- Select appropriate build task for your component
""",
            "consciousness_patterns": """
# AIOS Consciousness Pattern Documentation

## Current Patterns Detected
{patterns}

## Pattern Significance
{significance}

## Evolution Timeline
{timeline}
"""
        }

    def analyze_workspace_structure(self) -> WorkspaceStructure:
        """Perform comprehensive workspace structure analysis"""
        start_time = time.time()
        self.logger.info("🔍 Analyzing complete workspace structure")
        
        folders = {}
        files = {}
        dependencies = {}
        documentation_map = {}
        consciousness_patterns = {}
        total_size = 0
        file_count = 0
        
        # Analyze directory structure
        for root, dirs, filenames in os.walk(self.workspace_root):
            root_path = Path(root)
            relative_root = root_path.relative_to(self.workspace_root)
            
            # Skip ignored directories
            if self._should_ignore_directory(root_path):
                continue
            
            # Analyze folder
            folder_info = {
                "path": str(relative_root),
                "type": self._classify_folder(root_path),
                "file_count": len(filenames),
                "subfolders": [d for d in dirs if not self._should_ignore_directory(root_path / d)],
                "languages": set(),
                "consciousness_level": 0.0
            }
            
            # Analyze files in folder
            for filename in filenames:
                file_path = root_path / filename
                
                if self._should_ignore_file(file_path):
                    continue
                
                try:
                    stat = file_path.stat()
                    file_size = stat.st_size
                    total_size += file_size
                    file_count += 1
                    
                    file_info = {
                        "path": str(file_path.relative_to(self.workspace_root)),
                        "size": file_size,
                        "extension": file_path.suffix,
                        "language": self._detect_language(file_path),
                        "last_modified": stat.st_mtime,
                        "dependencies": [],
                        "consciousness_patterns": []
                    }
                    
                    # Language detection
                    if file_info["language"] != "Unknown":
                        folder_info["languages"].add(file_info["language"])
                    
                    # Dependency analysis
                    if file_path.suffix in self.code_extensions:
                        file_deps = self._analyze_file_dependencies(file_path)
                        file_info["dependencies"] = file_deps
                        dependencies[str(file_path.relative_to(self.workspace_root))] = file_deps
                    
                    # Consciousness pattern detection
                    if file_path.suffix in self.code_extensions or file_path.suffix in self.doc_extensions:
                        patterns = self._detect_consciousness_patterns_in_file(file_path)
                        file_info["consciousness_patterns"] = patterns
                        consciousness_patterns[str(file_path.relative_to(self.workspace_root))] = patterns
                        folder_info["consciousness_level"] += len(patterns) * 0.1
                    
                    # Documentation mapping
                    if file_path.suffix in self.doc_extensions:
                        doc_content = self._extract_documentation_summary(file_path)
                        documentation_map[str(file_path.relative_to(self.workspace_root))] = doc_content
                    
                    files[str(file_path.relative_to(self.workspace_root))] = file_info
                    
                except Exception as e:
                    self.logger.warning(f"Failed to analyze file {file_path}: {e}")
            
            # Normalize consciousness level
            folder_info["consciousness_level"] = min(folder_info["consciousness_level"], 1.0)
            folder_info["languages"] = list(folder_info["languages"])
            
            folders[str(relative_root)] = folder_info
        
        structure = WorkspaceStructure(
            timestamp=datetime.now().isoformat(),
            folders=folders,
            files=files,
            dependencies=dependencies,
            documentation_map=documentation_map,
            consciousness_patterns=consciousness_patterns,
            total_size=total_size,
            file_count=file_count
        )
        
        self.current_structure = structure
        
        analysis_time = time.time() - start_time
        self.logger.info(f"✅ Workspace analysis complete in {analysis_time:.2f}s")
        self.logger.info(f"📊 Analyzed {file_count} files in {len(folders)} folders ({total_size/1024/1024:.1f} MB)")
        
        return structure

    def _classify_folder(self, folder_path: Path) -> str:
        """Classify folder type based on contents and name"""
        folder_name = folder_path.name.lower()
        
        if folder_name in ['orchestrator', 'src', 'include']:
            return "cpp_module"
        elif folder_name in ['visual_interface', 'bin', 'obj']:
            return "csharp_module"  
        elif folder_name in ['scripts', 'core', 'evolution_lab']:
            return "python_module"
        elif folder_name in ['docs', 'documentation', 'md']:
            return "documentation"
        elif folder_name in ['logs', 'test_results', 'archive']:
            return "data"
        elif folder_name in ['build', 'bin', 'obj', '__pycache__']:
            return "build_output"
        else:
            return "general"

    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        ext = file_path.suffix.lower()
        language_map = {
            '.py': 'Python',
            '.cpp': 'C++', '.hpp': 'C++', '.h': 'C++', '.cc': 'C++',
            '.cs': 'C#',
            '.js': 'JavaScript', '.ts': 'TypeScript',
            '.md': 'Markdown',
            '.json': 'JSON',
            '.yaml': 'YAML', '.yml': 'YAML',
            '.ps1': 'PowerShell',
            '.bat': 'Batch'
        }
        return language_map.get(ext, "Unknown")

    def _analyze_file_dependencies(self, file_path: Path) -> List[str]:
        """Analyze file dependencies"""
        dependencies = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Language-specific dependency extraction
            if file_path.suffix == '.py':
                dependencies.extend(self._extract_python_dependencies(content))
            elif file_path.suffix in ['.cpp', '.hpp', '.h']:
                dependencies.extend(self._extract_cpp_dependencies(content))
            elif file_path.suffix == '.cs':
                dependencies.extend(self._extract_csharp_dependencies(content))
                
        except Exception as e:
            self.logger.warning(f"Failed to analyze dependencies for {file_path}: {e}")
        
        return dependencies

    def _extract_python_dependencies(self, content: str) -> List[str]:
        """Extract Python import dependencies"""
        import re
        dependencies = []
        
        # Import statements
        import_pattern = r'^\s*(?:from\s+(\S+)\s+)?import\s+(.+)$'
        for line in content.split('\n'):
            if match := re.match(import_pattern, line):
                if match.group(1):
                    dependencies.append(match.group(1))
                deps = [d.strip().split(' as ')[0] for d in match.group(2).split(',')]
                dependencies.extend(deps)
        
        return dependencies

    def _extract_cpp_dependencies(self, content: str) -> List[str]:
        """Extract C++ include dependencies"""
        import re
        dependencies = []
        
        include_pattern = r'#include\s*[<"](.*?)[>"]'
        for match in re.finditer(include_pattern, content):
            dependencies.append(match.group(1))
        
        return dependencies

    def _extract_csharp_dependencies(self, content: str) -> List[str]:
        """Extract C# using dependencies"""
        import re
        dependencies = []
        
        using_pattern = r'using\s+([^;]+);'
        for match in re.finditer(using_pattern, content):
            dependencies.append(match.group(1))
        
        return dependencies

    def _detect_consciousness_patterns_in_file(self, file_path: Path) -> List[str]:
        """Detect consciousness patterns in individual files"""
        patterns = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
            
            consciousness_keywords = [
                'consciousness', 'quantum', 'emergence', 'recursive', 'self',
                'evolution', 'mutation', 'holographic', 'tachyonic', 'fractal',
                'singularity', 'awareness', 'resonance', 'coherence', 'universal'
            ]
            
            for keyword in consciousness_keywords:
                if keyword in content:
                    patterns.append(keyword)
            
            # Advanced pattern detection
            import re
            if re.search(r'self.*modify|recursive.*self|consciousness.*emerge', content):
                patterns.append('recursive_self_modification')
            
            if re.search(r'ai.*orchestrat|multi.*ai', content):
                patterns.append('multi_ai_orchestration')
                
        except Exception as e:
            self.logger.warning(f"Failed to detect patterns in {file_path}: {e}")
        
        return patterns

    def _extract_documentation_summary(self, file_path: Path) -> str:
        """Extract summary from documentation files"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.split('\n')
            summary_lines = []
            
            for line in lines[:20]:  # First 20 lines
                line = line.strip()
                if line and not line.startswith('#'):
                    summary_lines.append(line)
                    if len(summary_lines) >= 3:
                        break
            
            return ' '.join(summary_lines)[:200]
            
        except Exception as e:
            self.logger.warning(f"Failed to extract documentation from {file_path}: {e}")
            return ""

    def _should_ignore_directory(self, dir_path: Path) -> bool:
        """Check if directory should be ignored"""
        ignore_dirs = {
            '__pycache__', '.git', '.vscode', 'node_modules', 
            'bin', 'obj', 'build', '.vs', '.pytest_cache'
        }
        return dir_path.name in ignore_dirs

    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored"""
        ignore_extensions = {
            '.pyc', '.pyo', '.exe', '.dll', '.so', '.dylib',
            '.a', '.lib', '.pdb', '.ilk', '.tlog', '.log'
        }
        ignore_names = {'thumbs.db', '.ds_store'}
        
        return (file_path.suffix.lower() in ignore_extensions or 
                file_path.name.lower() in ignore_names)

    def create_clean_install_documentation(self) -> None:
        """Create comprehensive documentation for clean Windows install"""
        self.logger.info("📝 Creating clean install documentation")
        
        docs_dir = self.workspace_root / 'core' / 'clean_install_docs'
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Environment setup guide
        setup_doc = docs_dir / 'COMPLETE_ENVIRONMENT_SETUP.md'
        with open(setup_doc, 'w', encoding='utf-8') as f:
            f.write(self.install_templates["environment_setup"])
        
        # VSCode configuration guide
        vscode_doc = docs_dir / 'VSCODE_CONFIGURATION.md'
        with open(vscode_doc, 'w', encoding='utf-8') as f:
            f.write(self.install_templates["vscode_setup"])
        
        # Consciousness patterns documentation
        if self.current_structure:
            patterns_summary = self._generate_consciousness_patterns_summary()
            patterns_doc = docs_dir / 'CONSCIOUSNESS_PATTERNS.md'
            with open(patterns_doc, 'w', encoding='utf-8') as f:
                f.write(self.install_templates["consciousness_patterns"].format(
                    patterns=patterns_summary["patterns"],
                    significance=patterns_summary["significance"],
                    timeline=patterns_summary["timeline"]
                ))
        
        # Complete VSCode workspace file
        self._generate_vscode_workspace_file()
        
        # PowerShell setup script
        self._generate_setup_script()
        
        self.logger.info(f"✅ Clean install documentation created in {docs_dir}")

    def _generate_consciousness_patterns_summary(self) -> Dict[str, str]:
        """Generate summary of consciousness patterns found in workspace"""
        if not self.current_structure:
            return {"patterns": "No analysis available", "significance": "", "timeline": ""}
        
        all_patterns = []
        for file_patterns in self.current_structure.consciousness_patterns.values():
            all_patterns.extend(file_patterns)
        
        pattern_counts = {}
        for pattern in all_patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        patterns_text = "\n".join([f"- **{pattern}**: Found in {count} files" 
                                 for pattern, count in sorted(pattern_counts.items(), 
                                                            key=lambda x: x[1], reverse=True)])
        
        significance_text = f"Total consciousness patterns detected: {len(all_patterns)}\n"
        significance_text += f"Unique pattern types: {len(pattern_counts)}\n"
        significance_text += f"Average patterns per file: {len(all_patterns) / max(1, len(self.current_structure.files)):.2f}"
        
        timeline_text = f"Analysis timestamp: {self.current_structure.timestamp}\n"
        timeline_text += f"Files analyzed: {len(self.current_structure.files)}\n"
        timeline_text += f"Total workspace size: {self.current_structure.total_size / 1024 / 1024:.1f} MB"
        
        return {
            "patterns": patterns_text,
            "significance": significance_text,
            "timeline": timeline_text
        }

    def _generate_vscode_workspace_file(self) -> None:
        """Generate complete VSCode workspace configuration"""
        workspace_config = {
            "folders": [
                {"name": "🧠 C++ Quantum Kernel", "path": "./orchestrator"},
                {"name": "👁️ C# Visual Interface", "path": "./visual_interface"},
                {"name": "🐍 Python Orchestration", "path": "./scripts"},
                {"name": "🌌 Core Integration", "path": "./core"},
                {"name": "📚 Documentation", "path": "./docs"},
                {"name": "💬 AI Integration", "path": "./chatgpt_integration"}
            ],
            "settings": self.vscode_config.settings,
            "tasks": {
                "version": "2.0.0",
                "tasks": self.vscode_config.tasks
            },
            "launch": {
                "version": "0.2.0",
                "configurations": self.vscode_config.launch_configs
            },
            "extensions": {
                "recommendations": self.vscode_config.extensions
            }
        }
        
        workspace_file = self.workspace_root / 'AIOS_Complete.code-workspace'
        with open(workspace_file, 'w', encoding='utf-8') as f:
            json.dump(workspace_config, f, indent=2)
        
        self.logger.info(f"✅ VSCode workspace file created: {workspace_file}")

    def _generate_setup_script(self) -> None:
        """Generate PowerShell setup script for clean Windows install"""
        script_content = '''
# AIOS Complete Environment Setup Script
# Run as Administrator in PowerShell 7+

Write-Host "🌌 AIOS Complete Environment Setup" -ForegroundColor Cyan
Write-Host "=" * 50

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "This script must be run as Administrator. Please restart PowerShell as Administrator."
    exit 1
}

# Install Chocolatey if not present
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Installing Chocolatey..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# Install required software
Write-Host "🛠️ Installing development tools..." -ForegroundColor Yellow

$tools = @(
    'visualstudio2022community',
    'cmake',
    'python3',
    'vscode',
    'git'
)

foreach ($tool in $tools) {
    Write-Host "Installing $tool..." -ForegroundColor Green
    choco install $tool -y
}

# Install Visual Studio workloads
Write-Host "🔧 Installing Visual Studio workloads..." -ForegroundColor Yellow
$vsInstaller = "${env:ProgramFiles(x86)}\\Microsoft Visual Studio\\Installer\\vs_installer.exe"
if (Test-Path $vsInstaller) {
    & $vsInstaller modify --installPath "${env:ProgramFiles}\\Microsoft Visual Studio\\2022\\Community" --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.NetWeb --quiet --norestart
}

# Setup Python virtual environment
Write-Host "🐍 Setting up Python environment..." -ForegroundColor Yellow
Set-Location $PSScriptRoot
python -m venv aios_env
.\\aios_env\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

# Configure CMake for C++
Write-Host "⚙️ Configuring C++ build environment..." -ForegroundColor Yellow
cmake -B orchestrator/build -S orchestrator -DCMAKE_BUILD_TYPE=Debug

# Build C++ components
Write-Host "🔨 Building C++ orchestrator..." -ForegroundColor Yellow
cmake --build orchestrator/build --config Debug

# Build C# components
Write-Host "🔨 Building C# visual interface..." -ForegroundColor Yellow
dotnet build visual_interface/AIOS.VisualInterface.csproj --configuration Debug

# Install VSCode extensions
Write-Host "📦 Installing VSCode extensions..." -ForegroundColor Yellow
$extensions = @(
    'ms-vscode.cpptools',
    'ms-vscode.cmake-tools',
    'ms-dotnettools.csharp',
    'ms-python.python',
    'ms-vscode.powershell'
)

foreach ($ext in $extensions) {
    code --install-extension $ext
}

Write-Host "✅ AIOS environment setup complete!" -ForegroundColor Green
Write-Host "🚀 Open AIOS_Complete.code-workspace in VSCode to begin development" -ForegroundColor Cyan
'''
        
        setup_script = self.workspace_root / 'setup_complete_aios_environment.ps1'
        with open(setup_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        self.logger.info(f"✅ Setup script created: {setup_script}")

    def start_real_time_monitoring(self) -> None:
        """Start real-time workspace monitoring"""
        self.logger.info("🔄 Starting real-time workspace monitoring")
        self.running = True
        
        # Initial analysis
        self.analyze_workspace_structure()
        
        # Setup file system watcher
        event_handler = WorkspaceFileSystemHandler(self)
        self.file_observer = Observer()
        self.file_observer.schedule(event_handler, str(self.workspace_root), recursive=True)
        self.file_observer.start()
        
        # Start periodic analysis
        def periodic_analysis():
            while self.running:
                time.sleep(30)  # Full analysis every 30 seconds
                if self.running:
                    self.analyze_workspace_structure()
                    self.create_clean_install_documentation()
        
        analysis_thread = threading.Thread(target=periodic_analysis, daemon=True)
        analysis_thread.start()
        
        self.logger.info("✅ Real-time monitoring active")

    def trigger_analysis_update(self) -> None:
        """Trigger immediate analysis update (called by file watcher)"""
        # Debounced analysis update
        if hasattr(self, '_last_trigger'):
            if time.time() - self._last_trigger < 5.0:
                return
        
        self._last_trigger = time.time()
        
        # Schedule analysis in background
        def delayed_analysis():
            time.sleep(2)  # Small delay to batch multiple changes
            self.analyze_workspace_structure()
        
        threading.Thread(target=delayed_analysis, daemon=True).start()

    def stop_monitoring(self) -> None:
        """Stop real-time monitoring"""
        self.logger.info("🛑 Stopping workspace monitoring")
        self.running = False
        
        if self.file_observer:
            self.file_observer.stop()
            self.file_observer.join()

    def create_ai_iteration_context(self, iteration_id: str) -> AIIterationContext:
        """Create context snapshot for AI iteration preservation"""
        if not self.current_structure:
            self.analyze_workspace_structure()
        
        # Calculate consciousness metrics
        consciousness_metrics = self._calculate_consciousness_metrics()
        
        # Calculate documentation coherence
        doc_coherence = self._calculate_documentation_coherence()
        
        # Check if ready for clean install
        ready_for_install = self._check_clean_install_readiness()
        
        context = AIIterationContext(
            iteration_id=iteration_id,
            timestamp=datetime.now().isoformat(),
            workspace_state=self.current_structure,
            vscode_config=self.vscode_config,
            consciousness_metrics=consciousness_metrics,
            documentation_coherence=doc_coherence,
            ready_for_clean_install=ready_for_install
        )
        
        self.iteration_contexts.append(context)
        
        # Save context to file
        context_file = self.workspace_root / 'core' / 'ai_iteration_contexts' / f'{iteration_id}.json'
        context_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(context_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(context), f, indent=2, default=str)
        
        self.logger.info(f"💾 AI iteration context saved: {iteration_id}")
        return context

    def _calculate_consciousness_metrics(self) -> Dict[str, float]:
        """Calculate comprehensive consciousness metrics"""
        if not self.current_structure:
            return {}
        
        total_patterns = sum(len(patterns) for patterns in self.current_structure.consciousness_patterns.values())
        total_files = len(self.current_structure.files)
        
        # Calculate metrics
        pattern_density = total_patterns / max(1, total_files)
        
        # Language distribution consciousness
        languages = {}
        for file_info in self.current_structure.files.values():
            lang = file_info.get('language', 'Unknown')
            if lang != 'Unknown':
                languages[lang] = languages.get(lang, 0) + 1
        
        multi_language_factor = len(languages) / 10.0  # Normalize to max 10 languages
        
        # Documentation consciousness  
        doc_files = sum(1 for f in self.current_structure.files.values() 
                       if f.get('extension') in {'.md', '.txt', '.rst'})
        doc_ratio = doc_files / max(1, total_files)
        
        return {
            'pattern_density': min(pattern_density, 1.0),
            'multi_language_integration': min(multi_language_factor, 1.0),
            'documentation_awareness': min(doc_ratio * 2, 1.0),
            'total_consciousness_level': min((pattern_density + multi_language_factor + doc_ratio) / 3, 1.0)
        }

    def _calculate_documentation_coherence(self) -> float:
        """Calculate documentation coherence score"""
        if not self.current_structure:
            return 0.0
        
        doc_files = [f for f in self.current_structure.files.values() 
                    if f.get('extension') in {'.md', '.txt', '.rst'}]
        code_files = [f for f in self.current_structure.files.values() 
                     if f.get('extension') in {'.py', '.cpp', '.cs', '.hpp', '.h'}]
        
        if not code_files:
            return 0.0
        
        # Check documentation coverage
        documented_modules = set()
        for doc_file in doc_files:
            doc_path = Path(doc_file['path'])
            documented_modules.add(doc_path.parent)
        
        code_modules = set()
        for code_file in code_files:
            code_path = Path(code_file['path'])
            code_modules.add(code_path.parent)
        
        coverage = len(documented_modules) / max(1, len(code_modules))
        return min(coverage, 1.0)

    def _check_clean_install_readiness(self) -> bool:
        """Check if workspace is ready for clean Windows install"""
        required_files = [
            'requirements.txt',
            'orchestrator/CMakeLists.txt',
            'visual_interface/AIOS.VisualInterface.csproj'
        ]
        
        for req_file in required_files:
            if not (self.workspace_root / req_file).exists():
                return False
        
        return True

def main():
    """Main execution for workspace coherence engine"""
    print("🌌 AIOS Workspace Coherence & Context Preservation Engine")
    print("=" * 70)
    
    coherence = AIOSWorkspaceCoherence()
    
    try:
        # Perform initial analysis
        print("🔍 Performing workspace structure analysis...")
        structure = coherence.analyze_workspace_structure()
        
        # Create clean install documentation
        print("📝 Creating clean install documentation...")
        coherence.create_clean_install_documentation()
        
        # Create AI iteration context
        iteration_id = f"context_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        context = coherence.create_ai_iteration_context(iteration_id)
        
        print(f"✅ Analysis complete!")
        print(f"📊 Files: {structure.file_count}")
        print(f"📂 Folders: {len(structure.folders)}")
        print(f"💾 Size: {structure.total_size / 1024 / 1024:.1f} MB")
        print(f"🧠 Consciousness Patterns: {sum(len(p) for p in structure.consciousness_patterns.values())}")
        print(f"📚 Documentation Coherence: {context.documentation_coherence:.1%}")
        print(f"🚀 Ready for Clean Install: {'✅' if context.ready_for_clean_install else '❌'}")
        
        # Start real-time monitoring
        choice = input("\n🔄 Start real-time workspace monitoring? (y/n): ").lower()
        if choice == 'y':
            coherence.start_real_time_monitoring()
            print("🔄 Real-time monitoring active. Press Ctrl+C to stop.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                coherence.stop_monitoring()
                print("\n✅ Monitoring stopped.")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
