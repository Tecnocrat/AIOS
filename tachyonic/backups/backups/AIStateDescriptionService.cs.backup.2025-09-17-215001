using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using System.Collections.Generic;
using System.Text;

namespace AIOS.VisualInterface
{
    /// <summary>
    /// AI State Description Service - Converts visual data to textual descriptions
    /// Enables AI engines to understand visual state through structured text analysis
    /// </summary>
    public class AIStateDescriptionService
    {
        private readonly ILogger<AIStateDescriptionService> _logger;
        private readonly string _stateDirectory;
        private readonly string _screenshotDirectory;

        public AIStateDescriptionService(ILogger<AIStateDescriptionService> logger)
        {
            _logger = logger;
            _stateDirectory = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "ai_visual_feedback", "state");
            _screenshotDirectory = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "ai_visual_feedback", "screenshots");
        }

        /// <summary>
        /// Generate comprehensive textual description of current AIOS visual state
        /// </summary>
        public async Task<string> DescribeCurrentStateAsync()
        {
            try
            {
                var latestFrameMetadata = GetLatestFrameMetadata();
                if (latestFrameMetadata == null)
                {
                    return "No visual data available - AIOS visual monitoring not active";
                }

                var description = new StringBuilder();
                description.AppendLine("=== AIOS VISUAL STATE ANALYSIS ===");
                description.AppendLine($"Timestamp: {latestFrameMetadata.Timestamp:yyyy-MM-dd HH:mm:ss}");
                description.AppendLine($"Resolution: {latestFrameMetadata.Resolution.Width}x{latestFrameMetadata.Resolution.Height}");
                description.AppendLine($"Window State: {latestFrameMetadata.WindowState}");
                description.AppendLine($"Active: {latestFrameMetadata.IsActive}");
                description.AppendLine();

                // Analyze screenshot for visual elements
                var visualAnalysis = AnalyzeScreenshotContent(latestFrameMetadata.Filename);
                description.AppendLine("=== VISUAL ELEMENT ANALYSIS ===");
                description.AppendLine(visualAnalysis);
                description.AppendLine();

                // Process management status
                var processStatus = AnalyzeProcessStatus();
                description.AppendLine("=== PROCESS STATUS ===");
                description.AppendLine(processStatus);
                description.AppendLine();

                // AI objectives analysis
                var objectiveStatus = AnalyzeAIObjectives();
                description.AppendLine("=== AI OBJECTIVES STATUS ===");
                description.AppendLine(objectiveStatus);

                return description.ToString();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating visual state description");
                return $"Error analyzing visual state: {ex.Message}";
            }
        }

        /// <summary>
        /// Analyze screenshot for UI elements and state indicators
        /// </summary>
        private string AnalyzeScreenshotContent(string filename)
        {
            var screenshotPath = Path.Combine(_screenshotDirectory, filename);
            if (!File.Exists(screenshotPath))
            {
                return "Screenshot file not found";
            }

            try
            {
                using (var bitmap = new Bitmap(screenshotPath))
                {
                    var analysis = new StringBuilder();
                    
                    // Basic image analysis
                    analysis.AppendLine($"Image Size: {bitmap.Width}x{bitmap.Height}");
                    analysis.AppendLine($"Pixel Format: {bitmap.PixelFormat}");
                    
                    // Analyze color patterns to infer UI state
                    var colorAnalysis = AnalyzeColorPatterns(bitmap);
                    analysis.AppendLine($"Dominant Colors: {colorAnalysis}");
                    
                    // Brightness analysis for activity indicators
                    var brightness = AnalyzeImageBrightness(bitmap);
                    analysis.AppendLine($"Average Brightness: {brightness:F1}% (Activity Level: {GetActivityLevel(brightness)})");
                    
                    // UI region detection
                    var regions = DetectUIRegions(bitmap);
                    analysis.AppendLine($"UI Regions Detected: {regions}");
                    
                    return analysis.ToString();
                }
            }
            catch (Exception ex)
            {
                return $"Screenshot analysis error: {ex.Message}";
            }
        }

        /// <summary>
        /// Analyze color patterns to infer UI state
        /// </summary>
        private string AnalyzeColorPatterns(Bitmap bitmap)
        {
            var colorCounts = new Dictionary<string, int>();
            var sampleCount = 0;
            var maxSamples = 1000; // Sample every nth pixel for performance
            
            for (int x = 0; x < bitmap.Width; x += bitmap.Width / 50)
            {
                for (int y = 0; y < bitmap.Height; y += bitmap.Height / 20)
                {
                    if (sampleCount >= maxSamples) break;
                    
                    var pixel = bitmap.GetPixel(x, y);
                    var colorName = GetColorName(pixel);
                    
                    if (colorCounts.ContainsKey(colorName))
                        colorCounts[colorName]++;
                    else
                        colorCounts[colorName] = 1;
                    
                    sampleCount++;
                }
            }
            
            // Find dominant colors
            var sortedColors = colorCounts.OrderByDescending(c => c.Value).Take(3);
            return string.Join(", ", sortedColors.Select(c => $"{c.Key}({c.Value})"));
        }

        /// <summary>
        /// Get simplified color name for analysis
        /// </summary>
        private string GetColorName(Color color)
        {
            if (color.GetBrightness() < 0.3) return "Dark";
            if (color.GetBrightness() > 0.8) return "Light";
            if (color.GetSaturation() < 0.3) return "Gray";
            if (color.GetHue() < 30 || color.GetHue() > 330) return "Red";
            if (color.GetHue() < 90) return "Yellow";
            if (color.GetHue() < 150) return "Green";
            if (color.GetHue() < 210) return "Cyan";
            if (color.GetHue() < 270) return "Blue";
            return "Purple";
        }

        /// <summary>
        /// Analyze overall image brightness as activity indicator
        /// </summary>
        private double AnalyzeImageBrightness(Bitmap bitmap)
        {
            double totalBrightness = 0;
            int sampleCount = 0;
            
            for (int x = 0; x < bitmap.Width; x += 10)
            {
                for (int y = 0; y < bitmap.Height; y += 10)
                {
                    var pixel = bitmap.GetPixel(x, y);
                    totalBrightness += pixel.GetBrightness();
                    sampleCount++;
                }
            }
            
            return (totalBrightness / sampleCount) * 100;
        }

        /// <summary>
        /// Determine activity level from brightness
        /// </summary>
        private string GetActivityLevel(double brightness)
        {
            if (brightness > 70) return "High Activity";
            if (brightness > 40) return "Moderate Activity";
            if (brightness > 20) return "Low Activity";
            return "Minimal Activity";
        }

        /// <summary>
        /// Detect UI regions based on visual patterns
        /// </summary>
        private string DetectUIRegions(Bitmap bitmap)
        {
            var regions = new List<string>();
            
            // Check for typical AIOS UI regions
            if (HasTitleBar(bitmap)) regions.Add("TitleBar");
            if (HasSidePanel(bitmap)) regions.Add("SidePanel");
            if (HasMainContent(bitmap)) regions.Add("MainContent");
            if (HasStatusBar(bitmap)) regions.Add("StatusBar");
            if (HasTachyonicViewer(bitmap)) regions.Add("TachyonicViewer");
            
            return regions.Count > 0 ? string.Join(", ", regions) : "No distinct regions detected";
        }

        private bool HasTitleBar(Bitmap bitmap) => AnalyzeRegion(bitmap, 0, 0, bitmap.Width, 50);
        private bool HasSidePanel(Bitmap bitmap) => AnalyzeRegion(bitmap, 0, 0, 200, bitmap.Height);
        private bool HasMainContent(Bitmap bitmap) => AnalyzeRegion(bitmap, bitmap.Width / 4, bitmap.Height / 4, bitmap.Width / 2, bitmap.Height / 2);
        private bool HasStatusBar(Bitmap bitmap) => AnalyzeRegion(bitmap, 0, bitmap.Height - 50, bitmap.Width, 50);
        private bool HasTachyonicViewer(Bitmap bitmap) => AnalyzeRegion(bitmap, bitmap.Width / 2, bitmap.Height / 2, bitmap.Width / 3, bitmap.Height / 3);

        /// <summary>
        /// Analyze specific region for UI elements
        /// </summary>
        private bool AnalyzeRegion(Bitmap bitmap, int x, int y, int width, int height)
        {
            if (x + width > bitmap.Width || y + height > bitmap.Height) return false;
            
            var distinctColors = new HashSet<Color>();
            for (int px = x; px < x + width && px < bitmap.Width; px += 5)
            {
                for (int py = y; py < y + height && py < bitmap.Height; py += 5)
                {
                    distinctColors.Add(bitmap.GetPixel(px, py));
                    if (distinctColors.Count > 20) return true; // Complex region likely has UI
                }
            }
            
            return distinctColors.Count > 10; // Simple heuristic for UI complexity
        }

        /// <summary>
        /// Analyze process status from metadata
        /// </summary>
        private string AnalyzeProcessStatus()
        {
            try
            {
                var sessionFile = Path.Combine(_stateDirectory, "current_session.json");
                if (!File.Exists(sessionFile))
                    return "No session data available";

                var sessionData = JsonSerializer.Deserialize<dynamic>(File.ReadAllText(sessionFile));
                return $"Session Active: {sessionData?.SessionId}, Purpose: {sessionData?.Purpose}";
            }
            catch
            {
                return "Process status analysis failed";
            }
        }

        /// <summary>
        /// Analyze AI objectives status
        /// </summary>
        private string AnalyzeAIObjectives()
        {
            try
            {
                var objectiveFiles = Directory.GetFiles(_stateDirectory, "objective_*.json");
                if (objectiveFiles.Length == 0)
                    return "No AI objectives registered";

                var objectives = new List<string>();
                foreach (var file in objectiveFiles.Take(3)) // Analyze latest 3
                {
                    var content = File.ReadAllText(file);
                    var objective = JsonSerializer.Deserialize<dynamic>(content);
                    objectives.Add($"Objective: {objective?.Description ?? "Unknown"}");
                }

                return string.Join("\n", objectives);
            }
            catch
            {
                return "AI objectives analysis failed";
            }
        }

        /// <summary>
        /// Get latest frame metadata
        /// </summary>
        private FrameMetadata? GetLatestFrameMetadata()
        {
            try
            {
                var metadataFiles = Directory.GetFiles(_stateDirectory, "frame_*_metadata.json")
                                           .OrderByDescending(f => f)
                                           .FirstOrDefault();

                if (metadataFiles == null) return null;

                var json = File.ReadAllText(metadataFiles);
                return JsonSerializer.Deserialize<FrameMetadata>(json);
            }
            catch
            {
                return null;
            }
        }
    }

    /// <summary>
    /// Frame metadata structure
    /// </summary>
    public class FrameMetadata
    {
        public int FrameNumber { get; set; }
        public DateTime Timestamp { get; set; }
        public string Filename { get; set; } = "";
        public Resolution Resolution { get; set; } = new();
        public string WindowState { get; set; } = "";
        public bool IsActive { get; set; }
        public AIAnalysisHints AIAnalysisHints { get; set; } = new();
    }

    public class Resolution
    {
        public int Width { get; set; }
        public int Height { get; set; }
    }

    public class AIAnalysisHints
    {
        public string Purpose { get; set; } = "";
        public List<string> ExpectedElements { get; set; } = new();
        public List<string> CompletionIndicators { get; set; } = new();
    }
}