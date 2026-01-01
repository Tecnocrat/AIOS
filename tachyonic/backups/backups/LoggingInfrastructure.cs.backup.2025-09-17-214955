using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging.Console;
using Microsoft.Extensions.Configuration;
using System.Text.Json;
using System.Runtime.CompilerServices;
using System.Diagnostics;

namespace AIOS.Models
{
    /// <summary>
    /// Structured logging infrastructure for AIOS
    /// Provides comprehensive logging capabilities across all components
    /// </summary>
    public static class AIOSLogger
    {
        private static ILoggerFactory? _loggerFactory;
        private static readonly object _lock = new object();
        private static readonly List<ILogSink> _sinks = new List<ILogSink>();
        private static bool _isInitialized = false;

        /// <summary>
        /// Initialize the AIOS logging system
        /// </summary>
        public static void Initialize(AIOSLoggingConfiguration config)
        {
            lock (_lock)
            {
                if (_isInitialized)
                    return;

                var services = new ServiceCollection();

                // Configure logging
                services.AddLogging(builder =>
                {
                    builder.SetMinimumLevel(config.MinimumLevel);

                    if (config.EnableConsole)
                    {
                        builder.AddConsole(options =>
                        {
                            options.IncludeScopes = config.IncludeScopes;
                            options.TimestampFormat = "yyyy-MM-dd HH:mm:ss.fff ";
                        });
                    }

                    if (config.EnableFile)
                    {
                        builder.AddProvider(new FileLoggerProvider(config.LogFilePath));
                    }

                    if (config.EnableStructuredJson)
                    {
                        builder.AddProvider(new JsonLoggerProvider(config.JsonLogPath));
                    }
                });

                var serviceProvider = services.BuildServiceProvider();
                _loggerFactory = serviceProvider.GetService<ILoggerFactory>();

                // Initialize sinks
                if (config.EnableDatabase)
                {
                    _sinks.Add(new DatabaseLogSink(config.DatabaseConnectionString));
                }

                if (config.EnableWebHook)
                {
                    _sinks.Add(new WebHookLogSink(config.WebHookUrl));
                }

                _isInitialized = true;
            }
        }

        /// <summary>
        /// Get a logger for a specific type
        /// </summary>
        public static ILogger<T> GetLogger<T>()
        {
            EnsureInitialized();
            return _loggerFactory!.CreateLogger<T>();
        }

        /// <summary>
        /// Get a logger for a specific category
        /// </summary>
        public static ILogger GetLogger(string categoryName)
        {
            EnsureInitialized();
            return _loggerFactory!.CreateLogger(categoryName);
        }

        /// <summary>
        /// Log structured data with context
        /// </summary>
        public static void LogStructured<T>(
            LogLevel level,
            string categoryName,
            string message,
            T data,
            Exception? exception = null,
            [CallerMemberName] string memberName = "",
            [CallerFilePath] string filePath = "",
            [CallerLineNumber] int lineNumber = 0)
        {
            var logger = GetLogger(categoryName);

            using var scope = logger.BeginScope(new Dictionary<string, object>
            {
                ["MemberName"] = memberName,
                ["FilePath"] = Path.GetFileName(filePath),
                ["LineNumber"] = lineNumber,
                ["Data"] = data,
                ["Timestamp"] = DateTime.UtcNow,
                ["ThreadId"] = Thread.CurrentThread.ManagedThreadId
            });

            if (exception != null)
            {
                logger.Log(level, exception, message);
            }
            else
            {
                logger.Log(level, message);
            }

            // Send to additional sinks
            foreach (var sink in _sinks)
            {
                Task.Run(() => sink.WriteAsync(new StructuredLogEntry
                {
                    Level = level,
                    Category = categoryName,
                    Message = message,
                    Data = JsonSerializer.Serialize(data),
                    Exception = exception?.ToString(),
                    MemberName = memberName,
                    FilePath = filePath,
                    LineNumber = lineNumber,
                    Timestamp = DateTime.UtcNow,
                    ThreadId = Thread.CurrentThread.ManagedThreadId
                }));
            }
        }

        /// <summary>
        /// Log performance metrics
        /// </summary>
        public static void LogPerformance(
            string operation,
            TimeSpan duration,
            Dictionary<string, object>? additionalData = null)
        {
            var performanceData = new PerformanceLogEntry
            {
                Operation = operation,
                Duration = duration,
                AdditionalData = additionalData ?? new Dictionary<string, object>()
            };

            LogStructured(LogLevel.Information, "Performance",
                $"Operation '{operation}' completed in {duration.TotalMilliseconds}ms",
                performanceData);
        }

        /// <summary>
        /// Log AI operations
        /// </summary>
        public static void LogAIOperation(
            string operation,
            string input,
            string output,
            TimeSpan processingTime,
            Dictionary<string, object>? metadata = null)
        {
            var aiData = new AILogEntry
            {
                Operation = operation,
                Input = input,
                Output = output,
                ProcessingTime = processingTime,
                Metadata = metadata ?? new Dictionary<string, object>()
            };

            LogStructured(LogLevel.Information, "AI",
                $"AI operation '{operation}' processed in {processingTime.TotalMilliseconds}ms",
                aiData);
        }

        /// <summary>
        /// Log system health events
        /// </summary>
        public static void LogHealthEvent(
            string component,
            HealthStatus status,
            Dictionary<string, object>? healthData = null)
        {
            var healthEvent = new HealthLogEntry
            {
                Component = component,
                Status = status,
                HealthData = healthData ?? new Dictionary<string, object>(),
                Timestamp = DateTime.UtcNow
            };

            var level = status == HealthStatus.Healthy ? LogLevel.Information : LogLevel.Warning;
            LogStructured(level, "Health",
                $"Component '{component}' health status: {status}",
                healthEvent);
        }

        /// <summary>
        /// Create a performance measurement scope
        /// </summary>
        public static IDisposable BeginPerformanceScope(string operation)
        {
            return new PerformanceScope(operation);
        }

        private static void EnsureInitialized()
        {
            if (!_isInitialized)
            {
                Initialize(AIOSLoggingConfiguration.Default);
            }
        }
    }

    /// <summary>
    /// Configuration for AIOS logging system
    /// </summary>
    public class AIOSLoggingConfiguration
    {
        public LogLevel MinimumLevel { get; set; } = LogLevel.Information;
        public bool EnableConsole { get; set; } = true;
        public bool EnableFile { get; set; } = true;
        public bool EnableStructuredJson { get; set; } = true;
        public bool EnableDatabase { get; set; } = false;
        public bool EnableWebHook { get; set; } = false;
        public bool IncludeScopes { get; set; } = true;
        public string LogFilePath { get; set; } = "logs/aios.log";
        public string JsonLogPath { get; set; } = "logs/aios.json";
        public string DatabaseConnectionString { get; set; } = "";
        public string WebHookUrl { get; set; } = "";

        public static AIOSLoggingConfiguration Default => new AIOSLoggingConfiguration();

        public static AIOSLoggingConfiguration Development => new AIOSLoggingConfiguration
        {
            MinimumLevel = LogLevel.Debug,
            EnableConsole = true,
            EnableFile = true,
            EnableStructuredJson = true,
            IncludeScopes = true
        };

        public static AIOSLoggingConfiguration Production => new AIOSLoggingConfiguration
        {
            MinimumLevel = LogLevel.Information,
            EnableConsole = false,
            EnableFile = true,
            EnableStructuredJson = true,
            EnableDatabase = true,
            IncludeScopes = false
        };
    }

    /// <summary>
    /// Structured log entry for advanced logging
    /// </summary>
    public class StructuredLogEntry
    {
        public LogLevel Level { get; set; }
        public string Category { get; set; } = "";
        public string Message { get; set; } = "";
        public string Data { get; set; } = "";
        public string? Exception { get; set; }
        public string MemberName { get; set; } = "";
        public string FilePath { get; set; } = "";
        public int LineNumber { get; set; }
        public DateTime Timestamp { get; set; }
        public int ThreadId { get; set; }
    }

    /// <summary>
    /// Performance log entry
    /// </summary>
    public class PerformanceLogEntry
    {
        public string Operation { get; set; } = "";
        public TimeSpan Duration { get; set; }
        public Dictionary<string, object> AdditionalData { get; set; } = new();
    }

    /// <summary>
    /// AI operation log entry
    /// </summary>
    public class AILogEntry
    {
        public string Operation { get; set; } = "";
        public string Input { get; set; } = "";
        public string Output { get; set; } = "";
        public TimeSpan ProcessingTime { get; set; }
        public Dictionary<string, object> Metadata { get; set; } = new();
    }

    /// <summary>
    /// Health log entry
    /// </summary>
    public class HealthLogEntry
    {
        public string Component { get; set; } = "";
        public HealthStatus Status { get; set; }
        public Dictionary<string, object> HealthData { get; set; } = new();
        public DateTime Timestamp { get; set; }
    }

    /// <summary>
    /// Health status enumeration
    /// </summary>
    public enum HealthStatus
    {
        Healthy,
        Degraded,
        Unhealthy,
        Unknown
    }

    /// <summary>
    /// Interface for log sinks
    /// </summary>
    public interface ILogSink
    {
        Task WriteAsync(StructuredLogEntry entry);
    }

    /// <summary>
    /// File logger provider
    /// </summary>
    public class FileLoggerProvider : ILoggerProvider
    {
        private readonly string _filePath;

        public FileLoggerProvider(string filePath)
        {
            _filePath = filePath;
            Directory.CreateDirectory(Path.GetDirectoryName(_filePath)!);
        }

        public ILogger CreateLogger(string categoryName)
        {
            return new FileLogger(categoryName, _filePath);
        }

        public void Dispose() { }
    }

    /// <summary>
    /// JSON logger provider
    /// </summary>
    public class JsonLoggerProvider : ILoggerProvider
    {
        private readonly string _filePath;

        public JsonLoggerProvider(string filePath)
        {
            _filePath = filePath;
            Directory.CreateDirectory(Path.GetDirectoryName(_filePath)!);
        }

        public ILogger CreateLogger(string categoryName)
        {
            return new JsonLogger(categoryName, _filePath);
        }

        public void Dispose() { }
    }

    /// <summary>
    /// File logger implementation
    /// </summary>
    public class FileLogger : ILogger
    {
        private readonly string _categoryName;
        private readonly string _filePath;
        private readonly object _lock = new object();

        public FileLogger(string categoryName, string filePath)
        {
            _categoryName = categoryName;
            _filePath = filePath;
        }

        public IDisposable BeginScope<TState>(TState state)
        {
            return new NoOpDisposable();
        }

        public bool IsEnabled(LogLevel logLevel)
        {
            return true;
        }

        public void Log<TState>(LogLevel logLevel, EventId eventId, TState state, Exception? exception, Func<TState, Exception?, string> formatter)
        {
            var message = formatter(state, exception);
            var logEntry = $"{DateTime.UtcNow:yyyy-MM-dd HH:mm:ss.fff} [{logLevel}] {_categoryName}: {message}";

            if (exception != null)
            {
                logEntry += $"\nException: {exception}";
            }

            lock (_lock)
            {
                File.AppendAllText(_filePath, logEntry + Environment.NewLine);
            }
        }
    }

    /// <summary>
    /// JSON logger implementation
    /// </summary>
    public class JsonLogger : ILogger
    {
        private readonly string _categoryName;
        private readonly string _filePath;
        private readonly object _lock = new object();

        public JsonLogger(string categoryName, string filePath)
        {
            _categoryName = categoryName;
            _filePath = filePath;
        }

        public IDisposable BeginScope<TState>(TState state)
        {
            return new NoOpDisposable();
        }

        public bool IsEnabled(LogLevel logLevel)
        {
            return true;
        }

        public void Log<TState>(LogLevel logLevel, EventId eventId, TState state, Exception? exception, Func<TState, Exception?, string> formatter)
        {
            var message = formatter(state, exception);
            var logObject = new
            {
                Timestamp = DateTime.UtcNow,
                Level = logLevel.ToString(),
                Category = _categoryName,
                Message = message,
                Exception = exception?.ToString(),
                EventId = eventId.Id,
                EventName = eventId.Name
            };

            var json = JsonSerializer.Serialize(logObject, new JsonSerializerOptions
            {
                WriteIndented = false
            });

            lock (_lock)
            {
                File.AppendAllText(_filePath, json + Environment.NewLine);
            }
        }
    }    /// <summary>
         /// Database log sink
         /// </summary>
    public class DatabaseLogSink : ILogSink
    {
        private readonly string _connectionString;

        public DatabaseLogSink(string connectionString)
        {
            _connectionString = connectionString;
        }

        public async Task WriteAsync(StructuredLogEntry entry)
        {
            // Implementation would depend on the database provider
            // This is a placeholder for database logging
            await Task.CompletedTask;
        }
    }    /// <summary>
         /// WebHook log sink
         /// </summary>
    public class WebHookLogSink : ILogSink
    {
        private readonly string _webHookUrl;
        private readonly HttpClient _httpClient;

        public WebHookLogSink(string webHookUrl)
        {
            _webHookUrl = webHookUrl;
            _httpClient = new HttpClient();
        }

        public async Task WriteAsync(StructuredLogEntry entry)
        {
            try
            {
                var json = JsonSerializer.Serialize(entry);
                var content = new StringContent(json, System.Text.Encoding.UTF8, "application/json");
                await _httpClient.PostAsync(_webHookUrl, content);
            }
            catch (Exception ex)
            {
                // Log the error to console as fallback
                Console.WriteLine($"Failed to send log to webhook: {ex.Message}");
            }
        }
    }

    /// <summary>
    /// Performance measurement scope
    /// </summary>
    public class PerformanceScope : IDisposable
    {
        private readonly string _operation;
        private readonly Stopwatch _stopwatch;

        public PerformanceScope(string operation)
        {
            _operation = operation;
            _stopwatch = Stopwatch.StartNew();
        }

        public void Dispose()
        {
            _stopwatch.Stop();
            AIOSLogger.LogPerformance(_operation, _stopwatch.Elapsed);
        }
    }

    /// <summary>
    /// No-op disposable
    /// </summary>
    public class NoOpDisposable : IDisposable
    {
        public void Dispose() { }
    }
}
