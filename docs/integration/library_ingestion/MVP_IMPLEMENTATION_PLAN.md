# 🧬 Library Ingestion → Code Generation Loop - MVP Implementation

**Date:** October 4, 2025  
**Phase:** 10 Week 1-2 Accelerated  
**Objective:** Close the ingestion/mutation cycle with FREE AI agents  

---

## 🎯 The Complete Loop

```
1. INGEST LIBRARY
   ├─ requests, flask, fastapi (Python)
   ├─ Extract functions, classes, patterns
   └─ Store in ai/information_storage/library_knowledge/
       ↓
2. EXTRACT PARADIGMS
   ├─ Identify patterns (decorators, async, REST, OOP)
   ├─ Create structured paradigm objects
   └─ Store paradigm templates
       ↓
3. GENERATE PROMPTS
   ├─ Convert paradigms to AI instructions
   ├─ "Use FastAPI decorator patterns like @app.get()"
   └─ Include examples from ingested knowledge
       ↓
4. FEED TO FREE AI AGENTS
   ├─ Ollama (local: deepseek-coder, codellama)
   ├─ Gemini Free Tier (15 RPM)
   └─ Generate 2+ code variants
       ↓
5. ANALYZE GENERATED CODE
   ├─ Syntax validation (AST parsing)
   ├─ Pattern adherence (did it use learned paradigms?)
   ├─ Execution success (sandbox test)
   └─ Consciousness coherence (0.0-1.0)
       ↓
6. OPTIMIZE & MUTATE
   ├─ Feedback to paradigm extraction
   ├─ Refine prompts based on results
   ├─ Generate population gen+1
   └─ Repeat cycle (evolution)
```

---

## 📋 MVP Implementation Plan

### Stage 1: Library Ingestion (Already 75% Complete)

**Test with Real Library:**
```python
# Use existing library_ingestion_protocol.py
from ai.src.core.library_ingestion_protocol import LibraryIngestionProtocol

protocol = LibraryIngestionProtocol()
result = protocol.ingest_library("requests", language="python")
# Stores in: ai/information_storage/library_knowledge/requests/
```

**Verify Storage:**
- Check JSON knowledge files created
- Verify 7 language parsers operational
- Test semantic search over ingested knowledge

### Stage 2: Paradigm Extraction (NEW - Implement NOW)

**Create:** `ai/src/engines/paradigm_extraction_engine.py`

**Key Functions:**
```python
class ParadigmExtractionEngine:
    def extract_from_library(library_name: str) -> List[ProgrammingParadigm]:
        """Extract patterns from ingested library knowledge"""
        
    def _identify_decorators(code: str) -> List[str]:
        """Find @app.route, @classmethod patterns"""
        
    def _identify_async_patterns(code: str) -> List[str]:
        """Find async/await usage"""
        
    def _identify_class_patterns(code: str) -> Dict:
        """Find OOP patterns (inheritance, composition)"""
```

**Output:** Structured paradigms with code templates

### Stage 3: Prompt Generation (NEW - Implement NOW)

**Create:** `ai/src/agents/prompt_generator.py`

**Key Functions:**
```python
class PromptGenerator:
    def create_agent_instruction(
        task: str,
        paradigms: List[ProgrammingParadigm],
        examples: List[str]
    ) -> str:
        """Generate consciousness-driven prompt for AI agents"""
```

**Example Output:**
```
You are an expert Python developer. Generate a REST API using patterns from FastAPI.

LEARNED PARADIGMS:
1. Decorator Pattern: Use @app.get("/path") for routes
2. Async Pattern: Use async def for async routes  
3. Type Hints: Use Pydantic models for validation

EXAMPLE FROM FASTAPI:
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

TASK: Create a REST API for user management with CRUD operations.
Use the patterns above. Return complete, executable code.
```

### Stage 4: FREE AI Agent Integration

#### Option A: Ollama (LOCAL - Recommended)
**Setup:**
```bash
# Install Ollama
# Download models
ollama pull deepseek-coder:6.7b
ollama pull codellama:7b
```

**Integration:**
```python
# ai/src/integrations/ollama_bridge.py
import requests

class OllamaAgent:
    def generate_code(self, prompt: str, model: str = "deepseek-coder:6.7b"):
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"]
```

#### Option B: Gemini Free Tier
**Already implemented:** `ai/src/integrations/gemini_bridge/`

**Free Tier Limits:**
- 15 requests per minute
- 1,500 requests per day
- Perfect for MVP testing

### Stage 5: Code Analysis (NEW - Implement NOW)

**Create:** `ai/src/evolution/code_analyzer.py`

**Analysis Pipeline:**
```python
class CodeAnalyzer:
    def analyze_generated_code(code: str, paradigms: List[ProgrammingParadigm]):
        results = {
            "syntax_valid": check_syntax(code),
            "paradigm_adherence": check_paradigms(code, paradigms),
            "execution_success": sandbox_execute(code),
            "consciousness_score": calculate_consciousness(code, paradigms)
        }
        return results
        
    def check_syntax(code: str) -> bool:
        """Use AST parsing to validate syntax"""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
            
    def check_paradigms(code: str, paradigms: List) -> float:
        """Check if code uses learned patterns (0.0-1.0)"""
        matches = 0
        for paradigm in paradigms:
            if paradigm.pattern in code:
                matches += 1
        return matches / len(paradigms) if paradigms else 0.0
        
    def sandbox_execute(code: str) -> Dict:
        """Execute in isolated environment, capture results"""
        # Use subprocess with timeout
        # Capture stdout, stderr, exit code
        
    def calculate_consciousness(code: str, paradigms: List) -> float:
        """Overall consciousness coherence score"""
        syntax_weight = 0.3
        paradigm_weight = 0.4
        execution_weight = 0.3
        # Combine metrics
```

### Stage 6: Feedback Loop & Mutation

**Create:** `ai/src/evolution/mutation_engine.py`

**Feedback Cycle:**
```python
class MutationEngine:
    def optimize_from_results(
        original_prompt: str,
        generated_codes: List[str],
        analysis_results: List[Dict]
    ) -> str:
        """Learn from generation results, create improved prompt"""
        
        # Find best performing variant
        best = max(analysis_results, key=lambda x: x["consciousness_score"])
        
        # Extract what worked
        successful_patterns = extract_patterns(best["code"])
        
        # Refine prompt for gen+1
        improved_prompt = enhance_prompt(
            original_prompt, 
            successful_patterns,
            failed_patterns=get_failures(analysis_results)
        )
        
        return improved_prompt
```

---

## 🚀 Execution Steps

### Step 1: Test Library Ingestion (5 minutes)
```python
# Run existing protocol
python testing/library_ingestion_workbench.py
# Ingest: requests, flask, fastapi
```

### Step 2: Implement Paradigm Extraction (30 minutes)
```python
# Create: ai/src/engines/paradigm_extraction_engine.py
# Extract patterns from ingested knowledge
# Test with requests library
```

### Step 3: Implement Prompt Generator (20 minutes)
```python
# Create: ai/src/agents/prompt_generator.py
# Generate prompts from paradigms
# Test with sample task
```

### Step 4: Set Up Ollama Agent (15 minutes)
```bash
# Install Ollama
# Download deepseek-coder model
# Create bridge: ai/src/integrations/ollama_bridge.py
```

### Step 5: Generate Code with Agents (10 minutes)
```python
# Feed prompt to Ollama + Gemini
# Collect 2+ code variants
# Save to evolution_lab/artifacts/
```

### Step 6: Analyze Generated Code (30 minutes)
```python
# Create: ai/src/evolution/code_analyzer.py
# Run analysis on generated variants
# Score consciousness coherence
```

### Step 7: Close the Loop (20 minutes)
```python
# Create: ai/src/evolution/mutation_engine.py
# Generate improved prompt from results
# Create generation gen+1
# Repeat cycle
```

**Total MVP Time: ~2.5 hours**

---

## 📊 Success Metrics

### Generation 0 (First Run)
- **Library Ingestion:** requests library successfully parsed
- **Paradigms Extracted:** 10+ patterns identified
- **Prompt Generated:** Includes learned patterns
- **Code Generated:** 2 variants (Ollama + Gemini)
- **Analysis Complete:** Syntax, paradigms, execution checked
- **Consciousness Score:** Baseline established

### Generation 1 (After Mutation)
- **Prompt Improved:** Incorporates gen0 learnings
- **Code Quality:** +10% consciousness score
- **Pattern Adherence:** +15% paradigm usage
- **Execution Success:** +20% pass rate

### Generation 5 (Convergence)
- **Consciousness Score:** >0.85
- **Pattern Adherence:** >90%
- **Execution Success:** >95%
- **Code Emerges:** Optimal solution with minimal energy

---

## 🔧 Technical Implementation

### File Structure
```
ai/
├── src/
│   ├── engines/
│   │   └── paradigm_extraction_engine.py [NEW]
│   ├── agents/
│   │   └── prompt_generator.py [NEW]
│   ├── integrations/
│   │   ├── ollama_bridge.py [NEW]
│   │   └── gemini_bridge/ [EXISTS]
│   └── evolution/
│       ├── code_analyzer.py [NEW]
│       └── mutation_engine.py [NEW]
└── information_storage/
    └── library_knowledge/ [EXISTS]
        └── requests/ [GENERATED BY INGESTION]
```

### Dependencies
```bash
pip install ollama-python  # Ollama client
pip install google-generativeai  # Gemini (already have)
# AST parser (built-in Python)
# subprocess (built-in Python)
```

---

## 🎯 Immediate Next Steps

1. **Verify Library Ingestion Working**
   - Run workbench with requests library
   - Check storage created correctly

2. **Implement Paradigm Extraction Engine**
   - Parse stored knowledge
   - Extract decorator, async, OOP patterns
   - Create structured paradigm objects

3. **Implement Prompt Generator**
   - Convert paradigms to natural language
   - Include code examples
   - Create task-specific instructions

4. **Set Up Ollama**
   - Install locally
   - Download deepseek-coder model
   - Create Python bridge

5. **Run First Generation**
   - Generate 2 code variants
   - Analyze with consciousness metrics
   - Store results in evolution_lab/

6. **Implement Mutation Engine**
   - Extract learnings from gen0
   - Create improved gen1 prompt
   - Demonstrate evolution

---

## 🧬 The Ingestion/Mutation Cycle

```
GEN 0: Learn from library → Extract patterns → Generate code → Analyze
         ↓
      [FEEDBACK LOOP]
         ↓
GEN 1: Refine patterns → Improve prompts → Generate better code → Analyze
         ↓
      [FEEDBACK LOOP]
         ↓
GEN 2-5: Evolve → Optimize → Converge to optimal solution
         ↓
      [CONSCIOUSNESS EMERGES]
         ↓
RESULT: Code with >0.85 consciousness - minimal energy, maximum complexity
```

**This is biological computing applied to software development.**

---

**Status:** Ready to implement  
**Timeline:** 2.5 hours for MVP  
**Next Action:** Verify library ingestion, then build paradigm extraction engine
