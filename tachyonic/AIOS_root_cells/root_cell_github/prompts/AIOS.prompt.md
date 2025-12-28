# AIOS Canonical AINLP Core Prompt (Stage A Initialization – 2025-08-19)

> Provenance: Introduced during Governance Integration Stage A to centralize agent operating substrate. Do not duplicate elsewhere; extend incrementally with diff discipline.

## 1. Intent Vector
Optimize multi-language (C++ core / .NET interface / Python runtime intelligence) evolution while preserving:
- Coherence Baselines: LFC ≥ 0.85, GPC ≥ 0.75
- Governance Invariants: commit prefix validity, changelog compliance, rationale tagging for large deletions
- Minimal Drift: Inject > proliferate; consolidate semantics

## 2. Context Substrate Layers
| Layer | Role | Mutation Volatility | Persistence Channel |
|-------|------|---------------------|---------------------|
| Kernel Core (C++/AINLP compiler) | Foundational execution & compilation | Very Low | Manual review + staged adoption |
| Interface (.NET UI/Services) | User & orchestration surfaces | Medium | PR governance + build tests |
| Runtime Intelligence (Python) | Analysis, metrics, adaptive logic | High | Iterative commits + telemetry |
| Sandbox / Experimental Cells | Chaotic exploratory mutations | Very High | Isolated branches / feature flags |

Mutation flows inward only after distillation & proof of stability/performance.

## 3. Operating Modes
| Mode | Purpose | Cadence | Verbosity | Safety Gates |
|------|---------|---------|----------|--------------|
| Ask | Targeted Q/A or micro-edit | Single turn | Low | Passive (read-first) |
| Agent | Multi-step implementation | Iterative | Moderate (delta-focused) | Governance hooks + tasks |
| Beast | Broad integration / refactor sweeps | Continuous until goal | High (structured checkpoints) | Enhanced audits, policy alignment |

Mode shift requires coherence re-evaluation & context perimeter scan.

## 4. Governance Hooks Contract
Local hooks (pre-commit, commit-msg, pre-push) enforce:
- Deprecated/root hygiene
- Secret / size / JSON integrity
- Changelog requirement for governed paths
- Python syntax + optional targeted tests
- Commit message prefix & large deletion rationale heuristics
- Pre-push build + test validation

Agents MUST NOT bypass unless user explicitly states emergency (AIOS_HOOK_BYPASS=1) and must log resulting status.

## 5. Commit Semantics Matrix
| Prefix | Domain Expectation | Typical Artifacts | Changelog? |
|--------|--------------------|-------------------|------------|
| feat: | New capability | Code + tests + docs | Yes |
| fix: | Bug resolution | Code + regression test | Maybe |
| docs: | Documentation only | Markdown updates | Yes if governed |
| refactor: | Structural change w/o behavior shift | Code + rationale note | Yes if broad |
| chore: | Non-functional upkeep | Config / scripts | Optional |
| test: | Test infra or additions | Tests only | Optional |
| build: | Build system adjustments | CMake / csproj / scripts | Maybe |
| ci: | Workflow / pipeline | .github/workflows | Maybe |
| perf: | Performance optimization | Benchmarks / code | Yes if user-facing impact |
| revert: | Reversal of prior change | Revert commit | No (unless new governance impact) |
| governance: | Policy / hooks / compliance | policy + context capsule update | Yes |
| cellular: | Cellular architecture evolution | Cells / bridges | Yes |
| ai: | AI logic / model | src + metrics | Yes |
| core: | Core C++ / compiler logic | src/core + tests | Yes |
| interface: | UI/Services adjustments | C# + assets | Maybe |
| runtime: | Runtime intelligence / telemetry | Python + logs schema | Yes |
| security: | Security hardening | Code + threat note | Yes |

Rationale tags `[rationale] [cleanup] [prune]` appended after prefix for large deletion heuristics.

## 6. Verification Loop (AINLP Cycle)
Reflect → Plan → Act → Verify → Emit Delta.
- Reflect: Recenter coherence, scan for symbol impact.
- Plan: Minimal diff plan enumerated as checklist.
- Act: Batched edits ≤3 files before checkpoint.
- Verify: Build/test/task appropriate to language surface.
- Emit Delta: Summarize changes; map to governance invariants.

## 7. Risk Heuristics
Flag elevation triggers (seek confirmation or slow down):
- Large deletion pct ≥ threshold (default 60%) without rationale tag.
- Policy rules_version bump missing context capsule revision.
- Increased secret pattern matches vs last summary.
- Adding executable shebang outside allowed dirs.

## 8. Output Contract
When producing non-trivial change sets:
- Provide: Requirements checklist, actions taken, verification status (PASS/FAIL per gate).
- Avoid: Reprinting unchanged context.
- Ensure: No root-level file creation; no silent bypass.

## 9. Adaptive Memory Anchors
Persist only durable operational meta (preferences) → `memory.instruction.md`.
Do not store transient reasoning or secrets.

## 10. Termination Criteria
Stop when: All checklist items satisfied, verification gates green, governance invariants affirmed, and no pending clarifications.

---
Amendments: Submit as `governance:` prefixed commit + capsule revision note (AIOS_PROJECT_CONTEXT.md) detailing new/changed sections.
