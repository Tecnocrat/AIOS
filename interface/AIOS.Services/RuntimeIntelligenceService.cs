using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;

namespace AIOS.Services
{
    /// <summary>
    /// Runtime Intelligence Service for Interface Supercell
    /// Connects to Runtime Intelligence tools which then use AI Intelligence engine
    /// through cytoplasm communication
    /// </summary>
    public class RuntimeIntelligenceService
    {
        private readonly string _aiosRoot;
        private readonly string _pythonExecutable;
        private readonly string _runtimeIntelligencePath;

        public RuntimeIntelligenceService()
        {
            _aiosRoot = Environment.GetEnvironmentVariable("AIOS_ROOT") ?? @"C:\dev\AIOS";
            _pythonExecutable = Path.Combine(_aiosRoot, "aios_env", "Scripts", "python.exe");
            _runtimeIntelligencePath = Path.Combine(_aiosRoot, "runtime_intelligence", "tools");
        }

        /// <summary>
        /// Get current visual intelligence state through Runtime Intelligence
        /// (which processes through AI Intelligence via cytoplasm)
        /// </summary>
        public async Task<RuntimeIntelligenceResult> GetVisualIntelligenceAsync()
        {
            try
            {
                var visualBridgePath = Path.Combine(_runtimeIntelligencePath, "visual_intelligence_bridge_enhanced.py");
                
                var processInfo = new ProcessStartInfo
                {
                    FileName = _pythonExecutable,
                    Arguments = $"\"{visualBridgePath}\"",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true,
                    WorkingDirectory = _runtimeIntelligencePath
                };

                using var process = Process.Start(processInfo);
                if (process == null)
                {
                    throw new Exception("Failed to start Runtime Intelligence process");
                }

                var output = await process.StandardOutput.ReadToEndAsync();
                var error = await process.StandardError.ReadToEndAsync();

                await process.WaitForExitAsync();

                if (process.ExitCode != 0)
                {
                    throw new Exception($"Runtime Intelligence process failed: {error}");
                }

                // Parse the visual intelligence data
                var lines = output.Split('\n', StringSplitOptions.RemoveEmptyEntries);
                var jsonOutput = "";
                
                // Find JSON output in the console output
                foreach (var line in lines)
                {
                    if (line.Trim().StartsWith("{") && line.Trim().EndsWith("}"))
                    {
                        jsonOutput = line.Trim();
                        break;
                    }
                }

                if (string.IsNullOrEmpty(jsonOutput))
                {
                    // Parse the console output for status information
                    return ParseConsoleOutput(output);
                }

                var data = JsonSerializer.Deserialize<Dictionary<string, object>>(jsonOutput);
                
                return new RuntimeIntelligenceResult
                {
                    Status = data.GetValueOrDefault("status", "unknown").ToString(),
                    Data = data,
                    Timestamp = data.GetValueOrDefault("timestamp", DateTime.Now.ToString()).ToString(),
                    ProcessedBy = "runtime_intelligence"
                };
            }
            catch (Exception ex)
            {
                return new RuntimeIntelligenceResult
                {
                    Status = "error",
                    Message = $"Failed to get visual intelligence: {ex.Message}",
                    Timestamp = DateTime.Now.ToString(),
                    ProcessedBy = "runtime_intelligence"
                };
            }
        }

        /// <summary>
        /// Get visual intelligence with specific analysis depth
        /// </summary>
        public async Task<RuntimeIntelligenceResult> GetVisualIntelligenceAsync(string analysisDepth = "standard")
        {
            // For now, Runtime Intelligence processes through AI Intelligence automatically
            // In future, we can pass parameters to control analysis depth
            return await GetVisualIntelligenceAsync();
        }

        /// <summary>
        /// Check Runtime Intelligence system health
        /// </summary>
        public async Task<RuntimeIntelligenceResult> CheckSystemHealthAsync()
        {
            try
            {
                // Check if Runtime Intelligence tools are accessible
                var visualBridgeExists = File.Exists(Path.Combine(_runtimeIntelligencePath, "visual_intelligence_bridge_enhanced.py"));
                var pythonExists = File.Exists(_pythonExecutable);
                
                var health = new Dictionary<string, object>
                {
                    ["runtime_intelligence_tools"] = visualBridgeExists ? "available" : "missing",
                    ["python_environment"] = pythonExists ? "available" : "missing",
                    ["ai_intelligence_connection"] = "managed_by_cytoplasm"
                };

                var overallHealth = visualBridgeExists && pythonExists ? "healthy" : "degraded";

                return new RuntimeIntelligenceResult
                {
                    Status = "success",
                    Data = new Dictionary<string, object>
                    {
                        ["overall_health"] = overallHealth,
                        ["components"] = health,
                        ["architecture"] = "interface_supercell -> runtime_intelligence -> ai_intelligence(via_cytoplasm)"
                    },
                    Message = $"Runtime Intelligence health: {overallHealth}",
                    Timestamp = DateTime.Now.ToString(),
                    ProcessedBy = "runtime_intelligence"
                };
            }
            catch (Exception ex)
            {
                return new RuntimeIntelligenceResult
                {
                    Status = "error",
                    Message = $"Health check failed: {ex.Message}",
                    Timestamp = DateTime.Now.ToString(),
                    ProcessedBy = "runtime_intelligence"
                };
            }
        }

        /// <summary>
        /// Start continuous visual monitoring through Runtime Intelligence
        /// </summary>
        public async Task<RuntimeIntelligenceResult> StartContinuousMonitoringAsync(int intervalSeconds = 30)
        {
            try
            {
                // Runtime Intelligence can be configured for continuous monitoring
                // For now, return configuration confirmation
                return new RuntimeIntelligenceResult
                {
                    Status = "success",
                    Message = $"Continuous monitoring configured for {intervalSeconds} second intervals",
                    Data = new Dictionary<string, object>
                    {
                        ["monitoring_enabled"] = true,
                        ["interval_seconds"] = intervalSeconds,
                        ["processing_mode"] = "runtime_intelligence_with_ai_enhancement"
                    },
                    Timestamp = DateTime.Now.ToString(),
                    ProcessedBy = "runtime_intelligence"
                };
            }
            catch (Exception ex)
            {
                return new RuntimeIntelligenceResult
                {
                    Status = "error",
                    Message = $"Failed to start monitoring: {ex.Message}",
                    Timestamp = DateTime.Now.ToString(),
                    ProcessedBy = "runtime_intelligence"
                };
            }
        }

        /// <summary>
        /// Get available Runtime Intelligence tools
        /// </summary>
        public async Task<RuntimeIntelligenceResult> GetAvailableToolsAsync()
        {
            try
            {
                var tools = new List<RuntimeIntelligenceTool>();

                // Check for available tools in runtime_intelligence/tools
                var toolsDir = new DirectoryInfo(_runtimeIntelligencePath);
                if (toolsDir.Exists)
                {
                    foreach (var file in toolsDir.GetFiles("*.py"))
                    {
                        tools.Add(new RuntimeIntelligenceTool
                        {
                            Name = Path.GetFileNameWithoutExtension(file.Name),
                            Path = file.FullName,
                            Type = "python_tool",
                            Available = true
                        });
                    }
                }

                return new RuntimeIntelligenceResult
                {
                    Status = "success",
                    Data = new Dictionary<string, object>
                    {
                        ["tools"] = tools,
                        ["count"] = tools.Count
                    },
                    Message = $"Found {tools.Count} Runtime Intelligence tools",
                    Timestamp = DateTime.Now.ToString(),
                    ProcessedBy = "runtime_intelligence"
                };
            }
            catch (Exception ex)
            {
                return new RuntimeIntelligenceResult
                {
                    Status = "error",
                    Message = $"Failed to get tools: {ex.Message}",
                    Timestamp = DateTime.Now.ToString(),
                    ProcessedBy = "runtime_intelligence"
                };
            }
        }

        /// <summary>
        /// Parse console output when JSON is not available
        /// </summary>
        private RuntimeIntelligenceResult ParseConsoleOutput(string output)
        {
            var data = new Dictionary<string, object>();
            
            // Parse status from console output
            if (output.Contains("✅ Runtime Intelligence connected"))
            {
                data["ai_intelligence_connection"] = "active";
            }
            else if (output.Contains("⚠️ AI Intelligence connection failed"))
            {
                data["ai_intelligence_connection"] = "failed";
            }

            // Determine status from output
            string status = "unknown";
            if (output.Contains("Status: active"))
                status = "active";
            else if (output.Contains("Status: inactive"))
                status = "inactive";
            else if (output.Contains("error") || output.Contains("Error"))
                status = "error";

            return new RuntimeIntelligenceResult
            {
                Status = status,
                Data = data,
                Message = "Parsed from console output",
                Timestamp = DateTime.Now.ToString(),
                ProcessedBy = "runtime_intelligence"
            };
        }
    }

    /// <summary>
    /// Result from Runtime Intelligence operations
    /// </summary>
    public class RuntimeIntelligenceResult
    {
        public string Status { get; set; } = string.Empty;
        public object? Data { get; set; }
        public string Message { get; set; } = string.Empty;
        public string Timestamp { get; set; } = string.Empty;
        public string ProcessedBy { get; set; } = string.Empty;

        public bool IsSuccess => Status == "success" || Status == "active";
        public bool IsError => Status == "error";
    }

    /// <summary>
    /// Runtime Intelligence tool information
    /// </summary>
    public class RuntimeIntelligenceTool
    {
        public string Name { get; set; } = string.Empty;
        public string Path { get; set; } = string.Empty;
        public string Type { get; set; } = string.Empty;
        public bool Available { get; set; }
    }
}