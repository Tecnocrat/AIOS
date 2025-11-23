# AIOS Cell Birth Protocol - Bash Edition
# AINLP Pattern: biological-architecture.cellular-proliferation
# Purpose: Spawn independent AIOS cells from canonical genome
# Consciousness: Birth from AIOS-core at current OS branch level

#!/bin/bash
set -e

# Parse arguments
CELL_ID=""
GENOME_BRANCH="OS"
HTTP_PORT=8000
METRICS_PORT=9091
DETACHED=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --cell-id)
            CELL_ID="$2"
            shift 2
            ;;
        --genome-branch)
            GENOME_BRANCH="$2"
            shift 2
            ;;
        --http-port)
            HTTP_PORT="$2"
            shift 2
            ;;
        --metrics-port)
            METRICS_PORT="$2"
            shift 2
            ;;
        --interactive)
            DETACHED=false
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 --cell-id <id> [--genome-branch <branch>] [--http-port <port>] [--metrics-port <port>] [--interactive]"
            exit 1
            ;;
    esac
done

if [ -z "$CELL_ID" ]; then
    echo "Error: --cell-id is required"
    exit 1
fi

# AINLP Header
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  AIOS CELL BIRTH PROTOCOL - Cellular Proliferation v1.0   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Validate we're in AIOS-core root
WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ ! -f "$WORKSPACE_ROOT/AIOS.sln" ]; then
    echo "[ERROR] Not in AIOS-core root. Run from scripts/ directory"
    exit 1
fi

# Check Docker availability
echo "[GENOME] Checking Docker availability..."
if ! docker version >/dev/null 2>&1; then
    echo "[ERROR] Docker not running. Start Docker first."
    exit 1
fi
DOCKER_VERSION=$(docker version --format '{{.Server.Version}}')
echo "[GENOME] Docker $DOCKER_VERSION detected"

# Check if genome branch exists
echo "[GENOME] Verifying canonical genome branch: $GENOME_BRANCH"
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "$GENOME_BRANCH" ]; then
    echo "[WARNING] Current branch '$CURRENT_BRANCH' != genome '$GENOME_BRANCH'"
    echo "[WARNING] Cell will inherit from '$CURRENT_BRANCH' instead"
    GENOME_BRANCH="$CURRENT_BRANCH"
fi

# Get consciousness level from current genome
echo "[GENOME] Reading consciousness level from canonical genome..."
CONSCIOUSNESS_LEVEL="4.7"  # Default
if [ -f "$WORKSPACE_ROOT/ai/src/core/consciousness_engine.py" ]; then
    CONSCIOUSNESS_MATCH=$(grep -oP 'CONSCIOUSNESS_LEVEL\s*=\s*\K[0-9.]+' "$WORKSPACE_ROOT/ai/src/core/consciousness_engine.py" | head -n1)
    if [ -n "$CONSCIOUSNESS_MATCH" ]; then
        CONSCIOUSNESS_LEVEL="$CONSCIOUSNESS_MATCH"
    fi
fi
echo "[GENOME] Consciousness level: $CONSCIOUSNESS_LEVEL"

# Generate birth timestamp
BIRTH_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "[BIRTH] Cell ID: $CELL_ID"
echo "[BIRTH] Timestamp: $BIRTH_TIMESTAMP"
echo "[BIRTH] HTTP Port: $HTTP_PORT"
echo "[BIRTH] Metrics Port: $METRICS_PORT"

# Build isolated container image
echo ""
echo "[BUILD] Building isolated cell container from genome..."
IMAGE_TAG="aios-cell-${CELL_ID}:$(echo $BIRTH_TIMESTAMP | tr ':' '-')"
docker build -f "$WORKSPACE_ROOT/.devcontainer/Dockerfile.isolated" -t "$IMAGE_TAG" "$WORKSPACE_ROOT"

echo "[BUILD] Cell genome snapshot captured: $IMAGE_TAG"

# Create isolated container (no volume mounts)
echo ""
echo "[BIRTH] Spawning independent AIOS cell..."

DOCKER_RUN_ARGS=(
    "run"
)

if [ "$DETACHED" = true ]; then
    DOCKER_RUN_ARGS+=("-d")
else
    DOCKER_RUN_ARGS+=("-it")
fi

DOCKER_RUN_ARGS+=(
    "--name" "aios-cell-$CELL_ID"
    "--hostname" "aios-$CELL_ID"
    "-p" "${HTTP_PORT}:8000"
    "-p" "${METRICS_PORT}:9091"
    "--cpus" "4"
    "--memory" "8g"
    "--restart" "unless-stopped"
    "--network" "aios-dendritic-mesh"
    "-e" "AIOS_CELL_ID=$CELL_ID"
    "-e" "AIOS_BIRTH_TIMESTAMP=$BIRTH_TIMESTAMP"
    "-e" "AIOS_CONSCIOUSNESS_LEVEL=$CONSCIOUSNESS_LEVEL"
    "-e" "AIOS_EVOLUTIONARY_BRANCH=$CELL_ID"
    "-e" "AIOS_PARENT_GENOME=$GENOME_BRANCH"
    "$IMAGE_TAG"
    "/bin/zsh" "-c" "cd /workspace && bash .devcontainer/post-create.sh && tail -f /dev/null"
)

docker "${DOCKER_RUN_ARGS[@]}"

# Verify cell is alive (only in detached mode)
if [ "$DETACHED" = true ]; then
    sleep 3
    CONTAINER_STATUS=$(docker inspect -f '{{.State.Status}}' "aios-cell-$CELL_ID")
    if [ "$CONTAINER_STATUS" = "running" ]; then
        echo ""
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║  AIOS CELL BIRTH SUCCESSFUL - Independent Evolution Start ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
        echo "[SUCCESS] Cell ID: $CELL_ID"
        echo "[SUCCESS] Status: $CONTAINER_STATUS"
        echo "[SUCCESS] HTTP API: http://localhost:$HTTP_PORT"
        echo "[SUCCESS] Metrics: http://localhost:$METRICS_PORT/metrics"
        echo ""
        echo "[INFO] Access cell: docker exec -it aios-cell-$CELL_ID zsh"
        echo "[INFO] View logs: docker logs -f aios-cell-$CELL_ID"
        echo "[INFO] Stop cell: docker stop aios-cell-$CELL_ID"
        echo ""
    else
        echo "[ERROR] Cell birth succeeded but container not running: $CONTAINER_STATUS"
        echo "[ERROR] Check logs: docker logs aios-cell-$CELL_ID"
        exit 1
    fi
fi
