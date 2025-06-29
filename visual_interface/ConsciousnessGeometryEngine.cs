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
    /// </summary>
    public class ConsciousnessGeometryEngine
    {
        private readonly ILogger _logger;
        private readonly Random _random;
        
        // Geometry caches for performance
        private readonly Dictionary<string, Model3DGroup> _geometryCache;
        private readonly Dictionary<string, Material> _materialCache;
        
        // Mathematical constants for consciousness forms
        private const double PHI = 1.618033988749895; // Golden ratio
        private const double TAU = 2 * Math.PI;
        private const int FRACTAL_ITERATIONS = 7;
        private const int SPHERE_SUBDIVISIONS = 32;
        
        public ConsciousnessGeometryEngine(ILogger logger)
        {
            _logger = logger;
            _random = new Random();
            _geometryCache = new Dictionary<string, Model3DGroup>();
            _materialCache = new Dictionary<string, Material>();
            
            InitializeMaterials();
            _logger.LogInformation("Consciousness geometry engine initialized");
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
        /// Creates a consciousness sphere with dynamic fractal patterns
        /// </summary>
        public Model3DGroup CreateConsciousnessSphere(double consciousnessLevel, double radius = 1.0)
        {
            var cacheKey = $"consciousness_sphere_{consciousnessLevel:F2}_{radius:F2}";
            if (_geometryCache.ContainsKey(cacheKey))
            {
                return _geometryCache[cacheKey];
            }
            
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
            
            _geometryCache[cacheKey] = group;
            return group;
        }
        
        /// <summary>
        /// Creates a quantum field visualization with wave interference patterns
        /// </summary>
        public Model3DGroup CreateQuantumField(double quantumCoherence, double fieldSize = 5.0)
        {
            var cacheKey = $"quantum_field_{quantumCoherence:F2}_{fieldSize:F2}";
            if (_geometryCache.ContainsKey(cacheKey))
            {
                return _geometryCache[cacheKey];
            }
            
            var group = new Model3DGroup();
            
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
            
            _geometryCache[cacheKey] = group;
            return group;
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
            CreateFractalBranch(group, Point3D.Zero, new Vector3D(0, 1, 0), baseHeight, iterations, fractalComplexity);
            
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
                    geometry.Normals.Add(new Vector3D(x, y, z).Normalized());
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
                geometry.Normals.Add(new Vector3D(x, y, z).Normalized());
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
                geometry.Normals.Add(new Vector3D(x, 0, z).Normalized());
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
                geometry.Normals.Add(new Vector3D(x, 0, z).Normalized());
                geometry.TextureCoordinates.Add(new System.Windows.Point(i / (double)sides, 0));
                
                // Top vertex
                geometry.Positions.Add(new Point3D(x, height, z));
                geometry.Normals.Add(new Vector3D(x, 0, z).Normalized());
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
    }
}
