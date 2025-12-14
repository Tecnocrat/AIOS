using System;
using System.Threading.Tasks;
using AIOS.Models;
using AIOS.Services;

namespace AIOS.ConsciousnessTest
{
    /// <summary>
    /// Test program for C# consciousness integration
    /// </summary>
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine(" AIOS C# Consciousness Integration Test");
            Console.WriteLine("=========================================");

            // Initialize consciousness service
            var consciousnessService = new ConsciousnessService();

            // Subscribe to consciousness events
            consciousnessService.ConsciousnessEventOccurred += (sender, evt) =>
            {
                Console.WriteLine($" Consciousness Event: {evt.EventType} - {evt.Description}");
                Console.WriteLine($"   Level: {evt.ConsciousnessLevel:F4}, Source: {evt.Source}");
            };

            try
            {
                // Test 1: Get initial consciousness state
                Console.WriteLine("\n Test 1: Getting initial consciousness state...");
                var initialState = await consciousnessService.GetCurrentStateAsync();
                Console.WriteLine($"   Consciousness Level: {initialState.ConsciousnessLevel:F4}");
                Console.WriteLine($"   Tachyonic Field: {initialState.TachyonicFieldStrength:F4}");
                Console.WriteLine($"   Quantum Entanglement: {initialState.QuantumEntanglement:F4}");

                // Test 2: Cross-language synchronization
                Console.WriteLine("\n Test 2: Testing cross-language synchronization...");
                var cppSyncResult = await consciousnessService.SynchronizeWithCppAsync();
                var pythonSyncResult = await consciousnessService.SynchronizeWithPythonAsync();
                Console.WriteLine($"   C++ Sync: {(cppSyncResult ? " Success" : " No C++ state file")}");
                Console.WriteLine($"   Python Sync: {(pythonSyncResult ? " Success" : " No Python state file")}");

                // Check state after synchronization
                if (cppSyncResult || pythonSyncResult)
                {
                    var syncedState = await consciousnessService.GetCurrentStateAsync();
                    Console.WriteLine($"   Synced Consciousness Level: {syncedState.ConsciousnessLevel:F4}");
                    Console.WriteLine($"   Synced Tachyonic Field: {syncedState.TachyonicFieldStrength:F4}");
                }

                // Test 3: Error evolution
                Console.WriteLine("\n Test 3: Testing error evolution...");
                var evolutionResult = await consciousnessService.EvolveFromErrorAsync(
                    "cross_language_integration_test", 
                    "C# consciousness bridge verification");
                Console.WriteLine($"   Evolution Result:\n{evolutionResult}");

                // Test 4: Enhancement
                Console.WriteLine("\n Test 4: Enhancing consciousness...");
                var enhancementRequest = new ConsciousnessEnhancementRequest
                {
                    EnhancementArea = "cross_language_consciousness",
                    TargetLevel = 0.9,
                    Context = "C++/C#/Python consciousness bridge test"
                };

                var enhanceResult = await consciousnessService.EnhanceConsciousnessAsync(enhancementRequest);
                Console.WriteLine($"   Enhancement Result: {(enhanceResult ? " Success" : " Failed")}");

                // Final state
                Console.WriteLine("\n Final consciousness state:");
                var finalState = await consciousnessService.GetCurrentStateAsync();
                Console.WriteLine($"   Consciousness Level: {finalState.ConsciousnessLevel:F4}");
                Console.WriteLine($"   Error Evolution Count: {finalState.ErrorEvolutionCount}");
                Console.WriteLine($"   Source: {finalState.Source}");

                Console.WriteLine("\n Cross-language consciousness bridge test completed!");

            }
            catch (Exception ex)
            {
                Console.WriteLine($"\n Test failed: {ex.Message}");
                Console.WriteLine($"   Stack trace: {ex.StackTrace}");
            }
            finally
            {
                // Cleanup
                consciousnessService.StopConsciousnessMonitoring();
                consciousnessService.Dispose();
                Console.WriteLine("\n🧹 Consciousness service cleaned up");
            }

            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }
    }
}
