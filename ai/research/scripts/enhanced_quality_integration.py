#!/usr/bin/env python3
"""
Enhanced GitHooks Quality Integration
====================================
Location: ai/laboratory/scripts/enhanced_quality_integration.py
Purpose: Real integration between quality analysis and GitHooks orchestration
Architecture: LABORATORY -> CYTOPLASM -> TRANSPORT intercellular communication

This creates genuine data flow between emoji detection, quality analysis,
and GitHooks orchestration with real supercell communication.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add AIOS paths
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent.parent))

from emoji_detector import EmojiDetector
from transport.intercellular.enhanced_cellular_communication import (
    get_cellular_bridge, SupercellType, InterCellularMessage
)


class QualityAnalysisEngine:
    """Enhanced quality analysis with real supercell integration"""
    
    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path(__file__).parent.parent.parent.parent
        self.cellular_bridge = get_cellular_bridge()
        self.emoji_detector = EmojiDetector(self.workspace_root)
        
    def perform_comprehensive_quality_scan(self) -> Dict[str, Any]:
        """Perform comprehensive quality analysis with supercell integration"""
        print("LABORATORY: Starting comprehensive quality analysis...")
        
        # Update supercell state
        self.cellular_bridge.update_supercell_state(
            SupercellType.LABORATORY,
            "analyzing",
            ["quality_scan", "emoji_detection"],
            {"scan_start": datetime.now().isoformat()}
        )
        
        # Emoji analysis
        emoji_results = self._analyze_emoji_usage()
        
        # File structure analysis 
        structure_results = self._analyze_file_structure()
        
        # Integration quality analysis
        integration_results = self._analyze_integration_quality()
        
        # Combine results
        comprehensive_results = {
            "analysis_timestamp": datetime.now().isoformat(),
            "emoji_analysis": emoji_results,
            "structure_analysis": structure_results,
            "integration_analysis": integration_results,
            "overall_quality_score": self._calculate_quality_score(
                emoji_results, structure_results, integration_results
            )
        }
        
        # Send results through supercell communication
        self._communicate_results(comprehensive_results)
        
        return comprehensive_results
    
    def _analyze_emoji_usage(self) -> Dict[str, Any]:
        """Analyze emoji usage across the system"""
        print("LABORATORY: Analyzing emoji usage patterns...")
        
        # Scan GitHooks directory
        githooks_path = self.workspace_root / '.githooks'
        emoji_matches = self.emoji_detector.scan_directory(githooks_path)
        
        # Analyze patterns
        emoji_by_file = {}
        emoji_counts = {}
        
        for match in emoji_matches:
            # Group by file
            rel_path = str(Path(match.file_path).relative_to(self.workspace_root))
            if rel_path not in emoji_by_file:
                emoji_by_file[rel_path] = []
            emoji_by_file[rel_path].append({
                'line': match.line_number,
                'emoji': match.emoji,
                'context': match.context.strip()
            })
            
            # Count emoji types
            emoji_counts[match.emoji] = emoji_counts.get(match.emoji, 0) + 1
        
        return {
            "total_emojis": len(emoji_matches),
            "files_with_emojis": len(emoji_by_file),
            "emoji_by_file": emoji_by_file,
            "emoji_frequency": dict(sorted(emoji_counts.items(), 
                                         key=lambda x: x[1], reverse=True)),
            "cleanup_priority": self._calculate_emoji_cleanup_priority(emoji_counts)
        }
    
    def _analyze_file_structure(self) -> Dict[str, Any]:
        """Analyze file structure and organization"""
        print("LABORATORY: Analyzing file structure...")
        
        githooks_path = self.workspace_root / '.githooks'
        
        # Count files by type
        file_counts = {}
        supercell_structure = {}
        
        for file_path in githooks_path.rglob('*'):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                file_counts[ext] = file_counts.get(ext, 0) + 1
                
                # Check supercell organization
                path_parts = file_path.relative_to(githooks_path).parts
                if len(path_parts) > 1 and path_parts[0] == 'supercells':
                    if len(path_parts) > 2:
                        supercell = path_parts[1]
                        if supercell not in supercell_structure:
                            supercell_structure[supercell] = 0
                        supercell_structure[supercell] += 1
        
        return {
            "total_files": sum(file_counts.values()),
            "file_types": file_counts,
            "supercell_organization": supercell_structure,
            "structure_score": len(supercell_structure) / 6.0  # 6 expected supercells
        }
    
    def _analyze_integration_quality(self) -> Dict[str, Any]:
        """Analyze integration quality between components"""
        print("LABORATORY: Analyzing integration quality...")
        
        # Check if orchestrator exists and can import
        orchestrator_path = self.workspace_root / 'ai' / 'cytoplasm' / 'scripts' / 'githook_orchestrator.py'
        transport_path = self.workspace_root / 'ai' / 'transport' / 'intercellular'
        
        integration_issues = []
        
        if not orchestrator_path.exists():
            integration_issues.append("GitHook orchestrator missing")
        
        if not transport_path.exists():
            integration_issues.append("Transport supercell missing")
        
        # Check for stub vs real implementations
        stub_files = []
        for stub_file in ['aios_runtime.py', 'cellular_communication.py']:
            stub_path = transport_path / stub_file
            if stub_path.exists():
                try:
                    content = stub_path.read_text()
                    if 'print(' in content and 'stub' in content.lower():
                        stub_files.append(stub_file)
                except:
                    pass
        
        return {
            "integration_issues": integration_issues,
            "stub_implementations": stub_files,
            "integration_score": max(0, 1.0 - (len(integration_issues) + len(stub_files)) * 0.2)
        }
    
    def _calculate_emoji_cleanup_priority(self, emoji_counts: Dict[str, int]) -> List[Dict[str, Any]]:
        """Calculate cleanup priority for emojis"""
        priorities = []
        
        # High priority emojis (most common or problematic)
        high_priority = ['', '', '', '', '', '', '']
        
        for emoji, count in emoji_counts.items():
            priority_level = "HIGH" if emoji in high_priority else "MEDIUM"
            if count == 1:
                priority_level = "LOW"
                
            priorities.append({
                "emoji": emoji,
                "count": count,
                "priority": priority_level,
                "suggested_replacement": self._get_emoji_replacement(emoji)
            })
        
        return sorted(priorities, key=lambda x: (x['priority'] == 'HIGH', x['count']), reverse=True)
    
    def _get_emoji_replacement(self, emoji: str) -> str:
        """Get suggested replacement for emoji"""
        replacements = {
            '': '[PASS]',
            '': '[FAIL]', 
            '': 'SUPERCELL:',
            '': 'TARGET:',
            '': 'LAUNCH:',
            '': 'METRICS:',
            '': 'ANALYSIS:',
            '': 'PROCESS:',
            '': 'CORE:',
            '': 'AI:',
            '': 'TOOL:',
            '': 'FOLDER:',
            '': 'NOTE:',
            '': 'SUCCESS:',
            '': 'WARNING:'
        }
        return replacements.get(emoji, f'[{emoji}]')
    
    def _calculate_quality_score(self, emoji_results: Dict, structure_results: Dict, 
                                integration_results: Dict) -> Dict[str, Any]:
        """Calculate overall quality score"""
        # Emoji penalty (more emojis = lower score)
        emoji_penalty = min(emoji_results["total_emojis"] / 100.0, 1.0)
        emoji_score = max(0, 1.0 - emoji_penalty)
        
        # Structure score
        structure_score = structure_results["structure_score"]
        
        # Integration score
        integration_score = integration_results["integration_score"]
        
        # Overall weighted score
        overall_score = (emoji_score * 0.3 + structure_score * 0.3 + integration_score * 0.4)
        
        return {
            "emoji_score": round(emoji_score, 3),
            "structure_score": round(structure_score, 3),
            "integration_score": round(integration_score, 3),
            "overall_score": round(overall_score, 3),
            "grade": self._score_to_grade(overall_score)
        }
    
    def _score_to_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 0.9:
            return "A"
        elif score >= 0.8:
            return "B"
        elif score >= 0.7:
            return "C"
        elif score >= 0.6:
            return "D"
        else:
            return "F"
    
    def _communicate_results(self, results: Dict[str, Any]):
        """Send results through supercell communication"""
        print("LABORATORY: Communicating results to other supercells...")
        
        # Send to CYTOPLASM for orchestration decisions
        cytoplasm_message = InterCellularMessage(
            source_supercell=SupercellType.LABORATORY,
            target_supercell=SupercellType.CYTOPLASM,
            message_type="quality_analysis_complete",
            data={
                "analysis_results": results,
                "recommendations": self._generate_recommendations(results)
            },
            timestamp=datetime.now(),
            correlation_id=f"quality_analysis_{int(datetime.now().timestamp())}"
        )
        self.cellular_bridge.send_message(cytoplasm_message)
        
        # Send to INFORMATION_STORAGE for persistence
        storage_message = InterCellularMessage(
            source_supercell=SupercellType.LABORATORY,
            target_supercell=SupercellType.INFORMATION_STORAGE,
            message_type="store_analysis_results",
            data=results,
            timestamp=datetime.now(),
            correlation_id=f"store_analysis_{int(datetime.now().timestamp())}"
        )
        self.cellular_bridge.send_message(storage_message)
        
        # Update LABORATORY state
        self.cellular_bridge.update_supercell_state(
            SupercellType.LABORATORY,
            "analysis_complete",
            ["quality_analysis_complete"],
            {"latest_analysis": results}
        )
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        emoji_count = results["emoji_analysis"]["total_emojis"]
        if emoji_count > 50:
            recommendations.append(f"HIGH PRIORITY: Remove {emoji_count} emoji characters causing encoding issues")
        elif emoji_count > 10:
            recommendations.append(f"MEDIUM PRIORITY: Clean up {emoji_count} emoji characters")
        
        structure_score = results["structure_analysis"]["structure_score"]
        if structure_score < 0.8:
            recommendations.append("Improve supercell file organization")
        
        integration_score = results["integration_analysis"]["integration_score"]
        if integration_score < 0.7:
            recommendations.append("Replace stub implementations with real functionality")
        
        overall_score = results["overall_quality_score"]["overall_score"]
        if overall_score < 0.6:
            recommendations.append("CRITICAL: System quality requires immediate attention")
        
        return recommendations


def main():
    """Main execution for enhanced quality integration"""
    print("Enhanced GitHooks Quality Integration")
    print("===================================")
    
    engine = QualityAnalysisEngine()
    results = engine.perform_comprehensive_quality_scan()
    
    # Print summary
    print(f"\nQUALITY ANALYSIS COMPLETE")
    print(f"========================")
    print(f"Overall Grade: {results['overall_quality_score']['grade']}")
    print(f"Overall Score: {results['overall_quality_score']['overall_score']:.3f}")
    print(f"Emojis Found: {results['emoji_analysis']['total_emojis']}")
    print(f"Files Affected: {results['emoji_analysis']['files_with_emojis']}")
    
    print(f"\nRECOMMENDATIONS:")
    for i, rec in enumerate(results.get('recommendations', []), 1):
        print(f"{i}. {rec}")
    
    # Save detailed results
    results_file = Path("c:/dev/AIOS/tachyonic/archive/quality_reports/quality_analysis_results.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results saved to: {results_file}")
    
    return results['emoji_analysis']['total_emojis']


if __name__ == '__main__':
    sys.exit(main())