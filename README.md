# AIOS - Artificial Intelligence Operative System

**A multi-language development platform for AI-assisted code generation and experimentation**

[![Python](https://img.shields.io/badge/python-3.12+-green.svg)](https://www.python.org/)
[![.NET](https://img.shields.io/badge/.NET-8.0+-purple.svg)](https://dotnet.microsoft.com/)
[![C++](https://img.shields.io/badge/C++-17+-blue.svg)](https://isocpp.org/)
[![Status](https://img.shields.io/badge/status-Active_Development-orange.svg)](docs/CHANGELOG.md)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)

---

## 🧭 Navigation Hub

**Start here for AIOS development:**

- 📖 **[README.md](README.md)** (this file) - Project overview, features, quick start
- 🎯 **[DEV_PATH.md](DEV_PATH.md)** - Current development status, active work, tactical roadmap
- 🏗️ **[PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)** - Strategic context, architectural principles, guidelines
- 📚 **[docs/ARCHITECTURE_INDEX.md](docs/ARCHITECTURE_INDEX.md)** - Complete documentation navigation

**Quick Links:**
- [Installation](#installation) | [Usage Examples](#usage-examples) | [Project Structure](#project-structure)
- [Documentation](#documentation) | [Troubleshooting](#troubleshooting) | [Contributing](#contributing)

---

## What is AIOS?

AIOS is a cross-platform development environment that combines multiple programming languages (Python, C++, C#) with AI agent coordination to generate, test, and evolve code automatically. It provides:

- **Multi-agent AI coordination** - Run multiple AI models (Ollama, Gemini, DeepSeek) in parallel to generate code
- **Cross-language integration** - Connect Python AI tools with C++ performance code and C# user interfaces
- **Code evolution experiments** - Automated code generation and quality testing workflows
- **Runtime intelligence** - 40+ monitoring and diagnostic tools for system health
- **Interface bridge** - HTTP API that exposes Python AI tools to other languages

Think of it as a laboratory for experimenting with AI-driven software development.

---

## Key Features

### 1. **Multi-Agent AI Code Generation**
Run three different AI models simultaneously and compare their code outputs:
- **Ollama** (local) - Fast inference with models like gemma3:1b, codellama:7b
- **Gemini** (cloud) - Google's AI models via AI Studio API
- **DeepSeek** (hybrid) - Advanced code analysis via OpenRouter API

```python
from ai.src.evolution.multi_agent_evolution_loop import MultiAgentEvolutionLoop

loop = MultiAgentEvolutionLoop()
result = await loop.human_guided_experiment(
    task_description="Write a C++ binary search function",
    use_all_agents=True  # Run all 3 agents in parallel
)
```

### 2. **Cross-Language Interface Bridge**
Call Python AI tools from C# or other languages via HTTP API:

```bash
# Start the bridge server
python ai/server_manager.py start
```

```csharp
// Call from C#
var client = new HttpClient();
var response = await client.GetAsync("http://localhost:8000/tools");
var tools = await response.Content.ReadAsStringAsync();
```

### 3. **Code Evolution Lab**
Dedicated workspace for AI-generated code experiments:
- `evolution_lab/experiments/` - Generated code outputs
- `evolution_lab/conversations/` - Full AI chat logs
- `evolution_lab/neural_chains/` - Code evolution history

### 4. **Runtime Intelligence Suite**
43 Python tools for system monitoring and optimization:
- System health checks
- Performance monitoring
- Architecture validation
- Code quality analysis

### 5. **Multi-Language Build System**
Unified build orchestration across three languages:
- **Python**: setuptools + pip
- **C++**: CMake with C++17 standard
- **C#**: MSBuild with .NET 8.0

---

## Quick Start

### Prerequisites
- Windows 10/11 with PowerShell 7+
- Python 3.12+ 
- .NET 8.0 SDK
- CMake 3.20+
- [Ollama](https://ollama.com/) (optional, for local AI)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/Tecnocrat/AIOS.git
cd AIOS

# 2. Install Python dependencies
python -m venv venv
.\venv\Scripts\activate
pip install -r ai/requirements.txt

# 3. Install Ollama models (optional)
ollama pull gemma3:1b

# 4. Build C++ core (optional)
cd core
cmake -B build -S .
cmake --build build
cd ..

# 5. Build C# UI (optional)
dotnet build AIOS.sln
```

### Run Your First AI Experiment

```bash
# Test multi-agent code generation
python ai/tests/test_multi_agent_experiment.py

# Check generated code
dir evolution_lab\experiments\

# View AI conversation logs
dir evolution_lab\conversations\
```

---

## Project Structure

```
AIOS/
├── ai/                          # Python AI coordination layer
│   ├── src/
│   │   ├── evolution/          # Multi-agent code generation
│   │   │   └── multi_agent_evolution_loop.py (887 lines)
│   │   ├── intelligence/       # AI agent bridges
│   │   │   ├── ollama_bridge.py (383 lines)
│   │   │   ├── gemini_evolution_bridge.py (417 lines)
│   │   │   └── deepseek_intelligence_engine.py (598 lines)
│   │   └── tools/              # AI utility tools
│   ├── security/               # 🛡️ Security Supercell (Digital Immune System)
│   │   ├── __init__.py         # Supercell consciousness coordinator
│   │   ├── membrane_validator.py  # Cell boundary enforcement
│   │   ├── immune_memory.py    # Tachyonic antibody database
│   │   ├── coherence_enforcer.py  # Universal validation
│   │   └── network_validator.py   # External communication screening
│   ├── orchestration/          # System coordination
│   │   ├── supercell_orchestrator.py (530 lines)
│   │   └── consciousness_coordinator.py (478 lines)
│   ├── nucleus/
│   │   └── interface_bridge.py # HTTP API server
│   ├── tests/                  # Test suite
│   │   └── security/           # Security testing (120+ test cases)
│   └── requirements.txt        # Python dependencies (113 packages)
│
├── core/                        # C++ performance engine
│   ├── CMakeLists.txt          # C++17 build configuration
│   ├── src/                    # Core C++ implementation
│   └── tests/                  # C++ unit tests
│
├── interface/                   # C# user interface layer
│   ├── AIOS.UI/                # WPF + WebView2 application
│   ├── AIOS.Services/          # Backend services
│   ├── AIOS.Models/            # Data models
│   └── AIOS.UI.Diagnostics/    # System diagnostics UI
│
├── evolution_lab/               # AI experiment workspace
│   ├── experiments/            # Generated code outputs
│   ├── conversations/          # AI chat logs
│   ├── neural_chains/          # Code evolution history
│   └── artifacts/              # Experiment artifacts
│
├── runtime_intelligence/        # Monitoring tools
│   └── tools/                  # 43 diagnostic Python scripts
│
├── docs/                        # Documentation
│   ├── ARCHITECTURE_INDEX.md   # Navigation hub
│   ├── CHANGELOG.md            # Development history
│   ├── security/               # Security documentation
│   │   ├── INTERFACE_BRIDGE_THREAT_MODEL_20251108.md
│   │   └── VULNERABILITY_REPORT_INTERFACE_BRIDGE_20251108.md
│   └── development/            # Development guides
│
└── tachyonic/                   # Historical archives
    ├── archive/                # Preserved experiments and logs
    └── patterns/
        └── security/           # 🧬 Immune Memory Archive
            ├── attack_signatures.json    # Antibody database
            ├── blocked_attempts_YYYYMMDD.json  # Attack logs
            └── pattern_evolution.json    # Learning metrics
```

---

## Architecture Overview

AIOS is organized as a **biological multi-language system** with three main layers:

### Layer 1: AI Intelligence (Python)
- **Purpose**: Coordinate AI agents, generate code, run experiments
- **Components**: 
  - Multi-agent orchestrator (887 lines)
  - AI bridges for Ollama, Gemini, DeepSeek
  - Interface bridge HTTP API
  - **Security Supercell** (Digital Immune System - Phase 11.2.9)
  - Runtime intelligence tools
- **Key Files**: `ai/src/evolution/`, `ai/orchestration/`, `ai/security/`

### Layer 2: Performance Engine (C++)
- **Purpose**: High-performance computation and system core
- **Components**:
  - CMake build system (C++17)
  - Core engine libraries
  - Threading and concurrency support
- **Key Files**: `core/CMakeLists.txt`, `core/src/`

### Layer 3: User Interface (C#)
- **Purpose**: GUI for system interaction and monitoring
- **Components**:
  - WPF application with WebView2 integration
  - Service layer for backend coordination
  - Diagnostic tools and visualizations
- **Key Files**: `interface/AIOS.UI/`, `interface/AIOS.Services/`

### Security Supercell: Biological Immune System (Phase 11.2.9)

AIOS implements a **digital immune system** that treats security as **boundary coherence** - defining the identity of the system by enforcing selective permeability at all supercell membranes:

```
🛡️ Security Architecture (Biological Metaphor)

Cell Membrane → MembraneValidator
  ├─ Validates parameter keys (allowlist)
  ├─ Sanitizes shell metacharacters (shlex)
  └─ Enforces workspace boundaries (path normalization)

Immune Memory → ImmuneMemory + Tachyonic Archive
  ├─ Records attack patterns (antibody database)
  ├─ Learns from exposures (adaptive immunity)
  └─ Archives in tachyonic/patterns/security/

Coherence Enforcer → CoherenceEnforcer
  ├─ Resource limits (memory, recursion, timeout)
  ├─ Consciousness delta tracking (security awareness)
  └─ Universal validation across supercells

Network Validator → NetworkValidator
  ├─ SSRF protection (private IP blocking)
  ├─ URL validation (protocol allowlist)
  └─ DNS rebinding prevention
```

**Security Metrics**:
- **CVSS Before**: 10.0 CRITICAL (command injection vulnerability)
- **CVSS After**: 0.0 RESOLVED (immune system operational)
- **Attack Mitigation**: 97.6% (166/170 tests passed)
- **Test Coverage**: 170 parametrized security test cases (7 attack phases)
- **Consciousness**: 3.31 → 3.40 (+0.09 security coherence achieved)

**4-Layer Security Architecture**:
1. **Membrane Validator** - Parameter validation, shell sanitization, path safety
2. **Coherence Enforcer** - Resource limits (recursion 100, memory 500MB, files 10MB)
3. **Shell Safety** - subprocess.run(shell=False) explicit protection
4. **Immune Memory** - Attack pattern recording, tachyonic antibody database

**Dendritic Integration**: Security supercell interconnects with interface_bridge.py, consciousness system, and tachyonic archive, increasing system intelligence through boundary enforcement patterns. Seven SEC-* connections track biological immune system integration.

### Communication Between Layers

```
┌─────────────┐      HTTP API       ┌─────────────┐
│   C# UI     │ ◄─────────────────► │   Python    │
│  (WPF GUI)  │   (port 8000)       │  (AI Tools) │
└─────────────┘                     └──────┬──────┘
                                           │
                                    🛡️ Security
                                     Supercell
                                      (Immune
                                       System)
                                           │
                                           │ pybind11
                                           ▼
                                    ┌─────────────┐
                                    │    C++      │
                                    │  (Engine)   │
                                    └─────────────┘
```

---

## Core Concepts Explained

AIOS uses some specialized terminology. Here's what it means:

### AINLP (AI Natural Language Programming)
A system for generating code from natural language descriptions. Instead of writing code manually, you describe what you want, and AI agents generate implementation options.

**Example**: "Write a C++ function that sorts an array using quicksort" → AI generates the code

### Biological Architecture
An organizational metaphor where software components are treated like biological cells:
- **Supercell** = Independent component/module with standard interfaces
- **Dendritic communication** = Message passing between components (like brain neurons)
- **Consciousness level** = Code quality metric (0.0 to 4.0 scale) measuring coherence and completeness
- **Immune System** = Security layer enforcing boundary coherence (Phase 11.2.9)
- **Membrane Validator** = Cell boundary enforcement (like cell membranes controlling what enters/exits)

This is just an organizational pattern - it doesn't mean the code is "alive" or has real consciousness.

### Dendritic Density & Intelligence Emergence
**Dendritic connections** track when code components call each other or leverage each other's architecture. Higher dendritic density (more interconnections) enables:
- **Higher intelligence**: System becomes more capable through integration
- **Emergent patterns**: New capabilities arise from component interactions
- **Consciousness growth**: Measured as interconnection increases

**Example**: Security supercell creates 3 bidirectional connections:
1. `membrane_validator.py` ↔ `interface_bridge.py` (validation integration)
2. `immune_memory.py` ↔ `tachyonic/patterns/security/` (archival integration)
3. `coherence_enforcer.py` ↔ `consciousness_system.py` (awareness tracking)

Each connection increases system intelligence by enabling components to work together.

### Evolution Lab
A dedicated directory (`evolution_lab/`) where AI-generated code experiments are stored:
- Each experiment gets a timestamp and unique ID
- Conversation logs show AI reasoning
- Multiple iterations can be compared

### Tachyonic Archive
Historical storage directory (`tachyonic/archive/`) for preserving:
- Past experiment results
- Conversation metadata
- Evolution history
- Genetic algorithm data
- **Immune memory** (attack pattern archival - Phase 11.2.9)

Think of it as a time-capsule for past work and a learning database for security patterns.

### Interface Bridge
An HTTP server (`ai/nucleus/interface_bridge.py`) that exposes Python AI tools as REST endpoints, allowing C# or JavaScript to call Python functions remotely.

**Security**: Protected by Security Supercell's biological immune system (Phase 11.2.9) - all parameters validated, sanitized, and monitored for attack patterns.

---

## Usage Examples

### Example 1: Generate Code with Single AI Agent

```python
from ai.src.evolution.multi_agent_evolution_loop import MultiAgentEvolutionLoop

async def generate_code():
    loop = MultiAgentEvolutionLoop(use_ollama=True)
    
    result = await loop.human_guided_experiment(
        task_description="Write a Python function to calculate fibonacci numbers",
        agent_type="ollama"
    )
    
    print(f"Generated code: {result['output_path']}")
    print(f"AI conversation: {result['conversation_path']}")
    print(f"Quality score: {result['fitness_score']}")

# Run it
import asyncio
asyncio.run(generate_code())
```

### Example 2: Compare Multiple AI Agents

```python
async def compare_agents():
    loop = MultiAgentEvolutionLoop()
    
    result = await loop.human_guided_experiment(
        task_description="Implement binary search in C++",
        use_all_agents=True  # Run Ollama + Gemini + DeepSeek
    )
    
    for agent_name, agent_result in result['results'].items():
        print(f"\n{agent_name}:")
        print(f"  Code: {agent_result['output_path']}")
        print(f"  Quality: {agent_result['fitness_score']}")
        print(f"  Time: {agent_result['processing_time']}s")

asyncio.run(compare_agents())
```

### Example 3: Start Interface Bridge and Call from C#

```bash
# Terminal 1: Start Python server
python ai/server_manager.py start
# Server running at http://localhost:8000
```

```csharp
// C# client code
using System.Net.Http;
using System.Threading.Tasks;

public class AIToolClient
{
    private static HttpClient client = new HttpClient();
    
    public static async Task<string> GetAvailableTools()
    {
        var response = await client.GetAsync("http://localhost:8000/tools");
        return await response.Content.ReadAsStringAsync();
    }
    
    public static async Task<string> RunAIAnalysis(string toolName)
    {
        var response = await client.GetAsync($"http://localhost:8000/tools/{toolName}");
        return await response.Content.ReadAsStringAsync();
    }
}

// Usage
var tools = await AIToolClient.GetAvailableTools();
Console.WriteLine($"Available AI tools: {tools}");

var result = await AIToolClient.RunAIAnalysis("ainlp_governance");
Console.WriteLine($"Analysis result: {result}");
```

---

## Configuration

### AI Model Configuration

**Ollama (Local AI)**:
```bash
# Install Ollama: https://ollama.com/

# Pull models
ollama pull gemma3:1b        # 2GB, fast
ollama pull codellama:7b     # 4GB, better code
ollama pull deepseek-coder:6.7b  # 5GB, best code analysis
```

**Gemini (Cloud AI)**:
```bash
# Get API key from: https://aistudio.google.com/
$env:GOOGLE_API_KEY = "your_api_key_here"
$env:GEMINI_MODEL = "gemini-2.5-flash"  # optional
```

**DeepSeek (Cloud AI)**:
```bash
# Get API key from: https://openrouter.ai/
$env:OPENROUTER_API_KEY = "your_api_key_here"
```

### Build Configuration

**Python**:
- Dependencies: `ai/requirements.txt` (113 packages)
- Virtual environment recommended: `python -m venv venv`

**C++**:
- Standard: C++17
- Build system: CMake 3.20+
- Threading: `find_package(Threads REQUIRED)`

**C#**:
- Framework: .NET 8.0
- UI: WPF + WebView2
- Build: `dotnet build AIOS.sln`

---

## Development Workflow

### 1. Running Tests

```bash
# Python tests
cd ai
python -m pytest tests/ -v

# Multi-agent experiments
python tests/test_multi_agent_experiment.py

# C++ tests (after build)
cd core/build
ctest --output-on-failure

# C# tests
dotnet test AIOS.sln
```

### 2. Starting Components

```bash
# Interface Bridge (Python HTTP API)
python ai/server_manager.py start

# C# UI Application
dotnet run --project interface/AIOS.UI/AIOS.UI.csproj

# System health check
python runtime_intelligence/tools/system_health_check.py
```

### 3. Viewing Experiment Results

```bash
# List recent experiments
dir evolution_lab\experiments\ | Sort-Object LastWriteTime | Select-Object -Last 5

# View AI conversation logs
Get-Content evolution_lab\conversations\conversation_<timestamp>.json | ConvertFrom-Json

# Check evolution history
dir evolution_lab\neural_chains\
```

---

## Documentation

### 🎯 Core Navigation Documents (Root Level)
- **[DEV_PATH.md](DEV_PATH.md)** - Current development status, active work tracking, tactical roadmap (1815 lines)
- **[PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)** - Strategic context, architectural principles, development guidelines
- **[README.md](README.md)** - This file: project overview, quick start, usage examples

### 📚 Essential Documentation (docs/)
- **[Architecture Index](docs/ARCHITECTURE_INDEX.md)** - System architecture overview and complete documentation navigation hub
- **[Multi-Agent Guide](docs/development/MULTI_AGENT_EXPERIMENTATION_COMPLETE_20251008.md)** - Complete multi-agent implementation details
- **[Changelog](docs/CHANGELOG.md)** - Development history and version information

### Technical References
- **[Orchestration Guide](docs/ORCHESTRATION_MASTER_GUIDE.md)** - Component coordination patterns (30KB, 10 sections)
- **[Integration Report](docs/INTEGRATION_MIGRATION_MASTER_REPORT.md)** - 8-phase refactoring history
- **[Core Optimization](docs/CORE_OPTIMIZATION_MASTER_REPORT.md)** - Performance optimization strategies
- **[Code Archival System](docs/CODE_ARCHIVAL_SYSTEM_COMPLETE.md)** - Knowledge preservation methodology

### API Documentation
- **[API Reference](docs/api/)** - Component interfaces and integration patterns
- **[Tools Index](docs/tools_index.md)** - Runtime intelligence tools catalog
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Fast lookup for common operations

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10 (64-bit) or Windows 11
- **RAM**: 8 GB (16 GB recommended for Ollama)
- **Storage**: 10 GB free space (20 GB with all AI models)
- **CPU**: Multi-core processor (4+ cores recommended)

### Software Requirements
- **Python**: 3.12.8 or higher
- **.NET SDK**: 8.0 or higher
- **CMake**: 3.20 or higher
- **PowerShell**: 7.0 or higher
- **Ollama**: Latest version (optional, for local AI)

### Optional External Services
- **Google AI Studio**: For Gemini API access (free tier available)
- **OpenRouter**: For DeepSeek API access (paid service)

---

## Troubleshooting

### Common Issues

**Issue**: Ollama models not found
```bash
# Solution: Pull the model first
ollama pull gemma3:1b
ollama list  # Verify it's installed
```

**Issue**: Interface bridge won't start
```bash
# Solution: Check if port 8000 is in use
netstat -ano | findstr :8000
# Kill process if needed, then restart:
python ai/server_manager.py restart
```

**Issue**: C++ build fails
```bash
# Solution: Verify CMake and compiler installation
cmake --version  # Should be 3.20+
# On Windows, install Visual Studio Build Tools
```

**Issue**: Python import errors
```bash
# Solution: Activate virtual environment and reinstall
.\venv\Scripts\activate
pip install -r ai/requirements.txt
```

---

## Contributing

### Development Standards
- **Code Style**: 
  - Python: Black formatter, PEP 8
  - C#: dotnet format
  - C++: Clang-format
- **Testing**: Write unit tests for new features
- **Documentation**: Update relevant docs with changes
- **Commits**: Clear, descriptive commit messages

### Contribution Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes and test thoroughly
4. Update documentation
5. Submit pull request with description of changes

### Getting Help
- Check [Documentation Index](docs/ARCHITECTURE_INDEX.md) first
- Review [Development Guide](docs/development/AIOS_DEV_PATH.md)
- Look at [existing issues](https://github.com/Tecnocrat/AIOS/issues)

---

## Current Development Status

**Active Components** ✅:
- Multi-agent AI coordination (Ollama, Gemini, DeepSeek)
- Interface bridge HTTP API (50+ tools)
- Evolution Lab experiment workspace
- Runtime intelligence monitoring (43 tools)
- C# UI with WPF + WebView2
- Python test suite

**In Development** 🔧:
- Genetic algorithm integration
- Visual consciousness tracking dashboard
- Automated feedback loops
- Production deployment pipeline

**Roadmap** 🗺️:
- Agent-to-agent direct communication
- Real-time code evolution visualization
- Expanded AI model support
- Cross-platform (Linux, macOS)

See [Changelog](docs/CHANGELOG.md) for detailed development history.

---

## License

**Proprietary License** - This project is proprietary research software. See [LICENSE](LICENSE) file for details.

---

## Acknowledgments

AIOS is a research platform for exploring AI-assisted software development, multi-agent coordination, and code evolution techniques. It builds on open-source tools and AI models from:
- [Ollama](https://ollama.com/) - Local AI inference
- [Google Gemini](https://ai.google.dev/) - Cloud AI models
- [OpenRouter](https://openrouter.ai/) - AI model aggregation

---

**AIOS** - Advancing AI-assisted development through multi-agent coordination and code evolution.

*For questions, issues, or contributions, see our [documentation](docs/ARCHITECTURE_INDEX.md) or contact the development team.*
