#!/usr/bin/env python3
"""
AIOS Interface Bridge Server Manager
Provides process management for running the Interface Bridge as a background service
"""

import subprocess
import sys
import time
import json
import requests
import os
from pathlib import Path

class InterfaceBridgeManager:
    def __init__(self):
        self.ai_root = Path(__file__).parent
        self.bridge_script = self.ai_root / "core" / "interface_bridge.py"
        self.pid_file = self.ai_root / "interface_bridge.pid"
        self.log_file = self.ai_root / "interface_bridge.log"
        
    def start_server(self):
        """Start the Interface Bridge server as a background process"""
        if self.is_running():
            print("Interface Bridge is already running")
            return True
            
        print("Starting AIOS Interface Bridge server...")
        
        # Start the server process in detached mode
        if sys.platform == "win32":
            # Windows: Use detached process flags
            creationflags = (subprocess.DETACHED_PROCESS |
                             subprocess.CREATE_NEW_PROCESS_GROUP)
            # Redirect output to files to prevent blocking
            with open(self.log_file, 'w') as log:
                process = subprocess.Popen(
                    [sys.executable, "-m", "uvicorn",
                     "ai.nucleus.interface_bridge:app",
                     "--host", "localhost", "--port", "8000"],
                    cwd=r"C:\dev\AIOS",
                    creationflags=creationflags,
                    stdout=log,
                    stderr=log,
                    env=os.environ.copy()
                )
        else:
            # Unix-like systems
            process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", 
                 "ai.nucleus.interface_bridge:app", 
                 "--host", "localhost", "--port", "8000"],
                cwd=r"C:\dev\AIOS",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env={"PYTHONIOENCODING": "utf-8"}
            )
        
        # Save PID
        with open(self.pid_file, 'w') as f:
            f.write(str(process.pid))
            
        # Wait for server to start
        max_attempts = 10
        for attempt in range(max_attempts):
            time.sleep(1)
            if self.check_health():
                print("Interface Bridge started successfully "
                      f"(PID: {process.pid})")
                print("API available at: http://localhost:8000")
                print("Documentation: http://localhost:8000/docs")
                return True
                
        print("Failed to start Interface Bridge")
        return False
        
    def stop_server(self):
        """Stop the Interface Bridge server"""
        if not self.pid_file.exists():
            print("Interface Bridge is not running (no PID file)")
            return True
            
        with open(self.pid_file, 'r') as f:
            pid = int(f.read().strip())
            
        try:
            import psutil
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=5)
            print(f"Interface Bridge stopped (PID: {pid})")
        except (psutil.NoSuchProcess, psutil.TimeoutExpired):
            print(f"Process {pid} not found or already stopped")
        except ImportError:
            # Fallback if psutil not available
            subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                           capture_output=True)
            print(f"Interface Bridge stopped (PID: {pid})")
            
        self.pid_file.unlink()
        return True
        
    def emergency_shutdown(self):
        """Emergency shutdown with immediate isolation"""
        print("EMERGENCY SHUTDOWN: Isolating Interface Bridge immediately...")
        
        if self.pid_file.exists():
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
                
            try:
                import psutil
                process = psutil.Process(pid)
                process.kill()  # Force kill for emergency
                print(f"Interface Bridge emergency shutdown (PID: {pid})")
            except (psutil.NoSuchProcess, ImportError):
                try:
                    subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                                   capture_output=True)
                    print(f"Interface Bridge emergency shutdown (PID: {pid})")
                except subprocess.SubprocessError:
                    print("Could not terminate process")
                    
            self.pid_file.unlink()
        
        # Log emergency shutdown
        with open(self.log_file, 'a') as log:
            log.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] EMERGENCY SHUTDOWN EXECUTED\n")
        
        return True
        
    def restart_server(self):
        """Restart the Interface Bridge server"""
        print("Restarting Interface Bridge...")
        self.stop_server()
        time.sleep(2)
        return self.start_server()
        
    def is_running(self):
        """Check if the server is running"""
        if not self.pid_file.exists():
            return False
            
        with open(self.pid_file, 'r') as f:
            pid = int(f.read().strip())
            
        try:
            import psutil
            return psutil.pid_exists(pid)
        except ImportError:
            # Fallback check
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}"],
                capture_output=True, text=True
            )
            return str(pid) in result.stdout
            
    def check_health(self):
        """Check if the API is responding"""
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            return response.status_code == 200
        except Exception:
            return False
            
    def status(self):
        """Show server status"""
        print("AIOS Interface Bridge Status")
        print("=" * 40)
        
        if self.is_running():
            print("Server Status: RUNNING")
            
            if self.check_health():
                try:
                    response = requests.get("http://localhost:8000/health")
                    health_data = response.json()
                    print("Tools Discovered: "
                          f"{health_data.get('tools_discovered', 'N/A')}")
                    print("Discovery Age: "
                          f"{health_data.get('discovery_age_seconds', 'N/A')}"
                          "s")
                    print("Sequencer Status: "
                          f"{health_data.get('sequencer_status', 'N/A')}")
                except Exception:
                    print("API responding but data unavailable")
            else:
                print("API Status: NOT RESPONDING")
        else:
            print("Server Status: STOPPED")
            
        print("API URL: http://localhost:8000")
        print("Documentation: http://localhost:8000/docs")


def main():
    manager = InterfaceBridgeManager()
    
    if len(sys.argv) < 2:
        print("Usage: python server_manager.py [start|stop|restart|status]")
        return
        
    command = sys.argv[1].lower()
    
    if command == "start":
        manager.start_server()
    elif command == "stop":
        manager.stop_server()
    elif command == "restart":
        manager.restart_server()
    elif command == "status":
        manager.status()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: start, stop, restart, status")


if __name__ == "__main__":
    main()
