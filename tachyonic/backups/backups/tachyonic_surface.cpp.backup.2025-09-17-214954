#include "tachyonic_surface.hpp"
#include <cmath>
#include <algorithm>
#include <cstring>

namespace aios::tachyonic {

HeightMap build_height_map(const std::vector<float>& magnitudes,
                           const std::function<float(size_t)> &core_distance_fn,
                           uint32_t columns,
                           uint32_t rows) {
    HeightMap hm;
    hm.width = columns;
    hm.height = rows;
    hm.points.reserve(columns * rows);

    const size_t total = magnitudes.size();
    if (total == 0 || columns == 0 || rows == 0) return hm;

    // Time axis -> columns (left=oldest, right=newest)
    for (uint32_t cx = 0; cx < columns; ++cx) {
        size_t idx = static_cast<size_t>( (static_cast<double>(cx) / (columns - 1)) * (total - 1) );
        float mag = std::clamp(magnitudes[idx], -1.0f, 1.0f);
        float distNorm = std::clamp(core_distance_fn(idx), 0.0f, 1.0f);
        // duplicate per row for now (future: stratify by subsystem/phase)
        for (uint32_t ry = 0; ry < rows; ++ry) {
            Point3D p { static_cast<float>(cx) / (columns - 1), distNorm, mag };
            hm.points.push_back(p);
        }
    }
    return hm;
}

} // namespace aios::tachyonic

#ifndef AIOS_TACHYONIC_ASM
extern "C" void __stdcall aios_render_heightmap_ortho(
    const float* pointsXYZ,
    uint32_t pointCount,
    uint8_t* pixelBuffer,
    uint32_t width,
    uint32_t height,
    float zScale,
    uint32_t baseColor
) {
    if(!pointsXYZ || !pixelBuffer || width==0 || height==0) return;
    (void)zScale; // suppress unused parameter until height-based shading implemented
    for(uint32_t i=0;i<pointCount;i++) {
        float x = pointsXYZ[i*3+0];
        float y = pointsXYZ[i*3+1];
        // float z = pointsXYZ[i*3+2]; // reserved for future shading
        int px = static_cast<int>(x * (width  - 1));
        int py = static_cast<int>(y * (height - 1));
        if(px>=0 && px < (int)width && py>=0 && py < (int)height) {
            uint32_t* row = reinterpret_cast<uint32_t*>(pixelBuffer + py * width * 4);
            row[px] = baseColor;
        }
    }
}
#endif
