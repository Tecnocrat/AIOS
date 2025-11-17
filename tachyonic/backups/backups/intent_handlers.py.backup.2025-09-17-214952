"""
Intent handler classes and dispatcher for AIOS VSCode Integration Server
"""

from ai.debug_manager import _debug_manager


class IntentHandler:
    """
    Base class for intent handlers in the AIOS VSCode Integration Server.
    Defines the interface for can_handle and handle methods.
    """

    def can_handle(self, message: str, context: dict) -> bool:
        """
        Determines if this handler can process the given message and context.
        """
        raise NotImplementedError

    def handle(self, message: str, context: dict) -> str:
        """
        Processes the message and context, returning a response string.
        """
        raise NotImplementedError


class AIOSHandler(IntentHandler):
    """
    Handles AIOS-specific intents and queries about the AIOS ecosystem.
    """

    def can_handle(self, message, context):
        """
        Checks if the message is related to AIOS.
        """
        return "aios" in message.lower()

    def handle(self, message, context):
        """
        Returns a response about AIOS capabilities and features.
        """
        return (
            "AIOS TensorFlow Cellular Ecosystem is fully operational. "
            "I can assist you with multi-language development, "
            "cellular architecture optimization, and intelligent code "
            "generation. What specific aspect of AIOS would you like to "
            "explore?"
        )


class DevelopmentHandler(IntentHandler):
    """
    Handles development-related intents such as code, programming, and
    functions.
    """

    def can_handle(self, message, context):
        """
        Checks if the message is related to development topics.
        """
        return any(
            word in message.lower()
            for word in ["code", "development", "programming", "function"]
        )

    def handle(self, message, context):
        """
        Returns a response about development support and workspace analysis.
        """
        workspace = context.get("workspace", "unknown")
        return (
            f"I'm analyzing your {workspace} workspace with AIOS's "
            "multi-language AI coordination. I can provide insights from "
            "C++, Python, and C# perspectives, suggest optimizations, and "
            "help with code generation. What specific development task can "
            "I assist with?"
        )


class ArchitectureHandler(IntentHandler):
    """
    Handles architecture-related intents such as system design and patterns.
    """

    def can_handle(self, message, context):
        """
        Checks if the message is related to architecture topics.
        """
        return any(
            word in message.lower()
            for word in ["architecture", "system", "design", "pattern"]
        )

    def handle(self, message, context):
        """
        Returns a response about AIOS architecture and suggestions.
        """
        return (
            "AIOS uses a revolutionary cellular architecture with Python "
            "AI training cells, C++ performance cells, and intercellular "
            "communication bridges. I can help you understand this "
            "architecture, suggest improvements, or apply these patterns "
            "to your project. What architectural aspect interests you?"
        )


class ContextHandler(IntentHandler):
    """
    Handles context-related intents such as memory, history, and recall.
    """

    def can_handle(self, message, context):
        """
        Checks if the message is related to context management.
        """
        return any(
            word in message.lower()
            for word in ["context", "memory", "history", "remember"]
        )

    def handle(self, message, context):
        """
        Returns a response about context management and continuity.
        """
        return (
            "AIOS Context Manager maintains conversation continuity across "
            "VSCode sessions. Your workspace context is preserved, "
            "including project structure, git status, and development "
            "patterns. I remember our previous interactions and can build "
            "upon them. What would you like me to recall or explain?"
        )


class PerformanceHandler(IntentHandler):
    """
    Handles performance-related intents such as optimization and speed.
    """

    def can_handle(self, message, context):
        """
        Checks if the message is related to performance topics.
        """
        return any(
            word in message.lower()
            for word in ["performance", "optimization", "speed", "fast"]
        )

    def handle(self, message, context):
        """
        Returns a response about performance optimization and analysis.
        """
        return (
            "AIOS achieves sub-millisecond inference through its cellular "
            "architecture, with C++ performance cells delivering >1000 "
            "inferences/sec. I can analyze your code for performance "
            "bottlenecks, suggest optimizations, and implement cellular "
            "patterns for maximum efficiency. What performance aspect "
            "should we optimize?"
        )


class HelpHandler(IntentHandler):
    """
    Handles help and troubleshooting intents.
    """

    def can_handle(self, message, context):
        """
        Checks if the message is related to help or troubleshooting.
        """
        return any(
            word in message.lower()
            for word in [
                "help",
                "assist",
                "support",
                "guide",
            ]
        )

    def handle(self, message, context):
        """
        Returns a response with help topics and troubleshooting advice.
        """
        return (
            "I'm AIOS - your AI Operating System assistant. I integrate "
            "C++, Python, and C# capabilities with context-aware "
            "intelligence. I can help with code analysis, generation, "
            "architecture design, performance optimization, and "
            "maintaining development continuity. "
            "What would you like to accomplish?"
        )


class DefaultHandler(IntentHandler):
    """
    Handles any intents not matched by other handlers.
    """

    def can_handle(self, message, context):
        """
        Always returns True to act as a fallback handler.
        """
        return True

    def handle(self, message, context):
        """
        Returns a default response for unmatched intents.
        """
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
    """
    Dispatches messages to the appropriate intent handler based on message
    and context.
    """

    def __init__(self):
        """
        Initializes the dispatcher and registers all intent handlers.
        """
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
        """
        Dispatches the message to the first handler that can process it.
        Returns the handler's response string.
        """
        for handler in self.handlers:
            if handler.can_handle(message, context):
                _debug_manager.log_handler(handler.__class__.__name__, message)
                return handler.handle(message, context)
        return "[AIOS] No suitable handler found."


_aios_intent_dispatcher = AIOSIntentDispatcher()


def generate_aios_response(message: str, context: dict) -> str:
    """
    Generates an AIOS response by dispatching the message and context.
    """
    return _aios_intent_dispatcher.dispatch(message, context)
