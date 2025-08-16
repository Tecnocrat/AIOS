#include "tachyonic_surface.hpp"
#include <vector>
#include <fstream>
#include <iostream>
#include <cstdint>
#include <cstdlib>
#include <filesystem>
#include <chrono>
#include <thread>
#include <atomic>
#ifdef _WIN32
#include <conio.h>
#endif
#include "image_io.hpp"

using namespace aios::tachyonic;

// Simple demo: generate synthetic magnitude data (sine wave + noise) and distance profile.
int main(int argc, char** argv) {
    const uint32_t cols = 256;
    const uint32_t rows = 8; // layer duplication for now
    std::vector<float> magnitudes(cols);
    for (uint32_t i = 0; i < cols; ++i) {
        float t = static_cast<float>(i) / (cols - 1);
        float wave = std::sin(t * 12.0f) * 0.6f;
        float noise = (static_cast<float>(rand()) / RAND_MAX - 0.5f) * 0.2f;
        magnitudes[i] = wave + noise;
    }

    auto hm = build_height_map(magnitudes, [](size_t idx){
        // distance from core example: closer in middle
        // normalized distance peaks at edges
        const float nf = static_cast<float>(idx);
        return std::abs(0.5f - (nf / 255.0f)) * 2.0f; // 0 center -> 1 edges
    }, cols, rows);

    auto regenerate = [&](float phase){
        // Recompute magnitudes with phase shift to simulate time
        for(uint32_t i=0;i<cols;++i){
            float t = static_cast<float>(i)/(cols-1);
            float wave = std::sin(t*12.0f + phase) * 0.6f;
            float noise = (static_cast<float>(rand())/RAND_MAX - 0.5f)*0.2f;
            magnitudes[i] = wave + noise;
        }
        hm = build_height_map(magnitudes, [](size_t idx){
            const float nf = static_cast<float>(idx);
            return std::abs(0.5f - (nf / 255.0f)) * 2.0f; }, cols, rows);
    };

    const uint32_t outW = 800, outH = 400;
    std::vector<uint8_t> buffer(outW * outH * 4, 0);
    auto colorForZ = [](float z){
        // map -1..1 to gradient (blue->cyan->green->yellow->red)
        float v = std::clamp((z+1.0f)/2.0f, 0.0f, 1.0f);
        float r,g,b;
        if(v < 0.25f){ // blue->cyan
            float t=v/0.25f; r=0; g=t*255; b=255; }
        else if(v<0.5f){ float t=(v-0.25f)/0.25f; r=0; g=255; b=255 - t*255; }
        else if(v<0.75f){ float t=(v-0.5f)/0.25f; r=t*255; g=255; b=0; }
        else { float t=(v-0.75f)/0.25f; r=255; g=255 - t*255; b=0; }
        return (uint32_t(b) | (uint32_t(g)<<8) | (uint32_t(r)<<16) | 0xFF000000u);
    };

    auto renderFrame = [&](float phase){
        regenerate(phase);
        std::vector<float> xyz; xyz.reserve(hm.points.size()*3);
        for(auto &p: hm.points){ xyz.push_back(p.x); xyz.push_back(p.y); xyz.push_back(p.z); }
        std::fill(buffer.begin(), buffer.end(), 0);
        // draw with per-point color based on z
        for(size_t i=0;i<hm.points.size();++i){
            float x=xyz[i*3+0]; float y=xyz[i*3+1]; float z=xyz[i*3+2];
            int px = (int)(x*(outW-1));
            int py = (int)(y*(outH-1));
            if(px>=0 && px<(int)outW && py>=0 && py<(int)outH){
                uint32_t color = colorForZ(z);
                uint8_t* dst = &buffer[(py*outW+px)*4];
                dst[0] = (uint8_t)(color & 0xFF);
                dst[1] = (uint8_t)((color>>8) & 0xFF);
                dst[2] = (uint8_t)((color>>16) & 0xFF);
                dst[3] = 255;
            }
        }
    };

    const int maxFrames = 120; // ~ few seconds of motion
    for(int f=0; f<maxFrames; ++f){
        float phase = f * 0.15f;
        renderFrame(phase);
        // Write a BMP for the last frame only (avoid flooding disk)
        if(f==maxFrames-1){
            aios::io::write_bmp_rgba("tachyonic_surface.bmp", buffer.data(), outW, outH);
        }
#ifdef _WIN32
        if(_kbhit()) { int c=_getch(); if(c=='q' || c==27) break; }
#endif
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }

    // Determine output path (arg0 optional). Default under runtime_intelligence logs for observability.
    std::filesystem::path outPath;
    if(argc > 1) {
        outPath = argv[1];
    } else {
        outPath = std::filesystem::path("..") / ".." / ".." / "runtime_intelligence" / "logs" / "tachyonic_surface.ppm"; // relative from build/bin/Debug
    }
    try {
        std::filesystem::create_directories(outPath.parent_path());
    } catch(...) {
        std::cerr << "Warning: could not ensure directory for output: " << outPath.parent_path() << std::endl;
    }
    // Emit also a final PPM for compatibility
    std::ofstream ppm(outPath, std::ios::binary);
    if(ppm){
        ppm << "P6\n" << outW << " " << outH << "\n255\n";
        for (uint32_t i = 0; i < outW * outH; ++i) {
            uint8_t b = buffer[i*4 + 0];
            uint8_t g = buffer[i*4 + 1];
            uint8_t r = buffer[i*4 + 2];
            ppm.put(r).put(g).put(b);
        }
    }
    std::cout << "Final frame written: " << std::filesystem::absolute(outPath).string() << " and tachyonic_surface.bmp (gradient). Press q earlier to abort." << std::endl;
    return 0;
}
