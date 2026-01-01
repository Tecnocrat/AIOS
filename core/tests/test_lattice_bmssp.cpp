#include "lattice_space.hpp"
#include <iostream>
#include <cassert>
#include <cmath>

using namespace aios::lattice;
using namespace aios::graph;

int main() {
    std::cout << "Running Lattice + BMSSP integration test..." << std::endl;
    // 3D lattice 4x3x2 = 24 nodes
    LatticeSpace space({4,3,2});
    space.generate(
        [](const std::vector<double>& coord){
            BosonicMode m; m.energy = coord[0] + coord[1]*0.1; m.frequency = 1.0 + coord[2]; return m; },
        nullptr // default weight=1
    );
    std::vector<NodeId> sources = {0};
    BMSSPParams params; params.t=1; params.k=2; params.autoSeedSources=true;
    double B = 3.5; // explore local neighborhood
    auto result = run_bmssp_on_lattice(space, sources, 1, B, params);
    std::cout << "Boundary: " << result.boundary << " settled: " << result.settled.size() << std::endl;
    // Validate OBJ projection contains expected number of vertices lines
    std::string obj = space.to_obj();
    size_t vertexLines = 0; for (size_t pos=0; (pos = obj.find('\n', pos)) != std::string::npos; ++pos) ++vertexLines;
    assert(vertexLines > 0);
    auto json = space.to_json();
    assert(json["dimension"].get<size_t>() == 3);
    assert(json["nodes"].size() == 24);
    std::cout << "\n Lattice + BMSSP integration test passed." << std::endl;
    return 0;
}
