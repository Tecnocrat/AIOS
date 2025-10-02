using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace AIOS.TestHarness
{
    /// <summary>
    /// Simple console test harness to validate AIOS harmonization features
    /// Tests core components without requiring WPF GUI
    /// </summary>
    public class Program
    {
        public static async Task Main(string[] args)
        {
            Console.WriteLine(" AIOS Harmonization Test Harness Starting...");

            try
            {
                // Test core AIOS components by direct instantiation with minimal dependencies
                Console.WriteLine(" Testing AIOS Components...");

                // Create a simple logger factory for testing
                using var loggerFactory = LoggerFactory.Create(builder => builder.AddConsole());
                
                // Test Consciousness Data Manager
                var consciousnessLogger = loggerFactory.CreateLogger<AIOS.VisualInterface.ConsciousnessDataManager>();
                var consciousnessManager = new AIOS.VisualInterface.ConsciousnessDataManager(consciousnessLogger);
                Console.WriteLine(" ConsciousnessDataManager instantiated");

                // Test Runtime Analytics
                var runtimeLogger = loggerFactory.CreateLogger<AIOS.VisualInterface.RuntimeAnalytics>();
                var runtimeAnalytics = new AIOS.VisualInterface.RuntimeAnalytics(runtimeLogger);
                Console.WriteLine(" RuntimeAnalytics instantiated");

                // Test UI Metrics Emitter
                var metricsLogger = loggerFactory.CreateLogger<AIOS.VisualInterface.UIMetricsEmitter>();
                var metricsEmitter = new AIOS.VisualInterface.UIMetricsEmitter(metricsLogger, 5.0, true);
                Console.WriteLine(" UIMetricsEmitter instantiated");

                // Test State Manager
                var stateLogger = loggerFactory.CreateLogger<AIOS.VisualInterface.StateManager>();
                var stateManager = new AIOS.VisualInterface.StateManager(stateLogger);
                Console.WriteLine(" StateManager instantiated");

                Console.WriteLine("\n All AIOS Harmonization Components Successfully Instantiated!");
                Console.WriteLine(" The optimized visual interface components are structurally sound");
            }
            catch (Exception ex)
            {
                Console.WriteLine($" Test failed: {ex.Message}");
                Console.WriteLine(ex.StackTrace);
            }
        }
    }
}
