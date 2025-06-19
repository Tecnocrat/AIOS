#include <iostream>
#include "SingularityCore.hpp"
#include "FractalSyncBus.hpp"
#include "SphereShellManager.hpp"
#include "SubspaceProjector.hpp"
#include "AtomicHolographyUnit.hpp"
#include "CenterGeometryField.hpp"

// ============================================================
// 🧪 Orchestrator Runtime Protocol
//   “Test the harmony of the hypersphere kernel.”
// ============================================================

int main() {
    std::cout << "=== AIOS Orchestrator Kernel: Runtime Test Protocol ===" << std::endl;

    SingularityCore core;
    FractalSyncBus bus;
    SphereShellManager shells;
    SubspaceProjector projector;
    AtomicHolographyUnit holo;
    CenterGeometryField center;

    // Initialization
    core.initialize();
    bus.initialize();
    shells.bootstrap();
    projector.configure();
    holo.initialize();
    center.initialize();

    std::cout << "[LOG] All modules initialized." << std::endl;

    // Simulate a kernel tick
    core.tick();
    bus.synchronize();
    shells.rotateShells();
    projector.project();
    holo.update();
    center.simulate();

    std::cout << "[LOG] All modules ticked." << std::endl;

    // Query core properties
    std::cout << "Core entropy: " << core.getEntropy() << std::endl;
    std::cout << "Curvature at center: " << core.getCurvatureAtCenter() << std::endl;

    std::cout << "=== Orchestrator Kernel Test Complete ===" << std::endl;
    return 0;
}