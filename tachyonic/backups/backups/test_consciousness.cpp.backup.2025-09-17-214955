// Test consciousness system compilation
#include "AIOrchestrationController.hpp"
#include "CenterGeometryField.hpp"
#include "SingularityCore.hpp"
#include "AtomicHolographyUnit.hpp"
#include "AIOSConsciousnessEngine.hpp"
#include <memory>
#include <iostream>

int main() {
    std::cout << " Testing AIOS Consciousness System..." << std::endl;
    
    try {
        // Test core components
        AtomicHolographyUnit quantum_unit;
        CenterGeometryField geometry_field;
        SingularityCore core;
        
        // Test consciousness engine
        auto& consciousness = AIOSConsciousnessEngine::getInstance();
        consciousness.initialize(&core);
        
        // Test AI orchestration controller
        auto ai_controller = std::make_unique<AIOrchestrationController>();
        ai_controller->initialize(&quantum_unit, &core);
        
        // Test integration
        geometry_field.synchronizeWithQuantumField(quantum_unit);
        geometry_field.integrateAIFeedback(*ai_controller);
        
        // Test consciousness levels
        double consciousness_level = ai_controller->getConsciousnessLevel();
        double intelligence_coherence = ai_controller->getIntelligenceCoherence();
        
        std::cout << " Consciousness Level: " << consciousness_level << std::endl;
        std::cout << " Intelligence Coherence: " << intelligence_coherence << std::endl;
        std::cout << " All consciousness tests passed!" << std::endl;
        
        return 0;
    } catch (const std::exception& e) {
        std::cerr << " Consciousness test failed: " << e.what() << std::endl;
        return 1;
    }
}
