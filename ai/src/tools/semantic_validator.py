#!/usr/bin/env python3
"""
[SEMANTIC] Intelligence Delimitation Validator

Validates semantic compression and detects intelligence
antipatterns in runtime supercell. Implements AINLP
namespace compression strategy with intelligence
localization.

VALIDATION SCOPE:
- Semantic compression compliance
- Intelligence antipattern detection
- Namespace strategy enforcement
- Pervasive intelligence prevention

AIOS - Semantic validation with intelligence delimitation

"""
import re
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class IntelligenceDelimitationValidator:
    """Validator for intelligence delimitation antipatterns
    and semantic compression."""

    def __init__(self, runtime_path: Path):
        self.runtime_path = runtime_path
        self.antipatterns = self._load_antipatterns()
        self.semantic_rules = self._load_semantic_rules()

    def _load_antipatterns(self) -> Dict[str, Any]:
        """Load intelligence antipattern definitions."""
        return {
            "pervasive_intelligence": {
                "pattern": (
                    r"\bintelligence\b(?!\s+"
                    r"(evolutionary|dendritic|cellular|"
                    r"meta|AINLP))"
                ),
                "description": (
                    "Generic intelligence usage without " "domain qualification"
                ),
                "severity": "high",
            },
            "adverbial_intelligence": {
                "pattern": r"\bintelligent\s+\w+",
                "description": ("Intelligence used as adverbial " "modifier"),
                "severity": "medium",
            },
            "intelligence_namespace": {
                "pattern": r"\bruntime\b",
                "description": "Uncompressed namespace usage",
                "severity": "high",
            },
            "intelligence_dilution": {
                "pattern": r"\bintelligence_[a-z_]+\b",
                "description": (
                    "Intelligence as generic qualifier " "in compound words"
                ),
                "severity": "medium",
            },
        }

    def _load_semantic_rules(self) -> Dict[str, Any]:
        """Load semantic compression rules."""
        return {
            "namespace_compression": {
                "from": "runtime",
                "to": "runtime",
                "rationale": "Remove adverbial intelligence qualifier",
            },
            "intelligence_localization": {
                "patterns": {
                    "intelligence_monitoring": "evolution_tracking",
                    "intelligence_analysis": "pattern_recognition",
                    "intelligence_processing": "meta_processing",
                    "intelligent_system": "adaptive_system",
                }
            },
        }

    def validate_semantic_compliance(self) -> Dict[str, Any]:
        """Validate semantic compression and intelligence
        delimitation compliance."""

        validation = {
            "timestamp": datetime.now().isoformat(),
            "runtime_path": str(self.runtime_path),
            "semantic_compression_score": 0.0,
            "intelligence_delimitation_score": 0.0,
            "antipatterns_detected": [],
            "compression_opportunities": [],
            "recommendations": [],
        }

        # Analyze all Python files
        python_files = list(self.runtime_path.rglob("*.py"))

        for file_path in python_files:
            file_analysis = self._analyze_file_semantics(file_path)
            validation["antipatterns_detected"].extend(file_analysis["antipatterns"])
            validation["compression_opportunities"].extend(
                file_analysis["opportunities"]
            )

        # Calculate scores
        total_antipatterns = len(validation["antipatterns_detected"])
        validation["intelligence_delimitation_score"] = max(
            0.0, 1.0 - (total_antipatterns * 0.1)
        )

        compression_opportunities = len(validation["compression_opportunities"])
        validation["semantic_compression_score"] = max(
            0.0, 1.0 - (compression_opportunities * 0.05)
        )

        # Generate recommendations
        validation["recommendations"] = self._generate_semantic_recommendations(
            validation
        )

        return validation

    def _analyze_file_semantics(self, file_path: Path) -> Dict[str, Any]:
        """Analyze semantic compliance of individual file."""

        analysis = {
            "file_path": str(file_path),
            "antipatterns": [],
            "opportunities": [],
        }

        try:
            content = file_path.read_text(encoding="utf-8")

            # Check for antipatterns
            for pattern_name, pattern_config in self.antipatterns.items():
                matches = re.findall(pattern_config["pattern"], content, re.IGNORECASE)
                if matches:
                    analysis["antipatterns"].append(
                        {
                            "file": str(file_path),
                            "pattern": pattern_name,
                            "description": pattern_config["description"],
                            "severity": pattern_config["severity"],
                            "occurrences": len(matches),
                            "examples": matches[:3],  # First 3 examples
                        }
                    )

            # Check for compression opportunities
            patterns = self.semantic_rules["intelligence_localization"]["patterns"]
            for old_term, new_term in patterns.items():
                if old_term in content:
                    analysis["opportunities"].append(
                        {
                            "file": str(file_path),
                            "from": old_term,
                            "to": new_term,
                            "occurrences": content.count(old_term),
                        }
                    )

        except Exception as e:
            analysis["error"] = str(e)

        return analysis

    def _generate_semantic_recommendations(
        self, validation: Dict[str, Any]
    ) -> List[str]:
        """Generate semantic improvement recommendations."""

        recommendations = []

        # Antipattern remediation
        high_severity = [
            a for a in validation["antipatterns_detected"] if a["severity"] == "high"
        ]
        if high_severity:
            msg = (
                f"Address {len(high_severity)} high-severity "
                "intelligence antipatterns immediately"
            )
            recommendations.append(msg)

        # Compression opportunities
        if validation["compression_opportunities"]:
            opportunities = len(validation["compression_opportunities"])
            msg = (
                f"Apply semantic compression to {opportunities} "
                "identified opportunities"
            )
            recommendations.append(msg)

        # Namespace strategy
        detected = validation["antipatterns_detected"]
        if any("namespace" in str(a) for a in detected):
            msg = "Implement namespace compression: " "runtime → runtime"
            recommendations.append(msg)

        # Intelligence localization
        pervasive_usage = [
            a
            for a in validation["antipatterns_detected"]
            if "pervasive" in a["pattern"]
        ]
        if pervasive_usage:
            msg = (
                "Localize intelligence usage to specific domains "
                "(evolutionary, dendritic, cellular, meta)"
            )
            recommendations.append(msg)

        return recommendations

    def apply_semantic_compression(self, dry_run: bool = True) -> Dict[str, Any]:
        """Apply semantic compression transformations."""

        compression = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "transformations_applied": [],
            "files_modified": 0,
        }

        # Apply namespace compression
        namespace_pattern = self.semantic_rules["namespace_compression"]
        old_namespace = namespace_pattern["from"]
        new_namespace = namespace_pattern["to"]

        for file_path in self.runtime_path.rglob("*.py"):
            try:
                content = file_path.read_text(encoding="utf-8")
                original_content = content

                # Apply namespace compression
                content = content.replace(old_namespace, new_namespace)

                # Apply intelligence localization
                patterns = self.semantic_rules["intelligence_localization"]["patterns"]
                for old_term, new_term in patterns.items():
                    content = content.replace(old_term, new_term)

                if content != original_content:
                    compression["transformations_applied"].append(
                        {
                            "file": str(file_path),
                            "changes": self._diff_content(original_content, content),
                        }
                    )

                    if not dry_run:
                        file_path.write_text(content, encoding="utf-8")
                        compression["files_modified"] += 1

            except Exception as e:
                compression["error"] = f"Failed to process {file_path}: {e}"

        return compression

    def _diff_content(self, original: str, modified: str) -> List[str]:
        """Generate simple diff of content changes."""
        original_lines = original.split("\n")
        modified_lines = modified.split("\n")

        changes = []
        for i, (orig, mod) in enumerate(zip(original_lines, modified_lines)):
            if orig != mod:
                changes.append(f"Line {i+1}: '{orig}' → '{mod}'")

        return changes


def main():
    """Execute semantic validation and compression."""
    validator = IntelligenceDelimitationValidator(Path(__file__).parent)

    # Validate current state
    validation = validator.validate_semantic_compliance()
    print("=== Intelligence Delimitation Validation ===")
    print(
        f"Semantic Compression Score: "
        f"{validation['semantic_compression_score']:.2f}"
    )
    print(
        f"Intelligence Delimitation Score: "
        f"{validation['intelligence_delimitation_score']:.2f}"
    )
    print(f"Antipatterns Detected: " f"{len(validation['antipatterns_detected'])}")

    # Apply compression (dry run first)
    compression = validator.apply_semantic_compression(dry_run=True)
    print(
        f"\nCompression Opportunities: "
        f"{len(compression['transformations_applied'])}"
    )

    # Save validation report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Archive reports in tachyonic for AINLP pattern analysis
    archive_path = (
        Path(__file__).parent.parent.parent.parent / "tachyonic" / "archive" / "runtime"
    )
    archive_path.mkdir(parents=True, exist_ok=True)
    report_file = archive_path / f"semantic_validation_{timestamp}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(validation, f, indent=2)

    print(f"Validation report archived: {report_file}")
    print(f"AINLP Pattern Analysis: Available in tachyonic/archive/runtime/")


if __name__ == "__main__":
    main()
