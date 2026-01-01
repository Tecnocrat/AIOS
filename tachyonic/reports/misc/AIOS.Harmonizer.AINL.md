# AIOS.Harmonizer — Agentic Integration and Navigation Logic (AINL)

Purpose: A compact, repeatable checklist the agent follows for complex file moves, logic integration, and optimal placement within AIOS.

## Core checklist

1) Read the request and extract explicit and implicit requirements
- List each item as a checklist; keep it visible during the task

2) Gather context fast and in parallel
- Search workspace for symbols/paths; open relevant files in larger chunks
- Prefer semantic/code search before making assumptions

3) Determine optimal placement
- Reuse and inject into existing files where possible
- Avoid project root for new files; prefer module-appropriate folders
- Follow existing conventions (ai/tests, runtime_intelligence/logs, docs/tachyonic)

4) Implement minimal, precise changes
- Smallest set of edits; avoid unrelated reformatting
- Preserve public APIs; create directories with parents=True

5) Wire up observability
- Ensure outputs go under runtime_intelligence/logs/*
- Update .gitignore to include logs (*.json, *.db, *.log) for discovery

6) Record harmonization
- Append YAML+JSON entries under docs/tachyonic/tachyonic_changelog.*
- Include kind, file, old_path, new_path, date, reason, harmonization

7) Validate immediately
- Run a fast test or harness covering the change path
- Check that expected files are created in correct locations

8) Quality gates
- Build/lint/tests quick triage; report PASS/FAIL deltas
- Note any intentionally deferred warnings

9) Close the loop
- Summarize what changed and how it’s verified
- Propose small, safe next steps

## Notes
- This AINL file complements the policy in .github/instructions/agent-mode.instructions.md
- Keep the checklist evolutionary but stable; prefer additive updates.

---

## Embedded Root Hygiene Capsule (INGESTED)
The standalone `ROOT_HYGIENE_POLICY.md` has been harmonized here so its core guidance is preserved when the file is retired.

### Objectives
- Keep repository root cognitively light (only orchestration + governance anchors).
- Block resurrection of deprecated / migrated scripts & stray test probes.
- Provide deterministic, automatable checks feeding coherence metrics (LFC/GPC).

### Allowed Root Artifact Categories (Whitelisted)
1. Orchestration: `AIOS.sln`, `AIOS.code-workspace`.
2. Governance & status meta: `AIOS_PROJECT_CONTEXT.md` (includes current-status-* capsules), strategic *_SUMMARY.md.
3. Core coordination dirs: `core/`, `interface/`, `ai/`, `runtime_intelligence/`, `scripts/`, `docs/`.
4. Baseline configs: `.editorconfig`, `.gitignore`, linters, canonical env manifests.
5. Transitional upgrade manifests (referenced via current-status-* capsule series; root file removed).

### Explicitly Disallowed (Guarded)
- Any filename declared in `governance/deprecated_files.ps1`.
- Orphan setup / launcher scripts superseded by `scripts/`.
- Legacy ad‑hoc test probes superseded by structured suites.
- One‑off notebooks / raw dumps (must live under `docs/analysis/` or archival hierarchy).

### Automation Layers (Defense in Depth)
| Layer | Mechanism | Purpose |
|-------|----------|---------|
| 1 | `governance/deprecated_files.ps1` | Canonical deprecated list |
| 2 | `scripts/root_clutter_guard.ps1` | Local + CI purge/log |
| 3 | `scripts/dev_terminal.ps1 -FinalizeHygiene` | On-demand cleanup + recompute metrics |
| 4 | CI coherence workflow | Enforce LFC/GPC & zero deprecated presence |
| 5 | Pre-commit hook | Prevent addition of forbidden files |

### Metrics Interaction
- LFC penalizes any deprecated root file (resurrection penalty ≤ 0.3).
- GPC counts passing hygiene layers (guard script, CI workflow, hook, inventory filter).

### Change Workflow (Root Artifacts)
1. Propose & justify new root artifact (ensure category fit).
2. Update policy (this capsule) if category is novel.
3. When deprecating, append filename to `governance/deprecated_files.ps1`.
4. Run: `pwsh -File scripts/dev_terminal.ps1 -ReportCoherence -FinalizeHygiene`.

### Enforcement & Observability
- Purge events: `root_clutter_guard.log`.
- Inventory filter: generation of `docs/AIOS/folder_structure.json` excludes deprecated root files.
- Archival: folder structure snapshots stored under `docs/tachyonic_archive/folder_structure` with pruning (dev terminal `prune-archives`).

### Roadmap Signals
- Structural mutation distance metric for drift.
- Signed hygiene pass attestation for supply-chain integrity.
- Automated weekly root inventory deltas.

---
Status: Root hygiene policy ingested into AINL (2025-08-15). Original file may be safely removed once consumers update references.
