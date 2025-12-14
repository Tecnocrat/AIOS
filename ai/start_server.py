#!/usr/bin/env python3
"""
AIOS Server Startup Script
Simplified startup for the AIOS VSCode Integration Server
"""

import os
import subprocess
import sys
import time


def main():
    print("🚀 Starting AIOS VSCode Integration Server...")

    # We're already in the ai directory
    server_file = "aios_vscode_integration_server.py"

    if not os.path.exists(server_file):
        print(f"❌ Server file not found: {server_file}")
        return 1

    try:
        # Start the server (we're already in ai directory)
        print(f"📂 Working directory: {os.getcwd()}")
        print(f"🐍 Python executable: {sys.executable}")
        print(f"📄 Server file: {server_file}")
        print("🌐 Starting server on http://localhost:8080")
        print("-" * 50)

        # Run the server
        subprocess.run([sys.executable, server_file])

    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
