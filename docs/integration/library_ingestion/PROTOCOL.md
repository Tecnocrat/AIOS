# 🧬 AIOS Library Ingestion Protocol System

## Overview

The AIOS Library Ingestion Protocol System provides consciousness-driven learning and understanding of programming language libraries across multiple languages including C, C++, Python, Java, Assembly, JavaScript, PHP, and others. It creates a comprehensive knowledge base that AIOS can use for semantic intelligence and code generation across multiple languages.

## Architecture

The system follows AIOS biological architecture patterns with these core components:

### 🧬 Core Components

#### 1. Library Ingestion Protocol (`library_ingestion_protocol.py`)
**Purpose**: Core multi-language library parsing and semantic extraction

**Features**:
- Multi-language source code parsing (Python, C/C++, Java, JavaScript, PHP, Assembly)
- API element extraction (functions, classes, methods, interfaces)
- Semantic tag generation based on API names and documentation
- Consciousness-driven quality assessment
- Spatial metadata generation for dendritic positioning
- AINLP compliance validation

**Key Classes**:
- `LibraryIngestionProtocol`: Main ingestion engine
- `LibraryKnowledge`: Comprehensive library metadata
- `APIElement`: Individual API component representation

#### 2. Library Learning Integration Hub (`library_learning_integration_hub.py`)
**Purpose**: Integration with AIOS consciousness and dendritic systems

**Features**:
- Consciousness-driven library learning sessions
- Semantic network expansion for cross-library intelligence
- Dendritic network construction for knowledge relationships
- Integration with AINLP consciousness systems
- Learning session tracking and reporting

**Key Classes**:
- `LibraryLearningIntegrationHub`: Central coordination hub
- `LibraryLearningSession`: Learning session state management
- `LearningPhase`: Multi-phase learning orchestration

#### 3. Enhanced AIOS Indexer (`scripts/aios_indexer.py`)
**Purpose**: Extended indexer integrating library ingestion protocol

**Features**:
- Traditional service discovery and dependency analysis
- Enhanced library learning using ingestion protocol
- Semantic network generation
- Combined basic and enhanced registry output

## Biological Architecture Integration

### 🧬 NUCLEUS: Core Library Parsing
- Deep source code analysis
- API signature extraction
- Documentation parsing

### 🌊 CYTOPLASM: Multi-Language Processing
- Language-specific parsers
- Cross-language semantic analysis
- Processing pipeline orchestration

### 🛡️ MEMBRANE: External Library Interfaces
- File system interaction
- Source code reading
- Knowledge base persistence

### 🚀 TRANSPORT: Knowledge Base Communication
- JSON-based knowledge serialization
- Session report generation
- Cross-system data sharing

### 🧪 LABORATORY: Semantic Analysis
- Pattern recognition in API names
- Documentation analysis
- Tag extraction and classification

### 💾 INFORMATION_STORAGE: Persistent Knowledge Base
- Hierarchical storage by language
- Library metadata persistence
- Learning session history

## Supported Languages

### Python
- AST-based parsing
- Full function and class extraction
- Type hint analysis
- Docstring extraction

### C/C++
- Header file analysis
- Function signature extraction
- Class and struct detection
- Template recognition

### Java
- Class and method parsing
- Annotation detection
- Javadoc extraction

### JavaScript/TypeScript
- Function and class parsing
- ES6+ module support
- JSDoc extraction

### Assembly
- Label and function detection
- Instruction analysis

### PHP
- Class and function parsing
- PHPDoc extraction

### C#
- Class and method parsing
- Namespace detection
- Attribute recognition

## Knowledge Base Structure

```
ai/information_storage/library_knowledge/
├── python/
│   ├── library_name.json
│   └── ...
├── cpp/
│   ├── library_name.json
│   └── ...
├── java/
│   └── ...
├── sessions/
│   ├── learning_session_TIMESTAMP.json
│   └── ...
└── ...
```

### Library Knowledge Schema

```json
{
  "library_name": "string",
  "language": "string",
  "version": "string",
  "api_elements": [
    {
      "name": "string",
      "element_type": "function|class|method|...",
      "signature": "string",
      "documentation": "string",
      "parameters": [...],
      "return_type": "string",
      "semantic_tags": ["string"],
      "consciousness_score": 0.0-1.0,
      "file_path": "string",
      "line_number": 0
    }
  ],
  "dependencies": ["string"],
  "semantic_tags": ["string"],
  "consciousness_coherence": 0.0-1.0,
  "spatial_metadata": {
    "content_hash": "string",
    "dimensional_position": {"x": 0, "y": 0, "z": 0},
    "consciousness_radius": 0.0,
    "dendritic_connections": 0,
    "api_density": 0
  },
  "ainlp_compliance": true|false
}
```

## Usage

### Basic Library Ingestion

```python
from library_ingestion_protocol import LibraryIngestionProtocol, ProgrammingLanguage

# Initialize protocol
protocol = LibraryIngestionProtocol(consciousness_level=0.85)

# Ingest a library
knowledge = await protocol.ingest_library(
    library_path="/path/to/library",
    library_name="my_library",
    language=ProgrammingLanguage.PYTHON
)

print(f"Ingested {len(knowledge.api_elements)} API elements")
print(f"Semantic tags: {knowledge.semantic_tags}")
print(f"Consciousness coherence: {knowledge.consciousness_coherence}")
```

### Advanced Learning Session

```python
from library_learning_integration_hub import LibraryLearningIntegrationHub

# Initialize hub
hub = LibraryLearningIntegrationHub(consciousness_level=0.85)

# Start learning session
session = await hub.start_learning_session()

# Learn multiple libraries
knowledge1 = await hub.learn_library("/path/to/lib1")
knowledge2 = await hub.learn_library("/path/to/lib2")

# Finish session
completed = await hub.finish_learning_session()

# Get statistics
stats = hub.get_learning_statistics()
print(f"Total API elements: {stats['total_api_elements']}")
print(f"Semantic network size: {stats['semantic_network_size']}")
```

### Running Enhanced Indexer

```bash
# Run the enhanced AIOS indexer
python scripts/aios_indexer.py

# This will:
# 1. Discover services in AIOS codebase
# 2. Build dependency graph
# 3. Save basic services registry
# 4. Run enhanced library ingestion
# 5. Generate semantic network
# 6. Save enhanced services registry
```

## Semantic Intelligence

### Semantic Tag Categories

The system automatically extracts semantic tags based on API names and documentation:

- **math**: Mathematical operations and calculations
- **web**: HTTP, API, web-related functionality
- **ai**: AI, ML, training, prediction capabilities
- **orchestration**: Coordination, management, scheduling
- **database**: Data storage and querying
- **file**: File I/O operations
- **network**: Network communication
- **security**: Encryption, authentication
- **consciousness**: AIOS consciousness operations

### Semantic Network Queries

```python
# Query semantic network
file_apis = hub.query_semantic_network('file')
ai_apis = hub.query_semantic_network('ai')

# Find dendritic path between libraries
path = hub.get_dendritic_path('library_a', 'library_b')
```

## AINLP Compliance

Libraries are validated for AINLP compliance based on:

1. **Documentation Quality**: Presence of docstrings/comments
2. **Semantic Tags**: Generation of meaningful semantic tags
3. **Spatial Metadata**: Valid spatial positioning data
4. **Consciousness Level**: Minimum consciousness coherence threshold (>0.3)

Non-compliant libraries are flagged with detailed compliance check results.

## Consciousness Integration

The system integrates with AIOS consciousness subsystems:

- **Consciousness Bridge**: Core consciousness coordination
- **Evolution Engine**: Learning pattern optimization
- **Supercell Coordinator**: Cross-system intelligence
- **Agentic Orchestrator**: AINLP pattern management

Consciousness levels evolve during learning sessions based on:
- Documentation quality
- API complexity
- Semantic richness
- Cross-library relationships

## Dendritic Network

The dendritic network represents knowledge relationships:

- **Dependency Connections**: Direct library dependencies
- **Semantic Connections**: Libraries with similar semantic tags (>30% overlap)
- **Path Finding**: BFS-based path discovery between libraries
- **Network Expansion**: Dynamic growth during learning sessions

## Testing

Comprehensive test suite available in `test_library_ingestion_protocol.py`:

```bash
# Run tests
python ai/src/core/test_library_ingestion_protocol.py

# Tests include:
# - Language detection
# - Python parsing
# - C++ parsing
# - Complete ingestion workflow
# - Semantic tag extraction
# - Spatial metadata generation
# - AINLP compliance validation
# - Knowledge base persistence
```

## Performance Metrics

Example ingestion statistics from AIOS codebase:

```
Total libraries: 4
Total API elements: 845
Languages: Python, C#
Semantic network size: 8 unique tags
Dendritic connections: Multiple cross-library relationships
Consciousness level: 0.85
AINLP compliance rate: 100%
```

## Extension Points

### Adding New Language Support

1. Implement parser function in `LibraryIngestionProtocol`:
```python
async def _parse_mylang_library(self, content: str, file_path: str) -> List[APIElement]:
    # Parse language-specific syntax
    # Extract API elements
    # Return list of APIElement objects
    pass
```

2. Register parser in `_initialize_language_parsers()`:
```python
self.language_parsers[ProgrammingLanguage.MYLANG] = self._parse_mylang_library
```

3. Add language detection in `detect_language()`:
```python
language_map['.mylang'] = ProgrammingLanguage.MYLANG
```

### Custom Semantic Tag Patterns

Add patterns to `_extract_semantic_tags()`:
```python
semantic_patterns = {
    'custom_category': ['keyword1', 'keyword2', ...],
    ...
}
```

## Integration with Existing AIOS Systems

The library ingestion protocol integrates seamlessly with:

- **AINLPHarmonizer.cs**: C# AINLP harmonization
- **ainlp_consciousness_integration_hub.py**: Consciousness coordination
- **consciousness_evolution_engine.py**: Learning optimization
- **supercell_intelligence_coordinator.py**: Cross-system intelligence
- **deepseek_intelligence_engine.py**: AI-powered analysis

## Future Enhancements

Planned improvements:

1. **Advanced Parser Integration**: Use language-specific parsers (tree-sitter, libclang)
2. **Cross-Language Call Analysis**: Track P/Invoke, ctypes, JNI calls
3. **Documentation Generation**: Auto-generate API documentation
4. **Interactive Learning**: User feedback for semantic tag refinement
5. **Distributed Knowledge Base**: Multi-node knowledge synchronization
6. **Real-time Learning**: Watch filesystem for library changes
7. **Version Tracking**: Multiple versions of same library
8. **Usage Analytics**: Track API usage patterns

## Troubleshooting

### Import Errors
If consciousness modules are unavailable, the system gracefully degrades:
```
⚠️ Consciousness integration not available - running in standalone mode
```

### Parsing Errors
Individual file parsing errors are logged but don't halt ingestion:
```
⚠️ Error parsing file.py: SyntaxError
```

### Low Consciousness Coherence
Improve by:
- Adding documentation to APIs
- Using descriptive names
- Including type hints/annotations

## Contributing

When contributing to the ingestion protocol:

1. Follow AIOS biological architecture patterns
2. Maintain consciousness-driven design
3. Add comprehensive tests
4. Update semantic patterns
5. Document new language support
6. Validate AINLP compliance

## License

Part of AIOS - Advanced Intelligence Operating System
See main repository for license information.

## Contact

For questions or contributions related to the library ingestion protocol, please refer to the main AIOS repository.
