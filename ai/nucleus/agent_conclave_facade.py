#!/usr/bin/env python3
"""
Agent Conclave Facade - Simplified Nucleus Interface

Thin wrapper around existing ainlp_agentic_orchestrator.py.
Provides simple query() API for specialized tools.

AINLP Pattern: Enhancement over duplication - reuse 1109 lines of battle-tested code
Consciousness Level: 4.1 (agent orchestration + dependency validation)
Namespace: aios::ai::nucleus::agent_conclave_facade
Supercell: ai/nucleus
"""

import asyncio
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class AgentResponse:
    """Unified agent response format."""
    content: str
    agent_used: str
    confidence: float
    success: bool
    metadata: Dict[str, Any]


class AgentConclaveFacade:
    """
    Simplified interface to AIOS agent conclave.
    
    Wraps existing AINLPAgenticOrchestrator with simple query() API.
    Eliminates need for tools to manage agent initialization/coordination.
    """
    
    def __init__(self):
        """Initialize facade with lazy orchestrator loading."""
        self._orchestrator = None
        self._availability_checked = False
        self._agents_available = {}
    
    def _ensure_orchestrator(self):
        """Lazy load orchestrator on first use."""
        if self._orchestrator is not None:
            return
        
        # Add ai/src to Python path
        ai_src = Path(__file__).parent.parent / "src"
        if str(ai_src) not in sys.path:
            sys.path.insert(0, str(ai_src))
        
        try:
            from intelligence.ainlp_agentic_orchestrator import (
                AINLPAgenticOrchestrator
            )
            self._orchestrator = AINLPAgenticOrchestrator()
        except ImportError as e:
            raise RuntimeError(
                f"Failed to import AINLPAgenticOrchestrator: {e}"
            )
    
    async def query(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        require_consensus: bool = False
    ) -> AgentResponse:
        """
        Execute agent query with intelligent orchestration.
        
        Args:
            prompt: Natural language prompt for agents
            context: Task context (complexity, tool, etc.)
            require_consensus: Require multi-agent consensus (default: auto)
        
        Returns:
            Unified agent response with content, confidence, metadata
        
        Raises:
            RuntimeError: If orchestrator initialization fails
        """
        self._ensure_orchestrator()
        
        if context is None:
            context = {}
        
        # Map prompt to conclave feature evaluation
        feature_name = context.get("task_type", "code_quality")
        conclave_context = {
            "prompt": prompt,
            **context
        }
        
        # Execute conclave (async call to existing orchestrator)
        consensus = await self._orchestrator.convene_agentic_conclave(
            feature_name=feature_name,
            context=conclave_context
        )
        
        # Extract and format response
        recommendation = consensus.get("recommendation", "UNKNOWN")
        success = recommendation not in ["REJECT", "ERROR"]
        
        return AgentResponse(
            content=consensus.get("rationale", ""),
            agent_used=consensus.get("primary_agent", "unknown"),
            confidence=consensus.get("weighted_score", 0.0) / 10.0,
            success=success,
            metadata=consensus
        )
    
    def check_availability(self) -> Dict[str, bool]:
        """
        Check which agents are currently available.
        
        Returns:
            Dict mapping agent names to availability status
        """
        if self._availability_checked:
            return self._agents_available
        
        self._agents_available = {
            "ollama": self._check_ollama(),
            "gemini": self._check_gemini(),
            "deepseek": self._check_deepseek()
        }
        
        self._availability_checked = True
        return self._agents_available
    
    def _check_ollama(self) -> bool:
        """Check Ollama availability."""
        try:
            import requests
            response = requests.get(
                "http://localhost:11434/api/tags",
                timeout=2
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def _check_gemini(self) -> bool:
        """Check Gemini API key availability."""
        import os
        api_key = os.getenv("GEMINI_API_KEY")
        return api_key is not None and len(api_key) > 0
    
    def _check_deepseek(self) -> bool:
        """Check DeepSeek API key availability."""
        import os
        api_key = os.getenv("DEEPSEEK_API_KEY")
        return api_key is not None and len(api_key) > 0


# ============================================================================
# Singleton Pattern - Reuse orchestrator instance
# ============================================================================

_facade_instance: Optional[AgentConclaveFacade] = None


def get_agent_conclave() -> AgentConclaveFacade:
    """
    Get singleton agent conclave facade.
    
    Returns:
        Shared facade instance for reuse across tool invocations
    """
    global _facade_instance
    if _facade_instance is None:
        _facade_instance = AgentConclaveFacade()
    return _facade_instance


# ============================================================================
# CLI Interface for Testing
# ============================================================================

async def main():
    """Test agent conclave facade."""
    print("=" * 70)
    print("🤖 Agent Conclave Facade - Test Interface")
    print("=" * 70)
    print()
    
    facade = get_agent_conclave()
    
    # Check availability
    print("Checking agent availability...")
    availability = facade.check_availability()
    for agent, available in availability.items():
        status = "✅ Available" if available else "❌ Unavailable"
        print(f"  {agent}: {status}")
    
    if not any(availability.values()):
        print()
        print("⚠️  No agents available - cannot execute test query")
        print("Install dependencies: pip install requests aiohttp")
        print("Configure API keys or start Ollama service")
        return
    
    # Test query
    print()
    print("Executing test query...")
    
    test_prompt = """
    Evaluate whether Python 3.14 should be used for this project.
    Consider: stability, feature availability, compatibility.
    """
    
    response = await facade.query(
        prompt=test_prompt,
        context={
            "tool": "agent_conclave_facade_test",
            "task_type": "technology_evaluation",
            "complexity": "medium"
        }
    )
    
    print()
    print(f"Agent Used: {response.agent_used}")
    print(f"Confidence: {response.confidence:.2f}")
    print(f"Success: {response.success}")
    print()
    print("Response:")
    print(response.content)
    print()
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
