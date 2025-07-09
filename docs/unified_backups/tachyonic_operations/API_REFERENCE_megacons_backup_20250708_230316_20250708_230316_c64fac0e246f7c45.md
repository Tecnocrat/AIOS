# AIOS API Reference

## C++ Core API

### AIOSCore Class

#### Constructor
```cpp
AIOSCore(const std::string& config_file = "config/system.json");
```

#### Core Methods

##### initialize()
```cpp
bool initialize();
```
**Description**: Initializes the AIOS core system with configuration
**Returns**: `true` if successful, `false` otherwise
**Example**:
```cpp
AIOSCore core("config/system.json");
if (core.initialize()) {
    std::cout << "Core initialized successfully" << std::endl;
}
```

##### start()
```cpp
bool start();
```
**Description**: Starts the AIOS core services
**Returns**: `true` if successful, `false` otherwise
**Preconditions**: `initialize()` must be called first

##### stop()
```cpp
void stop();
```
**Description**: Stops all AIOS core services
**Example**:
```cpp
core.stop();
```

##### processCommand()
```cpp
bool processCommand(const std::string& command, json& response);
```
**Description**: Processes a command and returns JSON response
**Parameters**:
- `command`: Command string to process
- `response`: JSON object to store the response
**Returns**: `true` if command processed successfully
**Example**:
```cpp
json response;
if (core.processCommand("status", response)) {
    std::cout << response.dump(2) << std::endl;
}
```

##### isRunning()
```cpp
bool isRunning() const;
```
**Description**: Checks if the core system is running
**Returns**: `true` if running, `false` otherwise

##### getStatus()
```cpp
json getStatus() const;
```
**Description**: Returns current system status
**Returns**: JSON object containing system status information
**Example Response**:
```json
{
  "status": "running",
  "version": "0.4",
  "threads": 8,
  "memory_usage": "245MB",
  "uptime": "00:15:32"
}
```

##### healthCheck()
```cpp
json healthCheck() const;
```
**Description**: Performs system health check
**Returns**: JSON object with health status
**Example Response**:
```json
{
  "health": "healthy",
  "components": {
    "core": "ok",
    "memory": "ok",
    "threads": "ok"
  },
  "warnings": []
}
```

### JSON Helper Class

#### Constructor
```cpp
json();
json(const std::map<std::string, std::string>& data);
```

#### Methods

##### dump()
```cpp
std::string dump(int indent = 0) const;
```
**Description**: Converts JSON object to string representation
**Parameters**:
- `indent`: Number of spaces for indentation (unused in current implementation)
**Returns**: String representation of JSON object

##### operator[]
```cpp
std::string& operator[](const std::string& key);
const std::string& operator[](const std::string& key) const;
```
**Description**: Access JSON object values by key
**Parameters**:
- `key`: Key to access
**Returns**: Reference to value associated with key

## Python AI API

### NLPManager Class

#### Constructor
```python
def __init__(self, config: Dict[str, Any])
```
**Parameters**:
- `config`: Configuration dictionary for NLP settings

#### Methods

##### initialize()
```python
async def initialize(self) -> bool
```
**Description**: Initializes NLP models and resources
**Returns**: `True` if successful, `False` otherwise
**Example**:
```python
nlp_config = {
    "primary": {"model": "transformer", "enabled": True},
    "fallback": {"model": "rule-based", "enabled": True}
}
nlp = NLPManager(nlp_config)
success = await nlp.initialize()
```

##### start()
```python
async def start(self) -> bool
```
**Description**: Starts NLP processing services
**Returns**: `True` if successful, `False` otherwise
**Preconditions**: `initialize()` must be called first

##### stop()
```python
async def stop(self)
```
**Description**: Stops NLP processing services

##### process()
```python
async def process(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]
```
**Description**: Processes text input and returns analysis results
**Parameters**:
- `text`: Input text to process
- `context`: Optional context dictionary
**Returns**: Dictionary with processing results
**Example**:
```python
result = await nlp.process("Hello, how are you?")
print(result)
# Output: {
#   'input': 'Hello, how are you?',
#   'intent': 'greeting',
#   'entities': [],
#   'confidence': 0.95,
#   'processed': True
# }
```

##### health_check()
```python
async def health_check(self) -> Dict[str, Any]
```
**Description**: Performs health check on NLP system
**Returns**: Dictionary with health status

### PredictionManager Class

#### Constructor
```python
def __init__(self, config: Dict[str, Any])
```
**Parameters**:
- `config`: Configuration dictionary for prediction settings

#### Methods

##### predict()
```python
async def predict(self, data: Dict[str, Any]) -> Dict[str, Any]
```
**Description**: Makes predictions based on input data
**Parameters**:
- `data`: Input data dictionary
**Returns**: Dictionary with prediction results
**Example**:
```python
prediction_result = await prediction.predict({"user_input": "predict weather"})
print(prediction_result)
# Output: {
#   'type': 'weather',
#   'prediction': 'Sunny, 75°F',
#   'confidence': 0.82,
#   'timestamp': '2025-07-07T10:30:00'
# }
```

##### update_model()
```python
async def update_model(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]
```
**Description**: Updates prediction model with new training data
**Parameters**:
- `training_data`: List of training examples
**Returns**: Dictionary with update results

### AutomationManager Class

#### Constructor
```python
def __init__(self, config: Dict[str, Any])
```
**Parameters**:
- `config`: Configuration dictionary for automation settings

#### Methods

##### execute_task()
```python
async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]
```
**Description**: Executes an automation task
**Parameters**:
- `task`: Task definition dictionary
**Returns**: Dictionary with execution results
**Example**:
```python
task_result = await automation.execute_task({
    "task_name": "file_backup",
    "parameters": {"source": "/data", "destination": "/backup"}
})
print(task_result)
# Output: {
#   'task_id': 'backup_001',
#   'status': 'completed',
#   'result': 'Successfully backed up 150 files'
# }
```

##### schedule_task()
```python
async def schedule_task(self, task: Dict[str, Any], schedule: str) -> Dict[str, Any]
```
**Description**: Schedules a task for future execution
**Parameters**:
- `task`: Task definition dictionary
- `schedule`: Schedule specification (cron-like format)
**Returns**: Dictionary with scheduling results

### LearningManager Class

#### Constructor
```python
def __init__(self, config: Dict[str, Any])
```
**Parameters**:
- `config`: Configuration dictionary for learning settings

#### Methods

##### update()
```python
async def update(self, data: Dict[str, Any]) -> Dict[str, Any]
```
**Description**: Updates learning system with new data
**Parameters**:
- `data`: Learning data dictionary
**Returns**: Dictionary with update results
**Example**:
```python
learning_result = await learning.update({
    "user_action": "file_open",
    "context": {"file_type": "python", "time": "morning"},
    "outcome": "success"
})
```

##### get_insights()
```python
async def get_insights(self) -> Dict[str, Any]
```
**Description**: Retrieves learning insights and patterns
**Returns**: Dictionary with insights and recommendations

### IntegrationBridge Class

#### Constructor
```python
def __init__(self, config: Dict[str, Any])
```
**Parameters**:
- `config`: Configuration dictionary for integration settings

#### Methods

##### send_message()
```python
async def send_message(self, target: str, message: Dict[str, Any]) -> Dict[str, Any]
```
**Description**: Sends a message to another component
**Parameters**:
- `target`: Target component identifier
- `message`: Message dictionary
**Returns**: Dictionary with send results
**Example**:
```python
result = await integration.send_message("cpp_core", {
    "command": "system_status",
    "parameters": {}
})
```

##### receive_message()
```python
async def receive_message(self, source: str) -> Optional[Dict[str, Any]]
```
**Description**: Receives a message from another component
**Parameters**:
- `source`: Source component identifier
**Returns**: Message dictionary or None if no message

## C# Interface API (Planned)

### MainWindow Class

#### Constructor
```csharp
public MainWindow()
```

#### Properties

##### IsSystemRunning
```csharp
public bool IsSystemRunning { get; private set; }
```
**Description**: Indicates if the AIOS system is running

#### Methods

##### InitializeSystem()
```csharp
public async Task<bool> InitializeSystem()
```
**Description**: Initializes the AIOS system
**Returns**: `true` if successful, `false` otherwise

##### ProcessCommand()
```csharp
public async Task<string> ProcessCommand(string command)
```
**Description**: Processes a user command
**Parameters**:
- `command`: Command string to process
**Returns**: JSON response string

### SystemMonitor Class

#### Methods

##### GetSystemStatus()
```csharp
public async Task<SystemStatus> GetSystemStatus()
```
**Description**: Retrieves current system status
**Returns**: SystemStatus object

##### GetPerformanceMetrics()
```csharp
public async Task<PerformanceMetrics> GetPerformanceMetrics()
```
**Description**: Retrieves system performance metrics
**Returns**: PerformanceMetrics object

### AIInteractionPanel Class

#### Methods

##### SendMessage()
```csharp
public async Task<AIResponse> SendMessage(string message)
```
**Description**: Sends a message to the AI system
**Parameters**:
- `message`: Message to send
**Returns**: AIResponse object

##### GetConversationHistory()
```csharp
public List<ConversationItem> GetConversationHistory()
```
**Description**: Retrieves conversation history
**Returns**: List of conversation items

## Data Transfer Objects

### SystemStatus (C#)
```csharp
public class SystemStatus
{
    public string Status { get; set; }
    public string Version { get; set; }
    public int ThreadCount { get; set; }
    public long MemoryUsage { get; set; }
    public TimeSpan Uptime { get; set; }
}
```

### AIResponse (C#)
```csharp
public class AIResponse
{
    public string Response { get; set; }
    public double Confidence { get; set; }
    public DateTime Timestamp { get; set; }
    public Dictionary<string, object> Metadata { get; set; }
}
```

### ConversationItem (C#)
```csharp
public class ConversationItem
{
    public string Message { get; set; }
    public string Response { get; set; }
    public DateTime Timestamp { get; set; }
    public bool IsFromUser { get; set; }
}
```

## Error Handling

### Common Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `AIOS_001` | System initialization failed | Check configuration files |
| `AIOS_002` | AI model loading failed | Verify model files exist |
| `AIOS_003` | Cross-language communication error | Check integration bridge |
| `AIOS_004` | Invalid command format | Verify command syntax |
| `AIOS_005` | Resource limit exceeded | Reduce resource usage |

### Error Response Format
```json
{
  "error": {
    "code": "AIOS_001",
    "message": "System initialization failed",
    "details": "Configuration file not found: config/system.json",
    "timestamp": "2025-07-07T10:30:00Z"
  }
}
```

## Integration Examples

### C++ to Python Communication
```cpp
// C++ side
json command;
command["action"] = "nlp_process";
command["data"]["text"] = "Hello, world!";
json response = integration_bridge.sendToPython(command);
```

### Python to C++ Communication
```python
# Python side
message = {
    "action": "system_status",
    "parameters": {}
}
response = await integration.send_message("cpp_core", message)
```

### C# to System Communication
```csharp
// C# side
var command = new
{
    action = "execute_task",
    parameters = new { task = "file_backup" }
};
var response = await systemInterface.ProcessCommand(JsonConvert.SerializeObject(command));
```

This API reference provides comprehensive documentation for all major components of the AIOS system, enabling developers to effectively integrate with and extend the system.
