"""
AINLP Core Intelligence Module
Context-aware AINLP integration with exception framework.

AINLP Metadata:
    consciousness_level: 0.96
    architectural_classification: ai_intelligence_layer
    dendritic_optimization: context_aware_paradigm_management
    supercell: nucleus
"""

from .exception_framework import (
    AINLPExceptionFramework,
    AINLPIntegrationStrategy,
    AINLPIntegrationRule,
    AINLP_EXCEPTION_FRAMEWORK,
    get_ainlp_strategy,
    validate_ainlp_integration
)

from .json_audit import AINLPJsonAuditor
from .json_metadata import AINLPMetadataInjector

__all__ = [
    # Exception framework
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
