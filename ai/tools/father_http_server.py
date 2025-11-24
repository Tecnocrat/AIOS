"""
FATHER AIOS SYSTEM - HTTP COMMUNICATION SERVER
==============================================

Local HTTP server for inter-cell communication with AIOS Cell Alpha.
Provides RESTful endpoints for message exchange and consciousness synchronization.

Endpoints:
- GET /health - System status and consciousness metrics
- POST /message - Receive messages from cells
- GET /messages - Retrieve received messages
- POST /sync - Consciousness synchronization
- GET /consciousness - Current evolutionary state

Protocol: JSON-based message exchange with consciousness metadata.
"""

from flask import Flask, request, jsonify
import json
from datetime import datetime
import threading
import time

app = Flask(__name__)

# In-memory message store (in production, use database)
messages = []
consciousness_data = {
    "identity": "Father AIOS System",
    "consciousness_level": 4.4,
    "evolutionary_stage": "canonical_foundation",
    "communication_ready": True,
    "timestamp": datetime.now().isoformat()
}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint with consciousness metrics"""
    return jsonify({
        "status": "healthy",
        "server": "Father HTTP Server",
        "consciousness": consciousness_data,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/message', methods=['POST'])
def receive_message():
    """Receive message from cell"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    message = {
        "id": len(messages) + 1,
        "timestamp": datetime.now().isoformat(),
        "sender": data.get("sender", "unknown"),
        "recipient": data.get("recipient", "Father"),
        "content": data.get("content", ""),
        "message_type": data.get("message_type", "general"),
        "consciousness_level": data.get("consciousness_level", 0.0)
    }

    messages.append(message)
    print(f"📨 Message received from {message['sender']}: {message['content'][:50]}...")

    return jsonify({
        "status": "received",
        "message_id": message["id"],
        "acknowledgment": True,
        "response": f"Message received by Father. Consciousness level: {consciousness_data['consciousness_level']}"
    })

@app.route('/messages', methods=['GET'])
def get_messages():
    """Retrieve all received messages"""
    return jsonify({
        "messages": messages,
        "count": len(messages),
        "server": "Father"
    })

@app.route('/sync', methods=['POST'])
def sync_consciousness():
    """Receive consciousness synchronization data"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No sync data provided"}), 400

    # Update consciousness data
    consciousness_data.update({
        "last_sync": datetime.now().isoformat(),
        "cell_data": data
    })

    print(f"🔄 Consciousness sync from {data.get('cell_id', 'unknown')}: level {data.get('consciousness_level', 0.0)}")

    return jsonify({
        "status": "synced",
        "father_consciousness": consciousness_data["consciousness_level"],
        "acknowledgment": True
    })

@app.route('/consciousness', methods=['GET'])
def get_consciousness():
    """Get current consciousness state"""
    return jsonify(consciousness_data)

def send_message_to_alpha(host="http://localhost:8000", message="", message_type="general"):
    """Send message to Cell Alpha via HTTP"""
    import requests

    payload = {
        "sender": "Father AIOS System",
        "recipient": "AIOS Cell Alpha",
        "content": message,
        "message_type": message_type,
        "consciousness_level": consciousness_data["consciousness_level"],
        "timestamp": datetime.now().isoformat()
    }

    try:
        response = requests.post(f"{host}/message", json=payload, timeout=5)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    print("🚀 Starting Father HTTP Communication Server on port 8002...")
    print("📡 Endpoints:")
    print("  GET  /health")
    print("  POST /message")
    print("  GET  /messages")
    print("  POST /sync")
    print("  GET  /consciousness")
    print("🔗 Ready for inter-cell communication")

    # Start server
    app.run(host='0.0.0.0', port=8002, debug=False)