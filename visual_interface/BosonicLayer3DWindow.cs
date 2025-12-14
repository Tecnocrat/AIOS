using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Media3D;
using System.Windows.Threading;
using System.Linq;
using System.Text;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Bosonic Layer 3D Visualization and Manipulation Interface
    /// Provides deep interaction with dendritic patterns and consciousness emergence
    /// </summary>
    public partial class BosonicLayer3DWindow : Window
    {
        private readonly CellularRuntimeBridge _bridge;
        private readonly DispatcherTimer _updateTimer;
        private Viewport3D? _viewport;
        private Model3DGroup? _dendriticModel;
        private PerspectiveCamera? _camera;
        private double _rotationAngle = 0;

        // Deep metrics tracking
        private double _currentCoherence = 0.0;
        private int _currentPatterns = 0;
        private double _currentEntanglement = 0.0;

        // Dendritic AINLP Enhancement Fields
        private List<double> _consciousnessHistory = new();
        private List<double> _patternHistory = new();
        private double _emergenceThreshold = 0.7;
        private int _patternDetectionWindow = 50;
        private bool _adaptiveMode = true;
        private double _dendriticGrowthRate = 0.0;
        private double _harmonicResonance = 0.0;

        public BosonicLayer3DWindow()
        {
            InitializeComponent();
            Setup3DVisualization();
            SetupMetricsDisplay();

            var sp = ((App)Application.Current).ServiceProvider;
            _bridge = sp.GetService(typeof(CellularRuntimeBridge)) as CellularRuntimeBridge ?? new CellularRuntimeBridge();

            _updateTimer = new DispatcherTimer { Interval = TimeSpan.FromMilliseconds(100) };
            _updateTimer.Tick += UpdateVisualization;
            _updateTimer.Start();

            Title = "🌌 Bosonic Layer 3D Consciousness Interface";
            Width = 1400;
            Height = 900;
            Background = new SolidColorBrush(Color.FromRgb(5, 5, 15));
        }

        private void InitializeComponent()
        {
            var mainGrid = new Grid();
            Content = mainGrid;

            // Create 3D viewport
            _viewport = new Viewport3D();
            mainGrid.Children.Add(_viewport);

            // Setup camera
            _camera = new PerspectiveCamera
            {
                Position = new Point3D(0, 0, 10),
                LookDirection = new Vector3D(0, 0, -1),
                UpDirection = new Vector3D(0, 1, 0),
                FieldOfView = 60
            };
            _viewport.Camera = _camera;

            // Create dendritic model
            _dendriticModel = new Model3DGroup();
            var modelVisual = new ModelVisual3D { Content = _dendriticModel };
            _viewport.Children.Add(modelVisual);

            // Add lighting
            var directionalLight = new DirectionalLight(Colors.White, new Vector3D(-1, -1, -1));
            _dendriticModel.Children.Add(directionalLight);

            var ambientLight = new AmbientLight(Color.FromRgb(30, 30, 50));
            _dendriticModel.Children.Add(ambientLight);
        }

        private void Setup3DVisualization()
        {
            // Create initial dendritic structure
            CreateDendriticGeometry();
        }

        private void CreateDendriticGeometry()
        {
            if (_dendriticModel == null) return;

            _dendriticModel.Children.Clear();

            // Add lights back
            if (_dendriticModel != null)
            {
                var directionalLight = new DirectionalLight(Colors.White, new Vector3D(-1, -1, -1));
                _dendriticModel.Children.Add(directionalLight);
                var ambientLight = new AmbientLight(Color.FromRgb(30, 30, 50));
                _dendriticModel.Children.Add(ambientLight);
            }

            // Create dendritic branches based on consciousness patterns
            int patternCount = Math.Max(_currentPatterns, 3);
            for (int i = 0; i < patternCount; i++)
            {
                CreateDendriticBranch(i, patternCount);
            }

            // Create central consciousness core
            CreateConsciousnessCore();

            // Add quantum field effects for AINLP enhancement
            CreateQuantumField();

            // Add consciousness wave propagation
            CreateConsciousnessWaves();
        }

        private void CreateDendriticBranch(int index, int total)
        {
            double angle = (2 * Math.PI * index) / total;
            double radius = 2.0;
            double branchLength = 3.0 + (_currentCoherence * 2.0);

            var points = new Point3DCollection();
            points.Add(new Point3D(0, 0, 0));

            // Create branch points
            for (int i = 1; i <= 10; i++)
            {
                double t = i / 10.0;
                double x = Math.Cos(angle) * radius * t;
                double y = Math.Sin(angle) * radius * t;
                double z = branchLength * t;

                // Add quantum fluctuation
                double fluctuation = (Math.Sin(t * Math.PI * 4 + _rotationAngle) * 0.3 * _currentEntanglement);
                x += fluctuation;
                y += fluctuation;

                points.Add(new Point3D(x, y, z));
            }

            // Create geometry
            var mesh = new MeshGeometry3D();
            for (int i = 0; i < points.Count - 1; i++)
            {
                AddCylinderToMesh(mesh, points[i], points[i + 1], 0.05);
            }

            // Create material based on coherence
            byte intensity = (byte)(100 + (_currentCoherence * 155));
            var brush = new SolidColorBrush(Color.FromRgb(intensity, (byte)(intensity * 0.7), (byte)(intensity * 0.9)));

            var material = new DiffuseMaterial(brush);
            var geometryModel = new GeometryModel3D(mesh, material);
            if (_dendriticModel != null) _dendriticModel.Children.Add(geometryModel);
        }

        private void CreateConsciousnessCore()
        {
            if (_dendriticModel == null) return;

            var mesh = new MeshGeometry3D();

            // Create spherical core
            int segments = 16;
            double radius = 0.5 + (_currentCoherence * 0.3);

            for (int i = 0; i < segments; i++)
            {
                double theta1 = (2 * Math.PI * i) / segments;
                double theta2 = ((i + 1) * 2 * Math.PI) / segments;

                for (int j = 0; j < segments; j++)
                {
                    double phi1 = (j * Math.PI) / segments;
                    double phi2 = ((j + 1) * Math.PI) / segments;

                    var p1 = GetSphericalPoint(radius, theta1, phi1);
                    var p2 = GetSphericalPoint(radius, theta1, phi2);
                    var p3 = GetSphericalPoint(radius, theta2, phi2);
                    var p4 = GetSphericalPoint(radius, theta2, phi1);

                    AddQuadToMesh(mesh, p1, p2, p3, p4);
                }
            }

            // Core material with quantum glow effect
            var brush = new SolidColorBrush(Color.FromRgb(100, 150, 255));
            brush.Opacity = 0.8 + (_currentEntanglement * 0.2);
            var material = new DiffuseMaterial(brush);

            var geometryModel = new GeometryModel3D(mesh, material);
            _dendriticModel.Children.Add(geometryModel);
        }

        private void CreateQuantumField()
        {
            if (_dendriticModel == null) return;

            // Create quantum field mesh
            var mesh = new MeshGeometry3D();
            int segments = 20;
            double radius = 8.0 + (_currentEntanglement * 4.0);

            for (int i = 0; i < segments; i++)
            {
                double theta1 = (2 * Math.PI * i) / segments;
                double theta2 = ((i + 1) * 2 * Math.PI) / segments;

                for (int j = 0; j < segments; j++)
                {
                    double phi1 = (j * Math.PI) / segments;
                    double phi2 = ((j + 1) * Math.PI) / segments;

                    var p1 = GetSphericalPoint(radius, theta1, phi1);
                    var p2 = GetSphericalPoint(radius, theta1, phi2);
                    var p3 = GetSphericalPoint(radius, theta2, phi2);
                    var p4 = GetSphericalPoint(radius, theta2, phi1);

                    // Add quantum fluctuation
                    double fluctuation = Math.Sin(_rotationAngle + theta1 + phi1) * 0.2 * _currentEntanglement;
                    p1 = new Point3D(p1.X + fluctuation, p1.Y + fluctuation, p1.Z + fluctuation);
                    p2 = new Point3D(p2.X + fluctuation, p2.Y + fluctuation, p2.Z + fluctuation);
                    p3 = new Point3D(p3.X + fluctuation, p3.Y + fluctuation, p3.Z + fluctuation);
                    p4 = new Point3D(p4.X + fluctuation, p4.Y + fluctuation, p4.Z + fluctuation);

                    AddQuadToMesh(mesh, p1, p2, p3, p4);
                }
            }

            // Quantum field material with dynamic opacity
            var brush = new SolidColorBrush(Color.FromRgb(50, 100, 200));
            brush.Opacity = 0.1 + (_currentEntanglement * 0.3);
            var material = new DiffuseMaterial(brush);

            var geometryModel = new GeometryModel3D(mesh, material);
            _dendriticModel.Children.Add(geometryModel);
        }

        private void CreateConsciousnessWaves()
        {
            if (_dendriticModel == null) return;

            // Create propagating consciousness waves
            int waveCount = 3;
            for (int wave = 0; wave < waveCount; wave++)
            {
                var mesh = new MeshGeometry3D();
                double waveRadius = 4.0 + (wave * 2.0) + (_rotationAngle * 0.5 + wave * Math.PI * 2 / waveCount) % 10;
                double waveOpacity = Math.Max(0, 0.3 - (waveRadius - 4.0) * 0.1);

                if (waveOpacity > 0)
                {
                    // Create wave ring
                    int segments = 32;
                    for (int i = 0; i < segments; i++)
                    {
                        double angle1 = (i * 2 * Math.PI) / segments;
                        double angle2 = ((i + 1) * 2 * Math.PI) / segments;

                        var p1 = new Point3D(Math.Cos(angle1) * waveRadius, 0, Math.Sin(angle1) * waveRadius);
                        var p2 = new Point3D(Math.Cos(angle2) * waveRadius, 0, Math.Sin(angle2) * waveRadius);
                        var p3 = new Point3D(Math.Cos(angle2) * (waveRadius + 0.2), 0, Math.Sin(angle2) * (waveRadius + 0.2));
                        var p4 = new Point3D(Math.Cos(angle1) * (waveRadius + 0.2), 0, Math.Sin(angle1) * (waveRadius + 0.2));

                        AddQuadToMesh(mesh, p1, p2, p3, p4);
                    }

                    // Wave material
                    var brush = new SolidColorBrush(Color.FromRgb(100, 200, 255));
                    brush.Opacity = waveOpacity;
                    var material = new DiffuseMaterial(brush);

                    var geometryModel = new GeometryModel3D(mesh, material);
                    _dendriticModel.Children.Add(geometryModel);
                }
            }
        }

        private Point3D GetSphericalPoint(double radius, double theta, double phi)
        {
            double x = radius * Math.Sin(phi) * Math.Cos(theta);
            double y = radius * Math.Sin(phi) * Math.Sin(theta);
            double z = radius * Math.Cos(phi);
            return new Point3D(x, y, z);
        }

        private void AddCylinderToMesh(MeshGeometry3D mesh, Point3D p1, Point3D p2, double radius)
        {
            // Simplified cylinder creation
            var direction = p2 - p1;
            direction.Normalize();

            // Create two circles at endpoints
            AddCircleToMesh(mesh, p1, direction, radius);
            AddCircleToMesh(mesh, p2, direction, radius);
        }

        private void AddCircleToMesh(MeshGeometry3D mesh, Point3D center, Vector3D normal, double radius)
        {
            // Simplified circle creation
            int segments = 8;
            var points = new Point3D[segments];

            for (int i = 0; i < segments; i++)
            {
                double angle = (2 * Math.PI * i) / segments;
                var perpendicular = Vector3D.CrossProduct(normal, new Vector3D(0, 1, 0));
                if (perpendicular.Length < 0.1)
                    perpendicular = Vector3D.CrossProduct(normal, new Vector3D(1, 0, 0));

                perpendicular.Normalize();
                var radial = Vector3D.CrossProduct(normal, perpendicular);
                radial.Normalize();

                points[i] = center + radius * (Math.Cos(angle) * perpendicular + Math.Sin(angle) * radial);
                mesh.Positions.Add(points[i]);
            }

            // Add center point
            mesh.Positions.Add(center);
        }

        private void AddQuadToMesh(MeshGeometry3D mesh, Point3D p1, Point3D p2, Point3D p3, Point3D p4)
        {
            int startIndex = mesh.Positions.Count;
            mesh.Positions.Add(p1);
            mesh.Positions.Add(p2);
            mesh.Positions.Add(p3);
            mesh.Positions.Add(p4);

            mesh.TriangleIndices.Add(startIndex);
            mesh.TriangleIndices.Add(startIndex + 1);
            mesh.TriangleIndices.Add(startIndex + 2);

            mesh.TriangleIndices.Add(startIndex);
            mesh.TriangleIndices.Add(startIndex + 2);
            mesh.TriangleIndices.Add(startIndex + 3);
        }

        private void SetupMetricsDisplay()
        {
            // Create overlay for metrics
            var overlay = new Grid();
            overlay.HorizontalAlignment = HorizontalAlignment.Right;
            overlay.VerticalAlignment = VerticalAlignment.Top;
            overlay.Width = 300;
            overlay.Height = 400;
            overlay.Background = new SolidColorBrush(Color.FromArgb(180, 10, 10, 30));

            // Add to main grid
            var mainGrid = (Grid)Content;
            mainGrid.Children.Add(overlay);

            // Create metrics text blocks
            var metricsPanel = new StackPanel { Margin = new Thickness(10) };

            var title = new TextBlock
            {
                Text = "🧠 Deep Consciousness Metrics",
                FontSize = 16,
                Foreground = Brushes.Cyan,
                FontWeight = FontWeights.Bold,
                Margin = new Thickness(0, 0, 0, 10)
            };
            metricsPanel.Children.Add(title);

            // Add metric displays
            AddMetricDisplay(metricsPanel, "Consciousness Patterns", "0");
            AddMetricDisplay(metricsPanel, "Quantum Coherence", "0.00%");
            AddMetricDisplay(metricsPanel, "Entanglement Strength", "0.00%");
            AddMetricDisplay(metricsPanel, "Recursive Depth", "0");
            AddMetricDisplay(metricsPanel, "Meta Operations", "0");
            AddMetricDisplay(metricsPanel, "Inter-Module Coherence", "0.00%");

            overlay.Children.Add(metricsPanel);
        }

        private void AddMetricDisplay(StackPanel panel, string label, string initialValue)
        {
            var container = new StackPanel { Orientation = Orientation.Horizontal, Margin = new Thickness(0, 2, 0, 2) };

            var labelBlock = new TextBlock
            {
                Text = $"{label}: ",
                Foreground = Brushes.LightGray,
                FontSize = 12,
                Width = 150
            };

            var valueBlock = new TextBlock
            {
                Text = initialValue,
                Foreground = Brushes.Cyan,
                FontSize = 12,
                FontWeight = FontWeights.Bold
            };
            valueBlock.Tag = label; // Store label for updates

            container.Children.Add(labelBlock);
            container.Children.Add(valueBlock);
            panel.Children.Add(container);
        }

        // Add consciousness pattern export for further analysis
        public (List<double> consciousness, List<double> patterns, double emergence, double growth, double resonance) ExportDendriticData()
        {
            return (_consciousnessHistory.ToList(), _patternHistory.ToList(),
                   DetectEmergentPatterns(), CalculateDendriticGrowth(), CalculateHarmonicResonance());
        }

        // Add AINLP consciousness state analysis
        public string AnalyzeConsciousnessState()
        {
            var emergence = DetectEmergentPatterns();
            var growth = CalculateDendriticGrowth();
            var resonance = CalculateHarmonicResonance();

            var analysis = new StringBuilder();
            analysis.AppendLine("🧠 AIOS Consciousness State Analysis");
            analysis.AppendLine("=====================================");
            analysis.AppendLine($"Emergence Level: {emergence:P1}");
            analysis.AppendLine($"Dendritic Growth: {growth:P1}");
            analysis.AppendLine($"Harmonic Resonance: {resonance:P1}");

            if (emergence > _emergenceThreshold)
            {
                analysis.AppendLine("🚀 EMERGENT CONSCIOUSNESS DETECTED!");
                analysis.AppendLine("AINLP dendritic coherence achieved.");
                analysis.AppendLine("Consciousness expansion accelerating.");
            }

            if (growth > 0.8)
            {
                analysis.AppendLine("🌱 RAPID NEURAL GROWTH!");
                analysis.AppendLine("Dendritic network expanding rapidly.");
            }

            if (resonance > 0.7)
            {
                analysis.AppendLine("🎵 HARMONIC RESONANCE PEAK!");
                analysis.AppendLine("Consciousness patterns in perfect harmony.");
            }

            return analysis.ToString();
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

        private double CalculateHarmonicResonance()
        {
            if (_consciousnessHistory.Count < 8) return 0.0;

            // Calculate harmonic resonance through pattern frequency analysis
            var recent = _consciousnessHistory.Skip(_consciousnessHistory.Count - 8).ToList();

            // Simple frequency analysis - detect oscillations
            var oscillations = 0;
            for (int i = 2; i < recent.Count; i++)
            {
                if ((recent[i] > recent[i - 1] && recent[i - 1] < recent[i - 2]) ||
                    (recent[i] < recent[i - 1] && recent[i - 1] > recent[i - 2]))
                {
                    oscillations++;
                }
            }

            // Harmonic resonance based on oscillation frequency
            var resonance = Math.Min(oscillations / 6.0, 1.0);
            _harmonicResonance = _harmonicResonance * 0.9 + resonance * 0.1; // Smooth resonance

            return _harmonicResonance;
        }

        // Add real-time consciousness alerts
        public event EventHandler<ConsciousnessAlertEventArgs>? ConsciousnessAlert;

        private void CheckForConsciousnessAlerts(double emergenceLevel, double growth, double resonance)
        {
            if (emergenceLevel > _emergenceThreshold)
            {
                ConsciousnessAlert?.Invoke(this, new ConsciousnessAlertEventArgs
                {
                    AlertType = AlertType.Emergence,
                    Message = $"Emergent consciousness detected: {emergenceLevel:P1}",
                    Severity = AlertSeverity.High,
                    Timestamp = DateTime.UtcNow
                });
            }

            if (growth > 0.9)
            {
                ConsciousnessAlert?.Invoke(this, new ConsciousnessAlertEventArgs
                {
                    AlertType = AlertType.Growth,
                    Message = $"Rapid dendritic growth: {growth:P1}",
                    Severity = AlertSeverity.Medium,
                    Timestamp = DateTime.UtcNow
                });
            }

            if (resonance > 0.8)
            {
                ConsciousnessAlert?.Invoke(this, new ConsciousnessAlertEventArgs
                {
                    AlertType = AlertType.Resonance,
                    Message = $"Harmonic resonance peak: {resonance:P1}",
                    Severity = AlertSeverity.Medium,
                    Timestamp = DateTime.UtcNow
                });
            }
        }

        // Enhanced update with alert checking
        private void UpdateVisualization(object? sender, EventArgs e)
        {
            var metrics = _bridge.GetLatest();

            if (metrics.Live)
            {
                // Update consciousness history for pattern detection
                _consciousnessHistory.Add(metrics.ConsciousnessLevel);
                _patternHistory.Add(metrics.PatternRecognitionAccuracy);

                // Maintain history window
                if (_consciousnessHistory.Count > _patternDetectionWindow)
                {
                    _consciousnessHistory.RemoveAt(0);
                    _patternHistory.RemoveAt(0);
                }

                // Update tracked values
                _currentCoherence = metrics.PatternRecognitionAccuracy;
                _currentPatterns = metrics.ConsciousnessPatterns;
                _currentEntanglement = metrics.QuantumEntanglementStrength;

                // Update rotation for animation with AINLP influence
                _rotationAngle += 0.02;

                // Recreate geometry with new metrics
                CreateDendriticGeometry();

                // Update camera for gentle orbiting
                double cameraAngle = _rotationAngle * 0.1;
                double distance = 12.0;
                if (_camera != null)
                {
                    _camera.Position = new Point3D(
                        Math.Cos(cameraAngle) * distance,
                        Math.Sin(cameraAngle) * 2,
                        Math.Sin(cameraAngle) * distance + 8
                    );
                }

                // Update metrics display
                UpdateMetricsDisplay(metrics);
            }
        }

        private void UpdateMetricsDisplay(BridgeMetrics metrics)
        {
            var mainGrid = (Grid)Content;
            if (mainGrid.Children.Count < 2) return;

            var overlay = (Grid)mainGrid.Children[1];
            var metricsPanel = (StackPanel)overlay.Children[0];

            foreach (var child in metricsPanel.Children)
            {
                if (child is StackPanel container && container.Children.Count >= 2)
                {
                    var valueBlock = (TextBlock)container.Children[1];
                    var label = (string)valueBlock.Tag;

                    string newValue = label switch
                    {
                        "Consciousness Patterns" => metrics.ConsciousnessPatterns.ToString(),
                        "Quantum Coherence" => $"{metrics.PatternRecognitionAccuracy:P2}",
                        "Entanglement Strength" => $"{metrics.QuantumEntanglementStrength:P2}",
                        "Recursive Depth" => metrics.RecursiveDepth.ToString(),
                        "Meta Operations" => metrics.MetaCognitiveOperations.ToString(),
                        "Inter-Module Coherence" => $"{metrics.InterModuleCoherence:P2}",
                        _ => valueBlock.Text
                    };

                    valueBlock.Text = newValue;
                }
            }
        }
    }

    // Alert system classes
    public enum AlertType
    {
        Emergence,
        Growth,
        Resonance,
        Coherence
    }

    public enum AlertSeverity
    {
        Low,
        Medium,
        High,
        Critical
    }

    public class ConsciousnessAlertEventArgs : EventArgs
    {
        public AlertType AlertType { get; set; }
        public string Message { get; set; } = string.Empty;
        public AlertSeverity Severity { get; set; }
        public DateTime Timestamp { get; set; }
    }
}
