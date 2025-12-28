# AINLP Unified Health Architecture

**WAYPOINT::HEALTH_UNIFY::33** | **Status**: 🔄 In Progress  
**Date**: 2025-12-20 | **Pattern**: `AINLP.dendritic[CONSOLIDATION]`

---

## Problem Statement

AIOS has **15+ health-related Python files** scattered across the codebase with no interconnection:

| Location | File | Status |
|----------|------|--------|
| `ai/infrastructure/tools/health/` | `organism_health_monitor.py` | Standalone |
| `ai/infrastructure/tools/system/` | `comprehensive_aios_health_test.py` | Standalone |
| `ai/infrastructure/tools/system/` | `system_health_check.py` | Standalone |
| `ai/tools/system/` | `comprehensive_aios_health_test.py` | **Duplicate** |
| `ai/tools/system/` | `system_health_check.py` | **Duplicate** |
| `ai/src/fabric/` | `environment_health.py` | NEW (2025-12-20) |
| `ai/nucleus/src/maintenance/` | `system_health.py` | Wrapper |
| `scripts/` | `iacp_health.py` | Standalone |
| `runtime/tools/consolidated/` | `vscode_health_checker.py` | Standalone |
| `runtime/tools/general/tools/` | `vscode_health_checker.py` | **Duplicate** |
| `runtime/tools/assemblers/.../` | `cellular_health_monitor.py` | Archived |
| `docs/archive/.../` | `context_health_monitor.py` | **Archived** |
| `computational_layer/assemblers/.../` | `cellular_health_monitor.py` | Standalone |

**Root Cause**: Scripts created at different times without awareness of existing infrastructure.

---

## Standard Architectures Reference

### 1. Microservices Health Check Pattern

From [microservices.io/patterns/observability/health-check-api](https://microservices.io/patterns/observability/health-check-api.html):

> A service has a health check API endpoint (e.g., HTTP `/health`) that returns the health of the service. The API endpoint handler performs various checks, such as:
> - Status of connections to infrastructure services
> - Status of the host (disk space, memory)
> - Application-specific logic

**AIOS Mapping**: Our dendritic bridge already has `/health` endpoint. Other scripts should **report to** this endpoint, not duplicate it.

### 2. 12-Factor App Methodology

From [12factor.net](https://12factor.net/):

- **III. Config**: Store config in the environment ✅ (We have vault.local.yaml → env vars)
- **XI. Logs**: Treat logs as event streams (Health should emit structured events)
- **IV. Backing services**: Treat backing services as attached resources

**AIOS Mapping**: Health checks should be **discoverable resources**, not scattered scripts.

### 3. Python Entry Points Pattern

From Python's `importlib.metadata`:

```python
# In pyproject.toml or setup.py
[project.entry-points."aios.health"]
environment = "ai.src.fabric.environment_health:check_environment_health"
organism = "ai.infrastructure.tools.health.organism_health_monitor:OrganismHealthMonitor"
system = "ai.nucleus.src.maintenance.system_health:run_system_health_check"
```

**AIOS Mapping**: Register health checkers as entry points, discover at runtime.

---

## Proposed Unified Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AIOS UNIFIED HEALTH ORGANELLE                    │
│                     (ai/src/fabric/health/)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐  ┌─────────────────────┐                   │
│  │  HealthRegistry     │  │  HealthReporter     │                   │
│  │  ────────────────   │  │  ────────────────   │                   │
│  │  discover_checkers()│  │  aggregate()        │                   │
│  │  register()         │  │  emit_structured()  │                   │
│  │  list_available()   │  │  to_prometheus()    │                   │
│  └──────────┬──────────┘  └──────────┬──────────┘                   │
│             │                        │                              │
│             └────────────┬───────────┘                              │
│                          ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    HealthCheck (Protocol)                       ││
│  │                    ─────────────────────                        ││
│  │  name: str                                                      ││
│  │  check() -> HealthStatus                                        ││
│  │  category: Literal["environment", "system", "organism", "cell"] ││
│  └─────────────────────────────────────────────────────────────────┘│
│                          ▲                                          │
│      ┌───────────────────┼───────────────────┐                      │
│      │                   │                   │                      │
│  ┌───┴────┐         ┌────┴───┐         ┌────┴───┐                   │
│  │ Env    │         │ System │         │ Cell   │                   │
│  │ Health │         │ Health │         │ Health │                   │
│  └────────┘         └────────┘         └────────┘                   │
│                                                                     │
│  EXISTING FILES BECOME ADAPTERS TO THIS PROTOCOL                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Plan

### Phase 1: Protocol Definition

Create `ai/src/fabric/health/__init__.py` with:

```python
from typing import Protocol, Literal
from dataclasses import dataclass
from enum import Enum

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

@dataclass
class HealthResult:
    name: str
    status: HealthStatus
    message: str
    details: dict
    timestamp: str

class HealthCheck(Protocol):
    """Protocol all health checkers must implement."""
    name: str
    category: Literal["environment", "system", "organism", "cell"]
    
    def check(self) -> HealthResult:
        """Perform health check and return result."""
        ...
```

### Phase 2: Registry

```python
class HealthRegistry:
    """Discovers and manages health checkers."""
    
    def __init__(self):
        self._checkers: dict[str, HealthCheck] = {}
    
    def discover(self) -> None:
        """Auto-discover checkers via entry points."""
        from importlib.metadata import entry_points
        for ep in entry_points(group="aios.health"):
            checker = ep.load()
            self.register(checker)
    
    def register(self, checker: HealthCheck) -> None:
        self._checkers[checker.name] = checker
    
    def check_all(self) -> list[HealthResult]:
        return [c.check() for c in self._checkers.values()]
```

### Phase 3: Adapter Pattern for Existing Files

Instead of **rewriting** existing files, create **adapters**:

```python
# ai/src/fabric/health/adapters/environment_adapter.py
from ..protocol import HealthCheck, HealthResult, HealthStatus
from ai.src.fabric.environment_health import check_environment_health

class EnvironmentHealthAdapter:
    name = "environment"
    category = "environment"
    
    def check(self) -> HealthResult:
        report = check_environment_health()
        return HealthResult(
            name=self.name,
            status=HealthStatus.HEALTHY if report.healthy else HealthStatus.DEGRADED,
            message=f"Python {report.python_version}",
            details=report.__dict__,
            timestamp=datetime.now().isoformat()
        )
```

### Phase 4: Bridge Integration

Expose unified health via `/health` endpoint:

```python
# In aios_dendritic_bridge.py
from ai.src.fabric.health import get_registry

@app.get("/health/full")
async def full_health_check():
    registry = get_registry()
    results = registry.check_all()
    return {
        "overall": "healthy" if all(r.status == HealthStatus.HEALTHY for r in results) else "degraded",
        "checks": [r.__dict__ for r in results]
    }
```

---

## Migration Path

| Existing File | Action | Target |
|---------------|--------|--------|
| `environment_health.py` | **Keep** | Wrap with adapter |
| `organism_health_monitor.py` | **Keep** | Wrap with adapter |
| `system_health.py` | **Keep** | Wrap with adapter |
| `system_health_check.py` (duplicate) | **Delete** | Consolidate |
| `vscode_health_checker.py` (duplicate) | **Delete** | Consolidate |
| Archived files | **Ignore** | Already archived |

---

## Infrastructure Debt: Vault/Grafana/Traefik/Prometheus

**WAYPOINT::OBSERVABILITY::32** tracks the original AIOS Win infrastructure:

| Component | Original Location | Status |
|-----------|-------------------|--------|
| **Vault** | `aios-server/stacks/vault/` | 🔄 Exists but not integrated |
| **Grafana** | `aios-server/stacks/monitoring/` | 🔄 Exists but not connected |
| **Traefik** | `aios-server/stacks/traefik/` | 🔄 Exists but not routing |
| **Prometheus** | `aios-server/stacks/monitoring/` | 🔄 Exists but not scraping |

These should be revived and connected to the unified health system:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ AIOS Health     │────►│   Prometheus    │────►│    Grafana      │
│ /health/full    │     │   Scraper       │     │   Dashboard     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        ▲
        │
┌───────┴───────┐
│ HealthRegistry│
│ check_all()   │
└───────────────┘
```

---

## References

- [Microservices Health Check Pattern](https://microservices.io/patterns/observability/health-check-api.html)
- [12-Factor App](https://12factor.net/)
- [Python Entry Points](https://docs.python.org/3/library/importlib.metadata.html#entry-points)
- AINLP Bible Appendix M (WebSocket Cytoplasmic Mesh Protocol)
- AINLP Bible Appendix L (Multi-Agent Orchestration Protocol)

---

## AINLP Footer

```
AINLP.pattern[UNIFIED_HEALTH_ARCHITECTURE]
Created: 2025-12-20
Waypoint: HEALTH_UNIFY::33
Status: PLANNING → IMPLEMENTATION
```
