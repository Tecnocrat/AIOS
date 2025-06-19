#pragma once
#include <fstream>
#include <string>
#include <ctime>
#include <iomanip>
#include <sstream>

class Logger {
public:
    Logger(const std::string& filename = "kernel.log")
        : log_file(filename, std::ios::app) {}

    ~Logger() { if (log_file.is_open()) log_file.close(); }

    void info(const std::string& msg)    { write("INFO", msg); }
    void warn(const std::string& msg)    { write("WARN", msg); }
    void error(const std::string& msg)   { write("ERROR", msg); }
    void meta(const std::string& key, const std::string& value) {
        write("META", key + ": " + value);
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
};

Logger logger("C:/dev/AIOS/orchestrator/archive/kernel.log");