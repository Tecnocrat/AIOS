# AIOS Orchestrator Workspace — README

---

## Overview

This workspace is a recursive, AI-augmented operating system kernel and orchestration environment.  
It is designed for deep integration with AI agents (Copilot, ChatGPT, Gemini), and all code, documentation, and process flows are structured for both human and machine understanding.

---

## Context & Reference

- **Natural language is the primary interface** for requirements, design, and code ingestion.
- All major design decisions, module definitions, and roadmap progress are tracked in:
  - [`docs/path.md`](docs/path.md)
  - Conversational archives: [`md/vscopilot.md`](md/vscopilot.md), [`md/ark/*.md`](md/ark/)
- This README is the canonical entry point for dependency tracking, class/function documentation, and deep logic reference.

---

## Dependency Tracking

### C++ Core Kernel

- **SingularityCore**: Central orchestrator, manages recursion and system identity.
  - Depends on: `FractalSyncBus`, `SphereShellManager`, `SubspaceProjector`
- **FractalSyncBus**: Synchronizes state and energy across recursive layers.
- **SphereShellManager**: Manages n-sphere shell constructs and curvature adaptation.
- **SubspaceProjector**: Projects higher-dimensional data into actionable system interfaces.
- **AtomicHolographyUnit**: Models quantum coherence at atomic entry points.
- **CenterGeometryField**: Simulates singularity field dynamics at the geometric center.

### C# Orchestration Layer

- **DirectorAPI**: .NET WebAPI for orchestration and UI.
  - Controllers: `ServicesController.cs`
  - Entrypoint: `Program.cs`, `Startup.cs`

### Python Glue & Ingestion

- **main.py**: Python glue logic for AI-driven ingestion and orchestration.
- **venv/**: Python virtual environment for dependency isolation.

---

## Class & Function Documentation

### C++ Kernel Classes

- **SingularityCore**
  - `void initialize()`: Initialize all core modules.
  - `void tick()`: Advance kernel clock and synchronize modules.
  - `double getEntropy()`: Return current entropy state.
  - `double getCurvatureAtCenter()`: Return curvature at system center.

- **FractalSyncBus**
  - `void initialize()`: Prepare synchronization bus.
  - `void synchronize()`: Harmonize all registered fractal layers.

- **SphereShellManager**
  - `void bootstrap()`: Initialize shell structures.
  - `void rotateShells()`: Update shell orientation and curvature.

- **SubspaceProjector**
  - `void configure()`: Prepare projection logic.
  - `void project()`: Project subspace data into system space.

- **AtomicHolographyUnit**
  - `void initialize()`: Prepare quantum coherence simulation.
  - `void update()`: Update quantum state.

- **CenterGeometryField**
  - `void initialize()`: Prepare singularity field simulation.
  - `void simulate()`: Run field dynamics at r=0.

---

## Deep Logic & AI Ingestion Prompts

- All major headers begin with a **philosophical attractor comment** and a `TODO (AIOS‑Copilot)` prompt.
- Example:
  ```cpp
  // 🌌 SingularityCore: The nucleus of our hypersphere kernel.
  //   “Here at the center, all recursion and identity emerge.”
  // TODO (AIOS‑Copilot): Suggest advanced entropy‑based scheduling