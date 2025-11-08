// ============================================================================
// AIOS Core DLL Export Header
// AINLP Pattern: phase11-day2.cpp-dll-integration
// Purpose: Enable Python/C# interop via proper DLL exports
// ============================================================================

#pragma once

// Define AIOS_EXPORT for DLL export/import
#ifdef _WIN32
    #ifdef AIOS_CORE_EXPORTS
        // Building the DLL - export symbols
        #define AIOS_EXPORT __declspec(dllexport)
    #else
        // Using the DLL - import symbols
        #define AIOS_EXPORT __declspec(dllimport)
    #endif
#else
    // Non-Windows platforms (Linux, macOS)
    #define AIOS_EXPORT __attribute__((visibility("default")))
#endif

// C linkage for FFI compatibility
#ifdef __cplusplus
    #define AIOS_EXTERN_C extern "C"
    #define AIOS_EXTERN_C_BEGIN extern "C" {
    #define AIOS_EXTERN_C_END }
#else
    #define AIOS_EXTERN_C
    #define AIOS_EXTERN_C_BEGIN
    #define AIOS_EXTERN_C_END
#endif

// Combined macro for C API functions
#define AIOS_API AIOS_EXTERN_C AIOS_EXPORT
