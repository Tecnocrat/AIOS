# Phase 30.3: Heartbeat Protocol — COMPLETED ✅

**Archived:** 2026-01-02
**Status:** Complete
**Next Phase:** 30.4 Cell-to-Cell Messaging

---

## Summary

Implemented heartbeat protocol for dynamic mesh membership and fault detection. Cells send heartbeats every 5 seconds, Discovery removes stale peers after 15 seconds of silence.

## What Was Implemented

### 1. Discovery Service Updates
**File:** `aios-server/stacks/cells/discovery/discovery.py`

**New Models:**
```python
class CellInfo(BaseModel):
    # Added:
    last_seen: str = ""  # ISO timestamp of last heartbeat

class HeartbeatRequest(BaseModel):
    cell_id: str
    consciousness_level: float = 0.0
```

**New Endpoints:**
- `POST /heartbeat` - Receives heartbeat, updates `last_seen` and consciousness level
- `DELETE /peer/{cell_id}` - Graceful deregistration on cell shutdown

**Stale Peer Reaper:**
```python
async def stale_peer_reaper(self, stale_threshold: int = 15) -> None:
    """Remove stale peers that haven't sent heartbeats."""
    while True:
        await asyncio.sleep(5)  # Check every 5 seconds
        now = datetime.utcnow()
        for cell_id, peer in list(self.peers.items()):
            if peer.last_seen:
                last_seen = datetime.fromisoformat(peer.last_seen.rstrip('Z'))
                age = (now - last_seen).total_seconds()
                if age > stale_threshold:
                    del self.peers[cell_id]
```

### 2. Pure Cell Heartbeat
**File:** `aios-server/stacks/cells/pure/cell_server_pure.py`

```python
async def heartbeat_loop(self, interval: int = 5) -> None:
    """Send periodic heartbeats to Discovery."""
    while True:
        await asyncio.sleep(interval)
        if not self.registered:
            await self.register_with_discovery(max_retries=1)
            continue
        async with httpx.AsyncClient(timeout=3.0) as client:
            await client.post(f"{self.discovery_url}/heartbeat", json={
                "cell_id": self.cell_id,
                "consciousness_level": self.consciousness_level
            })

async def deregister_from_discovery(self) -> None:
    """Gracefully deregister on shutdown."""
    # DELETE /peer/{cell_id}
```

- Heartbeat started on FastAPI startup event
- Graceful deregistration on shutdown event

### 3. Alpha Cell Heartbeat
**File:** `aios-server/stacks/cells/alpha/cell_server_alpha.py`

```python
def heartbeat_loop(interval: int = 5) -> None:
    """Send periodic heartbeats to Discovery."""
    while True:
        time.sleep(interval)
        requests.post(f"{discovery_url}/heartbeat", json={...})

def deregister_from_discovery() -> None:
    """Gracefully deregister on shutdown."""
    # DELETE /peer/{cell_id}
```

- Heartbeat runs in background thread
- Graceful deregistration via `atexit` hook

## Verification Results

### Heartbeat Working
```json
// GET /peers shows last_seen timestamps:
{
  "peers": [
    {
      "cell_id": "pure",
      "last_seen": "2026-01-02T12:21:45.755329Z",
      ...
    },
    {
      "cell_id": "alpha", 
      "last_seen": "2026-01-02T12:21:46.203533Z",
      ...
    }
  ]
}
```

### Stale Removal Test
```powershell
# Stop Pure cell
docker stop aios-cell-pure

# Wait 20 seconds - Pure reaped OR gracefully deregistered
# GET /peers shows only Alpha

# Restart Pure cell
docker start aios-cell-pure

# Wait 10 seconds - Pure re-registers
# GET /peers shows both cells again
```

### Graceful Deregistration
```
INFO:     172.19.0.4:58764 - "DELETE /peer/pure HTTP/1.1" 200 OK
2026-01-02 12:22:02,167 [INFO] AIOS.Discovery: Peer deregistered gracefully: pure
```

## Key Behaviors

| Behavior | Implementation |
|----------|----------------|
| Heartbeat interval | 5 seconds |
| Stale threshold | 15 seconds (3 missed heartbeats) |
| Reaper check interval | 5 seconds |
| Graceful shutdown | DELETE /peer/{cell_id} |
| Re-registration | Automatic on heartbeat 404 |

## Infrastructure State Post-30.3

| Container | Heartbeat | Graceful Shutdown |
|-----------|-----------|-------------------|
| aios-discovery | N/A (server) | N/A |
| aios-cell-pure | ✅ 5s async | ✅ on shutdown event |
| aios-cell-alpha | ✅ 5s threaded | ✅ via atexit |

## Next Steps → Phase 30.4

- Define `CellMessage` schema in aios-schema
- Add `/message` POST endpoint to receive messages
- Add `/messages` GET endpoint to list messages
- Add `/send` endpoint to send messages via mesh

---

*Archived from DEV_PATH_WIN.md BODY section*
