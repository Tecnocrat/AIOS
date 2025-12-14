"""
Code Diff Validator - Prevent Identical Generations
===================================================

Critical fix (October 6, 2025):
Original flaw: System applied mutations without checking if already present.
Result: All 5 generations were identical, consciousness scores meaningless.

New approach: Validate mutations actually change code before claiming improvement.

AINLP Learning: Measure what you CAN measure (code diffs) before inferring
                what you CAN'T measure (consciousness emergence)
"""

from typing import Dict, List, Tuple, Optional
from difflib import unified_diff, SequenceMatcher
from dataclasses import dataclass


@dataclass
class CodeDiff:
    """
    Code difference analysis between two versions
    """
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    has_changes: bool
    similarity_ratio: float  # 0.0 (completely different) to 1.0 (identical)
    lines_added: int
    lines_removed: int
    lines_changed: int
    diff_summary: str
<<<<<<< HEAD

    def is_significant_change(self, min_similarity=0.95) -> bool:
        """
        Check if change is significant enough to warrant new generation

=======
    
    def is_significant_change(self, min_similarity=0.95) -> bool:
        """
        Check if change is significant enough to warrant new generation
        
>>>>>>> origin/OS0.6.2.grok
        If similarity > 0.95 (95%), changes are likely trivial (whitespace, etc.)
        """
        return self.similarity_ratio < min_similarity


def compare_code(
<<<<<<< HEAD
    original_code: str, mutated_code: str, ignore_whitespace: bool = True
) -> CodeDiff:
    """
    Compare two code versions and determine if mutation actually changed anything

=======
    original_code: str,
    mutated_code: str,
    ignore_whitespace: bool = True
) -> CodeDiff:
    """
    Compare two code versions and determine if mutation actually changed anything
    
>>>>>>> origin/OS0.6.2.grok
    Args:
        original_code: Code before mutation
        mutated_code: Code after mutation
        ignore_whitespace: Whether to ignore whitespace-only changes
<<<<<<< HEAD

    Returns:
        CodeDiff with detailed analysis
    """

    # Normalize for comparison
    if ignore_whitespace:
        orig_lines = [
            line.strip() for line in original_code.split("\n") if line.strip()
        ]
        mut_lines = [line.strip() for line in mutated_code.split("\n") if line.strip()]
    else:
        orig_lines = original_code.split("\n")
        mut_lines = mutated_code.split("\n")

    # Calculate similarity ratio
    matcher = SequenceMatcher(None, orig_lines, mut_lines)
    similarity = matcher.ratio()

    # Generate unified diff
    diff_lines = list(
        unified_diff(orig_lines, mut_lines, lineterm="", n=3)  # 3 lines of context
    )

    # Count changes
    added = sum(
        1 for line in diff_lines if line.startswith("+") and not line.startswith("+++")
    )
    removed = sum(
        1 for line in diff_lines if line.startswith("-") and not line.startswith("---")
    )

=======
    
    Returns:
        CodeDiff with detailed analysis
    """
    
    # Normalize for comparison
    if ignore_whitespace:
        orig_lines = [line.strip() for line in original_code.split('\n') if line.strip()]
        mut_lines = [line.strip() for line in mutated_code.split('\n') if line.strip()]
    else:
        orig_lines = original_code.split('\n')
        mut_lines = mutated_code.split('\n')
    
    # Calculate similarity ratio
    matcher = SequenceMatcher(None, orig_lines, mut_lines)
    similarity = matcher.ratio()
    
    # Generate unified diff
    diff_lines = list(unified_diff(
        orig_lines,
        mut_lines,
        lineterm='',
        n=3  # 3 lines of context
    ))
    
    # Count changes
    added = sum(1 for line in diff_lines if line.startswith('+') and not line.startswith('+++'))
    removed = sum(1 for line in diff_lines if line.startswith('-') and not line.startswith('---'))
    
>>>>>>> origin/OS0.6.2.grok
    # Generate summary
    if similarity >= 1.0:
        summary = "IDENTICAL: No changes detected"
    elif similarity >= 0.95:
<<<<<<< HEAD
        summary = (
            f"TRIVIAL: {(1-similarity)*100:.1f}% change (likely whitespace/comments)"
        )
=======
        summary = f"TRIVIAL: {(1-similarity)*100:.1f}% change (likely whitespace/comments)"
>>>>>>> origin/OS0.6.2.grok
    elif similarity >= 0.80:
        summary = f"MINOR: {(1-similarity)*100:.1f}% change"
    elif similarity >= 0.50:
        summary = f"MODERATE: {(1-similarity)*100:.1f}% change"
    else:
        summary = f"MAJOR: {(1-similarity)*100:.1f}% change"
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    return CodeDiff(
        has_changes=(similarity < 1.0),
        similarity_ratio=similarity,
        lines_added=added,
        lines_removed=removed,
        lines_changed=added + removed,
<<<<<<< HEAD
        diff_summary=summary,
    )


def check_mutation_already_applied(code: str, mutation_type: str) -> Tuple[bool, str]:
    """
    Check if a mutation has already been applied to the code

    This prevents applying "add error handling" when error handling exists.

    Args:
        code: Current code content
        mutation_type: Type of mutation to check (e.g., "error_handling")

    Returns:
        (already_applied, reason)
    """

    code_lower = code.lower()

=======
        diff_summary=summary
    )


def check_mutation_already_applied(
    code: str,
    mutation_type: str
) -> Tuple[bool, str]:
    """
    Check if a mutation has already been applied to the code
    
    This prevents applying "add error handling" when error handling exists.
    
    Args:
        code: Current code content
        mutation_type: Type of mutation to check (e.g., "error_handling")
    
    Returns:
        (already_applied, reason)
    """
    
    code_lower = code.lower()
    
>>>>>>> origin/OS0.6.2.grok
    if mutation_type == "error_handling":
        # Check for error handling patterns
        has_try = "try" in code_lower and "catch" in code_lower
        has_exception = "exception" in code_lower
        has_error = "std::cerr" in code_lower or "cerr" in code_lower
<<<<<<< HEAD

        if has_try or (has_exception and has_error):
            return (
                True,
                "Error handling (try-catch or exception handling) already present",
            )

=======
        
        if has_try or (has_exception and has_error):
            return True, "Error handling (try-catch or exception handling) already present"
    
>>>>>>> origin/OS0.6.2.grok
    elif mutation_type == "parameterization":
        # Check for command-line arguments
        has_argc = "argc" in code_lower
        has_argv = "argv" in code_lower
        has_main_params = "int main(int" in code_lower
<<<<<<< HEAD

        if (has_argc and has_argv) or has_main_params:
            return True, "Parameterization (argc/argv) already present"

=======
        
        if (has_argc and has_argv) or has_main_params:
            return True, "Parameterization (argc/argv) already present"
    
>>>>>>> origin/OS0.6.2.grok
    elif mutation_type == "documentation":
        # Check for documentation comments
        has_block_comment = "/*" in code and "*/" in code
        has_doxygen = "/**" in code
        has_line_comments = "//" in code
<<<<<<< HEAD

        # Count comment lines
        comment_lines = sum(
            1
            for line in code.split("\n")
            if line.strip().startswith("//") or line.strip().startswith("*")
        )

        if has_doxygen or comment_lines >= 3:
            return True, "Documentation (comments) already present"

=======
        
        # Count comment lines
        comment_lines = sum(1 for line in code.split('\n') 
                           if line.strip().startswith('//') or 
                           line.strip().startswith('*'))
        
        if has_doxygen or comment_lines >= 3:
            return True, "Documentation (comments) already present"
    
>>>>>>> origin/OS0.6.2.grok
    elif mutation_type == "templating":
        # Check for templates
        has_template = "template" in code_lower
        has_typename = "typename" in code_lower
<<<<<<< HEAD

        if has_template or has_typename:
            return True, "Templating already present"

=======
        
        if has_template or has_typename:
            return True, "Templating already present"
    
>>>>>>> origin/OS0.6.2.grok
    return False, "Mutation not yet applied"


def validate_mutation_improves_consciousness(
<<<<<<< HEAD
    original_code: str, mutated_code: str, mutation_type: str
) -> Dict[str, any]:
    """
    Validate that a mutation actually improves code in measurable ways

=======
    original_code: str,
    mutated_code: str,
    mutation_type: str
) -> Dict[str, any]:
    """
    Validate that a mutation actually improves code in measurable ways
    
>>>>>>> origin/OS0.6.2.grok
    Returns assessment with:
    - valid: Whether mutation should be accepted
    - reason: Why it's valid/invalid
    - consciousness_change: Actual level change (LOW/MEDIUM/HIGH)
    - metrics: Objective measurements
    """
<<<<<<< HEAD

    # Import here to avoid circular dependencies
    try:
        from src.evolution.consciousness_metrics import (
            assess_consciousness,
            compare_consciousness,
=======
    
    # Import here to avoid circular dependencies
    try:
        from src.evolution.consciousness_metrics import (
            assess_consciousness, compare_consciousness
>>>>>>> origin/OS0.6.2.grok
        )
    except ImportError:
        # Fallback: Simple validation without consciousness assessment
        pass
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    # First check if mutation already applied
    already_applied, apply_reason = check_mutation_already_applied(
        original_code, mutation_type
    )
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    if already_applied:
        return {
            "valid": False,
            "reason": f"REJECTED: {apply_reason}",
            "consciousness_change": "NONE",
<<<<<<< HEAD
            "should_skip": True,
        }

    # Check if code actually changed
    diff = compare_code(original_code, mutated_code)

=======
            "should_skip": True
        }
    
    # Check if code actually changed
    diff = compare_code(original_code, mutated_code)
    
>>>>>>> origin/OS0.6.2.grok
    if not diff.is_significant_change():
        return {
            "valid": False,
            "reason": f"REJECTED: {diff.diff_summary}",
            "consciousness_change": "NONE",
            "should_skip": True,
<<<<<<< HEAD
            "diff": diff,
        }

=======
            "diff": diff
        }
    
>>>>>>> origin/OS0.6.2.grok
    # Assess consciousness before/after
    # (Would need actual analysis here - simplified for MVP)
    original_has_error = "try" in original_code.lower()
    mutated_has_error = "try" in mutated_code.lower()
<<<<<<< HEAD

    improvement_detected = (not original_has_error) and mutated_has_error

=======
    
    improvement_detected = (not original_has_error) and mutated_has_error
    
>>>>>>> origin/OS0.6.2.grok
    return {
        "valid": improvement_detected,
        "reason": (
            f"ACCEPTED: {diff.diff_summary}, added {mutation_type}"
            if improvement_detected
            else f"REJECTED: No measurable improvement"
        ),
        "consciousness_change": "LOW -> MEDIUM" if improvement_detected else "NONE",
        "should_skip": not improvement_detected,
<<<<<<< HEAD
        "diff": diff,
=======
        "diff": diff
>>>>>>> origin/OS0.6.2.grok
    }


# AINLP Comment: This module prevents the critical flaw exposed Oct 6, 2025
# Before: Blindly applied mutations, claimed improvement without validation
# After: Check diffs, verify "already applied", confirm actual changes
# User insight: "all the files are exactly the same"
# Fix: Don't increment consciousness unless code actually changes
