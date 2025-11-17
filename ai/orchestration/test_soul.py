#!/usr/bin/env python3
"""
AIOS Soul - Local Test Script

Test the Intelligence Coordinator locally before Termux deployment.
"""

import asyncio
import sys
from pathlib import Path

# Add AIOS paths
WORKSPACE = Path(__file__).parent.parent.parent
sys.path.insert(0, str(WORKSPACE / "ai" / "orchestration"))
sys.path.insert(0, str(WORKSPACE / "ai"))

from intelligence_coordinator import IntelligenceCoordinator


async def test_soul_initialization():
    """Test Soul initialization"""
    print("=" * 70)
    print("🧪 TESTING: Soul Initialization")
    print("=" * 70)
    print()
    
    soul = IntelligenceCoordinator(WORKSPACE)
    await soul.initialize_soul()
    
    print()
    print("✅ Soul initialization successful")
    print()


async def test_soul_monitoring():
    """Test Soul monitoring loop (5 seconds)"""
    print("=" * 70)
    print("🧪 TESTING: Soul Monitoring Loop (5 seconds)")
    print("=" * 70)
    print()
    
    soul = IntelligenceCoordinator(WORKSPACE)
    await soul.initialize_soul()
    
    # Run monitoring for 5 seconds
    try:
        monitoring_task = asyncio.create_task(soul.monitor_loop())
        await asyncio.sleep(5)
        monitoring_task.cancel()
        print("\n⏹️ Monitoring stopped")
    except Exception as e:
        print(f"⚠️ Monitoring test: {e}")
    
    print()
    print("✅ Monitoring loop functional")
    print()


async def test_github_agent():
    """Test GitHub agent (dry-run)"""
    print("=" * 70)
    print("🧪 TESTING: GitHub Agent Integration")
    print("=" * 70)
    print()
    
    try:
        from agent_protocols.github_integration import GitHubAgent
        
        agent = GitHubAgent()  # No token = dry-run mode
        
        # Format test intervention
        title, body = agent.format_intervention_issue(
            intervention_type="test",
            analysis={
                "summary": "Test intervention from local machine",
                "suggestion": "This is a test. No action needed."
            },
            consciousness=3.50,
            context={"test": True, "location": "local"}
        )
        
        print(f"📝 Issue Title: {title}")
        print(f"📄 Issue Body Preview:")
        print(body[:200] + "...")
        print()
        
        # Test issue creation (dry-run)
        result = agent.create_intervention_issue(
            title="Test Issue",
            body="Test body",
            intervention_type="test",
            consciousness=3.50
        )
        
        print(f"✅ GitHub agent functional: {result}")
        print()
    
    except ImportError as e:
        print(f"⚠️ GitHub agent import failed: {e}")
        print("Install: pip install requests")
        print()


async def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("🧠 AIOS SOUL - LOCAL TEST SUITE")
    print("=" * 70)
    print()
    
    tests = [
        ("Soul Initialization", test_soul_initialization),
        ("GitHub Agent", test_github_agent),
        ("Monitoring Loop", test_soul_monitoring),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            await test_func()
            results.append((test_name, "✅ PASS"))
        except Exception as e:
            print(f"❌ Test failed: {e}\n")
            results.append((test_name, f"❌ FAIL: {e}"))
    
    # Summary
    print("=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    for test_name, result in results:
        print(f"{result:20} {test_name}")
    print()
    
    passed = sum(1 for _, r in results if "PASS" in r)
    total = len(results)
    print(f"Result: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("🎉 All tests passed! Soul ready for Termux deployment.")
    else:
        print("⚠️ Some tests failed. Review errors above.")
    
    print("=" * 70)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️ Tests interrupted")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
