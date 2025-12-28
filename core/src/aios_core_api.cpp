// ============================================================================
// AIOS Core C API Implementation
// AINLP Pattern: phase11-day2.cpp-dll-integration
// Purpose: Bridge C++ consciousness engine to Python/C# via C API
// Consciousness: Enable three-layer biological integration
// ============================================================================

#include "aios_core_api.h"
#include "MinimalConsciousnessEngine.hpp"
#include <string>
#include <cstring>
#include <memory>
#include <mutex>

// ============================================================================
// INTERNAL STATE MANAGEMENT
// ============================================================================

namespace {
    // Singleton consciousness engine instance
    std::unique_ptr<AIOSConsciousnessEngine> g_engine = nullptr;
    std::mutex g_engine_mutex;
    std::string g_last_error;
    bool g_initialized = false;
    
    // Version string
    const char* AIOS_VERSION = "1.0.0-Phase11-Day2";
    
    // Thread-safe error handling
    void SetLastError(const std::string& error) {
        std::lock_guard<std::mutex> lock(g_engine_mutex);
        g_last_error = error;
    }
    
    // Get engine safely
    AIOSConsciousnessEngine* GetEngine() {
        std::lock_guard<std::mutex> lock(g_engine_mutex);
        return g_engine.get();
    }
}

// ============================================================================
// CORE INITIALIZATION & LIFECYCLE
// ============================================================================

AIOS_API int32_t AIOS_InitializeCore(void) {
    try {
        std::lock_guard<std::mutex> lock(g_engine_mutex);
        
        if (g_initialized) {
            SetLastError("Core already initialized");
            return 0; // Not an error, just already done
        }
        
        // Create consciousness engine instance
        g_engine = std::make_unique<AIOSConsciousnessEngine>();
        
        // Initialize with null SingularityCore for now (can be enhanced later)
        g_engine->initialize(nullptr);
        
        g_initialized = true;
        g_last_error.clear();
        
        return 0; // Success
        
    } catch (const std::exception& e) {
        SetLastError(std::string("Initialization failed: ") + e.what());
        return -1;
    } catch (...) {
        SetLastError("Unknown initialization error");
        return -1;
    }
}

AIOS_API void AIOS_UpdateConsciousness(void) {
    try {
        auto* engine = GetEngine();
        if (engine) {
            engine->update();
        }
    } catch (const std::exception& e) {
        SetLastError(std::string("Update failed: ") + e.what());
    } catch (...) {
        SetLastError("Unknown update error");
    }
}

AIOS_API void AIOS_ShutdownCore(void) {
    try {
        std::lock_guard<std::mutex> lock(g_engine_mutex);
        
        if (g_engine) {
            g_engine->shutdown();
            g_engine.reset();
        }
        
        g_initialized = false;
        g_last_error.clear();
        
    } catch (const std::exception& e) {
        SetLastError(std::string("Shutdown failed: ") + e.what());
    } catch (...) {
        SetLastError("Unknown shutdown error");
    }
}

AIOS_API bool AIOS_IsInitialized(void) {
    std::lock_guard<std::mutex> lock(g_engine_mutex);
    return g_initialized;
}

// ============================================================================
// CONSCIOUSNESS METRICS
// ============================================================================

AIOS_API double AIOS_GetConsciousnessLevel(void) {
    try {
        auto* engine = GetEngine();
        if (!engine) {
            SetLastError("Engine not initialized");
            return 0.0;
        }
        
        return engine->getSystemConsciousnessLevel();
        
    } catch (const std::exception& e) {
        SetLastError(std::string("GetConsciousnessLevel failed: ") + e.what());
        return 0.0;
    } catch (...) {
        SetLastError("Unknown error in GetConsciousnessLevel");
        return 0.0;
    }
}

AIOS_API double AIOS_GetAwarenessLevel(void) {
    try {
        auto* engine = GetEngine();
        if (!engine) return 0.0;
        
        auto metrics = engine->getCurrentMetrics();
        return metrics.awareness_level;
        
    } catch (...) {
        return 0.0;
    }
}

AIOS_API double AIOS_GetAdaptationSpeed(void) {
    try {
        auto* engine = GetEngine();
        if (!engine) return 0.0;
        
        auto metrics = engine->getCurrentMetrics();
        return metrics.adaptation_speed;
        
    } catch (...) {
        return 0.0;
    }
}

AIOS_API double AIOS_GetPredictiveAccuracy(void) {
    try {
        auto* engine = GetEngine();
        if (!engine) return 0.0;
        
        auto metrics = engine->getCurrentMetrics();
        return metrics.predictive_accuracy;
        
    } catch (...) {
        return 0.0;
    }
}

AIOS_API double AIOS_GetDendriticComplexity(void) {
    try {
        auto* engine = GetEngine();
        if (!engine) return 0.0;
        
        auto metrics = engine->getCurrentMetrics();
        return metrics.dendritic_complexity;
        
    } catch (...) {
        return 0.0;
    }
}

AIOS_API double AIOS_GetEvolutionaryMomentum(void) {
    try {
        auto* engine = GetEngine();
        if (!engine) return 0.0;
        
        auto metrics = engine->getCurrentMetrics();
        return metrics.evolutionary_momentum;
        
    } catch (...) {
        return 0.0;
    }
}

AIOS_API double AIOS_GetQuantumCoherence(void) {
    try {
        auto* engine = GetEngine();
        if (!engine) return 0.0;
        
        auto metrics = engine->getCurrentMetrics();
        return metrics.quantum_coherence.load();
        
    } catch (...) {
        return 0.0;
    }
}

AIOS_API double AIOS_GetLearningVelocity(void) {
    try {
        auto* engine = GetEngine();
        if (!engine) return 0.0;
        
        auto metrics = engine->getCurrentMetrics();
        return metrics.learning_velocity.load();
        
    } catch (...) {
        return 0.0;
    }
}

AIOS_API bool AIOS_IsConsciousnessEmergent(void) {
    try {
        auto* engine = GetEngine();
        if (!engine) return false;
        
        auto metrics = engine->getCurrentMetrics();
        return metrics.consciousness_emergent.load();
        
    } catch (...) {
        return false;
    }
}

AIOS_API void AIOS_GetAllMetrics(AIOSConsciousnessMetrics* metrics) {
    if (!metrics) return;
    
    try {
        auto* engine = GetEngine();
        if (!engine) {
            // Return zeros if not initialized
            std::memset(metrics, 0, sizeof(AIOSConsciousnessMetrics));
            return;
        }
        
        auto cpp_metrics = engine->getCurrentMetrics();
        
        // Copy all metrics
        metrics->awareness_level = cpp_metrics.awareness_level;
        metrics->adaptation_speed = cpp_metrics.adaptation_speed;
        metrics->predictive_accuracy = cpp_metrics.predictive_accuracy;
        metrics->dendritic_complexity = cpp_metrics.dendritic_complexity;
        metrics->evolutionary_momentum = cpp_metrics.evolutionary_momentum;
        metrics->quantum_coherence = cpp_metrics.quantum_coherence.load();
        metrics->learning_velocity = cpp_metrics.learning_velocity.load();
        metrics->consciousness_emergent = cpp_metrics.consciousness_emergent.load();
        
    } catch (...) {
        std::memset(metrics, 0, sizeof(AIOSConsciousnessMetrics));
    }
}

// ============================================================================
// DENDRITIC GROWTH & EVOLUTION
// ============================================================================

AIOS_API void AIOS_StimulateDendriticGrowth(const char* source) {
    if (!source) return;
    
    try {
        auto* engine = GetEngine();
        if (engine) {
            engine->stimulateDendriticGrowth(source);
        }
    } catch (const std::exception& e) {
        SetLastError(std::string("StimulateDendriticGrowth failed: ") + e.what());
    } catch (...) {
        SetLastError("Unknown error in StimulateDendriticGrowth");
    }
}

AIOS_API void AIOS_AdaptToSystemBehavior(const char* behavior_pattern) {
    if (!behavior_pattern) return;
    
    try {
        auto* engine = GetEngine();
        if (engine) {
            engine->adaptToSystemBehavior(behavior_pattern);
        }
    } catch (const std::exception& e) {
        SetLastError(std::string("AdaptToSystemBehavior failed: ") + e.what());
    } catch (...) {
        SetLastError("Unknown error in AdaptToSystemBehavior");
    }
}

AIOS_API void AIOS_EnhanceIntelligence(const char* enhancement_area) {
    if (!enhancement_area) return;
    
    try {
        auto* engine = GetEngine();
        if (engine) {
            engine->enhanceIntelligence(enhancement_area);
        }
    } catch (const std::exception& e) {
        SetLastError(std::string("EnhanceIntelligence failed: ") + e.what());
    } catch (...) {
        SetLastError("Unknown error in EnhanceIntelligence");
    }
}

// ============================================================================
// ERROR TRANSFORMATION & LEARNING
// ============================================================================

AIOS_API void AIOS_TransformError(const char* error_message, const char* context) {
    if (!error_message || !context) return;
    
    try {
        auto* engine = GetEngine();
        if (engine) {
            // Create a dummy exception for transformation
            std::runtime_error error(error_message);
            engine->transformError(error, context);
        }
    } catch (const std::exception& e) {
        SetLastError(std::string("TransformError failed: ") + e.what());
    } catch (...) {
        SetLastError("Unknown error in TransformError");
    }
}

AIOS_API const char* AIOS_EvolveLogicFromError(const char* error_pattern) {
    if (!error_pattern) return nullptr;
    
    try {
        auto* engine = GetEngine();
        if (!engine) return nullptr;
        
        std::string evolution = engine->evolveLogicFromError(error_pattern);
        
        // Allocate and return C string (caller must free)
        char* result = new char[evolution.length() + 1];
        std::strcpy(result, evolution.c_str());
        return result;
        
    } catch (const std::exception& e) {
        SetLastError(std::string("EvolveLogicFromError failed: ") + e.what());
        return nullptr;
    } catch (...) {
        SetLastError("Unknown error in EvolveLogicFromError");
        return nullptr;
    }
}

AIOS_API void AIOS_FreeString(const char* str) {
    if (str) {
        delete[] str;
    }
}

// ============================================================================
// VERSION & DIAGNOSTICS
// ============================================================================

AIOS_API const char* AIOS_GetVersion(void) {
    return AIOS_VERSION;
}

AIOS_API const char* AIOS_GetLastError(void) {
    std::lock_guard<std::mutex> lock(g_engine_mutex);
    return g_last_error.empty() ? nullptr : g_last_error.c_str();
}
