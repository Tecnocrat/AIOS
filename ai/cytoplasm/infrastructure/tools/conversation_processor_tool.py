#!/usr/bin/env python3
"""
AIOS Conversation Processor Tool
Enhanced conversation archiving and analysis tool based on chatgpt_integration

Provides multi-format conversation processing, archiving, and iteration management
for AI service interactions within the AIOS biological architecture.

INTEGRATION CAPABILITIES:
- Multi-format conversation export (JSON, CSV, XML, TXT)
- Conversation iteration management with timestamped archives
- AI service interaction pattern analysis
- Biological architecture compliance with dendritic processing

ARCHITECTURAL ROLE:
Nucleus: Conversation intelligence processing and management
Cytoplasm: Multi-format data transport and conversion
Cell Membrane: External AI service interaction boundaries
"""

import os
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import shutil


class ConversationProcessor:
    """
    Enhanced conversation processing tool with biological architecture integration
    """

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.conversation_archive = (
            self.workspace_root / "tachyonic" / "archive" / "conversation_data"
        )
        self.conversation_archive.mkdir(parents=True, exist_ok=True)

    def archive_conversation_iteration(
        self, conversation_data: Dict[str, Any], service_name: str = "ai_service"
    ) -> Dict[str, Any]:
        """
        Archive a conversation iteration with timestamped backup

        Args:
            conversation_data: Conversation data to archive
            service_name: Name of the AI service (chatgpt, copilot, gemini, etc.)

        Returns:
            Archive operation result
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_dir = self.conversation_archive / service_name
            archive_dir.mkdir(exist_ok=True)

            # Create iteration file
            iteration_file = archive_dir / f"{service_name}_iteration_{timestamp}.json"

            # Add metadata
            conversation_data["metadata"] = {
                "archived_at": datetime.now().isoformat(),
                "service": service_name,
                "iteration_id": timestamp,
                "format_version": "1.0",
            }

            with open(iteration_file, "w", encoding="utf-8") as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)

            return {
                "status": "success",
                "message": f"Conversation archived successfully",
                "archive_path": str(iteration_file),
                "service": service_name,
                "timestamp": timestamp,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Archive failed: {str(e)}",
                "service": service_name,
            }

    def export_conversation_formats(
        self, conversation_data: Dict[str, Any], output_dir: str, base_filename: str
    ) -> Dict[str, Any]:
        """
        Export conversation data in multiple formats (enhanced from chatgpt_integration)

        Args:
            conversation_data: Conversation data to export
            output_dir: Output directory path
            base_filename: Base filename for exports

        Returns:
            Export operation results
        """
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results = {}

            # JSON export
            json_file = output_path / f"{base_filename}_{timestamp}.json"
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            results["json"] = str(json_file)

            # TXT export
            txt_file = output_path / f"{base_filename}_{timestamp}.txt"
            with open(txt_file, "w", encoding="utf-8") as f:
                if "messages" in conversation_data:
                    for msg in conversation_data["messages"]:
                        f.write(
                            f"{msg.get('role', 'unknown')}: {msg.get('content', '')}\n\n"
                        )
                else:
                    f.write(str(conversation_data))
            results["txt"] = str(txt_file)

            # CSV export
            csv_file = output_path / f"{base_filename}_{timestamp}.csv"
            with open(csv_file, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Role", "Content", "Timestamp"])

                if "messages" in conversation_data:
                    for msg in conversation_data["messages"]:
                        writer.writerow(
                            [
                                msg.get("role", ""),
                                msg.get("content", "")[:500],  # Truncate long content
                                msg.get("timestamp", ""),
                            ]
                        )
            results["csv"] = str(csv_file)

            # XML export
            xml_file = output_path / f"{base_filename}_{timestamp}.xml"
            with open(xml_file, "w", encoding="utf-8") as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write("<conversation>\n")

                if "messages" in conversation_data:
                    for msg in conversation_data["messages"]:
                        f.write(f'  <message role="{msg.get("role", "")}">\n')
                        f.write(
                            f'    <content>{msg.get("content", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</content>\n'
                        )
                        f.write(
                            f'    <timestamp>{msg.get("timestamp", "")}</timestamp>\n'
                        )
                        f.write("  </message>\n")

                f.write("</conversation>\n")
            results["xml"] = str(xml_file)

            return {
                "status": "success",
                "message": f"Conversation exported in 4 formats",
                "exports": results,
                "output_dir": str(output_path),
            }

        except Exception as e:
            return {"status": "error", "message": f"Export failed: {str(e)}"}

    def analyze_conversation_patterns(
        self, conversation_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze conversation patterns for intelligence insights

        Args:
            conversation_history: List of conversation data

        Returns:
            Pattern analysis results
        """
        try:
            total_conversations = len(conversation_history)
            total_messages = sum(
                len(conv.get("messages", [])) for conv in conversation_history
            )

            # Analyze message patterns
            user_messages = []
            assistant_messages = []

            for conv in conversation_history:
                for msg in conv.get("messages", []):
                    if msg.get("role") == "user":
                        user_messages.append(msg.get("content", ""))
                    elif msg.get("role") == "assistant":
                        assistant_messages.append(msg.get("content", ""))

            # Calculate basic metrics
            avg_user_length = (
                sum(len(msg) for msg in user_messages) / len(user_messages)
                if user_messages
                else 0
            )
            avg_assistant_length = (
                sum(len(msg) for msg in assistant_messages) / len(assistant_messages)
                if assistant_messages
                else 0
            )

            # Identify common patterns (simplified)
            common_topics = []
            if any("code" in msg.lower() for msg in user_messages):
                common_topics.append("code_assistance")
            if any("error" in msg.lower() for msg in user_messages):
                common_topics.append("error_resolution")
            if any("explain" in msg.lower() for msg in user_messages):
                common_topics.append("explanation_requests")

            return {
                "status": "success",
                "metrics": {
                    "total_conversations": total_conversations,
                    "total_messages": total_messages,
                    "avg_user_message_length": round(avg_user_length, 2),
                    "avg_assistant_message_length": round(avg_assistant_length, 2),
                },
                "patterns": {
                    "common_topics": common_topics,
                    "conversation_depth": (
                        "high"
                        if avg_user_length > 100
                        else "medium" if avg_user_length > 50 else "low"
                    ),
                },
                "insights": {
                    "interaction_quality": (
                        "excellent"
                        if total_messages > 10
                        else "good" if total_messages > 5 else "basic"
                    ),
                    "engagement_level": (
                        "high"
                        if len(common_topics) > 2
                        else "medium" if len(common_topics) > 0 else "low"
                    ),
                },
            }

        except Exception as e:
            return {"status": "error", "message": f"Pattern analysis failed: {str(e)}"}


def process_conversation_data(
    conversation_data: Dict[str, Any], operation: str = "archive"
) -> Dict[str, Any]:
    """
    Main entry point for conversation processing operations

    Args:
        conversation_data: Conversation data to process
        operation: Operation to perform (archive, export, analyze)

    Returns:
        Operation result
    """
    try:
        processor = ConversationProcessor("C:/dev/AIOS")

        if operation == "archive":
            service_name = conversation_data.get("service", "ai_service")
            return processor.archive_conversation_iteration(
                conversation_data, service_name
            )

        elif operation == "export":
            output_dir = conversation_data.get(
                "output_dir", "ai/cytoplasm/runtime/exports"
            )
            base_filename = conversation_data.get("filename", "conversation_export")
            return processor.export_conversation_formats(
                conversation_data, output_dir, base_filename
            )

        elif operation == "analyze":
            history = conversation_data.get("history", [])
            return processor.analyze_conversation_patterns(history)

        else:
            return {
                "status": "error",
                "message": f"Unknown operation: {operation}",
                "supported_operations": ["archive", "export", "analyze"],
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Conversation processing failed: {str(e)}",
        }
