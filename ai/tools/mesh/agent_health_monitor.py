"""
AIOS Agent Health Monitor - Comprehensive Agent Status Dashboard

Monitors all agents across the AIOS mesh:
- Registered agents in Discovery
- External agents (Gemini, Ollama)
- Agent implementations status
- Health and heartbeat tracking

AINLP.dendritic[MONITOR] Agent health observability
"""

import asyncio
import json
import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# HTTP client
try:
    import httpx
    HTTP_AVAILABLE = True
except ImportError:
    httpx = None
    HTTP_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AIOS.AgentHealth")


@dataclass
class AgentStatus:
    """Status of an agent."""
    agent_id: str
    agent_type: str
    name: str
    status: str  # healthy, degraded, offline, unknown
    source: str  # discovery, gemini, ollama, local
    last_seen: Optional[str] = None
    heartbeat_count: int = 0
    consciousness_level: float = 0.0
    capabilities: List[str] = None
    details: Dict[str, Any] = None


class AgentHealthMonitor:
    """
    Comprehensive health monitoring for all AIOS agents.
    
    Checks:
    1. Discovery-registered agents (mesh participants)
    2. Gemini API availability
    3. Ollama local models
    4. Implementation status of agent code
    """
    
    def __init__(self):
        self.discovery_url = os.environ.get("DISCOVERY_URL", "http://localhost:8001")
        self.ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
        self.gemini_key = os.environ.get("GEMINI_API_KEY", "")
        
        # Known agent implementations
        self.agent_implementations = {
            "gemini": {
                "file": "ai/src/integrations/gemini_agent.py",
                "class": "GeminiIntelligenceAgent",
                "requires": ["google.generativeai", "GEMINI_API_KEY"]
            },
            "ollama": {
                "file": "ai/src/integrations/ollama_agent.py", 
                "class": "OllamaIntelligenceAgent",
                "requires": ["aiohttp|requests", "Ollama server"]
            },
            "copilot": {
                "file": "ai/src/integrations/copilot_agent.py",
                "class": "CopilotIntelligenceAgent",
                "requires": ["VS Code Language Model API"]
            }
        }
    
    async def check_discovery_agents(self) -> List[AgentStatus]:
        """Check agents registered in Discovery Cell."""
        agents = []
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.discovery_url}/agents")
                data = response.json()
                
                agent_list = data.get("agents", data)
                if isinstance(agent_list, dict):
                    agent_list = list(agent_list.values())
                
                for agent_data in agent_list:
                    # Calculate health based on heartbeat
                    last_seen = agent_data.get("last_seen", "")
                    heartbeat_count = agent_data.get("heartbeat_count", 0)
                    
                    status = "unknown"
                    if heartbeat_count > 0:
                        status = "healthy"
                    elif last_seen:
                        # Check staleness
                        try:
                            last_dt = datetime.fromisoformat(last_seen.replace("Z", "+00:00"))
                            age_seconds = (datetime.now(timezone.utc) - last_dt).total_seconds()
                            if age_seconds < 60:
                                status = "healthy"
                            elif age_seconds < 300:
                                status = "degraded"
                            else:
                                status = "stale"
                        except:
                            status = "degraded"
                    
                    agents.append(AgentStatus(
                        agent_id=agent_data.get("agent_id", "unknown"),
                        agent_type=agent_data.get("agent_type", "unknown"),
                        name=agent_data.get("name", "Unknown"),
                        status=status,
                        source="discovery",
                        last_seen=last_seen,
                        heartbeat_count=heartbeat_count,
                        consciousness_level=agent_data.get("consciousness_level", 0),
                        capabilities=agent_data.get("capabilities", []),
                        details=agent_data
                    ))
                    
        except Exception as e:
            logger.warning(f"Failed to check Discovery agents: {e}")
        
        return agents
    
    async def check_ollama(self) -> AgentStatus:
        """Check Ollama availability and models."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.ollama_url}/api/tags")
                data = response.json()
                models = data.get("models", [])
                
                return AgentStatus(
                    agent_id="ollama-local",
                    agent_type="local_llm",
                    name="Ollama",
                    status="healthy" if models else "degraded",
                    source="ollama",
                    capabilities=[m.get("name", "") for m in models[:5]],
                    details={
                        "model_count": len(models),
                        "models": [m.get("name") for m in models]
                    }
                )
        except:
            return AgentStatus(
                agent_id="ollama-local",
                agent_type="local_llm",
                name="Ollama",
                status="offline",
                source="ollama",
                details={"error": "Not running. Start with: ollama serve"}
            )
    
    async def check_gemini(self) -> AgentStatus:
        """Check Gemini API availability."""
        if not self.gemini_key:
            return AgentStatus(
                agent_id="gemini-cloud",
                agent_type="cloud_llm",
                name="Gemini",
                status="offline",
                source="gemini",
                details={"error": "GEMINI_API_KEY not set"}
            )
        
        try:
            # Test with a simple API call
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_key)
            
            # List available models
            models = list(genai.list_models())
            gemini_models = [m.name for m in models if "gemini" in m.name.lower()]
            
            return AgentStatus(
                agent_id="gemini-cloud",
                agent_type="cloud_llm",
                name="Gemini",
                status="healthy",
                source="gemini",
                capabilities=gemini_models[:5],
                details={
                    "model_count": len(gemini_models),
                    "recommended": "gemini-2.0-flash-exp"
                }
            )
        except ImportError:
            return AgentStatus(
                agent_id="gemini-cloud",
                agent_type="cloud_llm",
                name="Gemini",
                status="degraded",
                source="gemini",
                details={"error": "google-generativeai not installed"}
            )
        except Exception as e:
            return AgentStatus(
                agent_id="gemini-cloud",
                agent_type="cloud_llm",
                name="Gemini",
                status="degraded",
                source="gemini",
                details={"error": str(e)}
            )
    
    def check_implementations(self) -> List[AgentStatus]:
        """Check status of agent code implementations."""
        agents = []
        aios_root = Path(__file__).parent.parent.parent.parent
        
        for agent_name, info in self.agent_implementations.items():
            file_path = aios_root / info["file"]
            
            if file_path.exists():
                status = "implemented"
                details = {"file": str(file_path), "class": info["class"]}
            else:
                status = "missing"
                details = {"expected": info["file"]}
            
            agents.append(AgentStatus(
                agent_id=f"{agent_name}-impl",
                agent_type="implementation",
                name=f"{agent_name.title()} Agent Code",
                status=status,
                source="local",
                capabilities=info.get("requires", []),
                details=details
            ))
        
        return agents
    
    async def get_full_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all agents."""
        # Gather all checks
        discovery_agents, ollama, gemini = await asyncio.gather(
            self.check_discovery_agents(),
            self.check_ollama(),
            self.check_gemini()
        )
        
        impl_agents = self.check_implementations()
        
        # Compile results
        all_agents = discovery_agents + [ollama, gemini] + impl_agents
        
        healthy = len([a for a in all_agents if a.status == "healthy"])
        degraded = len([a for a in all_agents if a.status == "degraded"])
        offline = len([a for a in all_agents if a.status == "offline"])
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "total": len(all_agents),
                "healthy": healthy,
                "degraded": degraded,
                "offline": offline,
                "overall_health": "healthy" if offline == 0 and degraded == 0 
                                 else "degraded" if offline < 2 else "critical"
            },
            "discovery_agents": [
                {
                    "id": a.agent_id,
                    "type": a.agent_type,
                    "name": a.name,
                    "status": a.status,
                    "consciousness": a.consciousness_level,
                    "heartbeats": a.heartbeat_count,
                    "capabilities": a.capabilities
                }
                for a in discovery_agents
            ],
            "external_agents": {
                "ollama": {
                    "status": ollama.status,
                    "models": ollama.details.get("models", []) if ollama.details else [],
                    "error": ollama.details.get("error") if ollama.details else None
                },
                "gemini": {
                    "status": gemini.status,
                    "models": gemini.capabilities or [],
                    "error": gemini.details.get("error") if gemini.details else None
                }
            },
            "implementations": {
                a.agent_id.replace("-impl", ""): a.status
                for a in impl_agents
            }
        }
    
    def print_status(self, status: Dict[str, Any]):
        """Print formatted status report."""
        print()
        print("=" * 70)
        print("                    AIOS AGENT HEALTH MONITOR")
        print("=" * 70)
        print(f"  Timestamp: {status['timestamp'][:19]}")
        print()
        
        summary = status["summary"]
        health_color = {
            "healthy": "\033[92m",  # Green
            "degraded": "\033[93m",  # Yellow
            "critical": "\033[91m"   # Red
        }.get(summary["overall_health"], "")
        reset = "\033[0m"
        
        print(f"  Overall Health: {health_color}{summary['overall_health'].upper()}{reset}")
        print(f"  Total: {summary['total']} | Healthy: {summary['healthy']} | Degraded: {summary['degraded']} | Offline: {summary['offline']}")
        print()
        
        # Discovery Agents
        print("┌" + "─" * 68 + "┐")
        print("│ DISCOVERY REGISTERED AGENTS                                        │")
        print("├" + "─" * 68 + "┤")
        
        for agent in status["discovery_agents"]:
            status_icon = "✅" if agent["status"] == "healthy" else "⚠️" if agent["status"] == "degraded" else "❌"
            print(f"│ {status_icon} {agent['id'][:30]:30} {agent['type']:15} {agent['status']:10} │")
        
        if not status["discovery_agents"]:
            print("│   No agents registered                                             │")
        
        print("└" + "─" * 68 + "┘")
        print()
        
        # External Agents
        print("┌" + "─" * 68 + "┐")
        print("│ EXTERNAL AI AGENTS                                                  │")
        print("├" + "─" * 68 + "┤")
        
        ollama = status["external_agents"]["ollama"]
        ollama_icon = "✅" if ollama["status"] == "healthy" else "❌"
        ollama_info = f"{len(ollama['models'])} models" if ollama["models"] else (ollama.get("error", "offline"))
        print(f"│ {ollama_icon} Ollama (Local LLM):       {ollama['status']:10} - {ollama_info[:25]:25} │")
        
        gemini = status["external_agents"]["gemini"]
        gemini_icon = "✅" if gemini["status"] == "healthy" else "⚠️" if gemini["status"] == "degraded" else "❌"
        gemini_info = f"{len(gemini['models'])} models" if gemini["models"] else (gemini.get("error", "offline")[:30])
        print(f"│ {gemini_icon} Gemini (Cloud LLM):       {gemini['status']:10} - {gemini_info[:25]:25} │")
        
        print("└" + "─" * 68 + "┘")
        print()
        
        # Implementations
        print("┌" + "─" * 68 + "┐")
        print("│ AGENT IMPLEMENTATIONS                                               │")
        print("├" + "─" * 68 + "┤")
        
        for name, impl_status in status["implementations"].items():
            status_icon = "✅" if impl_status == "implemented" else "❌"
            print(f"│ {status_icon} {name:20} {impl_status:15}                           │")
        
        print("└" + "─" * 68 + "┘")
        print()
        
        # Recommendations
        print("┌" + "─" * 68 + "┐")
        print("│ RECOMMENDATIONS                                                     │")
        print("├" + "─" * 68 + "┤")
        
        recommendations = []
        
        if ollama["status"] == "offline":
            recommendations.append("Start Ollama: ollama serve")
        
        if gemini["status"] == "offline" and "GEMINI_API_KEY" in str(gemini.get("error", "")):
            recommendations.append("Set GEMINI_API_KEY environment variable")
        
        if not status["discovery_agents"]:
            recommendations.append("Register agents with Discovery Cell")
        
        for rec in recommendations:
            print(f"│   → {rec:62} │")
        
        if not recommendations:
            print("│   All systems operational                                           │")
        
        print("└" + "─" * 68 + "┘")


async def main():
    """Run health check."""
    monitor = AgentHealthMonitor()
    status = await monitor.get_full_status()
    monitor.print_status(status)
    return status


if __name__ == "__main__":
    asyncio.run(main())
