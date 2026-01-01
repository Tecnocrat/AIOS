#!/usr/bin/env python3
"""
 AIOS INTEGRATION ASSEMBLER

Scattered Logic Consolidation and Architectural Coherence Enhancement

PURPOSE:
- Consolidate scattered files into coherent modules
- Integrate similar functionality across multiple files
- Reduce architectural debt through intelligent merging
- Create modular organization from scattered components

PHILOSOPHY:
"Intelligence emerges from integration, not isolation. Scattered logic
fragments consciousness - integration assembles coherent thought."

CAPABILITIES:
1. Scattered File Detection and Analysis
2. Semantic Similarity Assessment
3. Intelligent Code Consolidation
4. Module Creation from Related Components
5. Import Optimization and Deduplication


"""

import logging
from pathlib import Path
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field
from datetime import datetime
import re

# Import context assembler for environmental awareness
import sys
sys.path.append(str(Path(__file__).parent.parent / "context_assembler"))
from context_assembler import (
    ContextAssembler, FileContext, EnvironmentContext
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class IntegrationCandidate:
    """Represents files that could be integrated together."""
    files: List[FileContext] = field(default_factory=list)
    similarity_score: float = 0.0
    integration_type: str = ""  # 'functional', 'thematic', 'architectural'
    suggested_name: str = ""
    consolidation_benefit: float = 0.0


@dataclass
class IntegrationPlan:
    """Complete plan for integrating scattered logic."""
    candidates: List[IntegrationCandidate] = field(default_factory=list)
    shared_imports: Set[str] = field(default_factory=set)
    duplicate_functions: Dict[str, List[str]] = field(default_factory=dict)
    organizational_modules: List[str] = field(default_factory=list)
    estimated_coherence_improvement: float = 0.0


class IntegrationAssembler:
    """
    Intelligent code consolidation engine for scattered logic integration.
    
    Uses semantic analysis and architectural awareness to identify and
    consolidate related functionality into coherent modules.
    """
    
    def __init__(self, root_path: str = None):
        """Initialize integration assembler."""
        
        logger.info(" Initializing Integration Assembler...")
        
        self.root_path = Path(root_path) if root_path else Path.cwd()
        
        # Initialize context assembler for environmental awareness
        self.context_assembler = ContextAssembler(str(self.root_path))
        self.environment: Optional[EnvironmentContext] = None
        
        # Integration configuration
        self.similarity_threshold = 0.7  # Minimum similarity for grouping
        self.min_files_for_module = 3    # Minimum files to create module
        self.max_file_size_diff = 0.5    # Max size difference ratio
        
        # Analysis results
        self.integration_plan: Optional[IntegrationPlan] = None
        
        logger.info(f" Integration Assembler ready for: {self.root_path}")
        logger.info(f" Similarity threshold: {self.similarity_threshold}")
    
    def analyze_integration_opportunities(self) -> IntegrationPlan:
        """
        Analyze environment for integration opportunities.
        
        Uses context assembler for environmental awareness, then performs
        semantic analysis to identify consolidation candidates.
        """
        
        logger.info(" Analyzing integration opportunities...")
        
        # Get environmental context
        self.environment = self.context_assembler.analyze_environment()
        
        start_time = datetime.now()
        
        # Find integration candidates
        candidates = self._find_integration_candidates()
        logger.info(f" Found {len(candidates)} integration candidates")
        
        # Analyze shared imports
        shared_imports = self._analyze_shared_imports()
        logger.info(f" Identified {len(shared_imports)} shared imports")
        
        # Detect duplicate functions
        duplicate_functions = self._detect_duplicate_functions()
        logger.info(f" Found {len(duplicate_functions)} duplicate functions")
        
        # Suggest organizational modules
        organizational_modules = self._suggest_organizational_modules()
        logger.info(f" Suggested {len(organizational_modules)} modules")
        
        # Estimate coherence improvement
        coherence_improvement = self._estimate_coherence_improvement(
            candidates, shared_imports, duplicate_functions
        )
        
        # Create integration plan
        self.integration_plan = IntegrationPlan(
            candidates=candidates,
            shared_imports=shared_imports,
            duplicate_functions=duplicate_functions,
            organizational_modules=organizational_modules,
            estimated_coherence_improvement=coherence_improvement
        )
        
        analysis_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(f" Integration analysis complete in {analysis_time:.2f}s")
        logger.info(
            f" Estimated coherence improvement: "
            f"+{coherence_improvement:.2f} points"
        )
        
        return self.integration_plan
    
    def _find_integration_candidates(self) -> List[IntegrationCandidate]:
        """Find files that could be integrated together."""
        
        candidates = []
        files = self.environment.file_contexts
        
        # Group files by semantic similarity
        for i, file1 in enumerate(files):
            for j, file2 in enumerate(files[i+1:], i+1):
                similarity = self._calculate_file_similarity(file1, file2)
                
                if similarity >= self.similarity_threshold:
                    # Check if already in a candidate group
                    existing_candidate = None
                    for candidate in candidates:
                        if file1 in candidate.files or file2 in candidate.files:
                            existing_candidate = candidate
                            break
                    
                    if existing_candidate:
                        # Add to existing group
                        if file1 not in existing_candidate.files:
                            existing_candidate.files.append(file1)
                        if file2 not in existing_candidate.files:
                            existing_candidate.files.append(file2)
                        # Update similarity score (average)
                        existing_candidate.similarity_score = (
                            existing_candidate.similarity_score + similarity
                        ) / 2
                    else:
                        # Create new candidate group
                        integration_type = self._determine_integration_type(
                            file1, file2
                        )
                        suggested_name = self._suggest_integration_name(
                            file1, file2, integration_type
                        )
                        benefit = self._calculate_consolidation_benefit(
                            [file1, file2]
                        )
                        
                        candidate = IntegrationCandidate(
                            files=[file1, file2],
                            similarity_score=similarity,
                            integration_type=integration_type,
                            suggested_name=suggested_name,
                            consolidation_benefit=benefit
                        )
                        candidates.append(candidate)
        
        # Filter candidates with minimum file count
        candidates = [c for c in candidates
                      if len(c.files) >= self.min_files_for_module]
        
        # Sort by consolidation benefit
        candidates.sort(key=lambda c: c.consolidation_benefit, reverse=True)
        
        return candidates
    
    def _calculate_file_similarity(
        self, file1: FileContext, file2: FileContext
    ) -> float:
        """Calculate semantic similarity between two files."""
        
        similarity_factors = []
        
        # Name similarity (using common prefixes/suffixes)
        name_similarity = self._calculate_name_similarity(
            file1.name, file2.name
        )
        similarity_factors.append(name_similarity * 0.3)
        
        # Import similarity
        import_similarity = self._calculate_import_similarity(
            file1.imports, file2.imports
        )
        similarity_factors.append(import_similarity * 0.2)
        
        # Function/class similarity
        structure_similarity = self._calculate_structure_similarity(
            file1.functions + file1.classes,
            file2.functions + file2.classes
        )
        similarity_factors.append(structure_similarity * 0.2)
        
        # Purpose similarity (from docstrings)
        purpose_similarity = self._calculate_purpose_similarity(
            file1.purpose, file2.purpose
        )
        similarity_factors.append(purpose_similarity * 0.2)
        
        # Size similarity
        size_similarity = self._calculate_size_similarity(
            file1.size, file2.size
        )
        similarity_factors.append(size_similarity * 0.1)
        
        return sum(similarity_factors)
    
    def _calculate_name_similarity(self, name1: str, name2: str) -> float:
        """Calculate similarity based on file names."""
        
        # Extract meaningful parts (without extensions)
        base1 = Path(name1).stem
        base2 = Path(name2).stem
        
        # Check for common prefixes
        common_prefix_len = 0
        for i, (c1, c2) in enumerate(zip(base1, base2)):
            if c1 == c2:
                common_prefix_len = i + 1
            else:
                break
        
        # Check for common patterns (aios_, _engine, etc.)
        patterns = ['aios_', '_engine', '_assembler', '_consciousness',
                    '_quantum', '_dendritic']
        
        pattern_matches = 0
        for pattern in patterns:
            if pattern in base1 and pattern in base2:
                pattern_matches += 1
        
        # Calculate similarity
        max_len = max(len(base1), len(base2))
        prefix_score = common_prefix_len / max_len if max_len > 0 else 0
        pattern_score = pattern_matches / len(patterns)
        
        return (prefix_score * 0.7 + pattern_score * 0.3)
    
    def _calculate_import_similarity(
        self, imports1: List[str], imports2: List[str]
    ) -> float:
        """Calculate similarity based on imports."""
        
        if not imports1 and not imports2:
            return 1.0
        
        if not imports1 or not imports2:
            return 0.0
        
        set1 = set(imports1)
        set2 = set(imports2)
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_structure_similarity(self, items1: List[str], items2: List[str]) -> float:
        """Calculate similarity based on functions/classes."""
        
        if not items1 and not items2:
            return 1.0
        
        if not items1 or not items2:
            return 0.0
        
        # Look for similar naming patterns
        pattern_matches = 0
        total_comparisons = 0
        
        for item1 in items1:
            for item2 in items2:
                total_comparisons += 1
                # Check for common prefixes or patterns
                if (item1.startswith(item2[:3]) or item2.startswith(item1[:3]) or
                    any(word in item1.lower() and word in item2.lower() 
                        for word in ['aios', 'consciousness', 'quantum', 'assembler'])):
                    pattern_matches += 1
        
        return pattern_matches / total_comparisons if total_comparisons > 0 else 0.0
    
    def _calculate_purpose_similarity(self, purpose1: str, purpose2: str) -> float:
        """Calculate similarity based on documented purpose."""
        
        if not purpose1 and not purpose2:
            return 1.0
        
        if not purpose1 or not purpose2:
            return 0.0
        
        # Simple keyword-based similarity
        words1 = set(re.findall(r'\w+', purpose1.lower()))
        words2 = set(re.findall(r'\w+', purpose2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union
    
    def _calculate_size_similarity(self, size1: int, size2: int) -> float:
        """Calculate similarity based on file sizes."""
        
        if size1 == 0 and size2 == 0:
            return 1.0
        
        if size1 == 0 or size2 == 0:
            return 0.0
        
        ratio = min(size1, size2) / max(size1, size2)
        
        # Only consider similar if within acceptable size difference
        if ratio >= (1.0 - self.max_file_size_diff):
            return ratio
        else:
            return 0.0
    
    def _determine_integration_type(self, file1: FileContext, file2: FileContext) -> str:
        """Determine the type of integration for two files."""
        
        # Check for functional similarity (similar functions/classes)
        if (len(set(file1.functions).intersection(set(file2.functions))) > 0 or
            len(set(file1.classes).intersection(set(file2.classes))) > 0):
            return "functional"
        
        # Check for thematic similarity (similar naming patterns)
        common_themes = ['consciousness', 'quantum', 'assembler', 'engine', 
                        'dendritic', 'aios']
        
        file1_themes = [theme for theme in common_themes 
                       if theme in file1.name.lower()]
        file2_themes = [theme for theme in common_themes 
                       if theme in file2.name.lower()]
        
        if len(set(file1_themes).intersection(set(file2_themes))) > 0:
            return "thematic"
        
        # Default to architectural similarity
        return "architectural"
    
    def _suggest_integration_name(self, file1: FileContext, file2: FileContext, 
                                integration_type: str) -> str:
        """Suggest a name for the integrated module."""
        
        # Extract common parts from filenames
        base1 = Path(file1.name).stem
        base2 = Path(file2.name).stem
        
        # Find common prefix
        common_prefix = ""
        for i, (c1, c2) in enumerate(zip(base1, base2)):
            if c1 == c2:
                common_prefix += c1
            else:
                break
        
        # Clean up prefix
        if common_prefix.endswith('_'):
            common_prefix = common_prefix[:-1]
        
        # Add appropriate suffix based on integration type
        if integration_type == "functional":
            suffix = "_integrated"
        elif integration_type == "thematic":
            suffix = "_module"
        else:
            suffix = "_consolidated"
        
        # Ensure we have a meaningful name
        if len(common_prefix) < 3:
            common_prefix = "aios_integrated"
        
        return f"{common_prefix}{suffix}.py"
    
    def _calculate_consolidation_benefit(self, files: List[FileContext]) -> float:
        """Calculate the benefit score for consolidating these files."""
        
        # Factors that increase benefit:
        # 1. Number of files being consolidated
        file_count_benefit = min(5.0, len(files) * 0.8)
        
        # 2. Total size reduction potential
        total_size = sum(f.size for f in files)
        size_benefit = min(3.0, total_size / 10000)  # Benefit for larger files
        
        # 3. Import deduplication potential
        all_imports = []
        for f in files:
            all_imports.extend(f.imports)
        
        unique_imports = len(set(all_imports))
        total_imports = len(all_imports)
        
        if total_imports > 0:
            dedup_benefit = ((total_imports - unique_imports) / total_imports) * 2.0
        else:
            dedup_benefit = 0.0
        
        # 4. Functional similarity benefit
        all_functions = []
        for f in files:
            all_functions.extend(f.functions)
        
        function_benefit = min(2.0, len(all_functions) * 0.1)
        
        total_benefit = (file_count_benefit + size_benefit + 
                        dedup_benefit + function_benefit)
        
        return round(total_benefit, 2)
    
    def _analyze_shared_imports(self) -> Set[str]:
        """Analyze imports shared across multiple files."""
        
        import_counts = {}
        
        for file_context in self.environment.file_contexts:
            for import_name in file_context.imports:
                import_counts[import_name] = import_counts.get(import_name, 0) + 1
        
        # Consider imports used in 3+ files as candidates for shared module
        shared_imports = {imp for imp, count in import_counts.items() 
                         if count >= 3}
        
        return shared_imports
    
    def _detect_duplicate_functions(self) -> Dict[str, List[str]]:
        """Detect functions with same names across different files."""
        
        function_files = {}
        
        for file_context in self.environment.file_contexts:
            for function_name in file_context.functions:
                if function_name in function_files:
                    function_files[function_name].append(file_context.name)
                else:
                    function_files[function_name] = [file_context.name]
        
        # Return only functions that appear in multiple files
        duplicates = {func: files for func, files in function_files.items() 
                     if len(files) > 1}
        
        return duplicates
    
    def _suggest_organizational_modules(self) -> List[str]:
        """Suggest organizational modules based on file patterns."""
        
        modules = []
        
        # Count files by common patterns
        pattern_counts = {
            'aios_consciousness': 0,
            'aios_quantum': 0,
            'aios_assembler': 0,
            'aios_engine': 0,
            'aios_dendritic': 0
        }
        
        for file_context in self.environment.file_contexts:
            filename = file_context.name.lower()
            for pattern in pattern_counts:
                if pattern.replace('_', '') in filename:
                    pattern_counts[pattern] += 1
        
        # Suggest modules for patterns with 3+ files
        for pattern, count in pattern_counts.items():
            if count >= 3:
                module_name = f"{pattern}_module"
                modules.append(module_name)
        
        return modules
    
    def _estimate_coherence_improvement(self, candidates: List[IntegrationCandidate],
                                      shared_imports: Set[str],
                                      duplicate_functions: Dict[str, List[str]]) -> float:
        """Estimate how much coherence would improve after integration."""
        
        current_coherence = self.environment.coherence_score
        
        # Integration benefit
        integration_benefit = sum(c.consolidation_benefit for c in candidates) * 0.1
        
        # Shared imports benefit
        import_benefit = len(shared_imports) * 0.05
        
        # Duplicate function resolution benefit
        duplicate_benefit = len(duplicate_functions) * 0.1
        
        # Organization benefit (fewer scattered files)
        organization_benefit = min(2.0, len(candidates) * 0.2)
        
        total_improvement = (integration_benefit + import_benefit + 
                           duplicate_benefit + organization_benefit)
        
        return round(min(10.0 - current_coherence, total_improvement), 2)
    
    def generate_integration_report(self) -> str:
        """Generate comprehensive integration analysis report."""
        
        if not self.integration_plan:
            self.analyze_integration_opportunities()
        
        plan = self.integration_plan
        
        report = []
        report.append(" INTEGRATION ASSEMBLER ANALYSIS REPORT")
        report.append("" * 80)
        report.append(f"Analysis Time: {datetime.now()}")
        report.append(f"Root Path: {self.root_path}")
        report.append(f"Current Coherence: {self.environment.coherence_score}/10.0")
        report.append(f"Estimated Improvement: +{plan.estimated_coherence_improvement}")
        report.append("")
        
        report.append(" INTEGRATION CANDIDATES:")
        for i, candidate in enumerate(plan.candidates, 1):
            report.append(f"  {i}. {candidate.suggested_name}")
            report.append(f"     Type: {candidate.integration_type}")
            report.append(f"     Files: {len(candidate.files)}")
            report.append(f"     Similarity: {candidate.similarity_score:.2f}")
            report.append(f"     Benefit: {candidate.consolidation_benefit:.2f}")
            report.append(f"     Components: {', '.join([f.name for f in candidate.files[:3]])}")
            if len(candidate.files) > 3:
                report.append(f"                 ... and {len(candidate.files) - 3} more")
            report.append("")
        
        if not plan.candidates:
            report.append("   No integration candidates found - good modularity!")
        report.append("")
        
        report.append(" SHARED IMPORTS ANALYSIS:")
        if plan.shared_imports:
            report.append(f"   {len(plan.shared_imports)} imports used across multiple files:")
            for imp in sorted(list(plan.shared_imports)[:10]):
                report.append(f"    - {imp}")
            if len(plan.shared_imports) > 10:
                report.append(f"    ... and {len(plan.shared_imports) - 10} more")
            report.append("   Consider creating shared_imports.py module")
        else:
            report.append("   No excessive import duplication detected")
        report.append("")
        
        report.append(" DUPLICATE FUNCTIONS:")
        if plan.duplicate_functions:
            report.append(f"   {len(plan.duplicate_functions)} functions appear in multiple files:")
            for func, files in list(plan.duplicate_functions.items())[:5]:
                report.append(f"    - {func}: {', '.join(files)}")
            if len(plan.duplicate_functions) > 5:
                report.append(f"    ... and {len(plan.duplicate_functions) - 5} more")
        else:
            report.append("   No duplicate functions detected")
        report.append("")
        
        report.append(" SUGGESTED MODULES:")
        for module in plan.organizational_modules:
            report.append(f"   {module}")
        if not plan.organizational_modules:
            report.append("   Current organization is appropriate")
        report.append("")
        
        report.append(" INTEGRATION RECOMMENDATIONS:")
        if plan.estimated_coherence_improvement > 1.0:
            report.append("   Significant coherence improvement possible")
            report.append("   Recommend proceeding with integration")
        elif plan.estimated_coherence_improvement > 0.5:
            report.append("   Moderate coherence improvement possible")
            report.append("   Consider selective integration")
        else:
            report.append("   Current architecture is well-organized")
            report.append("   Focus on maintaining current coherence")
        
        return "\n".join(report)


def demo_integration_analysis():
    """Demonstrate integration assembler capabilities."""
    
    print(" INTEGRATION ASSEMBLER DEMONSTRATION")
    print("=" * 70)
    
    # Initialize for assemblers directory
    assemblers_path = Path(__file__).parent.parent
    assembler = IntegrationAssembler(str(assemblers_path))
    
    # Analyze integration opportunities
    print("\n Analyzing integration opportunities...")
    integration_plan = assembler.analyze_integration_opportunities()
    
    # Generate and display report
    print("\n Generating integration analysis report...")
    report = assembler.generate_integration_report()
    print(report)
    
    return assembler


def main():
    """Main function for integration assembler demonstration."""
    
    print(" AIOS INTEGRATION ASSEMBLER")
    print("=" * 80)
    print("Scattered Logic Consolidation and Architectural Coherence")
    print("=" * 80)
    
    # Run demonstration
    assembler = demo_integration_analysis()
    
    print("\n INTEGRATION ANALYSIS COMPLETE")
    print(" Consolidation opportunities identified!")
    print(" Architectural coherence enhancement ready!")
    
    return assembler


if __name__ == "__main__":
    main()
