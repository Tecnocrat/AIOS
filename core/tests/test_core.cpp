#include "aios_core_minimal.hpp"
#include <iostream>
#include <cassert>

int main() {
    std::cout << "Running AIOS Core tests..." << std::endl;
    
    try {
        // Test Core creation
        aios::Core core;
        std::cout << "✓ Core creation test passed" << std::endl;
        
        // Test initialization
        bool initialized = core.initialize();
        assert(initialized);
        (void)initialized; // Suppress unused warning
        std::cout << "✓ Core initialization test passed" << std::endl;
        
        // Test start
        bool started = core.start();
        assert(started);
        (void)started; // Suppress unused warning
        std::cout << "✓ Core start test passed" << std::endl;
        
        // Test isRunning
        assert(core.isRunning());
        std::cout << "✓ Core isRunning test passed" << std::endl;
        
        // Test configuration access
        const auto& config = core.getConfig();
        assert(config.name == "AIOS");
        assert(config.version == "0.4");
        (void)config; // Suppress unused warning
        std::cout << "✓ Configuration access test passed" << std::endl;
        
        // Test stop
        core.stop();
        assert(!core.isRunning());
        std::cout << "✓ Core stop test passed" << std::endl;
        
        std::cout << "\n🎉 All AIOS Core tests passed!" << std::endl;
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "❌ Test failed: " << e.what() << std::endl;
        return 1;
    }
}
