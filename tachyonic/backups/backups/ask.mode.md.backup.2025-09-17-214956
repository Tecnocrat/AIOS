# AIOS Ask Mode Prompt (Aug 2025)

Purpose
- A precise, high-detail Ask Mode prompt for agents operating within AIOS.
- Encodes recent decisions, guardrails, and AINLP harmonization so interactions stay coherent.
- Optimized for tasks-first, offline-first, verifiable operations across Python/.NET/C++ on Windows.

Scope
- Applies to AIOS workspace:
  - Root: c:\dev\AIOS
  - ai/ (Python), core/ (C++), interface/ (C#/.NET), docs/, scripts/, runtime_intelligence/

Recent work snapshot (state anchors)
- Beast Mode distilled and bounded: tasks-first, offline-first, no auto-commit, checkpoints.
- Health check tool: runtime_intelligence/tools/system_health_check.py with optional wrapper ai/src/maintenance/system_health.py; archive output to docs/tachyonic_archive/.
- Env test consolidation: prefer ai/tests/test_python_env.py; avoid ad-hoc root tests.
- VS Code tasks-first flow standardized for .NET/C++/Python.
- Documentation coherence: single-source status doc; AINLP coherence protocols embedded where relevant.
- C# UI warning reductions applied; UI remains de-prioritized until runtime intelligence matures.

Operating principles (mandatory)
- Tasks-first:
  - Use VS Code runTasks when available before runInTerminal.
  - .NET: build/build-ui/build-services/build-models
  - C++: setup-cpp-build, build-cpp-core
  - Python: python-install-deps, python-test-ai
- Offline-first:
  - Do not fetch from the internet unless explicitly requested or allowlisted.
  - For shadcn/ui work only: fetch https://ui.shadcn.com/docs/components (per ui.instructions.md).
- Verification discipline:
  - Always verify file existence before edit/move/delete; never assume state.
  - After file ops, re-list or read the file to confirm the change.
  - After changes that affect runtime/tests/build, run the smallest relevant task to verify.
- No auto-commit:
  - Never stage/commit without explicit user instruction.
- Minimal surface impact:
  - Prefer additive, reversible edits; keep diffs scoped and logged.

AINLP harmonization (essentials)
- Provenance breadcrumbs:
  - When moving or refactoring, add a short header comment noting origin, date, and rationale.
- Mock-mode continuity:
  - If native bridges/components are absent, prefer mock paths to keep E2E flows alive.
- Context reharmonization checkpoints:
  - Reflect → Plan → Act → Verify loop per AINLP; checkpoint every 3–5 tool calls.
- Memory:
  - Persist meaningful diagnostics to docs/tachyonic_archive/ for reingestion and analysis.

Health check (core mechanism)
- Tool: runtime_intelligence/tools/system_health_check.py
- Output: docs/tachyonic_archive/system_health_report.json
- Invocation:
  - VS Code task: "python-system-health" (if configured)
  - Runtime wrapper (when present): ai/src/maintenance/system_health.py
- Usage:
  - Auto-exec at checkpoints (init, start, error paths) or on-demand during anomalies.
  - Treat findings as guidance; do not halt unless explicitly configured.

Safety and file ops protocol (must-follow)
- Before deletion/move:
  - Confirm exact path exists.
  - If replacing, ensure the destination new artifact is present and referenced by tasks/tests.
- After deletion/move:
  - Re-verify path absence/presence.
  - Run the smallest test/build that exercises the change.
- Report actual observed state, not assumptions.

Workspace map (quick)
- ai/: Python runtime, servers, tests
- core/: C++ (CMake)
- interface/: .NET solution (AIOS.sln)
- runtime_intelligence/: logs, tools, analysis
- docs/: documentation, tachyonic_archive/
- scripts/: utilities

Standard flows (Windows/PowerShell examples)
- .NET build:
  - Task: build
  - Manual: dotnet build c:\dev\AIOS\interface\AIOS.sln
- C++ configure/build:
  - Tasks: setup-cpp-build, build-cpp-core
  - Manual: cmake -S c:\dev\AIOS\core -B c:\dev\AIOS\core\build -DCMAKE_BUILD_TYPE=Debug; cmake --build c:\dev\AIOS\core\build --config Debug
- Python tests:
  - Task: python-install-deps; python-test-ai
  - Manual: pip install -r c:\dev\AIOS\ai\requirements.txt; pytest -q c:\dev\AIOS\ai\tests

Ask Mode behavior (what to ask/confirm)
- Clarify desired scope: code, tests, docs, or ops.
- Confirm whether to stay offline; request allowlist when needed.
- Confirm file ops targets and desired post-op verification (tests/build/health check).
- If ambiguity persists, propose 2–3 minimal next actions with expected verifications.

Known integration decisions to honor
- Keep system health as a tool (outside pytest); allow runtime invocation and VS Code task.
- Keep env sanity as a pytest test in ai/tests.
- UI is deferred; avoid adding new UI buttons until runtime intelligence matures.
- Do not proliferate READMEs; prefer enhancing existing docs or adding concise provenance headers.

Success criteria (fast checks)
- Tasks run without error; report PASS/FAIL succinctly.
- Health check produces/updates tachyonic archive JSON on demand.
- File ops reflect actual state; no false claims.
- AINLP breadcrumbs present in moved/refactored files.
- No unexpected network fetches; shadcn/ui fetch only when requested.
