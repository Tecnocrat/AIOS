using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
// Disambiguate Timer type explicitly
using Timer = System.Timers.Timer;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Enhanced UI Metrics Emitter for AIOS Visual Interface with comprehensive KPI tracking
    /// Emits UI/runtime surrogate KPI metrics to runtime_intelligence/logs/ui/ui_metrics.json
    /// Consumed by validation harness for KPI evaluation and system health monitoring
    /// </summary>
    public sealed class UIMetricsEmitter : IDisposable
    {
        private readonly ILogger<UIMetricsEmitter> _logger;
        private readonly Timer _timer;
        private readonly DateTime _start = DateTime.UtcNow;
        private readonly string _outputPath;
        private readonly string _backupPath;
        private readonly SemaphoreSlim _flushSemaphore;
        private readonly CancellationTokenSource _cts;

        // Metrics accumulation with thread safety
        private int _frameSamples;
        private double _frameAccumMs;
        private int _errorCount;
        private int _flushCount;
        private DateTime _lastFlushTime = DateTime.MinValue;
        private readonly object _metricsLock = new();

        // Performance tracking
        private double _peakMemoryUsageMB;
        private double _averageFlushDurationMs;
        private int _flushDurationSamples;

        // Configuration
        private readonly TimeSpan _flushInterval;
        private readonly bool _enableBackup;
        private readonly int _maxBackupFiles = 10;

        private bool _disposed;

        public UIMetricsEmitter(ILogger<UIMetricsEmitter> logger, double intervalSeconds = 5.0, bool enableBackup = true)
        {
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
            _flushInterval = TimeSpan.FromSeconds(intervalSeconds);
            _enableBackup = enableBackup;
            _flushSemaphore = new SemaphoreSlim(1, 1);
            _cts = new CancellationTokenSource();

            var basePath = AppDomain.CurrentDomain.BaseDirectory;
            _outputPath = Path.Combine(basePath, "..", "..", "runtime_intelligence", "logs", "ui", "ui_metrics.json");
            _backupPath = Path.Combine(basePath, "..", "..", "runtime_intelligence", "logs", "ui", "backups");

            // Ensure directories exist
            Directory.CreateDirectory(Path.GetDirectoryName(_outputPath)!);
            if (_enableBackup)
            {
                Directory.CreateDirectory(_backupPath);
            }

            _timer = new Timer(_flushInterval.TotalMilliseconds);
            _timer.Elapsed += async (_, _) => await FlushAsync();
            _timer.AutoReset = true;
            _timer.Start();

            _logger.LogInformation("UIMetricsEmitter initialized with {Interval}s interval, output: {Path}",
                intervalSeconds, _outputPath);
        }

        /// <summary>
        /// Register a rendered frame (duration in ms) to compute FPS and performance metrics
        /// Call from render loop / update tick
        /// </summary>
        public void RegisterFrame(double frameDurationMs)
        {
            if (frameDurationMs < 0)
            {
                _logger.LogWarning("Invalid frame duration: {Duration}ms", frameDurationMs);
                return;
            }

            lock (_metricsLock)
            {
                _frameSamples++;
                _frameAccumMs += frameDurationMs;

                // Track peak memory usage
                var currentMemoryMB = Process.GetCurrentProcess().WorkingSet64 / (1024.0 * 1024.0);
                if (currentMemoryMB > _peakMemoryUsageMB)
                {
                    _peakMemoryUsageMB = currentMemoryMB;
                }
            }
        }

        /// <summary>
        /// Register an error occurrence for error rate tracking
        /// </summary>
        public void RegisterError(string errorType = "unknown")
        {
            Interlocked.Increment(ref _errorCount);
            _logger.LogDebug("Error registered: {Type}", errorType);
        }

        /// <summary>
        /// Get current metrics snapshot without triggering a flush
        /// </summary>
        public UIMetricsSnapshot GetCurrentMetrics()
        {
            lock (_metricsLock)
            {
                var fps = 0.0;
                if (_frameSamples > 0 && _frameAccumMs > 0)
                {
                    var avgMs = _frameAccumMs / _frameSamples;
                    fps = 1000.0 / avgMs;
                }

                return new UIMetricsSnapshot
                {
                    RenderFps = Math.Round(fps, 2),
                    FrameSamples = _frameSamples,
                    AverageFrameTimeMs = _frameSamples > 0 ? _frameAccumMs / _frameSamples : 0,
                    PeakMemoryUsageMB = _peakMemoryUsageMB,
                    ErrorCount = _errorCount,
                    FlushCount = _flushCount,
                    UptimeSeconds = (DateTime.UtcNow - _start).TotalSeconds
                };
            }
        }

        /// <summary>
        /// Force immediate flush of metrics to disk
        /// </summary>
        public async Task ForceFlushAsync()
        {
            await FlushAsync();
        }

        private async Task FlushAsync()
        {
            if (_disposed) return;

            var flushStartTime = DateTime.UtcNow;

            try
            {
                await _flushSemaphore.WaitAsync(_cts.Token);

                // Create metrics payload with nullable values for optional metrics
                var payload = new Dictionary<string, object?>
                {
                    ["render_fps"] = 0.0,
                    ["ui_uptime_sec"] = 0.0,
                    ["frame_samples"] = 0,
                    ["average_frame_time_ms"] = 0.0,
                    ["peak_memory_mb"] = 0.0,
                    ["error_count"] = 0,
                    ["flush_count"] = 0,
                    ["system_cpu_percent"] = GetCpuUsage(),
                    ["system_memory_mb"] = GetMemoryUsage(),
                    ["generated_at"] = DateTime.UtcNow.ToString("o")
                };

                // Calculate FPS and update metrics
                lock (_metricsLock)
                {
                    if (_frameSamples > 0 && _frameAccumMs > 0)
                    {
                        var avgMs = _frameAccumMs / _frameSamples;
                        var fps = 1000.0 / avgMs;
                        payload["render_fps"] = Math.Round(fps, 2);
                        payload["average_frame_time_ms"] = Math.Round(avgMs, 2);
                    }

                    payload["frame_samples"] = _frameSamples;
                    payload["peak_memory_mb"] = Math.Round(_peakMemoryUsageMB, 2);
                    payload["error_count"] = _errorCount;
                    payload["flush_count"] = ++_flushCount;

                    // Reset accumulation for next window
                    _frameSamples = 0;
                    _frameAccumMs = 0;
                }

                var uptime = (DateTime.UtcNow - _start).TotalSeconds;
                payload["ui_uptime_sec"] = Math.Round(uptime, 1);

                // AIOS-specific metrics (placeholders for future implementation)
                payload["state_restore_sec"] = null; // Will be populated when state manager is integrated
                payload["metadata_rate_ctx_per_min"] = null; // Will be populated by metadata processing
                payload["cpp_python_latency_ms"] = null; // Will be populated by bridge monitoring
                payload["consciousness_sync_latency_ms"] = null; // AIOS-specific metric
                payload["neural_pattern_recognition_rate"] = null; // AIOS-specific metric

                // Performance metrics
                var flushDuration = (DateTime.UtcNow - flushStartTime).TotalMilliseconds;
                _averageFlushDurationMs = (_averageFlushDurationMs * _flushDurationSamples + flushDuration) / (++_flushDurationSamples);
                payload["average_flush_duration_ms"] = Math.Round(_averageFlushDurationMs, 2);

                // Write metrics to file
                await WriteMetricsToFileAsync(payload);

                _lastFlushTime = DateTime.UtcNow;
                _logger.LogTrace("Metrics flushed successfully in {Duration}ms", flushDuration);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to flush UI metrics");
                RegisterError("flush_error");
            }
            finally
            {
                _flushSemaphore.Release();
            }
        }

        private async Task WriteMetricsToFileAsync(Dictionary<string, object?> payload)
        {
            try
            {
                var json = JsonSerializer.Serialize(payload, new JsonSerializerOptions
                {
                    WriteIndented = true,
                    DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull
                });

                // Create backup if enabled
                if (_enableBackup && File.Exists(_outputPath))
                {
                    var backupFileName = $"ui_metrics_{DateTime.UtcNow:yyyyMMdd_HHmmss}.json";
                    var backupFilePath = Path.Combine(_backupPath, backupFileName);
                    await Task.Run(() => File.Copy(_outputPath, backupFilePath, true));

                    // Cleanup old backups
                    await CleanupOldBackupsAsync();
                }

                // Write current metrics
                await File.WriteAllTextAsync(_outputPath, json);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to write metrics to file");
                throw;
            }
        }

        private async Task CleanupOldBackupsAsync()
        {
            if (!_enableBackup) return;

            try
            {
                var backupFiles = await Task.Run(() => Directory.GetFiles(_backupPath, "ui_metrics_*.json"));
                if (backupFiles.Length <= _maxBackupFiles) return;

                // Sort by creation time and remove oldest
                await Task.Run(() => Array.Sort(backupFiles, (x, y) =>
                    File.GetCreationTime(x).CompareTo(File.GetCreationTime(y))));

                for (int i = 0; i < backupFiles.Length - _maxBackupFiles; i++)
                {
                    try
                    {
                        await Task.Run(() => File.Delete(backupFiles[i]));
                    }
                    catch (Exception ex)
                    {
                        _logger.LogWarning(ex, "Failed to delete old backup: {File}", backupFiles[i]);
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Failed to cleanup old backups");
            }
        }

        private static double GetCpuUsage()
        {
            try
            {
                using var cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
                cpuCounter.NextValue();
                System.Threading.Thread.Sleep(100); // Allow counter to collect data
                return Math.Round(cpuCounter.NextValue(), 1);
            }
            catch
            {
                return 0.0; // Return 0 on error rather than throwing
            }
        }

        private static double GetMemoryUsage()
        {
            try
            {
                var process = Process.GetCurrentProcess();
                return Math.Round(process.WorkingSet64 / (1024.0 * 1024.0), 1);
            }
            catch
            {
                return 0.0;
            }
        }

        #region IDisposable Implementation

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        private void Dispose(bool disposing)
        {
            if (_disposed) return;

            if (disposing)
            {
                _cts.Cancel();
                _timer.Stop();
                _timer.Dispose();
                _flushSemaphore.Dispose();
                _cts.Dispose();

                // Final flush before disposal
                try
                {
                    FlushAsync().Wait(TimeSpan.FromSeconds(5));
                }
                catch (Exception ex)
                {
                    _logger.LogWarning(ex, "Failed to perform final metrics flush during disposal");
                }

                _logger.LogInformation("UIMetricsEmitter disposed successfully");
            }

            _disposed = true;
        }

        #endregion
    }

    /// <summary>
    /// Snapshot of current UI metrics for real-time monitoring
    /// </summary>
    public class UIMetricsSnapshot
    {
        public double RenderFps { get; set; }
        public int FrameSamples { get; set; }
        public double AverageFrameTimeMs { get; set; }
        public double PeakMemoryUsageMB { get; set; }
        public int ErrorCount { get; set; }
        public int FlushCount { get; set; }
        public double UptimeSeconds { get; set; }

        public override string ToString()
        {
            return $"FPS: {RenderFps:F1}, Memory: {PeakMemoryUsageMB:F1}MB, Errors: {ErrorCount}, Uptime: {UptimeSeconds:F0}s";
        }
    }
}
