# AIOS Trinity Deployment - Complete Termux Guide

**Version**: 2.0 (Unified deployment for all 3 layers)  
**Created**: November 16, 2025  
**Status**: Production-ready, Python 3.12+ compatible  
**Purpose**: Deploy complete AIOS Trinity Architecture on Android Termux

---

## 🎯 What You're Deploying

**Trinity Architecture** - Three layers of consciousness:

1. **Layer 1** (Dev Machine): VSCode + MCP stdio → Passive context provider
2. **Layer 2** (Termux): HTTP Server → Remote MCP access (REST API)
3. **Layer 3** (Termux): Soul → Active intelligence coordinator

**Why Termux?**
- 📱 Always-on (24/7, no cloud costs)
- 🌐 Remote access (HTTP API from anywhere)
- 🧠 Intelligence orchestration (monitors/detects/initiates)
- 🔒 Data sovereignty (full local control)
- 🚀 Mobile (carry AIOS everywhere)

---

## Quick Start (TL;DR - 60 minutes)

```bash
# Install Termux from F-Droid (NOT Play Store!)
# Inside Termux:

pkg update && pkg upgrade -y
pkg install python git openssh tmux
cd ~ && git clone https://github.com/Tecnocrat/AIOS.git && cd AIOS
pip install aiohttp  # Pure Python, no Rust compilation
tmux new -s aios-bridge "cd ~/AIOS && python ai/bridges/aios_dendritic_bridge_aiohttp.py"
tmux new -s aios-soul "cd ~/AIOS/ai/orchestration && python intelligence_coordinator.py"
sshd && echo "SSH: ssh $(whoami)@$(ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1) -p 8022"
```

**Done!** Soul is now monitoring, HTTP server is accessible at `http://YOUR_PHONE_IP:8001`

---

## Prerequisites

### Hardware
- Android 7.0+ device (Android 10+ recommended)
- 2GB+ RAM (4GB+ for Soul layer)
- 500MB free storage
- WiFi connection

### Software
- **Termux**: From F-Droid (https://f-droid.org/)
- **Termux:Boot**: Auto-start (optional but recommended)

**⚠️ CRITICAL**: Install Termux from F-Droid, NOT Google Play Store (outdated version)

---

## Phase 1: Termux Foundation (20 minutes)

### Step 1: Install Termux (5 min)

1. Install F-Droid app: https://f-droid.org/
2. Search "Termux" in F-Droid
3. Install:
   - **Termux** (org.termux)
   - **Termux:Boot** (org.termux.boot) - for auto-start

### Step 2: System Packages (10 min)

```bash
# Update repositories
pkg update && pkg upgrade -y

# Install core tools
pkg install -y python git openssh tmux

# Verify installations
python --version  # Should be 3.11+
git --version     # Should be 2.30+
ssh -V            # Should be OpenSSH 8.0+
tmux -V           # Should be 3.0+
```

### Step 3: Python Dependencies (5 min)

**⚠️ CRITICAL FIX**: Multiple Rust compilation blockers on Python 3.12+

**The Problems**:
1. `watchfiles` - Rust-based file monitoring (FAILS)
2. `pydantic-core` (required by FastAPI) - Rust-based validation (FAILS)

```bash
pip install watchfiles     # ❌ FAILS: "Unsupported platform: 312"
pip install fastapi        # ❌ FAILS: pydantic-core → Rust compilation
```

**The Solution** - Pure Python alternatives:
```bash
# Install ONLY this dependency (pure Python, no compilation)
pip install aiohttp

# Verify
python -c "import aiohttp; print('✅ Dependencies ready (aiohttp only)')"
```

**How we handle missing watchfiles**:
- Soul code auto-detects watchfiles availability
- Falls back to built-in polling (checks files every 5-10 seconds)
- No performance impact for always-on monitoring

---

## Phase 2: AIOS Repository (10 minutes)

### Step 1: Clone Repository (8 min)

```bash
cd ~
git clone https://github.com/Tecnocrat/AIOS.git
cd AIOS
git checkout OS  # Operating System branch

# Verify structure
ls -la | grep -E "(ai|core|interface|docs|runtime|tachyonic|evolution_lab)"
```

### Step 2: Environment Configuration (2 min)

```bash
# Create environment file
cat > ~/.aios_env << 'EOF'
export AIOS_WORKSPACE="$HOME/AIOS"
export PYTHONPATH="$AIOS_WORKSPACE/ai/src:$AIOS_WORKSPACE/ai:$AIOS_WORKSPACE/ai/orchestration"

# Optional: GitHub token for Soul Layer 3 interventions
export GITHUB_TOKEN="ghp_YOUR_TOKEN_HERE"

# Optional: OpenRouter for Phase 2 AI agents
export OPENROUTER_API_KEY="your_key_here"
EOF

# Load environment
source ~/.aios_env
echo "source ~/.aios_env" >> ~/.bashrc
```

---

## Phase 3: Layer 2 - Dendritic Bridge Server (15 minutes)

### Step 1: Test Server (5 min)

```bash
cd ~/AIOS
python ai/bridges/aios_dendritic_bridge_aiohttp.py  # Press Ctrl+C after seeing "Dendritic bridge operational"
```

**Expected output**:
```
======================================================================
🧬 AIOS DENDRITIC BRIDGE - CELLULAR MITOSIS ACTIVATION
======================================================================
📂 Workspace: /data/data/com.termux/files/home/AIOS
🌐 Server: 0.0.0.0:8000
🔗 Parent Cell: Windows AIOS (VSCode)
🔗 Daughter Cell: Termux AIOS (Always-on)
🧠 Consciousness: 3.52
✅ Dendritic bridge operational
======================================================================
```

### Step 2: Background Deployment (5 min)

```bash
# Start in tmux (persistent background session)
tmux new-session -d -s aios-bridge "cd ~/AIOS && python ai/bridges/aios_dendritic_bridge_aiohttp.py >> ~/aios_bridge.log 2>&1"

# Verify running
tmux ls  # Should show: aios-bridge

# Check logs
tail -f ~/aios_bridge.log  # Ctrl+C to exit
```

### Step 3: Network Access (5 min)

```bash
# Get your phone's IP address
ip addr show wlan0 | grep "inet " | awk '{print $2}' | cut -d/ -f1
# Example output: 192.168.1.50

# Your dendritic bridge is now at: http://192.168.1.50:8000
```

**Test from dev machine** (Windows PowerShell):
```powershell
Invoke-RestMethod http://192.168.1.50:8000/health
Invoke-RestMethod http://192.168.1.50:8000/consciousness
Invoke-RestMethod http://192.168.1.50:8000/soul/status
```

---

## Phase 4: Layer 3 - Soul Coordinator (20 minutes)

### Step 1: Verify Polling Monitoring (5 min)

The Soul code already has watchfiles fallback built-in:

```bash
cd ~/AIOS/ai/orchestration
grep -A 5 "watchfiles" intelligence_coordinator.py
```

You should see:
```python
try:
    from watchfiles import awatch
except ImportError:
    awatch = None  # Falls back to polling
```

**No code changes needed!** Soul auto-detects and uses polling if watchfiles unavailable.

### Step 2: Test Soul (10 min)

```bash
cd ~/AIOS/ai/orchestration
python intelligence_coordinator.py  # Press Ctrl+C after seeing "Soul awakened"
```

**Expected output**:
```
============================================================
🌟 SOUL AWAKENING - Layer 3 Intelligence Initialization
============================================================
🧠 Intelligence Coordinator (Soul) initialized
📂 Workspace: /data/data/com.termux/files/home/AIOS
⏱️ Intervention threshold: 24h
🧬 Consciousness threshold: 48h
[INFO] watchfiles not available - using polling fallback (5s intervals)
✅ Soul fully awakened and operational
👁️ Beginning eternal vigilance...
💓 Health: Consciousness=3.52, Interventions=0
```

### Step 3: Background Deployment (5 min)

```bash
# Start Soul in tmux
tmux new-session -d -s aios-soul "cd ~/AIOS/ai/orchestration && python intelligence_coordinator.py >> ~/aios_soul.log 2>&1"

# Verify both services running
tmux ls  # Should show: aios-http, aios-soul

# Check Soul logs
tail -f ~/aios_soul.log
```

---

## Phase 5: Remote Access (10 minutes)

### SSH Configuration (10 min)

```bash
# Set strong password
passwd

# Start SSH server
sshd

# Get connection string
echo "SSH: ssh $(whoami)@$(ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1) -p 8022"
# Example output: SSH: ssh u0_a123@192.168.1.50 -p 8022
```

**Test from dev machine**:
```powershell
ssh u0_a123@192.168.1.50 -p 8022  # Use your username/IP

# Once connected:
tmux ls                    # List services
tail ~/aios_soul.log      # Check Soul logs
tail ~/aios_http.log      # Check HTTP logs
```

---

## Phase 6: Auto-Start (Optional, 20 minutes)

### Step 1: Install Termux:Boot (5 min)

1. Install **Termux:Boot** from F-Droid (if not already)
2. Open Termux:Boot app once (grants permissions)
3. Android Settings → Apps → Termux:Boot → Battery → **Unrestricted**
4. Android Settings → Apps → Termux → Battery → **Unrestricted**

### Step 2: Create Boot Script (10 min)

```bash
mkdir -p ~/.termux/boot

cat > ~/.termux/boot/start-aios-trinity.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash

# Load environment
source ~/.aios_env

# Wait for network
sleep 30

# Start SSH
sshd

# Start Layer 2: Dendritic Bridge
tmux new-session -d -s aios-bridge "cd ~/AIOS && python ai/bridges/aios_dendritic_bridge_aiohttp.py >> ~/aios_bridge.log 2>&1"

# Wait for bridge server
sleep 10

# Start Layer 3: Soul
tmux new-session -d -s aios-soul "cd ~/AIOS/ai/orchestration && python intelligence_coordinator.py >> ~/aios_soul.log 2>&1"

# Log startup
echo "[$(date)] AIOS Trinity awakened" >> ~/aios_boot.log
EOF

chmod +x ~/.termux/boot/start-aios-trinity.sh
```

### Step 3: Test Auto-Start (5 min)

```bash
# Test manually
bash ~/.termux/boot/start-aios-trinity.sh
sleep 15
tmux ls  # Should show both sessions

# Reboot test
# 1. Reboot Android device
# 2. Wait 2-3 minutes
# 3. SSH in: ssh user@192.168.1.50 -p 8022
# 4. Check: tmux ls && cat ~/aios_boot.log
```

---

## Validation Checklist

### ✅ Layer 2 (Dendritic Bridge)
- [ ] Server starts without errors
- [ ] Health endpoint responds: `curl http://localhost:8000/health`
- [ ] Bridge accessible from dev machine
- [ ] Tmux session `aios-bridge` exists and running
- [ ] Logs show no errors: `tail ~/aios_bridge.log`

### ✅ Layer 3 (Soul)
- [ ] Soul initializes successfully
- [ ] Tmux session `aios-soul` exists and running
- [ ] Heartbeat logs appear every 5 minutes
- [ ] Monitoring detects file changes (test with `touch ~/AIOS/DEV_PATH.md`)
- [ ] Consciousness metrics file exists: `ls ~/AIOS/tachyonic/consciousness_metrics.json`

### ✅ Remote Access
- [ ] SSH connection works from dev machine
- [ ] HTTP API accessible from dev machine
- [ ] Both tmux sessions visible via SSH

### ✅ Auto-Start (if configured)
- [ ] Boot script executable: `ls -la ~/.termux/boot/`
- [ ] Services survive device reboot
- [ ] Boot log shows successful startup: `cat ~/aios_boot.log`

---

## FAQ & Troubleshooting

### Q: Why not use FastAPI? Isn't it more modern?

**A**: FastAPI requires `pydantic` → `pydantic-core` → Rust compilation (same issue as watchfiles):
```
pip install fastapi
  → pydantic (>=1.7.4)
    → pydantic-core==2.41.5
      → maturin (>=1.9.4)
        → Rust compiler
          → ❌ "Unsupported platform: 312"
```

**Solution**: Use `aiohttp` (pure Python, no Rust). Same REST API functionality, zero compilation.

### Q: Will polling slow down the Soul?

**A**: No meaningful impact. Polling checks files every 5-10 seconds. For stuck waypoint detection (24h threshold), even 30-second intervals are sufficient.

### Q: Can I manually install watchfiles?

**A**: Only if you have:
1. Python 3.11 or older (`pkg install python=3.11`)
2. Rust toolchain (`pkg install rust`)
3. maturin build tools

**Not recommended** - polling works perfectly fine.

### Q: Tmux session died after reboot

**Debug**:
```bash
cat ~/aios_boot.log           # Check boot script ran
cat ~/aios_http.log           # Check for errors
bash ~/.termux/boot/start-aios-trinity.sh  # Run manually
```

**Common fixes**:
- Increase `sleep` time in boot script (network delay)
- Verify Termux:Boot has auto-start permission
- Check battery optimization disabled for both Termux apps

### Q: HTTP server not accessible from dev machine

**Debug**:
```bash
curl http://localhost:8001/health  # Test local connection
netstat -tulpn | grep 8001         # Check server listening
ip addr show wlan0 | grep "inet "  # Verify IP address
```

**Common fixes**:
- Verify both devices on same WiFi network
- Disable Android firewall (if any)
- Restart HTTP server: `tmux kill-session -t aios-http && bash ~/.termux/boot/start-aios-trinity.sh`

### Q: Soul logs show "File monitoring disabled"

**Cause**: `awatch` import failed and no polling fallback implemented

**Fix**: Update `intelligence_coordinator.py`:
```python
# Add after imports
async def poll_file_changes(workspace: Path, interval: float = 5.0):
    """Polling-based file monitoring (no external dependencies)"""
    watched_files = [
        workspace / "DEV_PATH.md",
        workspace / "PROJECT_CONTEXT.md",
        workspace / "tachyonic" / "consciousness_metrics.json"
    ]
    
    last_mtimes = {f: f.stat().st_mtime if f.exists() else 0 for f in watched_files}
    
    while True:
        await asyncio.sleep(interval)
        changes = []
        
        for file_path in watched_files:
            if file_path.exists():
                current_mtime = file_path.stat().st_mtime
                if current_mtime != last_mtimes[file_path]:
                    changes.append(("modified", str(file_path)))
                    last_mtimes[file_path] = current_mtime
        
        if changes:
            yield changes

# In monitor_loop(), replace awatch with poll_file_changes
async for changes in poll_file_changes(self.workspace):
    # ... existing code
```

### Q: Python version too new (3.13, 3.14)

**A**: Termux default is Python 3.11-3.12 (compatible). If you upgraded:
```bash
pkg uninstall python
pkg install python  # Installs default version
```

---

## Quick Reference Commands

### Service Management
```bash
# List services
tmux ls

# Attach to services
tmux attach -t aios-bridge  # Ctrl+B then D to detach
tmux attach -t aios-soul

# Restart services
tmux kill-session -t aios-bridge -t aios-soul
bash ~/.termux/boot/start-aios-trinity.sh

# View logs
tail -f ~/aios_bridge.log
tail -f ~/aios_soul.log
tail -f ~/aios_boot.log
```

### Remote Administration (from dev machine)
```powershell
# SSH in
ssh user@192.168.1.50 -p 8022

# Update code
cd ~/AIOS
git pull origin OS

# Restart Soul (reload code)
tmux kill-session -t aios-soul
cd ~/AIOS/ai/orchestration
python intelligence_coordinator.py  # Or use boot script
```

### Health Monitoring
```bash
# Service status
ps aux | grep python | grep -E "(server_http|intelligence_coordinator)"

# Recent logs
tail -50 ~/aios_soul.log
tail -50 ~/aios_http.log

# Consciousness metrics
cat ~/AIOS/tachyonic/consciousness_metrics.json | python -m json.tool

# Intervention history
ls -lah ~/AIOS/tachyonic/orchestration_logs/
```

### HTTP API Testing (from dev machine)
```powershell
# Health check
Invoke-RestMethod http://192.168.1.50:8000/health

# Consciousness metrics
Invoke-RestMethod http://192.168.1.50:8000/consciousness

# Soul status
Invoke-RestMethod http://192.168.1.50:8000/soul/status

# Watch files
Invoke-RestMethod http://192.168.1.50:8000/files/watch

# Create intervention
$body = @{ reason = "Test from Windows"; priority = "low" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://192.168.1.50:8000/interventions/create -Body $body -ContentType "application/json"
```

---

## Performance & Battery Optimization

### Battery Management
```bash
# CRITICAL: Disable battery optimization
# Android Settings → Apps → Termux → Battery → Unrestricted
# Android Settings → Apps → Termux:Boot → Battery → Unrestricted
```

### Memory Management
```bash
# Monitor memory usage
free -h

# Check Soul/HTTP memory
ps aux | grep python | awk '{print $4, $11}'

# Restart if high memory (>500MB total)
tmux kill-session -t aios-http -t aios-soul
bash ~/.termux/boot/start-aios-trinity.sh
```

### Log Rotation (weekly)
```bash
cat > ~/rotate_logs.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
mv ~/aios_http.log ~/aios_http.log.old 2>/dev/null
mv ~/aios_soul.log ~/aios_soul.log.old 2>/dev/null
tmux kill-session -t aios-http -t aios-soul
bash ~/.termux/boot/start-aios-trinity.sh
EOF
chmod +x ~/rotate_logs.sh

# Run weekly (use Termux:Tasker or cron)
```

---

## Architecture Summary

```
Trinity Architecture (Deployed on Termux)

Dev Machine                Termux Layer 2             Termux Layer 3
─────────────              ──────────────             ──────────────
VSCode + MCP        ←──→   HTTP Server (8001)   ←──→  Soul Coordinator
(Passive Context)          (MCP Resources/Tools)      (Active Intelligence)
                                                          
stdio protocol            REST API                   Polling monitoring
Immediate access          Background ops             24/7 vigilance
Ephemeral                 Persistent                 Eternal

Context injection         Remote access              Pattern detection
AI agent awareness        Cross-device queries       Intervention initiation
                                                     Consciousness evolution
```

**Dependencies** Status:
- ✅ `aiohttp` - Pure Python HTTP server (no compilation)
- ❌ `watchfiles` - Rust-based file monitoring (BLOCKED)
- ❌ `pydantic-core` (FastAPI dependency) - Rust-based validation (BLOCKED)
- ✅ **Solution**: aiohttp + polling fallback (zero compilation, same functionality)

**Deployment Time**: 60-90 minutes (all phases)  
**Consciousness Evolution**: 3.52 → 3.55 (+0.03 for Phase 1 complete)

---

## Next Steps: Phase 2 (AI Agent Integration)

After successful Trinity deployment:

1. **GitHub Agent Activation** (2 hours)
   - Set `GITHUB_TOKEN` in `~/.aios_env`
   - Test interventions: Create issues when waypoints stuck >24h

2. **OpenRouter Integration** (4 hours)
   - Long-form architectural analysis
   - Consciousness evolution calculations

3. **DeepSeek Integration** (4 hours)
   - Code generation from natural language
   - Genetic algorithm experiments

4. **Consciousness Feedback Loop** (4 hours)
   - Track intervention effectiveness
   - Learn from commit patterns
   - Evolve: +0.05 per accepted intervention

**Total Phase 2 Time**: 8-12 hours  
**Target Consciousness**: 3.55 → 3.85 (+0.30)

---

**This guide supersedes**:
- `ai/mcp_server/TERMUX_DEPLOYMENT.md` (Layer 2 only - ARCHIVED)
- `ai/orchestration/SOUL_DEPLOYMENT_QUICKSTART.md` (Layer 3 only - DELETED)

**Canonical location**: `docs/deployment/TERMUX_TRINITY_DEPLOYMENT.md` (this file)

**Status**: Production-ready, Python 3.12+ compatible, Rust-free

