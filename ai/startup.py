<<<<<<< HEAD
3 |  135 |             (  
   4 |  136 |                 f"   • Tool Discovery: {runtime_info['sequencer_state']['components_discovered']} "
   5 |  137 |                 "components discoverable"
   6 |  138 |             )
=======
#!/usr/bin/env python3
"""
AIOS Startup Orchestrator
Integrates the Sequencer system into main AIOS startup process
"""

import asyncio
import sys
import os
from pathlib import Path

# Add AI core to path for sequencer import
ai_core_path = Path(__file__).parent / "core"
sys.path.insert(0, str(ai_core_path))

try:
    from sequencer import AIOSSequencer
except ImportError as e:
    print(f"❌ Could not import AIOS Sequencer: {e}")
    print("Please ensure sequencer.py is in ai/core/ directory")
    sys.exit(1)


async def startup_aios():
    """
    Main AIOS startup with sequencer integration
    This replaces or enhances the traditional startup process
    """
    print("🚀 AIOS Starting with Sequencer Integration...")
    print("=" * 60)
    
    workspace_root = Path(__file__).parent.parent  # AIOS root
    sequencer = AIOSSequencer(str(workspace_root))
    
    try:
        # Phase 1: Component Discovery
        print("🔍 Phase 1: Discovering Components...")
        components = await sequencer.discover_components()
        print(f"   ✅ Found {len(components)} executable components")
        
        # Show component categories
        categories = {}
        for comp in components.values():
            categories[comp.category] = categories.get(comp.category, 0) + 1
        
        for category, count in categories.items():
            print(f"   📦 {category}: {count} components")
        
        # Phase 2: Dependency Validation
        print("\n🔗 Phase 2: Validating Dependencies...")
        valid, missing = await sequencer.validate_dependencies()
        
        if valid:
            print("   ✅ All dependencies satisfied")
        else:
            print(f"   ⚠️  {len(missing)} dependency issues found:")
            for issue in missing[:3]:  # Show first 3
                print(f"      • {issue}")
        
        # Phase 3: Component Startup
        print("\n🚀 Phase 3: Starting Components...")
        results = await sequencer.start_components(auto_start_only=True)
        
        active_count = len([r for r in results.values() if r])
        failed_count = len([r for r in results.values() if not r])
        
        print(f"   ✅ {active_count} components started successfully")
        if failed_count > 0:
            print(f"   ❌ {failed_count} components failed to start")
        
        # Phase 4: Health Check
        print("\n🏥 Phase 4: Health Monitoring...")
        health = await sequencer.health_check_all()
        
        healthy = len([s for s in health.values() if s == "running"])
        degraded = len([s for s in health.values() if s == "degraded"])
        failed = len([s for s in health.values() if "failed" in s])
        
        print(f"   ✅ {healthy} components healthy")
        if degraded > 0:
            print(f"   ⚠️  {degraded} components degraded")
        if failed > 0:
            print(f"   ❌ {failed} components failed")
        
        # Phase 5: Save State & Summary
        print("\n💾 Phase 5: Saving Runtime State...")
        state_file = sequencer.save_runtime_state()
        print(f"   ✅ Runtime state saved: {state_file.name}")
        
        # Final Summary
        print("\n" + "=" * 60)
        print("🎯 AIOS Startup Complete!")
        
        runtime_info = sequencer.get_runtime_info()
        uptime = runtime_info['sequencer_state']['uptime_seconds']
        
        print(f"📊 Summary:")
        print(f"   • Total Components: {runtime_info['sequencer_state']['components_discovered']}")
        print(f"   • Active Components: {runtime_info['sequencer_state']['components_active']}")
        print(f"   • Failed Components: {runtime_info['sequencer_state']['components_failed']}")
        print(f"   • Startup Time: {uptime:.2f} seconds")
        
        # Show key components status
        print(f"\n🔧 Key Components Status:")
        key_components = ['ai_engine_handoff', 'cross_pollination_automator', 'start_server']
        for name, comp_info in runtime_info['components'].items():
            if any(key in name for key in key_components):
                status_emoji = {
                    'running': '✅',
                    'failed': '❌',
                    'degraded': '⚠️',
                    'unknown': '❓'
                }.get(comp_info['status'], '❓')
                print(f"   {status_emoji} {name}: {comp_info['status']}")
        
        # Additional runtime guidance
        print(f"\n📋 Runtime Information:")
        print(f"   • State File: {state_file}")
        print(f"   • Log File: {sequencer.workspace_root}/ai/infrastructure/runtime/sequencer.log")
        print(f"   • Health Checks: Available via sequencer.health_check_all()")
        
        # Show available tools
        print(f"\n🛠️  Available AI Tools:")
        print(f"   • AI Engine Handoff: ai/core/ai_cells/ai_engine_handoff.py")
        print(f"   • Cross-Pollination: ai/infrastructure/tools/cross_pollination_automator.py")
        print(f"   • Runtime Sequencer: ai/core/sequencer.py")
        print(f"   • Interface Bridge: ai/core/interface_bridge.py")
        
        # Interface Bridge Information
        print(f"\n🌉 Interface Bridge:")
        print(f"   • API Endpoint: http://localhost:8000")
        print(f"   • Documentation: http://localhost:8000/docs")
        print(f"   • C# Integration: interface/AIOS.Models/PythonAIToolsService.cs")
        print(f"   • Tool Discovery: {runtime_info['sequencer_state']['components_discovered']} components discoverable")
        
        print("\n✨ AIOS is ready for operation!")
        return sequencer
        
    except Exception as e:
        print(f"\n❌ AIOS Startup Failed: {e}")
        print(f"   Check logs for details: {sequencer.workspace_root}/ai/infrastructure/runtime/")
        return None


def main():
    """Main entry point for AIOS startup"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("AIOS Startup Orchestrator")
        print("Usage: python startup.py [options]")
        print("")
        print("Options:")
        print("  --help          Show this help message")
        print("  --discover-only Only discover components, don't start them")
        print("  --health-only   Only run health checks")
        print("")
        print("This script integrates the AIOS Sequencer system into startup")
        print("and provides organized discovery, validation, and execution of")
        print("all AIOS executable components.")
        return
    
    try:
        # Run async startup
        sequencer = asyncio.run(startup_aios())
        
        if sequencer is None:
            sys.exit(1)
        
        # Optional: Keep running for continuous monitoring
        if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
            print("\n🔄 Entering monitoring mode...")
            print("Press Ctrl+C to exit")
            try:
                while True:
                    asyncio.run(asyncio.sleep(30))  # Check every 30 seconds
                    health = asyncio.run(sequencer.health_check_all())
                    failed = [name for name, status in health.items() 
                             if "failed" in status or "error" in status]
                    if failed:
                        print(f"⚠️  Components with issues: {', '.join(failed[:3])}")
            except KeyboardInterrupt:
                print("\n👋 AIOS monitoring stopped")
        
    except KeyboardInterrupt:
        print("\n👋 AIOS startup interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ AIOS startup error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
>>>>>>> origin/OS0.6.2.grok
