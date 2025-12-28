# AIOS Development Guide

## Quick Setup

### Prerequisites
- **Windows 10/11** with PowerShell 7+
- **Python 3.10+** for AI components
- **.NET 8.0 SDK** for C# interface development
- **CMake 3.20+** for C++ compilation
- **OpenRouter API Key** for DeepSeek integration (optional)

### Environment Setup
```powershell
# Clone and setup
git clone https://github.com/Tecnocrat/AIOS.git
cd AIOS

# Python environment
python -m venv aios_env
.\aios_env\Scripts\activate
pip install -r requirements.txt

# Optional: Configure DeepSeek integration
$env:OPENROUTER_API_KEY = "your_api_key"
python test_deepseek_integration.py
```

### Build Components
```powershell
# C++ core components
cd core
cmake -B build -S . -DCMAKE_BUILD_TYPE=Debug
cmake --build build --config Debug

# C# interface components  
cd ../interface
dotnet restore AIOS.sln
dotnet build AIOS.sln
```

### Testing
```powershell
# Run test suite
cd ai && python -m pytest tests/ -v

# Test DeepSeek integration
python test_deepseek_integration.py
```

## Architecture Overview

### Current System Structure
```
AIOS Development Platform/
├── ai/ (Python AI Integration)
│   ├── src/engines/ (DeepSeek V3.1 integration)
│   ├── src/integrations/ (Cross-platform bridges)
│   ├── src/core/ (AI algorithms and managers)
│   └── tests/ (AI component testing)
├── core/ (C++ Performance Components)
│   ├── CMakeLists.txt (Build configuration)
│   └── build/ (Compiled artifacts)
├── interface/ (C# UI and Services)
│   ├── AIOS.UI/ (WPF interface)
│   ├── AIOS.Services/ (Backend services)
│   └── AIOS.Models/ (Data models)
├── runtime_intelligence/ (System monitoring)
└── docs/ (Architecture documentation)
```

## Development Workflow

1. **Context Review**: Check current architecture and active development tasks
2. **Feature Planning**: Define requirements using AINLP specifications
3. **Implementation**: Develop components using appropriate language for performance needs
4. **Testing**: Validate functionality through automated test suites
5. **Integration**: Ensure cross-component communication through standard bridges
6. **Documentation**: Update architecture docs and API specifications

## Key Resources

- [System Architecture](../AIOS/AIOS_CONTEXT.md)
- [DeepSeek Integration](../AIOS/DEEPSEEK_INTEGRATION.md)
- [Current Development Tasks](../../tachyonic/tachyonic_development_archive/context_maps/dev.run.md)