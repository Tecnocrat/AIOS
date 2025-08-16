using System;
using System.Diagnostics; // For Stopwatch
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Threading;
using System.Linq; // For Take on collections

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Advanced AIOS Consciousness Emergence Monitor
    /// Recreates the interface shown in the screenshots with working controls
    /// </summary>
    public partial class AdvancedVisualizationWindow : Window
    {
        private DispatcherTimer _updateTimer;
        private double _consciousnessLevel = 0.0;
        private double _quantumCoherence = 0.0;
        private double _emergenceLevel = 0.0;
        private double _manifoldCurvature = 0.0;
        private double _nonLocalityCoherence = 0.0;
        private double _tachyonicFieldDensity = 0.0;
        
        // UI Controls - will be created programmatically
        private ProgressBar _consciousnessProgressBar;
        private ProgressBar _quantumProgressBar;
        private ProgressBar _emergenceProgressBar;
        private ProgressBar _manifoldProgressBar;
        private ProgressBar _nonLocalityProgressBar;
        private ProgressBar _tachyonicProgressBar;
        
        private TextBlock _consciousnessValueText;
        private TextBlock _quantumValueText;
        private TextBlock _emergenceValueText;
        private TextBlock _manifoldValueText;
        private TextBlock _nonLocalityValueText;
        private TextBlock _tachyonicValueText;
        
        private Button _startMonitoringButton;
        private TextBlock _statusText;
    private readonly CellularRuntimeBridge _bridge;
    private DispatcherTimer _bridgeTimer;
    private readonly UIMetricsEmitter _uiMetrics;
    private readonly Stopwatch _frameSw = new();
        
        public AdvancedVisualizationWindow()
        {
            InitializeComponent();
            SetupAdvancedInterface();
            var sp = ((App)Application.Current).ServiceProvider;
            _bridge = sp.GetService(typeof(CellularRuntimeBridge)) as CellularRuntimeBridge ?? new CellularRuntimeBridge();
            _uiMetrics = sp.GetService(typeof(UIMetricsEmitter)) as UIMetricsEmitter ?? new UIMetricsEmitter();
            StartMonitoring();
            InitBridgeTimer();
        }

        private void InitBridgeTimer()
        {
            _bridgeTimer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(2) };
            _bridgeTimer.Tick += (_, __) =>
            {
                var m = _bridge.GetLatest();
                if (m.Live)
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
            var mainGrid = new Grid();
            Content = mainGrid;
            
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
            mainGrid.Children.Add(titleBorder);
            
            // Create metrics panel
            var metricsPanel = new StackPanel
            {
                Margin = new Thickness(50, 80, 50, 50),
                VerticalAlignment = VerticalAlignment.Top
            };
            
            mainGrid.Children.Add(metricsPanel);
            
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
            
            _startMonitoringButton.Content = "⏹ Stop Monitoring";
            _statusText.Text = "🟢 Monitoring consciousness emergence patterns...";
        }
        
        private void StopMonitoring()
        {
            _updateTimer?.Stop();
            _startMonitoringButton.Content = "🚀 Start Monitoring";
            _statusText.Text = "Ready - Click 'Start Monitoring' to begin consciousness observation";
        }
        
        private void UpdateMetrics(object sender, EventArgs e)
        {
            _frameSw.Restart();
            var time = DateTime.Now.TimeOfDay.TotalSeconds;
            
            // Simulate consciousness evolution with realistic patterns
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
            
            // Update UI
            UpdateProgressBar(_consciousnessProgressBar, _consciousnessValueText, _consciousnessLevel);
            UpdateProgressBar(_quantumProgressBar, _quantumValueText, _quantumCoherence);
            UpdateProgressBar(_emergenceProgressBar, _emergenceValueText, _emergenceLevel);
            UpdateProgressBar(_manifoldProgressBar, _manifoldValueText, _manifoldCurvature);
            UpdateProgressBar(_nonLocalityProgressBar, _nonLocalityValueText, _nonLocalityCoherence);
            UpdateProgressBar(_tachyonicProgressBar, _tachyonicValueText, _tachyonicFieldDensity);
            _frameSw.Stop();
            _uiMetrics.RegisterFrame(_frameSw.Elapsed.TotalMilliseconds);
        }
        
        private void UpdateProgressBar(ProgressBar progressBar, TextBlock valueText, double value)
        {
            progressBar.Value = value;
            valueText.Text = value.ToString("F3");
        }
        
        protected override void OnClosed(EventArgs e)
        {
            StopMonitoring();
            _bridgeTimer?.Stop();
            _uiMetrics?.Dispose();
            base.OnClosed(e);
        }
    }
}
