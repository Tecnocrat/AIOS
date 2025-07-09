using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text.Json;
using System.Threading.Tasks;

namespace AIOS.Services;

public class AIServiceManager
{
    private readonly string _pythonPath;
    private readonly string _aiModulesPath;

    public AIServiceManager()
    {
        _pythonPath = "python";
        _aiModulesPath = @"c:\dev\AIOS\ai\src";
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

    // AINLP Evolution Support Methods
    public async Task<Dictionary<string, object>> ProcessNLP(string input)
    {
        try
        {
            var result = await CallPythonModule("nlp", input);
            return JsonSerializer.Deserialize<Dictionary<string, object>>(result) ?? new Dictionary<string, object>();
        }
        catch
        {
            return new Dictionary<string, object> { { "error", "NLP processing failed" } };
        }
    }

    public object GeneratePrediction(Dictionary<string, object> inputData, string modelType)
    {
        // Placeholder for prediction generation
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

        return new SystemHealthResponse
        {
            Success = false,
            Error = "Failed to get system health",
            Timestamp = DateTime.UtcNow
        };
    }

    // AINLP Evolution Support Methods for DatabaseService
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

    public async Task<bool> PredictCacheInvalidation(string key, object data)
    {
        try
        {
            var predictionResult = await CallPythonModule("prediction", JsonSerializer.Serialize(new
            {
                operation = "predict_cache_invalidation",
                key = key,
                data = data
            }));

            var result = JsonSerializer.Deserialize<Dictionary<string, object>>(predictionResult);
            return result?.ContainsKey("should_invalidate") == true && Convert.ToBoolean(result["should_invalidate"]);
        }
        catch
        {
            return false;
        }
    }

    public string? GetComponentReflections()
    {
        // Placeholder for component reflections
        return JsonSerializer.Serialize(new Dictionary<string, object>());
    }

    private async Task<string> CallPythonModule(string module, string input, Dictionary<string, object>? parameters = null)
    {
        var moduleName = GetModuleManagerName(module);
        var escapedInput = input.Replace("'", "\\'").Replace("\"", "\\\"");

        var pythonCode = $@"
import sys
sys.path.append(r'{_aiModulesPath}')
try:
    from core.{module.ToLower()} import {moduleName}
    manager = {moduleName}()
    result = manager.process('{escapedInput}')
    print(result)
except Exception as e:
    print(f'Error: {{e}}')
";

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

public class AIResponse
{
    public bool Success { get; set; }
    public string? Response { get; set; }
    public string? Error { get; set; }
    public string Module { get; set; } = "";
    public DateTime Timestamp { get; set; }
}

public class SystemHealthResponse
{
    public bool Success { get; set; }
    public double HealthScore { get; set; }
    public string HealthStatus { get; set; } = "";
    public string[] Issues { get; set; } = Array.Empty<string>();
    public string[] Warnings { get; set; } = Array.Empty<string>();
    public string[] Recommendations { get; set; } = Array.Empty<string>();
    public bool TriggerReingestion { get; set; }
    public string? Error { get; set; }
    public DateTime Timestamp { get; set; }
}

public class ValidationResult
{
    public bool IsValid { get; set; }
    public List<string> Errors { get; set; } = new();
}
