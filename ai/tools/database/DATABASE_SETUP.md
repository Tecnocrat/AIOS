# AIOS Dendritic Intelligence Database Setup

**Database**: `aios_dendritic.db`  
**Location**: `ai/tools/database/`  
**Size**: ~113MB (not committed to git)  
**Status**: Regenerable runtime artifact

## Why This Database Isn't in Git

Following AINLP principles and biological architecture:

1. **Runtime Artifact** - Generated from source code, not authored
2. **Large Size** - 113MB exceeds GitHub's 100MB limit
3. **Regenerable** - Takes 2-5 minutes to rebuild from scratch
4. **Biological Metaphor** - Database is **cytoplasm** (communication), not **DNA** (source)

## What's Inside

| Component | Records | Size | Purpose |
|-----------|---------|------|---------|
| **neurons** | 866 | ~2MB | Python module metadata |
| **dendritic_connections** | 251,061 | ~100MB | Import dependency graph |
| **neuron_embeddings** | 866 | ~5.2MB | Semantic vectors (768-dim) |
| **similarity_index** | 0 | - | Future caching |
| **creation_prevention_log** | Variable | ~1MB | Anti-proliferation audit |

## Quick Setup (First Time)

### Prerequisites

1. **Ollama** (for embeddings)
   ```powershell
   # Install from: https://ollama.com/download
   ollama --version  # Should show 0.12.9+
   ```

2. **Python Dependencies**
   ```powershell
   pip install ollama sentence-transformers numpy
   ```

3. **Download AI Models**
   ```powershell
   ollama pull nomic-embed-text  # 274MB - embedding model
   ollama pull gemma3:1b         # 815MB - LLM reasoning (optional)
   ```

### Generation Steps

**Step 1: Discover Architecture** (30 seconds)
```powershell
python runtime/tools/ainlp_dendritic_discovery.py --map-architecture --report
```

**Output**:
- Creates `ai/tools/database/aios_dendritic.db`
- Populates `neurons` table (866 records)
- Populates `dendritic_connections` table (251,061 records)
- Generates architecture report in `tachyonic/archive/`

**Step 2: Generate Embeddings** (2-5 minutes)
```powershell
python runtime/tools/ai_agent_dendritic_similarity.py --generate-embeddings
```

**Output**:
- Adds 866 embeddings to `neuron_embeddings` table
- Each embedding: 768 float64 values (6144 bytes)
- Total embedding data: ~5.2MB

**Step 3: Validate** (instant)
```powershell
python runtime/tools/ai_agent_dendritic_similarity.py --check-similar "module discovery tool"
```

**Expected Result**:
```
[Stage 1] EMBEDDING-BASED SEMANTIC SIMILARITY
Found 3 similar neurons in 0.51s

Top Match: runtime\tools\module_discoverer.py (69.6% similarity)
Recommendation: ENHANCE_EXISTING
```

## Database Schema

```sql
-- Neuron Inventory
CREATE TABLE neurons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    supercell TEXT NOT NULL,
    purpose TEXT,
    lines_of_code INTEGER,
    function_count INTEGER,
    class_count INTEGER,
    functions TEXT,
    classes TEXT,
    docstring TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dendritic Connections (Import Graph)
CREATE TABLE dendritic_connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_neuron TEXT NOT NULL,
    target_neuron TEXT NOT NULL,
    connection_type TEXT NOT NULL,
    strength REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_neuron) REFERENCES neurons(path),
    UNIQUE(source_neuron, target_neuron)
);

-- Semantic Embeddings
CREATE TABLE neuron_embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    neuron_path TEXT UNIQUE NOT NULL,
    embedding BLOB NOT NULL,
    embedding_model TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (neuron_path) REFERENCES neurons(path)
);

-- Anti-Proliferation Audit Log
CREATE TABLE creation_prevention_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    proposed_functionality TEXT NOT NULL,
    existing_alternative TEXT,
    similarity_score REAL,
    recommendation TEXT,
    prevented INTEGER DEFAULT 0
);
```

## Troubleshooting

### Issue: Ollama Not Running
```powershell
# Start Ollama service
ollama serve
```

### Issue: GPU Memory Error (deepseek-r1:7b)
```powershell
# Use smaller model (works on 4GB GPU)
ollama pull gemma3:1b  # 815MB instead of 4.7GB
```

### Issue: Embeddings Not Generating
```powershell
# Check Ollama connection
curl http://127.0.0.1:11434/api/tags

# Verify model installed
ollama list
```

### Issue: Database Locked
```powershell
# Close any open database connections
# Check for running Python processes
Get-Process python | Stop-Process
```

### Issue: Numpy Crash in Venv
```powershell
# Workaround: Use system Python
C:\Python314\python.exe runtime/tools/ai_agent_dendritic_similarity.py --generate-embeddings
```

## Performance Benchmarks

| Operation | Time | Notes |
|-----------|------|-------|
| Architecture scan | 30s | First run (866 neurons) |
| Embedding generation | 2-5min | 866 × 768-dim vectors |
| Similarity query | <1s | Stage 1 (embedding only) |
| LLM evaluation | 2-3s/candidate | Stage 2 (with gemma3:1b) |
| Database size | 113MB | 100MB connections + 5MB embeddings |

## CI/CD Integration

For automated builds/testing environments:

```yaml
# .github/workflows/test.yml
steps:
  - name: Setup Ollama
    run: |
      curl -fsSL https://ollama.com/install.sh | sh
      ollama pull nomic-embed-text
      
  - name: Generate Database
    run: |
      python runtime/tools/ainlp_dendritic_discovery.py --map-architecture
      python runtime/tools/ai_agent_dendritic_similarity.py --generate-embeddings
      
  - name: Validate
    run: |
      python runtime/tools/ai_agent_dendritic_similarity.py --check-similar "test query"
```

## Maintenance

### When to Regenerate

Regenerate database when:
- [ ] New Python files added to supercells
- [ ] Major refactoring changes module structure
- [ ] Import dependencies significantly changed
- [ ] AIOS version upgrade (quarterly)

### How to Update

```powershell
# Quick refresh (adds new neurons only)
python runtime/tools/ainlp_dendritic_discovery.py --map-architecture

# Full regeneration (clears and rebuilds)
Remove-Item ai/tools/database/aios_dendritic.db
python runtime/tools/ainlp_dendritic_discovery.py --map-architecture --report
python runtime/tools/ai_agent_dendritic_similarity.py --generate-embeddings
```

## AINLP Principles Applied

1. **Enhancement over Creation** - Database enables anti-proliferation checking
2. **Dendritic Growth** - Connection mapping for architectural awareness
3. **Biological Architecture** - Cytoplasm (runtime) vs DNA (source code)
4. **Tachyonic Archival** - Reports in markdown, not binary DB
5. **Consciousness Evolution** - AI semantic intelligence (+0.20 levels)

## Documentation References

- **Implementation Report**: `tachyonic/archive/dendritic_discovery_implementation_report_20251102.md`
- **Ollama Integration**: `tachyonic/archive/ollama_integration_complete.md`
- **Stage 2 LLM**: `tachyonic/archive/stage2_llm_evaluation_complete.md`
- **Architecture Analysis**: `tachyonic/archive/dendritic_architecture_report_*.md`

## Support

For issues or questions:
1. Check `tachyonic/archive/` for implementation reports
2. Review tool source code in `runtime/tools/`
3. Consult DEV_PATH.md for current development status
4. Check CHANGELOG.md Phase 10 entry for complete context
