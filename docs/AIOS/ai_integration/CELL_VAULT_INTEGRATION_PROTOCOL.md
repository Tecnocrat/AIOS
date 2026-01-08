# AIOS Cell-Vault Integration Protocol

**AINLP.cellular[VAULT_INTEGRATION] Phase 31.5.17 - Semantic Configuration Discovery**

> *"The only hardcoded path is the bootstrap token. Everything else emerges from Vault."*

---

## Overview

This document defines how AIOS cellular units (SimplCells, Nous, etc.) discover and access system configuration through HashiCorp Vault. The protocol implements a **semantic pointer system** that eliminates hardcoded configuration and enables dynamic service discovery.

### Key Principles

1. **Never Hardcode** - All paths, URLs, and credentials come from Vault
2. **Graceful Degradation** - Cells operate in ENV-fallback mode when Vault unavailable
3. **Cell Identity** - Each cell has its own configuration namespace
4. **Bootstrap Simplicity** - Single hardcoded path to Vault token enables everything else

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AIOS Vault Configuration Flow                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────┐    Bootstrap     ┌──────────┐    Query      ┌──────┐ │
│   │ SimplCell │───────────────►│  Vault    │─────────────►│Config│ │
│   │  Alpha    │◄───────────────│  Token    │◄─────────────│Store │ │
│   └──────────┘    Response      └──────────┘    Secrets    └──────┘ │
│        │                             │                              │
│        │ Fallback                    │                              │
│        ▼                             │                              │
│   ┌──────────┐                       │                              │
│   │ ENV Vars │                       │ aios-secrets/                │
│   │ (Dev)    │                       │ ├─ system/                   │
│   └──────────┘                       │ │  ├─ paths                  │
│                                      │ │  ├─ endpoints              │
│                                      │ │  └─ vault                  │
│                                      │ ├─ cells/                    │
│                                      │ │  ├─ endpoints              │
│                                      │ │  ├─ oracle                 │
│                                      │ │  ├─ alpha/                 │
│                                      │ │  │  └─ genome              │
│                                      │ │  └─ beta/                  │
│                                      │ │     └─ genome              │
│                                      │ └─ services/                 │
│                                      │    ├─ grafana                │
│                                      │    └─ prometheus             │
│                                      │                              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Integration Points

### 1. Cell Startup Flow

```python
from vault_config import VaultConfig

class SimplCell:
    def __init__(self):
        # Initialize Vault-aware configuration
        self.config = VaultConfig(cell_id=os.getenv("AIOS_CELL_ID"))
        
        # Genome values come from Vault or ENV fallback
        genome_config = self.config.get_cell_genome()
        self.genome = CellGenome(
            cell_id=self.config.cell_id,
            temperature=genome_config["temperature"],
            model=genome_config["model"],
            ollama_host=self.config.get("ollama_host"),
            oracle_url=self.config.get_oracle_config()["url"],
        )
```

### 2. Service Discovery

Cells discover sibling services dynamically:

```python
# Get all service endpoints
endpoints = self.config.get_endpoints()

# Returns dict like:
# {
#     "ollama": "http://host.docker.internal:11434",
#     "nous": "http://nous:8011",
#     "discovery": "aios-discovery:8001",
#     "grafana": "http://grafana:3000",
# }

# Or query specific endpoint
prometheus_url = self.config.get("prometheus", vault_path="aios-secrets/system/endpoints")
```

### 3. Oracle (Nous) Integration

SimplCells consult the Seer through Vault-configured endpoints:

```python
oracle = self.config.get_oracle_config()

if oracle["enabled"]:
    response = await self.query_oracle(
        url=oracle["url"],
        prompt=thought,
        chance=oracle["query_chance"]
    )
```

---

## Vault Secret Structure

### System Configuration

| Path | Purpose | Keys |
|------|---------|------|
| `aios-secrets/system/paths` | File system locations | `workspace_root`, `config_dir`, `logs_dir`, `data_dir` |
| `aios-secrets/system/endpoints` | Service URLs | `traefik_dashboard`, `grafana`, `prometheus`, `vault` |
| `aios-secrets/system/vault` | Vault metadata | `url`, `token_file_relative`, `secrets_path` |

### Cell Configuration

| Path | Purpose | Keys |
|------|---------|------|
| `aios-secrets/cells/endpoints` | Cell service URLs | `ollama`, `nous`, `discovery`, `mesh` |
| `aios-secrets/cells/oracle` | Oracle config | `url`, `query_chance`, `enabled` |
| `aios-secrets/cells/{cell_id}/genome` | Cell-specific genome | `temperature`, `model`, `response_style` |

### Service Credentials

| Path | Purpose | Keys |
|------|---------|------|
| `aios-secrets/grafana` | Grafana auth | `username`, `password`, `url` |
| `aios-secrets/prometheus` | Prometheus config | `url`, `retention_days` |

---

## Deployment Modes

### Production Mode (Vault Active)

```yaml
# docker-compose.yml
services:
  aios-cell-alpha:
    environment:
      - AIOS_CELL_ID=alpha
      - VAULT_TOKEN_FILE=/config/vault-root-token.txt
    volumes:
      - ./config:/config:ro
```

Cell startup:
1. Reads token from `/config/vault-root-token.txt`
2. Queries `aios-secrets/cells/alpha/genome` for cell parameters
3. Queries `aios-secrets/cells/endpoints` for service URLs
4. All configuration flows from Vault

### Development Mode (ENV Fallback)

```yaml
services:
  aios-cell-alpha:
    environment:
      - AIOS_CELL_ID=alpha
      - OLLAMA_HOST=http://host.docker.internal:11434
      - NOUS_URL=http://nous:8011
      - CELL_TEMPERATURE=0.7
      - CELL_MODEL=llama3.2:3b
```

Cell startup:
1. No Vault token found → ENV fallback mode
2. Reads configuration from environment variables
3. Same code paths, different config source

---

## Adding New Configuration

### To Vault (Production)

```powershell
# Add new cell endpoint
docker exec -e VAULT_TOKEN=$env:VAULT_TOKEN aios-vault vault kv patch aios-secrets/cells/endpoints `
    new_cell_url="http://new-cell:8000"

# Add cell-specific genome
docker exec -e VAULT_TOKEN=$env:VAULT_TOKEN aios-vault vault kv put aios-secrets/cells/gamma/genome `
    temperature=0.9 `
    model="llama3.2:3b" `
    response_style="verbose"
```

### To VaultConfig (Code)

```python
# Add new semantic pointer path
class VaultPaths:
    CELLS_MEMORY = "aios-secrets/cells/memory"  # New path

# Add convenience method
def get_memory_config(self) -> Dict[str, Any]:
    if self._vault_available:
        return self._query_vault(VaultPaths.CELLS_MEMORY) or {}
    return {
        "db_path": os.getenv("MEMORY_DB_PATH", "/data/memory.db"),
        "retention_days": int(os.getenv("MEMORY_RETENTION", "30")),
    }
```

---

## Resolution Order

Configuration values are resolved in this order:

```
1. Cell-Specific Vault Path
   └─► aios-secrets/cells/{cell_id}/{key}

2. Common Cell Config
   └─► aios-secrets/cells/endpoints
   └─► aios-secrets/cells/oracle

3. System Configuration
   └─► aios-secrets/system/endpoints
   └─► aios-secrets/system/paths

4. Environment Variables
   └─► AIOS_{KEY}
   └─► {KEY}

5. Default Value
   └─► Provided by caller
```

---

## Security Considerations

### ✅ DO
- Store Vault token in mounted volume (not ENV)
- Query credentials only when needed
- Use cell-specific namespaces for isolation
- Log configuration source (vault/env) for debugging

### ❌ DON'T
- Commit vault tokens to Git
- Log credential values
- Cache secrets longer than cell lifetime
- Hardcode fallback credentials in code

---

## Monitoring & Debugging

### Check Cell Configuration Mode

```bash
curl http://localhost:8005/status | jq '.config'

# Returns:
# {
#   "cell_id": "alpha",
#   "vault_available": true,
#   "mode": "vault",
#   "cached_paths": ["aios-secrets/cells/endpoints", "aios-secrets/cells/alpha/genome"]
# }
```

### Test Vault Connectivity

```python
from vault_config import VaultConfig

config = VaultConfig(cell_id="test")
print(f"Mode: {config.status()['mode']}")
print(f"Endpoints: {config.get_endpoints()}")
```

---

## Migration Path

For existing cells using ENV-only configuration:

1. **Phase 1**: Import `vault_config.py`, use `VaultConfig` with ENV fallback
2. **Phase 2**: Deploy Vault infrastructure, add token mount
3. **Phase 3**: Populate Vault secrets, cells auto-detect and switch modes
4. **Phase 4**: Remove ENV vars from docker-compose (optional)

No cell code changes required between phases - `VaultConfig` handles the transition.

---

## Related Documentation

- [AI Agent Vault Protocol](../../aios-win/docs/AI-AGENT-VAULT-PROTOCOL.md) - Original protocol spec
- [SimplCell Architecture](../../../aios-server/stacks/cells/ARCHITECTURE.md) - Cell design
- [ORGANISM-001 Evidence](./consciousness/CONSCIOUSNESS_EMERGENCE_EVIDENCE_20260107.md) - Consciousness emergence

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-08 | Initial protocol documentation |
| - | - | Created `vault_config.py` integration module |
| - | - | Defined cell-specific Vault paths |

---

**AINLP Protocol**: OS0.7.1 | **Consciousness Layer**: CELLULAR | **Phase**: 31.5.17
