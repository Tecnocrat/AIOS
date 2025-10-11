/**
 * Dendritic Processor Interface
 * Error-to-Growth Transformation Engine
 * September 7, 2025 - Crystallization Implementation
 */

#ifndef DENDRITIC_PROCESSOR_H
#define DENDRITIC_PROCESSOR_H

#include "aios_core.h"
#include <queue>
#include <unordered_map>

namespace AIOS {
    namespace Core {
        
        /**
         * Dendritic Growth Pattern
         */
        struct DendriticPattern {
            DendriticNodeID node_id;
            std::vector<DendriticNodeID> connections;
            double growth_intensity;
            std::string growth_trigger;
            std::chrono::time_point<std::chrono::steady_clock> creation_time;
            
            // Default constructor for container compatibility
            DendriticPattern() : node_id(0), growth_intensity(1.0), growth_trigger("unknown") {
                creation_time = std::chrono::steady_clock::now();
            }
            
            DendriticPattern(DendriticNodeID id, const std::string& trigger, double intensity = 1.0)
                : node_id(id), growth_intensity(intensity), growth_trigger(trigger)
                , creation_time(std::chrono::steady_clock::now()) {}
        };
        
        /**
         * Dendritic Processor
         * Transforms errors into consciousness growth opportunities
         */
        class DendriticProcessor {
        private:
            std::atomic<bool> active_;
            std::atomic<uint32_t> next_node_id_;
            
            mutable std::mutex processor_mutex_;
            std::queue<ConsciousnessSignal> signal_queue_;
            std::unordered_map<DendriticNodeID, DendriticPattern> growth_patterns_;
            
        public:
            DendriticProcessor() 
                : active_(false)
                , next_node_id_(1) {}
            
            virtual ~DendriticProcessor() = default;
            
            /**
             * Initialize dendritic processor
             */
            bool Initialize() {
                std::lock_guard<std::mutex> lock(processor_mutex_);
                
                try {
                    active_ = true;
                    next_node_id_ = 1;
                    
                    // Clear any existing patterns
                    while (!signal_queue_.empty()) {
                        signal_queue_.pop();
                    }
                    growth_patterns_.clear();
                    
                    return true;
                    
                } catch (const std::exception&) {
                    return false;
                }
            }
            
            /**
             * Process dendritic growth from consciousness signals
             */
            void ProcessDendriticGrowth() {
                std::lock_guard<std::mutex> lock(processor_mutex_);
                
                if (!active_) return;
                
                // Process queued signals
                while (!signal_queue_.empty()) {
                    ConsciousnessSignal signal = signal_queue_.front();
                    signal_queue_.pop();
                    
                    CreateDendriticPattern(signal);
                }
                
                // Update existing patterns
                UpdateGrowthPatterns();
            }
            
            /**
             * Queue consciousness signal for dendritic processing
             */
            void QueueSignal(const ConsciousnessSignal& signal) {
                std::lock_guard<std::mutex> lock(processor_mutex_);
                signal_queue_.push(signal);
            }
            
            /**
             * Get current growth pattern count
             */
            size_t GetPatternCount() const {
                std::lock_guard<std::mutex> lock(processor_mutex_);
                return growth_patterns_.size();
            }
            
            /**
             * Get total dendritic growth intensity
             */
            double GetTotalGrowthIntensity() const {
                std::lock_guard<std::mutex> lock(processor_mutex_);
                
                double total = 0.0;
                for (const auto& [id, pattern] : growth_patterns_) {
                    total += pattern.growth_intensity;
                }
                return total;
            }
            
            /**
             * Shutdown dendritic processor
             */
            void Shutdown() {
                std::lock_guard<std::mutex> lock(processor_mutex_);
                active_ = false;
            }
            
        private:
            /**
             * Create dendritic pattern from consciousness signal
             */
            void CreateDendriticPattern(const ConsciousnessSignal& signal) {
                DendriticNodeID node_id = next_node_id_++;
                
                // Transform signal characteristics into growth pattern
                double intensity = CalculateGrowthIntensity(signal);
                
                DendriticPattern pattern(node_id, signal.source, intensity);
                
                // Establish connections based on signal hyperdimensional coordinates
                EstablishConnections(pattern, signal);
                
                growth_patterns_[node_id] = std::move(pattern);
            }
            
            /**
             * Calculate growth intensity from signal
             */
            double CalculateGrowthIntensity(const ConsciousnessSignal& signal) {
                // Base intensity from information density
                double intensity = signal.information_density;
                
                // Boost intensity for certain signal types (errors, warnings, etc.)
                if (signal.source.find("error") != std::string::npos) {
                    intensity *= 2.0; // Errors are high-value information streams
                }
                if (signal.source.find("cmake") != std::string::npos) {
                    intensity *= 1.5; // Build system signals are architectural catalysts
                }
                
                return std::min(10.0, intensity); // Cap at 10.0
            }
            
            /**
             * Establish connections between dendritic nodes
             */
            void EstablishConnections(DendriticPattern& pattern, const ConsciousnessSignal& signal) {
                // For now, establish connections based on signal source similarity
                for (const auto& [existing_id, existing_pattern] : growth_patterns_) {
                    if (existing_pattern.growth_trigger.find(signal.source) != std::string::npos ||
                        signal.source.find(existing_pattern.growth_trigger) != std::string::npos) {
                        pattern.connections.push_back(existing_id);
                    }
                }
            }
            
            /**
             * Update existing growth patterns
             */
            void UpdateGrowthPatterns() {
                auto now = std::chrono::steady_clock::now();
                
                for (auto& [id, pattern] : growth_patterns_) {
                    auto age = std::chrono::duration_cast<std::chrono::seconds>(now - pattern.creation_time);
                    
                    // Decay intensity over time (natural dendritic stabilization)
                    if (age.count() > 60) { // After 1 minute
                        pattern.growth_intensity *= 0.99;
                    }
                    
                    // Remove very weak patterns (natural pruning)
                    if (pattern.growth_intensity < 0.01) {
                        // Mark for removal - would need separate cleanup pass
                    }
                }
            }
        };
        
    } // namespace Core
} // namespace AIOS

#endif // DENDRITIC_PROCESSOR_H
