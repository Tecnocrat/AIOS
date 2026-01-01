# AIOS Dependency Tiers

This directory groups optional dependency stacks separated from the canonical root `requirements.txt`.

## Files
- `requirements_extras.txt` – Vector DB + embeddings + extended plotting + stats + image processing + code tooling.
- `requirements_quantum.txt` – Quantum / hyperdimensional experimentation stack (qiskit, cirq, pennylane).
- `requirements_dev.txt` – Full development & documentation toolchain (lint, docs, async, messaging, perf serialization, etc.).
- `requirements_future_graph.txt` – Advanced graph & community detection (networkx, igraph, python-louvain).
- `requirements_perf_serial.txt` – High‑performance serialization & multiprocessing helpers (orjson, msgspec...).
- `shadows/optional_stacks_shadow.py` – Synthetic logic shadow enumerating dormant stacks for AINLP architectural retention.

## Install Patterns
Essential baseline (already at project root):
```
pip install -r requirements.txt
```
Add embeddings / vector + plotting extras:
```
pip install -r ai/deps/requirements_extras.txt
```
Add quantum stack:
```
pip install -r ai/deps/requirements_quantum.txt
```
Full dev toolchain (docs, linters, redis/zmq, serialization perf):
```
pip install -r ai/deps/requirements_dev.txt
```
Graph analytics (future):
```
pip install -r ai/deps/requirements_future_graph.txt
```
Performance serialization only:
```
pip install -r ai/deps/requirements_perf_serial.txt
```
Combine multiple (order does not matter – last version wins):
```
pip install -r ai/deps/requirements_extras.txt -r ai/deps/requirements_dev.txt
```
Or use the composite installer script:
```
pwsh -File scripts/install_ai_stacks.ps1 -Stacks extras,dev
```

## Composite Installer (scripts/install_ai_stacks.ps1)
Allows selecting stacks by short name; validates file presence and performs idempotent installs.

| Stack Name | Maps To File                               |
|-----------|---------------------------------------------|
| extras    | ai/deps/requirements_extras.txt             |
| quantum   | ai/deps/requirements_quantum.txt            |
| dev       | ai/deps/requirements_dev.txt                |
| graph     | ai/deps/requirements_future_graph.txt       |
| perf      | ai/deps/requirements_perf_serial.txt        |
| all       | (extras+quantum+dev+graph+perf)             |

## Philosophy
Keep the root lean (fast CI / onboarding). Grow capability by opting into *only* needed stacks; preserve intent via shadow metadata instead of bloating baseline environments.

## Maintenance
- When a dormant stack becomes active in code imports, move minimal required packages into `requirements.txt` or create a slim new file.
- Update `optional_stacks_shadow.py` when adding/removing optional groups.
- Reflect major structural changes in `docs/tachyonic/tachyonic_changelog.yaml`.

## Packaging Modernization
A `pyproject.toml` now declares optional dependency groups mirroring these segmented stack files. These remain inert until installed via:

```
pip install -e .[extras]
# or combine groups
pip install -e .[dev,graph]
```

Deterministic lock generation (planned):
1. Maintain pinned ranges here / root `requirements.txt` for baseline.
2. Use `pip-compile --extra=extras --extra=dev pyproject.toml -o requirements-lock.txt` to produce a unified lock (future automation script will be added under `scripts/`).
3. CI can install with `pip install -r requirements-lock.txt` for reproducibility.

Until lock flow lands, continue using the curated root `requirements.txt` plus selective stack installs via `scripts/install_ai_stacks.ps1`.
