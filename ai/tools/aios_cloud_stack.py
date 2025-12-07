#!/usr/bin/env python3
"""
AIOS Google Cloud Sync Stack
============================
Clean integration layer for Google Cloud services.

Architecture:
    ┌─────────────────────────────────────────────────────────────┐
    │                    AIOS Cloud Stack                         │
    ├─────────────────────────────────────────────────────────────┤
    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
    │  │ AI Studio   │  │  Firebase   │  │  Vertex AI          │  │
    │  │ (Primary)   │  │  (Storage)  │  │  (Enterprise)       │  │
    │  │             │  │             │  │                     │  │
    │  │ GEMINI_KEY  │  │ aios-28728  │  │  [DISABLED]         │  │
    │  │ Free tier   │  │ Firestore   │  │  Needs billing      │  │
    │  └─────────────┘  └─────────────┘  └─────────────────────┘  │
    └─────────────────────────────────────────────────────────────┘

Config: config/google_cloud.json
"""

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("AIOS.CloudStack")


class ServiceStatus(Enum):
    """Cloud service connection status."""

    CONNECTED = "connected"
    AVAILABLE = "available"
    DISABLED = "disabled"
    ERROR = "error"
    NOT_CONFIGURED = "not_configured"


@dataclass
class CloudConfig:
    """Google Cloud configuration loaded from config/google_cloud.json."""

    firebase_project: str = "gen-lang-client-0072186287"
    firebase_database: str = "aios-db"
    firebase_region: str = "us-central1"
    ai_studio_model: str = "gemini-2.0-flash"
    ai_studio_key_env: str = "GEMINI_API_KEY"
    vertex_enabled: bool = False
    vertex_project: Optional[str] = None
    vertex_region: str = "us-central1"

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "CloudConfig":
        """Load configuration from JSON file."""
        if config_path is None:
            # Find config relative to this file
            config_path = Path(__file__).parent.parent.parent / "config" / "google_cloud.json"

        if not config_path.exists():
            logger.warning(f"Config not found: {config_path}, using defaults")
            return cls()

        try:
            data = json.loads(config_path.read_text())
            fb = data.get("firebase", {})
            ai = data.get("ai_studio", {})
            vx = data.get("vertex_ai", {})
            return cls(
                firebase_project=fb.get("project_id", "gen-lang-client-0072186287"),
                firebase_database=fb.get("database_id", "aios-db"),
                firebase_region=fb.get("region", "us-central1"),
                ai_studio_model=ai.get("model", "gemini-2.0-flash"),
                ai_studio_key_env=ai.get("api_key_env", "GEMINI_API_KEY"),
                vertex_enabled=vx.get("enabled", False),
                vertex_project=vx.get("project_id"),
                vertex_region=vx.get("region", "us-central1"),
            )
        except Exception as e:
            logger.error(f"Config load error: {e}")
            return cls()


@dataclass
class ServiceHealth:
    """Health status of a cloud service."""

    name: str
    status: ServiceStatus
    message: str
    details: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AIOSCloudStack:
    """
    Unified Google Cloud integration for AIOS.

    This is the single entry point for all cloud operations.
    """

    def __init__(self, config: Optional[CloudConfig] = None):
        self.config = config or CloudConfig.load()
        self._ai_studio = None
        self._firebase = None
        self._vertex = None

    # =========================================================================
    # AI Studio (Primary Intelligence)
    # =========================================================================

    def check_ai_studio(self) -> ServiceHealth:
        """Check Google AI Studio connection."""
        api_key = os.getenv(self.config.ai_studio_key_env)

        if not api_key:
            return ServiceHealth(
                name="AI Studio",
                status=ServiceStatus.NOT_CONFIGURED,
                message=f"Set {self.config.ai_studio_key_env} environment variable",
                details={
                    "key_env": self.config.ai_studio_key_env,
                    "get_key_url": "https://aistudio.google.com/app/apikey",
                },
            )

        try:
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(self.config.ai_studio_model)

            # Quick test
            response = model.generate_content(
                "Respond with only: OK",
                generation_config={"max_output_tokens": 10},
            )

            return ServiceHealth(
                name="AI Studio",
                status=ServiceStatus.CONNECTED,
                message=f"Connected to {self.config.ai_studio_model}",
                details={
                    "model": self.config.ai_studio_model,
                    "response": response.text.strip()[:50],
                },
            )

        except ImportError:
            return ServiceHealth(
                name="AI Studio",
                status=ServiceStatus.ERROR,
                message="SDK not installed: pip install google-generativeai",
            )
        except Exception as e:
            return ServiceHealth(
                name="AI Studio",
                status=ServiceStatus.ERROR,
                message=str(e),
            )

    def get_ai_studio_client(self):
        """Get configured AI Studio client."""
        if self._ai_studio is None:
            import google.generativeai as genai

            api_key = os.getenv(self.config.ai_studio_key_env)
            if not api_key:
                raise ValueError(f"{self.config.ai_studio_key_env} not set")

            genai.configure(api_key=api_key)
            self._ai_studio = genai.GenerativeModel(self.config.ai_studio_model)

        return self._ai_studio

    # =========================================================================
    # Firebase (Persistence)
    # =========================================================================

    def check_firebase(self) -> ServiceHealth:
        """Check Firebase/Firestore connection."""
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore

            # Initialize if not already done
            if not firebase_admin._apps:
                # Try to use gcloud credentials
                try:
                    import google.auth

                    creds, project = google.auth.default()
                    firebase_admin.initialize_app(
                        credential=credentials.ApplicationDefault(),
                        options={"projectId": self.config.firebase_project},
                    )
                except Exception:
                    # Fall back to no credentials (will fail on operations)
                    firebase_admin.initialize_app(
                        options={"projectId": self.config.firebase_project}
                    )

            # Use named database 'aios-db'
            db = firestore.client(database_id=self.config.firebase_database)

            # Test connection
            test_ref = db.collection("_health_check").document("test")
            test_ref.set({"timestamp": datetime.now(timezone.utc).isoformat(), "status": "ok"})

            return ServiceHealth(
                name="Firebase",
                status=ServiceStatus.CONNECTED,
                message=f"Connected to {self.config.firebase_project}",
                details={
                    "project": self.config.firebase_project,
                    "console": f"https://console.firebase.google.com/project/{self.config.firebase_project}",
                },
            )

        except ImportError:
            return ServiceHealth(
                name="Firebase",
                status=ServiceStatus.ERROR,
                message="SDK not installed: pip install firebase-admin",
            )
        except Exception as e:
            error_msg = str(e)
            if "PERMISSION_DENIED" in error_msg or "403" in error_msg:
                return ServiceHealth(
                    name="Firebase",
                    status=ServiceStatus.NOT_CONFIGURED,
                    message="Firestore not set up in Firebase project",
                    details={
                        "project": self.config.firebase_project,
                        "setup_url": f"https://console.firebase.google.com/project/{self.config.firebase_project}/firestore",
                        "hint": "Create a Firestore database in Native mode",
                    },
                )
            return ServiceHealth(
                name="Firebase",
                status=ServiceStatus.ERROR,
                message=error_msg[:200],
            )

    # =========================================================================
    # Vertex AI (Enterprise - Disabled by default)
    # =========================================================================

    def check_vertex(self) -> ServiceHealth:
        """Check Vertex AI connection."""
        if not self.config.vertex_enabled:
            return ServiceHealth(
                name="Vertex AI",
                status=ServiceStatus.DISABLED,
                message="Disabled in config (enterprise tier requires billing)",
                details={
                    "enable_in": "config/google_cloud.json",
                    "pricing": "https://cloud.google.com/vertex-ai/pricing",
                },
            )

        try:
            import vertexai
            from vertexai.generative_models import GenerativeModel

            vertexai.init(project=self.config.vertex_project, location=self.config.vertex_region)

            model = GenerativeModel("gemini-1.5-flash")
            response = model.generate_content("Respond with only: OK")

            return ServiceHealth(
                name="Vertex AI",
                status=ServiceStatus.CONNECTED,
                message=f"Connected to {self.config.vertex_project}",
                details={
                    "project": self.config.vertex_project,
                    "region": self.config.vertex_region,
                },
            )

        except ImportError:
            return ServiceHealth(
                name="Vertex AI",
                status=ServiceStatus.ERROR,
                message="SDK not installed: pip install google-cloud-aiplatform",
            )
        except Exception as e:
            return ServiceHealth(
                name="Vertex AI",
                status=ServiceStatus.ERROR,
                message=str(e)[:200],
            )

    # =========================================================================
    # Stack Health
    # =========================================================================

    def check_all(self) -> dict[str, ServiceHealth]:
        """Check all cloud services."""
        return {
            "ai_studio": self.check_ai_studio(),
            "firebase": self.check_firebase(),
            "vertex": self.check_vertex(),
        }

    def print_status(self):
        """Print formatted status of all services."""
        print("\n" + "=" * 60)
        print("  AIOS Google Cloud Stack Status")
        print("=" * 60)

        status_icons = {
            ServiceStatus.CONNECTED: "✅",
            ServiceStatus.AVAILABLE: "🟡",
            ServiceStatus.DISABLED: "⬚ ",
            ServiceStatus.ERROR: "❌",
            ServiceStatus.NOT_CONFIGURED: "⚙️ ",
        }

        results = self.check_all()

        for service_key, health in results.items():
            icon = status_icons.get(health.status, "?")
            print(f"\n{icon} {health.name}")
            print(f"   Status: {health.status.value}")
            print(f"   {health.message}")

            if health.details:
                for key, value in health.details.items():
                    if not key.startswith("_"):
                        print(f"   {key}: {value}")

        print("\n" + "=" * 60)

        # Summary
        connected = sum(1 for h in results.values() if h.status == ServiceStatus.CONNECTED)
        total = len(results)
        print(f"  Connected: {connected}/{total} services")

        # Next steps
        not_configured = [h for h in results.values() if h.status == ServiceStatus.NOT_CONFIGURED]
        if not_configured:
            print("\n  📋 Setup needed:")
            for h in not_configured:
                if "setup_url" in h.details:
                    print(f"     • {h.name}: {h.details['setup_url']}")
                elif "get_key_url" in h.details:
                    print(f"     • {h.name}: {h.details['get_key_url']}")

        print()


# =============================================================================
# CLI
# =============================================================================


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="AIOS Google Cloud Stack")
    parser.add_argument("--check", "-c", action="store_true", help="Check all services")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--setup", "-s", action="store_true", help="Show setup instructions")

    args = parser.parse_args()

    stack = AIOSCloudStack()

    if args.setup:
        print(
            """
AIOS Google Cloud Setup
=======================

1. AI Studio (Required - Primary Intelligence)
   a. Go to: https://aistudio.google.com/app/apikey
   b. Create an API key
   c. Set environment variable:
      $env:GEMINI_API_KEY = "your-key-here"

2. Firebase (Optional - Persistence)
   a. Go to: https://console.firebase.google.com/project/aios-28728220
   b. Click "Firestore Database" in left menu
   c. Click "Create database"
   d. Choose "Start in production mode"
   e. Select region: us-central1
   f. Authenticate gcloud:
      gcloud auth application-default login
      gcloud config set project aios-28728220

3. Vertex AI (Optional - Enterprise)
   Currently disabled. Requires:
   - GCP billing account
   - Vertex AI API enabled
   - Set vertex_ai.enabled = true in config/google_cloud.json
"""
        )
        return

    if args.json:
        results = stack.check_all()
        output = {
            k: {"status": v.status.value, "message": v.message, "details": v.details}
            for k, v in results.items()
        }
        print(json.dumps(output, indent=2))
        return

    # Default: print status
    stack.print_status()


if __name__ == "__main__":
    main()
