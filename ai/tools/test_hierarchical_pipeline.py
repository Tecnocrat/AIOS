#!/usr/bin/env python3
"""
Test script for hierarchical three-tier E501 pipeline.

Tests: OLLAMA → GEMINI → DEEPSEEK pipeline
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from hierarchical_e501_pipeline import HierarchicalE501Pipeline


async def test_hierarchical_pipeline():
    """Test the three-tier hierarchical pipeline."""
    
    print("=" * 70)
    print("HIERARCHICAL E501 PIPELINE TEST")
    print("=" * 70)
    
    pipeline = HierarchicalE501Pipeline()
    
    # Test case: Long line with E501 violation
    test_line = (
        "    result = await self.hierarchical_pipeline.fix_line_hierarchical("
        "line, file_path, line_number)"
    )
    
    print(f"\nOriginal Line (len={len(test_line)}):")
    print(f"   {test_line}")
    
    print("\nExecuting hierarchical pipeline...")
    print("   Tier 1: OLLAMA (Context Manager)")
    print("   Tier 2: GEMINI (Code Generator)")
    print("   Tier 3: DEEPSEEK (Quality Validator)")
    
    try:
        result = await pipeline.fix_line_hierarchical(
            test_line,
            "test_file.py",
            123
        )
        
        print("\n[SUCCESS] Pipeline Result:")
        print(f"   Success: {result['success']}")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Agent Used: {result.get('agent_used', 'unknown')}")
        print(f"   Validator: {result.get('validator', 'unknown')}")
        
        print("\nFixed Lines:")
        for i, fixed_line in enumerate(result['fixed_lines'], 1):
            print(f"   {i}. {fixed_line} (len={len(fixed_line)})")
        
        print("\nTier Execution Log:")
        tier_log = result.get('tier_log', {})
        for tier, status in tier_log.items():
            print(f"   {tier}: {status}")
        
        print("\nPipeline Statistics:")
        for stat_name, stat_value in pipeline.stats.items():
            print(f"   {stat_name}: {stat_value}")
        
        return result
        
    except Exception as e:
        print(f"\n[ERROR] Pipeline Failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(test_hierarchical_pipeline())
