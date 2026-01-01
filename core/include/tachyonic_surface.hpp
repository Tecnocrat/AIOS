#pragma once
#include <cstdint>
#include <vector>
#include <string>
#include <functional>

namespace aios::tachyonic {

struct Point3D { float x; float y; float z; };

// Height map sample container (z is elevation)
struct HeightMap {
    std::vector<Point3D> points; // normalized x,y in [0,1], z elevation [-1,1]
    uint32_t width {0};
    uint32_t height {0};
};

// Generates a simple temporal X(time), Y(distance from core), Z(elevation = magnitude) mapping.
// 'core_distance_fn' computes normalized distance-from-core for an event.
HeightMap build_height_map(
    const std::vector<float>& magnitudes,
    const std::function<float(size_t /*index*/)> &core_distance_fn,
    uint32_t columns,
    uint32_t rows
);

// Assembly renderer interface (implemented in tachyonic_surface.asm)
// Renders height map to 32-bit BGRA pixel buffer using orthographic projection.
extern "C" void __stdcall aios_render_heightmap_ortho(
    const float* pointsXYZ, // interleaved x,y,z (normalized x,y in [0,1], z in [-1,1])
    uint32_t pointCount,
    uint8_t* pixelBuffer,
    uint32_t width,
    uint32_t height,
    float zScale,
    uint32_t baseColor // 0xAARRGGBB
);

} // namespace aios::tachyonic
