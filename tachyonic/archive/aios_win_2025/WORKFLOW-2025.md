# AIOS-WIN Deployment Workflow

**Complete Windows 11 → AIOS Supercell transformation in 3 steps.**

---

## 🎯 The 3-Step Path

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Clone Repository                                   │
│ Duration: 5 minutes                                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Bootstrap Windows 11                               │
│ Duration: 30-60 minutes (includes auto-restart)            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Deploy All Stacks                                  │
│ Duration: 15 minutes                                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    🧬 AIOS Supercell
```

---

## Step 1: Clone Repository

```powershell
# Clone with submodules
git clone --recursive https://github.com/Tecnocrat/aios-win.git C:\aios-supercell
cd C:\aios-supercell

# Verify
git submodule status
```

**What you get:**
- Complete PowerShell automation scripts
- Docker Compose configurations (via submodule)
- Documentation and guides

---

## Step 2: Bootstrap Windows 11

```powershell
# Run as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force
C:\aios-supercell\scripts\windows-bootstrap\00-master-bootstrap.ps1
```

**Automated actions:**
1. ✅ Harden OS (disable sleep, enable RDP)
2. ✅ Install PowerShell 7 + Windows Terminal
3. ✅ Enable Hyper-V and WSL2
4. ✅ **Auto-restart** (resumes after login)
5. ✅ Install Ubuntu on WSL2
6. ✅ Install Docker Desktop

**Wait for:**
- Automatic restart
- Auto-resume after login
- "Bootstrap complete!" message

---

## Step 3: Deploy All Stacks

```powershell
# Run unified deployment script
C:\aios-supercell\scripts\05-deploy-all-stacks.ps1
```

**Automated actions:**
1. ✅ Generate TLS certificates (*.lan)
2. ✅ Update Windows hosts file
3. ✅ Create Docker network
4. ✅ Deploy Traefik (ingress + TLS)
5. ✅ Deploy Observability (Prometheus, Grafana, Loki)
6. ✅ Deploy Vault (secrets management)
7. ✅ Initialize Vault with Shamir unsealing

**Services available:**
- https://traefik.lan
- https://grafana.lan
- https://prometheus.lan
- https://vault.lan
- https://loki.lan

---

## 🎉 Success Verification

```powershell
# Check all containers
docker ps --format "table {{.Names}}\t{{.Status}}"

# Expected output:
# aios-traefik       Up X minutes
# aios-prometheus    Up X minutes
# aios-grafana       Up X minutes
# aios-loki          Up X minutes
# aios-promtail      Up X minutes
# aios-node-exporter Up X minutes
# aios-cadvisor      Up X minutes
# aios-vault         Up X minutes
# aios-whoami        Up X minutes

# Test HTTPS access
curl https://traefik.lan -k
curl https://grafana.lan -k
```

---

## 🔐 Critical Post-Deployment Actions

```powershell
# 1. Backup Vault keys
Copy-Item C:\aios-supercell\config\vault-*.* -Destination D:\SecureBackup\

# 2. Change Traefik password
# Edit: C:\aios-supercell\server\stacks\ingress\docker-compose.yml
# Generate: htpasswd -nb admin YourNewPassword

# 3. Change Grafana password
# Login to https://grafana.lan → Profile → Change Password

# 4. Review Vault token
Get-Content C:\aios-supercell\config\vault-root-token.txt
```

---

## 🛠️ Day-2 Operations

### Update Server Stacks

```powershell
cd C:\aios-supercell

# Pull latest server changes
git submodule update --remote server

# Commit the update
git add server
git commit -m "Update server stacks to latest"
git push
```

### Manage Vault

```powershell
# Check status
C:\aios-supercell\scripts\vault-manager.ps1 -Action status

# Unseal (after restart)
C:\aios-supercell\scripts\vault-manager.ps1 -Action unseal

# Backup
C:\aios-supercell\scripts\vault-manager.ps1 -Action backup
```

### View Logs

```powershell
# Individual container
docker logs aios-traefik --tail 50 --follow

# All Traefik logs
docker logs aios-traefik -f

# Grafana logs
docker logs aios-grafana -f
```

### Restart Services

```powershell
# Restart single stack
cd C:\aios-supercell\server\stacks\ingress
docker compose restart

# Restart specific container
docker restart aios-traefik

# Restart all
cd C:\aios-supercell\server\stacks\ingress; docker compose restart
cd C:\aios-supercell\server\stacks\observability; docker compose restart
cd C:\aios-supercell\server\stacks\secrets; docker compose restart
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 7: Applications                                       │
│ AI Services, Databases, Custom Apps                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 6: Secrets Management (Vault)                        │
│ Policy-driven secrets, Shamir unsealing                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 5: Observability (Prometheus, Grafana, Loki)        │
│ Metrics, dashboards, logs, alerts                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: Ingress (Traefik)                                 │
│ HTTPS termination, routing, basic auth                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: Container Runtime (Docker Desktop + WSL2)         │
│ Container orchestration, networking, volumes                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: WSL2 Ubuntu                                        │
│ Linux execution layer, Docker Engine                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Windows 11 Core                                    │
│ Hardened OS, PowerShell 7, Hyper-V                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧬 Repository Architecture

```
aios-win (private) ← This machine's deployment
    ├── scripts/              PowerShell automation
    ├── docs/                 Documentation
    ├── config/               Generated configs
    ├── data/                 Persistent data
    ├── logs/                 Log files
    └── server/ (submodule)   ← Platform-agnostic stacks
            └── stacks/
                ├── ingress/
                ├── observability/
                └── secrets/
```

**Benefits:**
- **aios-win** (private): Your specific Windows 11 deployment
- **server** (public submodule): Shareable Docker stacks
- **Version pinning**: Submodule locks specific server commit
- **Independent evolution**: Update server without breaking aios-win

---

## 🔄 Common Workflows

### Fresh Clone on Another Machine

```powershell
# Clone with submodules
git clone --recursive https://github.com/Tecnocrat/aios-win.git C:\aios-supercell
cd C:\aios-supercell

# Bootstrap
C:\aios-supercell\scripts\windows-bootstrap\00-master-bootstrap.ps1

# Deploy
C:\aios-supercell\scripts\windows-bootstrap\05-deploy-all-stacks.ps1
```

### Update Configuration

```powershell
# Edit compose files
code C:\aios-supercell\server\stacks\ingress\docker-compose.yml

# Restart affected stack
cd C:\aios-supercell\server\stacks\ingress
docker compose up -d

# If in submodule, commit upstream
cd C:\aios-supercell\server
git add .
git commit -m "Update Traefik config"
git push origin main

# Update aios-win to reference new commit
cd C:\aios-supercell
git add server
git commit -m "Update server submodule"
git push
```

### Complete Teardown

```powershell
# Stop all containers
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)

# Remove networks
docker network rm aios-network

# Remove volumes (WARNING: deletes data)
docker volume prune -a

# Uninstall (if needed)
# - Docker Desktop
# - WSL2 Ubuntu: wsl --unregister Ubuntu
```

---

## 📚 Documentation Index

- **[README.md](README.md)** — Project overview
- **[QUICKSTART.md](QUICKSTART.md)** — Detailed deployment guide
- **[CHECKLIST.md](CHECKLIST.md)** — Phase-by-phase checklist
- **[WORKFLOW.md](WORKFLOW.md)** — This file (workflow reference)
- **[docs/AIOS-KNOWLEDGE-BASE.md](docs/AIOS-KNOWLEDGE-BASE.md)** — Complete architecture
- **[docs/AIOS-DEPLOYMENT-GUIDE.md](docs/AIOS-DEPLOYMENT-GUIDE.md)** — Step-by-step instructions
- **[docs/QUICK-REFERENCE.md](docs/QUICK-REFERENCE.md)** — Command cheat sheet
- **[AIOS-ORCHESTRATION-STRATEGY.md](AIOS-ORCHESTRATION-STRATEGY.md)** — Multi-repo strategy

---

## 🎯 Goals Achieved

✅ **Self-aware infrastructure** — Prometheus monitors everything  
✅ **Policy-driven secrets** — Vault manages all credentials  
✅ **Service mesh** — Traefik routes all HTTPS traffic  
✅ **Agentic behavior** — System monitors and adapts autonomously  
✅ **Reproducible** — Clone, bootstrap, deploy = supercell  
✅ **Composable** — Add services by extending Docker Compose  
✅ **Observable** — All logs and metrics centralized  

---

**The machine itself becomes an agent, not just a host for agents.** 🧬
