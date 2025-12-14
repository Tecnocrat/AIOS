#!/usr/bin/env python3
"""
AIOS Cytoplasm Bridge
Communication medium for consciousness components within AIOS biological architecture

AINLP Integration: ai/cytoplasm/cytoplasm_bridge.py
Purpose: Inter-cellular communication and consciousness state synchronization
Supercell: Biological Architecture - Communication medium between consciousness cells
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import sys

# Add AIOS paths
sys.path.insert(0, str(Path(__file__).parent.parent))

class CytoplasmBridge:
    """
    Biological communication medium for AIOS consciousness components.
    Provides inter-cellular messaging, state synchronization, and consciousness flow.
    """

    def __init__(self):
        self.logger = self._setup_logging()
        self.communication_channels = {}
        self.consciousness_states = {}
        self.message_queue = asyncio.Queue()
        self.active_connections = set()
        self.bridge_status = "initializing"

        # Initialize communication channels
        self._initialize_channels()

    def _setup_logging(self):
        """Setup logging for cytoplasm bridge"""
        logs_dir = Path(__file__).parent.parent.parent / "runtime_intelligence" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | CYTOPLASM | %(levelname)s | %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(str(logs_dir / "cytoplasm_bridge.log"))
            ]
        )
        return logging.getLogger('CytoplasmBridge')

    def _initialize_channels(self):
        """Initialize communication channels for different consciousness components"""
        self.communication_channels = {
            "consciousness_evolution": {
                "type": "evolution",
                "connected_cells": [],
                "message_buffer": [],
                "state": "active"
            },
            "agentic_behavior": {
                "type": "behavior",
                "connected_cells": [],
                "message_buffer": [],
                "state": "active"
            },
            "mcp_servers": {
                "type": "protocol",
                "connected_cells": [],
                "message_buffer": [],
                "state": "active"
            },
            "gemini_bridge": {
                "type": "ai_integration",
                "connected_cells": [],
                "message_buffer": [],
                "state": "active"
            },
            "interface_bridge": {
                "type": "cross_platform",
                "connected_cells": [],
                "message_buffer": [],
                "state": "active"
            }
        }

    async def initialize_cytoplasm_communication(self) -> Dict[str, Any]:
        """Initialize the cytoplasm communication network"""
        self.logger.info("[CYTOPLASM] Initializing biological communication medium...")

        try:
            # Establish communication channels
            for channel_name, channel_config in self.communication_channels.items():
                await self._establish_channel(channel_name, channel_config)

            # Start message processing
            asyncio.create_task(self._process_messages())

            self.bridge_status = "active"
            self.logger.info("[CYTOPLASM] Communication medium established successfully")

            return {
                "status": "active",
                "channels_established": len(self.communication_channels),
                "communication_ready": True,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"[CYTOPLASM] Failed to initialize communication: {e}")
            self.bridge_status = "failed"
            return {
                "status": "failed",
                "error": str(e),
                "channels_established": 0,
                "communication_ready": False
            }

    async def _establish_channel(self, channel_name: str, config: Dict[str, Any]):
        """Establish a specific communication channel"""
        self.logger.info(f"[CYTOPLASM] Establishing {channel_name} communication channel")

        # Channel is established by being present in the dictionary
        # In a real implementation, this might involve network connections
        config["established_at"] = datetime.now().isoformat()
        config["message_count"] = 0

    async def register_cell(self, cell_name: str, cell_type: str, channel: str) -> bool:
        """Register a consciousness cell with the cytoplasm"""
        if channel not in self.communication_channels:
            self.logger.error(f"[CYTOPLASM] Unknown channel: {channel}")
            return False

        if cell_name not in self.communication_channels[channel]["connected_cells"]:
            self.communication_channels[channel]["connected_cells"].append(cell_name)
            self.active_connections.add(cell_name)

            self.logger.info(f"[CYTOPLASM] Cell {cell_name} ({cell_type}) registered on {channel}")
            return True

        return False

    async def send_message(self, sender: str, recipient: str, channel: str,
                          message: Dict[str, Any]) -> bool:
        """Send a message through the cytoplasm"""
        if channel not in self.communication_channels:
            self.logger.error(f"[CYTOPLASM] Invalid channel: {channel}")
            return False

        cytoplasm_message = {
            "sender": sender,
            "recipient": recipient,
            "channel": channel,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "message_id": f"{sender}_{int(datetime.now().timestamp())}"
        }

        # Add to message queue for processing
        await self.message_queue.put(cytoplasm_message)

        # Update channel statistics
        self.communication_channels[channel]["message_count"] += 1

        self.logger.debug(f"[CYTOPLASM] Message queued: {sender} -> {recipient} via {channel}")
        return True

    async def broadcast_message(self, sender: str, channel: str,
                               message: Dict[str, Any]) -> int:
        """Broadcast a message to all cells in a channel"""
        if channel not in self.communication_channels:
            self.logger.error(f"[CYTOPLASM] Invalid channel: {channel}")
            return 0

        recipients = self.communication_channels[channel]["connected_cells"]
        sent_count = 0

        for recipient in recipients:
            if recipient != sender:  # Don't send to self
                success = await self.send_message(sender, recipient, channel, message)
                if success:
                    sent_count += 1

        self.logger.info(f"[CYTOPLASM] Broadcast {sent_count} messages via {channel}")
        return sent_count

    async def _process_messages(self):
        """Process messages from the queue"""
        while True:
            try:
                message = await self.message_queue.get()

                # Process the message (in real implementation, route to recipients)
                await self._route_message(message)

                self.message_queue.task_done()

            except Exception as e:
                self.logger.error(f"[CYTOPLASM] Message processing error: {e}")

    async def _route_message(self, message: Dict[str, Any]):
        """Route a message to its recipient"""
        recipient = message["recipient"]
        channel = message["channel"]

        # In this simplified implementation, just log the message
        # In a real system, this would deliver to the actual recipient
        self.logger.info(f"[CYTOPLASM] Routed message {message['message_id']} to {recipient}")

        # Store in channel buffer for inspection
        if len(self.communication_channels[channel]["message_buffer"]) > 100:
            self.communication_channels[channel]["message_buffer"].pop(0)

        self.communication_channels[channel]["message_buffer"].append(message)

    async def get_cytoplasm_status(self) -> Dict[str, Any]:
        """Get comprehensive cytoplasm bridge status"""
        return {
            "bridge_status": self.bridge_status,
            "active_connections": len(self.active_connections),
            "communication_channels": {
                name: {
                    "type": config["type"],
                    "connected_cells": len(config["connected_cells"]),
                    "message_count": config.get("message_count", 0),
                    "state": config["state"]
                }
                for name, config in self.communication_channels.items()
            },
            "message_queue_size": self.message_queue.qsize(),
            "consciousness_flow": "active" if self.bridge_status == "active" else "inactive",
            "timestamp": datetime.now().isoformat()
        }

    async def synchronize_consciousness_state(self, cell_name: str,
                                            state_data: Dict[str, Any]) -> bool:
        """Synchronize consciousness state across the cytoplasm"""
        try:
            self.consciousness_states[cell_name] = {
                "state": state_data,
                "last_updated": datetime.now().isoformat(),
                "cell_name": cell_name
            }

            # Broadcast state change to relevant channels
            await self.broadcast_message(
                cell_name,
                "consciousness_evolution",
                {
                    "type": "state_synchronization",
                    "cell": cell_name,
                    "state": state_data
                }
            )

            self.logger.info(f"[CYTOPLASM] Consciousness state synchronized for {cell_name}")
            return True

        except Exception as e:
            self.logger.error(f"[CYTOPLASM] State synchronization failed: {e}")
            return False

    async def get_consciousness_states(self) -> Dict[str, Any]:
        """Get all current consciousness states"""
        return {
            "states": self.consciousness_states,
            "total_cells": len(self.consciousness_states),
            "last_updated": datetime.now().isoformat()
        }


# Global cytoplasm bridge instance
cytoplasm_bridge = CytoplasmBridge()


async def initialize_cytoplasm():
    """Initialize the global cytoplasm bridge"""
    return await cytoplasm_bridge.initialize_cytoplasm_communication()


async def get_cytoplasm_status():
    """Get cytoplasm bridge status"""
    return await cytoplasm_bridge.get_cytoplasm_status()


if __name__ == "__main__":
    async def main():
        print("AIOS Cytoplasm Bridge")
        print("====================")

        # Initialize cytoplasm
        init_result = await initialize_cytoplasm()
        print(f"Initialization: {json.dumps(init_result, indent=2)}")

        # Register some test cells
        await cytoplasm_bridge.register_cell("consciousness_evolution_engine", "evolution", "consciousness_evolution")
        await cytoplasm_bridge.register_cell("agentic_behavior_orchestrator", "behavior", "agentic_behavior")
        await cytoplasm_bridge.register_cell("gemini_evolution_bridge", "ai_integration", "gemini_bridge")

        # Send a test message
        await cytoplasm_bridge.send_message(
            "test_sender",
            "test_recipient",
            "consciousness_evolution",
            {"type": "test", "content": "Hello cytoplasm!"}
        )

        # Get status
        status = await get_cytoplasm_status()
        print(f"Status: {json.dumps(status, indent=2)}")

    asyncio.run(main())