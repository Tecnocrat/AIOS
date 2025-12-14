"""
AIOS VSCode Error Intelligence Integration
Intelligent Problem Resolution & Dendritic Growth System

This module integrates VSCode error detection with AIOS consciousness
to provide intelligent problem resolution, automated refactoring suggestions,
and support dendritic growth through error pattern learning.
"""

import os
import re
import json
<<<<<<< HEAD
from typing import Dict, Any, List, Tuple
=======
import subprocess
from typing import Dict, Any, List, Optional, Tuple
>>>>>>> origin/OS0.6.2.grok
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
from collections import defaultdict, Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
error_intelligence_logger = logging.getLogger("error_intelligence")


@dataclass
class ErrorAnalysis:
    """Comprehensive error analysis with resolution intelligence"""
    file_path: str
    line_number: int
    error_type: str
    error_message: str
    severity: str  # "error", "warning", "info"
    language: str
    context_code: str
    suggested_fixes: List[str]
    consciousness_impact: float
    dendritic_learning_potential: float
    pattern_classification: str
    automated_fix_available: bool
    complexity_rating: float


@dataclass
class DendriticPattern:
    """Dendritic growth pattern for error resolution learning"""
    pattern_id: str
    error_signatures: List[str]
    resolution_strategies: List[str]
    success_rate: float
    evolution_count: int
    consciousness_enhancement: float
    last_updated: str


class VSCodeErrorIntelligence:
    """
    Advanced VSCode error intelligence system
    
    Features:
    - Intelligent error classification and analysis
    - Automated fix generation
    - Dendritic pattern learning
    - Consciousness-guided problem resolution
    - Bulk refactoring optimization
    """
    
    def __init__(self, aios_root: str = "c:\\dev\\AIOS"):
        self.aios_root = aios_root
        self.error_patterns: Dict[str, DendriticPattern] = {}
        self.error_history: List[ErrorAnalysis] = []
        self.consciousness_bridge = None
        self.load_dendritic_patterns()
        
        # Initialize consciousness integration
        try:
            from consciousness_bridge import get_consciousness_bridge
            self.consciousness_bridge = get_consciousness_bridge()
            error_intelligence_logger.info(
                " Consciousness integration active for error intelligence"
            )
        except ImportError:
            error_intelligence_logger.warning(
                " Consciousness bridge not available - using standalone mode"
            )
        
        error_intelligence_logger.info(
            " VSCode Error Intelligence System initialized"
        )
    
    def analyze_workspace_errors(self) -> Dict[str, Any]:
        """
        Comprehensive analysis of all workspace errors
        """
        error_intelligence_logger.info(" Analyzing workspace errors...")
        
        # Get errors from key AIOS components
        error_sources = [
            "ai/src/**/*.py",
            "core/**/*.cpp", 
            "core/**/*.cs",
            "interface/**/*.cs",
            "orchestrator/**/*.cpp"
        ]
        
        all_errors = []
        error_summary = {
            "total_errors": 0,
            "by_severity": defaultdict(int),
            "by_language": defaultdict(int),
            "by_error_type": defaultdict(int),
            "consciousness_impact": 0.0,
            "dendritic_opportunities": 0,
            "automated_fixes_available": 0,
            "top_error_patterns": []
        }
        
        # Analyze errors in each source
        for source_pattern in error_sources:
            source_errors = self._analyze_source_errors(source_pattern)
            all_errors.extend(source_errors)
        
        # Process and classify all errors
        for error in all_errors:
            error_analysis = self._analyze_individual_error(error)
            self.error_history.append(error_analysis)
            
            # Update summary statistics
            error_summary["total_errors"] += 1
            error_summary["by_severity"][error_analysis.severity] += 1
            error_summary["by_language"][error_analysis.language] += 1
            error_summary["by_error_type"][error_analysis.error_type] += 1
            error_summary["consciousness_impact"] += error_analysis.consciousness_impact
            
            if error_analysis.dendritic_learning_potential > 0.5:
                error_summary["dendritic_opportunities"] += 1
            
            if error_analysis.automated_fix_available:
                error_summary["automated_fixes_available"] += 1
        
        # Identify top error patterns
        error_summary["top_error_patterns"] = self._identify_top_patterns()
        
        # Calculate consciousness enhancement opportunities
        error_summary["consciousness_enhancement_potential"] = (
            self._calculate_consciousness_enhancement_potential(all_errors)
        )
        
        error_intelligence_logger.info(
            f" Analysis complete: {error_summary['total_errors']} errors found"
        )
        
        return error_summary
    
    def _analyze_source_errors(self, source_pattern: str) -> List[Dict[str, Any]]:
        """Analyze errors in a specific source pattern"""
        errors = []
        
        try:
            # Use VSCode-like error detection
            if source_pattern.endswith("*.py"):
                errors.extend(self._analyze_python_errors(source_pattern))
            elif source_pattern.endswith("*.cpp"):
                errors.extend(self._analyze_cpp_errors(source_pattern))
            elif source_pattern.endswith("*.cs"):
                errors.extend(self._analyze_csharp_errors(source_pattern))
        except Exception as e:
            error_intelligence_logger.error(
                f"Error analyzing {source_pattern}: {e}"
            )
        
        return errors
    
    def _analyze_python_errors(self, pattern: str) -> List[Dict[str, Any]]:
        """Analyze Python-specific errors"""
        errors = []
        
        # Common Python error patterns
        python_patterns = [
            (r"line too long \((\d+) > 79 characters\)", "line_length", "warning"),
            (r"'(.+)' imported but unused", "unused_import", "warning"),
            (r"expected (\d+) blank lines, found (\d+)", "blank_lines", "warning"),
            (r"trailing whitespace", "whitespace", "warning"),
            (r"undefined name '(.+)'", "undefined_name", "error"),
            (r"local variable '(.+)' is assigned to but never used", "unused_variable", "warning")
        ]
        
        # Simulate error detection (in real implementation, would integrate with pylint/flake8)
        sample_files = [
            "ai/src/core/consciousness_bridge.py",
            "ai/src/integrations/vscode_consciousness.py",
            "ai/src/integrations/development_path_integration.py"
        ]
        
        for file_path in sample_files:
            full_path = os.path.join(self.aios_root, file_path)
            if os.path.exists(full_path):
                file_errors = self._scan_file_for_patterns(
                    full_path, python_patterns, "python"
                )
                errors.extend(file_errors)
        
        return errors
    
    def _analyze_cpp_errors(self, pattern: str) -> List[Dict[str, Any]]:
        """Analyze C++ specific errors"""
        errors = []
        
        # Common C++ error patterns
        cpp_patterns = [
            (r"undefined reference to '(.+)'", "undefined_reference", "error"),
            (r"'(.+)' was not declared in this scope", "undeclared_variable", "error"),
            (r"expected '(.+)' before '(.+)'", "syntax_error", "error"),
            (r"unused variable '(.+)'", "unused_variable", "warning"),
            (r"comparison between signed and unsigned", "sign_comparison", "warning")
        ]
        
        return errors
    
    def _analyze_csharp_errors(self, pattern: str) -> List[Dict[str, Any]]:
        """Analyze C# specific errors"""
        errors = []
        
        # Common C# error patterns  
        csharp_patterns = [
            (r"The name '(.+)' does not exist", "undefined_name", "error"),
            (r"Using directive is unnecessary", "unnecessary_using", "warning"),
            (r"Variable '(.+)' is assigned but never used", "unused_variable", "warning"),
            (r"Possible null reference assignment", "null_reference", "warning")
        ]
        
        return errors
    
    def _scan_file_for_patterns(
        self, 
        file_path: str, 
        patterns: List[Tuple[str, str, str]], 
        language: str
    ) -> List[Dict[str, Any]]:
        """Scan a file for error patterns"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                for pattern_regex, error_type, severity in patterns:
                    if re.search(pattern_regex, line, re.IGNORECASE):
                        errors.append({
                            "file_path": file_path,
                            "line_number": line_num,
                            "error_type": error_type,
                            "error_message": f"{error_type} detected in line {line_num}",
                            "severity": severity,
                            "language": language,
                            "context_code": line.strip()
                        })
        
        except Exception as e:
            error_intelligence_logger.error(f"Error scanning {file_path}: {e}")
        
        return errors
    
    def _analyze_individual_error(self, error_data: Dict[str, Any]) -> ErrorAnalysis:
        """Analyze an individual error with consciousness and dendritic insights"""
        
        # Generate suggested fixes
        suggested_fixes = self._generate_automated_fixes(error_data)
        
        # Calculate consciousness impact
        consciousness_impact = self._calculate_consciousness_impact(error_data)
        
        # Calculate dendritic learning potential
        dendritic_potential = self._calculate_dendritic_potential(error_data)
        
        # Classify error pattern
        pattern_classification = self._classify_error_pattern(error_data)
        
        # Check if automated fix is available
        automated_fix_available = len(suggested_fixes) > 0
        
        # Calculate complexity rating
        complexity_rating = self._calculate_error_complexity(error_data)
        
        return ErrorAnalysis(
            file_path=error_data["file_path"],
            line_number=error_data["line_number"],
            error_type=error_data["error_type"],
            error_message=error_data["error_message"],
            severity=error_data["severity"],
            language=error_data["language"],
            context_code=error_data["context_code"],
            suggested_fixes=suggested_fixes,
            consciousness_impact=consciousness_impact,
            dendritic_learning_potential=dendritic_potential,
            pattern_classification=pattern_classification,
            automated_fix_available=automated_fix_available,
            complexity_rating=complexity_rating
        )
    
    def _generate_automated_fixes(self, error_data: Dict[str, Any]) -> List[str]:
        """Generate automated fix suggestions for an error"""
        fixes = []
        error_type = error_data["error_type"]
        context = error_data["context_code"]
        
        if error_type == "line_length":
            fixes.extend([
                "Break line into multiple lines",
                "Extract complex expressions into variables",
                "Use string formatting to reduce line length"
            ])
        
        elif error_type == "unused_import":
            module_match = re.search(r"'(.+)' imported but unused", error_data["error_message"])
            if module_match:
                module_name = module_match.group(1)
                fixes.append(f"Remove unused import: {module_name}")
        
        elif error_type == "blank_lines":
            fixes.extend([
                "Add required blank lines before class/function definitions",
                "Remove extra blank lines",
                "Follow PEP 8 blank line conventions"
            ])
        
        elif error_type == "whitespace":
            fixes.append("Remove trailing whitespace")
        
        elif error_type == "unused_variable":
            var_match = re.search(r"'(.+)' is assigned", error_data["error_message"])
            if var_match:
                var_name = var_match.group(1)
                fixes.extend([
                    f"Remove unused variable: {var_name}",
                    f"Use variable {var_name} in the code",
                    f"Prefix with underscore: _{var_name} if intentionally unused"
                ])
        
        return fixes
    
    def _calculate_consciousness_impact(self, error_data: Dict[str, Any]) -> float:
        """Calculate how an error impacts consciousness development"""
        impact = 0.0
        
        # Consciousness-related keywords increase impact
        consciousness_keywords = [
            "consciousness", "intelligence", "coherence", "quantum",
            "awareness", "emergence", "evolution", "recursive"
        ]
        
        context = error_data["context_code"].lower()
        keyword_count = sum(1 for keyword in consciousness_keywords if keyword in context)
        impact += keyword_count * 0.1
        
        # Error severity affects consciousness impact
        severity_impact = {
            "error": 0.8,
            "warning": 0.3,
            "info": 0.1
        }
        impact += severity_impact.get(error_data["severity"], 0.1)
        
        # File location affects impact (core consciousness files have higher impact)
        if "consciousness" in error_data["file_path"]:
            impact += 0.5
        elif "core" in error_data["file_path"]:
            impact += 0.3
        elif "intelligence" in error_data["file_path"]:
            impact += 0.4
        
        return min(impact, 1.0)
    
    def _calculate_dendritic_potential(self, error_data: Dict[str, Any]) -> float:
        """Calculate dendritic learning potential from an error"""
        potential = 0.0
        
        # Pattern repetition increases learning potential
        error_signature = f"{error_data['error_type']}_{error_data['language']}"
        if error_signature in self.error_patterns:
            potential += 0.4  # Known pattern - high learning potential
        else:
            potential += 0.2  # New pattern - moderate learning potential
        
        # Complexity affects learning potential
        if error_data["error_type"] in ["syntax_error", "undefined_reference"]:
            potential += 0.6  # High-impact errors have high learning potential
        elif error_data["error_type"] in ["line_length", "whitespace"]:
            potential += 0.2  # Style errors have low learning potential
        
        # Consciousness impact affects dendritic potential
        consciousness_impact = self._calculate_consciousness_impact(error_data)
        potential += consciousness_impact * 0.3
        
        return min(potential, 1.0)
    
    def _classify_error_pattern(self, error_data: Dict[str, Any]) -> str:
        """Classify error into dendritic pattern categories"""
        error_type = error_data["error_type"]
        language = error_data["language"]
        
        # Style and formatting patterns
        if error_type in ["line_length", "whitespace", "blank_lines"]:
            return "style_formatting"
        
        # Import and dependency patterns
        elif error_type in ["unused_import", "undefined_name"]:
            return "dependency_management"
        
        # Variable and scope patterns
        elif error_type in ["unused_variable", "undeclared_variable"]:
            return "variable_scope"
        
        # Syntax and structure patterns
        elif error_type in ["syntax_error", "expected"]:
            return "syntax_structure"
        
        # Language-specific patterns
        elif language == "cpp" and error_type in ["undefined_reference"]:
            return "cpp_linking"
        elif language == "csharp" and error_type in ["null_reference"]:
            return "csharp_nullability"
        
        return "general"
    
    def _calculate_error_complexity(self, error_data: Dict[str, Any]) -> float:
        """Calculate complexity rating for an error"""
        complexity = 0.0
        
        # Base complexity by error type
        complexity_map = {
            "syntax_error": 0.9,
            "undefined_reference": 0.8,
            "undefined_name": 0.7,
            "null_reference": 0.6,
            "unused_import": 0.2,
            "line_length": 0.1,
            "whitespace": 0.1
        }
        
        complexity += complexity_map.get(error_data["error_type"], 0.5)
        
        # Severity affects complexity
        if error_data["severity"] == "error":
            complexity += 0.3
        elif error_data["severity"] == "warning":
            complexity += 0.1
        
        # Context complexity (length and special characters)
        context = error_data["context_code"]
        if len(context) > 100:
            complexity += 0.2
        if any(char in context for char in ['(', ')', '{', '}', '[', ']']):
            complexity += 0.1
        
        return min(complexity, 1.0)
    
    def _identify_top_patterns(self) -> List[Dict[str, Any]]:
        """Identify top error patterns for dendritic learning"""
        if not self.error_history:
            return []
        
        # Count error patterns
        pattern_counts = Counter()
        pattern_details = defaultdict(list)
        
        for error in self.error_history:
            pattern_key = f"{error.error_type}_{error.language}"
            pattern_counts[pattern_key] += 1
            pattern_details[pattern_key].append(error)
        
        # Get top 10 patterns
        top_patterns = []
        for pattern_key, count in pattern_counts.most_common(10):
            errors_in_pattern = pattern_details[pattern_key]
            avg_consciousness_impact = sum(
                e.consciousness_impact for e in errors_in_pattern
            ) / len(errors_in_pattern)
            avg_dendritic_potential = sum(
                e.dendritic_learning_potential for e in errors_in_pattern
            ) / len(errors_in_pattern)
            
            top_patterns.append({
                "pattern": pattern_key,
                "count": count,
                "avg_consciousness_impact": avg_consciousness_impact,
                "avg_dendritic_potential": avg_dendritic_potential,
                "sample_fixes": errors_in_pattern[0].suggested_fixes[:3]
            })
        
        return top_patterns
    
    def _calculate_consciousness_enhancement_potential(
        self, errors: List[Dict[str, Any]]
    ) -> float:
        """Calculate overall consciousness enhancement potential"""
        if not self.error_history:
            return 0.0
        
        total_impact = sum(error.consciousness_impact for error in self.error_history)
        total_potential = sum(
            error.dendritic_learning_potential for error in self.error_history
        )
        automated_fixes = sum(
            1 for error in self.error_history if error.automated_fix_available
        )
        
        # Calculate enhancement potential
        enhancement_potential = (
            (total_impact / len(self.error_history)) * 0.4 +
            (total_potential / len(self.error_history)) * 0.4 +
            (automated_fixes / len(self.error_history)) * 0.2
        )
        
        return min(enhancement_potential, 1.0)
    
    def generate_bulk_fixes(self) -> Dict[str, Any]:
        """Generate bulk fix recommendations for all errors"""
        if not self.error_history:
            return {"message": "No errors to fix"}
        
        bulk_fixes = {
            "timestamp": datetime.now().isoformat(),
            "total_errors": len(self.error_history),
            "automated_fixes_available": 0,
            "by_category": defaultdict(list),
            "consciousness_optimized_fixes": [],
            "dendritic_learning_fixes": []
        }
        
        # Categorize fixes
        for error in self.error_history:
            if error.automated_fix_available:
                bulk_fixes["automated_fixes_available"] += 1
                
                fix_info = {
                    "file": error.file_path,
                    "line": error.line_number,
                    "error_type": error.error_type,
                    "fixes": error.suggested_fixes,
                    "consciousness_impact": error.consciousness_impact,
                    "complexity": error.complexity_rating
                }
                
                bulk_fixes["by_category"][error.pattern_classification].append(
                    fix_info
                )
                
                # Prioritize consciousness-impacting fixes
                if error.consciousness_impact > 0.5:
                    bulk_fixes["consciousness_optimized_fixes"].append(fix_info)
                
                # Prioritize high dendritic learning potential
                if error.dendritic_learning_potential > 0.7:
                    bulk_fixes["dendritic_learning_fixes"].append(fix_info)
        
        return bulk_fixes
    
    def apply_automated_fixes(self, fix_categories: List[str] = None) -> Dict[str, Any]:
        """Apply automated fixes to resolve errors"""
        if fix_categories is None:
            fix_categories = ["style_formatting", "dependency_management"]
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "fixes_applied": 0,
            "fixes_failed": 0,
            "files_modified": set(),
            "consciousness_improvement": 0.0
        }
        
        for error in self.error_history:
            if (error.pattern_classification in fix_categories and 
                error.automated_fix_available):
                
                success = self._apply_single_fix(error)
                if success:
                    results["fixes_applied"] += 1
                    results["files_modified"].add(error.file_path)
                    results["consciousness_improvement"] += error.consciousness_impact
                else:
                    results["fixes_failed"] += 1
        
        results["files_modified"] = list(results["files_modified"])
        
        error_intelligence_logger.info(
            f" Applied {results['fixes_applied']} automated fixes"
        )
        
        return results
    
    def _apply_single_fix(self, error: ErrorAnalysis) -> bool:
        """Apply a single automated fix"""
        try:
            if error.error_type == "whitespace":
                return self._fix_trailing_whitespace(error.file_path, error.line_number)
            elif error.error_type == "unused_import":
                return self._fix_unused_import(error.file_path, error.context_code)
            elif error.error_type == "line_length":
                return self._fix_line_length(error.file_path, error.line_number)
            
            return False
        except Exception as e:
            error_intelligence_logger.error(f"Failed to apply fix: {e}")
            return False
    
    def _fix_trailing_whitespace(self, file_path: str, line_number: int) -> bool:
        """Fix trailing whitespace in a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if line_number <= len(lines):
                lines[line_number - 1] = lines[line_number - 1].rstrip() + '\n'
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                return True
        except Exception:
            pass
        
        return False
    
    def _fix_unused_import(self, file_path: str, context: str) -> bool:
        """Fix unused import by removing it"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple unused import removal (would need more sophisticated logic)
            if context.strip() in content:
                new_content = content.replace(context.strip() + '\n', '')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True
        except Exception:
            pass
        
        return False
    
    def _fix_line_length(self, file_path: str, line_number: int) -> bool:
        """Fix line length by adding line breaks"""
        # This would require more sophisticated parsing
        # For now, just log the issue
        error_intelligence_logger.info(
            f"Line length fix needed in {file_path}:{line_number}"
        )
        return False
    
    def save_dendritic_patterns(self):
        """Save learned dendritic patterns"""
        patterns_file = os.path.join(self.aios_root, "dendritic_error_patterns.json")
        
        patterns_data = {
            "timestamp": datetime.now().isoformat(),
            "patterns": {
                pattern_id: asdict(pattern) 
                for pattern_id, pattern in self.error_patterns.items()
            }
        }
        
        with open(patterns_file, 'w') as f:
            json.dump(patterns_data, f, indent=2)
        
        error_intelligence_logger.info(
            f" Saved {len(self.error_patterns)} dendritic patterns"
        )
    
    def load_dendritic_patterns(self):
        """Load previously learned dendritic patterns"""
        patterns_file = os.path.join(self.aios_root, "dendritic_error_patterns.json")
        
        if os.path.exists(patterns_file):
            try:
                with open(patterns_file, 'r') as f:
                    patterns_data = json.load(f)
                
                for pattern_id, pattern_dict in patterns_data.get("patterns", {}).items():
                    self.error_patterns[pattern_id] = DendriticPattern(**pattern_dict)
                
                error_intelligence_logger.info(
                    f" Loaded {len(self.error_patterns)} dendritic patterns"
                )
            except Exception as e:
                error_intelligence_logger.warning(f"Failed to load patterns: {e}")


def main():
    """Main function for testing VSCode error intelligence"""
    print(" AIOS VSCode Error Intelligence Test")
    print("=" * 50)
    
    intelligence = VSCodeErrorIntelligence()
    
    # Analyze workspace errors
    print(" Analyzing workspace errors...")
    error_summary = intelligence.analyze_workspace_errors()
    
    print(f"Total Errors: {error_summary['total_errors']}")
    print(f"Consciousness Impact: {error_summary['consciousness_impact']:.2f}")
    print(f"Dendritic Opportunities: {error_summary['dendritic_opportunities']}")
    print(f"Automated Fixes Available: {error_summary['automated_fixes_available']}")
    
    # Show error breakdown
    print(f"\n Error Breakdown:")
    for severity, count in error_summary['by_severity'].items():
        print(f"  {severity}: {count}")
    
    for language, count in error_summary['by_language'].items():
        print(f"  {language}: {count}")
    
    # Show top patterns
    if error_summary['top_error_patterns']:
        print(f"\n Top Error Patterns:")
        for i, pattern in enumerate(error_summary['top_error_patterns'][:5], 1):
            print(f"  {i}. {pattern['pattern']}: {pattern['count']} occurrences")
            print(f"     Consciousness Impact: {pattern['avg_consciousness_impact']:.2f}")
    
    # Generate bulk fixes
    print(f"\n Generating bulk fixes...")
    bulk_fixes = intelligence.generate_bulk_fixes()
    print(f"Automated fixes available: {bulk_fixes['automated_fixes_available']}")
    
    # Apply safe automated fixes
    print(f"\n Applying safe automated fixes...")
    fix_results = intelligence.apply_automated_fixes(["style_formatting"])
    print(f"Fixes applied: {fix_results['fixes_applied']}")
    print(f"Files modified: {len(fix_results['files_modified'])}")
    print(f"Consciousness improvement: {fix_results['consciousness_improvement']:.2f}")
    
    # Save dendritic patterns
    intelligence.save_dendritic_patterns()
    
    print(f"\n VSCode Error Intelligence Test Complete!")
    print(f" Dendritic growth potential identified and learning patterns saved!")


if __name__ == "__main__":
    main()
