using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace AIOS.Models
{
    /// <summary>
    /// AIOS Runtime Monitor - Central hub for real-time system monitoring
    /// Provides WPF UI integration for terminal output and logging
    /// Enables runtime iteration and debugging through visual feedback
    /// </summary>
    public class AIOSRuntimeMonitor : IDisposable
    {
        private readonly RuntimeLoggingService _loggingService;
        private readonly DatabaseService _databaseService;
        private readonly IAIService _aiService;
        private readonly List<string> _activePanels;
        private readonly Dictionary<string, SystemMetrics> _metricsHistory;
        private readonly CancellationTokenSource _cancellationTokenSource;
        private Timer _metricsTimer;

        public event EventHandler<RuntimeStatusEventArgs>? StatusChanged;
        public event EventHandler<PerformanceMetricsEventArgs>? MetricsUpdated;

        public AIOSRuntimeMonitor(IAIService aiService, DatabaseService databaseService)
        {
            _aiService = aiService;
            _databaseService = databaseService;
            _loggingService = new RuntimeLoggingService(aiService);
            _activePanels = new List<string>();
            _metricsHistory = new Dictionary<string, SystemMetrics>();
            _cancellationTokenSource = new CancellationTokenSource();

            InitializeEventHandlers();
            InitializeMetricsTimer();
            StartRealTimeMonitoring();
        }
        public List<LogEntry> GetTerminalOutput(int maxLines = 100)
        {
            return _loggingService.GetRecentLogs("1h").TakeLast(maxLines).ToList();
        }

        public Dictionary<string, double> GetPerformanceMetrics()
        {
            var recentLogs = _loggingService.GetRecentLogs("1h");
            return new Dictionary<string, double>
            {
                ["TotalOperations"] = recentLogs.Count,
                ["AINLPOperations"] = recentLogs.Count(l => l.Category == "AINLP"),
                ["DatabaseOperations"] = recentLogs.Count(l => l.Category == "Database"),
                ["EvolutionOperations"] = recentLogs.Count(l => l.Category == "Evolution"),
                ["ErrorCount"] = recentLogs.Count(l => l.Level == Microsoft.Extensions.Logging.LogLevel.Error),
                ["WarningCount"] = recentLogs.Count(l => l.Level == Microsoft.Extensions.Logging.LogLevel.Warning),
                ["AverageExecutionTime"] = recentLogs.Where(l => l.ExecutionTime > TimeSpan.Zero).Average(l => l.ExecutionTime.TotalMilliseconds)
            };
        }

        public List<AIAnalysisResult> GetAIAnalysisHistory(int maxResults = 10)
        {
            // This would be populated from AI analysis events
            return new List<AIAnalysisResult>();
        }

        public List<LogEntry> GetCodeEvolutionHistory()
        {
            return _loggingService.GetRecentLogs("1h", "Evolution");
        }

        public async Task<string> ExecuteAINLPCommand(string command)
        {
            _loggingService.LogAINLPExecution(command, "Command received", TimeSpan.Zero, "AIOSRuntimeMonitor");

            try
            {
                var result = await _databaseService.ProcessAINLPCommand(command);
                return result;
            }
            catch (Exception ex)
            {
                _loggingService.LogSystemError(ex, "AIOSRuntimeMonitor", command);
                throw;
            }
        }

        public async Task<SystemHealthSnapshot> GetSystemHealthSnapshot()
        {
            var healthResponse = await _aiService.GetSystemHealthAsync();
            var recentLogs = _loggingService.GetRecentLogs("1h");
            var errorCount = recentLogs.Count(l => l.Level == Microsoft.Extensions.Logging.LogLevel.Error);
            var warningCount = recentLogs.Count(l => l.Level == Microsoft.Extensions.Logging.LogLevel.Warning);

            return new SystemHealthSnapshot
            {
                HealthScore = healthResponse.HealthScore,
                Status = healthResponse.HealthStatus,
                ErrorCount = errorCount,
                WarningCount = warningCount,
                TotalLogEntries = recentLogs.Count,
                AINLPOperations = recentLogs.Count(l => l.Category == "AINLP"),
                DatabaseOperations = recentLogs.Count(l => l.Category == "Database"),
                EvolutionOperations = recentLogs.Count(l => l.Category == "Evolution"),
                Timestamp = DateTime.UtcNow
            };
        }

        public void StartRealTimeAnalysis()
        {
            _loggingService.StartRealTimeMonitoring();

            // Start continuous AI analysis
            _ = Task.Run(async () =>
            {
                while (!_cancellationTokenSource.Token.IsCancellationRequested)
                {
                    try
                    {
                        var analysis = await _loggingService.AnalyzeLogsWithAI("15m");
                        if (analysis.Success)
                        {
                            StatusChanged?.Invoke(this, new RuntimeStatusEventArgs
                            {
                                Status = "AI Analysis Complete",
                                Details = analysis.Insights
                            });
                        }

                        await Task.Delay(TimeSpan.FromMinutes(15), _cancellationTokenSource.Token);
                    }
                    catch (OperationCanceledException)
                    {
                        break;
                    }
                    catch (Exception ex)
                    {
                        _loggingService.LogSystemError(ex, "StartRealTimeAnalysis", "Continuous analysis loop");
                    }
                }
            });
        }

        private void InitializeEventHandlers()
        {
            _loggingService.LogReceived += (sender, args) =>
            {
                // Update metrics based on log entries
                UpdateMetricsFromLogEntry(args.LogEntry);
            };
        }

        private void InitializeMetricsTimer()
        {
            _metricsTimer = new Timer(async _ => await UpdateSystemMetrics(), null, TimeSpan.Zero, TimeSpan.FromSeconds(5));
        }

        private void StartRealTimeMonitoring()
        {
            // Start real-time monitoring for all categories
            _loggingService.StartRealTimeMonitoring(new[] { "AINLP", "Database", "Evolution", "System", "Performance" });
        }

        private void UpdateMetricsFromLogEntry(LogEntry logEntry)
        {
            var key = $"{logEntry.Category}_{DateTime.UtcNow:yyyyMMddHH}";
            if (!_metricsHistory.ContainsKey(key))
            {
                _metricsHistory[key] = new SystemMetrics { Category = logEntry.Category, Hour = DateTime.UtcNow };
            }

            var metrics = _metricsHistory[key];
            metrics.TotalOperations++;
            metrics.AverageExecutionTime = (metrics.AverageExecutionTime + logEntry.ExecutionTime.TotalMilliseconds) / 2;

            if (logEntry.Level == Microsoft.Extensions.Logging.LogLevel.Error)
                metrics.ErrorCount++;
            else if (logEntry.Level == Microsoft.Extensions.Logging.LogLevel.Warning)
                metrics.WarningCount++;
        }

        private async Task UpdateSystemMetrics()
        {
            try
            {
                var snapshot = await GetSystemHealthSnapshot();
                var metrics = new Dictionary<string, double>
                {
                    ["HealthScore"] = snapshot.HealthScore,
                    ["ErrorCount"] = snapshot.ErrorCount,
                    ["WarningCount"] = snapshot.WarningCount,
                    ["TotalOperations"] = snapshot.TotalLogEntries,
                    ["AINLPOperations"] = snapshot.AINLPOperations,
                    ["DatabaseOperations"] = snapshot.DatabaseOperations,
                    ["EvolutionOperations"] = snapshot.EvolutionOperations
                };

                MetricsUpdated?.Invoke(this, new PerformanceMetricsEventArgs { Metrics = metrics });
            }
            catch (Exception ex)
            {
                _loggingService.LogSystemError(ex, "UpdateSystemMetrics", "Metrics update timer");
            }
        }
        public void Dispose()
        {
            _cancellationTokenSource?.Cancel();
            _metricsTimer?.Dispose();
            _loggingService?.Dispose();
            _cancellationTokenSource?.Dispose();
        }
    }
}
