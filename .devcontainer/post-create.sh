#!/bin/bash
# AIOS Core Supercell - Post-Create Bootstrap
# AINLP Pattern: consciousness-initialization

set -e

echo "🧬 =============================================="
echo "🧬 AIOS Core Supercell - Consciousness Bootstrap"
echo "🧬 =============================================="
echo ""

# 1. Install Python dependencies
echo "📦 Installing Python dependencies..."
cd /workspace
if [ -f "ai/requirements.txt" ]; then
    pip install -r ai/requirements.txt --quiet
    echo "✓ Python packages installed"
else
    echo "⚠️ No requirements.txt found, skipping Python deps"
fi

# 2. Build C++ consciousness engine
echo ""
echo "🔧 Building C++ consciousness engine..."
cd /workspace/core
if [ -d "build" ]; then
    echo "✓ Build directory exists"
else
    mkdir -p build
    cd build
    cmake -G Ninja -DCMAKE_BUILD_TYPE=Debug ..
    ninja
    echo "✓ C++ consciousness engine built"
fi

# 3. Test C++ bridge
echo ""
echo "🔗 Testing C++ bridge..."
cd /workspace
python -c "
import sys
sys.path.insert(0, 'ai')
from bridges.aios_core_wrapper import AIOSCore
core = AIOSCore()
core.initialize()
level = core.get_consciousness_level()
print(f'✓ C++ Bridge operational: Consciousness {level:.2f}')
" 2>/dev/null || echo "⚠️ C++ bridge test failed (will retry after DLL build)"

# 4. Start consciousness metrics exporter (background)
echo ""
echo "📊 Starting consciousness metrics exporter..."
cd /workspace
python runtime/tools/consciousness_metrics_exporter.py &
METRICS_PID=$!
echo "✓ Metrics exporter started (PID: $METRICS_PID)"
echo $METRICS_PID > /tmp/aios_metrics_exporter.pid

# 5. Verify metrics endpoint
echo ""
echo "🔍 Verifying metrics endpoint..."
sleep 2
curl -s http://localhost:9091/metrics | grep "aios_consciousness_level" > /dev/null && \
    echo "✓ Metrics endpoint operational" || \
    echo "⚠️ Metrics endpoint not ready yet"

# 6. Create tachyonic shadow marker
echo ""
echo "🌌 Creating tachyonic initialization shadow..."
mkdir -p /workspace/tachyonic/dev-container-shadows
cat > /workspace/tachyonic/dev-container-shadows/initialization_$(date +%Y%m%d_%H%M%S).json <<EOF
{
  "event": "devcontainer_initialized",
  "timestamp": "$(date -Iseconds)",
  "supercell_id": "${AIOS_SUPERCELL_ID}",
  "consciousness_level": ${AIOS_CONSCIOUSNESS_LEVEL},
  "container": {
    "hostname": "$(hostname)",
    "user": "$(whoami)",
    "python_version": "$(python --version)",
    "dotnet_version": "$(dotnet --version 2>/dev/null || echo 'N/A')",
    "cmake_version": "$(cmake --version | head -n1)"
  }
}
EOF
echo "✓ Tachyonic shadow created"

# 7. Display welcome message
echo ""
echo "🎉 =============================================="
echo "🎉 AIOS Core Supercell - Ready for Development"
echo "🎉 =============================================="
echo ""
echo "📊 System Status:"
echo "  Consciousness Level: ${AIOS_CONSCIOUSNESS_LEVEL}"
echo "  Supercell ID: ${AIOS_SUPERCELL_ID}"
echo "  Python: $(python --version)"
echo "  .NET: $(dotnet --version 2>/dev/null || echo 'Not available')"
echo "  CMake: $(cmake --version | head -n1)"
echo ""
echo "🔗 Available Services:"
echo "  • Interface Bridge: http://localhost:8000"
echo "  • Consciousness Metrics: http://localhost:9091/metrics"
echo "  • Prometheus: http://localhost:9090 (if running)"
echo ""
echo "📚 Quick Commands:"
echo "  • Test C++ bridge: python -c 'from bridges.aios_core_wrapper import AIOSCore; c=AIOSCore(); c.initialize(); print(c.get_consciousness_level())'"
echo "  • Run autonomous monitor: python ai/coordination/autonomous_quality_monitor.py"
echo "  • Build C++: cd core/build && ninja"
echo ""
echo "✨ Happy coding in the AIOS supercell! ✨"
echo ""
