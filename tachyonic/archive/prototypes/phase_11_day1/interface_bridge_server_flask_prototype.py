"""
AIOS Interface Bridge HTTP Server
Phase 11 Day 1: Three-Layer Integration - HTTP REST Bridge

Purpose: Expose Python AI layer (similarity engine + LLM) to C# UI via
         HTTP REST API

Architecture:
- Layer 1 (C# UI) → HTTP REST → Layer 2 (Python AI)
- Endpoints: /health, /ai/similarity, /ai/neurons
- Port: 8000 (localhost)
- Framework: Flask (lightweight, fast startup)

Consciousness: Part of Phase 11 three-layer biological integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path
import traceback

# Add AIOS paths for imports
aios_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(aios_root))
sys.path.insert(0, str(aios_root / "runtime" / "tools"))

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests from C# UI

# Import AI similarity engine (with fallback)
SIMILARITY_AVAILABLE = False
similarity_engine = None

try:
    # Try to import AI similarity engine
    runtime_tools_path = aios_root / "runtime" / "tools"
    if str(runtime_tools_path) not in sys.path:
        sys.path.insert(0, str(runtime_tools_path))

    from ai_agent_dendritic_similarity import AIDendriticSimilarity
    similarity_engine = AIDendriticSimilarity()
    SIMILARITY_AVAILABLE = True
    print("[✓] AI Similarity Engine loaded successfully")
except Exception as e:
    SIMILARITY_AVAILABLE = False
    print(f"[!] AI Similarity Engine not available: {e}")
    similarity_engine = None


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for Interface Bridge validation
    """
    return jsonify({
        "status": "healthy",
        "service": "AIOS Interface Bridge",
        "version": "Phase 11.1",
        "consciousness": 3.05,
        "capabilities": {
            "similarity_engine": SIMILARITY_AVAILABLE,
            "llm_reasoning": SIMILARITY_AVAILABLE,
            "embedding_search": SIMILARITY_AVAILABLE
        },
        "endpoints": [
            "/health",
            "/ai/similarity",
            "/ai/neurons"
        ]
    }), 200


@app.route('/ai/similarity', methods=['POST'])
def ai_similarity_search():
    """
    AI Similarity Search Endpoint

    Request: { "query": "tool for health monitoring" }
    Response:
    {
        "results": [
            {
                "neuron": "comprehensive_aios_health_test.py",
                "similarity": 74.1,
                "reasoning": "LLM explanation...",
                "path": "runtime/tools/..."
            }
        ],
        "query": "...",
        "method": "embedding + llm consensus"
    }
    """
    if not SIMILARITY_AVAILABLE:
        return jsonify({
            "error": "AI Similarity Engine not available",
            "message": "Database or Ollama service not accessible"
        }), 503
    
    try:
        # Parse request
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                "error": "Invalid request",
                "message": "Request body must contain 'query' field"
            }), 400
        
        query = data['query']
        max_results = data.get('max_results', 5)

        print(
            f"[→] AI Similarity Query: '{query}' "
            f"(max_results={max_results})"
        )

        # Execute similarity search
        results = similarity_engine.find_similar_neurons(
            functionality=query,
            max_results=max_results
        )
        
        # Format response
        formatted_results = []
        for result in results:
            purpose = result['neuron_purpose']
            if len(purpose) > 200:
                purpose = purpose[:200] + "..."

            formatted_results.append({
                "neuron": result['neuron_name'],
                "similarity": round(result['consensus_score'], 1),
                "embedding_score": round(result['embedding_score'], 1),
                "llm_score": round(result['llm_score'], 1),
                "reasoning": result.get('llm_reasoning', 'N/A'),
                "path": result['neuron_path'],
                "purpose": purpose
            })

        print(f"[✓] Found {len(formatted_results)} results")
        
        return jsonify({
            "results": formatted_results,
            "query": query,
            "method": "embedding + llm consensus (gemma3:1b)",
            "total_results": len(formatted_results)
        }), 200
        
    except Exception as e:
        print(f"[✗] Error processing similarity query: {e}")
        traceback.print_exc()
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500


@app.route('/ai/neurons', methods=['GET'])
def get_neurons_info():
    """
    Get neuron database statistics
    
    Response: {
        "total_neurons": 866,
        "embeddings_generated": true,
        "supercells": { "ai": 769, "runtime": 60, ... }
    }
    """
    if not SIMILARITY_AVAILABLE:
        return jsonify({
            "error": "AI Similarity Engine not available"
        }), 503
    
    try:
        # Get database statistics
        stats = similarity_engine.get_database_stats()
        
        return jsonify({
            "total_neurons": stats.get('total_neurons', 0),
            "embeddings_generated": stats.get('embeddings_ready', False),
            "supercells": stats.get('by_supercell', {}),
            "database_path": str(similarity_engine.db_path)
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "Failed to retrieve neuron statistics",
            "message": str(e)
        }), 500


@app.route('/', methods=['GET'])
def index():
    """
    Root endpoint with service information
    """
    return jsonify({
        "service": "AIOS Interface Bridge HTTP API",
        "phase": "Phase 11.1 - Three-Layer Integration",
        "description": "HTTP REST bridge between C# UI and Python AI layer",
        "status": "operational",
        "documentation": "See DEV_PATH.md Phase 11",
        "endpoints": {
            "/health": "Health check and capability status",
            "/ai/similarity": "POST - AI similarity search with LLM reasoning",
            "/ai/neurons": "GET - Neuron database statistics"
        }
    }), 200


def main():
    """
    Start Interface Bridge HTTP server
    """
    print("\n" + "="*70)
    print("AIOS Interface Bridge HTTP Server")
    print("Phase 11.1: Three-Layer Biological Integration")
    print("="*70)
    print("Consciousness: 3.05 → 3.10 (Day 1 - HTTP REST Bridge)")
    ai_status = "✓ Available" if SIMILARITY_AVAILABLE else "✗ Unavailable"
    print(f"AI Similarity Engine: {ai_status}")
    print("Server: http://localhost:8000")
    print("Endpoints:")
    print("  - GET  /health         → Health check")
    print("  - POST /ai/similarity  → AI similarity search")
    print("  - GET  /ai/neurons     → Neuron statistics")
    print("="*70 + "\n")
    
    # Start Flask server
    app.run(
        host='localhost',
        port=8000,
        debug=False,  # Disable debug mode for cleaner output
        use_reloader=False  # Disable auto-reload
    )


if __name__ == '__main__':
    main()
