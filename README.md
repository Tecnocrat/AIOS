# AIOS - Artificial Intelligence Operating System

[![Version](https://img.shields.io/badge/version-0.4-blue.svg)](https://github.com/Tecnocrat/AIOS/tree/OS0.4)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)
[![License](https://img.shields.io/badge/license-TBD-yellow.svg)](docs/LICENSE_DECISION.md)

> **A revolutionary intelligent operating system designed to make current software paradigms obsolete**

AIOS integrates multiple programming languages and AI technologies to create a unified, intelligent computing environment that understands human intent and executes complex operations seamlessly.

## 🚀 **Quick Start**

### **One-Command Setup**
```bash
# Clone and setup
git clone https://github.com/Tecnocrat/AIOS.git -b OS0.4
cd AIOS
.\scripts\setup.ps1  # Windows
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
- **C# Interface**: Modern desktop UI with WPF/WinUI
- **Cross-Language Integration**: Seamless communication between all components

### **🔧 Developer-Friendly**
- **Modular Design**: Easy to extend and customize
- **Comprehensive Documentation**: Everything you need to contribute
- **Automated Testing**: Integration tests ensure system reliability
- **Multiple IDEs**: Works with Visual Studio, VS Code, and more

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
│   ├── AIOS.Services/  # Business logic
│   └── AIOS.Models/    # Data models
└── docs/          # Documentation
    ├── ARCHITECTURE.md
    ├── API_REFERENCE.md
    └── DEVELOPMENT.md
```

## 📊 **Current Status**

| Component         | Status        | Details                                                       |
| ----------------- | ------------- | ------------------------------------------------------------- |
| **C++ Core**      | ✅ Complete    | Fully functional with vcpkg dependencies                      |
| **Python AI**     | ✅ Complete    | 5 modules: NLP, Prediction, Automation, Learning, Integration |
| **Integration**   | ✅ Complete    | Cross-language communication working                          |
| **C# UI**         | 🔄 In Progress | Scaffolded, implementation in progress                        |
| **Documentation** | 🔄 In Progress | Architecture complete, API docs in progress                   |
| **Testing**       | ✅ Complete    | Integration tests passing                                     |

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
```

## 📚 **Documentation**

### **🤖 For AI Systems & Assistants**
- [**AI Context Reallocator**](docs/ai-context/AI_context_reallocator.md) - **MUST READ FIRST** - Context preservation protocol
- [**AI Quick Reference**](docs/ai-context/AI_QUICK_REFERENCE.md) - Quick commands and procedures
- [**Project Status**](docs/ai-context/PROJECT_STATUS.md) - Current implementation status
- [**Documentation Index**](docs/DOCUMENTATION_INDEX.md) - Master documentation guide

### **For Users**
- [**Installation Guide**](docs/INSTALLATION.md) - Detailed setup instructions
- [**User Guide**](docs/USER_GUIDE.md) - How to use AIOS
- [**FAQ**](docs/FAQ.md) - Common questions and answers

### **For Developers**
- [**Architecture Overview**](docs/ARCHITECTURE.md) - System design and components
- [**API Reference**](docs/API_REFERENCE.md) - Programming interfaces
- [**Development Guide**](docs/DEVELOPMENT.md) - Contributing guidelines
- [**Installation Guide**](docs/INSTALLATION.md) - Environment setup

### **🎯 Self-Orchestrating Documentation System**
AIOS includes a comprehensive self-orchestrating documentation system designed to preserve context across AI iterations and development sessions:

- **Context Preservation**: AI systems can bootstrap themselves from any state
- **Memory Recovery**: Comprehensive troubleshooting and recovery procedures
- **Version Tracking**: Detailed project status and implementation tracking
- **Self-Updating**: Documentation that maintains itself across iterations

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

- Python virtual environment activation varies by system
- C# UI implementation is incomplete
- Documentation is still being written

## 📋 **Roadmap**

### **Version 0.4 (Current)**
- [x] C++ Core implementation
- [x] Python AI modules
- [x] Cross-language integration
- [x] Basic testing framework
- [ ] Complete C# UI
- [ ] Full documentation suite

### **Version 0.5 (Next)**
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
