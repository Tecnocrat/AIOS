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

            // AINLP Command Processing with Universal Quantum Holographic Integration
            if (input.find("@AIOS /refresh.context") == 0) {
                std::cout << "🧠 Processing AINLP /refresh.context with Universal Quantum Holographic paradigms..." << std::endl;

                // Extract refinement parameters if present
                std::string refinement = "";
                size_t refPos = input.find("(refinement");
                if (refPos != std::string::npos) {
                    size_t startQuote = input.find("\"", refPos);
                    size_t endQuote = input.find("\"", startQuote + 1);
                    if (startQuote != std::string::npos && endQuote != std::string::npos) {
                        refinement = input.substr(startQuote + 1, endQuote - startQuote - 1);
                    }
                }

                // Process with Universal → Quantum → Holographic integration
                auto result = core.processAINLPUniversalIntegration(input, refinement);

                std::cout << "✅ Universal Layer: " << result.universalResponse << std::endl;
                std::cout << "🌀 Quantum State: " << (result.quantumState.tachyonicActive ? "Active" : "Standby") << std::endl;
                std::cout << "🔮 Holographic Coherence: " << result.fractalCoherence << std::endl;
                std::cout << "🎯 Integration Status: " << (result.integrationSuccessful ? "SUCCESS" : "PENDING") << std::endl;

                continue;
            }

            // Standard holographic processing for other commands
            if (input == "help") {
                std::cout << "Available commands:" << std::endl;
                std::cout << "  @AIOS /refresh.context - AINLP context refresh with fractal paradigms" << std::endl;
                std::cout << "  quantum - Show quantum processing state" << std::endl;
                std::cout << "  holographic - Show holographic system state" << std::endl;
                std::cout << "  universal - Show universal system configuration" << std::endl;
                std::cout << "  status - Show overall system status" << std::endl;
                std::cout << "  help - Show this help message" << std::endl;
                std::cout << "  exit/quit - Exit the system" << std::endl;
                continue;
            }

            // Universal Quantum Holographic status commands
            if (input == "quantum") {
                auto state = core.getUniversalQuantumHolographicState();
                std::cout << "🌀 Quantum Processing State:" << std::endl;
                std::cout << "  Tachyonic Fields: " << (state.quantumState.tachyonicActive ? "Active" : "Standby") << std::endl;
                std::cout << "  Hyperdimensional Coupling: " << state.quantumState.hyperdimensionalFields.size() << " dimensions" << std::endl;
                std::cout << "  Synthetic Physical Laws: " << state.quantumState.syntheticPhysicalLaws.size() << " constants" << std::endl;
                continue;
            }

            if (input == "holographic") {
                auto state = core.getUniversalQuantumHolographicState();
                std::cout << "🔮 Holographic System State:" << std::endl;
                std::cout << "  Fractal Coherence: " << state.fractalCoherence << std::endl;
                std::cout << "  Component States: " << state.holographicContext.ComponentStates.size() << " active" << std::endl;
                std::cout << "  Distributed Intelligence: " << (state.integrationSuccessful ? "Synchronized" : "Synchronizing") << std::endl;
                continue;
            }

            if (input == "universal") {
                std::cout << "🌌 Universal System Configuration:" << std::endl;
                std::cout << "  Operating Paradigm: AI-Driven Intelligence OS" << std::endl;
                std::cout << "  Cross-Component Integration: C++/Python/C# Bridge Active" << std::endl;
                std::cout << "  System Scope: Complete OS Replacement Architecture" << std::endl;
                continue;
            }

            if (input == "status") {
                auto state = core.getUniversalQuantumHolographicState();
                std::cout << "🎯 AIOS Universal Quantum Holographic Status:" << std::endl;
                std::cout << "  Universal Layer: ✅ Operational" << std::endl;
                std::cout << "  Quantum Layer: " << (state.quantumState.tachyonicActive ? "✅" : "⏸️") << " " <<
                    (state.quantumState.tachyonicActive ? "Active" : "Standby") << std::endl;
                std::cout << "  Holographic Layer: " << (state.integrationSuccessful ? "✅" : "🔄") << " " <<
                    (state.integrationSuccessful ? "Synchronized" : "Synchronizing") << std::endl;
                std::cout << "  Fractal Coherence: " << (state.fractalCoherence > 0.8 ? "✅" : "⚠️") << " " << state.fractalCoherence << std::endl;
                std::cout << "  Overall Integration: " << (state.integrationSuccessful ? "🟢 OPTIMAL" : "🟡 ACTIVE") << std::endl;
                continue;
            }

            try {
                auto response = core.processCommand(input);
                std::cout << response.dump(2) << std::endl;
            }
            catch (const std::exception& e) {
                std::cerr << "Error processing command: " << e.what() << std::endl;
            }
        }

        std::cout << "Shutting down AIOS system..." << std::endl;
        core.stop();
        std::cout << "AIOS system stopped" << std::endl;

    }
    catch (const std::exception& e) {
        std::cerr << "Fatal error: " << e.what() << std::endl;
        return 1;
    }
    catch (...) {
        std::cerr << "Unknown fatal error occurred" << std::endl;
        return 1;
    }

    return 0;
}
