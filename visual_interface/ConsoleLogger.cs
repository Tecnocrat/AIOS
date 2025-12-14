using System;
using Microsoft.Extensions.Logging;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Simple console logger for AIOS visual interface
    /// </summary>
    public class ConsoleLogger : ILogger
    {
        private readonly string _categoryName;
        
        public ConsoleLogger(string categoryName = "AIOS.Visual")
        {
            _categoryName = categoryName;
        }
        
        public IDisposable BeginScope<TState>(TState state)
        {
            return null;
        }
        
        public bool IsEnabled(LogLevel logLevel)
        {
            return logLevel >= LogLevel.Information;
        }
        
        public void Log<TState>(LogLevel logLevel, EventId eventId, TState state, Exception exception, Func<TState, Exception, string> formatter)
        {
            if (!IsEnabled(logLevel))
                return;
                
            var message = formatter(state, exception);
            var timestamp = DateTime.Now.ToString("HH:mm:ss.fff");
            
            Console.WriteLine($"[{timestamp}] [{logLevel}] [{_categoryName}] {message}");
            
            if (exception != null)
            {
                Console.WriteLine($"Exception: {exception}");
            }
        }
    }
}
