#include "kernel_ops.hpp"
#include <iostream>
#include <vector>
#include <cassert>

using namespace aios::kernel;

int main() {
    std::cout << "Running kernel_ops extended test..." << std::endl;
    auto info = query_vendor();
    std::cout << "Vendor: " << info.vendor << " maxLeaf=" << info.maxLeaf << std::endl;

    // Feature sampling (basic leaves 0..min(4,maxLeaf))
    std::vector<std::pair<unsigned,unsigned>> q;
    for (unsigned l=0; l < 5 && l <= info.maxLeaf; ++l) q.emplace_back(l,0);
    auto features = sample_feature_block(q);
    std::cout << "Collected leaves: " << features.size() << std::endl;

    // Cycle counters
    unsigned aux = 0;
    auto c1 = monotonic_cycles();
    auto c2 = monotonic_cycles_serial(aux);
    auto c3 = monotonic_cycles();
    std::cout << "Cycles diff serial/non-serial: " << (c2 - c1) << " / " << (c3 - c2) << std::endl;

    // SIMD add
    std::vector<float> A(16), B(16), O(16, -1.f);
    for (int i=0;i<16;++i) { A[i]=float(i); B[i]=float(2*i); }
    simd_add_f32(A.data(), B.data(), O.data(), (unsigned)O.size());
    for (int i=0;i<16;++i) assert(O[i] == A[i]+B[i]);
    std::cout << "SIMD add validated." << std::endl;

    std::cout << "\n✅ kernel_ops extended test passed." << std::endl;
    return 0;
}
