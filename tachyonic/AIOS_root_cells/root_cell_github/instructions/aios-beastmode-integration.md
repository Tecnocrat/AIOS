---
applyTo: '**'
---

# AIOS Beast Mode Integration (AINLP-aligned)

Last updated: 2025-08-09

Purpose: Provide an AIOS-aligned, AINLP-synchronized variant of Beast Mode that preserves AIOS safety, orchestration, and polyglot build/test flows.

Key principles:
- Agent continues autonomously until done, but within AIOS safety protocols and PR-gated changes.
- Offline-first. Never exfiltrate secrets or make network calls unless explicitly requested by the user. Prefer local tools and docs.
- Align research: When UI work references shadcn/ui, always fetch docs from https://ui.shadcn.com/docs/components before codegen (see shadcn/ui instructions).
- Polyglot build/test tasks must use existing VS Code tasks in this workspace (see tasks.json and provided tasks from workspace). Prefer runTasks over ad-hoc shell.
- Respect AINLP paradigms: fractal orchestration, intercellular bridges, and mock-mode continuity when native components are missing.

Operational guardrails:
- Use the repo’s tasks: build, build-ui, build-models, build-services, setup-cpp-build, build-cpp-core, python-install-deps, python-test-ai, watch, clean, restore.
- Testing cadence: run Python tests after Python edits; run dotnet build for .NET changes; run CMake configure/build for C++ changes.
- Never stage/commit automatically. Only commit when the user explicitly asks.
- If long-running, checkpoint progress every 3–5 tool calls with a compact delta.

Beast Mode adaptations for AIOS:
- Research: default to local docs; when external research is necessary, summarize URLs and fetched takeaways; store any vendor-specific guidance as comments in modified files.
- AINLP synchronization: prefer mock-mode bridges if native components are absent; never hard-fail end-to-end flows—synthesize minimal steps and mark success=false when applicable.
- Memory: store lightweight preferences in .github/instructions/memory.instruction.md with front matter, no secrets.

Artifacts:
- Mode file: .vscode/aios.beastmode.chatmode.md
- Integration guide: docs/AIOS_BEASTMODE_INTEGRATION.md
- Instructions overlay (this file): .github/instructions/aios-beastmode-integration.md

