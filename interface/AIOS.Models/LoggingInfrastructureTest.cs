using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using AIOS.Models;

namespace AIOS.Models.Tests
{
    /// <summary>
    /// Test program to validate AIOS logging infrastructure
    /// Demonstrates various logging capabilities and patterns
    /// </summary>
    public class LoggingInfrastructureTest
    {
        public static async Task Main(string[] args)
        {
            Console.WriteLine("=== AIOS Logging Infrastructure Test ===\n");

            // Initialize logging with development configuration
            var config = AIOSLoggingConfiguration.Development;
            config.LogFilePath = "logs/test-aios.log";
            config.JsonLogPath = "logs/test-aios.json";

            AIOSLogger.Initialize(config);

            // Test basic logging
            TestBasicLogging();

            // Test structured logging
            TestStructuredLogging();

            // Test performance logging
            await TestPerformanceLogging();

            // Test AI operation logging
            TestAIOperationLogging();

            // Test health monitoring
            TestHealthMonitoring();

            // Test error scenarios
            TestErrorScenarios();

            Console.WriteLine("\n=== All logging tests completed ===");
            Console.WriteLine("Check the following files for output:");
            Console.WriteLine($"- {config.LogFilePath}");
            Console.WriteLine($"- {config.JsonLogPath}");
            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }

        private static void TestBasicLogging()
        {
            Console.WriteLine("1. Testing basic logging...");

            var logger = AIOSLogger.GetLogger<LoggingInfrastructureTest>();

            logger.LogTrace("This is a trace message");
            logger.LogDebug("This is a debug message");
            logger.LogInformation("This is an info message");
            logger.LogWarning("This is a warning message");
            logger.LogError("This is an error message");
            logger.LogCritical("This is a critical message");

            Console.WriteLine(" Basic logging test completed\n");
        }

        private static void TestStructuredLogging()
        {
            Console.WriteLine("2. Testing structured logging...");

            var userData = new
            {
                UserId = 12345,
                UserName = "TestUser",
                Action = "Login",
                Timestamp = DateTime.UtcNow,
                IPAddress = "192.168.1.1",
                UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            };

            AIOSLogger.LogStructured(
                LogLevel.Information,
                "UserActivity",
                "User performed login action",
                userData);

            var systemData = new
            {
                ComponentName = "DatabaseService",
                ConnectionString = "Server=localhost;Database=AIOS;",
                PoolSize = 25,
                ActiveConnections = 12,
                MaxConnections = 100
            };

            AIOSLogger.LogStructured(
                LogLevel.Information,
                "SystemState",
                "Database connection pool status",
                systemData);

            Console.WriteLine(" Structured logging test completed\n");
        }

        private static async Task TestPerformanceLogging()
        {
            Console.WriteLine("3. Testing performance logging...");

            // Test performance scope
            using (AIOSLogger.BeginPerformanceScope("DatabaseQuery"))
            {
                // Simulate database operation
                await Task.Delay(100);
            }

            // Test manual performance logging
            var stopwatch = System.Diagnostics.Stopwatch.StartNew();
            await Task.Delay(50);
            stopwatch.Stop();

            AIOSLogger.LogPerformance(
                "DataProcessing",
                stopwatch.Elapsed,
                new Dictionary<string, object>
                {
                    ["RecordsProcessed"] = 1000,
                    ["MemoryUsed"] = "25MB",
                    ["CacheHitRate"] = 0.85
                });

            Console.WriteLine(" Performance logging test completed\n");
        }

        private static void TestAIOperationLogging()
        {
            Console.WriteLine("4. Testing AI operation logging...");

            var input = "What is the weather like today?";
            var output = "I don't have access to real-time weather data, but I can help you find weather information.";
            var processingTime = TimeSpan.FromMilliseconds(150);

            AIOSLogger.LogAIOperation(
                "NLP-Query",
                input,
                output,
                processingTime,
                new Dictionary<string, object>
                {
                    ["Model"] = "GPT-4",
                    ["TokensUsed"] = 45,
                    ["Confidence"] = 0.92,
                    ["Language"] = "English"
                });

            // Test prediction logging
            AIOSLogger.LogAIOperation(
                "Prediction",
                "Historical sales data for Q4",
                "Predicted 15% increase in sales",
                TimeSpan.FromMilliseconds(300),
                new Dictionary<string, object>
                {
                    ["Algorithm"] = "LinearRegression",
                    ["AccuracyScore"] = 0.87,
                    ["DataPoints"] = 1000,
                    ["Features"] = new[] { "Season", "Marketing", "Economy" }
                });

            Console.WriteLine(" AI operation logging test completed\n");
        }

        private static void TestHealthMonitoring()
        {
            Console.WriteLine("5. Testing health monitoring...");

            // Test healthy component
            AIOSLogger.LogHealthEvent(
                "DatabaseService",
                HealthStatus.Healthy,
                new Dictionary<string, object>
                {
                    ["ResponseTime"] = "15ms",
                    ["ConnectionCount"] = 12,
                    ["MemoryUsage"] = "45MB",
                    ["LastHealthCheck"] = DateTime.UtcNow
                });

            // Test degraded component
            AIOSLogger.LogHealthEvent(
                "AIService",
                HealthStatus.Degraded,
                new Dictionary<string, object>
                {
                    ["ResponseTime"] = "500ms",
                    ["QueueLength"] = 25,
                    ["ErrorRate"] = 0.05,
                    ["LastError"] = "Timeout connecting to ML model"
                });

            // Test unhealthy component
            AIOSLogger.LogHealthEvent(
                "ExternalAPI",
                HealthStatus.Unhealthy,
                new Dictionary<string, object>
                {
                    ["Status"] = "Connection Failed",
                    ["LastSuccessful"] = DateTime.UtcNow.AddMinutes(-10),
                    ["RetryCount"] = 3,
                    ["ErrorMessage"] = "Service unavailable"
                });

            Console.WriteLine(" Health monitoring test completed\n");
        }

        private static void TestErrorScenarios()
        {
            Console.WriteLine("6. Testing error scenarios...");

            try
            {
                // Simulate an error
                throw new InvalidOperationException("This is a test exception");
            }
            catch (Exception ex)
            {
                AIOSLogger.LogStructured(
                    LogLevel.Error,
                    "ErrorHandling",
                    "Test exception occurred",
                    new
                    {
                        Operation = "TestErrorScenarios",
                        Context = "Infrastructure validation",
                        ErrorType = ex.GetType().Name,
                        HelpLink = ex.HelpLink
                    },
                    ex);
            }

            // Test warning scenario
            AIOSLogger.LogStructured(
                LogLevel.Warning,
                "ResourceMonitoring",
                "High memory usage detected",
                new
                {
                    MemoryUsage = "85%",
                    Threshold = "80%",
                    RecommendedAction = "Consider scaling up resources",
                    AffectedServices = new[] { "AIService", "DatabaseService" }
                });

            Console.WriteLine(" Error scenario testing completed\n");
        }
    }
}
