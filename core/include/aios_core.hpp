#ifndef AIOS_CORE_HPP
#define AIOS_CORE_HPP

#include <memory>
#include <string>
#include <vector>
#include <map>
#include <functional>
#include <thread>
#include <mutex>
#include <atomic>
#include <fstream>
#include <sstream>
#include <iostream>

// #include <boost/system/error_code.hpp>
// #include <boost/filesystem.hpp>
// #include <nlohmann/json.hpp>

// Simple JSON replacement for now
namespace simple_json {
    class json {
    public:
        std::map<std::string, std::string> data;
        
        json() = default;
        json(const std::map<std::string, std::string>& d) : data(d) {}
        
        std::string dump(int indent = 0) const {
            (void)indent; // Suppress unused parameter warning
            std::string result = "{\n";
            for (const auto& [key, value] : data) {
                result += "  \"" + key + "\": \"" + value + "\",\n";
            }
            if (!data.empty()) {
                result.pop_back(); // Remove last comma
                result.pop_back(); // Remove last newline
                result += "\n";
            }
            result += "}";
            return result;
        }
        
        std::string& operator[](const std::string& key) {
            return data[key];
        }
        
        const std::string& operator[](const std::string& key) const {
            static const std::string empty_string;
            auto it = data.find(key);
            return it != data.end() ? it->second : empty_string;
        }
    };
}

namespace aios {

// Forward declarations
class SystemManager;
class AIManager;
class ConfigManager;
class Logger;

/**
 * @brief Main AIOS Core class - Entry point for the system
 * 
 * This class initializes and manages all core components of the AIOS system,
 * including AI integration, system management, and cross-language communication.
 */
class Core {
public:
    /**
     * @brief Construct a new Core object
     * 
     * @param configPath Path to the configuration file
     */
    explicit Core(const std::string& configPath = "config/system.json");
    
    /**
     * @brief Destroy the Core object
     */
    ~Core();

    /**
     * @brief Initialize the AIOS system
     * 
     * @return true if initialization was successful
     * @return false if initialization failed
     */
    bool initialize();

    /**
     * @brief Start the AIOS system
     * 
     * @return true if startup was successful
     * @return false if startup failed
     */
    bool start();

    /**
     * @brief Stop the AIOS system
     */
    void stop();

    /**
     * @brief Check if the system is running
     * 
     * @return true if running
     * @return false if stopped
     */
    bool isRunning() const;

    /**
     * @brief Get the system manager
     * 
     * @return std::shared_ptr<SystemManager> 
     */
    std::shared_ptr<SystemManager> getSystemManager() const;

    /**
     * @brief Get the AI manager
     * 
     * @return std::shared_ptr<AIManager> 
     */
    std::shared_ptr<AIManager> getAIManager() const;

    /**
     * @brief Get the configuration manager
     * 
     * @return std::shared_ptr<ConfigManager> 
     */
    std::shared_ptr<ConfigManager> getConfigManager() const;

    /**
     * @brief Get the logger instance
     * 
     * @return std::shared_ptr<Logger> 
     */
    std::shared_ptr<Logger> getLogger() const;

    /**
     * @brief Process a natural language command
     * 
     * @param command The command to process
     * @return simple_json::json Response from the system
     */
    simple_json::json processCommand(const std::string& command);

private:
    class Impl;
    std::unique_ptr<Impl> pImpl;
};

/**
 * @brief System configuration structure
 */
struct SystemConfig {
    std::string name;
    std::string version;
    std::string description;
    int maxThreads;
    size_t memoryLimit;
    std::string logLevel;
    bool enableProfiling;
    
    // AI configuration
    std::string modelPath;
    std::string defaultModel;
    int maxContextLength;
    float temperature;
    bool enableGpu;
    int batchSize;
    
    // UI configuration
    std::string theme;
    std::string language;
    bool enableAnimations;
    int refreshRate;
    
    // Integration configuration
    bool enableCppPythonBridge;
    bool enableCsharpCppBridge;
    int apiPort;
    bool enableWebInterface;
    
    // Security configuration
    bool enableSandbox;
    bool allowUnsafeOperations;
    bool enableAuditLog;
};

/**
 * @brief Load system configuration from JSON file
 * 
 * @param configPath Path to the configuration file
 * @return SystemConfig The loaded configuration
 */
SystemConfig loadSystemConfig(const std::string& configPath);

/**
 * @brief Initialize global logging
 * 
 * @param config System configuration
 * @return true if logging was initialized successfully
 * @return false if logging initialization failed
 */
bool initializeLogging(const SystemConfig& config);

} // namespace aios

#endif // AIOS_CORE_HPP
