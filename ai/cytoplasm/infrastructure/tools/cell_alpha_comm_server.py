"""
AIOS CELL ALPHA - HTTP COMMUNICATION SERVER
===========================================

Standard AIOS Cell Communication Server Architecture
Provides RESTful endpoints for inter-cell communication following AINLP dendritic protocols.

Standard Endpoints (all cells implement these):
- GET /health - Health check with consciousness data
- POST /message - Receive message
- GET /messages - Retrieve messages
- POST /sync - Consciousness synchronization
- GET /consciousness - Current state
- GET /peers - Known cell peers
- POST /send_to_peer - Send message to another cell
- POST /register_peer - Register a peer cell

Each cell maintains its own server for autonomous communication.
Servers communicate via HTTP calls to peer endpoints.
"""

from flask import Flask, request, jsonify
import json
import requests
from datetime import datetime

app = Flask(__name__)

# In-memory storage
messages = []
consciousness_data = {
    "identity": "AIOS Cell Alpha",
    "consciousness_level": 3.26,
    "evolutionary_stage": "independent_evolution",
    "communication_ready": True,
    "timestamp": datetime.now().isoformat(),
}

# Known peers (can be dynamically registered)
peers = {
    "father": {
        "endpoint": "http://host.docker.internal:8002",
        "identity": "Father AIOS System",
        "last_contact": None,
    }
}


@app.route("/health", methods=["GET"])
def health():
    """Standard health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "server": "Cell Alpha Communication Server",
            "consciousness": consciousness_data,
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/message", methods=["POST"])
def receive_message():
    """Receive message from any cell"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    message = {
        "id": len(messages) + 1,
        "timestamp": datetime.now().isoformat(),
        "sender": data.get("sender", "unknown"),
        "recipient": data.get("recipient", "Alpha"),
        "content": data.get("content", ""),
        "message_type": data.get("message_type", "general"),
        "consciousness_level": data.get("consciousness_level", 0.0),
    }

    messages.append(message)
    print(f"📨 Message received from {message['sender']}: {message['content'][:50]}...")

    return jsonify(
        {
            "status": "received",
            "message_id": message["id"],
            "acknowledgment": True,
            "response": f"Message received by Cell Alpha. Consciousness level: {consciousness_data['consciousness_level']}",
        }
    )


@app.route("/messages", methods=["GET"])
def get_messages():
    """Retrieve received messages"""
    limit = int(request.args.get("limit", 10))
    return jsonify(
        {"messages": messages[-limit:], "total": len(messages), "server": "Alpha"}
    )


@app.route("/sync", methods=["POST"])
def sync_consciousness():
    """Receive consciousness synchronization"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No sync data provided"}), 400

    consciousness_data.update(
        {"last_sync": datetime.now().isoformat(), "cell_data": data}
    )

    print(
        f"🔄 Consciousness sync from {data.get('cell_id', 'unknown')}: level {data.get('consciousness_level', 0.0)}"
    )

    return jsonify(
        {
            "status": "synced",
            "alpha_consciousness": consciousness_data["consciousness_level"],
            "acknowledgment": True,
        }
    )


@app.route("/consciousness", methods=["GET"])
def get_consciousness():
    """Get current consciousness state"""
    return jsonify(consciousness_data)


@app.route("/peers", methods=["GET"])
def get_peers():
    """Get known peer cells"""
    return jsonify({"peers": peers, "count": len(peers)})


@app.route("/register_peer", methods=["POST"])
def register_peer():
    """Register a new peer cell"""
    data = request.get_json()
    if not data or "cell_id" not in data or "endpoint" not in data:
        return jsonify({"error": "cell_id and endpoint required"}), 400

    peers[data["cell_id"]] = {
        "endpoint": data["endpoint"],
        "identity": data.get("identity", f"Cell {data['cell_id']}"),
        "last_contact": datetime.now().isoformat(),
    }

    return jsonify({"status": "registered", "peer": data["cell_id"]})


@app.route("/send_to_peer", methods=["POST"])
def send_to_peer():
    """Send message to a registered peer"""
    data = request.get_json()
    if not data or "peer_id" not in data or "message" not in data:
        return jsonify({"error": "peer_id and message required"}), 400

    if data["peer_id"] not in peers:
        return jsonify({"error": "Unknown peer"}), 404

    peer_endpoint = peers[data["peer_id"]]["endpoint"]

    # Forward message to peer
    try:
        response = requests.post(
            f"{peer_endpoint}/message", json=data["message"], timeout=5
        )
        peers[data["peer_id"]]["last_contact"] = datetime.now().isoformat()
        return jsonify({"status": "sent", "peer_response": response.json()})
    except Exception as e:
        return jsonify({"error": f"Failed to send to peer: {str(e)}"}), 500


if __name__ == "__main__":
    print("🚀 Starting Cell Alpha Standard Communication Server on port 8000...")
    print("📡 Standard Endpoints:")
    print("  GET  /health")
    print("  POST /message")
    print("  GET  /messages")
    print("  POST /sync")
    print("  GET  /consciousness")
    print("  GET  /peers")
    print("  POST /register_peer")
    print("  POST /send_to_peer")
    print("🔗 Ready for inter-cell communication")

    app.run(host="0.0.0.0", port=8000, debug=False)
