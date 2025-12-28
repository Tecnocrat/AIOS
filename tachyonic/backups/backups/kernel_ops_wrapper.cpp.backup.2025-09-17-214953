#include "kernel_ops.hpp"
#include <cstring>
#include <chrono>

namespace aios::kernel {

CpuVendorInfo query_vendor() {
#ifdef _WIN32
    unsigned maxLeaf = static_cast<unsigned>(KernelCpuidLeaf0());
    unsigned eax=0, ebx=0, ecx=0, edx=0;
    KernelCpuidLeaf(0, 0, &eax, &ebx, &ecx, &edx);
    char vendor[13];
    std::memcpy(vendor+0, &ebx, 4);
    std::memcpy(vendor+4, &edx, 4);
    std::memcpy(vendor+8, &ecx, 4);
    vendor[12] = '\0';
    return {std::string(vendor), maxLeaf};
#else
    return {"unsupported", 0};
#endif
}

std::vector<CpuFeatureLeaf> sample_feature_block(const std::vector<std::pair<unsigned,unsigned>>& queries) {
    std::vector<CpuFeatureLeaf> out; out.reserve(queries.size());
#ifdef _WIN32
    for (auto [leaf, sub] : queries) {
        CpuFeatureLeaf f; f.leaf = leaf; f.subleaf = sub;
        KernelCpuidLeaf(leaf, sub, &f.eax, &f.ebx, &f.ecx, &f.edx);
        out.push_back(f);
    }
#endif
    return out;
}

unsigned long long monotonic_cycles() {
    return KernelReadTSC();
}

unsigned long long monotonic_cycles_serial(unsigned &aux) {
    return KernelReadTSCP(&aux);
}

void simd_add_f32(const float* a, const float* b, float* out, unsigned count) {
    KernelSimdAddF32(a,b,out,count);
}

} // namespace aios::kernel
