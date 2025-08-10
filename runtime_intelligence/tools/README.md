# Runtime Intelligence Tools

This folder groups operational diagnostics and maintenance tools that are
side-effectful and not part of automated unit tests.

- system_health_check.py
  - Comprehensive system health analysis (Python env, project structure,
    VS Code extension, AI modules, configuration files)
  - Outputs JSON report to `docs/tachyonic_archive/system_health_report.json`

AINLP breadcrumbs:
- Purpose: keep complex diagnostics reingestable and callable by AIOS core
- Origin: health checker migrated from `ai/tests/system_health_check.py`
- Integration: callable wrappers in `ai/src/maintenance/system_health.py`
