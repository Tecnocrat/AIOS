using System;
using System.Collections.Generic;
using Microsoft.Extensions.Logging;

namespace AIOS.Models
{
    /// <summary>
    /// Core data models for AIOS system
    /// These are the fundamental entities used across all layers
    /// </summary>

    #region AI Service Models

    public class AIResponse
    {
        public bool Success { get; set; }
        public string? Response { get; set; }
        public string? Error { get; set; }
        public string Module { get; set; } = "";
        public DateTime Timestamp { get; set; }
    // Extended fields used by UI layer
    public string Id { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public double Confidence { get; set; }
    public string ProcessedBy { get; set; } = string.Empty;
    public string HolographicSignature { get; set; } = string.Empty;
    public SystemAwareness? SystemAwareness { get; set; }
    public HolographicEnhancement? HolographicEnhancement { get; set; }
    public string ConversationId { get; set; } = string.Empty;
    public TimeSpan ProcessingTime { get; set; }
    public bool MultiModal { get; set; }
    public double FractalDimension { get; set; }
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

    public class NLPResponse
    {
        public string Input { get; set; } = "";
        public string Context { get; set; } = "";
        public string Intent { get; set; } = "";
        public Dictionary<string, object> Entities { get; set; } = new();
        public string Sentiment { get; set; } = "";
        public double Confidence { get; set; }
        public bool Success { get; set; }
        public string Response { get; set; } = "";
        public DateTime Timestamp { get; set; }
        public TimeSpan ProcessingTime { get; set; }
    }

    #endregion

    #region Evolution Models

    public class CodePopulation
    {
        public string Code { get; set; } = "";
        public double Fitness { get; set; }
        public int Generation { get; set; }
    }

    public class EvolvedCode
    {
        public string Code { get; set; } = "";
        public double FitnessScore { get; set; }
        public string AINLPEncoding { get; set; } = "";
        public int Generation { get; set; }
    }

    public class Intent
    {
        public string Description { get; set; } = "";
        public string Type { get; set; } = "";
        public Dictionary<string, object> Parameters { get; set; } = new();
    }

    #endregion

    #region Logging Models

    public class LogEntry
    {
        public string Id { get; set; } = "";
        public DateTime Timestamp { get; set; }
        public LogLevel Level { get; set; }
        public string Category { get; set; } = "";
        public string Message { get; set; } = "";
        public string Context { get; set; } = "";
        public TimeSpan ExecutionTime { get; set; }
        public Dictionary<string, object>? Data { get; set; }
    }

    public class LogContext
    {
        public string Name { get; set; } = "";
        public List<LogEntry> Logs { get; set; } = new();
    }

    public class AIAnalysisResult
    {
        public bool Success { get; set; }
        public string Message { get; set; } = "";
        public string Insights { get; set; } = "";
        public string Recommendations { get; set; } = "";
        public string Patterns { get; set; } = "";
        public DateTime Timestamp { get; set; }
    }

    public class LogEventArgs : EventArgs
    {
        public LogEntry LogEntry { get; set; } = new();
    }

    public class TerminalOutputEventArgs : EventArgs
    {
        public string Message { get; set; } = "";
        public ConsoleColor Color { get; set; }
        public DateTime Timestamp { get; set; }
    }

    public class AIAnalysisEventArgs : EventArgs
    {
        public AIAnalysisResult Analysis { get; set; } = new();
    }

    #endregion

    #region Maintenance Models

    public class MaintenanceResult
    {
        public bool Success { get; set; }
        public string Message { get; set; } = "";
        public Dictionary<string, object> Results { get; set; } = new();
        public DateTime Timestamp { get; set; }
        public List<string> Actions { get; set; } = new();
    }

    public class MaintenanceStatus
    {
        public string Status { get; set; } = "";
        public double HealthScore { get; set; }
        public string NetworkStatus { get; set; } = "";
        public int ActiveConnections { get; set; }
        public Dictionary<string, object> SystemMetrics { get; set; } = new();
        public string[] Alerts { get; set; } = Array.Empty<string>();
        public Dictionary<string, object> Performance { get; set; } = new();
        public DateTime Timestamp { get; set; }
    }

    public class TachyonicArchiveInfo
    {
        public string Status { get; set; } = "";
        public long TotalSize { get; set; }
        public int FileCount { get; set; }
        public DateTime LastBackup { get; set; }
        public string[] RecentOperations { get; set; } = Array.Empty<string>();
    }

    #endregion

    #region Runtime Monitor Models

    public class SystemHealthSnapshot
    {
        public double HealthScore { get; set; }
        public string Status { get; set; } = "";
        public int ErrorCount { get; set; }
        public int WarningCount { get; set; }
        public int TotalLogEntries { get; set; }
        public int AINLPOperations { get; set; }
        public int DatabaseOperations { get; set; }
        public int EvolutionOperations { get; set; }
        public DateTime Timestamp { get; set; }
    }

    public class SystemMetrics
    {
        public string Category { get; set; } = "";
        public DateTime Hour { get; set; }
        public int TotalOperations { get; set; }
        public double AverageExecutionTime { get; set; }
        public int ErrorCount { get; set; }
        public int WarningCount { get; set; }
    }

    public class RuntimeStatusEventArgs : EventArgs
    {
        public string Status { get; set; } = "";
        public string Details { get; set; } = "";
    }

    public class PerformanceMetricsEventArgs : EventArgs
    {
        public Dictionary<string, double> Metrics { get; set; } = new();
    }

    #endregion

    #region UI and Holographic System Models

    public class HolographicContext
    {
        public Dictionary<string, object> GlobalContext { get; set; } = new();
        public Dictionary<string, ComponentState> ComponentStates { get; set; } = new();
        public DateTime LastUpdate { get; set; }
        public double FractalCoherence { get; set; }
    }

    public class ComponentState
    {
        public string Name { get; set; } = "";
        public string Status { get; set; } = "";
        public object? Value { get; set; }
        public DateTime LastUpdate { get; set; }
        // Extended fields for UI compatibility
        public DateTime LastSync { get; set; }
        public Dictionary<string, object> Metadata { get; set; } = new();
    }

    public class HolographicSystemState
    {
        public bool IsActive { get; set; }
        public string Status { get; set; } = "";
        public Dictionary<string, ComponentState> Components { get; set; } = new();
        // Helper to update state from context and reflections
        public void Update(HolographicContext context, Dictionary<string, ComponentReflection> reflections)
        {
            IsActive = true;
            Status = "operational";
            Components = context.ComponentStates;
            // Optionally merge reflections metadata
            foreach (var kvp in reflections)
            {
                if (!Components.ContainsKey(kvp.Key))
                {
                    Components[kvp.Key] = new ComponentState { Name = kvp.Value.Name, Status = "reflected", LastUpdate = DateTime.Now, LastSync = DateTime.Now, Metadata = kvp.Value.Properties };
                }
                else
                {
                    foreach (var prop in kvp.Value.Properties)
                    {
                        Components[kvp.Key].Metadata[prop.Key] = prop.Value;
                    }
                }
            }
        }
    }

    public class ComponentReflection
    {
        public string Name { get; set; } = "";
        public string Type { get; set; } = "";
        public Dictionary<string, object> Properties { get; set; } = new();
    }

    public class ExtensionStatus
    {
        public string Name { get; set; } = "";
    public bool IsEnabled { get; set; }
        public string Version { get; set; } = "";
    public string Status { get; set; } = "";
    // Extended fields for UI bridge compatibility
    public bool IsActive { get; set; }
    public string Message { get; set; } = string.Empty;
    }

    public class AIResponseEventArgs : EventArgs
    {
    public AIResponse Response { get; set; } = new();
    // Extended event context for UI consumers
    public AIRequest? Request { get; set; }
    public AIConversation? Conversation { get; set; }
    public Exception? Error { get; set; }
    }

    public class ContextHealthEventArgs : EventArgs
    {
    public ContextHealthResult Result { get; set; } = new();
    public string TriggerInput { get; set; } = string.Empty;
    public bool RecoveryExecuted { get; set; }
    public List<string> RecoverySteps { get; set; } = new();
    public DateTime Timestamp { get; set; }
    public bool MonitoringCheck { get; set; }
    // Back-compat alias expected by some UI code
    public ContextHealthResult ContextHealth { get => Result; set => Result = value; }
    }

    public class ContextHealthResult
    {
    public bool IsHealthy { get; set; }
    public string Status { get; set; } = "";
    public List<string> Issues { get; set; } = new();
    public DateTime Timestamp { get; set; }
    // Extended fields used by UI
    public double Score { get; set; }
    public List<string> Indicators { get; set; } = new();
    public DateTime LastCheck { get; set; }
    public List<string> RecoveryActions { get; set; } = new();
    public bool NeedsImmediateRecovery { get; set; }
    }

    public class RecoveryResult
    {
        public bool Success { get; set; }
        public string Message { get; set; } = "";
        public List<string> Actions { get; set; } = new();
    // Extended fields expected by UI
    public DateTime Timestamp { get; set; }
    public List<string> StepsExecuted { get; set; } = new();
    public List<string> FilesRead { get; set; } = new();
    }

    public class AIStreamChunk
    {
    public string Content { get; set; } = "";
    public bool IsComplete { get; set; }
    public int ChunkIndex { get; set; }
    // Extended streaming metadata
    public string Id { get; set; } = string.Empty;
    public string ConversationId { get; set; } = string.Empty;
    public DateTime Timestamp { get; set; }
    public double FractalCoherence { get; set; }
    }

    public class AIAnalysis
    {
        public string Content { get; set; } = "";
        public AnalysisType Type { get; set; }
        public double Confidence { get; set; }
        public Dictionary<string, object> Metadata { get; set; } = new();
        // Extended fields for UI analysis flows
        public string Id { get; set; } = string.Empty;
        public string InputText { get; set; } = string.Empty;
        public AnalysisType AnalysisType { get; set; }
        public DateTime Timestamp { get; set; }
        public HolographicContext? HolographicContext { get; set; }
        public Dictionary<string, object> Results { get; set; } = new();
    }

    public enum AnalysisType
    {
        Sentiment,
        Intent,
        Entity,
        Classification,
        Summarization,
        Comprehensive,
        Context,
        Fractal
    }

    public class InputAnalysis
    {
        public string Input { get; set; } = "";
        public string Intent { get; set; } = "";
        public Dictionary<string, object> Entities { get; set; } = new();
        public double Confidence { get; set; }
    // Extended fields for UI flows
    public double Complexity { get; set; }
    public List<string> RequiredComponents { get; set; } = new();
    public string FractalPattern { get; set; } = string.Empty;
    public double ContextRelevance { get; set; }
    }

    public class SystemAwareness
    {
        public Dictionary<string, object> SystemState { get; set; } = new();
        public List<string> ActiveModules { get; set; } = new();
        public DateTime LastUpdate { get; set; }
        // Extended fields
        public int ActiveComponents { get; set; }
        public string SystemHealth { get; set; } = string.Empty;
        public double FractalCoherence { get; set; }
    }

    public class MultiModalInput
    {
        public string Text { get; set; } = "";
        public byte[]? Audio { get; set; }
        public byte[]? Image { get; set; }
        public string Type { get; set; } = "";
        // Alternate property names used by UI
        public byte[]? AudioData { get; set; }
        public byte[]? ImageData { get; set; }
    }

    public class AIRequest
    {
        public string Input { get; set; } = "";
        public AIRequestType Type { get; set; }
        public Dictionary<string, object> Parameters { get; set; } = new();
        public string Context { get; set; } = "";
        // Extended fields used in UI request pipeline
        public string Id { get; set; } = string.Empty;
        public string ConversationId { get; set; } = string.Empty;
        public string UserInput { get; set; } = string.Empty;
        public DateTime Timestamp { get; set; }
        public HolographicContext? HolographicContext { get; set; }
        public AIRequestType RequestType { get; set; }
        public int Priority { get; set; }
    }

    public enum AIRequestType
    {
        Query,
        Analysis,
        Generation,
        Translation,
        Summarization,
        General
    }

    public class VSCodeMessage
    {
        public string Type { get; set; } = "";
        public string Content { get; set; } = "";
    public object Data { get; set; } = new();
        public DateTime Timestamp { get; set; }
    }

    public class AIConversation
    {
        public string Id { get; set; } = "";
        public List<AIMessage> Messages { get; set; } = new();
        public DateTime StartTime { get; set; }
        public DateTime LastUpdate { get; set; }
        // Extended conversation tracking used by UI
        public List<AIExchange> Exchanges { get; set; } = new();
        public void AddExchange(AIRequest request, AIResponse response)
        {
            var ex = new AIExchange
            {
                Request = request,
                Response = response,
                Timestamp = DateTime.Now
            };
            Exchanges.Add(ex);
            Messages.Add(new AIMessage { Role = "user", Content = request.UserInput, Timestamp = request.Timestamp });
            Messages.Add(new AIMessage { Role = "assistant", Content = response.Content ?? response.Response ?? string.Empty, Timestamp = response.Timestamp });
            LastUpdate = DateTime.Now;
        }
    }

    public class AIExchange
    {
        public AIRequest Request { get; set; } = new();
        public AIResponse Response { get; set; } = new();
        public DateTime Timestamp { get; set; }
    }

    public class AIMessage
    {
        public string Role { get; set; } = "";
        public string Content { get; set; } = "";
        public DateTime Timestamp { get; set; }
    }

    #endregion

    #region AINLP and Core Models

    public class AINLPCompiler
    {
        public string Version { get; set; } = "1.0";
        public bool IsInitialized { get; set; }

        public Task<AIResponse> CompileAsync(string input)
        {
            return Task.FromResult(new AIResponse
            {
                Success = true,
                Response = $"Compiled: {input}",
                Timestamp = DateTime.Now
            });
        }

        // Minimal stub to satisfy UI calls; real implementation lives in core
        public Task<CompilationResult> CompileNaturalLanguage(string specification)
        {
            return Task.FromResult(new CompilationResult
            {
                Success = true,
                GeneratedCode = new ExecutableCode { Code = "// generated code", Language = "C#" },
                Confidence = 0.9
            });
        }
    }

    // Minimal types referenced by UI demo when interacting with AINLP
    public class ExecutableCode
    {
        public string Code { get; set; } = string.Empty;
        public string Language { get; set; } = string.Empty;
    }

    public class CompilationResult
    {
        public bool Success { get; set; }
        public ExecutableCode GeneratedCode { get; set; } = new ExecutableCode();
        public double Confidence { get; set; }
        public string Error { get; set; } = string.Empty;
    }

    public class FractalContextManager
    {
        private readonly Dictionary<string, object> _holographicContext;
        private readonly object _contextLock = new object();
        private DateTime _lastUpdate;

        public FractalContextManager()
        {
            _holographicContext = new Dictionary<string, object>();
            _lastUpdate = DateTime.Now;
        }

    // Shim for UI usage
    public HolographicContext CurrentContext => GetHolographicContext();
    public void Initialize() { /* no-op for now */ }

        public HolographicContext GetHolographicContext()
        {
            lock (_contextLock)
            {
                return new HolographicContext
                {
                    GlobalContext = new Dictionary<string, object>(_holographicContext),
                    ComponentStates = GetComponentStates(),
                    LastUpdate = _lastUpdate,
                    FractalCoherence = CalculateFractalCoherence()
                };
            }
        }

        public void UpdateContext(string key, object value)
        {
            lock (_contextLock)
            {
                _holographicContext[key] = value;
                _lastUpdate = DateTime.Now;
            }
        }

        private Dictionary<string, ComponentState> GetComponentStates()
        {
            return new Dictionary<string, ComponentState>
            {
                ["csharp_ui"] = new ComponentState { Status = "active", LastUpdate = DateTime.Now },
                ["cpp_core"] = new ComponentState { Status = "monitoring", LastUpdate = DateTime.Now.AddMinutes(-1) },
                ["python_ai"] = new ComponentState { Status = "processing", LastUpdate = DateTime.Now.AddSeconds(-30) },
                ["vscode_extension"] = new ComponentState { Status = "connected", LastUpdate = DateTime.Now.AddSeconds(-10) },
                ["ainlp_compiler"] = new ComponentState { Status = "ready", LastUpdate = DateTime.Now.AddMinutes(-2) }
            };
        }

        private double CalculateFractalCoherence()
        {
            return 0.87; // Simulated coherence metric
        }
    }

    public class HolographicUIOrchestrator
    {
        private readonly FractalContextManager _contextManager;

        public HolographicUIOrchestrator(FractalContextManager contextManager)
        {
            _contextManager = contextManager;
        }

        public Task StartAsync()
        {
            return Task.CompletedTask;
        }

    // Shim for UI usage
    public void Initialize() { /* no-op for now */ }
    }

    public class VSCodeExtensionBridge
    {
        public Task ConnectAsync()
        {
            return Task.CompletedTask;
        }

        public Task SendMessageAsync(VSCodeMessage message)
        {
            return Task.CompletedTask;
        }
    }

    public class ContextRecoveryUI
    {
        private readonly FractalContextManager _contextManager;

        public ContextRecoveryUI(FractalContextManager contextManager)
        {
            _contextManager = contextManager;
        }

        public Task<RecoveryResult> RecoverAsync()
        {
            return Task.FromResult(new RecoveryResult { Success = true, Message = "Recovery completed" });
        }
    }

    public class HolographicEnhancement
    {
        public string Type { get; set; } = "";
        public Dictionary<string, object> Properties { get; set; } = new();
        // Extended fields expected by UI
        public string ContextIntegration { get; set; } = string.Empty;
        public double FractalResonance { get; set; }
        public double SystemCoherence { get; set; }
    }

    #endregion
}
