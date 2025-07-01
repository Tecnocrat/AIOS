#!/usr/bin/env python3
"""
🏗️ AIOS Codebase Architect - Deep Analysis & Optimization Engine
=====================================================================

This tool performs comprehensive codebase mapping, analysis, and optimization 
planning for the AIOS consciousness system. It prepares for:

1. Full module relationship mapping
2. Dependency analysis and optimization
3. Code consolidation opportunities
4. Architecture refactoring recommendations
5. OS0.4 transition planning

Features:
- Multi-language support (C++, C#, Python, MD)
- Dependency graph generation with complexity metrics
- Module consolidation analysis
- Architecture quality assessment
- Next-gen UI design planning
- OS0.4 optimization roadmap
"""

import os
import json
import ast
import re
import datetime
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib


@dataclass
class ModuleMetrics:
    """Comprehensive metrics for a single module"""
    file_path: str
    language: str
    lines_of_code: int
    function_count: int
    class_count: int
    imports: List[str]
    exports: List[str]
    complexity_score: float
    dependencies: List[str]
    dependents: List[str]
    consolidation_potential: float
    last_modified: str
    size_bytes: int
    content_hash: str


@dataclass
class ArchitectureInsight:
    """Strategic insights about the codebase architecture"""
    insight_type: str
    severity: str  # "critical", "high", "medium", "low"
    description: str
    affected_modules: List[str]
    optimization_potential: float
    recommended_action: str
    implementation_effort: str  # "low", "medium", "high", "extreme"


class CodebaseArchitect:
    """
    Advanced codebase analysis and architecture optimization engine
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = base_path or os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.modules: Dict[str, ModuleMetrics] = {}
        self.insights: List[ArchitectureInsight] = []
        self.dependency_graph: Dict[str, Set[str]] = {}
        self.consolidation_candidates: List[Tuple[str, str, float]] = []
        
        # Analysis configuration
        self.target_dirs = [
            'orchestrator/src', 'orchestrator/include',
            'visual_interface', 'scripts', 'chatgpt_integration',
            'evolution_lab', 'runtime_intelligence', 'gemini_cli_bridge'
        ]
        
        self.exclude_patterns = [
            r'\.git', r'__pycache__', r'\.vs', r'bin/', r'obj/', r'build/',
            r'node_modules', r'\.vscode', r'venv/', r'\.conda/', r'archive/'
        ]
        
    def analyze_codebase(self) -> Dict:
        """
        Perform comprehensive codebase analysis
        """
        print("🏗️ Starting AIOS Codebase Architecture Analysis...")
        print(f"📁 Base path: {self.base_path}")
        
        # Phase 1: Module Discovery & Metrics
        self._discover_modules()
        
        # Phase 2: Dependency Analysis
        self._analyze_dependencies()
        
        # Phase 3: Architecture Insights
        self._generate_insights()
        
        # Phase 4: Consolidation Analysis
        self._analyze_consolidation_opportunities()
        
        # Phase 5: Next-Gen UI Planning
        self._plan_nextgen_ui()
        
        # Phase 6: OS0.4 Optimization Roadmap
        self._generate_os04_roadmap()
        
        return self._compile_results()
    
    def _discover_modules(self):
        """
        Discover and analyze all modules in the codebase
        """
        print("📊 Phase 1: Module Discovery & Metrics Analysis")
        
        for target_dir in self.target_dirs:
            full_path = os.path.join(self.base_path, target_dir)
            if not os.path.exists(full_path):
                continue
                
            print(f"  🔍 Scanning {target_dir}")
            
            for root, dirs, files in os.walk(full_path):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if not any(re.search(pattern, d) for pattern in self.exclude_patterns)]
                
                for file in files:
                    if self._should_analyze_file(file):
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, self.base_path)
                        
                        try:
                            metrics = self._analyze_file(file_path, relative_path)
                            self.modules[relative_path] = metrics
                        except Exception as e:
                            print(f"    ⚠️ Error analyzing {relative_path}: {e}")
        
        print(f"  ✅ Discovered {len(self.modules)} modules")
    
    def _should_analyze_file(self, filename: str) -> bool:
        """
        Determine if a file should be analyzed
        """
        extensions = {'.py', '.cpp', '.hpp', '.h', '.cs', '.xaml', '.md', '.json', '.xml'}
        return any(filename.endswith(ext) for ext in extensions)
    
    def _analyze_file(self, file_path: str, relative_path: str) -> ModuleMetrics:
        """
        Analyze a single file and extract comprehensive metrics
        """
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Basic metrics
        lines = content.split('\n')
        lines_of_code = len([line for line in lines if line.strip() and not line.strip().startswith('//')])
        
        # Language detection
        language = self._detect_language(file_path)
        
        # Content hash for change detection
        content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()[:16]
        
        # File stats
        stat = os.stat(file_path)
        last_modified = datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
        size_bytes = stat.st_size
        
        # Language-specific analysis
        if language == 'Python':
            functions, classes, imports, exports = self._analyze_python(content)
        elif language in ['C++', 'C']:
            functions, classes, imports, exports = self._analyze_cpp(content)
        elif language == 'C#':
            functions, classes, imports, exports = self._analyze_csharp(content)
        else:
            functions, classes, imports, exports = [], [], [], []
        
        # Complexity calculation
        complexity_score = self._calculate_complexity(content, language, len(functions), len(classes))
        
        return ModuleMetrics(
            file_path=relative_path,
            language=language,
            lines_of_code=lines_of_code,
            function_count=len(functions),
            class_count=len(classes),
            imports=imports,
            exports=exports,
            complexity_score=complexity_score,
            dependencies=[],  # Will be filled in dependency analysis
            dependents=[],
            consolidation_potential=0.0,  # Will be calculated later
            last_modified=last_modified,
            size_bytes=size_bytes,
            content_hash=content_hash
        )
    
    def _detect_language(self, file_path: str) -> str:
        """
        Detect programming language from file extension
        """
        ext = Path(file_path).suffix.lower()
        
        mapping = {
            '.py': 'Python',
            '.cpp': 'C++', '.hpp': 'C++', '.cc': 'C++', '.cxx': 'C++',
            '.h': 'C', '.c': 'C',
            '.cs': 'C#',
            '.xaml': 'XAML',
            '.md': 'Markdown',
            '.json': 'JSON',
            '.xml': 'XML'
        }
        
        return mapping.get(ext, 'Unknown')
    
    def _analyze_python(self, content: str) -> Tuple[List[str], List[str], List[str], List[str]]:
        """
        Analyze Python code for functions, classes, imports, and exports
        """
        try:
            tree = ast.parse(content)
        except:
            return [], [], [], []
        
        functions = []
        classes = []
        imports = []
        exports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        # Look for __all__ to identify exports
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == '__all__':
                        if isinstance(node.value, ast.List):
                            exports = [elt.s for elt in node.value.elts if isinstance(elt, ast.Str)]
        
        return functions, classes, imports, exports
    
    def _analyze_cpp(self, content: str) -> Tuple[List[str], List[str], List[str], List[str]]:
        """
        Analyze C++ code for functions, classes, includes, and exports
        """
        functions = []
        classes = []
        imports = []
        exports = []
        
        # Find includes
        include_pattern = r'#include\s*[<"]([^>"]+)[>"]'
        imports = re.findall(include_pattern, content)
        
        # Find function definitions (simplified)
        func_pattern = r'(?:^|\n)\s*(?:[\w:]+\s+)*(\w+)\s*\([^)]*\)\s*\{'
        functions = re.findall(func_pattern, content, re.MULTILINE)
        
        # Find class definitions
        class_pattern = r'class\s+(\w+)'
        classes = re.findall(class_pattern, content)
        
        return functions, classes, imports, exports
    
    def _analyze_csharp(self, content: str) -> Tuple[List[str], List[str], List[str], List[str]]:
        """
        Analyze C# code for functions, classes, using statements, and exports
        """
        functions = []
        classes = []
        imports = []
        exports = []
        
        # Find using statements
        using_pattern = r'using\s+([\w.]+);'
        imports = re.findall(using_pattern, content)
        
        # Find method definitions (simplified)
        method_pattern = r'(?:public|private|protected|internal)?\s*(?:static)?\s*\w+\s+(\w+)\s*\([^)]*\)'
        functions = re.findall(method_pattern, content)
        
        # Find class definitions
        class_pattern = r'(?:public|private|internal)?\s*(?:partial)?\s*class\s+(\w+)'
        classes = re.findall(class_pattern, content)
        
        return functions, classes, imports, exports
    
    def _calculate_complexity(self, content: str, language: str, func_count: int, class_count: int) -> float:
        """
        Calculate a complexity score for the module
        """
        lines = len(content.split('\n'))
        
        # Base complexity from size
        size_complexity = min(lines / 100.0, 10.0)
        
        # Structural complexity
        structural_complexity = (func_count * 0.5 + class_count * 1.0)
        
        # Conditional complexity (count ifs, fors, whiles, etc.)
        conditional_keywords = ['if', 'for', 'while', 'switch', 'case', 'try', 'catch']
        conditional_count = sum(content.lower().count(keyword) for keyword in conditional_keywords)
        conditional_complexity = conditional_count * 0.1
        
        # Nesting complexity (simplified - count indentation levels)
        max_indent = 0
        for line in content.split('\n'):
            if line.strip():
                indent = len(line) - len(line.lstrip())
                max_indent = max(max_indent, indent)
        nesting_complexity = max_indent / 4.0  # Assuming 4-space indents
        
        total_complexity = size_complexity + structural_complexity + conditional_complexity + nesting_complexity
        return round(total_complexity, 2)
    
    def _analyze_dependencies(self):
        """
        Analyze dependencies between modules
        """
        print("🔗 Phase 2: Dependency Analysis")
        
        # Build dependency graph
        for module_path, module in self.modules.items():
            dependencies = set()
            
            for import_name in module.imports:
                # Find which modules provide this import
                for other_path, other_module in self.modules.items():
                    if other_path != module_path:
                        # Check if this module exports the imported name
                        if (import_name in other_module.exports or 
                            any(import_name in other_path for import_name in [import_name]) or
                            import_name in os.path.basename(other_path)):
                            dependencies.add(other_path)
            
            module.dependencies = list(dependencies)
            self.dependency_graph[module_path] = dependencies
        
        # Calculate dependents (reverse dependencies)
        for module_path in self.modules:
            dependents = []
            for other_path, deps in self.dependency_graph.items():
                if module_path in deps:
                    dependents.append(other_path)
            self.modules[module_path].dependents = dependents
        
        print(f"  ✅ Mapped {sum(len(deps) for deps in self.dependency_graph.values())} dependencies")
    
    def _generate_insights(self):
        """
        Generate architecture insights and recommendations
        """
        print("💡 Phase 3: Architecture Insights Generation")
        
        # Insight 1: High complexity modules
        high_complexity = [m for m in self.modules.values() if m.complexity_score > 20]
        if high_complexity:
            self.insights.append(ArchitectureInsight(
                insight_type="complexity",
                severity="high",
                description=f"Found {len(high_complexity)} modules with high complexity (>20)",
                affected_modules=[m.file_path for m in high_complexity],
                optimization_potential=8.5,
                recommended_action="Refactor complex modules into smaller, focused components",
                implementation_effort="medium"
            ))
        
        # Insight 2: Highly connected modules (dependency hubs)
        hub_threshold = 5
        dependency_hubs = [m for m in self.modules.values() if len(m.dependents) > hub_threshold]
        if dependency_hubs:
            self.insights.append(ArchitectureInsight(
                insight_type="coupling",
                severity="medium",
                description=f"Found {len(dependency_hubs)} dependency hubs (>{hub_threshold} dependents)",
                affected_modules=[m.file_path for m in dependency_hubs],
                optimization_potential=7.0,
                recommended_action="Consider breaking down hub modules to reduce coupling",
                implementation_effort="high"
            ))
        
        # Insight 3: Orphaned modules (no dependencies or dependents)
        orphaned = [m for m in self.modules.values() if not m.dependencies and not m.dependents]
        if orphaned:
            self.insights.append(ArchitectureInsight(
                insight_type="isolation",
                severity="low",
                description=f"Found {len(orphaned)} potentially orphaned modules",
                affected_modules=[m.file_path for m in orphaned],
                optimization_potential=3.0,
                recommended_action="Review orphaned modules for consolidation or removal",
                implementation_effort="low"
            ))
        
        # Insight 4: Language distribution analysis
        lang_dist = {}
        for module in self.modules.values():
            lang_dist[module.language] = lang_dist.get(module.language, 0) + 1
        
        if len(lang_dist) > 3:
            self.insights.append(ArchitectureInsight(
                insight_type="diversity",
                severity="medium",
                description=f"High language diversity: {len(lang_dist)} languages in use",
                affected_modules=list(self.modules.keys()),
                optimization_potential=6.0,
                recommended_action="Consider consolidating functionality to reduce language complexity",
                implementation_effort="extreme"
            ))
        
        print(f"  ✅ Generated {len(self.insights)} architecture insights")
    
    def _analyze_consolidation_opportunities(self):
        """
        Identify opportunities for module consolidation
        """
        print("🔄 Phase 4: Consolidation Analysis")
        
        # Group modules by functionality patterns
        python_modules = [m for m in self.modules.values() if m.language == 'Python']
        
        # Look for modules in the same directory with similar names or functionality
        for i, module1 in enumerate(python_modules):
            for module2 in python_modules[i+1:]:
                similarity_score = self._calculate_consolidation_potential(module1, module2)
                if similarity_score > 0.6:  # 60% similarity threshold
                    self.consolidation_candidates.append((
                        module1.file_path, module2.file_path, similarity_score
                    ))
        
        print(f"  ✅ Found {len(self.consolidation_candidates)} consolidation opportunities")
    
    def _calculate_consolidation_potential(self, module1: ModuleMetrics, module2: ModuleMetrics) -> float:
        """
        Calculate potential for consolidating two modules
        """
        score = 0.0
        
        # Same directory bonus
        if os.path.dirname(module1.file_path) == os.path.dirname(module2.file_path):
            score += 0.3
        
        # Similar size bonus
        if abs(module1.lines_of_code - module2.lines_of_code) < 100:
            score += 0.2
        
        # Similar imports bonus
        common_imports = set(module1.imports) & set(module2.imports)
        if common_imports:
            score += min(len(common_imports) / max(len(module1.imports), len(module2.imports)), 0.3)
        
        # Similar complexity bonus
        if abs(module1.complexity_score - module2.complexity_score) < 5:
            score += 0.2
        
        return score
    
    def _plan_nextgen_ui(self):
        """
        Plan next-generation UI architecture
        """
        print("🎨 Phase 5: Next-Gen UI Planning")
        
        # Analyze current UI modules
        ui_modules = [m for m in self.modules.values() if 'visual' in m.file_path.lower() or m.language in ['C#', 'XAML']]
        
        ui_plan = {
            "current_ui_modules": len(ui_modules),
            "complexity_score": sum(m.complexity_score for m in ui_modules),
            "recommendations": [
                "Implement real-time consciousness visualization",
                "Add 3D mutation process display",
                "Create architect-level transparency interface",
                "Integrate live dependency graph visualization",
                "Add evolutionary process monitoring",
                "Implement quantum state visualization"
            ],
            "technology_stack": {
                "primary": "C# WPF/WinUI 3",
                "visualization": "Custom OpenGL/DirectX rendering",
                "real_time": "SignalR for live updates",
                "3d_engine": "Unity integration or custom 3D engine",
                "data_binding": "MVVM with reactive extensions"
            }
        }
        
        self.nextgen_ui_plan = ui_plan
        
        # Add UI insights
        self.insights.append(ArchitectureInsight(
            insight_type="ui_modernization",
            severity="high",
            description="Current UI lacks real-time consciousness visualization capabilities",
            affected_modules=[m.file_path for m in ui_modules],
            optimization_potential=9.5,
            recommended_action="Implement next-gen architect-level UI with real-time transparency",
            implementation_effort="high"
        ))
    
    def _generate_os04_roadmap(self):
        """
        Generate OS0.4 optimization roadmap
        """
        print("🚀 Phase 6: OS0.4 Optimization Roadmap")
        
        # Calculate consolidation impact
        total_modules = len(self.modules)
        consolidatable = len(self.consolidation_candidates)
        
        # Estimate file reduction potential
        estimated_reduction = int(total_modules * 0.3)  # 30% reduction target
        
        self.os04_roadmap = {
            "current_state": {
                "total_modules": total_modules,
                "total_lines": sum(m.lines_of_code for m in self.modules.values()),
                "average_complexity": sum(m.complexity_score for m in self.modules.values()) / total_modules,
                "languages": list(set(m.language for m in self.modules.values()))
            },
            "optimization_targets": {
                "file_reduction": f"{estimated_reduction} modules ({estimated_reduction/total_modules*100:.1f}%)",
                "complexity_reduction": "25% average complexity reduction",
                "dependency_optimization": "50% reduction in circular dependencies",
                "consolidation_opportunities": consolidatable
            },
            "phases": [
                {
                    "phase": "1. Dependency Cleanup",
                    "duration": "1-2 weeks",
                    "actions": [
                        "Resolve circular dependencies",
                        "Eliminate unused imports",
                        "Optimize module interfaces"
                    ]
                },
                {
                    "phase": "2. Module Consolidation",
                    "duration": "2-3 weeks", 
                    "actions": [
                        "Merge similar functionality modules",
                        "Refactor high-complexity modules",
                        "Standardize naming conventions"
                    ]
                },
                {
                    "phase": "3. Architecture Refactoring",
                    "duration": "3-4 weeks",
                    "actions": [
                        "Implement clean architecture patterns",
                        "Add comprehensive interfaces",
                        "Optimize performance bottlenecks"
                    ]
                },
                {
                    "phase": "4. Next-Gen UI Implementation",
                    "duration": "4-6 weeks",
                    "actions": [
                        "Design real-time visualization system",
                        "Implement 3D consciousness display",
                        "Add architect-level transparency"
                    ]
                },
                {
                    "phase": "5. OS0.4 Finalization",
                    "duration": "1-2 weeks",
                    "actions": [
                        "Final testing and validation",
                        "Documentation updates",
                        "Deployment preparation"
                    ]
                }
            ]
        }
    
    def _compile_results(self) -> Dict:
        """
        Compile all analysis results into a comprehensive report
        """
        print("📋 Compiling Comprehensive Analysis Report...")
        
        # Calculate summary statistics
        total_loc = sum(m.lines_of_code for m in self.modules.values())
        avg_complexity = sum(m.complexity_score for m in self.modules.values()) / len(self.modules)
        
        language_stats = {}
        for module in self.modules.values():
            if module.language not in language_stats:
                language_stats[module.language] = {"count": 0, "loc": 0, "complexity": 0}
            language_stats[module.language]["count"] += 1
            language_stats[module.language]["loc"] += module.lines_of_code
            language_stats[module.language]["complexity"] += module.complexity_score
        
        # Calculate average complexity per language
        for lang_stat in language_stats.values():
            lang_stat["avg_complexity"] = lang_stat["complexity"] / lang_stat["count"]
        
        results = {
            "analysis_timestamp": datetime.datetime.now().isoformat(),
            "summary": {
                "total_modules": len(self.modules),
                "total_lines_of_code": total_loc,
                "average_complexity": round(avg_complexity, 2),
                "languages_used": len(language_stats),
                "total_dependencies": sum(len(deps) for deps in self.dependency_graph.values()),
                "consolidation_opportunities": len(self.consolidation_candidates)
            },
            "language_distribution": language_stats,
            "modules": {path: asdict(module) for path, module in self.modules.items()},
            "dependency_graph": {k: list(v) for k, v in self.dependency_graph.items()},
            "architecture_insights": [asdict(insight) for insight in self.insights],
            "consolidation_candidates": [
                {"module1": c[0], "module2": c[1], "similarity_score": c[2]} 
                for c in self.consolidation_candidates
            ],
            "nextgen_ui_plan": getattr(self, 'nextgen_ui_plan', {}),
            "os04_roadmap": getattr(self, 'os04_roadmap', {})
        }
        
        return results
    
    def save_results(self, results: Dict, output_path: str = None):
        """
        Save analysis results to JSON file
        """
        if output_path is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.base_path, f"CODEBASE_ARCHITECTURE_ANALYSIS_{timestamp}.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Analysis results saved to: {output_path}")
        return output_path
    
    def generate_report(self, results: Dict) -> str:
        """
        Generate a human-readable markdown report
        """
        report_lines = [
            "# 🏗️ AIOS Codebase Architecture Analysis Report",
            f"Generated: {results['analysis_timestamp']}",
            "",
            "## 📊 Executive Summary",
            "",
            f"- **Total Modules**: {results['summary']['total_modules']}",
            f"- **Total Lines of Code**: {results['summary']['total_lines_of_code']:,}",
            f"- **Average Complexity**: {results['summary']['average_complexity']}/100",
            f"- **Languages Used**: {results['summary']['languages_used']}",
            f"- **Total Dependencies**: {results['summary']['total_dependencies']}",
            f"- **Consolidation Opportunities**: {results['summary']['consolidation_opportunities']}",
            "",
            "## 🎯 Language Distribution",
            ""
        ]
        
        for lang, stats in results['language_distribution'].items():
            report_lines.extend([
                f"### {lang}",
                f"- Modules: {stats['count']}",
                f"- Lines of Code: {stats['loc']:,}",
                f"- Average Complexity: {stats['avg_complexity']:.2f}",
                ""
            ])
        
        report_lines.extend([
            "## 🔍 Architecture Insights",
            ""
        ])
        
        for insight in results['architecture_insights']:
            severity_emoji = {
                "critical": "🚨", "high": "⚠️", "medium": "📝", "low": "💡"
            }.get(insight['severity'], "📝")
            
            report_lines.extend([
                f"### {severity_emoji} {insight['insight_type'].title()} ({insight['severity'].upper()})",
                f"**Description**: {insight['description']}",
                f"**Optimization Potential**: {insight['optimization_potential']}/10",
                f"**Recommended Action**: {insight['recommended_action']}",
                f"**Implementation Effort**: {insight['implementation_effort']}",
                f"**Affected Modules**: {len(insight['affected_modules'])}",
                ""
            ])
        
        if 'os04_roadmap' in results and results['os04_roadmap']:
            report_lines.extend([
                "## 🚀 OS0.4 Optimization Roadmap",
                "",
                "### Current State",
                f"- Total Modules: {results['os04_roadmap']['current_state']['total_modules']}",
                f"- Total Lines: {results['os04_roadmap']['current_state']['total_lines']:,}",
                f"- Average Complexity: {results['os04_roadmap']['current_state']['average_complexity']:.2f}",
                "",
                "### Optimization Targets",
            ])
            
            for target, value in results['os04_roadmap']['optimization_targets'].items():
                report_lines.append(f"- **{target.replace('_', ' ').title()}**: {value}")
            
            report_lines.extend(["", "### Implementation Phases", ""])
            
            for phase in results['os04_roadmap']['phases']:
                report_lines.extend([
                    f"#### {phase['phase']} ({phase['duration']})",
                    ""
                ])
                for action in phase['actions']:
                    report_lines.append(f"- {action}")
                report_lines.append("")
        
        return "\n".join(report_lines)


def main():
    """
    Main execution function
    """
    print("🏗️ AIOS Codebase Architect - Starting Deep Analysis")
    print("=" * 60)
    
    architect = CodebaseArchitect()
    results = architect.analyze_codebase()
    
    # Save detailed JSON results
    json_path = architect.save_results(results)
    
    # Generate and save markdown report
    report_content = architect.generate_report(results)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(architect.base_path, f"CODEBASE_ARCHITECTURE_REPORT_{timestamp}.md")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"📋 Architecture report saved to: {report_path}")
    
    # Print summary to console
    print("\n" + "=" * 60)
    print("🎯 ANALYSIS COMPLETE - KEY FINDINGS:")
    print("=" * 60)
    print(f"📊 {results['summary']['total_modules']} modules analyzed")
    print(f"📝 {results['summary']['total_lines_of_code']:,} lines of code")
    print(f"🔗 {results['summary']['total_dependencies']} dependencies mapped")
    print(f"💡 {len(results['architecture_insights'])} insights generated")
    print(f"🔄 {results['summary']['consolidation_opportunities']} consolidation opportunities")
    print(f"🎨 Next-gen UI plan ready")
    print(f"🚀 OS0.4 roadmap generated")
    
    print("\n🎯 Top Optimization Opportunities:")
    for insight in sorted(results['architecture_insights'], 
                         key=lambda x: x['optimization_potential'], reverse=True)[:3]:
        print(f"  • {insight['description']} (Potential: {insight['optimization_potential']}/10)")
    
    return json_path, report_path


if __name__ == "__main__":
    main()
