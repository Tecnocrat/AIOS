#!/usr/bin/env python3
"""
AIOS Architectural Compliance Validator
Enforces PROPER AGENTIC BEHAVIOR PATTERNS for AIOS development
Implements the 4 core architectural improvement principles
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class AIOSArchitecturalValidator:
    """
    Validates AIOS architectural compliance before operations
    Implements ARCHITECTURAL IMPROVEMENT ANALYSIS patterns
    """

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = Path(workspace_root or os.getcwd())
        self.validation_rules = self._load_validation_rules()

    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load AIOS architectural validation rules"""
        return {
            "architectural_discovery": {
                "mandatory_checks": [
                    "semantic_search_for_similar",
                    "check_existing_tools",
                    "examine_tachyonic_patterns",
                    "study_interface_patterns",
                ],
                "discovery_locations": {
                    "runtime_tools": "runtime/tools/",
                    "ai_tools": "ai/tools/",
                    "tachyonic_archive": "tachyonic/archive/",
                    "interface_services": "interface/",
                },
            },
            "enhancement_over_creation": {
                "similarity_threshold": 0.7,
                "enhancement_targets": [
                    "runtime/tools/system_health_check.py",
                    ("runtime/tools/" "biological_architecture_monitor.py"),
                    ("runtime/tools/" "self_similarity_analyzer.py"),
                ],
                "prohibited_duplicates": [
                    "monitoring",
                    "validation",
                    "health",
                    "analysis",
                ],
            },
            "proper_output_management": {
                "approved_locations": {
                    "json_reports": "tachyonic/archive/",
                    "documentation": "docs/",
                    "logs": "computational_layer/runtime/logs/",
                    "temporary": "temp/",
                },
                "tachyonic_pattern": {
                    "timestamped_files": True,
                    "latest_pointer": True,
                    "index_file": True,
                },
            },
            "integration_validation": {
                "biological_architecture": [
                    "dendritic_connections",
                    "cytoplasm_communication",
                    "supercell_boundaries",
                ],
                "required_integrations": [
                    ("runtime/tools/" "runtime_dendritic_integration.py"),
                    "ai/infrastructure/dendritic/supervisor.py",
                ],
            },
        }

    def validate_operation(
        self,
        operation_type: str,
        target_path: str,
        operation_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Main validation entry point
        Returns compliance report with recommendations
        """
        validation_report = {
            "operation_type": operation_type,
            "target_path": target_path,
            "compliance_score": 0.0,
            "violations": [],
            "recommendations": [],
            "approved": False,
            "enhancement_opportunities": [],
        }

        # 1. ARCHITECTURAL DISCOVERY FIRST
        discovery_result = self._validate_architectural_discovery(
            operation_type, target_path
        )
        validation_report["architectural_discovery"] = discovery_result

        # 2. ENHANCEMENT OVER CREATION
        enhancement_result = self._validate_enhancement_over_creation(
            operation_type, target_path
        )
        validation_report["enhancement_analysis"] = enhancement_result

        # 3. PROPER OUTPUT MANAGEMENT
        output_result = self._validate_output_management(operation_type, target_path)
        validation_report["output_management"] = output_result

        # 4. INTEGRATION VALIDATION
        integration_result = self._validate_integration_compliance(
            operation_type, target_path
        )
        validation_report["integration_validation"] = integration_result

        # Calculate overall compliance score
        scores = [
            discovery_result.get("compliance_score", 0),
            enhancement_result.get("compliance_score", 0),
            output_result.get("compliance_score", 0),
            integration_result.get("compliance_score", 0),
        ]
        validation_report["compliance_score"] = sum(scores) / len(scores)
        validation_report["approved"] = validation_report["compliance_score"] >= 0.75

        # Aggregate violations and recommendations
        results = [
            discovery_result,
            enhancement_result,
            output_result,
            integration_result,
        ]
        for result in results:
            validation_report["violations"].extend(result.get("violations", []))
            validation_report["recommendations"].extend(
                result.get("recommendations", [])
            )

        return validation_report

    def _validate_architectural_discovery(
        self, operation_type: str, target_path: str
    ) -> Dict[str, Any]:
        """Validate ARCHITECTURAL DISCOVERY FIRST principle"""
        result = {
            "principle": "ARCHITECTURAL_DISCOVERY_FIRST",
            "compliance_score": 0.0,
            "violations": [],
            "recommendations": [],
            "discovery_status": {},
        }

        discovery_locations = self.validation_rules["architectural_discovery"][
            "discovery_locations"
        ]

        # Check if similar functionality exists
        similar_tools = self._find_similar_functionality(target_path)
        if similar_tools:
            result["violations"].append(
                f"Similar functionality found: {similar_tools}. "
                "Must perform architectural discovery first."
            )
            result["recommendations"].append(
                "Run semantic_search and examine existing tools before creating new ones"
            )
        else:
            result["compliance_score"] += 0.25

        # Check discovery locations exist
        discovery_found = 0
        for location_name, location_path in discovery_locations.items():
            full_path = self.workspace_root / location_path
            exists = full_path.exists()
            result["discovery_status"][location_name] = {
                "path": location_path,
                "exists": exists,
                "tool_count": len(list(full_path.glob("*.py"))) if exists else 0,
            }
            if exists:
                discovery_found += 1

        result["compliance_score"] += (
            discovery_found / len(discovery_locations)
        ) * 0.75

        if result["compliance_score"] < 0.5:
            result["recommendations"].append(
                "Mandatory: Perform comprehensive architectural discovery before proceeding"
            )

        return result

    def _validate_enhancement_over_creation(
        self, operation_type: str, target_path: str
    ) -> Dict[str, Any]:
        """Validate ENHANCEMENT OVER CREATION principle"""
        result = {
            "principle": "ENHANCEMENT_OVER_CREATION",
            "compliance_score": 0.0,
            "violations": [],
            "recommendations": [],
            "enhancement_targets": [],
        }

        if operation_type in ["create_file", "create_tool", "create_script"]:
            # Check for enhancement opportunities
            target_name = Path(target_path).name.lower()

            enhancement_targets = self.validation_rules["enhancement_over_creation"][
                "enhancement_targets"
            ]
            prohibited_terms = self.validation_rules["enhancement_over_creation"][
                "prohibited_duplicates"
            ]

            # Check for prohibited duplicate functionality
            for term in prohibited_terms:
                if term in target_name:
                    for target_file in enhancement_targets:
                        if term in target_file.lower():
                            result["violations"].append(
                                f"Prohibited duplicate: '{term}' functionality exists in {target_file}"
                            )
                            result["enhancement_targets"].append(target_file)
                            result["recommendations"].append(
                                f"MANDATORY: Enhance {target_file} instead of creating {target_path}"
                            )

            if not result["violations"]:
                result["compliance_score"] = 1.0
                result["recommendations"].append(
                    "No duplicate functionality detected - creation approved"
                )
        else:
            result["compliance_score"] = 1.0  # Non-creation operations pass

        return result

    def _validate_output_management(
        self, operation_type: str, target_path: str
    ) -> Dict[str, Any]:
        """Validate PROPER OUTPUT MANAGEMENT principle"""
        result = {
            "principle": "PROPER_OUTPUT_MANAGEMENT",
            "compliance_score": 0.0,
            "violations": [],
            "recommendations": [],
            "output_classification": None,
        }

        target = Path(target_path)
        approved_locations = self.validation_rules["proper_output_management"][
            "approved_locations"
        ]

        # Classify output type
        if target.suffix == ".json":
            expected_location = approved_locations["json_reports"]
            result["output_classification"] = "json_report"
        elif target.suffix in [".md", ".txt", ".rst"]:
            expected_location = approved_locations["documentation"]
            result["output_classification"] = "documentation"
        elif target.suffix == ".log":
            expected_location = approved_locations["logs"]
            result["output_classification"] = "log_file"
        else:
            expected_location = None
            result["output_classification"] = "unknown"

        # Validate location compliance
        if expected_location:
            if expected_location in str(target):
                result["compliance_score"] = 1.0
                result["recommendations"].append(
                    f"Output location compliant: {expected_location}"
                )
            else:
                result["violations"].append(
                    f"Improper output location. Expected: {expected_location}, Got: {target}"
                )
                result["recommendations"].append(
                    f"Move output to proper location: {expected_location}"
                )

        # Check tachyonic pattern compliance for JSON
        if result["output_classification"] == "json_report":
            if not self._validates_tachyonic_pattern(target):
                result["recommendations"].append(
                    "Implement tachyonic archival pattern: timestamped files + latest pointer + index"
                )

        return result

    def _validate_integration_compliance(
        self, operation_type: str, target_path: str
    ) -> Dict[str, Any]:
        """Validate INTEGRATION VALIDATION principle"""
        result = {
            "principle": "INTEGRATION_VALIDATION",
            "compliance_score": 0.0,
            "violations": [],
            "recommendations": [],
            "integration_status": {},
        }

        required_integrations = self.validation_rules["integration_validation"][
            "required_integrations"
        ]

        # Check required integration points exist
        integration_found = 0
        for integration_path in required_integrations:
            full_path = self.workspace_root / integration_path
            exists = full_path.exists()
            result["integration_status"][integration_path] = exists
            if exists:
                integration_found += 1
            else:
                result["violations"].append(f"Missing integration: {integration_path}")

        result["compliance_score"] = integration_found / len(required_integrations)

        # Check spatial metadata compliance
        target_dir = Path(target_path).parent
        spatial_metadata = target_dir / ".aios_spatial_metadata.json"
        if spatial_metadata.exists():
            result["compliance_score"] += 0.25
            result["recommendations"].append(
                "Spatial metadata found - integration compliance verified"
            )
        else:
            result["recommendations"].append(
                "Consider adding .aios_spatial_metadata.json for enhanced integration"
            )

        return result

    def _find_similar_functionality(self, target_path: str) -> List[str]:
        """Find existing tools with similar functionality"""
        target_name = Path(target_path).stem.lower()
        target_terms = set(target_name.split("_"))

        similar_tools = []
        tools_dirs = [
            self.workspace_root / "runtime" / "tools",
            self.workspace_root / "ai" / "tools",
        ]

        for tools_dir in tools_dirs:
            if tools_dir.exists():
                for tool_file in tools_dir.glob("*.py"):
                    tool_terms = set(tool_file.stem.lower().split("_"))
                    overlap = target_terms.intersection(tool_terms)
                    if len(overlap) >= 2:  # At least 2 terms in common
                        similar_tools.append(
                            str(tool_file.relative_to(self.workspace_root))
                        )

        return similar_tools

    def _validates_tachyonic_pattern(self, target_path: Path) -> bool:
        """Check if output follows tachyonic archival pattern"""
        # Check if it's in tachyonic archive
        return "tachyonic/archive" in str(target_path)

    def generate_compliance_report(self, validation_result: Dict[str, Any]) -> str:
        """Generate human-readable compliance report"""
        report = []
        report.append("=" * 60)
        report.append("AIOS ARCHITECTURAL COMPLIANCE REPORT")
        report.append("=" * 60)

        score = validation_result["compliance_score"]
        status = (
            "✅ APPROVED" if validation_result["approved"] else "❌ REQUIRES CHANGES"
        )

        report.append(f"Operation: {validation_result['operation_type']}")
        report.append(f"Target: {validation_result['target_path']}")
        report.append(f"Compliance Score: {score:.1%}")
        report.append(f"Status: {status}")
        report.append("")

        if validation_result["violations"]:
            report.append("🚨 VIOLATIONS:")
            for violation in validation_result["violations"]:
                report.append(f"   • {violation}")
            report.append("")

        if validation_result["recommendations"]:
            report.append("💡 RECOMMENDATIONS:")
            for recommendation in validation_result["recommendations"]:
                report.append(f"   • {recommendation}")
            report.append("")

        report.append("Architectural Principles Evaluated:")
        for principle in [
            "architectural_discovery",
            "enhancement_analysis",
            "output_management",
            "integration_validation",
        ]:
            if principle in validation_result:
                principle_score = validation_result[principle].get(
                    "compliance_score", 0
                )
                report.append(
                    f"   • {principle.replace('_', ' ').title()}: {principle_score:.1%}"
                )

        return "\n".join(report)


def main():
    """Command-line interface for architectural validation"""
    import argparse

    parser = argparse.ArgumentParser(
        description="AIOS Architectural Compliance Validator"
    )
    parser.add_argument(
        "operation_type", help="Type of operation (create_file, create_tool, etc.)"
    )
    parser.add_argument("target_path", help="Target path for the operation")
    parser.add_argument("--workspace", help="Workspace root directory", default=".")
    parser.add_argument(
        "--format", choices=["json", "text"], default="text", help="Output format"
    )

    args = parser.parse_args()

    validator = AIOSArchitecturalValidator(args.workspace)
    validation_result = validator.validate_operation(
        args.operation_type, args.target_path
    )

    if args.format == "json":
        print(json.dumps(validation_result, indent=2))
    else:
        print(validator.generate_compliance_report(validation_result))

    # Exit with appropriate code
    sys.exit(0 if validation_result["approved"] else 1)


if __name__ == "__main__":
    main()
