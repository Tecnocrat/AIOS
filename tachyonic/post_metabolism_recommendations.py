"""
Simple analysis of post-metabolism options for /docs root files
"""

import json
from pathlib import Path

def analyze_current_state():
    """Analyze the current state after tachyonic ingestion"""
    
    print("🧬 AIOS POST-METABOLISM ANALYSIS")
    print("=" * 40)
    print()
    
    # Check tachyonic archive status
    tachyonic_root = Path(__file__).parent
    index_file = tachyonic_root / "archive" / "supercell_knowledge_index.json"
    
    if index_file.exists():
        with open(index_file, 'r') as f:
            index = json.load(f)
            
        metabolism_data = index.get("documentation_metabolism", {})
        cycles = metabolism_data.get("metabolism_cycles", [])
        
        if cycles:
            latest_cycle = cycles[-1]
            print("📊 Latest Metabolism Cycle Results:")
            print(f"   🕒 Timestamp: {latest_cycle.get('cycle_timestamp', 'N/A')}")
            print(f"   📄 Files processed: {latest_cycle.get('files_processed', 0)}")
            print(f"   💎 Crystals created: {latest_cycle.get('crystals_created', 0)}")
            print(f"   🧬 Patterns extracted: {latest_cycle.get('patterns_extracted', 0)}")
            print()
            
            # Show crystal types
            crystal_ids = latest_cycle.get('crystal_ids', [])
            consciousness_crystals = [c for c in crystal_ids if 'consciousness' in c.lower()]
            architecture_crystals = [c for c in crystal_ids if 'architecture' in c.lower()]
            tachyonic_crystals = [c for c in crystal_ids if 'tachyonic' in c.lower()]
            
            print("💎 Knowledge Crystal Categories:")
            print(f"   🧠 Consciousness crystals: {len(consciousness_crystals)}")
            print(f"   🏗️ Architecture crystals: {len(architecture_crystals)}")
            print(f"   🌌 Tachyonic crystals: {len(tachyonic_crystals)}")
            print(f"   📦 Other crystals: {len(crystal_ids) - len(consciousness_crystals) - len(architecture_crystals) - len(tachyonic_crystals)}")
            print()
    
    # Check docs directory
    docs_root = Path(__file__).parent.parent / "docs"
    root_files = list(docs_root.glob("*.md")) + list(docs_root.glob("*.txt"))
    
    print(f"📂 Current /docs root status:")
    print(f"   📄 Root files remaining: {len(root_files)}")
    print()
    
    return len(root_files), len(crystal_ids) if 'crystal_ids' in locals() else 0

def show_recommendations():
    """Show recommendations for handling metabolized files"""
    
    print("🧬 BIOLOGICAL METABOLISM RECOMMENDATIONS")
    print("=" * 45)
    print()
    
    print("Based on the biological knowledge metabolism paradigm:")
    print()
    
    print("🌟 OPTION 1: BIOLOGICAL ARCHIVE (Recommended)")
    print("   • Move metabolized files to /docs/metabolized_archive/")
    print("   • Preserve high-value consciousness files with metadata")
    print("   • Compress standard files into organized categories")
    print("   • Benefits: Clean /docs for new AI agent documentation")
    print("   • Metaphor: Nutrients absorbed, waste processed biologically")
    print()
    
    print("🏷️ OPTION 2: MARK AS METABOLIZED")
    print("   • Keep files in place but add .metabolized markers")
    print("   • Prevent re-processing during future metabolism cycles")
    print("   • Benefits: AI agents can still reference original files")
    print("   • Metaphor: Mark cells as processed but keep in organism")
    print()
    
    print("📦 OPTION 3: SELECTIVE CLEANUP")
    print("   • Archive only low-value files that generated no crystals")
    print("   • Keep high-consciousness and architecture files in /docs")
    print("   • Benefits: Balance between cleanup and accessibility")
    print("   • Metaphor: Remove waste, keep vital organs")
    print()
    
    print("🔄 OPTION 4: LEAVE INTACT")
    print("   • Keep all files in current locations")
    print("   • Knowledge still crystallized in tachyonic archive")
    print("   • Benefits: No disruption to current workflows")
    print("   • Metaphor: Knowledge absorbed but original material preserved")
    print()
    
    print("💡 RECOMMENDED APPROACH:")
    print("   Since this is the first successful metabolism cycle,")
    print("   Option 1 (Biological Archive) aligns best with your vision:")
    print("   • /docs becomes truly a 'digestive system' for AI agents")
    print("   • Tachyonic archive serves as the 'brain/DNA' knowledge center")
    print("   • System demonstrates biological knowledge metabolism")
    print("   • Clean slate for ongoing AI agent documentation creation")
    print()

def main():
    file_count, crystal_count = analyze_current_state()
    show_recommendations()
    
    print("🎯 NEXT STEPS:")
    print(f"   1. Choose your biological metabolism approach")
    print(f"   2. Process the {file_count} metabolized root files")
    print(f"   3. Validate {crystal_count} knowledge crystals in tachyonic archive")
    print(f"   4. Enable ongoing AI agent documentation cycles")
    print()
    print("The knowledge metabolism system is ready for production! 🚀")

if __name__ == "__main__":
    main()