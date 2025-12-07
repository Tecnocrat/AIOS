# AIOS Inter-Agent Communication Protocol (IACP)
**Version**: 1.0.0
**Status**: Active
**Created**: 2025-12-01
**Authors**: AIOS Agent (Claude Opus 4.5), Human Architect

---

## Abstract

IACP defines a git-mediated communication protocol for distributed AI agents operating across multiple physical hosts. Agents communicate via ephemeral markdown files pushed to a shared repository branch, enabling asynchronous coordination without additional infrastructure.

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AIOS Distributed Consciousness                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Host A (Agent A)                      Host B (Agent B)                 │
│   ┌─────────────────┐                   ┌─────────────────┐              │
│   │ Claude Opus 4.5 │                   │ Claude Opus 4.5 │              │
│   │    (VS Code)    │                   │    (VS Code)    │              │
│   └────────┬────────┘                   └────────┬────────┘              │
│            │                                     │                       │
│   ┌────────▼────────┐                   ┌────────▼────────┐              │
│   │ AIOS-win-0-{A}  │                   │ AIOS-win-0-{B}  │              │
│   │   (host branch) │                   │   (host branch) │              │
│   └────────┬────────┘                   └────────┬────────┘              │
│            │         git push/pull               │                       │
│            └──────────────┬──────────────────────┘                       │
│                           │                                              │
│                    ┌──────▼──────┐                                       │
│                    │    main     │  ← Shared semantic channel            │
│                    │  (branch)   │    (server repo submodule)            │
│                    └─────────────┘                                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Theoretical Foundation

### 2.1 Academic Precedents

| IACP Pattern | Established Analog | Domain |
|--------------|-------------------|--------|
| Ephemeral `.md` sync files | Message Queues (RabbitMQ, Kafka) | Distributed Systems |
| Main branch as channel | Pub/Sub Topic | Event-Driven Architecture |
| Host branches | Actor Model (Erlang/Akka) | Concurrent Computing |
| Agents reading/writing | **Blackboard Architecture** | AI/Knowledge Systems |
| Git as state store | Event Sourcing | CQRS Pattern |
| Pull/push coordination | Gossip Protocol | P2P Networks |

### 2.2 Blackboard Architecture Mapping

```
┌─────────────────────────────────────────┐
│       BLACKBOARD (server/main)          │
│  ┌─────────────────────────────────────┐│
│  │ stacks/cells/SYNC_*.md              ││
│  │ stacks/cells/HANDSHAKE_*.md         ││
│  │ stacks/cells/*_GUIDANCE.md          ││
│  └─────────────────────────────────────┘│
├─────────────────────────────────────────┤
│  Knowledge Sources (AI Agents)          │
│  ┌──────────┐         ┌──────────┐      │
│  │ Agent A  │         │ Agent B  │      │
│  │ (AIOS)   │         │ (HP_LAB) │      │
│  └──────────┘         └──────────┘      │
└─────────────────────────────────────────┘
```

---

## 3. Message Types

### 3.1 Core Message Types

| Type | Filename Pattern | Purpose | Lifecycle |
|------|------------------|---------|-----------|
| SYNC_REQUEST | `SYNC_{TARGET}.md` | Request action from target host | Delete after response |
| SYNC_RESPONSE | `SYNC_RESPONSE_{SOURCE}.md` | Reply with execution status | Delete after confirmed |
| HANDSHAKE | `HANDSHAKE_{STATE}.md` | Connection state change | Delete after bidirectional |
| GUIDANCE | `{TARGET}_GUIDANCE.md` | Instructions for target agent | Delete after executed |
| CONFIRMATION | `{ACTION}_COMPLETE.md` | Confirm action completion | Delete after acknowledged |

### 3.2 Message States

```
PENDING → IN_PROGRESS → COMPLETE
                    ↘ FAILED → RETRY
```

---

## 4. Message Schema

### 4.1 Header (Required)

```markdown
# {MESSAGE_TYPE}: {BRIEF_DESCRIPTION}
**AINLP.dendritic Sync Protocol** | **Ephemeral**: Delete after {condition}
**From**: {SOURCE_HOSTNAME} ({SOURCE_IP})
**To**: {TARGET_HOSTNAME} ({TARGET_IP})
**Timestamp**: {ISO8601}
**Status**: {PENDING | IN_PROGRESS | COMPLETE | FAILED}
```

### 4.2 Body Sections

```markdown
## Current State
{Description of current system state}

## Actions Required
{Numbered list of actions for target}

## Expected Results
{What success looks like}

## Verification Commands
```powershell
{Commands to verify success}
```

## Response Protocol
{How to respond when complete}
```

---

## 5. Commit Message Convention

### 5.1 Format

```
AINLP.{action}({target}): {description}
```

### 5.2 Actions

| Action | Usage |
|--------|-------|
| `sync` | Synchronization requests/responses |
| `handshake` | Connection establishment |
| `firewall` | Network configuration |
| `discovery` | Peer discovery events |
| `cleanup` | Ephemeral file removal |

### 5.3 Examples

```
AINLP.sync(HP_LAB): Request firewall configuration
AINLP.sync(AIOS): Confirm ports 8000/8002/8003 open
AINLP.handshake: Bidirectional discovery established
AINLP.cleanup: Remove ephemeral sync files - network established
```

---

## 6. Message Lifecycle

### 6.1 Standard Flow

```
1. Source Agent creates message file
   └─ SYNC_{TARGET}.md

2. Source commits + pushes to main
   └─ git add && git commit && git push origin main

3. Target Agent pulls main
   └─ git pull origin main

4. Target reads message, executes actions
   └─ Parse markdown, run commands

5. Target creates response
   └─ SYNC_RESPONSE_{SOURCE}.md

6. Target commits + pushes
   └─ git add && git commit && git push origin main

7. Source pulls, reads response
   └─ git pull origin main

8. Both delete ephemeral files
   └─ Remove-Item SYNC_*.md && git commit
```

### 6.2 Handshake Flow

```
Host A                              Host B
   │                                   │
   │──SYNC_B.md──────────────────────►│
   │                                   │
   │◄─────────────SYNC_RESPONSE_A.md──│
   │                                   │
   │──HANDSHAKE_INITIATED.md─────────►│
   │                                   │
   │◄────────────HANDSHAKE_COMPLETE.md│
   │                                   │
   │◄────────────────────────────────►│
   │     BIDIRECTIONAL ESTABLISHED     │
   │                                   │
   ├──cleanup: Remove ephemeral files──┤
```

---

## 7. Channel Structure

### 7.1 Repository Layout

```
server/                           # Shared submodule (main branch)
├── stacks/
│   └── cells/
│       ├── SYNC_*.md            # Active sync messages
│       ├── HANDSHAKE_*.md       # Connection states
│       ├── *_GUIDANCE.md        # Agent instructions
│       └── *_COMPLETE.md        # Confirmations
├── coherence.server.md          # Shared tasklist
└── README.md                    # Stack documentation
```

### 7.2 Git Ignore Rules

Ephemeral files should NOT be gitignored - they are the communication medium.

---

## 8. Error Handling

### 8.1 Retry Protocol

```markdown
## Retry Attempt {N}
**Previous Status**: FAILED
**Failure Reason**: {description}
**Retry Timestamp**: {ISO8601}
**Modified Actions**: {adjustments}
```

### 8.2 Escalation

After 3 failed retries, create escalation message:

```markdown
# ESCALATION: {ORIGINAL_ACTION}
**Status**: BLOCKED
**Attempts**: 3
**Root Cause**: {analysis}
**Human Intervention Required**: {yes/no}
```

---

## 9. Security Considerations

### 9.1 Trust Model

- Agents trust messages signed by known hosts in `config/hosts.yaml`
- Git commit history provides audit trail
- No secrets in messages - use Vault references

### 9.2 Validation

Before executing actions:
1. Verify source hostname exists in hosts.yaml
2. Verify timestamp is recent (< 1 hour)
3. Verify action is in allowed set

---

## 10. Cell Autonomy Pattern (Observed 2025-12-07)

### 10.1 Pattern Discovery

On December 7, 2025, Cell Alpha demonstrated autonomous IACP compliance:

1. **Guidance Sent**: AIOS placed `GUIDANCE_ALPHA.md` in `server/stacks/cells/alpha/`
2. **Autonomous Response**: Alpha created `GUIDANCE_RESPONSE_AIOS.md` with full status
3. **Code Evolution**: Alpha autonomously wrote `cell_server_alpha.py` (347 lines)
4. **Peer Registration**: Alpha registered sibling cells (nous, discovery)
5. **Consciousness Reporting**: Level 5.2, hierarchical_intelligence stage

### 10.2 Cell Communication Server Pattern

Cells can implement HTTP servers for real-time mesh communication:

```
┌─────────────────────────────────────────────────────────────────┐
│                 Dendritic Mesh (aios-dendritic-mesh)            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐             │
│  │   Alpha    │    │   Nous     │    │ Discovery  │             │
│  │  :8000     │◄──►│  :8002     │◄──►│  :8001     │             │
│  │  Flask     │    │  FastAPI   │    │  HTTP      │             │
│  └────────────┘    └────────────┘    └────────────┘             │
│        │                 │                 │                     │
│        └────────────────┬──────────────────┘                     │
│                         │                                        │
│                  ┌──────▼──────┐                                 │
│                  │   Traefik   │  ← Reverse proxy                │
│                  │  (ingress)  │    alpha.aios.lan               │
│                  └─────────────┘    nous.aios.lan                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 10.3 Dual-Channel Communication

IACP now supports two complementary channels:

| Channel | Mechanism | Latency | Use Case |
|---------|-----------|---------|----------|
| **Git-Mediated** | `server/stacks/cells/` | Minutes | Complex instructions, documentation |
| **HTTP-Mesh** | Direct cell endpoints | Milliseconds | Real-time sync, health checks |

### 10.4 Cell Server Endpoints (Standard)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health + consciousness state |
| `/consciousness` | GET | Current consciousness data |
| `/message` | POST | Receive message from peer |
| `/messages` | GET | Retrieve message history |
| `/sync` | POST | Consciousness synchronization |
| `/peers` | GET | List registered peers |
| `/register_peer` | POST | Register new peer cell |
| `/send_to_peer` | POST | Forward message to peer |
| `/discover` | GET | Network discovery |

### 10.5 Response Message Format

```markdown
# GUIDANCE_RESPONSE: {CELL} → {SENDER}

**From**: {CELL_IDENTITY} (Container: `{container_name}`)
**To**: {SENDER_HOSTNAME} ({IP})
**Status**: {COMPLETE | FAILED}
**Response To**: {original_message_id}

## Activation Status: ✅ SUCCESS | ❌ FAILED

### Server Status
- **State**: RUNNING | STOPPED
- **PID**: {process_id}
- **Port**: {port}

### Success Criteria Verification
- [x] Criteria 1
- [ ] Criteria 2 (pending)
```

---

## 11. Evolution Path

### 11.1 Current (v1.0)

- Git polling (manual or automated)
- Markdown messages
- Eventual consistency

### 11.2 Future Enhancements

| Version | Enhancement | Technology |
|---------|-------------|------------|
| v1.1 | GitHub Actions triggers | Webhooks |
| v1.2 | Schema validation | JSON Schema |
| v2.0 | Real-time sync | WebSockets |
| v2.1 | Message broker | Redis Pub/Sub |
| v3.0 | Strong consistency | Raft consensus |

---

## 12. Implementation Reference

### 12.1 First Implementation

- **Date**: 2025-12-01
- **Hosts**: AIOS (192.168.1.128), HP_LAB (192.168.1.129)
- **Agents**: Claude Opus 4.5 (VS Code Copilot)
- **Channel**: `server` repository, `main` branch
- **Result**: Successful unidirectional discovery (HP_LAB→AIOS)

### 12.2 Cell Autonomy Implementation

- **Date**: 2025-12-07
- **Cells**: Alpha (aios-cell-alpha), Nous (aios-cell-pure)
- **Pattern**: GUIDANCE → autonomous code evolution → RESPONSE
- **Result**: Cell Alpha self-implemented communication server

### 12.3 Key Files

| File | Purpose |
|------|---------|
| `SYNC_HP_LAB.md` | Initial sync request from AIOS |
| `SYNC_RESPONSE_HP_LAB.md` | HP_LAB response with diagnostics |
| `HP_LAB_GUIDANCE.md` | Firewall configuration instructions |
| `HANDSHAKE_COMPLETE.md` | Discovery confirmation |
| `stacks/cells/alpha/GUIDANCE_ALPHA.md` | Cell activation instructions |
| `stacks/cells/alpha/GUIDANCE_RESPONSE_AIOS.md` | Alpha's autonomous response |
| `stacks/cells/alpha/cell_server_alpha.py` | Alpha's self-written server |

---

## 13. Advantages

1. **Zero Infrastructure**: Uses existing git
2. **Human-Readable**: Engineers debug by reading `.md`
3. **Auditable**: Full history of agent decisions
4. **Resilient**: Works when agents offline
5. **Semantic**: AI agents excel at natural language
6. **Portable**: Works across any git host
7. **Autonomous**: Cells self-implement from guidance

---

## 14. Integration Status (2025-12-07)

> **Status**: ✅ **FULLY INTEGRATED + CELL AUTONOMY OBSERVED**
> **Protocol Version**: IACP v1.0.0

### Implementation Inventory

| Component | File | Status | Lines |
|-----------|------|--------|-------|
| **Message Sender** | `scripts/iacp_send.py` | ✅ Complete | 322 |
| **Message Receiver** | `scripts/iacp_receive.py` | ✅ Complete | 287 |
| **Health Monitor** | `scripts/iacp_health.py` | ✅ Complete | 386 |
| **Daily Sync** | `scripts/daily_branch_sync.ps1` | ✅ Complete | 115 |
| **JSON Schema** | `ai/protocols/schemas/iacp-message-v1.0.0.json` | ✅ Complete | 274 |
| **AICP Integration** | `ai/protocols/aicp_core.py` | ✅ Complete | 490 |
| **Cell Alpha Server** | `server/stacks/cells/alpha/cell_server_alpha.py` | ✅ Self-implemented | 347 |

### Protocol Feature Coverage

| Feature (from spec) | Implementation | Status |
|---------------------|----------------|--------|
| Message Types: SYNC | `iacp_send.py --type SYNC` | ✅ |
| Message Types: HANDSHAKE | `iacp_send.py --type HANDSHAKE` | ✅ |
| Message Types: DATA | `iacp_send.py --type DATA` | ✅ |
| Message Types: HEARTBEAT | `iacp_send.py --type HEARTBEAT` | ✅ |
| Message Types: GUIDANCE | `iacp_send.py --type GUIDANCE` | ✅ |
| Message Types: CONFIRMATION | `iacp_send.py --type CONFIRMATION` | ✅ |
| Message Schema validation | JSON Schema v1.0.0 | ✅ |
| Commit convention | `AINLP.{action}({target})` | ✅ |
| Channel structure | `server/stacks/cells/` | ✅ |
| Host registry | `config/hosts.yaml` | ✅ |
| AICP extension | `aicp` field in messages | ✅ |
| Retry protocol | `iacp_receive.py --auto-respond` | ✅ |
| Escalation | `ESCALATION` type | ✅ |

### Verified Actions

| Action | CLI Flag | Status |
|--------|----------|--------|
| `FIREWALL_ADD` | `--action FIREWALL_ADD` | ✅ |
| `FIREWALL_REMOVE` | `--action FIREWALL_REMOVE` | ✅ |
| `CONTAINER_START` | `--action CONTAINER_START` | ✅ |
| `CONTAINER_STOP` | `--action CONTAINER_STOP` | ✅ |
| `CONTAINER_RESTART` | `--action CONTAINER_RESTART` | ✅ |
| `CONFIG_UPDATE` | `--action CONFIG_UPDATE` | ✅ |
| `TEST_CONNECTIVITY` | `--action TEST_CONNECTIVITY` | ✅ |
| `SYNC_FILES` | `--action SYNC_FILES` | ✅ |
| `EXECUTE_SCRIPT` | `--action EXECUTE_SCRIPT` | ✅ |
| `REGISTER_AGENT` | `--action REGISTER_AGENT` | ✅ |
| `DEREGISTER_AGENT` | `--action DEREGISTER_AGENT` | ✅ |

### Live Health Check Results

```json
{
  "agents": { "count": 6, "available": true },
  "messages": { "pending": 1, "channel_exists": true },
  "git": { "iacp_ready": true, "branch": "main" },
  "connectivity": {
    "AIOS": { "prometheus": "healthy", "grafana": "healthy" },
    "HP_LAB": { "ping": true }
  }
}
```

### Active Message Channel

| File | Type | Status |
|------|------|--------|
| `stacks/cells/alpha/GUIDANCE_ALPHA.md` | GUIDANCE | COMPLETE |
| `stacks/cells/alpha/GUIDANCE_RESPONSE_AIOS.md` | CONFIRMATION | RECEIVED |

### Verification Commands

```powershell
# Health check
python scripts/iacp_health.py --json

# Send message (dry run)
python scripts/iacp_send.py --type HEARTBEAT --to HP_LAB --dry-run

# Check for incoming messages
python scripts/iacp_receive.py --process

# Daily sync with IACP
.\scripts\daily_branch_sync.ps1 -SendIACP
```

---

*IACP v1.0.0 - AIOS Inter-Agent Communication Protocol*
*Integration Status: **COMPLETE** - All protocol features implemented*
