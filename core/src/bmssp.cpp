#include "bmssp.hpp"
#include <algorithm>
#include <queue>

namespace aios::graph {

std::pair<double, std::vector<NodeId>> BucketQueue::pull() {
    if (heap.empty()) return {std::numeric_limits<double>::infinity(), {}};
    auto it = std::min_element(heap.begin(), heap.end(),
        [](auto &a, auto &b){ return a.first < b.first; });
    double d = it->first; NodeId v = it->second; heap.erase(it);
    return {d, std::vector<NodeId>{v}};
}

std::pair<std::vector<NodeId>, std::vector<NodeId>>
find_pivots(double /*B*/, const std::vector<NodeId>& S, const Graph& /*G*/,
            const std::vector<double>& /*dist*/, const BMSSPParams& /*params*/) {
    return {S, {}}; // Placeholder: P = S, W = none
}

BMSSPResult base_case(double B, const std::vector<NodeId>& S,
                      const Graph& G, std::vector<double>& dist,
                      const BMSSPParams& params, int recursionLevel) {
    BMSSPResult r; r.metrics.recursionLevel = recursionLevel; r.boundary = B;
    using Pair = std::pair<double, NodeId>;
    std::priority_queue<Pair, std::vector<Pair>, std::greater<Pair>> pq;
    for (auto s : S) {
        if (params.autoSeedSources && dist[s] == std::numeric_limits<double>::infinity())
            dist[s] = 0.0;
        if (dist[s] < B) pq.emplace(dist[s], s);
    }
    std::vector<char> inU(G.size(), 0);
    double minFuture = std::numeric_limits<double>::infinity();
    while (!pq.empty()) {
        auto [dcur, u] = pq.top(); pq.pop();
        if (dcur >= B) { minFuture = std::min(minFuture, dcur); break; }
        if (dcur != dist[u]) continue;
        if (inU[u]) continue;
        inU[u] = 1; r.metrics.settled++; r.settled.push_back(u);
        for (auto &e : G[u]) {
            double nd = dcur + e.w;
            if (nd < dist[e.to] && nd < B) {
                dist[e.to] = nd; pq.emplace(nd, e.to);
            } else if (nd < minFuture) {
                minFuture = nd;
            }
        }
    }
    if (minFuture < B) r.boundary = minFuture;
    return r;
}

BMSSPResult bmssp(int l, double B, const std::vector<NodeId>& S,
                  const Graph& G, std::vector<double>& dist,
                  const BMSSPParams& params, int recursionLevel) {
    if (l <= 0) return base_case(B, S, G, dist, params, recursionLevel);

    auto [P, W] = find_pivots(B, S, G, dist, params);
    BucketQueue D; D.initialize(static_cast<size_t>(1ULL << ((l-1)*params.t)), B);
    for (auto x : P) {
        if (params.autoSeedSources && dist[x] == std::numeric_limits<double>::infinity())
            dist[x] = 0.0;
        if (dist[x] < B) D.insert(x, dist[x]);
    }

    std::vector<NodeId> U; U.reserve(P.size()*2);
    std::vector<double> boundaryCandidates;
    BMSSPMetrics agg; agg.recursionLevel = recursionLevel;
    size_t limit = static_cast<size_t>(params.k) * (1ULL << (l*params.t));

    while (U.size() < limit && !D.empty()) {
        agg.pulls++;
        auto [Bi, Si] = D.pull();
        if (Si.empty()) break;
        auto sub = bmssp(l-1, Bi, Si, G, dist, params, recursionLevel+1);
        boundaryCandidates.push_back(sub.boundary);
        U.insert(U.end(), sub.settled.begin(), sub.settled.end());
        agg.relaxations += sub.metrics.relaxations;
        agg.inserts += sub.metrics.inserts;
        agg.batchPrepends += sub.metrics.batchPrepends;
        agg.settled += sub.metrics.settled;

        std::vector<std::pair<NodeId,double>> K;
        for (auto u : sub.settled) {
            double du = dist[u];
            for (auto &e : G[u]) {
                double nd = du + e.w;
                if (nd < dist[e.to] && nd < B) {
                    dist[e.to] = nd;
                    if (nd >= Bi) { D.insert(e.to, nd); agg.inserts++; }
                    else { K.emplace_back(e.to, nd); }
                    agg.relaxations++;
                }
            }
        }
        if (!K.empty()) { D.batchPrepend(K); agg.batchPrepends++; }
    }

    double Bprime = B;
    for (double c : boundaryCandidates) if (c < Bprime) Bprime = c;
    for (auto x : W) if (dist[x] < Bprime) U.push_back(x);

    BMSSPResult result; result.boundary = Bprime; result.settled = std::move(U); result.metrics = agg; return result;
}

} // namespace aios::graph
