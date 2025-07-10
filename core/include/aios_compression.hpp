#ifndef AIOS_COMPRESSION_HPP
#define AIOS_COMPRESSION_HPP

#include <string>
#include <vector>
#include <map>
#include <memory>
#include <future>

namespace AIOS {
    namespace Compression {

        /// Compression types available
        enum class CompressionType {
            SMART_MERGE,
            LOGIC_COMPRESS,
            PATTERN_MERGE
        };

        /// Compression levels
        enum class CompressionLevel {
            MINIMAL,
            STANDARD,
            AGGRESSIVE,
            MAXIMUM
        };

        /// Merge strategies
        enum class MergeStrategy {
            UNIFIED_MODULE,
            HIERARCHICAL,
            FUNCTIONAL
        };

        /// Compression request structure
        struct CompressionRequest {
            std::string source_path;
            std::string target_path = "";
            CompressionType compression_type = CompressionType::SMART_MERGE;
            bool preserve_functionality = true;
            bool create_backup = true;
            CompressionLevel compression_level = CompressionLevel::STANDARD;
            std::vector<std::string> file_patterns;
            std::vector<std::string> exclude_patterns;
            MergeStrategy merge_strategy = MergeStrategy::UNIFIED_MODULE;
        };

        /// Compression result structure
        struct CompressionResult {
            bool success = false;
            double compression_ratio = 0.0;
            int files_processed = 0;
            int files_merged = 0;
            int lines_saved = 0;
            std::string backup_location;
            std::vector<std::string> unified_modules;
            double execution_time = 0.0;
            std::string error_message;
            std::vector<std::string> warnings;
        };

        /// Compression status
        struct CompressionStatus {
            std::vector<std::string> active_compressions;
            std::map<std::string, double> stats;
        };

        /// Universal Compression Service Interface
        class ICompressionService {
        public:
            virtual ~ICompressionService() = default;

            /// Compress files asynchronously
            virtual std::future<CompressionResult> CompressAsync(const CompressionRequest& request) = 0;

            /// Compress files with simplified interface
            virtual std::future<CompressionResult> CompressFilesAsync(
                const std::string& source_path,
                CompressionType type = CompressionType::SMART_MERGE
            ) = 0;

            /// Get compression status
            virtual std::future<CompressionStatus> GetCompressionStatusAsync(
                const std::string& compression_id = ""
            ) = 0;

            /// Restore from backup
            virtual std::future<bool> RestoreFromBackupAsync(const std::string& backup_location) = 0;

            /// Register compression tool
            virtual void RegisterCompressionTool() = 0;
        };

        /// Python-based compression service implementation
        class PythonCompressionService : public ICompressionService {
        private:
            std::string python_path_;
            std::string compression_module_path_;
            std::string workspace_root_;

            /// Execute Python command and return result
            std::string ExecutePythonCommand(const std::string& command);

            /// Convert CompressionRequest to JSON string
            std::string RequestToJson(const CompressionRequest& request);

            /// Parse JSON result to CompressionResult
            CompressionResult ParseCompressionResult(const std::string& json_result);

        public:
            /// Constructor
            explicit PythonCompressionService(
                const std::string& workspace_root = "c:\\dev\\AIOS",
                const std::string& python_path = "python"
            );

            /// Compress files asynchronously
            std::future<CompressionResult> CompressAsync(const CompressionRequest& request) override;

            /// Compress files with simplified interface
            std::future<CompressionResult> CompressFilesAsync(
                const std::string& source_path,
                CompressionType type = CompressionType::SMART_MERGE
            ) override;

            /// Get compression status
            std::future<CompressionStatus> GetCompressionStatusAsync(
                const std::string& compression_id = ""
            ) override;

            /// Restore from backup
            std::future<bool> RestoreFromBackupAsync(const std::string& backup_location) override;

            /// Register compression tool
            void RegisterCompressionTool() override;

            /// Check if compression service is available
            bool IsAvailable() const;
        };

        /// Compression service factory
        class CompressionServiceFactory {
        public:
            /// Create compression service instance
            static std::unique_ptr<ICompressionService> CreateService(
                const std::string& workspace_root = "c:\\dev\\AIOS"
            );

            /// Get default compression service
            static ICompressionService& GetDefaultService();
        };

        /// Compression utilities for easy integration
        namespace Utils {

            /// Compress a directory or file
            std::future<CompressionResult> Compress(
                const std::string& path,
                CompressionType type = CompressionType::SMART_MERGE
            );

            /// Quick compression with default settings
            CompressionResult QuickCompress(const std::string& path);

            /// Check if compression is available
            bool IsCompressionAvailable();

            /// Get compression statistics
            std::map<std::string, double> GetCompressionStats();
        }

        /// RAII wrapper for compression operations
        class CompressionScope {
        private:
            std::unique_ptr<ICompressionService> service_;
            std::string source_path_;
            bool auto_backup_;

        public:
            /// Constructor with auto-backup
            explicit CompressionScope(
                const std::string& source_path,
                bool auto_backup = true
            );

            /// Destructor automatically handles cleanup
            ~CompressionScope();

            /// Execute compression
            CompressionResult Compress(
                CompressionType type = CompressionType::SMART_MERGE,
                CompressionLevel level = CompressionLevel::STANDARD
            );

            /// Get compression service
            ICompressionService& GetService();
        };

    } // namespace Compression
} // namespace AIOS

// Convenience macros for easy integration
#define AIOS_COMPRESS(path) AIOS::Compression::Utils::QuickCompress(path)
#define AIOS_COMPRESS_ASYNC(path, type) AIOS::Compression::Utils::Compress(path, type)
#define AIOS_COMPRESSION_AVAILABLE() AIOS::Compression::Utils::IsCompressionAvailable()

// Integration with AIOS Core
#ifdef AIOS_CORE_INTEGRATION
namespace AIOS {
    namespace Core {

        /// Add compression capability to AIOS Core
        class AIOSCoreWithCompression {
        private:
            std::unique_ptr<Compression::ICompressionService> compression_service_;

        public:
            AIOSCoreWithCompression();

            /// Get compression service
            Compression::ICompressionService& GetCompressionService();

            /// Integrate compression with existing AIOS Core functionality
            void IntegrateCompression();

            /// Compress AIOS modules
            std::future<Compression::CompressionResult> CompressAIOSModules();

            /// Optimize AIOS codebase
            std::future<Compression::CompressionResult> OptimizeCodebase();
        };

    } // namespace Core
} // namespace AIOS
#endif

#endif // AIOS_COMPRESSION_HPP
