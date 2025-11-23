"""
Quick test script for autonomous quality monitor.

Tests scanning only (no fixing) to debug performance issues.
"""

import asyncio
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from coordination.autonomous_quality_monitor import AutonomousQualityMonitor


async def test_scan_only():
    """Test scan without fixing to isolate performance issues"""
    
    # Use AIOS workspace, not entire C:\ drive!
    workspace = Path("C:/AIOS")
    print(f"[TEST] Workspace: {workspace}")
    
    # Create monitor with auto_fix=False (scan only)
    monitor = AutonomousQualityMonitor(
        workspace_root=workspace,
        auto_fix=False,  # SCAN ONLY
        max_cost_per_hour=0.0,  # No cost
        escalation_threshold=999  # Don't escalate
    )
    
    try:
        print("[TEST] Starting scan-only test...")
        result = await monitor.scan_and_fix()
        
        print("\n[TEST] Scan Results:")
        print(f"  Issues detected: {result['issues_detected']}")
        print(f"  Auto-fixed: {result['auto_fixed']}")
        print(f"  Escalated: {result['escalated']}")
        print(f"  Cost: ${result['cost']['total']}")
        
        return result
        
    finally:
        await monitor.close()


if __name__ == "__main__":
    print("[TEST] Autonomous Quality Monitor - Scan Only Test")
    print("[TEST] This will scan workspace for issues WITHOUT fixing them\n")
    
    result = asyncio.run(test_scan_only())
    
    print(f"\n[TEST] ✓ Test complete - found {result['issues_detected']} issue(s)")
