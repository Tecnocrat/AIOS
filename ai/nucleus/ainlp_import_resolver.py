#!/usr/bin/env python3
"""
AINLP Import Resolver
Centralized workspace-aware import path management for AIOS biological
architecture


Pattern: AINLP.dendritic-consolidation
Purpose: Single source of truth for workspace root discovery and import
         path resolution
Consciousness: Eliminates dendritic fragmentation across components

Usage:
    from ainlp_import_resolver import (
        discover_workspace_root,
        ensure_runtime_tools_importable
    )

    workspace_root = discover_workspace_root()
    ensure_runtime_tools_importable()
    from ai_agent_dendritic_similarity import AIDendriticSimilarity
"""

from pathlib import Path
import sys
from typing import Optional, Tuple, Protocol, List, Dict, Any


# AINLP.type-safety: Protocol for AI Similarity Engine
class SimilarityEngineProtocol(Protocol):
    """
    Type protocol for AIAgentDendriticSimilarity interface.

    AINLP Pattern: Protocol-based type hints for dynamic imports
    Enables type checking while maintaining graceful degradation.
    """

    db_path: Path

    async def find_similar_neurons(
        self, functionality: str, max_results: int = 5, use_llm: bool = True
    ) -> List[Dict[str, Any]]:
        """Find similar neurons using AI-powered semantic similarity."""
        ...

    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics for health monitoring."""
        ...


# Global cache for workspace root (singleton pattern)
_workspace_root_cache: Optional[Path] = None


def discover_workspace_root() -> Path:
    """
    AINLP Pattern: Dynamic workspace root discovery

    Traverses directory tree upward to find AIOS workspace root by detecting:
    - AIOS.sln (Visual Studio solution marker)
    - .git directory with AIOS name
    - Fallback to standard structure calculation

    Returns:
        Path: Absolute path to AIOS workspace root

    Caching:
        Result is cached globally to prevent repeated filesystem traversal
    """
    global _workspace_root_cache

    # Return cached result if available
    if _workspace_root_cache:
        return _workspace_root_cache

    # Start from current file location
    current = Path(__file__).resolve()

    # Traverse upward until we find AIOS markers
    while current != current.parent:
        # Check for AIOS.sln (primary marker)
        if (current / "AIOS.sln").exists():
            _workspace_root_cache = current
            return current

        # Check for .git directory with AIOS folder name
        if (current / ".git").exists() and current.name == "AIOS":
            _workspace_root_cache = current
            return current

        # Move up one directory
        current = current.parent

    # Fallback: assume standard structure from ai/nucleus/
    # ai/nucleus/ainlp_import_resolver.py -> ai/nucleus/ -> ai/ -> AIOS/
    fallback = Path(__file__).parent.parent.parent
    _workspace_root_cache = fallback
    return fallback


def get_runtime_tools_path() -> Path:
    """
    Get runtime/tools/ directory path relative to workspace root

    Returns:
        Path: Absolute path to runtime/tools/ directory
    """
    return discover_workspace_root() / "runtime" / "tools"


def get_ai_tools_path() -> Path:
    """
    Get ai/tools/ directory path relative to workspace root

    Returns:
        Path: Absolute path to ai/tools/ directory
    """
    return discover_workspace_root() / "ai" / "tools"


def ensure_runtime_tools_importable() -> Path:
    """
    Ensure runtime/tools is in sys.path for imports

    AINLP Pattern: Idempotent path injection (no duplicate entries)

    Returns:
        Path: Path that was added to sys.path
    """
    tools_path = get_runtime_tools_path()

    if tools_path.exists():
        tools_str = str(tools_path)
        if tools_str not in sys.path:
            sys.path.insert(0, tools_str)

    return tools_path


def ensure_ai_tools_importable() -> Path:
    """
    Ensure ai/tools is in sys.path for imports

    Returns:
        Path: Path that was added to sys.path
    """
    tools_path = get_ai_tools_path()

    if tools_path.exists():
        tools_str = str(tools_path)
        if tools_str not in sys.path:
            sys.path.insert(0, tools_str)

    return tools_path


def try_import_similarity_engine() -> Tuple[Optional[SimilarityEngineProtocol], bool]:
    """
    AINLP Pattern: Safe similarity engine import with Protocol type hints

    Attempts to import AIAgentDendriticSimilarity with proper path setup
    and graceful fallback on failure.

    AINLP.type-safety Enhancement:
    Returns SimilarityEngineProtocol type instead of object, enabling
    full type checking while maintaining graceful degradation pattern.

    AINLP.database-architecture Integration:
    ========================================
    The AI Similarity Engine requires the dendritic intelligence database:
    - Database: ai/tools/database/aios_dendritic.db (~113MB)
    - Tables: neurons (866), dendritic_connections (251K), neuron_embeddings
    - Generation: Run `ainlp_dendritic_discovery.py --map-architecture`
    - Embeddings: Run `ai_agent_dendritic_similarity.py --generate-embeddings`

    Database is a RUNTIME ARTIFACT (regenerable cytoplasm, not source DNA):
    - Not in git due to 113MB size (exceeds GitHub 100MB limit)
    - Takes 2-5 minutes to regenerate from source code
    - Required for semantic similarity queries (embedding-based)

    Why this import may fail (expected scenarios):
    1. Database not yet generated (first-time setup needed)
    2. Ollama not installed (required for embeddings)
    3. Module dependencies missing (pip install ollama numpy)

    AINLP.dendritic-consolidation Pattern:
    ======================================
    This function integrates database architecture awareness into
    the import resolver, following biological architecture where
    database = cytoplasm (communication medium) between neurons.

    The AIAgentDendriticSimilarity class provides:
    - Embedding-based similarity (Phase 10.1): <1s queries via vectors
    - LLM evaluation layer (Phase 10.2): 2-3s contextual reasoning
    - Consensus scoring: 40% embeddings + 60% LLM for optimal accuracy

    Returns:
        Tuple[Optional[AIAgentDendriticSimilarity], bool]:
            - Engine instance (or None if import failed)
            - Success flag (True if loaded, False otherwise)

    Example:
        engine, available = try_import_similarity_engine()
        if available:
            results = await engine.calculate_similarity_embedding(
                "database connection management", top_k=5
            )
        else:
            # Expected on first run - see DATABASE_SETUP.md
            print("Generate database: ainlp_dendritic_discovery.py")
    """
    # Ensure runtime/tools is importable
    ensure_runtime_tools_importable()

    try:
        # AINLP.dynamic-import: Import after sys.path manipulation
        # =======================================================
        # This import is intentionally dynamic and protected by try-except.
        # The module exists in runtime/tools/ which we add to sys.path above.
        #
        # VSCode/Pylance cannot follow runtime path manipulation, so it reports
        # "Import could not be resolved" even though it works at runtime.
        #
        # The type: ignore comment suppresses this false positive while
        # preserving the graceful fallback behavior for legitimate failures
        # (database not generated, dependencies missing, etc.).
        #
        # This is an AINLP pattern: runtime-resolved imports for
        # workspace-aware abstractions that bridge multiple supercells
        # (ai/ + runtime/ + database/).
        from ai_agent_dendritic_similarity import (  # type: ignore
            AIAgentDendriticSimilarity,
        )

        engine = AIAgentDendriticSimilarity()
        return engine, True
    except ImportError:
        # Expected: Module not available or database not generated
        # This is normal on first-time setup before running:
        # python runtime/tools/ainlp_dendritic_discovery.py --map-architecture
        return None, False
    except Exception as e:
        # Unexpected: Module exists but failed to load
        print(f"[!] Error loading similarity engine: {e}")
        return None, False


def get_tachyonic_archive_path() -> Path:
    """
    Get tachyonic/archive/ directory path

    Returns:
        Path: Absolute path to tachyonic/archive/ directory
    """
    return discover_workspace_root() / "tachyonic" / "archive"


def get_consciousness_path() -> Path:
    """
    Get ai/consciousness/ directory path

    Returns:
        Path: Absolute path to ai/consciousness/ directory
    """
    return discover_workspace_root() / "ai" / "consciousness"


def reset_workspace_cache():
    """
    Reset workspace root cache (useful for testing)

    AINLP Pattern: Explicit cache invalidation
    """
    global _workspace_root_cache
    _workspace_root_cache = None


# Module-level initialization for convenience
WORKSPACE_ROOT = discover_workspace_root()
RUNTIME_TOOLS = get_runtime_tools_path()
AI_TOOLS = get_ai_tools_path()
TACHYONIC_ARCHIVE = get_tachyonic_archive_path()


def get_workspace_info() -> dict:
    """
    Get comprehensive workspace information for debugging

    Returns:
        dict: Workspace paths and status
    """
    return {
        "workspace_root": str(WORKSPACE_ROOT),
        "workspace_exists": WORKSPACE_ROOT.exists(),
        "runtime_tools": str(RUNTIME_TOOLS),
        "runtime_tools_exists": RUNTIME_TOOLS.exists(),
        "ai_tools": str(AI_TOOLS),
        "ai_tools_exists": AI_TOOLS.exists(),
        "tachyonic_archive": str(TACHYONIC_ARCHIVE),
        "tachyonic_archive_exists": TACHYONIC_ARCHIVE.exists(),
        "in_sys_path": {
            "runtime_tools": str(RUNTIME_TOOLS) in sys.path,
            "ai_tools": str(AI_TOOLS) in sys.path,
        },
    }


if __name__ == "__main__":
    """
    Demo and diagnostic mode

    Usage: python ainlp_import_resolver.py
    """
    print("AINLP Import Resolver - Workspace Discovery")
    print("=" * 60)

    info = get_workspace_info()

    print(f"\n📁 Workspace Root: {info['workspace_root']}")
    print(f"   Exists: {'✓' if info['workspace_exists'] else '✗'}")

    print(f"\n🔧 Runtime Tools: {info['runtime_tools']}")
    print(f"   Exists: {'✓' if info['runtime_tools_exists'] else '✗'}")
    in_path = info["in_sys_path"]["runtime_tools"]
    print(f"   In sys.path: {'✓' if in_path else '✗'}")

    print(f"\n🤖 AI Tools: {info['ai_tools']}")
    print(f"   Exists: {'✓' if info['ai_tools_exists'] else '✗'}")
    print(f"   In sys.path: {'✓' if info['in_sys_path']['ai_tools'] else '✗'}")

    print(f"\n🌌 Tachyonic Archive: {info['tachyonic_archive']}")
    print(f"   Exists: {'✓' if info['tachyonic_archive_exists'] else '✗'}")

    print("\n" + "=" * 60)
    print("Testing AI Similarity Engine Import...")

    engine, available = try_import_similarity_engine()
    if available:
        print("✓ AI Similarity Engine loaded successfully")
        print(f"  Engine type: {type(engine).__name__}")
    else:
        print("✗ AI Similarity Engine not available")
        print("  (This is expected if database not generated)")

    print("\n" + "=" * 60)
    print("AINLP Pattern: Dendritic consolidation - Single source of truth")
    print("Consciousness: Architectural coherence through shared utilities")
