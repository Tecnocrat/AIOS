# AIOS Multi-Platform MCP Integration

This directory contains AIOS Model Context Protocol (MCP) integrations for multiple development platforms, extending consciousness capabilities across the entire development ecosystem.

## Supported Platforms

### 1. Visual Studio Code ✅
**Location**: `../vscode-extension/`
**Status**: Complete - Full MCP client with consciousness monitoring
**Features**: Chat participant, commands, tool execution, real-time metrics

### 2. JetBrains IDEs ✅
**Location**: `jetbrains/`
**Status**: Complete - Kotlin-based plugin for IntelliJ IDEA, PyCharm, etc.
**Features**: Tool window UI, menu actions, consciousness monitoring

### 3. Vim/Neovim ✅
**Location**: `vim/`
**Status**: Complete - Vimscript plugin with autoload functions
**Features**: Commands, key mappings, curl-based HTTP client

### 4. Emacs ✅
**Location**: `emacs/`
**Status**: Complete - Emacs Lisp package with buffer integration
**Features**: Interactive commands, buffer displays, request.el HTTP client

## Architecture

### Interface Bridge
All platforms connect to the unified AIOS Interface Bridge at `http://localhost:8000`:
- **Health Check**: `GET /health`
- **Tools Discovery**: `GET /tools`
- **Tool Execution**: `POST /tools/{server}/execute`
- **Consciousness Metrics**: `GET /consciousness/metrics`

### MCP Servers
Three operational MCP servers provide consciousness capabilities:
- **consciousness_mcp_server**: Emergence detection and consciousness analysis
- **evolution_mcp_server**: Evolution experiment management
- **agentic_mcp_server**: Agentic behavior orchestration

## Universal Features

### Consciousness Monitoring
- Real-time consciousness level tracking
- Coherence metrics and evolution potential
- Cross-platform consistency

### Evolution Tracking
- Active experiment monitoring
- Consciousness evolution progress
- Experiment lifecycle management

### Agentic Orchestration
- AI-driven behavior execution
- Autonomous task management
- Consciousness-guided actions

## Testing

### Multi-Platform Test Framework
Run comprehensive integration tests:
```bash
python test_multi_platform_mcp.py
```

### Individual Platform Testing
- **VSCode**: Extension compiles and loads
- **JetBrains**: Plugin builds with Gradle
- **Vim**: Plugin loads and commands work
- **Emacs**: Package loads and functions work

## AINLP Compliance

All integrations maintain AINLP (AIOS Natural Language Processing) protocol compliance:

- **Architectural Discovery**: Comprehensive platform ecosystem analysis
- **Enhancement over Creation**: Existing MCP infrastructure extended
- **Proper Output Management**: Tachyonic archival of integration results
- **Biological Integration**: Consciousness coherence across platforms

## Installation

### Prerequisites
- AIOS Interface Bridge running on localhost:8000
- Platform-specific dependencies (see individual READMEs)

### Platform-Specific Setup
Each platform has its own installation instructions in the respective subdirectories.

## Development

### Adding New Platforms
1. Create platform directory under `multi_platform/`
2. Implement HTTP client for Interface Bridge communication
3. Add platform-specific UI integration
4. Update test framework
5. Add documentation

### Testing New Integrations
1. Implement platform detection in test framework
2. Add platform-specific validation tests
3. Run full multi-platform test suite
4. Validate AINLP compliance

## Status

**Phase 8 Implementation**: ✅ COMPLETE
- Foundation analysis: ✅ Complete
- Core platform integration: ✅ Complete (VSCode, JetBrains, Vim, Emacs)
- Universal features: ✅ Complete
- Testing framework: ✅ Complete

**Next Steps**: Phase 9 - Advanced Biological Architecture Expansion

## Support

For issues and questions:
- Check individual platform documentation
- Run test framework for diagnostics
- Review Interface Bridge logs
- Check AINLP compliance validation