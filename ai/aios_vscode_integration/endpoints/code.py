"""
Code endpoints: /code/review, /code/refactor
"""

from datetime import datetime

from fastapi import APIRouter

from ..models import CodeRefactorRequest, CodeReviewRequest

router = APIRouter()


@router.post("/code/review")
async def code_review(request: CodeReviewRequest):
    review = (
        f"Review for {request.language} code: " "Looks good. Consider best practices."
    )
    return {
        "review": review,
        "suggestions": [
            "Use consistent naming",
            "Add docstrings",
            "Optimize imports",
        ],
        "confidence": 0.8,
        "timestamp": datetime.now().isoformat(),
    }


@router.post("/code/refactor")
async def code_refactor(request: CodeRefactorRequest):
    refactored_code = request.code
    suggestions = [
        "Extract functions",
        "Simplify logic",
        "Remove unused variables",
    ]
    return {
        "refactored_code": refactored_code,
        "suggestions": suggestions,
        "confidence": 0.75,
        "timestamp": datetime.now().isoformat(),
    }
