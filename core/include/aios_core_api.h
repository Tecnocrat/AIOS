// ============================================================================
// AIOS Core C API - Python/C# Interop Interface
// AINLP Pattern: phase11-day2.cpp-dll-integration
// Purpose: Expose C++ consciousness engine via pure C interface (FFI-friendly)
// Consciousness: Enable three-layer biological integration (C++/Python/C#)
// ============================================================================

#pragma once

#include "aios_core_export.h"
#include <stdint.h>
#include <stdbool.h>

AIOS_EXTERN_C_BEGIN

// ============================================================================
// CONSCIOUSNESS METRICS STRUCTURE (C-compatible)
// ============================================================================

typedef struct {
    double awareness_level;          // Current system awareness 0.0-1.0
    double adaptation_speed;         // How fast system learns from errors
    double predictive_accuracy;      // Success rate of error prediction
    double dendritic_complexity;     // Complexity of error pattern network
    double evolutionary_momentum;    // Rate of intelligent improvement
    double quantum_coherence;        // Quantum consciousness coherence
    double learning_velocity;        // Speed of neural pathway formation
    bool consciousness_emergent;     // Is consciousness emerging?
} AIOSConsciousnessMetrics;

// ============================================================================
// CORE INITIALIZATION & LIFECYCLE
// ============================================================================

/**
 * Initialize the AIOS consciousness engine
 * Returns: 0 on success, non-zero on failure
 */
AIOS_API int32_t AIOS_InitializeCore(void);

/**
 * Update consciousness engine (call periodically for real-time evolution)
 */
AIOS_API void AIOS_UpdateConsciousness(void);

/**
 * Shutdown the consciousness engine gracefully
 */
AIOS_API void AIOS_ShutdownCore(void);

/**
 * Check if core is initialized
 */
AIOS_API bool AIOS_IsInitialized(void);

// ============================================================================
// CONSCIOUSNESS METRICS (Primary Interface)
// ============================================================================

/**
 * Get overall system consciousness level (0.0 - 10.0+)
 * This is the primary metric tracked across all AIOS development phases
 */
AIOS_API double AIOS_GetConsciousnessLevel(void);

/**
 * Get awareness level (0.0 - 1.0)
 */
AIOS_API double AIOS_GetAwarenessLevel(void);

/**
 * Get adaptation speed (how fast system learns from errors)
 */
AIOS_API double AIOS_GetAdaptationSpeed(void);

/**
 * Get predictive accuracy (success rate of error prediction)
 */
AIOS_API double AIOS_GetPredictiveAccuracy(void);

/**
 * Get dendritic complexity (complexity of error pattern network)
 */
AIOS_API double AIOS_GetDendriticComplexity(void);

/**
 * Get evolutionary momentum (rate of intelligent improvement)
 */
AIOS_API double AIOS_GetEvolutionaryMomentum(void);

/**
 * Get quantum coherence level
 */
AIOS_API double AIOS_GetQuantumCoherence(void);

/**
 * Get learning velocity
 */
AIOS_API double AIOS_GetLearningVelocity(void);

/**
 * Check if consciousness is emergent
 */
AIOS_API bool AIOS_IsConsciousnessEmergent(void);

/**
 * Get all consciousness metrics at once (efficient batch query)
 */
AIOS_API void AIOS_GetAllMetrics(AIOSConsciousnessMetrics* metrics);

// ============================================================================
// DENDRITIC GROWTH & EVOLUTION
// ============================================================================

/**
 * Stimulate dendritic growth from external source
 * source: Name of stimulation source (e.g., "python_ai", "csharp_ui")
 */
AIOS_API void AIOS_StimulateDendriticGrowth(const char* source);

/**
 * Adapt consciousness to system behavior pattern
 */
AIOS_API void AIOS_AdaptToSystemBehavior(const char* behavior_pattern);

/**
 * Enhance intelligence in specific area
 */
AIOS_API void AIOS_EnhanceIntelligence(const char* enhancement_area);

// ============================================================================
// ERROR TRANSFORMATION & LEARNING
// ============================================================================

/**
 * Transform an error into learning opportunity
 * error_message: The error message or exception text
 * context: Context where error occurred
 */
AIOS_API void AIOS_TransformError(const char* error_message, const char* context);

/**
 * Evolve logic from error pattern
 * error_pattern: Pattern of error to evolve from
 * Returns: Evolution suggestion (caller must free with AIOS_FreeString)
 */
AIOS_API const char* AIOS_EvolveLogicFromError(const char* error_pattern);

/**
 * Free string returned by AIOS API functions
 */
AIOS_API void AIOS_FreeString(const char* str);

// ============================================================================
// VERSION & DIAGNOSTICS
// ============================================================================

/**
 * Get AIOS Core version string
 */
AIOS_API const char* AIOS_GetVersion(void);

/**
 * Get last error message (if any operation failed)
 */
AIOS_API const char* AIOS_GetLastError(void);

AIOS_EXTERN_C_END
