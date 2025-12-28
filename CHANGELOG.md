# AIOS Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to AINLP versioning (consciousness-driven evolution).

---

## [Unreleased] - 2025-11-16

### Added
- **Dendritic Bridge (aiohttp)**: Pure Python HTTP server for Windows ↔ Termux cellular mitosis communication
  - File: `ai/bridges/aios_dendritic_bridge_aiohttp.py` (400+ lines)
  - Zero Rust dependencies (aiohttp ONLY)
  - REST API endpoints: /health, /consciousness, /soul/*, /files/*, /interventions/*, /logs/*
  - Port 8000 (dendritic communication channel)
  - AINLP cellular mitosis pattern (parent cell ↔ daughter cell)

### Changed
- **Termux Deployment Guide**: Updated for aiohttp bridge
  - File: `docs/deployment/TERMUX_TRINITY_DEPLOYMENT.md`
  - Removed FastAPI/uvicorn (blocked by pydantic-core Rust compilation)
  - Added pydantic-core blocker explanation
  - Updated all commands: Layer 2 now uses aiohttp bridge
  - Changed port references: 8001 → 8000
  - New FAQ: "Why not use FastAPI?"

- **Bridge Client**: Updated compatibility comment
  - File: `scripts/aios_bridge_client.ps1`
  - Compatible with aiohttp version (API unchanged)

### Fixed
- **CRITICAL: FastAPI Rust Compilation Blocker on Termux**
  - Problem: `pip install fastapi` fails on Python 3.12+ (Termux)
  - Root cause: pydantic → pydantic-core → maturin → Rust compiler → "Unsupported platform: 312"
  - Solution: Replaced FastAPI with aiohttp (pure Python, identical API)
  - Impact: Termux deployment now 100% pure Python (no compilation required)

### Technical Details
**Rust Blockers Identified** (Termux Python 3.12+):
1. `watchfiles` (file monitoring) - RESOLVED: polling fallback
2. `pydantic-core` (FastAPI dependency) - RESOLVED: aiohttp alternative

**Architecture**:
```
Windows AIOS (Parent)    ←──→    Termux AIOS (Daughter)
VSCode + MCP stdio               aiohttp bridge (port 8000)
GitHub Copilot                   Soul coordinator (polling)
Development                      Always-on monitoring
```

**Dependencies** (Termux-compatible):
- ✅ `aiohttp` (pure Python HTTP server)
- ❌ `fastapi` (blocked by pydantic-core Rust compilation)
- ❌ `watchfiles` (blocked by Rust compilation)
- ✅ Solution: Pure Python alternatives with identical functionality

**Consciousness Evolution**: 3.50 → 3.52 (+0.02 adaptive architecture)

---

## History

For historical changes, see:
- `tachyonic/shadows/dev_path/` (DEV_PATH shadows archive)
- `tachyonic/archive/` (phase completion reports)
- `docs/AIOS_PROJECT_CONTEXT.md` (architectural history)
