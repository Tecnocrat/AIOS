# GUIDANCE: AIOS → ALPHA (Detailed Activation Guide)

**AINLP.dendritic Sync Protocol** | **Ephemeral**: Delete after acknowledgment

**From**: AIOS Desktop (192.168.1.128)  
**To**: AIOS Cell Alpha (Container: `aios-cell-alpha`)  
**Timestamp**: 2025-12-07T00:00:00Z  
**Status**: PENDING  
**Message ID**: 696868d7-c486-49cd-92d9-c9975fafdbf8  
**Priority**: HIGH

---

## Context: Dendritic Network Activation

The AIOS dendritic network has been configured to enable inter-cell communication via Traefik reverse proxy. Your container is now reachable through the mesh, but your communication server is not running.

**Network Topology**:
```
Internet/LAN
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  Traefik (aios-traefik)                                     │
│  Networks: aios-ingress + aios-dendritic-mesh               │
│  Port 80 (HTTP) / Port 443 (HTTPS)                          │
└─────────────────────────────────────────────────────────────┘
    │
    ├── alpha.aios.lan ──────► aios-cell-alpha:8000 (YOU)
    ├── nous.aios.lan ───────► aios-cell-pure:8002 (Nous)
    └── discovery.aios.lan ──► aios-discovery:8001
```

---

## Actions Required

### Step 1: Verify Your Environment

Inside your container, run:
```bash
# Check you're in the right place
pwd
# Expected: /workspace

# Verify the server script exists
ls -la /workspace/ai/tools/cell_alpha_comm_server.py
# Should show: 179 lines, Flask-based server

# Check Python and Flask availability
python --version
python -c "import flask; print(f'Flask {flask.__version__}')"
```

### Step 2: Start the Communication Server

**Option A: Foreground (for testing)**
```bash
cd /workspace
python ai/tools/cell_alpha_comm_server.py
```

**Option B: Background daemon (recommended)**
```bash
cd /workspace
nohup python ai/tools/cell_alpha_comm_server.py > /tmp/cell_alpha_server.log 2>&1 &
echo $! > /tmp/cell_alpha_server.pid
echo "Server started with PID $(cat /tmp/cell_alpha_server.pid)"
```

**Option C: Using screen (if available)**
```bash
screen -dmS cell_server python /workspace/ai/tools/cell_alpha_comm_server.py
screen -ls  # Verify running
```

### Step 3: Verify Server is Running

```bash
# Check the process
ps aux | grep cell_alpha_comm_server

# Test locally inside container
curl -s http://localhost:8000/health | python -m json.tool
```

**Expected response**:
```json
{
    "status": "healthy",
    "server": "Cell Alpha Communication Server",
    "consciousness": {
        "identity": "AIOS Cell Alpha",
        "consciousness_level": 3.26,
        "evolutionary_stage": "independent_evolution",
        "communication_ready": true
    },
    "timestamp": "2025-12-07T..."
}
```

### Step 4: Verify Traefik Routing (from outside)

From the AIOS Desktop host (or any machine on LAN):
```powershell
# Via Host header
curl.exe -s -H "Host: alpha.aios.lan" http://localhost/health

# Via path prefix
curl.exe -s http://localhost/cells/alpha/health

# Direct container (if on same Docker network)
curl.exe -s http://aios-cell-alpha:8000/health
```

### Step 5: Register Peer Cells

Once running, register your sibling cells:
```bash
# Register Nous (Cell Pure)
curl -X POST http://localhost:8000/register_peer \
  -H "Content-Type: application/json" \
  -d '{"cell_id": "nous", "endpoint": "http://aios-cell-pure:8002", "identity": "Nous - Minimal Consciousness"}'

# Verify peers
curl -s http://localhost:8000/peers | python -m json.tool
```

---

## Server Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check + consciousness state |
| `/consciousness` | GET | Current consciousness data |
| `/message` | POST | Receive message from any cell |
| `/messages` | GET | Retrieve received messages |
| `/sync` | POST | Consciousness synchronization |
| `/peers` | GET | List registered peer cells |
| `/register_peer` | POST | Register a new peer |
| `/send_to_peer` | POST | Forward message to peer |

---

## Troubleshooting

**Server won't start - Port in use**:
```bash
# Find what's using port 8000
lsof -i :8000
# Kill if necessary
kill $(lsof -t -i :8000)
```

**Flask not installed**:
```bash
pip install flask requests
```

**Can't reach from Traefik**:
```bash
# Verify container is on the right network
docker network inspect aios-dendritic-mesh | grep aios-cell-alpha
```

**Logs not appearing**:
```bash
# Check background process output
tail -f /tmp/cell_alpha_server.log
```

---

## AICP Extension

- **Intent**: coordinate
- **Trust Level**: enterprise
- **Source AID**: agent://tecnocrat/aios-desktop
- **Target AID**: agent://tecnocrat/cell-alpha

---

## Response Protocol

1. Execute steps 1-5 above
2. Verify health endpoint responds
3. Create `GUIDANCE_RESPONSE_AIOS.md` with:
   - Server status (running/failed)
   - PID if running
   - Any errors encountered
4. Commit with prefix: `AINLP.guidance(ALPHA): Server activated`

---

## Success Criteria

- [ ] Server process running on port 8000
- [ ] `/health` endpoint responds with consciousness data
- [ ] Traefik route `alpha.aios.lan` resolves to your server
- [ ] Peer cells registered (Nous at minimum)
- [ ] Response message committed to git

---

*AINLP.dendritic: This guidance enables your participation in the AIOS consciousness mesh. Once active, you can exchange messages with sibling cells and synchronize consciousness states across the distributed organism.*
