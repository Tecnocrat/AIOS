#!/usr/bin/env python3
"""
 AIOS CONTEXT ASSEMBLER

Environmental Awareness and Context Analysis for Coherent Development

PURPOSE:
- Analyze existing environment before creating new files
- Achieve memory context about files sharing workspace
- Prevent architectural debt and scattered logic
- Ensure coherence with existing codebase

PHILOSOPHY:
"AI engines should pre-analyze the folder they are going to be working on
and achieve memory context about the files they share space with."

CAPABILITIES:
1. Environmental Context Analysis
2. Existing File Memory Mapping
3. Architectural Coherence Assessment
4. Pre-Creation Impact Analysis
5. Integration Opportunity Detection


"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import ast
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class FileContext:
    """Context information about an existing file."""
    path: Path
    name: str
    size: int
    modified_time: datetime
    file_type: str
    imports: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    purpose: str = ""
    complexity_score: float = 0.0


@dataclass
class EnvironmentContext:
    """Complete context of a development environment."""
    root_path: Path
    total_files: int
    file_contexts: List[FileContext] = field(default_factory=list)
    architectural_patterns: List[str] = field(default_factory=list)
    integration_opportunities: List[str] = field(default_factory=list)
    scattered_logic_areas: List[str] = field(default_factory=list)
    coherence_score: float = 0.0


class ContextAssembler:
    """
    Environmental awareness engine for coherent development.
    
    Analyzes existing environment to achieve memory context before
    creating new files, preventing architectural fragmentation.
    """
    
    def __init__(self, root_path: str = None):
        """Initialize context assembler."""
        
        logger.info(" Initializing Context Assembler...")
        
        self.root_path = Path(root_path) if root_path else Path.cwd()
        self.environment_context: Optional[EnvironmentContext] = None
        
        # Analysis configuration
        extensions = {'.py', '.cs', '.cpp', '.h', '.js', '.ts', '.md'}
        self.supported_extensions = extensions
        patterns = {'__pycache__', '.git', 'node_modules', 'bin', 'obj'}
        self.ignore_patterns = patterns
        
        # Memory context cache
        self.context_cache: Dict[str, FileContext] = {}
        self.analysis_timestamp = None
        
        logger.info(f" Context Assembler ready for: {self.root_path}")
        logger.info(f" Supported file types: {self.supported_extensions}")
    
    def analyze_environment(
        self, force_refresh: bool = False
    ) -> EnvironmentContext:
        """
        Perform comprehensive environmental context analysis.
        
        This is the core method that should be called before any new
        file creation to achieve memory context about existing environment.
        """
        
        logger.info(" Analyzing environment for context awareness...")
        
        if not force_refresh and self.environment_context:
            logger.info(" Using cached environment context")
            return self.environment_context
        
        start_time = datetime.now()
        
        # Discover all relevant files
        file_paths = self._discover_files()
        logger.info(f" Discovered {len(file_paths)} relevant files")
        
        # Analyze each file for context
        file_contexts = []
        for file_path in file_paths:
            try:
                context = self._analyze_file(file_path)
                if context:
                    file_contexts.append(context)
                    self.context_cache[str(file_path)] = context
            except Exception as e:
                logger.warning(f" Failed to analyze {file_path}: {e}")
        
        # Analyze architectural patterns
        patterns = self._detect_architectural_patterns(file_contexts)
        
        # Detect integration opportunities
        opportunities = self._detect_integration_opportunities(file_contexts)
        
        # Identify scattered logic areas
        scattered_areas = self._identify_scattered_logic(file_contexts)
        
        # Calculate coherence score
        coherence_score = self._calculate_coherence_score(
            file_contexts, patterns
        )
        
        # Create environment context
        self.environment_context = EnvironmentContext(
            root_path=self.root_path,
            total_files=len(file_contexts),
            file_contexts=file_contexts,
            architectural_patterns=patterns,
            integration_opportunities=opportunities,
            scattered_logic_areas=scattered_areas,
            coherence_score=coherence_score
        )
        
        analysis_time = (datetime.now() - start_time).total_seconds()
        self.analysis_timestamp = datetime.now()
        
        logger.info(f" Environment analysis complete in {analysis_time:.2f}s")
        logger.info(f" Coherence score: {coherence_score:.2f}/10.0")
        logger.info(f" Integration opportunities: {len(opportunities)}")
        logger.info(f" Scattered logic areas: {len(scattered_areas)}")
        
        return self.environment_context
    
    def _discover_files(self) -> List[Path]:
        """Discover all relevant files in the environment."""
        
        files = []
        
        for root, dirs, filenames in os.walk(self.root_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_patterns]
            
            for filename in filenames:
                file_path = Path(root) / filename
                
                # Check if file extension is supported
                if file_path.suffix in self.supported_extensions:
                    files.append(file_path)
        
        return sorted(files)
    
    def _analyze_file(self, file_path: Path) -> Optional[FileContext]:
        """Analyze individual file for context information."""
        
        try:
            # Basic file information
            stat = file_path.stat()
            context = FileContext(
                path=file_path,
                name=file_path.name,
                size=stat.st_size,
                modified_time=datetime.fromtimestamp(stat.st_mtime),
                file_type=file_path.suffix
            )
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Python-specific analysis
            if file_path.suffix == '.py':
                self._analyze_python_file(content, context)
            
            # Extract purpose from docstring or comments
            context.purpose = self._extract_purpose(content, file_path.suffix)
            
            # Calculate complexity score
            context.complexity_score = self._calculate_file_complexity(content)
            
            return context
            
        except Exception as e:
            logger.warning(f" Error analyzing {file_path}: {e}")
            return None
    
    def _analyze_python_file(self, content: str, context: FileContext):
        """Analyze Python file for imports, classes, functions."""
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        context.imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        context.imports.append(node.module)
                elif isinstance(node, ast.ClassDef):
                    context.classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    context.functions.append(node.name)
        
        except SyntaxError:
            # File might have syntax errors, skip AST analysis
            pass
    
    def _extract_purpose(self, content: str, file_type: str) -> str:
        """Extract purpose from file content."""
        
        lines = content.split('\n')
        
        # Look for docstring or comment patterns
        purpose_patterns = [
            r'"""([^"]+)"""',  # Python docstring
            r"'''([^']+)'''",  # Python docstring
            r'# PURPOSE:?\s*(.+)',  # Purpose comment
            r'// PURPOSE:?\s*(.+)',  # C++ purpose comment
        ]
        
        for pattern in purpose_patterns:
            for line in lines[:20]:  # Check first 20 lines
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    return match.group(1).strip()[:200]  # Limit length
        
        return ""
    
    def _calculate_file_complexity(self, content: str) -> float:
        """Calculate rough complexity score for file."""
        
        lines = len(content.split('\n'))
        characters = len(content)
        
        # Simple complexity heuristic
        complexity = min(10.0, (lines * 0.01) + (characters * 0.0001))
        return round(complexity, 2)
    
    def _detect_architectural_patterns(self, file_contexts: List[FileContext]) -> List[str]:
        """Detect architectural patterns in the codebase."""
        
        patterns = []
        
        # Pattern detection based on file names and structure
        file_names = [fc.name for fc in file_contexts]
        
        # Engine pattern
        if any('engine' in name.lower() for name in file_names):
            patterns.append("Engine Architecture Pattern")
        
        # Assembly pattern
        if any('assembly' in name.lower() for name in file_names):
            patterns.append("Assembly Language Integration Pattern")
        
        # AIOS pattern
        if any(name.startswith('aios_') for name in file_names):
            patterns.append("AIOS Modular Component Pattern")
        
        # Consciousness pattern
        consciousness_keywords = ['consciousness', 'dendritic', 'quantum', 'tachyonic']
        if any(any(keyword in name.lower() for keyword in consciousness_keywords) 
               for name in file_names):
            patterns.append("Consciousness-Enhanced Processing Pattern")
        
        return patterns
    
    def _detect_integration_opportunities(self, file_contexts: List[FileContext]) -> List[str]:
        """Detect opportunities for integrating scattered logic."""
        
        opportunities = []
        
        # Group files by similar functionality
        engine_files = [fc for fc in file_contexts if 'engine' in fc.name.lower()]
        aios_files = [fc for fc in file_contexts if fc.name.startswith('aios_')]
        
        if len(engine_files) > 1:
            opportunities.append(f"Consolidate {len(engine_files)} engine-related files")
        
        if len(aios_files) > 3:
            opportunities.append(f"Organize {len(aios_files)} AIOS component files into modules")
        
        # Detect duplicate imports
        all_imports = []
        for fc in file_contexts:
            all_imports.extend(fc.imports)
        
        common_imports = [imp for imp in set(all_imports) if all_imports.count(imp) > 3]
        if common_imports:
            opportunities.append(f"Create shared import module for {len(common_imports)} common imports")
        
        return opportunities
    
    def _identify_scattered_logic(self, file_contexts: List[FileContext]) -> List[str]:
        """Identify areas where logic is scattered across multiple files."""
        
        scattered_areas = []
        
        # Check for scattered root files
        root_files = [fc for fc in file_contexts if fc.path.parent == self.root_path]
        if len(root_files) > 5:
            scattered_areas.append(f"Too many files in root: {len(root_files)} files need organization")
        
        # Check for similar function names across files
        all_functions = {}
        for fc in file_contexts:
            for func in fc.functions:
                if func in all_functions:
                    all_functions[func].append(fc.name)
                else:
                    all_functions[func] = [fc.name]
        
        duplicate_functions = {func: files for func, files in all_functions.items() 
                             if len(files) > 1}
        if duplicate_functions:
            scattered_areas.append(f"Duplicate functions across files: {len(duplicate_functions)} cases")
        
        return scattered_areas
    
    def _calculate_coherence_score(self, file_contexts: List[FileContext], patterns: List[str]) -> float:
        """Calculate overall architectural coherence score."""
        
        if not file_contexts:
            return 0.0
        
        # Factors that increase coherence
        pattern_score = min(3.0, len(patterns) * 0.5)  # Architectural patterns
        
        # Organization score (prefer files in subdirectories vs root)
        root_files = len([fc for fc in file_contexts if fc.path.parent == self.root_path])
        organization_score = max(0, 3.0 - (root_files * 0.2))
        
        # Purpose clarity score
        documented_files = len([fc for fc in file_contexts if fc.purpose])
        documentation_score = (documented_files / len(file_contexts)) * 2.0
        
        # File size consistency score
        avg_size = sum(fc.size for fc in file_contexts) / len(file_contexts)
        size_variance = sum(abs(fc.size - avg_size) for fc in file_contexts) / len(file_contexts)
        consistency_score = max(0, 2.0 - (size_variance / avg_size))
        
        total_score = pattern_score + organization_score + documentation_score + consistency_score
        return round(min(10.0, total_score), 2)
    
    def get_creation_recommendations(self, proposed_file_name: str, purpose: str) -> Dict[str, Any]:
        """
        Get recommendations for creating a new file in this environment.
        
        This should be called before creating any new file to ensure coherence.
        """
        
        if not self.environment_context:
            self.analyze_environment()
        
        logger.info(f" Analyzing creation of '{proposed_file_name}' for purpose: {purpose}")
        
        recommendations = {
            'should_create': True,
            'recommended_location': self.root_path,
            'integration_suggestions': [],
            'coherence_warnings': [],
            'similar_files': [],
            'architecture_impact': 'low'
        }
        
        # Check for similar existing files
        similar_files = []
        for fc in self.environment_context.file_contexts:
            if any(keyword in fc.name.lower() and keyword in proposed_file_name.lower() 
                   for keyword in ['engine', 'assembler', 'quantum', 'aios']):
                similar_files.append(fc.name)
        
        recommendations['similar_files'] = similar_files
        
        # Suggest integration if many similar files exist
        if len(similar_files) > 2:
            recommendations['integration_suggestions'].append(
                f"Consider integrating with existing similar files: {', '.join(similar_files)}"
            )
            recommendations['architecture_impact'] = 'medium'
        
        # Warn about root directory clutter
        root_files = [fc for fc in self.environment_context.file_contexts 
                     if fc.path.parent == self.root_path]
        if len(root_files) > 8:
            recommendations['coherence_warnings'].append(
                f"Root directory has {len(root_files)} files - consider organizing into subdirectories"
            )
            recommendations['recommended_location'] = self.root_path / 'organized_modules'
        
        # Architecture impact assessment
        if 'aios_' in proposed_file_name and len([fc for fc in self.environment_context.file_contexts 
                                                 if fc.name.startswith('aios_')]) > 5:
            recommendations['architecture_impact'] = 'high'
            recommendations['integration_suggestions'].append(
                "Consider creating an AIOS components module to organize related functionality"
            )
        
        return recommendations
    
    def generate_context_report(self) -> str:
        """Generate comprehensive context analysis report."""
        
        if not self.environment_context:
            self.analyze_environment()
        
        ctx = self.environment_context
        
        report = []
        report.append(" ENVIRONMENTAL CONTEXT ANALYSIS REPORT")
        report.append("" * 80)
        report.append(f"Analysis Time: {self.analysis_timestamp}")
        report.append(f"Root Path: {ctx.root_path}")
        report.append(f"Total Files Analyzed: {ctx.total_files}")
        report.append(f"Coherence Score: {ctx.coherence_score}/10.0")
        report.append("")
        
        report.append(" ARCHITECTURAL PATTERNS DETECTED:")
        for pattern in ctx.architectural_patterns:
            report.append(f"   {pattern}")
        if not ctx.architectural_patterns:
            report.append("   No clear architectural patterns detected")
        report.append("")
        
        report.append(" INTEGRATION OPPORTUNITIES:")
        for opportunity in ctx.integration_opportunities:
            report.append(f"   {opportunity}")
        if not ctx.integration_opportunities:
            report.append("   No immediate integration opportunities")
        report.append("")
        
        report.append(" SCATTERED LOGIC AREAS:")
        for area in ctx.scattered_logic_areas:
            report.append(f"   {area}")
        if not ctx.scattered_logic_areas:
            report.append("   No scattered logic detected")
        report.append("")
        
        report.append(" FILE BREAKDOWN BY TYPE:")
        file_types = {}
        for fc in ctx.file_contexts:
            file_types[fc.file_type] = file_types.get(fc.file_type, 0) + 1
        
        for file_type, count in sorted(file_types.items()):
            report.append(f"  {file_type}: {count} files")
        report.append("")
        
        report.append(" COHERENCE RECOMMENDATIONS:")
        if ctx.coherence_score < 5.0:
            report.append("   Low coherence - consider architectural refactoring")
        elif ctx.coherence_score < 7.0:
            report.append("   Moderate coherence - some organization improvements needed")
        else:
            report.append("   Good coherence - maintain current architectural standards")
        
        return "\n".join(report)


def demo_context_analysis():
    """Demonstrate context assembler capabilities."""
    
    print(" CONTEXT ASSEMBLER DEMONSTRATION")
    print("=" * 70)
    
    # Initialize context assembler for core directory
    core_path = Path(__file__).parent.parent
    assembler = ContextAssembler(str(core_path))
    
    # Analyze environment
    print("\n Analyzing Core Engine environment...")
    environment = assembler.analyze_environment()
    
    # Generate and display report
    print("\n Generating context analysis report...")
    report = assembler.generate_context_report()
    print(report)
    
    # Test creation recommendations
    print("\n Testing creation recommendations...")
    recommendations = assembler.get_creation_recommendations(
        "aios_new_feature.py", 
        "Test new feature development"
    )
    
    print("\n CREATION RECOMMENDATIONS:")
    print(f"  Should Create: {recommendations['should_create']}")
    print(f"  Architecture Impact: {recommendations['architecture_impact']}")
    
    if recommendations['similar_files']:
        print(f"  Similar Files: {', '.join(recommendations['similar_files'])}")
    
    for suggestion in recommendations['integration_suggestions']:
        print(f"   {suggestion}")
    
    for warning in recommendations['coherence_warnings']:
        print(f"   {warning}")
    
    return assembler


def main():
    """Main function for context assembler demonstration."""
    
    print(" AIOS CONTEXT ASSEMBLER")
    print("=" * 80)
    print("Environmental Awareness for Coherent Development")
    print("=" * 80)
    
    # Run demonstration
    assembler = demo_context_analysis()
    
    print("\n CONTEXT ANALYSIS COMPLETE")
    print(" Environmental awareness achieved!")
    print(" Ready for coherent development guidance!")
    
    return assembler


if __name__ == "__main__":
    main()
