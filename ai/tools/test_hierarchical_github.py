#!/usr/bin/env python3
"""Test hierarchical pipeline with GitHub Models integration"""
import asyncio
from hierarchical_e501_pipeline import HierarchicalE501Pipeline

async def test_pipeline():
    """Test GitHub Models-powered agentic E501 fixing"""
    
    # Test line: 97 characters (exceeds 79 limit)
    test_line = "x = very_long_function_name_that_exceeds_the_limit_with_many_arguments(arg1, arg2, arg3)"
    
    print("=" * 60)
    print("Testing Hierarchical Agentic Pipeline")
    print("GitHub Models: GPT-4o-mini (Tier 2) + GPT-4o (Tier 3)")
    print("=" * 60)
    print(f"\nOriginal line ({len(test_line)} chars):")
    print(f"  {test_line}")
    print()
    
    pipeline = HierarchicalE501Pipeline()
    result = await pipeline.fix_line_hierarchical(
        line=test_line,
        file_path="test.py",
        line_number=1
    )
    
    print("Results:")
    print(f"  Success: {result['success']}")
    print(f"  Tier Log: {' → '.join(result['tier_log'])}")
    print(f"  Confidence: {result.get('confidence', 'N/A')}")
    print()
    
    if result['success']:
        print("Fixed lines:")
        for i, line in enumerate(result['fixed_lines'], 1):
            print(f"  {i}. ({len(line)} chars) {line}")
    else:
        print(f"  Error: {result.get('error', 'Unknown')}")
    
    print("\n" + "=" * 60)
    
    # Show agentic behavior stats
    if hasattr(pipeline, 'tier2_stats'):
        print("\nAgentic Stats:")
        print(f"  Tier 2 generations: {pipeline.tier2_stats.get('total', 0)}")
        print(f"  Tier 3 validations: {pipeline.tier3_stats.get('total', 0)}")
        print(f"  Feedback loops: {pipeline.tier3_stats.get('rejections', 0)}")
        print(f"  API errors: {pipeline.tier2_stats.get('errors', 0)}")
    
    return result['success']

if __name__ == "__main__":
    success = asyncio.run(test_pipeline())
    exit(0 if success else 1)
