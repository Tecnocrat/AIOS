using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Threading;
using AIOS.Models;
using AIOS.Services;
using System.Text.Json;
using System.Net.Http;

namespace AIOS.UI;

/// <summary>
/// Fractal Holographic Main Window with system-wide awareness
/// Thread B: C# UI + VSCode Extension Synchronization
/// </summary>
public partial class MainWindow : Window
{
    private DispatcherTimer _healthTimer;
    private DispatcherTimer _activityTimer;
    private AIOS.Services.AIServiceManager _aiService;
    private AIOS.Models.FractalContextManager _contextManager;
    private AIOS.Models.HolographicUIOrchestrator _orchestrator;
    private VSCodeExtensionBridge _vscodeBridge;
    private AIOS.Services.MaintenanceService _maintenanceService;
    private string _currentModule = "nlp";
    private int _messageCount = 0;

    // Phase 11 Day 1: AI Layer Client for Python AI integration
    private AILayerClient _aiLayerClient;


        InitializeUI();
        InitializeFractalComponents();
        InitializeTimers();
    LoadSystemStatus();
    StartHolographicSynchronization();
    }

    private void InitializeUI()
    {
        // Set initial focus and placeholder behavior
        ChatInput.GotFocus += (s, e) =>
        {
            if (ChatInput.Text == "Type your message here...")
            {
                ChatInput.Text = "";
                ChatInput.Foreground = Brushes.White;
            }
        };

        ChatInput.LostFocus += (s, e) =>
        {
            if (string.IsNullOrWhiteSpace(ChatInput.Text))
            {
                ChatInput.Text = "Type your message here...";
                ChatInput.Foreground = new SolidColorBrush(Color.FromRgb(170, 170, 170));
            }
        };

        // Add welcome message
        AddChatMessage("AIOS", "Welcome to AIOS! I'm your AI assistant. Click on any module to switch modes, or just start chatting!", true);

        // Check Interface Bridge server status
        CheckServerStatus();
    }

    private async void CheckServerStatus()
    {
        try
        {
            using var httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(5) };
            var response = await httpClient.GetAsync("http://localhost:8000/health");

            if (response.IsSuccessStatusCode)
            {
                ServerStatusText.Text = "Server running";
                AddActivityLog("Interface Bridge server is running");
            }
            else
            {
                ServerStatusText.Text = "Server error";
                AddActivityLog("Interface Bridge server health check failed");
            }
        }
        catch
        {
            ServerStatusText.Text = "Server not running";
            AddActivityLog("Interface Bridge server not accessible");
        }
    }

    private void OpenKPIDashboard_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            var w = new KPIDashboardWindow();
            w.Owner = this;
            w.Show();
            AddActivityLog("Opened KPI Dashboard");
        }
        catch (Exception ex)
        {
            AddActivityLog($"KPI dashboard error: {ex.Message}");
        }
    }

    private void InitializeFractalComponents()
    {
        // Initialize fractal holographic components
    _contextManager.Initialize();
    _orchestrator.Initialize();

        // Load and apply component reflections
        LoadComponentReflections();

        // Update system state
        UpdateSystemState();
    }

    private void LoadComponentReflections()
    {
        // Load component reflections from configuration or service
        var reflectionsJson = _aiService.GetComponentReflections();
        if (reflectionsJson != null)
        {
            _componentReflections = JsonSerializer.Deserialize<Dictionary<string, ComponentReflection>>(reflectionsJson);
        }
    }

    private void UpdateSystemState()
    {
        // Update the holographic system state based on current context and reflections
    _systemState.Update(_contextManager.CurrentContext, _componentReflections);

        // Reflect state in the UI
        ReflectStateInUI();
    }

    private void ReflectStateInUI()
    {
        // Update UI elements based on the current system state
        // For example, update visibility or enable/disable controls
    }

    private void InitializeTimers()
    {
        // Health check timer - every 30 seconds
    _healthTimer = new DispatcherTimer
        {
            Interval = TimeSpan.FromSeconds(30)
        };
        _healthTimer.Tick += async (s, e) => await UpdateSystemHealth();
        _healthTimer.Start();

        // Activity update timer - every 5 seconds
        _activityTimer = new DispatcherTimer
        {
            Interval = TimeSpan.FromSeconds(5)
        };
        _activityTimer.Tick += UpdateSystemMetrics;
        _activityTimer.Start();
    }

    // Simple periodic sync stub used by UI
    private void StartHolographicSynchronization()
    {
        // For now just log a message via activity log; could hook VSCode bridge here
        AddActivityLog("Holographic synchronization active");
    }

    private async void LoadSystemStatus()
    {
        try
        {
            await UpdateSystemHealth();
            AddActivityLog("UI initialized successfully");
            StatusText.Text = "Ready - All systems operational";
        }
        catch (Exception ex)
        {
            AddActivityLog($"Initialization error: {ex.Message}");
            StatusText.Text = "Warning - Some systems may be unavailable";
        }
    }

    private async System.Threading.Tasks.Task UpdateSystemHealth()
    {
        try
        {
            var healthResponse = await _aiService.GetSystemHealthAsync();

            if (healthResponse.Success)
            {
                var healthScore = healthResponse.HealthScore * 100;

                HealthProgressBar.Value = healthScore;
                HealthScoreText.Text = $"{healthScore:F0}%";

                // Clean up status text (remove emojis for UI display)
                var cleanStatus = healthResponse.HealthStatus
                    .Replace("🟢 ", "").Replace("🟡 ", "").Replace(" ", "")
                    .Replace(">> ", "");
                StatusIndicator.Text = cleanStatus;

                // Update status indicator color based on health score
                StatusIndicator.Background = healthScore switch
                {
                    >= 90 => new SolidColorBrush(Color.FromRgb(0, 212, 255)),
                    >= 70 => new SolidColorBrush(Color.FromRgb(255, 193, 7)),
                    _ => new SolidColorBrush(Color.FromRgb(220, 53, 69))
                };

                // Update active modules count (simulate based on health)
                var activeModules = healthScore >= 80 ? "5 / 5" : healthScore >= 60 ? "4 / 5" : "3 / 5";
                ActiveModulesText.Text = activeModules;
            }
            else
            {
                AddActivityLog($"Health check failed: {healthResponse.Error}");
                StatusIndicator.Text = "ERROR";
                StatusIndicator.Background = new SolidColorBrush(Color.FromRgb(220, 53, 69));
            }
        }
        catch (Exception ex)
        {
            AddActivityLog($"Health update error: {ex.Message}");
        }
    }

    private void AddChatMessage(string sender, string message, bool isSystem = false)
    {
        var messagePanel = new StackPanel
        {
            Margin = new Thickness(0, 5, 0, 5)
        };

        var senderBlock = new TextBlock
        {
            Text = sender,
            FontWeight = FontWeights.Bold,
            FontSize = 12,
            Foreground = isSystem ? new SolidColorBrush(Color.FromRgb(0, 212, 255)) :
                        sender == "You" ? new SolidColorBrush(Color.FromRgb(100, 255, 100)) :
                        new SolidColorBrush(Color.FromRgb(255, 193, 7)),
            Margin = new Thickness(0, 0, 0, 2)
        };

        var messageBlock = new TextBlock
        {
            Text = message,
            FontSize = 14,
            Foreground = new SolidColorBrush(Color.FromRgb(204, 204, 204)),
            TextWrapping = TextWrapping.Wrap,
            Margin = new Thickness(sender == "You" ? 20 : 0, 0, sender == "You" ? 0 : 20, 0)
        };

        messagePanel.Children.Add(senderBlock);
        messagePanel.Children.Add(messageBlock);

        ChatMessages.Children.Add(messagePanel);

        // Auto-scroll to bottom
        ChatScrollViewer.ScrollToEnd();

        _messageCount++;
    }

    private void AddActivityLog(string activity)
    {
        Dispatcher.Invoke(() =>
        {
            var activityBlock = new TextBlock
            {
                Text = $"{DateTime.Now:HH:mm:ss} - {activity}",
                FontSize = 11,
                Foreground = new SolidColorBrush(Color.FromRgb(170, 170, 170)),
                Margin = new Thickness(0, 2, 0, 2),
                TextWrapping = TextWrapping.Wrap
            };

            ActivityLog.Children.Insert(0, activityBlock);

            // Keep only last 20 entries
            while (ActivityLog.Children.Count > 20)
            {
                ActivityLog.Children.RemoveAt(ActivityLog.Children.Count - 1);
            }
        });
    }

    private void UpdateSystemMetrics(object? sender, EventArgs e)
    {
        // Simulate system load (in real implementation, this would get actual metrics)
        var random = new Random();
        var baseLoad = _messageCount * 2; // Base load increases with activity
        var variance = random.NextDouble() * 20 - 10; // ±10% variance
        var currentLoad = Math.Max(15, Math.Min(85, baseLoad + variance));

        LoadProgressBar.Value = currentLoad;
        LoadText.Text = $"{currentLoad:F0}%";
    }

    // Event Handlers
    private async void SendButton_Click(object sender, RoutedEventArgs e)
    {
        await SendMessage();
    }

    private async void ChatInput_KeyDown(object sender, KeyEventArgs e)
    {
        if (e.Key == Key.Enter)
        {
            await SendMessage();
        }
    }

    private async System.Threading.Tasks.Task SendMessage()
    {
        var input = ChatInput.Text.Trim();
        if (string.IsNullOrEmpty(input) || input == "Type your message here...")
            return;

        // Add user message
        AddChatMessage("You", input);
        ChatInput.Text = "";

        // Show typing indicator
        var typingMessage = new TextBlock
        {
            Text = "AIOS is thinking...",
            FontStyle = FontStyles.Italic,
            Foreground = new SolidColorBrush(Color.FromRgb(170, 170, 170)),
            Margin = new Thickness(0, 5, 0, 5)
        };
        ChatMessages.Children.Add(typingMessage);
        ChatScrollViewer.ScrollToEnd();

        AddActivityLog($"Processing user input via {_currentModule} module");

        try
        {
            // Call AI service
            var response = await _aiService.ProcessAsync(_currentModule, input);

            // Remove typing indicator
            ChatMessages.Children.Remove(typingMessage);

            if (response.Success)
            {
                // Add AI response
                AddChatMessage($"AIOS ({_currentModule.ToUpper()})", response.Response ?? "No response");
                AddActivityLog($"Response generated by {_currentModule} module");
            }
            else
            {
                AddChatMessage("AIOS", $"I encountered an error: {response.Error}", true);
                AddActivityLog($"Error in {_currentModule} module: {response.Error}");
            }
        }
        catch (Exception ex)
        {
            // Remove typing indicator
            ChatMessages.Children.Remove(typingMessage);

            AddChatMessage("AIOS", $"Sorry, I encountered an unexpected error: {ex.Message}", true);
            AddActivityLog($"Unexpected error: {ex.Message}");
        }
    }

    // Module Button Handlers
    private void NLPButton_Click(object sender, RoutedEventArgs e)
    {
        _currentModule = "nlp";
        ChatHeader.Text = "Natural Language Processing - Active";
        AddChatMessage("AIOS", " Switched to Natural Language Processing mode. I can help with text analysis, intent recognition, and language understanding.", true);
        AddActivityLog("Switched to NLP module");
    }

    private void PredictionButton_Click(object sender, RoutedEventArgs e)
    {
        _currentModule = "prediction";
        ChatHeader.Text = "Prediction Engine - Active";
        AddChatMessage("AIOS", " Switched to Prediction Engine mode. I can analyze patterns and make predictions based on data.", true);
        AddActivityLog("Switched to Prediction module");
    }

    private void AutomationButton_Click(object sender, RoutedEventArgs e)
    {
        _currentModule = "automation";
        ChatHeader.Text = "Automation System - Active";
        AddChatMessage("AIOS", " Switched to Automation mode. I can help with task automation and process management.", true);
        AddActivityLog("Switched to Automation module");
    }

    private void LearningButton_Click(object sender, RoutedEventArgs e)
    {
        _currentModule = "learning";
        ChatHeader.Text = "Learning System - Active";
        AddChatMessage("AIOS", " Switched to Learning mode. I can adapt and improve based on interactions and feedback.", true);
        AddActivityLog("Switched to Learning module");
    }

    private void IntegrationButton_Click(object sender, RoutedEventArgs e)
    {
        _currentModule = "integration";
        ChatHeader.Text = "Integration Hub - Active";
        AddChatMessage("AIOS", " Switched to Integration mode. I can coordinate between different AI modules and external systems.", true);
        AddActivityLog("Switched to Integration module");
    }

    private async void FormatterButton_Click(object sender, RoutedEventArgs e)
    {
        _currentModule = "formatter";
        ChatHeader.Text = "AINLP Code Formatter - Active";
        AddChatMessage("AIOS", " Switched to Code Formatter mode. I can fix code formatting issues and improve code quality.", true);
        AddActivityLog("Switched to Code Formatter module");

        // Show file dialog for selecting Python file to format
        var dialog = new Microsoft.Win32.OpenFileDialog
        {
            Title = "Select Python file to format",
            Filter = "Python files (*.py)|*.py|All files (*.*)|*.*",
            DefaultExt = "py"
        };

        if (dialog.ShowDialog() == true)
        {
            try
            {
                AddChatMessage("AIOS", $" Analyzing file: {dialog.FileName}", true);

                // Check for E501 violations first
                var checkResult = await _aiService.CheckE501ViolationsAsync(dialog.FileName);

                if (checkResult.HasViolations)
                {
                    AddChatMessage("AIOS", $" Found {checkResult.ViolationCount} E501 violations. Fixing now...", true);

                    // Fix the violations
                    var fixResult = await _aiService.FixE501ViolationsAsync(dialog.FileName);

                    if (fixResult.Success)
                    {
                        AddChatMessage("AIOS", $" Successfully fixed {fixResult.LinesFixed}/{fixResult.TotalViolations} violations in {fixResult.ProcessingTimeMs}ms", true);
                        AddChatMessage("AIOS", $" {fixResult.Summary}", true);
                    }
                    else
                    {
                        AddChatMessage("AIOS", $" Error fixing E501 violations: {fixResult.ErrorMessage}", true);
                    }
                }
                else
                {
                    AddChatMessage("AIOS", " No E501 violations found. Code is already compliant!", true);
                }
            }
            catch (Exception ex)
            {
                AddChatMessage("AIOS", $" Error processing file: {ex.Message}", true);
            }
        }
    }

    private void FileExplorerButton_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            var fileExplorer = new FileExplorerWindow();
            fileExplorer.Owner = this;
            fileExplorer.Show();
            AddActivityLog("Opened File Explorer for code quality operations");
        }
        catch (Exception ex)
        {
            AddChatMessage("AIOS", $" Error opening File Explorer: {ex.Message}", true);
        }
    }

    private async void MaintenanceButton_Click(object sender, RoutedEventArgs e)
    {
        AddChatMessage("AIOS", " Opening Maintenance Center...", true);
        AddActivityLog("Opening Maintenance Center");

        try
        {
            // Open maintenance center window
            var maintenanceWindow = new MaintenanceWindow(_maintenanceService);
            maintenanceWindow.Owner = this;
            maintenanceWindow.Show();

            AddChatMessage("AIOS", " Maintenance Center opened. You can now access all maintenance operations through the dedicated interface.", true);
        }
        catch (Exception ex)
        {
            AddChatMessage("AIOS", $" Error opening Maintenance Center: {ex.Message}", true);
            AddActivityLog($"Maintenance Center error: {ex.Message}");
        }
    }

    private async void HealthCheckButton_Click(object sender, RoutedEventArgs e)
    {
        AddChatMessage("AIOS", " Running comprehensive system health check...", true);
        AddActivityLog("Manual health check requested");

        await UpdateSystemHealth();

        AddChatMessage("AIOS", $"Health check complete. Current status: {StatusIndicator.Text} ({HealthScoreText.Text})", true);
    }

    private void AIIntelligenceButton_Click(object sender, RoutedEventArgs e)
    {
        AddChatMessage("AIOS", " Opening AI Intelligence Control Center...", true);
        AddActivityLog("Opening AI Intelligence Control Center");

        try
        {
            // Open AI Intelligence control window
            var aiWindow = new AIIntelligenceWindow();
            aiWindow.Owner = this;
            aiWindow.Show();

            AddChatMessage("AIOS", " AI Intelligence Control Center opened. You now have full access to the AI supercell through the cytoplasm bridge.", true);
        }
        catch (Exception ex)
        {
            AddChatMessage("AIOS", $" Error opening AI Intelligence Center: {ex.Message}", true);
            AddActivityLog($"AI Intelligence Center error: {ex.Message}");
        }
    }

    private void RuntimeIntelligenceButton_Click(object sender, RoutedEventArgs e)
    {
        AddChatMessage("AIOS", " Opening Runtime Intelligence Control Center...", true);
        AddActivityLog("Opening Runtime Intelligence Control Center");

        try
        {
            // Open Runtime Intelligence control window
            var runtimeWindow = new RuntimeIntelligenceWindow();
            runtimeWindow.Owner = this;
            runtimeWindow.Show();

            AddChatMessage("AIOS", " Runtime Intelligence Control Center opened. Interface Supercell → Runtime Intelligence → AI Intelligence (via Cytoplasm) architecture is active.", true);
        }
        catch (Exception ex)
        {
            AddChatMessage("AIOS", $" Error opening Runtime Intelligence Center: {ex.Message}", true);
            AddActivityLog($"Runtime Intelligence Center error: {ex.Message}");
        }
    }

    private void SettingsButton_Click(object sender, RoutedEventArgs e)
    {
        AddChatMessage("AIOS", " Settings panel will be available in a future update. For now, you can configure the system via configuration files in the config/ directory.", true);
        AddActivityLog("Settings access attempted");
    }

    private async void StartServerButton_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            ServerStatusText.Text = "Starting server...";
            AddChatMessage("AIOS", " Starting Interface Bridge server...", true);
            AddActivityLog("Starting Interface Bridge server");

            // Use the server_manager.py script to start the server
            var startInfo = new System.Diagnostics.ProcessStartInfo
            {
                FileName = "python",
                Arguments = "ai/server_manager.py start",
                WorkingDirectory = @"C:\dev\AIOS",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };

            using var process = System.Diagnostics.Process.Start(startInfo);
            await process.WaitForExitAsync();

            if (process.ExitCode == 0)
            {
                ServerStatusText.Text = "Server running";
                AddChatMessage("AIOS", " Interface Bridge server started successfully on localhost:8000", true);
                AddActivityLog("Interface Bridge server started");
            }
            else
            {
                ServerStatusText.Text = "Start failed";
                AddChatMessage("AIOS", " Failed to start Interface Bridge server", true);
                AddActivityLog("Interface Bridge server start failed");
            }
        }
        catch (Exception ex)
        {
            ServerStatusText.Text = "Error";
            AddChatMessage("AIOS", $" Error starting server: {ex.Message}", true);
            AddActivityLog($"Server start error: {ex.Message}");
        }
    }

    private async void StopServerButton_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            ServerStatusText.Text = "Stopping server...";
            AddChatMessage("AIOS", " Stopping Interface Bridge server...", true);
            AddActivityLog("Stopping Interface Bridge server");

            var startInfo = new System.Diagnostics.ProcessStartInfo
            {
                FileName = "python",
                Arguments = "ai/server_manager.py stop",
                WorkingDirectory = @"C:\dev\AIOS",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };

            using var process = System.Diagnostics.Process.Start(startInfo);
            await process.WaitForExitAsync();

            if (process.ExitCode == 0)
            {
                ServerStatusText.Text = "Server stopped";
                AddChatMessage("AIOS", " Interface Bridge server stopped successfully", true);
                AddActivityLog("Interface Bridge server stopped");
            }
            else
            {
                ServerStatusText.Text = "Stop failed";
                AddChatMessage("AIOS", " Failed to stop Interface Bridge server", true);
                AddActivityLog("Interface Bridge server stop failed");
            }
        }
        catch (Exception ex)
        {
            ServerStatusText.Text = "Error";
            AddChatMessage("AIOS", $" Error stopping server: {ex.Message}", true);
            AddActivityLog($"Server stop error: {ex.Message}");
        }
    }

    private async void RestartServerButton_Click(object sender, RoutedEventArgs e)
    {
        try
        {
            ServerStatusText.Text = "Restarting server...";
            AddChatMessage("AIOS", " Restarting Interface Bridge server...", true);
            AddActivityLog("Restarting Interface Bridge server");

            var startInfo = new System.Diagnostics.ProcessStartInfo
            {
                FileName = "python",
                Arguments = "ai/server_manager.py restart",
                WorkingDirectory = @"C:\dev\AIOS",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true
            };

            using var process = System.Diagnostics.Process.Start(startInfo);
            await process.WaitForExitAsync();

            if (process.ExitCode == 0)
            {
                ServerStatusText.Text = "Server restarted";
                AddChatMessage("AIOS", " Interface Bridge server restarted successfully", true);
                AddActivityLog("Interface Bridge server restarted");
            }
            else
            {
                ServerStatusText.Text = "Restart failed";
                AddChatMessage("AIOS", " Failed to restart Interface Bridge server", true);
                AddActivityLog("Interface Bridge server restart failed");
            }
        }
        catch (Exception ex)
        {
            ServerStatusText.Text = "Error";
            AddChatMessage("AIOS", $" Error restarting server: {ex.Message}", true);
            AddActivityLog($"Server restart error: {ex.Message}");
        }
    }

    // ========================================================================
    // Phase 11 Day 1: AI Search Integration
    // ========================================================================

    /// <summary>
    /// Phase 11: AI Similarity Search button handler
    /// Queries Python AI Layer via Interface Bridge (port 8001)
    /// </summary>
    private async void SearchButton_Click(object sender, RoutedEventArgs e)
    {
        string query = SearchQueryInput.Text?.Trim() ?? "";
        
        if (string.IsNullOrEmpty(query) || 
            query == "Search for functionality (e.g., 'tool for health monitoring')")
        {
            MessageBox.Show(
                "Please enter a search query",
                "AI Search",
                MessageBoxButton.OK,
                MessageBoxImage.Information
            );
            return;
        }

        // Clear previous results
        SearchResults.Children.Clear();

        // Show loading indicator
        var loadingText = new TextBlock
        {
            Text = $"🔍 Searching for: '{query}'",
            FontSize = 14,
            FontWeight = FontWeights.Bold,
            Foreground = new SolidColorBrush(Color.FromRgb(0, 212, 255)),
            Margin = new Thickness(0, 10, 0, 10),
            TextWrapping = TextWrapping.Wrap
        };
        SearchResults.Children.Add(loadingText);

        var loadingSpinner = new TextBlock
        {
            Text = "⏳ Querying AI Layer (Embedding + LLM Consensus)...",
            FontSize = 13,
            Foreground = new SolidColorBrush(Color.FromRgb(170, 170, 170)),
            Margin = new Thickness(0, 0, 0, 10)
        };
        SearchResults.Children.Add(loadingSpinner);

        try
        {
            // Phase 11: Call Python AI Layer via HTTP REST
            var response = await _aiLayerClient.SimilaritySearchAsync(query, maxResults: 5);

            // Clear loading
            SearchResults.Children.Clear();

            if (response?.Results == null || response.Results.Count == 0)
            {
                var noResultsText = new TextBlock
                {
                    Text = "❌ No results found",
                    FontSize = 14,
                    Foreground = new SolidColorBrush(Color.FromRgb(220, 53, 69)),
                    Margin = new Thickness(0, 10, 0, 5)
                };
                SearchResults.Children.Add(noResultsText);
                return;
            }

            // Display success header
            var successText = new TextBlock
            {
                Text = $"✅ Found {response.Results.Count} result(s) via AI Agent Dendritic Similarity",
                FontSize = 14,
                FontWeight = FontWeights.Bold,
                Foreground = new SolidColorBrush(Color.FromRgb(40, 167, 69)),
                Margin = new Thickness(0, 10, 0, 15)
            };
            SearchResults.Children.Add(successText);

            // Display each result
            int rank = 1;
            foreach (var result in response.Results)
            {
                // Result container
                var resultBorder = new Border
                {
                    Background = new SolidColorBrush(Color.FromRgb(62, 62, 66)),
                    CornerRadius = new CornerRadius(8),
                    Padding = new Thickness(15),
                    Margin = new Thickness(0, 0, 0, 15)
                };

                var resultPanel = new StackPanel();

                // Rank and filename
                var titleText = new TextBlock
                {
                    Text = $"#{rank}. {result.Neuron}",
                    FontSize = 15,
                    FontWeight = FontWeights.Bold,
                    Foreground = new SolidColorBrush(Color.FromRgb(0, 212, 255)),
                    Margin = new Thickness(0, 0, 0, 8)
                };
                resultPanel.Children.Add(titleText);

                // Scores
                var scoresPanel = new WrapPanel { Margin = new Thickness(0, 0, 0, 8) };
                
                // Embedding similarity
                var embeddingScore = new TextBlock
                {
                    Text = $"📊 Embedding: {result.EmbeddingScore:P1}",
                    FontSize = 12,
                    Foreground = new SolidColorBrush(Color.FromRgb(170, 170, 170)),
                    Margin = new Thickness(0, 0, 15, 0)
                };
                scoresPanel.Children.Add(embeddingScore);

                // LLM consensus score
                var llmScore = new TextBlock
                {
                    Text = $"🧠 LLM Consensus: {result.LlmScore:P1}",
                    FontSize = 12,
                    Foreground = new SolidColorBrush(Color.FromRgb(170, 170, 170)),
                    Margin = new Thickness(0, 0, 15, 0)
                };
                scoresPanel.Children.Add(llmScore);

                // Final score (use Similarity property)
                var finalScore = new TextBlock
                {
                    Text = $"⭐ Final: {result.Similarity:P1}",
                    FontSize = 12,
                    FontWeight = FontWeights.Bold,
                    Foreground = new SolidColorBrush(Color.FromRgb(255, 215, 0))
                };
                scoresPanel.Children.Add(finalScore);

                resultPanel.Children.Add(scoresPanel);

                // LLM reasoning
                if (!string.IsNullOrWhiteSpace(result.Reasoning))
                {
                    var reasoningText = new TextBlock
                    {
                        Text = $"💭 {result.Reasoning}",
                        FontSize = 12,
                        Foreground = new SolidColorBrush(Color.FromRgb(204, 204, 204)),
                        TextWrapping = TextWrapping.Wrap,
                        Margin = new Thickness(0, 0, 0, 8)
                    };
                    resultPanel.Children.Add(reasoningText);
                }

                // File path
                var pathText = new TextBlock
                {
                    Text = $"📁 {result.Path}",
                    FontSize = 11,
                    Foreground = new SolidColorBrush(Color.FromRgb(136, 136, 136)),
                    TextWrapping = TextWrapping.Wrap
                };
                resultPanel.Children.Add(pathText);

                resultBorder.Child = resultPanel;
                SearchResults.Children.Add(resultBorder);

                rank++;
            }

            // Log success
            AddActivityLog($"AI Search: {response.Results.Count} results for '{query}'");
        }
        catch (HttpRequestException ex)
        {
            SearchResults.Children.Clear();
            
            var errorText = new TextBlock
            {
                Text = "❌ Interface Bridge Connection Error",
                FontSize = 14,
                FontWeight = FontWeights.Bold,
                Foreground = new SolidColorBrush(Color.FromRgb(220, 53, 69)),
                Margin = new Thickness(0, 10, 0, 10)
            };
            SearchResults.Children.Add(errorText);

            var detailsText = new TextBlock
            {
                Text = $"Could not connect to Python AI Layer (port 8001).\n\nError: {ex.Message}\n\nEnsure Interface Bridge server is running:\npython ai/server_manager.py start",
                FontSize = 12,
                Foreground = new SolidColorBrush(Color.FromRgb(170, 170, 170)),
                TextWrapping = TextWrapping.Wrap
            };
            SearchResults.Children.Add(detailsText);

            AddActivityLog($"AI Search failed: {ex.Message}");
        }
        catch (Exception ex)
        {
            SearchResults.Children.Clear();
            
            var errorText = new TextBlock
            {
                Text = "❌ Unexpected Error",
                FontSize = 14,
                FontWeight = FontWeights.Bold,
                Foreground = new SolidColorBrush(Color.FromRgb(220, 53, 69)),
                Margin = new Thickness(0, 10, 0, 10)
            };
            SearchResults.Children.Add(errorText);

            var detailsText = new TextBlock
            {
                Text = $"Error: {ex.Message}\n\nStack Trace:\n{ex.StackTrace}",
                FontSize = 11,
                Foreground = new SolidColorBrush(Color.FromRgb(170, 170, 170)),
                TextWrapping = TextWrapping.Wrap
            };
            SearchResults.Children.Add(detailsText);

            AddActivityLog($"AI Search error: {ex.Message}");
        }
    }
}
