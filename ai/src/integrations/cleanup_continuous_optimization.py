"""
AIOS Continuous Optimization Cleanup Script
Stop any running continuous optimization background processes

This script safely stops and cleans up any running continuous optimization
daemon processes and background threads.
"""

import os
import sys
import signal
import psutil
import time
from typing import List, Dict, Any

def find_aios_optimization_processes() -> List[Dict[str, Any]]:
    """Find any AIOS optimization processes currently running"""
    optimization_processes = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
            try:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                # Check for AIOS optimization-related processes
                if any(keyword in cmdline.lower() for keyword in [
                    'continuous_optimization',
                    'activate_continuous_optimization',
                    'demo_continuous_optimization',
                    'optimization_daemon'
                ]):
                    optimization_processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': cmdline,
                        'create_time': proc.info['create_time']
                    })
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
    except Exception as e:
        print(f"Error scanning processes: {e}")
    
    return optimization_processes

def stop_optimization_daemon():
    """Stop the continuous optimization daemon gracefully"""
    print(" Stopping AIOS Continuous Optimization Daemon...")
    
    try:
        # Add integration paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        integrations_dir = os.path.join(current_dir, "..", "integrations")
        sys.path.append(integrations_dir)
        
        # Try to get the daemon instance and stop it
        from continuous_optimization_daemon import get_continuous_optimization_daemon
        
        daemon = get_continuous_optimization_daemon()
        if daemon and daemon.is_running:
            print(" Daemon instance found - stopping gracefully...")
            daemon.stop_continuous_optimization()
            print(" Daemon stopped gracefully")
            return True
        else:
            print("ℹ No active daemon instance found")
            return False
            
    except Exception as e:
        print(f" Could not stop daemon gracefully: {e}")
        return False

def kill_optimization_processes(processes: List[Dict[str, Any]]) -> int:
    """Force kill optimization processes"""
    killed_count = 0
    
    for proc_info in processes:
        try:
            pid = proc_info['pid']
            print(f" Force killing process {pid}: {proc_info['name']}")
            
            # Try to terminate gracefully first
            proc = psutil.Process(pid)
            proc.terminate()
            
            # Wait a moment for graceful termination
            try:
                proc.wait(timeout=3)
                print(f" Process {pid} terminated gracefully")
                killed_count += 1
            except psutil.TimeoutExpired:
                # Force kill if not terminated gracefully
                print(f" Force killing process {pid}")
                proc.kill()
                killed_count += 1
                
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f" Could not kill process {proc_info['pid']}: {e}")
        except Exception as e:
            print(f" Error killing process {proc_info['pid']}: {e}")
    
    return killed_count

def cleanup_daemon_state_files():
    """Clean up any daemon state files"""
    print("🧹 Cleaning up daemon state files...")
    
    aios_root = "c:\\dev\\AIOS"
    # Check both old and new locations
    state_files = [
        "continuous_optimization_state.json",
        "tachyonic\\archive\\optimization_reports\\continuous_optimization_activation_report.json",
        "tachyonic\\archive\\optimization_reports\\continuous_optimization_final_status.json"
    ]
    
    cleaned_count = 0
    for state_file in state_files:
        file_path = os.path.join(aios_root, state_file)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f" Removed: {state_file}")
                cleaned_count += 1
            else:
                print(f"ℹ Not found: {state_file}")
        except Exception as e:
            print(f" Could not remove {state_file}: {e}")
    
    return cleaned_count

def check_vscode_python_processes():
    """Check if the Python processes are actually VSCode extensions"""
    print(" Analyzing Python processes...")
    
    vscode_processes = []
    other_processes = []
    
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] == 'python.exe':
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    
                    if 'vscode\\extensions' in cmdline.lower():
                        vscode_processes.append({
                            'pid': proc.info['pid'],
                            'cmdline': cmdline
                        })
                    elif 'aios' in cmdline.lower():
                        other_processes.append({
                            'pid': proc.info['pid'],
                            'cmdline': cmdline
                        })
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
    except Exception as e:
        print(f"Error analyzing processes: {e}")
    
    print(f" Found {len(vscode_processes)} VSCode extension Python processes")
    print(f" Found {len(other_processes)} other AIOS-related Python processes")
    
    if vscode_processes:
        print("\n VSCode Extension Processes (these are normal and should restart):")
        for proc in vscode_processes[:5]:  # Show first 5
            extension_name = "unknown"
            if "pylint" in proc['cmdline']:
                extension_name = "Python Pylint"
            elif "black-formatter" in proc['cmdline']:
                extension_name = "Python Black Formatter"
            elif "flake8" in proc['cmdline']:
                extension_name = "Python Flake8"
            elif "isort" in proc['cmdline']:
                extension_name = "Python isort"
            
            print(f"   • PID {proc['pid']}: {extension_name}")
        
        if len(vscode_processes) > 5:
            print(f"   • ... and {len(vscode_processes) - 5} more VSCode extension processes")
    
    if other_processes:
        print("\n Other AIOS Python Processes:")
        for proc in other_processes:
            print(f"   • PID {proc['pid']}: {proc['cmdline'][:100]}...")
    
    return vscode_processes, other_processes

def main():
    """Main cleanup function"""
    print("🧹 AIOS Continuous Optimization Cleanup")
    print("=" * 45)
    print()
    
    # Check what's currently running
    print(" Scanning for optimization processes...")
    optimization_processes = find_aios_optimization_processes()
    
    if optimization_processes:
        print(f" Found {len(optimization_processes)} optimization processes:")
        for proc in optimization_processes:
            print(f"   • PID {proc['pid']}: {proc['name']} - {proc['cmdline'][:80]}...")
        print()
    else:
        print(" No AIOS optimization processes found")
    
    # Analyze all Python processes
    vscode_processes, other_aios_processes = check_vscode_python_processes()
    
    # Try to stop daemon gracefully
    daemon_stopped = stop_optimization_daemon()
    
    # Kill any remaining optimization processes
    killed_count = 0
    if optimization_processes:
        print("\n Force stopping optimization processes...")
        killed_count = kill_optimization_processes(optimization_processes)
    
    # Clean up state files
    print()
    cleaned_files = cleanup_daemon_state_files()
    
    # Summary
    print()
    print(" CLEANUP SUMMARY:")
    print(f"   • Daemon gracefully stopped: {'Yes' if daemon_stopped else 'No'}")
    print(f"   • Optimization processes killed: {killed_count}")
    print(f"   • State files cleaned: {cleaned_files}")
    print(f"   • VSCode extension processes: {len(vscode_processes)} (these are normal)")
    print(f"   • Other AIOS processes: {len(other_aios_processes)}")
    
    print()
    if len(vscode_processes) > 0:
        print("ℹ NOTE: VSCode extension Python processes are normal and will restart")
        print("   automatically. These handle Python linting, formatting, etc.")
        print("   If you want to stop them, close VSCode completely.")
    
    if len(other_aios_processes) > 0:
        print(" WARNING: Found other AIOS-related Python processes.")
        print("   You may need to investigate these manually.")
    
    print()
    print(" Cleanup complete!")

if __name__ == "__main__":
    main()
