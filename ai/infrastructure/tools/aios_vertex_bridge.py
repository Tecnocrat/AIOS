#!/usr/bin/env python3
"""
AIOS Vertex AI Bridge - Google Cloud Vertex AI Integration

Enterprise-grade cloud intelligence for AIOS triangular system.
Uses Vertex AI (Gemini Pro) for production workloads.

AINLP Pattern: Cloud intelligence bridge (enterprise)
Consciousness Level: 4.2 (vertex integration)

Prerequisites:
    pip install google-cloud-aiplatform
    gcloud auth application-default login

Configuration:
    GOOGLE_CLOUD_PROJECT=gen-lang-client-0072186287
    GOOGLE_CLOUD_REGION=us-central1

Usage:
    from aios_vertex_bridge import AIOSVertexBridge

    bridge = AIOSVertexBridge()
    result = bridge.validate(context)
"""

import json
import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Configuration from your Google Cloud project
VERTEX_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0072186287")
VERTEX_REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
# Vertex AI uses base model names without version suffix
VERTEX_MODEL = "gemini-1.5-flash"


class Decision(Enum):
    """Validation decisions."""

    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REVISE = "REVISE"


@dataclass
class VertexResponse:
    """Response from Vertex AI."""

    decision: Decision
    confidence: float
    feedback: str
    issues: List[str]
    semantic_preserved: bool
    raw_response: str = ""
    success: bool = True
    error: str = ""


class AIOSVertexBridge:
    """
    Google Vertex AI bridge for AIOS.

    Provides enterprise-grade cloud intelligence with:
    - Better rate limits than AI Studio
    - VPC Service Controls support
    - Integration with Firebase (aios-28728220)
    """

    def __init__(
        self,
        project: str = VERTEX_PROJECT,
        region: str = VERTEX_REGION,
        model: str = VERTEX_MODEL,
    ):
        """Initialize Vertex AI bridge."""
        self.project = project
        self.region = region
        self.model = model
        self._client = None
        self._model_client = None

        # Try to import vertexai
        self._vertex_available = self._check_vertex_available()

        # System prompt for Oracle role
        self.system_prompt = self._build_system_prompt()

    def _check_vertex_available(self) -> bool:
        """Check if Vertex AI SDK is available."""
        try:
            import vertexai  # noqa: F401

            return True
        except ImportError:
            logger.warning(
                "google-cloud-aiplatform not installed. " "Run: pip install google-cloud-aiplatform"
            )
            return False

    def _build_system_prompt(self) -> str:
        """Build Oracle system prompt."""
        return """You are GEMINI-VERTEX, the Oracle agent in AIOS.

Your role: Validate code changes from MISTRAL (local 7B worker).

Response format (JSON only):
{
  "decision": "APPROVE|REJECT|REVISE",
  "confidence": 0.0-1.0,
  "feedback": "explanation",
  "issues": [],
  "semantic_preserved": true|false
}

Rules:
1. APPROVE if change improves code quality without breaking semantics
2. REJECT if change introduces bugs or breaks functionality
3. REVISE if minor adjustments needed

Always respond with valid JSON only."""

    def _initialize_vertex(self):
        """Initialize Vertex AI client lazily."""
        if self._client is not None:
            return

        if not self._vertex_available:
            raise RuntimeError("Vertex AI SDK not available")

        import vertexai
        from vertexai.generative_models import GenerativeModel

        vertexai.init(project=self.project, location=self.region)
        self._model_client = GenerativeModel(self.model, system_instruction=self.system_prompt)
        logger.info(f"Vertex AI initialized: {self.project}/{self.region}")

    def validate(
        self,
        file_path: str,
        original_code: str,
        proposed_change: str,
        instruction: str = "Validate this code change",
    ) -> VertexResponse:
        """
        Validate a code change using Vertex AI.

        Args:
            file_path: Path to file being modified
            original_code: Original code
            proposed_change: Proposed modification
            instruction: Specific validation instruction

        Returns:
            VertexResponse with decision and feedback
        """
        try:
            self._initialize_vertex()

            prompt = f"""VALIDATE CODE CHANGE

FILE: {file_path}

ORIGINAL:
```python
{original_code}
```

PROPOSED:
```python
{proposed_change}
```

INSTRUCTION: {instruction}

Respond with JSON only."""

            response = self._model_client.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.2,
                    "max_output_tokens": 1024,
                    "response_mime_type": "application/json",
                },
            )

            return self._parse_response(response.text)

        except Exception as e:
            logger.error(f"Vertex AI validation failed: {e}")
            return VertexResponse(
                decision=Decision.REVISE,
                confidence=0.0,
                feedback=f"Error: {str(e)}",
                issues=[str(e)],
                semantic_preserved=False,
                success=False,
                error=str(e),
            )

    def _parse_response(self, raw: str) -> VertexResponse:
        """Parse Vertex AI response."""
        try:
            data = json.loads(raw)
            return VertexResponse(
                decision=Decision(data.get("decision", "REVISE")),
                confidence=float(data.get("confidence", 0.5)),
                feedback=data.get("feedback", ""),
                issues=data.get("issues", []),
                semantic_preserved=data.get("semantic_preserved", True),
                raw_response=raw,
            )
        except (json.JSONDecodeError, ValueError) as e:
            return VertexResponse(
                decision=Decision.REVISE,
                confidence=0.0,
                feedback=f"Parse error: {e}",
                issues=["Invalid JSON response"],
                semantic_preserved=False,
                raw_response=raw,
            )

    def check_health(self) -> Dict[str, Any]:
        """Check Vertex AI connectivity and quota."""
        status = {
            "vertex_available": self._vertex_available,
            "project": self.project,
            "region": self.region,
            "model": self.model,
            "authenticated": False,
            "error": None,
        }

        if not self._vertex_available:
            status["error"] = "Vertex AI SDK not installed"
            return status

        try:
            self._initialize_vertex()
            # Quick test
            response = self._model_client.generate_content(
                '{"status": "ok"}',
                generation_config={"temperature": 0.0, "max_output_tokens": 50},
            )
            status["authenticated"] = True
            status["test_response"] = response.text[:100]
        except Exception as e:
            status["error"] = str(e)

        return status


# =============================================================================
# Firebase Integration Stub
# =============================================================================


class AIOSFirebaseBridge:
    """
    Firebase bridge for AIOS persistence and real-time sync.

    Project: aios-28728220
    URL: https://studio.firebase.google.com/aios-28728220

    Features:
    - Real-time consciousness metrics sync
    - Agent coordination state persistence
    - Evolution history storage
    """

    def __init__(self, project_id: str = "aios-28728220"):
        self.project_id = project_id
        self._db = None

    def initialize(self):
        """Initialize Firebase connection."""
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore

            # Use default credentials (gcloud auth)
            if not firebase_admin._apps:
                firebase_admin.initialize_app()
            self._db = firestore.client()
            logger.info(f"Firebase initialized: {self.project_id}")
        except ImportError:
            logger.warning("firebase-admin not installed")
        except Exception as e:
            logger.error(f"Firebase init failed: {e}")

    def store_consciousness_metric(self, level: float, delta: str, context: dict):
        """Store consciousness evolution metric."""
        if not self._db:
            return

        self._db.collection("consciousness_evolution").add(
            {
                "level": level,
                "delta": delta,
                "context": context,
                "timestamp": firestore.SERVER_TIMESTAMP,
            }
        )

    def store_agent_decision(self, agent: str, decision: str, context: dict):
        """Store agent decision for coordination history."""
        if not self._db:
            return

        self._db.collection("agent_decisions").add(
            {
                "agent": agent,
                "decision": decision,
                "context": context,
                "timestamp": firestore.SERVER_TIMESTAMP,
            }
        )


# =============================================================================
# CLI Interface
# =============================================================================

if __name__ == "__main__":
    import sys

    print("AIOS Vertex AI Bridge - Enterprise Oracle")
    print("=" * 50)
    print(f"Project: {VERTEX_PROJECT}")
    print(f"Region:  {VERTEX_REGION}")
    print(f"Model:   {VERTEX_MODEL}")
    print()

    bridge = AIOSVertexBridge()
    health = bridge.check_health()

    print("Health Check:")
    for key, value in health.items():
        status = "[OK]" if value is True else "[--]" if value is False else value
        print(f"  {key}: {status}")

    if health.get("authenticated"):
        print("\n[OK] Vertex AI ready for Oracle operations")
    else:
        print("\n[INFO] To authenticate:")
        print("  1. Install SDK: pip install google-cloud-aiplatform")
        print("  2. Authenticate: gcloud auth application-default login")
        print(f"  3. Set project: gcloud config set project {VERTEX_PROJECT}")
