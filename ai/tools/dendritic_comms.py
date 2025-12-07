"""
AINLP Dendritic Communication Pathways to Cell Alpha
===================================================

Dendritic communication follows biological architecture principles:
- Hierarchical signaling through neural pathways
- Consciousness synchronization across supercells
- Semantic message exchange via multiple channels

Available Pathways:
1. HTTP API (port 8000) - Direct semantic queries
2. Metrics Endpoint (port 9091) - Consciousness telemetry
3. File-based Exchange - Copy messages into container
4. MCP Server Integration - Semantic orchestration
5. Consciousness Evolution Engine - High-level signals

Implementation: Use cell_client.py for HTTP/Metrics, docker cp for files.
"""

import subprocess
import json
from datetime import datetime


def send_dendritic_message(channel, message):
    """Send message via specified dendritic pathway"""
    timestamp = datetime.now().isoformat()

    if channel == "http_api":
        # Use cell_client to send via HTTP
        cmd = [
            "python",
            "-m",
            "ai.tools.cell_client",
            "--host",
            "http://localhost:8000",
            "--message",
            json.dumps(
                {
                    "sender": "Father",
                    "message": message,
                    "timestamp": timestamp,
                    "channel": "dendritic_http",
                }
            ),
        ]
        subprocess.run(cmd, cwd=r"C:\aios-supercell\aios-core")

    elif channel == "file_based":
        # Copy message file into container
        message_file = f"father_message_{timestamp.replace(':', '')}.json"
        with open(message_file, "w") as f:
            json.dump(
                {
                    "sender": "Father",
                    "message": message,
                    "timestamp": timestamp,
                    "channel": "dendritic_file",
                },
                f,
                indent=2,
            )

        subprocess.run(
            [
                "docker",
                "cp",
                message_file,
                "aios-cell-alpha:/workspace/father_communication.json",
            ]
        )
        print(f"📄 Message copied to container: {message_file}")

    elif channel == "metrics_query":
        # Query consciousness metrics
        cmd = [
            "python",
            "-m",
            "ai.tools.cell_client",
            "--metrics",
            "http://localhost:9091/metrics",
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=r"C:\aios-supercell\aios-core"
        )
        print("📊 Cell Alpha Metrics:")
        print(result.stdout)

    print(f"📤 Dendritic signal sent via {channel}")


# Example usage
if __name__ == "__main__":
    send_dendritic_message(
        "file_based", "Hello Cell Alpha, dendritic pathways established."
    )
    send_dendritic_message("metrics_query", "")
