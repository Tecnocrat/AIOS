using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace AIOS.Models
{
    /// <summary>
    /// Advanced Runtime Logging and Terminal Output Architecture
    /// Provides real-time feedback for iterative improvements and debugging
    /// Integrates with AIOS kernel and AINLP logic for comprehensive monitoring
    /// </summary>
    public class RuntimeLoggingService
    {
        private readonly ConcurrentQueue<LogEntry> _logQueue;
        private readonly Dictionary<string, LogContext> _logContexts;
        private readonly CancellationTokenSource _cancellationTokenSource;
        private readonly Task _logProcessingTask;
        private readonly IAIService _aiService;
        private readonly string _logDirectory;
        private readonly bool _enableTerminalOutput;
        private readonly bool _enableFileOutput;
        private readonly bool _enableAIAnalysis;

        public event EventHandler<LogEventArgs>? LogReceived;
        public event EventHandler<TerminalOutputEventArgs>? TerminalOutputReceived;
        public event EventHandler<AIAnalysisEventArgs>? AIAnalysisReceived;

        public RuntimeLoggingService(IAIService aiService, bool enableTerminalOutput = true, bool enableFileOutput = true, bool enableAIAnalysis = true)
        {
            _logQueue = new ConcurrentQueue<LogEntry>();
            _logContexts = new Dictionary<string, LogContext>();
            _cancellationTokenSource = new CancellationTokenSource();
            _aiService = aiService;
            _logDirectory = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "logs");
            _enableTerminalOutput = enableTerminalOutput;
            _enableFileOutput = enableFileOutput;
            _enableAIAnalysis = enableAIAnalysis;

            EnsureLogDirectoryExists();
            _logProcessingTask = Task.Run(ProcessLogQueueAsync);
        }

        public void LogAINLPExecution(string command, string result, TimeSpan executionTime, string context = "")
        {
            var logEntry = new LogEntry
            {
                Id = Guid.NewGuid().ToString(),
                Timestamp = DateTime.UtcNow,
                Level = LogLevel.Information,
                Category = "AINLP",
                Message = $"AINLP Command: {command}",
                Context = context,
                ExecutionTime = executionTime,
                Data = new Dictionary<string, object>
                {
                    ["command"] = command,
                    ["result"] = result,
                    ["executionTimeMs"] = executionTime.TotalMilliseconds
                }
            };

            EnqueueLog(logEntry);

            if (_enableTerminalOutput)
            {
                WriteToTerminal($"[AINLP] {command} -> {result} ({executionTime.TotalMilliseconds:F2}ms)", ConsoleColor.Cyan);
            }
        }

        public void LogDatabaseOperation(string operation, string query, object result, TimeSpan executionTime, string context = "")
        {
            var logEntry = new LogEntry
            {
                Id = Guid.NewGuid().ToString(),
                Timestamp = DateTime.UtcNow,
                Level = LogLevel.Information,
                Category = "Database",
                Message = $"DB Operation: {operation}",
                Context = context,
                ExecutionTime = executionTime,
                Data = new Dictionary<string, object>
                {
                    ["operation"] = operation,
                    ["query"] = query,
                    ["result"] = result,
                    ["executionTimeMs"] = executionTime.TotalMilliseconds
                }
            };

            EnqueueLog(logEntry);

            if (_enableTerminalOutput)
            {
                WriteToTerminal($"[DB] {operation}: {query} ({executionTime.TotalMilliseconds:F2}ms)", ConsoleColor.Green);
            }
        }

        public void LogCodeEvolution(string generation, double fitnessScore, string evolutionMetrics, string context = "")
        {
            var logEntry = new LogEntry
            {
                Id = Guid.NewGuid().ToString(),
                Timestamp = DateTime.UtcNow,
                Level = LogLevel.Information,
                Category = "Evolution",
                Message = $"Code Evolution: Generation {generation}, Fitness: {fitnessScore:F3}",
                Context = context,
                Data = new Dictionary<string, object>
                {
                    ["generation"] = generation,
                    ["fitnessScore"] = fitnessScore,
                    ["metrics"] = evolutionMetrics
                }
            };

            EnqueueLog(logEntry);

            if (_enableTerminalOutput)
            {
                WriteToTerminal($"[EVOLUTION] Gen {generation} -> Fitness: {fitnessScore:F3} | {evolutionMetrics}", ConsoleColor.Magenta);
            }
        }

        public void LogSystemError(Exception exception, string context = "", string operation = "")
        {
            var logEntry = new LogEntry
            {
                Id = Guid.NewGuid().ToString(),
                Timestamp = DateTime.UtcNow,
                Level = LogLevel.Error,
                Category = "System",
                Message = $"System Error: {exception.Message}",
                Context = context,
                Data = new Dictionary<string, object>
                {
                    ["operation"] = operation,
                    ["exception"] = exception.ToString(),
                    ["stackTrace"] = exception.StackTrace ?? ""
                }
            };

            EnqueueLog(logEntry);

            if (_enableTerminalOutput)
            {
                WriteToTerminal($"[ERROR] {operation}: {exception.Message}", ConsoleColor.Red);
            }
        }

        public void LogPerformanceMetrics(string operation, Dictionary<string, object> metrics, string context = "")
        {
            var logEntry = new LogEntry
            {
                Id = Guid.NewGuid().ToString(),
                Timestamp = DateTime.UtcNow,
                Level = LogLevel.Information,
                Category = "Performance",
                Message = $"Performance Metrics: {operation}",
                Context = context,
                Data = metrics
            };

            EnqueueLog(logEntry);

            if (_enableTerminalOutput)
            {
                var metricsJson = JsonSerializer.Serialize(metrics);
                WriteToTerminal($"[PERF] {operation}: {metricsJson}", ConsoleColor.Yellow);
            }
        }

        public async Task<AIAnalysisResult> AnalyzeLogsWithAI(string timespan = "1h", string category = "")
        {
            if (!_enableAIAnalysis)
                return new AIAnalysisResult { Success = false, Message = "AI analysis is disabled" };

            try
            {
                var logs = GetRecentLogs(timespan, category);
                var analysisPrompt = $"Analyze these system logs for patterns, issues, and optimization opportunities: {JsonSerializer.Serialize(logs)}";

                var analysisResult = await _aiService.ProcessNLPAsync(analysisPrompt);

                var result = new AIAnalysisResult
                {
                    Success = true,
                    Insights = analysisResult.ContainsKey("insights") ? analysisResult["insights"]?.ToString() ?? "" : "",
                    Recommendations = analysisResult.ContainsKey("recommendations") ? analysisResult["recommendations"]?.ToString() ?? "" : "",
                    Patterns = analysisResult.ContainsKey("patterns") ? analysisResult["patterns"]?.ToString() ?? "" : "",
                    Timestamp = DateTime.UtcNow
                };

                AIAnalysisReceived?.Invoke(this, new AIAnalysisEventArgs { Analysis = result });
                return result;
            }
            catch (Exception ex)
            {
                LogSystemError(ex, "AI log analysis", "AnalyzeLogsWithAI");
                return new AIAnalysisResult { Success = false, Message = ex.Message };
            }
        }

        public List<LogEntry> GetRecentLogs(string timespan = "1h", string category = "")
        {
            var logs = new List<LogEntry>();
            var cutoffTime = DateTime.UtcNow.Subtract(ParseTimespan(timespan));

            // This is a simplified implementation - in a real system, you'd query from persistent storage
            foreach (var kvp in _logContexts)
            {
                var context = kvp.Value;
                foreach (var logEntry in context.Logs)
                {
                    if (logEntry.Timestamp >= cutoffTime)
                    {
                        if (string.IsNullOrEmpty(category) || logEntry.Category.Equals(category, StringComparison.OrdinalIgnoreCase))
                        {
                            logs.Add(logEntry);
                        }
                    }
                }
            }

            return logs;
        }

        public void StartRealTimeMonitoring(string[] categories = null)
        {
            var categoriesToMonitor = categories ?? new[] { "AINLP", "Database", "Evolution", "System", "Performance" };

            _ = Task.Run(async () =>
            {
                while (!_cancellationTokenSource.Token.IsCancellationRequested)
                {
                    foreach (var category in categoriesToMonitor)
                    {
                        var recentLogs = GetRecentLogs("5m", category);
                        if (recentLogs.Count > 0)
                        {
                            var analysis = await AnalyzeLogsWithAI("5m", category);
                            if (analysis.Success && !string.IsNullOrEmpty(analysis.Insights))
                            {
                                WriteToTerminal($"[AI-MONITOR] {category}: {analysis.Insights}", ConsoleColor.Blue);
                            }
                        }
                    }

                    await Task.Delay(TimeSpan.FromMinutes(5), _cancellationTokenSource.Token);
                }
            });
        }

        private async Task ProcessLogQueueAsync()
        {
            while (!_cancellationTokenSource.Token.IsCancellationRequested)
            {
                try
                {
                    if (_logQueue.TryDequeue(out var logEntry))
                    {
                        await ProcessLogEntry(logEntry);
                    }
                    else
                    {
                        await Task.Delay(100, _cancellationTokenSource.Token);
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error processing log queue: {ex.Message}");
                }
            }
        }

        private async Task ProcessLogEntry(LogEntry logEntry)
        {
            // Add to context
            if (!_logContexts.ContainsKey(logEntry.Context))
            {
                _logContexts[logEntry.Context] = new LogContext { Name = logEntry.Context, Logs = new List<LogEntry>() };
            }
            _logContexts[logEntry.Context].Logs.Add(logEntry);

            // Write to file if enabled
            if (_enableFileOutput)
            {
                await WriteToFile(logEntry);
            }

            // Notify subscribers
            LogReceived?.Invoke(this, new LogEventArgs { LogEntry = logEntry });

            // Trigger AI analysis for critical errors
            if (logEntry.Level == LogLevel.Error && _enableAIAnalysis)
            {
                _ = Task.Run(async () =>
                {
                    var analysis = await AnalyzeLogsWithAI("1h", logEntry.Category);
                    if (analysis.Success)
                    {
                        WriteToTerminal($"[AI-ANALYSIS] {logEntry.Category} Error Analysis: {analysis.Insights}", ConsoleColor.DarkYellow);
                    }
                });
            }
        }

        private void EnqueueLog(LogEntry logEntry)
        {
            _logQueue.Enqueue(logEntry);
        }

        private void WriteToTerminal(string message, ConsoleColor color)
        {
            var originalColor = Console.ForegroundColor;
            Console.ForegroundColor = color;
            Console.WriteLine($"{DateTime.Now:HH:mm:ss.fff} {message}");
            Console.ForegroundColor = originalColor;

            TerminalOutputReceived?.Invoke(this, new TerminalOutputEventArgs
            {
                Message = message,
                Color = color,
                Timestamp = DateTime.UtcNow
            });
        }

        private async Task WriteToFile(LogEntry logEntry)
        {
            var logFile = Path.Combine(_logDirectory, $"{logEntry.Category.ToLower()}_{DateTime.UtcNow:yyyyMMdd}.log");
            var logLine = $"{logEntry.Timestamp:yyyy-MM-dd HH:mm:ss.fff} [{logEntry.Level}] [{logEntry.Category}] {logEntry.Message}";

            if (logEntry.Data != null && logEntry.Data.Count > 0)
            {
                logLine += $" | Data: {JsonSerializer.Serialize(logEntry.Data)}";
            }

            await File.AppendAllTextAsync(logFile, logLine + Environment.NewLine);
        }

        private void EnsureLogDirectoryExists()
        {
            if (!Directory.Exists(_logDirectory))
            {
                Directory.CreateDirectory(_logDirectory);
            }
        }

        private TimeSpan ParseTimespan(string timespan)
        {
            var unit = timespan.Last();
            var value = int.Parse(timespan.Substring(0, timespan.Length - 1));

            return unit switch
            {
                's' => TimeSpan.FromSeconds(value),
                'm' => TimeSpan.FromMinutes(value),
                'h' => TimeSpan.FromHours(value),
                'd' => TimeSpan.FromDays(value),
                _ => TimeSpan.FromHours(1)
            };
        }

        public void Dispose()
        {
            _cancellationTokenSource?.Cancel();
            _logProcessingTask?.Wait(TimeSpan.FromSeconds(5));
            _cancellationTokenSource?.Dispose();
        }
    }
}
