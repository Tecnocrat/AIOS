# AIOS User Guide

## Getting Started

Welcome to AIOS (Artificial Intelligence Operating System)! This guide will help you get started with using and developing for AIOS.

## Installation

### Prerequisites
- Windows 10/11 (Linux/Mac support coming soon)
- Visual Studio 2022 or Visual Studio Code
- Python 3.11+
- .NET 8.0+
- CMake 3.20+
- Git

### Quick Setup
1. Clone the repository
2. Run the setup script:
   ```powershell
   .\setup.ps1
   ```
3. Open in Visual Studio Code
4. Install recommended extensions

## Basic Usage

### Starting AIOS

#### Option 1: Python AI Core
```bash
# Activate virtual environment
ai\venv\Scripts\activate

# Start AI services
python -m ai.src
```

#### Option 2: C++ Core
```bash
# Build first
cd build
cmake --build .

# Run
.\bin\aios_main.exe
```

### Natural Language Commands

AIOS understands natural language commands. Here are some examples:

#### System Monitoring
- "Show system status"
- "What's the current CPU usage?"
- "Monitor memory usage"
- "Check system health"

#### Predictions
- "Predict CPU usage for the next hour"
- "What will memory usage be like in 30 minutes?"
- "Forecast disk usage trends"

#### Automation
- "Schedule a system backup"
- "Automate log cleanup"
- "Set up performance monitoring"

#### Help and Information
- "What can you do?"
- "Show available commands"
- "Explain system architecture"

## Advanced Features

### Custom AI Models

You can configure custom AI models in `config/ai-models.json`:

```json
{
  "models": {
    "nlp": {
      "primary": {
        "name": "your-custom-model",
        "type": "conversational",
        "path": "./ai/models/your-model",
        "config": {
          "maxLength": 1000,
          "temperature": 0.8
        }
      }
    }
  }
}
```

### Theme Customization

Customize the UI theme in `config/ui-themes.json`:

```json
{
  "themes": {
    "custom": {
      "name": "My Custom Theme",
      "colors": {
        "primary": "#FF6B6B",
        "background": "#2C3E50",
        "text": "#FFFFFF"
      }
    }
  }
}
```

### System Configuration

Adjust system behavior in `config/system.json`:

```json
{
  "system": {
    "core": {
      "maxThreads": 16,
      "memoryLimit": "16GB",
      "logLevel": "DEBUG"
    },
    "ai": {
      "enableGpu": true,
      "batchSize": 64
    }
  }
}
```

## Development

### Project Structure
```
AIOS/
├── core/                 # C++ core system
│   ├── src/             # Source files
│   ├── include/         # Header files
│   └── CMakeLists.txt   # Build configuration
├── interface/           # C# UI interface
│   ├── AIOS.UI/        # WPF application
│   ├── AIOS.Services/  # Business logic
│   └── AIOS.Models/    # Data models
├── ai/                  # Python AI logic
│   ├── src/            # AI modules
│   ├── models/         # AI model files
│   └── requirements.txt # Python dependencies
├── config/             # Configuration files
├── docs/               # Documentation
└── resources/          # UI resources
```

### Adding New Features

#### Adding a New AI Capability

1. Create a new module in `ai/src/core/`:
   ```python
   # ai/src/core/mynewfeature/__init__.py
   class MyNewFeatureManager:
       def __init__(self, config):
           self.config = config
       
       async def initialize(self):
           # Initialize your feature
           pass
       
       async def process(self, data):
           # Process data
           return {"result": "processed"}
   ```

2. Register it in the main AI core:
   ```python
   # ai/src/__init__.py
   from .core.mynewfeature import MyNewFeatureManager
   
   class AICore:
       def __init__(self, config_path):
           # ... existing code ...
           self.mynewfeature_manager = MyNewFeatureManager(config)
   ```

#### Adding a New C++ Component

1. Create header file in `core/include/`:
   ```cpp
   // core/include/my_component.hpp
   #ifndef MY_COMPONENT_HPP
   #define MY_COMPONENT_HPP
   
   namespace aios {
       class MyComponent {
       public:
           MyComponent();
           bool initialize();
           void process();
       };
   }
   
   #endif
   ```

2. Create implementation in `core/src/`:
   ```cpp
   // core/src/my_component.cpp
   #include "my_component.hpp"
   
   namespace aios {
       MyComponent::MyComponent() {}
       
       bool MyComponent::initialize() {
           // Initialize component
           return true;
       }
       
       void MyComponent::process() {
           // Process logic
       }
   }
   ```

#### Adding a New C# Service

1. Create service class in `interface/AIOS.Services/`:
   ```csharp
   // interface/AIOS.Services/MyService.cs
   using System.Threading.Tasks;
   
   namespace AIOS.Services
   {
       public class MyService
       {
           public async Task<string> ProcessAsync(string input)
           {
               // Service logic
               return $"Processed: {input}";
           }
       }
   }
   ```

2. Register in dependency injection:
   ```csharp
   // interface/AIOS.UI/App.xaml.cs
   services.AddScoped<MyService>();
   ```

### Building and Testing

#### C++ Core
```bash
cd build
cmake ../core -DCMAKE_BUILD_TYPE=Debug
cmake --build .
ctest  # Run tests
```

#### C# Interface
```bash
cd interface
dotnet build
dotnet test
dotnet run --project AIOS.UI
```

#### Python AI
```bash
# Activate environment
ai\venv\Scripts\activate

# Run tests
python -m pytest ai/tests/

# Run AI services
python -m ai.src
```

## Troubleshooting

### Common Issues

#### Python Environment Issues
```bash
# Recreate virtual environment
Remove-Item -Recurse ai\venv
python -m venv ai\venv
ai\venv\Scripts\activate
pip install -r ai\requirements.txt
```

#### C++ Build Issues
```bash
# Clean build
Remove-Item -Recurse build
mkdir build
cd build
cmake ../core
```

#### Missing Dependencies
```bash
# Windows (using vcpkg)
vcpkg install boost opencv nlohmann-json

# Python
pip install --upgrade -r ai\requirements.txt
```

### Performance Optimization

#### AI Performance
- Enable GPU acceleration in `config/system.json`
- Adjust batch sizes for your hardware
- Use model quantization for faster inference

#### System Performance
- Adjust thread counts in configuration
- Monitor memory usage and adjust limits
- Enable profiling for performance analysis

### Debugging

#### Python Debugging
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable AI core debugging
ai_core = AICore()
ai_core.config["debug"] = True
```

#### C++ Debugging
```cpp
// Enable debug logging
#define AIOS_DEBUG 1

// Use debug builds
cmake ../core -DCMAKE_BUILD_TYPE=Debug
```

## Best Practices

### Code Organization
- Keep modules focused and single-purpose
- Use dependency injection for loose coupling
- Write comprehensive tests
- Document APIs thoroughly

### Configuration Management
- Use environment-specific configs
- Validate configuration on startup
- Provide sensible defaults
- Use structured logging

### Performance
- Profile critical paths
- Use async/await for I/O operations
- Implement proper caching
- Monitor resource usage

### Security
- Validate all inputs
- Use secure communication channels
- Implement proper authentication
- Regular security updates

## Contributing

### Development Workflow
1. Create feature branch
2. Implement changes
3. Write tests
4. Update documentation
5. Submit pull request

### Code Style
- Python: Follow PEP 8
- C++: Follow Google C++ Style Guide
- C#: Follow Microsoft C# conventions
- Use automated formatters

### Testing
- Write unit tests for all components
- Include integration tests
- Test cross-language communication
- Validate configuration scenarios

## Support

### Documentation
- [Architecture Guide](architecture.md)
- [API Reference](api-reference.md)
- [Project Context](../AIOS_PROJECT_CONTEXT.md)

### Community
- GitHub Issues for bugs
- Discussions for questions
- Wiki for community knowledge

### Resources
- [Official Website](https://aios.dev)
- [Developer Blog](https://blog.aios.dev)
- [Community Forum](https://forum.aios.dev)

## What's Next?

### Planned Features
- Cross-platform support (Linux, macOS)
- Plugin system for extensions
- Advanced AI model management
- Distributed system support
- Mobile companion app

### Roadmap
- Q1 2025: Core system stabilization
- Q2 2025: Advanced AI features
- Q3 2025: Cross-platform release
- Q4 2025: Plugin ecosystem

---

*This guide is continuously updated. For the latest information, check the documentation in the repository.*
