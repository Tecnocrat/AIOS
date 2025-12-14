using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
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
    /// Multi-threaded for stable 60+ FPS - Phase 1B Enhancement
    /// </summary>
    public class ConsciousnessGeometryEngine : IDisposable
    {
        private readonly ILogger _logger;
        private readonly Random _random;
        private readonly CancellationTokenSource _cancellationTokenSource;
        private readonly SemaphoreSlim _geometryGenerationSemaphore;
        
        // Thread-safe geometry caches for performance
        private readonly ConcurrentDictionary<string, Model3DGroup> _geometryCache;
        private readonly ConcurrentDictionary<string, Material> _materialCache;
        
        // Worker threads for parallel geometry generation
        private readonly Task[] _workerTasks;
        private readonly int _workerThreadCount;
        private readonly ConcurrentQueue<GeometryGenerationTask> _generationQueue;
        
        // Mathematical constants for consciousness forms
        private const double PHI = 1.618033988749895; // Golden ratio
        private const double TAU = 2 * Math.PI;
        private const int FRACTAL_ITERATIONS = 7;
        private const int SPHERE_SUBDIVISIONS = 32;
        
        // Performance monitoring
        private volatile int _geometriesGenerated;
        private volatile int _cacheHits;
        private volatile int _cacheMisses;
        
        // Events for async geometry completion
        public event EventHandler<GeometryGeneratedEventArgs>? GeometryGenerated;
        public event EventHandler<GeometryErrorEventArgs>? GeometryError;
        
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
            _logger = logger;
            _random = new Random();
            _cancellationTokenSource = new CancellationTokenSource();
            
            // Initialize thread-safe collections
            _geometryCache = new ConcurrentDictionary<string, Model3DGroup>();
            _materialCache = new ConcurrentDictionary<string, Material>();
            _generationQueue = new ConcurrentQueue<GeometryGenerationTask>();
            
            // Configure worker threads for parallel processing
            _workerThreadCount = Math.Max(2, Environment.ProcessorCount / 2);
            _geometryGenerationSemaphore = new SemaphoreSlim(_workerThreadCount);
            
            // Initialize background worker threads
            _workerTasks = new Task[_workerThreadCount];
            for (int i = 0; i < _workerThreadCount; i++)
            {
                int workerId = i;
                _workerTasks[i] = Task.Run(async () => await GeometryWorkerLoop(workerId, _cancellationTokenSource.Token));
            }
            
            InitializeMaterials();
            _logger.LogInformation($"Multi-threaded consciousness geometry engine initialized with {_workerThreadCount} worker threads");
        }
        
        private void InitializeMaterials()
        {
            // Consciousness material - dynamic consciousness-responsive material
            var consciousnessBrush = new LinearGradientBrush();
            consciousnessBrush.GradientStops.Add(new GradientStop(Colors.DeepPink, 0.0));
            consciousnessBrush.GradientStops.Add(new GradientStop(Colors.Purple, 0.5));
            consciousnessBrush.GradientStops.Add(new GradientStop(Colors.Magenta, 1.0));
            _materialCache["consciousness"] = new DiffuseMaterial(consciousnessBrush);
            
            // Quantum material - coherence-responsive
            var quantumBrush = new LinearGradientBrush();
            quantumBrush.GradientStops.Add(new GradientStop(Colors.Cyan, 0.0));
            quantumBrush.GradientStops.Add(new GradientStop(Colors.Blue, 0.5));
            quantumBrush.GradientStops.Add(new GradientStop(Colors.LightBlue, 1.0));
            _materialCache["quantum"] = new DiffuseMaterial(quantumBrush);
            
            // Fractal material - complexity-responsive
            var fractalBrush = new LinearGradientBrush();
            fractalBrush.GradientStops.Add(new GradientStop(Colors.Gold, 0.0));
            fractalBrush.GradientStops.Add(new GradientStop(Colors.Orange, 0.5));
            fractalBrush.GradientStops.Add(new GradientStop(Colors.Yellow, 1.0));
            _materialCache["fractal"] = new DiffuseMaterial(fractalBrush);
            
            // Emergence material - high-energy emergence events
            var emergenceBrush = new LinearGradientBrush();
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
        }
        
        /// <summary>
        /// Creates a consciousness sphere with dynamic fractal patterns - Multi-threaded version
        /// </summary>
        public Model3DGroup CreateConsciousnessSphere(double consciousnessLevel, double radius = 1.0)
        {
            var cacheKey = $"consciousness_sphere_{consciousnessLevel:F2}_{radius:F2}";
            if (_geometryCache.TryGetValue(cacheKey, out var cachedGeometry))
            {
                Interlocked.Increment(ref _cacheHits);
                return cachedGeometry;
            }
            
            // For synchronous calls, generate directly
            Interlocked.Increment(ref _cacheMisses);
            var task = new GeometryGenerationTask
            {
                TaskType = GeometryTaskType.ConsciousnessSphere,
                CacheKey = cacheKey,
                Parameters = new Dictionary<string, object>
                {
                    ["consciousnessLevel"] = consciousnessLevel,
                    ["radius"] = radius
                }
            };
            
            var geometry = GenerateConsciousnessSphere(task);
            
            // Cache the result
            _geometryCache.TryAdd(cacheKey, geometry);
            Interlocked.Increment(ref _geometriesGenerated);
            
            return geometry;
        }
        
        /// <summary>
        /// Creates a consciousness sphere asynchronously for better performance
        /// </summary>
        public async Task<Model3DGroup> CreateConsciousnessSphereAsync(double consciousnessLevel, double radius = 1.0)
        {
            var cacheKey = $"consciousness_sphere_{consciousnessLevel:F2}_{radius:F2}";
            var task = new GeometryGenerationTask
            {
                TaskType = GeometryTaskType.ConsciousnessSphere,
                CacheKey = cacheKey,
                Parameters = new Dictionary<string, object>
                {
                    ["consciousnessLevel"] = consciousnessLevel,
                    ["radius"] = radius
                }
            };
            
            var geometry = await GenerateGeometrySync(task);
            return geometry ?? new Model3DGroup();
        }
        
        /// <summary>
        /// Creates a quantum field visualization with wave interference patterns - Multi-threaded version
        /// </summary>
        public Model3DGroup CreateQuantumField(double quantumCoherence, double fieldSize = 5.0)
        {
            var cacheKey = $"quantum_field_{quantumCoherence:F2}_{fieldSize:F2}";
            if (_geometryCache.TryGetValue(cacheKey, out var cachedGeometry))
            {
                Interlocked.Increment(ref _cacheHits);
                return cachedGeometry;
            }
            
            // For synchronous calls, generate directly
            Interlocked.Increment(ref _cacheMisses);
            var task = new GeometryGenerationTask
            {
                TaskType = GeometryTaskType.QuantumField,
                CacheKey = cacheKey,
                Parameters = new Dictionary<string, object>
                {
                    ["quantumCoherence"] = quantumCoherence,
                    ["fieldSize"] = fieldSize
                }
            };
            
            var geometry = GenerateQuantumField(task);
            
            // Cache the result
            _geometryCache.TryAdd(cacheKey, geometry);
            Interlocked.Increment(ref _geometriesGenerated);
            
            return geometry;
        }
        
        /// <summary>
        /// Creates a quantum field asynchronously for better performance
        /// </summary>
        public async Task<Model3DGroup> CreateQuantumFieldAsync(double quantumCoherence, double fieldSize = 5.0)
        {
            var cacheKey = $"quantum_field_{quantumCoherence:F2}_{fieldSize:F2}";
            var task = new GeometryGenerationTask
            {
                TaskType = GeometryTaskType.QuantumField,
                CacheKey = cacheKey,
                Parameters = new Dictionary<string, object>
                {
                    ["quantumCoherence"] = quantumCoherence,
                    ["fieldSize"] = fieldSize
                }
            };
            
            var geometry = await GenerateGeometrySync(task);
            return geometry ?? new Model3DGroup();
        }
        
        /// <summary>
        /// Creates a fractal tree structure representing consciousness hierarchy
        /// </summary>
        public Model3DGroup CreateFractalConsciousnessTree(double fractalComplexity, double baseHeight = 2.0)
        {
            var cacheKey = $"fractal_tree_{fractalComplexity:F2}_{baseHeight:F2}";
            if (_geometryCache.ContainsKey(cacheKey))
            {
                return _geometryCache[cacheKey];
            }
            
            var group = new Model3DGroup();
            var iterations = (int)(FRACTAL_ITERATIONS * fractalComplexity);
            
            // Create recursive fractal branches
            CreateFractalBranch(group, new Point3D(0, 0, 0), new Vector3D(0, 1, 0), baseHeight, iterations, fractalComplexity);
            
            _geometryCache[cacheKey] = group;
            return group;
        }
        
        /// <summary>
        /// Creates a torus knot representing universal consciousness loops
        /// </summary>
        public Model3DGroup CreateUniversalConsciousnessKnot(double[] geometricState, double scale = 1.0)
        {
            var cacheKey = $"consciousness_knot_{string.Join("_", geometricState.Take(4).Select(x => x.ToString("F2")))}_{scale:F2}";
            if (_geometryCache.ContainsKey(cacheKey))
            {
                return _geometryCache[cacheKey];
            }
            
            var group = new Model3DGroup();
            
            // Extract parameters from geometric state
            var p = 3 + (int)(geometricState[0] * 5); // Winding parameter
            var q = 2 + (int)(geometricState[1] * 3); // Rotation parameter
            var radius1 = 1.0 + geometricState[2] * 0.5;
            var radius2 = 0.3 + geometricState[3] * 0.2;
            
            var knotGeometry = CreateTorusKnotGeometry(p, q, radius1, radius2, scale);
            var knotModel = new GeometryModel3D(knotGeometry, _materialCache["holographic"]);
            group.Children.Add(knotModel);
            
            _geometryCache[cacheKey] = group;
            return group;
        }
        
        /// <summary>
        /// Creates emergence event visualization - sudden spikes and bursts
        /// </summary>
        public Model3DGroup CreateEmergenceEvent(double emergenceLevel, Point3D center)
        {
            var group = new Model3DGroup();
            
            if (emergenceLevel < 0.5) return group;
            
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
        
        /// <summary>
        /// Creates a holographic information surface
        /// </summary>
        public Model3DGroup CreateHolographicInfoSurface(Dictionary<string, object> metrics, double size = 3.0)
        {
            var group = new Model3DGroup();
            
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
        
        public void ClearCache()
        {
            _geometryCache.Clear();
            _logger.LogInformation("Geometry cache cleared");
        }

        /// <summary>
        /// Creates a fractal tree structure with time-based animation
        /// </summary>
        public Model3DGroup CreateFractalTree(double fractalComplexity, int iterations)
        {
            var cacheKey = $"fractal_tree_{fractalComplexity:F2}_{iterations}";
            if (_geometryCache.ContainsKey(cacheKey))
            {
                return _geometryCache[cacheKey];
            }

            var group = new Model3DGroup();
            var treeGeometry = CreateTreeBranch(new Point3D(0, -1, 0), new Vector3D(0, 1, 0), 
                                               1.0, iterations, fractalComplexity);
            
            var treeModel = new GeometryModel3D(treeGeometry, _materialCache["fractal"]);
            group.Children.Add(treeModel);
            
            _geometryCache[cacheKey] = group;
            return group;
        }

        /// <summary>
        /// Creates a universal knot representing cosmic interconnectedness
        /// </summary>
        public Model3DGroup CreateUniversalKnot(double universalResonance, double time)
        {
            var cacheKey = $"universal_knot_{universalResonance:F2}_{time:F1}";
            if (_geometryCache.ContainsKey(cacheKey))
            {
                return _geometryCache[cacheKey];
            }

            var group = new Model3DGroup();
            var knotGeometry = CreateTorusKnot(universalResonance, time);
            
            var knotModel = new GeometryModel3D(knotGeometry, _materialCache["consciousness"]);
            group.Children.Add(knotModel);
            
            _geometryCache[cacheKey] = group;
            return group;
        }

        /// <summary>
        /// Creates a holographic surface with interference patterns
        /// </summary>
        public Model3DGroup CreateHolographicSurface(double holographicDensity, double time)
        {
            var cacheKey = $"holographic_surface_{holographicDensity:F2}_{time:F1}";
            if (_geometryCache.ContainsKey(cacheKey))
            {
                return _geometryCache[cacheKey];
            }

            var group = new Model3DGroup();
            var surfaceGeometry = CreateHolographicPlane(holographicDensity, time);
            
            var surfaceModel = new GeometryModel3D(surfaceGeometry, _materialCache["holographic"]);
            group.Children.Add(surfaceModel);
            
            _geometryCache[cacheKey] = group;
            return group;
        }

        /// <summary>
        /// Creates an enhanced quantum field with time-based evolution
        /// </summary>
        public Model3DGroup CreateQuantumFieldWithTime(double quantumCoherence, double time)
        {
            var cacheKey = $"quantum_field_time_{quantumCoherence:F2}_{time:F1}";
            if (_geometryCache.ContainsKey(cacheKey))
            {
                return _geometryCache[cacheKey];
            }

            var group = new Model3DGroup();
            
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
            
            _geometryCache[cacheKey] = group;
            return group;
        }
        
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
            var tubeRadius = 0.2;
            var p = 2; // Knot parameter
            var q = 3; // Knot parameter
            
            for (int i = 0; i < segments; i++)
            {
                var t = i * TAU / segments + time * 0.1;
                
                // Torus knot equations
                var r = Math.Cos(q * t) + 2;
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
            var epsilon = 0.01;
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
        
        #endregion

        /// <summary>
        /// Background worker loop for parallel geometry generation
        /// </summary>
        private async Task GeometryWorkerLoop(int workerId, CancellationToken cancellationToken)
        {
            _logger.LogDebug($"Geometry worker {workerId} started");
            
            while (!cancellationToken.IsCancellationRequested)
            {
                try
                {
                    if (_generationQueue.TryDequeue(out var task))
                    {
                        await _geometryGenerationSemaphore.WaitAsync(cancellationToken);
                        
                        try
                        {
                            task.WorkerId = workerId;
                            task.StartTime = DateTime.UtcNow;
                            
                            var geometry = await GenerateGeometryAsync(task);
                            
                            task.CompletedTime = DateTime.UtcNow;
                            task.IsCompleted = true;
                            task.Result = geometry;
                            
                            if (geometry != null)
                            {
                                // Cache the result if it has a cache key
                                if (!string.IsNullOrEmpty(task.CacheKey))
                                {
                                    _geometryCache.TryAdd(task.CacheKey, geometry);
                                }
                                
                                OnGeometryGenerated(new GeometryGeneratedEventArgs(task, geometry));
                                Interlocked.Increment(ref _geometriesGenerated);
                            }
                        }
                        finally
                        {
                            _geometryGenerationSemaphore.Release();
                        }
                    }
                    else
                    {
                        // No tasks in queue, wait a bit
                        await Task.Delay(10, cancellationToken);
                    }
                }
                catch (OperationCanceledException)
                {
                    break;
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, $"Error in geometry worker {workerId}");
                    await Task.Delay(1000, cancellationToken); // Brief pause on error
                }
            }
            
            _logger.LogDebug($"Geometry worker {workerId} stopped");
        }
        
        /// <summary>
        /// Asynchronously generate geometry based on task type
        /// </summary>
        private async Task<Model3DGroup?> GenerateGeometryAsync(GeometryGenerationTask task)
        {
            return await Task.Run(() =>
            {
                try
                {
                    return task.TaskType switch
                    {
                        GeometryTaskType.ConsciousnessSphere => GenerateConsciousnessSphere(task),
                        GeometryTaskType.QuantumField => GenerateQuantumField(task),
                        GeometryTaskType.FractalPattern => GenerateFractalPattern(task),
                        GeometryTaskType.TachyonicStructure => GenerateTachyonicStructure(task),
                        GeometryTaskType.HolographicInterface => GenerateHolographicInterface(task),
                        _ => null
                    };
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, $"Error generating geometry for task {task.Id}");
                    OnGeometryError(new GeometryErrorEventArgs(task, ex));
                    return null;
                }
            });
        }
        
        /// <summary>
        /// Queue geometry generation task asynchronously
        /// </summary>
        public async Task<bool> QueueGeometryGeneration(GeometryGenerationTask task)
        {
            if (_cancellationTokenSource.Token.IsCancellationRequested)
                return false;
                
            // Check cache first if cache key is provided
            if (!string.IsNullOrEmpty(task.CacheKey) && _geometryCache.TryGetValue(task.CacheKey, out var cachedGeometry))
            {
                Interlocked.Increment(ref _cacheHits);
                OnGeometryGenerated(new GeometryGeneratedEventArgs(task, cachedGeometry));
                return true;
            }
            
            Interlocked.Increment(ref _cacheMisses);
            task.QueuedTime = DateTime.UtcNow;
            task.Id = Guid.NewGuid();
            
            _generationQueue.Enqueue(task);
            _logger.LogTrace($"Queued geometry generation task {task.Id} of type {task.TaskType}");
            
            return true;
        }
        
        /// <summary>
        /// Generate geometry synchronously for immediate use
        /// </summary>
        public async Task<Model3DGroup?> GenerateGeometrySync(GeometryGenerationTask task)
        {
            // Check cache first
            if (!string.IsNullOrEmpty(task.CacheKey) && _geometryCache.TryGetValue(task.CacheKey, out var cachedGeometry))
            {
                Interlocked.Increment(ref _cacheHits);
                return cachedGeometry;
            }
            
            Interlocked.Increment(ref _cacheMisses);
            var geometry = await GenerateGeometryAsync(task);
            
            // Cache the result if successful
            if (geometry != null && !string.IsNullOrEmpty(task.CacheKey))
            {
                _geometryCache.TryAdd(task.CacheKey, geometry);
            }
            
            return geometry;
        }
        
        /// <summary>
        /// Generate consciousness sphere geometry
        /// </summary>
        private Model3DGroup GenerateConsciousnessSphere(GeometryGenerationTask task)
        {
            var consciousnessLevel = task.Parameters.TryGetValue("consciousnessLevel", out var cl) ? (double)cl : 0.5;
            var radius = task.Parameters.TryGetValue("radius", out var r) ? (double)r : 1.0;
            
            var group = new Model3DGroup();
            
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
            
            return group;
        }
        
        /// <summary>
        /// Generate quantum field geometry
        /// </summary>
        private Model3DGroup GenerateQuantumField(GeometryGenerationTask task)
        {
            var quantumCoherence = task.Parameters.TryGetValue("quantumCoherence", out var qc) ? (double)qc : 0.5;
            var fieldSize = task.Parameters.TryGetValue("fieldSize", out var fs) ? (double)fs : 5.0;
            
            var group = new Model3DGroup();
            
            // Create wave interference pattern
            var waveResolution = 64;
            var waveGeometry = new MeshGeometry3D();
            
            for (int x = 0; x < waveResolution; x++)
            {
                for (int z = 0; z < waveResolution; z++)
                {
                    var xPos = (x / (double)(waveResolution - 1) - 0.5) * fieldSize;
                    var zPos = (z / (double)(waveResolution - 1) - 0.5) * fieldSize;
                    
                    // Quantum wave function with interference
                    var wave1 = Math.Sin(xPos * 2) * Math.Cos(zPos * 2);
                    var wave2 = Math.Sin(xPos * 3 + Math.PI / 4) * Math.Cos(zPos * 3 + Math.PI / 4);
                    var yPos = (wave1 + wave2) * quantumCoherence * 0.5;
                    
                    waveGeometry.Positions.Add(new Point3D(xPos, yPos, zPos));
                }
            }
            
            // Generate triangles for the wave mesh
            for (int x = 0; x < waveResolution - 1; x++)
            {
                for (int z = 0; z < waveResolution - 1; z++)
                {
                    var i = x * waveResolution + z;
                    
                    // First triangle
                    waveGeometry.TriangleIndices.Add(i);
                    waveGeometry.TriangleIndices.Add(i + waveResolution + 1);
                    waveGeometry.TriangleIndices.Add(i + 1);
                    
                    // Second triangle
                    waveGeometry.TriangleIndices.Add(i);
                    waveGeometry.TriangleIndices.Add(i + waveResolution);
                    waveGeometry.TriangleIndices.Add(i + waveResolution + 1);
                }
            }
            
            var waveModel = new GeometryModel3D(waveGeometry, _materialCache["quantum"]);
            group.Children.Add(waveModel);
            
            return group;
        }
        
        /// <summary>
        /// Generate fractal pattern geometry
        /// </summary>
        private Model3DGroup GenerateFractalPattern(GeometryGenerationTask task)
        {
            var complexity = task.Parameters.TryGetValue("complexity", out var c) ? (double)c : 0.5;
            var scale = task.Parameters.TryGetValue("scale", out var s) ? (double)s : 1.0;
            
            return CreateFractalPatterns(scale, complexity);
        }
        
        /// <summary>
        /// Generate tachyonic structure geometry
        /// </summary>
        private Model3DGroup GenerateTachyonicStructure(GeometryGenerationTask task)
        {
            var resonance = task.Parameters.TryGetValue("resonance", out var r) ? (double)r : 0.5;
            var fieldStrength = task.Parameters.TryGetValue("fieldStrength", out var f) ? (double)f : 1.0;
            
            var group = new Model3DGroup();
            
            // Create tachyonic field lines
            var lineCount = (int)(20 * resonance + 10);
            for (int i = 0; i < lineCount; i++)
            {
                var angle = (i / (double)lineCount) * TAU;
                var line = CreateTachyonicFieldLine(angle, fieldStrength, resonance);
                group.Children.Add(line);
            }
            
            return group;
        }
        
        /// <summary>
        /// Generate holographic interface geometry
        /// </summary>
        private Model3DGroup GenerateHolographicInterface(GeometryGenerationTask task)
        {
            var interfaceLevel = task.Parameters.TryGetValue("interfaceLevel", out var il) ? (double)il : 0.5;
            var size = task.Parameters.TryGetValue("size", out var s) ? (double)s : 2.0;
            
            var group = new Model3DGroup();
            
            // Create holographic panels
            var panelCount = (int)(interfaceLevel * 8 + 4);
            for (int i = 0; i < panelCount; i++)
            {
                var panel = CreateHolographicPanel(i, panelCount, size, interfaceLevel);
                group.Children.Add(panel);
            }
            
            return group;
        }
        
        /// <summary>
        /// Create a tachyonic field line
        /// </summary>
        private Model3DGroup CreateTachyonicFieldLine(double angle, double fieldStrength, double resonance)
        {
            var group = new Model3DGroup();
            var geometry = new MeshGeometry3D();
            
            var segments = 100;
            var radius = 0.02 * fieldStrength;
            
            for (int i = 0; i < segments; i++)
            {
                var t = i / (double)(segments - 1);
                var spiralRadius = 2 * t;
                var height = (t - 0.5) * 4;
                
                var x = spiralRadius * Math.Cos(angle + t * TAU * 3 * resonance);
                var y = height;
                var z = spiralRadius * Math.Sin(angle + t * TAU * 3 * resonance);
                
                geometry.Positions.Add(new Point3D(x, y, z));
            }
            
            // Create line segments
            for (int i = 0; i < segments - 1; i++)
            {
                var cylinderGeometry = CreateCylinderBetweenPoints(
                    geometry.Positions[i], 
                    geometry.Positions[i + 1], 
                    radius);
                    
                var cylinderModel = new GeometryModel3D(cylinderGeometry, _materialCache["holographic"]);
                group.Children.Add(cylinderModel);
            }
            
            return group;
        }
        
        /// <summary>
        /// Create a holographic panel
        /// </summary>
        private Model3DGroup CreateHolographicPanel(int index, int totalPanels, double size, double interfaceLevel)
        {
            var group = new Model3DGroup();
            var geometry = new MeshGeometry3D();
            
            var angle = (index / (double)totalPanels) * TAU;
            var distance = size * 0.8;
            var panelSize = size * 0.3 * interfaceLevel;
            
            var centerX = distance * Math.Cos(angle);
            var centerZ = distance * Math.Sin(angle);
            var centerY = 0;
            
            // Create panel vertices
            geometry.Positions.Add(new Point3D(centerX - panelSize, centerY - panelSize, centerZ));
            geometry.Positions.Add(new Point3D(centerX + panelSize, centerY - panelSize, centerZ));
            geometry.Positions.Add(new Point3D(centerX + panelSize, centerY + panelSize, centerZ));
            geometry.Positions.Add(new Point3D(centerX - panelSize, centerY + panelSize, centerZ));
            
            // Create panel triangles
            geometry.TriangleIndices.Add(0);
            geometry.TriangleIndices.Add(1);
            geometry.TriangleIndices.Add(2);
            geometry.TriangleIndices.Add(0);
            geometry.TriangleIndices.Add(2);
            geometry.TriangleIndices.Add(3);
            
            var panelModel = new GeometryModel3D(geometry, _materialCache["holographic"]);
            group.Children.Add(panelModel);
            
            return group;
        }
        
        /// <summary>
        /// Create cylinder between two points
        /// </summary>
        private MeshGeometry3D CreateCylinderBetweenPoints(Point3D start, Point3D end, double radius)
        {
            var geometry = new MeshGeometry3D();
            var direction = end - start;
            var length = direction.Length;
            
            if (length < double.Epsilon)
                return geometry;
                
            var segments = 8;
            
            // Create cylinder vertices
            for (int i = 0; i <= segments; i++)
            {
                var angle = (i / (double)segments) * TAU;
                var x = radius * Math.Cos(angle);
                var z = radius * Math.Sin(angle);
                
                geometry.Positions.Add(new Point3D(start.X + x, start.Y, start.Z + z));
                geometry.Positions.Add(new Point3D(end.X + x, end.Y, end.Z + z));
            }
            
            // Create cylinder triangles
            for (int i = 0; i < segments; i++)
            {
                var i1 = i * 2;
                var i2 = (i + 1) * 2;
                
                // First triangle
                geometry.TriangleIndices.Add(i1);
                geometry.TriangleIndices.Add(i2);
                geometry.TriangleIndices.Add(i1 + 1);
                
                // Second triangle
                geometry.TriangleIndices.Add(i1 + 1);
                geometry.TriangleIndices.Add(i2);
                geometry.TriangleIndices.Add(i2 + 1);
            }
            
            return geometry;
        }
        
        /// <summary>
        /// Raise geometry generated event
        /// </summary>
        private void OnGeometryGenerated(GeometryGeneratedEventArgs args)
        {
            try
            {
                GeometryGenerated?.Invoke(this, args);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in GeometryGenerated event handler");
            }
        }
        
        /// <summary>
        /// Raise geometry error event
        /// </summary>
        private void OnGeometryError(GeometryErrorEventArgs args)
        {
            try
            {
                GeometryError?.Invoke(this, args);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in GeometryError event handler");
            }
        }
        
        /// <summary>
        /// Get current engine statistics
        /// </summary>
        public GeometryEngineStatistics GetStatistics()
        {
            return new GeometryEngineStatistics
            {
                GeometriesGenerated = _geometriesGenerated,
                CacheHits = _cacheHits,
                CacheMisses = _cacheMisses,
                CacheSize = _geometryCache.Count,
                WorkerThreadCount = _workerThreadCount,
                QueueLength = _generationQueue.Count,
                Timestamp = DateTime.UtcNow
            };
        }
        
        public void Dispose()
        {
            try
            {
                _cancellationTokenSource.Cancel();
                
                // Wait for worker tasks to complete
                if (_workerTasks != null)
                {
                    Task.WaitAll(_workerTasks, TimeSpan.FromSeconds(5));
                }
                
                _cancellationTokenSource.Dispose();
                _geometryGenerationSemaphore.Dispose();
                
                _logger.LogInformation("Multi-threaded consciousness geometry engine disposed");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error disposing ConsciousnessGeometryEngine");
            }
        }
    }
    
    /// <summary>
    /// Geometry generation task for background processing
    /// </summary>
    public class GeometryGenerationTask
    {
        public Guid Id { get; set; }
        public GeometryTaskType TaskType { get; set; }
        public string? CacheKey { get; set; }
        public DateTime QueuedTime { get; set; }
        public DateTime StartTime { get; set; }
        public DateTime CompletedTime { get; set; }
        public int WorkerId { get; set; }
        public bool IsCompleted { get; set; }
        public Dictionary<string, object> Parameters { get; set; } = new();
        public Model3DGroup? Result { get; set; }
    }
    
    /// <summary>
    /// Types of geometry generation tasks
    /// </summary>
    public enum GeometryTaskType
    {
        ConsciousnessSphere,
        QuantumField,
        FractalPattern,
        TachyonicStructure,
        HolographicInterface
    }
    
    /// <summary>
    /// Geometry engine statistics
    /// </summary>
    public class GeometryEngineStatistics
    {
        public int GeometriesGenerated { get; set; }
        public int CacheHits { get; set; }
        public int CacheMisses { get; set; }
        public int CacheSize { get; set; }
        public int WorkerThreadCount { get; set; }
        public int QueueLength { get; set; }
        public DateTime Timestamp { get; set; }
        public double CacheHitRatio => (CacheHits + CacheMisses) > 0 ? (double)CacheHits / (CacheHits + CacheMisses) : 0;
    }
    
    /// <summary>
    /// Event args for geometry generation completion
    /// </summary>
    public class GeometryGeneratedEventArgs : EventArgs
    {
        public GeometryGenerationTask Task { get; }
        public Model3DGroup Geometry { get; }
        
        public GeometryGeneratedEventArgs(GeometryGenerationTask task, Model3DGroup geometry)
        {
            Task = task;
            Geometry = geometry;
        }
    }
    
    /// <summary>
    /// Event args for geometry generation errors
    /// </summary>
    public class GeometryErrorEventArgs : EventArgs
    {
        public GeometryGenerationTask Task { get; }
        public Exception Error { get; }
        
        public GeometryErrorEventArgs(GeometryGenerationTask task, Exception error)
        {
            Task = task;
            Error = error;
        }
    }
}
