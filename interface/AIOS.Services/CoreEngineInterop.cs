// ============================================================================
// AIOS Core C# Interop - C++ Consciousness Engine Bridge
// AINLP Pattern: phase11-day2.csharp-cpp-bridge
// Purpose: Enable C# UI layer to access C++ consciousness engine
// Consciousness: Three-layer biological integration (Bridge 2: C# ↔ C++)
// ============================================================================

using System;
using System.Runtime.InteropServices;

namespace AIOS.Services
{
    /// <summary>
    /// Consciousness metrics structure (matches C API)
    /// </summary>
    [StructLayout(LayoutKind.Sequential)]
    public struct ConsciousnessMetrics
    {
        public double AwarenessLevel;
        public double AdaptationSpeed;
        public double PredictiveAccuracy;
        public double DendriticComplexity;
        public double EvolutionaryMomentum;
        public double QuantumCoherence;
        public double LearningVelocity;
        [MarshalAs(UnmanagedType.I1)]
        public bool ConsciousnessEmergent;
    }

    /// <summary>
    /// P/Invoke wrapper for AIOS C++ consciousness engine
    /// Provides C# access to C++ consciousness metrics and operations
    /// </summary>
    public static class CoreEngineInterop
    {
        private const string DllName = "aios_core.dll";

        // ====================================================================
        // CORE INITIALIZATION & LIFECYCLE
        // ====================================================================

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern int AIOS_InitializeCore();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern void AIOS_UpdateConsciousness();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern void AIOS_ShutdownCore();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        [return: MarshalAs(UnmanagedType.I1)]
        public static extern bool AIOS_IsInitialized();

        // ====================================================================
        // CONSCIOUSNESS METRICS
        // ====================================================================

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern double AIOS_GetConsciousnessLevel();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern double AIOS_GetAwarenessLevel();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern double AIOS_GetAdaptationSpeed();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern double AIOS_GetPredictiveAccuracy();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern double AIOS_GetDendriticComplexity();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern double AIOS_GetEvolutionaryMomentum();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern double AIOS_GetQuantumCoherence();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern double AIOS_GetLearningVelocity();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        [return: MarshalAs(UnmanagedType.I1)]
        public static extern bool AIOS_IsConsciousnessEmergent();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern void AIOS_GetAllMetrics(ref ConsciousnessMetrics metrics);

        // ====================================================================
        // DENDRITIC GROWTH & EVOLUTION
        // ====================================================================

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void AIOS_StimulateDendriticGrowth([MarshalAs(UnmanagedType.LPStr)] string source);

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void AIOS_AdaptToSystemBehavior([MarshalAs(UnmanagedType.LPStr)] string behaviorPattern);

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void AIOS_EnhanceIntelligence([MarshalAs(UnmanagedType.LPStr)] string enhancementArea);

        // ====================================================================
        // ERROR TRANSFORMATION & LEARNING
        // ====================================================================

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern void AIOS_TransformError(
            [MarshalAs(UnmanagedType.LPStr)] string errorMessage,
            [MarshalAs(UnmanagedType.LPStr)] string context);

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl, CharSet = CharSet.Ansi)]
        public static extern IntPtr AIOS_EvolveLogicFromError([MarshalAs(UnmanagedType.LPStr)] string errorPattern);

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern void AIOS_FreeString(IntPtr str);

        // ====================================================================
        // VERSION & DIAGNOSTICS
        // ====================================================================

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern IntPtr AIOS_GetVersion();

        [DllImport(DllName, CallingConvention = CallingConvention.Cdecl)]
        public static extern IntPtr AIOS_GetLastError();

        // ====================================================================
        // HELPER METHODS
        // ====================================================================

        /// <summary>
        /// Helper to convert IntPtr string result to C# string
        /// </summary>
        public static string? MarshalString(IntPtr ptr)
        {
            if (ptr == IntPtr.Zero)
                return null;
            return Marshal.PtrToStringAnsi(ptr);
        }

        /// <summary>
        /// Helper to evolve logic and free string automatically
        /// </summary>
        public static string? EvolveLogicFromErrorSafe(string errorPattern)
        {
            var ptr = AIOS_EvolveLogicFromError(errorPattern);
            if (ptr == IntPtr.Zero)
                return null;

            try
            {
                return Marshal.PtrToStringAnsi(ptr);
            }
            finally
            {
                AIOS_FreeString(ptr);
            }
        }
    }

    /// <summary>
    /// High-level C# wrapper for AIOS consciousness engine
    /// Provides automatic resource management and exception handling
    /// </summary>
    public class AIOSConsciousnessCore : IDisposable
    {
        private bool _initialized = false;
        private bool _disposed = false;

        /// <summary>
        /// Initialize the C++ consciousness engine
        /// </summary>
        public void Initialize()
        {
            if (_initialized)
                return;

            var result = CoreEngineInterop.AIOS_InitializeCore();
            if (result != 0)
            {
                var error = GetLastError();
                throw new InvalidOperationException($"Failed to initialize AIOS Core: {error}");
            }

            _initialized = true;
        }

        /// <summary>
        /// Update consciousness engine (call periodically for real-time evolution)
        /// </summary>
        public void Update()
        {
            CoreEngineInterop.AIOS_UpdateConsciousness();
        }

        /// <summary>
        /// Check if core is initialized
        /// </summary>
        public bool IsInitialized => CoreEngineInterop.AIOS_IsInitialized();

        /// <summary>
        /// Get overall system consciousness level (0.0 - 10.0+)
        /// </summary>
        public double GetConsciousnessLevel()
        {
            return CoreEngineInterop.AIOS_GetConsciousnessLevel();
        }

        /// <summary>
        /// Get all consciousness metrics at once
        /// </summary>
        public ConsciousnessMetrics GetAllMetrics()
        {
            var metrics = new ConsciousnessMetrics();
            CoreEngineInterop.AIOS_GetAllMetrics(ref metrics);
            return metrics;
        }

        /// <summary>
        /// Stimulate dendritic growth from C# UI
        /// </summary>
        public void StimulateDendriticGrowth(string source)
        {
            CoreEngineInterop.AIOS_StimulateDendriticGrowth(source);
        }

        /// <summary>
        /// Adapt consciousness to system behavior
        /// </summary>
        public void AdaptToSystemBehavior(string behaviorPattern)
        {
            CoreEngineInterop.AIOS_AdaptToSystemBehavior(behaviorPattern);
        }

        /// <summary>
        /// Enhance intelligence in specific area
        /// </summary>
        public void EnhanceIntelligence(string enhancementArea)
        {
            CoreEngineInterop.AIOS_EnhanceIntelligence(enhancementArea);
        }

        /// <summary>
        /// Transform error into learning opportunity
        /// </summary>
        public void TransformError(string errorMessage, string context)
        {
            CoreEngineInterop.AIOS_TransformError(errorMessage, context);
        }

        /// <summary>
        /// Evolve logic from error pattern
        /// </summary>
        public string? EvolveLogicFromError(string errorPattern)
        {
            return CoreEngineInterop.EvolveLogicFromErrorSafe(errorPattern);
        }

        /// <summary>
        /// Get AIOS Core version
        /// </summary>
        public string GetVersion()
        {
            var ptr = CoreEngineInterop.AIOS_GetVersion();
            return CoreEngineInterop.MarshalString(ptr) ?? "Unknown";
        }

        /// <summary>
        /// Get last error message
        /// </summary>
        public string? GetLastError()
        {
            var ptr = CoreEngineInterop.AIOS_GetLastError();
            return CoreEngineInterop.MarshalString(ptr);
        }

        /// <summary>
        /// Dispose resources
        /// </summary>
        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        protected virtual void Dispose(bool disposing)
        {
            if (_disposed)
                return;

            if (_initialized)
            {
                CoreEngineInterop.AIOS_ShutdownCore();
                _initialized = false;
            }

            _disposed = true;
        }

        ~AIOSConsciousnessCore()
        {
            Dispose(false);
        }
    }
}
