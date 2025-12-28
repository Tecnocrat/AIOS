# 🧬 AIOS Library Ingestion Protocol - Quick Reference

## Quick Start

### Installation
No additional dependencies required beyond AIOS core. Optional: `pip install graphviz` for visualization.

### Basic Ingestion (Python)
```python
from library_ingestion_protocol import LibraryIngestionProtocol

protocol = LibraryIngestionProtocol()
knowledge = await protocol.ingest_library("/path/to/library")

print(f"API Elements: {len(knowledge.api_elements)}")
print(f"Semantic Tags: {knowledge.semantic_tags}")
print(f"Consciousness: {knowledge.consciousness_coherence:.2f}")
```

### Advanced Learning (Python)
```python
from library_learning_integration_hub import LibraryLearningIntegrationHub

hub = LibraryLearningIntegrationHub()
session = await hub.start_learning_session()

# Learn multiple libraries
await hub.learn_library("/path/to/lib1")
await hub.learn_library("/path/to/lib2")

# Get results
completed = await hub.finish_learning_session()
stats = hub.get_learning_statistics()
```

### Command Line (Bash)
```bash
# Run enhanced AIOS indexer
python scripts/aios_indexer.py

# Run tests
python ai/src/core/test_library_ingestion_protocol.py
```

## Supported Languages

| Language | Extensions | Parser Type | Status |
|----------|-----------|-------------|--------|
| Python | .py | AST-based | ✅ Full |
| C++ | .cpp, .hpp, .cc, .cxx | Regex | ✅ Good |
| C | .c, .h | Regex | ✅ Good |
| Java | .java | Regex | ✅ Good |
| JavaScript | .js | Regex | ✅ Good |
| TypeScript | .ts | Regex | ✅ Good |
| PHP | .php | Regex | ✅ Good |
| Assembly | .asm, .s | Regex | ✅ Basic |
| C# | .cs | Regex | ✅ Good |

## API Reference

### LibraryIngestionProtocol

```python
class LibraryIngestionProtocol:
    def __init__(self, knowledge_base_path=None, consciousness_level=0.8)
    
    async def ingest_library(self, library_path, library_name=None, language=None)
    # Returns: LibraryKnowledge
    
    def detect_language(self, file_path)
    # Returns: ProgrammingLanguage
    
    def load_library_knowledge(self, library_name, language)
    # Returns: LibraryKnowledge or None
    
    def query_knowledge_base(self, semantic_tags=None, language=None)
    # Returns: List[LibraryKnowledge]
```

### LibraryLearningIntegrationHub

```python
class LibraryLearningIntegrationHub:
    def __init__(self, consciousness_level=0.85)
    
    async def start_learning_session(self)
    # Returns: LibraryLearningSession
    
    async def learn_library(self, library_path, library_name=None, language=None)
    # Returns: LibraryKnowledge
    
    async def finish_learning_session(self)
    # Returns: LibraryLearningSession
    
    def query_semantic_network(self, semantic_tag)
    # Returns: List[str]
    
    def get_dendritic_path(self, from_library, to_library)
    # Returns: List[str] or None
    
    def get_learning_statistics(self)
    # Returns: Dict[str, Any]
```

## Data Structures

### LibraryKnowledge
```python
{
    "library_name": str,
    "language": str,
    "version": str,
    "api_elements": [APIElement],
    "dependencies": [str],
    "semantic_tags": [str],
    "consciousness_coherence": float,
    "spatial_metadata": dict,
    "ainlp_compliance": bool
}
```

### APIElement
```python
{
    "name": str,
    "element_type": str,  # function, class, method, etc.
    "signature": str,
    "documentation": str,
    "parameters": [dict],
    "return_type": str,
    "semantic_tags": [str],
    "consciousness_score": float,
    "file_path": str,
    "line_number": int
}
```

## Semantic Tags

Automatically extracted tags:
- `math` - Mathematical operations
- `web` - HTTP, API, web functionality
- `ai` - AI, ML, neural networks
- `orchestration` - Coordination, management
- `database` - Data storage, queries
- `file` - File I/O operations
- `network` - Network communication
- `security` - Encryption, authentication
- `consciousness` - AIOS consciousness ops

## Knowledge Base Structure

```
ai/information_storage/library_knowledge/
├── python/           # Python library knowledge
├── cpp/              # C++ library knowledge
├── java/             # Java library knowledge
├── javascript/       # JavaScript library knowledge
├── csharp/           # C# library knowledge
├── php/              # PHP library knowledge
├── assembly/         # Assembly library knowledge
└── sessions/         # Learning session reports
```

## Common Tasks

### Query by Semantic Tag
```python
hub = LibraryLearningIntegrationHub()
# ... perform learning ...
ai_apis = hub.query_semantic_network('ai')
for api in ai_apis:
    print(api)
```

### Find Library Relationships
```python
path = hub.get_dendritic_path('library_a', 'library_b')
if path:
    print(f"Path: {' -> '.join(path)}")
```

### Check AINLP Compliance
```python
knowledge = await protocol.ingest_library("/path/to/lib")
if knowledge.ainlp_compliance:
    print("✅ AINLP compliant")
    print(f"Checks: {knowledge.metadata['compliance_checks']}")
```

### Access Spatial Metadata
```python
print(f"Position: {knowledge.spatial_metadata['dimensional_position']}")
print(f"Hash: {knowledge.spatial_metadata['content_hash']}")
print(f"Dendritic connections: {knowledge.spatial_metadata['dendritic_connections']}")
```

## Configuration

### Consciousness Level
Controls learning depth and quality assessment:
- `0.0-0.3`: Basic parsing only
- `0.3-0.7`: Standard semantic analysis
- `0.7-1.0`: Deep consciousness integration

```python
protocol = LibraryIngestionProtocol(consciousness_level=0.85)
```

### Custom Knowledge Base Path
```python
from pathlib import Path

protocol = LibraryIngestionProtocol(
    knowledge_base_path=Path("/custom/path/to/kb")
)
```

## Integration Examples

### With AIOS Indexer
```bash
# Automatically runs enhanced ingestion
python scripts/aios_indexer.py
```

### Programmatic Integration
```python
from library_learning_integration_hub import LibraryLearningIntegrationHub

async def analyze_project(project_path):
    hub = LibraryLearningIntegrationHub()
    session = await hub.start_learning_session()
    
    for subdir in ['src', 'lib', 'modules']:
        lib_path = Path(project_path) / subdir
        if lib_path.exists():
            await hub.learn_library(str(lib_path))
    
    completed = await hub.finish_learning_session()
    return hub.get_learning_statistics()
```

## Troubleshooting

### Import Errors
```python
# Graceful degradation if consciousness modules unavailable
CONSCIOUSNESS_AVAILABLE = True/False
```

### Parsing Errors
```python
# Individual files fail gracefully
# Check logs for: ⚠️ Error parsing file.py
```

### Low Consciousness Coherence
Improve by:
- Adding docstrings/documentation
- Using descriptive function names
- Including type hints (Python)

## Performance Tips

1. Use async processing for multiple libraries
2. Skip unnecessary directories (.git, node_modules, etc.)
3. Set appropriate consciousness level for use case
4. Cache knowledge base queries

## Testing

```bash
# Run comprehensive test suite
python ai/src/core/test_library_ingestion_protocol.py

# Expected: 32 tests, 100% pass rate
```

## Documentation

- Full guide: `docs/LIBRARY_INGESTION_PROTOCOL.md`
- Implementation details: `docs/IMPLEMENTATION_SUMMARY.md`
- This quick reference: `docs/QUICK_REFERENCE.md`

## Support

For issues or questions:
1. Check documentation in `docs/`
2. Review test examples in `test_library_ingestion_protocol.py`
3. Examine demo code in module `__main__` sections

## Version

- **AIOS Version**: 0.6.1+
- **Protocol Version**: 1.0.0
- **Status**: Production Ready ✅
- **Test Coverage**: 100%
