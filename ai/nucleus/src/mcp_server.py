# AINLP.loader [anchor:dev-path] (auto.AINLP.class)
#   Dev Path: MCP server entry point, imports protocol from core/integration/mcp.py
#   This file replaces aios_mcp_server.py for unified protocol integration.
#   AINLP.mind: Use this as the main entry for MCP-compliant AIOS server logic.

import json
import sys
import traceback
from datetime import UTC, datetime

from core.integration.mcp import MCPServer, Tool
from src.aios_core import AICore


def log_event(event_type, details):
    print(
        json.dumps(
            {
                "event": event_type,
                "details": details,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        ),
        file=sys.stderr,
    )


aios_core = AICore()


def analyze_code(params):
    log_event("analyzeCode_invoked", params)
    try:
        result = aios_core.process_natural_language(
            params.get("file"), params.get("context")
        )
        return {"result": result}
    except Exception as e:
        log_event("analyzeCode_error", traceback.format_exc())
        return {"error": str(e)}


def refactor_code(params):
    log_event("refactorCode_invoked", params)
    try:
        # Example: use update_learning for refactor logic
        result = aios_core.update_learning(params)
        return {"result": result}
    except Exception as e:
        log_event("refactorCode_error", traceback.format_exc())
        return {"error": str(e)}


def context_info(params):
    log_event("contextInfo_invoked", params)
    try:
        return {"context": aios_core.get_status()}
    except Exception as e:
        log_event("contextInfo_error", traceback.format_exc())
        return {"error": str(e)}


def quantum_diagnostics(params):
    log_event("quantumDiagnostics_invoked", params)
    try:
        # Example: use health_check for quantum diagnostics
        return {"quantum_status": aios_core.health_check()}
    except Exception as e:
        log_event("quantumDiagnostics_error", traceback.format_exc())
        return {"error": str(e)}


server = MCPServer()
server.register_tool(
    Tool("analyzeCode", analyze_code, description="AIOS code analysis")
)
server.register_tool(
    Tool("refactorCode", refactor_code, description="AIOS code refactor")
)
server.register_tool(
    Tool("contextInfo", context_info, description="AIOS context/state reporting")
)
server.register_tool(
    Tool("quantumDiagnostics", quantum_diagnostics, description="Quantum diagnostics")
)

if __name__ == "__main__":
    log_event("server_start", {"status": "initializing"})
    try:
        server.run_stdio()
    except Exception:
        log_event("server_fatal_error", traceback.format_exc())
        sys.exit(2)
