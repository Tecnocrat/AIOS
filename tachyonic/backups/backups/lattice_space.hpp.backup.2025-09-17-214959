// lattice_space.hpp - Pseudo 3D / N-D lattice scaffolding for AIOS Core
// Purpose: Provide a synthetic "bosonic layer" embedding for graph algorithms
// (e.g., BMSSP) and an upgrade path toward higher-dimensional exploratory
// geometries + visualization export (JSON / OBJ) without locking into a heavy
// renderer dependency.
//
// Design Principles:
// 1. Mutation Surface: Keep internal storage simple (vectors) so future quantum /
//    field-inspired refinements can replace energy models or neighbor topology.
// 2. Dimensional Abstraction: Support arbitrary dimensionality (>=1) but offer
//    fast path helpers for 3D usage.
// 3. Export Hooks: Provide self-describing JSON and minimal OBJ for external
//    visualization or ML ingestion.
// 4. Bosonic Layer Semantics: Each lattice node can hold zero or more BosonicMode
//    entries representing vibrational / energy quanta. Initial scaffold keeps
//    only energy & frequency; future work can add coupling tensors.

#pragma once
#include <vector>
#include <cstdint>
#include <string>
#include <limits>
#include <optional>
#include <functional>

#include <nlohmann/json.hpp>
#include "bmssp.hpp" // for Graph mapping

namespace aios::lattice {

using NodeId = uint32_t;

struct BosonicMode {
    double energy = 0.0;      // abstract energy unit
    double frequency = 0.0;   // Hz or normalized
};

struct LatticeNode {
    NodeId id = 0;
    std::vector<double> coord;      // N-D coordinate
    std::vector<BosonicMode> modes; // local bosonic excitations
};

// Simple lattice space: hyper-rect grid; adjacency uses Manhattan neighbors
// (one step +/- along each dimension). Edge weight function defaults to 1.0 or
// custom functor (receives nodeA, nodeB, axisDeltaIndex).
class LatticeSpace {
public:
    LatticeSpace() = default;
    LatticeSpace(std::vector<size_t> extents) : extents_(std::move(extents)) {
        dimension_ = extents_.size();
    }

    // Generate nodes & edges; optionally attach a seed mode generator.
    void generate(const std::function<BosonicMode(const std::vector<double>&)>& modeGen = nullptr,
                  const std::function<double(const LatticeNode&, const LatticeNode&, size_t axis)>& weightFn = nullptr) {
        nodes_.clear(); edgesFrom_.clear();
        if (dimension_ == 0) return;
        // Precompute strides for linear index mapping.
        strides_.assign(dimension_, 1);
        for (size_t i = 1; i < dimension_; ++i) strides_[i] = strides_[i-1] * extents_[i-1];
        size_t total = 1; for (auto e : extents_) total *= e;
        nodes_.reserve(total); edgesFrom_.resize(total);
        // Create nodes.
        for (size_t linear = 0; linear < total; ++linear) {
            std::vector<double> coord(dimension_);
            size_t rem = linear;
            for (size_t d = 0; d < dimension_; ++d) {
                size_t idx = (rem / strides_[d]) % extents_[d];
                coord[d] = static_cast<double>(idx);
            }
            LatticeNode n; n.id = static_cast<NodeId>(linear); n.coord = std::move(coord);
            if (modeGen) n.modes.push_back(modeGen(n.coord));
            nodes_.push_back(std::move(n));
        }
        // Connect neighbors (Manhattan)
        for (size_t linear = 0; linear < total; ++linear) {
            const auto &n = nodes_[linear];
            for (size_t d = 0; d < dimension_; ++d) {
                size_t idx = static_cast<size_t>(n.coord[d]);
                if (idx + 1 < extents_[d]) {
                    size_t neighborLinear = linear + strides_[d];
                    const auto &m = nodes_[neighborLinear];
                    double w = weightFn ? weightFn(n,m,d) : 1.0;
                    edgesFrom_[linear].push_back({static_cast<NodeId>(m.id), w});
                    edgesFrom_[neighborLinear].push_back({static_cast<NodeId>(n.id), w}); // undirected
                }
            }
        }
    }

    size_t dimension() const { return dimension_; }
    const std::vector<size_t>& extents() const { return extents_; }
    const std::vector<LatticeNode>& nodes() const { return nodes_; }

    // Build a BMSSP-compatible graph snapshot (copy edges). Mutation path: later could provide a view.
    aios::graph::Graph toGraph() const {
        aios::graph::Graph G(nodes_.size());
        for (size_t i=0;i<edgesFrom_.size();++i) {
            for (auto &e : edgesFrom_[i]) {
                G[i].push_back({e.to, e.w});
            }
        }
        return G;
    }

    // Export JSON structure with nodes + optional modes & edges.
    nlohmann::json to_json(bool includeModes=true, bool includeEdges=true) const {
        nlohmann::json j;
        j["dimension"] = dimension_;
        j["extents"] = extents_;
        j["nodes"] = nlohmann::json::array();
        for (auto &n : nodes_) {
            nlohmann::json nj;
            nj["id"] = n.id;
            nj["coord"] = n.coord;
            if (includeModes) {
                nlohmann::json modes = nlohmann::json::array();
                for (auto &m : n.modes) modes.push_back({{"energy", m.energy}, {"frequency", m.frequency}});
                nj["modes"] = modes;
            }
            j["nodes"].push_back(std::move(nj));
        }
        if (includeEdges) {
            j["edges"] = nlohmann::json::array();
            for (size_t i=0;i<edgesFrom_.size();++i) {
                for (auto &e : edgesFrom_[i]) {
                    if (i < static_cast<size_t>(e.to)) // avoid duplicating undirected edge
                        j["edges"].push_back({i, e.to, e.w});
                }
            }
        }
        return j;
    }

    // Minimal OBJ export (3D only). Higher D: project first 3 coords.
    std::string to_obj() const {
        std::string out; out.reserve(nodes_.size()*32);
        for (auto &n : nodes_) {
            double x = n.coord.size() > 0 ? n.coord[0] : 0.0;
            double y = n.coord.size() > 1 ? n.coord[1] : 0.0;
            double z = n.coord.size() > 2 ? n.coord[2] : 0.0;
            out += "v " + std::to_string(x) + " " + std::to_string(y) + " " + std::to_string(z) + "\n";
        }
        // Lines for edges
        for (size_t i=0;i<edgesFrom_.size();++i) {
            for (auto &e : edgesFrom_[i]) if (i < static_cast<size_t>(e.to)) {
                out += "l " + std::to_string(i+1) + " " + std::to_string(e.to+1) + "\n";
            }
        }
        return out;
    }

private:
    struct RawEdge { NodeId to; double w; };
    size_t dimension_ = 0;
    std::vector<size_t> extents_;
    std::vector<size_t> strides_;
    std::vector<LatticeNode> nodes_;
    std::vector<std::vector<RawEdge>> edgesFrom_;
};

// Convenience: run BMSSP over lattice starting from provided sources.
inline aios::graph::BMSSPResult run_bmssp_on_lattice(LatticeSpace &space,
                                                     const std::vector<NodeId>& sources,
                                                     int recursionLevel, double B,
                                                     const aios::graph::BMSSPParams& bparams) {
    auto G = space.toGraph();
    auto dist = aios::graph::make_distance_array(G);
    return aios::graph::bmssp(recursionLevel, B, sources, G, dist, bparams);
}

} // namespace aios::lattice
