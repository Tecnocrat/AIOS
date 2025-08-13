# AIOS Root Hygiene Policy

This policy defines what is allowed to live at the repository root and how automated guards enforce cleanliness.

## Objectives
- Keep the root cognitively light: only high‑signal, top‑level coordination artifacts.
- Prevent resurrection of deprecated / migrated scripts and ad‑hoc experiment debris.
- Provide deterministic, automatable checks (local + CI) contributing to coherence metrics (LFC/GPC).

## Allowed Root Artifacts (Whitelisted Categories)
1. Solution / workspace orchestration: `AIOS.sln`, `AIOS.code-workspace`
2. Governance & status meta: `AIOS_PROJECT_CONTEXT.md`, `CURRENT_STATUS.md`, strategic *_SUMMARY.md artifacts
3. Core coordination directories: `core/`, `interface/`, `ai/`, `runtime_intelligence/`, `scripts/`, `docs/`
4. Configuration baselines: `.editorconfig`, `.gitignore`, language linters, minimal env files (`environment.yml` if canonical)
5. Transitional upgrade manifests (must be referenced in CURRENT_STATUS) – expire or archive when complete.

## Explicitly Disallowed (Guarded)
- Any file listed in `governance/deprecated_files.ps1`
- Orphan setup or launcher scripts superseded by `scripts/`
- Legacy test probes superseded by structured test suites
- One‑off analysis notebooks or raw dumps (must go under `docs/analysis/` or archival hierarchy)

## Automation Layers
| Layer | Mechanism | Purpose |
|-------|-----------|---------|
| 1 | `governance/deprecated_files.ps1` | Single source of deprecated filenames |
| 2 | `scripts/root_clutter_guard.ps1` | Local / CI purge & log of forbidden files |
| 3 | `scripts/dev_terminal.ps1 -FinalizeHygiene` | Developer on‑demand cleanup + metrics recompute |
| 4 | `coherence-smoke` GitHub Action | Enforces LFC/GPC thresholds & zero deprecated presence |
| 5 | Pre‑commit hook (optional) | Prevent adds of forbidden files |

## Metrics Interaction
- LFC penalizes presence of any deprecated root file (resurrection penalty up to 0.3)
- GPC counts passing hygiene layers (currently guard, CI workflow presence, hook, inventory filter)

## Change Workflow
1. Propose addition of new root artifact → justify category
2. If approved, update this policy if category is novel
3. If deprecating an artifact, add its filename to `governance/deprecated_files.ps1`
4. Run `pwsh -File scripts/dev_terminal.ps1 -ReportCoherence -FinalizeHygiene` to validate

## Enforcement Log
- Purge events appended to `root_clutter_guard.log`
- Future: governance event stream (planned: `docs/unified_backups/tachyonic_operations/governance_events/`)

## Roadmap
- Implement mutation distance for structural drift signal
- Add signed attestation of hygiene pass (supply‑chain integrity)
- Auto‑generate weekly root inventory deltas

---
Maintained by the Governance subsystem. Update alongside any coherence scoring formula changes.
