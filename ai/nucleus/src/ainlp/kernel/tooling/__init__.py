"""
AINLP Kernel Tooling Package
============================

This package contains the recursive background processing tooling
for the AINLP kernel system.
"""

<<<<<<< HEAD
from .recursive_tooling import (
    RecursiveBackgroundProcessor,
    get_kernel_processor,
    initialize_kernel_tooling,
    shutdown_kernel_tooling,
)

__all__ = [
    "RecursiveBackgroundProcessor",
    "get_kernel_processor",
    "initialize_kernel_tooling",
    "shutdown_kernel_tooling",
=======
from .recursive_tooling import (RecursiveBackgroundProcessor,
                                get_kernel_processor,
                                initialize_kernel_tooling,
                                shutdown_kernel_tooling)

__all__ = [
    'RecursiveBackgroundProcessor',
    'get_kernel_processor',
    'initialize_kernel_tooling',
    'shutdown_kernel_tooling'
>>>>>>> origin/OS0.6.2.grok
]
