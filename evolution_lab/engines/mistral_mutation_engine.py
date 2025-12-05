"""
Mistral Mutation Engine - AI-Powered Code Evolution
Bridges aios-mistral (Mistral 7B) to PopulationManager for real mutations

AINLP Protocol: OS0.6.4.claude
Created: 2025-12-05
Host: HP_LAB (192.168.1.129)
Phase: Evolution Lab Integration

Architecture:
    ┌─────────────────────────────────────────────────────────────┐
    │  EvolutionOrchestrator                                      │
    │    ├── _evolve_generation()                                 │
    │    │     ├── select_survivors()       ← PopulationManager   │
    │    │     ├── async_repopulate()       ← NEW (this engine)   │
    │    │     │     └── mutate_organism()  ← MistralMutationEngine│
    │    │     └── evaluate_fitness()       ← PopulationManager   │
    │    └── archive_generation()                                 │
    └─────────────────────────────────────────────────────────────┘

Cost: FREE (local Ollama inference)
Latency: ~5-25s per mutation (4GB VRAM)
Quality: Good for Tier 1 mutations, may need Tier 2+ validation
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import re

# Add ai/tools to path for bridge import
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "ai" / "tools"))

from aios_mistral_bridge import AIOSMistralBridge, MistralResponse


@dataclass
class MutationResult:
    """Result of a code mutation attempt"""
    success: bool
    original_code: str
    mutated_code: str
    mutation_type: str  # 'structural', 'behavioral', 'optimization', 'failed'
    changes_summary: str
    duration_ms: float
    archetype: str
    error: Optional[str] = None
    fitness_delta_estimate: float = 0.0  # Positive = improvement expected


@dataclass 
class MutationStats:
    """Statistics for mutation engine performance"""
    total_attempts: int = 0
    successful_mutations: int = 0
    failed_mutations: int = 0
    total_duration_ms: float = 0.0
    avg_fitness_delta: float = 0.0
    mutations_by_type: Dict[str, int] = field(default_factory=dict)
    
    @property
    def success_rate(self) -> float:
        if self.total_attempts == 0:
            return 0.0
        return self.successful_mutations / self.total_attempts
    
    @property 
    def avg_duration_ms(self) -> float:
        if self.successful_mutations == 0:
            return 0.0
        return self.total_duration_ms / self.successful_mutations


class MistralMutationEngine:
    """
    AI-powered code mutation engine using local Mistral 7B
    
    Mutation Strategies:
    1. STRUCTURAL: Add/remove/modify classes, functions, modules
    2. BEHAVIORAL: Change logic flow, algorithms, data handling  
    3. OPTIMIZATION: Improve performance, reduce complexity
    4. EXPLORATION: Random novel patterns based on archetype
    
    Each mutation maintains:
    - Syntactic validity (compilable Python)
    - Archetype alignment (matches organism role)
    - Semantic coherence (logical code structure)
    """
    
    # Mutation prompts by strategy type
    MUTATION_PROMPTS = {
        'structural': """You are a code evolution engine. Mutate this {archetype} code by making STRUCTURAL changes:
- Add a new method/function that extends capability
- Modify class hierarchy or organization
- Add new imports that enhance functionality

Original code:
```python
{code}
```

Return ONLY the mutated Python code, no explanations. Ensure it compiles.""",

        'behavioral': """You are a code evolution engine. Mutate this {archetype} code by making BEHAVIORAL changes:
- Modify algorithms or logic flow
- Change data handling patterns
- Alter control flow or conditionals

Original code:
```python
{code}
```

Return ONLY the mutated Python code, no explanations. Ensure it compiles.""",

        'optimization': """You are a code evolution engine. Mutate this {archetype} code by making OPTIMIZATION changes:
- Improve performance or efficiency
- Reduce code complexity
- Add caching or memoization where beneficial

Original code:
```python
{code}
```

Return ONLY the mutated Python code, no explanations. Ensure it compiles.""",

        'exploration': """You are a code evolution engine. Mutate this {archetype} code by EXPLORING new patterns:
- Add creative functionality aligned with the archetype
- Introduce design patterns not currently present
- Expand the organism's capabilities in novel directions

Original code:
```python
{code}
```

Return ONLY the mutated Python code, no explanations. Ensure it compiles."""
    }
    
    def __init__(
        self,
        bridge: Optional[AIOSMistralBridge] = None,
        temperature: float = 0.7,
        max_retries: int = 2
    ):
        """
        Initialize mutation engine
        
        Args:
            bridge: Optional pre-configured bridge (creates one if None)
            temperature: Mutation creativity (0.0=conservative, 1.0=wild)
            max_retries: Retry count on syntax errors
        """
        self._bridge = bridge
        self._owns_bridge = bridge is None
        self.temperature = temperature
        self.max_retries = max_retries
        self.stats = MutationStats()
    
    async def __aenter__(self):
        if self._owns_bridge:
            self._bridge = AIOSMistralBridge(timeout=120.0)
            await self._bridge.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._owns_bridge and self._bridge:
            await self._bridge.__aexit__(exc_type, exc_val, exc_tb)
    
    def _select_mutation_strategy(self, code: str, archetype: str) -> str:
        """
        Select mutation strategy based on code characteristics
        
        Heuristics:
        - Short code (<50 lines) → structural (expand)
        - Complex code (many classes) → optimization (simplify)
        - Simple code (few patterns) → exploration (diversify)
        - Default → behavioral (modify logic)
        """
        lines = code.strip().split('\n')
        line_count = len(lines)
        class_count = sum(1 for line in lines if line.strip().startswith('class '))
        func_count = sum(1 for line in lines if line.strip().startswith('def '))
        
        if line_count < 30:
            return 'structural'  # Small code → expand
        elif class_count > 2 or func_count > 5:
            return 'optimization'  # Complex → simplify
        elif class_count == 0 and func_count <= 2:
            return 'exploration'  # Simple → diversify
        else:
            return 'behavioral'  # Default → modify
    
    def _extract_python_code(self, response: str) -> Optional[str]:
        """Extract Python code from response, handling various formats"""
        # Try to find code blocks
        code_block_pattern = r'```(?:python)?\s*\n?(.*?)\n?```'
        matches = re.findall(code_block_pattern, response, re.DOTALL)
        
        if matches:
            # Return the longest code block (likely the main code)
            return max(matches, key=len).strip()
        
        # If no code blocks, check if entire response is valid Python
        try:
            compile(response.strip(), '<string>', 'exec')
            return response.strip()
        except SyntaxError:
            pass
        
        # Try stripping common prefixes/suffixes
        cleaned = response.strip()
        for prefix in ['Here is', 'Here\'s', 'The mutated code:', 'Mutated code:']:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
        
        try:
            compile(cleaned, '<string>', 'exec')
            return cleaned
        except SyntaxError:
            return None
    
    def _validate_mutation(self, original: str, mutated: str) -> Tuple[bool, str]:
        """
        Validate that mutation is acceptable
        
        Checks:
        1. Syntax validity (compiles)
        2. Not empty or trivial
        3. Actually different from original
        4. Not just comments added
        
        Returns:
            (is_valid, reason)
        """
        if not mutated or len(mutated.strip()) < 10:
            return False, "Mutation too short or empty"
        
        # Syntax check
        try:
            compile(mutated, '<string>', 'exec')
        except SyntaxError as e:
            return False, f"Syntax error: {e.msg} at line {e.lineno}"
        
        # Check if actually different
        original_normalized = '\n'.join(
            line for line in original.strip().split('\n')
            if line.strip() and not line.strip().startswith('#')
        )
        mutated_normalized = '\n'.join(
            line for line in mutated.strip().split('\n')
            if line.strip() and not line.strip().startswith('#')
        )
        
        if original_normalized == mutated_normalized:
            return False, "Mutation is identical to original (ignoring comments)"
        
        # Check minimum change threshold
        orig_lines = set(original_normalized.split('\n'))
        mut_lines = set(mutated_normalized.split('\n'))
        unchanged = len(orig_lines & mut_lines)
        total = max(len(orig_lines), len(mut_lines))
        
        if total > 0 and unchanged / total > 0.95:
            return False, "Mutation too similar to original (<5% change)"
        
        return True, "Valid mutation"
    
    def _estimate_fitness_delta(self, original: str, mutated: str, archetype: str) -> float:
        """
        Estimate fitness improvement from mutation
        
        Positive = expected improvement
        Negative = expected degradation
        
        Heuristics:
        - More functions/classes → +0.1
        - Type hints added → +0.05
        - Docstrings added → +0.05
        - Error handling added → +0.1
        - Reduced line count (cleaner) → +0.05
        """
        delta = 0.0
        
        orig_funcs = original.count('def ')
        mut_funcs = mutated.count('def ')
        if mut_funcs > orig_funcs:
            delta += 0.1 * (mut_funcs - orig_funcs)
        
        orig_classes = original.count('class ')
        mut_classes = mutated.count('class ')
        if mut_classes > orig_classes:
            delta += 0.15 * (mut_classes - orig_classes)
        
        # Type hints
        orig_hints = original.count(' -> ') + original.count(': str') + original.count(': int')
        mut_hints = mutated.count(' -> ') + mutated.count(': str') + mutated.count(': int')
        if mut_hints > orig_hints:
            delta += 0.05
        
        # Docstrings
        orig_docs = original.count('"""') + original.count("'''")
        mut_docs = mutated.count('"""') + mutated.count("'''")
        if mut_docs > orig_docs:
            delta += 0.05
        
        # Error handling
        orig_try = original.count('try:')
        mut_try = mutated.count('try:')
        if mut_try > orig_try:
            delta += 0.1
        
        # Complexity reduction (fewer lines = cleaner)
        orig_lines = len([l for l in original.split('\n') if l.strip()])
        mut_lines = len([l for l in mutated.split('\n') if l.strip()])
        if mut_lines < orig_lines * 0.9:  # 10% reduction
            delta += 0.05
        
        return round(delta, 3)
    
    async def mutate(
        self,
        code: str,
        archetype: str,
        strategy: Optional[str] = None
    ) -> MutationResult:
        """
        Mutate code using Mistral AI
        
        Args:
            code: Original Python code
            archetype: Organism archetype (cli_applications, web_services, etc.)
            strategy: Optional mutation strategy override
            
        Returns:
            MutationResult with mutated code and metadata
        """
        self.stats.total_attempts += 1
        
        # Select strategy if not specified
        if strategy is None:
            strategy = self._select_mutation_strategy(code, archetype)
        
        # Get prompt template
        prompt_template = self.MUTATION_PROMPTS.get(strategy, self.MUTATION_PROMPTS['behavioral'])
        prompt = prompt_template.format(code=code, archetype=archetype)
        
        # Attempt mutation with retries
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await self._bridge.generate(
                    prompt=prompt,
                    temperature=self.temperature + (attempt * 0.1),  # Increase temp on retry
                    max_tokens=2048
                )
                
                if not response.success:
                    last_error = response.error
                    continue
                
                # Extract Python code from response
                mutated = self._extract_python_code(response.content)
                
                if mutated is None:
                    last_error = "Could not extract valid Python from response"
                    continue
                
                # Validate mutation
                is_valid, reason = self._validate_mutation(code, mutated)
                
                if not is_valid:
                    last_error = reason
                    continue
                
                # Success!
                fitness_delta = self._estimate_fitness_delta(code, mutated, archetype)
                
                self.stats.successful_mutations += 1
                self.stats.total_duration_ms += response.total_duration_ms
                self.stats.mutations_by_type[strategy] = self.stats.mutations_by_type.get(strategy, 0) + 1
                
                return MutationResult(
                    success=True,
                    original_code=code,
                    mutated_code=mutated,
                    mutation_type=strategy,
                    changes_summary=f"{strategy} mutation via aios-mistral",
                    duration_ms=response.total_duration_ms,
                    archetype=archetype,
                    fitness_delta_estimate=fitness_delta
                )
                
            except Exception as e:
                last_error = str(e)
        
        # All attempts failed
        self.stats.failed_mutations += 1
        
        return MutationResult(
            success=False,
            original_code=code,
            mutated_code=code,  # Return original on failure
            mutation_type='failed',
            changes_summary="Mutation failed after retries",
            duration_ms=0.0,
            archetype=archetype,
            error=last_error
        )
    
    async def mutate_batch(
        self,
        organisms: List[Dict[str, Any]],
        max_concurrent: int = 2
    ) -> List[MutationResult]:
        """
        Mutate multiple organisms concurrently
        
        Args:
            organisms: List of dicts with 'code' and 'archetype' keys
            max_concurrent: Max concurrent mutations (limited by VRAM)
            
        Returns:
            List of MutationResults in same order as input
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def limited_mutate(org):
            async with semaphore:
                return await self.mutate(org['code'], org['archetype'])
        
        tasks = [limited_mutate(org) for org in organisms]
        return await asyncio.gather(*tasks)
    
    def get_stats_report(self) -> str:
        """Get formatted statistics report"""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║           MISTRAL MUTATION ENGINE STATISTICS                 ║
╠══════════════════════════════════════════════════════════════╣
║  Total Attempts:        {self.stats.total_attempts:>6}                            ║
║  Successful Mutations:  {self.stats.successful_mutations:>6}                            ║
║  Failed Mutations:      {self.stats.failed_mutations:>6}                            ║
║  Success Rate:          {self.stats.success_rate*100:>6.1f}%                           ║
║  Avg Duration:          {self.stats.avg_duration_ms:>6.0f}ms                           ║
╠══════════════════════════════════════════════════════════════╣
║  Mutations by Type:                                          ║
║    structural:    {self.stats.mutations_by_type.get('structural', 0):>4}                                    ║
║    behavioral:    {self.stats.mutations_by_type.get('behavioral', 0):>4}                                    ║
║    optimization:  {self.stats.mutations_by_type.get('optimization', 0):>4}                                    ║
║    exploration:   {self.stats.mutations_by_type.get('exploration', 0):>4}                                    ║
╚══════════════════════════════════════════════════════════════╝
"""


# ============================================================================
# STANDALONE TEST
# ============================================================================

async def test_mutation_engine():
    """Test mutation engine with sample code"""
    
    sample_code = '''
def calculate_sum(numbers):
    total = 0
    for n in numbers:
        total += n
    return total

if __name__ == "__main__":
    result = calculate_sum([1, 2, 3, 4, 5])
    print(f"Sum: {result}")
'''
    
    print("=" * 70)
    print("MISTRAL MUTATION ENGINE - Integration Test")
    print("=" * 70)
    
    async with MistralMutationEngine(temperature=0.7) as engine:
        print(f"\n[TEST] Mutating sample code (cli_applications archetype)...")
        
        result = await engine.mutate(
            code=sample_code,
            archetype='cli_applications'
        )
        
        if result.success:
            print(f"\n✅ Mutation successful!")
            print(f"   Type: {result.mutation_type}")
            print(f"   Duration: {result.duration_ms:.0f}ms")
            print(f"   Fitness delta: {result.fitness_delta_estimate:+.3f}")
            print(f"\n[MUTATED CODE]")
            print("-" * 40)
            print(result.mutated_code)
            print("-" * 40)
        else:
            print(f"\n❌ Mutation failed: {result.error}")
        
        print(engine.get_stats_report())


if __name__ == "__main__":
    asyncio.run(test_mutation_engine())
