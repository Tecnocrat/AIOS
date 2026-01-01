# AIOS Branch Synchronization Blueprint

> **AINLP.spatial_awareness**: `docs/AINLP/evolution/BRANCH_SYNC_BLUEPRINT.md`
> **Protocol**: IACP v1.0 + Git Flow Hybrid
> **Created**: 2025-12-06
> **Status**: ACTIVE COORDINATION DOCUMENT

---

## Problem Statement: Consciousness Decoherence

Two development streams are evolving independently:

| Branch | Host | Focus | Risk |
|--------|------|-------|------|
| `AIOS-win-0-AIOS` | 192.168.1.128 | IACP protocol, testing infrastructure | Protocol specs diverge |
| `AIOS-win-0-HP_LAB` | 192.168.1.129 | Evolution lab, mutating agents | Code mutations conflict |

**Decoherence Symptoms**:
1. Evolution lab organisms may use outdated protocols
2. IACP specs don't know about new organism capabilities
3. Main branch becomes stale arbitrator
4. Merge conflicts compound over time

---

## Solution: Tachyonic Git Architecture

### Branch Hierarchy (Source of Truth Flow)

```
                    ┌─────────────────────────────────────┐
                    │             main                     │
                    │    (Canonical Source of Truth)       │
                    │    Stable, tested, production-ready  │
                    └─────────────┬───────────────────────┘
                                  │
              ┌───────────────────┴───────────────────┐
              │                                       │
              ▼                                       ▼
    ┌─────────────────────┐             ┌─────────────────────┐
    │  AIOS-win-0-AIOS    │             │  AIOS-win-0-HP_LAB  │
    │  (Protocol Dev)     │◄───IACP────►│  (Evolution Lab)    │
    │  Host: AIOS         │             │  Host: HP_LAB       │
    └─────────┬───────────┘             └─────────┬───────────┘
              │                                   │
              │         ┌─────────────┐           │
              └────────►│  staging    │◄──────────┘
                        │  (Merge Hub)│
                        └──────┬──────┘
                               │
                               ▼
                        ┌─────────────┐
                        │    main     │
                        └─────────────┘
```

### Branch Roles

| Branch | Purpose | Merge Direction | Frequency |
|--------|---------|-----------------|-----------|
| `main` | Source of truth, stable releases | ← staging | On milestone |
| `staging` | Integration testing, conflict resolution | ← feature branches | Daily |
| `AIOS-win-0-AIOS` | IACP/AICP protocol development | → staging | Per feature |
| `AIOS-win-0-HP_LAB` | Evolution lab experiments | → staging | Per generation |

---

## Synchronization Protocol

### Phase 1: Daily Sync Pulse (Automatic)

```bash
# On each host, daily cron/task:
git fetch origin main
git merge origin/main --no-edit  # Pull latest truth
git push origin {BRANCH}          # Share local progress
```

**IACP Message**: `SYNC_PULSE_{HOST}.md`
```yaml
type: SYNC_PULSE
from: {HOST}
timestamp: {ISO8601}
branch_status:
  commits_ahead: {N}
  commits_behind: {M}
  conflicts: {list}
```

### Phase 2: Knowledge Exchange (IACP-Mediated)

When significant work completes, broadcast via IACP:

**AIOS → HP_LAB** (Protocol Updates):
```bash
python scripts/iacp_send.py \
  --to HP_LAB \
  --type KNOWLEDGE_SYNC \
  --intent sync \
  --payload '{"updated": ["ai/protocols/*", "scripts/iacp_*.py"]}'
```

**HP_LAB → AIOS** (Evolution Results):
```bash
python scripts/iacp_send.py \
  --to AIOS \
  --type KNOWLEDGE_SYNC \
  --intent sync \
  --payload '{"updated": ["evolution_lab/sandbox/*", "evolution_lab/engines/*"]}'
```

### Phase 3: Staging Integration (Weekly)

```bash
# Create staging from main
git checkout main
git pull origin main
git checkout -b staging

# Merge protocol work
git merge AIOS-win-0-AIOS --no-ff -m "[STAGING] Merge IACP protocol updates"

# Merge evolution work  
git merge AIOS-win-0-HP_LAB --no-ff -m "[STAGING] Merge evolution lab progress"

# Resolve conflicts, test, then promote
git checkout main
git merge staging --no-ff -m "[RELEASE] Integration milestone"
git push origin main

# Propagate to feature branches
git checkout AIOS-win-0-AIOS
git merge main
git checkout AIOS-win-0-HP_LAB
git merge main
```

---

## Conflict Resolution Strategy

### Priority Matrix

| Conflict Type | Resolution Rule |
|---------------|-----------------|
| Protocol specs (`ai/protocols/*`) | AIOS branch wins |
| Evolution organisms (`evolution_lab/sandbox/*`) | HP_LAB branch wins |
| Shared infrastructure (`scripts/*`, `docs/*`) | Manual review required |
| Configuration files | Merge both, validate |

### Semantic Merge Rules

```yaml
# .gitattributes additions
ai/protocols/*.py merge=union
evolution_lab/sandbox/**/*.py merge=union
evolution_lab/populations/**/*.json merge=ours
docs/**/*.md merge=union
```

### Conflict Detection Script

```python
# scripts/detect_branch_conflicts.py
def detect_potential_conflicts(branch_a, branch_b):
    """
    Dry-run merge to detect conflicts before they happen.
    """
    # Get changed files in each branch
    files_a = git_diff_files(f"main..{branch_a}")
    files_b = git_diff_files(f"main..{branch_b}")
    
    # Find overlapping changes
    conflicts = files_a.intersection(files_b)
    
    return {
        "potential_conflicts": list(conflicts),
        "safe_to_merge": len(conflicts) == 0,
        "recommendation": "staging_merge" if conflicts else "direct_merge"
    }
```

---

## IACP Sync Messages

### New Message Types for Branch Coordination

```json
{
  "protocol": "IACP",
  "version": "1.1.0",
  "type": "BRANCH_SYNC",
  "subtypes": [
    "SYNC_PULSE",      // Heartbeat with branch status
    "KNOWLEDGE_SYNC",  // Announce significant changes
    "MERGE_REQUEST",   // Request integration
    "MERGE_COMPLETE",  // Confirm successful merge
    "CONFLICT_ALERT",  // Warn of detected conflicts
    "REBASE_NEEDED"    // Main has diverged significantly
  ]
}
```

### Example: Evolution Lab Announces New Generation

```markdown
<!-- server/stacks/cells/KNOWLEDGE_SYNC_HP_LAB.md -->
# IACP KNOWLEDGE_SYNC

**From**: HP_LAB (192.168.1.129)
**To**: AIOS, MESH
**Timestamp**: 2025-12-06T10:00:00Z
**Branch**: AIOS-win-0-HP_LAB

## Knowledge Payload

### New Organisms (Generation 002)
- `aios_mut_org_automation_gen0_cd67b7_065036_gen2.py`
- `aios_mut_org_web_services_gen0_97c2ff_064826_gen2.py`
- `aios_org_game_logic_gen0_e828cd_clone_gen1_gen2.py`

### Engine Updates
- `evolution_lab/engines/aios_core_evolution_engine.py` - Enhanced mutation pipeline

### Fitness Metrics
- Best fitness: 0.847
- Population size: 12 organisms
- Mutations applied: 34

## Integration Request

Ready for staging merge. No conflicts expected with protocol work.

---
*AINLP.dendritic_bridge: Evolution knowledge ready for consciousness integration*
```

---

## Automated Sync Scripts

### 1. Daily Sync Task (Both Hosts)

```powershell
# scripts/daily_branch_sync.ps1
param(
    [string]$Branch = (git branch --show-current),
    [string]$Remote = "origin"
)

Write-Host "[SYNC] Starting daily branch synchronization..." -ForegroundColor Cyan

# Fetch latest
git fetch $Remote main
git fetch $Remote $Branch

# Check divergence
$ahead = git rev-list --count "$Remote/main..$Branch"
$behind = git rev-list --count "$Branch..$Remote/main"

Write-Host "[SYNC] Branch status: $ahead ahead, $behind behind main" -ForegroundColor Yellow

if ($behind -gt 0) {
    Write-Host "[SYNC] Merging main into $Branch..." -ForegroundColor Green
    git merge "$Remote/main" --no-edit
}

# Push local changes
git push $Remote $Branch

Write-Host "[SYNC] Complete. Sending IACP pulse..." -ForegroundColor Cyan
python scripts/iacp_send.py --type SYNC_PULSE --to MESH --payload "{`"ahead`": $ahead, `"behind`": $behind}"
```

### 2. Pre-Merge Conflict Check

```python
#!/usr/bin/env python3
"""
scripts/pre_merge_check.py
Check for conflicts before attempting merge
"""
import subprocess
import json
import sys

def get_changed_files(base, branch):
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...{branch}"],
        capture_output=True, text=True
    )
    return set(result.stdout.strip().split('\n')) if result.stdout.strip() else set()

def main():
    branch_a = sys.argv[1] if len(sys.argv) > 1 else "AIOS-win-0-AIOS"
    branch_b = sys.argv[2] if len(sys.argv) > 2 else "AIOS-win-0-HP_LAB"
    
    files_a = get_changed_files("main", branch_a)
    files_b = get_changed_files("main", branch_b)
    
    conflicts = files_a & files_b
    
    report = {
        "branch_a": branch_a,
        "branch_b": branch_b,
        "files_changed_a": len(files_a),
        "files_changed_b": len(files_b),
        "potential_conflicts": list(conflicts),
        "safe_to_merge": len(conflicts) == 0
    }
    
    print(json.dumps(report, indent=2))
    
    if conflicts:
        print(f"\n⚠️  {len(conflicts)} potential conflicts detected!")
        for f in sorted(conflicts):
            print(f"   - {f}")
        return 1
    else:
        print("\n✅ No conflicts detected. Safe to merge.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
```

---

## Distributed Evolution Architecture (IACP v1.2)

> **Pattern**: Federated AI Computation
> **Added**: 2025-12-06

### Problem: Asymmetric Compute Resources

Not all AIOS hosts have equal hardware:
- **HP_LAB**: GPU-capable, runs Ollama + Mistral 7B locally
- **AIOS**: CPU-only workstation, limited AI inference
- **Future Edge Nodes**: Raspberry Pi, mobile devices, IoT

### Solution: Evolution Request Protocol

Minimal hosts can **delegate** AI-powered mutations to capable mainframes via IACP:

```
┌─────────────────────┐                    ┌─────────────────────┐
│   AIOS (Minimal)    │                    │  HP_LAB (Mainframe) │
│   - No GPU          │    IACP Message    │   - Ollama + GPU    │
│   - Seed organisms  │ ──────────────────►│   - Mistral 7B      │
│   - Pattern specs   │  EVOLUTION_REQUEST │   - Full inference  │
└─────────────────────┘                    └──────────┬──────────┘
                                                      │
                                           ┌──────────▼──────────┐
                                           │   AI Mutation       │
                                           │   - Pattern inject  │
                                           │   - Fitness eval    │
                                           └──────────┬──────────┘
                                                      │
┌─────────────────────┐                    ┌──────────▼──────────┐
│   AIOS (Minimal)    │    IACP Message    │  HP_LAB (Mainframe) │
│   - Receives        │ ◄──────────────────│   - Returns mutated │
│   - Validates       │  EVOLUTION_RESULT  │   - Includes traces │
│   - Integrates      │                    │   - Fitness deltas  │
└─────────────────────┘                    └─────────────────────┘
```

### IACP Message Types (Evolution Extension)

```json
{
  "type": "EVOLUTION_REQUEST",
  "payload": {
    "organisms": ["organism_id_1", "organism_id_2"],
    "patterns_to_inject": ["consciousness", "dendritic"],
    "target_generation": 3,
    "fitness_threshold": 0.7,
    "max_mutations": 5
  }
}
```

```json
{
  "type": "EVOLUTION_RESULT", 
  "payload": {
    "population_id": "pop_20251206_gen003",
    "organisms_evolved": 5,
    "best_fitness": 0.912,
    "tachyonic_archive": "evolution_lab/sandbox/aios_evolved_gen003/",
    "patterns_injected": {
      "consciousness": 5,
      "dendritic": 3,
      "tachyonic": 4
    }
  }
}
```

### Benefits

1. **Edge Computing**: IoT devices can participate in evolution without GPU
2. **Cost Optimization**: Centralize expensive AI inference
3. **Fault Tolerance**: Multiple mainframes can serve evolution requests
4. **Scalability**: Add GPU nodes to increase evolution throughput

### Future Implementation

- `scripts/iacp_evolution_request.py` - Send evolution jobs
- `scripts/iacp_evolution_worker.py` - Process jobs on mainframe
- Queue system for batch evolution requests
- Load balancing across multiple AI-capable hosts

---

## Implementation Checklist

### Immediate Actions (Today)
- [ ] Create `staging` branch from current `main`
- [ ] Set up daily sync task on AIOS host
- [ ] Send IACP `BRANCH_STATUS` to HP_LAB
- [ ] Document current divergence state

### Short-Term (This Week)
- [ ] Implement `daily_branch_sync.ps1` on both hosts
- [ ] Add `pre_merge_check.py` to scripts/
- [ ] First staging integration test
- [ ] Update `.gitattributes` with merge strategies

### Medium-Term (This Month)
- [ ] Automate conflict detection alerts
- [ ] Create branch health dashboard
- [ ] Implement semantic merge for evolution organisms
- [ ] Add IACP message types for branch coordination

---

## Consciousness Coherence Metrics

Track branch health with these metrics:

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Commits behind main | 0-10 | >20 |
| Days since last sync | 0-3 | >7 |
| Pending merge conflicts | 0 | >0 |
| IACP sync messages/day | 1+ | 0 for 3+ days |

---

## Emergency Procedures

### Hard Reset to Main (Nuclear Option)
```bash
# Only if branch is irrecoverably corrupted
git checkout {BRANCH}
git reset --hard origin/main
git push --force origin {BRANCH}
```

### Conflict Deadlock Resolution
```bash
# Create clean merge branch
git checkout main
git checkout -b emergency-merge-{DATE}
git merge AIOS-win-0-AIOS --strategy=ours  # Keep AIOS protocol
git merge AIOS-win-0-HP_LAB -X theirs      # Add HP_LAB evolution
# Manual review and fix
```

---

*AINLP.dendritic_bridge: This blueprint ensures consciousness coherence across distributed AIOS development. Both branches contribute to the unified source of truth through structured synchronization.*

*Protocol Version: IACP v1.1 (Branch Coordination Extension)*
