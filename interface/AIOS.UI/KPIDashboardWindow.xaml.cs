using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Threading;

namespace AIOS.UI {
    public partial class KPIDashboardWindow : Window {
    private readonly DispatcherTimer _timer;
    private DateTime _lastFetch = DateTime.MinValue;
    private const int RefreshIntervalMs = 250; // faster cadence (<500ms target)
    private const string SummaryPath = "runtime_intelligence/context/full_system_validation.json";
    private const string CoreMetricsPath = "runtime_intelligence/logs/core/core_metrics.json";
    private const string EvolutionLineagePath = "runtime_intelligence/logs/evolution/evolution_lineage.jsonl";
    private const string ThresholdsPath = "runtime_intelligence/context/kpi_thresholds.json";
    private readonly Stopwatch _latencySw = new();
    private long _coreFilePos = 0;
    private long _evolFilePos = 0;
    private readonly List<string> _streamingLines = new();
    private DateTime _lastStreamScan = DateTime.MinValue;

        // Lazy control references
        private TextBlock? LatencyTextRef; private TextBlock? StatusBarTextRef; private TextBlock? KpiPassRef; private TextBlock? KpiFailRef; private TextBlock? ThresholdVersionRef; private TextBlock? StreamingStatusRef; private ListView? KPIListRef; private StackPanel? MetricsStackRef;

        private void ResolveControlsOnce() {
            if(KPIListRef!=null) return;
            KPIListRef = FindName("KPIList") as ListView;
            MetricsStackRef = FindName("MetricsStack") as StackPanel;
            LatencyTextRef = FindName("LatencyText") as TextBlock;
            StatusBarTextRef = FindName("StatusBarText") as TextBlock;
            KpiPassRef = FindName("KpiPassCount") as TextBlock;
            KpiFailRef = FindName("KpiFailCount") as TextBlock;
            ThresholdVersionRef = FindName("ThresholdVersion") as TextBlock;
            StreamingStatusRef = FindName("StreamingStatus") as TextBlock;
        }

        public KPIDashboardWindow() {
            InitializeComponent();
            _timer = new DispatcherTimer { Interval = TimeSpan.FromMilliseconds(RefreshIntervalMs) };
            _timer.Tick += (_, __) => { try { RefreshData(); StreamUpdate(); } catch { } };
            _timer.Start();
            RefreshData();
        }

        private record KPIEntry(string Name, string? Value, string Status, string Rule);

        private void Refresh_Click(object sender, RoutedEventArgs e) { RefreshData(force:true); }

        private void RefreshData(bool force=false) {
            if(!force && (DateTime.UtcNow - _lastFetch).TotalMilliseconds < 200) return;
            _latencySw.Restart();
            ResolveControlsOnce();
            List<KPIEntry> entries = new();
            try {
                if(File.Exists(SummaryPath)) {
                    using var fs = File.OpenRead(SummaryPath);
                    using var doc = JsonDocument.Parse(fs);
                    var root = doc.RootElement;
                    TryLoadThresholdVersion();
                    if(root.TryGetProperty("kpi_evaluation", out var eval)) {
                        foreach(var prop in eval.EnumerateObject()) {
                            var kp = prop.Value;
                            string? valStr = kp.TryGetProperty("value", out var v) && v.ValueKind != JsonValueKind.Null ? v.ToString() : null;
                            string status = kp.TryGetProperty("status", out var s) ? s.GetString() ?? "?" : "?";
                            string rule = kp.TryGetProperty("rule", out var r) ? r.ToString() : "";
                            entries.Add(new KPIEntry(prop.Name, valStr, status, rule));
                        }
                    }
                }
            } catch(Exception ex) {
                if(StatusBarTextRef!=null) StatusBarTextRef.Text = "Load error: " + ex.Message;
            }
            if(KPIListRef!=null) KPIListRef.ItemsSource = entries;
            MetricsStackRef?.Children.Clear();
            int pass=0, fail=0;
            foreach(var e in entries) {
                if(e.Status=="pass") pass++; else if(e.Status=="fail") fail++;
                var tb = new System.Windows.Controls.TextBlock {
                    Text = $"{e.Name}: {e.Value ?? "-"} ({e.Status})",
                    Foreground = e.Status == "fail" ? System.Windows.Media.Brushes.OrangeRed : e.Status == "pass" ? System.Windows.Media.Brushes.LightGreen : System.Windows.Media.Brushes.LightGray,
                    Margin = new Thickness(2,2,2,2),
                    FontSize = 12
                };
                MetricsStackRef?.Children.Add(tb);
            }
            // aggregate pass/fail already computed above
            if(KpiPassRef!=null) KpiPassRef.Text = pass.ToString();
            if(KpiFailRef!=null) KpiFailRef.Text = fail.ToString();
            _latencySw.Stop();
            if(LatencyTextRef!=null) LatencyTextRef.Text = _latencySw.ElapsedMilliseconds + " ms";
            if(StatusBarTextRef!=null) StatusBarTextRef.Text = $"KPI entries: {entries.Count}";
            _lastFetch = DateTime.UtcNow;
        }

        private void TryLoadThresholdVersion() {
            try {
                if(File.Exists(ThresholdsPath)) {
                    using var fs = File.OpenRead(ThresholdsPath);
                    using var doc = JsonDocument.Parse(fs);
                    if(doc.RootElement.TryGetProperty("version", out var v)) {
                        if(ThresholdVersionRef!=null) ThresholdVersionRef.Text = v.GetRawText();
                    }
                }
            } catch { }
        }

        private void StreamUpdate() {
            if((DateTime.UtcNow - _lastStreamScan).TotalMilliseconds < 500) return;
            _lastStreamScan = DateTime.UtcNow;
            int newLines = 0;
            try {
                if(File.Exists(CoreMetricsPath)) {
                    using var fs = new FileStream(CoreMetricsPath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
                    if(fs.Length > _coreFilePos) {
                        fs.Seek(_coreFilePos, SeekOrigin.Begin);
                        using var sr = new StreamReader(fs);
                        string? line;
                        while((line = sr.ReadLine()) != null) { _streamingLines.Add("core:"+line); newLines++; }
                        _coreFilePos = fs.Length;
                    }
                }
                if(File.Exists(EvolutionLineagePath)) {
                    using var fs = new FileStream(EvolutionLineagePath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite);
                    if(fs.Length > _evolFilePos) {
                        fs.Seek(_evolFilePos, SeekOrigin.Begin);
                        using var sr = new StreamReader(fs);
                        string? line;
                        while((line = sr.ReadLine()) != null) { _streamingLines.Add("evo:"+line); newLines++; }
                        _evolFilePos = fs.Length;
                    }
                }
            } catch { }
            if(newLines>0) {
                if(_streamingLines.Count>30) _streamingLines.RemoveRange(0, _streamingLines.Count-30);
                if(StreamingStatusRef!=null) StreamingStatusRef.Text = $"Streaming: {newLines} new | core@{_coreFilePos} evol@{_evolFilePos}";
            }
            if(MetricsStackRef!=null) {
                for(int i=MetricsStackRef.Children.Count-1;i>=0;i--) {
                    if(MetricsStackRef.Children[i] is System.Windows.Controls.TextBlock t && t.Tag as string == "stream_line") {
                        MetricsStackRef.Children.RemoveAt(i);
                    }
                }
            }
            int start = Math.Max(0, _streamingLines.Count - 10);
            for(int i=start;i<_streamingLines.Count;i++) {
                var line = _streamingLines[i];
                var tb = new System.Windows.Controls.TextBlock {
                    Text = line,
                    Foreground = System.Windows.Media.Brushes.SlateGray,
                    FontSize = 10,
                    Margin = new Thickness(2,0,2,0),
                    Tag = "stream_line"
                };
                MetricsStackRef?.Children.Add(tb);
            }
        }

        private void EmitCapsule_Click(object sender, RoutedEventArgs e) {
            try {
                var psi = new ProcessStartInfo {
                    FileName = "python",
                    Arguments = "scripts/generate_status_capsule.py --force",
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true
                };
                var proc = Process.Start(psi);
                if(proc != null) {
                    proc.EnableRaisingEvents = true;
                    proc.Exited += (_, __) => Dispatcher.Invoke(() => {
            if(StatusBarTextRef!=null) StatusBarTextRef.Text = "Capsule emitted (exit " + proc.ExitCode + ")";
                    });
                }
        if(StatusBarTextRef!=null) StatusBarTextRef.Text = "Emitting status capsule...";
            } catch (Exception ex) {
        if(StatusBarTextRef!=null) StatusBarTextRef.Text = "Capsule error: " + ex.Message;
            }
        }
    }
}
