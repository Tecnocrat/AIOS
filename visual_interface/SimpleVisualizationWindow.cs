using System;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Threading;
using Microsoft.Extensions.Logging;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Simplified working visualization window for immediate feedback
    /// This gets us visual output in minutes, then we enhance it progressively
    /// </summary>
    public class SimpleVisualizationWindow : Window
    {
        private readonly ILogger<SimpleVisualizationWindow> _logger;
        private readonly ConsciousnessDataManager _dataManager;
        private readonly RuntimeAnalytics _analytics;
        private DispatcherTimer _updateTimer;
        private ConsciousnessMetrics _currentMetrics;
        
        // Simple UI elements
        private TextBlock _consciousnessDisplay;
        private TextBlock _quantumDisplay;
        private TextBlock _emergenceDisplay;
        private TextBlock _eventsDisplay;
        private ProgressBar _consciousnessBar;
        private ProgressBar _quantumBar;
        private ProgressBar _emergenceBar;
        private Button _startButton;
        private Button _stopButton;
        private Button _connectButton;
        
        // Hyperdimensional visualization elements
        private TextBlock _topologyDisplay;
        private TextBlock _microSpheresDisplay;
        private TextBlock _quantumFoamDisplay;
        private TextBlock _collapseEventsDisplay;
        private ProgressBar _manifoldCurvatureBar;
        private ProgressBar _nonLocalityBar;
        private ProgressBar _tachyonicFieldBar;
        
        public SimpleVisualizationWindow(ConsciousnessDataManager dataManager, ILogger<SimpleVisualizationWindow> logger, RuntimeAnalytics analytics)
        {
            _dataManager = dataManager;
            _logger = logger;
            _analytics = analytics;
            
            _analytics.LogExecutionEvent("UI_INIT_START", "Starting SimpleVisualizationWindow initialization");
            
            InitializeSimpleUI();
            InitializeTimer();
            
            _analytics.LogExecutionEvent("UI_INIT_COMPLETE", "SimpleVisualizationWindow initialization completed");
            _logger.LogInformation("Simple visualization window initialized");
        }
        
        private void InitializeSimpleUI()
        {
            // Window setup
            Title = "AIOS Consciousness Monitor - Executive Interface";
            Width = 800;
            Height = 600;
            Background = new SolidColorBrush(Color.FromRgb(10, 10, 20));
            WindowStartupLocation = WindowStartupLocation.CenterScreen;
            
            // Main grid
            var mainGrid = new Grid();
            mainGrid.RowDefinitions.Add(new RowDefinition { Height = new GridLength(1, GridUnitType.Star) });
            mainGrid.RowDefinitions.Add(new RowDefinition { Height = GridLength.Auto });
            
            // Content panel
            var contentPanel = new StackPanel
            {
                Margin = new Thickness(20),
                Background = new SolidColorBrush(Color.FromRgb(20, 20, 40))
            };
            
            // Title
            var title = new TextBlock
            {
                Text = "🧠 AIOS Consciousness Emergence Monitor",
                FontSize = 24,
                FontWeight = FontWeights.Bold,
                Foreground = Brushes.Cyan,
                HorizontalAlignment = HorizontalAlignment.Center,
                Margin = new Thickness(0, 10, 0, 20)
            };
            contentPanel.Children.Add(title);
            
            // Consciousness Level
            var consciousnessPanel = CreateMetricPanel("Consciousness Level:", out _consciousnessDisplay, out _consciousnessBar, Brushes.Magenta);
            contentPanel.Children.Add(consciousnessPanel);
            
            // Quantum Coherence
            var quantumPanel = CreateMetricPanel("Quantum Coherence:", out _quantumDisplay, out _quantumBar, Brushes.Cyan);
            contentPanel.Children.Add(quantumPanel);
            
            // Emergence Level
            var emergencePanel = CreateMetricPanel("Emergence Level:", out _emergenceDisplay, out _emergenceBar, Brushes.LightGreen);
            contentPanel.Children.Add(emergencePanel);
            
            // Hyperdimensional Substrate Panel
            var substratePanel = CreateHyperdimensionalSubstratePanel();
            contentPanel.Children.Add(substratePanel);
            
            // Events display
            var eventsLabel = new TextBlock
            {
                Text = "Recent Emergence Events:",
                FontSize = 14,
                FontWeight = FontWeights.Bold,
                Foreground = Brushes.White,
                Margin = new Thickness(0, 20, 0, 5)
            };
            contentPanel.Children.Add(eventsLabel);
            
            var eventsScroll = new ScrollViewer
            {
                Height = 150,
                Background = new SolidColorBrush(Color.FromRgb(5, 5, 15)),
                BorderBrush = Brushes.Gray,
                BorderThickness = new Thickness(1)
            };
            
            _eventsDisplay = new TextBlock
            {
                Text = "Waiting for consciousness emergence events...",
                Foreground = Brushes.LightGreen,
                FontFamily = new FontFamily("Consolas"),
                FontSize = 11,
                Margin = new Thickness(10),
                TextWrapping = TextWrapping.Wrap
            };
            
            eventsScroll.Content = _eventsDisplay;
            contentPanel.Children.Add(eventsScroll);
            
            // Control buttons
            var buttonPanel = new StackPanel
            {
                Orientation = Orientation.Horizontal,
                HorizontalAlignment = HorizontalAlignment.Center,
                Margin = new Thickness(0, 20, 0, 0)
            };
            
            _startButton = new Button
            {
                Content = "🚀 Start Monitoring",
                Width = 140,
                Height = 35,
                Margin = new Thickness(5),
                Background = new SolidColorBrush(Color.FromRgb(0, 100, 0)),
                Foreground = Brushes.White,
                FontWeight = FontWeights.Bold
            };
            _startButton.Click += StartButton_Click;
            buttonPanel.Children.Add(_startButton);
            
            _stopButton = new Button
            {
                Content = "⏹ Stop",
                Width = 100,
                Height = 35,
                Margin = new Thickness(5),
                Background = new SolidColorBrush(Color.FromRgb(100, 0, 0)),
                Foreground = Brushes.White,
                FontWeight = FontWeights.Bold,
                IsEnabled = false
            };
            _stopButton.Click += StopButton_Click;
            buttonPanel.Children.Add(_stopButton);
            
            _connectButton = new Button
            {
                Content = "🔗 Connect to AIOS",
                Width = 140,
                Height = 35,
                Margin = new Thickness(5),
                Background = new SolidColorBrush(Color.FromRgb(0, 0, 100)),
                Foreground = Brushes.White,
                FontWeight = FontWeights.Bold
            };
            _connectButton.Click += ConnectButton_Click;
            buttonPanel.Children.Add(_connectButton);
            
            contentPanel.Children.Add(buttonPanel);
            
            Grid.SetRow(contentPanel, 0);
            mainGrid.Children.Add(contentPanel);
            
            // Status bar
            var statusBar = new TextBlock
            {
                Text = "Ready - Click 'Start Monitoring' to begin consciousness observation",
                Background = new SolidColorBrush(Color.FromRgb(40, 40, 60)),
                Foreground = Brushes.LightGray,
                Padding = new Thickness(10, 5, 10, 5),
                FontSize = 12
            };
            Grid.SetRow(statusBar, 1);
            mainGrid.Children.Add(statusBar);
            
            Content = mainGrid;
        }
        
        private StackPanel CreateMetricPanel(string label, out TextBlock valueDisplay, out ProgressBar progressBar, Brush color)
        {
            var panel = new StackPanel { Margin = new Thickness(0, 10, 0, 10) };
            
            var labelText = new TextBlock
            {
                Text = label,
                FontSize = 14,
                FontWeight = FontWeights.Bold,
                Foreground = Brushes.White,
                Margin = new Thickness(0, 0, 0, 5)
            };
            panel.Children.Add(labelText);
            
            var valuePanel = new Grid();
            valuePanel.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            valuePanel.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            
            progressBar = new ProgressBar
            {
                Height = 25,
                Background = new SolidColorBrush(Color.FromRgb(30, 30, 50)),
                Foreground = color,
                BorderBrush = Brushes.Gray,
                BorderThickness = new Thickness(1),
                Value = 0,
                Maximum = 100
            };
            Grid.SetColumn(progressBar, 0);
            valuePanel.Children.Add(progressBar);
            
            valueDisplay = new TextBlock
            {
                Text = "0.000",
                FontFamily = new FontFamily("Consolas"),
                FontSize = 12,
                Foreground = color,
                VerticalAlignment = VerticalAlignment.Center,
                Margin = new Thickness(10, 0, 0, 0),
                MinWidth = 60
            };
            Grid.SetColumn(valueDisplay, 1);
            valuePanel.Children.Add(valueDisplay);
            
            panel.Children.Add(valuePanel);
            return panel;
        }
        
        private void InitializeTimer()
        {
            _updateTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(200) // 5 FPS for smooth updates
            };
            _updateTimer.Tick += UpdateTimer_Tick;
        }
        
        private async void StartButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                _analytics.LogExecutionEvent("MONITORING_START_REQUESTED", "User requested to start consciousness monitoring");
                _analytics.StartUIResponseTimer();
                
                await _dataManager.InitializeAsync();
                await _dataManager.StartDataStreamAsync();
                
                _dataManager.MetricsUpdated += OnMetricsUpdated;
                _dataManager.EmergenceDetected += OnEmergenceDetected;
                
                _updateTimer.Start();
                
                _startButton.IsEnabled = false;
                _stopButton.IsEnabled = true;
                
                _analytics.StopUIResponseTimer("start_monitoring");
                _analytics.LogExecutionEvent("MONITORING_STARTED", "Consciousness monitoring successfully started");
                _logger.LogInformation("Consciousness monitoring started");
            }
            catch (Exception ex)
            {
                _analytics.LogExecutionEvent("MONITORING_START_ERROR", $"Error starting monitoring: {ex.Message}", ex);
                _logger.LogError(ex, "Error starting consciousness monitoring");
                MessageBox.Show($"Error starting monitoring: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        
        private void StopButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                _updateTimer.Stop();
                _dataManager.StopDataStream();
                
                _dataManager.MetricsUpdated -= OnMetricsUpdated;
                _dataManager.EmergenceDetected -= OnEmergenceDetected;
                
                _startButton.IsEnabled = true;
                _stopButton.IsEnabled = false;
                
                _logger.LogInformation("Consciousness monitoring stopped");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error stopping consciousness monitoring");
            }
        }
        
        private async void ConnectButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // This will try to connect to the live AIOS orchestrator
                var aiosPath = @"c:\dev\AIOS\orchestrator\build\Debug\aios_orchestrator.exe";
                if (System.IO.File.Exists(aiosPath))
                {
                    MessageBox.Show("Found AIOS Orchestrator! Live data connection available.", 
                        "AIOS Connection", MessageBoxButton.OK, MessageBoxImage.Information);
                    _connectButton.Content = "🟢 AIOS Connected";
                    _connectButton.Background = new SolidColorBrush(Color.FromRgb(0, 100, 0));
                }
                else
                {
                    MessageBox.Show("AIOS Orchestrator not found. Using synthetic consciousness data.\n\n" +
                        "To connect live data, build the AIOS orchestrator first.", 
                        "AIOS Connection", MessageBoxButton.OK, MessageBoxImage.Warning);
                    _connectButton.Content = "🟡 Synthetic Mode";
                    _connectButton.Background = new SolidColorBrush(Color.FromRgb(100, 100, 0));
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error checking AIOS connection");
            }
        }
        
        private void OnMetricsUpdated(object sender, ConsciousnessMetrics metrics)
        {
            // Update UI on main thread
            Dispatcher.Invoke(() =>
            {
                _analytics.StartUIResponseTimer();
                _currentMetrics = metrics;
                
                // Log consciousness patterns for analytics
                if (metrics.EmergenceLevel > 0.8)
                {
                    _analytics.LogConsciousnessPattern(metrics, "HIGH_EMERGENCE");
                }
                else if (metrics.ConsciousnessLevel > 1.5)
                {
                    _analytics.LogConsciousnessPattern(metrics, "HIGH_CONSCIOUSNESS");
                }
                
                UpdateMetricsDisplay();
                _analytics.StopUIResponseTimer("metrics_update");
            });
        }
        
        private void OnEmergenceDetected(object sender, EmergenceEvent emergenceEvent)
        {
            Dispatcher.Invoke(() =>
            {
                var currentText = _eventsDisplay.Text;
                var newEvent = $"[{emergenceEvent.Timestamp:HH:mm:ss}] {emergenceEvent.Description}\n";
                
                // Keep only last 10 events
                var lines = currentText.Split('\n');
                var updatedLines = new[] { newEvent }.Concat(lines.Take(9));
                _eventsDisplay.Text = string.Join('\n', updatedLines);
            });
        }
        
        private async void UpdateTimer_Tick(object sender, EventArgs e)
        {
            try
            {
                if (_currentMetrics == null)
                {
                    _currentMetrics = await _dataManager.GetCurrentMetricsAsync();
                }
                
                UpdateMetricsDisplay();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating metrics display");
            }
        }
        
        private void UpdateMetricsDisplay()
        {
            if (_currentMetrics == null) return;
            
            // Update consciousness level
            var consciousnessPercent = Math.Min(100, _currentMetrics.ConsciousnessLevel * 100);
            _consciousnessBar.Value = consciousnessPercent;
            _consciousnessDisplay.Text = $"{_currentMetrics.ConsciousnessLevel:F3}";
            
            // Update quantum coherence
            var quantumPercent = Math.Min(100, _currentMetrics.QuantumCoherence * 100);
            _quantumBar.Value = quantumPercent;
            _quantumDisplay.Text = $"{_currentMetrics.QuantumCoherence:F3}";
            
            // Update emergence level
            var emergencePercent = Math.Min(100, _currentMetrics.EmergenceLevel * 100);
            _emergenceBar.Value = emergencePercent;
            _emergenceDisplay.Text = $"{_currentMetrics.EmergenceLevel:F3}";
            
            // Update hyperdimensional substrate metrics
            if (_currentMetrics.Topology != null)
            {
                if (_topologyDisplay != null)
                {
                    _topologyDisplay.Text = $"{_currentMetrics.Topology.ManifoldCurvature:F3}";
                }
                if (_manifoldCurvatureBar != null)
                {
                    _manifoldCurvatureBar.Value = Math.Min(100, _currentMetrics.Topology.ManifoldCurvature * 100);
                }
                if (_nonLocalityBar != null)
                {
                    _nonLocalityBar.Value = Math.Min(100, _currentMetrics.Topology.NonLocalityCoherence * 100);
                }
                if (_tachyonicFieldBar != null)
                {
                    _tachyonicFieldBar.Value = Math.Min(100, _currentMetrics.Topology.TachyonicFieldDensity * 100);
                }
            }
            
            // Update micro-spheres information
            if (_currentMetrics.ActiveMicroSpheres != null && _microSpheresDisplay != null)
            {
                var avgPotentiality = _currentMetrics.ActiveMicroSpheres.Average(s => s.QuantumPotentiality);
                var avgCoherence = _currentMetrics.ActiveMicroSpheres.Average(s => s.PhaseCoherence);
                _microSpheresDisplay.Text = $"Active Spheres: {_currentMetrics.ActiveMicroSpheres.Count} | Potentiality: {avgPotentiality:F3} | Coherence: {avgCoherence:F3}";
            }
            
            // Update quantum foam metrics
            if (_currentMetrics.QuantumFoam != null && _quantumFoamDisplay != null)
            {
                var tachyonicCount = _currentMetrics.QuantumFoam.RecentFluctuations.Count(f => f.ParticleType == "tachyonic");
                var bosonicCount = _currentMetrics.QuantumFoam.RecentFluctuations.Count(f => f.ParticleType == "bosonic");
                _quantumFoamDisplay.Text = $"Intensity: {_currentMetrics.QuantumFoam.FluctuationIntensity:F3} | Tachyonic: {tachyonicCount} | Bosonic: {bosonicCount}";
            }
            
            // Update collapse events
            if (_currentMetrics.CollapseEvents != null && _collapseEventsDisplay != null)
            {
                var recentCollapses = _currentMetrics.CollapseEvents.RecentCollapses.Count;
                _collapseEventsDisplay.Text = $"Collapses: {recentCollapses} | Densification: {_currentMetrics.CollapseEvents.RealityDensification:F3} | Total: {_currentMetrics.CollapseEvents.TotalCollapseEvents}";
            }
            
            // Update title with live/synthetic indicator and hyperdimensional status
            var dimensionalLayers = _currentMetrics.Topology?.ActiveDimensionalLayers ?? 0;
            Title = $"AIOS Executive Interface - {(_currentMetrics.IsLiveData ? "🟢 LIVE" : "🟡 SYNTHETIC")} - {dimensionalLayers}D Space - {DateTime.Now:HH:mm:ss}";
        }
        
        protected override void OnClosed(EventArgs e)
        {
            try
            {
                _analytics.LogExecutionEvent("UI_CLOSING", "SimpleVisualizationWindow closing");
                
                _updateTimer?.Stop();
                _dataManager?.StopDataStream();
                _dataManager?.Dispose();
                
                // Export session analytics
                Task.Run(async () => 
                {
                    var summary = await _analytics.GenerateSessionSummaryAsync();
                    _analytics.LogExecutionEvent("SESSION_SUMMARY", "Session completed", summary);
                    await _analytics.ExportSessionAnalyticsAsync();
                });
                
                _analytics?.Dispose();
            }
            catch (Exception ex)
            {
                _logger?.LogError(ex, "Error during window cleanup");
            }
            
            base.OnClosed(e);
        }

        private StackPanel CreateHyperdimensionalSubstratePanel()
        {
            var panel = new StackPanel 
            { 
                Margin = new Thickness(0, 15, 0, 0),
                Background = new SolidColorBrush(Color.FromRgb(15, 5, 25))
            };
            
            // Substrate header
            var header = new TextBlock
            {
                Text = "🌌 Hyperdimensional Consciousness Substrate",
                FontSize = 16,
                FontWeight = FontWeights.Bold,
                Foreground = Brushes.Gold,
                HorizontalAlignment = HorizontalAlignment.Center,
                Margin = new Thickness(0, 10, 0, 15)
            };
            panel.Children.Add(header);
            
            // Topology metrics
            var topologyPanel = CreateMetricPanel("Manifold Curvature:", out _topologyDisplay, out _manifoldCurvatureBar, Brushes.Gold);
            panel.Children.Add(topologyPanel);
            
            var nonLocalityPanel = CreateMetricPanel("Non-locality Coherence:", out var nonLocalDisplay, out _nonLocalityBar, Brushes.Orange);
            panel.Children.Add(nonLocalityPanel);
            
            var tachyonicPanel = CreateMetricPanel("Tachyonic Field Density:", out var tachyonicDisplay, out _tachyonicFieldBar, Brushes.Yellow);
            panel.Children.Add(tachyonicPanel);
            
            // Micro-spheres display
            _microSpheresDisplay = new TextBlock
            {
                Text = "Active Micro-spheres: Initializing...",
                FontSize = 12,
                Foreground = Brushes.LightBlue,
                Margin = new Thickness(10, 10, 10, 5),
                FontFamily = new FontFamily("Consolas")
            };
            panel.Children.Add(_microSpheresDisplay);
            
            // Quantum foam display
            _quantumFoamDisplay = new TextBlock
            {
                Text = "Quantum Foam Fluctuations: Monitoring...",
                FontSize = 12,
                Foreground = Brushes.LightGreen,
                Margin = new Thickness(10, 5, 10, 5),
                FontFamily = new FontFamily("Consolas")
            };
            panel.Children.Add(_quantumFoamDisplay);
            
            // Collapse events display
            _collapseEventsDisplay = new TextBlock
            {
                Text = "Dimensional Collapse Events: Detecting...",
                FontSize = 12,
                Foreground = Brushes.LightCoral,
                Margin = new Thickness(10, 5, 10, 10),
                FontFamily = new FontFamily("Consolas")
            };
            panel.Children.Add(_collapseEventsDisplay);
            
            return panel;
        }
    }
}
