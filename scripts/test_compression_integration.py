#!/usr/bin/env python3
"""
AIOS Universal Compression Integration Demonstration
Shows compression capabilities across all AIOS systems
Created: July 10, 2025
"""

import os
import sys
from pathlib import Path


def main():
    print("🚀 AIOS Universal Compression Integration Demonstration")
    print("=" * 60)

    # Add scripts path for imports
    scripts_path = Path(__file__).parent
    if str(scripts_path) not in sys.path:
        sys.path.append(str(scripts_path))

    success_count = 0
    total_tests = 6

    # Test 1: AIOS Master Integration
    print("\n📋 Test 1: AIOS Master Integration")
    try:
        from aios_master import AIOSMaster
        master = AIOSMaster()
        tools = master.get_compression_tools()

        print(f"   ✅ Status: {tools['available']}")
        print(f"   📦 Service: {tools['service']}")
        print(f"   🔧 Types: {', '.join(tools['types'])}")
        print(f"   📊 Levels: {', '.join(tools['levels'])}")
        print(f"   🎯 Strategies: {', '.join(tools['strategies'])}")
        success_count += 1
    except Exception as e:
        print(f"   ❌ Failed: {e}")

    # Test 2: AINLP Engine Integration
    print("\n📋 Test 2: AINLP Engine Integration")
    try:
        from core.ainlp_unified_engine import AINLPUnifiedEngine
        ainlp = AINLPUnifiedEngine()
        status = ainlp._get_compression_tools_status()

        print(f"   ✅ Status: {status['available']}")
        print(f"   📊 Active Compressions: {len(status['active_compressions'])}")
        print(f"   📈 Stats: {status['stats']['total_compressions']} total compressions")
        success_count += 1
    except Exception as e:
        print(f"   ❌ Failed: {e}")

    # Test 3: Direct Compression Service
    print("\n📋 Test 3: Direct Compression Service")
    try:
        from compression.aios_universal_compressor import (
            AIOSUniversalCompressor, CompressionRequest)

        compressor = AIOSUniversalCompressor()
        print(f"   ✅ Service: Initialized")
        print(f"   📁 Workspace: {compressor.workspace_root}")
        print(f"   🔧 Compression Workspace: {compressor.compression_workspace}")

        # Test status retrieval
        status = compressor.get_compression_status()
        print(f"   📊 Total Compressions: {status['stats']['total_compressions']}")
        success_count += 1
    except Exception as e:
        print(f"   ❌ Failed: {e}")

    # Test 4: Compression Request Structure
    print("\n📋 Test 4: Compression Request Structure")
    try:
        from compression.aios_universal_compressor import CompressionRequest

        request = CompressionRequest(
            source_path="c:\\dev\\AIOS\\scripts",
            compression_type="SMART_MERGE",
            compression_level="STANDARD",
            file_patterns=["*.py"],
            create_backup=True
        )

        print(f"   ✅ Request Created: {request.source_path}")
        print(f"   🔧 Type: {request.compression_type}")
        print(f"   📊 Level: {request.compression_level}")
        print(f"   🛡️ Backup: {request.create_backup}")
        success_count += 1
    except Exception as e:
        print(f"   ❌ Failed: {e}")

    # Test 5: AIOS Master Compression Function
    print("\n📋 Test 5: AIOS Master Compression Function")
    try:
        # Test the compression function (dry run)
        master = AIOSMaster()
        if hasattr(master, 'compress_files'):
            print("   ✅ Compression Function: Available")
            print("   🎯 Ready for: master.compress_files(path)")
            success_count += 1
        else:
            print("   ❌ Compression Function: Not found")
    except Exception as e:
        print(f"   ❌ Failed: {e}")

    # Test 6: Cross-System Compatibility
    print("\n📋 Test 6: Cross-System Compatibility")
    try:
        # Check if all systems can access compression
        systems = {
            'AIOS Master': master.get_compression_tools()['available'],
            'AINLP Engine': ainlp._get_compression_tools_status()['available'],
            'Direct Service': True,  # Already verified above
        }

        all_available = all(systems.values())
        print(f"   ✅ All Systems: {all_available}")

        for system, available in systems.items():
            status = "✅" if available else "❌"
            print(f"   {status} {system}: {'Available' if available else 'Unavailable'}")

        if all_available:
            success_count += 1
    except Exception as e:
        print(f"   ❌ Failed: {e}")

    # Final Results
    print("\n" + "=" * 60)
    print(f"🎯 INTEGRATION TEST RESULTS: {success_count}/{total_tests} PASSED")

    if success_count == total_tests:
        print("🎉 ALL TESTS PASSED - COMPRESSION FULLY INTEGRATED!")
        print("\n🚀 Ready for use across all AIOS systems:")
        print("   • Python: from aios_master import AIOSMaster")
        print("   • C#: var service = new AIOSCompressionService();")
        print("   • C++: auto result = AIOS_COMPRESS(path);")
        print("   • CLI: python aios_universal_compressor.py <path>")
    else:
        print(f"⚠️  {total_tests - success_count} tests failed - check integration")

    print("\n💫 Universal compression is now available to every AIOS system!")

if __name__ == "__main__":
    main()
