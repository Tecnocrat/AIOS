using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Threading;
using AIOS.Services;

namespace AIOS.UI;

/// <summary>
/// Interaction logic for MainWindow.xaml
/// </summary>
public partial class MainWindow : Window
{
    private readonly DispatcherTimer _healthTimer;
    private readonly DispatcherTimer _activityTimer;
    private readonly AIServiceManager _aiService;
    private string _currentModule = "nlp";
    private int _messageCount = 0;

    public MainWindow()
    {
        InitializeComponent();
        _aiService = new AIServiceManager();
        InitializeUI();
        InitializeTimers();
        LoadSystemStatus();
    }

    private void InitializeUI()
    {
        // Set initial focus and placeholder behavior
        ChatInput.GotFocus += (s, e) => {
            if (ChatInput.Text == "Type your message here...")
            {
                ChatInput.Text = "";
                ChatInput.Foreground = Brushes.White;
            }
        };

        ChatInput.LostFocus += (s, e) => {
            if (string.IsNullOrWhiteSpace(ChatInput.Text))
            {
                ChatInput.Text = "Type your message here...";
                ChatInput.Foreground = new SolidColorBrush(Color.FromRgb(170, 170, 170));
            }
        };

        // Add welcome message
        AddChatMessage("AIOS", "Welcome to AIOS! I'm your AI assistant. Click on any module to switch modes, or just start chatting!", true);
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
                    .Replace("🟢 ", "").Replace("🟡 ", "").Replace("🔴 ", "")
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
        AddChatMessage("AIOS", "🧠 Switched to Natural Language Processing mode. I can help with text analysis, intent recognition, and language understanding.", true);
        AddActivityLog("Switched to NLP module");
    }

    private void PredictionButton_Click(object sender, RoutedEventArgs e)
    {
        _currentModule = "prediction";
        ChatHeader.Text = "Prediction Engine - Active";
        AddChatMessage("AIOS", "🔮 Switched to Prediction Engine mode. I can analyze patterns and make predictions based on data.", true);
        AddActivityLog("Switched to Prediction module");
    }

    private void AutomationButton_Click(object sender, RoutedEventArgs e)
    {
        _currentModule = "automation";
        ChatHeader.Text = "Automation System - Active";
        AddChatMessage("AIOS", "🔧 Switched to Automation mode. I can help with task automation and process management.", true);
        AddActivityLog("Switched to Automation module");
    }

    private void LearningButton_Click(object sender, RoutedEventArgs e)
    {
        _currentModule = "learning";
        ChatHeader.Text = "Learning System - Active";
        AddChatMessage("AIOS", "📚 Switched to Learning mode. I can adapt and improve based on interactions and feedback.", true);
        AddActivityLog("Switched to Learning module");
    }

    private void IntegrationButton_Click(object sender, RoutedEventArgs e)
    {
        _currentModule = "integration";
        ChatHeader.Text = "Integration Hub - Active";
        AddChatMessage("AIOS", "🔗 Switched to Integration mode. I can coordinate between different AI modules and external systems.", true);
        AddActivityLog("Switched to Integration module");
    }

    private async void HealthCheckButton_Click(object sender, RoutedEventArgs e)
    {
        AddChatMessage("AIOS", "🏥 Running comprehensive system health check...", true);
        AddActivityLog("Manual health check requested");
        
        await UpdateSystemHealth();
        
        AddChatMessage("AIOS", $"Health check complete. Current status: {StatusIndicator.Text} ({HealthScoreText.Text})", true);
    }

    private void SettingsButton_Click(object sender, RoutedEventArgs e)
    {
        AddChatMessage("AIOS", "⚙️ Settings panel will be available in a future update. For now, you can configure the system via configuration files in the config/ directory.", true);
        AddActivityLog("Settings access attempted");
    }
}