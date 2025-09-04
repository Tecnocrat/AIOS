"""AIOS AI module source package.

Provides the main AI functionality for the AIOS system,
including natural language processing, predictive analytics, and
intelligent automation capabilities.
"""

from .aios_core import (
    AICore,
    get_ai_core,
    initialize_ai_core,
    start_ai_core,
    stop_ai_core,
)

# Optionally expose subsystems if needed:
# from .core.automation import AutomationManager
# from .core.learning import LearningManager
# from .core.integration.integration_bridge import IntegrationBridge
# from .core.nlp.nlp_core import NLPManager
# from .core.prediction import PredictionManager

__all__ = [
    "AICore",
    "get_ai_core",
    "initialize_ai_core",
    "start_ai_core",
    "stop_ai_core",
    # "AutomationManager",
    # "LearningManager",
    # "IntegrationBridge",
    # "NLPManager",
    # "PredictionManager",
]
