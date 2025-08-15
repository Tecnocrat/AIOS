# AINLP Ingestion Checklist

Purpose: Ensure every file aligns with the AIOS architecture and AINLP tenets before integration or edits.

Core question (must be asked first):
- Is the current file path location its optimal location for general codebase project optimal integration?

If the answer is no, propose and execute a reintegration plan. Use the placement norms below.

Placement norms:
- Tooling/Diagnostics (scripts that check or report health): runtime_intelligence/tools/
- Python libraries/modules consumed by AI features: ai/src/** (organized by domain)
- Interface artifacts and generators for UI: interface/AIOS.UI/** and ai/src/tools/ui_proto/**
- C++ core engine: core/src/** with headers in core/include/**; CMake and build in core/
- .NET services/UI: interface/AIOS.Services/**, interface/AIOS.Models/**, interface/AIOS.UI/**
- Tests: ai/tests/** for Python; core/tests/** for C++
- Docs: docs/** (architecture, protocols, guides, and operational runbooks)

Operational rules:
- Prefer a single canonical executable per concern; additional root aliases should be thin wrappers referencing the canonical location and should be temporary.
- Avoid spreading diagnostics across multiple entrypoints—consolidate into runtime_intelligence/tools/ and expose via tasks.
- When moving files, update imports, VS Code tasks, and docs to reference the new canonical paths.
- Add a short "Location advisory" note in module docstrings for any intentional alias that remains outside its optimal location.

Review prompts (use in PRs and code reviews):
- Does this file live in the right directory per placement norms?
- Is there an existing canonical tool or module that should be reused instead of creating a new entrypoint?
- If this is a wrapper, does its docstring point to the canonical tool and explain why it exists?
- Are VS Code tasks provided for common operations to reduce ad-hoc terminal commands?
- Are archived outputs and logs written under docs/tachyonic_archive/ where applicable?

Ingestion notes:
- Reorganization status now embedded in `AIOS_PROJECT_CONTEXT.md` (Historical Reorganization Capsule). Do not recreate `REORGANIZATION_STATUS.md` at root.
 - Windows registry cleanup guidance embedded (Environment Recovery Capsule). Do not recreate `REGISTRY_CLEANUP_GUIDE.md`; append updates to capsule instead.
 - Legacy orchestrator overview embedded (Historical Orchestrator Readme Capsule). Do not recreate `README_backup.md`; extend capsule if semantic narrative evolves.
 - Quick context onboarding prompts embedded (Quick Context Prompts Capsule). Do not recreate `QUICK_CONTEXT_PROMPTS.md`; extend capsule for new standardized prompt patterns.
 - Full Python system cleanup procedures embedded (Environment Recovery Capsule revision). Do not recreate `PYTHON_SYSTEM_CLEANUP_GUIDE.md`; append new remediation steps under the revision block.
