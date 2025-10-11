using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;

namespace AIOS.Services
{
    /// <summary>
    /// AI Intelligence Service for WPF UI Integration
    /// Connects to the Python AI Intelligence through the Cytoplasm UI Bridge
    /// </summary>
    public class AIIntelligenceService
    {
        private readonly string _aiPath;
        private readonly string _pythonExecutable;
        private readonly string _cytoplasmBridgePath;

        public AIIntelligenceService()
        {
            _aiPath = Path.Combine(Environment.GetEnvironmentVariable("AIOS_ROOT") ?? @"C:\dev\AIOS", "ai");
            _pythonExecutable = Path.Combine(Environment.GetEnvironmentVariable("AIOS_ROOT") ?? @"C:\dev\AIOS", "aios_env", "Scripts", "python.exe");
            _cytoplasmBridgePath = Path.Combine(_aiPath, "cytoplasm", "ui_interaction_bridge.py");
        }

        /// <summary>
        /// Get all available AI Intelligence functions
        /// </summary>
        public async Task<List<AIFunction>> GetAvailableFunctionsAsync()
        {
            try
            {
                var result = await ExecutePythonCommandAsync("get_available_functions", new Dictionary<string, object>());
                
                if (result.ContainsKey("functions"))
                {
                    var functionsJson = JsonSerializer.Serialize(result["functions"]);
                    return JsonSerializer.Deserialize<List<AIFunction>>(functionsJson);
                }

                return new List<AIFunction>();
            }
            catch (Exception ex)
            {
                throw new Exception($"Failed to get available AI functions: {ex.Message}", ex);
            }
        }

        /// <summary>
        /// Execute an AI Intelligence function
        /// </summary>
        public async Task<AIExecutionResult> ExecuteAIFunctionAsync(string functionName, Dictionary<string, object> parameters = null)
        {
            try
            {
                var commandParameters = new Dictionary<string, object>
                {
                    ["function_name"] = functionName,
                    ["parameters"] = parameters ?? new Dictionary<string, object>()
                };

                var result = await ExecutePythonCommandAsync("execute_ai_function", commandParameters);

                return new AIExecutionResult
                {
                    Status = result.GetValueOrDefault("status", "unknown").ToString(),
                    Data = result.GetValueOrDefault("data"),
                    Message = result.GetValueOrDefault("message", "").ToString(),
                    Timestamp = result.GetValueOrDefault("timestamp", DateTime.Now.ToString()).ToString()
                };
            }
            catch (Exception ex)
            {
                return new AIExecutionResult
                {
                    Status = "error",
                    Message = $"Failed to execute AI function '{functionName}': {ex.Message}",
                    Timestamp = DateTime.Now.ToString()
                };
            }
        }

        /// <summary>
        /// Start real-time visual intelligence monitoring
        /// </summary>
        public async Task<AIExecutionResult> StartRealTimeMonitoringAsync(int intervalSeconds = 30)
        {
            var parameters = new Dictionary<string, object>
            {
                ["enabled"] = true,
                ["interval"] = intervalSeconds
            };

            return await ExecuteAIFunctionAsync("real_time_monitoring", parameters);
        }

        /// <summary>
        /// Stop real-time visual intelligence monitoring
        /// </summary>
        public async Task<AIExecutionResult> StopRealTimeMonitoringAsync()
        {
            var parameters = new Dictionary<string, object>
            {
                ["enabled"] = false
            };

            return await ExecuteAIFunctionAsync("real_time_monitoring", parameters);
        }

        /// <summary>
        /// Process visual intelligence with specified analysis depth
        /// </summary>
        public async Task<AIExecutionResult> ProcessVisualIntelligenceAsync(bool realTime = false, string analysisDepth = "standard")
        {
            var parameters = new Dictionary<string, object>
            {
                ["real_time"] = realTime,
                ["analysis_depth"] = analysisDepth
            };

            return await ExecuteAIFunctionAsync("process_visual_intelligence", parameters);
        }

        /// <summary>
        /// Analyze consciousness patterns
        /// </summary>
        public async Task<AIExecutionResult> AnalyzeConsciousnessPatternsAsync(object data = null, int temporalWindow = 300)
        {
            var parameters = new Dictionary<string, object>
            {
                ["data"] = data ?? new { },
                ["temporal_window"] = temporalWindow
            };

            return await ExecuteAIFunctionAsync("analyze_consciousness_patterns", parameters);
        }

        /// <summary>
        /// Perform enhanced visual analysis
        /// </summary>
        public async Task<AIExecutionResult> EnhancedVisualAnalysisAsync(object data = null, bool cellularIntegration = true)
        {
            var parameters = new Dictionary<string, object>
            {
                ["data"] = data ?? new { },
                ["cellular_integration"] = cellularIntegration
            };

            return await ExecuteAIFunctionAsync("enhanced_visual_analysis", parameters);
        }

        /// <summary>
        /// Check system health of all AI components
        /// </summary>
        public async Task<AIExecutionResult> SystemHealthCheckAsync()
        {
            return await ExecuteAIFunctionAsync("system_health_check");
        }

        /// <summary>
        /// Create a new AI analysis session
        /// </summary>
        public async Task<AIExecutionResult> CreateSessionAsync()
        {
            var parameters = new Dictionary<string, object>
            {
                ["action"] = "create"
            };

            return await ExecuteAIFunctionAsync("session_management", parameters);
        }

        /// <summary>
        /// Get list of active sessions
        /// </summary>
        public async Task<AIExecutionResult> GetActiveSessionsAsync()
        {
            var parameters = new Dictionary<string, object>
            {
                ["action"] = "list"
            };

            return await ExecuteAIFunctionAsync("session_management", parameters);
        }

        /// <summary>
        /// Export analysis data
        /// </summary>
        public async Task<AIExecutionResult> ExportAnalysisDataAsync(string format = "json", string sessionId = null)
        {
            var parameters = new Dictionary<string, object>
            {
                ["format"] = format
            };

            if (!string.IsNullOrEmpty(sessionId))
            {
                parameters["session_id"] = sessionId;
            }

            return await ExecuteAIFunctionAsync("export_analysis_data", parameters);
        }

        /// <summary>
        /// Get debug information from the AI system
        /// </summary>
        public async Task<AIExecutionResult> GetDebugInfoAsync()
        {
            return await ExecuteAIFunctionAsync("get_debug_info");
        }

        /// <summary>
        /// Execute a Python command through the cytoplasm bridge
        /// </summary>
        private async Task<Dictionary<string, object>> ExecutePythonCommandAsync(string command, Dictionary<string, object> parameters)
        {
            try
            {
                var commandJson = JsonSerializer.Serialize(new
                {
                    command = command,
                    parameters = parameters
                });

                var tempFile = Path.GetTempFileName();
                await File.WriteAllTextAsync(tempFile, commandJson);

                var processInfo = new ProcessStartInfo
                {
                    FileName = _pythonExecutable,
                    Arguments = $"\"{_cytoplasmBridgePath}\" --command-file \"{tempFile}\"",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true,
                    WorkingDirectory = _aiPath
                };

                using var process = Process.Start(processInfo);
                if (process == null)
                {
                    throw new Exception("Failed to start Python process");
                }

                var output = await process.StandardOutput.ReadToEndAsync();
                var error = await process.StandardError.ReadToEndAsync();

                await process.WaitForExitAsync();

                // Clean up temp file
                try { File.Delete(tempFile); } catch { }

                if (process.ExitCode != 0)
                {
                    throw new Exception($"Python process failed with exit code {process.ExitCode}: {error}");
                }

                if (string.IsNullOrWhiteSpace(output))
                {
                    return new Dictionary<string, object> { ["status"] = "no_output" };
                }

                return JsonSerializer.Deserialize<Dictionary<string, object>>(output) ?? new Dictionary<string, object>();
            }
            catch (Exception ex)
            {
                throw new Exception($"Failed to execute Python command '{command}': {ex.Message}", ex);
            }
        }
    }

    /// <summary>
    /// Represents an AI function available to the UI
    /// </summary>
    public class AIFunction
    {
        public string Name { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string Category { get; set; } = string.Empty;
        public Dictionary<string, object> Parameters { get; set; } = new();
        public string Endpoint { get; set; } = string.Empty;
    }

    /// <summary>
    /// Result of AI function execution
    /// </summary>
    public class AIExecutionResult
    {
        public string Status { get; set; } = string.Empty;
        public object? Data { get; set; }
        public string Message { get; set; } = string.Empty;
        public string Timestamp { get; set; } = string.Empty;

        public bool IsSuccess => Status == "success";
        public bool IsError => Status == "error";
    }

    /// <summary>
    /// AI Intelligence event args for UI notifications
    /// </summary>
    public class AIIntelligenceEventArgs : EventArgs
    {
        public string FunctionName { get; set; } = string.Empty;
        public AIExecutionResult Result { get; set; } = new();
        public DateTime Timestamp { get; set; } = DateTime.Now;
    }
}