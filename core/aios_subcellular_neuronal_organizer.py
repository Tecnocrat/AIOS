#!/usr/bin/env python3
"""
🧬 AIOS Subcellular Neuronal Organizer
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
    """Advanced neuronal organizer for subcellular units."""

    def __init__(self, subcellular_path: Path):
        self.subcellular_path = Path(subcellular_path)
        self.subcellular_name = self.subcellular_path.name
        self.parent_path = self.subcellular_path.parent

        # Neuronal categorization patterns
        self.neuronal_categories = {
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
            backup_ratio = len(analysis['categories']['consciousness_backups']['files']) / total_files
            metadata_ratio = len(analysis['categories']['metadata_files']['files']) / total_files  
            operational_ratio = len(analysis['categories']['operational_tools']['files']) / total_files
            output_ratio = len(analysis['categories']['analysis_outputs']['files']) / total_files
            
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
            print(f"🧬 DRY RUN: Neuronal optimization for {self.subcellular_name}")
        else:
            print(f"🧬 EXECUTING: Neuronal optimization for {self.subcellular_name}")
            
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
            
            print(f"  📁 {category.upper()}: {data['count']} files -> {action}")
            
            if action == 'tachyonic_archive' and files:
                self._archive_files(files, category, archive_path, dry_run, optimization_log)
            elif action == 'subcellular_organize' and files:
                self._organize_metadata_files(files, dry_run, optimization_log)
            elif action == 'keep_active':
                print(f"    ✅ Keeping {len(files)} operational files active")
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
            
            print(f"  🧠 Neuronal coherence improvement: {improvement:+.3f}")
        
        return optimization_log
    
    def _archive_files(self, files: List[str], category: str, archive_path: Path, 
                      dry_run: bool, log: Dict[str, Any]) -> None:
        """Archive files to tachyonic storage."""
        
        if dry_run:
            print(f"    📦 Would archive {len(files)} {category} files")
            return
            
        if not archive_path:
            print(f"    ⚠️  Cannot archive {category} files - no archive path")
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
                print(f"    📦 Archived: {file}")
            except Exception as e:
                print(f"    ⚠️  Failed to archive {file}: {e}")
        
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
            print(f"    📋 Would organize {len(files)} metadata files")
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
                print(f"    📋 Organized: {file}")
            except Exception as e:
                print(f"    ⚠️  Failed to organize {file}: {e}")
        
        log['actions_taken'].append({
            'action': 'subcellular_organize',
            'category': 'metadata_files',
            'files_organized': organized_files,
            'target_path': str(metadata_path)
        })
    
    def generate_optimization_report(self, optimization_log: Dict[str, Any]) -> str:
        """Generate detailed optimization report."""
        
        report = f"""
# 🧬 SUBCELLULAR NEURONAL OPTIMIZATION REPORT

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
    parser.add_argument('subcellular_path', help='Path to subcellular unit (e.g., analysis_tools)')
    parser.add_argument('--mode', choices=['analyze', 'optimize', 'dry-run'], 
                       default='analyze', help='Operation mode')
    parser.add_argument('--report', action='store_true', 
                       help='Generate detailed report')
    
    args = parser.parse_args()
    
    organizer = AIOSSubcellularNeuronalOrganizer(Path(args.subcellular_path))
    
    if args.mode == 'analyze':
        print("🧬 NEURONAL ANALYSIS MODE")
        analysis = organizer.analyze_neuronal_coherence()
        
        if 'error' in analysis:
            print(f"❌ Error: {analysis['error']}")
            return
        
        print(f"\n📊 SUBCELLULAR ANALYSIS: {analysis['subcellular_name']}")
        print("=" * 50)
        print(f"Total Files: {analysis['total_files']}")
        print(f"Neuronal Coherence Score: {analysis['neuronal_metrics']['neuronal_coherence_score']:.3f}")
        print()
        
        print("📁 FILE CATEGORIES:")
        for category, data in analysis['categories'].items():
            if data['count'] > 0:
                print(f"  {category.upper()}: {data['count']} files ({data['recommended_action']})")
        print()
        
        if analysis['optimization_recommendations']:
            print("⚠️  OPTIMIZATION RECOMMENDATIONS:")
            for rec in analysis['optimization_recommendations']:
                print(f"  - {rec['issue']}: {rec['ratio']:.3f} -> {rec['action']}")
        else:
            print("✅ No optimization recommendations - neuronal structure is coherent")
    
    elif args.mode in ['optimize', 'dry-run']:
        dry_run = (args.mode == 'dry-run')
        optimization_log = organizer.execute_neuronal_optimization(dry_run=dry_run)
        
        if 'error' in optimization_log:
            print(f"❌ Error: {optimization_log['error']}")
            return
        
        if args.report:
            report = organizer.generate_optimization_report(optimization_log)
            
            # Save report
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = f"SUBCELLULAR_NEURONAL_OPTIMIZATION_{organizer.subcellular_name}_{timestamp}.md"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"📋 Report saved: {report_file}")


if __name__ == '__main__':
    main()
