"""
DebugManager for runtime inspection in AIOS
"""

from datetime import datetime


class DebugManager:
    def __init__(self):
        self.requests = []
        self.handlers = []
        self.errors = []

    def log_request(self, endpoint, data):
        self.requests.append(
            {
                "timestamp": datetime.now().isoformat(),
                "endpoint": endpoint,
                "data": data,
            }
        )
        if len(self.requests) > 20:
            self.requests.pop(0)

    def log_handler(self, handler_name, message):
        self.handlers.append(
            {
                "timestamp": datetime.now().isoformat(),
                "handler": handler_name,
                "message": message,
            }
        )
        if len(self.handlers) > 20:
            self.handlers.pop(0)

    def log_error(self, error):
        self.errors.append(
            {
                "timestamp": datetime.now().isoformat(),
                "error": str(error),
            }
        )
        if len(self.errors) > 20:
            self.errors.pop(0)

    def get_debug_info(self):
        return {
            "requests": self.requests,
            "handlers": self.handlers,
            "errors": self.errors,
        }


_debug_manager = DebugManager()
