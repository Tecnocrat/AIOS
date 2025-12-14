"""
UX endpoints for AIOS VSCode Integration Server
Consolidated from ux.py for logic densification
AINLP dendritic paradigm: Enhanced user experience and guidance
"""

from datetime import datetime

from fastapi import APIRouter

from services.debug_manager import _debug_manager
from services.fractal_cache_manager import _fractal_cache_manager

router = APIRouter()


@router.get("/ux/onboarding")
async def ux_onboarding():
    """
    Provides onboarding steps for new AIOS VSCode extension users.
    Enhanced dendritic implementation with intelligent guidance
    Returns a list of steps, timestamp, and contextual help.
    """
    try:
        # Check cache for onboarding steps
        cache_key = "ux_onboarding"
        cached_onboarding = await _fractal_cache_manager.get_cached(cache_key)

        if cached_onboarding:
            return cached_onboarding

        # Enhanced onboarding with AINLP integration
        steps = [
            "Install AIOS VSCode extension from marketplace",
            "Configure private settings and API keys",
            "Start chat with @aios in any file",
            "Test context persistence across sessions",
            "Explore AIOS commands: /save, /refresh, /status",
            "Try code generation and analysis features",
            "Set up workspace-specific configurations",
        ]

        onboarding_guide = {
            "onboarding_steps": steps,
            "timestamp": datetime.now().isoformat(),
            "estimated_time": "10-15 minutes",
            "prerequisites": [
                "VSCode 1.70+ installed",
                "Python 3.8+ available",
                "Internet connection for AI features",
            ],
            "next_steps": [
                "Complete workspace analysis",
                "Run initial health check",
                "Configure personal preferences",
            ],
            "note": "Enhanced onboarding with AINLP guidance system",
        }

        # Cache the onboarding guide
<<<<<<< HEAD
        await _fractal_cache_manager.set_cached(cache_key, onboarding_guide, ttl=3600)
=======
        await _fractal_cache_manager.set_cached(
            cache_key, onboarding_guide, ttl=3600
        )
>>>>>>> origin/OS0.6.2.grok

        return onboarding_guide

    except Exception as e:
        _debug_manager.log_error(e, {"endpoint": "ux_onboarding"})
        return {
            "onboarding_steps": ["Basic setup required"],
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "note": "Onboarding guide unavailable",
        }


@router.get("/ux/help")
async def ux_help():
    """
    Returns help topics and troubleshooting guidance for AIOS users.
    Enhanced dendritic implementation with intelligent assistance
    Includes a list of topics, timestamp, and interactive help.
    """
    try:
        # Check cache for help topics
        cache_key = "ux_help"
        cached_help = await _fractal_cache_manager.get_cached(cache_key)

        if cached_help:
            return cached_help

        # Enhanced help system with categorization
        help_topics = {
            "getting_started": [
                "Extension installation and setup",
                "First chat with AIOS",
                "Understanding context persistence",
                "Basic commands and shortcuts",
            ],
            "troubleshooting": [
                "Extension not loading or responding",
                "Context not persisting between sessions",
                "AIOS commands not appearing",
                "Settings not being applied",
                "Performance issues and optimization",
            ],
            "features": [
                "Code generation and analysis",
                "Architecture visualization",
                "Performance optimization",
                "Multi-language support (C++, Python, C#)",
                "Cellular ecosystem integration",
            ],
            "advanced": [
                "Custom intent handlers",
                "Workspace configuration",
                "Integration with external tools",
                "AINLP paradigm customization",
            ],
        }

        help_guide = {
            "help_topics": help_topics,
            "timestamp": datetime.now().isoformat(),
            "quick_actions": [
                "Run '/status' to check system health",
                "Use '/refresh' to update context",
                "Try '/save' to persist current state",
            ],
<<<<<<< HEAD
            "contact_support": ("Report issues via GitHub or extension feedback"),
=======
            "contact_support": (
                "Report issues via GitHub or extension feedback"
            ),
>>>>>>> origin/OS0.6.2.grok
            "note": "Enhanced help system with fractal intelligence",
        }

        # Cache the help guide
<<<<<<< HEAD
        await _fractal_cache_manager.set_cached(cache_key, help_guide, ttl=1800)
=======
        await _fractal_cache_manager.set_cached(
            cache_key, help_guide, ttl=1800
        )
>>>>>>> origin/OS0.6.2.grok

        return help_guide

    except Exception as e:
        _debug_manager.log_error(e, {"endpoint": "ux_help"})
        return {
            "help_topics": ["Basic assistance available"],
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "note": "Help system temporarily unavailable",
        }


@router.get("/ux/tutorial")
async def ux_tutorial():
    """
    Interactive tutorial for AIOS features
    Dendritic expansion: Tutorial system with adaptive learning
    """
    try:
        # Check cache for tutorial
        cache_key = "ux_tutorial"
        cached_tutorial = await _fractal_cache_manager.get_cached(cache_key)

        if cached_tutorial:
            return cached_tutorial

        # Enhanced tutorial with modules
        tutorial_modules = [
            {
                "title": "Introduction to AIOS",
                "duration": "5 minutes",
                "steps": [
                    "Understand cellular architecture",
                    "Learn about multi-language integration",
                    "Explore context persistence",
                ],
                "interactive": True,
            },
            {
                "title": "Code Analysis & Generation",
                "duration": "10 minutes",
                "steps": [
                    "Code review and suggestions",
                    "Automated refactoring",
                    "Performance optimization",
                ],
                "interactive": True,
            },
            {
                "title": "Architecture Visualization",
                "duration": "8 minutes",
                "steps": [
                    "Project structure analysis",
                    "Dependency mapping",
                    "Integration visualization",
                ],
                "interactive": True,
            },
        ]

        tutorial_guide = {
            "tutorial_modules": tutorial_modules,
            "timestamp": datetime.now().isoformat(),
            "total_duration": "23 minutes",
            "difficulty": "Beginner to Intermediate",
            "prerequisites": ["Basic programming knowledge"],
            "completion_rewards": [
                "Master AIOS features",
                "Optimize development workflow",
                "Unlock advanced capabilities",
            ],
            "note": "Adaptive tutorial with AINLP personalization",
        }

        # Cache the tutorial
<<<<<<< HEAD
        await _fractal_cache_manager.set_cached(cache_key, tutorial_guide, ttl=3600)
=======
        await _fractal_cache_manager.set_cached(
            cache_key, tutorial_guide, ttl=3600
        )
>>>>>>> origin/OS0.6.2.grok

        return tutorial_guide

    except Exception as e:
        _debug_manager.log_error(e, {"endpoint": "ux_tutorial"})
        return {
            "tutorial_modules": ["Basic tutorial available"],
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "note": "Tutorial system unavailable",
        }


@router.get("/ux/shortcuts")
async def ux_shortcuts():
    """
    Keyboard shortcuts and quick commands for AIOS
    Dendritic expansion: Shortcut management and customization
    """
    try:
        # Check cache for shortcuts
        cache_key = "ux_shortcuts"
        cached_shortcuts = await _fractal_cache_manager.get_cached(cache_key)

        if cached_shortcuts:
            return cached_shortcuts

        # Enhanced shortcuts with categories
        shortcuts = {
            "basic_commands": {
                "@aios": "Start chat with AIOS",
                "/status": "Check system health",
                "/save": "Persist current context",
                "/refresh": "Update workspace context",
            },
            "code_operations": {
                "/review": "Request code review",
                "/refactor": "Suggest refactoring",
                "/optimize": "Performance optimization",
                "/generate": "Code generation",
            },
            "analysis_commands": {
                "/analyze": "Architecture analysis",
                "/visualize": "Integration visualization",
                "/diagnostics": "System diagnostics",
                "/health": "Component health check",
            },
            "customization": {
                "/config": "Workspace configuration",
                "/preferences": "User preferences",
                "/shortcuts": "Customize shortcuts",
                "/integrations": "External tool integration",
            },
        }

        shortcuts_guide = {
            "shortcuts": shortcuts,
            "timestamp": datetime.now().isoformat(),
            "customization_available": True,
            "voice_commands": "Supported for accessibility",
            "note": "Comprehensive shortcut system with customization",
        }

        # Cache the shortcuts
<<<<<<< HEAD
        await _fractal_cache_manager.set_cached(cache_key, shortcuts_guide, ttl=7200)
=======
        await _fractal_cache_manager.set_cached(
            cache_key, shortcuts_guide, ttl=7200
        )
>>>>>>> origin/OS0.6.2.grok

        return shortcuts_guide

    except Exception as e:
        _debug_manager.log_error(e, {"endpoint": "ux_shortcuts"})
        return {
            "shortcuts": {"basic": {"@aios": "Start AIOS chat"}},
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "note": "Shortcuts unavailable",
        }


@router.get("/ux/feedback")
async def ux_feedback():
    """
    Collect user feedback and suggestions
    Dendritic expansion: Feedback analysis and continuous improvement
    """
    try:
        # Check cache for feedback form
        cache_key = "ux_feedback"
        cached_feedback = await _fractal_cache_manager.get_cached(cache_key)

        if cached_feedback:
            return cached_feedback

        # Enhanced feedback system
        feedback_form = {
            "categories": [
                "Feature Request",
                "Bug Report",
                "Performance Issue",
                "User Experience",
                "Documentation",
                "Integration",
            ],
            "rating_scales": {
                "satisfaction": [
<<<<<<< HEAD
                    "Very Dissatisfied",
                    "Dissatisfied",
                    "Neutral",
                    "Satisfied",
                    "Very Satisfied",
                ],
                "ease_of_use": [
                    "Very Difficult",
                    "Difficult",
                    "Moderate",
                    "Easy",
                    "Very Easy",
                ],
                "performance": ["Very Slow", "Slow", "Moderate", "Fast", "Very Fast"],
=======
                    "Very Dissatisfied", "Dissatisfied", "Neutral",
                    "Satisfied", "Very Satisfied"
                ],
                "ease_of_use": [
                    "Very Difficult", "Difficult", "Moderate",
                    "Easy", "Very Easy"
                ],
                "performance": [
                    "Very Slow", "Slow", "Moderate", "Fast", "Very Fast"
                ],
>>>>>>> origin/OS0.6.2.grok
            },
            "timestamp": datetime.now().isoformat(),
            "anonymous_submission": True,
            "follow_up_available": True,
            "note": "Feedback drives AINLP paradigm evolution",
        }

        # Cache the feedback form
<<<<<<< HEAD
        await _fractal_cache_manager.set_cached(cache_key, feedback_form, ttl=3600)
=======
        await _fractal_cache_manager.set_cached(
            cache_key, feedback_form, ttl=3600
        )
>>>>>>> origin/OS0.6.2.grok

        return feedback_form

    except Exception as e:
        _debug_manager.log_error(e, {"endpoint": "ux_feedback"})
        return {
            "categories": ["General Feedback"],
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "note": "Feedback system unavailable",
        }
