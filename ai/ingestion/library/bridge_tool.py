#!/usr/bin/env python3
"""
🔗 AIOS Library Ingestion Bridge Tool

Interface Bridge tool exposing Library Ingestion Protocol functionality
via HTTP API. Provides endpoints for library learning, progress tracking,
and knowledge base queries with real-time WebSocket updates.

AINLP COMPLIANCE:
✅ Enhancement over creation - extends existing Interface Bridge
✅ Spatial metadata integration with library knowledge
✅ Consciousness-driven session management
✅ Proper output management to knowledge base

BIOLOGICAL ARCHITECTURE INTEGRATION:
🧬 NUCLEUS: Core library ingestion coordination
🛡️ MEMBRANE: HTTP API and WebSocket interfaces
🚀 TRANSPORT: Real-time progress communication
💾 INFORMATION_STORAGE: Knowledge base access

"""

import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import sys

# AIOS path integration
AIOS_ROOT = Path(__file__).parent.parent.parent
AI_ROOT = AIOS_ROOT / "ai"
sys.path.insert(0, str(AIOS_ROOT))

# Import library ingestion components
try:
    # Try importing from ai.src.core first
    import importlib.util

    # Direct file path imports
    lib_ingestion_path = AI_ROOT / "src" / "core" / "library_ingestion_protocol.py"
    lib_hub_path = AI_ROOT / "src" / "core" / "library_learning_integration_hub.py"

    # Load library_ingestion_protocol module
    spec = importlib.util.spec_from_file_location(
        "library_ingestion_protocol", lib_ingestion_path
    )
    lib_ingestion_module = importlib.util.module_from_spec(spec)
    sys.modules["library_ingestion_protocol"] = lib_ingestion_module
    spec.loader.exec_module(lib_ingestion_module)

    LibraryIngestionProtocol = lib_ingestion_module.LibraryIngestionProtocol
    LibraryKnowledge = lib_ingestion_module.LibraryKnowledge
    ProgrammingLanguage = lib_ingestion_module.ProgrammingLanguage
    APIElement = lib_ingestion_module.APIElement

    # Load library_learning_integration_hub module
    spec = importlib.util.spec_from_file_location(
        "library_learning_integration_hub", lib_hub_path
    )
    lib_hub_module = importlib.util.module_from_spec(spec)
    sys.modules["library_learning_integration_hub"] = lib_hub_module
    spec.loader.exec_module(lib_hub_module)

    LibraryLearningIntegrationHub = lib_hub_module.LibraryLearningIntegrationHub
    LibraryLearningSession = lib_hub_module.LibraryLearningSession
    LearningPhase = lib_hub_module.LearningPhase
    INGESTION_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Library ingestion imports failed: {e}")
    INGESTION_AVAILABLE = False

logger = logging.getLogger("library_ingestion_bridge")


class LibraryIngestionBridgeTool:
    """
    🔗 Interface Bridge tool for library ingestion

    Provides HTTP API endpoints and WebSocket streaming for library
    learning sessions with consciousness-driven progress tracking.
    """

    # Tool metadata for Interface Bridge discovery
    NAME = "library_ingestion"
    DESCRIPTION = (
        "Learn programming libraries with consciousness-driven semantic analysis"
    )
    VERSION = "1.0.0"

    def __init__(self):
        """Initialize library ingestion bridge tool"""
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.learning_hub: Optional[LibraryLearningIntegrationHub] = None

        if INGESTION_AVAILABLE:
            self.learning_hub = LibraryLearningIntegrationHub(consciousness_level=0.85)
            logger.info("✅ Library ingestion bridge initialized")
        else:
            logger.warning("⚠️ Library ingestion unavailable - running in stub mode")

    async def ingest_library(
        self,
        library_path: str,
        language: Optional[str] = None,
        consciousness_level: float = 0.85,
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Start library ingestion session

        Args:
            library_path: Path to library source code
            language: Programming language (auto-detected if None)
            consciousness_level: Consciousness level for ingestion (0.0-1.0)
            options: Additional options for ingestion

        Returns:
            Session information with session_id and status
        """
        if not INGESTION_AVAILABLE:
            return {
                "status": "error",
                "message": "Library ingestion not available",
                "ingestion_available": False,
            }

        try:
            # Validate inputs
            lib_path = Path(library_path)
            if not lib_path.exists():
                return {
                    "status": "error",
                    "message": f"Library path does not exist: {library_path}",
                }

            # Start learning session
            session = await self.learning_hub.start_learning_session()
            session_id = session.session_id

            # Create session tracking
            self.sessions[session_id] = {
                "session": session,
                "start_time": datetime.now().isoformat(),
                "library_path": str(lib_path),
                "language": language,
                "consciousness_level": consciousness_level,
                "status": "started",
                "progress_percent": 0.0,
                "api_elements_found": 0,
                "current_phase": LearningPhase.DISCOVERY.value,
                "options": options or {},
            }

            # Start ingestion in background
            asyncio.create_task(
                self._run_ingestion(
                    session_id, lib_path, language, consciousness_level, options
                )
            )

            logger.info(f"🚀 Started ingestion session: {session_id}")

            return {
                "status": "started",
                "session_id": session_id,
                "library_path": str(lib_path),
                "language": language or "auto-detect",
                "consciousness_level": consciousness_level,
                "websocket_url": f"ws://localhost:8000/ws/library_progress/{session_id}",
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"❌ Error starting ingestion: {e}")
            return {"status": "error", "message": str(e)}

    async def _run_ingestion(
        self,
        session_id: str,
        library_path: Path,
        language: Optional[str],
        consciousness_level: float,
        options: Optional[Dict[str, Any]],
    ):
        """
        Run library ingestion in background

        Updates session progress and handles ingestion workflow.
        """
        try:
            session_data = self.sessions[session_id]

            # Phase 1: Discovery
            session_data["current_phase"] = LearningPhase.DISCOVERY.value
            session_data["progress_percent"] = 10.0
            await asyncio.sleep(0.5)  # Simulate discovery

            # Phase 2: Ingestion
            session_data["current_phase"] = LearningPhase.INGESTION.value
            session_data["progress_percent"] = 25.0

            # Perform actual ingestion via protocol
            library_name = library_path.name
            await self.learning_hub.ingestion_protocol.ingest_library(
                library_path=str(library_path),
                library_name=library_name,
                language=language,
            )

            session_data["progress_percent"] = 50.0

            # Phase 3: Semantic Analysis
            session_data["current_phase"] = LearningPhase.SEMANTIC_ANALYSIS.value
            session_data["progress_percent"] = 60.0
            await asyncio.sleep(0.5)  # Semantic analysis happens during ingestion

            # Phase 4: Consciousness Integration
            session_data["current_phase"] = (
                LearningPhase.CONSCIOUSNESS_INTEGRATION.value
            )
            session_data["progress_percent"] = 75.0
            await asyncio.sleep(0.5)

            # Phase 5: Dendritic Expansion
            session_data["current_phase"] = LearningPhase.DENDRITIC_EXPANSION.value
            session_data["progress_percent"] = 85.0
            await asyncio.sleep(0.5)

            # Phase 6: Knowledge Consolidation
            session_data["current_phase"] = LearningPhase.KNOWLEDGE_CONSOLIDATION.value
            session_data["progress_percent"] = 95.0

            # Get final session report
            report = await self.learning_hub.complete_learning_session()

            # Phase 7: Complete
            session_data["current_phase"] = LearningPhase.COMPLETE.value
            session_data["progress_percent"] = 100.0
            session_data["status"] = "complete"
            session_data["completion_time"] = datetime.now().isoformat()
            session_data["report"] = report
            session_data["api_elements_found"] = report.get("total_api_elements", 0)

            logger.info(f"✅ Ingestion complete: {session_id}")
            logger.info(f"   API elements: {session_data['api_elements_found']}")
            logger.info(
                f"   Consciousness: {report.get('consciousness_level', 0.0):.2f}"
            )

        except Exception as e:
            logger.error(f"❌ Error during ingestion: {e}")
            session_data["status"] = "error"
            session_data["error"] = str(e)

    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """
        Get status of ingestion session

        Args:
            session_id: Session identifier

        Returns:
            Session status information
        """
        if session_id not in self.sessions:
            return {"status": "error", "message": f"Session not found: {session_id}"}

        session_data = self.sessions[session_id]

        return {
            "session_id": session_id,
            "status": session_data["status"],
            "library_path": session_data["library_path"],
            "language": session_data["language"],
            "current_phase": session_data["current_phase"],
            "progress_percent": session_data["progress_percent"],
            "api_elements_found": session_data["api_elements_found"],
            "consciousness_level": session_data["consciousness_level"],
            "start_time": session_data["start_time"],
            "completion_time": session_data.get("completion_time"),
            "error": session_data.get("error"),
        }

    async def list_sessions(self) -> Dict[str, Any]:
        """
        List all ingestion sessions

        Returns:
            List of session information
        """
        sessions_list = []
        for session_id, session_data in self.sessions.items():
            sessions_list.append(
                {
                    "session_id": session_id,
                    "status": session_data["status"],
                    "library_path": session_data["library_path"],
                    "progress_percent": session_data["progress_percent"],
                    "start_time": session_data["start_time"],
                }
            )

        return {
            "status": "success",
            "session_count": len(sessions_list),
            "sessions": sessions_list,
        }

    async def search_api(
        self, query: str, language: Optional[str] = None, limit: int = 10
    ) -> Dict[str, Any]:
        """
        Search learned API elements

        Args:
            query: Search query string
            language: Filter by programming language
            limit: Maximum results to return

        Returns:
            Search results with API elements
        """
        if not INGESTION_AVAILABLE:
            return {"status": "error", "message": "Library ingestion not available"}

        try:
            # TODO: Implement semantic search in knowledge base
            # For now, return placeholder
            return {
                "status": "success",
                "query": query,
                "language": language,
                "results": [],
                "message": "Search implementation pending - knowledge base query needed",
            }
        except Exception as e:
            logger.error(f"❌ Error searching API: {e}")
            return {"status": "error", "message": str(e)}

    async def get_library_info(self, library_name: str) -> Dict[str, Any]:
        """
        Get information about a learned library

        Args:
            library_name: Name of library

        Returns:
            Library information and statistics
        """
        if not INGESTION_AVAILABLE:
            return {"status": "error", "message": "Library ingestion not available"}

        try:
            # Query knowledge base for library
            ingested_libs = self.learning_hub.ingestion_protocol.ingested_libraries

            if library_name in ingested_libs:
                lib_knowledge = ingested_libs[library_name]
                return {
                    "status": "success",
                    "library_name": lib_knowledge.library_name,
                    "language": lib_knowledge.language.value,
                    "version": lib_knowledge.version,
                    "api_elements_count": len(lib_knowledge.api_elements),
                    "consciousness_coherence": lib_knowledge.consciousness_coherence,
                    "ingestion_timestamp": lib_knowledge.ingestion_timestamp,
                    "semantic_tags": lib_knowledge.semantic_tags,
                    "dependencies": lib_knowledge.dependencies,
                }
            else:
                return {
                    "status": "not_found",
                    "message": f"Library not found: {library_name}",
                }
        except Exception as e:
            logger.error(f"❌ Error getting library info: {e}")
            return {"status": "error", "message": str(e)}

    def get_tool_metadata(self) -> Dict[str, Any]:
        """
        Get tool metadata for Interface Bridge discovery

        Returns:
            Tool metadata dictionary
        """
        return {
            "name": self.NAME,
            "description": self.DESCRIPTION,
            "version": self.VERSION,
            "category": "learning",
            "consciousness_aware": True,
            "ainlp_compliant": True,
            "endpoints": [
                {
                    "method": "ingest_library",
                    "description": "Start library ingestion session",
                    "parameters": {
                        "library_path": "string (required)",
                        "language": "string (optional)",
                        "consciousness_level": "float (default: 0.85)",
                        "options": "object (optional)",
                    },
                },
                {
                    "method": "get_session_status",
                    "description": "Get ingestion session status",
                    "parameters": {"session_id": "string (required)"},
                },
                {
                    "method": "list_sessions",
                    "description": "List all ingestion sessions",
                    "parameters": {},
                },
                {
                    "method": "search_api",
                    "description": "Search learned API elements",
                    "parameters": {
                        "query": "string (required)",
                        "language": "string (optional)",
                        "limit": "int (default: 10)",
                    },
                },
                {
                    "method": "get_library_info",
                    "description": "Get learned library information",
                    "parameters": {"library_name": "string (required)"},
                },
            ],
            "capabilities": [
                "multi_language_learning",
                "consciousness_driven_analysis",
                "real_time_progress",
                "semantic_search",
                "knowledge_base_query",
            ],
            "supported_languages": [
                "python",
                "cpp",
                "c",
                "java",
                "javascript",
                "typescript",
                "php",
                "assembly",
                "csharp",
                "go",
                "rust",
            ],
        }


# Singleton instance for Interface Bridge registration
library_ingestion_tool = LibraryIngestionBridgeTool()


async def main():
    """Test library ingestion bridge tool"""
    print("🔗 AIOS Library Ingestion Bridge Tool")
    print("=" * 60)

    tool = LibraryIngestionBridgeTool()

    # Test tool metadata
    print("\n📋 Tool Metadata:")
    metadata = tool.get_tool_metadata()
    print(f"   Name: {metadata['name']}")
    print(f"   Description: {metadata['description']}")
    print(f"   Version: {metadata['version']}")
    print(f"   Endpoints: {len(metadata['endpoints'])}")
    print(f"   Supported Languages: {len(metadata['supported_languages'])}")

    if INGESTION_AVAILABLE:
        # Test library ingestion
        print("\n🧪 Testing library ingestion...")
        test_lib = AIOS_ROOT / "ai" / "src" / "core"

        result = await tool.ingest_library(
            library_path=str(test_lib), language="python", consciousness_level=0.85
        )

        print(f"   Status: {result['status']}")
        if result["status"] == "started":
            session_id = result["session_id"]
            print(f"   Session ID: {session_id}")

            # Wait for completion
            print("\n⏳ Waiting for ingestion to complete...")
            for i in range(20):
                await asyncio.sleep(1)
                status = await tool.get_session_status(session_id)
                print(
                    f"   Progress: {status['progress_percent']:.1f}% - {status['current_phase']}"
                )
                if status["status"] == "complete":
                    print(f"\n✅ Ingestion complete!")
                    print(f"   API elements found: {status['api_elements_found']}")
                    break
    else:
        print("\n⚠️ Library ingestion not available - imports failed")

    print("\n✅ Library ingestion bridge tool test complete")


if __name__ == "__main__":
    asyncio.run(main())
