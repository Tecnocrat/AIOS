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
        self.bridge_script = self.ai_root / "nucleus" / "interface_bridge.py"
        self.pid_file = self.ai_root / "interface_bridge.pid"
        self.log_file = self.ai_root / "interface_bridge.log"
        
        # Detect Python executable (prefer venv if exists)
        self.python_exe = self._detect_python()
        
    def _detect_python(self):
        """Detect the correct Python executable (venv or system)"""
        # TEMPORARY: Skip venv detection due to corrupted .venv314t (missing pyvenv.cfg)
        # TODO: Fix venv corruption, then re-enable detection below
        print(f"⚠️  TEMPORARY: Using system Python due to venv corruption")
        print(f"   System Python: {sys.executable}")
        return sys.executable
        
        # PRODUCTION (after venv fix): Uncomment below
        # # Check for virtual environment in ai directory
        # venv_paths = [
        #     self.ai_root / ".venv314t" / "Scripts" / "python.exe",
        #     self.ai_root / ".venv" / "Scripts" / "python.exe",
        #     self.ai_root / "venv" / "Scripts" / "python.exe",
        # ]
        # 
        # for venv_python in venv_paths:
        #     if venv_python.exists():
        #         print(f"Using venv Python: {venv_python}")
        #         return str(venv_python)
        # 
        # # Fallback to system Python
        # print(f"Using system Python: {sys.executable}")
        # return sys.executable
        return sys.executable
        
    def start_server(self):
        """Start the Interface Bridge server as a background process"""
        if self.is_running():
            print("Interface Bridge is already running")
            return True
            
        print("Starting AIOS Interface Bridge server...")
        
        # Start the server process in detached mode
        if sys.platform == "win32":
            # TEMPORARY DEBUG MODE: Use python.exe for visible logging
            # TODO: Switch to pythonw.exe after debugging complete
            # pythonw = windowless Python interpreter (no console, production mode)
            python_path = Path(self.python_exe)
            python_dir = python_path.parent
            
            # DEBUG: Use python.exe to see startup errors in console
            pythonw = self.python_exe
            print(f"🐛 DEBUG MODE: Using {pythonw} for visible logging")
            
            # PRODUCTION (after debug): Uncomment below
            # pythonw = python_dir / "pythonw.exe"
            # if not pythonw.exists():
            #     print(f"Warning: pythonw.exe not found, using {self.python_exe}")
            #     pythonw = self.python_exe
            
            # Windows-specific: CREATE_NEW_PROCESS_GROUP + DETACHED_PROCESS
            # ensures complete independence from parent process
            # DEBUG MODE: Remove CREATE_NO_WINDOW to see console output
            creationflags = (subprocess.CREATE_NEW_PROCESS_GROUP |
                           subprocess.DETACHED_PROCESS)
            # PRODUCTION (after debug): Add CREATE_NO_WINDOW flag
            # creationflags = (subprocess.CREATE_NEW_PROCESS_GROUP |
            #                subprocess.DETACHED_PROCESS |
            #                0x08000000)  # CREATE_NO_WINDOW
            
            # Use shell=False and full paths for maximum stability
            cmd = [
                str(pythonw),
                "-m", "uvicorn",
                "ai.nucleus.interface_bridge:app",
                "--host", "localhost",
                "--port", "8000",
                "--log-level", "info"
            ]
            
            # Redirect output to log file
            with open(self.log_file, 'w') as log:
                # Launch with full detachment - will survive terminal closure
                process = subprocess.Popen(
                    cmd,
                    cwd=str(Path(__file__).parent.parent),  # AIOS root
                    creationflags=creationflags,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    env=os.environ.copy(),
                    close_fds=False  # Keep file handles open for logging
                )
        else:
            # Unix-like systems: Use nohup pattern
            process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", 
                 "ai.nucleus.interface_bridge:app", 
                 "--host", "localhost", "--port", "8000"],
                cwd=str(Path(__file__).parent.parent),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True,  # Unix: detach from terminal
                env=os.environ.copy()
            )
        
        # Save PID for later management
        with open(self.pid_file, 'w') as f:
            f.write(str(process.pid))
            
        # Wait for server to start (health check)
        max_attempts = 15  # 15 seconds max wait
        for attempt in range(max_attempts):
            time.sleep(1)
            if self.check_health():
                print(f"✅ Interface Bridge started successfully (PID: {process.pid})")
                print(f"   API: http://localhost:8000")
                print(f"   Docs: http://localhost:8000/docs")
                print(f"   Health: http://localhost:8000/health")
                print(f"   Log: {self.log_file}")
                return True
        
        print("⚠️  Interface Bridge launched but health check timeout")
        print(f"   PID: {process.pid} (may still be starting)")
        print(f"   Check log: {self.log_file}")
        return False
        
    def stop_server(self):
        """Stop the Interface Bridge server"""
        if not self.pid_file.exists():
            print("Interface Bridge is not running (no PID file)")
            return True
            
        with open(self.pid_file, 'r') as f:
            pid = int(f.read().strip())
            
        # Try psutil first for graceful shutdown
        try:
            import psutil
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=5)
            print(f"Interface Bridge stopped (PID: {pid})")
            self.pid_file.unlink()
            return True
        except ImportError:
            # psutil not available, use taskkill
            pass
        except Exception as e:
            # psutil failed (process not found, etc.)
            print(f"Graceful shutdown failed: {e}")
        
        # Fallback to Windows taskkill
        try:
            result = subprocess.run(
                ["taskkill", "/F", "/PID", str(pid)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"Interface Bridge stopped (PID: {pid})")
            else:
                print(f"Process {pid} not found or already stopped")
        except Exception as e:
            print(f"Failed to stop process {pid}: {e}")
        
        if self.pid_file.exists():
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
