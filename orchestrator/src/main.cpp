#include "Logger.hpp"
#include "SingularityCore.hpp"
#include <fstream>
#include <nlohmann/json.hpp>

int main() {
    Logger logger; // Will auto-create kernel_N.log in ../archive/

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

    std::ofstream meta_out(Logger::next_diag_filename());
    meta_out << meta.dump(4);
    meta_out.close();

    logger.info("Orchestrator finished");
    return 0;
}