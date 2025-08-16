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
        private readonly Timer _pollTimer;
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
                if (session.TryGetProperty("consciousness_metrics", out var cm) && cm.TryGetProperty("current_level", out var cl))
                {
                    if (cl.ValueKind == JsonValueKind.Number) consciousnessLevel = cl.GetDouble();
                }
                var modules = session.GetProperty("events_by_module").EnumerateObject().Select(p => p.Name).ToArray();
                lock (_lock)
                {
                    _latest = new BridgeMetrics
                    {
                        Timestamp = DateTime.UtcNow,
                        ConsciousnessLevel = consciousnessLevel,
                        QuantumCoherence = 0.0, // Not yet surfaced in context dump
                        EmergenceLevel = consciousnessLevel, // Placeholder mapping
                        EventsPerSecond = eventsPerSecond,
                        TotalEvents = totalEvents,
                        ActiveModules = modules,
                        Live = true
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
    }
}
