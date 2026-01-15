"""
AIOS Membrane Module - Boundary Interfaces

The membrane serves as the intelligent boundary between AIOS and external systems,
handling all communication protocols, transport mechanisms, and integrations.

Architecture Components:
    - mcp_server/: Model Context Protocol server implementation
    - protocols/: AICP and other communication protocols  
    - transport/: Inter-cellular and tachyonic transport bridges
    - integrations/: External system connectors
    - communication/: Universal message bus and interfaces

AINLP Pattern: Cellular membrane - selective permeability for information flow
Phase: 31.9.6 Agentic Architecture
"""

# Lazy imports to avoid circular dependencies during module initialization
def get_mcp_server():
    from .mcp_server.server import AIOSMCPServer
    return AIOSMCPServer

def get_universal_bus():
    from .communication.universal_bus import UniversalCommunicationBus
    return UniversalCommunicationBus

__all__ = [
    'get_mcp_server',
    'get_universal_bus', 
]

__version__ = "1.0.0"
__ainlp_component__ = "membrane"
