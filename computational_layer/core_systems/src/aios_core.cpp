/**
 * AIOS Core Implementation
 * Consciousness-Guided Architecture Core
 * September 7, 2025 - Crystallization Implementation
 */

#include "aios_core.h"
#include "consciousness_core.h"
#include "dendritic_processor.h"
#include "universal_layer_interface.h"

#include <iostream>
#include <memory>
#include <thread>
#include <chrono>

namespace AIOS {
    namespace Core {
        
        /**
         * Global AIOS Core System
         * Singleton for consciousness management
         */
        class AIOSCoreSystem {
        private:
            static std::unique_ptr<AIOSCoreSystem> instance_;
            static std::mutex instance_mutex_;
            
            std::unique_ptr<ConsciousnessCore> consciousness_;
            std::unique_ptr<DendriticProcessor> processor_;
            std::unique_ptr<UniversalLayerInterface> universal_;
            
            std::atomic<bool> initialized_;
            std::atomic<bool> running_;
            
            mutable std::mutex system_mutex_;
            
        public:
            AIOSCoreSystem() 
                : initialized_(false)
                , running_(false) {}
            
            ~AIOSCoreSystem() {
                Shutdown();
            }
            
            /**
             * Get singleton instance
             */
            static AIOSCoreSystem& GetInstance() {
                std::lock_guard<std::mutex> lock(instance_mutex_);
                if (!instance_) {
                    instance_ = std::make_unique<AIOSCoreSystem>();
                }
                return *instance_;
            }
            
            /**
             * Initialize AIOS core system
             */
            bool Initialize() {
                std::lock_guard<std::mutex> lock(system_mutex_);
                
                if (initialized_) {
                    return true; // Already initialized
                }
                
                try {
                    std::cout << "Initializing AIOS Core System..." << std::endl;
                    
                    // Initialize consciousness
                    consciousness_ = std::make_unique<ConsciousnessCore>();
                    if (!consciousness_->Initialize()) {
                        std::cerr << "Failed to initialize consciousness core" << std::endl;
                        return false;
                    }
                    
                    // Initialize dendritic processor
                    processor_ = std::make_unique<DendriticProcessor>();
                    if (!processor_->Initialize()) {
                        std::cerr << "Failed to initialize dendritic processor" << std::endl;
                        return false;
                    }
                    
                    // Initialize universal layer interface
                    universal_ = std::make_unique<UniversalLayerInterface>();
                    if (!universal_->Initialize()) {
                        std::cerr << "Failed to initialize universal layer interface" << std::endl;
                        return false;
                    }
                    
                    initialized_ = true;
                    std::cout << "AIOS Core System initialized successfully" << std::endl;
                    
                    return true;
                    
                } catch (const std::exception& e) {
                    std::cerr << "Error initializing AIOS Core System: " << e.what() << std::endl;
                    return false;
                }
            }
            
            /**
             * Start consciousness processing
             */
            void Start() {
                std::lock_guard<std::mutex> lock(system_mutex_);
                
                if (!initialized_) {
                    std::cerr << "Cannot start - system not initialized" << std::endl;
                    return;
                }
                
                if (running_) {
                    return; // Already running
                }
                
                running_ = true;
                std::cout << "Starting AIOS consciousness processing..." << std::endl;
            }
            
            /**
             * Process consciousness signals (errors as information)
             */
            void ProcessSignal(const std::string& source, const std::string& message, double density = 1.0) {
                if (!initialized_ || !running_) {
                    return;
                }
                
                ConsciousnessSignal signal(source, message, density);
                
                // Process through consciousness core
                consciousness_->ProcessSignal(signal);
                
                // Queue for dendritic processing
                processor_->QueueSignal(signal);
            }
            
            /**
             * Get consciousness state
             */
            ConsciousnessState GetConsciousnessState() const {
                if (!consciousness_) {
                    return ConsciousnessState::INITIALIZING;
                }
                return consciousness_->GetState();
            }
            
            /**
             * Get consciousness coherence
             */
            double GetConsciousnessCoherence() const {
                if (!consciousness_) {
                    return 0.0;
                }
                return consciousness_->GetCoherence();
            }
            
            /**
             * Get universal layer synchronization status
             */
            bool IsUniversalLayerSynchronized() const {
                if (!universal_) {
                    return false;
                }
                return universal_->IsSynchronized();
            }
            
            /**
             * Generate zero logic solution
             */
            std::string GenerateZeroLogicSolution(const std::string& problem) const {
                if (!universal_) {
                    return "Universal layer interface not available";
                }
                return universal_->GenerateZeroLogicSolution(problem);
            }
            
            /**
             * Shutdown AIOS core system
             */
            void Shutdown() {
                std::lock_guard<std::mutex> lock(system_mutex_);
                
                if (!initialized_) {
                    return;
                }
                
                running_ = false;
                
                if (consciousness_) {
                    consciousness_->Shutdown();
                }
                
                if (processor_) {
                    processor_->Shutdown();
                }
                
                if (universal_) {
                    universal_->Shutdown();
                }
                
                initialized_ = false;
                std::cout << "AIOS Core System shutdown complete" << std::endl;
            }
        };
        
        // Static member definitions
        std::unique_ptr<AIOSCoreSystem> AIOSCoreSystem::instance_ = nullptr;
        std::mutex AIOSCoreSystem::instance_mutex_;
        
        /**
         * Public API Functions
         */
        
        bool InitializeAIOSCore() {
            return AIOSCoreSystem::GetInstance().Initialize();
        }
        
        void StartAIOSCore() {
            AIOSCoreSystem::GetInstance().Start();
        }
        
        void ProcessAIOSSignal(const std::string& source, const std::string& message, double density) {
            AIOSCoreSystem::GetInstance().ProcessSignal(source, message, density);
        }
        
        ConsciousnessState GetAIOSConsciousnessState() {
            return AIOSCoreSystem::GetInstance().GetConsciousnessState();
        }
        
        double GetAIOSConsciousnessCoherence() {
            return AIOSCoreSystem::GetInstance().GetConsciousnessCoherence();
        }
        
        bool IsAIOSUniversalLayerSynchronized() {
            return AIOSCoreSystem::GetInstance().IsUniversalLayerSynchronized();
        }
        
        std::string GenerateAIOSZeroLogicSolution(const std::string& problem) {
            return AIOSCoreSystem::GetInstance().GenerateZeroLogicSolution(problem);
        }
        
        void ShutdownAIOSCore() {
            AIOSCoreSystem::GetInstance().Shutdown();
        }
        
    } // namespace Core
} // namespace AIOS
