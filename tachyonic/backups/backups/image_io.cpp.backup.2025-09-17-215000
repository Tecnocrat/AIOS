#include "image_io.hpp"
#include <fstream>
#include <cstring>

namespace aios::io {
#pragma pack(push,1)
struct BMPFileHeader { uint16_t bfType{0x4D42}; uint32_t bfSize{0}; uint16_t bfReserved1{0}; uint16_t bfReserved2{0}; uint32_t bfOffBits{54}; };
struct BMPInfoHeader { uint32_t biSize{40}; int32_t biWidth{0}; int32_t biHeight{0}; uint16_t biPlanes{1}; uint16_t biBitCount{24}; uint32_t biCompression{0}; uint32_t biSizeImage{0}; int32_t biXPelsPerMeter{0}; int32_t biYPelsPerMeter{0}; uint32_t biClrUsed{0}; uint32_t biClrImportant{0}; };
#pragma pack(pop)

bool write_bmp_rgba(const std::string& path, const uint8_t* rgba, uint32_t width, uint32_t height) {
    if(!rgba || width==0 || height==0) return false;
    const uint32_t rowStride = ((width * 3 + 3) / 4) * 4; // 4-byte aligned
    BMPFileHeader fh; BMPInfoHeader ih; ih.biWidth = (int32_t)width; ih.biHeight = (int32_t)height; ih.biSizeImage = rowStride * height; fh.bfOffBits = 54; fh.bfSize = fh.bfOffBits + ih.biSizeImage;
    std::ofstream out(path, std::ios::binary); if(!out) return false;
    out.write(reinterpret_cast<const char*>(&fh), sizeof(fh));
    out.write(reinterpret_cast<const char*>(&ih), sizeof(ih));
    std::vector<uint8_t> row(rowStride);
    for(uint32_t y=0; y<height; ++y){
        const uint8_t* src = rgba + (height-1-y)*width*4; // BMP bottom-up
        for(uint32_t x=0; x<width; ++x){
            row[x*3+0] = src[x*4+0]; // B
            row[x*3+1] = src[x*4+1]; // G
            row[x*3+2] = src[x*4+2]; // R
        }
        out.write(reinterpret_cast<const char*>(row.data()), rowStride);
    }
    return true;
}

} // namespace aios::io
