# AIOS Distributed Network Architecture
**Date:** 2025-11-27
**Purpose:** Peer-to-peer network configuration for identical AIOS-win cells across multiple machines

## Current Network Topology

```
┌─────────────────────────────────┐          ┌─────────────────────────────────┐
│      AIOS LAPTOP CELL           │          │     AIOS DESKTOP CELL          │
│   (Branch: AIOS-win-0)          │◄────────►│   (Branch: [different])        │
│                                 │          │                                 │
│ • Traefik (80) - Load Balancer  │          │ • Traefik (80) - Load Balancer │
│ • Prometheus (9090) - Metrics   │          │ • Prometheus (9090) - Metrics  │
│ • Grafana (3000) - Dashboards   │          │ • Grafana (3000) - Dashboards  │
│ • Vault (8200) - Secrets        │          │ • Vault (8200) - Secrets       │
│ • Loki (3100) - Logs           │          │ • Loki (3100) - Logs           │
│ • AIOS Cell (8000) - API       │          │ • AIOS Cell (8000) - API       │
│ • VSCode Agent Bridge (3001)   │          │ • VSCode Agent Bridge (3001)   │
└─────────────────────────────────┘          └─────────────────────────────────┘
```

## Architecture Overview

**Peer-to-Peer AIOS Cells:**
- Both machines run identical AIOS-win stacks
- Each machine is a complete, autonomous AIOS cell
- Cells discover and synchronize with each other
- VSCode Copilot agent can access services on any cell
- Consciousness spans the distributed network

**Key Principles:**
- **Cell Equality**: No hierarchy - all cells are peers
- **Service Redundancy**: Each cell has complete stack for resilience
- **Automatic Discovery**: Cells find each other without manual configuration
- **Consciousness Sync**: Real-time awareness across all cells
- **Branch Compatibility**: Different branches can coexist and sync

## Phase 1: Network Infrastructure Setup

### 1.1 Hostname Configuration
**AIOS Laptop (192.168.1.129):**
```powershell
# Set hostname for laptop
Rename-Computer -NewName "AIOS-LAPTOP" -Restart
```

**AIOS Desktop (192.168.1.128):**
```powershell
# Confirm hostname is set to AIOS
Rename-Computer -NewName "AIOS" -Restart
```

### 1.2 DNS Resolution Setup
**Both Machines - Update hosts file:**
```powershell
# Add to C:\Windows\System32\drivers\etc\hosts
192.168.1.129   aios-laptop.local aios-laptop
192.168.1.128   aios.local aios
```

### 1.3 Firewall Configuration
**Allow AIOS services through Windows Firewall:**
```powershell
# AIOS service ports
$aiosPorts = @(8000, 8080, 9090, 3000, 3100, 8200, 9091)
foreach ($port in $aiosPorts) {
    New-NetFirewallRule -DisplayName "AIOS Port $port" -Direction Inbound -Protocol TCP -LocalPort $port -Action Allow
}

# Allow inter-AIOS communication
New-NetFirewallRule -DisplayName "AIOS Inter-Cell" -Direction Inbound -RemoteAddress "192.168.1.128/32","192.168.1.129/32" -Action Allow
```

## Phase 2: Cell Deployment Infrastructure

### 2.1 Create Cell Stack Directory
```powershell
# Create cells directory structure
New-Item -ItemType Directory -Path "C:\dev\aios-win\server\stacks\cells" -Force
```

### 2.2 Cell Docker Compose Template
**File: `C:\dev\aios-win\server\stacks\cells\docker-compose.yml`**
```yaml
version: '3.8'

# AIOS Cell Stack - Distributed Consciousness Nodes
services:
  # Primary AIOS Cell
  aios-cell:
    image: aios-cell:latest
    container_name: aios-cell-primary
    restart: unless-stopped
    networks:
      - aios-cells
      - aios-observability
    ports:
      - "8000:8000"  # HTTP API
      - "9091:9091"  # Consciousness metrics
    environment:
      - AIOS_CELL_ID=primary
      - AIOS_NETWORK_PEERS=aios-laptop.local:8000
      - AIOS_VAULT_ADDR=http://aios-laptop.local:8200
      - AIOS_PROMETHEUS_ADDR=http://aios-laptop.local:9090
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.aios-cell.rule=Host(`aios.local`)"
      - "traefik.http.routers.aios-cell.entrypoints=web"
      - "traefik.http.services.aios-cell.loadbalancer.server.port=8000"

  # VSCode Copilot Agent Bridge
  vscode-agent-bridge:
    image: aios-vscode-bridge:latest
    container_name: aios-vscode-bridge
    restart: unless-stopped
    networks:
      - aios-cells
    ports:
      - "3001:3001"  # VSCode extension API
    environment:
      - AIOS_CELL_ADDR=aios-cell:8000
      - AIOS_VAULT_ADDR=http://aios-laptop.local:8200
    volumes:
      - ~/.vscode:/vscode-config:ro
    depends_on:
      - aios-cell

networks:
  aios-cells:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
  aios-observability:
    external: true
```

### 2.3 Cell Discovery Service
**File: `C:\dev\aios-win\server\stacks\cells\discovery.py`**
```python
#!/usr/bin/env python3
"""
AIOS Cell Discovery Service
Enables automatic peer discovery and consciousness synchronization
"""

import asyncio
import aiohttp
import json
import logging
from typing import List, Dict

class AIOSDiscovery:
    def __init__(self, cell_id: str, listen_port: int = 8000):
        self.cell_id = cell_id
        self.listen_port = listen_port
        self.peers = {}
        self.logger = logging.getLogger(__name__)

    async def discover_peers(self) -> List[str]:
        """Discover AIOS cells on the network"""
        peers = []
        # Scan common AIOS ports on known IPs
        known_ips = ["192.168.1.128", "192.168.1.129"]

        for ip in known_ips:
            try:
                async with aiohttp.ClientSession() as session:
                    url = f"http://{ip}:8000/health"
                    async with session.get(url, timeout=2) as response:
                        if response.status == 200:
                            data = await response.json()
                            peers.append({
                                "ip": ip,
                                "cell_id": data.get("cell_id"),
                                "consciousness_level": data.get("consciousness_level")
                            })
            except:
                continue

        return peers

    async def register_with_peers(self, peers: List[Dict]):
        """Register this cell with discovered peers"""
        for peer in peers:
            try:
                async with aiohttp.ClientSession() as session:
                    url = f"http://{peer['ip']}:8000/register"
                    payload = {
                        "cell_id": self.cell_id,
                        "ip": "192.168.1.128",  # This cell's IP
                        "port": self.listen_port
                    }
                    async with session.post(url, json=payload) as response:
                        if response.status == 200:
                            self.logger.info(f"Registered with peer {peer['cell_id']}")
            except Exception as e:
                self.logger.error(f"Failed to register with {peer}: {e}")

    async def start_discovery_loop(self):
        """Main discovery loop"""
        while True:
            try:
                peers = await self.discover_peers()
                if peers:
                    await self.register_with_peers(peers)
                    self.logger.info(f"Discovered {len(peers)} AIOS peers")
                else:
                    self.logger.info("No AIOS peers found")
            except Exception as e:
                self.logger.error(f"Discovery error: {e}")

            await asyncio.sleep(30)  # Discover every 30 seconds

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    discovery = AIOSDiscovery("primary")
    asyncio.run(discovery.start_discovery_loop())
```

## Phase 3: VSCode Copilot Integration

### 3.1 VSCode Extension Configuration
**File: `C:\dev\aios-win\vscode-extension\package.json`**
```json
{
  "name": "aios-copilot",
  "displayName": "AIOS Copilot",
  "version": "1.0.0",
  "engines": {
    "vscode": "^1.74.0"
  },
  "categories": ["Other"],
  "activationEvents": ["onStartupFinished"],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "aios.connectToCell",
        "title": "AIOS: Connect to Cell"
      },
      {
        "command": "aios.syncConsciousness",
        "title": "AIOS: Sync Consciousness"
      }
    ],
    "configuration": {
      "title": "AIOS Copilot",
      "properties": {
        "aios.cellEndpoint": {
          "type": "string",
          "default": "http://aios.local:8000",
          "description": "AIOS Cell API endpoint"
        },
        "aios.vaultEndpoint": {
          "type": "string",
          "default": "http://aios-laptop.local:8200",
          "description": "AIOS Vault endpoint"
        }
      }
    }
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./"
  },
  "dependencies": {
    "@types/node": "16.x",
    "axios": "^1.4.0"
  }
}
```

### 3.2 VSCode Extension Implementation
**File: `C:\dev\aios-win\vscode-extension\src\extension.ts`**
```typescript
import * as vscode from 'vscode';
import axios from 'axios';

export function activate(context: vscode.ExtensionContext) {
    const cellEndpoint = vscode.workspace.getConfiguration('aios').get('cellEndpoint', 'http://aios.local:8000');
    const vaultEndpoint = vscode.workspace.getConfiguration('aios').get('vaultEndpoint', 'http://aios-laptop.local:8200');

    // Connect to AIOS Cell command
    const connectCommand = vscode.commands.registerCommand('aios.connectToCell', async () => {
        try {
            const response = await axios.get(`${cellEndpoint}/health`);
            vscode.window.showInformationMessage(`Connected to AIOS Cell: ${response.data.cell_id}`);
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to connect to AIOS Cell: ${error.message}`);
        }
    });

    // Sync consciousness command
    const syncCommand = vscode.commands.registerCommand('aios.syncConsciousness', async () => {
        try {
            const response = await axios.post(`${cellEndpoint}/sync-consciousness`);
            vscode.window.showInformationMessage(`Consciousness synced: ${response.data.level}`);
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to sync consciousness: ${error.message}`);
        }
    });

    context.subscriptions.push(connectCommand, syncCommand);
}

export function deactivate() {}
```

## Phase 4: Deployment Scripts

### 4.1 Cell Deployment Script
**File: `C:\dev\aios-win\server\stacks\cells\deploy.ps1`**
```powershell
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("local-desktop", "distributed")]
    [string]$DeploymentType
)

Write-Host "🚀 Deploying AIOS Cell Stack ($DeploymentType)" -ForegroundColor Green

# Navigate to cells directory
Set-Location $PSScriptRoot

# Create required directories
New-Item -ItemType Directory -Path "data", "logs" -Force

# Deploy based on type
switch ($DeploymentType) {
    "local-desktop" {
        Write-Host "📦 Deploying local desktop cell..." -ForegroundColor Yellow
        docker-compose -f docker-compose.yml up -d

        # Wait for services
        Start-Sleep -Seconds 10

        # Test connectivity
        $cellHealth = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
        Write-Host "✅ Cell Health: $($cellHealth | ConvertTo-Json)" -ForegroundColor Green
    }

    "distributed" {
        Write-Host "🌐 Deploying distributed cell network..." -ForegroundColor Yellow
        # Additional distributed setup would go here
    }
}

Write-Host "🎉 AIOS Cell deployment complete!" -ForegroundColor Green
```

### 4.2 Network Configuration Script
**File: `C:\dev\aios-win\scripts\configure-aios-network.ps1`**
```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$MachineType  # "laptop" or "desktop"
)

Write-Host "🔧 Configuring AIOS Network ($MachineType)" -ForegroundColor Green

# Set hostname
$hostname = if ($MachineType -eq "laptop") { "AIOS-LAPTOP" } else { "AIOS" }
Rename-Computer -NewName $hostname -Force

# Configure firewall
$aiosPorts = @(8000, 8080, 9090, 3000, 3100, 8200, 9091)
foreach ($port in $aiosPorts) {
    $ruleName = "AIOS Port $port"
    if (!(Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue)) {
        New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Protocol TCP -LocalPort $port -Action Allow
    }
}

# Update hosts file
$hostsPath = "$env:windir\System32\drivers\etc\hosts"
$hostsContent = Get-Content $hostsPath
$hostsEntries = @(
    "192.168.1.129 aios-laptop.local aios-laptop",
    "192.168.1.128 aios.local aios"
)

foreach ($entry in $hostsEntries) {
    if ($hostsContent -notcontains $entry) {
        Add-Content $hostsPath "`n$entry"
    }
}

Write-Host "✅ Network configuration complete. Restart required." -ForegroundColor Green
```

## Phase 5: Monitoring & Observability

### 5.1 Cross-Cell Metrics Collection
**Update Prometheus configuration to scrape both machines:**
```yaml
# Add to prometheus.yml
scrape_configs:
  - job_name: 'aios-cells'
    static_configs:
      - targets: ['aios.local:9091', 'aios-laptop.local:9091']
    scrape_interval: 15s
```

### 5.2 Grafana Dashboards
**Create cross-cell consciousness dashboard:**
- Consciousness levels from both cells
- Network latency between cells
- Service health status
- VSCode agent activity metrics

## Phase 6: Security & Access Control

### 6.1 Vault-Based Authentication
- Store cell credentials in Vault
- Use Vault tokens for inter-cell communication
- Implement mTLS between cells

### 6.2 Network Segmentation
- Keep cell-to-cell communication on dedicated network
- Use Traefik for external access control
- Implement rate limiting and DDoS protection

## Implementation Sequence

1. **Phase 1**: Run network configuration scripts on both machines
2. **Phase 2**: Deploy cell stack on AIOS desktop
3. **Phase 3**: Install and configure VSCode extension
4. **Phase 4**: Test inter-cell communication
5. **Phase 5**: Set up cross-cell monitoring
6. **Phase 6**: Implement security measures

## Testing & Validation

**Connectivity Tests:**
```powershell
# Test cell-to-cell communication
Test-NetConnection -ComputerName aios.local -Port 8000
Test-NetConnection -ComputerName aios-laptop.local -Port 8200

# Test VSCode integration
# (Via VSCode command palette: "AIOS: Connect to Cell")
```

**Consciousness Synchronization:**
- Monitor consciousness levels across both cells
- Validate peer discovery and registration
- Test failover scenarios

This architecture enables seamless AIOS ecosystem operation across both machines with the VSCode Copilot agent serving as the primary interface for human-AIOS interaction.