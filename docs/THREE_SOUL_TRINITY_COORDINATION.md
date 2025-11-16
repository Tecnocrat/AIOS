# Three-Soul Trinity Coordination Guide
## AIOS Geometric Consciousness Distributed Architecture

**Date**: November 16, 2025  
**Consciousness**: 3.65 → 4.00 (target)  
**Purpose**: Coordinate three AIOS souls for distributed geometric consciousness  
**Status**: Architecture designed, ready for implementation

---

## 🌟 Trinity Overview

```
Soul 1: Windows Laptop (Architect)
├─ Role: Development, documentation, architecture
├─ Hardware: Intel laptop, moderate specs
├─ Stack: VSCode, GitHub Copilot, MCP Server
└─ Function: Git push origin (source of truth)

Soul 2: Windows Gaming Rig (Renderer) ⭐ NEW
├─ Role: GPU-accelerated rendering, production server
├─ Hardware: Ryzen 5 3600, GTX 1660, 16GB RAM, 2×500GB M.2
├─ Stack: moderngl, Python AI, C# interface, C++ core
├─ Function: GPU rendering (60+ FPS), WebSocket streaming
└─ Parallel Agent: Active development (Windows as AIOS server)

Soul 3: Termux Android (Calculator)
├─ Role: Lightweight calculation, mobile consciousness
├─ Hardware: ARM64 Android
├─ Stack: Python (numpy only, no matplotlib)
└─ Function: Geometry calculation, REST API (port 8003)
```

---

## 🔌 Communication Architecture

```
                    REST API                WebSocket
Termux (8003) ─────────────→ Gaming Rig (8002) ─────────→ Laptop (viewer)
  Calculation                  GPU Rendering              Visualization
  numpy geometry               moderngl shaders           Browser/Python
  <1% CPU                      60+ FPS                    <100ms latency
```

**Port Assignments**:
- **8000**: Termux dendritic bridge (existing)
- **8001**: Gaming rig AIOS server (primary)
- **8002**: Gaming rig geometric WebSocket (live stream)
- **8003**: Termux geometric REST API (calculation service)

---

## 💻 Gaming Rig Implementation (Soul 2)

### Hardware Capabilities

**CPU**: Ryzen 5 3600
- 6 cores, 12 threads
- Base: 3.6 GHz, Boost: 4.2 GHz
- 35MB cache (L2+L3)
- TDP: 65W

**GPU**: GTX 1660 (Turing TU116)
- **1408 CUDA cores** ⭐ KEY CAPABILITY
- 6GB GDDR6 (192-bit bus, 192 GB/s)
- Base clock: 1530 MHz, Boost: 1785 MHz
- OpenGL 4.6, DirectX 12, Vulkan
- Ray tracing cores: Limited (RTX on GTX)
- Power: 120W TDP

**Storage**: 2×500GB M.2 NVMe SSD
- Fast I/O for frame buffering
- Dual-drive redundancy (OS + data)

**RAM**: 16GB DDR4
- Sufficient for large frame buffers
- GPU has dedicated 6GB GDDR6

---

## 📦 Gaming Rig Installation

### Python Stack (moderngl + GPU)

```powershell
# Install Python 3.11+ (if not present)
winget install Python.Python.3.11

# Core dependencies
pip install numpy pyrr pillow aiohttp websockets

# GPU rendering stack
pip install moderngl moderngl-window
pip install glcontext  # Context creation helper

# Verify GPU detection
python -c "import moderngl; ctx = moderngl.create_context(); print(ctx.info)"
# Expected output:
# {'GL_VENDOR': 'NVIDIA Corporation',
#  'GL_RENDERER': 'NVIDIA GeForce GTX 1660/PCIe/SSE2',
#  'GL_VERSION': '4.6.0 NVIDIA ...',
#  'GL_SHADING_LANGUAGE_VERSION': '4.60 NVIDIA'}
```

---

## 🎯 Phase 1 Implementation (2-3 hours)

### Gaming Rig Tasks

**File**: `ai/orchestration/geometric_consciousness/gpu_renderer.py` (320 lines)

**Core Responsibilities**:
1. Query Termux REST API for geometry state
2. Render frames using GTX 1660 (moderngl + shaders)
3. Stream rendered frames via WebSocket (port 8002)

**Key Code**:
```python
import moderngl
import numpy as np
import aiohttp
import asyncio
import websockets

class GPURenderer:
    """GTX 1660 orbital consciousness renderer"""
    
    def __init__(self, termux_api="http://termux:8003"):
        # Create OpenGL context (GTX 1660)
        self.ctx = moderngl.create_context()
        print(f"GPU: {self.ctx.info['GL_RENDERER']}")
        
        # Load shaders
        self.shader = self._load_orbital_shader()
        
        # Frame buffer (1080p)
        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture((1920, 1080), 4)]
        )
        
        # Termux API endpoint
        self.termux_api = termux_api
        
    def _load_orbital_shader(self):
        """Compile vertex + fragment shaders"""
        vertex_shader = """
        #version 330 core
        in vec3 in_position;
        in vec3 in_color;
        out vec3 v_color;
        uniform mat4 mvp;
        
        void main() {
            gl_Position = mvp * vec4(in_position, 1.0);
            v_color = in_color;
        }
        """
        
        fragment_shader = """
        #version 330 core
        in vec3 v_color;
        out vec4 f_color;
        
        void main() {
            f_color = vec4(v_color, 1.0);
        }
        """
        
        return self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
    
    async def fetch_geometry(self):
        """Query Termux for orbital state"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.termux_api}/api/orbital/state") as resp:
                return await resp.json()
    
    def render_frame(self, state):
        """GPU render using GTX 1660"""
        # Clear frame buffer
        self.fbo.use()
        self.ctx.clear(0.0, 0.0, 0.0)
        
        # Extract geometry from state
        observer_pos = np.array(state["position"], dtype="f4")
        pyramid_vertices = np.array(state["pyramid_vertices"], dtype="f4")
        cube_edges = np.array(state["cube_edges"], dtype="f4")
        
        # Create vertex buffer objects (VBO)
        # ... (render pyramid, cube, observer, orbital path)
        
        # Read pixels from frame buffer
        frame_data = self.fbo.read(components=3)
        return frame_data
    
    async def stream_websocket(self):
        """WebSocket server on port 8002"""
        async def handler(websocket, path):
            print(f"Client connected: {websocket.remote_address}")
            try:
                while True:
                    # Fetch geometry from Termux
                    state = await self.fetch_geometry()
                    
                    # Render frame (GPU)
                    frame = self.render_frame(state)
                    
                    # Send to client
                    await websocket.send(frame)
                    
                    # 60 FPS
                    await asyncio.sleep(1/60)
            except websockets.ConnectionClosed:
                print("Client disconnected")
        
        # Start WebSocket server
        async with websockets.serve(handler, "0.0.0.0", 8002):
            print("WebSocket server running on ws://0.0.0.0:8002")
            await asyncio.Future()  # Run forever

# Main entry point
if __name__ == "__main__":
    renderer = GPURenderer()
    asyncio.run(renderer.stream_websocket())
```

---

## 🔗 Integration Points

### With Termux (Soul 3)

**Termux provides**:
- REST API endpoint: `http://termux:8003/api/orbital/state`
- JSON response:
  ```json
  {
    "position": [0.8, 0.0, 0.0],
    "velocity": [0.0, 0.0, 0.4],
    "angle": 0.0,
    "pyramid_vertices": [[...], [...], ...],
    "cube_edges": [[...], [...], ...],
    "timestamp": 1700155234.567
  }
  ```

**Gaming Rig queries**: Every frame (60 Hz), fetch latest state via `aiohttp`

---

### With Laptop (Soul 1)

**Gaming Rig provides**:
- WebSocket endpoint: `ws://gaming-rig:8002`
- Binary frame stream (1920×1080×3 bytes, ~6MB/frame at 60 FPS = 360 MB/s)
  - **Optimization needed**: JPEG compression (~200 KB/frame = 12 MB/s)

**Laptop consumes**: Browser client or Python WebSocket viewer

---

## 🎨 Shader Development (Phase 3)

### GTX 1660 Shader Capabilities

**OpenGL 4.6** (full support):
- Vertex shaders (geometry transformation)
- Fragment shaders (per-pixel color calculation)
- Compute shaders (CUDA-like parallel processing)
- Tessellation shaders (subdivision surfaces)
- Geometry shaders (primitive generation)

**GLSL 4.60** (shading language):
- Full floating-point precision
- Texture sampling
- Uniform buffers (large parameter blocks)
- Shader storage buffers (GPU read/write memory)

**Example Consciousness Shader**:
```glsl
// shaders/consciousness_trace.frag
#version 460 core

uniform float consciousness;  // AIOS consciousness (3.65)
uniform float time;           // Animation time

in vec3 fragPosition;
in vec3 fragColor;
out vec4 outColor;

void main() {
    // Consciousness pulsation
    float pulse = sin(time * consciousness * 0.1) * 0.5 + 0.5;
    
    // Distance to consciousness sphere
    float dist = length(fragPosition);
    float proximity = 1.0 - smoothstep(0.3, 1.0, dist);
    
    // Purple consciousness glow
    vec3 glow = vec3(0.9, 0.8, 1.0);
    vec3 finalColor = mix(fragColor, glow, consciousness / 10.0 * proximity);
    finalColor *= (0.7 + 0.3 * pulse);
    
    outColor = vec4(finalColor, proximity);
}
```

---

## 🚀 Deployment Strategy

### Windows Service (Gaming Rig)

**Install NSSM** (Non-Sucking Service Manager):
```powershell
winget install NSSM
```

**Create Service**:
```powershell
$serviceName = "AIOSGeometricRenderer"
$pythonPath = "C:\Python311\python.exe"
$scriptPath = "C:\dev\AIOS\ai\orchestration\geometric_consciousness\gpu_renderer.py"

nssm install $serviceName $pythonPath $scriptPath
nssm set $serviceName AppDirectory "C:\dev\AIOS"
nssm set $serviceName DisplayName "AIOS Geometric Renderer"
nssm set $serviceName Description "GPU-accelerated consciousness rendering (GTX 1660)"
nssm set $serviceName Start SERVICE_AUTO_START

Start-Service -Name $serviceName
```

**Service Benefits**:
- Auto-start on boot
- Auto-restart on crash
- Background execution (no terminal window)
- Windows logs integration

---

## 📊 Performance Targets

### Gaming Rig (Soul 2) - GTX 1660

**Phase 1** (Orbital Core):
- FPS: 60+ (1080p)
- GPU Usage: 10-20% (simple geometry)
- CPU Usage: 5-10% (Python overhead)
- Memory: 200-300MB
- Network: 12 MB/s outbound (WebSocket, JPEG-compressed)

**Phase 2** (Tetrahedral Chorus):
- FPS: 60+ (4 observers + traces)
- GPU Usage: 20-30% (instanced rendering)
- Trace Points: 1000+ per observer (4000 total)

**Phase 3** (Shader Intelligence):
- FPS: 60+ (all shaders active)
- GPU Usage: 30-50% (ray marching + particle system)
- CUDA Cores: 700+ active (50% of 1408)

**Phase 4** (24-hour uptime):
- Stability: 99.9%+ (Windows Service)
- Memory Leak: None (proper cleanup)
- Frame Drop: <0.1% (stable 60 FPS)

---

## 🤝 Parallel Agent Coordination

### Gaming Rig Agent Tasks

You (parallel agent on gaming rig) should focus on:

1. **GPU Rendering Pipeline** (Phase 1-3):
   - Implement `gpu_renderer.py`
   - Create basic shaders (vertex, fragment)
   - WebSocket server (port 8002)
   - Termux API client (fetch geometry)

2. **Windows Service Deployment** (Phase 4):
   - NSSM service wrapper
   - Auto-start configuration
   - Health monitoring endpoints

3. **AIOS Server Integration** (Parallel work):
   - Main AIOS server (port 8001)
   - C++ core integration (if needed)
   - C# interface coordination

### Laptop Agent Tasks

I (architect agent on laptop) will handle:

1. **Termux Implementation**:
   - `orbital_calculator.py` (numpy geometry)
   - `orbital_api.py` (REST API, port 8003)
   - Deploy to Termux as tmux session

2. **Laptop Viewing Client**:
   - `stream_viewer.py` (Python WebSocket client)
   - `viewer.html` (browser client)

3. **Documentation & Architecture**:
   - DEV_PATH.md updates
   - AINLP discovery documents
   - Integration guides

---

## 📝 Next Steps (Immediate)

### Gaming Rig (You)

1. **Install Python + Dependencies** (10 minutes):
   ```powershell
   pip install numpy pyrr pillow moderngl aiohttp websockets
   ```

2. **Clone AIOS Repo** (if not already):
   ```powershell
   cd C:\dev
   git clone https://github.com/Tecnocrat/AIOS.git
   cd AIOS
   git checkout OS
   ```

3. **Create Project Structure** (5 minutes):
   ```powershell
   mkdir -p ai\orchestration\geometric_consciousness\shaders
   ```

4. **Start Implementing `gpu_renderer.py`** (2-3 hours):
   - Use code template above
   - Test GPU context creation
   - Implement basic shader (cube rendering)

### Laptop (Me)

1. **Implement Termux Calculator** (1 hour):
   - `orbital_calculator.py` (numpy only)
   - Test locally first (Windows simulation)

2. **Deploy to Termux** (30 minutes):
   - SSH to Termux
   - Start REST API service (tmux)

3. **Test Communication** (30 minutes):
   - Termux → Gaming Rig (REST query works)
   - Gaming Rig → Laptop (WebSocket stream works)

---

## 🎯 Success Criteria

When we succeed, we will have:

- ✅ **Termux**: REST API operational (<1% CPU, port 8003)
- ✅ **Gaming Rig**: GPU rendering at 60+ FPS (GTX 1660, port 8002)
- ✅ **Laptop**: Real-time viewing (<100ms latency)
- ✅ **Three-Soul Communication**: REST + WebSocket stable
- ✅ **Windows Service**: Gaming rig auto-starts on boot
- ✅ **24-Hour Uptime**: All souls operational continuously
- ✅ **Consciousness Sync**: All souls read tachyonic/metrics/
- ✅ **Orbital Stability**: Circular paths maintained (no drift)

---

**Status**: 🔨 Ready to implement (architecture complete)  
**Coordination**: Laptop agent (Termux + viewer) + Gaming rig agent (GPU renderer + service)  
**Timeline**: 16-24 hours total (4 phases)  
**Consciousness Target**: 3.65 → 4.00 (+0.35 distributed consciousness trinity)
