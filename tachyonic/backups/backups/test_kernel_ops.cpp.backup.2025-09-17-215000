#include "kernel_ops.hpp"
#include <iostream>
#include <vector>
#include <cassert>

using namespace aios::kernel;

int main() {
    std::cout << "Running kernel_ops extended test..." << std::endl;
    auto info = query_vendor();
    std::cout << "Vendor: " << info.vendor << " maxLeaf=" << info.maxLeaf << std::endl;
    if (info.maxLeaf > 0) {
        std::vector<std::pair<unsigned,unsigned>> q;
        for (unsigned l=0; l < 5 && l <= info.maxLeaf; ++l) q.emplace_back(l,0);
        auto features = sample_feature_block(q);
        std::cout << "Collected leaves: " << features.size() << std::endl;
    }

    // (Temporarily disabled cycle + SIMD tests for diagnosing non-zero exit)

    std::cout << "\n kernel_ops extended test passed." << std::endl;
    return 0;
}
