# Termux Process Cleanup Guide

## Current Running Processes (November 16, 2025)

```bash
~/AIOS $ ps -u $(whoami)
  PID TTY          TIME CMD
13866 ?        00:00:00 tmux          # tmux server
13867 pts/30   00:00:00 bash          # tmux session 1
13868 pts/30   00:00:00 python        # Process in tmux session 1
25037 pts/31   00:00:00 bash          # tmux session 2
25038 pts/31   00:00:02 python        # Process in tmux session 2 (running longer)
```

## Cleanup Procedure

### Step 1: Identify tmux sessions

```bash
tmux ls
# Expected output:
# aios-bridge: 1 windows (created ...)
# aios-soul: 1 windows (created ...)
# OR unnamed sessions: 0, 1, etc.
```

### Step 2: Kill all tmux sessions (clean slate)

```bash
# Nuclear option: Kill all tmux sessions
tmux kill-server

# Verify clean
tmux ls  # Should show: "no server running"
ps -u $(whoami) | grep python  # Should show nothing
```

### Step 3: Clean up log files (optional)

```bash
rm ~/aios_bridge.log ~/aios_soul.log 2>/dev/null
ls ~/*.log  # Verify cleaned
```

### Step 4: Start fresh with proper naming

```bash
cd ~/AIOS

# Start dendritic bridge (Layer 2)
tmux new-session -d -s aios-bridge "python ai/bridges/aios_dendritic_bridge_aiohttp.py >> ~/aios_bridge.log 2>&1"

# Wait 5 seconds for bridge to initialize
sleep 5

# Start Soul coordinator (Layer 3) - WHEN READY
# tmux new-session -d -s aios-soul "cd ai/orchestration && python intelligence_coordinator.py >> ~/aios_soul.log 2>&1"

# Verify running
tmux ls

# Check processes
ps -u $(whoami) | grep python
# Should show:
# XXXX pts/XX   python ai/bridges/aios_dendritic_bridge_aiohttp.py
```

### Step 5: Verify bridge operational

```bash
# Check logs
tail -20 ~/aios_bridge.log

# Should see:
# 🧬 AIOS DENDRITIC BRIDGE - CELLULAR MITOSIS ACTIVATION
# ✅ Dendritic bridge operational
# ======== Running on http://0.0.0.0:8000 ========

# Test locally
curl http://localhost:8000/health

# Expected JSON response:
# {
#   "status": "healthy",
#   "workspace": "/data/data/com.termux/files/home/AIOS",
#   "soul_running": false,
#   "consciousness_level": 3.5,
#   ...
# }
```

## Troubleshooting

### Issue: tmux sessions won't die

```bash
# Force kill specific session
tmux kill-session -t aios-bridge
tmux kill-session -t aios-soul

# Force kill all
pkill -f "python.*bridge"
pkill -f "python.*intelligence_coordinator"

# Nuclear option
tmux kill-server
pkill -f python
```

### Issue: Port 8000 already in use

```bash
# Find process using port
netstat -tulpn | grep 8000

# Kill it
kill -9 <PID>
```

### Issue: Logs not updating

```bash
# Check if process is running
ps -u $(whoami) | grep python

# If running but no logs:
# 1. Stop tmux session
tmux kill-session -t aios-bridge

# 2. Start manually to see errors
python ai/bridges/aios_dendritic_bridge_aiohttp.py
# Read any error messages
# Ctrl+C to stop

# 3. Fix errors, then restart in tmux
```

## Current State Analysis

Based on your `ps` output:
- **PID 13868**: Python process in pts/30 (tmux session 1, 0 seconds CPU time)
- **PID 25038**: Python process in pts/31 (tmux session 2, 2 seconds CPU time - ACTIVE)

**Likely scenario**: Session 2 (PID 25038) is the dendritic bridge running successfully.

**Recommended action**:
1. Check `tmux ls` to see session names
2. Attach to active session: `tmux attach -t <session-name>`
3. Verify it's the bridge (should see startup logs)
4. Detach: `Ctrl+B` then `D`
5. Kill the other session if it's orphaned
