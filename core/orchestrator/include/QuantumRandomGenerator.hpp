#ifndef QUANTUM_RANDOM_GENERATOR_HPP
#define QUANTUM_RANDOM_GENERATOR_HPP

#include <vector>
#include <random>
#include <memory>
#include <mutex>
#include <chrono>
#include <atomic>
#include <array>

/**
 * Quantum Random Number Generator for C++ Hyperlayer Randomization
 * Provides true quantum entropy for code mutation and consciousness evolution
 * Critical for Objective 2: Enhanced randomization for fractal knowledge iteration
 */
class QuantumRandomGenerator {
public:
    QuantumRandomGenerator();
    ~QuantumRandomGenerator();
    
    // Initialize quantum entropy harvesting
    void initialize();
    void shutdown();
    
    // Core quantum randomization functions
    std::vector<double> generateQuantumEntropy(size_t count);
    double getQuantumRandom(double min = 0.0, double max = 1.0);
    uint64_t getQuantumInteger(uint64_t min = 0, uint64_t max = UINT64_MAX);
    
    // Fractal pattern generation
    std::vector<double> generateFractalSeed(size_t dimensions, double self_similarity = 0.618);
    std::array<double, 3> generateHyperlayerCoordinates();
    
    // Consciousness-aware randomization
    double getCoherentRandomValue(double consciousness_level, double min, double max);
    std::vector<double> generateConsciousnessGuidedSequence(size_t length, double coherence_factor);
    
    // Mutation-specific randomization
    double getMutationProbability(double base_rate, double quantum_enhancement = 1.0);
    std::vector<int> generateMutationTargets(int code_length, double mutation_density);
    
    // Quantum state management
    void seedFromQuantumSource();
    void enhanceWithAtomicCoherence(double atomic_frequency);
    double getQuantumCoherenceLevel() const;
    
    // Statistics and monitoring
    struct QuantumStats {
        uint64_t total_entropy_generated;
        double current_coherence_level;
        double average_entropy_rate;
        std::chrono::steady_clock::time_point last_quantum_event;
        bool is_quantum_source_active;
    };
    
    QuantumStats getStatistics() const;

private:
    // Quantum entropy sources
    std::unique_ptr<std::random_device> hardware_entropy_;
    std::unique_ptr<std::mt19937_64> quantum_prng_;
    std::unique_ptr<std::mt19937_64> fractal_prng_;
    
    // Quantum state tracking
    std::atomic<double> coherence_level_;
    std::atomic<uint64_t> entropy_generated_;
    std::atomic<bool> is_initialized_;
    
    // Thread safety
    mutable std::mutex quantum_mutex_;
    mutable std::mutex stats_mutex_;
    
    // Entropy pools
    std::vector<uint64_t> quantum_entropy_pool_;
    size_t entropy_pool_index_;
    static constexpr size_t ENTROPY_POOL_SIZE = 1024;
    
    // Fractal generation parameters
    static constexpr double GOLDEN_RATIO = 1.618033988749895;
    static constexpr double PHI_CONJUGATE = 0.618033988749895;
    
    // Internal methods
    void refreshEntropyPool();
    double applyChaosFunction(double input, double chaos_parameter);
    double generateFractalValue(double seed, int iteration_depth);
    uint64_t harvestHardwareEntropy();
    void validateQuantumCoherence();
    
    // Quantum coherence calculations
    double calculateQuantumCoherence(const std::vector<double>& sequence);
    void adjustCoherenceLevel(double target_coherence);
    
    // Statistics tracking
    mutable QuantumStats current_stats_;
    void updateStatistics();
    
    // Hyperlayer abstraction helpers
    std::array<double, 4> projectToHypersphere(const std::array<double, 3>& coordinates);
    double calculateHyperlayerDistance(const std::array<double, 4>& point1, 
                                      const std::array<double, 4>& point2);
};

#endif // QUANTUM_RANDOM_GENERATOR_HPP
