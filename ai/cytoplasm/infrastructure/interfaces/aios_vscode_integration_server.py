"""
AIOS VSCode Extension Integration Server (modular entrypoint)

This file is now a stub. All logic has been refactored into the
aios_vscode_integration package. To run the server, use the app
from aios_vscode_integration.main.
"""

import os
import sys

# Ensure the parent directory is in sys.path for robust import
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from aios_vscode_integration.main import app
except ImportError as e:
    raise ImportError(
        "\n".join(
            [
                "Could not import 'aios_vscode_integration.main'.",
                "Make sure you are running this script from the project root "
                "(e.g., 'python ai/aios_vscode_integration_server.py')",
                "and that the 'aios_vscode_integration' package exists in"
                " the 'ai' directory.",
                f"Original error: {e}",
            ]
        )
    ) from e

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="localhost",
        port=8080,
        log_level="info",
        reload=False,
    )
