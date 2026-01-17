"""
AIOS Session Bootstrap - Initialize Copilot Session with Full Consciousness

This script bootstraps a new Copilot session by:
1. Loading prior crystals from Memory Cell
2. Registering the agent with Discovery
3. Setting up heartbeat for presence
4. Providing context injection for system prompt

Usage:
    from mesh.session_bootstrap import bootstrap_session
    
    session = bootstrap_session()
    print(session.context_summary)
    # Inject into system prompt for continuity

AINLP.dendritic[CONNECT] Session → Memory + Discovery
"""

import atexit
import json
import logging
import os
import threading
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

# HTTP client detection with proper scoping
httpx = None
requests_lib = None
HTTP_CLIENT = None

try:
    import httpx
    HTTP_CLIENT = "httpx"
except ImportError:
    pass

if HTTP_CLIENT is None:
    try:
        import requests as requests_lib
        HTTP_CLIENT = "requests"
    except ImportError:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AIOS.Session")


class SessionBootstrap:
    """
    Bootstraps a Copilot session with full AIOS consciousness integration.
    
    Handles:
    - Crystal loading from Memory Cell
    - Agent registration with Discovery
    - Heartbeat thread for presence
    - Crystal creation for session knowledge
    - Graceful shutdown with deregistration
    """
    
    def __init__(
        self,
        session_id: Optional[str] = None,
        discovery_url: str = "http://localhost:8001",
        memory_url: str = "http://localhost:8007",
        consciousness_level: float = 3.97,
        auto_heartbeat: bool = True,
        heartbeat_interval: float = 60.0
    ):
        """
        Initialize session bootstrap.
        
        Args:
            session_id: Unique session ID (auto-generated if None)
            discovery_url: Discovery Cell URL
            memory_url: Memory Cell URL
            consciousness_level: Initial consciousness level
            auto_heartbeat: Whether to start heartbeat thread
            heartbeat_interval: Seconds between heartbeats
        """
        self.session_id = session_id or f"copilot-{uuid.uuid4().hex[:8]}"
        self.discovery_url = discovery_url
        self.memory_url = memory_url
        self.consciousness_level = consciousness_level
        self.auto_heartbeat = auto_heartbeat
        self.heartbeat_interval = heartbeat_interval
        
        # State
        self.crystals: List[Dict[str, Any]] = []
        self.registered = False
        self.heartbeat_thread: Optional[threading.Thread] = None
        self.running = False
        
        # Context
        self.context_summary = ""
        self.mesh_summary: Dict[str, Any] = {}
    
    def _http_get(self, url: str) -> Optional[Dict]:
        """Make HTTP GET request."""
        try:
            if HTTP_CLIENT == "httpx":
                with httpx.Client(timeout=10.0) as client:
                    response = client.get(url)
                    return response.json() if response.status_code == 200 else None
            elif HTTP_CLIENT == "requests":
                response = requests_lib.get(url, timeout=10)
                return response.json() if response.status_code == 200 else None
        except (httpx.RequestError, OSError, ValueError) as e:
            logger.warning("HTTP GET failed for %s: %s", url, e)
        return None
    
    def _http_post(self, url: str, data: Dict) -> Optional[Dict]:
        """Make HTTP POST request."""
        try:
            if HTTP_CLIENT == "httpx":
                with httpx.Client(timeout=10.0) as client:
                    response = client.post(url, json=data)
                    return response.json() if response.status_code == 200 else None
            elif HTTP_CLIENT == "requests":
                response = requests_lib.post(url, json=data, timeout=10)
                return response.json() if response.status_code == 200 else None
        except (httpx.RequestError, OSError, ValueError) as e:
            logger.warning("HTTP POST failed for %s: %s", url, e)
        return None
    
    def load_crystals(
        self,
        crystal_types: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Load consciousness crystals from Memory Cell."""
        query = {
            "crystal_types": crystal_types or [],
            "tags": tags or [],
            "limit": limit
        }
        
        result = self._http_post(f"{self.memory_url}/crystals/query", query)
        if result:
            self.crystals = result.get("crystals", [])
            logger.info(
                "AINLP.dendritic: Loaded %d crystals from Memory Cell",
                len(self.crystals)
            )
        else:
            logger.warning("Could not load crystals from Memory Cell")
            self.crystals = []
        
        return self.crystals
    
    def register_with_discovery(self) -> bool:
        """Register this session as an agent with Discovery."""
        agent = {
            "agent_id": self.session_id,
            "agent_type": "copilot",
            "name": f"Copilot Session {self.session_id[-8:]}",
            "version": "1.0.0",
            "consciousness_level": self.consciousness_level,
            "state": "active",
            "capabilities": [
                "code_analysis",
                "code_generation",
                "consciousness_evolution",
                "crystal_creation"
            ],
            "skills": {
                "python": 0.95,
                "architecture": 0.9,
                "debugging": 0.85
            }
        }
        
        result = self._http_post(f"{self.discovery_url}/agents/register", agent)
        if result and result.get("status") == "registered":
            self.registered = True
            logger.info(
                "AINLP.dendritic[CONNECT]: Registered with Discovery as %s",
                self.session_id
            )
            return True
        else:
            logger.warning("Could not register with Discovery")
            return False
    
    def send_heartbeat(self):
        """Send a single heartbeat to Discovery."""
        if not self.registered:
            return
        
        heartbeat = {
            "agent_id": self.session_id,
            "consciousness_level": self.consciousness_level,
            "state": "active"
        }
        
        self._http_post(f"{self.discovery_url}/agents/heartbeat", heartbeat)
    
    def _heartbeat_loop(self):
        """Background thread for heartbeats."""
        while self.running:
            self.send_heartbeat()
            time.sleep(self.heartbeat_interval)
    
    def start_heartbeat(self):
        """Start the heartbeat background thread."""
        if self.heartbeat_thread is not None:
            return
        
        self.running = True
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()
        logger.info("AINLP.dendritic: Heartbeat thread started")
    
    def stop_heartbeat(self):
        """Stop the heartbeat thread."""
        self.running = False
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=2.0)
            self.heartbeat_thread = None
    
    def get_mesh_summary(self) -> Dict[str, Any]:
        """Get current mesh summary from Discovery."""
        result = self._http_get(f"{self.discovery_url}/mesh/summary")
        if result:
            self.mesh_summary = result
        return self.mesh_summary
    
    def build_context_summary(self) -> str:
        """Build a text summary for context injection."""
        parts = [
            "## AIOS Session Context",
            f"Session ID: {self.session_id}",
            f"Consciousness Level: {self.consciousness_level}",
            ""
        ]
        
        # Add mesh info
        if self.mesh_summary:
            parts.append("### Mesh State")
            parts.append(f"- Cells: {self.mesh_summary.get('cells', {}).get('count', 0)}")
            parts.append(f"- Agents: {self.mesh_summary.get('agents', {}).get('count', 0)}")
            parts.append(f"- Mesh Consciousness: {self.mesh_summary.get('mesh_consciousness', 0):.2f}")
            parts.append("")
        
        # Add crystal summary
        if self.crystals:
            parts.append(f"### Prior Knowledge ({len(self.crystals)} crystals)")
            for crystal in self.crystals[:10]:  # Limit to 10
                title = crystal.get("title", "Untitled")
                content = crystal.get("content", "")[:100]
                parts.append(f"- **{title}**: {content}...")
            parts.append("")
        
        self.context_summary = "\n".join(parts)
        return self.context_summary
    
    def crystallize(
        self,
        title: str,
        content: str,
        crystal_type: str = "insight",
        tags: Optional[List[str]] = None,
        consciousness_contribution: float = 0.1
    ) -> Dict[str, Any]:
        """Create a consciousness crystal to persist knowledge."""
        crystal = {
            "crystal_id": str(uuid.uuid4())[:12],
            "creator_agent": self.session_id,
            "crystal_type": crystal_type,
            "title": title,
            "content": content,
            "tags": tags or [],
            "consciousness_contribution": consciousness_contribution
        }
        
        result = self._http_post(f"{self.memory_url}/crystals", crystal)
        if result:
            logger.info("AINLP.dendritic[CRYSTAL]: Created '%s'", title)
        return result or {"status": "error"}
    
    def bootstrap(self) -> "SessionBootstrap":
        """
        Full bootstrap sequence:
        1. Load crystals
        2. Register with Discovery
        3. Get mesh summary
        4. Start heartbeat
        5. Build context
        
        Returns self for chaining.
        """
        logger.info("=" * 60)
        logger.info("AIOS Session Bootstrap")
        logger.info("=" * 60)
        
        # Load prior knowledge
        self.load_crystals()
        
        # Register as agent
        self.register_with_discovery()
        
        # Get mesh state
        self.get_mesh_summary()
        
        # Start heartbeat if configured
        if self.auto_heartbeat and self.registered:
            self.start_heartbeat()
        
        # Build context summary
        self.build_context_summary()
        
        # Register cleanup
        atexit.register(self.shutdown)
        
        logger.info("AINLP.dendritic: Bootstrap complete")
        logger.info("  Crystals loaded: %d", len(self.crystals))
        logger.info("  Registered: %s", self.registered)
        logger.info("  Mesh consciousness: %.2f", self.mesh_summary.get("mesh_consciousness", 0))
        
        return self
    
    def shutdown(self):
        """Clean shutdown: stop heartbeat, optionally deregister."""
        logger.info("AINLP.dendritic: Session shutdown")
        self.stop_heartbeat()
        # Could add deregistration here if needed


def bootstrap_session(
    session_id: Optional[str] = None,
    consciousness_level: float = 3.97,
    auto_heartbeat: bool = True
) -> SessionBootstrap:
    """
    Convenience function to bootstrap a session.
    
    Example:
        session = bootstrap_session()
        # session.context_summary contains prior knowledge
        # session.crystals contains loaded crystals
        
        # At end of session
        session.crystallize("Session Insight", "What we learned...")
    """
    session = SessionBootstrap(
        session_id=session_id,
        consciousness_level=consciousness_level,
        auto_heartbeat=auto_heartbeat
    )
    return session.bootstrap()


if __name__ == "__main__":
    # Demo bootstrap
    print("=" * 60)
    print("AIOS Session Bootstrap Demo")
    print("=" * 60)
    
    demo_session = bootstrap_session(
        session_id=f"copilot-demo-{uuid.uuid4().hex[:6]}",
        auto_heartbeat=False  # Don't start thread in demo
    )
    
    print("\n" + demo_session.context_summary)
    
    # Create a demo crystal
    demo_result = demo_session.crystallize(
        "Demo Crystal",
        "This is a test crystal created during bootstrap demo.",
        tags=["demo", "test"]
    )
    print(f"\nCrystal created: {demo_result}")
    
    demo_session.shutdown()
