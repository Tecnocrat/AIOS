// kernel_ops.hpp - Low-level CPU / lattice primitive hooks.
// These functions expose architectural signals upward into the metaphysical
// abstraction layers (runtime intelligence, bosonic lattice, BMSSP evolution).
// They are intentionally broad; higher layers may sample a subset.

#pragma once
#include <cstdint>
#include <array>
#include <string>
#include <vector>

#ifdef _WIN32
extern "C" unsigned __int64 KernelCpuidLeaf0();
extern "C" void KernelCpuidLeaf(unsigned __int32 leaf, unsigned __int32 subleaf,
								 unsigned __int32* eax, unsigned __int32* ebx,
								 unsigned __int32* ecx, unsigned __int32* edx);
extern "C" unsigned __int64 KernelReadTSC();
extern "C" unsigned __int64 KernelReadTSCP(unsigned __int32* aux);
extern "C" void KernelSimdAddF32(const float* a, const float* b, float* out, unsigned __int32 count);
#else
inline unsigned long long KernelCpuidLeaf0() { return 0ULL; }
inline void KernelCpuidLeaf(unsigned, unsigned, unsigned*, unsigned*, unsigned*, unsigned*) {}
inline unsigned long long KernelReadTSC() { return 0ULL; }
inline unsigned long long KernelReadTSCP(unsigned*) { return 0ULL; }
inline void KernelSimdAddF32(const float*, const float*, float*, unsigned) {}
#endif

namespace aios::kernel {

struct CpuVendorInfo {
	std::string vendor;
	unsigned maxLeaf = 0;
};

struct CpuFeatureLeaf {
	unsigned leaf = 0;
	unsigned subleaf = 0;
	unsigned eax = 0, ebx = 0, ecx = 0, edx = 0;
};

CpuVendorInfo query_vendor();
std::vector<CpuFeatureLeaf> sample_feature_block(const std::vector<std::pair<unsigned,unsigned>>& queries);
unsigned long long monotonic_cycles();
unsigned long long monotonic_cycles_serial(unsigned &aux); // rdtscp variant
void simd_add_f32(const float* a, const float* b, float* out, unsigned count);

} // namespace aios::kernel
