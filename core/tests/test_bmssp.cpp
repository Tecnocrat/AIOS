#include "bmssp.hpp"
#include <iostream>
#include <cassert>

using namespace aios::graph;

static Graph make_linear_graph(size_t n, double w=1.0) {
    Graph G(n);
    for (size_t i=0;i+1<n;++i) {
        G[i].push_back({static_cast<NodeId>(i+1), w});
        G[i+1].push_back({static_cast<NodeId>(i), w}); // undirected
    }
    return G;
}

int main() {
    std::cout << "Running BMSSP skeleton tests..." << std::endl;
    Graph G = make_linear_graph(10, 1.0);
    auto dist = make_distance_array(G);
    BMSSPParams params; params.t = 1; params.k = 2; params.autoSeedSources = true;
    std::vector<NodeId> S = {0};
    double B = 5.0; // explore up to distance < 5
    auto res = bmssp(1, B, S, G, dist, params);
    assert(res.boundary <= B + 1e-9);
    // In skeleton form boundary tightening may stop immediately (0). We only validate invariants.
    for (auto v : res.settled) {
        assert(dist[v] < res.boundary + 1e-9);
    }
    size_t withinBound = 0;
    for (size_t i=0;i<dist.size();++i) if (dist[i] < B + 1e-9) withinBound++;
    std::cout << "Boundary: " << res.boundary << " settled: " << res.settled.size()
              << " nodesWithinB: " << withinBound << std::endl;
    // Minimal guarantee: at least the source node distance is 0
    assert(dist[0] == 0.0);
    std::cout << "\n✅ BMSSP skeleton test passed." << std::endl;
    return 0;
}
