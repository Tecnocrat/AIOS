// bmssp.hpp - Initial high-abstraction BMSSP (Bounded Multi-Source Shortest Path) interface
// Purpose: Mutation-friendly, instrumentable scaffold. Future optimizations can
// replace internal data structures without changing external API semantics.

#pragma once
#include <vector>
#include <cstdint>
#include <limits>
#include <utility>
#include <optional>
#include <functional>
#include <string>

namespace aios::graph {

using NodeId = uint32_t;

struct Edge { NodeId to; double w; };
using Graph = std::vector<std::vector<Edge>>; // adjacency list

struct BMSSPMetrics {
    int recursionLevel = 0;
    size_t pulls = 0;
    size_t inserts = 0;
    size_t batchPrepends = 0;
    size_t relaxations = 0;
    size_t settled = 0;
};

struct BMSSPParams {
    int t = 1;     // pivot growth exponent
    int k = 2;     // size threshold factor
    bool autoSeedSources = true; // seed dist[source]=0 if infinity
};

struct BMSSPResult {
    double boundary = std::numeric_limits<double>::infinity();
    std::vector<NodeId> settled; // U
    BMSSPMetrics metrics;        // aggregated metrics (root-level call)
};

class BucketQueue {
public:
    void initialize(std::size_t /*M*/, double /*B*/) {/* future bucket logic */}
    bool empty() const { return heap.empty(); }
    void insert(NodeId v, double d) { heap.emplace_back(d, v); }
    std::pair<double, std::vector<NodeId>> pull();
    void batchPrepend(const std::vector<std::pair<NodeId,double>>& items) {
        for (auto &p : items) insert(p.first, p.second);
    }
private:
    std::vector<std::pair<double,NodeId>> heap; // (dist, node)
};

inline std::vector<double> make_distance_array(const Graph& G) {
    return std::vector<double>(G.size(), std::numeric_limits<double>::infinity());
}

std::pair<std::vector<NodeId>, std::vector<NodeId>>
find_pivots(double B, const std::vector<NodeId>& S, const Graph& G,
            const std::vector<double>& dist, const BMSSPParams& params);

BMSSPResult base_case(double B, const std::vector<NodeId>& S,
                      const Graph& G, std::vector<double>& dist,
                      const BMSSPParams& params, int recursionLevel);

BMSSPResult bmssp(int l, double B, const std::vector<NodeId>& S,
                  const Graph& G, std::vector<double>& dist,
                  const BMSSPParams& params, int recursionLevel = 0);

} // namespace aios::graph
