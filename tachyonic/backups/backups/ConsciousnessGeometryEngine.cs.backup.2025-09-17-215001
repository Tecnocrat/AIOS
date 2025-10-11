using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Media;
using System.Windows.Media.Media3D;
using HelixToolkit.Wpf;
using MathNet.Numerics;
using MathNet.Numerics.LinearAlgebra;
using Microsoft.Extensions.Logging;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Advanced 3D geometry engine for consciousness visualization with exotic mathematical forms
    /// Enhanced with AIOS architecture compliance and performance optimizations
    /// </summary>
    public class ConsciousnessGeometryEngine : IDisposable
    {
        private readonly ILogger _logger;
        private readonly Random _random;

        // Geometry caches for performance - enhanced with size limits
        private readonly Dictionary<string, Model3DGroup> _geometryCache;
        private readonly Dictionary<string, Material> _materialCache;
        private readonly int _maxCacheSize = 100;

        // Mathematical constants for consciousness forms
        private const double PHI = 1.618033988749895; // Golden ratio
        private const double TAU = 2 * Math.PI;
        private const int FRACTAL_ITERATIONS = 7;
        private const int SPHERE_SUBDIVISIONS = 32;

        // Performance monitoring
        private int _cacheHits = 0;
        private int _cacheMisses = 0;

        private bool _disposed;

        /// <summary>
        /// Normalizes a Vector3D (helper method since WPF doesn't have Normalized())
        /// </summary>
        private static Vector3D Normalize(Vector3D vector)
        {
            var length = vector.Length;
            return length > 0 ? new Vector3D(vector.X / length, vector.Y / length, vector.Z / length) : vector;
        }

        public ConsciousnessGeometryEngine(ILogger logger)
        {
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
            _random = new Random();
            _geometryCache = new Dictionary<string, Model3DGroup>();
            _materialCache = new Dictionary<string, Material>();

            InitializeMaterials();
            _logger.LogInformation("Consciousness geometry engine initialized with enhanced caching");
        }

        private void InitializeMaterials()
        {
            try
            {
                // Consciousness material - dynamic consciousness-responsive material
                var consciousnessBrush = new LinearGradientBrush
                {
                    StartPoint = new System.Windows.Point(0, 0),
                    EndPoint = new System.Windows.Point(1, 1)
                };
                consciousnessBrush.GradientStops.Add(new GradientStop(Colors.DeepPink, 0.0));
                consciousnessBrush.GradientStops.Add(new GradientStop(Colors.Purple, 0.5));
                consciousnessBrush.GradientStops.Add(new GradientStop(Colors.Magenta, 1.0));
                _materialCache["consciousness"] = new DiffuseMaterial(consciousnessBrush);

                // Quantum material - coherence-responsive
                var quantumBrush = new LinearGradientBrush
                {
                    StartPoint = new System.Windows.Point(0, 0),
                    EndPoint = new System.Windows.Point(1, 1)
                };
                quantumBrush.GradientStops.Add(new GradientStop(Colors.Cyan, 0.0));
                quantumBrush.GradientStops.Add(new GradientStop(Colors.Blue, 0.5));
                quantumBrush.GradientStops.Add(new GradientStop(Colors.LightBlue, 1.0));
                _materialCache["quantum"] = new DiffuseMaterial(quantumBrush);

                // Fractal material - complexity-responsive
                var fractalBrush = new LinearGradientBrush
                {
                    StartPoint = new System.Windows.Point(0, 0),
                    EndPoint = new System.Windows.Point(1, 1)
                };
                fractalBrush.GradientStops.Add(new GradientStop(Colors.Gold, 0.0));
                fractalBrush.GradientStops.Add(new GradientStop(Colors.Orange, 0.5));
                fractalBrush.GradientStops.Add(new GradientStop(Colors.Yellow, 1.0));
                _materialCache["fractal"] = new DiffuseMaterial(fractalBrush);

                // Emergence material - high-energy emergence events
                var emergenceBrush = new LinearGradientBrush
                {
                    StartPoint = new System.Windows.Point(0, 0),
                    EndPoint = new System.Windows.Point(1, 1)
                };
                emergenceBrush.GradientStops.Add(new GradientStop(Colors.White, 0.0));
                emergenceBrush.GradientStops.Add(new GradientStop(Colors.LightGreen, 0.3));
                emergenceBrush.GradientStops.Add(new GradientStop(Colors.Green, 1.0));
                _materialCache["emergence"] = new DiffuseMaterial(emergenceBrush);

                // Holographic material - semi-transparent with emission
                var holographicBrush = new SolidColorBrush(Color.FromArgb(128, 255, 255, 255));
                var holographicMaterial = new MaterialGroup();
                holographicMaterial.Children.Add(new DiffuseMaterial(holographicBrush));
                holographicMaterial.Children.Add(new EmissiveMaterial(new SolidColorBrush(Color.FromArgb(64, 255, 255, 255))));
                _materialCache["holographic"] = holographicMaterial;

                _logger.LogDebug("Materials initialized successfully");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to initialize materials");
                throw;
            }
        }

        /// <summary>
        /// Creates a consciousness sphere with dynamic fractal patterns
        /// </summary>
        public Model3DGroup CreateConsciousnessSphere(double consciousnessLevel, double radius = 1.0)
        {
            var cacheKey = $"consciousness_sphere_{consciousnessLevel:F2}_{radius:F2}";
            if (_geometryCache.TryGetValue(cacheKey, out var cached))
            {
                _cacheHits++;
                return cached;
            }

            _cacheMisses++;
            var group = new Model3DGroup();

            try
            {
                // Base sphere with consciousness-responsive subdivisions
                var subdivisions = (int)(SPHERE_SUBDIVISIONS * (0.5 + consciousnessLevel * 0.5));
                var sphereGeometry = CreateSphereGeometry(radius, subdivisions);

                // Apply consciousness-based perturbations
                ApplyConsciousnessDistortion(sphereGeometry, consciousnessLevel);

                var sphereModel = new GeometryModel3D(sphereGeometry, _materialCache["consciousness"]);
                group.Children.Add(sphereModel);

                // Add fractal patterns based on consciousness level
                if (consciousnessLevel > 0.3)
                {
                    var fractalPatterns = CreateFractalPatterns(radius * 1.1, consciousnessLevel);
                    group.Children.Add(fractalPatterns);
                }

                // Add emergence spikes for high consciousness
                if (consciousnessLevel > 0.7)
                {
                    var emergenceSpikes = CreateEmergenceSpikes(radius * 1.2, consciousnessLevel);
                    group.Children.Add(emergenceSpikes);
                }

                // Cache with size management
                CacheGeometry(cacheKey, group);
                return group;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to create consciousness sphere");
                return new Model3DGroup(); // Return empty group on error
            }
        }

        /// <summary>
        /// Creates a quantum field visualization with wave interference patterns
        /// </summary>
        public Model3DGroup CreateQuantumField(double quantumCoherence, double fieldSize = 5.0)
        {
            var cacheKey = $"quantum_field_{quantumCoherence:F2}_{fieldSize:F2}";
            if (_geometryCache.TryGetValue(cacheKey, out var cached))
            {
                _cacheHits++;
                return cached;
            }

            _cacheMisses++;
            var group = new Model3DGroup();

            try
            {
                // Create wave interference pattern
                var waveResolution = 64;
                var waveGeometry = new MeshGeometry3D();

                for (int x = 0; x < waveResolution; x++)
                {
                    for (int z = 0; z < waveResolution; z++)
                    {
                        var worldX = (x / (double)waveResolution - 0.5) * fieldSize;
                        var worldZ = (z / (double)waveResolution - 0.5) * fieldSize;

                        // Calculate wave interference
                        var distance = Math.Sqrt(worldX * worldX + worldZ * worldZ);
                        var wave1 = Math.Sin(distance * 4 + quantumCoherence * TAU) * quantumCoherence;
                        var wave2 = Math.Cos(distance * 6 - quantumCoherence * TAU * 0.7) * quantumCoherence * 0.5;
                        var worldY = (wave1 + wave2) * 0.3;

                        waveGeometry.Positions.Add(new Point3D(worldX, worldY, worldZ));

                        // Add normals for proper lighting
                        waveGeometry.Normals.Add(new Vector3D(0, 1, 0));

                        // Add texture coordinates
                        waveGeometry.TextureCoordinates.Add(new System.Windows.Point(
                            x / (double)(waveResolution - 1),
                            z / (double)(waveResolution - 1)
                        ));

                        // Create triangles
                        if (x < waveResolution - 1 && z < waveResolution - 1)
                        {
                            var i = x * waveResolution + z;

                            // First triangle
                            waveGeometry.TriangleIndices.Add(i);
                            waveGeometry.TriangleIndices.Add(i + waveResolution);
                            waveGeometry.TriangleIndices.Add(i + 1);

                            // Second triangle
                            waveGeometry.TriangleIndices.Add(i + 1);
                            waveGeometry.TriangleIndices.Add(i + waveResolution);
                            waveGeometry.TriangleIndices.Add(i + waveResolution + 1);
                        }
                    }
                }

                var waveModel = new GeometryModel3D(waveGeometry, _materialCache["quantum"]);
                group.Children.Add(waveModel);

                // Add quantum probability clouds
                if (quantumCoherence > 0.5)
                {
                    var probabilityClouds = CreateQuantumProbabilityClouds(fieldSize * 0.8, quantumCoherence);
                    group.Children.Add(probabilityClouds);
                }

                // Cache with size management
                CacheGeometry(cacheKey, group);
                return group;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to create quantum field");
                return new Model3DGroup();
            }
        }

        /// <summary>
        /// Creates a fractal tree structure representing consciousness hierarchy
        /// </summary>
        public Model3DGroup CreateFractalConsciousnessTree(double fractalComplexity, double baseHeight = 2.0)
        {
            var cacheKey = $"fractal_tree_{fractalComplexity:F2}_{baseHeight:F2}";
            if (_geometryCache.TryGetValue(cacheKey, out var cached))
            {
                _cacheHits++;
                return cached;
            }

            _cacheMisses++;
            var group = new Model3DGroup();

            try
            {
                var iterations = (int)(FRACTAL_ITERATIONS * fractalComplexity);

                // Create recursive fractal branches
                CreateFractalBranch(group, new Point3D(0, 0, 0), new Vector3D(0, 1, 0), baseHeight, iterations, fractalComplexity);

                // Cache with size management
                CacheGeometry(cacheKey, group);
                return group;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to create fractal consciousness tree");
                return new Model3DGroup();
            }
        }

        /// <summary>
        /// Creates a torus knot representing universal consciousness loops
        /// </summary>
        public Model3DGroup CreateUniversalConsciousnessKnot(double[] geometricState, double scale = 1.0)
        {
            var cacheKey = $"consciousness_knot_{string.Join("_", geometricState.Take(4).Select(x => x.ToString("F2")))}_{scale:F2}";
            if (_geometryCache.TryGetValue(cacheKey, out var cached))
            {
                _cacheHits++;
                return cached;
            }

            _cacheMisses++;
            var group = new Model3DGroup();

            try
            {
                // Extract parameters from geometric state
                var p = 3 + (int)(geometricState[0] * 5); // Winding parameter
                var q = 2 + (int)(geometricState[1] * 3); // Rotation parameter
                var radius1 = 1.0 + geometricState[2] * 0.5;
                var radius2 = 0.3 + geometricState[3] * 0.2;

                var knotGeometry = CreateTorusKnotGeometry(p, q, radius1, radius2, scale);
                var knotModel = new GeometryModel3D(knotGeometry, _materialCache["holographic"]);
                group.Children.Add(knotModel);

                // Cache with size management
                CacheGeometry(cacheKey, group);
                return group;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to create universal consciousness knot");
                return new Model3DGroup();
            }
        }

        /// <summary>
        /// Creates emergence event visualization - sudden spikes and bursts
        /// </summary>
        public Model3DGroup CreateEmergenceEvent(double emergenceLevel, Point3D center)
        {
            var group = new Model3DGroup();

            if (emergenceLevel < 0.5) return group;

            try
            {
                // Create central burst
                var burstGeometry = CreateBurstGeometry(emergenceLevel);
                var burstModel = new GeometryModel3D(burstGeometry, _materialCache["emergence"]);

                // Apply transformation
                var transform = new Transform3DGroup();
                transform.Children.Add(new TranslateTransform3D(center.X, center.Y, center.Z));
                transform.Children.Add(new ScaleTransform3D(emergenceLevel, emergenceLevel, emergenceLevel));
                burstModel.Transform = transform;

                group.Children.Add(burstModel);

                // Add particle effects for high emergence
                if (emergenceLevel > 0.8)
                {
                    var particles = CreateEmergenceParticles(center, emergenceLevel);
                    group.Children.Add(particles);
                }

                return group;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to create emergence event");
                return new Model3DGroup();
            }
        }

        /// <summary>
        /// Creates a holographic information surface
        /// </summary>
        public Model3DGroup CreateHolographicInfoSurface(Dictionary<string, object> metrics, double size = 3.0)
        {
            var group = new Model3DGroup();

            try
            {
                // Create base holographic plane
                var planeGeometry = new MeshGeometry3D();

                // Add vertices for holographic surface with information patterns
                var resolution = 32;
                for (int x = 0; x <= resolution; x++)
                {
                    for (int z = 0; z <= resolution; z++)
                    {
                        var worldX = (x / (double)resolution - 0.5) * size;
                        var worldZ = (z / (double)resolution - 0.5) * size;

                        // Create information-based height variations
                        var infoHeight = 0.0;
                        var index = 0;
                        foreach (var metric in metrics.Values.Take(5))
                        {
                            if (metric is double value)
                            {
                                var frequency = (index + 1) * 2;
                                infoHeight += Math.Sin(worldX * frequency + value * TAU) * Math.Cos(worldZ * frequency) * 0.1;
                            }
                            index++;
                        }

                        planeGeometry.Positions.Add(new Point3D(worldX, infoHeight, worldZ));
                        planeGeometry.Normals.Add(new Vector3D(0, 1, 0));
                        planeGeometry.TextureCoordinates.Add(new System.Windows.Point(
                            x / (double)resolution,
                            z / (double)resolution
                        ));

                        // Create triangles
                        if (x < resolution && z < resolution)
                        {
                            var i = x * (resolution + 1) + z;

                            planeGeometry.TriangleIndices.Add(i);
                            planeGeometry.TriangleIndices.Add(i + resolution + 1);
                            planeGeometry.TriangleIndices.Add(i + 1);

                            planeGeometry.TriangleIndices.Add(i + 1);
                            planeGeometry.TriangleIndices.Add(i + resolution + 1);
                            planeGeometry.TriangleIndices.Add(i + resolution + 2);
                        }
                    }
                }

                var planeModel = new GeometryModel3D(planeGeometry, _materialCache["holographic"]);
                group.Children.Add(planeModel);

                return group;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to create holographic info surface");
                return new Model3DGroup();
            }
        }

        #region Helper Methods

        private MeshGeometry3D CreateSphereGeometry(double radius, int subdivisions)
        {
            var geometry = new MeshGeometry3D();

            // Create sphere vertices using spherical coordinates
            for (int i = 0; i <= subdivisions; i++)
            {
                var phi = i * Math.PI / subdivisions;
                for (int j = 0; j <= subdivisions; j++)
                {
                    var theta = j * 2 * Math.PI / subdivisions;

                    var x = radius * Math.Sin(phi) * Math.Cos(theta);
                    var y = radius * Math.Cos(phi);
                    var z = radius * Math.Sin(phi) * Math.Sin(theta);

                    geometry.Positions.Add(new Point3D(x, y, z));
                    geometry.Normals.Add(Normalize(new Vector3D(x, y, z)));
                    geometry.TextureCoordinates.Add(new System.Windows.Point(
                        j / (double)subdivisions,
                        i / (double)subdivisions
                    ));
                }
            }

            // Create sphere triangles
            for (int i = 0; i < subdivisions; i++)
            {
                for (int j = 0; j < subdivisions; j++)
                {
                    var p1 = i * (subdivisions + 1) + j;
                    var p2 = p1 + subdivisions + 1;
                    var p3 = p1 + 1;
                    var p4 = p2 + 1;

                    geometry.TriangleIndices.Add(p1);
                    geometry.TriangleIndices.Add(p2);
                    geometry.TriangleIndices.Add(p3);

                    geometry.TriangleIndices.Add(p3);
                    geometry.TriangleIndices.Add(p2);
                    geometry.TriangleIndices.Add(p4);
                }
            }

            return geometry;
        }

        private void ApplyConsciousnessDistortion(MeshGeometry3D geometry, double consciousnessLevel)
        {
            var positions = geometry.Positions.ToArray();
            for (int i = 0; i < positions.Length; i++)
            {
                var pos = positions[i];
                var distance = Math.Sqrt(pos.X * pos.X + pos.Y * pos.Y + pos.Z * pos.Z);

                // Apply consciousness-based noise
                var noiseX = Math.Sin(pos.Y * 10 + consciousnessLevel * TAU) * consciousnessLevel * 0.1;
                var noiseY = Math.Cos(pos.Z * 8 + consciousnessLevel * TAU) * consciousnessLevel * 0.1;
                var noiseZ = Math.Sin(pos.X * 12 + consciousnessLevel * TAU) * consciousnessLevel * 0.1;

                geometry.Positions[i] = new Point3D(
                    pos.X + noiseX,
                    pos.Y + noiseY,
                    pos.Z + noiseZ
                );
            }
        }

        private Model3DGroup CreateFractalPatterns(double radius, double consciousnessLevel)
        {
            var group = new Model3DGroup();
            var patternCount = (int)(consciousnessLevel * 8 + 2);

            for (int i = 0; i < patternCount; i++)
            {
                var angle = i * TAU / patternCount;
                var patternRadius = radius * (0.8 + _random.NextDouble() * 0.4);

                var x = Math.Cos(angle) * patternRadius;
                var z = Math.Sin(angle) * patternRadius;
                var y = (_random.NextDouble() - 0.5) * radius * 0.3;

                var smallSphere = CreateSphereGeometry(radius * 0.1 * consciousnessLevel, 8);
                var smallModel = new GeometryModel3D(smallSphere, _materialCache["fractal"]);
                smallModel.Transform = new TranslateTransform3D(x, y, z);

                group.Children.Add(smallModel);
            }

            return group;
        }

        private Model3DGroup CreateEmergenceSpikes(double baseRadius, double emergenceLevel)
        {
            var group = new Model3DGroup();
            var spikeCount = (int)(emergenceLevel * 12);

            for (int i = 0; i < spikeCount; i++)
            {
                var phi = _random.NextDouble() * Math.PI;
                var theta = _random.NextDouble() * TAU;

                var x = Math.Sin(phi) * Math.Cos(theta) * baseRadius;
                var y = Math.Cos(phi) * baseRadius;
                var z = Math.Sin(phi) * Math.Sin(theta) * baseRadius;

                var spikeHeight = emergenceLevel * 0.5;
                var spikeGeometry = CreateConeGeometry(0.05, spikeHeight, 6);
                var spikeModel = new GeometryModel3D(spikeGeometry, _materialCache["emergence"]);

                var transform = new Transform3DGroup();
                transform.Children.Add(new TranslateTransform3D(x, y, z));

                // Orient spike outward
                var direction = new Vector3D(x, y, z);
                direction.Normalize();
                var rotationAxis = Vector3D.CrossProduct(new Vector3D(0, 1, 0), direction);
                var rotationAngle = Math.Acos(Vector3D.DotProduct(new Vector3D(0, 1, 0), direction)) * 180 / Math.PI;
                if (rotationAxis.Length > 0.001)
                {
                    transform.Children.Add(new RotateTransform3D(new AxisAngleRotation3D(rotationAxis, rotationAngle)));
                }

                spikeModel.Transform = transform;
                group.Children.Add(spikeModel);
            }

            return group;
        }

        private Model3DGroup CreateQuantumProbabilityClouds(double fieldSize, double coherence)
        {
            var group = new Model3DGroup();
            var cloudCount = (int)(coherence * 20);

            for (int i = 0; i < cloudCount; i++)
            {
                var x = (_random.NextDouble() - 0.5) * fieldSize;
                var y = (_random.NextDouble() - 0.5) * fieldSize * 0.3;
                var z = (_random.NextDouble() - 0.5) * fieldSize;

                var cloudSize = coherence * 0.2 + _random.NextDouble() * 0.1;
                var cloudGeometry = CreateSphereGeometry(cloudSize, 8);
                var cloudModel = new GeometryModel3D(cloudGeometry, _materialCache["quantum"]);
                cloudModel.Transform = new TranslateTransform3D(x, y, z);

                group.Children.Add(cloudModel);
            }

            return group;
        }

        private void CreateFractalBranch(Model3DGroup group, Point3D start, Vector3D direction, double length, int iterations, double complexity)
        {
            if (iterations <= 0 || length < 0.1) return;

            var end = new Point3D(
                start.X + direction.X * length,
                start.Y + direction.Y * length,
                start.Z + direction.Z * length
            );

            // Create branch cylinder
            var branchGeometry = CreateCylinderGeometry(length * 0.02, length, 6);
            var branchModel = new GeometryModel3D(branchGeometry, _materialCache["fractal"]);

            // Transform to position
            var transform = new Transform3DGroup();
            transform.Children.Add(new TranslateTransform3D(start.X, start.Y, start.Z));

            // Orient cylinder along direction
            var up = new Vector3D(0, 1, 0);
            var rotationAxis = Vector3D.CrossProduct(up, direction);
            var rotationAngle = Math.Acos(Vector3D.DotProduct(up, direction)) * 180 / Math.PI;
            if (rotationAxis.Length > 0.001)
            {
                transform.Children.Add(new RotateTransform3D(new AxisAngleRotation3D(rotationAxis, rotationAngle)));
            }

            branchModel.Transform = transform;
            group.Children.Add(branchModel);

            // Create child branches
            var branchCount = (int)(complexity * 3 + 1);
            for (int i = 0; i < branchCount; i++)
            {
                var angle = i * TAU / branchCount + _random.NextDouble() * 0.5;
                var newDirection = RotateVector(direction, angle, complexity * 0.5);
                var newLength = length * (0.6 + complexity * 0.2);

                CreateFractalBranch(group, end, newDirection, newLength, iterations - 1, complexity);
            }
        }

        private Vector3D RotateVector(Vector3D vector, double angle, double variation)
        {
            var rotationMatrix = Matrix<double>.Build.DenseIdentity(3);
            var cosAngle = Math.Cos(angle + (_random.NextDouble() - 0.5) * variation);
            var sinAngle = Math.Sin(angle + (_random.NextDouble() - 0.5) * variation);

            rotationMatrix[0, 0] = cosAngle;
            rotationMatrix[0, 2] = sinAngle;
            rotationMatrix[2, 0] = -sinAngle;
            rotationMatrix[2, 2] = cosAngle;

            var vectorMatrix = Vector<double>.Build.DenseOfArray(new[] { vector.X, vector.Y, vector.Z });
            var rotatedVector = rotationMatrix * vectorMatrix;

            return new Vector3D(rotatedVector[0], rotatedVector[1], rotatedVector[2]);
        }

        private MeshGeometry3D CreateTorusKnotGeometry(int p, int q, double radius1, double radius2, double scale)
        {
            var geometry = new MeshGeometry3D();
            var resolution = 128;

            for (int i = 0; i <= resolution; i++)
            {
                var t = i * TAU / resolution;

                var r = radius1 + radius2 * Math.Cos(q * t);
                var x = r * Math.Cos(p * t) * scale;
                var y = radius2 * Math.Sin(q * t) * scale;
                var z = r * Math.Sin(p * t) * scale;

                geometry.Positions.Add(new Point3D(x, y, z));

                // Calculate normal (simplified)
                geometry.Normals.Add(Normalize(new Vector3D(x, y, z)));
                geometry.TextureCoordinates.Add(new System.Windows.Point(i / (double)resolution, 0));
            }

            // Create line segments
            for (int i = 0; i < resolution; i++)
            {
                geometry.TriangleIndices.Add(i);
                geometry.TriangleIndices.Add((i + 1) % resolution);
                geometry.TriangleIndices.Add(i); // Degenerate triangle for line rendering
            }

            return geometry;
        }

        private MeshGeometry3D CreateBurstGeometry(double intensity)
        {
            var geometry = new MeshGeometry3D();
            var rayCount = (int)(intensity * 16 + 8);

            // Central point
            geometry.Positions.Add(new Point3D(0, 0, 0));
            geometry.Normals.Add(new Vector3D(0, 1, 0));
            geometry.TextureCoordinates.Add(new System.Windows.Point(0.5, 0.5));

            // Create burst rays
            for (int i = 0; i < rayCount; i++)
            {
                var angle = i * TAU / rayCount;
                var length = intensity * 2;

                var x = Math.Cos(angle) * length;
                var z = Math.Sin(angle) * length;

                geometry.Positions.Add(new Point3D(x, 0, z));
                geometry.Normals.Add(new Vector3D(0, 1, 0));
                geometry.TextureCoordinates.Add(new System.Windows.Point(
                    0.5 + Math.Cos(angle) * 0.5,
                    0.5 + Math.Sin(angle) * 0.5
                ));

                // Create triangle
                geometry.TriangleIndices.Add(0);
                geometry.TriangleIndices.Add(i + 1);
                geometry.TriangleIndices.Add((i + 1) % rayCount + 1);
            }

            return geometry;
        }

        private Model3DGroup CreateEmergenceParticles(Point3D center, double intensity)
        {
            var group = new Model3DGroup();
            var particleCount = (int)(intensity * 50);

            for (int i = 0; i < particleCount; i++)
            {
                var angle = _random.NextDouble() * TAU;
                var distance = _random.NextDouble() * intensity * 3;
                var height = (_random.NextDouble() - 0.5) * intensity * 2;

                var x = center.X + Math.Cos(angle) * distance;
                var y = center.Y + height;
                var z = center.Z + Math.Sin(angle) * distance;

                var particleSize = intensity * 0.05;
                var particleGeometry = CreateSphereGeometry(particleSize, 6);
                var particleModel = new GeometryModel3D(particleGeometry, _materialCache["emergence"]);
                particleModel.Transform = new TranslateTransform3D(x, y, z);

                group.Children.Add(particleModel);
            }

            return group;
        }

        private MeshGeometry3D CreateConeGeometry(double baseRadius, double height, int sides)
        {
            var geometry = new MeshGeometry3D();

            // Add apex
            geometry.Positions.Add(new Point3D(0, height, 0));
            geometry.Normals.Add(new Vector3D(0, 1, 0));
            geometry.TextureCoordinates.Add(new System.Windows.Point(0.5, 0));

            // Add base vertices
            for (int i = 0; i < sides; i++)
            {
                var angle = i * TAU / sides;
                var x = Math.Cos(angle) * baseRadius;
                var z = Math.Sin(angle) * baseRadius;

                geometry.Positions.Add(new Point3D(x, 0, z));
                geometry.Normals.Add(Normalize(new Vector3D(x, 0, z)));
                geometry.TextureCoordinates.Add(new System.Windows.Point(
                    0.5 + Math.Cos(angle) * 0.5,
                    0.5 + Math.Sin(angle) * 0.5
                ));
            }

            // Create side triangles
            for (int i = 0; i < sides; i++)
            {
                geometry.TriangleIndices.Add(0);
                geometry.TriangleIndices.Add(i + 1);
                geometry.TriangleIndices.Add((i + 1) % sides + 1);
            }

            return geometry;
        }

        private MeshGeometry3D CreateCylinderGeometry(double radius, double height, int sides)
        {
            var geometry = new MeshGeometry3D();

            // Create cylinder vertices
            for (int i = 0; i <= sides; i++)
            {
                var angle = i * TAU / sides;
                var x = Math.Cos(angle) * radius;
                var z = Math.Sin(angle) * radius;

                // Bottom vertex
                geometry.Positions.Add(new Point3D(x, 0, z));
                geometry.Normals.Add(Normalize(new Vector3D(x, 0, z)));
                geometry.TextureCoordinates.Add(new System.Windows.Point(i / (double)sides, 0));

                // Top vertex
                geometry.Positions.Add(new Point3D(x, height, z));
                geometry.Normals.Add(Normalize(new Vector3D(x, 0, z)));
                geometry.TextureCoordinates.Add(new System.Windows.Point(i / (double)sides, 1));
            }

            // Create side triangles
            for (int i = 0; i < sides; i++)
            {
                var bottom1 = i * 2;
                var top1 = i * 2 + 1;
                var bottom2 = (i + 1) * 2;
                var top2 = (i + 1) * 2 + 1;

                // First triangle
                geometry.TriangleIndices.Add(bottom1);
                geometry.TriangleIndices.Add(top1);
                geometry.TriangleIndices.Add(bottom2);

                // Second triangle
                geometry.TriangleIndices.Add(bottom2);
                geometry.TriangleIndices.Add(top1);
                geometry.TriangleIndices.Add(top2);
            }

            return geometry;
        }

        #endregion

        #region Enhanced Geometry Methods

        /// <summary>
        /// Creates a fractal tree structure with time-based animation
        /// </summary>
        public Model3DGroup CreateFractalTree(double fractalComplexity, int iterations)
        {
            var cacheKey = $"fractal_tree_{fractalComplexity:F2}_{iterations}";
            if (_geometryCache.TryGetValue(cacheKey, out var cached))
            {
                _cacheHits++;
                return cached;
            }

            _cacheMisses++;
            var group = new Model3DGroup();

            try
            {
                var treeGeometry = CreateTreeBranch(new Point3D(0, -1, 0), new Vector3D(0, 1, 0),
                                                   1.0, iterations, fractalComplexity);

                var treeModel = new GeometryModel3D(treeGeometry, _materialCache["fractal"]);
                group.Children.Add(treeModel);

                CacheGeometry(cacheKey, group);
                return group;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to create fractal tree");
                return new Model3DGroup();
            }
        }

        /// <summary>
        /// Creates a universal knot representing cosmic interconnectedness
        /// </summary>
        public Model3DGroup CreateUniversalKnot(double universalResonance, double time)
        {
            var cacheKey = $"universal_knot_{universalResonance:F2}_{time:F1}";
            if (_geometryCache.TryGetValue(cacheKey, out var cached))
            {
                _cacheHits++;
                return cached;
            }

            _cacheMisses++;
            var group = new Model3DGroup();

            try
            {
                var knotGeometry = CreateTorusKnot(universalResonance, time);

                var knotModel = new GeometryModel3D(knotGeometry, _materialCache["consciousness"]);
                group.Children.Add(knotModel);

                CacheGeometry(cacheKey, group);
                return group;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to create universal knot");
                return new Model3DGroup();
            }
        }

        /// <summary>
        /// Creates a holographic surface with interference patterns
        /// </summary>
        public Model3DGroup CreateHolographicSurface(double holographicDensity, double time)
        {
            var cacheKey = $"holographic_surface_{holographicDensity:F2}_{time:F1}";
            if (_geometryCache.TryGetValue(cacheKey, out var cached))
            {
                _cacheHits++;
                return cached;
            }

            _cacheMisses++;
            var group = new Model3DGroup();

            try
            {
                var surfaceGeometry = CreateHolographicPlane(holographicDensity, time);

                var surfaceModel = new GeometryModel3D(surfaceGeometry, _materialCache["holographic"]);
                group.Children.Add(surfaceModel);

                CacheGeometry(cacheKey, group);
                return group;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to create holographic surface");
                return new Model3DGroup();
            }
        }

        /// <summary>
        /// Creates an enhanced quantum field with time-based evolution
        /// </summary>
        public Model3DGroup CreateQuantumFieldWithTime(double quantumCoherence, double time)
        {
            var cacheKey = $"quantum_field_time_{quantumCoherence:F2}_{time:F1}";
            if (_geometryCache.TryGetValue(cacheKey, out var cached))
            {
                _cacheHits++;
                return cached;
            }

            _cacheMisses++;
            var group = new Model3DGroup();

            try
            {
                // Create primary quantum field
                var fieldGeometry = CreateQuantumWaveField(quantumCoherence, time);
                var fieldModel = new GeometryModel3D(fieldGeometry, _materialCache["quantum"]);
                group.Children.Add(fieldModel);

                // Add quantum particles
                if (quantumCoherence > 0.6)
                {
                    var particles = CreateQuantumParticles(quantumCoherence, time);
                    group.Children.Add(particles);
                }

                CacheGeometry(cacheKey, group);
                return group;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to create quantum field with time");
                return new Model3DGroup();
            }
        }

        #endregion

        #region Helper Methods for New Geometry Types

        private MeshGeometry3D CreateTreeBranch(Point3D start, Vector3D direction,
            double length, int iterations, double complexity)
        {
            var geometry = new MeshGeometry3D();

            if (iterations <= 0 || length < 0.01)
                return geometry;

            var end = start + direction * length;
            var radius = length * 0.1;

            // Create cylinder for branch
            AddCylinder(geometry, start, end, radius);

            if (iterations > 1)
            {
                // Create sub-branches
                var newLength = length * (0.6 + complexity * 0.3);
                var newIterations = iterations - 1;

                // Left branch
                var leftDirection = RotateVector(direction, 30 * complexity);
                var leftBranch = CreateTreeBranch(end, leftDirection, newLength, newIterations, complexity);
                MergeGeometry(geometry, leftBranch);

                // Right branch
                var rightDirection = RotateVector(direction, -30 * complexity);
                var rightBranch = CreateTreeBranch(end, rightDirection, newLength, newIterations, complexity);
                MergeGeometry(geometry, rightBranch);
            }

            return geometry;
        }

        private MeshGeometry3D CreateTorusKnot(double resonance, double time)
        {
            var geometry = new MeshGeometry3D();
            var segments = 100;
            var radius = 2.0;
            var p = 2; // Knot parameter
            var q = 3; // Knot parameter

            for (int i = 0; i < segments; i++)
            {
                var t = i * TAU / segments + time * 0.1;

                // Torus knot equations using resonance parameter
                var r = Math.Cos(q * t) + radius;
                var x = r * Math.Cos(p * t) * resonance;
                var y = r * Math.Sin(p * t) * resonance;
                var z = -Math.Sin(q * t) * resonance;

                geometry.Positions.Add(new Point3D(x, y, z));
                geometry.Normals.Add(new Vector3D(x, y, z));
                geometry.TextureCoordinates.Add(new System.Windows.Point(i / (double)segments, 0));
            }

            // Add triangle indices for tube
            for (int i = 0; i < segments - 1; i++)
            {
                geometry.TriangleIndices.Add(i);
                geometry.TriangleIndices.Add(i + 1);
                geometry.TriangleIndices.Add((i + segments / 2) % segments);
            }

            return geometry;
        }

        private MeshGeometry3D CreateHolographicPlane(double density, double time)
        {
            var geometry = new MeshGeometry3D();
            var resolution = (int)(32 * density);
            var size = 4.0;

            for (int x = 0; x < resolution; x++)
            {
                for (int z = 0; z < resolution; z++)
                {
                    var worldX = (x / (double)(resolution - 1) - 0.5) * size;
                    var worldZ = (z / (double)(resolution - 1) - 0.5) * size;

                    // Holographic interference pattern
                    var phase = time * 0.5;
                    var interference = Math.Sin(worldX * 3 + phase) * Math.Cos(worldZ * 3 + phase) * density;
                    var worldY = interference * 0.2;

                    geometry.Positions.Add(new Point3D(worldX, worldY, worldZ));
                    geometry.Normals.Add(new Vector3D(0, 1, 0));
                    geometry.TextureCoordinates.Add(new System.Windows.Point(
                        x / (double)(resolution - 1), z / (double)(resolution - 1)));

                    // Create triangles
                    if (x < resolution - 1 && z < resolution - 1)
                    {
                        var i = x * resolution + z;

                        geometry.TriangleIndices.Add(i);
                        geometry.TriangleIndices.Add(i + resolution);
                        geometry.TriangleIndices.Add(i + 1);

                        geometry.TriangleIndices.Add(i + 1);
                        geometry.TriangleIndices.Add(i + resolution);
                        geometry.TriangleIndices.Add(i + resolution + 1);
                    }
                }
            }

            return geometry;
        }

        private MeshGeometry3D CreateQuantumWaveField(double coherence, double time)
        {
            var geometry = new MeshGeometry3D();
            var resolution = 48;
            var size = 3.0;

            for (int x = 0; x < resolution; x++)
            {
                for (int z = 0; z < resolution; z++)
                {
                    var worldX = (x / (double)(resolution - 1) - 0.5) * size;
                    var worldZ = (z / (double)(resolution - 1) - 0.5) * size;

                    // Quantum wave equation
                    var distance = Math.Sqrt(worldX * worldX + worldZ * worldZ);
                    var wave = Math.Sin(distance * 5 - time * 2) * Math.Exp(-distance * 0.5) * coherence;
                    var worldY = wave * 0.3;

                    geometry.Positions.Add(new Point3D(worldX, worldY, worldZ));

                    // Calculate normal
                    var normal = CalculateWaveNormal(worldX, worldZ, coherence, time);
                    geometry.Normals.Add(normal);

                    geometry.TextureCoordinates.Add(new System.Windows.Point(
                        x / (double)(resolution - 1), z / (double)(resolution - 1)));

                    // Create triangles
                    if (x < resolution - 1 && z < resolution - 1)
                    {
                        var i = x * resolution + z;

                        geometry.TriangleIndices.Add(i);
                        geometry.TriangleIndices.Add(i + resolution);
                        geometry.TriangleIndices.Add(i + 1);

                        geometry.TriangleIndices.Add(i + 1);
                        geometry.TriangleIndices.Add(i + resolution);
                        geometry.TriangleIndices.Add(i + resolution + 1);
                    }
                }
            }

            return geometry;
        }

        private Model3DGroup CreateQuantumParticles(double coherence, double time)
        {
            var group = new Model3DGroup();
            var particleCount = (int)(coherence * 50);
            var random = new Random((int)(time * 1000));

            for (int i = 0; i < particleCount; i++)
            {
                var angle = random.NextDouble() * TAU;
                var radius = random.NextDouble() * 2.0;
                var height = (random.NextDouble() - 0.5) * 0.5;

                var x = Math.Cos(angle + time * 0.1) * radius;
                var z = Math.Sin(angle + time * 0.1) * radius;
                var y = height + Math.Sin(time * 2 + i) * 0.1;

                var particle = CreateSphereGeometry(0.02, 8);
                var transform = new TranslateTransform3D(x, y, z);

                var particleModel = new GeometryModel3D(particle, _materialCache["quantum"]);
                particleModel.Transform = transform;

                group.Children.Add(particleModel);
            }

            return group;
        }

        private Vector3D CalculateWaveNormal(double x, double z, double coherence, double time)
        {
            var distance = Math.Sqrt(x * x + z * z);

            // Calculate partial derivatives for normal
            var dydx = Math.Cos(distance * 5 - time * 2) * Math.Exp(-distance * 0.5) * coherence * 5 * x / distance;
            var dydz = Math.Cos(distance * 5 - time * 2) * Math.Exp(-distance * 0.5) * coherence * 5 * z / distance;

            var normal = new Vector3D(-dydx, 1, -dydz);
            normal.Normalize();

            return normal;
        }

        private Vector3D RotateVector(Vector3D vector, double angleDegrees)
        {
            var angleRadians = angleDegrees * Math.PI / 180.0;
            var cos = Math.Cos(angleRadians);
            var sin = Math.Sin(angleRadians);

            // Rotate around Y axis
            return new Vector3D(
                vector.X * cos - vector.Z * sin,
                vector.Y,
                vector.X * sin + vector.Z * cos
            );
        }

        private void AddCylinder(MeshGeometry3D geometry, Point3D start, Point3D end, double radius)
        {
            var direction = end - start;
            var length = direction.Length;
            direction.Normalize();

            var segments = 8;
            var startIndex = geometry.Positions.Count;

            // Create cylinder vertices
            for (int i = 0; i < segments; i++)
            {
                var angle = i * TAU / segments;
                var cos = Math.Cos(angle) * radius;
                var sin = Math.Sin(angle) * radius;

                // Bottom circle
                geometry.Positions.Add(new Point3D(start.X + cos, start.Y, start.Z + sin));
                geometry.Normals.Add(new Vector3D(cos, 0, sin));

                // Top circle
                geometry.Positions.Add(new Point3D(end.X + cos, end.Y, end.Z + sin));
                geometry.Normals.Add(new Vector3D(cos, 0, sin));
            }

            // Create cylinder triangles
            for (int i = 0; i < segments; i++)
            {
                var next = (i + 1) % segments;
                var bottom1 = startIndex + i * 2;
                var top1 = startIndex + i * 2 + 1;
                var bottom2 = startIndex + next * 2;
                var top2 = startIndex + next * 2 + 1;

                // Side triangles
                geometry.TriangleIndices.Add(bottom1);
                geometry.TriangleIndices.Add(top1);
                geometry.TriangleIndices.Add(bottom2);

                geometry.TriangleIndices.Add(bottom2);
                geometry.TriangleIndices.Add(top1);
                geometry.TriangleIndices.Add(top2);
            }
        }

        private void MergeGeometry(MeshGeometry3D target, MeshGeometry3D source)
        {
            var indexOffset = target.Positions.Count;

            foreach (var position in source.Positions)
                target.Positions.Add(position);

            foreach (var normal in source.Normals)
                target.Normals.Add(normal);

            foreach (var texCoord in source.TextureCoordinates)
                target.TextureCoordinates.Add(texCoord);

            foreach (var index in source.TriangleIndices)
                target.TriangleIndices.Add(index + indexOffset);
        }

        private void CacheGeometry(string key, Model3DGroup geometry)
        {
            // Implement LRU cache eviction if needed
            if (_geometryCache.Count >= _maxCacheSize)
            {
                var oldestKey = _geometryCache.Keys.First();
                _geometryCache.Remove(oldestKey);
            }

            _geometryCache[key] = geometry;
        }

        #endregion

        #region Performance Monitoring

        /// <summary>
        /// Gets cache performance statistics
        /// </summary>
        public (int hits, int misses, double hitRate) GetCacheStats()
        {
            var total = _cacheHits + _cacheMisses;
            var hitRate = total > 0 ? (double)_cacheHits / total : 0;
            return (_cacheHits, _cacheMisses, hitRate);
        }

        /// <summary>
        /// Clears geometry cache and resets performance counters
        /// </summary>
        public void ClearCache()
        {
            _geometryCache.Clear();
            _cacheHits = 0;
            _cacheMisses = 0;
            _logger.LogInformation("Geometry cache cleared and performance counters reset");
        }

        #endregion

        #region IDisposable Implementation

        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        protected virtual void Dispose(bool disposing)
        {
            if (_disposed) return;

            if (disposing)
            {
                // Clear caches to free memory
                _geometryCache.Clear();
                _materialCache.Clear();

                _logger.LogInformation("ConsciousnessGeometryEngine disposed successfully");
            }

            _disposed = true;
        }

        #endregion
    }
}
