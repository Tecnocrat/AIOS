# AIOS Development Guide

## Getting Started

### Development Environment Setup

#### Required Tools
- **Visual Studio 2022** (C# development)
- **Visual Studio Code** (multi-language development)
- **CMake 3.20+** (C++ build system)
- **Python 3.11+** (AI modules)
- **vcpkg** (C++ package manager)
- **Git** (version control)

#### Recommended Extensions for VS Code
```json
{
  "recommendations": [
    "ms-vscode.cpptools",
    "ms-dotnettools.csharp",
    "ms-python.python",
    "ms-vscode.cmake-tools",
    "github.copilot",
    "ms-vscode.vscode-json",
    "yzhang.markdown-all-in-one"
  ]
}
```

### Initial Setup

1. **Clone the Repository**
```bash
git clone https://github.com/user/AIOS.git -b OS0.4
cd AIOS
```

2. **Run Setup Script**
```bash
./setup.ps1  # Windows
```

3. **Verify Installation**
```bash
python test_integration.py
```

## Development Workflow

### Branch Strategy
- **OS0.4**: Main development branch for version 0.4
- **feature/***: Feature development branches
- **hotfix/***: Critical bug fixes
- **docs/***: Documentation updates

### Commit Guidelines

#### Commit Message Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

#### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only changes
- **style**: Formatting, missing semi-colons, etc.
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **test**: Adding missing tests
- **chore**: Changes to build process or auxiliary tools

#### Examples
```bash
feat(core): add command processing interface
fix(ai): resolve NLP model loading issue
docs(api): update Python API documentation
test(integration): add cross-language communication tests
```

### Pull Request Process

1. **Create Feature Branch**
```bash
git checkout -b feature/amazing-feature
```

2. **Make Changes and Test**
```bash
# Make your changes
# Run tests
python test_integration.py
cd core/build && ./tests/Debug/test_core.exe
```

3. **Commit Changes**
```bash
git add .
git commit -m "feat(component): add amazing feature"
```

4. **Push and Create PR**
```bash
git push origin feature/amazing-feature
# Create pull request on GitHub
```

## Code Standards

### C++ Standards

#### Style Guide
- Follow Google C++ Style Guide
- Use modern C++20 features
- Prefer RAII and smart pointers
- Use const-correctness

#### Example Code
```cpp
// Good
class AIOSCore {
private:
    std::unique_ptr<ConfigManager> config_manager_;
    std::atomic<bool> is_running_{false};

public:
    bool initialize(const std::string& config_path) {
        if (config_path.empty()) {
            return false;
        }
        
        config_manager_ = std::make_unique<ConfigManager>(config_path);
        return config_manager_->load();
    }
    
    void stop() noexcept {
        is_running_.store(false);
    }
};

// Bad
class AIOSCore {
    ConfigManager* config_manager;  // Raw pointer
    bool is_running;                // Not thread-safe
    
public:
    bool initialize(std::string config_path) {  // Unnecessary copy
        config_manager = new ConfigManager(config_path);  // Manual memory management
        return true;
    }
};
```

#### Build Configuration
```cmake
# CMakeLists.txt best practices
cmake_minimum_required(VERSION 3.20)
project(AIOS_Core VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Use vcpkg for dependencies
find_package(Boost REQUIRED COMPONENTS system filesystem thread)
find_package(OpenCV REQUIRED)
find_package(nlohmann_json REQUIRED)

# Enable warnings
if(MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()
```

### Python Standards

#### Style Guide
- Follow PEP 8
- Use type hints for all functions
- Prefer async/await for I/O operations
- Use dataclasses for data structures

#### Example Code
```python
# Good
from typing import Dict, List, Optional, Any
import asyncio
import logging
from dataclasses import dataclass

@dataclass
class ProcessingResult:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class NLPManager:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self._is_running = False
        self._logger = logging.getLogger(__name__)
    
    async def process(self, text: str, context: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        if not self._is_running:
            return ProcessingResult(
                success=False,
                error_message="NLP Manager is not running"
            )
        
        try:
            result = await self._process_text(text, context)
            return ProcessingResult(success=True, data=result)
        except Exception as e:
            self._logger.error(f"Processing failed: {e}")
            return ProcessingResult(success=False, error_message=str(e))

# Bad
class NLPManager:
    def __init__(self, config):  # No type hints
        self.config = config
        self.is_running = False
    
    def process(self, text, context=None):  # Synchronous, no error handling
        result = self.process_text(text, context)
        return result
```

#### Project Structure
```
ai/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── nlp/
│   │   ├── prediction/
│   │   ├── automation/
│   │   ├── learning/
│   │   └── integration/
│   └── utils/
├── tests/
│   ├── __init__.py
│   ├── test_nlp.py
│   ├── test_prediction.py
│   └── conftest.py
├── requirements.txt
└── setup.py
```

### C# Standards

#### Style Guide
- Follow Microsoft C# Coding Conventions
- Use async/await for asynchronous operations
- Implement proper disposal patterns
- Use dependency injection

#### Example Code
```csharp
// Good
public interface ISystemMonitor
{
    Task<SystemStatus> GetStatusAsync();
    Task<bool> StartMonitoringAsync();
    void StopMonitoring();
}

public class SystemMonitor : ISystemMonitor, IDisposable
{
    private readonly ILogger<SystemMonitor> _logger;
    private readonly CancellationTokenSource _cancellationTokenSource;
    private bool _disposed = false;

    public SystemMonitor(ILogger<SystemMonitor> logger)
    {
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _cancellationTokenSource = new CancellationTokenSource();
    }

    public async Task<SystemStatus> GetStatusAsync()
    {
        try
        {
            // Implementation
            return new SystemStatus { IsHealthy = true };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to get system status");
            throw;
        }
    }

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

    protected virtual void Dispose(bool disposing)
    {
        if (!_disposed && disposing)
        {
            _cancellationTokenSource?.Dispose();
            _disposed = true;
        }
    }
}

// Bad
public class SystemMonitor
{
    public SystemStatus GetStatus()  // Synchronous
    {
        return new SystemStatus();   // No error handling
    }
}
```

## Testing Guidelines

### Test Organization

#### C++ Testing
```cpp
// tests/test_core.cpp
#include <gtest/gtest.h>
#include "aios_core.hpp"

class AIOSCoreTest : public ::testing::Test {
protected:
    void SetUp() override {
        core = std::make_unique<AIOSCore>("test_config.json");
    }
    
    void TearDown() override {
        if (core && core->isRunning()) {
            core->stop();
        }
    }
    
    std::unique_ptr<AIOSCore> core;
};

TEST_F(AIOSCoreTest, InitializeSuccessfully) {
    EXPECT_TRUE(core->initialize());
    EXPECT_FALSE(core->isRunning());
}

TEST_F(AIOSCoreTest, StartAndStopCorrectly) {
    ASSERT_TRUE(core->initialize());
    EXPECT_TRUE(core->start());
    EXPECT_TRUE(core->isRunning());
    
    core->stop();
    EXPECT_FALSE(core->isRunning());
}
```

#### Python Testing
```python
# tests/test_nlp.py
import pytest
import asyncio
from unittest.mock import Mock, patch
from src.core.nlp import NLPManager

@pytest.fixture
async def nlp_manager():
    config = {
        "primary": {"model": "test", "enabled": True},
        "fallback": {"model": "simple", "enabled": True}
    }
    manager = NLPManager(config)
    await manager.initialize()
    await manager.start()
    yield manager
    await manager.stop()

@pytest.mark.asyncio
async def test_process_text_successfully(nlp_manager):
    result = await nlp_manager.process("Hello, world!")
    
    assert result["processed"] is True
    assert "intent" in result
    assert result["confidence"] > 0

@pytest.mark.asyncio
async def test_process_with_context(nlp_manager):
    context = {"user_id": "test_user", "session_id": "test_session"}
    result = await nlp_manager.process("Book a meeting", context)
    
    assert result["processed"] is True
    assert result["context"] == context
```

#### Integration Testing
```python
# test_integration.py
async def test_cross_language_communication():
    # Test C++ core
    cpp_result = test_cpp_core()
    assert cpp_result, "C++ core failed"
    
    # Test Python AI modules
    ai_result = await test_ai_modules()
    assert ai_result, "Python AI modules failed"
    
    # Test integration
    integration_result = await test_integration_bridge()
    assert integration_result, "Integration bridge failed"
```

### Test Configuration

#### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

#### Test Requirements
```txt
# tests/requirements.txt
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-mock>=3.10.0
pytest-cov>=4.0.0
```

## Debugging Guidelines

### Multi-Language Debugging

#### C++ Debugging
```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug C++ Core",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/core/build/bin/Debug/aios_main.exe",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        }
    ]
}
```

#### Python Debugging
```json
{
    "name": "Debug Python AI",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/test_integration.py",
    "console": "integratedTerminal",
    "cwd": "${workspaceFolder}",
    "env": {
        "PYTHONPATH": "${workspaceFolder}/ai/src"
    }
}
```

### Logging Configuration

#### C++ Logging
```cpp
// Include logging utility
#include "logger.hpp"

class AIOSCore {
private:
    Logger logger_;
    
public:
    bool initialize() {
        logger_.info("Initializing AIOS Core");
        
        try {
            // Initialization code
            logger_.info("AIOS Core initialized successfully");
            return true;
        } catch (const std::exception& e) {
            logger_.error("Failed to initialize: " + std::string(e.what()));
            return false;
        }
    }
};
```

#### Python Logging
```python
import logging
import json
from datetime import datetime

# Configure structured logging
class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "file": record.filename,
            "line": record.lineno
        }
        return json.dumps(log_entry)

# Setup logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(StructuredFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

## Performance Guidelines

### Optimization Strategies

#### C++ Performance
- Use move semantics for large objects
- Prefer stack allocation over heap allocation
- Use const references for read-only parameters
- Implement proper caching strategies

```cpp
// Good: Move semantics
std::vector<std::string> processData(std::vector<std::string>&& input) {
    std::vector<std::string> result;
    result.reserve(input.size());
    
    for (auto&& item : input) {
        result.emplace_back(std::move(item));
    }
    
    return result;
}

// Good: Const reference
void processConfig(const json& config) {
    // Read-only access, no copying
}
```

#### Python Performance
- Use async/await for I/O bound operations
- Implement connection pooling
- Cache expensive computations
- Use type hints for better optimization

```python
import asyncio
from functools import lru_cache
from typing import Dict, Any

class NLPManager:
    @lru_cache(maxsize=1000)
    def _cached_process(self, text: str) -> Dict[str, Any]:
        """Cache frequently processed text"""
        return self._expensive_nlp_operation(text)
    
    async def process_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Process multiple texts concurrently"""
        tasks = [self._process_single(text) for text in texts]
        return await asyncio.gather(*tasks)
```

### Memory Management

#### C++ Memory Best Practices
```cpp
// Use smart pointers
std::unique_ptr<Resource> createResource() {
    return std::make_unique<Resource>();
}

// RAII for resource management
class ResourceManager {
private:
    std::unique_ptr<Resource> resource_;
    
public:
    ResourceManager() : resource_(std::make_unique<Resource>()) {}
    
    // Automatic cleanup when object goes out of scope
    ~ResourceManager() = default;
};
```

#### Python Memory Best Practices
```python
import gc
import weakref
from contextlib import contextmanager

@contextmanager
def managed_resource(resource_factory):
    """Context manager for automatic resource cleanup"""
    resource = None
    try:
        resource = resource_factory()
        yield resource
    finally:
        if resource and hasattr(resource, 'cleanup'):
            resource.cleanup()
        gc.collect()  # Force garbage collection if needed
```

## Documentation Standards

### Code Documentation

#### C++ Documentation
```cpp
/**
 * @brief Processes a command and returns a JSON response
 * 
 * This method takes a command string, validates it, processes it through
 * the appropriate subsystem, and returns a structured JSON response.
 * 
 * @param command The command string to process
 * @param response JSON object to store the response
 * @return true if the command was processed successfully, false otherwise
 * 
 * @throws std::invalid_argument if command is empty
 * @throws std::runtime_error if system is not initialized
 * 
 * @example
 * ```cpp
 * json response;
 * if (core.processCommand("status", response)) {
 *     std::cout << response.dump(2) << std::endl;
 * }
 * ```
 */
bool processCommand(const std::string& command, json& response);
```

#### Python Documentation
```python
async def process(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Process text input and return analysis results.
    
    This method performs natural language processing on the input text,
    including intent recognition, entity extraction, and context analysis.
    
    Args:
        text: The input text to process. Must not be empty.
        context: Optional context dictionary containing additional information
                that may influence processing results.
    
    Returns:
        A dictionary containing:
        - input: The original input text
        - intent: Recognized intent classification
        - entities: List of extracted entities
        - confidence: Confidence score (0.0 to 1.0)
        - context: The provided context (if any)
        - processed: Boolean indicating successful processing
    
    Raises:
        ValueError: If text is empty or None
        RuntimeError: If the NLP manager is not running
    
    Example:
        >>> result = await nlp.process("Hello, world!")
        >>> print(result['intent'])
        'greeting'
    """
```

### API Documentation Updates

When adding new APIs, update the following files:
1. `docs/API_REFERENCE.md` - Add method signatures and examples
2. `README.md` - Update feature list if applicable
3. `CHANGELOG.md` - Document the changes
4. `AI_context_reallocator.md` - Update context if significant

## Contributing Guidelines

### Before Contributing
1. Read this development guide thoroughly
2. Check existing issues and pull requests
3. Run the full test suite
4. Ensure code follows style guidelines

### Contribution Checklist
- [ ] Code follows style guidelines
- [ ] Tests added for new functionality
- [ ] Documentation updated
- [ ] Integration tests pass
- [ ] No breaking changes (or properly documented)
- [ ] Commit messages follow convention

### Review Process
1. **Automated Checks**: All CI/CD checks must pass
2. **Code Review**: At least one maintainer review required
3. **Testing**: Integration tests must pass
4. **Documentation**: Relevant documentation must be updated

This development guide ensures consistent, high-quality contributions to the AIOS project while maintaining the system's architectural integrity and performance standards.
