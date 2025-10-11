"""
NLP package for AIOS.

Provides NLP core classes and functions.

Baselayer integration: AINLP logical hooks for extensibility.
"""

from .nlp_core import NLPManager
__all__ = ["NLPManager"]

# AINLP.loader [latent:confidence_score] (auto.AINLP.class)
#   Original code (F401: 'confidence' missing in NLPManager output):
#   # result = await nlp_manager.process(text)
#   # confidence = result.get('confidence', None)
#   Reason: Baselayer does not yet provide confidence scoring.
#   AINLP.mind: Integrate confidence scoring in NLPManager
#   for future transformer/intent models.
