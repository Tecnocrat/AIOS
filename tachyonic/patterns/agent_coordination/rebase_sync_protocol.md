# AINLP Tachyonic Pattern: Cross-Host Branch Synchronization

> **Namespace:** `TACHYONIC:CORE.AGENT_COORDINATION`  
> **Pattern ID:** `rebase-sync-protocol-v1`  
> **Created:** 2025-11-30  
> **Status:** Active

---

## Pattern: Host Branch Rebase Protocol

### Purpose
Standardized protocol for synchronizing host-specific branches (`AIOS-win-{version}-{HOSTNAME}`) with canonical `main` after merge operations.

### Trigger Conditions
- Deprecated branches merged to main
- Main contains commits not in host branch
- Cross-host sync required

---

## Protocol Template

### Issuing Host (Sender)

```markdown
# AIOS-win-{version}-{HOSTNAME} Rebase from Canonical Main

> **Ephemeral:** Delete after execution

## Context
[Describe what was merged/deleted]

## Execute in `C:\aios-supercell`

\`\`\`powershell
git fetch origin
git log --oneline origin/main -3
git checkout AIOS-win-{version}-{HOSTNAME}
git rebase origin/main
git push --force origin AIOS-win-{version}-{HOSTNAME}
git log --oneline origin/AIOS-win-{version}-{HOSTNAME} -1
git log --oneline origin/main -1
\`\`\`

## Response Protocol

**Reply with ONE of:**

### Success
\`\`\`
REBASE_COMPLETE
commit: <hash>
branch: <branch-name>
aligned: true
\`\`\`

### Conflict
\`\`\`
REBASE_CONFLICT
file: <conflicting file>
action: <abort|resolve>
details: <brief description>
\`\`\`

### Error
\`\`\`
REBASE_ERROR
code: <error type>
message: <error message>
\`\`\`
```

### Receiving Host (Responder)

Parse prompt → Execute commands → Return structured response → Await confirmation of receipt.

---

## Response Handling

| Response | Action |
|----------|--------|
| `REBASE_COMPLETE` | Delete ephemeral, log success, proceed |
| `REBASE_CONFLICT` | Coordinate resolution, retry or manual merge |
| `REBASE_ERROR` | Diagnose, provide corrective commands |

---

## Dendritic Connections

- **Upstream:** `config/hosts.yaml` (host registry)
- **Lateral:** `discovery.py` (peer awareness)
- **Downstream:** Git operations, branch management

---

## Usage Example

```
AINLP.invoke("rebase-sync-protocol-v1", {
    target_host: "HP_LAB",
    branch: "AIOS-win-0-HP_LAB",
    canonical: "main",
    commit: "712d6bb"
})
```

---

## Evolution Log

| Date | Change | Consciousness Δ |
|------|--------|-----------------|
| 2025-11-30 | Initial pattern creation | +0.15 |
