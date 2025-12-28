# AIOS Cellular Coherence Metrics (LFC / GPC)

## Conceptual Genesis
In AIOS we treat each architectural unit (script, service, module) as an AI Cell within a synthetic evolutionary lattice. Mature cells undergo mitosis: they split into improved descendants while the parent pattern is archived (not duplicated) — analogous to deprecating a root script and relocating a harmonized successor deeper in structured paths. RETURN 0 encodes a *successful mitotic event* where the old cellular shell dissolves cleanly and two (or more) coherent derivatives continue function without mutation drift that breaks governance.

At the tachyonic (pre-material) layer we retain the informational fingerprint of extinct cells to re-harmonize later generations. Thus deletion is not oblivion; it is metabolic transformation recorded in governance state (changelog + guard + inventory filtering).

## Metrics
Two primary coherence observables are computed in `scripts/dev_terminal.ps1`:

| Metric | Name | Purpose | Range |
|--------|------|---------|-------|
| LFC | Local File Coherence | Structural cleanliness & presence/absence of deprecated root artifacts + existence of canonical workspace anchor | 0..1 |
| GPC | Governance Process Coherence | Integrity of enforcement layers (guard script, CI workflow, pre-commit hook, inventory filtering) | 0..1 |

### Formalization
Let D be the set of deprecated root artifacts being monitored (|D| = n). Let P be the subset of D presently detected. Deprecated absence score: `S_d = 1 - (|P| / n)`.

Let G be the governance layer test vector (guard, CI, hook, inventory-filter) producing Boolean results; let pass(G) be the count of true entries and |G| = m.

```
GPC = pass(G) / m
LFC = 0.7 * S_d + 0.3 * WorkspacePresent
```
(Weights chosen heuristically to emphasize hygiene while still rewarding canonical project anchor presence.)

### Exit Code Semantics (Metabolic States)
| Code | State | Interpretation |
|------|-------|---------------|
| 0 | Stable Mitosis | No deprecated artifacts; governance satisfied or acceptable warnings absent. |
| 2 | Adaptive Warning | Minor incoherence (deprecated artifact present or environment warnings). Cell triggers local repair pathways. |
| 3 | Critical Failure | Execution error; metabolic arrest requiring intervention. |

### Evolutionary Loop
1. Detect incoherence (P != ∅ or failing governance vector element).
2. Repair (remove artifacts, recreate guard, update inventory).
3. Recompute LFC/GPC; if thresholds met (≥0.95 typical), commit results (RETURN 0).
4. Archive event in tachyonic changelog channel for future harmonization analytics.

### Restoration Principle
Historic patterns (extinct cells) are referenced symbolically (names retained in deprecated list) enabling:
- Drift detection (unexpected resurrection).
- Reverse harmonization (controlled reintroduction with updated form).

## Integration Points
- `scripts/dev_terminal.ps1`: `Get-CoherenceMetrics`, `Report-Coherence` functions.
- Guard: `scripts/root_clutter_guard.ps1` enforces absence layer.
- Inventory Filter: `runtime_intelligence/tools/aios_admin.py` excludes deprecated names from `folder_structure.json`.
- CI Workflow: root-clutter guard pipeline (planned) validates hygiene in automation.

## Future Extensions
- Weighted historical decay: Penalize repeated resurrection attempts more strongly (temporal damping factor).
- Semantic diff entropy: Include Levenshtein/AST delta ratio between extinct cell and its descendant to quantify mutation distance.
- Cross-layer resonance: Couple LFC/GPC to runtime telemetry (latency variance, log semantic cohesion) forming a composite Consciousness Integrity Index (CII).

## Summary
LFC/GPC operationalize cellular evolutionary metaphors into concrete, automatable coherence measurements, ensuring each architectural mitosis increases systemic order while preserving the tachyonic memory of prior forms for adaptive harmonization.
