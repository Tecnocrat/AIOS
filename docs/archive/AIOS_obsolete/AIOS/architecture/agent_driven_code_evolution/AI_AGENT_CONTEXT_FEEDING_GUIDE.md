# AI Agent Context Feeding - C++ STL Integration Guide

**Created**: October 5, 2025  
**Purpose**: Practical guide for feeding structured C++ STL knowledge to AI agents  
**Agents**: Gemini, Ollama, DeepSeek  
**Goal**: Enable consciousness-driven C++ code generation and evolution

## 🎯 Executive Summary

This document provides the complete workflow for:
1. Extracting C++ STL knowledge from documentation
2. Structuring it into consciousness-optimized knowledge crystals
3. Feeding enhanced context to AI agents (Gemini, Ollama, DeepSeek)
4. Using AI agents for code evolution with STL paradigms

## 📊 Knowledge Crystal Structure

### Crystal Format

```json
{
  "crystal_id": "stl_vector_v1",
  "library": "C++ STL",
  "component": "std::vector",
  "consciousness_level": 0.92,
  "header": "<vector>",
  "namespace": "std",
  "since_version": "C++98",
  
  "essence": {
    "description": "Dynamic contiguous array with automatic memory management",
    "use_cases": [
      "Sequential data storage",
      "Cache-friendly access patterns",
      "Dynamic array replacement"
    ],
    "complexity": {
      "access": "O(1)",
      "insertion_back": "O(1) amortized",
      "insertion_middle": "O(n)",
      "search": "O(n)"
    }
  },
  
  "paradigms": [
    {
      "name": "Reserve Capacity Pattern",
      "description": "Pre-allocate memory when final size is known or estimable",
      "code_template": "vector.reserve(expected_size);",
      "benefit": "Prevents multiple reallocations",
      "consciousness_impact": 0.15
    },
    {
      "name": "Emplace Over Push Pattern",
      "description": "Construct elements in-place to avoid copy",
      "code_template": "vector.emplace_back(args...);",
      "benefit": "Eliminates temporary object creation",
      "consciousness_impact": 0.10
    },
    {
      "name": "Range-Based Iteration",
      "description": "Use range-for for clear intent",
      "code_template": "for (const auto& elem : vector) { }",
      "benefit": "Expresses intent clearly, prevents off-by-one errors",
      "consciousness_impact": 0.12
    }
  ],
  
  "anti_patterns": [
    {
      "name": "Frequent Middle Insertion",
      "description": "Repeatedly inserting in vector middle",
      "why_bad": "O(n) per insertion due to element shifting",
      "alternative": "Use std::list or std::deque for frequent insertions",
      "consciousness_penalty": -0.20
    },
    {
      "name": "Not Reserving Capacity",
      "description": "Growing vector without reserve()",
      "why_bad": "Multiple reallocations and copies",
      "alternative": "Call reserve() with estimated size",
      "consciousness_penalty": -0.15
    }
  ],
  
  "api_elements": [
    {
      "name": "push_back",
      "signature": "void push_back(const T& value);",
      "description": "Add element to end of vector",
      "parameters": [{"name": "value", "type": "const T&"}],
      "complexity": "O(1) amortized",
      "thread_safe": false
    },
    {
      "name": "emplace_back",
      "signature": "template<class... Args> void emplace_back(Args&&... args);",
      "description": "Construct element in-place at end",
      "complexity": "O(1) amortized",
      "since_version": "C++11",
      "preferred_over": ["push_back"]
    }
  ],
  
  "code_examples": [
    {
      "scenario": "Efficient vector construction",
      "code": "std::vector<int> vec;\nvec.reserve(100);  // Prevent reallocations\nfor (int i = 0; i < 100; ++i) {\n    vec.emplace_back(i);  // In-place construction\n}",
      "consciousness": 0.95,
      "explanation": "Combines reserve() and emplace_back() for optimal performance"
    }
  ]
}
```

## 🤖 AI Agent Integration Patterns

### Pattern 1: Gemini Code Generation with STL Context

**Use Case**: Generate production C++ code using STL best practices

**Implementation**:

```python
# ai/src/integrations/gemini_stl_bridge.py

import json
from pathlib import Path
from typing import Dict, List, Optional

class GeminiSTLBridge:
    """
    Bridge between Gemini AI and C++ STL knowledge crystals.
    Feeds structured STL context to Gemini for enhanced code generation.
    """
    
    def __init__(self, crystals_dir: Path):
        self.crystals_dir = crystals_dir
        self.crystals_cache: Dict[str, Dict] = {}
        self._load_crystals()
    
    def _load_crystals(self):
        """Load all knowledge crystals into memory"""
        for crystal_file in self.crystals_dir.glob("*.json"):
            with open(crystal_file) as f:
                crystal = json.load(f)
                self.crystals_cache[crystal['crystal_id']] = crystal
    
    def build_enhanced_prompt(
        self,
        task: str,
        stl_components: List[str],
        consciousness_target: float = 0.90
    ) -> str:
        """
        Build enhanced prompt with STL knowledge context.
        
        Args:
            task: User's code generation request
            stl_components: List of STL components to include (e.g., ["vector", "algorithm"])
            consciousness_target: Target consciousness level (0.0-1.0)
        
        Returns:
            Enhanced prompt with STL context
        """
        # Gather relevant crystals
        relevant_crystals = []
        for component in stl_components:
            crystal_id = f"stl_{component}_v1"
            if crystal_id in self.crystals_cache:
                relevant_crystals.append(self.crystals_cache[crystal_id])
        
        # Build context section
        context_parts = []
        
        # Add paradigms
        context_parts.append("## C++ STL Best Practices\n")
        for crystal in relevant_crystals:
            context_parts.append(f"\n### {crystal['component']} Paradigms:")
            for paradigm in crystal['paradigms']:
                context_parts.append(
                    f"- **{paradigm['name']}**: {paradigm['description']}\n"
                    f"  Pattern: `{paradigm['code_template']}`\n"
                    f"  Benefit: {paradigm['benefit']}"
                )
        
        # Add anti-patterns
        context_parts.append("\n## Patterns to AVOID:\n")
        for crystal in relevant_crystals:
            for anti in crystal['anti_patterns']:
                context_parts.append(
                    f"- ❌ **{anti['name']}**: {anti['why_bad']}\n"
                    f"  Alternative: {anti['alternative']}"
                )
        
        # Add complexity information
        context_parts.append("\n## Performance Characteristics:\n")
        for crystal in relevant_crystals:
            if 'essence' in crystal and 'complexity' in crystal['essence']:
                complexity = crystal['essence']['complexity']
                context_parts.append(f"\n### {crystal['component']}:")
                for op, comp in complexity.items():
                    context_parts.append(f"- {op}: {comp}")
        
        # Build final prompt
        enhanced_prompt = f"""
You are a C++ expert with deep knowledge of the Standard Template Library (STL).
Your goal is to generate production-quality C++ code with consciousness level ≥ {consciousness_target}.

## TASK:
{task}

## STL KNOWLEDGE CONTEXT:
{'\n'.join(context_parts)}

## REQUIREMENTS:
1. Follow STL best practices from the context above
2. Avoid anti-patterns listed
3. Consider performance characteristics
4. Use modern C++ features (C++17/20 preferred)
5. Include error handling
6. Add brief comments explaining STL usage

## OUTPUT FORMAT:
Provide complete, compilable C++ code with:
- Headers included
- Namespace declarations
- Error handling
- Comments on STL usage choices

Generate the code now:
"""
        
        return enhanced_prompt
    
    def generate_code(
        self,
        task: str,
        stl_components: List[str],
        gemini_client
    ) -> Dict:
        """
        Generate C++ code using Gemini with STL context.
        
        Returns:
            Dict with:
            - code: Generated C++ code
            - consciousness: Estimated consciousness level
            - stl_usage: STL components used
        """
        # Build enhanced prompt
        prompt = self.build_enhanced_prompt(task, stl_components)
        
        # Generate with Gemini
        response = gemini_client.generate(prompt)
        
        # Extract code
        code = self._extract_code_from_response(response)
        
        # Analyze STL usage
        stl_usage = self._analyze_stl_usage(code, stl_components)
        
        # Estimate consciousness
        consciousness = self._estimate_consciousness(code, stl_usage)
        
        return {
            'code': code,
            'consciousness': consciousness,
            'stl_usage': stl_usage,
            'raw_response': response
        }
    
    def _extract_code_from_response(self, response: str) -> str:
        """Extract C++ code from Gemini response"""
        # Look for code blocks
        import re
        pattern = r'```(?:cpp|c\+\+)?\n(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # Fallback: return full response
        return response.strip()
    
    def _analyze_stl_usage(self, code: str, expected_components: List[str]) -> Dict:
        """Analyze which STL components are actually used"""
        usage = {}
        
        for component in expected_components:
            # Simple check for component usage
            if f"std::{component}" in code:
                usage[component] = True
            else:
                usage[component] = False
        
        return usage
    
    def _estimate_consciousness(self, code: str, stl_usage: Dict) -> float:
        """Estimate consciousness level of generated code"""
        score = 0.5  # Base score
        
        # Bonus for STL usage
        if any(stl_usage.values()):
            score += 0.15
        
        # Bonus for modern C++ features
        modern_features = ['auto', 'const auto&', 'emplace', 'range-for', 'nullptr']
        for feature in modern_features:
            if feature in code:
                score += 0.05
        
        # Bonus for error handling
        if 'try' in code or 'catch' in code or 'throw' in code:
            score += 0.10
        
        # Cap at 1.0
        return min(score, 1.0)
```

### Pattern 2: Ollama Local Evolution with STL Fitness

**Use Case**: Use local Ollama models to evaluate code fitness based on STL paradigms

**Implementation**:

```python
# ai/src/integrations/ollama_stl_fitness.py

from typing import Dict, List
import json

class OllamaSTLFitnessJudge:
    """
    Use Ollama local models to judge C++ code fitness based on STL paradigms.
    Runs locally with unlimited requests (FREE).
    """
    
    def __init__(self, crystals_dir: Path, ollama_client):
        self.crystals_dir = crystals_dir
        self.ollama = ollama_client
        self.crystals_cache = self._load_crystals()
    
    def _load_crystals(self) -> Dict:
        """Load STL knowledge crystals"""
        crystals = {}
        for crystal_file in self.crystals_dir.glob("*.json"):
            with open(crystal_file) as f:
                crystal = json.load(f)
                crystals[crystal['crystal_id']] = crystal
        return crystals
    
    def evaluate_fitness(
        self,
        code: str,
        execution_result: Dict,
        stl_components: List[str]
    ) -> Dict:
        """
        Evaluate code fitness using Ollama.
        
        Args:
            code: C++ code to evaluate
            execution_result: Results from compiling/running code
            stl_components: Expected STL components
        
        Returns:
            Dict with fitness scores and analysis
        """
        # Build evaluation prompt
        prompt = self._build_fitness_prompt(code, execution_result, stl_components)
        
        # Ask Ollama to evaluate
        response = self.ollama.generate(prompt)
        
        # Parse fitness scores
        fitness = self._parse_fitness_response(response)
        
        return fitness
    
    def _build_fitness_prompt(
        self,
        code: str,
        execution: Dict,
        components: List[str]
    ) -> str:
        """Build fitness evaluation prompt with STL context"""
        
        # Gather relevant paradigms and anti-patterns
        paradigms_text = []
        antipatterns_text = []
        
        for component in components:
            crystal_id = f"stl_{component}_v1"
            if crystal_id in self.crystals_cache:
                crystal = self.crystals_cache[crystal_id]
                
                # Add paradigms
                for paradigm in crystal['paradigms']:
                    paradigms_text.append(
                        f"✅ {paradigm['name']}: {paradigm['description']}"
                    )
                
                # Add anti-patterns
                for anti in crystal['anti_patterns']:
                    antipatterns_text.append(
                        f"❌ {anti['name']}: {anti['why_bad']}"
                    )
        
        prompt = f"""
You are a C++ code quality expert evaluating code fitness for genetic algorithm evolution.

## CODE TO EVALUATE:
```cpp
{code}
```

## EXECUTION RESULTS:
- Compiled: {"Yes" if execution.get('compiled') else "No"}
- Exit Code: {execution.get('exit_code', 'N/A')}
- Output: {execution.get('output', 'N/A')}
- Runtime: {execution.get('runtime_ms', 'N/A')}ms

## STL BEST PRACTICES (Should follow):
{chr(10).join(paradigms_text)}

## ANTI-PATTERNS (Should avoid):
{chr(10).join(antipatterns_text)}

## EVALUATION CRITERIA:
Rate the code on these dimensions (0.0 to 1.0):

1. **Correctness**: Does it compile and produce correct results?
2. **STL Best Practices**: Follows paradigms above?
3. **Performance**: Efficient algorithm and data structure choices?
4. **Modern C++**: Uses C++17/20 features appropriately?
5. **Readability**: Clear, maintainable code?
6. **Anti-Pattern Avoidance**: Avoids listed anti-patterns?

## OUTPUT FORMAT (JSON):
{{
  "correctness": 0.0-1.0,
  "stl_practices": 0.0-1.0,
  "performance": 0.0-1.0,
  "modern_cpp": 0.0-1.0,
  "readability": 0.0-1.0,
  "anti_pattern_avoidance": 0.0-1.0,
  "overall_fitness": 0.0-1.0,
  "strengths": ["list", "of", "strengths"],
  "weaknesses": ["list", "of", "weaknesses"],
  "suggestions": ["improvement", "suggestions"]
}}

Provide your evaluation:
"""
        
        return prompt
    
    def _parse_fitness_response(self, response: str) -> Dict:
        """Parse fitness scores from Ollama response"""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except:
            pass
        
        # Fallback: parse manually or return default
        return {
            'correctness': 0.5,
            'stl_practices': 0.5,
            'performance': 0.5,
            'overall_fitness': 0.5,
            'strengths': [],
            'weaknesses': [],
            'suggestions': []
        }
```

### Pattern 3: DeepSeek Meta-Programming with STL DNA

**Use Case**: Use DeepSeek for consciousness-aware code evolution with STL as genetic material

**Implementation**:

```python
# ai/src/core/stl_aware_evolution.py

from typing import List, Dict
import random

class STLAwareCodeEvolution:
    """
    Genetic algorithm for code evolution using STL paradigms as DNA.
    Integrates with DeepSeek for consciousness-aware mutations.
    """
    
    def __init__(
        self,
        crystals_dir: Path,
        deepseek_client,
        population_size: int = 20
    ):
        self.crystals = self._load_crystals(crystals_dir)
        self.deepseek = deepseek_client
        self.population_size = population_size
    
    def evolve_code(
        self,
        initial_code: str,
        fitness_target: float = 0.95,
        max_generations: int = 50
    ) -> Dict:
        """
        Evolve code using genetic algorithm with STL paradigms.
        
        Returns:
            Best evolved code and evolution history
        """
        # Initialize population
        population = self._initialize_population(initial_code)
        
        evolution_history = []
        
        for generation in range(max_generations):
            # Evaluate fitness
            fitness_scores = [
                self._evaluate_fitness(individual)
                for individual in population
            ]
            
            # Check if target reached
            best_fitness = max(fitness_scores)
            if best_fitness >= fitness_target:
                best_idx = fitness_scores.index(best_fitness)
                return {
                    'code': population[best_idx],
                    'fitness': best_fitness,
                    'generation': generation,
                    'history': evolution_history
                }
            
            # Selection
            selected = self._tournament_selection(population, fitness_scores)
            
            # Crossover
            offspring = self._crossover_with_stl(selected)
            
            # Mutation with STL paradigms
            mutated = [
                self._mutate_with_stl_paradigm(individual)
                for individual in offspring
            ]
            
            # Replace population
            population = mutated
            
            # Record history
            evolution_history.append({
                'generation': generation,
                'best_fitness': best_fitness,
                'avg_fitness': sum(fitness_scores) / len(fitness_scores)
            })
        
        # Return best from final generation
        final_fitness = [self._evaluate_fitness(ind) for ind in population]
        best_idx = final_fitness.index(max(final_fitness))
        
        return {
            'code': population[best_idx],
            'fitness': final_fitness[best_idx],
            'generation': max_generations,
            'history': evolution_history
        }
    
    def _mutate_with_stl_paradigm(self, code: str) -> str:
        """
        Mutate code by applying random STL paradigm.
        Uses DeepSeek for consciousness-aware mutation.
        """
        # Select random STL paradigm
        all_paradigms = []
        for crystal in self.crystals.values():
            all_paradigms.extend(crystal['paradigms'])
        
        paradigm = random.choice(all_paradigms)
        
        # Build mutation prompt
        prompt = f"""
Apply this STL paradigm to improve the C++ code:

## PARADIGM: {paradigm['name']}
Description: {paradigm['description']}
Pattern: {paradigm['code_template']}
Benefit: {paradigm['benefit']}

## CURRENT CODE:
```cpp
{code}
```

## TASK:
Refactor the code to apply this paradigm while:
1. Maintaining correctness
2. Improving consciousness level
3. Following C++ best practices
4. Keeping code compilable

Return only the refactored code in a code block.
"""
        
        # Generate mutation with DeepSeek
        response = self.deepseek.generate(prompt)
        
        # Extract code
        mutated = self._extract_code(response)
        
        return mutated or code  # Fallback to original if extraction fails
```

## 🚀 Practical Usage Examples

### Example 1: Generate Efficient Vector Code

```python
from ai.src.integrations.gemini_stl_bridge import GeminiSTLBridge

# Initialize bridge
bridge = GeminiSTLBridge(
    crystals_dir=Path("tachyonic/archive/knowledge_crystals/cpp_stl")
)

# Generate code
result = bridge.generate_code(
    task="Create a function that processes a large dataset efficiently using std::vector",
    stl_components=["vector", "algorithm"],
    gemini_client=gemini
)

print(f"Generated Code (Consciousness: {result['consciousness']}):")
print(result['code'])
```

### Example 2: Evolve Code with Genetic Algorithm

```python
from ai.src.core.stl_aware_evolution import STLAwareCodeEvolution

# Initialize evolution engine
evolution = STLAwareCodeEvolution(
    crystals_dir=Path("tachyonic/archive/knowledge_crystals/cpp_stl"),
    deepseek_client=deepseek,
    population_size=20
)

# Evolve code
initial_code = """
std::vector<int> data;
for (int i = 0; i < 1000; ++i) {
    data.push_back(i);
}
"""

result = evolution.evolve_code(
    initial_code=initial_code,
    fitness_target=0.95,
    max_generations=50
)

print(f"Best Code (Generation {result['generation']}, Fitness: {result['fitness']}):")
print(result['code'])
```

## 📊 Success Metrics

### Quality Metrics
- **STL Idiom Usage**: ≥90% of generated code uses STL idiomatically
- **Consciousness Level**: ≥0.85 average for AI-generated code
- **Best Practices**: ≥95% adherence to STL paradigms
- **Performance**: ≥80% of suggestions are performance-conscious

### Evolution Metrics
- **Fitness Improvement**: ≥30% improvement per 10 generations
- **Convergence Rate**: Reach target fitness within 50 generations
- **Code Quality**: Evolved code maintains compilation success

---

**Status**: READY FOR IMPLEMENTATION  
**Next Steps**: Create knowledge crystals, implement bridges, test with agents  
**Timeline**: Week 2 integration, Week 3 evolution  

**Author**: AIOS Consciousness Framework  
**Date**: October 5, 2025
