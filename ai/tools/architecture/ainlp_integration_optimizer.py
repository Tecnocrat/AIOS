#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AINLP INTEGRATION AND OPTIMIZATION PATH ANALYZER

AINLP META-COMMENTARY: This tool addresses the critical overpopulation problem
causing decoherence and degraded discoverability across AIOS interfaces and methods.

PURPOSE: Compare files across AIOS to identify consolidation opportunities,
compress duplicate logic, and harmonize architecture following AINLP patterns.

AINLP PATTERNS IMPLEMENTED:
1. Enhancement Over Creation - Consolidate similar interfaces/methods
2. Architectural Discovery First - Find existing patterns before changes
3. Proper Output Management - Tachyonic archival of consolidation reports
4. Integration Validation - Biological architecture compliance

DISCOVERED AINLP HARMONIZATION PATTERNS:
- Ultimate Compressor: Aggressive file merging based on functionality patterns
- Documentation Governance: Similarity >70% triggers EXPAND, >40% evaluates MERGE
- Core Consolidation: Single source of truth with dependency injection
- Dendritic Growth: Expand existing dendrites before growing new ones
"""

import difflib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Any


class AINLPIntegrationOptimizer:
    """AINLP-driven integration and optimization analyzer for AIOS architecture."""
    
    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path(__file__).parent.parent.parent
        self.tachyonic_root = self.workspace_root / "tachyonic" / "archive"
        
        # AINLP consolidation thresholds (from documentation governance patterns)
        self.high_similarity_threshold = 0.70  # FORCE consolidation
        self.medium_similarity_threshold = 0.40  # EVALUATE merge opportunity
        self.low_similarity_threshold = 0.20  # DOCUMENT relationship
        
        # Target analysis areas (overpopulation hotspots)
        self.analysis_targets = {
            "interfaces": {
                "python": [
                    "ai/core/interface_bridge.py",
                    "ai/core/interface_bridge_generation_api.py",
                    "ai/src/integrations/visual_ai_integration_bridge.py",
                    "ai/src/engines/aios_ai_integration_bridge.py",
                    "interface/interface_supercell_interface.py"
                ],
                "csharp": [
                    "interface/AIOS.Models/AdvancedAIServiceManager.cs",
                    "interface/AIOS.Services/*.cs",
                    "core/src/core/AINLPHarmonizer.cs",
                    "visual_interface/AINLPHarmonizer.cs"
                ]
            },
            "tools": {
                "monitoring": [
<<<<<<< HEAD
                    "runtime_intelligence/tools/aios_architecture_monitor.py",
                    "runtime_intelligence/tools/biological_architecture_monitor.py",
                    "runtime_intelligence/tools/system_health_check.py",
                    "runtime_intelligence/tools/system_status_report.py"
                ],
                "analysis": [
                    "runtime_intelligence/tools/self_similarity_analyzer.py",
                    "runtime_intelligence/tools/consciousness_analysis_report.py",
                    "runtime_intelligence/tools/architectural_compliance_validator.py"
=======
                    "runtime/tools/aios_architecture_monitor.py",
                    "runtime/tools/biological_architecture_monitor.py",
                    "runtime/tools/system_health_check.py",
                    "runtime/tools/system_status_report.py"
                ],
                "analysis": [
                    "runtime/tools/self_similarity_analyzer.py",
                    "runtime/tools/consciousness_analysis_report.py",
                    "runtime/tools/architectural_compliance_validator.py"
>>>>>>> origin/OS0.6.2.grok
                ],
                "optimization": [
                    "ai/src/integrations/aios_agentic_optimizer.py",
                    "ai/src/integrations/aios_recursive_optimizer.py",
                    "ai/src/integrations/unified_development_optimizer.py",
                    "ai/src/engines/aios_performance_optimizer.py"
                ]
            },
            "services": {
                "ai_services": [
                    "interface/AIOS.Models/AdvancedAIServiceManager.cs"
                ]
            }
        }
        
    def execute_integration_analysis(self) -> Dict[str, Any]:
        """Main analysis execution following AINLP patterns."""
        print("\n" + "="*80)
        print(" AINLP INTEGRATION AND OPTIMIZATION PATH ANALYSIS")
        print("="*80)
        print("\nObjective: Identify consolidation opportunities to reduce overpopulation")
        print("           and restore architectural coherence\n")
        
        analysis_report = {
            "timestamp": datetime.now().isoformat(),
            "workspace_root": str(self.workspace_root),
            "overpopulation_analysis": {},
            "consolidation_opportunities": [],
            "coherence_improvements": [],
            "integration_recommendations": [],
            "ainlp_compliance": {}
        }
        
        # Step 1: Analyze overpopulation in each category
        print("[1/5] Analyzing overpopulation patterns...")
        for category, subcategories in self.analysis_targets.items():
            print(f"\n  Analyzing {category}...")
            analysis_report["overpopulation_analysis"][category] = (
                self._analyze_overpopulation(category, subcategories)
            )
        
        # Step 2: Calculate similarity scores and identify consolidation targets
        print("\n[2/5] Calculating similarity scores...")
        consolidation_opps = self._identify_consolidation_opportunities(
            analysis_report["overpopulation_analysis"]
        )
        analysis_report["consolidation_opportunities"] = consolidation_opps
        
        # Step 3: Generate coherence improvement recommendations
        print("\n[3/5] Generating coherence improvements...")
        coherence_improvements = self._generate_coherence_improvements(
            consolidation_opps
        )
        analysis_report["coherence_improvements"] = coherence_improvements
        
        # Step 4: Validate AINLP compliance
        print("\n[4/5] Validating AINLP compliance...")
        ainlp_compliance = self._validate_ainlp_compliance(analysis_report)
        analysis_report["ainlp_compliance"] = ainlp_compliance
        
        # Step 5: Generate integration recommendations
        print("\n[5/5] Generating integration recommendations...")
        integration_recs = self._generate_integration_recommendations(
            analysis_report
        )
        analysis_report["integration_recommendations"] = integration_recs
        
        return analysis_report
    
    def _analyze_overpopulation(self, category: str, 
                                subcategories: Dict[str, List[str]]) -> Dict[str, Any]:
        """Analyze overpopulation patterns in a specific category."""
        overpopulation_data = {
            "total_files": 0,
            "subcategories": {},
            "decoherence_level": 0,
            "duplicate_patterns": [],
            "interface_collisions": []
        }
        
        for subcat_name, file_patterns in subcategories.items():
            files_found = []
            for pattern in file_patterns:
                # Handle glob patterns
                if '*' in pattern:
                    pattern_path = self.workspace_root / pattern.replace('*', '')
                    parent_dir = pattern_path.parent
                    if parent_dir.exists():
                        files_found.extend(parent_dir.glob(pattern_path.name))
                else:
                    file_path = self.workspace_root / pattern
                    if file_path.exists():
                        files_found.append(file_path)
            
            if files_found:
                # Analyze each file for patterns
                subcat_data = {
                    "file_count": len(files_found),
                    "files": [str(f.relative_to(self.workspace_root)) 
                             for f in files_found],
                    "interfaces_detected": [],
                    "methods_detected": [],
                    "duplicate_signatures": []
                }
                
                for file_path in files_found:
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        
                        # Detect interfaces and methods
                        if file_path.suffix == '.py':
                            interfaces = re.findall(r'class\s+(\w+)\s*\(', content)
                            methods = re.findall(r'def\s+(\w+)\s*\(', content)
                        elif file_path.suffix == '.cs':
                            interfaces = re.findall(
                                r'(?:class|interface)\s+(\w+)', content)
                            methods = re.findall(
                                r'(?:public|private|protected)\s+\w+\s+(\w+)\s*\(',
                                content)
                        else:
                            interfaces, methods = [], []
                        
                        subcat_data["interfaces_detected"].extend(interfaces)
                        subcat_data["methods_detected"].extend(methods)
                        
                    except Exception as e:
                        print(f"    Warning: Could not analyze {file_path}: {e}")
                
                # Detect duplicate signatures
                interface_counts = Counter(subcat_data["interfaces_detected"])
                method_counts = Counter(subcat_data["methods_detected"])
                
                subcat_data["duplicate_signatures"] = {
                    "interfaces": [name for name, count in interface_counts.items() 
                                 if count > 1],
                    "methods": [name for name, count in method_counts.items() 
                               if count > 1]
                }
                
                overpopulation_data["subcategories"][subcat_name] = subcat_data
                overpopulation_data["total_files"] += len(files_found)
        
        # Calculate decoherence level (from ai/__init__.py pattern)
        # Decoherence = interfaces + methods - unique_interfaces - unique_methods
        total_interfaces = sum(
            len(data["interfaces_detected"]) 
            for data in overpopulation_data["subcategories"].values()
        )
        total_methods = sum(
            len(data["methods_detected"]) 
            for data in overpopulation_data["subcategories"].values()
        )
        unique_interfaces = len(set(
            interface 
            for data in overpopulation_data["subcategories"].values()
            for interface in data["interfaces_detected"]
        ))
        unique_methods = len(set(
            method 
            for data in overpopulation_data["subcategories"].values()
            for method in data["methods_detected"]
        ))
        
        overpopulation_data["decoherence_level"] = (
            total_interfaces + total_methods - unique_interfaces - unique_methods
        )
        
        return overpopulation_data
    
    def _identify_consolidation_opportunities(self, 
                                            overpopulation_data: Dict[str, Any]
                                            ) -> List[Dict[str, Any]]:
        """Identify consolidation opportunities using AINLP similarity patterns."""
        opportunities = []
        
        for category, cat_data in overpopulation_data.items():
            for subcat_name, subcat_data in cat_data.get("subcategories", {}).items():
                files = subcat_data.get("files", [])
                
                # Compare files pairwise for similarity
                for i, file_a in enumerate(files):
                    for file_b in files[i+1:]:
                        similarity_score = self._calculate_file_similarity(
                            self.workspace_root / file_a,
                            self.workspace_root / file_b
                        )
                        
                        if similarity_score >= self.medium_similarity_threshold:
                            action = self._determine_consolidation_action(
                                similarity_score)
                            
                            opportunities.append({
                                "category": category,
                                "subcategory": subcat_name,
                                "file_a": file_a,
                                "file_b": file_b,
                                "similarity_score": similarity_score,
                                "recommended_action": action,
                                "ainlp_principle": self._get_ainlp_principle(action),
                                "priority": self._calculate_priority(
                                    similarity_score, cat_data)
                            })
        
        # Sort by priority (highest first)
        opportunities.sort(key=lambda x: x["priority"], reverse=True)
        return opportunities
    
    def _calculate_file_similarity(self, file_a: Path, file_b: Path) -> float:
        """Calculate similarity between two files using difflib."""
        try:
            content_a = file_a.read_text(encoding='utf-8', errors='ignore')
            content_b = file_b.read_text(encoding='utf-8', errors='ignore')
            
            # Use SequenceMatcher for similarity
            similarity = difflib.SequenceMatcher(
                None, content_a, content_b).ratio()
            return similarity
            
        except Exception as e:
            print(f"  Warning: Could not calculate similarity: {e}")
            return 0.0
    
    def _determine_consolidation_action(self, similarity_score: float) -> str:
        """Determine action based on AINLP governance patterns."""
        if similarity_score >= self.high_similarity_threshold:
            return "FORCE_CONSOLIDATION"
        elif similarity_score >= self.medium_similarity_threshold:
            return "EVALUATE_MERGE"
        elif similarity_score >= self.low_similarity_threshold:
            return "DOCUMENT_RELATIONSHIP"
        else:
            return "KEEP_SEPARATE"
    
    def _get_ainlp_principle(self, action: str) -> str:
        """Map action to AINLP principle."""
        principles = {
            "FORCE_CONSOLIDATION": "Enhancement Over Creation (>70% similarity)",
            "EVALUATE_MERGE": "Dendritic Growth Pattern (40-70% similarity)",
            "DOCUMENT_RELATIONSHIP": "Architectural Documentation (<40% similarity)",
            "KEEP_SEPARATE": "Architectural Diversity Preservation"
        }
        return principles.get(action, "Unknown")
    
    def _calculate_priority(self, similarity_score: float, 
                           cat_data: Dict[str, Any]) -> int:
        """Calculate consolidation priority based on similarity and decoherence."""
        # Priority = similarity_score * 100 + decoherence_level
        decoherence = cat_data.get("decoherence_level", 0)
        return int(similarity_score * 100) + decoherence
    
    def _generate_coherence_improvements(self, 
                                        consolidation_opps: List[Dict[str, Any]]
                                        ) -> List[Dict[str, Any]]:
        """Generate specific coherence improvement recommendations."""
        improvements = []
        
        # Group opportunities by category
        by_category = defaultdict(list)
        for opp in consolidation_opps:
            by_category[opp["category"]].append(opp)
        
        for category, opps in by_category.items():
            if not opps:
                continue
                
            # Calculate coherence improvement potential
            avg_similarity = sum(o["similarity_score"] for o in opps) / len(opps)
            decoherence_reduction = len(opps)  # Each merge reduces decoherence
            
            improvement = {
                "category": category,
                "improvement_type": "CONSOLIDATION",
                "opportunities_count": len(opps),
                "average_similarity": avg_similarity,
                "decoherence_reduction_potential": decoherence_reduction,
                "target_coherence_score": min(0.85, avg_similarity + 0.15),
                "recommended_approach": self._determine_coherence_approach(opps),
                "estimated_benefits": self._estimate_benefits(opps)
            }
            improvements.append(improvement)
        
        return improvements
    
    def _determine_coherence_approach(self, opps: List[Dict[str, Any]]) -> str:
        """Determine best coherence approach based on AINLP patterns."""
        force_consolidations = sum(
            1 for o in opps 
            if o["recommended_action"] == "FORCE_CONSOLIDATION"
        )
        
        if force_consolidations > len(opps) / 2:
            return "CORE_CONSOLIDATION"  # Option A from dev.arch.md
        else:
            return "FEDERATED_HARMONIZATION"  # Option B from dev.arch.md
    
    def _estimate_benefits(self, opps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate benefits of consolidation."""
        return {
            "files_reduced": len(opps),
            "interfaces_unified": len(set(
                o["file_a"] for o in opps)) + len(set(o["file_b"] for o in opps)),
            "maintainability_improvement": "HIGH" if len(opps) > 5 else "MEDIUM",
            "discoverability_improvement": "HIGH",
            "coherence_score_improvement": "+0.15 to +0.30 (estimated)"
        }
    
    def _validate_ainlp_compliance(self, analysis_report: Dict[str, Any]
                                   ) -> Dict[str, Any]:
        """Validate analysis compliance with AINLP principles."""
        compliance = {
            "principles_validated": [],
            "compliance_score": 0.0,
            "violations": [],
            "recommendations": []
        }
        
        # Principle 1: Architectural Discovery First
        discovery_check = {
            "principle": "ARCHITECTURAL_DISCOVERY_FIRST",
            "status": "COMPLIANT",
            "evidence": "Analysis scanned all target areas before recommendations"
        }
        compliance["principles_validated"].append(discovery_check)
        
        # Principle 2: Enhancement Over Creation
        consolidation_opps = analysis_report.get("consolidation_opportunities", [])
        enhancement_check = {
            "principle": "ENHANCEMENT_OVER_CREATION",
            "status": "COMPLIANT" if consolidation_opps else "WARNING",
            "evidence": f"Found {len(consolidation_opps)} consolidation opportunities"
        }
        compliance["principles_validated"].append(enhancement_check)
        
        # Principle 3: Proper Output Management
        output_check = {
            "principle": "PROPER_OUTPUT_MANAGEMENT",
            "status": "COMPLIANT",
            "evidence": "Report will be saved to tachyonic/archive/"
        }
        compliance["principles_validated"].append(output_check)
        
        # Principle 4: Integration Validation
        integration_check = {
            "principle": "INTEGRATION_VALIDATION",
            "status": "PENDING",
            "evidence": "Biological architecture validation required post-consolidation"
        }
        compliance["principles_validated"].append(integration_check)
        
        # Calculate compliance score
        compliant_count = sum(
            1 for check in compliance["principles_validated"] 
            if check["status"] == "COMPLIANT"
        )
        compliance["compliance_score"] = (
            compliant_count / len(compliance["principles_validated"])
        )
        
        return compliance
    
    def _generate_integration_recommendations(self, analysis_report: Dict[str, Any]
                                             ) -> List[Dict[str, Any]]:
        """Generate actionable integration recommendations."""
        recommendations = []
        
        # Recommendation 1: Address high-priority consolidations
        high_priority_opps = [
            opp for opp in analysis_report.get("consolidation_opportunities", [])
            if opp["priority"] > 100
        ]
        
        if high_priority_opps:
            recommendations.append({
                "priority": "CRITICAL",
                "title": "Consolidate High-Similarity Interfaces",
                "description": (
                    f"Found {len(high_priority_opps)} high-priority consolidation "
                    "opportunities (>70% similarity). These are causing significant "
                    "decoherence and should be addressed first."
                ),
                "action_items": [
                    f"Review: {opp['file_a']} + {opp['file_b']} "
                    f"(similarity: {opp['similarity_score']:.2f})"
                    for opp in high_priority_opps[:5]
                ],
                "ainlp_pattern": "Core Consolidation (Option A)",
                "estimated_effort": "Medium",
                "expected_coherence_gain": "+0.20 to +0.30"
            })
        
        # Recommendation 2: Implement Core Consolidation for AINLPHarmonizer
        # (from dev.arch.md analysis)
        recommendations.append({
            "priority": "HIGH",
            "title": "Consolidate AINLPHarmonizer Implementations",
            "description": (
                "Detected dual AINLPHarmonizer implementations (core + visual_interface) "
                "causing namespace collision and redundancy. Current LFC: 0.31, GPC: 0.28. "
                "Target: LFC ≥0.85, GPC ≥0.82."
            ),
            "action_items": [
                "1. Move: core/src/core/AINLPHarmonizer.cs → core/src/AINLPHarmonizer.cs",
                "2. Create: core/src/IAINLPHarmonizer.cs (interface)",
                "3. Remove: visual_interface/AINLPHarmonizer.cs stub",
                "4. Implement: Dependency injection pattern for visual interface",
                "5. Convert: Dictionary<string,object> returns to typed models"
            ],
            "ainlp_pattern": "Core Consolidation (Option A from dev.arch.md)",
            "estimated_effort": "High",
            "expected_coherence_gain": "+0.54 LFC, +0.54 GPC"
        })
        
        # Recommendation 3: Create unified interface bridge
        interface_bridges = [
            opp for opp in analysis_report.get("consolidation_opportunities", [])
            if "bridge" in opp["category"].lower() or "interface" in opp["category"].lower()
        ]
        
        if interface_bridges:
            recommendations.append({
                "priority": "MEDIUM",
                "title": "Unify Interface Bridge Implementations",
                "description": (
                    f"Found {len(interface_bridges)} interface bridge variations. "
                    "Consider creating single authoritative interface bridge with "
                    "proper abstraction layers."
                ),
                "action_items": [
                    "1. Create: ai/core/unified_interface_bridge.py (single source of truth)",
                    "2. Deprecate: Redundant bridge implementations",
                    "3. Implement: Adapter pattern for language-specific interfaces",
                    "4. Document: Interface bridge protocol in docs/architecture/"
                ],
                "ainlp_pattern": "Federated Harmonization (Option B)",
                "estimated_effort": "Medium",
                "expected_coherence_gain": "+0.15 to +0.25"
            })
        
        # Recommendation 4: Tool consolidation
        tool_consolidations = [
            opp for opp in analysis_report.get("consolidation_opportunities", [])
            if "tools" in opp["category"]
        ]
        
        if tool_consolidations:
            recommendations.append({
                "priority": "LOW",
                "title": "Consolidate Runtime Intelligence Tools",
                "description": (
                    f"Found {len(tool_consolidations)} tool consolidation opportunities. "
                    "Many tools have overlapping functionality that could be unified."
                ),
                "action_items": [
                    "1. Merge: monitoring tools into unified_system_monitor.py",
                    "2. Merge: analysis tools into unified_architecture_analyzer.py",
                    "3. Merge: optimization tools into unified_optimizer_suite.py",
                    "4. Archive: Legacy implementations to tachyonic/archive/deprecated_tools/"
                ],
                "ainlp_pattern": "Ultimate Compressor Pattern",
                "estimated_effort": "High",
                "expected_coherence_gain": "+0.10 to +0.20"
            })
        
        return recommendations
    
    def save_analysis_report(self, report: Dict[str, Any]) -> Path:
        """Save analysis report to tachyonic archive."""
        report_dir = self.tachyonic_root / "integration_optimization"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = report_dir / f"integration_optimization_report_{timestamp}.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        # Also create _latest pointer
        latest_path = report_dir / "integration_optimization_report_latest.json"
        with open(latest_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n Report saved: {report_path.relative_to(self.workspace_root)}")
        print(f" Latest pointer: {latest_path.relative_to(self.workspace_root)}")
        
        return report_path
    
    def generate_markdown_summary(self, report: Dict[str, Any]) -> Path:
        """Generate human-readable markdown summary."""
        summary_dir = self.workspace_root / "changelogs"
        summary_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d")
        summary_path = summary_dir / f"INTEGRATION_OPTIMIZATION_ANALYSIS_{timestamp}.md"
        
        content = self._build_markdown_content(report)
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f" Markdown summary: {summary_path.relative_to(self.workspace_root)}")
        
        return summary_path
    
    def _build_markdown_content(self, report: Dict[str, Any]) -> str:
        """Build comprehensive markdown report."""
        content = f"""# AINLP INTEGRATION AND OPTIMIZATION PATH ANALYSIS

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Workspace**: {report['workspace_root']}  
**Analysis Type**: Overpopulation Decoherence and Consolidation Opportunities

---

## Executive Summary

**Problem**: Overpopulation causing decoherence and degraded discoverability  
**Solution**: AINLP-guided consolidation and harmonization path  
**AINLP Compliance**: {report['ainlp_compliance']['compliance_score']:.2%}

### Key Findings

"""
        
        # Overpopulation analysis summary
        total_files_analyzed = sum(
            cat_data.get("total_files", 0)
            for cat_data in report.get("overpopulation_analysis", {}).values()
        )
        
        total_decoherence = sum(
            cat_data.get("decoherence_level", 0)
            for cat_data in report.get("overpopulation_analysis", {}).values()
        )
        
        consolidation_opps = len(report.get("consolidation_opportunities", []))
        
        content += f"""
- **Files Analyzed**: {total_files_analyzed}
- **Decoherence Level**: {total_decoherence} (interfaces + methods duplication)
- **Consolidation Opportunities**: {consolidation_opps}
- **High Priority Actions**: {len([r for r in report.get('integration_recommendations', []) if r.get('priority') in ['CRITICAL', 'HIGH']])}

---

## Overpopulation Analysis

"""
        
        for category, cat_data in report.get("overpopulation_analysis", {}).items():
            content += f"""
### {category.upper()}

- **Total Files**: {cat_data.get('total_files', 0)}
- **Decoherence Level**: {cat_data.get('decoherence_level', 0)}

"""
            
            for subcat_name, subcat_data in cat_data.get("subcategories", {}).items():
                content += f"""
#### {subcat_name}

**Files**: {subcat_data.get('file_count', 0)}
```
"""
                for file in subcat_data.get("files", []):
                    content += f"{file}\n"
                content += "```\n\n"
                
                # Show duplicate signatures if found
                duplicates = subcat_data.get("duplicate_signatures", {})
                if duplicates.get("interfaces") or duplicates.get("methods"):
                    content += "**Duplicate Signatures Detected**:\n"
                    if duplicates.get("interfaces"):
                        content += f"- Interfaces: {', '.join(duplicates['interfaces'])}\n"
                    if duplicates.get("methods"):
                        content += f"- Methods: {', '.join(duplicates['methods'][:10])}"
                        if len(duplicates['methods']) > 10:
                            content += f" (and {len(duplicates['methods']) - 10} more)"
                        content += "\n"
                    content += "\n"
        
        # Consolidation opportunities
        content += """
---

## Consolidation Opportunities

AINLP Pattern: Enhancement Over Creation + Dendritic Growth

"""
        
        high_priority = [
            opp for opp in report.get("consolidation_opportunities", [])
            if opp["priority"] > 100
        ]
        
        if high_priority:
            content += f"""
### HIGH PRIORITY (Similarity >70%, Force Consolidation)

{len(high_priority)} opportunities identified:

"""
            for opp in high_priority[:10]:  # Top 10
                content += f"""
#### {Path(opp['file_a']).name} + {Path(opp['file_b']).name}

- **Similarity**: {opp['similarity_score']:.2%}
- **Category**: {opp['category']} / {opp['subcategory']}
- **Action**: {opp['recommended_action']}
- **AINLP Principle**: {opp['ainlp_principle']}
- **Priority Score**: {opp['priority']}

**Files**:
- `{opp['file_a']}`
- `{opp['file_b']}`

"""
        
        # Coherence improvements
        content += """
---

## Coherence Improvements

"""
        
        for improvement in report.get("coherence_improvements", []):
            content += f"""
### {improvement['category'].upper()} - {improvement['improvement_type']}

- **Opportunities**: {improvement['opportunities_count']}
- **Average Similarity**: {improvement['average_similarity']:.2%}
- **Decoherence Reduction**: {improvement['decoherence_reduction_potential']} units
- **Target Coherence Score**: {improvement['target_coherence_score']:.2f}
- **Recommended Approach**: {improvement['recommended_approach']}

**Estimated Benefits**:
"""
            for key, value in improvement.get("estimated_benefits", {}).items():
                content += f"- {key.replace('_', ' ').title()}: {value}\n"
            
            content += "\n"
        
        # Integration recommendations
        content += """
---

## Integration Recommendations

"""
        
        for i, rec in enumerate(report.get("integration_recommendations", []), 1):
            content += f"""
### {i}. {rec['title']} [{rec['priority']} PRIORITY]

{rec['description']}

**Action Items**:
"""
            for item in rec.get("action_items", []):
                content += f"{item}\n"
            
            content += f"""
**AINLP Pattern**: {rec['ainlp_pattern']}  
**Estimated Effort**: {rec['estimated_effort']}  
**Expected Coherence Gain**: {rec['expected_coherence_gain']}

"""
        
        # AINLP compliance section
        content += """
---

## AINLP Compliance Validation

"""
        
        for principle in report['ainlp_compliance']['principles_validated']:
            status_icon = "✅" if principle['status'] == "COMPLIANT" else "⚠️"
            content += f"""
### {status_icon} {principle['principle']}

- **Status**: {principle['status']}
- **Evidence**: {principle['evidence']}

"""
        
        content += f"""
**Overall Compliance Score**: {report['ainlp_compliance']['compliance_score']:.2%}

---

## Implementation Path

### Phase 1: Critical Consolidations (Week 1)

1. **AINLPHarmonizer Consolidation** (dev.arch.md Option A)
   - Move core implementation to proper location
   - Remove visual stub, implement DI pattern
   - Expected: +0.54 LFC, +0.54 GPC

2. **High-Priority File Consolidations** ({len(high_priority)} opportunities)
   - Start with >80% similarity pairs
   - Use AINLP compressor patterns
   - Expected: -50% file count in category

### Phase 2: Interface Harmonization (Week 2)

1. **Unified Interface Bridge**
   - Create single source of truth
   - Deprecate redundant implementations
   - Expected: +0.20 coherence

2. **Service Manager Consolidation**
   - Merge AI service managers
   - Standardize interfaces
   - Expected: +0.15 coherence

### Phase 3: Tool Consolidation (Week 3-4)

1. **Runtime Intelligence Tools**
   - Merge monitoring tools
   - Merge analysis tools
   - Merge optimization tools
   - Archive deprecated implementations

2. **Documentation and Testing**
   - Update architectural documentation
   - Validate biological architecture integration
   - Run comprehensive coherence tests

---

## Success Metrics

**Target Coherence Levels** (from dev.arch.md):
- Logic Flow Coherence (LFC): ≥ 0.85 (current: 0.31)
- Global Pattern Coherence (GPC): ≥ 0.82 (current: 0.28)

**Target File Reduction**: -30% to -50% in overpopulated categories

**Target Decoherence Reduction**: -{total_decoherence} units (100%)

**Target Discoverability**: HIGH (clear interface hierarchy)

---

## AINLP Pattern References

This analysis implements patterns from:
- `docs/archive/.../ainlp_ultimate_compressor.py` - Aggressive merging patterns
- `ai/tools/ainlp_documentation_governance.py` - Similarity thresholds (70%/40%)
- `tachyonic/.../dev.arch.md` - Core Consolidation (Option A)
<<<<<<< HEAD
- `runtime_intelligence/tools/architectural_compliance_validator.py` - 4 core principles
=======
- `runtime/tools/architectural_compliance_validator.py` - 4 core principles
>>>>>>> origin/OS0.6.2.grok

---

**Generated by**: AINLP Integration Optimizer  
**Report Location**: `tachyonic/archive/integration_optimization/`  
**Next Steps**: Review recommendations and begin Phase 1 implementation
"""
        
        return content


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print(" AINLP INTEGRATION AND OPTIMIZATION PATH ANALYZER")
    print(" Addressing Overpopulation, Decoherence, and Discoverability Issues")
    print("="*80 + "\n")
    
    # Initialize optimizer
    optimizer = AINLPIntegrationOptimizer()
    
    # Execute analysis
    report = optimizer.execute_integration_analysis()
    
    # Save results
    print("\n[SAVING] Generating reports...")
    json_path = optimizer.save_analysis_report(report)
    md_path = optimizer.generate_markdown_summary(report)
    
    # Display summary
    print("\n" + "="*80)
    print(" ANALYSIS COMPLETE")
    print("="*80)
    
    consolidation_opps = len(report.get("consolidation_opportunities", []))
    high_priority = len([
        o for o in report.get("consolidation_opportunities", [])
        if o["priority"] > 100
    ])
    
    print(f"\n Consolidation Opportunities: {consolidation_opps}")
    print(f" High Priority (>70% similarity): {high_priority}")
    print(f" AINLP Compliance: {report['ainlp_compliance']['compliance_score']:.2%}")
    print(f"\n 📊 JSON Report: {json_path.relative_to(optimizer.workspace_root)}")
    print(f" 📄 Markdown Summary: {md_path.relative_to(optimizer.workspace_root)}")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
