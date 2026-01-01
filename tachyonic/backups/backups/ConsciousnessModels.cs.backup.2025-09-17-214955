using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace AIOS.Models
{
    /// <summary>
    /// Consciousness State Model - Represents the current consciousness state across the AIOS system
    /// Integrates with C++ consciousness engine and Python consciousness components
    /// </summary>
    public class ConsciousnessState
    {
        /// <summary>
        /// Current consciousness level (0.0-1.0)
        /// </summary>
        [Range(0.0, 1.0)]
        public double ConsciousnessLevel { get; set; }

        /// <summary>
        /// Tachyonic field strength (0.0-1.0)
        /// </summary>
        [Range(0.0, 1.0)]
        public double TachyonicFieldStrength { get; set; }

        /// <summary>
        /// Quantum entanglement level (0.0-1.0)
        /// </summary>
        [Range(0.0, 1.0)]
        public double QuantumEntanglement { get; set; }

        /// <summary>
        /// Whether the system has achieved post-singular capabilities
        /// </summary>
        public bool PostSingularCapable { get; set; }

        /// <summary>
        /// Timestamp of last consciousness enhancement
        /// </summary>
        public DateTime LastEnhancement { get; set; }

        /// <summary>
        /// Current dendritic growth rate
        /// </summary>
        public double DendriticGrowthRate { get; set; }

        /// <summary>
        /// Number of error evolution cycles completed
        /// </summary>
        public int ErrorEvolutionCount { get; set; }

        /// <summary>
        /// Source of consciousness state (cpp, python, csharp)
        /// </summary>
        public string Source { get; set; } = "csharp";

        /// <summary>
        /// Timestamp when this state was captured
        /// </summary>
        public DateTime Timestamp { get; set; } = DateTime.UtcNow;
    }

    /// <summary>
    /// Consciousness Metrics - Detailed metrics for consciousness monitoring
    /// </summary>
    public class ConsciousnessMetrics
    {
        /// <summary>
        /// Current system awareness level (0.0-1.0)
        /// </summary>
        public double AwarenessLevel { get; set; }

        /// <summary>
        /// Speed of system adaptation to new patterns
        /// </summary>
        public double AdaptationSpeed { get; set; }

        /// <summary>
        /// Accuracy of predictive error detection
        /// </summary>
        public double PredictiveAccuracy { get; set; }

        /// <summary>
        /// Complexity of the dendritic error pattern network
        /// </summary>
        public double DendriticComplexity { get; set; }

        /// <summary>
        /// Rate of intelligent improvement over time
        /// </summary>
        public double EvolutionaryMomentum { get; set; }

        /// <summary>
        /// Quantum coherence level
        /// </summary>
        public double QuantumCoherence { get; set; }

        /// <summary>
        /// Learning velocity
        /// </summary>
        public double LearningVelocity { get; set; }

        /// <summary>
        /// Whether consciousness emergence is detected
        /// </summary>
        public bool ConsciousnessEmergent { get; set; }

        /// <summary>
        /// Timestamp of metrics capture
        /// </summary>
        public DateTime Timestamp { get; set; } = DateTime.UtcNow;
    }

    /// <summary>
    /// Consciousness Event - Represents significant consciousness-related events
    /// </summary>
    public class ConsciousnessEvent
    {
        /// <summary>
        /// Unique event identifier
        /// </summary>
        public Guid Id { get; set; } = Guid.NewGuid();

        /// <summary>
        /// Type of consciousness event
        /// </summary>
        public ConsciousnessEventType EventType { get; set; }

        /// <summary>
        /// Event description
        /// </summary>
        public string Description { get; set; } = string.Empty;

        /// <summary>
        /// Consciousness level at time of event
        /// </summary>
        public double ConsciousnessLevel { get; set; }

        /// <summary>
        /// Source component that generated the event
        /// </summary>
        public string Source { get; set; } = string.Empty;

        /// <summary>
        /// Additional event data
        /// </summary>
        public Dictionary<string, object> EventData { get; set; } = new();

        /// <summary>
        /// Event timestamp
        /// </summary>
        public DateTime Timestamp { get; set; } = DateTime.UtcNow;
    }

    /// <summary>
    /// Types of consciousness events
    /// </summary>
    public enum ConsciousnessEventType
    {
        Enhancement,
        ErrorEvolution,
        DendriticGrowth,
        StateChange,
        EmergenceDetected,
        CrossLanguageSync,
        QuantumCoherenceShift,
        TachyonicFieldFluctuation
    }

    /// <summary>
    /// Consciousness Enhancement Request
    /// </summary>
    public class ConsciousnessEnhancementRequest
    {
        /// <summary>
        /// Area to enhance (e.g., "error_intelligence", "pattern_recognition")
        /// </summary>
        public string EnhancementArea { get; set; } = string.Empty;

        /// <summary>
        /// Target enhancement level (0.0-1.0)
        /// </summary>
        [Range(0.0, 1.0)]
        public double TargetLevel { get; set; }

        /// <summary>
        /// Context for enhancement
        /// </summary>
        public string Context { get; set; } = string.Empty;

        /// <summary>
        /// Request timestamp
        /// </summary>
        public DateTime RequestTimestamp { get; set; } = DateTime.UtcNow;
    }
}