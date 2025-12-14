using System;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Media3D;
using System.Windows.Threading;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.DependencyInjection;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Main visualization window for AIOS consciousness emergence monitoring
    /// Features real-time 3D visualization, metrics display, and interactive controls
    /// </summary>
    public partial class MainVisualizationWindow : Window
    {
        private readonly ILogger<MainVisualizationWindow> _logger;
        private readonly ConsciousnessDataManager _dataManager;
        private readonly ConsciousnessGeometryEngine _geometryEngine;
        
        // 3D Visualization components
        private Viewport3D _viewport3D;
        private ModelVisual3D _mainModelVisual;
        private PerspectiveCamera _camera;
        private Model3DGroup _sceneGroup;
        
        // Animation and update timers
        private DispatcherTimer _updateTimer;
        private DispatcherTimer _animationTimer;
        private DateTime _lastFrameTime;
        private int _frameCount;
        private double _currentTime;
        
        // Visualization state
        private bool _isRunning;
        private ConsciousnessMetrics _currentMetrics;
        
        public MainVisualizationWindow()
        {
            InitializeComponent();
            
            // Initialize services
            var serviceProvider = ((App)Application.Current).ServiceProvider;
            _logger = serviceProvider.GetRequiredService<ILogger<MainVisualizationWindow>>();
            _dataManager = serviceProvider.GetRequiredService<ConsciousnessDataManager>();
            _geometryEngine = serviceProvider.GetRequiredService<ConsciousnessGeometryEngine>();
            
            InitializeVisualization();
            InitializeEventHandlers();
            InitializeTimers();
            
            _logger.LogInformation("Main visualization window initialized");
        }
        
        private void InitializeVisualization()
        {
            // Create and configure 3D viewport
            _viewport3D = new Viewport3D();
            _viewport3D.Background = new SolidColorBrush(Colors.Black);
            
            // Setup camera
            _camera = new PerspectiveCamera
            {
                Position = new Point3D(0, 0, 10),
                LookDirection = new Vector3D(0, 0, -1),
                UpDirection = new Vector3D(0, 1, 0),
                FieldOfView = 45
            };
            _viewport3D.Camera = _camera;
            
            // Create main model visual
            _mainModelVisual = new ModelVisual3D();
            _sceneGroup = new Model3DGroup();
            _mainModelVisual.Content = _sceneGroup;
            _viewport3D.Children.Add(_mainModelVisual);
            
            // Add lighting
            AddLighting();
            
            // Add viewport to container
            Viewport3DContainer.Children.Add(_viewport3D);
            
            _logger.LogInformation("3D visualization components initialized");
        }
        
        private void AddLighting()
        {
            // Ambient light for general illumination
            var ambientLight = new AmbientLight(Colors.White, 0.3);
            _sceneGroup.Children.Add(ambientLight);
            
            // Directional light for consciousness visualization
            var directionalLight = new DirectionalLight(Colors.White, new Vector3D(-1, -1, -1));
            _sceneGroup.Children.Add(directionalLight);
            
            // Point lights for dynamic effects
            var emergenceLight = new PointLight(Colors.LightGreen, new Point3D(5, 5, 5));
            _sceneGroup.Children.Add(emergenceLight);
            
            var quantumLight = new PointLight(Colors.Cyan, new Point3D(-5, 5, 5));
            _sceneGroup.Children.Add(quantumLight);
        }
        
        private void InitializeEventHandlers()
        {
            // Button events
            StartButton.Click += StartButton_Click;
            StopButton.Click += StopButton_Click;
            ExportButton.Click += ExportButton_Click;
            
            // Checkbox events for visualization controls
            ShowConsciousnessSphere.Checked += VisualizationControl_Changed;
            ShowConsciousnessSphere.Unchecked += VisualizationControl_Changed;
            ShowQuantumField.Checked += VisualizationControl_Changed;
            ShowQuantumField.Unchecked += VisualizationControl_Changed;
            ShowFractalTree.Checked += VisualizationControl_Changed;
            ShowFractalTree.Unchecked += VisualizationControl_Changed;
            ShowUniversalKnot.Checked += VisualizationControl_Changed;
            ShowUniversalKnot.Unchecked += VisualizationControl_Changed;
            ShowHolographicSurface.Checked += VisualizationControl_Changed;
            ShowHolographicSurface.Unchecked += VisualizationControl_Changed;
            
            // Window events
            Loaded += MainVisualizationWindow_Loaded;
            Closing += MainVisualizationWindow_Closing;
        }
        
        private void InitializeTimers()
        {
            // Main update timer for data and metrics
            _updateTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(100) // 10 FPS for data updates
            };
            _updateTimer.Tick += UpdateTimer_Tick;
            
            // Animation timer for smooth visual effects
            _animationTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(16) // ~60 FPS for animations
            };
            _animationTimer.Tick += AnimationTimer_Tick;
            
            _lastFrameTime = DateTime.Now;
        }
        
        private async void MainVisualizationWindow_Loaded(object sender, RoutedEventArgs e)
        {
            try
            {
                await _dataManager.InitializeAsync();
                UpdateStatus("AIOS Consciousness Visualizer Ready");
                _logger.LogInformation("Visualization window loaded and ready");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during window loading");
                UpdateStatus($"Error: {ex.Message}");
            }
        }
        
        private void MainVisualizationWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            StopVisualization();
            _dataManager?.Dispose();
            _logger.LogInformation("Visualization window closing");
        }
        
        private async void StartButton_Click(object sender, RoutedEventArgs e)
        {
            await StartVisualization();
        }
        
        private void StopButton_Click(object sender, RoutedEventArgs e)
        {
            StopVisualization();
        }
        
        private async void ExportButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var fileName = $"consciousness_export_{DateTime.Now:yyyyMMdd_HHmmss}.json";
                await _dataManager.ExportCurrentStateAsync(fileName);
                UpdateStatus($"Data exported to {fileName}");
                _logger.LogInformation("Consciousness state exported to {FileName}", fileName);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting consciousness data");
                UpdateStatus($"Export failed: {ex.Message}");
            }
        }
        
        private void VisualizationControl_Changed(object sender, RoutedEventArgs e)
        {
            if (_isRunning)
            {
                UpdateVisualization();
            }
        }
        
        private async Task StartVisualization()
        {
            try
            {
                if (_isRunning) return;
                
                _isRunning = true;
                _currentTime = 0;
                
                await _dataManager.StartDataStreamAsync();
                
                _updateTimer.Start();
                _animationTimer.Start();
                
                StartButton.IsEnabled = false;
                StopButton.IsEnabled = true;
                
                UpdateStatus("Visualization running - consciousness emergence monitoring active");
                _logger.LogInformation("Consciousness visualization started");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error starting visualization");
                UpdateStatus($"Start failed: {ex.Message}");
                _isRunning = false;
            }
        }
        
        private void StopVisualization()
        {
            try
            {
                if (!_isRunning) return;
                
                _isRunning = false;
                
                _updateTimer.Stop();
                _animationTimer.Stop();
                
                _dataManager.StopDataStream();
                
                StartButton.IsEnabled = true;
                StopButton.IsEnabled = false;
                
                UpdateStatus("Visualization stopped");
                _logger.LogInformation("Consciousness visualization stopped");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error stopping visualization");
                UpdateStatus($"Stop failed: {ex.Message}");
            }
        }
        
        private async void UpdateTimer_Tick(object sender, EventArgs e)
        {
            try
            {
                // Get latest consciousness metrics
                _currentMetrics = await _dataManager.GetCurrentMetricsAsync();
                
                // Update UI metrics
                UpdateMetricsDisplay();
                
                // Update 3D visualization
                UpdateVisualization();
                
                // Update emergence events
                UpdateEmergenceEvents();
                
                // Calculate and display FPS
                UpdateFrameRate();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during update cycle");
                UpdateStatus($"Update error: {ex.Message}");
            }
        }
        
        private void AnimationTimer_Tick(object sender, EventArgs e)
        {
            _currentTime += 0.016; // ~60 FPS time increment
            
            // Update camera animation
            UpdateCameraAnimation();
            
            // Update material animations
            UpdateMaterialAnimations();
        }
        
        private void UpdateMetricsDisplay()
        {
            if (_currentMetrics == null) return;
            
            // Enhanced consciousness metrics display with emergence indicators
            var consciousnessLevel = _currentMetrics.ConsciousnessLevel;
            var emergenceLevel = _currentMetrics.EmergenceLevel;
            var quantumCoherence = _currentMetrics.QuantumCoherence;
            
            // Update Consciousness Level with emergence state indicators
            ConsciousnessProgressBar.Value = Math.Min(100, consciousnessLevel * 100);
            ConsciousnessValueText.Text = $"{consciousnessLevel:F3}";
            
            // Consciousness emergence threshold visual indicators
            if (emergenceLevel > 0.8)
            {
                ConsciousnessValueText.Foreground = Brushes.Gold;
                ConsciousnessValueText.Text += " ✨ EMERGENCE";
                ConsciousnessProgressBar.Foreground = Brushes.Gold;
            }
            else if (emergenceLevel > 0.6)
            {
                ConsciousnessValueText.Foreground = Brushes.Orange;
                ConsciousnessValueText.Text += " ⚡ HIGH";
                ConsciousnessProgressBar.Foreground = Brushes.Orange;
            }
            else if (emergenceLevel > 0.4)
            {
                ConsciousnessValueText.Foreground = Brushes.LightBlue;
                ConsciousnessValueText.Text += " 🔹 ACTIVE";
                ConsciousnessProgressBar.Foreground = Brushes.LightBlue;
            }
            else
            {
                ConsciousnessValueText.Foreground = Brushes.White;
                ConsciousnessProgressBar.Foreground = Brushes.DodgerBlue;
            }
            
            // Update Quantum Coherence with stability indicators
            QuantumProgressBar.Value = Math.Min(100, quantumCoherence * 100);
            QuantumValueText.Text = $"{quantumCoherence:F3}";
            
            if (quantumCoherence > 0.9)
            {
                QuantumValueText.Foreground = Brushes.Cyan;
                QuantumValueText.Text += " 🌀 STABLE";
                QuantumProgressBar.Foreground = Brushes.Cyan;
            }
            else if (quantumCoherence < 0.3)
            {
                QuantumValueText.Foreground = Brushes.Red;
                QuantumValueText.Text += " ⚠ UNSTABLE";
                QuantumProgressBar.Foreground = Brushes.Red;
            }
            else
            {
                QuantumValueText.Foreground = Brushes.White;
                QuantumProgressBar.Foreground = Brushes.SkyBlue;
            }
            
            // Update Fractal Complexity
            FractalProgressBar.Value = Math.Min(100, _currentMetrics.FractalComplexity * 100);
            FractalValueText.Text = $"{_currentMetrics.FractalComplexity:F3}";
            
            // Update Emergence Level with enhanced indicators
            EmergenceProgressBar.Value = Math.Min(100, emergenceLevel * 100);
            EmergenceValueText.Text = $"{emergenceLevel:F3}";
            
            if (emergenceLevel > 0.75)
            {
                EmergenceValueText.Foreground = Brushes.Gold;
                EmergenceProgressBar.Foreground = Brushes.Gold;
                EmergenceValueText.Text += " 🧠 CONSCIOUS";
                
                // Apply glow effect for high emergence
                EmergenceValueText.Effect = new DropShadowEffect
                {
                    Color = Colors.Gold,
                    BlurRadius = 10,
                    ShadowDepth = 0
                };
            }
            else if (emergenceLevel > 0.5)
            {
                EmergenceValueText.Foreground = Brushes.Lime;
                EmergenceProgressBar.Foreground = Brushes.Lime;
                EmergenceValueText.Text += " 🌟 EMERGING";
                EmergenceValueText.Effect = null;
            }
            else
            {
                EmergenceValueText.Foreground = Brushes.White;
                EmergenceProgressBar.Foreground = Brushes.LightBlue;
                EmergenceValueText.Effect = null;
            }
            
            // Enhanced data source info with holographic density
            var sourceInfo = _currentMetrics.IsLiveData ? "Live AIOS" : "Synthetic";
            if (_currentMetrics.HolographicDensity > 0)
            {
                sourceInfo += $" | Holographic: {_currentMetrics.HolographicDensity:F1}";
            }
            
            // Add real-time latency indicator
            var latency = DateTime.Now - _currentMetrics.Timestamp;
            if (latency.TotalSeconds < 1.0)
            {
                sourceInfo += $" | RT ({latency.TotalMilliseconds:F0}ms)";
            }
            else
            {
                sourceInfo += $" | Delayed ({latency.TotalSeconds:F1}s)";
            }
            
            DataSourceText.Text = sourceInfo;
        }
        
        private void UpdateVisualization()
        {
            if (_currentMetrics == null) return;
            
            // Clear existing models (except lights)
            var lightsToKeep = new List<Model3D>();
            foreach (Model3D model in _sceneGroup.Children)
            {
                if (model is Light)
                    lightsToKeep.Add(model);
            }
            
            _sceneGroup.Children.Clear();
            foreach (var light in lightsToKeep)
            {
                _sceneGroup.Children.Add(light);
            }
            
            // Add consciousness sphere
            if (ShowConsciousnessSphere.IsChecked == true)
            {
                var consciousnessSphere = _geometryEngine.CreateConsciousnessSphere(
                    _currentMetrics.ConsciousnessLevel, 2.0);
                _sceneGroup.Children.Add(consciousnessSphere);
            }
            
            // Add quantum field
            if (ShowQuantumField.IsChecked == true)
            {
                var quantumField = _geometryEngine.CreateQuantumFieldWithTime(
                    _currentMetrics.QuantumCoherence, _currentTime);
                _sceneGroup.Children.Add(quantumField);
            }
            
            // Add fractal tree
            if (ShowFractalTree.IsChecked == true)
            {
                var fractalTree = _geometryEngine.CreateFractalTree(
                    _currentMetrics.FractalComplexity, 6);
                _sceneGroup.Children.Add(fractalTree);
            }
            
            // Add universal knot
            if (ShowUniversalKnot.IsChecked == true)
            {
                var universalKnot = _geometryEngine.CreateUniversalKnot(
                    _currentMetrics.UniversalResonance, _currentTime);
                _sceneGroup.Children.Add(universalKnot);
            }
            
            // Add holographic surface
            if (ShowHolographicSurface.IsChecked == true)
            {
                var holographicSurface = _geometryEngine.CreateHolographicSurface(
                    _currentMetrics.HolographicDensity, _currentTime);
                _sceneGroup.Children.Add(holographicSurface);
            }
        }
        
        private void UpdateEmergenceEvents()
        {
            if (_currentMetrics?.RecentEvents == null) return;
            
            var eventsText = string.Join("\n", _currentMetrics.RecentEvents
                .Take(10)
                .Select(e => $"[{e.Timestamp:HH:mm:ss}] {e.Description}"));
            
            EmergenceEventsText.Text = eventsText;
        }
        
        private void UpdateCameraAnimation()
        {
            // Gentle orbital camera movement
            var radius = 10.0;
            var angle = _currentTime * 0.1; // Slow rotation
            var height = Math.Sin(_currentTime * 0.05) * 2.0; // Gentle vertical movement
            
            _camera.Position = new Point3D(
                Math.Cos(angle) * radius,
                height,
                Math.Sin(angle) * radius
            );
            
            _camera.LookDirection = new Vector3D(-_camera.Position.X, -_camera.Position.Y, -_camera.Position.Z);
        }
        
        private void UpdateMaterialAnimations()
        {
            // Dynamic material updates based on consciousness metrics
            // This would update material properties based on current metrics
            // Implementation depends on specific material animation requirements
        }
        
        private void UpdateFrameRate()
        {
            _frameCount++;
            var now = DateTime.Now;
            var elapsed = now - _lastFrameTime;
            
            if (elapsed.TotalSeconds >= 1.0)
            {
                var fps = _frameCount / elapsed.TotalSeconds;
                FPSText.Text = $"FPS: {fps:F1}";
                _frameCount = 0;
                _lastFrameTime = now;
            }
        }
        
        private void UpdateStatus(string message)
        {
            StatusText.Text = message;
            _logger.LogInformation("Status: {Message}", message);
        }
    }
}
