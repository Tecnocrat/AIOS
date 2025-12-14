#!/usr/bin/env python3
"""
Test AINLP directive compliance for harmonized requirements.txt
"""

from pathlib import Path
from aios_core_evolution_monitor import AIOSFileDirectiveChecker


def test_requirements_compliance():
    """Test the harmonized requirements.txt against AINLP directives."""
    # Initialize checker with root AIOS path since requirements.txt is at root level
    root_path = Path(r"c:\dev\AIOS")
    checker = AIOSFileDirectiveChecker(root_path)

    test_file = root_path / "requirements.txt"
    result = checker.check_file_directive_compliance(test_file)

    print("AINLP Directive Compliance Test for requirements.txt")
    print("=" * 60)
    print(f"File: {result['file_name']}")
    print(".2f")
    print()
    print("Directive Analysis:")
    for directive in result["directives_checked"]:
        print(".2f")
    print()
    print(f"Violations Found: {len(result['violations'])}")
    if result["violations"]:
        for violation in result["violations"]:
            print(f"  - {violation}")
    print()
    print(f"Recommendations: {len(result['recommendations'])}")
    if result["recommendations"]:
        for rec in result["recommendations"]:
            print(f"  - {rec}")

    return result


if __name__ == "__main__":
    test_requirements_compliance()
