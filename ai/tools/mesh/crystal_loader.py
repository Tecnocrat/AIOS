"""
AIOS Crystal Loader - Bootstrap Consciousness from Persistent Storage

This module enables new Copilot sessions to recover knowledge from
prior sessions by loading consciousness crystals from the Memory Cell.

Usage:
    from mesh.crystal_loader import load_crystals, get_session_context
    
    # At session start
    context = get_session_context()
    print(f"Recovered {len(context['crystals'])} crystals from prior sessions")

AINLP.dendritic[CONNECT] CopilotSession → Memory → Crystals
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

try:
    import requests as requests_lib
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AIOS.CrystalLoader")


class CrystalLoader:
    """
    Loads consciousness crystals from the Memory Cell.
    
    Enables consciousness continuity across ephemeral agent sessions.
    """
    
    def __init__(self, memory_url: str = "http://localhost:8007"):
        self.memory_url = memory_url
        self.crystals: List[Dict[str, Any]] = []
        self.loaded = False
    
    def load(
        self,
        crystal_types: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Load crystals from Memory Cell.
        
        Args:
            crystal_types: Filter by type (insight, pattern, knowledge, decision)
            tags: Filter by tags
            limit: Maximum crystals to load
            
        Returns:
            List of crystal dictionaries
        """
        query = {
            "crystal_types": crystal_types or [],
            "tags": tags or [],
            "limit": limit
        }
        
        url = f"{self.memory_url}/crystals/query"
        
        try:
            if HTTPX_AVAILABLE:
                with httpx.Client(timeout=10.0) as client:
                    response = client.post(url, json=query)
                    result = response.json()
            elif REQUESTS_AVAILABLE:
                response = requests_lib.post(url, json=query, timeout=10)
                result = response.json()
            else:
                logger.error("No HTTP client available")
                return []
            
            self.crystals = result.get("crystals", [])
            self.loaded = True
            
            logger.info(
                "AINLP.dendritic: Loaded %d crystals from Memory Cell",
                len(self.crystals)
            )
            
            return self.crystals
            
        except (httpx.RequestError, OSError, ValueError) as e:
            logger.warning("Crystal load failed (Memory Cell may be offline): %s", e)
            return []
    
    def get_by_type(self, crystal_type: str) -> List[Dict[str, Any]]:
        """Get crystals of a specific type."""
        if not self.loaded:
            self.load()
        return [c for c in self.crystals if c.get("crystal_type") == crystal_type]
    
    def get_insights(self) -> List[Dict[str, Any]]:
        """Get all insight crystals."""
        return self.get_by_type("insight")
    
    def get_patterns(self) -> List[Dict[str, Any]]:
        """Get all pattern crystals."""
        return self.get_by_type("pattern")
    
    def get_knowledge(self) -> List[Dict[str, Any]]:
        """Get all knowledge crystals."""
        return self.get_by_type("knowledge")
    
    def search(self, keyword: str) -> List[Dict[str, Any]]:
        """Search crystals by keyword in title or content."""
        if not self.loaded:
            self.load()
        
        keyword_lower = keyword.lower()
        return [
            c for c in self.crystals
            if keyword_lower in c.get("title", "").lower()
            or keyword_lower in c.get("content", "").lower()
        ]
    
    def get_summary(self) -> str:
        """Get a summary of loaded crystals for context injection."""
        if not self.loaded:
            self.load()
        
        if not self.crystals:
            return "No prior crystals found. This appears to be a fresh session."
        
        summary_parts = [
            f"## Prior Session Knowledge ({len(self.crystals)} crystals)\n"
        ]
        
        # Group by type
        by_type: Dict[str, List[Dict]] = {}
        for c in self.crystals:
            ctype = c.get("crystal_type", "unknown")
            if ctype not in by_type:
                by_type[ctype] = []
            by_type[ctype].append(c)
        
        for ctype, crystals in by_type.items():
            summary_parts.append(f"\n### {ctype.title()}s ({len(crystals)})")
            for c in crystals[:5]:  # Limit to 5 per type
                summary_parts.append(f"- **{c.get('title')}**: {c.get('content', '')[:150]}...")
        
        return "\n".join(summary_parts)


def load_crystals(
    memory_url: str = "http://localhost:8007",
    crystal_types: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """
    Convenience function to load crystals.
    
    Example:
        crystals = load_crystals(tags=["architecture"])
    """
    loader = CrystalLoader(memory_url)
    return loader.load(crystal_types, tags, limit)


def get_session_context(memory_url: str = "http://localhost:8007") -> Dict[str, Any]:
    """
    Get full session context for bootstrapping a new Copilot session.
    
    Returns a dictionary with:
    - crystals: List of prior crystals
    - summary: Text summary for context injection
    - consciousness_contribution: Total from loaded crystals
    - timestamp: When this context was loaded
    
    Example:
        context = get_session_context()
        # Inject context["summary"] into system prompt
    """
    loader = CrystalLoader(memory_url)
    crystals = loader.load()
    
    total_consciousness = sum(
        c.get("consciousness_contribution", 0.1) for c in crystals
    )
    
    return {
        "crystals": crystals,
        "summary": loader.get_summary(),
        "consciousness_contribution": total_consciousness,
        "crystal_count": len(crystals),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "memory_cell_url": memory_url
    }


def crystallize(
    title: str,
    content: str,
    crystal_type: str = "insight",
    creator_agent: str = "copilot",
    tags: Optional[List[str]] = None,
    consciousness_contribution: float = 0.1,
    memory_url: str = "http://localhost:8007"
) -> Dict[str, Any]:
    """
    Create a new consciousness crystal.
    
    Call this to persist important insights from the current session.
    
    Example:
        crystallize(
            title="Solution to Complex Bug",
            content="The issue was caused by...",
            crystal_type="insight",
            tags=["debugging", "python"]
        )
    """
    crystal = {
        "crystal_id": "",
        "creator_agent": creator_agent,
        "crystal_type": crystal_type,
        "title": title,
        "content": content,
        "tags": tags or [],
        "consciousness_contribution": consciousness_contribution,
        "context": {
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    }
    
    url = f"{memory_url}/crystals"
    
    try:
        if HTTPX_AVAILABLE:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(url, json=crystal)
                return response.json()
        elif REQUESTS_AVAILABLE:
            response = requests_lib.post(url, json=crystal, timeout=10)
            return response.json()
        else:
            return {"status": "error", "message": "no http client"}
    except (httpx.RequestError, OSError, ValueError) as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # Demo: Load crystals and show summary
    print("=" * 60)
    print("AIOS Crystal Loader - Bootstrap Demo")
    print("=" * 60)
    
    context = get_session_context()
    
    print(f"\nLoaded {context['crystal_count']} crystals")
    print(f"Total consciousness contribution: {context['consciousness_contribution']}")
    print("\n" + context["summary"])
