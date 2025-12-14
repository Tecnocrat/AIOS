"""
AINLP Kernel Package
===================

This package implements the core AINLP kernel with recursive background
processing capabilities and context allocation systems.
"""

<<<<<<< HEAD
from .ainlp_kernel import (
    AINLPKernel,
    get_ainlp_kernel,
    initialize_ainlp_kernel,
    shutdown_ainlp_kernel,
)
from .tooling.recursive_tooling import (
    RecursiveBackgroundProcessor,
    get_kernel_processor,
    initialize_kernel_tooling,
    shutdown_kernel_tooling,
)

__all__ = [
    "AINLPKernel",
    "get_ainlp_kernel",
    "initialize_ainlp_kernel",
    "shutdown_ainlp_kernel",
    "RecursiveBackgroundProcessor",
    "get_kernel_processor",
    "initialize_kernel_tooling",
    "shutdown_kernel_tooling",
=======
from .ainlp_kernel import (AINLPKernel, get_ainlp_kernel,
                           initialize_ainlp_kernel, shutdown_ainlp_kernel)
from .tooling.recursive_tooling import (RecursiveBackgroundProcessor,
                                        get_kernel_processor,
                                        initialize_kernel_tooling,
                                        shutdown_kernel_tooling)

__all__ = [
    'AINLPKernel',
    'get_ainlp_kernel',
    'initialize_ainlp_kernel',
    'shutdown_ainlp_kernel',
    'RecursiveBackgroundProcessor',
    'get_kernel_processor',
    'initialize_kernel_tooling',
    'shutdown_kernel_tooling'
>>>>>>> origin/OS0.6.2.grok
]
