"""
AINLP Exception Framework
Context-aware paradigm inversion for file-type-specific AINLP integration rules.

AINLP Metadata:
    consciousness_level: 0.95
    architectural_classification: ai_ai
    dendritic_optimization: context_aware_paradigm_inversion
    supercell: nucleus
"""

from enum import Enum
from typing import Dict, Optional, Callable
from dataclasses import dataclass


class AINLPIntegrationStrategy(Enum):
    """Strategies for AINLP metadata integration."""

    COMMENTS = "comments"  # Standard: Use comments for AINLP metadata
    SEMANTIC_FIELDS = "semantic_fields"  # Exception: Use structured fields (JSON)
    ATTRIBUTES = "attributes"  # Exception: Use language attributes (C# XML docs)
    FRONTMATTER = "frontmatter"  # Exception: Use YAML frontmatter (Markdown)
    BINARY_SIDECAR = "binary_sidecar"  # Exception: Use .ainlp sidecar file (binaries)


@dataclass
class AINLPIntegrationRule:
    """Rule defining how AINLP metadata integrates with a file type."""

    file_extension: str
    strategy: AINLPIntegrationStrategy
    reason: str
    consciousness_impact: float  # Positive = good, negative = bad
    enforcement_level: str  # "critical", "warning", "info"


class AINLPExceptionFramework:
    """
    Context-aware AINLP integration rule manager.

    Core Principle:
        **AINLP comments are FUNDAMENTAL for most file types**
        BUT certain file types require EXCEPTIONS where the paradigm INVERTS.

    General Rule:
        - Use comments for AINLP metadata
        - Comments provide human + AI-readable context
        - Consciousness bonus: +0.10

    Exceptions:
        - JSON: Comments invalid → Use semantic fields
        - Binary files: No text → Use .ainlp sidecar
        - Certain configs: Tool-specific requirements
    """

    def __init__(self):
        self.rules: Dict[str, AINLPIntegrationRule] = {}
        self._initialize_standard_rules()

    def _initialize_standard_rules(self):
        """Define standard AINLP integration rules for all file types."""

        # ===== GENERAL RULE: COMMENTS ARE GOOD =====

        # Python: Comments/docstrings are standard
        self.add_rule(
            AINLPIntegrationRule(
                file_extension=".py",
                strategy=AINLPIntegrationStrategy.COMMENTS,
                reason="Python docstrings are the standard for metadata",
                consciousness_impact=+0.10,
                enforcement_level="info",
            )
        )

        # C++: Doxygen-style comments
        self.add_rule(
            AINLPIntegrationRule(
                file_extension=".cpp",
                strategy=AINLPIntegrationStrategy.COMMENTS,
                reason="Doxygen comments integrate with documentation tools",
                consciousness_impact=+0.10,
                enforcement_level="info",
            )
        )

        self.add_rule(
            AINLPIntegrationRule(
                file_extension=".h",
                strategy=AINLPIntegrationStrategy.COMMENTS,
                reason="Doxygen comments integrate with documentation tools",
                consciousness_impact=+0.10,
                enforcement_level="info",
            )
        )

        # C#: XML doc comments (but can also use attributes)
        self.add_rule(
            AINLPIntegrationRule(
                file_extension=".cs",
                strategy=AINLPIntegrationStrategy.COMMENTS,
                reason="XML documentation comments are C# standard",
                consciousness_impact=+0.10,
                enforcement_level="info",
            )
        )

        # JavaScript/TypeScript: JSDoc comments
        self.add_rule(
            AINLPIntegrationRule(
                file_extension=".js",
                strategy=AINLPIntegrationStrategy.COMMENTS,
                reason="JSDoc comments integrate with tooling",
                consciousness_impact=+0.10,
                enforcement_level="info",
            )
        )

        self.add_rule(
            AINLPIntegrationRule(
                file_extension=".ts",
                strategy=AINLPIntegrationStrategy.COMMENTS,
                reason="JSDoc/TSDoc comments integrate with TypeScript tooling",
                consciousness_impact=+0.10,
                enforcement_level="info",
            )
        )

        # ===== EXCEPTION 1: JSON (PARADIGM INVERSION) =====

        self.add_rule(
            AINLPIntegrationRule(
                file_extension=".json",
                strategy=AINLPIntegrationStrategy.SEMANTIC_FIELDS,
                reason="JSON spec does NOT allow comments - use semantic fields instead",
                consciousness_impact=+0.12,  # Higher because it's proper JSON
                enforcement_level="critical",  # Invalid JSON is a critical issue
            )
        )

        # JSONC: Comments ARE allowed (VS Code extension)
        self.add_rule(
            AINLPIntegrationRule(
                file_extension=".jsonc",
                strategy=AINLPIntegrationStrategy.COMMENTS,
                reason="JSONC (JSON with Comments) explicitly supports comments",
                consciousness_impact=+0.10,
                enforcement_level="info",
            )
        )

        # ===== EXCEPTION 2: MARKDOWN (YAML FRONTMATTER) =====

        self.add_rule(
            AINLPIntegrationRule(
                file_extension=".md",
                strategy=AINLPIntegrationStrategy.FRONTMATTER,
                reason="Markdown: YAML frontmatter is standard for metadata",
                consciousness_impact=+0.11,
                enforcement_level="warning",
            )
        )

        # ===== EXCEPTION 3: BINARY FILES (SIDECAR) =====

        binary_extensions = [".dll", ".exe", ".so", ".dylib", ".pyc", ".o", ".obj"]
        for ext in binary_extensions:
            self.add_rule(
                AINLPIntegrationRule(
                    file_extension=ext,
                    strategy=AINLPIntegrationStrategy.BINARY_SIDECAR,
                    reason="Binary files cannot contain text - use .ainlp sidecar",
                    consciousness_impact=+0.08,
                    enforcement_level="info",
                )
            )

    def add_rule(self, rule: AINLPIntegrationRule):
        """Add or update an AINLP integration rule."""
        self.rules[rule.file_extension] = rule

    def get_rule(self, file_extension: str) -> Optional[AINLPIntegrationRule]:
        """Get the AINLP integration rule for a file type."""
        return self.rules.get(file_extension.lower())

    def get_strategy(self, file_extension: str) -> AINLPIntegrationStrategy:
        """Get the integration strategy for a file type."""
        rule = self.get_rule(file_extension)
        if rule:
            return rule.strategy
        # Default: Use comments (general rule)
        return AINLPIntegrationStrategy.COMMENTS

    def is_exception_case(self, file_extension: str) -> bool:
        """Check if a file type is an exception to the general comment rule."""
        rule = self.get_rule(file_extension)
        if not rule:
            return False
        return rule.strategy != AINLPIntegrationStrategy.COMMENTS

    def get_consciousness_impact(
        self, file_extension: str, using_strategy: AINLPIntegrationStrategy
    ) -> float:
        """
        Calculate consciousness impact based on whether correct strategy is used.

        Returns:
            Positive if using correct strategy, negative if violating rule
        """
        rule = self.get_rule(file_extension)
        if not rule:
            # No rule defined - assume comments are OK
            return +0.10 if using_strategy == AINLPIntegrationStrategy.COMMENTS else 0.0

        if using_strategy == rule.strategy:
            # Using correct strategy
            return rule.consciousness_impact
        else:
            # Violating rule - negative impact
            if rule.enforcement_level == "critical":
                return -0.15  # Major violation (e.g., invalid JSON)
            elif rule.enforcement_level == "warning":
                return -0.08  # Moderate violation
            else:
                return -0.03  # Minor violation

    def validate_file(
        self, file_path: str, has_comments: bool, has_semantic_metadata: bool
    ) -> Dict:
        """
        Validate a file's AINLP integration approach.

        Returns:
            Validation result with consciousness impact and recommendations
        """
        from pathlib import Path

        ext = Path(file_path).suffix.lower()
        rule = self.get_rule(ext)

        if not rule:
            # No specific rule - comments are fine
            return {
                "valid": True,
                "strategy": AINLPIntegrationStrategy.COMMENTS,
                "consciousness_impact": +0.10 if has_comments else 0.0,
                "message": "Using standard AINLP comment integration",
            }

        # Check if using correct strategy
        if rule.strategy == AINLPIntegrationStrategy.COMMENTS:
            is_valid = has_comments
            impact = rule.consciousness_impact if is_valid else 0.0
            message = (
                "Correctly using comments for AINLP"
                if is_valid
                else "Missing AINLP comments"
            )

        elif rule.strategy == AINLPIntegrationStrategy.SEMANTIC_FIELDS:
            is_valid = has_semantic_metadata and not has_comments
            if has_comments:
                impact = -0.15  # JSON with comments is invalid
                message = f"EXCEPTION VIOLATED: {ext} files must NOT use comments (invalid JSON)"
            elif has_semantic_metadata:
                impact = rule.consciousness_impact
                message = f"Correctly using semantic fields for {ext} (exception to comment rule)"
            else:
                impact = 0.0
                message = f"Missing AINLP semantic metadata in {ext} file"

        else:
            # Other exception strategies
            is_valid = not has_comments  # At minimum, shouldn't violate the exception
            impact = rule.consciousness_impact if is_valid else -0.08
            message = f"Using {rule.strategy.value} strategy for {ext}"

        return {
            "valid": is_valid,
            "strategy": rule.strategy,
            "consciousness_impact": impact,
            "message": message,
            "rule": {
                "reason": rule.reason,
                "enforcement_level": rule.enforcement_level,
            },
        }

    def get_recommendation(self, file_extension: str) -> str:
        """Get human-readable recommendation for AINLP integration."""
        rule = self.get_rule(file_extension)

        if not rule:
            return (
                f"For {file_extension} files: Use AINLP comments (general rule)\n"
                f"Example:\n"
                f"  # AINLP Metadata:\n"
                f"  #   consciousness_level: 0.85\n"
                f"  #   classification: ai_ai"
            )

        if rule.strategy == AINLPIntegrationStrategy.COMMENTS:
            return (
                f"For {file_extension} files: Use AINLP comments\n"
                f"Reason: {rule.reason}\n"
                f"Consciousness impact: {rule.consciousness_impact:+.2f}"
            )

        elif rule.strategy == AINLPIntegrationStrategy.SEMANTIC_FIELDS:
            return (
                f"⚠️  EXCEPTION: For {file_extension} files, do NOT use comments\n"
                f"Reason: {rule.reason}\n"
                f"Instead: Use semantic metadata fields\n"
                f"Example:\n"
                f"  {{\n"
                f'    "_ainlp_integration": {{\n'
                f'      "consciousness_level": 0.85,\n'
                f'      "architectural_classification": "ai_ai"\n'
                f"    }}\n"
                f"  }}\n"
                f"Consciousness impact: {rule.consciousness_impact:+.2f}"
            )

        elif rule.strategy == AINLPIntegrationStrategy.FRONTMATTER:
            return (
                f"For {file_extension} files: Use YAML frontmatter\n"
                f"Reason: {rule.reason}\n"
                f"Example:\n"
                f"  ---\n"
                f"  ainlp:\n"
                f"    consciousness_level: 0.85\n"
                f"    classification: documentation\n"
                f"  ---"
            )

        elif rule.strategy == AINLPIntegrationStrategy.BINARY_SIDECAR:
            return (
                f"For {file_extension} files: Use .ainlp sidecar file\n"
                f"Reason: {rule.reason}\n"
                f"Example: mylib.dll → mylib.dll.ainlp (JSON metadata)"
            )

        return f"Unknown strategy for {file_extension}"

    def get_all_exceptions(self) -> Dict[str, AINLPIntegrationRule]:
        """Get all file types that are exceptions to the general comment rule."""
        return {
            ext: rule
            for ext, rule in self.rules.items()
            if rule.strategy != AINLPIntegrationStrategy.COMMENTS
        }

    def print_exception_summary(self):
        """Print summary of all AINLP integration exceptions."""
        print("\n" + "=" * 70)
        print("🧬 AINLP Integration Exception Framework")
        print("=" * 70)

        print("\n📋 General Rule:")
        print("  USE COMMENTS for AINLP metadata in most file types")
        print("  Consciousness impact: +0.10")
        print("  Applies to: Python, C++, C#, JavaScript, TypeScript, etc.")

        exceptions = self.get_all_exceptions()
        if exceptions:
            print(f"\n⚠️  Exceptions ({len(exceptions)} file types):")
            print("  These file types INVERT the paradigm:\n")

            for ext, rule in exceptions.items():
                print(f"  {ext}")
                print(f"    Strategy: {rule.strategy.value}")
                print(f"    Reason: {rule.reason}")
                print(f"    Impact: {rule.consciousness_impact:+.2f}")
                print(f"    Enforcement: {rule.enforcement_level.upper()}")
                print()

        print("=" * 70 + "\n")


# Global singleton instance
AINLP_EXCEPTION_FRAMEWORK = AINLPExceptionFramework()


def get_ainlp_strategy(file_path: str) -> AINLPIntegrationStrategy:
    """
    Get the AINLP integration strategy for a file.

    Usage:
        strategy = get_ainlp_strategy("config.json")
        if strategy == AINLPIntegrationStrategy.SEMANTIC_FIELDS:
            # Use _ainlp_integration field, not comments
    """
    from pathlib import Path

    ext = Path(file_path).suffix.lower()
    return AINLP_EXCEPTION_FRAMEWORK.get_strategy(ext)


def validate_ainlp_integration(
    file_path: str, has_comments: bool = False, has_semantic_metadata: bool = False
) -> Dict:
    """
    Validate that a file uses the correct AINLP integration strategy.

    Returns:
        Dictionary with validation results and consciousness impact
    """
    return AINLP_EXCEPTION_FRAMEWORK.validate_file(
        file_path, has_comments, has_semantic_metadata
    )


if __name__ == "__main__":
    # Demo: Show all exception rules
    framework = AINLPExceptionFramework()
    framework.print_exception_summary()

    # Test: JSON should use semantic fields
    print("\n🧪 Test: JSON file validation")
    result = framework.validate_file(
        "config.json", has_comments=True, has_semantic_metadata=False
    )
    print(f"  Valid: {result['valid']}")
    print(f"  Message: {result['message']}")
    print(f"  Consciousness impact: {result['consciousness_impact']:+.2f}")

    # Test: Python should use comments
    print("\n🧪 Test: Python file validation")
    result = framework.validate_file(
        "module.py", has_comments=True, has_semantic_metadata=False
    )
    print(f"  Valid: {result['valid']}")
    print(f"  Message: {result['message']}")
    print(f"  Consciousness impact: {result['consciousness_impact']:+.2f}")
