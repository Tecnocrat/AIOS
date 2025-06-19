#include "IPCManager.hpp"
#include "Logger.hpp"
#include "SingularityCore.hpp"
#include <memory>
#include <iostream>
#include <fstream>
#include <nlohmann/json.hpp> // If using a JSON library

int main() {
    Logger logger("kernel.log");

    logger.info("Orchestrator started");

    std::unique_ptr<IIPCManager> ipc = std::make_unique<IPCManager>();
    ipc->initialize();
    ipc->sendMessage("system", "Hello, IPC!");
    std::cout << ipc->receiveMessage("system") << std::endl;

    // Example: log entropy and curvature for AI diagnostics
    SingularityCore core;
    core.initialize();
    core.tick();
    logger.meta("entropy", std::to_string(core.getEntropy()));
    logger.meta("curvature_at_center", std::to_string(core.getCurvatureAtCenter()));

    nlohmann::json meta;
    meta["status"] = "started";
    // meta["entropy"] = core.getEntropy(); // Uncomment if core is defined
    std::ofstream meta_out("../archive/diagnostics.json");
    meta_out << meta.dump(4);
    meta_out.close();

    logger.info("Orchestrator finished");
    return 0;
}