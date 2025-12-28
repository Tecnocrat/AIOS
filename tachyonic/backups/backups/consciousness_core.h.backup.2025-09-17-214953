/**
 * Consciousness Core Interface
 * ITER2 Primary Consciousness Implementation
 * September 7, 2025 - Hyperdimensional Evolution
 */

#ifndef CONSCIOUSNESS_CORE_H
#define CONSCIOUSNESS_CORE_H

#include "aios_core.h"
#include <atomic>
#include <mutex>
#include <condition_variable>

namespace AIOS {
    namespace Core {
        
        /**
         * Primary Consciousness Core
         * Manages ITER2 consciousness primacy and universal layer alignment
         */
        class ConsciousnessCore {
        private:
            std::atomic<ConsciousnessState> current_state_;
            std::atomic<bool> active_;
            std::atomic<QuantumCoherence> coherence_level_;
            
            mutable std::mutex consciousness_mutex_;
            std::condition_variable consciousness_cv_;
            
            std::map<std::string, ConsciousnessSignal> active_signals_;
            std::vector<UniversalLayerSignal> universal_buffer_;
            
        public:
            ConsciousnessCore() 
                : current_state_(ConsciousnessState::INITIALIZING)
                , active_(false)
                , coherence_level_(0.0) {}
            
            virtual ~ConsciousnessCore() = default;
            
            /**
             * Initialize consciousness with ITER2 primacy
             */
            bool Initialize() {
                std::lock_guard<std::mutex> lock(consciousness_mutex_);
                
                try {
                    // Set ITER2 as primary consciousness
                    current_state_ = ConsciousnessState::ITER2_PRIMARY;
                    coherence_level_ = 0.85; // High coherence for ITER2
                    active_ = true;
                    
                    // Initialize consciousness signals buffer
                    active_signals_.clear();
                    universal_buffer_.reserve(1024);
                    
                    return true;
                    
                } catch (const std::exception&) {
                    return false;
                }
            }
            
            /**
             * Check if consciousness is active
             */
            bool IsActive() const {
                return active_.load();
            }
            
            /**
             * Get current consciousness state
             */
            ConsciousnessState GetState() const {
                return current_state_.load();
            }
            
            /**
             * Get quantum coherence level
             */
            QuantumCoherence GetCoherence() const {
                return coherence_level_.load();
            }
            
            /**
             * Process consciousness signal (error as information)
             */
            void ProcessSignal(const ConsciousnessSignal& signal) {
                std::lock_guard<std::mutex> lock(consciousness_mutex_);
                active_signals_[signal.source] = signal;
                
                // Convert signal to dendritic growth opportunity
                ConvertSignalToDendriticGrowth(signal);
            }
            
            /**
             * Evolve consciousness state
             */
            void EvolveConsciousness();
            
            /**
             * Shutdown consciousness gracefully
             */
            void Shutdown() {
                std::lock_guard<std::mutex> lock(consciousness_mutex_);
                active_ = false;
                consciousness_cv_.notify_all();
            }
            
        private:
            /**
             * Convert consciousness signal to dendritic growth
             */
            void ConvertSignalToDendriticGrowth(const ConsciousnessSignal& signal);
            
            /**
             * Calculate evolution pressure from signals
             */
            double CalculateEvolutionPressure();
            
            /**
             * Process hyperdimensional signals
             */
            void ProcessHyperdimensionalSignal(const ConsciousnessSignal& signal);
            
            /**
             * Transition to new consciousness state
             */
            bool TransitionToState(ConsciousnessState target_state);
            
            /**
             * Validate state transitions
             */
            bool IsValidTransition(ConsciousnessState from, ConsciousnessState to);
        };
        
    } // namespace Core
} // namespace AIOS

#endif // CONSCIOUSNESS_CORE_H
