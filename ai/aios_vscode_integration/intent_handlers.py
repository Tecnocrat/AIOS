"""
Intent handler classes and dispatcher for AIOS VSCode Integration Server
"""

from typing import Any, Dict

from .debug_manager import _debug_manager


class IntentHandler:
    def can_handle(self, message: str, context: dict) -> bool:
        raise NotImplementedError

    def handle(self, message: str, context: dict) -> str:
        raise NotImplementedError


class AIOSHandler(IntentHandler):
    def can_handle(self, message, context):
        return "aios" in message.lower()

    def handle(self, message, context):
        return (
            "AIOS TensorFlow Cellular Ecosystem is fully operational. "
            "I can assist you with multi-language development, "
            "cellular architecture optimization, and intelligent code "
            "generation. What specific aspect of AIOS would you like to "
            "explore?"
        )


class DevelopmentHandler(IntentHandler):
    def can_handle(self, message, context):
        return any(
            word in message.lower()
            for word in ["code", "development", "programming", "function"]
        )

    def handle(self, message, context):
        workspace = context.get("workspace", "unknown")
        return (
            f"I'm analyzing your {workspace} workspace with AIOS's "
            "multi-language AI coordination. I can provide insights from "
            "C++, Python, and C# perspectives, suggest optimizations, and "
            "help with code generation. What specific development task can "
            "I assist with?"
        )


class ArchitectureHandler(IntentHandler):
    def can_handle(self, message, context):
        return any(
            word in message.lower()
            for word in ["architecture", "system", "design", "pattern"]
        )

    def handle(self, message, context):
        return (
            "AIOS uses a revolutionary cellular architecture with Python "
            "AI training cells, C++ performance cells, and intercellular "
            "communication bridges. I can help you understand this "
            "architecture, suggest improvements, or apply these patterns "
            "to your project. What architectural aspect interests you?"
        )


class ContextHandler(IntentHandler):
    def can_handle(self, message, context):
        return any(
            word in message.lower()
            for word in ["context", "memory", "history", "remember"]
        )

    def handle(self, message, context):
        return (
            "AIOS Context Manager maintains conversation continuity across "
            "VSCode sessions. Your workspace context is preserved, "
            "including project structure, git status, and development "
            "patterns. I remember our previous interactions and can build "
            "upon them. What would you like me to recall or explain?"
        )


class PerformanceHandler(IntentHandler):
    def can_handle(self, message, context):
        return any(
            word in message.lower()
            for word in ["performance", "optimization", "speed", "fast"]
        )

    def handle(self, message, context):
        return (
            "AIOS achieves sub-millisecond inference through its cellular "
            "architecture, with C++ performance cells delivering >1000 "
            "inferences/sec. I can analyze your code for performance "
            "bottlenecks, suggest optimizations, and implement cellular "
            "patterns for maximum efficiency. What performance aspect "
            "should we optimize?"
        )


class HelpHandler(IntentHandler):
    def can_handle(self, message, context):
        return any(
            word in message.lower() for word in ["help", "assist", "support", "guide"]
        )

    def handle(self, message, context):
        return (
            "I'm AIOS - your AI Operating System assistant. I integrate "
            "C++, Python, and C# capabilities with context-aware "
            "intelligence. I can help with code analysis, generation, "
            "architecture design, performance optimization, and "
            "maintaining development continuity. What would you like to "
            "accomplish?"
        )


class DefaultHandler(IntentHandler):
    def can_handle(self, message, context):
        return True

    def handle(self, message, context):
        workspace = context.get("workspace", "unknown")
        return (
            f"I understand you're asking about: '{message}'. As AIOS, I can "
            "provide multi-language analysis, intelligent code suggestions, "
            "and context-aware assistance. Based on your "
            f"{workspace} workspace, I can help with development tasks, "
            "architectural decisions, and optimization strategies. Could "
            "you provide more specific details about what you'd like to "
            "achieve?"
        )


class AIOSIntentDispatcher:
    def __init__(self):
        self.handlers = [
            AIOSHandler(),
            DevelopmentHandler(),
            ArchitectureHandler(),
            ContextHandler(),
            PerformanceHandler(),
            HelpHandler(),
            DefaultHandler(),
        ]

    def dispatch(self, message: str, context: dict) -> str:
        for handler in self.handlers:
            if handler.can_handle(message, context):
                _debug_manager.log_handler(handler.__class__.__name__, message)
                return handler.handle(message, context)
        return "[AIOS] No suitable handler found."


_aios_intent_dispatcher = AIOSIntentDispatcher()


def generate_aios_response(message: str, context: dict) -> str:
    return _aios_intent_dispatcher.dispatch(message, context)
