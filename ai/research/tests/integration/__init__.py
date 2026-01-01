"""
AIOS Integration Tests Package

Tests for Phase 10 library ingestion infrastructure:
- AI agent bridges (Gemini, Ollama)
- Library code generation loop
- Paradigm extraction engine
- Complete ingestion-to-generation cycle

All tests generate tachyonic metadata on execution.
Orchestration available via integration_test_orchestrator.py
"""

__version__ = "1.0.0"

__all__ = [
    "test_gemini_bridge",
    "test_library_generation",
    "test_ollama_bridge",
    "test_paradigm_extraction",
    "integration_test_orchestrator",
]
