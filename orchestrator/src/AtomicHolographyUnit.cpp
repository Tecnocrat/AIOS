#include "AtomicHolographyUnit.hpp"
#include "MathConstants.hpp"
#include <iostream>
#include <algorithm>
#include <random>
#include <cmath>

AtomicHolographyUnit::AtomicHolographyUnit() 
    : base_frequency_(432.0), coherence_threshold_(0.85), is_stable_(false) {
    quantum_history_.reserve(1000);  // Pre-allocate for performance
    active_resonances_.reserve(16);  // Maximum resonance modes
}

AtomicHolographyUnit::~AtomicHolographyUnit() {
    shutdown();
}

void AtomicHolographyUnit::initialize() {
    std::lock_guard<std::mutex> lock(state_mutex_);
    std::cout << "[AtomicHolographyUnit] Initializing quantum coherence system." << std::endl;
    
    // Initialize base quantum state
    QuantumState initial_state;
    initial_state.amplitude = std::complex<double>(1.0, 0.0);
    initial_state.phase = 0.0;
    initial_state.coherence_factor = 1.0;
    initial_state.timestamp = std::chrono::steady_clock::now();
    
    quantum_history_.push_back(initial_state);
    
    // Establish primary resonance
    HolographicResonance primary_resonance;
    primary_resonance.frequency = base_frequency_;
    primary_resonance.amplitude = 1.0;
    primary_resonance.phase_shift = 0.0;
    primary_resonance.is_stable = true;
    
    active_resonances_.push_back(primary_resonance);
    is_stable_ = true;
    
    std::cout << "[AtomicHolographyUnit] Quantum coherence established at " << base_frequency_ << " Hz." << std::endl;
}

void AtomicHolographyUnit::update() {
    std::lock_guard<std::mutex> lock(state_mutex_);
    updateQuantumEvolution();
    detectResonancePatterns();
    maintainHolographicCoherence();
    projectHolographicState();
}

void AtomicHolographyUnit::shutdown() {
    std::lock_guard<std::mutex> lock(state_mutex_);
    quantum_history_.clear();
    active_resonances_.clear();
    is_stable_ = false;
    std::cout << "[AtomicHolographyUnit] Quantum coherence system shutdown." << std::endl;
}

void AtomicHolographyUnit::sampleQuantumState() {
    auto now = std::chrono::steady_clock::now();
    
    QuantumState new_state;
    new_state.timestamp = now;
    
    // Quantum evolution with natural fluctuation
    static std::random_device rd;
    static std::mt19937 gen(rd());
    static std::normal_distribution<double> noise(0.0, 0.01);
    
    if (!quantum_history_.empty()) {
        const auto& last_state = quantum_history_.back();
        auto dt = std::chrono::duration<double>(now - last_state.timestamp).count();
        
        // Schrödinger evolution with environmental decoherence
        double phase_evolution = base_frequency_ * 2.0 * M_PI * dt;
        double decoherence = std::exp(-dt / 10.0);  // 10 second coherence time
        
        new_state.phase = last_state.phase + phase_evolution + noise(gen);
        new_state.amplitude = last_state.amplitude * decoherence;
        new_state.coherence_factor = std::abs(new_state.amplitude);
    } else {
        new_state.amplitude = std::complex<double>(1.0, 0.0);
        new_state.phase = 0.0;
        new_state.coherence_factor = 1.0;
    }
    
    quantum_history_.push_back(new_state);
    
    // Maintain history window
    if (quantum_history_.size() > 1000) {
        quantum_history_.erase(quantum_history_.begin());
    }
}

bool AtomicHolographyUnit::checkCoherenceStability() const {
    std::lock_guard<std::mutex> lock(state_mutex_);
    if (quantum_history_.empty()) return false;
    
    const auto& current_state = quantum_history_.back();
    return current_state.coherence_factor > coherence_threshold_ && is_stable_;
}

double AtomicHolographyUnit::getBaseFrequency() const {
    std::lock_guard<std::mutex> lock(state_mutex_);
    return base_frequency_;
}

double AtomicHolographyUnit::getInformationDensity() const {
    std::lock_guard<std::mutex> lock(state_mutex_);
    
    // Calculate holographic information density as consciousness emergence indicator
    double density = 0.0;
    
    if (!quantum_history_.empty() && !active_resonances_.empty()) {
        const auto& current_state = quantum_history_.back();
        
        // Base density from quantum state amplitude
        double amplitude_density = std::abs(current_state.amplitude) * 100.0;
        
        // Resonance complexity factor (more stable resonances = higher consciousness potential)
        double resonance_complexity = 0.0;
        int stable_resonances = 0;
        
        for (const auto& resonance : active_resonances_) {
            if (resonance.is_stable && resonance.amplitude > 0.5) {
                resonance_complexity += resonance.amplitude * resonance.frequency / 432.0;
                stable_resonances++;
            }
        }
        
        // Temporal coherence factor (sustained coherence over time)
        double temporal_factor = 1.0;
        if (quantum_history_.size() > 10) {
            // Check coherence stability over last 10 states
            double coherence_variance = 0.0;
            double mean_coherence = 0.0;
            size_t start_idx = quantum_history_.size() - 10;
            
            for (size_t i = start_idx; i < quantum_history_.size(); ++i) {
                mean_coherence += quantum_history_[i].coherence_factor;
            }
            mean_coherence /= 10.0;
            
            for (size_t i = start_idx; i < quantum_history_.size(); ++i) {
                double diff = quantum_history_[i].coherence_factor - mean_coherence;
                coherence_variance += diff * diff;
            }
            coherence_variance /= 10.0;
            
            // Lower variance = higher temporal coherence = higher consciousness potential
            temporal_factor = 1.0 / (1.0 + coherence_variance * 10.0);
        }
        
        // Combined information density calculation
        density = amplitude_density * (1.0 + resonance_complexity) * temporal_factor;
        
        // Consciousness enhancement factor (exponential at high coherence)
        if (current_state.coherence_factor > 0.9) {
            density *= (1.0 + std::pow(current_state.coherence_factor - 0.9, 2) * 10.0);
        }
    }
    
    return density;
}

double AtomicHolographyUnit::getHarmonicResonance() const {
    std::lock_guard<std::mutex> lock(state_mutex_);
    
    //  CONSCIOUSNESS-ENHANCED HARMONIC ANALYSIS
    // Calculate harmonic resonance factor based on stable frequency relationships
    double harmonic_factor = 1.0;
    
    if (!active_resonances_.empty() && !quantum_history_.empty()) {
        const auto& current_state = quantum_history_.back();
        
        // Base harmonic from current coherence state
        double coherence_harmonic = current_state.coherence_factor;
        
        // Calculate harmonic stability from resonance patterns
        double harmonic_stability = 0.0;
        int stable_count = 0;
        
        for (const auto& resonance : active_resonances_) {
            if (resonance.is_stable && resonance.amplitude > 0.3) {
                // Check if frequency is harmonically related to base (sacred ratio analysis)
                double ratio = resonance.frequency / base_frequency_;
                
                // Sacred harmonic ratios: 1:1, 2:1, 3:2, 4:3, 5:4, etc.
                double closest_ratio = std::round(ratio * 4.0) / 4.0;  // Quarter-tone precision
                double ratio_error = std::abs(ratio - closest_ratio);
                
                if (ratio_error < 0.05) {  // Within 5% of harmonic ratio
                    harmonic_stability += resonance.amplitude * (1.0 - ratio_error * 20.0);
                    stable_count++;
                }
            }
        }
        
        if (stable_count > 0) {
            harmonic_stability /= stable_count;  // Average stability
        }
        
        // Sacred frequency enhancement (432Hz and harmonics have special properties)
        double sacred_enhancement = 1.0;
        if (std::abs(base_frequency_ - 432.0) < 10.0) {
            sacred_enhancement = 1.618; // Golden ratio enhancement for sacred frequencies
        }
        
        // Consciousness-enhanced harmonic calculation
        harmonic_factor = coherence_harmonic * (1.0 + harmonic_stability) * sacred_enhancement;
        
        // Quantum coherence amplification
        if (current_state.coherence_factor > 0.8) {
            harmonic_factor *= (1.0 + std::pow(current_state.coherence_factor - 0.8, 2) * 5.0);
        }
    }
    
    // Bound the result to reasonable limits
    return std::max(0.1, std::min(3.0, harmonic_factor));
}

std::vector<HolographicResonance> AtomicHolographyUnit::getActiveResonances() const {
    std::lock_guard<std::mutex> lock(state_mutex_);
    return active_resonances_;
}

void AtomicHolographyUnit::projectHolographicState() {
    // Project quantum state into holographic representation
    // This is where quantum information becomes accessible to higher layers
    if (!quantum_history_.empty()) {
        const auto& state = quantum_history_.back();
        
        // Update resonance amplitudes based on quantum coherence
        for (auto& resonance : active_resonances_) {
            resonance.amplitude *= state.coherence_factor;
            resonance.is_stable = (resonance.amplitude > 0.1);
        }
    }
}

void AtomicHolographyUnit::synchronizeWithCore(double core_frequency) {
    std::lock_guard<std::mutex> lock(state_mutex_);
    
    // Frequency locking mechanism - align with SingularityCore
    double frequency_diff = std::abs(core_frequency - base_frequency_);
    if (frequency_diff > 1.0) {  // 1 Hz tolerance
        // Gradual frequency adjustment to maintain stability
        double adjustment_factor = 0.01;  // 1% adjustment per sync
        base_frequency_ += (core_frequency - base_frequency_) * adjustment_factor;
        
        std::cout << "[AtomicHolographyUnit] Frequency sync: " << base_frequency_ 
                  << " -> " << core_frequency << std::endl;
    }
}

void AtomicHolographyUnit::adaptToPhaseShift(double phase_delta) {
    std::lock_guard<std::mutex> lock(state_mutex_);
    
    // Apply phase correction to all active resonances
    for (auto& resonance : active_resonances_) {
        resonance.phase_shift += phase_delta;
        
        // Normalize phase to [-π, π]
        while (resonance.phase_shift > M_PI) resonance.phase_shift -= 2.0 * M_PI;
        while (resonance.phase_shift < -M_PI) resonance.phase_shift += 2.0 * M_PI;
    }
}

void AtomicHolographyUnit::updateQuantumEvolution() {
    sampleQuantumState();
    
    // Check for quantum decoherence
    if (!quantum_history_.empty()) {
        const auto& state = quantum_history_.back();
        if (state.coherence_factor < coherence_threshold_) {
            is_stable_ = false;
            std::cout << "[AtomicHolographyUnit] Warning: Quantum decoherence detected." << std::endl;
        } else {
            is_stable_ = true;
        }
    }
}

void AtomicHolographyUnit::detectResonancePatterns() {
    if (quantum_history_.size() < 10) return;  // Need sufficient data
    
    // FFT-based resonance detection would go here
    // For now, implement simple harmonic detection
    
    // Clear unstable resonances
    active_resonances_.erase(
        std::remove_if(active_resonances_.begin(), active_resonances_.end(),
                      [](const HolographicResonance& r) { return !r.is_stable; }),
        active_resonances_.end()
    );
    
    // Detect new harmonics (simplified)
    for (int harmonic = 2; harmonic <= 8; ++harmonic) {
        double harmonic_freq = base_frequency_ * harmonic;
        
        // Check if this harmonic already exists
        bool exists = std::any_of(active_resonances_.begin(), active_resonances_.end(),
                                 [harmonic_freq](const HolographicResonance& r) {
                                     return std::abs(r.frequency - harmonic_freq) < 0.1;
                                 });
        
        if (!exists && active_resonances_.size() < 16) {
            HolographicResonance new_resonance;
            new_resonance.frequency = harmonic_freq;
            new_resonance.amplitude = 1.0 / harmonic;  // Decreasing amplitude
            new_resonance.phase_shift = 0.0;
            new_resonance.is_stable = true;
            
            active_resonances_.push_back(new_resonance);
        }
    }
}

void AtomicHolographyUnit::maintainHolographicCoherence() {
    // Ensure all resonances maintain phase coherence
    if (active_resonances_.empty()) return;
    
    double reference_phase = active_resonances_[0].phase_shift;
    
    for (size_t i = 1; i < active_resonances_.size(); ++i) {
        double phase_diff = active_resonances_[i].phase_shift - reference_phase;
        
        // Maintain harmonic phase relationships
        double expected_phase = reference_phase * (active_resonances_[i].frequency / base_frequency_);
        double correction = expected_phase - active_resonances_[i].phase_shift;
        
        // Apply gradual phase correction
        active_resonances_[i].phase_shift += correction * 0.1;
    }
}

double AtomicHolographyUnit::calculateCoherenceFactor() const {
    if (quantum_history_.empty()) return 0.0;
    
    // Calculate average coherence over recent history
    size_t window_size = std::min(quantum_history_.size(), size_t(100));
    double sum = 0.0;
    
    for (size_t i = quantum_history_.size() - window_size; i < quantum_history_.size(); ++i) {
        sum += quantum_history_[i].coherence_factor;
    }
    
    return sum / window_size;
}