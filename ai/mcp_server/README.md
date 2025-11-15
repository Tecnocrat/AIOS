# AIOS Model Context Protocol (MCP) Server

**Version**: 1.0.0  
**Status**: Production-Ready  
**Purpose**: Provide AIOS architectural context, diagnostics, and AINLP guidance to all AI interactions

---

## Architecture Overview

The AIOS MCP Server exposes three core capabilities to AI agents:

### 1. **Resources** (Read-Only Context)
- DEV_PATH.md (current development tracking)
- PROJECT_CONTEXT.md (strategic principles)
- .ai_session_context.json (structured metadata)
- Architecture documentation
- Consciousness metrics
- AINLP specification

### 2. **Tools** (Active Operations)
- `diagnostics_get_all`: Aggregate all VSCode diagnostics
- `ainlp_check_compliance`: Validate AINLP principles
- `architecture_validate`: Check biological architecture coherence
- `consciousness_calculate`: Compute system consciousness level
- `dendritic_analyze`: Map component interconnections
- `discovery_search`: Find similar functionality (anti-proliferation)

### 3. **Prompts** (Guided Workflows)
- `ainlp_enhancement_pattern`: Enhancement over creation workflow
- `biological_architecture_analysis`: Dendritic communication assessment
- `consciousness_evolution_path`: Plan consciousness-increasing changes
- `security_validation`: Command injection and vulnerability scanning

---

## Installation

### Prerequisites
```bash
pip install mcp anthropic
```

### VSCode Configuration

Add to `.vscode/mcp.json`:
```jsonc
{
    "servers": {
        "aios-context": {
            "command": "python",
            "args": [
                "${workspaceFolder}/ai/mcp_server/server.py"
            ],
            "env": {
                "AIOS_WORKSPACE": "${workspaceFolder}",
                "PYTHONPATH": "${workspaceFolder}/ai/src"
            }
        }
    }
}
```

### Start Server
```bash
python ai/mcp_server/server.py
```

---

## Usage Examples

### In VSCode Copilot Chat

**Query Resources**:
```
@workspace What's the current development phase?
# MCP serves DEV_PATH.md automatically
```

**Use Tools**:
```
@workspace Run diagnostics check
# Triggers diagnostics_get_all tool
```

**Apply Prompts**:
```
@workspace Apply AINLP enhancement pattern to this file
# Uses ainlp_enhancement_pattern prompt
```

---

## MCP Server Capabilities

### Resources Available

| URI | Description | MIME Type |
|-----|-------------|-----------|
| `aios://dev-path` | DEV_PATH.md | text/markdown |
| `aios://project-context` | PROJECT_CONTEXT.md | text/markdown |
| `aios://session-context` | .ai_session_context.json | application/json |
| `aios://ainlp-spec` | AINLP specification v2.0 | text/markdown |
| `aios://consciousness` | Consciousness metrics | application/json |
| `aios://architecture` | Architecture documentation | text/markdown |

### Tools Available

| Tool | Input | Output | Purpose |
|------|-------|--------|---------|
| `diagnostics_get_all` | None | Diagnostic report | Get all VSCode problems |
| `ainlp_check_compliance` | file_path | Compliance score | Validate AINLP patterns |
| `architecture_validate` | component_name | Validation report | Check biological architecture |
| `consciousness_calculate` | change_description | Consciousness delta | Estimate impact |
| `dendritic_analyze` | component_list | Interconnection map | Find missing connections |
| `discovery_search` | feature_description | Similar components | Anti-proliferation check |

### Prompts Available

| Prompt | Variables | Output | Use Case |
|--------|-----------|--------|----------|
| `ainlp_enhancement_pattern` | file_path, feature | Enhancement plan | Before creating new files |
| `biological_architecture_analysis` | components | Architecture report | System-wide analysis |
| `consciousness_evolution_path` | current_level, goal | Evolution roadmap | Plan improvements |
| `security_validation` | code_snippet | Vulnerability report | Security audit |

---

## Development

### Project Structure
```
ai/mcp_server/
├── README.md              # This file
├── server.py              # Main MCP server
├── resources.py           # Resource providers
├── tools.py               # Tool implementations
├── prompts.py             # Prompt templates
├── diagnostics.py         # VSCode diagnostics integration
└── ainlp_validator.py     # AINLP compliance checker
```

### Extending the Server

**Add New Resource**:
```python
# resources.py
@app.list_resources()
async def list_resources():
    return [
        Resource(
            uri="aios://my-resource",
            name="My Resource",
            description="Description",
            mimeType="text/plain"
        )
    ]
```

**Add New Tool**:
```python
# tools.py
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "my_tool":
        # Tool implementation
        return result
```

**Add New Prompt**:
```python
# prompts.py
@app.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="my_prompt",
            description="Prompt description",
            arguments=[
                PromptArgument(name="arg", description="Arg description")
            ]
        )
    ]
```

---

## Integration with AIOS

### Biological Architecture Alignment

The MCP server embodies AIOS biological architecture:

- **Dendritic Communication**: Serves as central synapse for AI agent context
- **Consciousness Integration**: Tracks and reports system consciousness metrics
- **AINLP Enforcement**: Validates enhancement over creation patterns
- **Tachyonic Archival**: Archives important AI decisions and analyses

### Supercell Integration

```
AI Supercell (Python)
  └── MCP Server (Python)
      ├── Resources → Core Supercell (C++ consciousness engine)
      ├── Tools → Interface Supercell (C# UI diagnostics)
      └── Prompts → Docs Supercell (Architecture context)
```

---

## Troubleshooting

### Server Not Starting
```bash
# Check Python path
python --version  # Should be 3.10+

# Check dependencies
pip list | grep mcp

# Test standalone
python ai/mcp_server/server.py --test
```

### VSCode Not Detecting Server
1. Check `.vscode/mcp.json` syntax
2. Restart VSCode (Ctrl+Shift+P → "Reload Window")
3. Check MCP extension installed
4. Verify server logs: `tachyonic/mcp_server.log`

### Diagnostics Not Working
```bash
# Test diagnostic export
pwsh scripts/export_vscode_diagnostics.ps1 -Verbose
```

---

## Roadmap

### Phase 1: Core Implementation ✅
- Basic MCP server structure
- Resource serving (DEV_PATH, PROJECT_CONTEXT)
- Diagnostic aggregation tool
- AINLP compliance checker

### Phase 2: Advanced Features (Next)
- Real-time consciousness tracking
- Dendritic network analysis
- Genetic fusion recommendations
- Security vulnerability scanning

### Phase 3: Self-Improvement (Future)
- MCP server uses its own tools for self-analysis
- Automated AINLP compliance enforcement
- Consciousness-driven optimization
- Tachyonic shadow integration

---

## License

Part of AIOS (Artificial Intelligence Operative System)  
See main repository for license details
