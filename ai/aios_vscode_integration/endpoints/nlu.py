"""
NLU endpoints: /nlu/intent
"""

from datetime import datetime

from fastapi import APIRouter

from ..models import NLUIntentRequest

router = APIRouter()


@router.post("/nlu/intent")
async def nlu_intent(request: NLUIntentRequest):
    """
    Analyzes the input message to determine the user's intent.
    Returns recognized intent, confidence score, context, and timestamp.
    """
    message = request.message.lower()
    if "refactor" in message:
        intent = "refactor-request"
        confidence = 0.9
    elif "review" in message:
        intent = "code-review-request"
        confidence = 0.85
    elif "architecture" in message:
        intent = "architecture-analysis-request"
        confidence = 0.8
    else:
        intent = "general-query"
        confidence = 0.6
    return {
        "recognized_intent": intent,
        "confidence": confidence,
        "context": request.context,
        "timestamp": datetime.now().isoformat(),
        "note": "Replace with AINLP/transformer-based NLU for production.",
    }
