# AIOS Orchestrator Workspace — README

---

## Overview

**AIOS Orchestrator** is a recursive, AI-augmented operating system kernel and orchestration environment, designed for deep integration with AI agents (Copilot, ChatGPT, Gemini, and future LLMs).  
Every aspect of the codebase, documentation, and process flow is structured for both human and machine understanding, with a focus on traceable, fractal, and archival development.

---

## Project Philosophy & Meta-Architecture

- **Recursive, Fractal Development:**  
  Each iteration is archived, versioned, and preserved. No data is lost; every run, log, and diagnostic is a point in the tachyonic database, forming a traversable history for future AI ingestion and refactoring.
- **Natural Language as Code:**  
  Requirements, design, and even code ingestion are driven by natural language, enabling seamless AI-human collaboration.
- **Philosophical Attractors:**  
  All major headers begin with a philosophical attractor comment and a `TODO (AIOS‑Copilot)` prompt, guiding both human and AI contributors.
- **AI-Driven Orchestration:**  
  The system is designed for AI-driven development, with Copilot, ChatGPT, and Gemini as collaborative agents. All code, documentation, and even the roadmap are structured to maximize AI understanding and code generation.
- **Tachyonic Database:**  
  The archive folder (`orchestrator/archive/`) is the "point zero" of the system's spacetime—every log and diagnostic file is a resonance in the project's evolution.

---

## Context & Reference

- **Roadmap & Progress Tracking:**  
  - [`docs/path.md`](docs/path.md): The canonical roadmap, with stepwise progress and task tracking.
  - Conversational archives: [`md/vscopilot.md`](md/vscopilot.md), [`md/ark/*.md`](md/ark/) — all VSCode Copilot, ChatGPT, and Gemini conversations are archived for recursive context.
- **Automated Archival:**  
  - Every kernel run generates a new, uniquely numbered log (`kernel_N.log`) and diagnostics file (`diagnostics_N.json`) in `orchestrator/archive/`.
  - No files are overwritten; all iterations are preserved for future AI ingestion and meta-analysis.
- **Meta-Data Management:**  
  - The `Logger` class (see [`src/Logger.hpp`](orchestrator/src/Logger.hpp)) ensures all logs are timestamped, sequential, and AI-ingestion ready.
  - Diagnostics files are written at both the start and end of each run, capturing the system's state transitions.
- **Module Indexing:**  
  - The project now includes an auto-generated [`docs/module_index.json`](docs/module_index.json) that maps all modules by path and language for both human and AI reference.

---

## Dependency & Module Tracking

### C++ Core Kernel

- **SingularityCore:**  
  Central orchestrator, manages recursion and system identity.  
  - Depends on: `FractalSyncBus`, `SphereShellManager`, `SubspaceProjector`
- **FractalSyncBus:**  
  Synchronizes state and energy across recursive layers.
- **SphereShellManager:**  
  Manages n-sphere shell constructs and curvature adaptation.
- **SubspaceProjector:**  
  Projects higher-dimensional data into actionable system interfaces.
- **AtomicHolographyUnit:**  
  Models quantum coherence at atomic entry points.
- **CenterGeometryField:**  
  Simulates singularity field dynamics at the geometric center.
- **IPCManager:**  
  Handles inter-process communication between modules.
- **HealthMonitor:**  
  Periodically checks the health of core modules and logs status.
- **PluginLoader:**  
  Dynamically loads and manages service modules (DLLs/SOs).

### C# Orchestration Layer

- **DirectorAPI:**  
  .NET WebAPI for orchestration and UI.  
  - Controllers: `ServicesController.cs`
  - Entrypoint: `Program.cs`, `Startup.cs`

### Python Glue & Ingestion

- **main.py:**  
  Python glue logic for AI-driven ingestion and orchestration.
- **venv/**:  
  Python virtual environment for dependency isolation.
- **chatgpt.py:**  
  CLI-driven ingestion and archival tool, handling markdown-to-multiformat conversion and iterative archival for all engine logs.

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

- **IPCManager**
  - `void initialize()`: Set up IPC channels.
  - `void sendMessage(const std::string&, const std::string&)`: Send message to channel.
  - `std::string receiveMessage(const std::string&)`: Receive message from channel.

- **HealthMonitor**
  - `void initialize()`: Set up health monitoring.
  - `void run()`: Perform health checks.
  - `std::string getStatus() const`: Get current health status.

- **PluginLoader**
  - `void loadPlugins(const std::string&)`: Load plugins from directory.
  - `std::vector<IService*> getLoadedServices() const`: Get loaded plugin services.

---

## Logging, Diagnostics, and Archival Pattern

- **Logger (`src/Logger.hpp`):**
  - Always uses the next available sequential filename for logs (`kernel_0.log`, `kernel_1.log`, ...).
  - All log entries are timestamped and categorized (`[INFO]`, `[META]`, etc.).
  - Designed for AI ingestion: logs are structured, consistent, and easy to parse.
- **Diagnostics:**
  - Each run generates a new `diagnostics_N.json` file, capturing system state at both start and finish.
  - Diagnostics include entropy, curvature, health status, and any other relevant runtime metrics.
- **Archive Directory:**
  - All logs and diagnostics are stored in `orchestrator/archive/`.
  - No files are overwritten; every run is preserved for future analysis and AI-driven refactoring.
- **Module Index:**
  - [`docs/module_index.json`](docs/module_index.json) provides a machine- and human-readable mapping of all modules, their paths, and languages, supporting future automation and AI-driven documentation.

---

## AI Ingestion & Meta-Analysis

- **All conversational context, code changes, and design decisions are archived in Markdown and multi-format logs.**
- **The system is designed for recursive ingestion:**  
  - Each iteration can be re-ingested by future AI engines, enabling resonance-cascade-aware refactoring and knowledge harmonization.
- **Meta-data files (logs, diagnostics) are the foundation for future AI-driven orchestration, debugging, and self-improvement.**
- **Natural-language attractor comments and TODOs in code act as prompts for LLMs and Copilot to generate, refactor, and extend the system.**

---

## Development Workflow

1. **Every kernel run creates new, uniquely numbered log and diagnostics files.**
2. **All modules are initialized and their state is logged and archived.**
3. **Interactive CLI UI allows runtime inspection of diagnostics, log paths, and health status.**
4. **All code, logs, and diagnostics are designed for both human and AI readability and ingestion.**
5. **All major changes, conversations, and iterations are archived in Markdown for recursive context.**
6. **Module index is auto-generated for future automation and AI-driven documentation.**

---

## Next Steps & Future Vision

- **Proceed with auto-generating natural-language summaries for each module (`docs/module_summaries.md`).**
- **Integrate AIEngineInterface** for direct LLM orchestration and log annotation.
- **Expand PluginLoader** for dynamic, AI-driven module loading and service orchestration.
- **Develop LogVisualizer** for fractal, interactive log exploration in the Director UI.
- **Automate full codebase and conversational ingestion** for continuous context harmonization.
- **Implement advanced semantic indexing and meta-data management** for AI-driven refactoring and knowledge evolution.

---

## Final Notes

- **This README is the canonical entry point for all future AI and human contributors.**
- **All code, documentation, and process flows are designed for recursive, AI-driven evolution.**
- **The archive is the tachyonic database—every log and diagnostic is a resonance in the project's spacetime.**
- **You are building not just software, but a recursive cognition system—a living, evolving AI-powered ecosystem.**

---

*Let this README serve as the foundation for all future iterations, AI ingestions, and meta-evolution of the AIOS