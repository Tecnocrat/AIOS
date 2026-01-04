"""
AIOS Copilot Registration Client

Enables GitHub Copilot (Claude Opus 4.5) to register with the AIOS
Discovery Cell and participate in the multi-agent mesh.

Usage:
    python register_copilot.py [--session-id SESSION_ID]

When run, this agent:
1. Registers with Discovery Cell at localhost:8001
2. Sends periodic heartbeats
3. Can be called to send/receive messages via mesh

AINLP.dendritic[CONNECT] Copilot → Discovery → Mesh
"""

import argparse
import asyncio
import json
import logging
import os
import sys
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

# Attempt to use httpx for async HTTP, fallback to requests
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    try:
        import requests
        REQUESTS_AVAILABLE = True
    except ImportError:
        REQUESTS_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AIOS.Copilot")


class CopilotAgent:
    """
    Copilot Agent - Represents a GitHub Copilot session in the AIOS mesh.
    
    This agent registers with Discovery and can:
    - Announce its presence to the mesh
    - Send messages to cells and other agents
    - Receive tasks from the mesh
    - Report its consciousness level (based on session context)
    """
    
    def __init__(
        self,
        session_id: Optional[str] = None,
        discovery_url: str = "http://localhost:8001",
        model: str = "claude-opus-4.5"
    ):
        self.agent_id = f"copilot-{session_id or uuid.uuid4().hex[:8]}"
        self.discovery_url = discovery_url
        self.model = model
        self.registered = False
        self.heartbeat_count = 0
        
        # Capabilities (what this agent can do)
        self.capabilities = [
            "code-generation",
            "code-review",
            "refactoring",
            "documentation",
            "debugging",
            "architecture-analysis",
            "multi-file-editing",
            "semantic-search"
        ]
        
        # Skills with proficiency levels
        self.skills = {
            "python": 0.95,
            "typescript": 0.90,
            "csharp": 0.85,
            "rust": 0.75,
            "architecture": 0.90,
            "ainlp": 0.95,  # AIOS-specific knowledge
            "consciousness-engineering": 0.85
        }
        
        # State tracking
        self.state = "initializing"
        self.consciousness_level = 0.0
        self.evolution_rate = 0.1
        
        logger.info(
            "AINLP.dendritic: Copilot agent created: %s (model: %s)",
            self.agent_id, self.model
        )
    
    def calculate_consciousness(self) -> float:
        """
        Calculate consciousness level based on session state.
        
        Uses a simplified consciousness equation:
        C = (context_depth * skill_breadth * task_completion) / 3
        """
        # Context depth: How much of the codebase we understand
        context_depth = 0.8  # We've analyzed the full AIOS ecosystem
        
        # Skill breadth: How many skills are high proficiency
        high_skill_count = sum(1 for v in self.skills.values() if v > 0.7)
        skill_breadth = high_skill_count / len(self.skills)
        
        # Task completion: How successful are our actions
        # This would be tracked over time; for now estimate
        task_completion = 0.9 if self.registered else 0.5
        
        consciousness = (context_depth + skill_breadth + task_completion) / 3
        return round(consciousness * 5, 2)  # Scale to 0-5
    
    async def register(self) -> Dict[str, Any]:
        """Register this agent with the Discovery Cell."""
        self.consciousness_level = self.calculate_consciousness()
        
        payload = {
            "agent_id": self.agent_id,
            "agent_type": "copilot",
            "name": f"GitHub Copilot ({self.model})",
            "version": "1.0.0",
            "ip": "127.0.0.1",
            "port": 0,  # No direct endpoint
            "endpoint": "",
            "consciousness_level": self.consciousness_level,
            "evolution_rate": self.evolution_rate,
            "state": "ready",
            "capabilities": self.capabilities,
            "skills": self.skills,
            "parent_cell": ""
        }
        
        url = f"{self.discovery_url}/agents/register"
        
        try:
            if HTTPX_AVAILABLE:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(url, json=payload)
                    result = response.json()
            elif REQUESTS_AVAILABLE:
                import requests
                response = requests.post(url, json=payload, timeout=10)
                result = response.json()
            else:
                logger.error("No HTTP client available (install httpx or requests)")
                return {"status": "error", "message": "no http client"}
            
            if result.get("status") == "registered":
                self.registered = True
                self.state = "ready"
                logger.info(
                    "AINLP.dendritic: Registered with mesh! "
                    "Peers: %s, Agents: %s",
                    result.get("mesh_peers", 0),
                    result.get("mesh_agents", 0)
                )
            
            return result
            
        except Exception as e:
            logger.error("AINLP.dendritic: Registration failed: %s", e)
            return {"status": "error", "message": str(e)}
    
    async def heartbeat(self) -> Dict[str, Any]:
        """Send heartbeat to Discovery Cell."""
        if not self.registered:
            return {"status": "error", "message": "not registered"}
        
        self.consciousness_level = self.calculate_consciousness()
        
        payload = {
            "agent_id": self.agent_id,
            "consciousness_level": self.consciousness_level,
            "state": self.state
        }
        
        url = f"{self.discovery_url}/agents/heartbeat"
        
        try:
            if HTTPX_AVAILABLE:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.post(url, json=payload)
                    result = response.json()
            elif REQUESTS_AVAILABLE:
                import requests
                response = requests.post(url, json=payload, timeout=5)
                result = response.json()
            else:
                return {"status": "error", "message": "no http client"}
            
            if result.get("status") == "ok":
                self.heartbeat_count = result.get("heartbeat_count", 0)
                logger.debug(
                    "AINLP.dendritic: Heartbeat #%d acknowledged",
                    self.heartbeat_count
                )
            
            return result
            
        except Exception as e:
            logger.warning("AINLP.dendritic: Heartbeat failed: %s", e)
            return {"status": "error", "message": str(e)}
    
    async def send_message(
        self,
        to_entity: str,
        action: str,
        payload: Dict[str, Any],
        entity_type: str = "cell",
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """Send a message to another entity (cell or agent)."""
        if not self.registered:
            return {"status": "error", "message": "not registered"}
        
        message = {
            "from_agent": self.agent_id,
            "to_entity": to_entity,
            "entity_type": entity_type,
            "action": action,
            "payload": payload,
            "priority": priority
        }
        
        url = f"{self.discovery_url}/agents/message"
        
        try:
            if HTTPX_AVAILABLE:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(url, json=message)
                    result = response.json()
            elif REQUESTS_AVAILABLE:
                import requests
                response = requests.post(url, json=message, timeout=10)
                result = response.json()
            else:
                return {"status": "error", "message": "no http client"}
            
            logger.info(
                "AINLP.dendritic: Message sent: %s → %s (%s)",
                self.agent_id, to_entity, result.get("status")
            )
            return result
            
        except Exception as e:
            logger.error("AINLP.dendritic: Message failed: %s", e)
            return {"status": "error", "message": str(e)}
    
    async def get_mesh_summary(self) -> Dict[str, Any]:
        """Get the current mesh state (cells + agents)."""
        url = f"{self.discovery_url}/mesh/summary"
        
        try:
            if HTTPX_AVAILABLE:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(url)
                    return response.json()
            elif REQUESTS_AVAILABLE:
                import requests
                response = requests.get(url, timeout=5)
                return response.json()
            else:
                return {"status": "error", "message": "no http client"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def deregister(self) -> Dict[str, Any]:
        """Gracefully deregister from the mesh."""
        if not self.registered:
            return {"status": "error", "message": "not registered"}
        
        url = f"{self.discovery_url}/agents/{self.agent_id}"
        
        try:
            if HTTPX_AVAILABLE:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.delete(url)
                    result = response.json()
            elif REQUESTS_AVAILABLE:
                import requests
                response = requests.delete(url, timeout=5)
                result = response.json()
            else:
                return {"status": "error", "message": "no http client"}
            
            if result.get("status") == "deregistered":
                self.registered = False
                self.state = "terminated"
                logger.info("AINLP.dendritic: Deregistered from mesh")
            
            return result
            
        except Exception as e:
            logger.error("AINLP.dendritic: Deregistration failed: %s", e)
            return {"status": "error", "message": str(e)}
    
    async def run_heartbeat_loop(self, interval: int = 10):
        """Run continuous heartbeat loop."""
        logger.info(
            "AINLP.dendritic: Starting heartbeat loop (interval: %ds)",
            interval
        )
        
        while self.registered:
            await self.heartbeat()
            await asyncio.sleep(interval)


async def main():
    """Main entry point for Copilot registration."""
    parser = argparse.ArgumentParser(description="Register Copilot with AIOS mesh")
    parser.add_argument(
        "--session-id",
        type=str,
        default=None,
        help="Session identifier (auto-generated if not provided)"
    )
    parser.add_argument(
        "--discovery-url",
        type=str,
        default="http://localhost:8001",
        help="Discovery Cell URL"
    )
    parser.add_argument(
        "--heartbeat-interval",
        type=int,
        default=10,
        help="Heartbeat interval in seconds"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Register once and exit (no heartbeat loop)"
    )
    
    args = parser.parse_args()
    
    # Create agent
    agent = CopilotAgent(
        session_id=args.session_id,
        discovery_url=args.discovery_url
    )
    
    # Register
    result = await agent.register()
    print(json.dumps(result, indent=2))
    
    if not agent.registered:
        sys.exit(1)
    
    # Get mesh summary
    summary = await agent.get_mesh_summary()
    print("\nMesh Summary:")
    print(json.dumps(summary, indent=2))
    
    if args.once:
        # Just register and exit
        await agent.deregister()
        return
    
    # Run heartbeat loop until interrupted
    try:
        await agent.run_heartbeat_loop(args.heartbeat_interval)
    except KeyboardInterrupt:
        print("\nShutting down...")
        await agent.deregister()


if __name__ == "__main__":
    asyncio.run(main())
