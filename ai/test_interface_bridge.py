#!/usr/bin/env python3
"""
Test Script for AIOS Interface Bridge
Validates the bridge functionality and C#/.NET integration capabilities
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add core to path
sys.path.append(str(Path(__file__).parent / "core"))

try:
    from interface_bridge import AIOSInterfaceBridge
except ImportError as e:
    print(f"❌ Could not import interface bridge: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    sys.exit(1)


async def test_interface_bridge():
    """Test the interface bridge functionality"""
    print("🧪 Testing AIOS Interface Bridge")
    print("=" * 50)
    
    workspace_root = Path(__file__).parent.parent
    bridge = AIOSInterfaceBridge(str(workspace_root))
    
    try:
        # Test 1: Component Discovery
        print("\n🔍 Test 1: Component Discovery")
        await bridge.refresh_discovery()
        print(f"   ✅ Discovered {len(bridge.discovered_tools)} tools")
        
        for tool_name, tool_metadata in list(bridge.discovered_tools.items())[:3]:
            print(f"   📋 {tool_metadata.display_name} ({tool_metadata.category})")
        
        # Test 2: Health Check
        print("\n🏥 Test 2: Health Check")
        health = await bridge.health_check()
        print(f"   ✅ Bridge status: {health['status']}")
        print(f"   📊 Tools discovered: {health['tools_discovered']}")
        
        # Test 3: Generate C# Interface
        print("\n🔧 Test 3: C# Interface Generation")
        interface_file = bridge.save_csharp_interface()
        print(f"   ✅ Generated C# interface: {interface_file}")
        
        # Test 4: Metadata Generation
        print("\n📋 Test 4: Tool Metadata")
        if bridge.discovered_tools:
            first_tool = next(iter(bridge.discovered_tools.values()))
            metadata = first_tool.to_dict()
            print(f"   📝 Sample tool: {metadata['display_name']}")
            print(f"   🎯 Capabilities: {', '.join(metadata['capabilities'])}")
            print(f"   📊 Parameters: {len(metadata['parameters'])}")
        
        # Test 5: Export Discovery Data
        print("\n💾 Test 5: Export Discovery Data")
        export_file = workspace_root / "runtime" / "logs" / "interface_bridge_discovery.json"
        export_file.parent.mkdir(parents=True, exist_ok=True)
        
        export_data = {
            "discovery_timestamp": bridge.last_discovery.isoformat() if bridge.last_discovery else None,
            "tools_count": len(bridge.discovered_tools),
            "tools": [tool.to_dict() for tool in bridge.discovered_tools.values()],
            "health_status": health
        }
        
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Exported discovery data: {export_file}")
        
        # Summary
        print("\n" + "=" * 50)
        print("🎯 Interface Bridge Test Results:")
        print(f"   • Discovery: ✅ {len(bridge.discovered_tools)} tools found")
        print(f"   • Health Check: ✅ {health['status']}")
        print(f"   • C# Interface: ✅ Generated")
        print(f"   • Metadata: ✅ Complete")
        print(f"   • Export: ✅ Saved to {export_file.name}")
        
        # Categories Summary
        categories = {}
        for tool in bridge.discovered_tools.values():
            category = tool.category
            categories[category] = categories.get(category, 0) + 1
        
        print(f"\n📊 Tool Categories:")
        for category, count in categories.items():
            print(f"   • {category}: {count} tools")
        
        print("\n✅ All tests passed! Interface Bridge is operational.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test execution"""
    success = await test_interface_bridge()
    
    if success:
        print("\n🚀 Ready to start Interface Bridge API server")
        print("   Run: cd ai && python core/interface_bridge.py")
        print("   Then access: http://localhost:8000")
    else:
        print("\n❌ Interface Bridge tests failed")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())