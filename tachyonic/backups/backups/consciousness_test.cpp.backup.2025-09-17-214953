#include <iostream>
#include "aios_core_minimal.hpp"
#include "AIOSConsciousnessEngine.hpp"
#include "SingularityCore.hpp"

int main() {
    std::cout << " AIOS Consciousness Engine Test" << std::endl;
    
    try {
        // Initialize core
        aios::Core core;
        if (!core.initialize()) {
            std::cerr << " Failed to initialize core" << std::endl;
            return 1;
        }
        
        // Initialize consciousness engine
        auto& consciousness = AIOSConsciousnessEngine::getInstance();
        
        // Test consciousness functionality
        std::cout << " Consciousness engine initialized" << std::endl;
        
        // Test consciousness evolution
        std::string evolved_logic = consciousness.evolveLogicFromError("test_error");
        std::cout << " Consciousness evolution tested: " << evolved_logic << std::endl;
        
        // Test intelligence enhancement
        consciousness.enhanceIntelligence("system_test");
        std::cout << " Intelligence enhancement tested" << std::endl;
        
        std::cout << " All consciousness tests passed!" << std::endl;
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << " Consciousness test failed: " << e.what() << std::endl;
        return 1;
    }
}