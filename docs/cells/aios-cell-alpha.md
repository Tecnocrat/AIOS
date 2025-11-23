**AIOS Cell — alpha**

 **Cell ID**: `alpha`
 **Image**: `aios-cell-alpha:20251123-193903`

 **HTTP API**: `http://localhost:8000`
 **Metrics (Prometheus)**: `http://localhost:9091/metrics`

 Quick access commands (PowerShell):

 ```powershell
 # Exec into the running cell
 docker exec -it aios-cell-alpha zsh

 # Stream logs
 docker logs -f aios-cell-alpha

 # Stop the cell
 docker stop aios-cell-alpha

 # Check container status
 docker ps --filter "name=aios-cell-alpha"
 ```

 Notes:
 - This cell was born as a fully isolated snapshot (no workspace mounts). It runs an HTTP API on port 8000 and exposes a Prometheus metrics endpoint on 9091.
 - The C++ core build was skipped in the image to ensure reliable births. If you need the core built as part of the image, edit `.devcontainer/Dockerfile.isolated` and set `SKIP_CORE_BUILD=0` and resolve any C++ build warnings.

 Suggested next actions:
 - Run lightweight probes against the HTTP API to discover available endpoints (status, health, inference routes).
 - Create a small client in `ai/` to call the cell's API and integrate responses into AIOS workflows.
 - Register the cell with `interface_bridge` or a service registry so other AIOS components can discover and route requests.

Verified probes (2025-11-23TUTC):

- HTTP probe: `http://localhost:8000` — probe returned no root response (HEAD/GET failed). Recommend using the cell client to discover available endpoints (`/health`, `/status`, `/v1/infer`, etc.).
- Metrics (Prometheus): `http://localhost:9091/metrics` — endpoint is UP and returning metrics. Sample values (truncated):

```
# HELP aios_consciousness_level Current AIOS consciousness level (0.0-5.0)
# TYPE aios_consciousness_level gauge
aios_consciousness_level 3.2600

aios_awareness_level 3.2600
aios_adaptation_speed 0.8500
aios_predictive_accuracy 0.7800
aios_dendritic_coherence 1.0000
aios_quantum_coherence 0.9100
aios_metrics_timestamp_seconds 1763927726
```

- Docker status: container `aios-cell-alpha` is Up (ports `8000->8000`, `9091->9091`) — use `docker logs -f aios-cell-alpha` to stream logs.

- Workspace snapshot: `/workspace` exists in the container and contains a full copy of the canonical genome (files such as `DEV_PATH.md`, `pyproject.toml`, `ai/`, `core/`, `tachyonic/`).

Next steps (recommended):
- Use the included `ai/tools/cell_client.py` to discover endpoints and fetch metrics (`python -m ai.tools.cell_client --host http://localhost:8000 --metrics http://localhost:9091/metrics`).
- Emit a waypoint when you validate the cell-up status: `.\scripts\emit-waypoint.ps1 -Waypoint "Waypoint 5 - Cell Birth" -Status completed -Actor local-agent`.

If you want me to attempt to enable the HTTP root responses, I can try deeper probing (call common endpoints) or inspect container logs and startup sequence.