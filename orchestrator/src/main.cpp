#include "Logger.hpp"
#include "SingularityCore.hpp"
#include "IPCManager.h"
#include "HealthMonitor.h"
#include "PluginLoader.h"
#include <fstream>
#include <nlohmann/json.hpp>
#include <iostream>

int main() {
    std::string archive_path = "C:/dev/AIOS/orchestrator/archive/";
    std::string log_path = Logger::next_diag_filename("kernel", ".log", archive_path);
    std::string diag_path = Logger::next_diag_filename("diagnostics", ".json", archive_path);

    std::cout << "Log file path: " << log_path << std::endl;
    std::cout << "Diagnostics file path: " << diag_path << std::endl;

    Logger logger(log_path);
    logger.info("Orchestrator starting...");

    // Initialize all modules
    SingularityCore core;
    IPCManager ipcManager;
    HealthMonitor healthMonitor;
    PluginLoader pluginLoader;

    core.initialize();
    ipcManager.initialize();
    healthMonitor.initialize();
    healthMonitor.run();
    pluginLoader.loadPlugins("./plugins"); // TODO: Make path configurable

    // Kernel logic - Enhanced quantum-aware orchestration
    std::cout << "\n=== AIOS Quantum Kernel Loop ===" << std::endl;
    
    // Primary tick with quantum coherence monitoring
    core.tick();
    
    // Enhanced metrics logging
    logger.meta("entropy", std::to_string(core.getEntropy()));
    logger.meta("curvature_at_center", std::to_string(core.getCurvatureAtCenter()));
    logger.meta("coherence_level", std::to_string(core.getCoherenceLevel()));
    logger.meta("quantum_stable", core.isQuantumStable() ? "true" : "false");

    // Diagnostics JSON with tachyonic sync
    nlohmann::json meta;
    meta["status"] = "running";
    meta["entropy"] = core.getEntropy();
    meta["curvature_at_center"] = core.getCurvatureAtCenter();
    meta["health"] = healthMonitor.getStatus();

    // Write initial diagnostics
    std::ofstream meta_out(diag_path);
    if (meta_out.is_open()) {
        meta_out << meta.dump(4);
        meta_out.close();
        std::cout << "Diagnostics written successfully." << std::endl;
    } else {
        std::cout << "Failed to write diagnostics file!" << std::endl;
    }

    // Example IPC usage
    ipcManager.sendMessage("core", "Kernel boot complete");
    std::string msg = ipcManager.receiveMessage("core");
    std::cout << "[Kernel] IPC Received: " << msg << std::endl;

    // Debug UI loop
    std::cout << "AIOS Kernel running. Press 'x' to quit." << std::endl;
    char cmd = 0;
    while (cmd != 'x' && cmd != 'X') {
        std::cout << "[d] Show diagnostics, [l] Show log path, [h] Health status, [x] Quit: ";
        std::cin >> cmd;
        if (cmd == 'd') {
            std::cout << meta.dump(4) << std::endl;
        } else if (cmd == 'l') {
            std::cout << "Log file: " << log_path << std::endl;
        } else if (cmd == 'h') {
            std::cout << "Health: " << healthMonitor.getStatus() << std::endl;
        }
    }

    // Write final diagnostics just before exit
    meta["status"] = "finished";
    meta_out.open(diag_path); // Reuse the same variable
    if (meta_out.is_open()) {
        meta_out << meta.dump(4);
        meta_out.close();
        std::cout << "Final diagnostics written." << std::endl;
    }

    logger.info("Orchestrator finished");
    return 0;
}