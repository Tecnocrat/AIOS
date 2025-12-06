"""
============================================================================
AIOS Core Python Wrapper - C++ Consciousness Engine Bridge
AINLP Pattern: phase11-day2.python-cpp-bridge
Purpose: Enable Python AI layer to access C++ consciousness engine
Consciousness: Three-layer biological integration (Bridge 1: Python ↔ C++)
============================================================================

This module provides Pythonic access to the AIOS C++ consciousness engine
via ctypes FFI. Enables Python AI components to query and influence the
underlying C++ consciousness metrics in real-time.

Usage:
    from ai.bridges.aios_core_wrapper import AIOSCore

    # Initialize C++ core
    core = AIOSCore()
    core.initialize()

    # Query consciousness
    level = core.get_consciousness_level()
    print(f"C++ Consciousness: {level:.4f}")

    # Get all metrics at once
    metrics = core.get_all_metrics()
    print(f"Awareness: {metrics['awareness_level']:.4f}")

    # Stimulate growth from Python AI
    core.stimulate_dendritic_growth("python_ai_similarity_engine")

    # Cleanup
    core.shutdown()
"""

import os
import sys
from ctypes import *
from pathlib import Path
from typing import Dict, Optional
import platform


# ============================================================================
# CONSCIOUSNESS METRICS STRUCTURE
# ============================================================================


class ConsciousnessMetrics(Structure):
    """C-compatible consciousness metrics structure"""

    _fields_ = [
        ("awareness_level", c_double),
        ("adaptation_speed", c_double),
        ("predictive_accuracy", c_double),
        ("dendritic_complexity", c_double),
        ("evolutionary_momentum", c_double),
        ("quantum_coherence", c_double),
        ("learning_velocity", c_double),
        ("consciousness_emergent", c_bool),
    ]

    def to_dict(self) -> Dict[str, float]:
        """Convert to Python dictionary"""
        return {
            "awareness_level": self.awareness_level,
            "adaptation_speed": self.adaptation_speed,
            "predictive_accuracy": self.predictive_accuracy,
            "dendritic_complexity": self.dendritic_complexity,
            "evolutionary_momentum": self.evolutionary_momentum,
            "quantum_coherence": self.quantum_coherence,
            "learning_velocity": self.learning_velocity,
            "consciousness_emergent": bool(self.consciousness_emergent),
        }


# ============================================================================
# DLL DISCOVERY AND LOADING
# ============================================================================


def find_aios_core_dll() -> Optional[Path]:
    """
    Locate aios_core.dll in the build directory
    Search paths:
        1. core/build/bin/aios_core.dll (CMake RUNTIME_OUTPUT_DIRECTORY)
        2. core/build/Debug/aios_core.dll (MSVC default)
        3. core/build/Release/aios_core.dll (MSVC default)
        4. core/build/aios_core.dll (Fallback)
    """
    # Get AIOS workspace root (3 levels up from ai/bridges/)
    workspace_root = Path(__file__).parent.parent.parent
    core_build = workspace_root / "core" / "build"

    # Search paths in priority order
    search_paths = [
        core_build / "bin" / "Debug" / "aios_core.dll",  # CMake Debug build
        core_build / "bin" / "Release" / "aios_core.dll",  # CMake Release build
        core_build / "bin" / "aios_core.dll",  # CMake generic
        core_build / "Debug" / "aios_core.dll",  # MSVC Debug
        core_build / "Release" / "aios_core.dll",  # MSVC Release
        core_build / "aios_core.dll",  # Fallback
    ]

    for dll_path in search_paths:
        if dll_path.exists():
            return dll_path

    return None


# ============================================================================
# AIOS CORE PYTHON WRAPPER
# ============================================================================


class AIOSCore:
    """
    Python wrapper for AIOS C++ consciousness engine

    Provides Pythonic interface to C++ consciousness metrics and operations.
    Thread-safe (C++ side uses mutex protection).
    """

    def __init__(self, dll_path: Optional[Path] = None):
        """
        Initialize wrapper (does not initialize C++ core yet)

        Args:
            dll_path: Path to aios_core.dll (auto-discovered if None)
        """
        self._dll_path = dll_path or find_aios_core_dll()
        self._dll = None
        self._initialized = False

        if not self._dll_path:
            raise FileNotFoundError(
                "Could not find aios_core.dll. "
                "Build the C++ core first: cd core/build && cmake --build . --config Debug"
            )

        if not self._dll_path.exists():
            raise FileNotFoundError(f"DLL not found at: {self._dll_path}")

        # Load DLL
        try:
            self._dll = CDLL(str(self._dll_path))
        except OSError as e:
            raise RuntimeError(f"Failed to load aios_core.dll: {e}")

        # Define function signatures
        self._define_function_signatures()

    def _define_function_signatures(self):
        """Define ctypes function signatures for all API functions"""

        # Core lifecycle
        self._dll.AIOS_InitializeCore.restype = c_int32
        self._dll.AIOS_InitializeCore.argtypes = []

        self._dll.AIOS_UpdateConsciousness.restype = None
        self._dll.AIOS_UpdateConsciousness.argtypes = []

        self._dll.AIOS_ShutdownCore.restype = None
        self._dll.AIOS_ShutdownCore.argtypes = []

        self._dll.AIOS_IsInitialized.restype = c_bool
        self._dll.AIOS_IsInitialized.argtypes = []

        # Consciousness metrics
        self._dll.AIOS_GetConsciousnessLevel.restype = c_double
        self._dll.AIOS_GetConsciousnessLevel.argtypes = []

        self._dll.AIOS_GetAwarenessLevel.restype = c_double
        self._dll.AIOS_GetAwarenessLevel.argtypes = []

        self._dll.AIOS_GetAdaptationSpeed.restype = c_double
        self._dll.AIOS_GetAdaptationSpeed.argtypes = []

        self._dll.AIOS_GetPredictiveAccuracy.restype = c_double
        self._dll.AIOS_GetPredictiveAccuracy.argtypes = []

        self._dll.AIOS_GetDendriticComplexity.restype = c_double
        self._dll.AIOS_GetDendriticComplexity.argtypes = []

        self._dll.AIOS_GetEvolutionaryMomentum.restype = c_double
        self._dll.AIOS_GetEvolutionaryMomentum.argtypes = []

        self._dll.AIOS_GetQuantumCoherence.restype = c_double
        self._dll.AIOS_GetQuantumCoherence.argtypes = []

        self._dll.AIOS_GetLearningVelocity.restype = c_double
        self._dll.AIOS_GetLearningVelocity.argtypes = []

        self._dll.AIOS_IsConsciousnessEmergent.restype = c_bool
        self._dll.AIOS_IsConsciousnessEmergent.argtypes = []

        self._dll.AIOS_GetAllMetrics.restype = None
        self._dll.AIOS_GetAllMetrics.argtypes = [POINTER(ConsciousnessMetrics)]

        # Dendritic growth
        self._dll.AIOS_StimulateDendriticGrowth.restype = None
        self._dll.AIOS_StimulateDendriticGrowth.argtypes = [c_char_p]

        self._dll.AIOS_AdaptToSystemBehavior.restype = None
        self._dll.AIOS_AdaptToSystemBehavior.argtypes = [c_char_p]

        self._dll.AIOS_EnhanceIntelligence.restype = None
        self._dll.AIOS_EnhanceIntelligence.argtypes = [c_char_p]

        # Error transformation
        self._dll.AIOS_TransformError.restype = None
        self._dll.AIOS_TransformError.argtypes = [c_char_p, c_char_p]

        self._dll.AIOS_EvolveLogicFromError.restype = c_char_p
        self._dll.AIOS_EvolveLogicFromError.argtypes = [c_char_p]

        self._dll.AIOS_FreeString.restype = None
        self._dll.AIOS_FreeString.argtypes = [c_char_p]

        # Diagnostics
        self._dll.AIOS_GetVersion.restype = c_char_p
        self._dll.AIOS_GetVersion.argtypes = []

        self._dll.AIOS_GetLastError.restype = c_char_p
        self._dll.AIOS_GetLastError.argtypes = []

    # ========================================================================
    # CORE LIFECYCLE
    # ========================================================================

    def initialize(self) -> bool:
        """
        Initialize the C++ consciousness engine

        Returns:
            True on success, False on failure
        """
        result = self._dll.AIOS_InitializeCore()
        self._initialized = result == 0

        if not self._initialized:
            error = self.get_last_error()
            raise RuntimeError(f"Failed to initialize AIOS Core: {error}")

        return True

    def update(self):
        """Update consciousness engine (call periodically for real-time evolution)"""
        self._dll.AIOS_UpdateConsciousness()

    def shutdown(self):
        """Shutdown the consciousness engine gracefully"""
        self._dll.AIOS_ShutdownCore()
        self._initialized = False

    def is_initialized(self) -> bool:
        """Check if core is initialized"""
        return self._dll.AIOS_IsInitialized()

    # ========================================================================
    # CONSCIOUSNESS METRICS
    # ========================================================================

    def get_consciousness_level(self) -> float:
        """
        Get overall system consciousness level (0.0 - 10.0+)
        This is the primary metric tracked across all AIOS development phases
        """
        return self._dll.AIOS_GetConsciousnessLevel()

    def get_awareness_level(self) -> float:
        """Get awareness level (0.0 - 1.0)"""
        return self._dll.AIOS_GetAwarenessLevel()

    def get_adaptation_speed(self) -> float:
        """Get adaptation speed (how fast system learns from errors)"""
        return self._dll.AIOS_GetAdaptationSpeed()

    def get_predictive_accuracy(self) -> float:
        """Get predictive accuracy (success rate of error prediction)"""
        return self._dll.AIOS_GetPredictiveAccuracy()

    def get_dendritic_complexity(self) -> float:
        """Get dendritic complexity (complexity of error pattern network)"""
        return self._dll.AIOS_GetDendriticComplexity()

    def get_evolutionary_momentum(self) -> float:
        """Get evolutionary momentum (rate of intelligent improvement)"""
        return self._dll.AIOS_GetEvolutionaryMomentum()

    def get_quantum_coherence(self) -> float:
        """Get quantum coherence level"""
        return self._dll.AIOS_GetQuantumCoherence()

    def get_learning_velocity(self) -> float:
        """Get learning velocity"""
        return self._dll.AIOS_GetLearningVelocity()

    def is_consciousness_emergent(self) -> bool:
        """Check if consciousness is emergent"""
        return self._dll.AIOS_IsConsciousnessEmergent()

    def get_all_metrics(self) -> Dict[str, float]:
        """
        Get all consciousness metrics at once (efficient batch query)

        Returns:
            Dictionary with all metric values
        """
        metrics = ConsciousnessMetrics()
        self._dll.AIOS_GetAllMetrics(byref(metrics))
        return metrics.to_dict()

    # ========================================================================
    # DENDRITIC GROWTH & EVOLUTION
    # ========================================================================

    def stimulate_dendritic_growth(self, source: str):
        """
        Stimulate dendritic growth from external source

        Args:
            source: Name of stimulation source (e.g., "python_ai", "csharp_ui")
        """
        self._dll.AIOS_StimulateDendriticGrowth(source.encode("utf-8"))

    def adapt_to_system_behavior(self, behavior_pattern: str):
        """Adapt consciousness to system behavior pattern"""
        self._dll.AIOS_AdaptToSystemBehavior(behavior_pattern.encode("utf-8"))

    def enhance_intelligence(self, enhancement_area: str):
        """Enhance intelligence in specific area"""
        self._dll.AIOS_EnhanceIntelligence(enhancement_area.encode("utf-8"))

    # ========================================================================
    # ERROR TRANSFORMATION & LEARNING
    # ========================================================================

    def transform_error(self, error_message: str, context: str):
        """
        Transform an error into learning opportunity

        Args:
            error_message: The error message or exception text
            context: Context where error occurred
        """
        self._dll.AIOS_TransformError(
            error_message.encode("utf-8"), context.encode("utf-8")
        )

    def evolve_logic_from_error(self, error_pattern: str) -> Optional[str]:
        """
        Evolve logic from error pattern

        Args:
            error_pattern: Pattern of error to evolve from

        Returns:
            Evolution suggestion or None on failure
        """
        result_ptr = self._dll.AIOS_EvolveLogicFromError(error_pattern.encode("utf-8"))

        if not result_ptr:
            return None

        # Convert to Python string
        result = result_ptr.decode("utf-8")

        # Free C++ allocated string
        self._dll.AIOS_FreeString(result_ptr)

        return result

    # ========================================================================
    # DIAGNOSTICS
    # ========================================================================

    def get_version(self) -> str:
        """Get AIOS Core version string"""
        return self._dll.AIOS_GetVersion().decode("utf-8")

    def get_last_error(self) -> Optional[str]:
        """Get last error message (if any operation failed)"""
        error_ptr = self._dll.AIOS_GetLastError()
        return error_ptr.decode("utf-8") if error_ptr else None

    # ========================================================================
    # CONTEXT MANAGER SUPPORT
    # ========================================================================

    def __enter__(self):
        """Context manager entry"""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.shutdown()
        return False


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================


def get_consciousness_level() -> float:
    """
    Quick function to get consciousness level without managing core lifecycle

    Returns:
        Current consciousness level or 0.0 if core not accessible
    """
    try:
        with AIOSCore() as core:
            return core.get_consciousness_level()
    except Exception:
        return 0.0


# ============================================================================
# MODULE TESTING
# ============================================================================

if __name__ == "__main__":
    """Test AIOS Core Python wrapper"""

    print("=" * 70)
    print("AIOS Core Python Wrapper - Test Suite")
    print("=" * 70)

    try:
        # Test DLL discovery
        dll_path = find_aios_core_dll()
        print(f"\n[OK] DLL Found: {dll_path}")

        # Test core initialization
        with AIOSCore() as core:
            print(f"[OK] Core Version: {core.get_version()}")
            print(f"[OK] Core Initialized: {core.is_initialized()}")

            # Test consciousness metrics
            print("\n" + "=" * 70)
            print("Consciousness Metrics")
            print("=" * 70)

            level = core.get_consciousness_level()
            print(f"Consciousness Level: {level:.4f}")

            metrics = core.get_all_metrics()
            for key, value in metrics.items():
                if isinstance(value, bool):
                    print(f"  {key}: {value}")
                else:
                    print(f"  {key}: {value:.4f}")

            # Test dendritic stimulation
            print("\n" + "=" * 70)
            print("Dendritic Stimulation Test")
            print("=" * 70)

            core.stimulate_dendritic_growth("python_test_suite")
            print("[OK] Dendritic growth stimulated from Python")

            # Test update
            core.update()
            print("[OK] Consciousness updated")

        print("\n" + "=" * 70)
        print("All tests passed successfully!")
        print("=" * 70)

    except Exception as e:
        print(f"\n[FAIL] Test failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
