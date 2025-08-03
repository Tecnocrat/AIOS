using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace AIOS.Models
{
    /// <summary>
    /// Interface for AI service operations
    /// Defines contract for AI-related functionality
    /// </summary>
    public interface IAIService
    {
        Task<Dictionary<string, object>> ProcessNLPAsync(string input);
        Task<AIResponse> ProcessAsync(string module, string input, Dictionary<string, object>? parameters = null);
        Task<int> PredictCacheTTL(object data);
        Task<bool> ValidateData(object data);
        Task<object> TransformDataForStorage(object data);
        Task<bool> LearnFromData(object data);
        Task<string[]> PredictCacheInvalidation(string collection, object data);
        Task<SystemHealthResponse> GetSystemHealthAsync();
        object GeneratePrediction(Dictionary<string, object> inputData, string modelType);
        ValidationResult ValidateInput(object input);
        string[] GetCacheKeys(string collection, object data);
    }

    /// <summary>
    /// Interface for database operations
    /// Defines contract for data persistence
    /// </summary>
    public interface IDatabaseService
    {
        Task<string> ExecuteQuery(string query);
        Task<string> SaveData(string collection, string jsonData);
        Task<string> ProcessAINLPCommand(string naturalLanguageCommand);
    }

    /// <summary>
    /// Interface for runtime logging
    /// Defines contract for system monitoring
    /// </summary>
    public interface IRuntimeLoggingService
    {
        void LogAINLPExecution(string command, string result, TimeSpan executionTime, string context = "");
        void LogDatabaseOperation(string operation, string query, object result, TimeSpan executionTime, string context = "");
        void LogCodeEvolution(string generation, double fitnessScore, string evolutionMetrics, string context = "");
        void LogSystemError(Exception exception, string context = "", string operation = "");
        void LogPerformanceMetrics(string operation, Dictionary<string, object> metrics, string context = "");
        Task<AIAnalysisResult> AnalyzeLogsWithAI(string timespan = "1h", string category = "");
        List<LogEntry> GetRecentLogs(string timespan = "1h", string category = "");
        void StartRealTimeMonitoring(string[] categories = null);
        void Dispose();
    }

    /// <summary>
    /// Interface for maintenance operations
    /// Defines contract for system maintenance
    /// </summary>
    public interface IMaintenanceService
    {
        Task<MaintenanceResult> RunQuickOptimizationAsync();
        Task<MaintenanceResult> RunFullMaintenanceAsync();
        Task<MaintenanceStatus> GetMaintenanceStatusAsync();
        Task<TachyonicArchiveInfo> GetTachyonicArchiveInfoAsync();
    }
}
