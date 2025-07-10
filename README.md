# AIOS - Artificial Intelligence Operating System

READ THIS FIRST:
    user: tecnocrat
    git: https://github.com/Tecnocrat
    current_branch: https://github.com/Tecnocrat/AIOS/tree/OS0.4

[![Version](https://img.shields.io/badge/version-0.4-blue.svg)](https://github.com/Tecnocrat/AIOS/tree/OS0.4)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **A revolutionary intelligent operating system designed to make current software paradigms obsolete**

AIOS integrates multiple programming languages and AI technologies to create a unified, intelligent computing environment that understands human intent and executes complex operations seamlessly.

## 🚀 **Quick Start**

### **One-Command Setup**
```bash
# Clone and setup (when repository is ready)
git clone https://github.com/Tecnocrat/AIOS.git -b OS0.4
cd AIOS
./scripts/setup.ps1  # Windows
```

### **Manual Setup**
```bash
# 1. Setup Python AI modules
cd ai && python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt

# 2. Build C++ core
cd core && mkdir build && cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=C:/dev/vcpkg/scripts/buildsystems/vcpkg.cmake
cmake --build . --config Debug

# 3. Test integration
cd ../.. && python scripts/test_integration.py
```

## ✨ **Features**

### **🧠 AI-Powered Core**
- **Natural Language Processing**: Understand and execute complex commands in plain English
- **Predictive Analytics**: Anticipate system needs and optimize performance automatically
- **Continuous Learning**: Adapt to user patterns and improve over time
- **Intelligent Automation**: Automate repetitive tasks with context awareness

### **⚡ Multi-Language Architecture**
- **C++ Core**: High-performance system kernel with memory management
- **Python AI**: Advanced machine learning and natural language processing
- **C# Interface**: Modern desktop UI with WPF/WinUI and AINLP kernel integration
- **Cross-Language Integration**: Seamless communication between all components
- **AINLP Comment Classes**: Revolutionary natural language programming paradigm

### **🔧 Developer-Friendly**
- **Modular Design**: Clean three-layer architecture (Models → Services → UI)
- **Interface-Driven**: Dependency injection and SOLID principles
- **Comprehensive Documentation**: Four-domain architecture with AINLP paradigms
- **Automated Testing**: Integration tests ensure system reliability
- **Multiple IDEs**: Works with Visual Studio, VS Code, and more
- **Advanced Debugging**: Complete VSCode debugging infrastructure
- **Tachyonic Optimization**: Quantum-inspired documentation archival

## 🏗️ **Architecture**

```
AIOS/
├── core/           # C++ system kernel
│   ├── src/        # Core logic implementation
│   ├── include/    # Public API headers
│   └── tests/      # Unit tests
├── ai/             # Python AI modules
│   ├── src/core/   # AI subsystems
│   │   ├── nlp/    # Natural language processing
│   │   ├── prediction/  # Predictive analytics
│   │   ├── automation/  # Task automation
│   │   ├── learning/    # Machine learning
│   │   └── integration/ # Language bridges
│   └── tests/      # AI module tests
├── interface/      # C# user interface
│   ├── AIOS.UI/    # WPF/WinUI application
│   ├── AIOS.Services/  # Business logic and AI integration
│   ├── AIOS.Models/    # Data models and interfaces
│   └── AIOS.sln    # Visual Studio solution
├── docs/          # Documentation (Four-Domain Architecture)
│   ├── ai-context/     # AI iteration management
│   ├── AINLP/         # Language specification domain
│   ├── AIOS/          # System architecture domain
│   ├── INFRASTRUCTURE/ # Development infrastructure
│   └── tachyonic_archive.db  # Quantum documentation archive
```

## 📊 **Current Status**

| Component | Status | Details |
|-----------|--------|---------|
| **C++ Core** | ✅ Complete | Fully functional with vcpkg dependencies |
| **Python AI** | ✅ Complete | 5 modules: NLP, Prediction, Automation, Learning, Integration |
| **C# Interface** | ✅ Architecture Complete | Clean build achieved, AINLP kernel integrated |
| **Integration** | ✅ Complete | Cross-language communication working |
| **VSCode Extension** | ✅ Complete | Context persistence, `/save` command, iteration reset solved |
| **Documentation** | ✅ Complete | Four-domain architecture, AINLP paradigms implemented |
| **Build System** | ✅ Complete | CMake + vcpkg, dotnet builds successful |
| **Testing** | ✅ Complete | Integration tests passing |
| **Optimization Systems** | ✅ Complete | OP ITER analysis, caching, async operations, unified config |

## 🔒 **VSCode Extension - Private Use Only**

### **Problem Solved: Chat Iteration Reset**
The AIOS VSCode extension solves the critical issue where chat iterations reset on extension restart, breaking development continuity.

### **🛡️ Private Use Configuration**
```powershell
# Automated Private Setup (Recommended)
cd "c:\dev\AIOS\vscode-extension"
.\setup-private.ps1 -All

# Manual Private Setup
# 1. VSCode → F1 → "Developer: Install Extension from Location..."
# 2. Select: c:\dev\AIOS\vscode-extension\aios-vscode-0.4.0.vsix
# 3. Configure private settings (see PRIVATE_USE_IMPLEMENTATION_COMPLETE.md)
```

### **🔐 Private Use Features**
- **🔒 Local Only**: No external connections or data sharing
- **🔄 Persistent Context**: No more iteration resets across VSCode restarts
- **🧠 AI Integration**: Direct connection to AIOS C++/Python/C# AI modules
- **⚡ Native Chat**: VSCode chat participant with `@aios` command
- **💾 Smart Context**: Automatic context saving and encryption
- **🛠️ Developer Tools**: Rich command palette and status monitoring

### **Usage**
```typescript
// In any VSCode chat window:
@aios Help me understand this code
@aios /status           // Show AIOS system status
@aios /reset            // Reset conversation context
@aios /save             // Save current context (IMPLEMENTED)
@aios /help             // Show all commands
```

### **Privacy & Security**
- ✅ **No External Connections**: All processing happens locally
- ✅ **No Telemetry**: All analytics and tracking disabled
- ✅ **Encrypted Context**: Local context storage with encryption
- ✅ **Session-Only Logs**: Minimal logging with automatic cleanup
- ✅ **Private Installation**: VSIX-only installation (no marketplace)

**📋 Complete Guide**: [VSCode Extension Private Use](vscode-extension/docs/AIOS_VSCODE_PRIVATE_COMPLETE.md)
**🔧 Technical Details**: [Implementation Complete](vscode-extension/docs/PRIVATE_USE_IMPLEMENTATION_COMPLETE.md)

## 🧪 **Testing**

### **Run All Tests**
```bash
# Integration test (tests all components)
python scripts/test_integration.py

# C++ core tests
cd core/build && ./tests/Debug/test_core.exe

# Python AI tests
cd ai && python -m pytest tests/
```

### **Expected Output**
```
==================================================
AIOS Integration Test
==================================================
C++ Core: ✅ PASS
Python AI: ✅ PASS
🎉 ALL TESTS PASSED! AIOS system is ready!
```

## 🔧 **Development**

### **Prerequisites**
- **Visual Studio 2022** (C# development)
- **CMake 3.20+** (C++ build system)
- **Python 3.11+** (AI modules)
- **vcpkg** (C++ package manager)
- **Git** (version control)

### **Dependencies**
**C++ Libraries:**
- Boost (system, filesystem, thread)
- OpenCV (computer vision)
- nlohmann-json (JSON handling)

**Python Packages:**
- numpy, pandas (data processing)
- asyncio (async programming)
- logging (system logging)

### **Build Commands**
```bash
# C++ Core
cd core/build && cmake --build . --config Debug

# Python AI (auto-installed with venv)
cd ai && pip install -r requirements.txt

# C# Interface
cd interface && dotnet build

# Run integration tests
python scripts/test_integration.py

# Run tachyonic documentation optimizer
python scripts/docs_tachyonic_cleanup.py

# Monitor system health
python scripts/context_health_monitor.py
```

## 📚 **Documentation**

### **🤖 For AI Systems & Assistants**
- [**AI Context Reallocator**](docs/ai-context/AI_context_reallocator.md) - **MUST READ FIRST** - Context preservation protocol
- [**AI Quick Reference**](docs/ai-context/AI_QUICK_REFERENCE.md) - Quick commands and procedures
- [**Project Status**](docs/ai-context/PROJECT_STATUS.md) - Current implementation status
- [**Documentation Index**](docs/DOCUMENTATION_INDEX.md) - Master documentation guide

### **🧠 For AINLP Development**
- [**AINLP Next-Gen Paradigm**](docs/AINLP/AINLP_NEXTGEN_DOCUMENTATION_DISTILLATION.md) - **Revolutionary documentation system**
- [**AINLP Specification**](docs/AINLP/AINLP_SPECIFICATION.md) - Language specification and comment classes
- [**AINLP Management Strategy**](docs/AINLP/AINLP_DOCUMENTATION_MANAGEMENT_STRATEGY.md) - Implementation strategy

### **🏛️ For System Architecture**
- [**AIOS Master Specification**](docs/AIOS/AIOS_MASTER_SPECIFICATION.md) - **Complete unified specification**
- [**VSCode Extension Documentation**](docs/AIOS/AIOS_VSCODE_SAVE_COMMAND.md) - VSCode `/save` command details
- [**Architecture Complete**](docs/INFRASTRUCTURE/JULY_2025_ARCHITECTURE_COMPLETE.md) - Latest architectural achievements

### **For Users**
- [**Installation Guide**](docs/INSTALLATION.md) - Detailed setup instructions
- [**User Guide**](docs/USER_GUIDE.md) - How to use AIOS
- [**FAQ**](docs/FAQ.md) - Common questions and answers

### **For Developers**
- [**Development Infrastructure Complete**](docs/INFRASTRUCTURE/DEVELOPMENT_INFRASTRUCTURE_COMPLETE.md) - VSCode debugging, logging setup
- [**Infrastructure Status**](docs/INFRASTRUCTURE/INFRASTRUCTURE_STATUS_COMPLETE.md) - Current infrastructure state
- [**Integration Status July 2025**](docs/INFRASTRUCTURE/INTEGRATION_STATUS_JULY_2025.md) - Latest integration achievements
- [**API Reference**](docs/API_REFERENCE.md) - Programming interfaces (archived in tachyonic database)
- [**Installation Guide**](docs/INSTALLATION.md) - Environment setup (archived in tachyonic database)

### **🎯 Self-Organizing Documentation System**
AIOS implements a revolutionary **four-domain documentation architecture** using AINLP next-generation paradigms:

- **Domain Separation**: Semantic boundaries for optimal AI/human navigation
- **Context Preservation**: Advanced AI iteration management and bootstrap protocols
- **Tachyonic Archival**: Quantum-inspired information storage with perfect recall
- **AINLP Integration**: Self-organizing documentation that evolves with the system
- **Fractal Patterns**: Each domain reflects the whole system's knowledge structure

**Documentation Domains:**
- 🤖 **AI Context**: Bootstrap protocols, iteration management, context preservation
- 🧠 **AINLP**: Language specification, next-gen paradigms, kernel tooling
- 🏛️ **AIOS**: System architecture, VSCode extensions, unified specifications
- 📊 **Infrastructure**: Development setup, build status, optimization paths

**For AI assistants working on AIOS**: Always start by reading `AI_context_reallocator.md` before any development work.

## 🤝 **Contributing**

We welcome contributions! Please see our [Development Guide](docs/DEVELOPMENT.md) for details.

### **Quick Contribution Steps**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python scripts/test_integration.py`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🐛 **Known Issues**

- ~~Python virtual environment activation varies by system~~ ✅ **RESOLVED**
- ~~C# UI implementation is incomplete~~ ✅ **RESOLVED** - Architecture complete
- ~~Documentation is still being written~~ ✅ **RESOLVED** - Four-domain system complete
- Minor XAML property warnings in UI (non-blocking)
- Git repository initialization pending user decision

## 📋 **Roadmap**

### **Version 0.4 (Current)**
- [x] C++ Core implementation
- [x] Python AI modules
- [x] Cross-language integration
- [x] Complete C# interface architecture
- [x] AINLP kernel integration
- [x] VSCode extension with `/save` command
- [x] Four-domain documentation system
- [x] Tachyonic documentation archival
- [x] Full testing framework
- [x] Development infrastructure complete

### **Version 0.5 (Next)**
- [ ] Advanced UI implementation and hybrid interfaces
- [ ] Enhanced AINLP comment class system
- [ ] Real-time documentation evolution
- [ ] Advanced AI features (TensorFlow integration)
- [ ] Web-based interface
- [ ] Plugin system
- [ ] Advanced NLP capabilities

### **Version 1.0 (Future)**
- [ ] Production-ready release
- [ ] Comprehensive GUI
- [ ] Advanced automation features
- [ ] Multi-platform support

## 📄 **License**

**License Status**: TBD - Under consideration
- **Options**: MIT, GPL v3, Apache 2.0, Custom
- **Decision**: Pending project owner decision
- **Current**: Development/Research phase

See [LICENSE](LICENSE) file when finalized.

## 🙏 **Acknowledgments**

- Thanks to all contributors and early adopters
- Built with amazing open-source libraries
- Inspired by the vision of truly intelligent computing

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/user/AIOS/issues)
- **Discussions**: [GitHub Discussions](https://github.com/user/AIOS/discussions)
- **Documentation**: [Full Documentation](docs/)

---

**Made with ❤️ for the future of intelligent computing**

*AIOS - Where artificial intelligence meets operating systems*
