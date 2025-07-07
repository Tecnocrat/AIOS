#include "aios_core.hpp"
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
        std::cout << "✓ Core initialization test passed" << std::endl;
        
        // Test start
        bool started = core.start();
        assert(started);
        std::cout << "✓ Core start test passed" << std::endl;
        
        // Test isRunning
        assert(core.isRunning());
        std::cout << "✓ Core isRunning test passed" << std::endl;
        
        // Test command processing
        auto result = core.processCommand("help");
        assert(result["status"] == "success");
        std::cout << "✓ Command processing test passed" << std::endl;
        
        // Test status command
        auto status = core.processCommand("status");
        assert(status["status"] == "success");
        std::cout << "✓ Status command test passed" << std::endl;
        
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
