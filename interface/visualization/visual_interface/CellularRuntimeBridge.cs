using System;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// MAGNUS taxonomy component CellularRuntimeBridge (Revision 2025-08-16)
    /// Provides a lightweight, file-based cellular connector between the wider AIOS runtime
    /// (runtime_intelligence logs + context dumps) and the visualization layer.
    /// Phase 1 implementation: Polls latest ai_context_dump_* JSON and exposes basic metrics.
    /// Future phases: WebSocket streaming, delta-based ingestion, bidirectional control.
    /// </summary>
    public class CellularRuntimeBridge : IDisposable
    {
        private readonly string _contextDir;
        private readonly Timer? _pollTimer;
        private readonly TimeSpan _pollInterval = TimeSpan.FromSeconds(1.5);
        private readonly object _lock = new();
        private volatile BridgeMetrics _latest = new();
        private bool _enabled;

        public CellularRuntimeBridge()
        {
            _contextDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory,
                "..", "runtime_intelligence", "logs", "aios_context");
            try
            {
                if (Directory.Exists(_contextDir))
                {
                    _enabled = true;
                    _pollTimer = new Timer(Poll, null, TimeSpan.Zero, _pollInterval);
                }
            }
            catch
            {
                _enabled = false;
            }
        }

        private void Poll(object? state)
        {
            if (!_enabled) return;
            try
            {
                var dir = new DirectoryInfo(_contextDir);
                var file = dir.GetFiles("ai_context_dump_*.json")
                    .OrderByDescending(f => f.LastWriteTimeUtc)
                    .FirstOrDefault();
                if (file == null) return;
                string json = File.ReadAllText(file.FullName);
                using var doc = JsonDocument.Parse(json);
                var root = doc.RootElement.GetProperty("aios_runtime_intelligence_dump");
                var session = root.GetProperty("session_summary");
                double eventsPerSecond = session.GetProperty("events_per_second").GetDouble();
                int totalEvents = session.GetProperty("total_events").GetInt32();
                double consciousnessLevel = 0.0;
                if (session.TryGetProperty("consciousness_metrics", out var cl) && cl.TryGetProperty("current_level", out var clv))
                {
                    if (clv.ValueKind == JsonValueKind.Number) consciousnessLevel = clv.GetDouble();
                }
                var modules = session.GetProperty("events_by_module").EnumerateObject().Select(p => p.Name).ToArray();
                
                // Extract deep consciousness indicators
                int consciousnessPatterns = 0;
                double patternRecognitionAccuracy = 0.0;
                int recursiveDepth = 0;
                int metaCognitiveOperations = 0;
                double interModuleCoherence = 0.0;
                double temporalConsistency = 0.0;
                double quantumEntanglementStrength = 0.0;
                double memoryUsageMB = 0.0;
                double cpuPercent = 0.0;
                int threadCount = 0;
                string[] recentEvents = Array.Empty<string>();
                
                if (session.TryGetProperty("consciousness_metrics", out var consciousnessMetrics))
                {
                    if (consciousnessMetrics.TryGetProperty("indicators", out var indicators))
                    {
                        patternRecognitionAccuracy = indicators.GetProperty("pattern_recognition_accuracy").GetDouble();
                        recursiveDepth = indicators.GetProperty("recursive_depth").GetInt32();
                        metaCognitiveOperations = indicators.GetProperty("meta_cognitive_operations").GetInt32();
                        interModuleCoherence = indicators.GetProperty("inter_module_coherence").GetDouble();
                        temporalConsistency = indicators.GetProperty("temporal_consistency").GetDouble();
                        quantumEntanglementStrength = indicators.GetProperty("quantum_entanglement_strength").GetDouble();
                    }
                }
                
                if (session.TryGetProperty("system_health", out var sh))
                {
                    memoryUsageMB = sh.GetProperty("memory_usage_mb").GetDouble();
                    cpuPercent = sh.GetProperty("cpu_percent").GetDouble();
                    threadCount = sh.GetProperty("thread_count").GetInt32();
                }
                
                // Extract recent significant events
                if (root.TryGetProperty("recent_significant_events", out var events))
                {
                    recentEvents = events.EnumerateArray()
                        .Take(10)
                        .Select(e => $"{e.GetProperty("module").GetString()}: {e.GetProperty("event_type").GetString()}")
                        .ToArray();
                }
                
                lock (_lock)
                {
                    _latest = new BridgeMetrics
                    {
                        Timestamp = DateTime.UtcNow,
                        ConsciousnessLevel = consciousnessLevel,
                        QuantumCoherence = patternRecognitionAccuracy, // Map to actual quantum coherence
                        EmergenceLevel = consciousnessLevel,
                        EventsPerSecond = eventsPerSecond,
                        TotalEvents = totalEvents,
                        ActiveModules = modules,
                        Live = true,
                        ConsciousnessPatterns = consciousnessPatterns,
                        PatternRecognitionAccuracy = patternRecognitionAccuracy,
                        RecursiveDepth = recursiveDepth,
                        MetaCognitiveOperations = metaCognitiveOperations,
                        InterModuleCoherence = interModuleCoherence,
                        TemporalConsistency = temporalConsistency,
                        QuantumEntanglementStrength = quantumEntanglementStrength,
                        MemoryUsageMB = memoryUsageMB,
                        CpuPercent = cpuPercent,
                        ThreadCount = threadCount,
                        RecentEvents = recentEvents
                    };
                }
            }
            catch
            {
                // swallow; non-fatal
            }
        }

        public BridgeMetrics GetLatest() => _latest;

        public void Dispose()
        {
            _pollTimer?.Dispose();
        }
    }

    public record BridgeMetrics
    {
        public DateTime Timestamp { get; init; } = DateTime.UtcNow;
        public double ConsciousnessLevel { get; init; }
        public double QuantumCoherence { get; init; }
        public double EmergenceLevel { get; init; }
        public double EventsPerSecond { get; init; }
        public int TotalEvents { get; init; }
        public string[] ActiveModules { get; init; } = Array.Empty<string>();
        public bool Live { get; init; }

        // NEW: Deep Consciousness Metrics
        public int ConsciousnessPatterns { get; init; }
        public double PatternRecognitionAccuracy { get; init; }
        public int RecursiveDepth { get; init; }
        public int MetaCognitiveOperations { get; init; }
        public double InterModuleCoherence { get; init; }
        public double TemporalConsistency { get; init; }
        public double QuantumEntanglementStrength { get; init; }
        public double MemoryUsageMB { get; init; }
        public double CpuPercent { get; init; }
        public int ThreadCount { get; init; }
        public string[] RecentEvents { get; init; } = Array.Empty<string>();
    }
}
