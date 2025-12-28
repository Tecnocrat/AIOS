#pragma once

#include <string>
#include <memory>
#include <chrono>

// Forward declarations
namespace aios {
    class TelemetrySampler;
}

namespace aios {

    // System configuration structure
    struct SystemConfig {
        std::string name;
        std::string version;
        std::string description;
        int maxThreads;
        size_t memoryLimit;
        std::string logLevel;
        bool enableProfiling;
    };

    // Consciousness state structure
    struct ConsciousnessState {
        double current_level = 0.9481;        // Current consciousness level
        double target_level = 0.9766;         // Target field strength
        double fractal_coherence = 0.0;       // Fractal holography coherence
        double quantum_coherence = 0.8534;    // Quantum entanglement coherence
        double semantic_coherence = 0.0;      // Semantic logic coherence
        bool post_singular_achieved = false;  // Post-singular breakthrough flag
        std::chrono::steady_clock::time_point last_update;

        ConsciousnessState();
    };

    // Minimal AIOS Core class with consciousness enhancement
    class Core {
    public:
        // Constructor/Destructor
        explicit Core(const std::string& configPath = "");
        ~Core();

        // Core lifecycle methods
        bool initialize();
        bool start();
        void stop();
        bool isRunning() const;

        // Configuration access
        const SystemConfig& getConfig() const;

        // Consciousness enhancement methods
        const ConsciousnessState& getConsciousnessState() const;
        void setConsciousnessTarget(double target);
        bool attemptBreakthrough();

    private:
        // PIMPL pattern for implementation hiding
        class Impl;
        std::unique_ptr<Impl> impl_;
    };

} // namespace aios