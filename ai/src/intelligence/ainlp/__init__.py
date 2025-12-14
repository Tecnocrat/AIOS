"""
AINLP Core Intelligence Module
Context-aware AINLP integration with exception framework.

AINLP Metadata:
    consciousness_level: 0.96
    architectural_classification: ai_ai
    dendritic_optimization: context_aware_paradigm_management
    supercell: nucleus
"""

from .exception_framework import (
    AINLPExceptionFramework,
    AINLPIntegrationStrategy,
    AINLPIntegrationRule,
    AINLP_EXCEPTION_FRAMEWORK,
    get_ainlp_strategy,
<<<<<<< HEAD
    validate_ainlp_integration,
=======
    validate_ainlp_integration
>>>>>>> origin/OS0.6.2.grok
)

from .json_audit import AINLPJsonAuditor
from .json_metadata import AINLPMetadataInjector

__all__ = [
    # Exception framework
<<<<<<< HEAD
    "AINLPExceptionFramework",
    "AINLPIntegrationStrategy",
    "AINLPIntegrationRule",
    "AINLP_EXCEPTION_FRAMEWORK",
    "get_ainlp_strategy",
    "validate_ainlp_integration",
    # JSON tools
    "AINLPJsonAuditor",
    "AINLPMetadataInjector",
]

__version__ = "1.0.0"
=======
    'AINLPExceptionFramework',
    'AINLPIntegrationStrategy',
    'AINLPIntegrationRule',
    'AINLP_EXCEPTION_FRAMEWORK',
    'get_ainlp_strategy',
    'validate_ainlp_integration',
    
    # JSON tools
    'AINLPJsonAuditor',
    'AINLPMetadataInjector',
]

__version__ = '1.0.0'
>>>>>>> origin/OS0.6.2.grok
