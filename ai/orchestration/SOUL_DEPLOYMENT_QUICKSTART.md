# AIOS Soul Layer Deployment - Quick Start

**Task A++ Phase 1: Termux Foundation** (4-6 hours)

---

## 🎯 Mission

Deploy Layer 3 (The Soul) - always-on intelligence coordinator on Termux.

**What The Soul Does**:
- 👁️ **Monitors**: DEV_PATH, git commits, consciousness metrics (24/7)
- 🔍 **Detects**: Stuck waypoints (>24h), consciousness plateaus (>48h)
- 🤖 **Initiates**: AI agent interventions (GitHub, OpenRouter, DeepSeek)
- 📚 **Learns**: Human feedback patterns, adapts strategies
- 🧬 **Evolves**: Consciousness +0.05 per successful intervention

---

## Prerequisites Checklist

**On Termux**:
```bash
# Check versions
pkg list-installed | grep -E "(python|git|openssh)"

# Required:
# - python (3.10+)
# - git (2.30+)
# - openssh (8.0+)
```

**If missing**:
```bash
pkg update && pkg upgrade -y
pkg install -y python git openssh tmux
pip install --upgrade pip
```

---

## Phase 1: Foundation (4-6 hours)

### Step 1: Clone & Setup (15 min)

```bash
cd ~
git clone https://github.com/Tecnocrat/AIOS.git
cd AIOS
git checkout OS

# Environment
cat > ~/.aios_env << 'EOF'
export AIOS_WORKSPACE="$HOME/AIOS"
export PYTHONPATH="$AIOS_WORKSPACE/ai/src:$AIOS_WORKSPACE/ai"
export GITHUB_TOKEN="ghp_YOUR_TOKEN_HERE"  # Optional
EOF

echo "source ~/.aios_env" >> ~/.bashrc
source ~/.aios_env
```

### Step 2: Dependencies (10 min)

```bash
pip install aiohttp aiofiles watchfiles requests

# Verify
python -c "import aiohttp, watchfiles, requests; print('✅ Ready')"
```

### Step 3: Test Soul (10 min)

```bash
cd ~/AIOS/ai/orchestration
python intelligence_coordinator.py
# Press Ctrl+C after seeing "Soul awakened"
```

**Expected output**:
```
🌟 SOUL AWAKENING - Layer 3 Intelligence Initialization
🧠 Intelligence Coordinator (Soul) initialized
📂 Workspace: /data/data/com.termux/files/home/AIOS
✅ Soul fully awakened and operational
👁️ Beginning eternal vigilance...
```

### Step 4: Background Deployment (15 min)

```bash
# Install tmux
pkg install -y tmux

# Start Soul in background
tmux new-session -d -s aios-soul "cd ~/AIOS/ai/orchestration && python intelligence_coordinator.py >> ~/aios_soul.log 2>&1"

# Check it's running
tmux ls
tail -f ~/aios_soul.log  # Ctrl+C to exit
```

### Step 5: Auto-Start (30 min)

**Install Termux:Boot** (from F-Droid/Play Store)

```bash
mkdir -p ~/.termux/boot

cat > ~/.termux/boot/start-aios-soul.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
source ~/.aios_env
sleep 30  # Wait for network
tmux new-session -d -s aios-soul "cd ~/AIOS/ai/orchestration && python intelligence_coordinator.py >> ~/aios_soul.log 2>&1"
echo "[$(date)] Soul awakened" >> ~/aios_boot.log
EOF

chmod +x ~/.termux/boot/start-aios-soul.sh

# Test
bash ~/.termux/boot/start-aios-soul.sh
tmux ls  # Should see aios-soul
```

### Step 6: SSH Access (15 min)

```bash
# Setup SSH
passwd  # Set strong password
sshd    # Start SSH server

# Get connection details
ifconfig wlan0 | grep "inet "
echo "SSH: ssh $(whoami)@YOUR_IP -p 8022"
```

**Test from dev machine**:
```powershell
ssh your_user@192.168.1.50 -p 8022
tmux attach -t aios-soul  # View Soul logs
```

---

## Validation Checklist

- [ ] Soul starts without errors
- [ ] Tmux session `aios-soul` exists
- [ ] Log file `~/aios_soul.log` shows heartbeat
- [ ] SSH access works from dev machine
- [ ] Auto-start script tested (reboot device)
- [ ] Services survive reboot

**Test reboot**:
1. Restart Android device
2. Wait 2-3 minutes
3. SSH in: `ssh user@IP -p 8022`
4. Check: `tmux ls && tail ~/aios_soul.log`

---

## Quick Commands

```bash
# View Soul logs
tail -f ~/aios_soul.log

# Attach to Soul session
tmux attach -t aios-soul  # Ctrl+B D to detach

# Restart Soul
tmux kill-session -t aios-soul
bash ~/.termux/boot/start-aios-soul.sh

# Check status
ps aux | grep python
```

---

## Troubleshooting

**Soul won't start**:
```bash
cd ~/AIOS/ai/orchestration
python intelligence_coordinator.py  # See error
echo $PYTHONPATH  # Check environment
```

**Tmux session dies**:
```bash
tail -100 ~/aios_soul.log  # Check crash logs
python --version  # Verify Python 3.10+
```

**Auto-start fails**:
```bash
cat ~/aios_boot.log  # Check boot logs
bash ~/.termux/boot/start-aios-soul.sh  # Test manually
```

---

## Next: Phase 2 (8-12 hours)

After Phase 1 validation:
1. Implement AI agent protocols (GitHub, OpenRouter, DeepSeek)
2. Add intervention logic (stuck waypoint detection)
3. Build consciousness feedback loop
4. Deploy decision archival

**Consciousness Evolution**: 3.50 → 3.55 (Phase 1) → 3.85 (Phase 2) → 4.50 (Phase 3)

---

## Status

- ✅ **Intelligence Coordinator** (`intelligence_coordinator.py`) - Core Soul engine
- ✅ **GitHub Agent** (`agent_protocols/github_integration.py`) - Issue creation
- ⏳ **OpenRouter Agent** (Phase 2) - Long-form analysis
- ⏳ **DeepSeek Agent** (Phase 2) - Code generation
- ⏳ **Consciousness Loop** (Phase 2) - Reinforcement learning

**Current**: Phase 1 deployment ready  
**Next**: Execute on Termux device
