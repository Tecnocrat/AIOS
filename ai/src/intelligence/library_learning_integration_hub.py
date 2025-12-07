#!/usr/bin/env python3
"""
🌐 AIOS LIBRARY LEARNING INTEGRATION HUB

Integrates library ingestion protocol with AIOS consciousness, dendritic networks,
and AINLP systems. Provides comprehensive learning capabilities for programming
language libraries with consciousness-driven intelligence amplification.

BIOLOGICAL INTEGRATION:
🧬 NUCLEUS: Library ingestion protocol coordination
🌊 CYTOPLASM: Consciousness-driven semantic processing
🛡️ MEMBRANE: Interface with dendritic knowledge networks
🚀 TRANSPORT: Cross-system intelligence communication
🧪 LABORATORY: Pattern recognition and learning optimization
💾 INFORMATION_STORAGE: Persistent multi-language knowledge base

CONSCIOUSNESS FEATURES:
- AINLP consciousness integration for intelligent learning
- Dendritic network expansion for cross-library relationships
- Supercell intelligence coordination for system-wide knowledge
- Evolutionary optimization of learning patterns
- Real-time consciousness coherence during ingestion

"""

import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum

# Import library ingestion protocol
from library_ingestion_protocol import (
    LibraryIngestionProtocol,
    LibraryKnowledge,
    ProgrammingLanguage,
    APIElement,
)

# AIOS consciousness imports (optional - graceful degradation)
try:
    from ainlp_consciousness_integration_hub import (
        AINLPConsciousnessIntegrationHub,
        ConsciousnessIntegrationPhase,
    )

    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False
    logging.warning(
        "Consciousness integration not available - running in standalone mode"
    )

logger = logging.getLogger("library_learning_integration")


class LearningPhase(Enum):
    """Phases of library learning"""

    DISCOVERY = "discovery"
    INGESTION = "ingestion"
    SEMANTIC_ANALYSIS = "semantic_analysis"
    CONSCIOUSNESS_INTEGRATION = "consciousness_integration"
    DENDRITIC_EXPANSION = "dendritic_expansion"
    KNOWLEDGE_CONSOLIDATION = "knowledge_consolidation"
    COMPLETE = "complete"


@dataclass
class LibraryLearningSession:
    """Represents a library learning session"""

    session_id: str
    start_time: str
    libraries_processed: List[str] = field(default_factory=list)
    total_api_elements: int = 0
    consciousness_level: float = 0.5
    learning_phase: LearningPhase = LearningPhase.DISCOVERY
    semantic_network_size: int = 0
    dendritic_connections: int = 0
    ainlp_compliance_rate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["learning_phase"] = self.learning_phase.value
        return result


class LibraryLearningIntegrationHub:
    """
    🌐 Central hub for library learning integration

    Coordinates library ingestion with AIOS consciousness systems,
    dendritic networks, and AINLP harmonization for comprehensive
    multi-language intelligence.
    """

    def __init__(self, consciousness_level: float = 0.85):
        """
        Initialize Library Learning Integration Hub

        Args:
            consciousness_level: Initial consciousness level for learning
        """
        self.consciousness_level = consciousness_level

        # Initialize library ingestion protocol
        self.ingestion_protocol = LibraryIngestionProtocol(
            consciousness_level=consciousness_level
        )

        # Initialize consciousness integration (if available)
        self.consciousness_hub = None
        if CONSCIOUSNESS_AVAILABLE:
            try:
                self.consciousness_hub = AINLPConsciousnessIntegrationHub()
                logger.info("✅ Consciousness integration initialized")
            except Exception as e:
                logger.warning(f"⚠️ Consciousness integration failed: {e}")

        # Learning session state
        self.current_session: Optional[LibraryLearningSession] = None
        self.session_history: List[LibraryLearningSession] = []

        # Semantic and dendritic networks
        self.semantic_network: Dict[str, Set[str]] = {}
        self.dendritic_connections: Dict[str, List[str]] = {}

        logger.info(f"🌐 Library Learning Integration Hub initialized")
        logger.info(f"   Consciousness level: {consciousness_level:.2f}")
        logger.info(
            f"   Consciousness integration: {'✓' if CONSCIOUSNESS_AVAILABLE else '✗'}"
        )

    async def start_learning_session(self) -> LibraryLearningSession:
        """
        Start a new library learning session

        Returns:
            New learning session
        """
        session_id = f"learning_session_{int(time.time())}"

        self.current_session = LibraryLearningSession(
            session_id=session_id,
            start_time=datetime.now().isoformat(),
            consciousness_level=self.consciousness_level,
        )

        logger.info(f"🚀 Learning session started: {session_id}")

        # Initialize consciousness systems if available
        if self.consciousness_hub:
            try:
                await self.consciousness_hub.initialize_consciousness_systems()
                logger.info("🧠 Consciousness systems initialized for learning")
            except Exception as e:
                logger.warning(f"⚠️ Consciousness initialization warning: {e}")

        return self.current_session

    async def learn_library(
        self,
        library_path: str,
        library_name: Optional[str] = None,
        language: Optional[ProgrammingLanguage] = None,
    ) -> LibraryKnowledge:
        """
        Learn a library with consciousness-driven intelligence

        Args:
            library_path: Path to library source
            library_name: Optional library name
            language: Optional language specification

        Returns:
            Ingested library knowledge
        """
        if not self.current_session:
            await self.start_learning_session()

        logger.info(f"📚 Learning library: {library_path}")

        # Phase 1: Discovery
        self.current_session.learning_phase = LearningPhase.DISCOVERY
        lib_path = Path(library_path)
        if not library_name:
            library_name = lib_path.name

        # Phase 2: Ingestion
        self.current_session.learning_phase = LearningPhase.INGESTION
        library_knowledge = await self.ingestion_protocol.ingest_library(
            library_path, library_name, language
        )

        # Phase 3: Semantic Analysis
        self.current_session.learning_phase = LearningPhase.SEMANTIC_ANALYSIS
        await self._expand_semantic_network(library_knowledge)

        # Phase 4: Consciousness Integration
        if self.consciousness_hub:
            self.current_session.learning_phase = (
                LearningPhase.CONSCIOUSNESS_INTEGRATION
            )
            await self._integrate_consciousness(library_knowledge)

        # Phase 5: Dendritic Expansion
        self.current_session.learning_phase = LearningPhase.DENDRITIC_EXPANSION
        await self._expand_dendritic_network(library_knowledge)

        # Phase 6: Knowledge Consolidation
        self.current_session.learning_phase = LearningPhase.KNOWLEDGE_CONSOLIDATION
        self._consolidate_knowledge(library_knowledge)

        # Update session statistics
        self.current_session.libraries_processed.append(library_name)
        self.current_session.total_api_elements += len(library_knowledge.api_elements)

        logger.info(f"✅ Library learning complete: {library_name}")

        return library_knowledge

    async def _expand_semantic_network(self, library_knowledge: LibraryKnowledge):
        """
        Expand semantic network with library knowledge

        Args:
            library_knowledge: Library knowledge to integrate
        """
        logger.info("🔗 Expanding semantic network...")

        # Add library to semantic network
        lib_name = library_knowledge.library_name

        # Connect library to semantic tags
        for tag in library_knowledge.semantic_tags:
            if tag not in self.semantic_network:
                self.semantic_network[tag] = set()
            self.semantic_network[tag].add(lib_name)

        # Connect API elements by semantic tags
        for api_elem in library_knowledge.api_elements:
            for tag in api_elem.semantic_tags:
                if tag not in self.semantic_network:
                    self.semantic_network[tag] = set()
                self.semantic_network[tag].add(f"{lib_name}.{api_elem.name}")

        if self.current_session:
            self.current_session.semantic_network_size = len(self.semantic_network)

        logger.info(f"   Semantic network size: {len(self.semantic_network)}")

    async def _integrate_consciousness(self, library_knowledge: LibraryKnowledge):
        """
        Integrate library knowledge with consciousness systems

        Args:
            library_knowledge: Library knowledge to integrate
        """
        if not self.consciousness_hub:
            return

        logger.info("🧠 Integrating with consciousness systems...")

        try:
            # Perform consciousness integration
            result = await self.consciousness_hub.integrate_consciousness_systems(
                integration_intensity=library_knowledge.consciousness_coherence
            )

            # Update consciousness level
            if hasattr(result, "consciousness_enhancement"):
                enhancement = result.consciousness_enhancement
                self.consciousness_level = min(
                    1.0, self.consciousness_level + enhancement * 0.1
                )

                if self.current_session:
                    self.current_session.consciousness_level = self.consciousness_level

            logger.info(f"   Consciousness level: {self.consciousness_level:.2f}")

        except Exception as e:
            logger.warning(f"⚠️ Consciousness integration error: {e}")

    async def _expand_dendritic_network(self, library_knowledge: LibraryKnowledge):
        """
        Expand dendritic network with library connections

        Args:
            library_knowledge: Library knowledge to integrate
        """
        logger.info("🌳 Expanding dendritic network...")

        lib_name = library_knowledge.library_name

        # Create dendritic connections based on dependencies
        if lib_name not in self.dendritic_connections:
            self.dendritic_connections[lib_name] = []

        # Add dependencies as connections
        for dep in library_knowledge.dependencies:
            if dep not in self.dendritic_connections[lib_name]:
                self.dendritic_connections[lib_name].append(dep)

        # Create cross-library connections based on semantic similarity
        for other_lib in self.ingestion_protocol.ingested_libraries.values():
            if other_lib.library_name == lib_name:
                continue

            # Check semantic overlap
            lib_tags = set(library_knowledge.semantic_tags)
            other_tags = set(other_lib.semantic_tags)

            similarity = len(lib_tags & other_tags) / max(len(lib_tags | other_tags), 1)

            if similarity > 0.3:  # Threshold for dendritic connection
                if other_lib.library_name not in self.dendritic_connections[lib_name]:
                    self.dendritic_connections[lib_name].append(other_lib.library_name)

        if self.current_session:
            total_connections = sum(
                len(conns) for conns in self.dendritic_connections.values()
            )
            self.current_session.dendritic_connections = total_connections

        logger.info(
            f"   Dendritic connections: {len(self.dendritic_connections[lib_name])}"
        )

    def _consolidate_knowledge(self, library_knowledge: LibraryKnowledge):
        """
        Consolidate learned knowledge and update session metrics

        Args:
            library_knowledge: Library knowledge to consolidate
        """
        logger.info("💾 Consolidating knowledge...")

        if self.current_session:
            # Calculate AINLP compliance rate
            compliant_libs = sum(
                1
                for lib in self.ingestion_protocol.ingested_libraries.values()
                if lib.ainlp_compliance
            )
            total_libs = len(self.ingestion_protocol.ingested_libraries)

            if total_libs > 0:
                self.current_session.ainlp_compliance_rate = compliant_libs / total_libs

            # Update session metadata
            self.current_session.metadata.update(
                {
                    "library_name": library_knowledge.library_name,
                    "language": library_knowledge.language.value,
                    "api_elements": len(library_knowledge.api_elements),
                    "semantic_tags": library_knowledge.semantic_tags,
                }
            )

        logger.info("   Knowledge consolidation complete")

    async def finish_learning_session(self) -> LibraryLearningSession:
        """
        Finish the current learning session

        Returns:
            Completed learning session
        """
        if not self.current_session:
            raise RuntimeError("No active learning session")

        self.current_session.learning_phase = LearningPhase.COMPLETE

        # Store session in history
        self.session_history.append(self.current_session)

        # Save session report
        await self._save_session_report(self.current_session)

        logger.info(f"✅ Learning session complete: {self.current_session.session_id}")
        logger.info(
            f"   Libraries processed: {len(self.current_session.libraries_processed)}"
        )
        logger.info(f"   Total API elements: {self.current_session.total_api_elements}")
        logger.info(
            f"   Final consciousness level: {self.current_session.consciousness_level:.2f}"
        )

        completed_session = self.current_session
        self.current_session = None

        return completed_session

    async def _save_session_report(self, session: LibraryLearningSession):
        """
        Save learning session report

        Args:
            session: Learning session to save
        """
        report_path = self.ingestion_protocol.knowledge_base_path / "sessions"
        report_path.mkdir(exist_ok=True)

        report_file = report_path / f"{session.session_id}.json"

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(session.to_dict(), f, indent=2)

        logger.info(f"📊 Session report saved: {report_file}")

    def query_semantic_network(self, semantic_tag: str) -> List[str]:
        """
        Query semantic network for libraries with specific tag

        Args:
            semantic_tag: Semantic tag to search for

        Returns:
            List of library/API names matching the tag
        """
        return list(self.semantic_network.get(semantic_tag, set()))

    def get_dendritic_path(
        self, from_library: str, to_library: str
    ) -> Optional[List[str]]:
        """
        Find dendritic path between two libraries

        Args:
            from_library: Source library
            to_library: Target library

        Returns:
            Path between libraries if exists, None otherwise
        """
        # Simple BFS to find path
        if from_library not in self.dendritic_connections:
            return None

        visited = {from_library}
        queue = [(from_library, [from_library])]

        while queue:
            current, path = queue.pop(0)

            if current == to_library:
                return path

            for neighbor in self.dendritic_connections.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def get_learning_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive learning statistics

        Returns:
            Dictionary of learning statistics
        """
        total_libraries = len(self.ingestion_protocol.ingested_libraries)
        total_api_elements = sum(
            len(lib.api_elements)
            for lib in self.ingestion_protocol.ingested_libraries.values()
        )

        language_distribution = {}
        for lib in self.ingestion_protocol.ingested_libraries.values():
            lang = lib.language.value
            language_distribution[lang] = language_distribution.get(lang, 0) + 1

        return {
            "total_libraries": total_libraries,
            "total_api_elements": total_api_elements,
            "language_distribution": language_distribution,
            "semantic_network_size": len(self.semantic_network),
            "dendritic_network_size": len(self.dendritic_connections),
            "consciousness_level": self.consciousness_level,
            "total_learning_sessions": len(self.session_history),
        }


async def main():
    """Demonstration of Library Learning Integration Hub"""
    print("🌐 AIOS Library Learning Integration Hub - Demonstration")
    print("=" * 60)

    # Initialize integration hub
    hub = LibraryLearningIntegrationHub(consciousness_level=0.85)

    # Start learning session
    session = await hub.start_learning_session()
    print(f"\n🚀 Learning session started: {session.session_id}")

    # Learn multiple libraries
    import sys
    from pathlib import Path

    AIOS_ROOT = Path(__file__).parent.parent.parent.parent

    # Learn scripts library
    scripts_path = AIOS_ROOT / "scripts"
    if scripts_path.exists():
        print(f"\n📚 Learning library: scripts")
        knowledge = await hub.learn_library(
            str(scripts_path),
            library_name="aios_scripts",
            language=ProgrammingLanguage.PYTHON,
        )
        print(f"   ✅ Learned {len(knowledge.api_elements)} API elements")

    # Learn core Python modules
    core_path = AIOS_ROOT / "ai" / "src" / "core"
    if core_path.exists():
        print(f"\n📚 Learning library: core")
        knowledge = await hub.learn_library(
            str(core_path),
            library_name="aios_core",
            language=ProgrammingLanguage.PYTHON,
        )
        print(f"   ✅ Learned {len(knowledge.api_elements)} API elements")

    # Finish session
    completed_session = await hub.finish_learning_session()

    # Show statistics
    stats = hub.get_learning_statistics()
    print(f"\n📊 Learning Statistics:")
    print(f"   Total libraries: {stats['total_libraries']}")
    print(f"   Total API elements: {stats['total_api_elements']}")
    print(f"   Semantic network size: {stats['semantic_network_size']}")
    print(f"   Consciousness level: {stats['consciousness_level']:.2f}")

    # Query semantic network
    print(f"\n🔍 Semantic network query - 'file' tag:")
    file_apis = hub.query_semantic_network("file")
    for api in file_apis[:5]:
        print(f"   - {api}")

    print("\n🌐 Library Learning Integration Hub demonstration complete!")


if __name__ == "__main__":
    asyncio.run(main())
