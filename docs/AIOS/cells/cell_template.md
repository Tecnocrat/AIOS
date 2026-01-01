## Cell metadata template

Fill this template after a cell birth to record provenance and verification artifacts.

- Cell ID: `alpha`
- Image: `aios-cell-<id>:<timestamp>`
- Born at: `2025-11-23T...Z`
- Actor: `local-agent` or `CI` or `user`
- Git commit (canonical genome): `<sha>`
- SKIP_CORE_BUILD: `1` or `0`
- Verified endpoints:
  - HTTP base: `http://localhost:8000` (status: up/down, notes)
  - Metrics: `http://localhost:9091/metrics` (status: up/down)
  - Docker status: container name and ports
- Artifacts:
  - waypoint file: `tachyonic/waypoints/waypoint-*.json`
  - logs archive: `logs/aios-cell-<id>-startup.log`

Notes:
