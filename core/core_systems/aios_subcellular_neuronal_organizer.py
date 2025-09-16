#!/usr/bin/env python3
"""
 AIOS Subcellular Neuronal Organizer
=====================================

Advanced neuronal intelligence for subcellular organization and enhancement.
Specifically designed for analysis_tools and similar subcellular units.

Features:
- Neuronal coherence analysis
- Tachyonic archival recommendations
- Subcellular structure optimization
- Consciousness backup management
- Dendritic enhancement patterns

Author: AIOS Neuronal Intelligence Framework
Version: 1.0.0 (Neuronal Evolution)
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class AIOSSubcellularNeuronalOrganizer:
    """Advanced neuronal organizer for subcellular units and Core Engine structure."""

    def __init__(self, subcellular_path: Path, mode: str = 'subcellular'):
        self.subcellular_path = Path(subcellular_path)
        self.subcellular_name = self.subcellular_path.name
        self.parent_path = self.subcellular_path.parent
        self.mode = mode  # 'subcellular' or 'core_engine'

        # Neuronal categorization patterns (expanded for Core Engine mode)
        if mode == 'core_engine':
            self.neuronal_categories = self._get_core_engine_categories()
        else:
            self.neuronal_categories = self._get_subcellular_categories()
    
    def _get_subcellular_categories(self) -> Dict[str, Any]:
        """Get categorization patterns for subcellular units."""
        return {
            'operational_tools': {
                'pattern': lambda f: (f.endswith('.py') and
                                      not f.endswith('.consciousness_backup')),
                'priority': 'high',
                'action': 'keep_active'
            },
            'consciousness_backups': {
                'pattern': lambda f: f.endswith('.consciousness_backup'),
                'priority': 'low',
                'action': 'tachyonic_archive'
            },
            'metadata_files': {
                'pattern': lambda f: (f.endswith('.md') and
                                      not f.startswith('CORE_ENGINE')),
                'priority': 'medium',
                'action': 'subcellular_organize'
            },
            'analysis_outputs': {
                'pattern': lambda f: f.endswith('.json') or f.endswith('.log'),
                'priority': 'low',
                'action': 'tachyonic_archive'
            },
            'guidance_docs': {
                'pattern': lambda f: (f.startswith('AIOS_') and
                                      f.endswith('.md')),
                'priority': 'high',
                'action': 'keep_active'
            }
        }
    
    def _get_core_engine_categories(self) -> Dict[str, Any]:
        """Get categorization patterns for Core Engine organization."""
        return {
            'documentation_files': {
                'pattern': lambda f: f.endswith('.md'),
                'priority': 'medium',
                'action': 'move_to_documentation',
                'target_subcell': 'documentation'
            },
            'runtime_reports': {
                'pattern': lambda f: (f.endswith('.json') and 
                                     ('REPORT' in f.upper() or 'ANALYSIS' in f.upper())),
                'priority': 'medium',
                'action': 'move_to_runtime_intelligence',
                'target_subcell': 'runtime_intelligence'
            },
            'bridge_implementations': {
                'pattern': lambda f: ('_bridge.py' in f),
                'priority': 'high',
                'action': 'move_to_bridges',
                'target_subcell': 'bridges'
            },
            'analysis_tools': {
                'pattern': lambda f: (f.endswith('.py') and 
                                     ('_test.py' in f or '_analysis' in f or 
                                      '_connectivity_enhancer.py' in f)),
                'priority': 'high',
                'action': 'move_to_analysis_tools',
                'target_subcell': 'analysis_tools'
            },
            'core_systems': {
                'pattern': lambda f: (f.startswith('aios_') and f.endswith('.py') and
                                     any(core_pattern in f for core_pattern in [
                                         'autonomous_supercell', 'consciousness_monitor',
                                         'enhancement_patch', 'root_neuronal',
                                         'neuronal_dendritic', 'subcellular_neuronal'
                                     ])),
                'priority': 'high', 
                'action': 'move_to_core_systems',
                'target_subcell': 'core_systems'
            },
            'keep_in_root': {
                'pattern': lambda f: f in ['CMakeLists.txt', 'AINLPCompiler.cs',
                                          'EnhancedAINLPCompiler.cs', 
                                          'aios_enhanced_connectivity_demo.py'],
                'priority': 'critical',
                'action': 'keep_active'
            }
        }
        
    def analyze_neuronal_coherence(self) -> Dict[str, Any]:
        """Analyze neuronal coherence of subcellular structure."""
        
        if not self.subcellular_path.exists():
            return {'error': f'Subcellular path not found: '
                            f'{self.subcellular_path}'}

        files = [f for f in os.listdir(self.subcellular_path)
                 if os.path.isfile(self.subcellular_path / f)]
        
        analysis = {
            'subcellular_name': self.subcellular_name,
            'total_files': len(files),
            'categories': {},
            'neuronal_metrics': {},
            'optimization_recommendations': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Categorize files using neuronal patterns
        for category, config in self.neuronal_categories.items():
            category_files = [f for f in files if config['pattern'](f)]
            analysis['categories'][category] = {
                'files': category_files,
                'count': len(category_files),
                'priority': config['priority'],
                'recommended_action': config['action']
            }
        
        # Calculate neuronal metrics
        total_files = len(files)
        if total_files > 0:
            if self.mode == 'core_engine':
                # Core Engine specific metrics
                doc_ratio = len(analysis['categories'].get('documentation_files', {'files': []})['files']) / total_files
                report_ratio = len(analysis['categories'].get('runtime_reports', {'files': []})['files']) / total_files
                bridge_ratio = len(analysis['categories'].get('bridge_implementations', {'files': []})['files']) / total_files
                tool_ratio = len(analysis['categories'].get('analysis_tools', {'files': []})['files']) / total_files
                core_ratio = len(analysis['categories'].get('core_systems', {'files': []})['files']) / total_files
                root_ratio = len(analysis['categories'].get('keep_in_root', {'files': []})['files']) / total_files
                
                analysis['neuronal_metrics'] = {
                    'documentation_ratio': doc_ratio,
                    'runtime_reports_ratio': report_ratio,
                    'bridge_implementations_ratio': bridge_ratio,
                    'analysis_tools_ratio': tool_ratio,
                    'core_systems_ratio': core_ratio,
                    'root_files_ratio': root_ratio,
                    'organization_coherence_score': self._calculate_core_coherence_score(
                        doc_ratio, report_ratio, bridge_ratio, tool_ratio, core_ratio, root_ratio
                    )
                }
                
                # Core Engine organization recommendations
                if doc_ratio > 0.15:
                    analysis['optimization_recommendations'].append({
                        'issue': 'High documentation file ratio in root',
                        'ratio': doc_ratio,
                        'action': 'move_to_documentation',
                        'priority': 'medium'
                    })
                    
                if report_ratio > 0.10:
                    analysis['optimization_recommendations'].append({
                        'issue': 'Runtime reports accumulation in root',
                        'ratio': report_ratio,
                        'action': 'move_to_runtime_intelligence',
                        'priority': 'medium'
                    })
                    
                if bridge_ratio > 0.05 and bridge_ratio < 1.0:
                    analysis['optimization_recommendations'].append({
                        'issue': 'Bridge implementations scattered',
                        'ratio': bridge_ratio,
                        'action': 'move_to_bridges',
                        'priority': 'high'
                    })
            else:
                # Subcellular specific metrics
                backup_ratio = len(analysis['categories'].get('consciousness_backups', {'files': []})['files']) / total_files
                metadata_ratio = len(analysis['categories'].get('metadata_files', {'files': []})['files']) / total_files  
                operational_ratio = len(analysis['categories'].get('operational_tools', {'files': []})['files']) / total_files
                output_ratio = len(analysis['categories'].get('analysis_outputs', {'files': []})['files']) / total_files
                
                analysis['neuronal_metrics'] = {
                    'backup_pollution_ratio': backup_ratio,
                    'metadata_saturation_ratio': metadata_ratio,
                    'operational_efficiency_ratio': operational_ratio,
                    'output_accumulation_ratio': output_ratio,
                    'neuronal_coherence_score': self._calculate_coherence_score(
                        backup_ratio, metadata_ratio, operational_ratio, output_ratio
                    )
                }
                
                # Generate optimization recommendations
                if backup_ratio > 0.3:
                    analysis['optimization_recommendations'].append({
                        'issue': 'High consciousness backup pollution',
                        'ratio': backup_ratio,
                        'action': 'tachyonic_archival',
                        'priority': 'high'
                    })
                    
                if metadata_ratio > 0.2:
                    analysis['optimization_recommendations'].append({
                        'issue': 'Metadata saturation',
                        'ratio': metadata_ratio,
                        'action': 'subcellular_organization',
                        'priority': 'medium'
                    })
                    
                if output_ratio > 0.25:
                    analysis['optimization_recommendations'].append({
                        'issue': 'Analysis output accumulation',
                        'ratio': output_ratio,
                        'action': 'tachyonic_archival',
                        'priority': 'medium'
                    })
                    
                if operational_ratio < 0.4:
                    analysis['optimization_recommendations'].append({
                        'issue': 'Low operational tool density',
                        'ratio': operational_ratio,
                        'action': 'consolidate_operational_tools',
                        'priority': 'low'
                    })
        
        return analysis
    
    def _calculate_coherence_score(self, backup_ratio: float, metadata_ratio: float, 
                                 operational_ratio: float, output_ratio: float) -> float:
        """Calculate neuronal coherence score (0-1, higher is better)."""
        
        # Optimal ratios for neuronal coherence
        optimal_operational = 0.6
        optimal_metadata = 0.15
        optimal_backup = 0.1
        optimal_output = 0.15
        
        # Calculate deviations from optimal
        operational_dev = abs(operational_ratio - optimal_operational)
        metadata_dev = abs(metadata_ratio - optimal_metadata)
        backup_dev = abs(backup_ratio - optimal_backup)
        output_dev = abs(output_ratio - optimal_output)
        
        # Weight the deviations (backup pollution is most critical)
        weighted_deviation = (
            operational_dev * 0.3 +
            metadata_dev * 0.2 +
            backup_dev * 0.4 +  # High weight for backup pollution
            output_dev * 0.1
        )
        
        # Convert to coherence score (1 - deviation, clamped to 0-1)
        coherence_score = max(0.0, 1.0 - weighted_deviation)
        return coherence_score
    
    def _calculate_core_coherence_score(self, doc_ratio: float, report_ratio: float,
                                       bridge_ratio: float, tool_ratio: float,
                                       core_ratio: float, root_ratio: float) -> float:
        """Calculate organization coherence score for Core Engine (0-1, higher is better)."""
        
        # Optimal ratios for organized Core Engine
        optimal_doc = 0.0      # Should be moved to documentation/
        optimal_report = 0.0   # Should be moved to runtime_intelligence/
        optimal_bridge = 0.0   # Should be moved to bridges/
        optimal_tool = 0.0     # Should be moved to analysis_tools/
        optimal_core = 0.0     # Should be moved to core_systems/
        optimal_root = 0.15    # Only essential files in root
        
        # Calculate deviations from optimal (organized state)
        doc_dev = abs(doc_ratio - optimal_doc)
        report_dev = abs(report_ratio - optimal_report)
        bridge_dev = abs(bridge_ratio - optimal_bridge)
        tool_dev = abs(tool_ratio - optimal_tool)
        core_dev = abs(core_ratio - optimal_core)
        root_dev = abs(root_ratio - optimal_root)
        
        # Weight the deviations (disorganization in root is critical)
        weighted_deviation = (
            doc_dev * 0.2 +
            report_dev * 0.15 +
            bridge_dev * 0.25 +    # Bridges are critical
            tool_dev * 0.15 +
            core_dev * 0.15 +
            root_dev * 0.1
        )
        
        # Convert to coherence score (1 - deviation, clamped to 0-1)
        coherence_score = max(0.0, 1.0 - weighted_deviation)
        return coherence_score
    
    def create_tachyonic_archive_structure(self) -> Path:
        """Create tachyonic archive structure for consciousness backups and outputs."""
        
        archive_path = self.parent_path / 'tachyonic_archive' / 'subcellular_archives' / self.subcellular_name
        archive_path.mkdir(parents=True, exist_ok=True)
        
        # Create subcategory folders
        (archive_path / 'consciousness_backups').mkdir(exist_ok=True)
        (archive_path / 'analysis_outputs').mkdir(exist_ok=True)
        (archive_path / 'metadata_overflow').mkdir(exist_ok=True)
        
        return archive_path
    
    def execute_neuronal_optimization(self, dry_run: bool = False) -> Dict[str, Any]:
        """Execute neuronal optimization of subcellular structure."""
        
        analysis = self.analyze_neuronal_coherence()
        
        if 'error' in analysis:
            return analysis
        
        optimization_log = {
            'subcellular_name': self.subcellular_name,
            'pre_optimization_analysis': analysis,
            'actions_taken': [],
            'dry_run': dry_run,
            'timestamp': datetime.now().isoformat()
        }
        
        if dry_run:
            print(f" DRY RUN: Neuronal optimization for {self.subcellular_name}")
        else:
            print(f" EXECUTING: Neuronal optimization for {self.subcellular_name}")
            
        # Create tachyonic archive if needed
        archive_path = None
        archival_needed = any(rec['action'] == 'tachyonic_archival' 
                            for rec in analysis['optimization_recommendations'])
        
        if archival_needed and not dry_run:
            archive_path = self.create_tachyonic_archive_structure()
            optimization_log['actions_taken'].append({
                'action': 'created_tachyonic_archive',
                'path': str(archive_path)
            })
        
        # Process each category according to recommendations
        for category, data in analysis['categories'].items():
            if data['count'] == 0:
                continue
                
            action = data['recommended_action']
            files = data['files']
            
            print(f"   {category.upper()}: {data['count']} files -> {action}")
            
            if action == 'tachyonic_archive' and files:
                self._archive_files(files, category, archive_path, dry_run, optimization_log)
            elif action == 'subcellular_organize' and files:
                self._organize_metadata_files(files, dry_run, optimization_log)
            elif action == 'keep_active':
                print(f"     Keeping {len(files)} operational files active")
                optimization_log['actions_taken'].append({
                    'action': 'kept_active',
                    'category': category,
                    'file_count': len(files)
                })
        
        # Generate post-optimization analysis
        if not dry_run:
            post_analysis = self.analyze_neuronal_coherence()
            optimization_log['post_optimization_analysis'] = post_analysis
            
            improvement = (post_analysis['neuronal_metrics']['neuronal_coherence_score'] - 
                         analysis['neuronal_metrics']['neuronal_coherence_score'])
            optimization_log['coherence_improvement'] = improvement
            
            print(f"   Neuronal coherence improvement: {improvement:+.3f}")
        
        return optimization_log
    
    def organize_core_engine_structure(self, dry_run: bool = False) -> Dict[str, Any]:
        """Organize Core Engine files into proper subcellular structure."""
        
        if self.mode != 'core_engine':
            return {'error': 'Organizer not in core_engine mode'}
        
        print(" CORE ENGINE SUBCELLULAR ORGANIZATION")
        print("=" * 50)
        
        # Analyze current structure
        analysis = self.analyze_neuronal_coherence()
        if 'error' in analysis:
            return analysis
        
        organization_log = {
            'operation': 'core_engine_organization',
            'pre_organization_analysis': analysis,
            'actions_taken': [],
            'dry_run': dry_run,
            'timestamp': datetime.now().isoformat()
        }
        
        # Ensure subcellular directories exist
        subcell_dirs = ['documentation', 'runtime_intelligence', 'bridges', 
                       'analysis_tools', 'core_systems']
        
        for subcell in subcell_dirs:
            subcell_path = self.subcellular_path / subcell
            if not dry_run:
                subcell_path.mkdir(exist_ok=True)
                print(f" Ensured subcell: {subcell}/")
            else:
                print(f" Would ensure subcell: {subcell}/")
        
        # Process each category
        for category, data in analysis['categories'].items():
            if data['count'] == 0:
                continue
                
            action = data['recommended_action']
            files = data['files']
            target_subcell = data.get('target_subcell', None)
            
            print(f"\n {category.upper()}: {data['count']} files -> {action}")
            
            if action.startswith('move_to_') and target_subcell:
                self._move_files_to_subcell(files, target_subcell, dry_run, organization_log)
            elif action == 'keep_active':
                print(f"     Keeping {len(files)} files in root")
                organization_log['actions_taken'].append({
                    'action': 'kept_in_root',
                    'category': category,
                    'file_count': len(files)
                })
        
        # Create subcellular indexes
        if not dry_run:
            self._create_subcellular_indexes(subcell_dirs, organization_log)
        
        print(f"\n Core Engine organization {'simulated' if dry_run else 'complete'}!")
        return organization_log
    
    def _move_files_to_subcell(self, files: List[str], target_subcell: str, 
                              dry_run: bool, log: Dict[str, Any]) -> None:
        """Move files to target subcell directory."""
        
        target_path = self.subcellular_path / target_subcell
        moved_files = []
        
        for file in files:
            source = self.subcellular_path / file
            target = target_path / file
            
            if dry_run:
                print(f"     Would move: {file} → {target_subcell}/")
            else:
                try:
                    shutil.move(str(source), str(target))
                    moved_files.append(file)
                    print(f"     Moved: {file} → {target_subcell}/")
                except Exception as e:
                    print(f"      Failed to move {file}: {e}")
        
        log['actions_taken'].append({
            'action': f'moved_to_{target_subcell}',
            'files_moved': moved_files if not dry_run else files,
            'target_path': str(target_path)
        })
    
    def _create_subcellular_indexes(self, subcell_dirs: List[str], 
                                   log: Dict[str, Any]) -> None:
        """Create README.md index files for each subcell."""
        
        subcell_descriptions = {
            'documentation': 'Architecture documentation and development guidelines',
            'runtime_intelligence': 'Runtime reports, analysis data, and intelligence logs',
            'bridges': 'Dendritic bridge implementations for Core-AI connectivity',
            'analysis_tools': 'Analysis, testing, and diagnostic tools',
            'core_systems': 'Core system implementations and neuronal organizers'
        }
        
        for subcell in subcell_dirs:
            subcell_path = self.subcellular_path / subcell
            if not subcell_path.exists():
                continue
                
            # Get files in subcell
            files = [f.name for f in subcell_path.iterdir() if f.is_file()]
            
            readme_content = f"""#  {subcell.title().replace('_', ' ')} Subcell

##  Description
{subcell_descriptions.get(subcell, 'Subcellular component of AIOS Core Engine')}

##  Files ({len(files)})
"""
            
            for file_name in sorted(files):
                if file_name != "README.md":
                    readme_content += f"- `{file_name}`\n"
            
            readme_content += f"""
##  Subcellular Organization
This subcell is part of the AIOS Core Engine enhanced dendritic architecture.

**Organization Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Generated by**: AIOS Subcellular Neuronal Organizer
"""
            
            readme_path = subcell_path / "README.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print(f" Created index: {subcell}/README.md")
        
        log['actions_taken'].append({
            'action': 'created_subcellular_indexes',
            'subcells': subcell_dirs
        })

    def execute_neuronal_optimization(self, dry_run: bool = False) -> Dict[str, Any]:
        """Execute neuronal optimization of subcellular structure."""
        
        analysis = self.analyze_neuronal_coherence()
        
        if 'error' in analysis:
            return analysis
        
        optimization_log = {
            'subcellular_name': self.subcellular_name,
            'pre_optimization_analysis': analysis,
            'actions_taken': [],
            'dry_run': dry_run,
            'timestamp': datetime.now().isoformat()
        }
        
        if dry_run:
            print(f" DRY RUN: Neuronal optimization for {self.subcellular_name}")
        else:
            print(f" EXECUTING: Neuronal optimization for {self.subcellular_name}")
            
        # Create tachyonic archive if needed
        archive_path = None
        archival_needed = any(rec['action'] == 'tachyonic_archival' 
                            for rec in analysis['optimization_recommendations'])
        
        if archival_needed and not dry_run:
            archive_path = self.create_tachyonic_archive_structure()
            optimization_log['actions_taken'].append({
                'action': 'created_tachyonic_archive',
                'path': str(archive_path)
            })
        
        # Process each category according to recommendations
        for category, data in analysis['categories'].items():
            if data['count'] == 0:
                continue
                
            action = data['recommended_action']
            files = data['files']
            
            print(f"   {category.upper()}: {data['count']} files -> {action}")
            
            if action == 'tachyonic_archive' and files:
                self._archive_files(files, category, archive_path, dry_run, optimization_log)
            elif action == 'subcellular_organize' and files:
                self._organize_metadata_files(files, dry_run, optimization_log)
            elif action == 'keep_active':
                print(f"     Keeping {len(files)} operational files active")
                optimization_log['actions_taken'].append({
                    'action': 'kept_active',
                    'category': category,
                    'file_count': len(files)
                })
        
        # Generate post-optimization analysis
        if not dry_run:
            post_analysis = self.analyze_neuronal_coherence()
            optimization_log['post_optimization_analysis'] = post_analysis
            
            pre_score = analysis['neuronal_metrics']['neuronal_coherence_score']
            post_score = post_analysis['neuronal_metrics']['neuronal_coherence_score']
            improvement = post_score - pre_score
            optimization_log['coherence_improvement'] = improvement
            
            print(f"   Neuronal coherence improvement: {improvement:+.3f}")
        
        return optimization_log
    
    def _archive_files(self, files: List[str], category: str, archive_path: Path, 
                      dry_run: bool, log: Dict[str, Any]) -> None:
        """Archive files to tachyonic storage."""
        
        if dry_run:
            print(f"     Would archive {len(files)} {category} files")
            return
            
        if not archive_path:
            print(f"      Cannot archive {category} files - no archive path")
            return
        
        # Map category to archive subfolder
        subfolder_map = {
            'consciousness_backups': 'consciousness_backups',
            'analysis_outputs': 'analysis_outputs',
            'metadata_files': 'metadata_overflow'
        }
        
        subfolder = subfolder_map.get(category, 'misc')
        target_path = archive_path / subfolder
        
        archived_files = []
        for file in files:
            source = self.subcellular_path / file
            target = target_path / file
            
            try:
                shutil.move(str(source), str(target))
                archived_files.append(file)
                print(f"     Archived: {file}")
            except Exception as e:
                print(f"      Failed to archive {file}: {e}")
        
        log['actions_taken'].append({
            'action': 'tachyonic_archive',
            'category': category,
            'files_archived': archived_files,
            'archive_path': str(target_path)
        })
    
    def _organize_metadata_files(self, files: List[str], dry_run: bool, 
                               log: Dict[str, Any]) -> None:
        """Organize metadata files into subcellular structure."""
        
        if dry_run:
            print(f"     Would organize {len(files)} metadata files")
            return
        
        # Create metadata subfolder
        metadata_path = self.subcellular_path / 'metadata'
        metadata_path.mkdir(exist_ok=True)
        
        organized_files = []
        for file in files:
            if file == 'CELLULAR_METADATA.md':  # Keep core metadata in root
                continue
                
            source = self.subcellular_path / file
            target = metadata_path / file
            
            try:
                shutil.move(str(source), str(target))
                organized_files.append(file)
                print(f"     Organized: {file}")
            except Exception as e:
                print(f"      Failed to organize {file}: {e}")
        
        log['actions_taken'].append({
            'action': 'subcellular_organize',
            'category': 'metadata_files',
            'files_organized': organized_files,
            'target_path': str(metadata_path)
        })
    
    def generate_optimization_report(self, optimization_log: Dict[str, Any]) -> str:
        """Generate detailed optimization report."""
        
        report = f"""
#  SUBCELLULAR NEURONAL OPTIMIZATION REPORT

## Subcellular Unit: {optimization_log['subcellular_name']}
**Timestamp**: {optimization_log['timestamp']}
**Mode**: {'DRY RUN' if optimization_log['dry_run'] else 'EXECUTION'}

## Pre-Optimization Analysis
- **Total Files**: {optimization_log['pre_optimization_analysis']['total_files']}
- **Neuronal Coherence Score**: {optimization_log['pre_optimization_analysis']['neuronal_metrics']['neuronal_coherence_score']:.3f}

### File Categories:
"""
        
        for category, data in optimization_log['pre_optimization_analysis']['categories'].items():
            if data['count'] > 0:
                report += f"- **{category.replace('_', ' ').title()}**: {data['count']} files\n"
        
        report += f"\n### Neuronal Metrics:\n"
        metrics = optimization_log['pre_optimization_analysis']['neuronal_metrics']
        report += f"- **Backup Pollution**: {metrics['backup_pollution_ratio']:.3f}\n"
        report += f"- **Metadata Saturation**: {metrics['metadata_saturation_ratio']:.3f}\n"
        report += f"- **Operational Efficiency**: {metrics['operational_efficiency_ratio']:.3f}\n"
        
        if not optimization_log['dry_run'] and 'post_optimization_analysis' in optimization_log:
            report += f"\n## Post-Optimization Analysis\n"
            post_metrics = optimization_log['post_optimization_analysis']['neuronal_metrics']
            report += f"- **New Coherence Score**: {post_metrics['neuronal_coherence_score']:.3f}\n"
            report += f"- **Improvement**: {optimization_log['coherence_improvement']:+.3f}\n"
        
        report += f"\n## Actions Taken\n"
        for action in optimization_log['actions_taken']:
            report += f"- **{action['action'].replace('_', ' ').title()}**"
            if 'file_count' in action:
                report += f": {action['file_count']} files"
            elif 'files_archived' in action:
                report += f": {len(action['files_archived'])} files archived"
            elif 'files_organized' in action:
                report += f": {len(action['files_organized'])} files organized"
            report += "\n"
        
        return report


def main():
    """Main execution function for subcellular neuronal optimization."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='AIOS Subcellular Neuronal Organizer')
    parser.add_argument('subcellular_path', help='Path to subcellular unit or Core Engine root')
    parser.add_argument('--mode', choices=['analyze', 'optimize', 'dry-run', 'core-organize'], 
                       default='analyze', help='Operation mode')
    parser.add_argument('--type', choices=['subcellular', 'core_engine'], 
                       default='subcellular', help='Organizer type')
    parser.add_argument('--report', action='store_true', 
                       help='Generate detailed report')
    
    args = parser.parse_args()
    
    # Initialize organizer with appropriate mode
    organizer_mode = 'core_engine' if args.type == 'core_engine' else 'subcellular'
    organizer = AIOSSubcellularNeuronalOrganizer(Path(args.subcellular_path), mode=organizer_mode)
    
    if args.mode == 'core-organize':
        # Core Engine organization mode
        print(" CORE ENGINE ORGANIZATION MODE")
        dry_run = input("Run in dry-run mode? (y/N): ").lower().startswith('y')
        
        result = organizer.organize_core_engine_structure(dry_run=dry_run)
        
        if 'error' in result:
            print(f" Error: {result['error']}")
            return
        
        if args.report:
            # Generate organization report
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = f"CORE_ENGINE_ORGANIZATION_REPORT_{timestamp}.md"
            
            report_content = f"""#  CORE ENGINE ORGANIZATION REPORT

**Timestamp**: {result['timestamp']}
**Mode**: {'DRY RUN' if result['dry_run'] else 'EXECUTION'}

## Pre-Organization Analysis
- **Total Files**: {result['pre_organization_analysis']['total_files']}

## Actions Taken
"""
            for action in result['actions_taken']:
                report_content += f"- **{action['action'].replace('_', ' ').title()}**"
                if 'file_count' in action:
                    report_content += f": {action['file_count']} files"
                elif 'files_moved' in action:
                    report_content += f": {len(action['files_moved'])} files moved"
                report_content += "\n"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f" Report saved: {report_file}")
    
    elif args.mode == 'analyze':
        print(" NEURONAL ANALYSIS MODE")
        analysis = organizer.analyze_neuronal_coherence()
        
        if 'error' in analysis:
            print(f" Error: {analysis['error']}")
            return
        
        print(f"\n ANALYSIS: {analysis['subcellular_name']}")
        print("=" * 50)
        print(f"Total Files: {analysis['total_files']}")
        if 'neuronal_coherence_score' in analysis['neuronal_metrics']:
            score = analysis['neuronal_metrics']['neuronal_coherence_score']
            print(f"Neuronal Coherence Score: {score:.3f}")
        print()
        
        print(" FILE CATEGORIES:")
        for category, data in analysis['categories'].items():
            if data['count'] > 0:
                action = data['recommended_action']
                print(f"  {category.upper()}: {data['count']} files ({action})")
        print()
        
        if analysis['optimization_recommendations']:
            print("  OPTIMIZATION RECOMMENDATIONS:")
            for rec in analysis['optimization_recommendations']:
                print(f"  - {rec['issue']}: {rec['ratio']:.3f} -> {rec['action']}")
        else:
            print(" No optimization recommendations - structure is coherent")
    
    elif args.mode in ['optimize', 'dry-run']:
        dry_run = (args.mode == 'dry-run')
        optimization_log = organizer.execute_neuronal_optimization(dry_run=dry_run)
        
        if 'error' in optimization_log:
            print(f" Error: {optimization_log['error']}")
            return
        
        if args.report:
            report = organizer.generate_optimization_report(optimization_log)
            
            # Save report
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = f"SUBCELLULAR_NEURONAL_OPTIMIZATION_{organizer.subcellular_name}_{timestamp}.md"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f" Report saved: {report_file}")


if __name__ == '__main__':
    main()
