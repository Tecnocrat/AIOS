"""
Test Paradigm Extraction from Ingested Library
This tests ONLY the paradigm extraction step without code generation
"""

import sys
from pathlib import Path

# Add AIOS to path
sys.path.append(str(Path(__file__).parent / "ai" / "src"))

from engines.paradigm_extraction_engine import ParadigmExtractionEngine


def main():
    """Test paradigm extraction from ingested library"""
    print("🔍 Testing Paradigm Extraction")
    print("=" * 60)
    
    # Initialize extractor
    print("\nInitializing Paradigm Extraction Engine...")
    engine = ParadigmExtractionEngine()
    
    # Extract paradigms from aios_core JSON file directly
    json_file = engine.knowledge_base_path / "python" / "aios_core.json"
    print(f"\nExtracting paradigms from '{json_file}'...")
    
    try:
        if not json_file.exists():
            print(f"❌ File not found: {json_file}")
            return
            
        print(f"📄 Processing: {json_file.name} ({json_file.stat().st_size} bytes)")
        engine._extract_from_file(json_file)
        paradigms = engine.paradigms
        
        print(f"\n✅ SUCCESS: Extracted {len(paradigms)} paradigms")
        print("=" * 60)
        
        # Show top paradigms
        top = engine.get_top_paradigms(10)
        print(f"\nTop 10 Paradigms:")
        for i, p in enumerate(top, 1):
            print(f"\n{i}. {p.name}")
            print(f"   Category: {p.category}")
            print(f"   Pattern: {p.pattern}")
            print(f"   Usage: {p.usage_count}x")
            if p.examples:
                example = p.examples[0][:60] + "..." if len(p.examples[0]) > 60 else p.examples[0]
                print(f"   Example: {example}")
        
        # Save to file for inspection
        output_file = Path("paradigms_extracted_test.json")
        engine.save_paradigms(output_file)
        print(f"\n📁 Paradigms saved to: {output_file}")
        
        # Show pattern distribution
        print(f"\n📊 Pattern Distribution:")
        pattern_counts = {}
        for p in paradigms:
            pattern_counts[p.pattern] = pattern_counts.get(p.pattern, 0) + 1
        
        for pattern, count in sorted(pattern_counts.items(), 
                                     key=lambda x: x[1], 
                                     reverse=True)[:5]:
            print(f"  {pattern}: {count} instances")
        
        return True
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ Paradigm extraction successful!")
        print("Next step: Install Ollama and run full generation cycle")
        print("  1. Install: https://ollama.ai/download")
        print("  2. Pull model: ollama pull deepseek-coder:6.7b")
        print("  3. Run: python test_library_generation.py")
        sys.exit(0)
    else:
        print("\n❌ Paradigm extraction failed")
        sys.exit(1)
