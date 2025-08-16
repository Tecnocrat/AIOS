// Simple BMP writing utility (24-bit) for tachyonic visualization outputs
#pragma once
#include <cstdint>
#include <string>
namespace aios::io {
    // Writes RGBA buffer (top-down) as 24-bit BMP (bottom-up stored). Alpha is discarded.
    bool write_bmp_rgba(const std::string& path, const uint8_t* rgba, uint32_t width, uint32_t height);
}
#pragma once
#include <cstdint>
#include <vector>
#include <string>

namespace aios::io {
bool write_bmp_rgba(const std::string& path, const uint8_t* rgba, uint32_t width, uint32_t height);
}
