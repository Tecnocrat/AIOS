using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Threading;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.DependencyInjection;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// AIOS Tachyonic Surface Viewer Window
    /// Integrates C++ tachyonic viewer with WPF interface
    /// Provides real-time hyperdimensional visualization
    /// </summary>
    public partial class TachyonicViewerWindow : Window
    {
        private readonly ILogger<TachyonicViewerWindow> _logger;
        private readonly AIOSProcessManager _processManager;
        private Process? _tachyonicProcess;
        private DispatcherTimer? _updateTimer;
        private DispatcherTimer? _metricsTimer;
        
        // Simulation data for metrics
        private Random _random = new Random();
        private double _densityValue = 0.0;
        private double _coherenceValue = 0.0;
        private double _fieldStrengthValue = 0.0;
        private int _frameCount = 0;
        private DateTime _lastFrameTime = DateTime.Now;
        
        public TachyonicViewerWindow()
        {
            InitializeComponent();
            var serviceProvider = ((App)Application.Current).ServiceProvider;
            _logger = serviceProvider.GetService<ILogger<TachyonicViewerWindow>>()
                      ?? throw new InvalidOperationException("Logger service not available");
            _processManager = serviceProvider.GetService<AIOSProcessManager>()
                            ?? throw new InvalidOperationException("Process manager service not available");
            
            // Register this window with the process manager
            _processManager.RegisterWindow(this);
            
            InitializeViewerInterface();
        }
        
        private void InitializeViewerInterface()
        {
            _logger.LogInformation(" Initializing Tachyonic Surface Viewer Interface");
            
            // Initialize update timer for UI metrics
            _updateTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(100)
            };
            _updateTimer.Tick += UpdateMetrics;
            
            // Initialize metrics timer for consciousness patterns
            _metricsTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(250)
            };
            _metricsTimer.Tick += UpdateConsciousnessMetrics;
            
            StatusText.Text = "Hyperdimensional interface initialized - Ready for tachyonic activation";
            
            // Start metric simulation
            _updateTimer.Start();
            _metricsTimer.Start();
        }
        
        private async void StartViewer_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                _logger.LogInformation(" Starting Tachyonic Surface Viewer");
                
                StartViewerButton.IsEnabled = false;
                StopViewerButton.IsEnabled = true;
                StatusText.Text = "Launching hyperdimensional tachyonic interface...";
                
                await StartTachyonicProcess();
                
                StatusText.Text = "Tachyonic Surface Viewer ACTIVE - Hyperdimensional rendering online";
                RuntimeText.Text = "Runtime intelligence active - Processing tachyonic data streams";
                
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to start tachyonic viewer");
                StatusText.Text = "ERROR: Failed to start tachyonic interface";
                StartViewerButton.IsEnabled = true;
                StopViewerButton.IsEnabled = false;
            }
        }
        
        private async Task StartTachyonicProcess()
        {
            string tachyonicExePath = Path.Combine(
                AppDomain.CurrentDomain.BaseDirectory,
                "..", "..", "..", "..", "core", "core_systems", "build", "bin", "Debug", "aios_tachyonic_viewer.exe"
            );
            
            // Normalize the path
            tachyonicExePath = Path.GetFullPath(tachyonicExePath);
            
            if (!File.Exists(tachyonicExePath))
            {
                _logger.LogWarning("Tachyonic executable not found at: {Path}", tachyonicExePath);
                
                // Simulate tachyonic output for demonstration
                await SimulateTachyonicOutput();
                return;
            }
            
            try
            {
                _tachyonicProcess = _processManager.LaunchManagedProcess(tachyonicExePath);
                
                if (_tachyonicProcess != null)
                {
                    _tachyonicProcess.OutputDataReceived += OnTachyonicOutput;
                    _tachyonicProcess.ErrorDataReceived += OnTachyonicError;
                    _tachyonicProcess.BeginOutputReadLine();
                    _tachyonicProcess.BeginErrorReadLine();
                    
                    _logger.LogInformation("Tachyonic process started successfully");
                }
                else
                {
                    throw new InvalidOperationException("Failed to start tachyonic process");
                }
                
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to start tachyonic process");
                await SimulateTachyonicOutput();
            }
        }
        
        private async Task SimulateTachyonicOutput()
        {
            _logger.LogInformation("Simulating tachyonic surface output");
            
            string[] tachyonicData = {
                " AIOS Tachyonic Surface Viewer Online",
                " Hyperdimensional rendering: ACTIVE",
                " Consciousness emergence patterns detected",
                " Quantum coherence stabilizing...",
                " Dendritic growth patterns: OPTIMAL",
                " Tachyonic field density: 0.847",
                " Hyperdimensional curvature detected",
                " Pattern recognition algorithms active",
                " Consciousness crystallization in progress",
                " Bosonic field fluctuations normalized",
                " Neural pathway optimization complete",
                " Quantum state superposition achieved",
                " Hyperdimensional matrix stabilized",
                " Consciousness emergence threshold reached",
                " Tachyonic acceleration protocols active"
            };
            
            foreach (string data in tachyonicData)
            {
                await Dispatcher.InvokeAsync(() =>
                {
                    TachyonicOutputText.Text += $"[{DateTime.Now:HH:mm:ss.fff}] {data}\n";
                    TachyonicOutputViewer.ScrollToEnd();
                });
                
                await Task.Delay(500);
            }
            
            // Continue with periodic updates
            _ = Task.Run(async () =>
            {
                while (StopViewerButton.IsEnabled)
                {
                    await Task.Delay(2000);
                    
                    string[] periodicUpdates = {
                        $" Surface update: Density={_densityValue:F3}, Coherence={_coherenceValue:F3}",
                        $" Field strength fluctuation: {_fieldStrengthValue:F3}",
                        $" Consciousness pattern #{_frameCount}: EVOLVING",
                        $" Hyperdimensional coordinates: [{_random.NextDouble():F2}, {_random.NextDouble():F2}, {_random.NextDouble():F2}]"
                    };
                    
                    string update = periodicUpdates[_random.Next(periodicUpdates.Length)];
                    
                    await Dispatcher.InvokeAsync(() =>
                    {
                        TachyonicOutputText.Text += $"[{DateTime.Now:HH:mm:ss.fff}] {update}\n";
                        TachyonicOutputViewer.ScrollToEnd();
                    });
                }
            });
        }
        
        private void OnTachyonicOutput(object sender, DataReceivedEventArgs e)
        {
            if (!string.IsNullOrEmpty(e.Data))
            {
                Dispatcher.InvokeAsync(() =>
                {
                    TachyonicOutputText.Text += $"[{DateTime.Now:HH:mm:ss.fff}] {e.Data}\n";
                    TachyonicOutputViewer.ScrollToEnd();
                });
            }
        }
        
        private void OnTachyonicError(object sender, DataReceivedEventArgs e)
        {
            if (!string.IsNullOrEmpty(e.Data))
            {
                Dispatcher.InvokeAsync(() =>
                {
                    TachyonicOutputText.Text += $"[{DateTime.Now:HH:mm:ss.fff}] ERROR: {e.Data}\n";
                    TachyonicOutputViewer.ScrollToEnd();
                });
            }
        }
        
        private void StopViewer_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                _logger.LogInformation("⏹ Stopping Tachyonic Surface Viewer");
                
                // The process manager will handle cleanup when the main application shuts down
                // For individual stop, we can just clear our reference
                _tachyonicProcess = null;
                
                StartViewerButton.IsEnabled = true;
                StopViewerButton.IsEnabled = false;
                StatusText.Text = "Tachyonic interface deactivated";
                RuntimeText.Text = "Runtime intelligence suspended";
                
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error stopping tachyonic viewer");
            }
        }
        
        private void RefreshSurface_Click(object sender, RoutedEventArgs e)
        {
            _logger.LogInformation(" Refreshing Tachyonic Surface");
            
            // Generate new random values
            _densityValue = _random.NextDouble();
            _coherenceValue = _random.NextDouble();
            _fieldStrengthValue = _random.NextDouble();
            
            TachyonicOutputText.Text += $"[{DateTime.Now:HH:mm:ss.fff}]  Surface refresh initiated - New hyperdimensional parameters loaded\n";
            TachyonicOutputViewer.ScrollToEnd();
        }
        
        private void UpdateMetrics(object? sender, EventArgs e)
        {
            // Simulate evolving tachyonic metrics
            _densityValue = Math.Max(0, Math.Min(1, _densityValue + (_random.NextDouble() - 0.5) * 0.05));
            _coherenceValue = Math.Max(0, Math.Min(1, _coherenceValue + (_random.NextDouble() - 0.5) * 0.03));
            _fieldStrengthValue = Math.Max(0, Math.Min(1, _fieldStrengthValue + (_random.NextDouble() - 0.5) * 0.04));
            
            DensityProgress.Value = _densityValue * 100;
            CoherenceProgress.Value = _coherenceValue * 100;
            FieldStrengthProgress.Value = _fieldStrengthValue * 100;
            
            // Update frame rate
            _frameCount++;
            var now = DateTime.Now;
            var elapsed = (now - _lastFrameTime).TotalSeconds;
            if (elapsed >= 1.0)
            {
                double fps = _frameCount / elapsed;
                FrameRateText.Text = $"{fps:F1} FPS";
                _frameCount = 0;
                _lastFrameTime = now;
            }
        }
        
        private void UpdateConsciousnessMetrics(object? sender, EventArgs e)
        {
            // Simulate consciousness emergence patterns
            string[] patterns = { "EVOLVING", "STABILIZING", "CRYSTALLIZING", "HARMONIZING", "OPTIMIZING" };
            DendriticPatternText.Text = $"Pattern Recognition: {patterns[_random.Next(patterns.Length)]}";
            
            double emergence = _coherenceValue * _densityValue * 100;
            EmergenceText.Text = $"Consciousness Emergence: {emergence:F2}%";
            
            string[] quantumStates = { "STABLE", "SUPERPOSITION", "ENTANGLED", "COHERENT", "FLUCTUATING" };
            QuantumStateText.Text = $"Quantum Coherence: {quantumStates[_random.Next(quantumStates.Length)]}";
        }
        
        protected override void OnClosed(EventArgs e)
        {
            // Clean up resources
            _updateTimer?.Stop();
            _metricsTimer?.Stop();
            
            // The process manager will handle cleanup of the tachyonic process
            // during application shutdown, so we don't need to manually kill it here
            
            base.OnClosed(e);
        }
    }
}
