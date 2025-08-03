"""
Request/Response logging middleware for AIOS VSCode Integration Server
"""

from fastapi import Request

from .debug_manager import _debug_manager


async def log_requests(request: Request, call_next):
    body = await request.body()
    _debug_manager.log_request(request.url.path, body.decode("utf-8"))
    response = await call_next(request)
    return response
