#!/usr/bin/env python3
"""
AIOS Quantum Interface Launcher
Launch both the Quantum Visor (C#) and Code Ingestor (Python) simultaneously
"""

import subprocess
import sys
import time
import threading
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

class QuantumInterfaceLauncher:
    """Launch and manage both quantum interfaces"""
    
    def __init__(self):
        self.aios_root = Path(r"c:\dev\AIOS")
        self.visual_interface_path = self.aios_root / "visual_interface"
        self.scripts_path = self.aios_root / "scripts"
        
        self.visor_process = None
        self.ingestor_process = None
        
    def launch_quantum_visor(self):
        """Launch the C# Quantum Visor"""
        try:
            print("🌌 Launching Quantum Visor (C# WPF)...")
            cmd = ["dotnet", "run", "--project", str(self.visual_interface_path)]
            self.visor_process = subprocess.Popen(
                cmd,
                cwd=str(self.visual_interface_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Quantum Visor launched successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to launch Quantum Visor: {e}")
            return False
            
    def launch_code_ingestor(self):
        """Launch the Python Code Ingestor"""
        try:
            print("🧬 Launching Code Ingestor (Python)...")
            cmd = [sys.executable, "quantum_code_ingestor.py"]
            self.ingestor_process = subprocess.Popen(
                cmd,
                cwd=str(self.scripts_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Code Ingestor launched successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to launch Code Ingestor: {e}")
            return False
            
    def launch_both_interfaces(self):
        """Launch both interfaces simultaneously"""
        print("🚀 AIOS Quantum Interface Launcher")
        print("=" * 50)
        
        # Launch visor first
        visor_success = self.launch_quantum_visor()
        time.sleep(2)  # Give visor time to start
        
        # Launch ingestor
        ingestor_success = self.launch_code_ingestor()
        
        if visor_success and ingestor_success:
            print("\n🎉 Both quantum interfaces launched successfully!")
            print("🌌 Quantum Visor: Consciousness emergence monitoring")
            print("🧬 Code Ingestor: Live code mutation and AI schema processing")
            print("\nPress Ctrl+C to stop both interfaces")
            
            try:
                # Wait for processes
                while True:
                    if self.visor_process and self.visor_process.poll() is not None:
                        print("⚠️ Quantum Visor has stopped")
                        break
                    if self.ingestor_process and self.ingestor_process.poll() is not None:
                        print("⚠️ Code Ingestor has stopped")
                        break
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n🛑 Shutting down quantum interfaces...")
                self.shutdown_interfaces()
                
        else:
            print("❌ Failed to launch one or both interfaces")
            self.shutdown_interfaces()
            
    def shutdown_interfaces(self):
        """Gracefully shutdown both interfaces"""
        if self.visor_process:
            self.visor_process.terminate()
            print("🌌 Quantum Visor terminated")
            
        if self.ingestor_process:
            self.ingestor_process.terminate()
            print("🧬 Code Ingestor terminated")
            
    def create_launcher_gui(self):
        """Create a simple GUI launcher"""
        root = tk.Tk()
        root.title("🚀 AIOS Quantum Interface Launcher")
        root.geometry("500x300")
        root.configure(bg='#000000')
        
        # Title
        title_label = tk.Label(
            root,
            text="🚀 AIOS QUANTUM INTERFACE LAUNCHER",
            font=('Courier New', 14, 'bold'),
            fg='#00FF00',
            bg='#000000'
        )
        title_label.pack(pady=20)
        
        # Status
        self.status_label = tk.Label(
            root,
            text="Ready to launch quantum interfaces",
            font=('Courier New', 10),
            fg='#00FFFF',
            bg='#000000'
        )
        self.status_label.pack(pady=10)
        
        # Buttons
        button_frame = tk.Frame(root, bg='#000000')
        button_frame.pack(pady=20)
        
        launch_visor_btn = tk.Button(
            button_frame,
            text="🌌 Launch Quantum Visor",
            command=self.gui_launch_visor,
            bg='#001133',
            fg='#00AAFF',
            font=('Courier New', 10, 'bold'),
            width=20
        )
        launch_visor_btn.pack(pady=5)
        
        launch_ingestor_btn = tk.Button(
            button_frame,
            text="🧬 Launch Code Ingestor",
            command=self.gui_launch_ingestor,
            bg='#330033',
            fg='#FF00FF',
            font=('Courier New', 10, 'bold'),
            width=20
        )
        launch_ingestor_btn.pack(pady=5)
        
        launch_both_btn = tk.Button(
            button_frame,
            text="🚀 Launch Both Interfaces",
            command=self.gui_launch_both,
            bg='#003300',
            fg='#00FF00',
            font=('Courier New', 12, 'bold'),
            width=20
        )
        launch_both_btn.pack(pady=10)
        
        stop_btn = tk.Button(
            button_frame,
            text="🛑 Stop All",
            command=self.gui_stop_all,
            bg='#330000',
            fg='#FF0000',
            font=('Courier New', 10, 'bold'),
            width=20
        )
        stop_btn.pack(pady=5)
        
        root.mainloop()
        
    def gui_launch_visor(self):
        """GUI launch visor"""
        self.status_label.config(text="Launching Quantum Visor...")
        threading.Thread(target=self.launch_quantum_visor, daemon=True).start()
        
    def gui_launch_ingestor(self):
        """GUI launch ingestor"""
        self.status_label.config(text="Launching Code Ingestor...")
        threading.Thread(target=self.launch_code_ingestor, daemon=True).start()
        
    def gui_launch_both(self):
        """GUI launch both"""
        self.status_label.config(text="Launching both interfaces...")
        threading.Thread(target=self.launch_both_interfaces, daemon=True).start()
        
    def gui_stop_all(self):
        """GUI stop all"""
        self.status_label.config(text="Stopping all interfaces...")
        self.shutdown_interfaces()


if __name__ == "__main__":
    launcher = QuantumInterfaceLauncher()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        launcher.create_launcher_gui()
    else:
        launcher.launch_both_interfaces()
