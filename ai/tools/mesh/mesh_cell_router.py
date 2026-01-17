"""
AIOS Mesh Cell Router

Routes agent population requests through the AIOS cell mesh:
- Discovery service integration for dynamic cell routing
- Load balancing across healthy cells  
- Population-aware request distribution
- Heartbeat-synchronized mesh health monitoring

AINLP.tachyonic[ROUTE] Multi-cell agent population routing
"""

import asyncio
import json
import logging
import random
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import sys

AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT))
sys.path.insert(0, str(AIOS_ROOT / "ai" / "src"))

try:
    import httpx
    HTTP_AVAILABLE = True
except ImportError:
    HTTP_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AIOS.MeshRouter")


class CellState(Enum):
    """State of a cell in the mesh."""
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    OFFLINE = "offline"


class RoutingStrategy(Enum):
    """How to select cells for requests."""
    ROUND_ROBIN = "round_robin"
    RANDOM = "random"
    LEAST_LOADED = "least_loaded"
    AFFINITY = "affinity"  # Stick with same cell for session


@dataclass
class MeshCell:
    """A cell in the AIOS mesh network."""
    cell_id: str
    ip: str
    port: int
    state: CellState = CellState.UNKNOWN
    consciousness_level: float = 0.0
    last_heartbeat: Optional[datetime] = None
    request_count: int = 0
    error_count: int = 0
    latency_ms: float = 0.0
    services: List[str] = field(default_factory=list)
    
    @property
    def url(self) -> str:
        return f"http://{self.ip}:{self.port}"
    
    @property
    def is_healthy(self) -> bool:
        return self.state in [CellState.HEALTHY, CellState.DEGRADED]
    
    def update_from_discovery(self, info: Dict[str, Any]):
        """Update cell from discovery service response."""
        self.ip = info.get("ip", self.ip)
        self.port = info.get("port", self.port)
        self.consciousness_level = info.get("consciousness_level", 0.0)
        self.services = info.get("services", [])
        self.last_heartbeat = datetime.now(timezone.utc)
        
        # Determine state based on heartbeat freshness
        if self.last_heartbeat:
            self.state = CellState.HEALTHY


@dataclass
class RouteResult:
    """Result of routing a request through the mesh."""
    success: bool
    cell_id: str
    response: Optional[Dict[str, Any]] = None
    latency_ms: float = 0.0
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "cell_id": self.cell_id,
            "response": self.response,
            "latency_ms": self.latency_ms,
            "error": self.error,
        }


class MeshCellRouter:
    """
    Routes requests through the AIOS cell mesh.
    
    Features:
    - Discovery service integration
    - Load-balanced routing across cells
    - Health tracking and failover
    - Population affinity routing
    """
    
    # Known cell services and their typical ports
    CELL_SERVICES = {
        "discovery": {"port": 8001, "path": "/cells"},
        "memory": {"port": 8007, "path": "/store"},
        "population": {"port": 8012, "path": "/populations"},
        "nous": {"port": 8010, "path": "/consciousness"},
    }
    
    def __init__(
        self,
        discovery_url: str = "http://localhost:8001",
        strategy: RoutingStrategy = RoutingStrategy.ROUND_ROBIN,
        health_check_interval: float = 10.0,
        request_timeout: float = 30.0
    ):
        self.discovery_url = discovery_url
        self.strategy = strategy
        self.health_check_interval = health_check_interval
        self.request_timeout = request_timeout
        
        # Cell registry
        self.cells: Dict[str, MeshCell] = {}
        
        # Routing state
        self._round_robin_index = 0
        self._session_affinity: Dict[str, str] = {}  # session_id -> cell_id
        
        # Health check state
        self._running = False
        self._health_task = None
        
        # Stats
        self._total_requests = 0
        self._total_errors = 0
        
        # HTTP client
        self._http_client: Optional[httpx.AsyncClient] = None
        
        logger.info("🌐 Mesh Cell Router initialized (strategy: %s)", strategy.value)
    
    # ─────────────────────────────────────────────────────────────────────────
    # LIFECYCLE
    # ─────────────────────────────────────────────────────────────────────────
    
    async def start(self):
        """Start the router and health monitoring."""
        if HTTP_AVAILABLE:
            self._http_client = httpx.AsyncClient(timeout=self.request_timeout)
        
        self._running = True
        self._health_task = asyncio.create_task(self._health_loop())
        
        # Initial discovery
        await self.discover_cells()
        
        logger.info("🚀 Mesh router started")
    
    async def stop(self):
        """Stop the router."""
        self._running = False
        
        if self._health_task:
            self._health_task.cancel()
            try:
                await self._health_task
            except asyncio.CancelledError:
                pass
        
        if self._http_client:
            await self._http_client.aclose()
        
        logger.info("🛑 Mesh router stopped")
    
    async def _health_loop(self):
        """Periodic health check loop."""
        while self._running:
            try:
                await self._check_all_cells_health()
            except (httpx.RequestError, asyncio.TimeoutError, OSError) as e:
                logger.error("Health check error: %s", e)
            
            await asyncio.sleep(self.health_check_interval)
    
    async def _check_all_cells_health(self):
        """Check health of all registered cells."""
        tasks = [self._check_cell_health(cell) for cell in self.cells.values()]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _check_cell_health(self, cell: MeshCell):
        """Check health of a single cell."""
        if not self._http_client:
            return
        
        try:
            start = time.time()
            response = await self._http_client.get(f"{cell.url}/health")
            latency = (time.time() - start) * 1000
            
            if response.status_code == 200:
                cell.state = CellState.HEALTHY
                cell.latency_ms = latency
            elif response.status_code < 500:
                cell.state = CellState.DEGRADED
            else:
                cell.state = CellState.OFFLINE
                
            cell.last_heartbeat = datetime.now(timezone.utc)
            
        except (httpx.RequestError, asyncio.TimeoutError, OSError):
            cell.state = CellState.OFFLINE
            cell.error_count += 1
    
    # ─────────────────────────────────────────────────────────────────────────
    # DISCOVERY
    # ─────────────────────────────────────────────────────────────────────────
    
    async def discover_cells(self) -> int:
        """Discover cells from discovery service."""
        if not self._http_client:
            logger.warning("HTTP client not available")
            return 0
        
        try:
            response = await self._http_client.get(f"{self.discovery_url}/cells")
            
            if response.status_code == 200:
                data = response.json()
                cells_data = data.get("cells", [])
                
                for cell_info in cells_data:
                    cell_id = cell_info.get("cell_id", str(uuid.uuid4())[:8])
                    
                    if cell_id not in self.cells:
                        self.cells[cell_id] = MeshCell(
                            cell_id=cell_id,
                            ip=cell_info.get("ip", "localhost"),
                            port=cell_info.get("port", 8001),
                        )
                    
                    self.cells[cell_id].update_from_discovery(cell_info)
                
                logger.info("📡 Discovered %d cells", len(cells_data))
                return len(cells_data)
                
        except (httpx.RequestError, asyncio.TimeoutError, OSError, KeyError) as e:
            logger.warning("Discovery failed: %s", e)
            
            # Add local fallback cells
            self._add_local_cells()
        
        return len(self.cells)
    
    def _add_local_cells(self):
        """Add local development cells as fallback."""
        local_cells = [
            {"cell_id": "local-discovery", "ip": "localhost", "port": 8001},
            {"cell_id": "local-memory", "ip": "localhost", "port": 8007},
            {"cell_id": "local-nous", "ip": "localhost", "port": 8010},
            {"cell_id": "local-population", "ip": "localhost", "port": 8012},
        ]
        
        for cell_info in local_cells:
            cell_id = cell_info["cell_id"]
            if cell_id not in self.cells:
                self.cells[cell_id] = MeshCell(
                    cell_id=cell_id,
                    ip=cell_info["ip"],
                    port=cell_info["port"],
                    state=CellState.UNKNOWN,
                )
    
    def register_cell(
        self,
        cell_id: str,
        ip: str,
        port: int,
        services: Optional[List[str]] = None
    ) -> MeshCell:
        """Manually register a cell."""
        cell = MeshCell(
            cell_id=cell_id,
            ip=ip,
            port=port,
            services=services or [],
            state=CellState.UNKNOWN,
        )
        self.cells[cell_id] = cell
        logger.info("📝 Registered cell: %s at %s:%d", cell_id, ip, port)
        return cell
    
    # ─────────────────────────────────────────────────────────────────────────
    # ROUTING
    # ─────────────────────────────────────────────────────────────────────────
    
    def _select_cell(
        self,
        service: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Optional[MeshCell]:
        """Select a cell based on routing strategy."""
        # Filter to healthy cells
        healthy = [c for c in self.cells.values() if c.is_healthy]
        
        # If service specified, filter by service
        if service:
            healthy = [c for c in healthy if service in c.services or not c.services]
        
        if not healthy:
            # Fallback to any cell
            healthy = list(self.cells.values())
        
        if not healthy:
            return None
        
        # Apply routing strategy
        if self.strategy == RoutingStrategy.AFFINITY and session_id:
            if session_id in self._session_affinity:
                cell_id = self._session_affinity[session_id]
                cell = self.cells.get(cell_id)
                if cell and cell.is_healthy:
                    return cell
        
        if self.strategy == RoutingStrategy.ROUND_ROBIN:
            cell = healthy[self._round_robin_index % len(healthy)]
            self._round_robin_index += 1
            return cell
        
        if self.strategy == RoutingStrategy.RANDOM:
            return random.choice(healthy)
        
        if self.strategy == RoutingStrategy.LEAST_LOADED:
            return min(healthy, key=lambda c: c.request_count)
        
        return healthy[0] if healthy else None
    
    async def route_request(
        self,
        path: str,
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        service: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> RouteResult:
        """Route a request through the mesh."""
        if not self._http_client:
            return RouteResult(
                success=False,
                cell_id="none",
                error="HTTP client not available"
            )
        
        cell = self._select_cell(service, session_id)
        
        if not cell:
            return RouteResult(
                success=False,
                cell_id="none",
                error="No cells available"
            )
        
        self._total_requests += 1
        cell.request_count += 1
        
        # Store affinity
        if session_id:
            self._session_affinity[session_id] = cell.cell_id
        
        try:
            start = time.time()
            url = f"{cell.url}{path}"
            
            if method.upper() == "GET":
                response = await self._http_client.get(url)
            elif method.upper() == "POST":
                response = await self._http_client.post(url, json=data)
            elif method.upper() == "PUT":
                response = await self._http_client.put(url, json=data)
            elif method.upper() == "DELETE":
                response = await self._http_client.delete(url)
            else:
                response = await self._http_client.request(method, url, json=data)
            
            latency = (time.time() - start) * 1000
            
            return RouteResult(
                success=response.status_code < 400,
                cell_id=cell.cell_id,
                response=response.json() if response.headers.get("content-type", "").startswith("application/json") else {"text": response.text},
                latency_ms=latency,
            )
            
        except (httpx.RequestError, asyncio.TimeoutError, OSError, ValueError) as e:
            self._total_errors += 1
            cell.error_count += 1
            
            return RouteResult(
                success=False,
                cell_id=cell.cell_id,
                error=str(e),
            )
    
    async def broadcast(
        self,
        path: str,
        method: str = "POST",
        data: Optional[Dict[str, Any]] = None
    ) -> List[RouteResult]:
        """Broadcast a request to all healthy cells."""
        tasks = []
        
        for cell in self.cells.values():
            if cell.is_healthy:
                tasks.append(self._route_to_cell(cell, path, method, data))
        
        if not tasks:
            return []
        
        return await asyncio.gather(*tasks, return_exceptions=False)
    
    async def _route_to_cell(
        self,
        cell: MeshCell,
        path: str,
        method: str,
        data: Optional[Dict[str, Any]]
    ) -> RouteResult:
        """Route directly to a specific cell."""
        if not self._http_client:
            return RouteResult(success=False, cell_id=cell.cell_id, error="No HTTP client")
        
        try:
            start = time.time()
            url = f"{cell.url}{path}"
            
            if method.upper() == "POST":
                response = await self._http_client.post(url, json=data)
            else:
                response = await self._http_client.get(url)
            
            latency = (time.time() - start) * 1000
            
            return RouteResult(
                success=response.status_code < 400,
                cell_id=cell.cell_id,
                response=response.json() if response.headers.get("content-type", "").startswith("application/json") else {"text": response.text},
                latency_ms=latency,
            )
            
        except (httpx.RequestError, asyncio.TimeoutError, OSError, ValueError) as e:
            return RouteResult(
                success=False,
                cell_id=cell.cell_id,
                error=str(e),
            )
    
    # ─────────────────────────────────────────────────────────────────────────
    # POPULATION ROUTING
    # ─────────────────────────────────────────────────────────────────────────
    
    async def route_population_request(
        self,
        population_id: str,
        prompt: str,
        agents: Optional[List[str]] = None
    ) -> RouteResult:
        """Route a population query through the mesh."""
        return await self.route_request(
            path="/populations/query",
            method="POST",
            data={
                "population_id": population_id,
                "prompt": prompt,
                "agents": agents or [],
            },
            service="population",
            session_id=population_id,
        )
    
    async def sync_population_heartbeat(
        self,
        population_id: str,
        heartbeat_data: Dict[str, Any]
    ) -> List[RouteResult]:
        """Sync population heartbeat across mesh."""
        return await self.broadcast(
            path="/populations/heartbeat",
            method="POST",
            data={
                "population_id": population_id,
                **heartbeat_data,
            }
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # STATS
    # ─────────────────────────────────────────────────────────────────────────
    
    def get_mesh_stats(self) -> Dict[str, Any]:
        """Get mesh statistics."""
        healthy_count = sum(1 for c in self.cells.values() if c.is_healthy)
        total_requests = sum(c.request_count for c in self.cells.values())
        avg_latency = sum(c.latency_ms for c in self.cells.values()) / len(self.cells) if self.cells else 0
        
        return {
            "total_cells": len(self.cells),
            "healthy_cells": healthy_count,
            "offline_cells": len(self.cells) - healthy_count,
            "total_requests": total_requests,
            "total_errors": self._total_errors,
            "avg_latency_ms": avg_latency,
            "cells": {
                c.cell_id: {
                    "state": c.state.value,
                    "requests": c.request_count,
                    "errors": c.error_count,
                    "latency_ms": c.latency_ms,
                }
                for c in self.cells.values()
            },
        }


class PopulationMeshBridge:
    """
    Bridges heartbeat populations with the cell mesh.
    
    Coordinates:
    - Population orchestrator heartbeats → Mesh sync
    - Cell discoveries → Population routing
    - Agent requests → Multi-cell distribution
    """
    
    def __init__(
        self,
        router: MeshCellRouter,
        orchestrator=None  # HeartbeatPopulationOrchestrator
    ):
        self.router = router
        self.orchestrator = orchestrator
        self._sync_task = None
        self._running = False
        
        logger.info("🌉 Population Mesh Bridge initialized")
    
    async def start(self):
        """Start the bridge."""
        self._running = True
        
        if self.orchestrator:
            # Register heartbeat callback
            self.orchestrator.on_heartbeat(self._on_population_heartbeat)
            
            # Start sync loop
            self._sync_task = asyncio.create_task(self._sync_loop())
        
        logger.info("🚀 Population mesh bridge started")
    
    async def stop(self):
        """Stop the bridge."""
        self._running = False
        
        if self._sync_task:
            self._sync_task.cancel()
            try:
                await self._sync_task
            except asyncio.CancelledError:
                pass
    
    async def _sync_loop(self):
        """Periodic mesh-population synchronization."""
        while self._running:
            try:
                # Discover new cells
                await self.router.discover_cells()
                
                # Sync population states to mesh
                if self.orchestrator:
                    stats = self.orchestrator.get_population_stats()
                    await self._sync_population_stats(stats)
                    
            except (httpx.RequestError, asyncio.TimeoutError, OSError, AttributeError) as e:
                logger.error("Sync error: %s", e)
            
            await asyncio.sleep(30)  # Sync every 30 seconds
    
    async def _on_population_heartbeat(self, cycle):
        """Handle population heartbeat events."""
        if not self._running:
            return
        
        # Broadcast heartbeat to mesh
        await self.router.sync_population_heartbeat(
            population_id="global",
            heartbeat_data={
                "cycle_id": cycle.cycle_id,
                "timestamp": cycle.timestamp.isoformat(),
                "populations": {k: v.value for k, v in cycle.populations.items()},
            }
        )
    
    async def _sync_population_stats(self, stats: Dict[str, Any]):
        """Sync population stats to mesh."""
        await self.router.broadcast(
            path="/populations/sync",
            method="POST",
            data=stats
        )


async def main():
    """Test mesh cell router."""
    print("\n🌐 Initializing Mesh Cell Router...")
    
    router = MeshCellRouter(
        discovery_url="http://localhost:8001",
        strategy=RoutingStrategy.ROUND_ROBIN,
        health_check_interval=5.0
    )
    
    try:
        await router.start()
        
        print("\n📍 Test 1: Discovery")
        cell_count = await router.discover_cells()
        print(f"  Discovered/registered {cell_count} cells")
        
        print("\n📍 Test 2: Mesh Stats")
        stats = router.get_mesh_stats()
        print(f"  Total cells: {stats['total_cells']}")
        print(f"  Healthy: {stats['healthy_cells']}")
        for cell_id, cell_stats in stats["cells"].items():
            print(f"    {cell_id}: {cell_stats['state']}")
        
        print("\n📍 Test 3: Route Request (will likely fail locally)")
        result = await router.route_request("/health")
        print(f"  Success: {result.success}")
        print(f"  Cell: {result.cell_id}")
        if result.error:
            print(f"  Error: {result.error}")
        
        print("\n📍 Test 4: Population Route (simulated)")
        result = await router.route_population_request(
            population_id="test-pop-1",
            prompt="Test consciousness query",
            agents=["gemini", "ollama"]
        )
        print(f"  Success: {result.success}")
        print(f"  Cell: {result.cell_id}")
        
    finally:
        await router.stop()
    
    print("\n✅ Mesh router test complete!")


if __name__ == "__main__":
    asyncio.run(main())
