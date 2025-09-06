"""
AIOS Core Engine Package

The Core Engine provides foundational analysis tools, cellular intelligence systems,
and evolutionary assembler capabilities for the AIOS consciousness architecture.

Key Components:
- analysis_tools: Cellular intelligence diagnostics and enhancement systems
- bridges: Cross-system communication interfaces  
- core_systems: Fundamental AIOS core functionality
- evolutionary_assembler: Dynamic system evolution capabilities
"""

__version__ = "0.6.0"
__author__ = "AIOS Core Development Team"

# Core Engine Initialization
import sys
import os

# Add core directories to Python path for proper imports
CORE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CORE_DIR)

# Initialize core systems
def initialize_core_engine():
    """Initialize AIOS Core Engine systems"""
    try:
        from analysis_tools import initialize_analysis_tools
        from core_systems import initialize_core_systems
        
        initialize_analysis_tools()
        initialize_core_systems()
        return True
    except ImportError as e:
        print(f"Core Engine initialization warning: {e}")
        return False

# Auto-initialize when imported
_core_initialized = initialize_core_engine()
