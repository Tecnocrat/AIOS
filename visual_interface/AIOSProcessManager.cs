using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using Microsoft.Extensions.Logging;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Centralized Process Manager for AIOS System
    /// Manages lifecycle of all AIOS components and ensures proper cleanup
    /// </summary>
    public class AIOSProcessManager : IDisposable
    {
        private readonly ILogger<AIOSProcessManager> _logger;
        private readonly List<Process> _managedProcesses = new();
        private readonly List<Window> _managedWindows = new();
        private bool _isShuttingDown = false;

        public AIOSProcessManager(ILogger<AIOSProcessManager> logger)
        {
            _logger = logger;
            
            // Subscribe to application exit events
            Application.Current.Exit += OnApplicationExit;
            Application.Current.SessionEnding += OnSessionEnding;
            
            _logger.LogInformation("🔧 AIOS Process Manager initialized");
        }

        /// <summary>
        /// Launches the AIOS UI process and tracks it
        /// </summary>
        public async Task<Process?> LaunchAIOSUIAsync()
        {
            try
            {
                string uiPath = Path.Combine(
                    AppDomain.CurrentDomain.BaseDirectory,
                    "..", "..", "..", "..", "interface", "AIOS.UI", "bin", "Debug", "net9.0-windows", "AIOS.UI.exe"
                );
                
                uiPath = Path.GetFullPath(uiPath);
                
                if (!File.Exists(uiPath))
                {
                    _logger.LogWarning("AIOS UI executable not found at: {Path}", uiPath);
                    return null;
                }

                var process = new Process
                {
                    StartInfo = new ProcessStartInfo
                    {
                        FileName = uiPath,
                        UseShellExecute = true,
                        CreateNoWindow = false
                    }
                };

                process.Start();
                _managedProcesses.Add(process);
                
                _logger.LogInformation("✅ AIOS UI process launched (PID: {ProcessId})", process.Id);
                return process;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Failed to launch AIOS UI process");
                return null;
            }
        }

        /// <summary>
        /// Registers a window to be managed by the process manager
        /// </summary>
        public void RegisterWindow(Window window)
        {
            if (window == null) return;
            
            _managedWindows.Add(window);
            
            // Subscribe to window closing event
            window.Closing += (sender, args) =>
            {
                if (sender is Window closingWindow && IsMainWindow(closingWindow))
                {
                    _logger.LogInformation("🚪 Main window closing - initiating system shutdown");
                    _ = InitiateSystemShutdownAsync();
                }
            };
            
            _logger.LogInformation("📋 Window registered for management: {WindowTitle}", window.Title);
        }

        /// <summary>
        /// Determines if a window is the main application window
        /// </summary>
        private bool IsMainWindow(Window window)
        {
            return window is AdvancedVisualizationWindow || 
                   window == Application.Current.MainWindow ||
                   window.Title.Contains("AIOS") && window.Title.Contains("Visualization");
        }

        /// <summary>
        /// Launches a managed external process
        /// </summary>
        public Process? LaunchManagedProcess(string executablePath, string arguments = "")
        {
            try
            {
                if (!File.Exists(executablePath))
                {
                    _logger.LogWarning("Executable not found: {Path}", executablePath);
                    return null;
                }

                var process = new Process
                {
                    StartInfo = new ProcessStartInfo
                    {
                        FileName = executablePath,
                        Arguments = arguments,
                        UseShellExecute = false,
                        CreateNoWindow = true
                    }
                };

                process.Start();
                _managedProcesses.Add(process);
                
                _logger.LogInformation("🚀 Managed process launched: {ProcessName} (PID: {ProcessId})", 
                    Path.GetFileName(executablePath), process.Id);
                
                return process;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Failed to launch managed process: {Path}", executablePath);
                return null;
            }
        }

        /// <summary>
        /// Initiates graceful shutdown of all managed components
        /// </summary>
        public async Task InitiateSystemShutdownAsync()
        {
            if (_isShuttingDown)
            {
                _logger.LogInformation("⏸️ Shutdown already in progress");
                return;
            }

            _isShuttingDown = true;
            _logger.LogInformation("🔄 Initiating AIOS system shutdown...");

            try
            {
                // Close all managed windows first
                await CloseAllWindowsAsync();
                
                // Then terminate all managed processes
                await TerminateAllProcessesAsync();
                
                // Kill any orphaned .NET host processes
                await CleanupOrphanedHostsAsync();
                
                _logger.LogInformation("✅ AIOS system shutdown completed successfully");
                
                // Finally, exit the application
                Application.Current.Dispatcher.BeginInvoke(() =>
                {
                    Application.Current.Shutdown(0);
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Error during system shutdown");
                
                // Force exit if graceful shutdown fails
                Application.Current.Dispatcher.BeginInvoke(() =>
                {
                    Application.Current.Shutdown(1);
                });
            }
        }

        /// <summary>
        /// Closes all managed windows gracefully
        /// </summary>
        private async Task CloseAllWindowsAsync()
        {
            _logger.LogInformation("🚪 Closing all managed windows...");
            
            var windowsToClose = _managedWindows.ToList();
            
            foreach (var window in windowsToClose)
            {
                try
                {
                    if (window.IsLoaded && window.IsVisible)
                    {
                        await Application.Current.Dispatcher.InvokeAsync(() =>
                        {
                            window.Close();
                        });
                        
                        _logger.LogInformation("✅ Window closed: {WindowTitle}", window.Title);
                    }
                }
                catch (Exception ex)
                {
                    _logger.LogWarning(ex, "⚠️ Failed to close window: {WindowTitle}", window.Title);
                }
            }
            
            _managedWindows.Clear();
        }

        /// <summary>
        /// Terminates all managed processes
        /// </summary>
        private async Task TerminateAllProcessesAsync()
        {
            _logger.LogInformation("⏹️ Terminating all managed processes...");
            
            var processesToKill = _managedProcesses.ToList();
            
            foreach (var process in processesToKill)
            {
                try
                {
                    if (!process.HasExited)
                    {
                        _logger.LogInformation("🔄 Terminating process: {ProcessName} (PID: {ProcessId})", 
                            process.ProcessName, process.Id);
                        
                        // Try graceful termination first
                        process.CloseMainWindow();
                        
                        // Wait a moment for graceful shutdown
                        if (!process.WaitForExit(3000))
                        {
                            // Force kill if graceful shutdown fails
                            process.Kill();
                            _logger.LogWarning("⚡ Force-killed process: {ProcessName} (PID: {ProcessId})", 
                                process.ProcessName, process.Id);
                        }
                        else
                        {
                            _logger.LogInformation("✅ Process terminated gracefully: {ProcessName}", process.ProcessName);
                        }
                    }
                    
                    process.Dispose();
                }
                catch (Exception ex)
                {
                    _logger.LogWarning(ex, "⚠️ Failed to terminate process: {ProcessId}", process.Id);
                }
            }
            
            _managedProcesses.Clear();
        }

        /// <summary>
        /// Cleans up orphaned .NET host processes
        /// </summary>
        private async Task CleanupOrphanedHostsAsync()
        {
            try
            {
                _logger.LogInformation("🧹 Cleaning up orphaned .NET host processes...");
                
                var currentProcessId = Process.GetCurrentProcess().Id;
                var netHostProcesses = Process.GetProcessesByName("dotnet")
                    .Concat(Process.GetProcesses().Where(p => 
                        p.ProcessName.Contains("AIOS") || 
                        p.ProcessName.Contains(".NET") ||
                        p.MainWindowTitle.Contains("AIOS")))
                    .Where(p => p.Id != currentProcessId)
                    .ToList();

                foreach (var process in netHostProcesses)
                {
                    try
                    {
                        // Check if this is likely an AIOS-related process
                        if (IsAIOSRelatedProcess(process))
                        {
                            _logger.LogInformation("🔄 Terminating orphaned process: {ProcessName} (PID: {ProcessId})", 
                                process.ProcessName, process.Id);
                            
                            process.Kill();
                            process.WaitForExit(2000);
                        }
                    }
                    catch (Exception ex)
                    {
                        _logger.LogWarning(ex, "⚠️ Failed to terminate orphaned process: {ProcessId}", process.Id);
                    }
                    finally
                    {
                        process.Dispose();
                    }
                }
                
                _logger.LogInformation("✅ Orphaned process cleanup completed");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ Error during orphaned process cleanup");
            }
        }

        /// <summary>
        /// Determines if a process is related to AIOS
        /// </summary>
        private bool IsAIOSRelatedProcess(Process process)
        {
            try
            {
                return process.ProcessName.Contains("AIOS", StringComparison.OrdinalIgnoreCase) ||
                       process.MainWindowTitle.Contains("AIOS", StringComparison.OrdinalIgnoreCase) ||
                       (process.ProcessName.Equals("dotnet", StringComparison.OrdinalIgnoreCase) && 
                        process.MainModule?.FileName?.Contains("AIOS", StringComparison.OrdinalIgnoreCase) == true);
            }
            catch
            {
                // If we can't determine, err on the side of caution
                return false;
            }
        }

        /// <summary>
        /// Event handler for application exit
        /// </summary>
        private async void OnApplicationExit(object sender, ExitEventArgs e)
        {
            _logger.LogInformation("🚪 Application exit event triggered");
            await InitiateSystemShutdownAsync();
        }

        /// <summary>
        /// Event handler for session ending
        /// </summary>
        private async void OnSessionEnding(object sender, SessionEndingCancelEventArgs e)
        {
            _logger.LogInformation("🔄 Session ending event triggered: {Reason}", e.ReasonSessionEnding);
            await InitiateSystemShutdownAsync();
        }

        /// <summary>
        /// Gets the count of currently managed processes
        /// </summary>
        public int ManagedProcessCount => _managedProcesses.Count(p => !p.HasExited);

        /// <summary>
        /// Gets the count of currently managed windows
        /// </summary>
        public int ManagedWindowCount => _managedWindows.Count;

        /// <summary>
        /// Dispose pattern implementation
        /// </summary>
        public void Dispose()
        {
            if (!_isShuttingDown)
            {
                _ = InitiateSystemShutdownAsync();
            }
        }
    }
}
