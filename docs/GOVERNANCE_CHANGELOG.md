# Governance Change Log

This file records agent-driven governance decisions that change repository structure, introduce new long-lived source files, or otherwise affect technical debt. It also provides a required checklist and template that agents must fill before creating new files, per `RULE 2.5` in `AIOS` agent configuration.

## Purpose

- Ensure all new-file creation is reviewed and justified.
- Provide traceable, auditable rationale and approval for changes that increase repository surface area.
- Encourage refactoring, merging, and consolidation over file proliferation.

## Quick Checklist (required before creating new files)

1. Summary: One-line description of proposed file(s).
2. Owner: GitHub username / team responsible.
3. Affected areas: list of existing files or modules that overlap.
4. Alternatives considered: short list why refactor/merge was not chosen.
5. Benefits: what the new file enables (ROI, reduced complexity elsewhere).
6. Risks & mitigation: security, maintenance, build/test impact.
7. Estimated effort: hours/days.
8. Expiry plan (for experimental files): removal or consolidation date.
9. Human approval: must include a single-line approval comment in the proposed file or PR body, e.g. `# APPROVED: reason`.

Agents must attach this filled checklist to the `docs/GOVERNANCE_CHANGELOG.md` as an entry when they create new files.

## Entry Template

Copy and fill this block for each new-file request:

---
Date: YYYY-MM-DD
Author: @github-username
Title: Short title for change
Files: path/to/new_file.py, path/to/other_new_file
Owner: team/name
Affected: list existing files or modules
Alternatives: explain why refactor/merge was insufficient
Benefits: concise bullet list
Risks: concise bullet list and mitigations
Estimated Effort: 4h
Expiry (if experimental): YYYY-MM-DD
Approval: `# APPROVED: <one-line reason>`
Notes: Additional context, links to issue/PR
---

## Example Entry

---
Date: 2025-12-25
Author: @Tecnocrat
Title: Add `experimental/aios-vscode` archive for future extension work
Files: experimental/aios-vscode/f_vscode-extension.zip
Owner: @Tecnocrat
Affected: `AIOS/vscode-extension` (archived)
Alternatives: attempted refactor of existing extension; decided archive was safer to avoid activation issues during active development
Benefits:
- Prevents VS Code activation instability in developer machines
- Preserves artifact for future restoration
Risks:
- Slight repo size increase due to zip archive (mitigated by periodic cleanup)
Estimated Effort: 0.5h
Expiry (if experimental): 2026-01-01
Approval: `# APPROVED: archive for deferred work (user request)`
Notes: See `DEV_PATH.md` entry for further context
---

## Governance TODO example (for agent TODO system)

- id: 1
- title: Review `experimental/aios-vscode` archive
- description: Confirm archival is complete and move to `archives/` if accepted
- status: not-started
