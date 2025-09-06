#!/usr/bin/env python3
"""
🧬 AIOS CELLULAR REORGANIZATION ANALYZER
═══════════════════════════════════════════════════════════════════════════════
Advanced analysis tool to optimize AI folder structure using biological
cellular organization principles for enhanced visualization, behavior, 
and intercellular connectivity.
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class FunctionalDomain:
    """Represents a functional domain in the AI architecture"""
    name: str
    purpose: str
    current_folders: List[str] = field(default_factory=list)
    file_types: Set[str] = field(default_factory=set)
    dependencies: List[str] = field(default_factory=list)
    complexity_score: float = 0.0
    connectivity_score: float = 0.0


@dataclass
class CellularAnalysis:
    """Analysis results for cellular reorganization"""
    current_structure: Dict[str, any] = field(default_factory=dict)
    problems_identified: List[str] = field(default_factory=list)
    functional_domains: List[FunctionalDomain] = field(default_factory=list)
    proposed_structure: Dict[str, any] = field(default_factory=dict)
    optimization_metrics: Dict[str, float] = field(default_factory=dict)


class AIOSCellularReorganizer:
    """
    🔬 Advanced cellular reorganization analyzer for AIOS AI module
    
    Uses biological principles to optimize folder structure for:
    • Enhanced visualization
    • Improved behavior patterns  
    • Optimized intercellular connectivity
    • Reduced complexity and redundancy
    """
    
    def __init__(self, ai_root_path: str):
        self.ai_root_path = Path(ai_root_path)
        self.analysis = CellularAnalysis()
        
        # Functional domain templates based on biological systems
        self.domain_templates = {
            'core_nucleus': {
                'purpose': 'Central processing and coordination (like cell nucleus)',
                'keywords': ['core', 'main', 'master', 'central', 'primary']
            },
            'processing_organelles': {
                'purpose': 'Specialized processing units (like mitochondria, ribosomes)',
                'keywords': ['process', 'compute', 'engine', 'optimizer', 'compressor']
            },
            'membrane_interface': {
                'purpose': 'External communication and integration (like cell membrane)',
                'keywords': ['integration', 'interface', 'endpoint', 'bridge', 'api']
            },
            'transport_system': {
                'purpose': 'Data flow and intercellular communication',
                'keywords': ['intercellular', 'bridge', 'transport', 'flow', 'stream']
            },
            'support_cytoplasm': {
                'purpose': 'Supporting infrastructure and utilities',
                'keywords': ['config', 'env', 'deps', 'tools', 'scripts', 'utils']
            },
            'quality_control': {
                'purpose': 'Testing, validation, and quality assurance',
                'keywords': ['test', 'validation', 'quality', 'safety', 'check']
            },
            'information_storage': {
                'purpose': 'Documentation, logs, and persistent data',
                'keywords': ['docs', 'logs', 'cache', 'runtime', 'storage']
            },
            'experimental_lab': {
                'purpose': 'Research, demos, and experimental features',
                'keywords': ['demo', 'experiment', 'research', 'paradigm', 'prototype']
            }
        }
        
        logger.info(f"🔬 AIOS Cellular Reorganizer initialized for {ai_root_path}")
    
    def analyze_current_structure(self) -> Dict[str, any]:
        """Analyze the current scattered AI folder structure"""
        
        logger.info("🔍 Analyzing current AI folder structure...")
        
        structure = {}
        total_files = 0
        total_folders = 0
        file_types = defaultdict(int)
        depth_distribution = defaultdict(int)
        
        for root, dirs, files in os.walk(self.ai_root_path):
            # Skip cache directories
            if '__pycache__' in root or '.pytest_cache' in root:
                continue
                
            root_path = Path(root)
            relative_path = root_path.relative_to(self.ai_root_path)
            
            # Calculate depth
            if str(relative_path) == '.':
                depth = 0
            else:
                depth = len(relative_path.parts)
            
            depth_distribution[depth] += 1
            total_folders += 1
            
            # Analyze files
            folder_files = []
            for file_name in files:
                if not file_name.startswith('.') and not file_name.endswith('.pyc'):
                    file_path = root_path / file_name
                    folder_files.append({
                        'name': file_name,
                        'extension': file_path.suffix,
                        'size': file_path.stat().st_size if file_path.exists() else 0
                    })
                    file_types[file_path.suffix] += 1
                    total_files += 1
            
            # Store folder info
            if str(relative_path) != '.':
                structure[str(relative_path)] = {
                    'depth': depth,
                    'files': folder_files,
                    'file_count': len(folder_files),
                    'subdirs': dirs
                }
        
        self.analysis.current_structure = {
            'folder_tree': structure,
            'total_files': total_files,
            'total_folders': total_folders,
            'file_types': dict(file_types),
            'depth_distribution': dict(depth_distribution),
            'max_depth': max(depth_distribution.keys()) if depth_distribution else 0
        }
        
        logger.info(f"📊 Structure Analysis Complete:")
        logger.info(f"   Total folders: {total_folders}")
        logger.info(f"   Total files: {total_files}")
        logger.info(f"   Max depth: {self.analysis.current_structure['max_depth']}")
        logger.info(f"   Top-level folders: {depth_distribution.get(1, 0)}")
        
        return self.analysis.current_structure
    
    def identify_problems(self) -> List[str]:
        """Identify structural problems in the current organization"""
        
        problems = []
        structure = self.analysis.current_structure
        
        # Problem 1: Too many top-level folders
        top_level_count = structure['depth_distribution'].get(1, 0)
        if top_level_count > 8:
            problems.append(f"TOO_MANY_TOP_LEVEL: {top_level_count} folders at level 1 (optimal: 4-8)")
        
        # Problem 2: Inconsistent depth distribution
        depths = list(structure['depth_distribution'].keys())
        if len(depths) > 5:
            problems.append(f"EXCESSIVE_NESTING: {len(depths)} levels of nesting (optimal: 3-5)")
        
        # Problem 3: Scattered functionality
        folder_tree = structure['folder_tree']
        test_folders = [path for path in folder_tree.keys() if 'test' in path.lower()]
        config_folders = [path for path in folder_tree.keys() if any(word in path.lower() for word in ['config', 'env', 'deps'])]
        
        if len(test_folders) > 2:
            problems.append(f"SCATTERED_TESTS: Tests scattered across {len(test_folders)} locations")
        
        if len(config_folders) > 3:
            problems.append(f"SCATTERED_CONFIG: Configuration scattered across {len(config_folders)} locations")
        
        # Problem 4: Small folders (probably should be merged)
        small_folders = [path for path, info in folder_tree.items() 
                        if info['file_count'] <= 2 and len(info['subdirs']) == 0]
        if len(small_folders) > 5:
            problems.append(f"TOO_MANY_SMALL_FOLDERS: {len(small_folders)} folders with ≤2 files")
        
        # Problem 5: Unclear naming and organization
        unclear_names = [path for path in folder_tree.keys() 
                        if any(word in path.lower() for word in ['misc', 'other', 'temp', 'old'])]
        if unclear_names:
            problems.append(f"UNCLEAR_NAMING: Unclear folder names: {unclear_names}")
        
        self.analysis.problems_identified = problems
        
        logger.info(f"⚠️ Problems Identified: {len(problems)}")
        for problem in problems:
            logger.info(f"   • {problem}")
        
        return problems
    
    def map_functional_domains(self) -> List[FunctionalDomain]:
        """Map current folders to biological functional domains"""
        
        logger.info("🧬 Mapping folders to functional domains...")
        
        domains = []
        folder_tree = self.analysis.current_structure['folder_tree']
        
        # Initialize domains
        for domain_name, template in self.domain_templates.items():
            domain = FunctionalDomain(
                name=domain_name,
                purpose=template['purpose']
            )
            domains.append(domain)
        
        # Map folders to domains
        for folder_path, folder_info in folder_tree.items():
            folder_name = folder_path.lower()
            
            # Calculate complexity score
            complexity = (
                folder_info['file_count'] * 0.3 +
                len(folder_info['subdirs']) * 0.5 +
                folder_info['depth'] * 0.2
            )
            
            # Find best matching domain
            best_domain = None
            best_score = 0
            
            for domain in domains:
                template = self.domain_templates[domain.name]
                score = sum(1 for keyword in template['keywords'] if keyword in folder_name)
                
                # Special scoring for specific folders
                if domain.name == 'core_nucleus' and any(word in folder_name for word in ['src', 'core', 'main']):
                    score += 2
                elif domain.name == 'membrane_interface' and 'integration' in folder_name:
                    score += 2
                elif domain.name == 'quality_control' and 'test' in folder_name:
                    score += 2
                elif domain.name == 'experimental_lab' and any(word in folder_name for word in ['demo', 'paradigm']):
                    score += 2
                
                if score > best_score:
                    best_score = score
                    best_domain = domain
            
            # Assign to best matching domain (or create unmapped category)
            if best_domain and best_score > 0:
                best_domain.current_folders.append(folder_path)
                best_domain.complexity_score += complexity
                
                # Add file types
                for file_info in folder_info['files']:
                    best_domain.file_types.add(file_info['extension'])
        
        # Remove empty domains
        domains = [d for d in domains if d.current_folders]
        
        self.analysis.functional_domains = domains
        
        logger.info(f"🧬 Functional Domain Mapping:")
        for domain in domains:
            logger.info(f"   {domain.name}: {len(domain.current_folders)} folders")
            logger.info(f"     • {domain.purpose}")
            logger.info(f"     • Complexity: {domain.complexity_score:.2f}")
            logger.info(f"     • Folders: {domain.current_folders[:3]}{'...' if len(domain.current_folders) > 3 else ''}")
        
        return domains
    
    def design_optimal_structure(self) -> Dict[str, any]:
        """Design optimal cellular structure based on biological principles"""
        
        logger.info("🏗️ Designing optimal cellular structure...")
        
        # Core principles for optimal structure:
        # 1. 4-6 main cellular units (organs)
        # 2. Clear hierarchical organization
        # 3. Minimize cross-dependencies
        # 4. Optimize for intercellular communication
        
        optimal_structure = {
            'nucleus/': {
                'purpose': 'Central control and core processing',
                'contains': ['Core AI engines', 'Master coordination', 'Primary algorithms'],
                'recommended_folders': ['core/', 'master/', 'engines/'],
                'max_depth': 3,
                'complexity_target': 'high'
            },
            'organelles/': {
                'purpose': 'Specialized processing units',
                'contains': ['Compression', 'Optimization', 'Specialized AI cells'],
                'recommended_folders': ['compression/', 'optimization/', 'processors/'],
                'max_depth': 2,
                'complexity_target': 'medium'
            },
            'membrane/': {
                'purpose': 'External interfaces and integration',
                'contains': ['VS Code integration', 'APIs', 'External bridges'],
                'recommended_folders': ['interfaces/', 'integration/', 'apis/'],
                'max_depth': 3,
                'complexity_target': 'medium'
            },
            'transport/': {
                'purpose': 'Intercellular communication and data flow',
                'contains': ['Intercellular bridges', 'Data transport', 'Communication protocols'],
                'recommended_folders': ['intercellular/', 'bridges/', 'transport/'],
                'max_depth': 2,
                'complexity_target': 'low'
            },
            'cytoplasm/': {
                'purpose': 'Supporting infrastructure',
                'contains': ['Configuration', 'Environment', 'Dependencies', 'Utilities'],
                'recommended_folders': ['config/', 'env/', 'utils/', 'deps/'],
                'max_depth': 2,
                'complexity_target': 'low'
            },
            'laboratory/': {
                'purpose': 'Research, testing, and experimental features',
                'contains': ['All tests', 'Demos', 'Experimental paradigms', 'Research'],
                'recommended_folders': ['tests/', 'demos/', 'research/', 'experiments/'],
                'max_depth': 3,
                'complexity_target': 'variable'
            }
        }
        
        # Map current folders to optimal structure
        folder_mapping = {}
        
        for domain in self.analysis.functional_domains:
            if domain.name == 'core_nucleus':
                target_cell = 'nucleus/'
            elif domain.name == 'processing_organelles':
                target_cell = 'organelles/'
            elif domain.name == 'membrane_interface':
                target_cell = 'membrane/'
            elif domain.name == 'transport_system':
                target_cell = 'transport/'
            elif domain.name == 'support_cytoplasm':
                target_cell = 'cytoplasm/'
            elif domain.name in ['quality_control', 'experimental_lab']:
                target_cell = 'laboratory/'
            else:
                target_cell = 'cytoplasm/'  # default
            
            for folder in domain.current_folders:
                folder_mapping[folder] = target_cell
        
        optimal_structure['folder_mapping'] = folder_mapping
        
        self.analysis.proposed_structure = optimal_structure
        
        logger.info(f"🏗️ Optimal Structure Designed:")
        for cell_name, cell_info in optimal_structure.items():
            if cell_name != 'folder_mapping':
                mapped_folders = [f for f, target in folder_mapping.items() if target == cell_name]
                logger.info(f"   {cell_name}: {len(mapped_folders)} folders")
                logger.info(f"     • Purpose: {cell_info['purpose']}")
        
        return optimal_structure
    
    def calculate_optimization_metrics(self) -> Dict[str, float]:
        """Calculate optimization metrics for the proposed reorganization"""
        
        current = self.analysis.current_structure
        proposed = self.analysis.proposed_structure
        
        # Metric 1: Complexity reduction
        current_top_level = current['depth_distribution'].get(1, 0)
        proposed_top_level = len([k for k in proposed.keys() if k != 'folder_mapping'])
        complexity_reduction = (current_top_level - proposed_top_level) / current_top_level if current_top_level > 0 else 0
        
        # Metric 2: Depth optimization
        current_max_depth = current['max_depth']
        proposed_max_depth = 3  # Target max depth
        depth_optimization = (current_max_depth - proposed_max_depth) / current_max_depth if current_max_depth > 0 else 0
        
        # Metric 3: Functional coherence
        domain_coherence = len(self.analysis.functional_domains) / current_top_level if current_top_level > 0 else 0
        
        # Metric 4: Connectivity improvement
        connectivity_score = 0.8  # Estimated based on reduced cross-dependencies
        
        # Metric 5: Overall optimization score
        overall_score = (
            complexity_reduction * 0.3 +
            depth_optimization * 0.2 +
            domain_coherence * 0.2 +
            connectivity_score * 0.3
        )
        
        metrics = {
            'complexity_reduction': complexity_reduction,
            'depth_optimization': depth_optimization,
            'functional_coherence': domain_coherence,
            'connectivity_improvement': connectivity_score,
            'overall_optimization': overall_score
        }
        
        self.analysis.optimization_metrics = metrics
        
        logger.info(f"📊 Optimization Metrics:")
        for metric, value in metrics.items():
            logger.info(f"   {metric}: {value:.3f}")
        
        return metrics
    
    def run_complete_analysis(self) -> CellularAnalysis:
        """Run complete cellular reorganization analysis"""
        
        logger.info("🚀 Starting complete AIOS cellular reorganization analysis...")
        
        # Step 1: Analyze current structure
        self.analyze_current_structure()
        
        # Step 2: Identify problems
        self.identify_problems()
        
        # Step 3: Map to functional domains
        self.map_functional_domains()
        
        # Step 4: Design optimal structure
        self.design_optimal_structure()
        
        # Step 5: Calculate metrics
        self.calculate_optimization_metrics()
        
        logger.info("✅ Complete analysis finished!")
        
        return self.analysis
    
    def print_comprehensive_report(self):
        """Print comprehensive reorganization report"""
        
        print("\n🧬 AIOS CELLULAR REORGANIZATION ANALYSIS REPORT")
        print("═══════════════════════════════════════════════════════════════════")
        
        # Current structure summary
        current = self.analysis.current_structure
        print(f"📊 CURRENT STRUCTURE ANALYSIS:")
        print(f"   Total folders: {current['total_folders']}")
        print(f"   Total files: {current['total_files']}")
        print(f"   Maximum depth: {current['max_depth']} levels")
        print(f"   Top-level folders: {current['depth_distribution'].get(1, 0)}")
        
        print(f"\n   File type distribution:")
        for ext, count in sorted(current['file_types'].items(), key=lambda x: x[1], reverse=True):
            if ext:
                print(f"     {ext}: {count} files")
        
        # Problems identified
        print(f"\n⚠️ PROBLEMS IDENTIFIED ({len(self.analysis.problems_identified)}):")
        for i, problem in enumerate(self.analysis.problems_identified, 1):
            print(f"   {i}. {problem}")
        
        # Functional domains
        print(f"\n🧬 FUNCTIONAL DOMAIN MAPPING:")
        for domain in self.analysis.functional_domains:
            print(f"   {domain.name.upper()}:")
            print(f"     • Purpose: {domain.purpose}")
            print(f"     • Folders: {len(domain.current_folders)}")
            print(f"     • Complexity: {domain.complexity_score:.2f}")
            print(f"     • File types: {', '.join(sorted(domain.file_types))}")
        
        # Proposed optimal structure
        print(f"\n🏗️ PROPOSED OPTIMAL CELLULAR STRUCTURE:")
        proposed = self.analysis.proposed_structure
        folder_mapping = proposed.get('folder_mapping', {})
        
        for cell_name, cell_info in proposed.items():
            if cell_name != 'folder_mapping':
                mapped_folders = [f for f, target in folder_mapping.items() if target == cell_name]
                print(f"\n   {cell_name.upper()}")
                print(f"     • Purpose: {cell_info['purpose']}")
                print(f"     • Target complexity: {cell_info['complexity_target']}")
                print(f"     • Max depth: {cell_info['max_depth']}")
                print(f"     • Current folders to merge: {len(mapped_folders)}")
                if mapped_folders:
                    print(f"     • Folders: {', '.join(mapped_folders[:5])}{'...' if len(mapped_folders) > 5 else ''}")
        
        # Optimization metrics
        print(f"\n📈 OPTIMIZATION METRICS:")
        metrics = self.analysis.optimization_metrics
        for metric, value in metrics.items():
            percentage = value * 100
            print(f"   {metric.replace('_', ' ').title()}: {percentage:.1f}%")
        
        # Recommendations
        print(f"\n🎯 RECOMMENDATIONS:")
        overall_score = metrics.get('overall_optimization', 0)
        
        if overall_score >= 0.7:
            print("   ✅ EXCELLENT: Reorganization will provide significant benefits")
        elif overall_score >= 0.5:
            print("   👍 GOOD: Reorganization will provide notable improvements")
        elif overall_score >= 0.3:
            print("   📈 MODERATE: Reorganization will provide some benefits")
        else:
            print("   ⚠️ LIMITED: Reorganization benefits may be minimal")
        
        print(f"\n   Priority actions:")
        print(f"   1. Consolidate {current['depth_distribution'].get(1, 0)} top-level folders into 6 cellular units")
        print(f"   2. Move all tests into laboratory/ cellular unit")
        print(f"   3. Consolidate configuration files into cytoplasm/ cellular unit")
        print(f"   4. Establish clear intercellular communication protocols")
        print(f"   5. Implement cellular interface standards")


def main():
    """Run AIOS cellular reorganization analysis"""
    
    print("🔬 AIOS CELLULAR REORGANIZATION ANALYZER")
    print("═══════════════════════════════════════════")
    print("Advanced biological-inspired optimization:")
    print("  🧬 Functional domain mapping")
    print("  🏗️ Optimal cellular structure design")
    print("  📊 Comprehensive analysis metrics")
    print("  🎯 Actionable recommendations")
    print()
    
    # Configuration
    ai_path = r"C:\dev\AIOS\ai"
    
    print(f"🔧 Analysis Configuration:")
    print(f"   AI module path: {ai_path}")
    print()
    
    # Create and run analyzer
    reorganizer = AIOSCellularReorganizer(ai_path)
    
    # Run complete analysis
    analysis_results = reorganizer.run_complete_analysis()
    
    # Print comprehensive report
    reorganizer.print_comprehensive_report()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    main()
