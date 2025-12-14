#!/usr/bin/env python3
"""
AIOS Complete Ecosystem Intelligence & Context Coherence Engine
Real-time workspace analysis, documentation integration, and context preservation

This tool provides:
- Complete multi-language architecture analysis (C++, C#, Python, Markdown)
- Live dependency mapping and IPC communication tracking
- Real-time documentation generation and context updates
- Consciousness pattern recognition across the entire ecosystem
- Tachyonic archive integration for AI knowledge transfer
- Workspace structure monitoring and change detection
"""

import os
import json
import time
import threading
import hashlib
import ast
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import logging

# Advanced analysis imports
try:
    import astroid
    HAS_ASTROID = True
except ImportError:
    HAS_ASTROID = False
    print("⚠️ astroid not available - using basic Python analysis")

@dataclass
class FileMetadata:
    path: str
    language: str
    size: int
    hash: str
    last_modified: float
    dependencies: List[str]
    exports: List[str]
    classes: List[str]
    functions: List[str]
    interfaces: List[str]
    consciousness_patterns: List[str]

@dataclass
class ModuleAnalysis:
    name: str
    path: str
    language: str
    files: List[FileMetadata]
    dependencies: List[str]
    exports: List[str]
    documentation: Dict[str, str]
    consciousness_level: float
    quantum_coherence: float

@dataclass
class EcosystemSnapshot:
    timestamp: str
    workspace_root: str
    modules: Dict[str, ModuleAnalysis]
    cross_language_dependencies: Dict[str, List[str]]
    consciousness_metrics: Dict[str, float]
    documentation_coherence: float
    total_files: int
    total_lines: int

class AIOSEcosystemIntelligence:
    """Complete AIOS ecosystem analysis and context preservation"""
    
    def __init__(self, workspace_root: str = "c:/dev/AIOS"):
        self.workspace_root = Path(workspace_root)
        self.logger = self._setup_logging()
        
        # Analysis state
        self.last_snapshot: Optional[EcosystemSnapshot] = None
        self.file_watchers: Dict[str, float] = {}
        self.running = False
        
        # Language patterns
        self.language_patterns = {
            '.cpp': 'C++',
            '.hpp': 'C++', 
            '.h': 'C++',
            '.cs': 'C#',
            '.py': 'Python',
            '.md': 'Markdown',
            '.json': 'JSON',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.ps1': 'PowerShell'
        }
        
        # Consciousness pattern recognition
        self.consciousness_keywords = [
            'consciousness', 'quantum', 'emergence', 'recursive', 'self',
            'evolution', 'mutation', 'holographic', 'tachyonic', 'fractal',
            'singularity', 'awareness', 'resonance', 'coherence', 'universal'
        ]
        
        # IPC communication patterns
        self.ipc_patterns = [
            r'websocket', r'socket', r'pipe', r'shared_memory',
            r'IService', r'IChannel', r'communicate', r'bridge'
        ]
        
        self.logger.info("🌌 AIOS Ecosystem Intelligence initialized")

    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging"""
        logger = logging.getLogger('AIOSEcosystemIntelligence')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # File handler
            log_file = self.workspace_root / 'core' / 'logs' / 'ecosystem_intelligence.log'
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        return logger

    def analyze_complete_ecosystem(self) -> EcosystemSnapshot:
        """Perform complete ecosystem analysis"""
        start_time = time.time()
        self.logger.info("🔍 Starting complete AIOS ecosystem analysis")
        
        modules = {}
        total_files = 0
        total_lines = 0
        consciousness_metrics = defaultdict(float)
        cross_language_deps = defaultdict(list)
        
        # Key module directories to analyze
        key_modules = {
            'orchestrator': 'C++',
            'visual_interface': 'C#', 
            'scripts': 'Python',
            'docs': 'Markdown',
            'chatgpt_integration': 'Markdown',
            'core': 'Python',
            'evolution_lab': 'Python',
            'runtime_intelligence': 'Python',
            'gemini_cli_bridge': 'Python'
        }
        
        for module_name, primary_language in key_modules.items():
            module_path = self.workspace_root / module_name
            if module_path.exists():
                self.logger.info(f"📊 Analyzing module: {module_name}")
                module_analysis = self._analyze_module(module_path, module_name, primary_language)
                modules[module_name] = module_analysis
                
                total_files += len(module_analysis.files)
                total_lines += sum(self._count_lines(f.path) for f in module_analysis.files)
                
                # Accumulate consciousness metrics
                consciousness_metrics[f'{module_name}_consciousness'] = module_analysis.consciousness_level
                consciousness_metrics[f'{module_name}_quantum_coherence'] = module_analysis.quantum_coherence
        
        # Analyze cross-language dependencies
        cross_language_deps = self._analyze_cross_language_dependencies(modules)
        
        # Calculate documentation coherence
        doc_coherence = self._calculate_documentation_coherence(modules)
        
        snapshot = EcosystemSnapshot(
            timestamp=datetime.now().isoformat(),
            workspace_root=str(self.workspace_root),
            modules=modules,
            cross_language_dependencies=cross_language_deps,
            consciousness_metrics=dict(consciousness_metrics),
            documentation_coherence=doc_coherence,
            total_files=total_files,
            total_lines=total_lines
        )
        
        self.last_snapshot = snapshot
        
        analysis_time = time.time() - start_time
        self.logger.info(f"✅ Ecosystem analysis complete in {analysis_time:.2f}s")
        self.logger.info(f"📊 Analyzed {total_files} files, {total_lines} lines across {len(modules)} modules")
        
        return snapshot

    def _analyze_module(self, module_path: Path, module_name: str, primary_language: str) -> ModuleAnalysis:
        """Analyze a single module comprehensively"""
        files = []
        dependencies = set()
        exports = set()
        documentation = {}
        consciousness_level = 0.0
        quantum_coherence = 0.0
        
        # Scan all files in module
        for file_path in module_path.rglob('*'):
            if file_path.is_file() and not self._should_ignore_file(file_path):
                file_metadata = self._analyze_file(file_path)
                if file_metadata:
                    files.append(file_metadata)
                    dependencies.update(file_metadata.dependencies)
                    exports.update(file_metadata.exports)
                    
                    # Calculate consciousness metrics
                    consciousness_level += len(file_metadata.consciousness_patterns) * 0.1
                    if 'quantum' in str(file_path).lower():
                        quantum_coherence += 0.2
        
        # Analyze documentation
        doc_files = [f for f in files if f.language == 'Markdown']
        for doc_file in doc_files:
            try:
                with open(doc_file.path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documentation[doc_file.path] = self._extract_documentation_summary(content)
            except Exception as e:
                self.logger.warning(f"Failed to read documentation {doc_file.path}: {e}")
        
        # Normalize metrics
        consciousness_level = min(consciousness_level, 1.0)
        quantum_coherence = min(quantum_coherence, 1.0)
        
        return ModuleAnalysis(
            name=module_name,
            path=str(module_path),
            language=primary_language,
            files=files,
            dependencies=list(dependencies),
            exports=list(exports),
            documentation=documentation,
            consciousness_level=consciousness_level,
            quantum_coherence=quantum_coherence
        )

    def _analyze_file(self, file_path: Path) -> Optional[FileMetadata]:
        """Analyze individual file comprehensively"""
        try:
            # Determine language
            language = self.language_patterns.get(file_path.suffix, 'Unknown')
            if language == 'Unknown':
                return None
            
            # Get file stats
            stat = file_path.stat()
            size = stat.st_size
            last_modified = stat.st_mtime
            
            # Calculate hash
            with open(file_path, 'rb') as f:
                content_hash = hashlib.md5(f.read()).hexdigest()
            
            # Read content for analysis
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Language-specific analysis
            dependencies = []
            exports = []
            classes = []
            functions = []
            interfaces = []
            
            if language == 'Python':
                deps, exps, cls, funcs = self._analyze_python_file(content)
                dependencies.extend(deps)
                exports.extend(exps)
                classes.extend(cls)
                functions.extend(funcs)
            elif language == 'C++':
                deps, exps, cls, funcs, ints = self._analyze_cpp_file(content)
                dependencies.extend(deps)
                exports.extend(exps)
                classes.extend(cls)
                functions.extend(funcs)
                interfaces.extend(ints)
            elif language == 'C#':
                deps, exps, cls, funcs, ints = self._analyze_csharp_file(content)
                dependencies.extend(deps)
                exports.extend(exps)
                classes.extend(cls)
                functions.extend(funcs)
                interfaces.extend(ints)
            
            # Consciousness pattern recognition
            consciousness_patterns = self._detect_consciousness_patterns(content)
            
            return FileMetadata(
                path=str(file_path),
                language=language,
                size=size,
                hash=content_hash,
                last_modified=last_modified,
                dependencies=dependencies,
                exports=exports,
                classes=classes,
                functions=functions,
                interfaces=interfaces,
                consciousness_patterns=consciousness_patterns
            )
            
        except Exception as e:
            self.logger.warning(f"Failed to analyze file {file_path}: {e}")
            return None

    def _analyze_python_file(self, content: str) -> Tuple[List[str], List[str], List[str], List[str]]:
        """Analyze Python file for dependencies and exports"""
        dependencies = []
        exports = []
        classes = []
        functions = []
        
        try:
            # Parse AST
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        dependencies.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        dependencies.append(node.module)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                    exports.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                    if not node.name.startswith('_'):
                        exports.append(node.name)
                        
        except SyntaxError:
            # Fallback to regex analysis
            import_pattern = r'^\s*(?:from\s+(\S+)\s+)?import\s+(.+)$'
            class_pattern = r'^\s*class\s+(\w+)'
            func_pattern = r'^\s*def\s+(\w+)'
            
            for line in content.split('\n'):
                if match := re.match(import_pattern, line):
                    if match.group(1):
                        dependencies.append(match.group(1))
                    deps = [d.strip().split(' as ')[0] for d in match.group(2).split(',')]
                    dependencies.extend(deps)
                elif match := re.match(class_pattern, line):
                    classes.append(match.group(1))
                    exports.append(match.group(1))
                elif match := re.match(func_pattern, line):
                    functions.append(match.group(1))
                    if not match.group(1).startswith('_'):
                        exports.append(match.group(1))
        
        return dependencies, exports, classes, functions

    def _analyze_cpp_file(self, content: str) -> Tuple[List[str], List[str], List[str], List[str], List[str]]:
        """Analyze C++ file for dependencies and exports"""
        dependencies = []
        exports = []
        classes = []
        functions = []
        interfaces = []
        
        # Include patterns
        include_pattern = r'#include\s*[<"](.*?)[>"]'
        for match in re.finditer(include_pattern, content):
            dependencies.append(match.group(1))
        
        # Class patterns
        class_pattern = r'class\s+(\w+)'
        for match in re.finditer(class_pattern, content):
            classes.append(match.group(1))
            exports.append(match.group(1))
        
        # Function patterns
        func_pattern = r'(?:^|\s)(\w+)\s*\([^)]*\)\s*{'
        for match in re.finditer(func_pattern, content, re.MULTILINE):
            if match.group(1) not in ['if', 'while', 'for', 'switch']:
                functions.append(match.group(1))
                exports.append(match.group(1))
        
        # Interface patterns (assuming I prefix)
        interface_pattern = r'class\s+(I\w+)'
        for match in re.finditer(interface_pattern, content):
            interfaces.append(match.group(1))
        
        return dependencies, exports, classes, functions, interfaces

    def _analyze_csharp_file(self, content: str) -> Tuple[List[str], List[str], List[str], List[str], List[str]]:
        """Analyze C# file for dependencies and exports"""
        dependencies = []
        exports = []
        classes = []
        functions = []
        interfaces = []
        
        # Using patterns
        using_pattern = r'using\s+([^;]+);'
        for match in re.finditer(using_pattern, content):
            dependencies.append(match.group(1))
        
        # Class patterns
        class_pattern = r'(?:public\s+)?class\s+(\w+)'
        for match in re.finditer(class_pattern, content):
            classes.append(match.group(1))
            exports.append(match.group(1))
        
        # Method patterns
        method_pattern = r'(?:public\s+|private\s+|protected\s+)?(?:static\s+)?(?:\w+\s+)?(\w+)\s*\([^)]*\)'
        for match in re.finditer(method_pattern, content):
            if match.group(1) not in ['if', 'while', 'for', 'switch', 'using', 'class']:
                functions.append(match.group(1))
                exports.append(match.group(1))
        
        # Interface patterns
        interface_pattern = r'interface\s+(I\w+)'
        for match in re.finditer(interface_pattern, content):
            interfaces.append(match.group(1))
        
        return dependencies, exports, classes, functions, interfaces

    def _detect_consciousness_patterns(self, content: str) -> List[str]:
        """Detect consciousness-related patterns in content"""
        patterns = []
        content_lower = content.lower()
        
        for keyword in self.consciousness_keywords:
            if keyword in content_lower:
                patterns.append(keyword)
        
        # Advanced pattern detection
        if re.search(r'self.*modify|recursive.*self|consciousness.*emerge', content_lower):
            patterns.append('recursive_self_modification')
        
        if re.search(r'quantum.*coherence|holographic.*pattern', content_lower):
            patterns.append('quantum_holographic_processing')
        
        if re.search(r'ai.*orchestrat|multi.*ai.*harmon', content_lower):
            patterns.append('multi_ai_orchestration')
        
        return patterns

    def _analyze_cross_language_dependencies(self, modules: Dict[str, ModuleAnalysis]) -> Dict[str, List[str]]:
        """Analyze dependencies across different programming languages"""
        cross_deps = defaultdict(list)
        
        # Look for IPC patterns, shared libraries, and communication protocols
        for module_name, module in modules.items():
            for file_meta in module.files:
                content_path = Path(file_meta.path)
                try:
                    with open(content_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                    
                    # Look for cross-language communication patterns
                    for pattern in self.ipc_patterns:
                        if re.search(pattern, content):
                            cross_deps[module_name].append(f"ipc_{pattern}")
                    
                    # Language-specific cross-references
                    if file_meta.language == 'Python':
                        if 'ctypes' in content or 'dll' in content:
                            cross_deps[module_name].append('cpp_integration')
                        if 'websocket' in content or 'socket' in content:
                            cross_deps[module_name].append('csharp_communication')
                    
                    elif file_meta.language == 'C++':
                        if 'python' in content or '.py' in content:
                            cross_deps[module_name].append('python_integration')
                    
                    elif file_meta.language == 'C#':
                        if 'websocket' in content or 'tcp' in content:
                            cross_deps[module_name].append('python_communication')
                
                except Exception as e:
                    self.logger.warning(f"Failed to analyze cross-deps for {file_meta.path}: {e}")
        
        return dict(cross_deps)

    def _calculate_documentation_coherence(self, modules: Dict[str, ModuleAnalysis]) -> float:
        """Calculate documentation coherence across the ecosystem"""
        total_code_files = 0
        documented_files = 0
        
        for module in modules.values():
            code_files = [f for f in module.files if f.language in ['Python', 'C++', 'C#']]
            total_code_files += len(code_files)
            
            # Check if module has documentation
            if module.documentation:
                documented_files += len(code_files)
        
        return documented_files / total_code_files if total_code_files > 0 else 0.0

    def _extract_documentation_summary(self, content: str) -> str:
        """Extract summary from documentation content"""
        lines = content.split('\n')
        summary_lines = []
        
        for line in lines[:20]:  # First 20 lines
            line = line.strip()
            if line and not line.startswith('#'):
                summary_lines.append(line)
                if len(summary_lines) >= 3:
                    break
        
        return ' '.join(summary_lines)[:200]

    def _count_lines(self, file_path: str) -> int:
        """Count lines in a file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except Exception:
            return 0

    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored in analysis"""
        ignore_patterns = [
            '__pycache__', '.git', '.vscode', 'node_modules', 'bin', 'obj',
            '.pyc', '.exe', '.dll', '.so', '.a', '.lib', '.pdb'
        ]
        
        file_str = str(file_path).lower()
        return any(pattern in file_str for pattern in ignore_patterns)

    def generate_ecosystem_report(self, snapshot: EcosystemSnapshot) -> str:
        """Generate comprehensive ecosystem report"""
        report = f"""
# 🌌 AIOS Ecosystem Intelligence Report
**Generated:** {snapshot.timestamp}
**Workspace:** {snapshot.workspace_root}

## 📊 Ecosystem Overview
- **Total Modules:** {len(snapshot.modules)}
- **Total Files:** {snapshot.total_files}
- **Total Lines:** {snapshot.total_lines:,}
- **Documentation Coherence:** {snapshot.documentation_coherence:.1%}

## 🔍 Module Analysis
"""
        
        for module_name, module in snapshot.modules.items():
            report += f"""
### {module_name} ({module.language})
- **Files:** {len(module.files)}
- **Dependencies:** {len(module.dependencies)}
- **Exports:** {len(module.exports)}
- **Consciousness Level:** {module.consciousness_level:.1%}
- **Quantum Coherence:** {module.quantum_coherence:.1%}
"""
        
        report += f"""
## 🔗 Cross-Language Dependencies
"""
        for module, deps in snapshot.cross_language_dependencies.items():
            if deps:
                report += f"- **{module}:** {', '.join(deps)}\n"
        
        report += f"""
## 🧠 Consciousness Metrics
"""
        for metric, value in snapshot.consciousness_metrics.items():
            report += f"- **{metric}:** {value:.1%}\n"
        
        return report

    def save_snapshot(self, snapshot: EcosystemSnapshot, filepath: Optional[Path] = None) -> None:
        """Save ecosystem snapshot to file"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.workspace_root / 'core' / 'logs' / f'ecosystem_snapshot_{timestamp}.json'
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert snapshot to JSON-serializable format
        snapshot_dict = asdict(snapshot)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(snapshot_dict, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"💾 Ecosystem snapshot saved to {filepath}")

    def start_continuous_monitoring(self, interval: float = 30.0) -> None:
        """Start continuous ecosystem monitoring"""
        self.running = True
        self.logger.info(f"🔄 Starting continuous ecosystem monitoring (interval: {interval}s)")
        
        def monitor():
            while self.running:
                try:
                    snapshot = self.analyze_complete_ecosystem()
                    self.save_snapshot(snapshot)
                    
                    # Generate report
                    report = self.generate_ecosystem_report(snapshot)
                    report_path = self.workspace_root / 'core' / 'logs' / 'latest_ecosystem_report.md'
                    with open(report_path, 'w', encoding='utf-8') as f:
                        f.write(report)
                    
                    time.sleep(interval)
                except Exception as e:
                    self.logger.error(f"Error in continuous monitoring: {e}")
                    time.sleep(10)  # Wait before retrying
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()

    def stop_continuous_monitoring(self) -> None:
        """Stop continuous ecosystem monitoring"""
        self.running = False
        self.logger.info("🛑 Stopping continuous ecosystem monitoring")

def main():
    """Main execution"""
    print("🌌 AIOS Ecosystem Intelligence & Context Coherence Engine")
    print("=" * 60)
    
    # Initialize ecosystem intelligence
    ecosystem = AIOSEcosystemIntelligence()
    
    try:
        # Perform complete analysis
        print("🔍 Performing complete ecosystem analysis...")
        snapshot = ecosystem.analyze_complete_ecosystem()
        
        # Generate and save report
        print("📊 Generating ecosystem report...")
        report = ecosystem.generate_ecosystem_report(snapshot)
        
        # Save snapshot and report
        ecosystem.save_snapshot(snapshot)
        
        report_path = ecosystem.workspace_root / 'core' / 'COMPLETE_ECOSYSTEM_ANALYSIS.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Analysis complete! Report saved to: {report_path}")
        print("\n" + "=" * 60)
        print("📊 ECOSYSTEM SUMMARY")
        print("=" * 60)
        print(f"Modules: {len(snapshot.modules)}")
        print(f"Files: {snapshot.total_files}")
        print(f"Lines: {snapshot.total_lines:,}")
        print(f"Documentation Coherence: {snapshot.documentation_coherence:.1%}")
        
        # Start continuous monitoring
        choice = input("\n🔄 Start continuous monitoring? (y/n): ").lower()
        if choice == 'y':
            ecosystem.start_continuous_monitoring()
            print("🔄 Continuous monitoring started. Press Ctrl+C to stop.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                ecosystem.stop_continuous_monitoring()
                print("\n✅ Monitoring stopped.")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
