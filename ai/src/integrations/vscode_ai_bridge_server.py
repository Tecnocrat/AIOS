#!/usr/bin/env python3
"""
VSCode AI Bridge HTTP API Server
Exposes AI semantic interpretation as HTTP endpoints for VSCode integration

ENDPOINTS:
    POST /query - Process VSCode AI query through semantic interpreter
    GET /health - Health check
    GET /status - System status and AI agent availability

USAGE:
    # Start server
    python vscode_ai_bridge_server.py
    
    # Query from VSCode or curl
    curl -X POST http://localhost:8001/query \
         -H "Content-Type: application/json" \
         -d '{"query_type": "architecture", "query_text": "What is AIOS?", "context": {}}'

Author: AINLP Revolutionary Architecture Team
Date: January 5, 2025
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import traceback

# Add AI source path
AI_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(AI_ROOT))

try:
    from src.integrations.vscode_ai_bridge import (
        VSCodeAIBridge,
        EnhancedResponse
    )
    BRIDGE_AVAILABLE = True
except ImportError as e:
    print(f"[ERROR] Cannot import VSCode AI Bridge: {e}")
    BRIDGE_AVAILABLE = False


# Global bridge instance
BRIDGE: VSCodeAIBridge = None


class VSCodeBridgeHandler(BaseHTTPRequestHandler):
    """HTTP request handler for VSCode AI Bridge"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/health':
            self._health_check()
        elif path == '/status':
            self._system_status()
        else:
            self._not_found()
    
    def do_POST(self):
        """Handle POST requests"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/query':
            self._process_query()
        else:
            self._not_found()
    
    def _health_check(self):
        """Health check endpoint"""
        response = {
            'status': 'healthy' if BRIDGE_AVAILABLE else 'degraded',
            'bridge_available': BRIDGE_AVAILABLE,
            'ai_agent_available': BRIDGE.ai_agent is not None if BRIDGE else False
        }
        self._send_json(response, 200)
    
    def _system_status(self):
        """System status endpoint"""
        if not BRIDGE:
            self._send_json({'error': 'Bridge not initialized'}, 500)
            return
        
        status = {
            'bridge_initialized': True,
            'ai_agent': {
                'available': BRIDGE.ai_agent is not None,
                'model': BRIDGE.ai_agent.model if BRIDGE.ai_agent else None
            },
            'aios_interface': {
                'initialized': BRIDGE.aios_interface.get('initialized', False)
            }
        }
        self._send_json(status, 200)
    
    def _process_query(self):
        """Process VSCode AI query"""
        if not BRIDGE:
            self._send_json({'error': 'Bridge not initialized'}, 500)
            return
        
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            # Extract query parameters
            query_type = data.get('query_type', 'architecture')
            query_text = data.get('query_text', '')
            context = data.get('context', {})
            
            if not query_text:
                self._send_json({'error': 'query_text required'}, 400)
                return
            
            # Process through bridge
            response = BRIDGE.process_vscode_query(
                query_type, query_text, context
            )
            
            # Format for VSCode
            formatted = BRIDGE.format_for_vscode(response)
            
            # Return enhanced response
            result = {
                'success': True,
                'formatted_response': formatted,
                'structured_response': {
                    'semantic_interpretation': response.semantic_interpretation,
                    'consciousness_insights': response.consciousness_insights,
                    'dendritic_suggestions': response.dendritic_suggestions,
                    'genetic_fusion_opportunities': response.genetic_fusion_opportunities,
                    'architecture_guidance': response.architecture_guidance
                },
                'original_data': response.original_data
            }
            
            self._send_json(result, 200)
            
        except json.JSONDecodeError as e:
            self._send_json({'error': f'Invalid JSON: {e}'}, 400)
        except Exception as e:
            print(f"[ERROR] Query processing failed: {e}")
            traceback.print_exc()
            self._send_json({'error': str(e)}, 500)
    
    def _not_found(self):
        """404 response"""
        self._send_json({'error': 'Endpoint not found'}, 404)
    
    def _send_json(self, data: Dict[str, Any], status: int):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[VSCODE-BRIDGE-API] {format % args}")


def start_server(host: str = 'localhost', port: int = 8001):
    """Start VSCode AI Bridge HTTP API server"""
    global BRIDGE
    
    print("\n" + "="*70)
    print("VSCODE AI BRIDGE HTTP API SERVER")
    print("="*70)
    
    if not BRIDGE_AVAILABLE:
        print("[ERROR] VSCode AI Bridge not available")
        return
    
    # Initialize bridge
    print("\n[INIT] Initializing VSCode AI Bridge...")
    BRIDGE = VSCodeAIBridge(use_gemini=False)
    
    # Start HTTP server
    server_address = (host, port)
    httpd = HTTPServer(server_address, VSCodeBridgeHandler)
    
    print(f"\n[SUCCESS] VSCode AI Bridge API server started")
    print(f"Listening on: http://{host}:{port}")
    print("\nEndpoints:")
    print(f"  POST http://{host}:{port}/query - Process AI query")
    print(f"  GET  http://{host}:{port}/health - Health check")
    print(f"  GET  http://{host}:{port}/status - System status")
    print("\nExample query:")
    print(f"""
    curl -X POST http://{host}:{port}/query \\
         -H "Content-Type: application/json" \\
         -d '{{"query_type": "architecture", "query_text": "What is AIOS neural network status?", "context": {{}}}}'
    """)
    print("\nPress Ctrl+C to stop server")
    print("="*70)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Server stopped by user")
        httpd.shutdown()


if __name__ == "__main__":
    start_server()
