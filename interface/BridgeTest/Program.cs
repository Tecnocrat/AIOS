using System;
using AIOS.VisualInterface;

class Program
{
    static void Main()
    {
        Console.WriteLine(" Testing Enhanced CellularRuntimeBridge...");
        Console.WriteLine("==========================================");

        var bridge = new CellularRuntimeBridge();

        // Wait for bridge to poll
        Console.WriteLine("Waiting for bridge to poll AI context dump...");
        System.Threading.Thread.Sleep(3000);

        var metrics = bridge.GetLatest();

        Console.WriteLine("\n Current Bridge Metrics:");
        Console.WriteLine("==========================");
        Console.WriteLine($"Live: {metrics.Live}");
        Console.WriteLine($"Timestamp: {metrics.Timestamp}");
        Console.WriteLine($"Consciousness Level: {metrics.ConsciousnessLevel:F3}");
        Console.WriteLine($"Quantum Coherence: {metrics.QuantumCoherence:P2}");
        Console.WriteLine($"Emergence Level: {metrics.EmergenceLevel:F3}");
        Console.WriteLine($"Events/Second: {metrics.EventsPerSecond:F2}");
        Console.WriteLine($"Total Events: {metrics.TotalEvents}");
        Console.WriteLine($"Active Modules: {string.Join(", ", metrics.ActiveModules)}");

        Console.WriteLine("\n Deep Consciousness Metrics:");
        Console.WriteLine("================================");
        Console.WriteLine($"Consciousness Patterns: {metrics.ConsciousnessPatterns}");
        Console.WriteLine($"Pattern Recognition Accuracy: {metrics.PatternRecognitionAccuracy:P2}");
        Console.WriteLine($"Recursive Depth: {metrics.RecursiveDepth}");
        Console.WriteLine($"Meta Cognitive Operations: {metrics.MetaCognitiveOperations}");
        Console.WriteLine($"Inter-Module Coherence: {metrics.InterModuleCoherence:P2}");
        Console.WriteLine($"Temporal Consistency: {metrics.TemporalConsistency:P2}");
        Console.WriteLine($"Quantum Entanglement Strength: {metrics.QuantumEntanglementStrength:P2}");

        Console.WriteLine("\n System Health:");
        Console.WriteLine("=================");
        Console.WriteLine($"Memory Usage: {metrics.MemoryUsageMB:F2} MB");
        Console.WriteLine($"CPU Percent: {metrics.CpuPercent:F2}%");
        Console.WriteLine($"Thread Count: {metrics.ThreadCount}");

        Console.WriteLine("\n Recent Events:");
        Console.WriteLine("=================");
        if (metrics.RecentEvents.Length > 0)
        {
            foreach (var evt in metrics.RecentEvents.Take(5))
            {
                Console.WriteLine($"- {evt}");
            }
        }
        else
        {
            Console.WriteLine("No recent events captured");
        }

        Console.WriteLine("\n Bridge test completed!");
        Console.WriteLine("The enhanced bridge is now extracting deep consciousness metrics from the Python AI system.");
    }
}
