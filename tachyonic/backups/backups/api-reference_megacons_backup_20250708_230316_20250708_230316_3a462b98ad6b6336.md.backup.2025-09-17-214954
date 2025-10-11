# AIOS API Reference

## Python AI Core API

### AICore Class

The main entry point for all AI functionality.

#### Initialization
```python
from ai.src import AICore

# Initialize with default config
ai_core = AICore()

# Initialize with custom config
ai_core = AICore("custom/config/path.json")
```

#### Basic Operations
```python
# Initialize the AI system
await ai_core.initialize()

# Start AI services
await ai_core.start()

# Process natural language
result = await ai_core.process_natural_language("predict cpu usage for next hour")

# Get system predictions
prediction = await ai_core.get_system_prediction("cpu", horizon=3600)

# Stop AI services
await ai_core.stop()
```

#### Status and Health
```python
# Get current status
status = ai_core.get_status()

# Perform health check
health = await ai_core.health_check()
```

### NLP Manager

Handles natural language processing tasks.

#### Methods
- `process(text, context=None)` - Process natural language input
- `get_status()` - Get current status
- `health_check()` - Perform health check

### Prediction Manager

Handles predictive analytics.

#### Methods
- `predict(data)` - Make general predictions
- `predict_resource(metric, horizon)` - Predict system resource usage
- `get_status()` - Get current status
- `health_check()` - Perform health check

### Automation Manager

Handles task automation.

#### Methods
- `execute_task(task)` - Execute an automation task
- `process_task(nlp_result)` - Process task from NLP result
- `get_status()` - Get current status
- `health_check()` - Perform health check

### Learning Manager

Handles continuous learning.

#### Methods
- `update(data)` - Update learning system with new data
- `get_knowledge_summary()` - Get knowledge base summary
- `get_status()` - Get current status
- `health_check()` - Perform health check

### Integration Bridge

Handles cross-language communication.

#### Methods
- `send_message(target, message)` - Send message to target component
- `receive_message(source)` - Receive message from source
- `get_bridge_status(bridge_name)` - Get specific bridge status
- `get_status()` - Get current status
- `health_check()` - Perform health check

## C++ Core API

### Core Class

The main system manager.

#### Initialization
```cpp
#include "aios_core.hpp"

// Initialize with default config
aios::Core core;

// Initialize with custom config
aios::Core core("custom/config/path.json");
```

#### Basic Operations
```cpp
// Initialize the system
bool success = core.initialize();

// Start the system
bool started = core.start();

// Process natural language command
nlohmann::json result = core.processCommand("show system status");

// Stop the system
core.stop();
```

#### Component Access
```cpp
// Get system manager
auto sysManager = core.getSystemManager();

// Get AI manager
auto aiManager = core.getAIManager();

// Get configuration manager
auto configManager = core.getConfigManager();

// Get logger
auto logger = core.getLogger();
```

## Configuration API

### System Configuration (`config/system.json`)

```json
{
  "system": {
    "name": "AIOS",
    "version": "1.0.0",
    "core": {
      "maxThreads": 8,
      "memoryLimit": "8GB",
      "logLevel": "INFO"
    },
    "ai": {
      "modelPath": "./ai/models/",
      "enableGpu": true,
      "batchSize": 32
    },
    "ui": {
      "theme": "dark",
      "language": "en-US"
    }
  }
}
```

### AI Models Configuration (`config/ai-models.json`)

```json
{
  "models": {
    "nlp": {
      "primary": {
        "name": "microsoft/DialoGPT-medium",
        "type": "conversational",
        "config": {
          "maxLength": 1000,
          "temperature": 0.7
        }
      }
    }
  }
}
```

### UI Themes Configuration (`config/ui-themes.json`)

```json
{
  "themes": {
    "dark": {
      "colors": {
        "primary": "#2D3748",
        "background": "#1A202C",
        "text": "#F7FAFC"
      }
    }
  }
}
```

## Error Handling

### Python
```python
try:
    result = await ai_core.process_natural_language("invalid command")
except RuntimeError as e:
    print(f"Runtime error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### C++
```cpp
try {
    auto result = core.processCommand("invalid command");
} catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << std::endl;
}
```

## Best Practices

1. **Always initialize before use**
   ```python
   await ai_core.initialize()
   await ai_core.start()
   ```

2. **Handle errors gracefully**
   ```python
   if not await ai_core.initialize():
       print("Failed to initialize AI core")
       return
   ```

3. **Clean up resources**
   ```python
   try:
       # Your code here
   finally:
       await ai_core.stop()
   ```

4. **Use structured logging**
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.info("Processing started")
   ```

5. **Validate configurations**
   ```python
   if not config.get("ai", {}).get("enableGpu", False):
       logger.warning("GPU acceleration disabled")
   ```

## Examples

### Complete Python Example
```python
import asyncio
from ai.src import AICore

async def main():
    ai_core = AICore()
    
    try:
        # Initialize
        if not await ai_core.initialize():
            print("Failed to initialize")
            return
        
        if not await ai_core.start():
            print("Failed to start")
            return
        
        # Process commands
        result = await ai_core.process_natural_language(
            "predict memory usage for next 30 minutes"
        )
        print(f"Result: {result}")
        
        # Get status
        status = ai_core.get_status()
        print(f"Status: {status}")
        
    finally:
        await ai_core.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### Complete C++ Example
```cpp
#include "aios_core.hpp"
#include <iostream>

int main() {
    try {
        aios::Core core;
        
        if (!core.initialize()) {
            std::cerr << "Failed to initialize" << std::endl;
            return 1;
        }
        
        if (!core.start()) {
            std::cerr << "Failed to start" << std::endl;
            return 1;
        }
        
        auto result = core.processCommand("show system health");
        std::cout << result.dump(2) << std::endl;
        
        core.stop();
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
```
