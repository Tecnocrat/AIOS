"""
DebugManager for runtime inspection in AIOS VSCode Integration Server
"""

from datetime import datetime


class DebugManager:
    def __init__(self):
        self.recent_requests = []
        self.errors = []
        self.handler_matches = []

    def log_request(self, endpoint, data):
        self.recent_requests.append(
            {
                "timestamp": datetime.now().isoformat(),
                "endpoint": endpoint,
                "data": data,
            }
        )
        if len(self.recent_requests) > 20:
            self.recent_requests.pop(0)

    def log_error(self, error):
        self.errors.append(
            {
                "timestamp": datetime.now().isoformat(),
                "error": str(error),
            }
        )
        if len(self.errors) > 20:
            self.errors.pop(0)

    def log_handler(self, handler_name, message):
        self.handler_matches.append(
            {
                "timestamp": datetime.now().isoformat(),
                "handler": handler_name,
                "message": message,
            }
        )
        if len(self.handler_matches) > 20:
            self.handler_matches.pop(0)

    def get_debug_info(self):
        return {
            "recent_requests": self.recent_requests,
            "errors": self.errors,
            "handler_matches": self.handler_matches,
        }


_debug_manager = DebugManager()
