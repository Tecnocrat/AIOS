#pragma once
#include <fstream>
#include <string>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <filesystem>

class Logger {
public:
    Logger(const std::string& base = "kernel", const std::string& ext = ".log", const std::string& dir = "../archive/") {
        std::filesystem::create_directories(dir);
        int idx = get_next_index(base, ext, dir);
        std::ostringstream fname;
        fname << dir << base << "_" << idx << ext;
        log_file.open(fname.str(), std::ios::app);
    }

    ~Logger() { if (log_file.is_open()) log_file.close(); }

    void info(const std::string& msg)    { write("INFO", msg); }
    void warn(const std::string& msg)    { write("WARN", msg); }
    void error(const std::string& msg)   { write("ERROR", msg); }
    void meta(const std::string& key, const std::string& value) {
        write("META", key + ": " + value);
    }

    // Utility for diagnostics file naming
    static std::string next_diag_filename(const std::string& base = "diagnostics", const std::string& ext = ".json", const std::string& dir = "../archive/") {
        std::filesystem::create_directories(dir);
        int idx = get_next_index(base, ext, dir);
        std::ostringstream fname;
        fname << dir << base << "_" << idx << ext;
        return fname.str();
    }

private:
    std::ofstream log_file;

    void write(const std::string& level, const std::string& msg) {
        if (log_file.is_open()) {
            std::time_t now = std::time(nullptr);
            std::tm tm_now;
        #ifdef _WIN32
            localtime_s(&tm_now, &now);
        #else
            localtime_r(&now, &tm_now);
        #endif
            char buf[32];
            std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", &tm_now);
            log_file << "[" << buf << "][" << level << "] " << msg << std::endl;
        }
    }

    static int get_next_index(const std::string& base, const std::string& ext, const std::string& dir) {
        namespace fs = std::filesystem;
        int max_idx = -1;
        for (const auto& entry : fs::directory_iterator(dir)) {
            std::string fname = entry.path().filename().string();
            if (fname.find(base) == 0 && fname.find(ext) != std::string::npos) {
                size_t start = base.size() + 1;
                size_t end = fname.find(ext);
                try {
                    int idx = std::stoi(fname.substr(start, end - start));
                    if (idx > max_idx) max_idx = idx;
                } catch (...) {}
            }
        }
        return max_idx + 1;
    }
};