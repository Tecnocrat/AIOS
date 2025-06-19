#include "Logger.hpp"
#include "SingularityCore.hpp"
#include "IPCManager.h"
#include "HealthMonitor.h"
#include "PluginLoader.h"
#include <fstream>
#include <nlohmann/json.hpp>
#include <iostream>

int main() {
    // Always use the next available log file
    Logger logger(Logger::next_diag_filename("kernel", ".log", "../archive/"));

    logger.info("Orchestrator started");

    SingularityCore core;
    core.initialize();
    core.tick();

    logger.meta("entropy", std::to_string(core.getEntropy()));
    logger.meta("curvature_at_center", std::to_string(core.getCurvatureAtCenter()));

    // Diagnostics JSON with tachyonic sync
    nlohmann::json meta;
    meta["status"] = "finished";
    meta["entropy"] = core.getEntropy();
    meta["curvature_at_center"] = core.getCurvatureAtCenter();

    // Always use the next available diagnostics file
    std::ofstream meta_out(Logger::next_diag_filename("diagnostics", ".json", "../archive/"));
    meta_out << meta.dump(4);
    meta_out.close();

    logger.info("Orchestrator finished");

    std::cout << "[Kernel] Starting AIOS Kernel Core..." << std::endl;

    // Initialize IPC Manager
    IPCManager ipcManager;
    ipcManager.initialize();

    // Initialize Health Monitor
    HealthMonitor healthMonitor;
    healthMonitor.initialize();
    healthMonitor.run();
    std::cout << "[Kernel] Health Status: " << healthMonitor.getStatus() << std::endl;

    // Initialize Plugin Loader
    PluginLoader pluginLoader;
    pluginLoader.loadPlugins("./plugins"); // TODO: Make path configurable

    // TODO: Add static analysis hooks here (e.g., memory checks, thread sanitizer)
    // TODO: Integrate Logger for diagnostics and event tracing

    // Example IPC usage
    ipcManager.sendMessage("core", "Kernel boot complete");
    std::string msg = ipcManager.receiveMessage("core");
    std::cout << "[Kernel] IPC Received: " << msg << std::endl;

    // TODO: Main event loop and graceful shutdown logic

    return 0;
}