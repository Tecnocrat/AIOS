#ifndef AIOS_CORE_MINIMAL_HPP
#define AIOS_CORE_MINIMAL_HPP

#include <memory>
#include <string>
#include <vector>
#include <map>
#include <atomic>
#include <mutex>

namespace aios {

    /**
     * @brief System configuration structure
     */
    struct SystemConfig {
        std::string name;
        std::string version;
        std::string description;
        int maxThreads;
        uint64_t memoryLimit;
        std::string logLevel;
        bool enableProfiling;
    };

    /**
     * @brief Minimal AIOS Core for TensorFlow integration
     * 
     * This is a simplified version of the core that provides basic
     * functionality needed for TensorFlow C++ ↔ Python cellular communication
     */
    class Core {
    public:
        /**
         * @brief Construct a new Core object
         */
        explicit Core(const std::string& configPath = "../ai/infrastructure/config/system.json");

        /**
         * @brief Destroy the Core object
         */
        ~Core();

        /**
         * @brief Initialize the AIOS system
         */
        bool initialize();

        /**
         * @brief Start the AIOS system
         */
        bool start();

        /**
         * @brief Stop the AIOS system
         */
        void stop();

        /**
         * @brief Check if the system is running
         */
        bool isRunning() const;

        /**
         * @brief Get system configuration
         */
        const SystemConfig& getConfig() const;

    private:
        // Implementation class (PIMPL pattern)
        class Impl;
        std::unique_ptr<Impl> impl_;
    };

} // namespace aios

#endif // AIOS_CORE_MINIMAL_HPP