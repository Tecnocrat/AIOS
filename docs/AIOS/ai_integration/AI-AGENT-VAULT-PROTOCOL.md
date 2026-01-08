# AI Agent Vault Protocol

**Semantic Pointer System for AI Agents**

## Overview

This document defines how AI agents should discover and access AIOS system configuration. All sensitive data (paths, credentials, endpoints) is stored in Vault using semantic pointers. Agents query Vault rather than hardcoding values.

---

## 🎯 Core Principle

**Never hardcode. Always query Vault first.**

```
Agent → Vault → Configuration/Secrets → Action
```

---

## 🔑 Bootstrap: How to Access Vault

AI agents must first obtain Vault access. The **only** hardcoded path is:

```powershell
# Bootstrap Vault access
$vaultToken = Get-Content ".\config\vault-root-token.txt"
$env:VAULT_TOKEN = $vaultToken
```

From this point, all other configuration is discovered via Vault queries.

---

## 📍 Semantic Pointer Structure

### System Paths (`aios-secrets/system/paths`)

```powershell
# Query system paths
docker exec -e VAULT_TOKEN=$env:VAULT_TOKEN aios-vault vault kv get aios-secrets/system/paths
```

**Returns:**
- `workspace_root` - AIOS workspace root directory
- `config_dir` - Configuration files location
- `scripts_dir` - PowerShell scripts location
- `logs_dir` - Log files location
- `data_dir` - Data storage location
- `server_stacks` - Docker compose stacks location

### Vault Configuration (`aios-secrets/system/vault`)

```powershell
# Query Vault metadata
docker exec -e VAULT_TOKEN=$env:VAULT_TOKEN aios-vault vault kv get aios-secrets/system/vault
```

**Returns:**
- `url` - Vault API endpoint
- `token_file_relative` - Relative path to root token
- `unseal_keys_file` - Relative path to unseal keys
- `service_tokens_file` - Relative path to service tokens
- `secrets_path` - Base path for secrets (aios-secrets)

### Service Endpoints (`aios-secrets/system/endpoints`)

```powershell
# Query service URLs
docker exec -e VAULT_TOKEN=$env:VAULT_TOKEN aios-vault vault kv get aios-secrets/system/endpoints
```

**Returns:**
- `traefik_dashboard` - Traefik dashboard URL
- `traefik_metrics` - Traefik metrics endpoint
- `grafana` - Grafana UI URL
- `prometheus` - Prometheus API URL
- `loki` - Loki API URL
- `vault` - Vault UI URL
- `whoami` - Test service URL

### Service Credentials

```powershell
# Query Grafana credentials
docker exec -e VAULT_TOKEN=$env:VAULT_TOKEN aios-vault vault kv get aios-secrets/grafana

# Query Traefik credentials
docker exec -e VAULT_TOKEN=$env:VAULT_TOKEN aios-vault vault kv get aios-secrets/traefik
```

**Returns:** `username`, `password`, `url` for each service

### Backup Configuration (`aios-secrets/system/backup`)

```powershell
# Query backup settings
docker exec -e VAULT_TOKEN=$env:VAULT_TOKEN aios-vault vault kv get aios-secrets/system/backup
```

**Returns:**
- `local_path` - Local backup directory
- `cloud_archive_path` - Cloud-ready ZIP location
- `backup_script` - Backup utility script path

---

## 🤖 AI Agent Helper Script

Use the provided helper script for quick discovery:

```powershell
# Discover all configuration
.\scripts\agent-helper.ps1 -Query all

# Query specific categories
.\scripts\agent-helper.ps1 -Query paths
.\scripts\agent-helper.ps1 -Query endpoints
.\scripts\agent-helper.ps1 -Query credentials
.\scripts\agent-helper.ps1 -Query backup
```

---

## 🔄 Agent Workflow Example

```powershell
# Step 1: Bootstrap Vault access
$env:VAULT_TOKEN = Get-Content ".\config\vault-root-token.txt"

# Step 2: Discover configuration
$paths = docker exec -e VAULT_TOKEN=$env:VAULT_TOKEN aios-vault vault kv get -format=json aios-secrets/system/paths | ConvertFrom-Json
$endpoints = docker exec -e VAULT_TOKEN=$env:VAULT_TOKEN aios-vault vault kv get -format=json aios-secrets/system/endpoints | ConvertFrom-Json

# Step 3: Extract values
$workspaceRoot = $paths.data.data.workspace_root
$grafanaUrl = $endpoints.data.data.grafana

# Step 4: Use discovered configuration
Write-Host "Working in: $workspaceRoot"
Write-Host "Grafana at: $grafanaUrl"

# Step 5: Get credentials when needed
$grafanaCreds = docker exec -e VAULT_TOKEN=$env:VAULT_TOKEN aios-vault vault kv get -format=json aios-secrets/grafana | ConvertFrom-Json
$username = $grafanaCreds.data.data.username
$password = $grafanaCreds.data.data.password
```

---

## 🛡️ Security Best Practices

### ✅ DO:
- Query Vault for all paths, URLs, and credentials
- Use `agent-helper.ps1` for discovery
- Store new configuration in Vault immediately
- Use relative paths in bootstrap (`.\\config\\vault-root-token.txt`)

### ❌ DON'T:
- Hardcode absolute paths in scripts or documentation
- Expose credentials in logs or markdown files
- Commit Vault tokens or keys to Git
- Cache credentials longer than needed

---

## 📊 Vault Secrets Map

```
aios-secrets/
├── system/
│   ├── paths          # File system paths
│   ├── vault          # Vault configuration
│   ├── endpoints      # Service URLs
│   └── backup         # Backup configuration
├── grafana            # Grafana credentials
├── traefik            # Traefik credentials
└── prometheus         # Prometheus metadata
```

---

## 🔧 Adding New Configuration

When adding new secrets or configuration:

```powershell
# Example: Add new service endpoint
docker exec -e VAULT_TOKEN=$env:VAULT_TOKEN aios-vault vault kv patch aios-secrets/system/endpoints `
    new_service_url="http://newservice.lan"

# Example: Add new credential set
docker exec -e VAULT_TOKEN=$env:VAULT_TOKEN aios-vault vault kv put aios-secrets/newservice `
    username=admin `
    password=secure123 `
    url="http://newservice.lan"
```

---

## 🎯 Agent Onboarding Checklist

For new AI agents:

1. ✅ Obtain Vault token from `.\config\vault-root-token.txt`
2. ✅ Run `.\scripts\agent-helper.ps1 -Query all` to discover environment
3. ✅ Query `aios-secrets/system/paths` for file system structure
4. ✅ Query `aios-secrets/system/endpoints` for service URLs
5. ✅ Query specific credential paths only when needed
6. ✅ Never log or expose retrieved secrets
7. ✅ Always use Vault paths, not hardcoded values

---

## 📞 Support

If configuration is missing from Vault:
1. Check if service is deployed: `docker ps`
2. Verify Vault is unsealed: `docker exec aios-vault vault status`
3. Re-run bootstrap if needed: `.\scripts\windows-bootstrap\00-master-bootstrap.ps1`
4. Consult `.\docs\AIOS-KNOWLEDGE-BASE.md`

---

**Remember: The only hardcoded path is `.\config\vault-root-token.txt`. Everything else comes from Vault.**
