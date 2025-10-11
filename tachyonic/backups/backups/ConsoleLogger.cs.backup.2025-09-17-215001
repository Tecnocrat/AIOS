using System;
using System.Diagnostics;
using Microsoft.Extensions.Logging;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Enhanced console logger for AIOS visual interface with nullability compliance and performance optimizations
    /// </summary>
    public class ConsoleLogger : ILogger
    {
        private readonly string _categoryName;
        private readonly LogLevel _minLogLevel;
        private readonly bool _includeTimestamp;
        private readonly bool _includeCategory;
        private readonly bool _useColors;

        /// <summary>
        /// Creates a new ConsoleLogger with enhanced configuration options
        /// </summary>
        public ConsoleLogger(string categoryName = "AIOS.Visual",
                           LogLevel minLogLevel = LogLevel.Information,
                           bool includeTimestamp = true,
                           bool includeCategory = true,
                           bool useColors = true)
        {
            _categoryName = categoryName ?? throw new ArgumentNullException(nameof(categoryName));
            _minLogLevel = minLogLevel;
            _includeTimestamp = includeTimestamp;
            _includeCategory = includeCategory;
            _useColors = useColors;
        }

        /// <summary>
        /// Begins a logical operation scope with enhanced nullability compliance
        /// </summary>
        public IDisposable? BeginScope<TState>(TState state) where TState : notnull
        {
            // Return null for console logger - no scope management needed
            // This is compliant with ILogger interface expectations
            return null;
        }

        /// <summary>
        /// Determines if the given log level is enabled with performance optimization
        /// </summary>
        public bool IsEnabled(LogLevel logLevel)
        {
            return logLevel >= _minLogLevel;
        }

        /// <summary>
        /// Logs a message with enhanced formatting and nullability compliance
        /// </summary>
        public void Log<TState>(LogLevel logLevel, EventId eventId, TState state, Exception? exception, Func<TState, Exception?, string> formatter)
        {
            if (!IsEnabled(logLevel))
                return;

            if (formatter == null)
                throw new ArgumentNullException(nameof(formatter));

            try
            {
                var message = formatter(state, exception);
                if (string.IsNullOrEmpty(message))
                    return;

                var formattedMessage = FormatLogMessage(logLevel, eventId, message, exception);
                WriteToConsole(logLevel, formattedMessage);
            }
            catch (Exception ex)
            {
                // Fallback logging in case of formatting errors
                WriteToConsole(LogLevel.Error, $"Logger error: {ex.Message}");
            }
        }

        /// <summary>
        /// Formats the log message with enhanced visual elements
        /// </summary>
        private string FormatLogMessage(LogLevel logLevel, EventId eventId, string message, Exception? exception)
        {
            var parts = new System.Collections.Generic.List<string>();

            if (_includeTimestamp)
            {
                parts.Add($"[{DateTime.Now:HH:mm:ss.fff}]");
            }

            parts.Add($"[{GetLogLevelString(logLevel)}]");

            if (_includeCategory)
            {
                parts.Add($"[{_categoryName}]");
            }

            if (eventId.Id != 0)
            {
                parts.Add($"[EventId:{eventId.Id}]");
            }

            parts.Add(message);

            var formattedMessage = string.Join(" ", parts);

            if (exception != null)
            {
                formattedMessage += $"{Environment.NewLine}Exception: {exception.GetType().Name}: {exception.Message}";
                if (!string.IsNullOrEmpty(exception.StackTrace))
                {
                    formattedMessage += $"{Environment.NewLine}StackTrace: {exception.StackTrace}";
                }
            }

            return formattedMessage;
        }

        /// <summary>
        /// Gets the string representation of the log level with optional color coding
        /// </summary>
        private string GetLogLevelString(LogLevel logLevel)
        {
            if (!_useColors)
            {
                return logLevel.ToString().ToUpper();
            }

            return logLevel switch
            {
                LogLevel.Trace => "TRACE",
                LogLevel.Debug => "DEBUG",
                LogLevel.Information => "INFO",
                LogLevel.Warning => "WARN",
                LogLevel.Error => "ERROR",
                LogLevel.Critical => "CRIT",
                LogLevel.None => "NONE",
                _ => logLevel.ToString().ToUpper()
            };
        }

        /// <summary>
        /// Writes the formatted message to console with performance optimization
        /// </summary>
        private void WriteToConsole(LogLevel logLevel, string message)
        {
            // Use Console.WriteLine for thread safety and performance
            // In high-performance scenarios, consider using a background writer
            Console.WriteLine(message);
        }

        /// <summary>
        /// Creates a logger factory for AIOS visual interface components
        /// </summary>
        public static ILoggerFactory CreateLoggerFactory(LogLevel minLogLevel = LogLevel.Information)
        {
            return LoggerFactory.Create(builder =>
            {
                builder.SetMinimumLevel(minLogLevel);
                builder.AddProvider(new ConsoleLoggerProvider());
            });
        }

        /// <summary>
        /// Creates a logger instance for a specific category
        /// </summary>
        public static ILogger CreateLogger(string categoryName, LogLevel minLogLevel = LogLevel.Information)
        {
            return new ConsoleLogger(categoryName, minLogLevel);
        }
    }

    /// <summary>
    /// Logger provider for creating ConsoleLogger instances
    /// </summary>
    public class ConsoleLoggerProvider : ILoggerProvider
    {
        private readonly LogLevel _minLogLevel;
        private readonly bool _includeTimestamp;
        private readonly bool _includeCategory;
        private readonly bool _useColors;

        public ConsoleLoggerProvider(LogLevel minLogLevel = LogLevel.Information,
                                   bool includeTimestamp = true,
                                   bool includeCategory = true,
                                   bool useColors = true)
        {
            _minLogLevel = minLogLevel;
            _includeTimestamp = includeTimestamp;
            _includeCategory = includeCategory;
            _useColors = useColors;
        }

        public ILogger CreateLogger(string categoryName)
        {
            return new ConsoleLogger(categoryName, _minLogLevel, _includeTimestamp, _includeCategory, _useColors);
        }

        public void Dispose()
        {
            // No resources to dispose
        }
    }
}
