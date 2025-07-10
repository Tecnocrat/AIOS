using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Text.Json;
using System.Linq;
using Microsoft.Extensions.Logging;
using System.Runtime.InteropServices;
using System.Diagnostics;
using AIOS.Models;

namespace AIOS.Services
{
    /// <summary>
    /// AI Service Manager - Core AI functionality implementation
    /// Implements IAIService interface for dependency injection
    /// Enhanced with Universal Compression Service
    /// </summary>
    [ComVisible(true)]
    public class AIServiceManager : IAIService
    {
        private readonly ILogger<AIServiceManager> _logger;
        private readonly Dictionary<string, AIModule> _aiModules;
        private readonly List<SystemEvent> _recentEvents;
        private readonly Random _random;
        private readonly string _pythonPath;
        private readonly string _aiModulesPath;

        // Universal Compression Service Integration
        private readonly ICompressionService _compressionService;

        public AIServiceManager(ILogger<AIServiceManager>? logger = null, ICompressionService compressionService = null)
        {
            _logger = logger ?? Microsoft.Extensions.Logging.Abstractions.NullLogger<AIServiceManager>.Instance;
            _aiModules = new Dictionary<string, AIModule>();
            _recentEvents = new List<SystemEvent>();
            _random = new Random();
            _pythonPath = "python";
            _aiModulesPath = @"c:\dev\AIOS\ai\src";

            // Initialize compression service
            _compressionService = compressionService ?? new AIOSCompressionService(_logger as ILogger<AIOSCompressionService>);

            InitializeAIModules();
            RegisterCompressionTool();
        }

        private void InitializeAIModules()
        {
            _aiModules["nlp"] = new AIModule
            {
                Id = "nlp",
                Name = "Natural Language Processing",
                Status = "Active",
                Description = "Advanced NLP capabilities",
                Version = "2.1.0",
                LastUpdated = DateTime.UtcNow
            };

            _aiModules["prediction"] = new AIModule
            {
                Id = "prediction",
                Name = "Prediction Engine",
                Status = "Active",
                Description = "Machine learning predictions",
                Version = "1.8.0",
                LastUpdated = DateTime.UtcNow
            };

            _aiModules["automation"] = new AIModule
            {
                Id = "automation",
                Name = "Automation Engine",
                Status = "Active",
                Description = "Intelligent automation",
                Version = "1.5.0",
                LastUpdated = DateTime.UtcNow
            };

            // Add compression module to AI modules
            _aiModules["compression"] = new AIModule
            {
                Id = "compression",
                Name = "Universal Compression Engine",
                Status = "Active",
                Description = "Advanced file compression and merging capabilities",
                Version = "1.0.0",
                LastUpdated = DateTime.UtcNow
            };
        }

        /// <summary>
        /// Register compression tool with AIOS system
        /// </summary>
        private void RegisterCompressionTool()
        {
            try
            {
                _compressionService?.RegisterCompressionTool();
                _logger.LogInformation("Universal Compression Service integrated with AI Service Manager");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to register compression tool with AI Service Manager");
            }
        }

        /// <summary>
        /// Compress files using the integrated compression service
        /// </summary>
        public async Task<CompressionResult> CompressAsync(string sourcePath, CompressionType type = CompressionType.SmartMerge)
        {
            try
            {
                _logger.LogInformation($"AI Service Manager initiating compression: {sourcePath}");
                var result = await _compressionService.CompressFilesAsync(sourcePath, type);

                // Log compression event
                LogSystemEvent($"Compression completed: {sourcePath}", result.Success ? "SUCCESS" : "FAILED");

                return result;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"AI Service Manager compression failed: {sourcePath}");
                LogSystemEvent($"Compression failed: {sourcePath}", "ERROR");

                return new CompressionResult
                {
                    Success = false,
                    ErrorMessage = ex.Message
                };
            }
        }

        /// <summary>
        /// Get compression status through AI Service Manager
        /// </summary>
        public async Task<CompressionStatus> GetCompressionStatusAsync(string compressionId = null)
        {
            return await _compressionService.GetCompressionStatusAsync(compressionId);
        }

        /// <summary>
        /// Access to compression service for other components
        /// </summary>
        public ICompressionService CompressionService => _compressionService;

        public async Task<Dictionary<string, object>> ProcessNLPAsync(string input)
        {
            try
            {
                var result = await CallPythonModule("nlp", input);
                return JsonSerializer.Deserialize<Dictionary<string, object>>(result) ?? new Dictionary<string, object>();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "NLP processing failed for input: {Input}", input);
                return new Dictionary<string, object> { { "error", ex.Message } };
            }
        }

        public async Task<AIResponse> ProcessAsync(string module, string input, Dictionary<string, object>? parameters = null)
        {
            try
            {
                var result = await CallPythonModule(module, input, parameters);
                return new AIResponse
                {
                    Success = true,
                    Response = result,
                    Module = module,
                    Timestamp = DateTime.UtcNow
                };
            }
            catch (Exception ex)
            {
                return new AIResponse
                {
                    Success = false,
                    Error = ex.Message,
                    Module = module,
                    Timestamp = DateTime.UtcNow
                };
            }
        }

        public async Task<int> PredictCacheTTL(object data)
        {
            try
            {
                var analysisResult = await CallPythonModule("prediction", JsonSerializer.Serialize(new
                {
                    operation = "predict_cache_ttl",
                    data = data
                }));

                var result = JsonSerializer.Deserialize<Dictionary<string, object>>(analysisResult);
                return result?.ContainsKey("ttl") == true ? Convert.ToInt32(result["ttl"]) : 3600;
            }
            catch
            {
                return 3600; // Default fallback
            }
        }

        public async Task<bool> ValidateData(object data)
        {
            try
            {
                var validationResult = await CallPythonModule("nlp", JsonSerializer.Serialize(new
                {
                    operation = "validate_data",
                    data = data
                }));

                var result = JsonSerializer.Deserialize<Dictionary<string, object>>(validationResult);
                return result?.ContainsKey("valid") == true && Convert.ToBoolean(result["valid"]);
            }
            catch
            {
                return false;
            }
        }

        public async Task<object> TransformDataForStorage(object data)
        {
            try
            {
                var transformResult = await CallPythonModule("automation", JsonSerializer.Serialize(new
                {
                    operation = "transform_for_storage",
                    data = data
                }));

                return JsonSerializer.Deserialize<Dictionary<string, object>>(transformResult) ?? data;
            }
            catch
            {
                return data;
            }
        }

        public async Task<bool> LearnFromData(object data)
        {
            try
            {
                var learningResult = await CallPythonModule("learning", JsonSerializer.Serialize(new
                {
                    operation = "learn_from_data",
                    data = data
                }));

                var result = JsonSerializer.Deserialize<Dictionary<string, object>>(learningResult);
                return result?.ContainsKey("learned") == true && Convert.ToBoolean(result["learned"]);
            }
            catch
            {
                return false;
            }
        }

        public async Task<string[]> PredictCacheInvalidation(string collection, object data)
        {
            try
            {
                var predictionResult = await CallPythonModule("prediction", JsonSerializer.Serialize(new
                {
                    operation = "predict_cache_invalidation",
                    key = collection,
                    data = data
                }));

                var result = JsonSerializer.Deserialize<Dictionary<string, object>>(predictionResult);
                if (result?.ContainsKey("keys") == true && result["keys"] is JsonElement keysElement)
                {
                    return keysElement.EnumerateArray().Select(k => k.GetString() ?? "").ToArray();
                }
                return new[] { $"cache_{collection}_{data.GetHashCode()}" };
            }
            catch
            {
                return new[] { $"cache_{collection}_{data.GetHashCode()}" };
            }
        }

        public async Task<SystemHealthResponse> GetSystemHealthAsync()
        {
            var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = _pythonPath,
                    Arguments = "scripts/context_health_monitor.py --json",
                    WorkingDirectory = @"c:\dev\AIOS",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                }
            };

            try
            {
                process.Start();
                var output = await process.StandardOutput.ReadToEndAsync();
                await process.WaitForExitAsync();

                if (process.ExitCode == 0 && !string.IsNullOrWhiteSpace(output))
                {
                    var healthData = JsonSerializer.Deserialize<JsonElement>(output);
                    return new SystemHealthResponse
                    {
                        Success = true,
                        HealthScore = GetJsonDouble(healthData, "health_score", 0.8),
                        HealthStatus = GetJsonString(healthData, "status", "Unknown"),
                        Issues = GetJsonStringArray(healthData, "issues"),
                        Warnings = GetJsonStringArray(healthData, "warnings"),
                        Recommendations = GetJsonStringArray(healthData, "recommendations"),
                        TriggerReingestion = GetJsonBool(healthData, "trigger_reingestion", false),
                        Timestamp = DateTime.UtcNow
                    };
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to get system health");
            }

            return new SystemHealthResponse
            {
                Success = false,
                Error = "Failed to get system health",
                Timestamp = DateTime.UtcNow
            };
        }

        public object GeneratePrediction(Dictionary<string, object> inputData, string modelType)
        {
            return new { prediction = "Generated prediction", confidence = 0.85 };
        }

        public ValidationResult ValidateInput(object input)
        {
            return new ValidationResult { IsValid = true, Errors = new List<string>() };
        }

        public string[] GetCacheKeys(string collection, object data)
        {
            return new[] { $"cache_{collection}_{data.GetHashCode()}" };
        }

        private async Task<string> CallPythonModule(string module, string input, Dictionary<string, object>? parameters = null)
        {
            var moduleName = GetModuleManagerName(module);
            var escapedInput = input.Replace("'", "\\'").Replace("\"", "\\\"");
            var pythonCode = $@"import sys
sys.path.append(r'{_aiModulesPath}')
try:
    from core.{module.ToLower()} import {moduleName}
    manager = {moduleName}()
    result = manager.process('{escapedInput}')
    print(result)
except Exception as e:
    print(f'Error: {{e}}')";

            var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = _pythonPath,
                    Arguments = $"-c \"{pythonCode}\"",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                }
            };

            process.Start();
            var output = await process.StandardOutput.ReadToEndAsync();
            await process.WaitForExitAsync();

            return output.Trim();
        }

        private string GetModuleManagerName(string module)
        {
            return module.ToLower() switch
            {
                "nlp" => "NLPManager",
                "prediction" => "PredictionManager",
                "automation" => "AutomationManager",
                "learning" => "LearningManager",
                "integration" => "IntegrationManager",
                _ => "AIManager"
            };
        }

        private double GetJsonDouble(JsonElement root, string propertyName, double defaultValue)
        {
            try
            {
                return root.TryGetProperty(propertyName, out var property) && property.ValueKind == JsonValueKind.Number
                    ? property.GetDouble()
                    : defaultValue;
            }
            catch
            {
                return defaultValue;
            }
        }

        private string GetJsonString(JsonElement root, string propertyName, string defaultValue)
        {
            try
            {
                return root.TryGetProperty(propertyName, out var property) && property.ValueKind == JsonValueKind.String
                    ? property.GetString() ?? defaultValue
                    : defaultValue;
            }
            catch
            {
                return defaultValue;
            }
        }

        private bool GetJsonBool(JsonElement root, string propertyName, bool defaultValue)
        {
            try
            {
                if (root.TryGetProperty(propertyName, out var property))
                {
                    return property.ValueKind == JsonValueKind.True;
                }
            }
            catch
            {
                // Ignore errors and return default
            }
            return defaultValue;
        }

        private string[] GetJsonStringArray(JsonElement root, string propertyName)
        {
            try
            {
                if (root.TryGetProperty(propertyName, out var property) && property.ValueKind == JsonValueKind.Array)
                {
                    var list = new List<string>();
                    foreach (var item in property.EnumerateArray())
                    {
                        if (item.ValueKind == JsonValueKind.String)
                        {
                            list.Add(item.GetString() ?? "");
                        }
                    }
                    return list.ToArray();
                }
            }
            catch
            {
                // Ignore errors and return empty array
            }

            return Array.Empty<string>();
        }
    }

    // Supporting classes for AIServiceManager
    public class AIModule
    {
        public string Id { get; set; } = "";
        public string Name { get; set; } = "";
        public string Status { get; set; } = "";
        public string Description { get; set; } = "";
        public string Version { get; set; } = "";
        public DateTime LastUpdated { get; set; }
    }

    public class SystemEvent
    {
        public string Id { get; set; } = "";
        public string Type { get; set; } = "";
        public string Message { get; set; } = "";
        public DateTime Timestamp { get; set; }
        public string Source { get; set; } = "";
    }
}
