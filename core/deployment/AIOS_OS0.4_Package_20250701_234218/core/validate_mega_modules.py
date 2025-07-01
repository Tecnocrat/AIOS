#!/usr/bin/env python3
"""
🧠 AIOS OS0.4 - Mega-Module Validation Script
============================================

Validates all mega-modules and provides comprehensive status report.
"""

import sys
import os
from pathlib import Path

# Add core directory to path
core_path = Path(__file__).parent
sys.path.insert(0, str(core_path))

def test_mega_modules():
    """Test all mega-modules and report status"""
    print("🧠 AIOS OS0.4 - Mega-Module Validation")
    print("=" * 50)
    
    modules_to_test = [
        ("aios_consciousness_engine", "Consciousness Engine"),
        ("aios_evolution_lab", "Evolution Lab"),
        ("aios_knowledge_distillation", "Knowledge Distillation"),
        ("aios_admin_orchestrator", "Admin Orchestrator")
    ]
    
    results = {}
    
    for module_name, display_name in modules_to_test:
        print(f"\n🧪 Testing {display_name}...")
        
        try:
            # Import module
            module = __import__(module_name)
            
            # Try to get basic info
            if hasattr(module, '__doc__') and module.__doc__:
                doc_lines = module.__doc__.strip().split('\n')
                description = doc_lines[1] if len(doc_lines) > 1 else "No description"
            else:
                description = "No documentation"
            
            # Try to find main classes
            classes = [name for name in dir(module) 
                      if name[0].isupper() and not name.startswith('_')]
            
            results[module_name] = {
                "status": "✅ SUCCESS",
                "description": description,
                "classes": classes[:5],  # First 5 classes
                "file_size": os.path.getsize(f"{module_name}.py") / 1024  # KB
            }
            
            print(f"   ✅ {display_name}: OK ({len(classes)} classes, {results[module_name]['file_size']:.1f}KB)")
            
        except ImportError as e:
            results[module_name] = {
                "status": "❌ IMPORT ERROR",
                "error": str(e),
                "file_size": 0
            }
            print(f"   ❌ {display_name}: Import Error - {e}")
            
        except Exception as e:
            results[module_name] = {
                "status": "⚠️ ERROR",
                "error": str(e),
                "file_size": 0
            }
            print(f"   ⚠️ {display_name}: Error - {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 MEGA-MODULE CONSOLIDATION SUMMARY")
    print("=" * 50)
    
    successful = sum(1 for r in results.values() if "SUCCESS" in r["status"])
    total_size = sum(r.get("file_size", 0) for r in results.values())
    
    print(f"✅ Successful modules: {successful}/{len(modules_to_test)}")
    print(f"📦 Total consolidated code: {total_size:.1f}KB")
    print(f"🎯 Consolidation ratio: {len(modules_to_test)} mega-modules vs 15+ original scripts")
    
    # Detailed results
    print("\n📋 DETAILED RESULTS:")
    for module_name, result in results.items():
        print(f"\n🔍 {module_name}:")
        print(f"   Status: {result['status']}")
        if "classes" in result:
            print(f"   Classes: {', '.join(result['classes'][:3])}{'...' if len(result['classes']) > 3 else ''}")
            print(f"   Size: {result['file_size']:.1f}KB")
        if "error" in result:
            print(f"   Error: {result['error']}")
    
    # OS0.4 Progress
    print("\n" + "=" * 50)
    print("🚀 AIOS OS0.4 PROGRESS")
    print("=" * 50)
    print("✅ Phase 1: Python Intelligence Fusion - COMPLETED")
    print("   - 4 mega-modules created in /core/")
    print("   - Consolidated 15+ scattered scripts")
    print("   - Enhanced functionality and unified interfaces")
    print("\n🔄 Next Steps:")
    print("   - Phase 2: Next-Gen UI Implementation")
    print("   - Phase 3: C++ Orchestrator Optimization") 
    print("   - Phase 4: Real-time Runtime Transparency")
    print("   - Phase 5: System Finalization & Clean Install Prep")
    
    return results

if __name__ == "__main__":
    results = test_mega_modules()
    
    # Exit with appropriate code
    successful = sum(1 for r in results.values() if "SUCCESS" in r["status"])
    sys.exit(0 if successful == len(results) else 1)
