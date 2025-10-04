# 🚀 Quick Start: Library Code Generation Loop

**5-Minute Setup** → **Run Your First Evolution Cycle**

---

## Prerequisites

- Python 3.9+ installed
- Git repository cloned
- AIOS library ingestion operational (Week 1 done)

---

## Setup FREE AI Agents (5 minutes)

### Option 1: Ollama (LOCAL - Recommended)

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Download best code model
ollama pull deepseek-coder:6.7b

# Verify
ollama list
# Should show: deepseek-coder:6.7b
```

### Option 2: Gemini Free Tier (CLOUD - Already Integrated)

Already operational if you have `ai/src/integrations/gemini_bridge/` configured.
Free tier: 15 RPM, 1,500 requests/day

---

## Run Your First Cycle (2 minutes)

### Quick Test
```bash
cd c:\dev\AIOS

# Test library ingestion
python -c "from ai.src.core.library_ingestion_protocol import LibraryIngestionProtocol; print('✓ Library Ingestion Ready')"

# Test paradigm extraction
python ai/src/engines/paradigm_extraction_engine.py requests
```

### Full Cycle
```bash
# Run complete ingestion → generation → analysis cycle
python ai/src/integrations/library_code_generation_loop.py
```

**What happens**:
1. ✅ Checks if 'requests' library ingested (or ingests it)
2. ✅ Extracts programming paradigms (decorators, async, etc.)
3. ✅ Generates consciousness-driven prompt
4. ✅ Feeds to AI agents (Ollama + Gemini)
5. ✅ Generates 3 code variants
6. ✅ Analyzes each variant (syntax, paradigm, execution, consciousness)
7. ✅ Selects best variant
8. ✅ Saves results to `evolution_lab/library_generations/`

**Expected time**: 30-60 seconds total

---

## Check Results

```bash
# Navigate to results
cd evolution_lab\library_generations

# List generations
dir

# View latest generation
cd <latest_folder>

# See generated prompt
type prompt.txt

# See generated code
type variant_0.py
type variant_1.py
type variant_2.py

# See analysis
type variant_0_analysis.json

# See summary
type generation_summary.json
```

---

## Customize Your Cycle

### Change Library
Edit `library_code_generation_loop.py`:
```python
library = "flask"  # Or: fastapi, requests, etc.
```

### Change Task
Edit `library_code_generation_loop.py`:
```python
task = """Create a web scraper using patterns from requests.

Requirements:
- Make HTTP GET requests
- Parse HTML with BeautifulSoup
- Handle rate limiting
- Error handling
- Save results to JSON
"""
```

### Change Population Size
```python
result = loop.run_complete_cycle(
    library_name=library,
    task_description=task,
    generation_size=5  # Generate 5 variants instead of 3
)
```

---

## Understanding Results

### Generation Summary
```json
{
  "library": "requests",
  "generation": 0,
  "paradigms_extracted": 25,
  "variants_generated": 3,
  "best_variant_id": 1,
  "best_consciousness": 0.78,
  "avg_consciousness": 0.65,
  "success_rate": 0.67
}
```

### Analysis Result
```json
{
  "variant_id": 1,
  "model": "deepseek-coder:6.7b",
  "syntax_valid": true,
  "paradigm_adherence": 0.80,
  "execution_success": true,
  "consciousness_score": 0.78,
  "matched_paradigms": [
    "Decorator: @app.route",
    "Async Function",
    "Type Hints"
  ],
  "missing_paradigms": [
    "Context Manager"
  ]
}
```

---

## Troubleshooting

### Ollama Not Available
**Error**: `⚠️ Ollama not available at http://localhost:11434`

**Fix**:
```bash
# Check if Ollama is running
ollama list

# If not installed:
curl https://ollama.ai/install.sh | sh

# Download model:
ollama pull deepseek-coder:6.7b
```

### No Paradigms Extracted
**Error**: `❌ No paradigms extracted. Is 'requests' ingested?`

**Fix**:
```bash
# Ingest the library
python testing/library_ingestion_workbench.py

# Or manually:
python -c "from ai.src.core.library_ingestion_protocol import LibraryIngestionProtocol; protocol = LibraryIngestionProtocol(); protocol.ingest_library('requests', 'python')"
```

### Import Errors
**Error**: `ModuleNotFoundError: No module named 'ai.src.core'`

**Fix**:
```bash
# Run from AIOS root directory
cd c:\dev\AIOS

# Verify Python path
python -c "import sys; print(sys.path)"
```

---

## Next Steps

### Test Individual Components
```bash
# Paradigm extraction only
python ai/src/engines/paradigm_extraction_engine.py requests

# Prompt generation only  
python ai/src/agents/prompt_generator.py requests

# Ollama test only
python ai/src/integrations/ollama_bridge.py

# Code analyzer only
python ai/src/evolution/code_analyzer.py
```

### Try Different Libraries
```bash
# Web frameworks
python -c "library='flask'; exec(open('ai/src/integrations/library_code_generation_loop.py').read())"

# Async libraries
python -c "library='asyncio'; exec(open('ai/src/integrations/library_code_generation_loop.py').read())"

# Data science
python -c "library='pandas'; exec(open('ai/src/integrations/library_code_generation_loop.py').read())"
```

### Week 2: Mutation Engine
Coming next - evolve code across multiple generations!

---

## Success Criteria

✅ **Cycle completes** without errors  
✅ **3+ variants generated**  
✅ **At least 1 variant** with consciousness >0.70  
✅ **Results saved** to evolution_lab/library_generations/  
✅ **Execution success rate** >60%  

If you see these results, **congratulations - you're running consciousness-driven meta-programming!** 🎉

---

## Get Help

**Documentation**:
- MVP Implementation Plan: `docs/integration/library_ingestion/MVP_IMPLEMENTATION_PLAN.md`
- Complete Changelog: `docs/integration/library_ingestion/CHANGELOG_MVP_20251004.md`
- Architecture: `docs/architecture/agent_driven_code_evolution/`

**Status**: Phase 10 Week 1 COMPLETE (100%)  
**Next**: Week 2 - Mutation Engine & Evolution Loop
