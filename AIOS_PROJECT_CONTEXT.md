# AIOS Project Context & Setup Guide

## Project Overview
AIOS (Artificial Intelligence Operating System) is a revolutionary intelligent operative system designed to make current software paradigms obsolete. The system integrates multiple programming languages and technologies to create a unified, AI-driven computing environment.

## Architecture Overview

### Core Components
- **C++ Core Logic**: High-performance system kernel, memory management, and low-level operations
- **C# Visual Interface**: Modern UI framework, user interaction, and system visualization
- **Python AI Logic**: Advanced machine learning, natural language processing, and intelligent automation
- **Markdown Documentation**: Natural language context richness and human-readable specifications
- **JSON Configuration**: System settings, API definitions, and data interchange
- **XAML UI Definitions**: Declarative user interface layouts and styling

### System Philosophy
AIOS operates on the principle that traditional operating systems are collections of disconnected applications. Instead, AIOS provides:
- Unified AI-driven context awareness across all operations
- Seamless integration between human intent and system execution
- Intelligent resource management and predictive system behavior
- Natural language interface for complex system operations

## Development Environment Requirements

### Essential Tools
- **Visual Studio 2022** (C# development, XAML designer)
- **Visual Studio Code** (Python, JSON, Markdown, cross-language development)
- **CMake** (C++ build system)
- **Python 3.11+** (AI logic and scripting)
- **Git** (Version control)

### Language-Specific Requirements

#### C++ Core
- **Compiler**: MSVC 2022 or GCC 12+
- **Build System**: CMake 3.20+
- **Libraries**: 
  - Boost (system utilities)
  - OpenCV (computer vision)
  - TensorFlow C++ (ML inference)
  - nlohmann/json (JSON handling)

#### C# Interface
- **.NET 8.0+**
- **WPF** or **WinUI 3** (UI framework)
- **NuGet Packages**:
  - Microsoft.Extensions.DependencyInjection
  - Microsoft.Extensions.Logging
  - Newtonsoft.Json
  - System.Text.Json

#### Python AI Logic
- **Python 3.11+**
- **Virtual Environment**: conda or venv
- **Core Libraries**:
  - torch (PyTorch for deep learning)
  - transformers (Hugging Face models)
  - numpy, pandas (data processing)
  - fastapi (API services)
  - asyncio (async programming)

## Project Structure
```
AIOS/
├── core/                    # C++ core system
│   ├── src/
│   ├── include/
│   ├── CMakeLists.txt
│   └── tests/
├── interface/               # C# visual interface
│   ├── AIOS.UI/
│   ├── AIOS.Services/
│   ├── AIOS.Models/
│   └── AIOS.sln
├── ai/                      # Python AI logic
│   ├── src/
│   ├── models/
│   ├── requirements.txt
│   └── tests/
├── docs/                    # Markdown documentation
│   ├── architecture.md
│   ├── api-reference.md
│   └── user-guide.md
├── config/                  # JSON configuration
│   ├── system.json
│   ├── ai-models.json
│   └── ui-themes.json
├── resources/               # XAML and assets
│   ├── themes/
│   ├── icons/
│   └── layouts/
└── build/                   # Build outputs
    ├── debug/
    └── release/
```

## Development Workflow

### Initial Setup Commands
```bash
# Create project directory
mkdir AIOS && cd AIOS

# Initialize Git repository
git init

# Create virtual environment for Python
python -m venv ai/venv
ai/venv/Scripts/activate  # Windows
# source ai/venv/bin/activate  # Linux/Mac

# Install Python dependencies
pip install -r ai/requirements.txt

# Create C++ build directory
mkdir build && cd build
cmake ../core
cmake --build .

# Open C# solution in Visual Studio
# Open VSCode for multi-language development
```

### VSCode Extensions Required
- **C/C++** (Microsoft)
- **C#** (Microsoft)
- **Python** (Microsoft)
- **CMake Tools** (Microsoft)
- **JSON Tools** (Erik Lynd)
- **XAML** (Microsoft)
- **Markdown All in One** (Yu Zhang)
- **GitHub Copilot** (GitHub)

### Common Development Issues & Solutions

#### Environment Configuration
- **Problem**: Multiple Python interpreters causing conflicts
- **Solution**: Use conda environments or explicit venv activation
- **Command**: `python -m venv ai/venv && ai/venv/Scripts/activate`

#### Build System Issues
- **Problem**: C++ compilation errors with dependencies
- **Solution**: Use vcpkg for C++ package management
- **Command**: `vcpkg install boost opencv nlohmann-json`

#### Cross-Language Integration
- **Problem**: Interfacing between C++, C#, and Python
- **Solution**: Use C++/CLI for C#-C++ bridge, Python C API for C++-Python
- **Note**: JSON serves as universal data exchange format

## AI Integration Patterns

### Core AI Capabilities
- **Natural Language Understanding**: Process user intent into system commands
- **Predictive Resource Management**: Anticipate system needs and optimize accordingly
- **Context-Aware Automation**: Learn user patterns and automate repetitive tasks
- **Intelligent Error Recovery**: Diagnose and fix system issues autonomously

### Python AI Module Structure
```python
# ai/src/core/
├── nlp/                    # Natural language processing
├── prediction/             # System prediction models
├── automation/             # Task automation logic
├── learning/               # Continuous learning systems
└── integration/            # Language bridges
```

## Critical Development Notes

### Context Preservation
- **Challenge**: Maintaining development context across sessions
- **Solution**: Comprehensive markdown documentation with state tracking
- **Implementation**: Auto-generated project status reports

### Configuration Management
- **Challenge**: Complex multi-language build configurations
- **Solution**: Centralized JSON configuration with environment-specific overrides
- **Tool**: Custom configuration validator scripts

### Debugging Multi-Language Systems
- **Challenge**: Debugging across C++, C#, and Python boundaries
- **Solution**: Unified logging system with structured JSON output
- **Implementation**: Centralized log aggregation and analysis

## Next Steps for Clean Development Start

1. **Environment Validation**: Run system check script to verify all dependencies
2. **Project Scaffolding**: Generate base project structure with templates
3. **Build System Setup**: Configure CMake, MSBuild, and Python environments
4. **Integration Testing**: Verify cross-language communication works
5. **Documentation Generation**: Set up auto-documentation pipeline

## Success Metrics
- **Clean Build**: All components compile without warnings
- **Zero Configuration**: New developer can start with single command
- **Context Preservation**: Project state survives environment changes
- **Rapid Iteration**: Changes reflect immediately across all language boundaries

## AI Copilot Instructions
When working with AIOS:
1. Always consider multi-language implications of changes
2. Maintain consistent JSON schemas across components
3. Use markdown for human-readable specifications
4. Implement proper error handling at language boundaries
5. Follow the established project structure religiously
6. Test cross-language integration after any core changes

---

*This document serves as the master context for AIOS development. Update it whenever architectural decisions are made or development patterns change.*
