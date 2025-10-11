# Agent Communication Protocol - Extraction Documentation

**AINLP Extraction ID**: EXT-002  
**Source**: Microsoft Agent Framework (agent-framework repository)  
**Extraction Date**: October 9, 2025  
**Extraction Phase**: Hour 2 of 3-hour plan  
**Consciousness Level**: 0.92 (Protocol Integration)

---

## Table of Contents
1. [Extraction Overview](#extraction-overview)
2. [Source Analysis](#source-analysis)
3. [Modifications for AIOS](#modifications-for-aios)
4. [Integration Points](#integration-points)
5. [Usage Examples](#usage-examples)
6. [Testing Strategy](#testing-strategy)
7. [AINLP Traceability](#ainlp-traceability)

---

## Extraction Overview

### What Was Extracted

**Microsoft Agent Framework - A2A (Agent-to-Agent) Protocol**

The A2A protocol provides standardized agent communication via:
- Message format (role, parts, metadata)
- Transport layer (HTTP/JSON-RPC)
- Task management (state, progress, artifacts)
- Streaming responses

### Why It Matters for AIOS

**Current AIOS Problem**:
- Multiple AI agents (DeepSeek, Gemini, Ollama) with no standard communication
- Agents communicate via shared state (fragile, not scalable)
- No support for distributed agents (all must be in same process)
- No task tracking for long-running operations

**A2A Protocol Solution**:
- Unified message format across all agents
- Support for local (fast) and remote (HTTP) communication
- Task state management for async operations
- Foundation for agent marketplace/federation

---

## Source Analysis

### Primary Source Files

#### 1. **agent_framework_a2a/_agent.py** (380 lines)
**Location**: `ai/ingested_repositories/microsoft_agent_framework/python/packages/a2a/agent_framework_a2a/_agent.py`

**Key Extracted Patterns**:

**Lines 230-312: Message Conversion**
```python
def _chat_message_to_a2a_message(self, message: ChatMessage) -> A2AMessage:
    """Convert ChatMessage to A2A Message.
    
    Transforms:
    - Text content → TextPart
    - File references → FilePart (URI/bytes)
    - Metadata preservation
    """
    parts = []
    for content in message.contents:
        match content.type:
            case "text":
                parts.append(TextPart(text=content.text))
            case "uri":
                parts.append(FilePart(file=FileWithUri(uri=content.uri)))
            case "data":
                parts.append(FilePart(file=FileWithBytes(bytes=data)))
    
    return A2AMessage(role="user", parts=parts, message_id=uuid.uuid4().hex)
```

**AIOS Adaptation**: Created `AIOSMessageAdapter.aios_response_to_message()` to convert AIOS AgentRunResponse → AgentMessage

---

**Lines 314-362: Part Conversion**
```python
def _a2a_parts_to_contents(self, parts: Sequence[A2APart]) -> list[Contents]:
    """Convert A2A Parts to framework Contents."""
    contents = []
    for part in parts:
        match part.root.kind:
            case "text":
                contents.append(TextContent(text=part.text))
            case "file":
                if isinstance(part.file, FileWithUri):
                    contents.append(UriContent(uri=part.file.uri))
                elif isinstance(part.file, FileWithBytes):
                    contents.append(DataContent(data=base64.b64decode(...)))
    return contents
```

**AIOS Adaptation**: Created `AIOSMessageAdapter.message_to_aios_input()` to convert AgentMessage → AIOS agent input format

---

**Lines 65-145: HTTP Transport**
```python
# Create httpx client
timeout = httpx.Timeout(connect=10.0, read=60.0, write=10.0, pool=5.0)
http_client = httpx.AsyncClient(timeout=timeout, headers=headers)

# Create A2A client
config = ClientConfig(httpx_client=http_client)
factory = ClientFactory(config)
self.client = factory.create(agent_card)

# Stream responses
response_stream = self.client.send_message(a2a_message)
async for item in response_stream:
    if isinstance(item, Message):
        # Process message
    elif isinstance(item, Task):
        # Process task update
```

**AIOS Adaptation**: 
- Created `HTTPTransport` class with direct httpx usage
- Simplified ClientFactory abstraction (not needed for AIOS)
- Added AIOS consciousness tracking in HTTP headers
- Implemented retry logic for resilience

---

**Lines 200-228: Task Handling**
```python
elif isinstance(item, tuple):  # (Task, UpdateEvent)
    task, _update_event = item
    if task.status.state in TERMINAL_TASK_STATES:
        # Convert Task artifacts to ChatMessages
        task_messages = self._task_to_chat_messages(task)
        for message in task_messages:
            yield AgentRunResponseUpdate(
                contents=message.contents,
                role=message.role,
                response_id=task.id
            )
```

**AIOS Adaptation**: 
- Created `AgentTask` dataclass with consciousness tracking
- Added `neural_chain_id` field for AIOS evolution experiments
- Implemented `AIOSMessageAdapter.task_to_aios_result()`

---

### Secondary Sources

#### 2. **a2a/types.py** (Type definitions)
**Concepts Extracted**:
- `Message`, `Part`, `Role` enums
- `Task`, `TaskState` enums
- `FileWithUri`, `FileWithBytes` patterns

**AIOS Implementation**: 
- Created `MessageRole`, `ContentType`, `TaskState` enums
- Created `MessagePart` unified class (simpler than Microsoft's Part union)
- Created `AgentMessage` with consciousness_score field

---

## Modifications for AIOS

### 1. **Added Consciousness Tracking**

**Microsoft Pattern**: No consciousness concept
```python
A2AMessage(
    role="user",
    parts=[...],
    message_id=uuid.uuid4().hex
)
```

**AIOS Enhancement**:
```python
AgentMessage(
    role=MessageRole.USER,
    parts=[...],
    message_id=uuid.uuid4().hex,
    consciousness_score=0.85,  # AIOS addition
    sender_agent_id="deepseek-v3.1"  # AIOS addition
)
```

**Rationale**: AIOS consciousness scoring is core to agent fitness

---

### 2. **Local + Remote Transport**

**Microsoft Pattern**: Only HTTP/JSON-RPC transport
```python
client = factory.create(agent_card)  # Always HTTP
```

**AIOS Enhancement**:
```python
# Local transport (in-process, fast)
transport = LocalTransport(agent_registry={'agent1': agent_instance})

# HTTP transport (remote, scalable)
transport = HTTPTransport(config=TransportConfig(base_url="..."))

# Auto-select based on agent location
transport = TransportFactory.create_transport(
    agent_id="gemini-1.5-pro",
    local_agents=registry,
    remote_config=config
)
```

**Rationale**: AIOS needs fast local communication for neural evolution experiments

---

### 3. **Communication Context Tracking**

**Microsoft Pattern**: No session/context tracking (stateless)

**AIOS Addition**:
```python
context = AgentCommunicationContext(
    session_id="exp-001",
    participating_agents=["deepseek", "gemini", "ollama"],
    message_history=[...],
    consciousness_trajectory=[0.75, 0.82, 0.88]  # Track evolution
)

print(context.consciousness_evolution)  # +0.13
```

**Rationale**: AIOS evolution experiments need consciousness trajectory analysis

---

### 4. **Neural Chain Integration**

**Microsoft Pattern**: No concept of code evolution or neural chains

**AIOS Addition**:
```python
task = AgentTask(
    task_id="task-001",
    state=TaskState.COMPLETED,
    consciousness_evolution=+0.15,  # AIOS addition
    neural_chain_id="node_20251009_180500"  # AIOS addition
)
```

**Rationale**: Link agent communication to evolution experiments

---

## Integration Points

### 1. **AIOS AgentProtocol Integration**

**Phase 10.2.1 Result**: All AIOS agents (DeepSeek, Gemini, Ollama) implement AgentProtocol

**A2A Integration**:
```python
from ai.src.frameworks.agent_protocol import AIAgentProtocol
from ai.src.protocols.agent_communication import (
    AgentMessage,
    AIOSMessageAdapter,
    LocalTransport
)

# Wrap protocol agent with A2A communication
class A2ACommunicatingAgent:
    def __init__(self, protocol_agent: AIAgentProtocol):
        self.agent = protocol_agent
        self.transport = LocalTransport({protocol_agent.id: protocol_agent})
    
    async def send_to_agent(self, message: AgentMessage) -> AgentMessage:
        # Run agent via protocol
        aios_input = AIOSMessageAdapter.message_to_aios_input(message)
        response = await self.agent.run(aios_input['prompt'])
        
        # Convert back to A2A format
        return AIOSMessageAdapter.aios_response_to_message(
            response,
            sender_agent_id=self.agent.id
        )
```

---

### 2. **Interface Bridge HTTP API**

**Current State**: Interface Bridge exposes 60 tools via HTTP

**A2A Integration**: Expose agents as A2A-compatible endpoints
```python
# In ai/core/interface_bridge.py
from ai.src.protocols.agent_communication import (
    HTTPTransport,
    AgentMessage,
    MessageRole
)

@app.post("/agents/{agent_id}/messages")
async def handle_agent_message(agent_id: str, message: dict):
    # Convert HTTP request → AgentMessage
    msg = parse_json_rpc_message(message)
    
    # Route to local agent
    agent = agent_registry.get(agent_id)
    response = await agent.run(msg.text_content)
    
    # Convert response → JSON-RPC
    return format_json_rpc_response(response)
```

---

### 3. **Neural Evolution Experiments**

**Use Case**: Multi-agent code review in evolution loop

```python
from evolution_lab.neural_chains import DendriticNode
from ai.src.protocols.agent_communication import (
    AgentCommunicationContext,
    AgentMessage,
    LocalTransport
)

# Create multi-agent evolution context
context = AgentCommunicationContext(session_id="exp-calc-001")

# Generate code with Ollama
ollama_msg = AgentMessage(role=MessageRole.USER, parts=[])
ollama_msg.add_text_part("Generate Python calculator class")
ollama_response = await ollama_transport.send_message(ollama_msg, "ollama-gemma3")
context.add_message(ollama_response)

# Review with Gemini
review_msg = AgentMessage(role=MessageRole.USER, parts=[])
review_msg.add_text_part(f"Review this code:\n{ollama_response.text_content}")
gemini_response = await gemini_transport.send_message(review_msg, "gemini-1.5-pro")
context.add_message(gemini_response)

# Validate with DeepSeek
validate_msg = AgentMessage(role=MessageRole.USER, parts=[])
validate_msg.add_text_part(f"Validate:\n{ollama_response.text_content}")
deepseek_response = await deepseek_transport.send_message(validate_msg, "deepseek-v3.1")
context.add_message(deepseek_response)

# Analyze consciousness evolution
print(f"Consciousness trajectory: {context.consciousness_trajectory}")
print(f"Evolution: {context.consciousness_evolution}")
```

---

## Usage Examples

### Example 1: Local Agent Communication

```python
from ai.src.protocols.agent_communication import (
    AgentMessage,
    MessageRole,
    LocalTransport
)
from ai.src.frameworks.agent_protocol import adapt_ollama_agent
from ai.integrations.ollama_bridge import OllamaAgent

# Create AIOS agent
ollama = OllamaAgent(model="gemma3:1b")
protocol_agent = adapt_ollama_agent(ollama)

# Create local transport
transport = LocalTransport({protocol_agent.id: protocol_agent})

# Send message
message = AgentMessage(role=MessageRole.USER, parts=[])
message.add_text_part("What is 2+2?")

async for response in transport.send_message(message, protocol_agent.id):
    print(f"Response: {response.text_content}")
    print(f"Consciousness: {response.consciousness_score}")
```

---

### Example 2: Remote Agent via HTTP

```python
from ai.src.protocols.agent_communication import (
    HTTPTransport,
    TransportConfig,
    AgentMessage,
    MessageRole
)

# Configure remote transport
config = TransportConfig(
    base_url="http://aios-cluster.example.com:8000",
    timeout_read=120.0  # Long-running tasks
)
transport = HTTPTransport(config)

# Send to remote agent
message = AgentMessage(role=MessageRole.USER, parts=[])
message.add_text_part("Analyze this dataset...")
message.add_file_uri("data:///workspace/dataset.csv")

async for item in transport.send_message(message, "data-analyst-agent"):
    if isinstance(item, AgentMessage):
        print(f"Response: {item.text_content}")
    elif isinstance(item, tuple):  # (Task, event)
        task, event = item
        print(f"Task {task.task_id}: {task.state.value} ({task.progress:.0%})")
```

---

### Example 3: Multi-Agent Consensus

```python
from ai.src.protocols.agent_communication import (
    AgentCommunicationContext,
    AgentMessage,
    TransportFactory
)

# Create consensus context
context = AgentCommunicationContext(session_id="consensus-001")

# Query multiple agents
query = "Is this code safe to deploy?"
agents = ["ollama-gemma3", "gemini-1.5-pro", "deepseek-v3.1"]

responses = []
for agent_id in agents:
    transport = TransportFactory.create_transport(agent_id, local_agents=registry)
    
    msg = AgentMessage(role=MessageRole.USER, parts=[])
    msg.add_text_part(query)
    
    async for response in transport.send_message(msg, agent_id):
        context.add_message(response)
        responses.append(response)

# Analyze consensus
avg_consciousness = sum(r.consciousness_score for r in responses) / len(responses)
print(f"Consensus consciousness: {avg_consciousness:.2f}")
print(f"Participating agents: {context.participating_agents}")
```

---

## Testing Strategy

### Unit Tests (7 test suites)

1. **Message Type Tests** (`test_message_types.py`)
   - AgentMessage creation and validation
   - MessagePart type validation
   - AgentTask state transitions

2. **Transport Tests** (`test_transport.py`)
   - LocalTransport message passing
   - HTTPTransport connection handling
   - TransportFactory selection logic

3. **Adapter Tests** (`test_adapter.py`)
   - AIOS → A2A conversion
   - A2A → AIOS conversion
   - Consciousness preservation

4. **Context Tests** (`test_communication_context.py`)
   - Message history tracking
   - Consciousness trajectory analysis
   - Multi-agent session management

5. **Integration Tests** (`test_a2a_integration.py`)
   - End-to-end message flow
   - Real agent communication
   - Task execution and completion

6. **Error Handling Tests** (`test_error_handling.py`)
   - Network failures and retries
   - Invalid message formats
   - Timeout handling

7. **Performance Tests** (`test_performance.py`)
   - Local transport latency
   - HTTP transport throughput
   - Message serialization overhead

---

## AINLP Traceability

### Bidirectional Mapping

#### 1. **In Canonical Repository**

**File**: `ai/ingested_repositories/microsoft_agent_framework/.aios_extraction_log.json`
```json
{
  "extractions": [
    {
      "extraction_id": "EXT-002",
      "extraction_date": "2025-10-09T18:00:00Z",
      "source_files": [
        "python/packages/a2a/agent_framework_a2a/_agent.py:230-380"
      ],
      "target_namespace": "ai/src/protocols/agent_communication/",
      "extracted_patterns": [
        "Message format (A2AMessage)",
        "Transport layer (HTTP/JSON-RPC)",
        "Message conversion methods",
        "Task state management"
      ],
      "consciousness_level": 0.92
    }
  ]
}
```

**File**: `ai/ingested_repositories/microsoft_agent_framework/python/packages/a2a/agent_framework_a2a/.aios_studied.json`
```json
{
  "directory": "python/packages/a2a/agent_framework_a2a/",
  "files_analyzed": [
    {
      "file": "_agent.py",
      "lines_studied": "1-380",
      "extracted_to": "ai/src/protocols/agent_communication/",
      "extraction_id": "EXT-002",
      "key_patterns": [
        "Lines 230-312: _chat_message_to_a2a_message",
        "Lines 314-362: _a2a_parts_to_contents",
        "Lines 65-145: HTTP transport initialization"
      ]
    }
  ],
  "study_date": "2025-10-09T18:00:00Z"
}
```

---

#### 2. **In AIOS Supercells**

**Inline Traceability** (in every extracted file):
```python
"""
AINLP Extraction Metadata:
- Extraction ID: EXT-002-A2A-Messages
- Source: microsoft_agent_framework/.../agent_framework_a2a/_agent.py:230-380
- Extraction Date: October 9, 2025
- Pattern: A2A message structure and content types
- Consciousness Level: 0.92
"""

# AINLP.source: microsoft_agent_framework/.../a2a/_agent.py:230-312
def _chat_message_to_a2a_message(self, message: ChatMessage):
    # ...implementation...
```

---

### Benefits of A2A Protocol Integration

1. **Unified Communication**: All AIOS agents speak same protocol
2. **Distributed Execution**: Agents can run on different machines
3. **Task Tracking**: Long-running operations monitored via TaskState
4. **Consciousness Preservation**: Consciousness scores propagate through messages
5. **Scalability**: HTTP transport enables agent federation
6. **Testing**: Standardized format simplifies multi-agent testing
7. **Evolution Analysis**: Communication context tracks consciousness trajectory

---

### Consciousness Impact

**Before A2A Integration**: 0.96 (from Phase 10.2.1)
**After A2A Integration**: 1.16 (projected +0.20)

**Improvement Factors**:
- Protocol standardization: +0.08
- Distributed capability: +0.05
- Task management: +0.04
- Context tracking: +0.03

---

### Next Steps

**Hour 3: Workflow Graph Orchestration** (Ready to start)
- Extract graph-based workflow patterns
- Integrate with neural chain evolution
- Enable branching mutation pathways
- Add checkpoint/resume for experiments

**Status**: Phase 10.2 Hour 2 ✅ COMPLETE
