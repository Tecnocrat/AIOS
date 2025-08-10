#pragma once
#include <cstdint>

#ifdef _WIN32
extern "C" unsigned __int64 KernelCpuidLeaf0();
#else
inline unsigned long long KernelCpuidLeaf0() { return 0ULL; }
#endif
