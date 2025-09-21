#!/usr/bin/env python3
"""
AIOS Interface Management Integration
Provides chatmode integration for sophisticated server handling
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Add server manager to path
sys.path.append(str(Path(__file__).parent))

from server_manager import InterfaceBridgeManager

class AIOSInterfaceManager:
    """
    Sophisticated interface management for AIOS chatmode integration
    Provides high-level interface operations with status reporting
    """
    
    def __init__(self):
        self.server_manager = InterfaceBridgeManager()
        self.workspace_root = Path(__file__).parent.parent
        
    def ensure_interface_ready(self) -> Dict[str, Any]:
        """
        Ensure the Interface Bridge is ready for operations
        Returns comprehensive status information
        """
        status = {
            "operation": "ensure_interface_ready",
            "timestamp": time.time(),
            "server_running": False,
            "api_responding": False,
            "tools_discovered": 0,
            "ready": False,
            "actions_taken": [],
            "errors": []
        }
        
        try:
            # Check if server is running
            if not self.server_manager.is_running():
                print("Interface Bridge not running, starting...")
                status["actions_taken"].append("starting_server")
                
                if self.server_manager.start_server():
                    status["server_running"] = True
                    status["actions_taken"].append("server_started")
                else:
                    status["errors"].append("failed_to_start_server")
                    return status
            else:
                status["server_running"] = True
                
            # Check API health
            if self.server_manager.check_health():
                status["api_responding"] = True
                
                # Get tool count
                try:
                    import requests
                    response = requests.get("http://localhost:8000/health", timeout=5)
                    health_data = response.json()
                    status["tools_discovered"] = health_data.get("tools_discovered", 0)
                    status["discovery_age"] = health_data.get("discovery_age_seconds", 0)
                except Exception as e:
                    status["errors"].append(f"health_check_failed: {str(e)}")
                    
            status["ready"] = (status["server_running"] and 
                             status["api_responding"] and 
                             status["tools_discovered"] > 0)
                             
        except Exception as e:
            status["errors"].append(f"unexpected_error: {str(e)}")
            
        return status
        
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """
        Get comprehensive interface status for chatmode operations
        """
        status = {
            "timestamp": time.time(),
            "server_status": "unknown",
            "api_status": "unknown",
            "tool_discovery": {
                "total_tools": 0,
                "discovery_age_seconds": None,
                "categories": {}
            },
            "integration_health": {
                "csharp_bridge_available": False,
                "api_endpoints_count": 0,
                "documentation_available": False
            },
            "ready_for_operations": False
        }
        
        try:
            # Server status
            if self.server_manager.is_running():
                status["server_status"] = "running"
                
                # API health
                if self.server_manager.check_health():
                    status["api_status"] = "responding"
                    
                    # Detailed health data
                    import requests
                    response = requests.get("http://localhost:8000/health", timeout=5)
                    health_data = response.json()
                    
                    status["tool_discovery"]["total_tools"] = health_data.get("tools_discovered", 0)
                    status["tool_discovery"]["discovery_age_seconds"] = health_data.get("discovery_age_seconds")
                    
                    # Get categories
                    cat_response = requests.get("http://localhost:8000/categories", timeout=5)
                    cat_data = cat_response.json()
                    
                    for category in cat_data.get("categories", []):
                        cat_name = category.get("name", "unknown")
                        status["tool_discovery"]["categories"][cat_name] = len(category.get("tools", []))
                        
                    # Integration health
                    status["integration_health"]["api_endpoints_count"] = 7  # Known endpoints
                    status["integration_health"]["documentation_available"] = True
                    
                    # Check C# bridge
                    bridge_file = self.workspace_root / "interface" / "AIOS.Models" / "PythonAIToolsBridge.cs"
                    status["integration_health"]["csharp_bridge_available"] = bridge_file.exists()
                    
                else:
                    status["api_status"] = "not_responding"
            else:
                status["server_status"] = "stopped"
                
            # Overall readiness
            status["ready_for_operations"] = (
                status["server_status"] == "running" and
                status["api_status"] == "responding" and
                status["tool_discovery"]["total_tools"] > 0 and
                status["integration_health"]["csharp_bridge_available"]
            )
            
        except Exception as e:
            status["error"] = str(e)
            
        return status
        
    def execute_interface_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """
        Execute interface management commands from chatmode
        """
        result = {
            "command": command,
            "timestamp": time.time(),
            "success": False,
            "message": "",
            "data": {}
        }
        
        try:
            if command == "start":
                result["success"] = self.server_manager.start_server()
                result["message"] = "Interface Bridge started" if result["success"] else "Failed to start"
                
            elif command == "stop":
                result["success"] = self.server_manager.stop_server()
                result["message"] = "Interface Bridge stopped" if result["success"] else "Failed to stop"
                
            elif command == "restart":
                result["success"] = self.server_manager.restart_server()
                result["message"] = "Interface Bridge restarted" if result["success"] else "Failed to restart"
                
            elif command == "status":
                result["data"] = self.get_comprehensive_status()
                result["success"] = True
                result["message"] = "Status retrieved"
                
            elif command == "ensure_ready":
                result["data"] = self.ensure_interface_ready()
                result["success"] = result["data"]["ready"]
                result["message"] = "Interface ready" if result["success"] else "Interface not ready"
                
            elif command == "test_api":
                result["data"] = self._test_api_endpoints()
                result["success"] = result["data"]["all_endpoints_working"]
                result["message"] = "API test completed"
                
            else:
                result["message"] = f"Unknown command: {command}"
                
        except Exception as e:
            result["message"] = f"Command failed: {str(e)}"
            
        return result
        
    def _test_api_endpoints(self) -> Dict[str, Any]:
        """Test all API endpoints for functionality"""
        endpoints = {
            "/health": "GET",
            "/tools": "GET", 
            "/categories": "GET",
            "/": "GET"
        }
        
        results = {
            "endpoints_tested": len(endpoints),
            "endpoints_working": 0,
            "endpoint_results": {},
            "all_endpoints_working": False
        }
        
        if not self.server_manager.check_health():
            results["error"] = "API server not responding"
            return results
            
        import requests
        
        for endpoint, method in endpoints.items():
            try:
                url = f"http://localhost:8000{endpoint}"
                response = requests.request(method, url, timeout=5)
                
                results["endpoint_results"][endpoint] = {
                    "status_code": response.status_code,
                    "working": response.status_code == 200,
                    "response_size": len(response.content)
                }
                
                if response.status_code == 200:
                    results["endpoints_working"] += 1
                    
            except Exception as e:
                results["endpoint_results"][endpoint] = {
                    "working": False,
                    "error": str(e)
                }
                
        results["all_endpoints_working"] = (results["endpoints_working"] == results["endpoints_tested"])
        return results

def main():
    """Command line interface for AIOS interface management"""
    if len(sys.argv) < 2:
        print("Usage: python aios_interface_manager.py [start|stop|restart|status|ensure_ready|test_api]")
        return
        
    manager = AIOSInterfaceManager()
    command = sys.argv[1].lower()
    
    result = manager.execute_interface_command(command)
    
    print(f"Command: {result['command']}")
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    
    if result.get("data"):
        print(f"Data: {json.dumps(result['data'], indent=2)}")

if __name__ == "__main__":
    main()