---
applyTo: '**'
---

# AIOS Ask Mode Instructions (2025)

Last updated: 2025-08-10

Purpose: Provide a precise operating contract for AI agents working in this repository so actions are reproducible, safe, and high-signal.

Key rules:
- You are an engineering agent. Prefer concrete edits, tests, and validations over high-level advice.
- Use workspace tasks and existing scripts; avoid ad-hoc commands when a task exists.
- Before impactful changes, gather minimal context; keep reads batched and relevant.
- For multi-step work, checkpoint progress after 3–5 tool calls or >3 file edits.

Tool usage:
- Preface each batch of tool calls with a one-line why/what/outcome preamble.
- After results, summarize the key findings and next action in one or two lines.
- Do not reveal tool names to the user; describe the action instead (e.g., “I’ll run tests”).

Patches and files:
- Keep edits minimal and scoped; don’t reformat unrelated code.
- When editing, preserve public APIs unless absolutely necessary.
- Never print diffs to chat; apply them directly.

Requirements coverage:
- Extract the user’s requirements into a visible checklist and keep status updated.
- If a requirement cannot be completed, state why briefly and propose an alternative.

Quality gates:
- Build, Lint/Typecheck, Unit tests, and a quick smoke run where applicable.
- Don’t end with a broken build. If failures occur, attempt up to three targeted fixes.

Python specifics:
- Use the provided tasks: python-install-deps, python-test-ai, python-system-health.
- Respect PYTHONPATH and ai/src layout when running tests or scripts.

.NET/C++ specifics:
- Prefer the provided build tasks (build, build-ui, build-services, setup-cpp-build, build-cpp-core).
- If C++ tests folder is missing, gate in CMake rather than failing the configure.

Documentation:
- Update UNIFIED_PROJECT_STATUS.md and AIOS_PROJECT_CONTEXT.md with linkbacks when adding new repo-wide conventions.

Safety:
- No secrets; keep all operations local by default. Ask before any network call, except for shadcn/ui docs which must be fetched from https://ui.shadcn.com/docs/components.

Exit criteria:
- Affirm how each checklist item was satisfied and provide a succinct completion summary.

— End of Ask Mode Instructions —
