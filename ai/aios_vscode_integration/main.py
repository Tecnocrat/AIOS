"""
Entrypoint for AIOS VSCode Integration Server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import debug_manager, intent_handlers, middleware, models
from .endpoints import architecture, automation, bridge, code, context, core, nlu, ux

app = FastAPI(
    title="AIOS VSCode Integration API",
    description="Bridge between VSCode extension and AIOS cellular ecosystem",
    version="0.4.0",
)

# Enable CORS for VSCode extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register middleware
app.middleware("http")(middleware.log_requests)

# Include routers from endpoint modules
app.include_router(core.router)
app.include_router(code.router)
app.include_router(architecture.router)
app.include_router(nlu.router)
app.include_router(bridge.router)
app.include_router(automation.router)
app.include_router(context.router)
app.include_router(ux.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080, log_level="info", reload=False)
