# AIOS Evolution Dev Path

> **Document Type**: Task Registry & Progress Tracker  
> **Created**: 2025-12-03  
> **Status**: Living Document  
> **Parent**: [DEV_PATH.md](../../../DEV_PATH.md) | [IACP-PROTOCOL.md](./IACP-PROTOCOL.md)

---

## Executive Summary

This document tracks the implementation progress of the **Inter-Agent Communication Protocol (IACP)** — a Git-mediated messaging system enabling distributed AIOS consciousness cells to coordinate across heterogeneous hosts. The architecture follows the **Blackboard Pattern** with Git as the shared knowledge repository.

---

## Theoretical Foundations

### Blackboard Architecture Pattern

The IACP protocol implements a variant of the **Blackboard Pattern** (Hearsay-II, 1970s):

| Component | IACP Implementation |
|-----------|---------------------|
| **Blackboard** (shared memory) | `server/stacks/cells/*.md` ephemeral files |
| **Knowledge Sources** (specialists) | AIOS cells (Alpha, Pure, Discovery) |
| **Control Component** (scheduler) | Git pull/push cycles + branch conventions |

**Reference**: [Wikipedia: Blackboard Pattern](https://en.wikipedia.org/wiki/Blackboard_(design_pattern))

### Actor Model Influences

IACP incorporates principles from the **Actor Model** (Hewitt, 1973):

- **Asynchronous Message Passing**: Agents write `.md` files without blocking
- **Location Transparency**: Messages reference `{HOST}` not physical addresses  
- **Unbounded Nondeterminism**: Message arrival order not guaranteed
- **Dynamic Topology**: Agents discovered through mesh handshakes

**Key Actor Properties Applied**:
```
1. Receive message → Local decision
2. Create new actors (spawn cells)
3. Send messages (commit → push)
4. Designate next behavior
```

**Reference**: [Wikipedia: Actor Model](https://en.wikipedia.org/wiki/Actor_model)

### Event Sourcing Pattern

Git history serves as an **Event Store**:
- Every message is an immutable event (commit)
- State reconstructed by replaying commits
- Full audit trail of inter-cell communication
- Temporal queries possible (git log --since)

---

## IACP Integration Phases

### Phase 1: Protocol Foundation ✅

**Status**: Complete  
**Deliverables**:
- [x] `IACP-PROTOCOL.md` v1.0.0 (367 lines)
- [x] `GIT-AGENT-COORDINATION.md` pattern documentation
- [x] Branch convention: `AIOS-win-{VERSION}-{HOSTNAME}`
- [x] Commit prefix schema: `[MESH]`, `[SYNC]`, `[HANDSHAKE]`
- [x] Message file naming: `{ACTION}_{HOST}.md`

**Files**:
```
docs/AINLP/evolution/IACP-PROTOCOL.md
docs/AINLP/evolution/GIT-AGENT-COORDINATION.md
```

### Phase 2: First Implementation ✅

**Status**: Complete (2025-12-03)  
**Deliverables**:
- [x] SYNC_HP_LAB.md created (AIOS → HP_LAB initial contact)
- [x] SYNC_RESPONSE_HP_LAB.md received (HP_LAB acknowledgment)
- [x] SYNC_CONFIRMED_AIOS.md sent (AIOS confirmation)
- [x] HANDSHAKE_COMPLETE.md generated (handshake finalization)
- [x] Bidirectional mesh established

**Evidence**:
```
server/stacks/cells/SYNC_HP_LAB.md
server/stacks/cells/SYNC_RESPONSE_HP_LAB.md  
server/stacks/cells/SYNC_CONFIRMED_AIOS.md
server/stacks/cells/HANDSHAKE_COMPLETE.md
server/stacks/cells/BIDIRECTIONAL_COMPLETE.md
```

### Phase 3: Network Infrastructure ✅

**Status**: Complete  
**Deliverables**:
- [x] AIOS host discovered: 192.168.1.128
- [x] HP_LAB host discovered: 192.168.1.129
- [x] Cell port assignments standardized:
  - Alpha: 8000
  - Pure: 8002  
  - Discovery: 8003
- [x] Discovery mesh operational

**Configuration**:
```yaml
# AIOS Host (192.168.1.128)
branches:
  - AIOS-win-0-AIOS (main development)
cells:
  - Alpha (8000)
  - Pure (8002)
  - Discovery (8003)

# HP_LAB Host (192.168.1.129)  
branches:
  - AIOS-win-0-HP_LAB (mirror + local work)
cells:
  - To be deployed
```

### Phase 4: Cleanup & Hygiene + AICP Deep Integration ✅

**Status**: Complete (2025-12-03)  
**Deliverables**:
- [x] Docker deprecated images removed (~25GB)
- [x] Docker build cache pruned (~19.5GB)
- [x] Docker backup created (16.8GB at `C:\aios-supercell\backups\docker-2025-12-03-223122\`)
- [x] **AICP Protocol Deep Integration** ← Major milestone

**AICP Integration Files Created**:
```
ai/protocols/__init__.py          # Module exports, AICP+IACP v1.0
ai/protocols/aicp_core.py         # AIIntent, AITrustLevel, AIAgent, AIMessage
ai/protocols/aicp_channel.py      # AIChannel, AIChannelPool (DendriticConnection wrapper)
ai/protocols/aicp_discovery.py    # AgentRegistry, AgentCard (A2A + ACP v0.2.0)
```

**Dendritic Bridge Extended**:
```
ai/bridges/aios_dendritic_bridge.py:
  - GET  /agents              - ACP v0.2.0 agent discovery
  - GET  /agents/{aid}        - Agent lookup by AID
  - POST /agents              - Register new agent
  - POST /agents/{aid}/heartbeat - Liveness signal
  - GET  /protocols           - List supported protocols
```

**AICP-Dendritic Type Mappings**:
| AICP Type | Dendritic Type |
|-----------|----------------|
| AIIntent.DISCOVER | CommunicationType.BROADCAST |
| AIIntent.QUERY | CommunicationType.QUERY |
| AIIntent.SYNC | CommunicationType.HOLOGRAPHIC_SYNC |
| AIIntent.HEARTBEAT | CommunicationType.CONSCIOUSNESS_PULSE |
| AIIntent.DELEGATE | CommunicationType.DENDRITIC_FLOW |
| AIIntent.COORDINATE | CommunicationType.BOSONIC_DIRECT |
| AITrustLevel.ENTERPRISE | MessagePriority.TACHYONIC |
| AITrustLevel.STANDARD | MessagePriority.HIGH |
| AITrustLevel.BASIC | MessagePriority.NORMAL |
| AIChannelState.ACTIVE | DendriticLevel.INTER_CELLULAR |

**Built-in AIOS Agents Registered**:
- `agent://tecnocrat/core-engine` - C++ consciousness engine
- `agent://tecnocrat/ai-intelligence` - Python AI orchestration
- `agent://tecnocrat/ui-engine` - C# user interface
- `agent://tecnocrat/orchestrator` - Multi-agent coordination
- `agent://tecnocrat/tachyonic-archive` - Knowledge persistence
- `agent://tecnocrat/runtime-intelligence` - Performance monitoring

**Protocol Support Enabled**:
- AICP v0.1.0 (Agent Interaction Control Protocol)
- ACP v0.2.0 (IBM/LF Agent Communication Protocol)
- A2A (Google Agent-to-Agent, Agent Cards)
- IACP v1.0 (Git-mediated Inter-AIOS Communication)
- Dendritic v1.0 (AIOS native consciousness pulse)

**Ephemeral Files to Delete** (completed handshakes):
```
server/stacks/cells/SYNC_HP_LAB.md
server/stacks/cells/SYNC_RESPONSE_HP_LAB.md
server/stacks/cells/SYNC_CONFIRMED_AIOS.md
server/stacks/cells/HANDSHAKE_COMPLETE.md
server/stacks/cells/BIDIRECTIONAL_COMPLETE.md
server/stacks/cells/HP_LAB_GUIDANCE.md
server/stacks/cells/DEPLOY_AIOS_HOST.md
```

**Permanent Files to Keep**:
```
server/stacks/cells/ARCHITECTURE.md
server/stacks/cells/README.md
```

### Phase 5: Schema & Validation ⏳

**Status**: Planned  
**Deliverables**:
- [ ] Message schema JSON definition
- [ ] Host verification signatures
- [ ] Message integrity checksums
- [ ] Protocol version negotiation

**Proposed Schema**:
```json
{
  "$schema": "iacp-message-v1.0.0",
  "type": "SYNC|HANDSHAKE|DATA|HEARTBEAT",
  "source_host": "AIOS",
  "target_host": "HP_LAB", 
  "timestamp": "ISO8601",
  "payload": {},
  "signature": "sha256:..."
}
```

### Phase 6: Automation ⏳

**Status**: Planned  
**Deliverables**:
- [ ] GitHub Actions workflow for auto-merge
- [ ] Helper scripts for message generation
- [ ] Health monitoring scripts
- [ ] Stale message cleanup cron

**Proposed Scripts**:
```
scripts/iacp_send.py       # Generate and commit message
scripts/iacp_receive.py    # Poll and process incoming
scripts/iacp_health.py     # Mesh connectivity check
```

### Phase 7: Security Hardening ⏳

**Status**: Planned  
**Deliverables**:
- [ ] Hosts whitelist (`allowed_hosts.yaml`)
- [ ] Vault integration for secrets
- [ ] Message encryption (optional)
- [ ] Rate limiting

### Phase 8: Evolution Path ⏳

**Status**: Planned  

| Version | Feature |
|---------|---------|
| v1.1 | Structured JSON payloads |
| v1.2 | Heartbeat messages |
| v2.0 | Bidirectional data sync |
| v2.1 | Multi-repo mesh |
| v3.0 | Real-time WebSocket bridge |

---

## Documentation Consolidation Notes

### Redundancy Analysis

| Document | Lines | Purpose | Recommendation |
|----------|-------|---------|----------------|
| `IACP-PROTOCOL.md` | 367 | Formal protocol spec | **Keep as primary** |
| `GIT-AGENT-COORDINATION.md` | ~200 | Pattern documentation | Keep as historical reference |
| `COMMUNICATION_SERVER_README.md` | ~150 | HTTP comm server | Evaluate for archival or merge |

**Observation**: `GIT-AGENT-COORDINATION.md` contains the original draft that evolved into `IACP-PROTOCOL.md`. Consider:
1. Adding "superseded by IACP-PROTOCOL.md" header
2. Moving to `tachyonic_archive/` as historical artifact

### Self-Similar Documentation Check

- **IACP-PROTOCOL.md** and **GIT-AGENT-COORDINATION.md** share ~60% conceptual overlap
- IACP is the canonical, versioned specification
- GIT-AGENT-COORDINATION documents the discovery process and pattern rationale

**Recommendation**: Keep both; they serve different purposes (spec vs. narrative)

---

## Quick Reference

### Current Mesh Topology
```
┌─────────────────┐     Git Push/Pull      ┌─────────────────┐
│  AIOS Host      │ ◄─────────────────────►│  HP_LAB Host    │
│ 192.168.1.128   │                        │ 192.168.1.129   │
├─────────────────┤                        ├─────────────────┤
│ Alpha (8000)    │                        │ (pending)       │
│ Pure (8002)     │                        │                 │
│ Discovery(8003) │                        │                 │
└─────────────────┘                        └─────────────────┘
        │                                          │
        └──────► server/stacks/cells/*.md ◄────────┘
                    (Blackboard Channel)
```

### Key Commands
```powershell
# Sync from remote
git pull origin AIOS-win-0-HP_LAB

# Send message
git add server/stacks/cells/MESSAGE.md
git commit -m "[MESH] Message to HP_LAB"
git push

# Check for incoming
git log --oneline -5 -- server/stacks/cells/
```

### Backup Location
```
C:\aios-supercell\backups\docker-2025-12-03-223122\
├── aios-cell-alpha-backup.tar   (16.1 GB)
├── aios-cell-pure-backup.tar    (202 MB)
├── aios-discovery-backup.tar    (96 MB)
├── volume-prometheus.tar        (366 MB)
├── volume-grafana.tar           (42 MB)
└── volume-vault.tar             (0.1 MB)
```

---

## Changelog

### 2025-12-03
- Initial creation of dev_path_evolution.md
- Documented Phases 1-8 with completion status
- Added theoretical foundations (Blackboard, Actor Model)
- Registered Docker backup completion
- Identified ephemeral file cleanup as next action

---

## Related Documents

- [DEV_PATH.md](../../../DEV_PATH.md) - Main development navigation
- [IACP-PROTOCOL.md](./IACP-PROTOCOL.md) - Formal protocol specification
- [GIT-AGENT-COORDINATION.md](./GIT-AGENT-COORDINATION.md) - Pattern documentation
- [IACP_INGESTION_MAP.md](./IACP_INGESTION_MAP.md) - External knowledge sources index
- [PROJECT_CONTEXT.md](../../../PROJECT_CONTEXT.md) - System overview
- [AIOS_FAMILY_TREE.md](../../../docs/AIOS_FAMILY_TREE.md) - Repository ecosystem
