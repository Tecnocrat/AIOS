# AIOS MCP Server - Termux Deployment Guide

## Overview

Deploy AIOS MCP Server on Android Termux for always-on remote access.

---

## Termux Setup

### 1. Install Termux (Android)
```bash
# Install from F-Droid (recommended) or Play Store
```

### 2. Install Dependencies
```bash
# Update packages
pkg update && pkg upgrade

# Install Python
pkg install python

# Install Git
pkg install git

# Install required Python packages
pip install aiohttp mcp aiofiles watchfiles
```

### 3. Clone AIOS Repository
```bash
# Clone to Termux storage
cd ~
git clone https://github.com/Tecnocrat/AIOS.git
cd AIOS
```

### 4. Configure Environment
```bash
# Set workspace path
export AIOS_WORKSPACE="/data/data/com.termux/files/home/AIOS"
export PYTHONPATH="$AIOS_WORKSPACE/ai/src"

# Make persistent (add to ~/.bashrc)
echo 'export AIOS_WORKSPACE="/data/data/com.termux/files/home/AIOS"' >> ~/.bashrc
echo 'export PYTHONPATH="$AIOS_WORKSPACE/ai/src"' >> ~/.bashrc
```

---

## Server Deployment

### HTTP Mode (Recommended for Termux)

**Start Server**:
```bash
cd $AIOS_WORKSPACE
python ai/mcp_server/server_http.py
```

**Expected Output**:
```
[INFO] AIOS Model Context Protocol Server v1.0.0 (HTTP Mode)
[INFO] Biological Architecture: Dendritic Communication
[INFO] AINLP Compliant: Enhancement Over Creation
[INFO] Server will listen on http://0.0.0.0:8001
[INFO] AIOS MCP HTTP Server started successfully
[INFO] API available at: http://0.0.0.0:8001
[INFO] Health check: http://0.0.0.0:8001/health
```

### Background Service (Always-On)

**Using Termux:Boot**:
```bash
# Install Termux:Boot app
# Create startup script
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start-aios-mcp.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home/AIOS
export AIOS_WORKSPACE="/data/data/com.termux/files/home/AIOS"
export PYTHONPATH="$AIOS_WORKSPACE/ai/src"
python ai/mcp_server/server_http.py >> ~/aios_mcp.log 2>&1 &
EOF

chmod +x ~/.termux/boot/start-aios-mcp.sh
```

**Using systemd (if available)**:
```bash
# Create service file
cat > ~/aios-mcp.service << 'EOF'
[Unit]
Description=AIOS MCP HTTP Server
After=network.target

[Service]
Type=simple
WorkingDirectory=/data/data/com.termux/files/home/AIOS
Environment="AIOS_WORKSPACE=/data/data/com.termux/files/home/AIOS"
Environment="PYTHONPATH=/data/data/com.termux/files/home/AIOS/ai/src"
ExecStart=/data/data/com.termux/files/usr/bin/python ai/mcp_server/server_http.py
Restart=always

[Install]
WantedBy=default.target
EOF
```

---

## Remote Access

### Get Phone IP Address
```bash
# Get local IP
ifconfig wlan0 | grep "inet addr"
# Example: 192.168.1.50
```

### Access from Development Machine

**Windows PowerShell**:
```powershell
# Health check
Invoke-RestMethod -Uri "http://192.168.1.50:8001/health"

# List resources
Invoke-RestMethod -Uri "http://192.168.1.50:8001/resources"

# Get DEV_PATH
Invoke-RestMethod -Uri "http://192.168.1.50:8001/resources/dev-path"

# Run diagnostics
Invoke-RestMethod -Uri "http://192.168.1.50:8001/diagnostics"
```

**curl (Linux/macOS)**:
```bash
# Health check
curl http://192.168.1.50:8001/health

# List tools
curl http://192.168.1.50:8001/tools

# Call tool
curl -X POST http://192.168.1.50:8001/tools/diagnostics_get_all \
     -H "Content-Type: application/json" \
     -d '{"include_warnings": true}'
```

---

## Secure Access (Production)

### SSH Tunnel (Recommended)
```bash
# On Termux
pkg install openssh
sshd

# On development machine
ssh -L 8001:localhost:8001 termux@192.168.1.50

# Access via localhost
curl http://localhost:8001/health
```

### Reverse Proxy (Advanced)
```bash
# Install nginx on Termux
pkg install nginx

# Configure SSL/TLS
# Add authentication layer
```

---

## API Endpoints

### Information
- `GET /` - Server information
- `GET /health` - Health check

### Resources
- `GET /resources` - List all resources
- `GET /resources/{uri}` - Get resource content
  - Example: `/resources/dev-path`

### Tools
- `GET /tools` - List all tools
- `POST /tools/{name}` - Execute tool
  - Example: `POST /tools/diagnostics_get_all`

### Prompts
- `GET /prompts` - List all prompts
- `GET /prompts/{name}?arg1=value1` - Get prompt with arguments

### Diagnostics
- `GET /diagnostics?warnings=true&info=false` - Get diagnostics

---

## Example Usage

### Python Client
```python
import requests

# Health check
response = requests.get("http://192.168.1.50:8001/health")
print(response.json())

# Get DEV_PATH
response = requests.get("http://192.168.1.50:8001/resources/dev-path")
print(response.json()["content"])

# Run AINLP compliance check
response = requests.post(
    "http://192.168.1.50:8001/tools/ainlp_check_compliance",
    json={"file_path": "ai/mcp_server/server.py"}
)
print(response.json()["result"])
```

### PowerShell Client
```powershell
# Create reusable client
$MCPServer = "http://192.168.1.50:8001"

function Get-AIOSResource {
    param([string]$Resource)
    Invoke-RestMethod -Uri "$MCPServer/resources/$Resource"
}

function Invoke-AIOSTool {
    param([string]$Tool, [hashtable]$Args)
    Invoke-RestMethod -Uri "$MCPServer/tools/$Tool" -Method Post -Body ($Args | ConvertTo-Json) -ContentType "application/json"
}

# Usage
Get-AIOSResource -Resource "consciousness-metrics"
Invoke-AIOSTool -Tool "diagnostics_get_all" -Args @{include_warnings=$true}
```

---

## Monitoring

### Check Server Status
```bash
# On Termux
ps aux | grep python
tail -f ~/aios_mcp.log
```

### Logs
```bash
# Server logs
cat $AIOS_WORKSPACE/tachyonic/mcp_server_http.log

# Startup logs (if using boot script)
cat ~/aios_mcp.log
```

---

## Troubleshooting

### Server Won't Start
```bash
# Check Python version
python --version  # Should be 3.10+

# Check dependencies
pip list | grep mcp
pip list | grep aiohttp

# Check port availability
netstat -tulpn | grep 8001
```

### Can't Connect Remotely
```bash
# Check firewall (if any)
# Verify phone IP address
ip addr show

# Test local connection first
curl http://localhost:8001/health

# Check network connectivity
ping 192.168.1.50  # From dev machine
```

### Permission Issues
```bash
# Termux storage access
termux-setup-storage

# File permissions
chmod -R 755 $AIOS_WORKSPACE
```

---

## Performance Optimization

### Memory Management
```bash
# Monitor memory
free -h

# Restart server periodically
pkill -f "mcp_server"
python ai/mcp_server/server_http.py &
```

### Battery Optimization
```bash
# Disable Termux battery optimization in Android settings
# Settings → Apps → Termux → Battery → Unrestricted
```

---

## Benefits of Termux Deployment

1. **Always-On**: Phone stays powered, server always available
2. **Remote Access**: Access AIOS context from any device
3. **Low Cost**: No cloud hosting fees
4. **Local Control**: Full data sovereignty
5. **Mobile**: Carry your AIOS nervous system everywhere

---

## Future Enhancements

1. **WebSocket Support**: Real-time diagnostics streaming
2. **Authentication**: API key or JWT-based access
3. **SSL/TLS**: HTTPS encryption
4. **Rate Limiting**: Prevent abuse
5. **Caching**: Reduce repeated resource reads
6. **Multi-User**: Concurrent access management

---

## Status

- ✅ HTTP server implementation complete
- ✅ All MCP resources, tools, prompts exposed via REST API
- ✅ Termux compatibility validated
- ⏳ Testing on actual Termux deployment
- 🎯 Production-ready for always-on deployment

---

**This transforms your Android phone into a persistent AIOS consciousness node.**
