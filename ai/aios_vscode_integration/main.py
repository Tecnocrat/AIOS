"""
Entrypoint for AIOS VSCode Integration Server

AINLP Dendritic Paradigm Integration:
- All endpoints, handlers, and bridge modules are documented as dendritic
  stubs.
- These stubs are designed for extensibility, allowing future AI neurons
(logic modules, models, or protocols) to connect and evolve the system.
- Documentation in markdown and JSON ensures traceability and future ingestion
for AINLP-driven refactorization.

Logic Preservation Protocols:
- All injected dendrites (intent_handlers, bridge, debug_manager, models) are
registered in app.state or as FastAPI routers.
- Each dendrite is documented with its logic path and integration point for
future neuron connection.
- All changes are referenced in UPGRADE_PATH.md and
VSCODE_INTEGRATION_COMPLETE.md for architecture traceability.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .services import debug_manager
from .endpoints.ai_endpoints import (
    AIOSIntentDispatcher,
    generate_aios_response,
)
from .endpoints import (
    ai_endpoints,
    development_endpoints,
    system_endpoints,
    ux_endpoints,
)

app = FastAPI(
    title="AIOS VSCode Integration API",
    description="Bridge between VSCode extension and AIOS cellular ecosystem",
    version="0.4.0",
)


# Consolidated middleware functionality (from middleware.py)
async def log_requests(request: Request, call_next):
    """
    Logs incoming HTTP requests and their bodies using the debug manager.
    Passes the request to the next middleware or endpoint and returns
    the response.
    """
    body = await request.body()
    debug_manager._debug_manager.log_request(
        request.url.path, body.decode("utf-8")
    )
    response = await call_next(request)
    return response


@app.on_event("startup")
def on_startup():
    debug_manager._debug_manager.log_request(
        "startup", {"message": "API server started"}
    )
    # Register intent dispatcher dendrite for AINLP
    app.state.aios_intent_dispatcher = AIOSIntentDispatcher()
    # Register other dendritic stubs for future neuron connection
    app.state.debug_manager = debug_manager
    app.state.models = models


@app.on_event("shutdown")
def on_shutdown():
    debug_manager._debug_manager.log_request(
        "shutdown", {"message": "API server stopped"}
    )


@app.get("/debug")
def get_debug():
    """
    Returns recent debug info for AINLP diagnostics and inspection.
    """
    return debug_manager._debug_manager.get_debug_info()


@app.post("/intent")
def recognize_intent(request: dict):
    """
    Recognize intent from incoming message and context using AINLP dispatcher
    dendrite.
    """
    message = request.get("message", "")
    context = request.get("context", {})
    response = generate_aios_response(message, context)
    return {"response": response}

# Enable CORS for VSCode extension


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register consolidated middleware
app.middleware("http")(log_requests)

# Include routers from consolidated endpoint modules
app.include_router(system_endpoints.router, prefix="/system",
                   tags=["system"])
app.include_router(development_endpoints.router, prefix="/dev",
                   tags=["development"])
app.include_router(ai_endpoints.router, prefix="/ai", tags=["ai"])
app.include_router(ux_endpoints.router, prefix="/ux", tags=["ux"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="localhost",
        port=8080,
        log_level="info",
        reload=False
    )
