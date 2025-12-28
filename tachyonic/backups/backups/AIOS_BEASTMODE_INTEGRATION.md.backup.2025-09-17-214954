# AIOS Beast Mode Integration (AINLP-aligned)

This document describes the selected distillation and refactorization to align Beast Mode 3.1 with AIOS core logic and AINLP paradigms.

## Goals
- Create an evolved, AIOS-compatible version of Beast Mode.
- Enable ingestion by AIOS while syncing with AINLP logic to ensure seamless integration.
- Preserve AIOS safety and orchestration patterns.

## Selected Distillation
- Retain autonomy and iterative tooling from Beast Mode.
- Replace blanket internet-research requirement with AIOS offline-first policy. External fetches only when necessary and explicitly approved.
- Map Beast Mode tools to AIOS workspace tasks and conventions.
- Enforce AINLP mock-mode continuity to avoid hard failures when native components are absent.

## Refactorization Approach
1. Introduce an instructions overlay at `.github/instructions/aios-beastmode-integration.md` to constrain behavior and align with AIOS.
2. Add an AIOS-specific mode file at `.vscode/aios.beastmode.chatmode.md` that references AIOS tasks and guardrails.
3. Use memory at `.github/instructions/memory.instruction.md` to store lightweight preferences.
4. Keep original Beast Mode sources under `C:\dev\projects\beastmode` as upstream reference; do not modify in place.
5. Future: migrate or mirror upstream updates selectively into `.vscode/aios.beastmode.chatmode.md`.

## Tooling Mapping
- runTasks → prefer existing tasks: build, build-ui, build-models, build-services, setup-cpp-build, build-cpp-core, python-install-deps, python-test-ai, publish, watch, clean, restore, start-mcp-server.
- runInTerminal → restricted; use for ad-hoc only when no task exists.
- fetch → allowed for shadcn/ui docs and explicit researcher-approved URLs.
- tests → use `python-test-ai` task and .NET build as tests proxy until unit tests expand.

## AINLP Synchronization
- Respect fractal orchestration; intercellular bridges must operate in mock mode if native components missing and must not break end-to-end flows.
- Synthesize minimal steps when required by tests; record success=false when degraded.

## Safety & Governance
- No automatic staging/committing.
- Summarize actions and checkpoint progress automatically.
- Do not touch secrets; avoid network calls unless requested.

## Next Steps
- Add the mode file to `.vscode/aios.beastmode.chatmode.md` (done in this change if present).
- Validate by running existing tasks in a dry flow.
- Iterate on warnings cleanup in .NET and CMake policy silencing within the mode’s workflow.
