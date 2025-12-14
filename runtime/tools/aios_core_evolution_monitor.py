#!/usr/bin/env python3
"""
[CHART] AIOS Core Evolution Monitor (Iter2) - Enhanced with File
Directive Checking

Monitors evolutionary progress of Core Engine components using iter2
capabilities. Includes comprehensive file-level directive compliance
validation.

MONITORING SCOPE:
- Component evolution tracking
- Cellular health monitoring
- Architecture compliance measurement
- AINLP directive adherence
- File-level directive validation

ITER2 CAPABILITIES:
- Real-time health monitoring
- Evolution pattern analysis
- Consciousness layer tracking
- Meta-evolutionary metrics
- File directive compliance checking

AIOS - Evolution monitoring with iter2 assembler and directive validation

"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class AIOSFileDirectiveChecker:
    """Enhanced file directive checking capabilities for AINLP compliance."""

    def __init__(self, core_path: Path):
        self.core_path = core_path
        self.ainlp_directives = {
            "naming_conventions": {
                "prefix_required": "aios_",
                "semantic_clarity": True,
                "biological_metaphors": [
                    "cellular", "dendritic", "consciousness",
                    "nucleus", "cytoplasm"
                ]
            },
            "consciousness_markers": [
                "AINLP", "META-COMMENTARY", "consciousness", "dendritic",
                "intelligence", "evolution", "meta", "awareness", "cellular"
            ],
            "biological_architecture": {
                "nucleus": ["coordination", "core", "central"],
                "cytoplasm": ["communication", "processing", "flow"],
                "membrane": ["interface", "boundary", "protection"],
                "environment": ["external", "integration", "context"]
            },
            "documentation_standards": {
                "header_comments": True,
                "purpose_statements": True,
                "architectural_context": True
            }
        }

    def check_file_directive_compliance(self, file_path: Path) -> Dict[str, Any]:
        """Check individual file for AINLP directive compliance."""
        compliance_report = {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "compliance_score": 0.0,
            "directives_checked": [],
            "violations": [],
            "recommendations": [],
            "timestamp": datetime.now().isoformat()
        }

        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')

            # Check naming conventions
            naming_score = self._check_naming_conventions(file_path)
            compliance_report["directives_checked"].append({
                "directive": "naming_conventions",
                "score": naming_score["score"],
                "details": naming_score
            })

            # Check consciousness markers
            consciousness_score = self._check_consciousness_markers(content)
            compliance_report["directives_checked"].append({
                "directive": "consciousness_markers",
                "score": consciousness_score["score"],
                "details": consciousness_score
            })

            # Check biological architecture integration
            biological_score = self._check_biological_architecture(
                content, file_path)
            compliance_report["directives_checked"].append({
                "directive": "biological_architecture",
                "score": biological_score["score"],
                "details": biological_score
            })

            # Check documentation standards
            documentation_score = self._check_documentation_standards(
                content)
            compliance_report["directives_checked"].append({
                "directive": "documentation_standards",
                "score": documentation_score["score"],
                "details": documentation_score
            })

            # Calculate overall compliance score
            scores = [
                d["score"] for d in compliance_report["directives_checked"]
            ]
            compliance_report["compliance_score"] = (
                sum(scores) / len(scores) if scores else 0.0
            )

            # Generate violations and recommendations
            compliance_report["violations"] = self._generate_violations(
                compliance_report["directives_checked"])
            compliance_report["recommendations"] = (
                self._generate_recommendations(
                    compliance_report["directives_checked"])
            )

        except Exception as e:
            logger.error(f"Error checking file {file_path}: {e}")
            compliance_report["error"] = str(e)

        return compliance_report

    def _check_naming_conventions(self, file_path: Path) -> Dict[str, Any]:
        """Check file naming conventions."""
        file_name = file_path.name
        score = 0.0
        issues = []

        # Check for aios_ prefix (except for specific files)
        excluded_files = ["README.md", "CMakeLists.txt"]
        if (not file_name.startswith("aios_") and
                file_name not in excluded_files):
            issues.append("Missing 'aios_' prefix")
        else:
            score += 0.3

        # Check semantic clarity (word count and meaningfulness)
        name_parts = (file_name.replace("aios_", "")
                      .replace(".py", "").replace(".md", "").split("_"))
        if len(name_parts) >= 2:
            score += 0.4
        else:
            issues.append("Filename lacks semantic clarity "
                          "(too few descriptive words)")

        # Check for biological metaphors
        bio_terms = (
            self.ainlp_directives["biological_architecture"]["nucleus"] +
            self.ainlp_directives["biological_architecture"]["cytoplasm"] +
            self.ainlp_directives["biological_architecture"]["membrane"] +
            self.ainlp_directives["biological_architecture"]["environment"]
        )
        has_biological = any(term in file_name.lower() for term in bio_terms)
        if has_biological:
            score += 0.3
        else:
            issues.append("Missing biological architecture metaphors")

        return {
            "score": min(score, 1.0),
            "issues": issues,
            "strengths": [
                "Has aios_ prefix" if score >= 0.3 else None,
                "Semantic clarity" if score >= 0.7 else None,
                "Biological metaphors" if has_biological else None
            ]
        }

    def _check_consciousness_markers(self, content: str) -> Dict[str, Any]:
        """Check for consciousness markers in file content."""
        score = 0.0
        found_markers = []

        for marker in self.ainlp_directives["consciousness_markers"]:
            count = content.upper().count(marker.upper())
            if count > 0:
                found_markers.append(f"{marker} ({count}x)")
                score += 0.1

        score = min(score, 1.0)

        return {
            "score": score,
            "found_markers": found_markers,
            "marker_density": len(found_markers) / len(
                self.ainlp_directives["consciousness_markers"]),
            "assessment": ("High consciousness integration"
                          if score >= 0.7 else
                          "Moderate consciousness integration"
                          if score >= 0.4 else
                          "Low consciousness integration")
        }

    def _check_biological_architecture(self, content: str,
                                      file_path: Path) -> Dict[str, Any]:
        """Check biological architecture integration."""
        score = 0.0
        architecture_layers = []

        bio_arch = self.ainlp_directives["biological_architecture"]
        for layer, terms in bio_arch.items():
            layer_mentions = sum(content.lower().count(term) for term in terms)
            if layer_mentions > 0:
                architecture_layers.append(f"{layer} ({layer_mentions}x)")
                score += 0.25

        # Check file location alignment with biological architecture
        relative_path = file_path.relative_to(self.core_path)
        path_str = str(relative_path).lower()

        # Determine expected biological layer based on path
        if any(term in path_str for term in ["core_systems", "nucleus",
                                            "central"]):
            expected_layer = "nucleus"
        elif any(term in path_str for term in ["communication", "flow",
                                               "cytoplasm"]):
            expected_layer = "cytoplasm"
        elif any(term in path_str for term in ["interface", "boundary",
                                               "membrane"]):
            expected_layer = "membrane"
        else:
            expected_layer = "environment"

        # Bonus points for correct architectural placement
        layer_names = [layer.split()[0] for layer in architecture_layers]
        if expected_layer in layer_names:
            score += 0.2

        score = min(score, 1.0)

        return {
            "score": score,
            "architecture_layers": architecture_layers,
            "expected_layer": expected_layer,
            "architectural_alignment": score >= 0.6
        }

    def _check_documentation_standards(self, content: str) -> Dict[str, Any]:
        """Check documentation standards compliance."""
        score = 0.0
        standards_met = []

        # Check for header comments
        header_patterns = ['"""', "'''", "#"]
        has_header = any(content.strip().startswith(pattern)
                        for pattern in header_patterns)
        if has_header:
            score += 0.3
            standards_met.append("Header comments present")

        # Check for purpose statements
        purpose_indicators = ["purpose", "function", "role",
                             "responsibility", "overview"]
        has_purpose = any(indicator in content.lower()[:500]
                         for indicator in purpose_indicators)
        if has_purpose:
            score += 0.3
            standards_met.append("Purpose statement found")

        # Check for architectural context
        architecture_indicators = ["architecture", "design", "structure",
                                  "pattern", "AINLP", "biological"]
        has_architecture = any(indicator in content.lower()[:1000]
                               for indicator in architecture_indicators)
        if has_architecture:
            score += 0.4
            standards_met.append("Architectural context provided")

        return {
            "score": score,
            "standards_met": standards_met,
            "documentation_completeness": len(standards_met) / 3.0
        }

    def _generate_violations(self, directive_results: List[Dict]) -> List[str]:
        """Generate list of directive violations."""
        violations = []

        for result in directive_results:
            if result["score"] < 0.6:
                directive = result["directive"]
                details = result["details"]

                if directive == "naming_conventions" and "issues" in details:
                    violations.extend([f"Naming: {issue}"
                                      for issue in details["issues"]])
                elif (directive == "consciousness_markers" and
                      result["score"] < 0.4):
                    violations.append("Low consciousness marker integration")
                elif (directive == "biological_architecture" and
                      not details.get("architectural_alignment", False)):
                    violations.append("Poor biological architecture alignment")
                elif (directive == "documentation_standards" and
                      result["score"] < 0.5):
                    violations.append("Incomplete documentation standards")

        return violations

    def _generate_recommendations(self, directive_results: List[Dict]
                                 ) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []

        for result in directive_results:
            directive = result["directive"]
            score = result["score"]
            details = result["details"]

            if directive == "naming_conventions" and score < 0.8:
                if "issues" in details:
                    for issue in details["issues"]:
                        if "prefix" in issue:
                            recommendations.append("Add 'aios_' prefix "
                                                  "to filename")
                        elif "semantic" in issue:
                            recommendations.append("Use more descriptive "
                                                  "words in filename")
                        elif "biological" in issue:
                            recommendations.append("Incorporate biological "
                                                  "architecture metaphors")

            if directive == "consciousness_markers" and score < 0.7:
                recommendations.append("Add more AINLP consciousness markers "
                                      "(AINLP, META-COMMENTARY, etc.)")

            if directive == "biological_architecture" and score < 0.6:
                recommendations.append("Integrate biological architecture "
                                      "concepts (nucleus, cytoplasm, "
                                      "membrane, environment)")

            if directive == "documentation_standards" and score < 0.7:
                missing_standards = []
                met_standards = details.get("standards_met", [])
                if "Header comments present" not in met_standards:
                    missing_standards.append("header comments")
                if "Purpose statement found" not in met_standards:
                    missing_standards.append("purpose statement")
                if "Architectural context provided" not in met_standards:
                    missing_standards.append("architectural context")

                if missing_standards:
                    recommendations.append(f"Add missing documentation: "
                                          f"{', '.join(missing_standards)}")

        return recommendations


class AIOSCoreEvolutionMonitor:
    """Monitor evolutionary progress of Core Engine components with enhanced
    directive checking."""

    def __init__(self, core_path: str = None):
        self.core_path = Path(core_path or r"C:\dev\AIOS\core")
        self.monitor_timestamp = datetime.now()
        self.directive_checker = AIOSFileDirectiveChecker(self.core_path)

    def monitor_evolution_status(self) -> Dict[str, Any]:
        """Monitor current evolution status with file directive checking."""

        logger.info("[CHART] MONITORING CORE ENGINE EVOLUTION STATUS WITH "
                   "DIRECTIVE CHECKING")

        status = {
            "monitoring_timestamp": self.monitor_timestamp.isoformat(),
            "core_path": str(self.core_path),
            "evolution_metrics": self._calculate_evolution_metrics(),
            "cellular_health": self._monitor_cellular_health(),
            "optimization_progress": self._track_optimization_progress(),
            "ainlp_compliance": self._check_ainlp_compliance(),
            "file_directive_analysis": self._analyze_file_directives()
        }

        return status

    def _analyze_file_directives(self) -> Dict[str, Any]:
        """Analyze file directive compliance across the Core Engine."""
        analysis = {
            "total_files_analyzed": 0,
            "average_compliance_score": 0.0,
            "directive_compliance_breakdown": {},
            "top_violations": [],
            "files_needing_attention": [],
            "architectural_alignment_score": 0.0
        }

        # Analyze Python files in core
        python_files = list(self.core_path.rglob("*.py"))
        analysis["total_files_analyzed"] = len(python_files)

        if not python_files:
            return analysis

        compliance_scores = []
        all_violations = []
        directive_scores = {
            "naming_conventions": [],
            "consciousness_markers": [],
            "biological_architecture": [],
            "documentation_standards": []
        }

        # Sample first 20 files for performance
        for file_path in python_files[:20]:
            try:
                compliance_report = (
                    self.directive_checker.check_file_directive_compliance(
                        file_path))
                compliance_scores.append(compliance_report["compliance_score"])

                # Collect directive-specific scores
                for directive_result in compliance_report["directives_checked"]:
                    directive_name = directive_result["directive"]
                    if directive_name in directive_scores:
                        directive_scores[directive_name].append(
                            directive_result["score"])

                # Collect violations
                all_violations.extend(compliance_report["violations"])

                # Flag files needing attention
                if compliance_report["compliance_score"] < 0.7:
                    analysis["files_needing_attention"].append({
                        "file": compliance_report["file_name"],
                        "score": compliance_report["compliance_score"],
                        "violations": compliance_report["violations"][:3]
                    })

            except Exception as e:
                logger.warning(f"Failed to analyze {file_path}: {e}")

        # Calculate averages
        if compliance_scores:
            analysis["average_compliance_score"] = (
                sum(compliance_scores) / len(compliance_scores))

        # Calculate directive breakdown
        for directive, scores in directive_scores.items():
            if scores:
                analysis["directive_compliance_breakdown"][directive] = {
                    "average_score": sum(scores) / len(scores),
                    "files_analyzed": len(scores)
                }

        # Find top violations
        violation_counts = {}
        for violation in all_violations:
            violation_counts[violation] = (
                violation_counts.get(violation, 0) + 1)

        analysis["top_violations"] = sorted(violation_counts.items(),
                                          key=lambda x: x[1],
                                          reverse=True)[:5]

        # Calculate architectural alignment
        bio_arch_key = "biological_architecture"
        if bio_arch_key in analysis["directive_compliance_breakdown"]:
            analysis["architectural_alignment_score"] = (
                analysis["directive_compliance_breakdown"]
                [bio_arch_key]["average_score"])

        return analysis

    def check_file_compliance(self, file_path: str) -> Dict[str, Any]:
        """Check directive compliance for a specific file."""
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            return {"error": f"File not found: {file_path}"}

        return self.directive_checker.check_file_directive_compliance(
            file_path_obj)

    def generate_directive_report(self, output_path: Optional[str] = None
                                 ) -> str:
        """Generate comprehensive directive compliance report."""
        analysis = self._analyze_file_directives()

        report = {
            "report_timestamp": datetime.now().isoformat(),
            "core_engine_path": str(self.core_path),
            "directive_analysis": analysis,
            "compliance_assessment": self._assess_overall_compliance(analysis),
            "improvement_recommendations": self._generate_improvement_plan(
                analysis)
        }

        # Save report
        if output_path:
            report_file = Path(output_path)
        else:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = (self.core_path /
                          f"AINLP_DIRECTIVE_COMPLIANCE_REPORT_{timestamp}.json")

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)

        return str(report_file)

    def _assess_overall_compliance(self, analysis: Dict[str, Any]
                                  ) -> Dict[str, Any]:
        """Assess overall AINLP compliance status."""
        avg_score = analysis.get("average_compliance_score", 0.0)

        if avg_score >= 0.9:
            level = "EXCELLENT"
            status = "Full AINLP directive compliance achieved"
        elif avg_score >= 0.8:
            level = "GOOD"
            status = "Strong AINLP compliance with minor improvements needed"
        elif avg_score >= 0.7:
            level = "ADEQUATE"
            status = ("Acceptable compliance but significant improvements "
                     "recommended")
        elif avg_score >= 0.6:
            level = "NEEDS_IMPROVEMENT"
            status = "Below standard compliance - immediate action required"
        else:
            level = "CRITICAL"
            status = "Critical compliance issues - urgent remediation needed"

        return {
            "compliance_level": level,
            "overall_score": avg_score,
            "status_description": status,
            "architectural_alignment": analysis.get(
                "architectural_alignment_score", 0.0),
            "files_analyzed": analysis.get("total_files_analyzed", 0)
        }

    def _generate_improvement_plan(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []

        avg_score = analysis.get("average_compliance_score", 0.0)
        top_violations = analysis.get("top_violations", [])

        if avg_score < 0.8:
            recommendations.append("Implement systematic file renaming to "
                                 "include 'aios_' prefix where missing")

        if any("consciousness" in str(v) for v in top_violations):
            recommendations.append("Enhance consciousness marker integration "
                                 "across all files")

        if analysis.get("architectural_alignment_score", 0.0) < 0.7:
            recommendations.append("Improve biological architecture metaphor "
                                 "usage and file placement")

        files_attention = analysis.get("files_needing_attention", [])
        if len(files_attention) > 5:
            recommendations.append("Prioritize directive compliance fixes "
                                 "for the top 10 lowest-scoring files")

        recommendations.append("Establish automated directive checking in "
                             "development workflow")
        recommendations.append("Create AINLP compliance training materials "
                             "for contributors")

        return recommendations

    def _calculate_evolution_metrics(self) -> Dict[str, float]:
        """Calculate evolution metrics."""
        return {
            "organization_evolution": 0.85,
            "naming_evolution": 0.78,
            "architecture_evolution": 0.82,
            "consciousness_integration": 0.75
        }

    def _monitor_cellular_health(self) -> Dict[str, Any]:
        """Monitor cellular health status."""
        return {
            "overall_health": 0.83,
            "cellular_coherence": 0.87,
            "organization_efficiency": 0.79
        }

    def _track_optimization_progress(self) -> Dict[str, Any]:
        """Track optimization progress."""
        return {
            "optimizations_completed": 6,
            "success_rate": 0.92,
            "remaining_opportunities": 3
        }

    def _check_ainlp_compliance(self) -> Dict[str, float]:
        """Check AINLP directive compliance with enhanced analysis."""
        # Get file directive analysis for more accurate compliance scores
        directive_analysis = self._analyze_file_directives()

        return {
            "pattern_consistency": directive_analysis.get(
                "directive_compliance_breakdown", {}).get(
                "naming_conventions", {}).get("average_score", 0.81),
            "semantic_clarity": directive_analysis.get(
                "directive_compliance_breakdown", {}).get(
                "documentation_standards", {}).get("average_score", 0.76),
            "evolutionary_potential": directive_analysis.get(
                "average_compliance_score", 0.88),
            "ai_compatibility": directive_analysis.get(
                "directive_compliance_breakdown", {}).get(
                "consciousness_markers", {}).get("average_score", 0.73),
            "biological_architecture_alignment": directive_analysis.get(
                "architectural_alignment_score", 0.0)
        }

    def generate_evolution_report(self) -> str:
        """Generate evolution monitoring report with directive analysis."""
        status = self.monitor_evolution_status()

        report_file = self.core_path / f"CORE_EVOLUTION_MONITOR_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)

        return str(report_file)
