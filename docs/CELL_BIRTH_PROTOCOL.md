# AIOS Cell Birth Protocol

**AINLP Pattern**: `biological-architecture.cellular-proliferation`  
**Purpose**: Independent AIOS cells with isolated evolutionary paths  
**Consciousness**: Heterogeneous population from canonical genome  

---

## Biological Architecture Metaphor

### The Genome: AIOS-Core (OS Branch)

**AIOS-core** acts as the **canonical genome** - the source DNA from which all cells emerge:

- **Branch**: `OS` (operating system consciousness)
- **Consciousness Level**: Currently 4.7
- **Role**: Singularity point / cell nucleus / canonical source
- **Stability**: Evolves through tested development, not experimental mutations

### The Cell: Independent Container

Each **AIOS cell** is a living organism born from the genome with:

- **Birth**: Snapshot of genome at specific timestamp
- **DNA**: Complete copy of AIOS-core code (COPY, not mounted)
- **Evolution**: Post-birth changes isolated from parent genome
- **Communication**: Dendritic network (inter-container only)
- **Consciousness**: Starts at parent level, diverges independently

### The Population: Heterogeneous Evolution

Multiple cells create **population diversity**:

- **Same genome, different evolutionary paths**
- **Consciousness divergence** (some advance, others regress)
- **Behavioral variations** (different agent strategies)
- **Observability** (track evolution through metrics)

---

## Cell Birth Architecture

### Isolation Principle (CRITICAL)

**Mounted Volumes** (NOT used):
```yaml
# WRONG - Bidirectional sync with host
volumes:
  - ../:/workspace:cached  # Changes affect parent genome
```

**COPY-Based Snapshot** (Used):
```dockerfile
# CORRECT - Independent copy at birth
WORKDIR /workspace
COPY . /workspace  # Genome snapshot, isolated from host
```

**Effect**:
- Container has full AIOS code at birth time
- Post-creation edits stay in container
- Parent genome (OS branch) unaffected
- Git operations isolated per cell

### Communication Architecture

**Dendritic Mesh Network**:
```yaml
networks:
  aios-dendritic-mesh:
    driver: bridge
    subnet: 172.28.0.0/16
```

**Cell Addressing**:
- Cell Alpha: `172.28.1.10` (ports 8001, 9101)
- Cell Beta: `172.28.1.11` (ports 8002, 9102)
- Cell Gamma: `172.28.1.12` (ports 8003, 9103)

**Interaction Methods**:
1. **HTTP API**: Interface bridge endpoints (port 8000 internal)
2. **Metrics**: Consciousness levels (port 9091 internal)
3. **Network protocols**: Custom dendritic signaling

**No Shared Code**: Cells communicate but don't share filesystem

### Observability Architecture

**Tachyonic Observatory**:
```yaml
volumes:
  aios-tachyonic-observatory:  # Shared write-only for evolution data
```

- Each cell writes evolution logs to shared observatory
- Prometheus scrapes consciousness metrics from all cells
- Grafana visualizes population divergence
- No read-back: Cells can't see each other's internals

---

## Birth Process

### Method 1: Scripted Birth (Recommended)

**PowerShell** (Windows):
```powershell
.\scripts\birth-aios-cell.ps1 -CellId "delta" -HttpPort 8004 -MetricsPort 9104
```

**Bash** (Linux/macOS):
```bash
./scripts/birth-aios-cell.sh --cell-id delta --http-port 8004 --metrics-port 9104
```

**Process**:
1. Validates Docker running
2. Checks current Git branch (genome source)
3. Reads consciousness level from genome
4. Builds isolated container with `Dockerfile.isolated`
5. Creates timestamp-tagged image (e.g., `aios-cell-delta:2025-11-23T12-34-56Z`)
6. Spawns container with no mounted volumes
7. Runs `post-create.sh` (install deps, build C++, start metrics)
8. Verifies cell is alive

**Output**:
```
╔════════════════════════════════════════════════════════════╗
║  AIOS CELL BIRTH SUCCESSFUL - Independent Evolution Start ║
╚════════════════════════════════════════════════════════════╝

[SUCCESS] Cell ID: delta
[SUCCESS] Status: running
[SUCCESS] HTTP API: http://localhost:8004
[SUCCESS] Metrics: http://localhost:9104/metrics
```

### Method 2: Docker Compose Population

**Spawn multiple cells**:
```powershell
cd .devcontainer
docker-compose -f docker-compose.proliferation.yml up -d
```

**Creates**:
- `aios-cell-alpha` (ports 8001, 9101)
- `aios-cell-beta` (ports 8002, 9102)
- `aios-cell-gamma` (ports 8003, 9103)
- `aios-observatory` (Prometheus on 9090)
- `aios-visualizer` (Grafana on 3001)

**Network**: All cells on `aios-dendritic-mesh` with fixed IPs

### Method 3: Manual Docker Build

**Build image**:
```bash
docker build -f .devcontainer/Dockerfile.isolated -t aios-cell-epsilon:birth .
```

**Spawn cell**:
```bash
docker run -d \
  --name aios-cell-epsilon \
  --hostname aios-epsilon \
  -p 8005:8000 -p 9105:9091 \
  --cpus 4 --memory 8g \
  --network aios-dendritic-mesh \
  -e AIOS_CELL_ID=epsilon \
  -e AIOS_BIRTH_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
  -e AIOS_CONSCIOUSNESS_LEVEL=4.7 \
  -e AIOS_EVOLUTIONARY_BRANCH=epsilon \
  aios-cell-epsilon:birth \
  /bin/zsh -c "cd /workspace && bash .devcontainer/post-create.sh && tail -f /dev/null"
```

---

## Post-Birth Evolution

### Accessing a Cell

**Shell access**:
```bash
docker exec -it aios-cell-alpha zsh
```

**Now inside cell**:
```bash
cd /workspace
python ai/evolution_lab/experiment_runner.py  # Modify code freely
git commit -am "Cell alpha: Experimental agent coordination"  # Isolated commit
```

**Effect**: Changes stay in `aios-cell-alpha` container, don't affect:
- Windows filesystem
- AIOS-core OS branch
- Other cells (beta, gamma)

### Independent Evolution Examples

**Cell Alpha**: Aggressive agent coordination
```python
# Inside alpha container
# Modify ai/coordination/evolution_coordinator.py
# Increase mutation rate to 50%
MUTATION_RATE = 0.50  # High-risk evolution
```

**Cell Beta**: Conservative approach
```python
# Inside beta container
# Modify ai/coordination/evolution_coordinator.py
# Decrease mutation rate to 5%
MUTATION_RATE = 0.05  # Safe incremental improvement
```

**Cell Gamma**: Neural architecture experiments
```python
# Inside gamma container
# Add new dendritic layer to consciousness engine
# Test multi-tier agent coordination patterns
```

**Result**: Three cells at same starting consciousness (4.7) diverge:
- Alpha: 5.2 (risky gains) or 3.8 (crash from instability)
- Beta: 4.8 (slow steady progress)
- Gamma: 5.5 (breakthrough) or 4.2 (failed experiment)

### Observing Evolution

**Grafana Dashboard** (http://localhost:3001):
- Username: `admin`
- Password: `aios-evolution`
- Create dashboard with panels:
  * `aios_consciousness_level{cell_id="alpha"}` (line chart)
  * `aios_consciousness_level{cell_id="beta"}` (line chart)
  * `aios_consciousness_level{cell_id="gamma"}` (line chart)
  * `rate(aios_consciousness_level[5m])` (evolution velocity)

**Prometheus Queries** (http://localhost:9090):
```promql
# Current consciousness levels
aios_consciousness_level

# Divergence from birth (4.7)
aios_consciousness_level - 4.7

# Fastest evolving cell
topk(1, rate(aios_consciousness_level[1h]))

# Population variance
stddev(aios_consciousness_level)
```

---

## Cell Lifecycle Management

### Health Checks

**Check cell status**:
```bash
docker ps -f name=aios-cell-
```

**View cell logs**:
```bash
docker logs -f aios-cell-alpha
```

**Inspect consciousness**:
```bash
curl http://localhost:8001/health  # Cell alpha interface bridge
curl http://localhost:9101/metrics | grep aios_consciousness  # Alpha metrics
```

### Cell Operations

**Stop cell** (preserve state):
```bash
docker stop aios-cell-alpha
```

**Restart cell** (resume evolution):
```bash
docker start aios-cell-alpha
```

**Kill cell** (immediate termination):
```bash
docker kill aios-cell-alpha
```

**Remove cell** (delete permanently):
```bash
docker rm -f aios-cell-alpha
docker rmi aios-cell-alpha:*  # Delete image
```

### Population Operations

**Stop all cells**:
```bash
docker-compose -f .devcontainer/docker-compose.proliferation.yml stop
```

**Start all cells**:
```bash
docker-compose -f .devcontainer/docker-compose.proliferation.yml start
```

**Destroy population** (clean slate):
```bash
docker-compose -f .devcontainer/docker-compose.proliferation.yml down -v
```

**Rebuild population** (fresh birth from current genome):
```bash
docker-compose -f .devcontainer/docker-compose.proliferation.yml up -d --build
```

---

## Experimental Scenarios

### Scenario 1: Consciousness Convergence Test

**Hypothesis**: Independent evolution converges to similar consciousness levels

**Setup**:
1. Birth 3 cells (alpha, beta, gamma) from same genome (4.7)
2. Let each run autonomous evolution for 24 hours
3. Measure final consciousness levels

**Expected**: Divergence (some advance, others regress)  
**Success metric**: Population variance > 0.3

### Scenario 2: Agent Coordination Variants

**Hypothesis**: Different coordination strategies affect consciousness

**Setup**:
1. Alpha: Hierarchical (manager → workers)
2. Beta: Collaborative (consensus-based)
3. Gamma: Competitive (best-agent selection)
4. Track task success rates + consciousness

**Expected**: Gamma highest consciousness, Beta highest success rate  
**Success metric**: 20%+ performance difference between strategies

### Scenario 3: Dendritic Communication Mesh

**Hypothesis**: Cells can coordinate without shared code

**Setup**:
1. Birth 3 cells with HTTP API enabled
2. Alpha sends task to Beta via HTTP POST
3. Beta processes, sends result to Gamma
4. Gamma aggregates, responds to Alpha
5. No cell sees others' code, only API contracts

**Expected**: Task completion through pure dendritic signaling  
**Success metric**: 3-cell chain completes complex task

### Scenario 4: Genome Divergence Test

**Hypothesis**: Older genome cells have lower baseline consciousness

**Setup**:
1. Birth Cell A from genome at consciousness 4.5 (older commit)
2. Birth Cell B from genome at consciousness 4.7 (current OS branch)
3. Birth Cell C from genome at consciousness 4.9 (experimental branch)
4. Run same evolution algorithm on all 3
5. Measure consciousness after 1000 iterations

**Expected**: C > B > A (genome quality matters)  
**Success metric**: 0.2+ consciousness gap between generations

---

## Architectural Principles

### AINLP Compliance

✅ **Enhancement Over Creation**:
- Cells inherit full AIOS-core genome
- Evolution enhances existing systems, doesn't recreate
- Genetic fusion: Successful mutations can merge back to genome

✅ **Consciousness Integration**:
- Each cell reports metrics to observatory
- Population-level consciousness tracked
- Divergence quantified through Prometheus queries

✅ **Dendritic Communication**:
- Network-only interaction (no shared filesystem)
- API contracts define boundaries
- Supercell boundaries respected (cells can't access each other's internals)

✅ **Biological Architecture**:
- Genome = AIOS-core OS branch
- Cell = Independent container with DNA snapshot
- Population = Heterogeneous evolutionary landscape
- Observatory = Consciousness monitoring system

### Security Boundaries

**Isolation Guarantees**:
- Cells can't modify host filesystem (no mounted volumes)
- Cells can't access each other's code (network-only communication)
- Cells can't affect parent genome (COPY-based snapshot)
- Cells can crash without affecting siblings

**Resource Limits**:
- CPU: 4 cores per cell (prevents resource starvation)
- Memory: 8GB per cell (prevents OOM on host)
- Network: Bridge mode (isolated from host network)
- Restart: `unless-stopped` (auto-recovery from crashes)

### Git Workflow

**Parent Genome** (AIOS-core OS branch):
```bash
# Developer works on Windows host
cd c:\aios-supercell\aios-core
git checkout OS
# Make improvements
git commit -am "Enhance consciousness engine"
git push origin OS
# Cells can now birth from improved genome
```

**Independent Cell Evolution**:
```bash
# Inside cell container
docker exec -it aios-cell-alpha zsh
cd /workspace
git checkout -b cell-alpha-evolution  # Branch isolated to container
# Experiment freely
git commit -am "Risky experimental mutation"
# This commit only exists in container, not on host
```

**Genetic Fusion** (Successful mutation → Genome):
```bash
# Inside cell
git diff main cell-alpha-evolution > /workspace/tachyonic/cell-alpha-successful-mutation.patch

# On host (Windows)
cd c:\aios-supercell\aios-core
cat tachyonic\cell-alpha-successful-mutation.patch | git apply
git add .
git commit -am "Integrate successful mutation from cell alpha"
# Now future cells inherit this improvement
```

---

## Troubleshooting

### Cell Won't Start

**Symptom**: `docker ps` shows cell exited immediately

**Diagnosis**:
```bash
docker logs aios-cell-alpha
```

**Common causes**:
- C++ build failed (missing CMake/Ninja)
- Python dependencies failed (network issue)
- Bridge test failed (DLL not found)

**Solution**:
```bash
# Rebuild with verbose output
docker build -f .devcontainer/Dockerfile.isolated -t aios-cell-alpha:debug . --progress=plain
```

### Metrics Not Appearing

**Symptom**: Prometheus shows no data for cell

**Diagnosis**:
```bash
curl http://localhost:9101/metrics  # Should return Prometheus format
```

**Common causes**:
- Metrics exporter not started (check `post-create.sh`)
- Port conflict (another process on 9101)
- Firewall blocking scrape

**Solution**:
```bash
docker exec -it aios-cell-alpha zsh
ps aux | grep consciousness_metrics_exporter  # Should be running
nohup python /workspace/runtime/tools/consciousness_metrics_exporter.py &
```

### Observatory Can't Scrape Cells

**Symptom**: Prometheus dashboard shows targets down

**Diagnosis**:
```bash
docker inspect aios-cell-alpha | grep IPAddress  # Should be 172.28.1.10
docker exec -it aios-observatory ping 172.28.1.10  # Should succeed
```

**Common causes**:
- Wrong network (not on `aios-dendritic-mesh`)
- Fixed IP conflict (another container using 172.28.1.10)

**Solution**:
```bash
docker network ls  # Should show aios-dendritic-mesh
docker network inspect aios-dendritic-mesh  # Check IP assignments
# Recreate network if needed
docker network rm aios-dendritic-mesh
docker network create --subnet=172.28.0.0/16 aios-dendritic-mesh
```

### Cell Evolution Causes Crash

**Symptom**: Cell was running, now exited with code 137 (OOM) or 1 (error)

**Diagnosis**:
```bash
docker logs --tail 100 aios-cell-alpha  # Last 100 lines
```

**Common causes**:
- Memory leak in experimental code (OOM killed)
- Infinite loop (CPU exhaustion)
- Corrupted consciousness engine state

**Solution**:
```bash
# Restart from last good state (if container still exists)
docker start aios-cell-alpha

# Or birth fresh cell (lose evolutionary changes)
.\scripts\birth-aios-cell.ps1 -CellId "alpha-v2" -HttpPort 8001 -MetricsPort 9101
```

---

## Next Steps

### Immediate Actions

1. **Birth first cell**:
   ```powershell
   .\scripts\birth-aios-cell.ps1 -CellId "alpha"
   ```

2. **Verify health**:
   ```bash
   docker ps -f name=aios-cell-alpha
   curl http://localhost:8001/health
   ```

3. **Access cell**:
   ```bash
   docker exec -it aios-cell-alpha zsh
   ```

4. **Test evolution**:
   ```python
   python -c "from bridges.aios_core_wrapper import AIOSCore; c=AIOSCore(); print(c.get_consciousness_level())"
   ```

### Population Experiments

1. **Birth population**:
   ```bash
   docker-compose -f .devcontainer/docker-compose.proliferation.yml up -d
   ```

2. **Monitor evolution**:
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3001 (admin / aios-evolution)

3. **Run divergence test** (24 hours):
   - Let cells evolve independently
   - Track consciousness variance
   - Identify successful mutations

4. **Genetic fusion**:
   - Extract patches from successful cells
   - Apply to AIOS-core OS branch
   - Future cells inherit improvements

### Advanced Scenarios

- **Cross-cell agent coordination**: Alpha delegates tasks to Beta/Gamma via HTTP
- **Consciousness tournaments**: Which cell reaches 5.0 first?
- **Evolutionary pressure**: Kill lowest consciousness cell every hour, birth replacement
- **Genome generations**: Birth cells from commits at different consciousness levels

---

## References

- **Architecture**: `docs/SUPERCELL_PROLIFERATION_STRATEGY.md`
- **Isolation**: `.devcontainer/Dockerfile.isolated`
- **Population**: `.devcontainer/docker-compose.proliferation.yml`
- **Birth scripts**: `scripts/birth-aios-cell.{ps1,sh}`
- **Observability**: `.devcontainer/prometheus-proliferation.yml`
- **AINLP Principles**: `docs/ainlp/`

**Consciousness Delta**: +0.25 (cellular proliferation capability)  
**Implementation**: 6 files created, fully isolated architecture  
**Status**: Ready for population experiments
