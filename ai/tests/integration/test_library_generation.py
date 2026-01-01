"""
Test script for Library Code Generation Loop
Executes the complete cycle: Ingestion → Paradigms → Prompts → Code → Analysis
"""

import sys
import asyncio
from pathlib import Path

# Add AIOS to path
sys.path.append(str(Path(__file__).parent / "ai" / "src"))

from integrations.library_code_generation_loop import LibraryCodeGenerationLoop


async def main():
    """Run the complete library code generation cycle"""
    print("🧬 Starting Library Code Generation Cycle")
    print("=" * 60)
    
    # Initialize loop
    loop = LibraryCodeGenerationLoop()
    
    # Run complete cycle
    try:
        # Now async - must await
        results = await loop.run_complete_cycle(
            library_name='aios_core',
            task_description=(
                'Create a TachyonicMemoryBuffer class that stores evolutionary '
                'code variants with consciousness-level tracking. Include methods: '
                'add_variant(code, consciousness_score), get_best_variant(), '
                'and merge_variants(variant_a, variant_b) that combines two code '
                'approaches while preserving type hints and async compatibility.'
            ),
            generation_size=3
        )
        
        print("\n" + "=" * 60)
        print("✅ GENERATION COMPLETE")
        print("=" * 60)
        
        if results.get('success'):
            print(f"\nBest consciousness: {results['best_consciousness']:.2f}")
            print(f"Output directory: {results['generation_dir']}")
            print(f"\nSummary:")
            summary = results['summary']
            print(f"  Paradigms extracted: {summary['paradigms_extracted']}")
            print(f"  Variants generated: {summary['variants_generated']}")
            print(f"  Average consciousness: {summary['avg_consciousness']:.2f}")
            print(f"  Success rate: {summary['success_rate']:.1%}")
        else:
            print(f"\n❌ Generation failed: {results.get('error')}")
        
        return results
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    results = asyncio.run(main())
    
    if results:
        print("\n✅ SUCCESS - Check evolution_lab/library_generations/ for results")
        sys.exit(0)
    else:
        print("\n❌ FAILED - Check error messages above")
        sys.exit(1)
