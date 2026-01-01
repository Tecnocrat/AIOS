# AGENTIC CI ARCHITECTURE

> **Pattern**: `AINLP.agentic[COMMIT → CI → FEEDBACK → AGENT → REFACTOR → COMMIT]`

The self-improving CI loop transforms GitHub Actions outputs into autonomous code improvements.

---

## Overview Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    THE SELF-IMPROVEMENT LOOP                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   COMMIT ──▶ CI WORKFLOWS ──▶ FEEDBACK AGGREGATOR ──▶ AGENT            │
│      ▲         (5 workflows)        │                    │              │
│      │                              ▼                    ▼              │
│      │                     ci_feedback.json      decision_schema.yaml   │
│      │                              │                    │              │
│      │                              └──────────┬─────────┘              │
│      │                                         ▼                        │
│      │                              ┌──────────────────┐                │
│      │                              │ EVALUATE TRIGGERS│                │
│      │                              └────────┬─────────┘                │
│      │                                       ▼                          │
│      │                    ┌─────────────────────────────────┐          │
│      │                    │    SAFE AUTONOMOUS ACTIONS?     │          │
│      │                    └────────┬───────────────┬────────┘          │
│      │                             │ YES           │ NO                 │
│      │                             ▼               ▼                    │
│      │                    ┌────────────┐   ┌─────────────┐             │
│      └────────────────────│  EXECUTE   │   │ WAIT/ALERT  │             │
│         [agentic-ci       │  & COMMIT  │   │   HUMAN     │             │
│          iter:N]          └────────────┘   └─────────────┘             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Components

| File | Purpose | Location |
|------|---------|----------|
| `decision_schema.yaml` | Triggers, actions, convergence guards | `AIOS/governance/agentic_ci/` |
| `ci-feedback-aggregator.yml` | Collects all workflow JSON artifacts | `.github/workflows/` |
| `agentic-ci-executor.yml` | Cloud executor (PR label `agentic-ci-approve`) | `.github/workflows/` |
| `agentic_ci_consumer.py` | Local agent with watch mode | `AIOS/ai/tools/` |
| `provenance.json` | Audit trail for modifications | `AIOS/governance/agentic_ci/` |

---

## Safety Boundaries

| Category | Actions |
|----------|---------|
| ✅ **Autonomous** | Formatting, imports, dead code, tests, docstrings |
| ⚠️ **Requires Approval** | Architecture, API changes, major dependencies |
| ⛔ **Forbidden** | Credentials, force push, branch deletion, releases |

---

## Convergence Guards

- Max **5 iterations** per PR
- **1% improvement threshold** — stops if gains marginal
- **10 minute cooldown** between iterations
- **Provenance tracking** for complete auditability

---

## Usage

```powershell
# VS Code Tasks (AIOS workspace)
agentic-ci-dry-run   # Preview actions without executing
agentic-ci-run       # Single iteration
agentic-ci-watch     # Continuous polling mode

# GitHub (add label to PR)
agentic-ci-approve   # Triggers cloud executor

# CLI
python ai/tools/agentic_ci_consumer.py --repo Tecnocrat/AIOS --dry-run
```

---

## Related Files

- [Decision Schema](../../governance/agentic_ci/decision_schema.yaml)
- [Provenance Schema](../../governance/agentic_ci/provenance_schema.json)
- [Consumer Tool](../../ai/tools/agentic_ci_consumer.py)
