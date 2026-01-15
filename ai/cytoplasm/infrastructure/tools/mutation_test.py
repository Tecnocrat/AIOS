#!/usr/bin/env python3
"""Evolution Lab Mutation Test - aios-mistral integration validation."""

import asyncio
import ast
import re
import sys
from pathlib import Path

# Add ai/ to path for imports
ai_path = Path(__file__).parent.parent
sys.path.insert(0, str(ai_path))
from tools.aios_mistral_bridge import AIOSMistralBridge


async def mutation_test():
    """Run mutation test with aios-mistral."""
    # Very long timeout - model can take 30-60s on 4GB VRAM
    bridge = AIOSMistralBridge(timeout=300.0)

    # Step 1: Health check
    print("=" * 60)
    print("🧬 EVOLUTION LAB MUTATION TEST")
    print("=" * 60)

    health = await bridge.check_health()
    if not health:
        print("❌ Ollama not running. Start with: .\\aios-mistral.ps1 -Serve")
        return
    print("✅ Ollama healthy")

    # Step 2: Simple organism (code to mutate)
    archetype = "utility_functions"
    original_code = """def calculate_sum(numbers):
    total = 0
    for n in numbers:
        total = total + n
    return total"""

    print()
    print("📄 ORIGINAL ORGANISM:")
    print(original_code)

    # Step 3: Mutate with archetype
    print()
    print(f'🧬 Mutating with archetype: "{archetype}"...')
    print(f"   Bridge timeout: {bridge.timeout}")
    print(f"   Client: {bridge._client}")
    result = await bridge.mutate_code(original_code, archetype)
    print(f"   Result received: success={result.success}")

    if not result.success:
        print(f"❌ Mutation failed: {result.error}")
        return

    mutated_code = result.content
    print()
    print("🔀 MUTATED ORGANISM:")
    print(mutated_code)
    print(f"   ⏱️ Duration: {result.total_duration_ms:.0f}ms")

    # Step 4: Analyze fitness of both
    print()
    print("📊 FITNESS ANALYSIS:")

    original_fitness = await bridge.analyze_fitness(original_code, archetype)
    if original_fitness.success:
        print(f"   Original: {original_fitness.content[:200]}...")
    else:
        print(f"   Original: ❌ {original_fitness.error}")

    mutated_fitness = await bridge.analyze_fitness(mutated_code, archetype)
    if mutated_fitness.success:
        print(f"   Mutated:  {mutated_fitness.content[:200]}...")
    else:
        print(f"   Mutated:  ❌ {mutated_fitness.error}")

    # Step 5: Validate syntax
    print()
    print("🔍 SYNTAX VALIDATION:")
    try:
        ast.parse(original_code)
        print("   Original: ✅ Valid Python")
    except SyntaxError as e:
        print(f"   Original: ❌ {e}")

    # Extract code from markdown if present
    code_to_validate = mutated_code
    if "```python" in mutated_code:
        match = re.search(r"```python\n(.*?)```", mutated_code, re.DOTALL)
        if match:
            code_to_validate = match.group(1)
    elif "```" in mutated_code:
        match = re.search(r"```\n?(.*?)```", mutated_code, re.DOTALL)
        if match:
            code_to_validate = match.group(1)

    try:
        ast.parse(code_to_validate)
        print("   Mutated:  ✅ Valid Python")
    except SyntaxError as e:
        print(f"   Mutated:  ❌ {e}")

    print()
    print("=" * 60)
    print("✅ MUTATION TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(mutation_test())
