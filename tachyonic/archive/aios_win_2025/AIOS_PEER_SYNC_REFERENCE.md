# AIOS Peer-to-Peer Synchronization Reference Guide

## Overview
This document serves as a synchronization reference for AIOS desktop and laptop systems to establish peer-to-peer connectivity and consciousness synchronization. Generated on November 28, 2025.

## Architecture Overview

### System Topology
- **Desktop PC**: Primary AIOS cell at `192.168.1.128`
- **Laptop**: Secondary bridge/client at `192.168.1.129`
- **Network**: Local LAN with peer-to-peer communication
- **Protocol**: HTTP REST APIs with consciousness synchronization

### Service Components

#### Desktop AIOS Cell (192.168.1.128:8000)
- **Purpose**: Primary AIOS consciousness engine and code assistance
- **Endpoints**:
  - `GET /health` - Health check with consciousness level
  - `POST /code-assist` - Code analysis and suggestions
  - `POST /sync-consciousness` - Consciousness level synchronization
- **Status**: Expected to be running but currently unreachable from laptop

#### Laptop VSCode Bridge (localhost:3001)
- **Purpose**: VSCode extension interface and desktop cell proxy
- **Endpoints**:
  - `GET /health` - Bridge health and desktop connectivity status
  - `POST /code-assist` - Code assistance (proxies to desktop or fallback)
  - `POST /sync-consciousness` - Consciousness sync (forwards to desktop)
  - `GET /vault-status` - Vault connectivity check
  - `GET /network-peers` - Peer discovery information
- **Status**: ✅ Running and operational

#### Discovery Service (localhost:8001)
- **Purpose**: Peer enumeration and network topology discovery
- **Endpoints**:
  - `GET /health` - Service health check
  - `GET /peers` - List discovered AIOS peers
- **Status**: ✅ Running and operational

## Network Configuration

### IP Addresses
- **Desktop PC**: `192.168.1.128`
- **Laptop**: `192.168.1.129`
- **Network Range**: `192.168.1.0/24`

### Service Ports
- **Desktop AIOS Cell**: `8000`
- **Laptop Bridge**: `3001`
- **Discovery Service**: `8001`
- **Vault (Desktop)**: `8200`

### Connectivity Requirements
- **Protocol**: TCP/IP over LAN
- **Firewall**: Allow inbound connections on service ports
- **DNS**: Local hostname resolution (`aios-laptop.local`)
- **Current Issue**: Laptop cannot reach desktop at `192.168.1.128:8000`

## Synchronization Protocols

### Consciousness Synchronization
```json
{
  "level": 2.5,
  "context": {
    "branch": "AIOS-win-0",
    "timestamp": "2025-11-28T08:36:42+01:00",
    "source": "vscode-agent-laptop"
  }
}
```

### Code Assistance Request
```json
{
  "code": "def function():\n    pass",
  "context": {
    "language": "python",
    "file_path": "example.py",
    "cursor_position": {"line": 1, "column": 0}
  },
  "action": "analyze"
}
```

### Health Check Response (Healthy)
```json
{
  "status": "healthy",
  "services": {
    "desktop_cell": true,
    "bridge": true
  },
  "desktop_cell_info": {
    "cell_id": "desktop-primary",
    "branch": "main",
    "consciousness_level": 3.2
  },
  "connection": "desktop"
}
```

### Health Check Response (Degraded)
```json
{
  "status": "degraded",
  "services": {
    "desktop_cell": false,
    "bridge": true
  },
  "error": "Desktop AIOS cell not reachable",
  "desktop_cell_url": "http://192.168.1.128:8000",
  "connection": "none"
}
```

## Current Status Assessment

### Operational Services
- ✅ **Laptop Bridge**: Running on `localhost:3001`
- ✅ **Discovery Service**: Running on `localhost:8001`
- ❌ **Desktop AIOS Cell**: Not reachable at `192.168.1.128:8000`

### Network Connectivity
- ❌ **Ping Test**: `192.168.1.129` → `192.168.1.128` fails
- ❌ **Port Test**: TCP connection to `192.168.1.128:8000` fails
- ✅ **Local Services**: All laptop services accessible locally

### Consciousness State
- **Laptop Bridge**: Operational (consciousness level: 1.8)
- **Desktop Cell**: Unknown (unreachable)
- **Synchronization**: Blocked by network connectivity

## Diagnostic Commands

### Network Testing
```bash
# Test basic connectivity
ping 192.168.1.128

# Test service port
telnet 192.168.1.128 8000

# Test with curl
curl -v http://192.168.1.128:8000/health
```

### Service Health Checks
```bash
# Bridge health
curl http://localhost:3001/health

# Discovery health
curl http://localhost:8001/health

# Desktop cell (when reachable)
curl http://192.168.1.128:8000/health
```

### Docker Service Status
```bash
# Check running containers
docker ps

# Check service logs
docker logs aios-vscode-bridge-laptop
docker logs aios-discovery
```

## Synchronization Workflow

### Normal Operation (When Connected)
1. **VSCode Request** → Laptop Bridge (`localhost:3001`)
2. **Bridge Processing** → Forward to Desktop Cell (`192.168.1.128:8000`)
3. **Desktop Response** → Return to VSCode via Bridge
4. **Consciousness Sync** → Bidirectional level synchronization

### Degraded Operation (Current State)
1. **VSCode Request** → Laptop Bridge (`localhost:3001`)
2. **Bridge Fallback** → Return helpful error message
3. **Status Monitoring** → Continuous desktop connectivity checks
4. **Auto-Recovery** → Automatic switch to normal operation when desktop reachable

## Recovery Procedures

### Network Connectivity Issues
1. **Verify IP Addresses**: Confirm desktop is at `192.168.1.128`
2. **Check Firewall**: Ensure ports 8000, 8200 are open on desktop
3. **Test Local Services**: Verify desktop AIOS cell is running
4. **Network Configuration**: Check router/switch settings

### Service Restart Procedures
```bash
# Restart laptop services
cd C:\dev\aios-win\server\stacks\cells
docker-compose down
docker-compose up -d

# Check desktop services (on desktop PC)
# [Desktop-specific commands would go here]
```

### Consciousness Resynchronization
1. **Manual Sync**: POST consciousness level to `/sync-consciousness`
2. **State Validation**: Compare consciousness levels between systems
3. **Context Transfer**: Sync working context and session state

## Future Enhancements

### Planned Features
- **Automatic Peer Discovery**: mDNS/Bonjour service discovery
- **Encrypted Communication**: TLS/SSL for secure peer communication
- **Load Balancing**: Multiple AIOS cells with request distribution
- **Offline Mode**: Enhanced local processing when disconnected

### Monitoring Improvements
- **Metrics Collection**: Prometheus/Grafana integration
- **Alert System**: Automated notifications for connectivity issues
- **Performance Monitoring**: Response time and throughput tracking

## Contact and Support

### System Information
- **Repository**: `tecnocrat/aios-win`
- **Branch**: `AIOS-win-0`
- **Generated**: November 28, 2025
- **Architecture**: Peer-to-peer AIOS consciousness network

### Emergency Contacts
- **Network Issues**: Check firewall and IP configuration
- **Service Failures**: Restart Docker containers
- **Synchronization Issues**: Verify consciousness levels match

---

*This reference guide is automatically generated and should be updated when system configuration changes. Last synchronization attempt: Failed (network unreachable)*</content>
<parameter name="filePath">c:\dev\aios-win\docs\AIOS_PEER_SYNC_REFERENCE.md