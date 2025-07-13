#!/usr/bin/env python3
"""
AIOS Server Startup Script
Simplified startup for the AIOS VSCode Integration Server
"""

import os
import subprocess
import sys
import time


def find_server_file(possible_names=None):
    """Search for the server file in likely locations."""
    if possible_names is None:
        possible_names = [
            "aios_vscode_integration_server.py",
            os.path.join("..", "aios_vscode_integration_server.py"),
        ]
    for name in possible_names:
        if os.path.exists(name):
            return os.path.abspath(name)
    return None


def run_preflight_diagnostics():
    """Run integration diagnostics before starting the server."""
    integration_path = os.path.join(
        os.path.dirname(__file__), "tests", "aios_vscode_integration.py"
    )
    if os.path.exists(integration_path):
        print("🧪 Running preflight integration diagnostics...")
        result = subprocess.run([sys.executable, integration_path, "--preflight"])
        if result.returncode != 0:
            print("⚠️  Preflight diagnostics reported issues.")
        else:
            print("✅ Preflight diagnostics passed.")
    else:
        print("⚠️  Integration diagnostics script not found.")


def run_server_with_supervisor(server_file, max_restarts=5, restart_delay=3):
    """Run the server with auto-restart and supervisor logic, with error detection."""
    restarts = 0
    delay = restart_delay
    last_error = None
    while restarts < max_restarts:
        print(
            f"🟢 [Supervisor] Launching server (attempt {restarts+1}/"
            f"{max_restarts})..."
        )
        start_time = time.time()
        proc = subprocess.Popen([sys.executable, server_file], stderr=subprocess.PIPE)
        try:
            _, stderr = proc.communicate()
            exit_code = proc.returncode
            run_time = time.time() - start_time
            if exit_code == 0:
                print("✅ Server exited cleanly.")
                return 0
            else:
                # If server fails in <2s, treat as unrecoverable
                if run_time < 2:
                    print(
                        f"❌ Server failed immediately (exit {exit_code}). Not retrying."
                    )
                    if stderr:
                        print("--- Server error output ---")
                        print(stderr.decode(errors="ignore")[-500:])
                    print(
                        "ℹ️  Run diagnostics with: python ai/tests/aios_vscode_integration.py --preflight"
                    )
                    return exit_code
                print(
                    f"⚠️  Server exited with code {exit_code} after {run_time:.1f}s. "
                    f"Restarting in {delay}s..."
                )
                if stderr:
                    print("--- Server error output ---")
                    print(stderr.decode(errors="ignore")[-500:])
                last_error = stderr.decode(errors="ignore") if stderr else None
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user (supervisor exiting)")
            proc.terminate()
            return 0
        except Exception as e:
            print(f"❌ Supervisor error: {e}")
            proc.terminate()
        restarts += 1
        time.sleep(delay)
        delay = min(delay * 2, 60)  # Exponential backoff, max 60s
    print("❌ Max restart attempts reached. Supervisor exiting.")
    if last_error:
        print("--- Last server error output ---")
        print(last_error[-500:])
    print(
        "ℹ️  Run diagnostics with: python ai/tests/aios_vscode_integration.py --preflight"
    )
    return 1


def main():
    print("🚀 Starting AIOS VSCode Integration Server...")

    # Ensure venv is activated or activate if possible
    venv_path = os.path.join(os.path.dirname(__file__), "venv")
    if not os.environ.get("VIRTUAL_ENV"):
        # Not in venv, try to activate or run setup
        if not os.path.exists(venv_path):
            print(
                "[AIOS] No venv found. " "Running setup_env.py to create environment..."
            )
            subprocess.check_call([sys.executable, "setup_env.py"])
        # Relaunch script in venv
        if os.name == "nt":
            python_bin = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            python_bin = os.path.join(venv_path, "bin", "python")
        print(f"[AIOS] Relaunching under venv: {python_bin}")
        os.execv(python_bin, [python_bin] + sys.argv)

    # Find the server file
    server_file = find_server_file()
    if not server_file:
        print("❌ Server file not found: aios_vscode_integration_server.py")
        print(
            "ℹ️  Run diagnostics with: "
            "python ai/tests/aios_vscode_integration.py --preflight"
        )
        return 1

    # Optionally run preflight diagnostics
    run_preflight_diagnostics()

    # Run with supervisor/auto-restart logic
    return run_server_with_supervisor(server_file)


if __name__ == "__main__":
    exit(main())
