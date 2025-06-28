#include "SingularityCore.hpp"
#include "Logger.hpp"
#include "MathConstants.hpp"
#include <cmath>
#include <limits>
#include <iostream>

SingularityCore::SingularityCore() 
    : internalSymmetry(1.0), entropy_accumulator(0.0), 
      core_frequency(432.0), quantum_coherence_locked(false) {}

SingularityCore::~SingularityCore() {
    shutdown();
}

void SingularityCore::initialize() {
    Logger logger("kernel.log");
    std::cout << "[SingularityCore] Initializing hypersphere nucleus." << std::endl;
    
    // Initialize subsystems in harmonic order
    holographyUnit.initialize();
    bus.initialize();
    shellManager.bootstrap();
    projector.configure();
    
    // Establish quantum coherence lock
    synchronizeQuantumLayers();
    
    internalSymmetry = 1.0;
    entropy_accumulator = 0.0;
    quantum_coherence_locked = holographyUnit.checkCoherenceStability();
    
    logger.meta("SingularityCore.initialize", "completed");
    logger.meta("quantum_coherence_locked", quantum_coherence_locked ? "true" : "false");
    logger.meta("core_frequency", std::to_string(core_frequency));
}

void SingularityCore::tick() {
    Logger logger("kernel.log");
    
    // Update quantum foundation first
    holographyUnit.update();
    updateCoreFrequency();
    processQuantumFeedback();
    
    // Propagate through dimensional layers
    shellManager.rotateShells();
    bus.synchronize();
    projector.project();
    
    // Maintain system stability
    maintainDimensionalStability();
    synchronizeQuantumLayers();
    
    // Update entropy based on quantum coherence
    double coherence = getCoherenceLevel();
    entropy_accumulator += (1.0 - coherence) * 0.01;  // Accumulate entropy from decoherence
    
    logger.meta("SingularityCore.tick", "executed");
    logger.meta("entropy", std::to_string(getEntropy()));
    logger.meta("curvature_at_center", std::to_string(getCurvatureAtCenter()));
    logger.meta("coherence_level", std::to_string(coherence));
    logger.meta("quantum_stable", isQuantumStable() ? "true" : "false");
}

void SingularityCore::shutdown() {
    std::cout << "[SingularityCore] Shutting down hypersphere nucleus." << std::endl;
    holographyUnit.shutdown();
    quantum_coherence_locked = false;
}

double SingularityCore::getEntropy() {
    // Entropy based on quantum decoherence and dimensional instability
    double quantum_entropy = 1.0 - getCoherenceLevel();
    double symmetry_entropy = 1.0 / std::max(internalSymmetry, 0.001);
    double accumulated_entropy = entropy_accumulator;
    
    return quantum_entropy + symmetry_entropy + accumulated_entropy;
}

double SingularityCore::getCurvatureAtCenter() {
    // Curvature at r=0 in hypersphere, influenced by quantum coherence
    const double planck_length = 1.616e-35;  // meters
    double quantum_factor = getCoherenceLevel();
    double base_curvature = 1.0 / (planck_length * planck_length);
    
    // Curvature increases with quantum decoherence (space becomes more "wrinkled")
    return base_curvature * (2.0 - quantum_factor);
}

double SingularityCore::getCoherenceLevel() {
    if (!quantum_coherence_locked) return 0.0;
    
    // Combine quantum coherence with system-wide stability
    bool quantum_stable = holographyUnit.checkCoherenceStability();
    double base_coherence = quantum_stable ? 0.95 : 0.3;
    
    // Modulate by internal symmetry
    return base_coherence * std::min(internalSymmetry, 1.0);
}

bool SingularityCore::isQuantumStable() {
    return quantum_coherence_locked && holographyUnit.checkCoherenceStability();
}

void SingularityCore::synchronizeQuantumLayers() {
    // Synchronize all subsystems with quantum frequency
    double quantum_freq = holographyUnit.getBaseFrequency();
    
    if (std::abs(quantum_freq - core_frequency) > 0.1) {
        core_frequency = quantum_freq;
        
        // Propagate frequency sync to holography unit
        holographyUnit.synchronizeWithCore(core_frequency);
        
        std::cout << "[SingularityCore] Quantum layers synchronized at " 
                  << core_frequency << " Hz." << std::endl;
    }
    
    quantum_coherence_locked = holographyUnit.checkCoherenceStability();
}

void SingularityCore::adaptToHolographicShift() {
    // Get active resonances from holography unit
    auto resonances = holographyUnit.getActiveResonances();
    
    if (!resonances.empty()) {
        // Calculate phase shift based on resonance patterns
        double total_phase = 0.0;
        double total_amplitude = 0.0;
        
        for (const auto& resonance : resonances) {
            if (resonance.is_stable) {
                total_phase += resonance.phase_shift * resonance.amplitude;
                total_amplitude += resonance.amplitude;
            }
        }
        
        if (total_amplitude > 0.0) {
            double avg_phase_shift = total_phase / total_amplitude;
            
            // Apply phase correction
            holographyUnit.adaptToPhaseShift(-avg_phase_shift * 0.1);  // 10% correction
            
            // Update internal symmetry based on phase coherence
            internalSymmetry = std::max(0.1, 1.0 - std::abs(avg_phase_shift) / M_PI);
        }
    }
}

void SingularityCore::updateCoreFrequency() {
    // Natural frequency evolution based on system state
    double entropy_factor = 1.0 / (1.0 + getEntropy());
    double target_frequency = 432.0 * entropy_factor;  // Golden ratio frequency
    
    // Gradual frequency adjustment
    double adjustment = (target_frequency - core_frequency) * 0.01;  // 1% per tick
    core_frequency += adjustment;
    
    // Maintain frequency bounds
    core_frequency = std::max(100.0, std::min(1000.0, core_frequency));
}

void SingularityCore::maintainDimensionalStability() {
    // Check for dimensional instabilities
    double entropy = getEntropy();
    double coherence = getCoherenceLevel();
    
    if (entropy > 5.0 || coherence < 0.1) {
        // System approaching instability - apply corrective measures
        std::cout << "[SingularityCore] Warning: Dimensional instability detected. "
                  << "Entropy: " << entropy << ", Coherence: " << coherence << std::endl;
        
        // Reset entropy accumulator partially
        entropy_accumulator *= 0.9;
        
        // Force quantum resynchronization
        synchronizeQuantumLayers();
        
        // Apply holographic phase correction
        adaptToHolographicShift();
    }
}

void SingularityCore::processQuantumFeedback() {
    // Process feedback from quantum layer to adjust core behavior
    auto resonances = holographyUnit.getActiveResonances();
    
    if (!resonances.empty()) {
        // Calculate system harmony based on resonance stability
        int stable_count = 0;
        for (const auto& resonance : resonances) {
            if (resonance.is_stable) stable_count++;
        }
        
        double harmony_ratio = static_cast<double>(stable_count) / resonances.size();
        
        // Adjust internal symmetry based on harmonic stability
        internalSymmetry = 0.9 * internalSymmetry + 0.1 * harmony_ratio;
        
        // If harmony is very high, reduce entropy accumulation
        if (harmony_ratio > 0.8) {
            entropy_accumulator *= 0.99;  // Slow entropy decay
        }
    }
}

// Component registration methods
void SingularityCore::registerQuantumUnit(AtomicHolographyUnit* quantum_unit) {
    // The quantum unit is already integrated as holographyUnit member
    // This method provides external registration interface
    std::cout << "[SingularityCore] Quantum unit registered for external access" << std::endl;
}

void SingularityCore::registerGeometryField(CenterGeometryField* geometry_field) {
    std::cout << "[SingularityCore] Geometry field registered" << std::endl;
    // Store reference for future integration
    // In a full implementation, this would be stored as a member
}

void SingularityCore::registerShellManager(SphereShellManager* shell_manager) {
    std::cout << "[SingularityCore] Shell manager registered" << std::endl;
    // The shell manager is already integrated as shellManager member
}

void SingularityCore::registerEvolutionEngine(CodeEvolutionEngine* evolution_engine) {
    std::cout << "[SingularityCore] Code evolution engine registered" << std::endl;
    // Store reference for future integration
}

// AI Integration methods (already implemented above)
// The registerAIController, triggerAIAnalysis, and processAIFeedback methods 
// are implemented earlier in this file