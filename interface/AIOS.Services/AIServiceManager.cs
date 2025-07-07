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

    public async Task<SystemHealthResponse> GetSystemHealthAsync()
    {
        try
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
                    HealthScore = healthData.GetProperty("health_score").GetDouble(),
                    HealthStatus = healthData.GetProperty("health_status").GetString() ?? "Unknown",
                    Issues = JsonElementToStringArray(healthData, "issues"),
                    Warnings = JsonElementToStringArray(healthData, "warnings"),
                    Recommendations = JsonElementToStringArray(healthData, "recommendations"),
                    TriggerReingestion = healthData.GetProperty("trigger_reingestion").GetBoolean(),
                    Timestamp = DateTime.UtcNow
                };
            }
            else
            {
                return new SystemHealthResponse
                {
                    Success = false,
                    Error = "Failed to get health data from monitor",
                    Timestamp = DateTime.UtcNow
                };
            }
        }
        catch (Exception ex)
        {
            return new SystemHealthResponse
            {
                Success = false,
                Error = ex.Message,
                Timestamp = DateTime.UtcNow
            };
        }
    }

    public async Task<bool> TestIntegrationAsync()
    {
        try
        {
            var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = _pythonPath,
                    Arguments = "scripts/test_integration.py",
                    WorkingDirectory = @"c:\dev\AIOS",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                }
            };

            process.Start();
            await process.WaitForExitAsync();
            
            return process.ExitCode == 0;
        }
        catch
        {
            return false;
        }
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
                Arguments = $"-c \"{pythonCode.Replace("\"", "\\\"")}\"",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            }
        };

        process.Start();
        var output = await process.StandardOutput.ReadToEndAsync();
        var error = await process.StandardError.ReadToEndAsync();
        await process.WaitForExitAsync();

        if (process.ExitCode == 0)
        {
            return output.Trim();
        }
        else
        {
            throw new Exception($"Python module error: {error}");
        }
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
            _ => "NLPManager"
        };
    }

    private string[] JsonElementToStringArray(JsonElement root, string propertyName)
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
