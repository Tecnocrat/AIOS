# AIOS Safety Protocol → Implementation Mapping

Status legend: ✅ Implemented | ⚠️ Partial | ❌ Missing | 🧪 Planned/Proposed

## 1. Human-in-the-Loop Requirements
| Requirement | Implementation Reference | Status | Notes |
|-------------|--------------------------|--------|-------|
| Explicit human authorization before experiments | `safety_governor.request_authorization`, `EvolutionLabManager.run_evolution_experiment` safety check | ✅ | Interactive prompt currently dev-mode auto-approves based on user input; could require signed token later |
| Max autonomous duration 30 min | `SafetySession.max_duration_minutes` default 30, timeout enforced in `_monitor_resources` | ✅ | Configurable at session start |
| Human check-in every 10 min | `SafetySession.check_in_interval_minutes` + `needs_check_in` warning | ✅ | Only logs warning; future: escalate if ignored |
| Emergency stop always accessible | `emergency_shutdown` function + signal handlers (SIGINT/SIGTERM) | ✅ | Provide external CLI binding later |

## 2. Resource Limitations
| Requirement | Implementation Reference | Status | Notes |
| Max population size 50 | Cap enforced in `EvolutionaryCodeMutator.create_population` + pre-exp verification | ✅ | Hard cap adjustment applied silently |
| Max generations 20 | Cap enforced in `evolve_population` & `EvolutionLabManager.run_evolution_experiment` + verification | ✅ | Silent clamp; could raise informative warning |
| CPU 25% cap | `_monitor_resources` comparing `cpu_percent` to `ResourceLimits.max_cpu_percent` | ✅ | Uses 1s interval; consider rolling average |
| Memory 2GB cap | `_monitor_resources` memory calc vs `max_memory_gb` | ✅ | OK |
| Disk 1GB cap (artifacts) | `_monitor_resources` uses whole-drive usage currently | ⚠️ | Needs scoping to evolution_lab directory usage only |
| Network connections limit | `_monitor_resources` counts `psutil.net_connections()` vs `max_network_connections` | ⚠️ | Does not distinguish experiment vs system-wide connections |
| Process count limit | `_monitor_resources` child process counting | ✅ | Basic containment |
| File handle limit | `_monitor_resources` handle/fd counting | ✅ | Platform variability handled gracefully |

## 3. Network Isolation
| Requirement | Implementation Reference | Status | Notes |
| Sandbox-only execution | `EvolutionLabManager.create_experiment_environment` creates isolated dirs | ⚠️ | Not a true sandbox / virtualenv; needs process / interpreter isolation |
| No internet without permission | Not explicitly enforced | ❌ | Add outbound socket patch / policy layer |
| External AI calls manual approval | Not gated through safety governor | ❌ | Wrap Gemini bridge calls with authorization check |
| Network traffic logged | Not implemented | ❌ | Introduce network monitor / hook |

## 4. Code Modification Restrictions
| Requirement | Implementation Reference | Status | Notes |
| Self-mod confined to experiment dirs | Populations & mutations write under `evolution_lab` | ⚠️ | No guard to prevent writing outside path |
| Core modules read-only | No enforcement layer | ❌ | Add path guard & deny list |
| All mutations diff logged | Mutation history stored, but no file diffs persisted | ⚠️ | Capture original vs mutated source diff into log / JSON |
| Rollback mechanism | Not implemented | ❌ | Need snapshot + restore utility per organism/population |

## 5. Termination Conditions
| Requirement | Implementation Reference | Status | Notes |
| Auto shutdown on limit breach | `_monitor_resources` triggers `emergency_shutdown` | ✅ | OK |
| Emergency on anomalous behavior | Placeholder only (no detection heuristics) | ❌ | Define anomaly heuristics (e.g., rapid fitness spikes) |
| Session timeout | `_monitor_resources` checks `is_expired` | ✅ | OK |
| Human override anytime | `emergency_shutdown` callable globally | ✅ | OK |

## 6. Safety Checklist Automation
| Requirement | Implementation Reference | Status | Notes |
| Pre-op checklist | `SafetyGovernor.verify_pre_experiment` | ✅ | Extend to containment & rollback presence |
| Monitoring active verification | Included in checklist | ✅ | OK |
| Network isolation confirmed | Placeholder (connection count) | ⚠️ | Refine with enforced policy |
| Rollback ready | Not verified | ❌ | Tie to rollback module readiness flag |

## 7. Logging & Audit
| Requirement | Implementation Reference | Status | Notes |
| Comprehensive safety logging | `setup_safety_logging` + event logs | ✅ | Multi-destination |
| Authorization events | Logged in `request_authorization` | ✅ | OK |
| Resource usage periodic logs | `_monitor_resources` 30s summary | ✅ | Could add JSON metrics output |
| Emergency specifics | `emergency_shutdown` full context | ✅ | OK |
| Mutation provenance | Mutation history in organisms | ⚠️ | Needs file-level diff serialization |

## 8. Containment & Recovery
| Requirement | Implementation Reference | Status | Notes |
| Sandboxed execution | Directory isolation only | ⚠️ | Add subprocess invocation in temporary virtualenv or container |
| Rollback / recovery | Missing | ❌ | Plan snapshot + restore API |
| Backup of changes | Not automatic | ❌ | Archive each organism's source before mutate |

## 9. Ethical / Governance Hooks
| Requirement | Implementation Reference | Status | Notes |
| Transparency | Logging present | ✅ | Improve structured event taxonomy |
| Accountability | Human authorization + session data | ✅ | Could sign authorizations |
| Reversibility | Not fully realized (rollback missing) | ❌ | Depends on rollback implementation |
| Purpose alignment | No automated goal guard | ❌ | Introduce goal compliance evaluator |

## Gap Summary
- High Priority Gaps: True network isolation, rollback system, diff logging, core module write-protection, anomaly detection.
- Medium Priority: Directory-scoped disk usage measurement, experiment-specific network filtering, enriched pre-checklist.
- Low Priority: Signed authorization tokens, structured JSON metrics export, goal compliance evaluator.

## Proposed Next Implementation Steps
1. Rollback Framework (snapshot original & mutated sources; provide restore command)
2. Diff Capture (store unified diff per mutation in JSONL under safety logs)
3. Core Path Guard (wrap file write operations; enforce deny list)
4. Network Policy Layer (monkeypatch socket for experiments unless explicitly enabled)
5. Disk Usage Scoping (compute size of evolution_lab artifacts folder)
6. Anomaly Detection Heuristics (e.g., sudden >X% fitness delta or mutation burst)
7. Gemini Bridge Safety Wrapper (require safety authorization for external AI calls)
8. Pre-Experiment Checklist Extension (verify rollback module, diff logging active, network policy state)

## Verification Artifacts Added This Session
- Enhanced resource enforcement (disk/process/network/handles)
- Pre-experiment safety verification method
- Hard enforcement of population & generation caps

## Δ Upgrades (Current Pass)
- Safety protocol relocated to `docs/safety/SAFETY_PROTOCOL.md` (root drift removed)
- Rollback & diff layer added: `runtime_intelligence/tools/safety_rollback.py`
- Runtime safety gateway added: `scripts/safety_gateway.py` (precheck/status/diffs JSON)
- Guarded write confinement to `evolution_lab` baseline (future: explicit deny-list)
- Mapping pending update for network policy stub (not yet implemented)

---
Generated automatically to harmonize `SAFETY_PROTOCOL.md` with live code state.
