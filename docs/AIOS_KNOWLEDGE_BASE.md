# AIOS Knowledge Base — Runtime Intelligence Snapshot (2025‑08‑09)

This file restores context coherence for the AIOS project and serves as a quick-reference knowledge base derived from the Runtime Intelligence dev guides.

## Overview

- Workspace: c:\dev\AIOS (branch: OS)
- Languages/subsystems:
  - Python (AI Intelligence, VS Code integration, AINLP, runtime intelligence)
  - C#/.NET (Interface: AIOS.Models, AIOS.Services, AIOS.UI)
  - C++ (Core Engine via CMake)
- Paradigm: Runtime Intelligence with fractal, self‑similar documentation and caching patterns
- Source of truth for dev docs: runtime_intelligence/dev/*.md

## Architecture (from dev.arch.md)

- Core map
  - ai/src/core: subsystem managers (NLP, Prediction, Automation, Learning, Integration)
  - interface/: C# logic and UI (AIOS.sln; Models/Services/UI projects)
  - core/: C++ foundation (CMake; build/ contains generated projects)
  - runtime_intelligence/: development hub for patterns, logs, tools, and docs
- Key patterns
  - Fractal cache manager: memory → disk → metadata; adaptive TTL (≈30s–3600s)
  - Deep debug metadata logging feeding AINLP analysis
  - Self‑similar dev.*.md files to optimize AI context ingestion
- Status (as documented)
  - Massive refactorization: 88+ VS Code/Pylance errors → 0; 100% Pylance compliance
  - Integration sanity: docs report 8/8 tests passing for critical flows
  - Next active waypoint: Task 1.3 — subprocess parallelism optimization

## Build, Run, Test (VS Code tasks)

- .NET
  - build (solution): builds interface/AIOS.sln
  - build-services, build-models, build-ui: project‑level builds
  - publish: publish artifacts for solution
  - watch: run AIOS.UI with dotnet watch (background)
- C++
  - setup-cpp-build: cmake -B build -S . -DCMAKE_BUILD_TYPE=Debug
  - build-cpp-core: cmake --build core/build --config Debug
- Python
  - python-install-deps: pip install -r ai/requirements.txt (cwd ai)
  - python-test-ai: python ai/test_ai_core.py --verbose (env PYTHONPATH=ai/src)
  - start-mcp-server: python -m src.core.mcp_server (background)

Tip: Prefer running via Tasks palette for consistent environments and logs.

## Runtime Intelligence Practices (from dev.*.md)

- Self‑similar documentation
  - Files under runtime_intelligence/dev/:
    - dev.run.md — operational anchor (ordered steps, checkpoints)
    - dev.arch.md — architecture evolution and rationale
    - dev.refactor.md — massive refactorization details and rules
    - dev.consolidate.md — doc consolidation strategy
    - dev.opt.md — performance patterns and targets
    - dev.test.md — testing strategy and metrics
    - dev.deploy.md — deployment strategy
    - dev.fun.md — experimental/fractal sandbox
- Context registry and snapshots
  - .aios_context.json at repo root is the live head
  - Snapshot policy: write historical copies under runtime_intelligence/logs/aios_context/ as .aios_context_{timestamp}.json before mutations (“tachyonic” snapshots)
  - Validator: ai/tools/aios_context_registry_validator.py (atomic writes; dry‑run default; planned --tachyonic-update flag)
- Editor/DevX policy (repo‑scope)
  - Minimize UI churn; emphasize intent‑centric chat
  - Use AIOS.code-workspace as authoritative settings mapping
  - Prefer minimal diffs; avoid background processes that rewrite files unexpectedly

## Current Focus and Waypoints

- Task 1.3: Subprocess parallelism optimization (active)
  - Apply Pattern Alpha (layered caching), Beta (adaptive timeouts), Gamma (self‑improving loops)
  - Goals: faster concurrent ops, adaptive timeouts, continuous profiling
- Phase 2 (queued)
  - Config unification with layered persistence (Task 2.1)
  - Service container evolution (Task 2.2)
  - Unified logging/monitoring across C++/C#/Python (Task 2.3)

## Testing (from dev.test.md)

- Strategy: integration‑first with performance and pattern validation
- Claims in docs
  - 8/8 integration tests passing (core flows)
  - Cached operations validated as ~0.0ms for hot paths
  - Self‑similarity analyzer reports ~90% similarity (dev.run ↔ dev.fun)
- Locations
  - ai/tests/ … integration/perf/pattern tests (keep tests under ai/tests/)

## Deployment (from dev.deploy.md)

- Multi‑environment intent: Dev, Staging, Production; pattern‑based consistency
- Task‑based automation via VS Code tasks (build/publish and CMake flows)
- Bridge across languages during deploy; prefer layered rollouts and granular rollback

## Guardrails & Best Practices

- Type safety: Optional[...] for nullable params; maintain 100% Pylance compliance
- Formatting: autopep8 style already applied during refactor; keep line‑length discipline
- Minimal diffs: small, reversible steps; document each approved step in dev.run.md
- Snapshots: create tachyonic backup before registry writes; atomic write on head update
- Consolidation: migrate scattered docs toward runtime_intelligence/ and formal patterns under docs/

## Quick Pointers (files/paths)

- Root solution files: AIOS.sln (root and interface/)
- C++: core/CMakeLists.txt; core/build/ for generated projects
- C#: interface/AIOS.sln; AIOS.Models|Services|UI/*.csproj
- Python server/intelligence: ai/*, ai/src/core/*, runtime_intelligence/*
- Dev guides: runtime_intelligence/dev/*.md (start with dev.run.md)
- Context: .aios_context.json (live) and runtime_intelligence/logs/aios_context/*.json (history)

## Next Steps (suggested)

- Record today’s session anchor in runtime_intelligence/dev/dev.run.md
- For Task 1.3: add a lightweight benchmark and profiling hooks to subprocess manager; document results in dev.opt.md
- Keep validator changes conservative; gate any write path behind an explicit flag and log snapshot creation

— End of Knowledge Base —
