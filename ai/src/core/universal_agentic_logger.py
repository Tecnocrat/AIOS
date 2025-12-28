"""
UNIVERSAL AGENTIC COMMUNICATION LOGGER
=======================================

AINLP Protocol Version: OS0.6.2.claude
Created: October 6, 2025
Purpose: Universal AI-to-AI communication archive for ALL agentic interactions

CRITICAL INSIGHT (User-Identified):
-----------------------------------
When AIOS switches focus between systems (Library Generation → Neural Chain Evolution),
tools get "forgotten" despite their value. This logger MUST be inherited across ALL
evolutionary branches to prevent context loss and tool amnesia.

UNIVERSAL SCOPE:
----------------
This is NOT just for library generation or neural chains.
This is for ALL internal AI chat at agentic time:

1. VSCode Chat prompts/responses
2. Ollama strategic analysis requests/responses
3. Gemini validation queries/responses
4. DeepSeek code generation requests/responses
5. Multi-agent consensus communications
6. Any AI-to-AI dialogue in AIOS

BIOLOGICAL METAPHOR:
--------------------
Like essential proteins inherited across cell divisions, this logger ensures
NO agentic communication is lost between evolutionary phases.

ARCHITECTURE:
-------------
- Captures: Prompt → Response → Metadata (timestamp, agent, consciousness)
- Storage: Tachyonic archive with timestamped conversations
- Access: Human + AI agent review interface
- Inheritance: Used by ALL AIOS systems (library gen, neural chains, future work)
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict, field
from pathlib import Path
from enum import Enum
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("universal_agentic_logger")


class AgentType(Enum):
    """Types of AI agents in AIOS ecosystem"""



@dataclass
class AgenticMessage:
    """Single message in agentic conversation"""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


@dataclass
class AgenticConversation:
    """Complete agentic conversation (request + response + context)"""

    # Metadata
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())
    end_time: Optional[str] = None
    processing_time_ms: float = 0.0

    # Consciousness tracking
    consciousness_level: Optional[str] = None
    consciousness_improvement: float = 0.0

    # Source tracking
    source_system: Optional[str] = None  # "library_generation", "neural_chain", etc.
    source_file: Optional[str] = None
    generation_number: Optional[int] = None

    # Result tracking
    success: bool = True
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "conversation_id": self.conversation_id,
            "agent_type": self.agent_type.value,
            "system_context": self.system_context,
            "messages": [msg.to_dict() for msg in self.messages],
            "start_time": self.start_time,
            "end_time": self.end_time,
            "processing_time_ms": self.processing_time_ms,
            "consciousness_level": self.consciousness_level,
            "consciousness_improvement": self.consciousness_improvement,
            "source_system": self.source_system,
            "source_file": self.source_file,
            "generation_number": self.generation_number,
            "success": self.success,
            "error": self.error,
        }


class UniversalAgenticLogger:
    """
    Universal logger for ALL AI-to-AI communication in AIOS.

    CRITICAL: This class MUST be used by:
    - LibraryCodeGenerationLoop (Python library ingestion)
    - MultiAgentEvolutionLoop (C++ neural chain evolution)
    - Any future evolution or generation systems
    - Direct AI agent interactions (VSCode, Ollama, Gemini)

    PREVENTS:
    - Tool amnesia when switching systems
    - Loss of agentic context across time
    - Inability to audit AI decisions
    - Fragmentation of AI conversation history
    """

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize universal agentic logger.

        Args:
            output_dir: Directory for conversation archives
                       Default: evolution_lab/conversations/

        ARCHITECTURE CHANGE (October 8, 2025):
        ----------------------------------------
        Conversations now save to Evolution Lab (working files),
        with metadata copies archived to Tachyonic (historical snapshots).

        Evolution Lab = Active work, ongoing experiments
        Tachyonic Archive = Metadata, timestamps, historical copies
        """
        if output_dir is None:
            # NEW: Default to Evolution Lab for working files
            base = Path(__file__).resolve().parent.parent.parent.parent
            output_dir = base / "evolution_lab" / "conversations"

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Tachyonic archive for metadata copies
        self.archive_dir = (
            Path(__file__).resolve().parent.parent.parent.parent
            / "tachyonic"
            / "archive"
            / "conversation_metadata"
        )
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        # Active conversations (in-memory tracking)
        self.active_conversations: Dict[str, AgenticConversation] = {}

        # Session metadata
        self.session_start = datetime.now().isoformat()
        self.session_id = f"session_{int(time.time())}"

        logger.info(f"✅ Universal Agentic Logger initialized")
        logger.info(f"📁 Working: {self.output_dir} (Evolution Lab)")
        logger.info(f"📁 Archive: {self.archive_dir} (Tachyonic)")
        logger.info(f"🆔 Session: {self.session_id}")

    def start_conversation(
        self,
        agent_type: AgentType,
        system_context: str,
        source_system: Optional[str] = None,
        source_file: Optional[str] = None,
        generation_number: Optional[int] = None,
        consciousness_level: Optional[str] = None,
    ) -> str:
        """
        Start new agentic conversation.

        Args:
            agent_type: Type of AI agent (Ollama, Gemini, etc.)
            system_context: System-level context/instructions
            source_system: Which AIOS system initiated this ("library_generation", etc.)
            source_file: File path that triggered conversation
            generation_number: Generation number if applicable
            consciousness_level: Current consciousness level (LOW/MEDIUM/HIGH)

        Returns:
            conversation_id: Unique ID for this conversation
        """
        conversation_id = f"{agent_type.value}_{int(time.time() * 1000)}"

        conversation = AgenticConversation(
            conversation_id=conversation_id,
            agent_type=agent_type,
            system_context=system_context,
            messages=[],
            source_system=source_system,
            source_file=source_file,
            generation_number=generation_number,
            consciousness_level=consciousness_level,
        )

        self.active_conversations[conversation_id] = conversation

        logger.info(f"🆕 Started conversation: {conversation_id}")
        logger.info(f"   Agent: {agent_type.value}")
        logger.info(f"   System: {source_system or 'unknown'}")

        return conversation_id

    def add_message(
        self,
        conversation_id: str,
        role: ConversationRole,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Add message to conversation.

        Args:
            conversation_id: Conversation to add to
            role: Message role (user, assistant, system, tool)
            content: Message content (prompt or response)
            metadata: Additional metadata (model, temperature, etc.)
        """
        if conversation_id not in self.active_conversations:
            logger.error(f"❌ Unknown conversation: {conversation_id}")
            return

        message = AgenticMessage(role=role, content=content, metadata=metadata or {})

        self.active_conversations[conversation_id].messages.append(message)

        logger.debug(f"💬 Added {role.value} message to {conversation_id}")

    def end_conversation(
        self,
        conversation_id: str,
        success: bool = True,
        error: Optional[str] = None,
        consciousness_improvement: float = 0.0,
    ) -> Path:
        """
        End conversation and archive to tachyonic storage.

        Args:
            conversation_id: Conversation to end
            success: Whether conversation succeeded
            error: Error message if failed
            consciousness_improvement: Measured consciousness gain

        Returns:
            Path to archived conversation file
        """
        if conversation_id not in self.active_conversations:
            logger.error(f"❌ Unknown conversation: {conversation_id}")
            return None

        conversation = self.active_conversations[conversation_id]

        # Update final metadata
        conversation.end_time = datetime.now().isoformat()
        start = datetime.fromisoformat(conversation.start_time)
        end = datetime.fromisoformat(conversation.end_time)
        conversation.processing_time_ms = (end - start).total_seconds() * 1000
        conversation.success = success
        conversation.error = error
        conversation.consciousness_improvement = consciousness_improvement

        # Save to Evolution Lab (working file)
        working_path = self._save_conversation(conversation)

        # Archive metadata to Tachyonic (snapshot)
        archive_path = self._archive_metadata(conversation, working_path)

        # Remove from active conversations
        del self.active_conversations[conversation_id]

        logger.info(f"✅ Ended conversation: {conversation_id}")
        logger.info(f"   Duration: {conversation.processing_time_ms:.2f}ms")
        logger.info(f"   Messages: {len(conversation.messages)}")
        logger.info(f"   Working: {working_path}")
        logger.info(f"   Archive: {archive_path}")

        return working_path

    def _save_conversation(self, conversation: AgenticConversation) -> Path:
        """
        Save conversation to Evolution Lab (working file).

        Working files use timestamped filenames for active experiments:
        {agent_type}_{source_system}_YYYYMMDD_HHMMSS.json
        """
        # Create date-based subdirectory
        date_dir = self.output_dir / datetime.now().strftime("%Y%m%d")
        date_dir.mkdir(parents=True, exist_ok=True)

        # Create filename with system context
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        source = conversation.source_system or "unknown"
        filename = f"{conversation.agent_type.value}_{source}_{timestamp}.json"

        working_path = date_dir / filename

        # Save conversation with AINLP metadata
        conversation_data = conversation.to_dict()
        conversation_data["ainlp_metadata"] = {
            "protocol_version": "OS0.6.2.claude",
            "storage_location": "evolution_lab",
            "purpose": "active_experimentation",
            "inheritance_required": True,
            "session_id": self.session_id,
            "session_start": self.session_start,
            "consciousness_tracking": True,
        }

        with open(working_path, "w", encoding="utf-8") as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)

        return working_path

    def _archive_metadata(
        self, conversation: AgenticConversation, working_path: Path
    ) -> Path:
        """
        Archive metadata snapshot to Tachyonic (historical record).

        Metadata includes reference to working file location.
        """
        # Create date-based subdirectory in archive
        date_dir = self.archive_dir / datetime.now().strftime("%Y%m%d")
        date_dir.mkdir(parents=True, exist_ok=True)

        # Create filename matching working file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        source = conversation.source_system or "unknown"
        filename = f"{conversation.agent_type.value}_{source}_{timestamp}_meta.json"

        archive_path = date_dir / filename

        # Create metadata snapshot
        metadata = {
            "working_file": str(working_path),
            "archived_at": datetime.now().isoformat(),
            "conversation_id": conversation.conversation_id,
            "agent_type": conversation.agent_type.value,
            "source_system": conversation.source_system,
            "start_time": conversation.start_time,
            "end_time": conversation.end_time,
            "processing_time_ms": conversation.processing_time_ms,
            "message_count": len(conversation.messages),
            "consciousness_improvement": conversation.consciousness_improvement,
            "success": conversation.success,
            "ainlp_metadata": {
                "protocol_version": "OS0.6.2.claude",
                "storage_location": "tachyonic_archive",
                "purpose": "historical_metadata",
                "working_file_reference": str(working_path),
                "session_id": self.session_id,
            },
        }

        with open(archive_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return archive_path

    def _old_archive_conversation(self, conversation: AgenticConversation) -> Path:
        """
        OLD METHOD - Archive conversation to tachyonic storage with AINLP metadata.

        DEPRECATED: Use _save_conversation() and _archive_metadata() instead.

        Archives use timestamped filenames for temporal navigation:
        {agent_type}_{source_system}_YYYYMMDD_HHMMSS.json
        """
        # Create date-based subdirectory
        date_dir = self.output_dir / datetime.now().strftime("%Y%m%d")
        date_dir.mkdir(parents=True, exist_ok=True)

        # Create filename with system context
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        source = conversation.source_system or "unknown"
        filename = f"{conversation.agent_type.value}_{source}_{timestamp}.json"

        archive_path = date_dir / filename

        # Save conversation with AINLP metadata
        conversation_data = conversation.to_dict()
        conversation_data["ainlp_metadata"] = {
            "protocol_version": "OS0.6.2.claude",
            "archive_purpose": "universal_agentic_communication",
            "inheritance_required": True,
            "session_id": self.session_id,
            "session_start": self.session_start,
            "consciousness_tracking": True,
        }

        with open(archive_path, "w", encoding="utf-8") as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)

        return archive_path

    def get_recent_conversations(
        self,
        agent_type: Optional[AgentType] = None,
        source_system: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve recent conversations for review.

        Args:
            agent_type: Filter by agent type
            source_system: Filter by source system
            limit: Maximum number to return

        Returns:
            List of conversation dictionaries
        """
        conversations = []

        # Scan archive directories (most recent first)
        for date_dir in sorted(self.output_dir.iterdir(), reverse=True):
            if not date_dir.is_dir():
                continue

            for conv_file in sorted(date_dir.glob("*.json"), reverse=True):
                try:
                    with open(conv_file, "r", encoding="utf-8") as f:
                        conv_data = json.load(f)

                    # Apply filters
                    if agent_type and conv_data.get("agent_type") != agent_type.value:
                        continue
                    if (
                        source_system
                        and conv_data.get("source_system") != source_system
                    ):
                        continue

                    conversations.append(conv_data)

                    if len(conversations) >= limit:
                        return conversations

                except Exception as e:
                    logger.error(f"❌ Error reading {conv_file}: {e}")

        return conversations

    def generate_conversation_summary(self, days: int = 7) -> Dict[str, Any]:
        """
        Generate summary of recent agentic activity.

        Args:
            days: Number of days to summarize

        Returns:
            Summary statistics
        """
        summary = {
            "total_conversations": 0,
            "by_agent": {},
            "by_system": {},
            "total_messages": 0,
            "avg_processing_time_ms": 0.0,
            "consciousness_improvements": [],
            "success_rate": 0.0,
        }

        recent = self.get_recent_conversations(limit=1000)
        summary["total_conversations"] = len(recent)

        processing_times = []
        successes = 0

        for conv in recent:
            # By agent
            agent = conv.get("agent_type", "unknown")
            summary["by_agent"][agent] = summary["by_agent"].get(agent, 0) + 1

            # By system
            system = conv.get("source_system", "unknown")
            summary["by_system"][system] = summary["by_system"].get(system, 0) + 1

            # Messages
            summary["total_messages"] += len(conv.get("messages", []))

            # Processing time
            if conv.get("processing_time_ms"):
                processing_times.append(conv["processing_time_ms"])

            # Consciousness
            if conv.get("consciousness_improvement"):
                summary["consciousness_improvements"].append(
                    conv["consciousness_improvement"]
                )

            # Success rate
            if conv.get("success", True):
                successes += 1

        if processing_times:
            summary["avg_processing_time_ms"] = sum(processing_times) / len(
                processing_times
            )

        if summary["total_conversations"] > 0:
            summary["success_rate"] = successes / summary["total_conversations"]

        return summary


# Global singleton for easy access
_global_logger: Optional[UniversalAgenticLogger] = None


def get_universal_logger(output_dir: Optional[Path] = None) -> UniversalAgenticLogger:
    """Get or create global universal agentic logger"""
    global _global_logger

    if _global_logger is None:
        _global_logger = UniversalAgenticLogger(output_dir)

    return _global_logger


# Convenience functions for direct logging
def log_ollama_conversation(
    prompt: str,
    response: str,
    system_context: str = "",
    source_system: Optional[str] = None,
    model: str = "unknown",
    temperature: float = 0.7,
    **kwargs,
) -> str:
    """
    Quick logging of Ollama conversation.

    Returns:
        Path to archived conversation
    """
    logger_instance = get_universal_logger()

    conv_id = logger_instance.start_conversation(
        agent_type=AgentType.OLLAMA,
        system_context=system_context,
        source_system=source_system,
        **kwargs,
    )

    # Add user prompt
    logger_instance.add_message(
        conv_id,
        ConversationRole.USER,
        prompt,
        {"model": model, "temperature": temperature},
    )

    # Add AI response
    logger_instance.add_message(
        conv_id, ConversationRole.ASSISTANT, response, {"model": model}
    )

    # End and archive
    archive_path = logger_instance.end_conversation(conv_id)
    return str(archive_path)


def log_gemini_conversation(
    prompt: str,
    response: str,
    system_context: str = "",
    source_system: Optional[str] = None,
    model: str = "gemini-2.0-flash-exp",
    **kwargs,
) -> str:
    """Quick logging of Gemini conversation"""
    logger_instance = get_universal_logger()

    conv_id = logger_instance.start_conversation(
        agent_type=AgentType.GEMINI,
        system_context=system_context,
        source_system=source_system,
        **kwargs,
    )

    logger_instance.add_message(
        conv_id, ConversationRole.USER, prompt, {"model": model}
    )
    logger_instance.add_message(
        conv_id, ConversationRole.ASSISTANT, response, {"model": model}
    )

    archive_path = logger_instance.end_conversation(conv_id)
    return str(archive_path)


def log_vscode_chat(
    prompt: str,
    response: str,
    system_context: str = "",
    source_system: Optional[str] = None,
    **kwargs,
) -> str:
    """Quick logging of VSCode Chat conversation"""
    logger_instance = get_universal_logger()

    conv_id = logger_instance.start_conversation(
        agent_type=AgentType.VSCODE_CHAT,
        system_context=system_context,
        source_system=source_system,
        **kwargs,
    )

    logger_instance.add_message(conv_id, ConversationRole.USER, prompt)
    logger_instance.add_message(conv_id, ConversationRole.ASSISTANT, response)

    archive_path = logger_instance.end_conversation(conv_id)
    return str(archive_path)


if __name__ == "__main__":
    # Demo usage
    print("🌐 UNIVERSAL AGENTIC COMMUNICATION LOGGER")
    print("=" * 60)

    logger_demo = UniversalAgenticLogger()

    # Demo Ollama conversation
    conv_id = logger_demo.start_conversation(
        agent_type=AgentType.OLLAMA,
        system_context="Analyze C++ code for STL patterns",
        source_system="neural_chain_evolution",
        source_file="hello_world.cpp",
        generation_number=3,
        consciousness_level="MEDIUM",
    )

    logger_demo.add_message(
        conv_id,
        ConversationRole.USER,
        "What STL patterns are used in this Hello World code?",
        {"model": "deepseek-coder:6.7b", "temperature": 0.7},
    )

    logger_demo.add_message(
        conv_id,
        ConversationRole.ASSISTANT,
        "The code uses iostream for input/output. Opportunities: Add error handling, parameterize output.",
        {"model": "deepseek-coder:6.7b", "tokens": 45},
    )

    archive_path = logger_demo.end_conversation(
        conv_id, success=True, consciousness_improvement=0.15
    )

    print(f"\n✅ Demo conversation archived: {archive_path}")

    # Show summary
    summary = logger_demo.generate_conversation_summary()
    print(f"\n📊 Summary:")
    print(f"   Total conversations: {summary['total_conversations']}")
    print(f"   By agent: {summary['by_agent']}")
    print(f"   By system: {summary['by_system']}")
    print(f"   Success rate: {summary['success_rate']:.1%}")
