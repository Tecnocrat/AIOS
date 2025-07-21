"""
UX endpoints: /ux/onboarding, /ux/help, /ux/chat-format
"""

from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter

router = APIRouter()


@router.get("/ux/onboarding")
async def ux_onboarding():
    steps = [
        "Install AIOS VSCode extension",
        "Configure private settings",
        "Start chat with @aios",
        "Test context persistence",
        "Explore AIOS commands",
    ]
    return {
        "onboarding_steps": steps,
        "timestamp": datetime.now().isoformat(),
        "note": "Replace with real onboarding wizard logic.",
    }


@router.get("/ux/help")
async def ux_help():
    help_topics = [
        "Extension not loading",
        "Context not persisting",
        "AIOS commands missing",
        "Settings not applied",
        "How to run diagnostics",
    ]
    return {
        "help_topics": help_topics,
        "timestamp": datetime.now().isoformat(),
        "note": "Replace with real help and troubleshooting logic.",
    }


@router.post("/ux/chat-format")
async def ux_chat_format(request: Dict[str, Any]):
    message = request.get("message", "")
    formatted = f"**AIOS:** {message}"
    suggestions = [
        "Show code snippet",
        "Suggest improvement",
        "Explain architecture",
    ]
    return {
        "formatted_message": formatted,
        "suggestions": suggestions,
        "timestamp": datetime.now().isoformat(),
        "note": "Replace with real chat formatting and UX logic.",
    }
