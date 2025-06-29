#pragma once
#include <fstream>
#include <string>
#include <ctime>
#include <iomanip>
#include <filesystem>
#include <regex>

class Logger {
public:
    explicit Logger(const std::string& filename)
        : log_file_(filename, std::ios::app) {}

    void info(const std::string& msg) {
        log("[INFO]", msg);
    }
    void meta(const std::string& key, const std::string& value) {
        log("[META]", key + ": " + value);
    }
    void consciousness(const std::string& event_type, const std::string& message) {
        log("[CONSCIOUSNESS]", event_type + ": " + message);
    }

    // Implementation moved here
    static std::string next_diag_filename(const std::string& base, const std::string& ext, const std::string& dir) {
        namespace fs = std::filesystem;
        int max_index = -1;
        std::regex pattern(base + R"(_(\d+)\)" + ext);

        for (const auto& entry : fs::directory_iterator(dir)) {
            if (!entry.is_regular_file()) continue;
            std::smatch match;
            std::string filename = entry.path().filename().string();
            if (std::regex_match(filename, match, pattern)) {
                int idx = std::stoi(match[1]);
                if (idx > max_index) max_index = idx;
            }
        }
        return dir + base + "_" + std::to_string(max_index + 1) + ext;
    }

private:
    std::ofstream log_file_;

    void log(const std::string& level, const std::string& msg) {
        if (log_file_.is_open()) {
            log_file_ << timestamp() << level << " " << msg << std::endl;
        }
    }
    std::string timestamp() {
        std::time_t t = std::time(nullptr);
        std::tm tm;
        localtime_s(&tm, &t);
        char buf[32];
        std::strftime(buf, sizeof(buf), "[%Y-%m-%d %H:%M:%S]", &tm);
        return buf;
    }
};