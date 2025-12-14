using System;
using System.Threading.Tasks;
using System.Windows;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// Main application class for AIOS 3D Consciousness Visualizer
    /// Provides real-time visualization of consciousness emergence patterns
    /// </summary>
    public partial class App : Application
    {
        private IHost _host;
        private ILogger<App> _logger;
        
        public IServiceProvider ServiceProvider => _host.Services;

        protected override async void OnStartup(StartupEventArgs e)
        {
            try
            {
                // Create host builder with dependency injection
                _host = Host.CreateDefaultBuilder()
                    .ConfigureServices(ConfigureServices)
                    .ConfigureLogging(ConfigureLogging)
                    .Build();

                await _host.StartAsync();

                _logger = _host.Services.GetRequiredService<ILogger<App>>();
                _logger.LogInformation("AIOS Advanced Consciousness Visualizer starting up");

                // Create and show main visualization window with enhanced persistence
                var mainWindow = _host.Services.GetRequiredService<MainVisualizationWindow>();
                mainWindow.Show();

                base.OnStartup(e);
                _logger.LogInformation("AIOS Advanced Consciousness Visualizer started successfully");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Failed to start application: {ex.Message}", "Startup Error", 
                    MessageBoxButton.OK, MessageBoxImage.Error);
                Shutdown(1);
            }
        }

        private void ConfigureServices(IServiceCollection services)
        {
            // Register core services
            services.AddSingleton<ConsciousnessDataManager>();
            services.AddSingleton<ConsciousnessGeometryEngine>();
            services.AddSingleton<ConsoleLogger>();
            services.AddSingleton<RuntimeAnalytics>();
            
            // Register persistence infrastructure (Phase 1A: UI Persistence Infrastructure)
            services.AddSingleton<StateManager>();
            services.AddSingleton<SessionContext>();
            services.AddSingleton<PersistenceEngine>();
            
            // Register Tachyonic Intelligence Bridge for repository ingestion
            services.AddSingleton<TachyonicIntelligenceBridge>();
            
            // Register both visualization windows
            services.AddTransient<SimpleVisualizationWindow>();
            services.AddTransient<MainVisualizationWindow>();
            
            // Configure HTTP client for potential remote connections
            services.AddHttpClient();
        }

        private void ConfigureLogging(ILoggingBuilder builder)
        {
            builder.ClearProviders();
            builder.AddConsole();
            builder.AddDebug();
            builder.SetMinimumLevel(LogLevel.Information);
            
            // Add custom console logger for the visual interface
            builder.Services.AddSingleton<ConsoleLogger>();
        }

        protected override async void OnExit(ExitEventArgs e)
        {
            try
            {
                _logger?.LogInformation("AIOS Consciousness Visualizer shutting down");
                
                // Ensure clean shutdown of persistence services
                var sessionContext = _host?.Services.GetService<SessionContext>();
                if (sessionContext != null)
                {
                    await sessionContext.MarkCleanShutdownAsync();
                    sessionContext.Dispose();
                }
                
                var persistenceEngine = _host?.Services.GetService<PersistenceEngine>();
                persistenceEngine?.Dispose();
                
                var stateManager = _host?.Services.GetService<StateManager>();
                stateManager?.Dispose();
                
                // Stop and dispose host
                if (_host != null)
                {
                    await _host.StopAsync();
                    _host.Dispose();
                }
            }
            catch (Exception ex)
            {
                // Log shutdown error but don't prevent shutdown
                _logger?.LogError(ex, "Error during application shutdown");
            }
            finally
            {
                base.OnExit(e);
            }
        }

        private void Application_DispatcherUnhandledException(object sender, 
            System.Windows.Threading.DispatcherUnhandledExceptionEventArgs e)
        {
            try
            {
                _logger?.LogError(e.Exception, "Unhandled application exception");
                
                var result = MessageBox.Show(
                    $"An unexpected error occurred:\n\n{e.Exception.Message}\n\nWould you like to continue?",
                    "AIOS Visualizer Error",
                    MessageBoxButton.YesNo,
                    MessageBoxImage.Error);

                if (result == MessageBoxResult.Yes)
                {
                    e.Handled = true;
                }
                else
                {
                    Shutdown(1);
                }
            }
            catch
            {
                // If logging fails, just show basic error
                MessageBox.Show("A critical error occurred. The application will close.", 
                    "Critical Error", MessageBoxButton.OK, MessageBoxImage.Error);
                Shutdown(1);
            }
        }
    }
}
