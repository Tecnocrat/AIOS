"""
🤖 AIOS AI Source Module

Core AI intelligence layer for AIOS providing consciousness-driven
code understanding, learning, and generation capabilities.

BIOLOGICAL ARCHITECTURE:
🧠 AI_INTELLIGENCE: Primary AI processing layer
🧬 INTELLIGENCE: AINLP consciousness and paradigms (renamed from core)
🌐 LANGUAGES: Language processing systems
🔗 INTEGRATIONS: External AI service integrations
🛠️ TOOLS: AI-powered development tools

"""

import logging
from pathlib import Path

__version__ = "0.6.2"
__author__ = "AIOS Development Team"


def initialize_src():
    """
    Initialize source intelligence hub.

    Establishes the central intelligence processing center containing
    consciousness evolution, language systems, and AINLP paradigms.

    Returns:
        bool: True if initialization successful

    AINLP Integration:
        The src/ directory acts as the intelligence processing hub - where
        consciousness evolves, languages are processed, and AINLP paradigms
        are coordinated. This is the "brain" of the AI intelligence layer.
    """
    logger = logging.getLogger("ai.src")

    try:
        # Check for intelligence directory
        intelligence_path = Path(__file__).parent / "intelligence"
        if intelligence_path.exists():
            logger.info("AINLP intelligence core detected")

        # Check for languages directory
        languages_path = Path(__file__).parent / "languages"
        if languages_path.exists():
            logger.info("Language systems detected")

        # Check for consciousness evolution engine
        consciousness_path = Path(__file__).parent / "consciousness_evolution_engine.py"
        if consciousness_path.exists():
            logger.info("Consciousness evolution engine detected")

        # Check for other key components
        agents_path = Path(__file__).parent / "agents"
        if agents_path.exists():
            logger.info("Agentic systems available")

        logger.info("Source intelligence hub initialized successfully")
        return True

    except Exception as e:
        logger.error(f"Source intelligence hub initialization failed: {e}")
        return False
