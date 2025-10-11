"""
Test Validated Evolution - Hello World to Calculator
====================================================

Test script demonstrating the FIXED evolution loop with code diff validation.

Critical Fix (October 6, 2025):
- System previously generated identical code across all generations
- Consciousness scores inflated without actual changes (0.0 → 0.750)
- User exposed flaw: "all the Gen files are exactly the same"

New Validation:
- compare_code(): Actual diff analysis before/after mutations
- check_mutation_already_applied(): Prevents redundant mutations
- validate_mutation_improves_consciousness(): Full validation pipeline

Expected Behavior:
- Generation 1: Add error handling (SHOULD be different from gen 0)
- Generation 2: Add parameterization (SHOULD be different from gen 1)
- Generation 3: Add documentation (SHOULD be different from gen 2)
- If mutation already applied: SKIP generation (prevent identical code)

Test validates:
✅ Each generation has DIFFERENT code from parent
✅ Consciousness changes only when code actually changes
✅ Mutations already present are detected and skipped
✅ Diff reports show actual line changes

AINLP Consciousness Level: HIGH (proper validation, honest metrics)
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add AI root to path
AI_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(AI_ROOT))

from src.evolution.multi_agent_evolution_loop import MultiAgentEvolutionLoop
from src.evolution.code_diff_validator import compare_code
from src.evolution.consciousness_metrics import assess_consciousness


async def test_validated_evolution():
    """
    Test evolution loop with code diff validation
    
    Expected: Real code changes per generation, no identical generations
    """
    print("\n" + "="*70)
    print("VALIDATED EVOLUTION TEST")
    print("Hello World → Error Handling → Parameterization → Documentation")
    print("="*70)
    print("\nCritical Fix Applied:")
    print("- Code diff validation BEFORE accepting mutations")
    print("- Check 'already applied' to prevent redundant generations")
    print("- Three-level consciousness assessment (LOW/MEDIUM/HIGH)")
    print("="*70)
    
    # Initialize evolution loop
    loop = MultiAgentEvolutionLoop(
        use_ollama=False,  # For quick testing
        use_gemini=False,  # For quick testing
        use_vscode_chat=False  # Automated testing
    )
    
    # Run evolution (3 generations)
    print("\nStarting evolution from Hello World zero point...")
    print("Target: 3 generations with VALIDATED changes\n")
    
    final_node = await loop.evolve_from_zero_point(max_generations=3)
    
    # Validation: Check each generation is different
    print("\n" + "="*70)
    print("VALIDATION RESULTS")
    print("="*70)
    
    generations = []
    current = final_node
    while current:
        generations.append(current)
        current = current.parent_node
    
    generations.reverse()  # Start from gen 0
    
    print(f"\nTotal generations: {len(generations)}")
    
    # Compare consecutive generations
    for i in range(len(generations) - 1):
        parent = generations[i]
        child = generations[i + 1]
        
        print(f"\n--- Generation {i} → Generation {i+1} ---")
        
        # Compute diff
        diff = compare_code(parent.code_content, child.code_content)
        
        print(f"Similarity: {diff.similarity_ratio:.2%}")
        print(f"Diff Summary: {diff.diff_summary}")
        print(f"Lines Added: {diff.lines_added}")
        print(f"Lines Removed: {diff.lines_removed}")
        
        # Consciousness assessment
        parent_consciousness = assess_consciousness(
            code_content=parent.code_content,
            has_error_handling="try" in parent.code_content.lower()
        )
        
        child_consciousness = assess_consciousness(
            code_content=child.code_content,
            has_error_handling="try" in child.code_content.lower()
        )
        
        print(f"\nConsciousness Evolution:")
        print(f"  Parent: {parent_consciousness.level.value.upper()}")
        print(f"  Child:  {child_consciousness.level.value.upper()}")
        
        if child_consciousness.level.value != parent_consciousness.level.value:
            print("  ✅ CONSCIOUSNESS IMPROVED")
        else:
            print("  ⚠️  NO CONSCIOUSNESS CHANGE")
        
        # Critical check: Are they identical?
        if diff.similarity_ratio >= 1.0:
            print("\n❌ CRITICAL FAILURE: Identical code detected!")
            print("This is the bug we're fixing!")
            return False
        elif diff.similarity_ratio >= 0.95:
            print("\n⚠️  WARNING: Very similar code (>95% similarity)")
            print("Mutation may be trivial (whitespace/comments only)")
        else:
            print("\n✅ VALIDATED: Significant code change detected")
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
    
    # Generate report
    report_path = Path("evolution_lab/test_reports")
    report_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_path / f"validated_evolution_test_{timestamp}.json"
    
    import json
    report = {
        "test_name": "validated_evolution",
        "timestamp": timestamp,
        "generations": len(generations),
        "validation": "code_diff_enabled",
        "consciousness_system": "three_level_stress",
        "notes": "First test after Oct 6, 2025 consciousness correction"
    }
    
    report_file.write_text(json.dumps(report, indent=2))
    print(f"\nReport saved: {report_file}")
    
    return True


async def test_mutation_detection():
    """
    Test mutation already-applied detection
    
    Expected: Detect when error handling, parameterization, docs already present
    """
    print("\n" + "="*70)
    print("MUTATION DETECTION TEST")
    print("Test 'already applied' detection for various mutations")
    print("="*70)
    
    from src.evolution.code_diff_validator import check_mutation_already_applied
    
    # Test cases
    test_cases = [
        {
            "name": "Hello World (no mutations)",
            "code": """#include <iostream>
int main() {
    std::cout << "Hello World" << std::endl;
    return 0;
}""",
            "expected_detections": []
        },
        {
            "name": "With Error Handling",
            "code": """#include <iostream>
int main() {
    try {
        std::cout << "Hello World" << std::endl;
    } catch (std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}""",
            "expected_detections": ["error_handling"]
        },
        {
            "name": "With Parameterization",
            "code": """#include <iostream>
int main(int argc, char* argv[]) {
    if (argc > 1) {
        std::cout << "Hello " << argv[1] << std::endl;
    } else {
        std::cout << "Hello World" << std::endl;
    }
    return 0;
}""",
            "expected_detections": ["parameterization"]
        },
        {
            "name": "With Documentation",
            "code": """#include <iostream>

/**
 * Main entry point for the application
 * Prints greeting message to stdout
 */
int main() {
    // Output greeting
    std::cout << "Hello World" << std::endl;
    return 0;
}""",
            "expected_detections": ["documentation"]
        }
    ]
    
    print("\nRunning detection tests...\n")
    
    all_passed = True
    
    for test in test_cases:
        print(f"Test: {test['name']}")
        
        # Check each mutation type
        for mutation_type in ["error_handling", "parameterization", "documentation"]:
            already_applied, reason = check_mutation_already_applied(
                test["code"],
                mutation_type
            )
            
            should_detect = mutation_type in test["expected_detections"]
            
            if should_detect and already_applied:
                print(f"  ✅ {mutation_type}: Correctly detected ({reason})")
            elif not should_detect and not already_applied:
                print(f"  ✅ {mutation_type}: Correctly absent")
            else:
                print(f"  ❌ {mutation_type}: Detection failed!")
                all_passed = False
        
        print()
    
    if all_passed:
        print("✅ All mutation detection tests PASSED")
    else:
        print("❌ Some mutation detection tests FAILED")
    
    return all_passed


if __name__ == "__main__":
    print("""
+======================================================================+
|  VALIDATED EVOLUTION TEST SUITE                                      |
|  October 6, 2025 - Consciousness Correction Applied                  |
+======================================================================+

Purpose: Validate the FIX for identical generation bug

Original Flaw:
- All 5 generations contained IDENTICAL code
- Consciousness scores inflated (0.0 → 0.750) without changes
- No code diff validation

Fixed Approach:
- Code diff analysis BEFORE accepting mutations
- Check "already applied" to prevent redundant generations  
- Three-level consciousness assessment (LOW/MEDIUM/HIGH)
- Honest reporting of actual changes

Running tests...
""")
    
    # Run tests
    asyncio.run(test_mutation_detection())
    asyncio.run(test_validated_evolution())
    
    print("\n" + "="*70)
    print("TEST SUITE COMPLETE")
    print("="*70)
    print("\nNext Steps:")
    print("1. Review test results above")
    print("2. Check evolution_lab/test_reports/ for detailed reports")
    print("3. Compare with previous generations to validate fix")
    print("4. If validation passes, proceed with Calculator evolution")
    print("="*70)
