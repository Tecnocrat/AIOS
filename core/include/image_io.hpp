#pragma once
#include <cstdint>
#include <vector>
#include <string>

namespace aios::io {
bool write_bmp_rgba(const std::string& path, const uint8_t* rgba, uint32_t width, uint32_t height);
}
