using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Interop;
using System.Windows.Media.Imaging;
using Microsoft.Extensions.Logging;
using System.Text.Json;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// AI Visual Feedback Service - Real-time UI Capture for AI Engine Integration
    /// Implements agentic stimulation points through continuous visual state monitoring
    /// Enables AI engines to 'see' the application state in real-time for task completion
    /// </summary>
    public class AIVisualFeedbackService : IDisposable
    {
        private readonly ILogger<AIVisualFeedbackService> _logger;
        private readonly Timer _captureTimer;
        private readonly string _captureDirectory;
        private readonly string _aiStateDirectory;
        private bool _isCapturing = false;
        private int _frameCounter = 0;
        private DateTime _sessionStart;
        private bool _disposed = false;

        public AIVisualFeedbackService(ILogger<AIVisualFeedbackService> logger)
        {
            _logger = logger;
            _sessionStart = DateTime.Now;
            
            // Create AI-readable directories
            _captureDirectory = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "ai_visual_feedback", "screenshots");
            _aiStateDirectory = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "ai_visual_feedback", "state");
            
            Directory.CreateDirectory(_captureDirectory);
            Directory.CreateDirectory(_aiStateDirectory);
            
            // Initialize capture timer (500ms intervals)
            _captureTimer = new Timer(CaptureScreenshotCallback, null, Timeout.Infinite, 500);
            
            _logger.LogInformation("🔍 AI Visual Feedback Service initialized - Ready for agentic stimulation");
        }

        /// <summary>
        /// Start real-time visual capture for AI integration
        /// </summary>
        public void StartVisualCapture()
        {
            if (_isCapturing) return;
            
            _isCapturing = true;
            _frameCounter = 0;
            _sessionStart = DateTime.Now;
            
            // Start the capture timer
            _captureTimer.Change(0, 500); // Immediate start, then every 500ms
            
            // Create session metadata for AI engine
            var sessionMetadata = new
            {
                SessionId = Guid.NewGuid(),
                StartTime = _sessionStart,
                Purpose = "AI_Visual_Feedback_Integration",
                CaptureInterval = 500,
                Resolution = "Auto-detect",
                AIObjective = "Real-time UI monitoring for task completion validation"
            };
            
            File.WriteAllText(
                Path.Combine(_aiStateDirectory, "current_session.json"),
                JsonSerializer.Serialize(sessionMetadata, new JsonSerializerOptions { WriteIndented = true })
            );
            
            _logger.LogInformation("📸 AI Visual Capture Started - Agentic feedback loop active");
        }

        /// <summary>
        /// Stop visual capture
        /// </summary>
        public void StopVisualCapture()
        {
            if (!_isCapturing) return;
            
            _isCapturing = false;
            _captureTimer.Change(Timeout.Infinite, Timeout.Infinite);
            
            // Create session summary for AI analysis
            var sessionSummary = new
            {
                SessionEnd = DateTime.Now,
                Duration = DateTime.Now - _sessionStart,
                TotalFrames = _frameCounter,
                AverageFrameRate = _frameCounter / (DateTime.Now - _sessionStart).TotalSeconds,
                Status = "Completed",
                AIAnalysisReady = true
            };
            
            File.WriteAllText(
                Path.Combine(_aiStateDirectory, "session_summary.json"),
                JsonSerializer.Serialize(sessionSummary, new JsonSerializerOptions { WriteIndented = true })
            );
            
            _logger.LogInformation("🛑 AI Visual Capture Stopped - {Frames} frames captured", _frameCounter);
        }

        /// <summary>
        /// Capture screenshot callback for timer
        /// </summary>
        private void CaptureScreenshotCallback(object? state)
        {
            if (!_isCapturing || _disposed) return;

            try
            {
                Application.Current.Dispatcher.Invoke(() =>
                {
                    CaptureMainWindowScreenshot();
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error capturing screenshot for AI feedback");
            }
        }

        /// <summary>
        /// Capture screenshot of main AIOS window
        /// </summary>
        private void CaptureMainWindowScreenshot()
        {
            try
            {
                var mainWindow = Application.Current.MainWindow;
                if (mainWindow == null || !mainWindow.IsVisible) return;

                // Get window bounds
                var rect = new Int32Rect(
                    (int)mainWindow.Left,
                    (int)mainWindow.Top,
                    (int)mainWindow.ActualWidth,
                    (int)mainWindow.ActualHeight
                );

                if (rect.Width <= 0 || rect.Height <= 0) return;

                // Create bitmap from window
                var renderTargetBitmap = new RenderTargetBitmap(
                    rect.Width, rect.Height, 96, 96, System.Windows.Media.PixelFormats.Pbgra32);
                
                renderTargetBitmap.Render(mainWindow);

                // Save for AI analysis
                var timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss_fff");
                var filename = $"aios_frame_{_frameCounter:D6}_{timestamp}.png";
                var filepath = Path.Combine(_captureDirectory, filename);

                using (var fileStream = new FileStream(filepath, FileMode.Create))
                {
                    var encoder = new PngBitmapEncoder();
                    encoder.Frames.Add(BitmapFrame.Create(renderTargetBitmap));
                    encoder.Save(fileStream);
                }

                // Create AI-readable frame metadata
                var frameMetadata = new
                {
                    FrameNumber = _frameCounter,
                    Timestamp = DateTime.Now,
                    Filename = filename,
                    Resolution = new { Width = rect.Width, Height = rect.Height },
                    WindowState = mainWindow.WindowState.ToString(),
                    IsActive = mainWindow.IsActive,
                    AIAnalysisHints = new
                    {
                        Purpose = "Real-time UI state monitoring",
                        ExpectedElements = new[] { "Tachyonic Viewer", "Process Management", "Consciousness Metrics" },
                        CompletionIndicators = new[] { "All processes running", "Tachyonic active", "No errors" }
                    }
                };

                File.WriteAllText(
                    Path.Combine(_aiStateDirectory, $"frame_{_frameCounter:D6}_metadata.json"),
                    JsonSerializer.Serialize(frameMetadata, new JsonSerializerOptions { WriteIndented = true })
                );

                _frameCounter++;

                // Log every 10 frames to avoid spam
                if (_frameCounter % 10 == 0)
                {
                    _logger.LogDebug("📸 AI Visual Feedback: Frame {Frame} captured", _frameCounter);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to capture screenshot for AI feedback");
            }
        }

        /// <summary>
        /// Get current visual state summary for AI consumption
        /// </summary>
        public object GetCurrentVisualState()
        {
            return new
            {
                IsCapturing = _isCapturing,
                CurrentFrame = _frameCounter,
                SessionDuration = DateTime.Now - _sessionStart,
                CaptureDirectory = _captureDirectory,
                StateDirectory = _aiStateDirectory,
                LastFrameTime = DateTime.Now,
                AIReadyStatus = _isCapturing && _frameCounter > 0
            };
        }

        /// <summary>
        /// Register an AI objective for completion tracking
        /// </summary>
        public void RegisterAIObjective(string objective, object parameters)
        {
            var objectiveData = new
            {
                Objective = objective,
                Parameters = parameters,
                RegisteredAt = DateTime.Now,
                Status = "Active",
                RequiresVisualValidation = true
            };

            var objectiveFile = Path.Combine(_aiStateDirectory, $"objective_{Guid.NewGuid():N}.json");
            File.WriteAllText(objectiveFile, JsonSerializer.Serialize(objectiveData, new JsonSerializerOptions { WriteIndented = true }));

            _logger.LogInformation("🎯 AI Objective Registered: {Objective}", objective);
        }

        public void Dispose()
        {
            if (_disposed) return;

            StopVisualCapture();
            _captureTimer?.Dispose();
            _disposed = true;

            _logger.LogInformation("🔍 AI Visual Feedback Service disposed");
        }
    }
}
