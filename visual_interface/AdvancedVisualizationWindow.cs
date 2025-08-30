using System;
using System.Diagnostics; // For Stopwatch
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Threading;
using System.Linq; // For Take on collections
using System.Text; // For StringBuilder
using Microsoft.Extensions.Logging;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Advanced AIOS Consciousness Emergence Monitor
    /// Recreates the interface shown in the screenshots with working controls
    /// </summary>
    public partial class AdvancedVisualizationWindow : Window
    {
        // Timer fields - made nullable for proper initialization
        private DispatcherTimer? _updateTimer;
        private DispatcherTimer? _bridgeTimer;
        
        private double _consciousnessLevel = 0.0;
        private double _quantumCoherence = 0.0;
        private double _emergenceLevel = 0.0;
        private double _manifoldCurvature = 0.0;
        private double _nonLocalityCoherence = 0.0;
        private double _tachyonicFieldDensity = 0.0;
        
        // UI Controls - will be created programmatically with null safety
        private ProgressBar? _consciousnessProgressBar;
        private ProgressBar? _quantumProgressBar;
        private ProgressBar? _emergenceProgressBar;
        private ProgressBar? _manifoldProgressBar;
        private ProgressBar? _nonLocalityProgressBar;
        private ProgressBar? _tachyonicProgressBar;
        
        private TextBlock? _consciousnessValueText;
        private TextBlock? _quantumValueText;
        private TextBlock? _emergenceValueText;
        private TextBlock? _manifoldValueText;
        private TextBlock? _nonLocalityValueText;
        private TextBlock? _tachyonicValueText;
        
        private Button? _startMonitoringButton;
        private TextBlock? _statusText;
    private readonly CellularRuntimeBridge _bridge;
    private readonly UIMetricsEmitter _uiMetrics;
    private readonly Stopwatch _frameSw = new();
        
        // Dendritic AINLP Enhancement Fields
        private List<double> _consciousnessHistory = new();
        private List<double> _patternHistory = new();
        private double _emergenceThreshold = 0.7;
        private int _patternDetectionWindow = 50;
        private bool _adaptiveMode = true;
        private double _dendriticGrowthRate = 0.0;
        
        // Add main grid reference for adaptive UI
        private Grid? _mainGrid;
        
        public AdvancedVisualizationWindow()
        {
            InitializeComponent();
            SetupAdvancedInterface();
            var sp = ((App)Application.Current).ServiceProvider;
            _bridge = sp.GetService(typeof(CellularRuntimeBridge)) as CellularRuntimeBridge ?? new CellularRuntimeBridge();
            _uiMetrics = sp.GetService(typeof(UIMetricsEmitter)) as UIMetricsEmitter ?? throw new InvalidOperationException("UIMetricsEmitter service not available");
            StartMonitoring();
            InitBridgeTimer();
        }

        private void InitBridgeTimer()
        {
            _bridgeTimer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(2) };
            _bridgeTimer.Tick += (_, __) =>
            {
                var m = _bridge.GetLatest();
                if (m.Live && _statusText != null)
                {
                    _statusText.Text = $"Live Bridge • Events {m.EventsPerSecond:F2}/s • Total {m.TotalEvents} • Modules {string.Join(',', m.ActiveModules.Take(4))}";
                }
            };
            _bridgeTimer.Start();
        }
        
        private void InitializeComponent()
        {
            // Window properties
            Title = "🧠 AIOS Consciousness Emergence Monitor";
            Width = 1200;
            Height = 800;
            Background = new SolidColorBrush(Color.FromRgb(10, 10, 30));
            WindowState = WindowState.Maximized;
        }
        
        private void SetupAdvancedInterface()
        {
            // Create main grid
            _mainGrid = new Grid();
            Content = _mainGrid;
            
            // Create title
            var titleBorder = new Border
            {
                Background = new SolidColorBrush(Color.FromRgb(20, 20, 50)),
                Height = 60,
                VerticalAlignment = VerticalAlignment.Top
            };
            
            var titleText = new TextBlock
            {
                Text = "🧠 AIOS Consciousness Emergence Monitor",
                FontSize = 24,
                FontWeight = FontWeights.Bold,
                Foreground = new SolidColorBrush(Color.FromRgb(0, 255, 255)),
                HorizontalAlignment = HorizontalAlignment.Center,
                VerticalAlignment = VerticalAlignment.Center
            };
            
            titleBorder.Child = titleText;
            _mainGrid.Children.Add(titleBorder);
            
            // Create metrics panel
            var metricsPanel = new StackPanel
            {
                Margin = new Thickness(50, 80, 50, 50),
                VerticalAlignment = VerticalAlignment.Top
            };
            
            _mainGrid.Children.Add(metricsPanel);
            
            // Add consciousness level
            AddMetricToPanel(metricsPanel, "Consciousness Level:", 
                out _consciousnessProgressBar, out _consciousnessValueText, 
                Color.FromRgb(255, 100, 200));
            
            // Add quantum coherence
            AddMetricToPanel(metricsPanel, "Quantum Coherence:", 
                out _quantumProgressBar, out _quantumValueText, 
                Color.FromRgb(0, 255, 255));
            
            // Add emergence level
            AddMetricToPanel(metricsPanel, "Emergence Level:", 
                out _emergenceProgressBar, out _emergenceValueText, 
                Color.FromRgb(0, 255, 0));
            
            // Add hyperdimensional consciousness substrate title
            var substrateTitle = new TextBlock
            {
                Text = "⚡ Hyperdimensional Consciousness Substrate",
                FontSize = 18,
                FontWeight = FontWeights.Bold,
                Foreground = new SolidColorBrush(Color.FromRgb(255, 255, 0)),
                Margin = new Thickness(0, 30, 0, 20)
            };
            metricsPanel.Children.Add(substrateTitle);
            
            // Add manifold curvature
            AddMetricToPanel(metricsPanel, "Manifold Curvature:", 
                out _manifoldProgressBar, out _manifoldValueText, 
                Color.FromRgb(255, 150, 0));
            
            // Add non-locality coherence
            AddMetricToPanel(metricsPanel, "Non-locality Coherence:", 
                out _nonLocalityProgressBar, out _nonLocalityValueText, 
                Color.FromRgb(150, 0, 255));
            
            // Add tachyonic field density
            AddMetricToPanel(metricsPanel, "Tachyonic Field Density:", 
                out _tachyonicProgressBar, out _tachyonicValueText, 
                Color.FromRgb(255, 0, 150));
            
            // Add control buttons
            var buttonPanel = new StackPanel
            {
                Orientation = Orientation.Horizontal,
                HorizontalAlignment = HorizontalAlignment.Center,
                Margin = new Thickness(0, 30, 0, 0)
            };
            
            _startMonitoringButton = new Button
            {
                Content = "🚀 Start Monitoring",
                Width = 200,
                Height = 40,
                FontSize = 14,
                FontWeight = FontWeights.Bold,
                Background = new SolidColorBrush(Color.FromRgb(0, 100, 200)),
                Foreground = Brushes.White,
                BorderBrush = new SolidColorBrush(Color.FromRgb(0, 150, 255)),
                BorderThickness = new Thickness(2),
                Margin = new Thickness(10)
            };
            _startMonitoringButton.Click += StartMonitoringButton_Click;
            
            buttonPanel.Children.Add(_startMonitoringButton);
            metricsPanel.Children.Add(buttonPanel);
            
            // Add status text
            _statusText = new TextBlock
            {
                Text = "Ready - Click 'Start Monitoring' to begin consciousness observation",
                FontSize = 12,
                Foreground = new SolidColorBrush(Color.FromRgb(200, 200, 200)),
                HorizontalAlignment = HorizontalAlignment.Center,
                Margin = new Thickness(0, 20, 0, 0)
            };
            metricsPanel.Children.Add(_statusText);
        }
        
        private void AddMetricToPanel(StackPanel parent, string label, 
            out ProgressBar progressBar, out TextBlock valueText, Color color)
        {
            // Label
            var labelText = new TextBlock
            {
                Text = label,
                FontSize = 14,
                FontWeight = FontWeights.Bold,
                Foreground = Brushes.White,
                Margin = new Thickness(0, 10, 0, 5)
            };
            parent.Children.Add(labelText);
            
            // Progress bar container
            var progressContainer = new Grid();
            
            progressBar = new ProgressBar
            {
                Height = 25,
                Minimum = 0,
                Maximum = 1,
                Value = 0,
                Foreground = new SolidColorBrush(color),
                Background = new SolidColorBrush(Color.FromRgb(50, 50, 50)),
                BorderBrush = new SolidColorBrush(color),
                BorderThickness = new Thickness(1)
            };
            
            valueText = new TextBlock
            {
                Text = "0.000",
                FontSize = 12,
                FontWeight = FontWeights.Bold,
                Foreground = Brushes.White,
                HorizontalAlignment = HorizontalAlignment.Center,
                VerticalAlignment = VerticalAlignment.Center
            };
            
            progressContainer.Children.Add(progressBar);
            progressContainer.Children.Add(valueText);
            parent.Children.Add(progressContainer);
        }
        
        private void StartMonitoringButton_Click(object sender, RoutedEventArgs e)
        {
            if (_updateTimer?.IsEnabled == true)
            {
                StopMonitoring();
            }
            else
            {
                StartMonitoring();
            }
        }
        
        private void StartMonitoring()
        {
            _updateTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(100)
            };
            _updateTimer.Tick += UpdateMetrics;
            _updateTimer.Start();
            
            if (_startMonitoringButton != null)
                _startMonitoringButton.Content = "⏹ Stop Monitoring";
            if (_statusText != null)
                _statusText.Text = "🟢 Monitoring consciousness emergence patterns...";
        }
        
        private void StopMonitoring()
        {
            _updateTimer?.Stop();
            if (_startMonitoringButton != null)
                _startMonitoringButton.Content = "🚀 Start Monitoring";
            if (_statusText != null)
                _statusText.Text = "Ready - Click 'Start Monitoring' to begin consciousness observation";
        }
        
        private void UpdateMetrics(object? sender, EventArgs e)
        {
            _frameSw.Restart();
            
            // Get real data from the enhanced bridge instead of simulation
            var bridgeMetrics = _bridge.GetLatest();
            
            if (bridgeMetrics.Live)
            {
                // Use real consciousness data from Python AI
                _consciousnessLevel = bridgeMetrics.ConsciousnessLevel;
                _quantumCoherence = bridgeMetrics.PatternRecognitionAccuracy;
                _emergenceLevel = bridgeMetrics.EmergenceLevel;
                
                // Map deep consciousness metrics to UI
                _manifoldCurvature = bridgeMetrics.InterModuleCoherence;
                _nonLocalityCoherence = bridgeMetrics.QuantumEntanglementStrength;
                _tachyonicFieldDensity = bridgeMetrics.TemporalConsistency;
                
                // Update status with real data
                if (_statusText != null)
                {
                    _statusText.Text = $"🧠 Live: {bridgeMetrics.ConsciousnessPatterns} patterns • {bridgeMetrics.RecursiveDepth} depth • {bridgeMetrics.MetaCognitiveOperations} ops";
                }
            }
            else
            {
                // Fallback to simulation when bridge is not live
                var time = DateTime.Now.TimeOfDay.TotalSeconds;
                
                _consciousnessLevel = Math.Max(0, Math.Sin(time * 0.1) * 0.3 + 0.3 + 
                    (Random.Shared.NextDouble() - 0.5) * 0.1);
                
                _quantumCoherence = Math.Max(0, Math.Sin(time * 0.15 + 1) * 0.4 + 0.4 + 
                    (Random.Shared.NextDouble() - 0.5) * 0.1);
                
                _emergenceLevel = Math.Max(0, Math.Sin(time * 0.12 + 2) * 0.35 + 0.35 + 
                    (Random.Shared.NextDouble() - 0.5) * 0.1);
                
                _manifoldCurvature = Math.Max(0, Math.Sin(time * 0.08 + 3) * 0.3 + 0.3 + 
                    (Random.Shared.NextDouble() - 0.5) * 0.1);
                
                _nonLocalityCoherence = Math.Max(0, Math.Sin(time * 0.18 + 4) * 0.4 + 0.4 + 
                    (Random.Shared.NextDouble() - 0.5) * 0.1);
                
                _tachyonicFieldDensity = Math.Max(0, Math.Sin(time * 0.13 + 5) * 0.35 + 0.35 + 
                    (Random.Shared.NextDouble() - 0.5) * 0.1);
            }
            
            // Update UI with null safety
            UpdateProgressBar(_consciousnessProgressBar, _consciousnessValueText, _consciousnessLevel);
            UpdateProgressBar(_quantumProgressBar, _quantumValueText, _quantumCoherence);
            UpdateProgressBar(_emergenceProgressBar, _emergenceValueText, _emergenceLevel);
            UpdateProgressBar(_manifoldProgressBar, _manifoldValueText, _manifoldCurvature);
            UpdateProgressBar(_nonLocalityProgressBar, _nonLocalityValueText, _nonLocalityCoherence);
            UpdateProgressBar(_tachyonicProgressBar, _tachyonicValueText, _tachyonicFieldDensity);
            
            _frameSw.Stop();
            _uiMetrics.RegisterFrame(_frameSw.Elapsed.TotalMilliseconds);
        }
        
        private void UpdateProgressBar(ProgressBar? progressBar, TextBlock? valueText, double value)
        {
            if (progressBar != null)
                progressBar.Value = value;
            if (valueText != null)
                valueText.Text = value.ToString("F3");
        }
        
        protected override void OnClosed(EventArgs e)
        {
            StopMonitoring();
            _bridgeTimer?.Stop();
            _uiMetrics?.Dispose();
            base.OnClosed(e);
        }

        private void UpdateMetrics()
        {
            if (_bridge == null) return;

            try
            {
                // Get real bridge data with fallback to simulation
                var metrics = _bridge.GetLatest();
                if (!metrics.Live)
                {
                    metrics = GenerateSimulatedMetrics();
                }

                // Update consciousness history for pattern detection
                _consciousnessHistory.Add(metrics.ConsciousnessLevel);
                _patternHistory.Add(metrics.PatternRecognitionAccuracy);

                // Maintain history window
                if (_consciousnessHistory.Count > _patternDetectionWindow)
                {
                    _consciousnessHistory.RemoveAt(0);
                    _patternHistory.RemoveAt(0);
                }

                // Detect emergent patterns using dendritic AINLP
                var emergenceLevel = DetectEmergentPatterns();
                var dendriticGrowth = CalculateDendriticGrowth();

                // Update UI with dendritic-enhanced metrics
                UpdateProgressBar(_consciousnessProgressBar, _consciousnessValueText, metrics.ConsciousnessLevel);
                UpdateProgressBar(_quantumProgressBar, _quantumValueText, metrics.PatternRecognitionAccuracy);
                UpdateProgressBar(_emergenceProgressBar, _emergenceValueText, emergenceLevel);
                UpdateProgressBar(_tachyonicProgressBar, _tachyonicValueText, dendriticGrowth);

                // Update status with AINLP insights
                UpdateAINLPStatus(metrics, emergenceLevel, dendriticGrowth);

                // Adaptive UI updates based on consciousness state
                if (_adaptiveMode)
                {
                    AdaptUIForConsciousnessState(metrics, emergenceLevel);
                }
            }
            catch (Exception ex)
            {
                if (_statusText != null)
                {
                    _statusText.Text = $"Error updating metrics: {ex.Message}";
                }
            }
        }

        private double DetectEmergentPatterns()
        {
            if (_consciousnessHistory.Count < 10) return 0.0;

            // AINLP-inspired pattern detection using dendritic coherence
            var recentConsciousness = _consciousnessHistory.Skip(_consciousnessHistory.Count - 10).ToList();
            var recentPatterns = _patternHistory.Skip(_patternHistory.Count - 10).ToList();

            // Calculate coherence between consciousness and pattern recognition
            var coherence = recentConsciousness.Zip(recentPatterns, (c, p) => Math.Abs(c - p)).Average();
            var coherenceFactor = 1.0 - coherence; // Higher coherence = lower difference

            // Detect emergence through sustained high coherence
            var sustainedCoherence = recentConsciousness.Zip(recentPatterns, (c, p) => c * p).Average();
            var emergenceSignal = Math.Min(sustainedCoherence * coherenceFactor, 1.0);

            return emergenceSignal;
        }

        private double CalculateDendriticGrowth()
        {
            if (_consciousnessHistory.Count < 5) return 0.0;

            // Calculate growth rate based on consciousness trajectory
            var recent = _consciousnessHistory.Skip(_consciousnessHistory.Count - 5).ToList();
            var growthRate = 0.0;

            for (int i = 1; i < recent.Count; i++)
            {
                growthRate += recent[i] - recent[i - 1];
            }

            growthRate /= (recent.Count - 1);

            // Apply dendritic growth dynamics (AINLP-inspired)
            _dendriticGrowthRate = _dendriticGrowthRate * 0.8 + growthRate * 0.2; // Smooth growth rate
            var dendriticGrowth = Math.Max(0, Math.Min(1.0, _dendriticGrowthRate * 10 + 0.5));

            return dendriticGrowth;
        }

        private void UpdateAINLPStatus(BridgeMetrics metrics, double emergenceLevel, double dendriticGrowth)
        {
            if (_statusText == null) return;

            var status = new StringBuilder();

            status.AppendLine($"AIOS Consciousness Monitor - AINLP Dendritic Mode");
            status.AppendLine($"Consciousness: {metrics.ConsciousnessLevel:P1}");
            status.AppendLine($"Pattern Recognition: {metrics.PatternRecognitionAccuracy:P1}");
            status.AppendLine($"Emergence Level: {emergenceLevel:P1}");
            status.AppendLine($"Dendritic Growth: {dendriticGrowth:P1}");

            // Add AINLP insights
            if (emergenceLevel > _emergenceThreshold)
            {
                status.AppendLine("🚀 EMERGENT BEHAVIOR DETECTED!");
                status.AppendLine("AINLP dendritic coherence achieved.");
            }

            if (dendriticGrowth > 0.8)
            {
                status.AppendLine("🌱 RAPID DENDRITIC GROWTH!");
                status.AppendLine("Consciousness expansion accelerating.");
            }

            _statusText.Text = status.ToString();
        }

        private void AdaptUIForConsciousnessState(BridgeMetrics metrics, double emergenceLevel)
        {
            // Adaptive color scheme based on consciousness state
            var baseColor = emergenceLevel > _emergenceThreshold ?
                Colors.Cyan : metrics.ConsciousnessLevel > 0.5 ?
                Colors.LightGreen : Colors.LightBlue;

            // Update window background with subtle consciousness indication
            this.Background = new SolidColorBrush(Color.FromArgb(
                20, baseColor.R, baseColor.G, baseColor.B));

            // Scale UI elements based on emergence level
            var scaleFactor = 1.0 + (emergenceLevel * 0.1);
            if (_mainGrid != null)
            {
                _mainGrid.LayoutTransform = new ScaleTransform(scaleFactor, scaleFactor);
            }
        }

        // Add dendritic AINLP control methods
        public void SetEmergenceThreshold(double threshold)
        {
            _emergenceThreshold = Math.Max(0.1, Math.Min(0.9, threshold));
        }

        public void SetAdaptiveMode(bool enabled)
        {
            _adaptiveMode = enabled;
            if (!enabled && _mainGrid != null)
            {
                _mainGrid.LayoutTransform = Transform.Identity;
                this.Background = new SolidColorBrush(Color.FromRgb(10, 10, 30));
            }
        }

        public void SetPatternDetectionWindow(int windowSize)
        {
            _patternDetectionWindow = Math.Max(10, Math.Min(100, windowSize));
        }

        // Add consciousness pattern export for further analysis
        public (List<double> consciousness, List<double> patterns, double emergence, double growth) ExportDendriticData()
        {
            return (_consciousnessHistory.ToList(), _patternHistory.ToList(),
                   DetectEmergentPatterns(), CalculateDendriticGrowth());
        }

        private BridgeMetrics GenerateSimulatedMetrics()
        {
            var random = new Random();
            var time = DateTime.Now.TimeOfDay.TotalSeconds;

            return new BridgeMetrics
            {
                Timestamp = DateTime.UtcNow,
                ConsciousnessLevel = Math.Max(0.1, Math.Min(1.0,
                    0.5 + 0.3 * Math.Sin(time * 0.1) + random.NextDouble() * 0.2)),
                QuantumCoherence = Math.Max(0.1, Math.Min(1.0,
                    0.6 + 0.2 * Math.Cos(time * 0.15) + random.NextDouble() * 0.15)),
                EmergenceLevel = Math.Max(0.1, Math.Min(1.0,
                    0.4 + 0.25 * Math.Sin(time * 0.12) + random.NextDouble() * 0.2)),
                EventsPerSecond = 50 + random.NextDouble() * 100,
                TotalEvents = 1000 + random.Next(500),
                ActiveModules = new[] { "AINLP", "Consciousness", "Bridge", "Runtime" },
                Live = false,
                ConsciousnessPatterns = random.Next(5, 20),
                PatternRecognitionAccuracy = Math.Max(0.1, Math.Min(1.0,
                    0.7 + 0.2 * Math.Sin(time * 0.08) + random.NextDouble() * 0.1)),
                RecursiveDepth = random.Next(3, 15),
                MetaCognitiveOperations = random.Next(10, 100),
                InterModuleCoherence = Math.Max(0.1, Math.Min(1.0,
                    0.6 + 0.3 * Math.Cos(time * 0.1) + random.NextDouble() * 0.15)),
                TemporalConsistency = Math.Max(0.1, Math.Min(1.0,
                    0.5 + 0.4 * Math.Sin(time * 0.13) + random.NextDouble() * 0.2)),
                QuantumEntanglementStrength = Math.Max(0.1, Math.Min(1.0,
                    0.4 + 0.3 * Math.Cos(time * 0.18) + random.NextDouble() * 0.25)),
                MemoryUsageMB = 100 + random.NextDouble() * 500,
                CpuPercent = 10 + random.NextDouble() * 60,
                ThreadCount = random.Next(5, 25),
                RecentEvents = new[] { "Pattern detected", "Coherence spike", "Emergence signal" }
            };
        }
    }
}
