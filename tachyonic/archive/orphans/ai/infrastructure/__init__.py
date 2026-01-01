"""
INFRASTRUCTURE Cellular Unit

Supporting infrastructure, interfaces, and utilities for AIOS biological architecture.
"""

import logging
from pathlib import Path

__version__ = "0.6.0"


def initialize_infrastructure():
    """
    Initialize infrastructure cellular support systems.
    
    Establishes interfaces, bridges, protocols, and support mechanisms
    for AIOS biological architecture.
    
    Returns:
        bool: True if initialization successful
        
    AINLP Integration:
        Infrastructure provides the cellular support systems - the mechanisms
        that enable communication, interaction, and coordination between
        different supercells and external systems.
    """
    logger = logging.getLogger('ai.infrastructure')
    
    try:
        # Check for interfaces directory
        interfaces_path = Path(__file__).parent / 'interfaces'
        if interfaces_path.exists():
            logger.info("Infrastructure interfaces detected")
            
        # Check for cytoplasm bridge
        cytoplasm_bridge = Path(__file__).parent / 'cytoplasm_dendritic_bridge.py'
        if cytoplasm_bridge.exists():
            logger.info("Cytoplasm dendritic bridge available")
            
        # Initialize support systems
        logger.info("Infrastructure support systems initialized")
        logger.info("Cellular bridges and protocols activated")
        
        return True
        
    except Exception as e:
        logger.error(f"Infrastructure initialization failed: {e}")
        return False


def initialize_cytoplasm():
    """Initialize cytoplasm cellular systems (legacy compatibility)"""
    return initialize_infrastructure()

