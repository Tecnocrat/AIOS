"""
Test Autonomous Monitor - Auto-Fix Mode with GitHub Models

Tests GPT-4o-mini (Tier 2) fixing E501 violations automatically.
Creates a temporary test file with known E501 issues, monitors it,
verifies fixes are applied correctly, and tracks cost.

Requirements:
- GITHUB_TOKEN environment variable set
- GitHub Models API access enabled
"""

import asyncio
import sys
import tempfile
from pathlib import Path

# Fix Windows console encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Add ai/ to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "ai"))

from coordination.autonomous_quality_monitor import AutonomousQualityMonitor


TEST_FILE_CONTENT = '''"""
Test file with E501 violations for autonomous monitor testing.
"""

def very_long_function_with_extremely_verbose_parameter_names_that_definitely_exceeds_79_characters(param1, param2):
    """This function has an E501 violation in its signature."""
    result = param1 + param2
    return result

class VeryLongClassName_ThatExceedsTheLineLength_AndNeedsToBeFixed_ForAINLP_Compliance_Testing:
    """This class name is way too long and violates E501."""
    pass

# Another E501: This comment line is intentionally very long to test the autonomous monitor's ability to detect and fix line length violations
x = 1
'''


async def test_autofix():
    """Test autonomous monitor with auto-fix enabled."""
    print("\n" + "="*60)
    print("[TEST] Autonomous Quality Monitor - Auto-Fix Mode")
    print("[TEST] Testing GPT-4o-mini (Tier 2) E501 fixing")
    print("="*60 + "\n")
    
    # Create temporary test file
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        dir=Path(__file__).parent / "coordination",
        delete=False,
        encoding='utf-8'
    ) as f:
        test_file = Path(f.name)
        f.write(TEST_FILE_CONTENT)
    
    print(f"[TEST] Created test file: {test_file}")
    print(f"[TEST] File contains 3 known E501 violations\n")
    
    try:
        # Initialize monitor with auto-fix enabled
        monitor = AutonomousQualityMonitor(
            workspace_root=Path(__file__).parent.parent,
            auto_fix=True,  # Enable GitHub Models fixing
            max_cost_per_hour=0.50
        )
        
        print("[TEST] Starting autonomous monitor scan with auto-fix...")
        print("[TEST] This will call GitHub Models GPT-4o-mini API\n")
        
        # Run single scan cycle
        result = await monitor.scan_and_fix()
        
        # Print results
        print("\n" + "="*60)
        print("[TEST] Auto-Fix Results:")
        print("="*60)
        print(f"  Issues detected: {result['issues_detected']}")
        print(f"  Auto-fixed: {result['auto_fixed']}")
        print(f"  Escalated: {result['escalated']}")
        print(f"  Cost total: ${result['cost']['total']:.4f}")
        print(f"  Cost this hour: ${result['cost']['this_hour']:.4f}")
        print(f"  Auto-fix rate: {result['auto_fix_rate']:.1%}")
        print("="*60 + "\n")
        
        # Read fixed file
        fixed_content = test_file.read_text(encoding='utf-8')
        
        print("[TEST] Fixed file content:")
        print("-" * 60)
        print(fixed_content)
        print("-" * 60 + "\n")
        
        # Validate fixes
        lines_over_79 = [
            i+1 for i, line in enumerate(fixed_content.split('\n'))
            if len(line) > 79
        ]
        
        if lines_over_79:
            print(f"⚠️  Still has E501 on lines: {lines_over_79}")
            print("   (GPT-4o-mini may need better prompt)")
        else:
            print("✅ All E501 violations fixed!")
        
        # Cost analysis
        cost_total = result['cost']['total']
        if cost_total > 0.01:
            print(f"\n⚠️  Cost ${cost_total:.4f} > $0.01 target")
        else:
            print(f"\n✅ Cost ${cost_total:.4f} within budget")
        
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()
            print(f"\n[TEST] Cleaned up: {test_file}")


if __name__ == "__main__":
    asyncio.run(test_autofix())
