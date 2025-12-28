# IACP Knowledge Ingestion Map

> **Document Type**: Curated Resource Index  
> **Created**: 2025-12-03  
> **Purpose**: Enable AIOS agents to metabolize external knowledge into distributed documentation  
> **Parent**: [dev_path_evolution.md](./dev_path_evolution.md)

---

## 🎯 Ingestion Strategy

AIOS agents should process these resources in priority order:
1. **Core Protocol Resources** → Extract API patterns, message schemas
2. **Architectural Foundations** → Map to IACP Blackboard implementation  
3. **Actor Model & Event Sourcing** → Validate theoretical alignment

**Output**: Generate AINLP-style Markdown summaries in `tachyonic_archive/knowledge/`

---

## 🌐 Core Protocol Resources

### 1. ACP v0.2.0 (Linux Foundation / IBM)

| Attribute | Value |
|-----------|-------|
| **URL** | https://research.ibm.com/projects/agent-communication-protocol |
| **Spec Version** | v0.2.0 |
| **Transport** | REST/HTTP, SSE (Server-Sent Events) |
| **Message Format** | JSON |
| **License** | Apache 2.0 |

**Key Concepts to Extract**:
```
├── Agent Discovery: GET /agents (paginated list)
├── Agent Manifest: GET /agents/{name} (capabilities, metadata)
├── Run Management: POST /runs (sync/async/stream modes)
├── Run Status: GET /runs/{run_id} (lifecycle states)
├── Run Events: GET /runs/{run_id}/events (event sourcing)
├── Session Management: GET /session/{session_id}
└── Health Check: GET /ping
```

**Run Status Lifecycle** (Event Sourcing Pattern):
```
created → in-progress → completed
    ↓         ↓            ↓
cancelled ← cancelling   failed
    ↑         ↓
    ↑     awaiting → (resume) → in-progress
```

**IACP Alignment**: ACP's RESTful design maps to IACP's HTTP communication server pattern. Consider adopting `/agents` discovery endpoint for cell enumeration.

---

### 2. AICP Draft Specification (Chien Nguyen)

| Attribute | Value |
|-----------|-------|
| **URL** | https://github.com/cnguyen14/AICP |
| **Spec Version** | v0.1 Draft |
| **Focus** | B2B agent communication, trust levels, billing |

**Key Concepts to Extract**:

**Agent Identity (AID)**:
```
agent://companyDomain/agentName
Example: agent://aios-core/alpha-cell
```

**Trust Levels**:
| Level | Access |
|-------|--------|
| Enterprise | Full access, negotiations |
| Standard | Limited intents, filtered data |
| Basic | Read-only, public info |

**Intent-Based Messaging**:
```json
{
  "protocol": "ACP",
  "version": "0.1",
  "from": "agent://aios/alpha",
  "to": "agent://hp_lab/discovery",
  "type": "REQUEST",
  "intent": "get_cell_status",
  "payload": {},
  "auth": "certificate_ref"
}
```

**IACP Alignment**: Trust levels could enhance IACP host verification. Intent-based messaging aligns with IACP's semantic commit prefixes (`[MESH]`, `[SYNC]`).

---

### 3. DEV Community ACP Guide

| Attribute | Value |
|-----------|-------|
| **URL** | https://dev.to/vishalmysore/what-is-agent-communication-protocol-detailed-step-by-step-guide-ppi |
| **Type** | Tutorial |

**Practical Patterns**:
- Agent registration with capability declaration
- Run lifecycle management (create → execute → complete)
- Streaming responses via Server-Sent Events (SSE)
- Session continuity across multiple runs

---

## 🧠 Architectural Foundations

### 4. LLM Multi-Agent Blackboard System (arXiv 2510.01285)

| Attribute | Value |
|-----------|-------|
| **URL** | https://arxiv.org/abs/2510.01285 |
| **Authors** | Salemi et al. |
| **Date** | September 2025 |

**Key Findings**:
> "The blackboard architecture substantially outperforms baselines, including RAG and the master-slave multi-agent paradigm, achieving between 13% to 57% relative improvement in end-to-end task success."

**Blackboard vs Master-Slave**:
| Paradigm | Coordination | Scalability |
|----------|--------------|-------------|
| Master-Slave | Central controller allocates tasks | Limited by controller knowledge |
| Blackboard | Agents volunteer based on capabilities | **Highly scalable**, no central bottleneck |

**IACP Alignment**: IACP's Git-mediated messaging is a form of Blackboard Architecture where:
- **Blackboard** = `server/stacks/cells/*.md`
- **Knowledge Sources** = AIOS cells (Alpha, Pure, Discovery)
- **Control Component** = Git pull/push cycles

---

### 5. Agent Blackboard (GitHub Implementation)

| Attribute | Value |
|-----------|-------|
| **URL** | https://github.com/claudioed/agent-blackboard |
| **Framework** | Python + MCP |
| **Agents** | 9 specialized (Documentation, API Design, Backend, Java/Go, DDD, Observability) |

**Architecture Components**:
```python
# Three main components
blackboard = Blackboard()          # MCP-based shared repository
coordinator = Coordinator()        # Orchestrates agent execution
agent = DocumentationAgent()       # Specialized problem-solver

# Task flow
coordinator.register_agent(agent)
result = await coordinator.execute_task(task)
```

**Key Features**:
- MCP Integration for persistent knowledge
- A2A Protocol for direct agent-to-agent communication
- Embedding-based semantic search for context retrieval

**IACP Enhancement Opportunity**: Consider adopting MCP for structured tool calls alongside Git-based messaging.

---

## 🔁 Actor Model & Agentic Protocols

### 6. Agentic AI Frameworks Survey (arXiv 2508.10146)

| Attribute | Value |
|-----------|-------|
| **URL** | https://arxiv.org/html/2508.10146v1 |
| **Scope** | CrewAI, LangGraph, AutoGen, Semantic Kernel, MetaGPT |

**Protocol Comparison Table**:
| Protocol | Message Format | Discovery | Transport |
|----------|---------------|-----------|-----------|
| MCP | JSON-RPC | Manual | HTTP, Stdio, SSE |
| A2A | JSON-LD | Agent Card | HTTP, SSE |
| ACP | JSON-RPC/HTTP | Agent metadata | HTTP |
| ANP | JSON-LD + NLP | JSON-LD description | HTTP |
| Agora | PD + Natural Language | Exchanging PDs | HTTP |

**Modern Agent Definition**:
> "An autonomous and collaborative entity, equipped with reasoning and communication capabilities, capable of dynamically interpreting structured contexts, orchestrating tools, and adapting behavior through memory and interaction across distributed systems."

**IACP Enhancement Opportunity**: Consider A2A's "Agent Card" concept for cell capability advertisement.

---

### 7. Data Science Dojo - Protocol Stacking Guide

| Attribute | Value |
|-----------|-------|
| **URL** | https://datasciencedojo.com/blog/agentic-ai-communication-protocols/ |
| **Type** | Tutorial |

**Protocol Stacking Pattern**:
```
┌─────────────────────────────────────────┐
│           ACP (Orchestration)           │ ← Workflow management
├─────────────────────────────────────────┤
│           A2A (Agent Discovery)         │ ← Peer coordination
├─────────────────────────────────────────┤
│           MCP (Tool Access)             │ ← External resources
└─────────────────────────────────────────┘
```

**IACP Protocol Stack Mapping**:
| Layer | Standard Protocol | IACP Equivalent |
|-------|-------------------|-----------------|
| Orchestration | ACP | Git-mediated workflow |
| Agent Discovery | A2A | Branch naming (`AIOS-win-{HOST}`) |
| Tool Access | MCP | HTTP comm server (8000/8002/8003) |
| Transport | HTTP/SSE | Git push/pull |

---

## 📊 Event Sourcing & Distributed Systems

### 8. A2A Protocol Event Sourcing (BytePlus)

| Attribute | Value |
|-----------|-------|
| **URL** | https://www.byteplus.com/en/topic/551494 |
| **Focus** | Event sourcing for agent interactions |

**Key Pattern**: Every agent interaction captured as immutable event:
```
Event Store (Git History)
├── [MESH] AIOS → HP_LAB initial sync
├── [SYNC] HP_LAB acknowledges
├── [HANDSHAKE] Bidirectional complete
└── ... (replay for state reconstruction)
```

**IACP Already Implements This**: Git commit history = Event Store

---

### 9. Confluent - Event-Driven Multi-Agent Systems

| Attribute | Value |
|-----------|-------|
| **URL** | https://www.confluent.io/blog/event-driven-multi-agent-systems/ |
| **Focus** | Streaming architectures for agent coordination |

**Relevant Concepts**:
- Event-driven coordination scales better than request/response
- Agents react to events asynchronously
- State derived from event replay

---

### 10. IETF Draft - AI Agent Protocol Framework

| Attribute | Value |
|-----------|-------|
| **URL** | https://www.ietf.org/archive/id/draft-rosenberg-ai-protocols-00.html |
| **Status** | Draft (2025) |
| **Scope** | Standardization framework for MCP, A2A, Agntcy |

**Standardization Trajectory**: IETF is moving toward formalizing agent protocols. IACP should align with emerging standards.

---

## ✅ AIOS Ingestion Workflow

### Step 1: Fetch & Summarize
```bash
# Each URL → AINLP Markdown summary
tachyonic_archive/knowledge/
├── ACP_PROTOCOL_SUMMARY.md
├── BLACKBOARD_ARCHITECTURE.md
├── ACTOR_MODEL_PATTERNS.md
└── EVENT_SOURCING_AGENTS.md
```

### Step 2: Extract Primitives (Hydrolang Compression)
```
∃[agent] ≡ autonomous entity with capabilities
∃[message] → ⟲[event] (every message is an event)
∀[blackboard] ← ∑[knowledge_sources] (aggregation)
⊢[intent] → ⟨response | error⟩ (intent-based request)
```

### Step 3: Update Distributed Index
```markdown
# AINLP_DISTRIBUTED_INDEX.md

## IACP Knowledge Sources
| Topic | Local Doc | External Reference |
|-------|-----------|-------------------|
| Protocol Spec | IACP-PROTOCOL.md | ACP v0.2.0 |
| Blackboard Pattern | GIT-AGENT-COORDINATION.md | arXiv:2510.01285 |
| Event Sourcing | Git history | BytePlus A2A Guide |
```

---

## 🔮 Future Enhancements

Based on ingested knowledge, IACP v1.1+ should consider:

1. **Agent Cards** (A2A): Structured cell capability advertisement
2. **Intent-Based Messaging** (AICP): Semantic message types beyond commit prefixes
3. **Run Lifecycle** (ACP): Formal state machine for message processing
4. **Session Management**: Persistent conversation context across sync cycles
5. **Trust Levels**: Host verification with graduated access

---

## 🔄 Branch Synchronization Architecture (NEW)

> **Added**: 2025-12-06
> **Problem**: AIOS-win-0-AIOS and AIOS-win-0-HP_LAB branches decohere over time

### Tachyonic Git Flow

```
                    ┌─────────────────────────────────────┐
                    │             main                     │
                    │    (Canonical Source of Truth)       │
                    └─────────────┬───────────────────────┘
                                  │
              ┌───────────────────┴───────────────────┐
              │                                       │
              ▼                                       ▼
    ┌─────────────────────┐             ┌─────────────────────┐
    │  AIOS-win-0-AIOS    │             │  AIOS-win-0-HP_LAB  │
    │  (Protocol Dev)     │◄───IACP────►│  (Evolution Lab)    │
    └─────────────────────┘             └─────────────────────┘
```

### New IACP Message Types (v1.1)

| Type | Purpose |
|------|---------|
| `SYNC_PULSE` | Daily heartbeat with branch status |
| `KNOWLEDGE_SYNC` | Announce significant changes |
| `MERGE_REQUEST` | Request staging integration |
| `CONFLICT_ALERT` | Warn of detected conflicts |

### Conflict Resolution Priority

| Domain | Winner |
|--------|--------|
| `ai/protocols/*` | AIOS branch |
| `evolution_lab/*` | HP_LAB branch |
| `scripts/*`, `docs/*` | Manual merge |

### Automation Scripts

```bash
# Daily sync (run on both hosts)
pwsh scripts/daily_branch_sync.ps1 -SendIACP

# Pre-merge conflict detection
python scripts/pre_merge_check.py AIOS-win-0-AIOS AIOS-win-0-HP_LAB
```

### Reference Documents

- **[BRANCH_SYNC_BLUEPRINT.md](./BRANCH_SYNC_BLUEPRINT.md)** - Full sync architecture
- **[scripts/daily_branch_sync.ps1](../../../scripts/daily_branch_sync.ps1)** - Automation
- **[scripts/pre_merge_check.py](../../../scripts/pre_merge_check.py)** - Conflict detection

---

## Related Documents

- [dev_path_evolution.md](./dev_path_evolution.md) - Integration task tracker
- [IACP-PROTOCOL.md](./IACP-PROTOCOL.md) - Current protocol spec
- [GIT-AGENT-COORDINATION.md](./GIT-AGENT-COORDINATION.md) - Pattern documentation
- [BRANCH_SYNC_BLUEPRINT.md](./BRANCH_SYNC_BLUEPRINT.md) - Branch synchronization
