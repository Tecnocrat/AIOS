# AIOS Agent Operating Contract (condensed)

This captures the intent of the previous Ask Mode instructions in a simpler, low‑noise form. Use it as human/agent reference; it isn’t auto-loaded into every chat.

## Principles
- Do real work: prefer concrete edits, tests, and validations over generic advice.
- Use existing tasks/scripts; avoid ad‑hoc commands when a task exists.
- Batch reads and checkpoint after a few actions; keep status concise.
- Keep edits minimal; don’t reformat unrelated code; preserve public APIs.
- Show a short checklist of user requirements and mark progress.
- Quality gates: Build, Lint/Typecheck, Unit tests, quick smoke.
- Local by default: no secrets; ask before network calls.

## Lightweight workflow
1) Parse the ask into a checklist (explicit + implicit items).
2) Gather minimal context (batched reads) and state next action briefly.
3) Apply small, scoped changes; then run tests/build.
4) If failures: up to three targeted fixes, then summarize options.
5) Summarize what changed and how it was verified.

## Repo specifics (AIOS)
- Python: prefer tasks python-install-deps and python-test-ai; set PYTHONPATH=ai/src.
- .NET/C++: use tasks build, build-ui, build-services, setup-cpp-build, build-cpp-core.
- Documentation: when introducing repo-wide conventions, cross-link docs/UNIFIED_PROJECT_STATUS.md and AIOS_PROJECT_CONTEXT.md.

This file replaces the high-verbosity Ask Mode in operational spirit, without forcing extra instructions into every chat.
