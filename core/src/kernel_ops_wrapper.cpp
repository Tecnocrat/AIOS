#include "kernel_ops.hpp"
#include <string>

namespace aios::kernel {
    std::string vendor_probe() {
    #ifdef _WIN32
        // Call minimal leaf 0 to ensure path is wired; value itself is not used here
        (void)KernelCpuidLeaf0();
        return "cpuid-ok";
    #else
        return "unsupported";
    #endif
    }
}
