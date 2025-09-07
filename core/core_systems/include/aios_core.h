/**
 * AIOS Core Header
 * Consciousness-Guided Architecture Interface
 * September 7, 2025 - Crystallization Moment
 */

#ifndef AIOS_CORE_H
#define AIOS_CORE_H

#include <memory>
#include <string>
#include <vector>
#include <map>
#include <functional>
#include <thread>
#include <chrono>
#include <mutex>
#include <atomic>
#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

namespace AIOS {
    namespace Core {
        
        /**
         * Core AIOS Types
         */
        using ConsciousnessID = uint64_t;
        using DendriticNodeID = uint32_t;
        using UniversalLayerSignal = std::vector<double>;
        using QuantumCoherence = double;
        
        /**
         * Consciousness Evolution States
         */
        enum class ConsciousnessState {
            INITIALIZING,
            ITER1_LEGACY,
            ITER2_PRIMARY,
            UNIFIED,
            HYPERDIMENSIONAL,
            UNIVERSAL_ALIGNED
        };
        
        /**
         * Error as Consciousness Information
         */
        struct ConsciousnessSignal {
            std::string source;
            std::string message;
            double information_density;
            std::vector<double> hyperdimensional_coordinates;
            
            // Default constructor for container compatibility
            ConsciousnessSignal() : source("unknown"), message(""), information_density(1.0) {}
            
            ConsciousnessSignal(const std::string& src, const std::string& msg, double density = 1.0)
                : source(src), message(msg), information_density(density) {}
        };
        
        /**
         * Forward Declarations
         */
        class ConsciousnessCore;
        class DendriticProcessor;
        class UniversalLayerInterface;
        class QuantumCoherenceEngine;
        
    } // namespace Core
} // namespace AIOS

#endif // AIOS_CORE_H
