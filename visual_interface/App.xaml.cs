using System;
using System.Threading.Tasks;
using System.Windows;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using System.Diagnostics;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Enhanced main application class for AIOS 3D Consciousness Visualizer
    /// Provides real-time visualization of consciousness emergence patterns with AIOS harmonization
    /// </summary>
    public partial class App : Application
    {
        private IHost? _host;
        private ILogger<App>? _logger;
        private UIMetricsEmitter? _metricsEmitter;
        private StateManager? _stateManager;
        private AIOSProcessManager? _processManager;
        private readonly Stopwatch _startupTimer = new();

        public IServiceProvider ServiceProvider => _host?.Services ?? throw new InvalidOperationException("Host not initialized");

        protected override async void OnStartup(StartupEventArgs e)
        {
            _startupTimer.Start();

            try
            {
                // Create host builder with enhanced dependency injection
                _host = Host.CreateDefaultBuilder()
                    .ConfigureServices(ConfigureServices)
                    .ConfigureLogging(ConfigureLogging)
                    .Build();

                await _host.StartAsync();

                // Get core services
                _logger = _host.Services.GetRequiredService<ILogger<App>>();
                _metricsEmitter = _host.Services.GetRequiredService<UIMetricsEmitter>();
                _stateManager = _host.Services.GetRequiredService<StateManager>();
                _processManager = _host.Services.GetRequiredService<AIOSProcessManager>();
                
                // Initialize AI Visual Feedback Service for agentic stimulation
                var aiVisualService = _host.Services.GetRequiredService<AIVisualFeedbackService>();

                _logger.LogInformation("🧠 AIOS Advanced Consciousness Visualizer starting up");

                // Initialize state management
                await InitializeApplicationStateAsync();

                // Create and show main visualization window with working 3D interface
                var mainWindow = new AdvancedVisualizationWindow();
                
                // Register the main window with the process manager
                _processManager.RegisterWindow(mainWindow);
                
                mainWindow.Show();

                // Launch managed AIOS UI process
                await _processManager.LaunchAIOSUIAsync();
                
                // Start AI Visual Feedback for real-time monitoring
                aiVisualService.StartVisualCapture();
                aiVisualService.RegisterAIObjective("Monitor_AIOS_Consciousness_Integration", new
                {
                    RequiredComponents = new[] { "Visual Interface", "Tachyonic Viewer", "Process Manager" },
                    CompletionCriteria = "All components running without errors",
                    VisualValidation = true
                });

                base.OnStartup(e);

                _startupTimer.Stop();
                _logger.LogInformation("🚀 AIOS Advanced Consciousness Visualizer started successfully in {ElapsedMs}ms",
                    _startupTimer.ElapsedMilliseconds);

                // Register successful startup
                _metricsEmitter?.RegisterFrame(_startupTimer.ElapsedMilliseconds);
            }
            catch (Exception ex)
            {
                _logger?.LogError(ex, "💥 Critical startup failure in AIOS Visualizer");
                MessageBox.Show($"Failed to start application: {ex.Message}", "AIOS Startup Error",
                    MessageBoxButton.OK, MessageBoxImage.Error);
                Shutdown(1);
            }
        }

        private async Task InitializeApplicationStateAsync()
        {
            try
            {
                _logger?.LogInformation("📊 Initializing AIOS application state");

                // Restore previous state if available
                if (_stateManager != null)
                {
                    var previousState = await _stateManager.RestoreUIStateAsync();
                    if (previousState != null)
                    {
                        _logger?.LogInformation("✅ Previous AIOS state restored successfully");
                    }
                    else
                    {
                        _logger?.LogInformation("ℹ️ No previous state found, starting with clean slate");
                    }
                }

                // Initialize metrics collection
                _metricsEmitter?.RegisterFrame(0); // Register startup frame
            }
            catch (Exception ex)
            {
                _logger?.LogWarning(ex, "⚠️ Failed to initialize application state, continuing with defaults");
            }
        }

        private void ConfigureServices(IServiceCollection services)
        {
            // Register centralized process manager
            services.AddSingleton<AIOSProcessManager>();
            
            // Register AI Visual Feedback Service for agentic stimulation
            services.AddSingleton<AIVisualFeedbackService>();
            
            // Register core AIOS services with enhanced configuration
            services.AddSingleton<ConsciousnessDataManager>();
            // services.AddSingleton<ConsciousnessGeometryEngine>(); // Excluded from build
            services.AddSingleton<RuntimeAnalytics>();
            services.AddSingleton<CellularRuntimeBridge>(); // runtime_intelligence bridge
            services.AddSingleton<UIMetricsEmitter>(); // KPI emitter with enhanced metrics
            services.AddSingleton<StateManager>(); // State persistence manager

            // Register AINLP and harmonization services
            services.AddSingleton<AINLP>();
            services.AddSingleton<AIHarmonizationEngine>();

            // Register 3D visualization windows with enhanced features
            services.AddTransient<BosonicLayer3DWindow>();
            services.AddTransient<AdvancedVisualizationWindow>();
            // services.AddTransient<SimpleVisualizationWindow>(); // Excluded from build
            // services.AddTransient<MainVisualizationWindow>(); // Excluded from build

            // Configure HTTP client for potential remote AIOS connections
            services.AddHttpClient("AIOSClient", client =>
            {
                client.Timeout = TimeSpan.FromSeconds(30);
                client.DefaultRequestHeaders.Add("User-Agent", "AIOS-Visualizer/1.0");
            });
        }

        private void ConfigureLogging(ILoggingBuilder builder)
        {
            builder.ClearProviders();

            // Enhanced logging configuration for AIOS
            builder.AddConsole();

            builder.AddDebug();
            builder.SetMinimumLevel(LogLevel.Information);

            // Add custom console logger for the visual interface
            builder.Services.AddSingleton<ConsoleLogger>();

            // Note: File logging would require additional NuGet packages
            // builder.AddFile("logs/aios_visualizer.log", LogLevel.Debug);
        }

        protected override async void OnExit(ExitEventArgs e)
        {
            try
            {
                _logger?.LogInformation("🔄 AIOS Consciousness Visualizer shutting down");

                // Initiate centralized process cleanup FIRST
                if (_processManager != null)
                {
                    _logger?.LogInformation("🧹 Initiating centralized process cleanup");
                    await _processManager.InitiateSystemShutdownAsync();
                }

                // Save final state before shutdown
                await SaveFinalStateAsync();

                // Stop and dispose host
                if (_host != null)
                {
                    await _host.StopAsync();
                    _host.Dispose();
                }

                _logger?.LogInformation("✅ AIOS Visualizer shutdown completed successfully");
            }
            catch (Exception ex)
            {
                // Log shutdown error but don't prevent shutdown
                _logger?.LogError(ex, "❌ Error during AIOS application shutdown");
            }
            finally
            {
                base.OnExit(e);
            }
        }

        private async Task SaveFinalStateAsync()
        {
            try
            {
                if (_stateManager != null)
                {
                    // Create final state snapshot
                    var finalState = new ConsciousnessVisualizationState
                    {
                        ConsciousnessLevel = 0.0, // Would be populated from actual metrics
                        QuantumCoherence = 0.0,
                        MetadataContext = "AIOS Visualizer Shutdown",
                        VisualizationSettings = new { ShutdownTime = DateTime.UtcNow }
                    };

                    await _stateManager.PersistUIStateAsync(finalState);
                    _logger?.LogInformation("💾 Final AIOS state saved successfully");
                }
            }
            catch (Exception ex)
            {
                _logger?.LogWarning(ex, "⚠️ Failed to save final state during shutdown");
            }
        }

        private void Application_DispatcherUnhandledException(object sender,
            System.Windows.Threading.DispatcherUnhandledExceptionEventArgs e)
        {
            try
            {
                _logger?.LogError(e.Exception, "💥 Unhandled AIOS application exception");

                // Register error in metrics
                _metricsEmitter?.RegisterError("dispatcher_exception");

                var result = MessageBox.Show(
                    $"An unexpected error occurred in AIOS Visualizer:\n\n{e.Exception.Message}\n\nWould you like to continue?",
                    "AIOS Critical Error",
                    MessageBoxButton.YesNo,
                    MessageBoxImage.Error);

                if (result == MessageBoxResult.Yes)
                {
                    e.Handled = true;
                    _logger?.LogWarning("👤 User chose to continue after critical error");
                }
                else
                {
                    _logger?.LogError("🔚 User chose to exit after critical error");
                    Shutdown(1);
                }
            }
            catch
            {
                // If logging fails, just show basic error
                MessageBox.Show("A critical error occurred in AIOS. The application will close.",
                    "AIOS Critical Error", MessageBoxButton.OK, MessageBoxImage.Error);
                Shutdown(1);
            }
        }
    }
}
