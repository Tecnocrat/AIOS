using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
// Disambiguate Timer type explicitly
using Timer = System.Timers.Timer;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Emits UI/runtime surrogate KPI metrics to runtime_intelligence/logs/ui/ui_metrics.json
    /// Consumed by validation harness for KPI evaluation.
    /// </summary>
    public sealed class UIMetricsEmitter : IDisposable
    {
    private readonly Timer _timer;
        private readonly DateTime _start = DateTime.UtcNow;
        private readonly string _outputPath;
        private int _frameSamples;
        private double _frameAccumMs;
        private readonly object _lock = new();

        public UIMetricsEmitter(double intervalSeconds = 5.0)
        {
            var basePath = AppDomain.CurrentDomain.BaseDirectory;
            _outputPath = Path.Combine(basePath, "..", "..", "runtime_intelligence", "logs", "ui", "ui_metrics.json");
            Directory.CreateDirectory(Path.GetDirectoryName(_outputPath)!);
            _timer = new Timer(intervalSeconds * 1000.0);
            _timer.Elapsed += (_, _) => Flush();
            _timer.AutoReset = true;
            _timer.Start();
        }

        /// <summary>
        /// Register a rendered frame (duration in ms) to compute FPS.
        /// Call from render loop / update tick.
        /// </summary>
        public void RegisterFrame(double frameDurationMs)
        {
            lock (_lock)
            {
                _frameSamples++;
                _frameAccumMs += frameDurationMs;
            }
        }

        private void Flush()
        {
            Dictionary<string, object> payload = new();
            double fps = 0;
            lock (_lock)
            {
                if (_frameSamples > 0 && _frameAccumMs > 0)
                {
                    double avgMs = _frameAccumMs / _frameSamples;
                    fps = 1000.0 / avgMs;
                }
                // Reset accumulation for next window
                _frameSamples = 0;
                _frameAccumMs = 0;
            }
            var uptime = (DateTime.UtcNow - _start).TotalSeconds;
            payload["render_fps"] = Math.Round(fps, 2);
            payload["ui_uptime_sec"] = Math.Round(uptime, 1);
            // Placeholder: future instrumentation
            payload["state_restore_sec"] = null;
            payload["metadata_rate_ctx_per_min"] = null;
            payload["cpp_python_latency_ms"] = null;
            payload["generated_at"] = DateTime.UtcNow.ToString("o");

            try
            {
                var json = JsonSerializer.Serialize(payload, new JsonSerializerOptions { WriteIndented = true });
                File.WriteAllText(_outputPath, json);
            }
            catch { /* ignore IO errors */ }
        }

        public void Dispose()
        {
            _timer.Stop();
            _timer.Dispose();
        }
    }
}
