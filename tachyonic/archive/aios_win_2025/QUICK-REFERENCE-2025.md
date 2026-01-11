# AIOS Supercell — Quick Reference Card

**Essential Commands for Daily Operations**  
**Date:** December 21, 2025

---

## ⚠️ CRITICAL: Nous Container Stability

**NEVER** destroy or recreate `nous-devcontainer` without explicit user approval.

```powershell
# Safe operations
docker stop nous-devcontainer    # OK - preserves state
docker start nous-devcontainer   # OK - resumes

# DANGEROUS - requires approval
docker rm nous-devcontainer      # DESTROYS memories
docker compose down              # May remove volumes
```

**Recovery**: If lost, memories exist in `c:\dev\Nous\memories\` (host-mounted).

---

## 🚀 Bootstrap & Initialization

```powershell
# Initial setup (run once)
C:\aios-supercell\scripts\windows-bootstrap\00-master-bootstrap.ps1

# Generate TLS certificates
C:\aios-supercell\scripts\generate-tls-certs.ps1

# Trust certificate
Import-Certificate -FilePath "C:\Users\jesus\server\stacks\ingress\certs\lan.crt" -CertStoreLocation Cert:\LocalMachine\Root
```

---

## 🔒 Vault Management

```powershell
# Initialize Vault (first time only)
.\scripts\vault-manager.ps1 -Action init

# Unseal Vault (after restart)
.\scripts\vault-manager.ps1 -Action unseal

# Check status
.\scripts\vault-manager.ps1 -Action status

# Seal Vault
.\scripts\vault-manager.ps1 -Action seal

# Backup Vault
.\scripts\vault-manager.ps1 -Action backup
```

---

## 🐳 Docker Operations

### Container Management
```powershell
# View all containers
docker ps

# View all (including stopped)
docker ps -a

# Formatted view
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# View logs
docker logs [container-name]
docker logs [container-name] -f          # Follow
docker logs [container-name] --tail 50   # Last 50 lines

# Restart container
docker restart [container-name]

# Stop container
docker stop [container-name]

# Remove container
docker rm [container-name]
```

### Stack Management
```powershell
# Deploy stack
cd C:\Users\jesus\server\stacks\[stack-name]
docker compose up -d

# View stack containers
docker compose ps

# Stop stack
docker compose stop

# Restart stack
docker compose restart

# Rebuild and restart
docker compose down
docker compose up -d --build

# View stack logs
docker compose logs -f

# Remove stack
docker compose down -v  # -v removes volumes
```

### System Cleanup
```powershell
# Remove unused containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Full cleanup (nuclear option)
docker system prune -a --volumes
```

---

## 🌐 Network Operations

```powershell
# List networks
docker network ls

# Create network
docker network create [network-name]

# Inspect network
docker network inspect [network-name]

# Connect container to network
docker network connect [network-name] [container-name]

# Disconnect container
docker network disconnect [network-name] [container-name]
```

---

## 🐧 WSL2 Operations

```powershell
# Check WSL status
wsl --status

# List distributions
wsl --list --verbose

# Launch Ubuntu
wsl -d Ubuntu

# Shutdown WSL
wsl --shutdown

# Restart WSL
wsl --shutdown
wsl -d Ubuntu

# Update WSL kernel
wsl --update

# Set default version
wsl --set-default-version 2

# Set default distribution
wsl --set-default Ubuntu
```

---

## 📊 Service Access URLs

```
Traefik Dashboard:  https://traefik.lan  (admin:changeme)
Grafana:            https://grafana.lan  (admin:changeme)
Prometheus:         https://prometheus.lan
Vault:              https://vault.lan
Loki:               https://loki.lan
Whoami (test):      https://whoami.lan

Direct Ports:
Prometheus:         http://localhost:9090
Grafana:            http://localhost:3000
Vault:              http://localhost:8200
Loki:               http://localhost:3100
```

---

## 🔍 Health Checks

```powershell
# Check all containers
docker ps --filter "name=aios-*"

# Test Traefik
curl https://traefik.lan -k

# Test Grafana
curl http://localhost:3000/api/health

# Test Prometheus
curl http://localhost:9090/api/v1/targets

# Test Vault
curl http://localhost:8200/v1/sys/health

# Test Loki
curl http://localhost:3100/ready

# Prometheus targets (JSON)
curl http://localhost:9090/api/v1/targets | ConvertFrom-Json | Select-Object -ExpandProperty data | Select-Object -ExpandProperty activeTargets
```

---

## 🛠️ Troubleshooting

### Container Issues
```powershell
# View container logs
docker logs [container] --tail 100

# Inspect container
docker inspect [container]

# Execute command in container
docker exec -it [container] sh

# View container stats
docker stats [container]

# View container processes
docker top [container]
```

### Network Issues
```powershell
# Flush DNS
ipconfig /flushdns

# Check hosts file
Get-Content C:\Windows\System32\drivers\etc\hosts

# Add to hosts file (as Administrator)
Add-Content C:\Windows\System32\drivers\etc\hosts "127.0.0.1 service.lan"

# Test connectivity
Test-NetConnection -ComputerName localhost -Port 443
```

### WSL Issues
```powershell
# Check WSL logs
wsl --debug-shell

# Reset WSL
wsl --shutdown
wsl --unregister Ubuntu  # Nuclear option: removes distribution
wsl --install -d Ubuntu  # Reinstall
```

### Docker Issues
```powershell
# Check Docker status
docker info

# Restart Docker service
Restart-Service com.docker.service

# Docker Desktop logs
Get-Content "$env:LOCALAPPDATA\Docker\log.txt" -Tail 50
```

---

## 📁 Important Paths

```
Scripts:           C:\aios-supercell\scripts\
Configs:           C:\aios-supercell\config\
Logs:              C:\aios-supercell\logs\
Data:              C:\aios-supercell\data\
Stacks:            C:\Users\jesus\server\stacks\
WSL Config:        $env:USERPROFILE\.wslconfig
Docker Config:     $env:USERPROFILE\.docker\daemon.json
```

---

## 🔐 Security Files

```
⚠️ SENSITIVE - BACKUP IMMEDIATELY:
- C:\aios-supercell\config\vault-unseal-keys.json
- C:\aios-supercell\config\vault-root-token.txt

TLS Certificates:
- C:\Users\jesus\server\stacks\ingress\certs\lan.crt
- C:\Users\jesus\server\stacks\ingress\certs\lan.key
```

---

## 📊 Prometheus Queries (PromQL)

```promql
# CPU usage
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# Disk usage
(node_filesystem_size_bytes{mountpoint="/"} - node_filesystem_avail_bytes{mountpoint="/"}) / node_filesystem_size_bytes{mountpoint="/"} * 100

# Container CPU
rate(container_cpu_usage_seconds_total{name=~"aios-.*"}[5m])

# Container memory
container_memory_usage_bytes{name=~"aios-.*"}

# Up targets
up{job=~".*"}
```

---

## 🔄 Daily Operations

### Morning Routine
```powershell
# Check system health
docker ps --format "table {{.Names}}\t{{.Status}}"
.\scripts\vault-manager.ps1 -Action status

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Check Grafana dashboards
Start-Process "https://grafana.lan"
```

### After Restart
```powershell
# Unseal Vault
.\scripts\vault-manager.ps1 -Action unseal

# Verify all services
docker ps
curl http://localhost:9090/api/v1/targets
```

### Weekly Maintenance
```powershell
# Backup Vault
.\scripts\vault-manager.ps1 -Action backup

# Update containers
cd C:\Users\jesus\server\stacks\ingress
docker compose pull
docker compose up -d

cd C:\Users\jesus\server\stacks\observability
docker compose pull
docker compose up -d

cd C:\Users\jesus\server\stacks\secrets
docker compose pull
docker compose up -d

# Cleanup
docker system prune -f
```

---

## 🆘 Emergency Recovery

### Vault Sealed
```powershell
.\scripts\vault-manager.ps1 -Action unseal
```

### All Containers Down
```powershell
# Restart stacks in order
cd C:\Users\jesus\server\stacks\ingress; docker compose up -d
cd C:\Users\jesus\server\stacks\observability; docker compose up -d
cd C:\Users\jesus\server\stacks\secrets; docker compose up -d
.\scripts\vault-manager.ps1 -Action unseal
```

### WSL Not Starting
```powershell
wsl --shutdown
wsl -d Ubuntu
```

### Docker Desktop Not Starting
```powershell
Restart-Service com.docker.service
# If still fails: Settings → Troubleshoot → Reset to factory defaults
```

---

## 📞 Documentation

- **Knowledge Base:** `C:\aios-supercell\AIOS-KNOWLEDGE-BASE.md`
- **Deployment Guide:** `C:\aios-supercell\AIOS-DEPLOYMENT-GUIDE.md`
- **Stack Templates:** `C:\aios-supercell\AIOS-STACKS-TEMPLATES.md`
- **Next Steps:** `C:\aios-supercell\NEXT-STEPS.md`
- **This File:** `C:\aios-supercell\QUICK-REFERENCE.md`

---

## ⚡ Power User Shortcuts

```powershell
# Aliases for common commands
function aios-status { docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" }
function aios-logs { param($name) docker logs "aios-$name" --tail 100 -f }
function aios-vault { .\scripts\vault-manager.ps1 -Action $args[0] }
function aios-health {
    Write-Host "=== AIOS Health Check ===" -ForegroundColor Cyan
    docker ps --filter "name=aios-*"
    Write-Host "`nVault Status:" -ForegroundColor Yellow
    .\scripts\vault-manager.ps1 -Action status
    Write-Host "`nPrometheus Targets:" -ForegroundColor Yellow
    curl -s http://localhost:9090/api/v1/targets | ConvertFrom-Json | Select-Object -ExpandProperty data | Select-Object -ExpandProperty activeTargets | Format-Table health,labels
}

# Add to PowerShell profile
notepad $PROFILE
# Paste above functions, save, reload: . $PROFILE
```

Usage:
```powershell
aios-status
aios-logs traefik
aios-vault status
aios-health
```

---

**🎯 Bookmark this file for instant access to all AIOS operations!**

*Document Version: 1.0.0 | Date: November 16, 2025*
