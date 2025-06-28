"""
AI Integration Bridge: Python-C++ Bridge for AI Code Analysis and Evolution

This module provides the Python interface to the AIOS AI evolution system,
enabling natural language interaction with the C++ code evolution engine.

HSE Philosophy: This bridge represents the "translation layer" where human
natural language intentions are converted into quantum-coherent code mutations.
"""

import json
import os
import subprocess
import logging
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import ast
import importlib.util
import hashlib

@dataclass
class CodeAnalysisRequest:
    file_path: str
    language: str
    analysis_type: str  # "structure", "complexity", "dependencies", "mutations"
    parameters: Dict[str, Any]

@dataclass
class CodeAnalysisResult:
    request_id: str
    file_path: str
    language: str
    analysis_type: str
    results: Dict[str, Any]
    confidence: float
    timestamp: datetime
    recommendations: List[str]

@dataclass
class MutationRequest:
    source_code: str
    language: str
    mutation_type: str  # "optimize", "refactor", "enhance", "modernize"
    fitness_criteria: Dict[str, float]
    quantum_guided: bool = True

@dataclass
class MutationResult:
    original_hash: str
    mutated_code: str
    mutation_type: str
    fitness_improvement: float
    quantum_coherence_factor: float
    success: bool
    error_message: Optional[str] = None

class AICodeAnalyzer:
    """Intelligent code analysis using multiple AI techniques."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_languages = ["Python", "C++", "C#", "JavaScript"]
        self.analysis_cache = {}
        
    def analyze_python_code(self, file_path: str) -> Dict[str, Any]:
        """Deep analysis of Python code structure and patterns."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                source_code = file.read()
            
            # Parse AST
            tree = ast.parse(source_code)
            
            analysis = {
                "functions": [],
                "classes": [],
                "imports": [],
                "complexity_score": 0,
                "maintainability_index": 0,
                "potential_issues": [],
                "optimization_opportunities": []
            }
            
            # Extract functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_analysis = {
                        "name": node.name,
                        "line_number": node.lineno,
                        "parameters": [arg.arg for arg in node.args.args],
                        "complexity": self._calculate_cyclomatic_complexity(node),
                        "docstring": ast.get_docstring(node)
                    }
                    analysis["functions"].append(func_analysis)
                
                elif isinstance(node, ast.ClassDef):
                    class_analysis = {
                        "name": node.name,
                        "line_number": node.lineno,
                        "methods": [],
                        "inheritance": [base.id for base in node.bases if hasattr(base, 'id')],
                        "docstring": ast.get_docstring(node)
                    }
                    
                    # Extract methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            class_analysis["methods"].append(item.name)
                    
                    analysis["classes"].append(class_analysis)
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis["imports"].append(alias.name)
                    else:
                        module = node.module or ""
                        for alias in node.names:
                            analysis["imports"].append(f"{module}.{alias.name}")
            
            # Calculate overall complexity
            analysis["complexity_score"] = self._calculate_overall_complexity(tree)
            analysis["maintainability_index"] = self._calculate_maintainability_index(source_code, analysis)
            
            # Identify potential issues
            analysis["potential_issues"] = self._identify_python_issues(tree, source_code)
            
            # Find optimization opportunities
            analysis["optimization_opportunities"] = self._find_python_optimizations(tree, source_code)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Failed to analyze Python code {file_path}: {e}")
            return {"error": str(e)}
    
    def analyze_cpp_code(self, file_path: str) -> Dict[str, Any]:
        """Analysis of C++ code using pattern matching and heuristics."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                source_code = file.read()
            
            analysis = {
                "includes": [],
                "namespaces": [],
                "classes": [],
                "functions": [],
                "templates": [],
                "complexity_score": 0,
                "memory_safety_score": 0,
                "modernization_opportunities": []
            }
            
            lines = source_code.split('\n')
            
            # Extract includes
            for line in lines:
                line = line.strip()
                if line.startswith('#include'):
                    include_match = line.split()
                    if len(include_match) > 1:
                        analysis["includes"].append(include_match[1].strip('<>"'))
            
            # Pattern matching for classes, functions, etc.
            import re
            
            # Find classes
            class_pattern = r'class\s+(\w+)'
            classes = re.findall(class_pattern, source_code)
            analysis["classes"] = classes
            
            # Find functions
            function_pattern = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{'
            functions = re.findall(function_pattern, source_code)
            analysis["functions"] = [{"return_type": f[0], "name": f[1]} for f in functions]
            
            # Find namespaces
            namespace_pattern = r'namespace\s+(\w+)'
            namespaces = re.findall(namespace_pattern, source_code)
            analysis["namespaces"] = namespaces
            
            # Find templates
            template_pattern = r'template\s*<[^>]*>'
            templates = re.findall(template_pattern, source_code)
            analysis["templates"] = templates
            
            # Calculate complexity and safety scores
            analysis["complexity_score"] = self._calculate_cpp_complexity(source_code)
            analysis["memory_safety_score"] = self._calculate_memory_safety(source_code)
            
            # Find modernization opportunities
            analysis["modernization_opportunities"] = self._find_cpp_modernizations(source_code)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Failed to analyze C++ code {file_path}: {e}")
            return {"error": str(e)}
    
    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity for a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.With, ast.Try)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _calculate_overall_complexity(self, tree: ast.AST) -> float:
        """Calculate overall code complexity."""
        total_complexity = 0
        function_count = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                total_complexity += self._calculate_cyclomatic_complexity(node)
                function_count += 1
        
        return total_complexity / max(function_count, 1)
    
    def _calculate_maintainability_index(self, source_code: str, analysis: Dict) -> float:
        """Calculate maintainability index (0-100)."""
        lines_of_code = len(source_code.split('\n'))
        avg_complexity = analysis.get("complexity_score", 1)
        
        # Simplified maintainability index
        mi = max(0, 171 - 5.2 * avg_complexity - 0.23 * lines_of_code)
        return min(100, mi)
    
    def _identify_python_issues(self, tree: ast.AST, source_code: str) -> List[str]:
        """Identify potential issues in Python code."""
        issues = []
        
        # Check for common anti-patterns
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for too many parameters
                if len(node.args.args) > 5:
                    issues.append(f"Function '{node.name}' has too many parameters ({len(node.args.args)})")
                
                # Check for missing docstrings
                if not ast.get_docstring(node):
                    issues.append(f"Function '{node.name}' missing docstring")
        
        # Check for overly long lines
        lines = source_code.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append(f"Line {i} exceeds 120 characters ({len(line)})")
        
        return issues
    
    def _find_python_optimizations(self, tree: ast.AST, source_code: str) -> List[str]:
        """Find optimization opportunities in Python code."""
        optimizations = []
        
        for node in ast.walk(tree):
            # Check for list comprehension opportunities
            if isinstance(node, ast.For):
                optimizations.append("Consider using list comprehension for better performance")
            
            # Check for string concatenation in loops
            if isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Add):
                optimizations.append("Consider using join() for string concatenation")
        
        return optimizations
    
    def _calculate_cpp_complexity(self, source_code: str) -> float:
        """Calculate C++ code complexity."""
        import re
        
        # Count control structures
        control_patterns = [
            r'\bif\b', r'\bwhile\b', r'\bfor\b', r'\bswitch\b',
            r'\bcatch\b', r'\btry\b'
        ]
        
        total_complexity = 1  # Base complexity
        for pattern in control_patterns:
            matches = re.findall(pattern, source_code)
            total_complexity += len(matches)
        
        # Normalize by lines of code
        lines_of_code = len(source_code.split('\n'))
        return total_complexity / max(lines_of_code / 10, 1)
    
    def _calculate_memory_safety(self, source_code: str) -> float:
        """Calculate memory safety score for C++ code."""
        import re
        
        safety_score = 100.0
        
        # Deduct points for risky patterns
        risky_patterns = {
            r'\bnew\b': 5,      # Raw new
            r'\bdelete\b': 5,   # Raw delete
            r'\bmalloc\b': 10,  # C-style malloc
            r'\bfree\b': 10,    # C-style free
            r'\bstrcpy\b': 15,  # Unsafe string copy
            r'\bsprintf\b': 10, # Unsafe string formatting
        }
        
        for pattern, penalty in risky_patterns.items():
            matches = re.findall(pattern, source_code)
            safety_score -= len(matches) * penalty
        
        # Add points for safe patterns
        safe_patterns = {
            r'\bstd::unique_ptr\b': 10,
            r'\bstd::shared_ptr\b': 10,
            r'\bstd::vector\b': 5,
            r'\bstd::string\b': 5,
        }
        
        for pattern, bonus in safe_patterns.items():
            matches = re.findall(pattern, source_code)
            safety_score += len(matches) * bonus
        
        return max(0, min(100, safety_score))
    
    def _find_cpp_modernizations(self, source_code: str) -> List[str]:
        """Find C++ modernization opportunities."""
        import re
        
        modernizations = []
        
        # Check for C-style casts
        if re.search(r'\([^)]*\)\s*\w+', source_code):
            modernizations.append("Consider using static_cast, dynamic_cast, or const_cast instead of C-style casts")
        
        # Check for raw pointers
        if re.search(r'\bnew\b', source_code) and not re.search(r'std::unique_ptr|std::shared_ptr', source_code):
            modernizations.append("Consider using smart pointers (unique_ptr, shared_ptr) instead of raw pointers")
        
        # Check for NULL vs nullptr
        if re.search(r'\bNULL\b', source_code):
            modernizations.append("Consider using nullptr instead of NULL")
        
        # Check for old-style for loops
        if re.search(r'for\s*\(\s*\w+\s+\w+\s*=.*?<.*?\+\+', source_code):
            modernizations.append("Consider using range-based for loops or iterators")
        
        return modernizations

class AICodeMutator:
    """AI-driven code mutation and evolution system."""
    
    def __init__(self, cpp_evolution_bridge: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.analyzer = AICodeAnalyzer()
        self.cpp_bridge_path = cpp_evolution_bridge or "./aios_kernel"
        
    async def mutate_code(self, request: MutationRequest) -> MutationResult:
        """Apply AI-guided mutations to source code."""
        try:
            # Calculate original hash
            original_hash = hashlib.sha256(request.source_code.encode()).hexdigest()
            
            if request.language == "Python":
                result = await self._mutate_python_code(request)
            elif request.language == "C++":
                result = await self._mutate_cpp_code(request)
            else:
                return MutationResult(
                    original_hash=original_hash,
                    mutated_code=request.source_code,
                    mutation_type=request.mutation_type,
                    fitness_improvement=0.0,
                    quantum_coherence_factor=0.0,
                    success=False,
                    error_message=f"Unsupported language: {request.language}"
                )
            
            result.original_hash = original_hash
            return result
            
        except Exception as e:
            self.logger.error(f"Code mutation failed: {e}")
            return MutationResult(
                original_hash=hashlib.sha256(request.source_code.encode()).hexdigest(),
                mutated_code=request.source_code,
                mutation_type=request.mutation_type,
                fitness_improvement=0.0,
                quantum_coherence_factor=0.0,
                success=False,
                error_message=str(e)
            )
    
    async def _mutate_python_code(self, request: MutationRequest) -> MutationResult:
        """Apply Python-specific mutations."""
        mutated_code = request.source_code
        fitness_improvement = 0.0
        
        try:
            tree = ast.parse(request.source_code)
            
            if request.mutation_type == "optimize":
                # Apply optimization mutations
                mutated_code = self._optimize_python_loops(mutated_code)
                mutated_code = self._optimize_python_imports(mutated_code)
                fitness_improvement = 0.15
                
            elif request.mutation_type == "refactor":
                # Apply refactoring mutations
                mutated_code = self._refactor_python_functions(mutated_code)
                mutated_code = self._improve_python_naming(mutated_code)
                fitness_improvement = 0.10
                
            elif request.mutation_type == "modernize":
                # Apply modernization mutations
                mutated_code = self._modernize_python_syntax(mutated_code)
                fitness_improvement = 0.08
            
            return MutationResult(
                original_hash="",  # Will be set by caller
                mutated_code=mutated_code,
                mutation_type=request.mutation_type,
                fitness_improvement=fitness_improvement,
                quantum_coherence_factor=1.0 if request.quantum_guided else 0.5,
                success=True
            )
            
        except Exception as e:
            return MutationResult(
                original_hash="",
                mutated_code=request.source_code,
                mutation_type=request.mutation_type,
                fitness_improvement=0.0,
                quantum_coherence_factor=0.0,
                success=False,
                error_message=str(e)
            )
    
    async def _mutate_cpp_code(self, request: MutationRequest) -> MutationResult:
        """Apply C++-specific mutations using the C++ evolution engine."""
        try:
            # Prepare command for C++ evolution engine
            command = [
                self.cpp_bridge_path,
                "--mutate",
                "--language", "C++",
                "--type", request.mutation_type,
                "--quantum-guided" if request.quantum_guided else "--no-quantum"
            ]
            
            # Create temporary file for source code
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as temp_file:
                temp_file.write(request.source_code)
                temp_file_path = temp_file.name
            
            command.extend(["--input", temp_file_path])
            
            # Execute C++ evolution engine
            result = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await result.communicate()
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            if result.returncode == 0:
                # Parse result from C++ engine
                output = json.loads(stdout.decode())
                return MutationResult(
                    original_hash="",
                    mutated_code=output.get("mutated_code", request.source_code),
                    mutation_type=request.mutation_type,
                    fitness_improvement=output.get("fitness_improvement", 0.0),
                    quantum_coherence_factor=output.get("quantum_coherence", 0.5),
                    success=True
                )
            else:
                error_msg = stderr.decode() if stderr else "Unknown error"
                return MutationResult(
                    original_hash="",
                    mutated_code=request.source_code,
                    mutation_type=request.mutation_type,
                    fitness_improvement=0.0,
                    quantum_coherence_factor=0.0,
                    success=False,
                    error_message=error_msg
                )
                
        except Exception as e:
            return MutationResult(
                original_hash="",
                mutated_code=request.source_code,
                mutation_type=request.mutation_type,
                fitness_improvement=0.0,
                quantum_coherence_factor=0.0,
                success=False,
                error_message=str(e)
            )
    
    def _optimize_python_loops(self, code: str) -> str:
        """Optimize Python loops using list comprehensions where appropriate."""
        import re
        
        # Simple pattern for basic for loop that could be a list comprehension
        pattern = r'(\w+)\s*=\s*\[\]\s*\n\s*for\s+(\w+)\s+in\s+([^:]+):\s*\n\s*\1\.append\(([^)]+)\)'
        
        def replace_with_comprehension(match):
            list_var = match.group(1)
            loop_var = match.group(2)
            iterable = match.group(3)
            expression = match.group(4)
            return f"{list_var} = [{expression} for {loop_var} in {iterable}]"
        
        return re.sub(pattern, replace_with_comprehension, code, flags=re.MULTILINE)
    
    def _optimize_python_imports(self, code: str) -> str:
        """Optimize Python imports by removing unused ones."""
        # This is a simplified version - real implementation would use AST analysis
        return code
    
    def _refactor_python_functions(self, code: str) -> str:
        """Refactor Python functions for better structure."""
        # Placeholder for function refactoring logic
        return code
    
    def _improve_python_naming(self, code: str) -> str:
        """Improve variable and function naming."""
        import re
        
        # Replace single-letter variables with more descriptive names
        replacements = {
            r'\bi\b': 'index',
            r'\bj\b': 'inner_index',
            r'\bk\b': 'counter',
            r'\bn\b': 'number',
            r'\bx\b': 'value',
        }
        
        for pattern, replacement in replacements.items():
            code = re.sub(pattern, replacement, code)
        
        return code
    
    def _modernize_python_syntax(self, code: str) -> str:
        """Modernize Python syntax to use newer features."""
        import re
        
        # Replace old-style string formatting
        code = re.sub(r'%\s*\([^)]+\)', '.format()', code)
        
        # Other modernization patterns...
        
        return code

class AIOrchestrationBridge:
    """Main bridge between Python AI logic and C++ evolution engine."""
    
    def __init__(self, cpp_engine_path: str = "./aios_kernel"):
        self.analyzer = AICodeAnalyzer()
        self.mutator = AICodeMutator(cpp_engine_path)
        self.logger = logging.getLogger(__name__)
        self.active_tasks = {}
        
    async def analyze_codebase(self, root_directory: str) -> Dict[str, Any]:
        """Analyze entire codebase and generate comprehensive report."""
        analysis_report = {
            "root_directory": root_directory,
            "timestamp": datetime.now().isoformat(),
            "languages_found": {},
            "overall_metrics": {},
            "recommendations": [],
            "evolution_candidates": []
        }
        
        # Scan directory for code files
        code_files = []
        for root, dirs, files in os.walk(root_directory):
            for file in files:
                if file.endswith(('.py', '.cpp', '.hpp', '.h', '.cs', '.js')):
                    code_files.append(os.path.join(root, file))
        
        # Analyze each file
        for file_path in code_files:
            try:
                # Determine language
                ext = os.path.splitext(file_path)[1]
                language_map = {
                    '.py': 'Python',
                    '.cpp': 'C++',
                    '.hpp': 'C++',
                    '.h': 'C++',
                    '.cs': 'C#',
                    '.js': 'JavaScript'
                }
                
                language = language_map.get(ext, 'Unknown')
                
                if language == 'Python':
                    file_analysis = self.analyzer.analyze_python_code(file_path)
                elif language == 'C++':
                    file_analysis = self.analyzer.analyze_cpp_code(file_path)
                else:
                    continue  # Skip unsupported languages
                
                # Update language statistics
                if language not in analysis_report["languages_found"]:
                    analysis_report["languages_found"][language] = {
                        "file_count": 0,
                        "total_complexity": 0,
                        "files": []
                    }
                
                lang_stats = analysis_report["languages_found"][language]
                lang_stats["file_count"] += 1
                lang_stats["total_complexity"] += file_analysis.get("complexity_score", 0)
                lang_stats["files"].append({
                    "path": file_path,
                    "analysis": file_analysis
                })
                
                # Identify evolution candidates
                if self._is_evolution_candidate(file_analysis):
                    analysis_report["evolution_candidates"].append({
                        "file_path": file_path,
                        "language": language,
                        "reason": self._get_evolution_reason(file_analysis)
                    })
                    
            except Exception as e:
                self.logger.error(f"Failed to analyze {file_path}: {e}")
        
        # Generate overall metrics
        analysis_report["overall_metrics"] = self._calculate_overall_metrics(analysis_report)
        
        # Generate recommendations
        analysis_report["recommendations"] = self._generate_recommendations(analysis_report)
        
        return analysis_report
    
    def _is_evolution_candidate(self, file_analysis: Dict[str, Any]) -> bool:
        """Determine if a file is a good candidate for evolution."""
        complexity = file_analysis.get("complexity_score", 0)
        issues = len(file_analysis.get("potential_issues", []))
        optimizations = len(file_analysis.get("optimization_opportunities", []))
        
        # High complexity or many issues/optimizations = good candidate
        return complexity > 5 or issues > 3 or optimizations > 2
    
    def _get_evolution_reason(self, file_analysis: Dict[str, Any]) -> str:
        """Get reason why file is evolution candidate."""
        reasons = []
        
        complexity = file_analysis.get("complexity_score", 0)
        if complexity > 5:
            reasons.append(f"High complexity ({complexity:.1f})")
        
        issues = len(file_analysis.get("potential_issues", []))
        if issues > 3:
            reasons.append(f"Multiple issues ({issues})")
        
        optimizations = len(file_analysis.get("optimization_opportunities", []))
        if optimizations > 2:
            reasons.append(f"Optimization opportunities ({optimizations})")
        
        return "; ".join(reasons)
    
    def _calculate_overall_metrics(self, analysis_report: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall codebase metrics."""
        metrics = {
            "total_files": 0,
            "average_complexity": 0,
            "total_issues": 0,
            "evolution_readiness": 0
        }
        
        total_complexity = 0
        total_files = 0
        total_issues = 0
        
        for language, lang_data in analysis_report["languages_found"].items():
            metrics["total_files"] += lang_data["file_count"]
            total_complexity += lang_data["total_complexity"]
            total_files += lang_data["file_count"]
            
            for file_data in lang_data["files"]:
                total_issues += len(file_data["analysis"].get("potential_issues", []))
        
        if total_files > 0:
            metrics["average_complexity"] = total_complexity / total_files
            metrics["total_issues"] = total_issues
            
            # Evolution readiness based on complexity and issues
            evolution_candidates = len(analysis_report["evolution_candidates"])
            metrics["evolution_readiness"] = (evolution_candidates / total_files) * 100
        
        return metrics
    
    def _generate_recommendations(self, analysis_report: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        metrics = analysis_report["overall_metrics"]
        
        if metrics["average_complexity"] > 5:
            recommendations.append("Consider refactoring high-complexity functions")
        
        if metrics["total_issues"] > metrics["total_files"] * 2:
            recommendations.append("Address code quality issues before evolution")
        
        if metrics["evolution_readiness"] > 30:
            recommendations.append("Good candidates for AI-driven evolution identified")
        
        evolution_count = len(analysis_report["evolution_candidates"])
        if evolution_count > 5:
            recommendations.append(f"Start evolution cycle with top {min(evolution_count, 10)} candidates")
        
        return recommendations

# Example usage and integration functions
async def main():
    """Example usage of the AI integration bridge."""
    logging.basicConfig(level=logging.INFO)
    
    # Initialize bridge
    bridge = AIOrchestrationBridge()
    
    # Analyze codebase
    print("Analyzing AIOS codebase...")
    analysis = await bridge.analyze_codebase("c:/dev/AIOS")
    
    print(f"Analysis complete:")
    print(f"- Total files: {analysis['overall_metrics']['total_files']}")
    print(f"- Average complexity: {analysis['overall_metrics']['average_complexity']:.1f}")
    print(f"- Evolution candidates: {len(analysis['evolution_candidates'])}")
    
    # Example mutation
    if analysis['evolution_candidates']:
        candidate = analysis['evolution_candidates'][0]
        print(f"\nTesting mutation on: {candidate['file_path']}")
        
        with open(candidate['file_path'], 'r') as f:
            source_code = f.read()
        
        mutation_request = MutationRequest(
            source_code=source_code,
            language=candidate['language'],
            mutation_type="optimize",
            fitness_criteria={"complexity": 0.3, "readability": 0.7},
            quantum_guided=True
        )
        
        mutation_result = await bridge.mutator.mutate_code(mutation_request)
        
        if mutation_result.success:
            print(f"Mutation successful! Fitness improvement: {mutation_result.fitness_improvement:.2f}")
        else:
            print(f"Mutation failed: {mutation_result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())
