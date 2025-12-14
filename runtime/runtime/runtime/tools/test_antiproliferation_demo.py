"""
AINLP Dendritic Discovery Anti-Proliferation Demo
=================================================

Demonstrates the anti-proliferation system preventing duplicate file creation.
"""

import subprocess


def run_similarity_check(description):
    """Run anti-proliferation check."""
    cmd = [
        'python', 'runtime/tools/ainlp_dendritic_discovery.py',
        '--check-similar', description
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


# Test scenarios
test_scenarios = [
    {
        "description": "tool for system health monitoring and diagnostics",
        "expected_match": "runtime tools for health checking",
        "category": "monitoring"
    },
    {
        "description": "AINLP dendritic intelligence pattern analyzer",
        "expected_match": "ainlp_dendritic_enhancer.py or similar",
        "category": "ainlp_patterns"
    },
    {
        "description": "module discovery and import analysis tool",
        "expected_match": "module_discoverer.py",
        "category": "code_analysis"
    },
    {
        "description": "tachyonic archive visualization with 3D rendering",
        "expected_match": "tachyonic_visualizer.py",
        "category": "visualization"
    },
    {
        "description": (
            "completely novel quantum entanglement simulator for AIOS"
        ),
        "expected_match": "None - should allow creation",
        "category": "novel"
    }
]

print("="*70)
print("AINLP DENDRITIC DISCOVERY - ANTI-PROLIFERATION DEMONSTRATION")
print("="*70)
print("\nTesting file creation prevention system...")
print(f"Total test scenarios: {len(test_scenarios)}\n")

for i, scenario in enumerate(test_scenarios, 1):
    print(f"\n{'='*70}")
    print(f"Test {i}/{len(test_scenarios)}: {scenario['category'].upper()}")
    print(f"{'='*70}")
    print(f"Proposed: \"{scenario['description']}\"")
    print(f"Expected match: {scenario['expected_match']}")
    print()

    output = run_similarity_check(scenario['description'])

    # Extract recommendation
    for line in output.split('\n'):
        if 'RECOMMENDATION:' in line:
            recommendation = line.split('RECOMMENDATION:')[1].strip()
            print(f"Result: {recommendation}")

            # Color code based on recommendation
            if 'ENHANCE' in recommendation:
                print(
                    "✅ ANTI-PROLIFERATION WORKING - "
                    "File creation prevented"
                )
            elif 'CONSIDER' in recommendation or 'REVIEW' in recommendation:
                print(
                    "⚠️  WARNING ISSUED - "
                    "Similar functionality detected"
                )
            else:
                print(
                    "✓ Creation allowed - "
                    "No similar functionality found"
                )
            break

    # Show top match if found
    lines = output.split('\n')
    for i, line in enumerate(lines):
        if 'Path:' in line:
            path = line.split('Path:')[1].strip()
            if i+2 < len(lines) and 'Similarity:' in lines[i+2]:
                sim = lines[i+2].split('Similarity:')[1].strip()
                print(f"Match found: {path} ({sim})")
            break

print(f"\n\n{'='*70}")
print("SUMMARY")
print(f"{'='*70}")
print("""
The AINLP Dendritic Discovery engine:

1. Scans all existing code modules (neurons) across AIOS supercells
2. Analyzes similarity using keyword overlap + docstring analysis
3. Prevents file proliferation by recommending enhancement of existing files
4. Logs all creation checks to database for pattern analysis

Thresholds:
- ≥70%: ENHANCE_EXISTING (prevents creation)
- ≥40%: CONSIDER_ENHANCEMENT (warning)
- ≥30%: REVIEW_EXISTING (informational)
- <30%: CREATE (allows new file)

This enforces the AINLP principle of enhancement over creation, preventing
the anti-pattern of AI agents spawning new files unnecessarily.
""")
