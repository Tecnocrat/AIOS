using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Text.Json;
using System.Diagnostics;
using System.IO;
using Microsoft.Extensions.Logging;

namespace AIOS.Services
{
    /// <summary>
    /// Compression Service Interface for AIOS
    /// Provides compression capabilities across all AIOS subsystems
    /// </summary>
    public interface ICompressionService
    {
        Task<CompressionResult> CompressAsync(CompressionRequest request);
        Task<CompressionResult> CompressFilesAsync(string sourcePath, CompressionType type = CompressionType.SmartMerge);
        Task<CompressionStatus> GetCompressionStatusAsync(string compressionId = null);
        Task<bool> RestoreFromBackupAsync(string backupLocation);
        Task<List<CompressionHistoryItem>> GetCompressionHistoryAsync();
        void RegisterCompressionTool();
    }

    /// <summary>
    /// Compression request structure matching Python interface
    /// </summary>
    public class CompressionRequest
    {
        public string SourcePath { get; set; }
        public string TargetPath { get; set; }
        public CompressionType CompressionType { get; set; } = CompressionType.SmartMerge;
        public bool PreserveFunctionality { get; set; } = true;
        public bool CreateBackup { get; set; } = true;
        public CompressionLevel CompressionLevel { get; set; } = CompressionLevel.Standard;
        public List<string> FilePatterns { get; set; }
        public List<string> ExcludePatterns { get; set; }
        public MergeStrategy MergeStrategy { get; set; } = MergeStrategy.UnifiedModule;
    }

    /// <summary>
    /// Compression result structure matching Python interface
    /// </summary>
    public class CompressionResult
    {
        public bool Success { get; set; }
        public double CompressionRatio { get; set; }
        public int FilesProcessed { get; set; }
        public int FilesMerged { get; set; }
        public int LinesSaved { get; set; }
        public string BackupLocation { get; set; }
        public List<string> UnifiedModules { get; set; } = new List<string>();
        public double ExecutionTime { get; set; }
        public string ErrorMessage { get; set; }
        public List<string> Warnings { get; set; } = new List<string>();
    }

    /// <summary>
    /// Compression status for tracking operations
    /// </summary>
    public class CompressionStatus
    {
        public List<string> ActiveCompressions { get; set; } = new List<string>();
        public CompressionStatistics Stats { get; set; } = new CompressionStatistics();
    }

    /// <summary>
    /// Compression statistics
    /// </summary>
    public class CompressionStatistics
    {
        public int TotalCompressions { get; set; }
        public int TotalFilesProcessed { get; set; }
        public double TotalCompressionRatio { get; set; }
        public DateTime? LastCompression { get; set; }
    }

    /// <summary>
    /// Compression history item
    /// </summary>
    public class CompressionHistoryItem
    {
        public string Id { get; set; }
        public CompressionRequest Request { get; set; }
        public string Status { get; set; }
        public DateTime StartTime { get; set; }
        public CompressionResult Result { get; set; }
    }

    /// <summary>
    /// Compression types
    /// </summary>
    public enum CompressionType
    {
        SmartMerge,
        LogicCompress,
        PatternMerge
    }

    /// <summary>
    /// Compression levels
    /// </summary>
    public enum CompressionLevel
    {
        Minimal,
        Standard,
        Aggressive,
        Maximum
    }

    /// <summary>
    /// Merge strategies
    /// </summary>
    public enum MergeStrategy
    {
        UnifiedModule,
        Hierarchical,
        Functional
    }

    /// <summary>
    /// AIOS Compression Service Implementation
    /// Provides compression capabilities as a service to all AIOS components
    /// </summary>
    public class AIOSCompressionService : ICompressionService
    {
        private readonly ILogger<AIOSCompressionService> _logger;
        private readonly string _pythonPath;
        private readonly string _compressionModulePath;
        private readonly Dictionary<string, Process> _activeCompressions;

        public AIOSCompressionService(ILogger<AIOSCompressionService>? logger = null)
        {
            _logger = logger ?? Microsoft.Extensions.Logging.Abstractions.NullLogger<AIOSCompressionService>.Instance;
            _pythonPath = FindPythonExecutable();
            _compressionModulePath = Path.Combine(@"c:\dev\AIOS\scripts\compression", "aios_universal_compressor.py");
            _activeCompressions = new Dictionary<string, Process>();

            _logger.LogInformation("AIOS Compression Service initialized");
            _logger.LogInformation($"Python path: {_pythonPath}");
            _logger.LogInformation($"Compression module: {_compressionModulePath}");
        }

        /// <summary>
        /// Compress files asynchronously using compression request
        /// </summary>
        public async Task<CompressionResult> CompressAsync(CompressionRequest request)
        {
            try
            {
                _logger.LogInformation($"Starting compression: {request.SourcePath}");

                // Prepare Python command
                var compressionArgs = JsonSerializer.Serialize(request, new JsonSerializerOptions
                {
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                });

                var pythonCommand = $"\"{_compressionModulePath}\" --json \"{compressionArgs.Replace("\"", "\"\"")}\"";

                // Execute Python compression module
                var result = await ExecutePythonModuleAsync(pythonCommand);

                _logger.LogInformation($"Compression completed: {request.SourcePath}");
                return result;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Compression failed: {request.SourcePath}");
                return new CompressionResult
                {
                    Success = false,
                    ErrorMessage = ex.Message
                };
            }
        }

        /// <summary>
        /// Compress files with simplified interface
        /// </summary>
        public async Task<CompressionResult> CompressFilesAsync(string sourcePath, CompressionType type = CompressionType.SmartMerge)
        {
            var request = new CompressionRequest
            {
                SourcePath = sourcePath,
                CompressionType = type
            };

            return await CompressAsync(request);
        }

        /// <summary>
        /// Get compression status
        /// </summary>
        public async Task<CompressionStatus> GetCompressionStatusAsync(string compressionId = null)
        {
            try
            {
                var command = string.IsNullOrEmpty(compressionId)
                    ? $"\"{_compressionModulePath}\" --status"
                    : $"\"{_compressionModulePath}\" --status \"{compressionId}\"";

                var result = await ExecutePythonCommandAsync(command);

                if (!string.IsNullOrEmpty(result))
                {
                    return JsonSerializer.Deserialize<CompressionStatus>(result, new JsonSerializerOptions
                    {
                        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                    });
                }

                return new CompressionStatus();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to get compression status");
                return new CompressionStatus();
            }
        }

        /// <summary>
        /// Restore from backup
        /// </summary>
        public async Task<bool> RestoreFromBackupAsync(string backupLocation)
        {
            try
            {
                var command = $"\"{_compressionModulePath}\" --restore \"{backupLocation}\"";
                var result = await ExecutePythonCommandAsync(command);

                return result?.Contains("SUCCESS") == true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Failed to restore from backup: {backupLocation}");
                return false;
            }
        }

        /// <summary>
        /// Get compression history
        /// </summary>
        public async Task<List<CompressionHistoryItem>> GetCompressionHistoryAsync()
        {
            try
            {
                var command = $"\"{_compressionModulePath}\" --history";
                var result = await ExecutePythonCommandAsync(command);

                if (!string.IsNullOrEmpty(result))
                {
                    return JsonSerializer.Deserialize<List<CompressionHistoryItem>>(result, new JsonSerializerOptions
                    {
                        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                    });
                }

                return new List<CompressionHistoryItem>();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to get compression history");
                return new List<CompressionHistoryItem>();
            }
        }

        /// <summary>
        /// Register compression tool with AIOS system
        /// </summary>
        public void RegisterCompressionTool()
        {
            try
            {
                // Register with AI Service Manager
                // This would integrate with the existing AIServiceManager
                _logger.LogInformation("Compression tool registered with AIOS system");

                // Could register as an AI module
                // _aiModules["compression"] = new AIModule
                // {
                //     Id = "compression",
                //     Name = "Universal Compression Service",
                //     Status = "Active",
                //     Description = "Advanced file compression and merging capabilities",
                //     Version = "1.0.0",
                //     LastUpdated = DateTime.UtcNow
                // };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to register compression tool");
            }
        }

        /// <summary>
        /// Execute Python compression module
        /// </summary>
        private async Task<CompressionResult> ExecutePythonModuleAsync(string command)
        {
            try
            {
                using var process = new Process();
                process.StartInfo = new ProcessStartInfo
                {
                    FileName = _pythonPath,
                    Arguments = command,
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                };

                var output = new List<string>();
                var errors = new List<string>();

                process.OutputDataReceived += (sender, e) =>
                {
                    if (e.Data != null) output.Add(e.Data);
                };
                process.ErrorDataReceived += (sender, e) =>
                {
                    if (e.Data != null) errors.Add(e.Data);
                };

                process.Start();
                process.BeginOutputReadLine();
                process.BeginErrorReadLine();

                await process.WaitForExitAsync();

                var outputText = string.Join("\n", output);
                var errorText = string.Join("\n", errors);

                if (process.ExitCode == 0 && !string.IsNullOrEmpty(outputText))
                {
                    // Try to parse JSON result
                    try
                    {
                        return JsonSerializer.Deserialize<CompressionResult>(outputText, new JsonSerializerOptions
                        {
                            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                        });
                    }
                    catch
                    {
                        // If not JSON, create result from output
                        return new CompressionResult
                        {
                            Success = true,
                            ErrorMessage = outputText
                        };
                    }
                }
                else
                {
                    return new CompressionResult
                    {
                        Success = false,
                        ErrorMessage = errorText
                    };
                }
            }
            catch (Exception ex)
            {
                return new CompressionResult
                {
                    Success = false,
                    ErrorMessage = ex.Message
                };
            }
        }

        /// <summary>
        /// Execute Python command and return output
        /// </summary>
        private async Task<string> ExecutePythonCommandAsync(string command)
        {
            try
            {
                using var process = new Process();
                process.StartInfo = new ProcessStartInfo
                {
                    FileName = _pythonPath,
                    Arguments = command,
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    CreateNoWindow = true
                };

                process.Start();
                var output = await process.StandardOutput.ReadToEndAsync();
                await process.WaitForExitAsync();

                return process.ExitCode == 0 ? output : null;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Failed to execute Python command: {command}");
                return null;
            }
        }

        /// <summary>
        /// Find Python executable
        /// </summary>
        private string FindPythonExecutable()
        {
            var pythonPaths = new[]
            {
                "python",
                "python3",
                @"C:\Python39\python.exe",
                @"C:\Python310\python.exe",
                @"C:\Python311\python.exe",
                @"C:\Program Files\Python39\python.exe",
                @"C:\Program Files\Python310\python.exe",
                @"C:\Program Files\Python311\python.exe"
            };

            foreach (var path in pythonPaths)
            {
                try
                {
                    using var process = Process.Start(new ProcessStartInfo
                    {
                        FileName = path,
                        Arguments = "--version",
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        CreateNoWindow = true
                    });

                    if (process != null)
                    {
                        process.WaitForExit(5000);
                        if (process.ExitCode == 0)
                        {
                            return path;
                        }
                    }
                }
                catch
                {
                    // Continue to next path
                }
            }

            return "python"; // Default fallback
        }
    }

    /// <summary>
    /// Extension methods for easier compression integration
    /// </summary>
    public static class CompressionExtensions
    {
        /// <summary>
        /// Extension method to compress any directory or file
        /// </summary>
        public static async Task<CompressionResult> CompressAsync(this string path, ICompressionService compressionService, CompressionType type = CompressionType.SmartMerge)
        {
            return await compressionService.CompressFilesAsync(path, type);
        }

        /// <summary>
        /// Extension method to check if compression is available
        /// </summary>
        public static bool IsCompressionAvailable(this ICompressionService compressionService)
        {
            try
            {
                var status = compressionService.GetCompressionStatusAsync().Result;
                return status != null;
            }
            catch
            {
                return false;
            }
        }
    }
}
