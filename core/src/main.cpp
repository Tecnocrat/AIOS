#include "aios_core.hpp"
#include <iostream>
#include <fstream>
#include <stdexcept>

int main(int argc, char* argv[]) {
    try {
        std::cout << "AIOS - Artificial Intelligence Operating System" << std::endl;
        std::cout << "Version 1.0.0" << std::endl;
        std::cout << "Initializing system..." << std::endl;

        // Parse command line arguments
        std::string configPath = "config/system.json";
        if (argc > 1) {
            configPath = argv[1];
        }

        // Create and initialize the core system
        aios::Core core(configPath);
        
        if (!core.initialize()) {
            std::cerr << "Failed to initialize AIOS core system" << std::endl;
            return 1;
        }

        std::cout << "System initialized successfully" << std::endl;
        
        // Start the system
        if (!core.start()) {
            std::cerr << "Failed to start AIOS system" << std::endl;
            return 1;
        }

        std::cout << "AIOS system started successfully" << std::endl;
        std::cout << "Type 'help' for available commands, 'exit' to quit" << std::endl;

        // Main command loop
        std::string input;
        while (core.isRunning()) {
            std::cout << "AIOS> ";
            std::getline(std::cin, input);

            if (input == "exit" || input == "quit") {
                break;
            }

            if (input.empty()) {
                continue;
            }

            try {
                auto response = core.processCommand(input);
                std::cout << response.dump(2) << std::endl;
            } catch (const std::exception& e) {
                std::cerr << "Error processing command: " << e.what() << std::endl;
            }
        }

        std::cout << "Shutting down AIOS system..." << std::endl;
        core.stop();
        std::cout << "AIOS system stopped" << std::endl;

    } catch (const std::exception& e) {
        std::cerr << "Fatal error: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "Unknown fatal error occurred" << std::endl;
        return 1;
    }

    return 0;
}
