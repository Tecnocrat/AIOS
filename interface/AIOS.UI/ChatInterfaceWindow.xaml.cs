using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Threading;
using AIOS.Models;
using AIOS.Services;

namespace AIOS.UI;

/// <summary>
/// Enhanced Chat Interface Window for AI Agent Interaction
/// Provides comprehensive chat capabilities with AI agents, file operations, and linting commands
/// </summary>
public partial class ChatInterfaceWindow : Window
{
    private readonly HttpClient _httpClient;
    private readonly DispatcherTimer _statusTimer;
    private readonly DispatcherTimer _connectionTimer;
    private ObservableCollection<AgentInfo> _availableAgents;
    private AgentInfo _selectedAgent;
    private List<ChatMessage> _chatHistory;
    private bool _isConnected;
    private string _interfaceBridgeUrl = "http://localhost:8000";

    public ChatInterfaceWindow()
    {
        InitializeComponent();

        _httpClient = new HttpClient();
        _httpClient.Timeout = TimeSpan.FromSeconds(30);

        _availableAgents = new ObservableCollection<AgentInfo>();
        _chatHistory = new List<ChatMessage>();

        _statusTimer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(5) };
        _statusTimer.Tick += StatusTimer_Tick;

        _connectionTimer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(10) };
        _connectionTimer.Tick += ConnectionTimer_Tick;

        InitializeAsync();
    }

    private async void InitializeAsync()
    {
        try
        {
            UpdateStatus("Initializing chat interface...");
            await LoadAvailableAgents();
            SetupAgentButtons();
            _statusTimer.Start();
            _connectionTimer.Start();
            UpdateStatus("Chat interface ready");
        }
        catch (Exception ex)
        {
            UpdateStatus($"Initialization failed: {ex.Message}");
            AddSystemMessage("Failed to initialize chat interface. Please check Interface Bridge connection.");
        }
    }

    private async Task LoadAvailableAgents()
    {
        try
        {
            var response = await _httpClient.GetAsync($"{_interfaceBridgeUrl}/tools");
            response.EnsureSuccessStatusCode();

            var content = await response.Content.ReadAsStringAsync();
            var toolsResponse = JsonSerializer.Deserialize<ToolsResponse>(content);

            if (toolsResponse?.Tools != null)
            {
                _availableAgents.Clear();
                foreach (var tool in toolsResponse.Tools)
                {
                    var agent = new AgentInfo
                    {
                        Name = tool.Name,
                        DisplayName = tool.DisplayName,
                        Description = tool.Description,
                        Category = tool.Category,
                        Status = tool.Status,
                        Capabilities = tool.Capabilities ?? new List<string>(),
                        Version = tool.Version
                    };
                    _availableAgents.Add(agent);
                }
            }

            UpdateConnectionStatus(true);
        }
        catch (Exception ex)
        {
            UpdateConnectionStatus(false);
            AddSystemMessage($"Failed to load agents: {ex.Message}");
        }
    }

    private void SetupAgentButtons()
    {
        AgentButtonsPanel.Children.Clear();

        foreach (var agent in _availableAgents)
        {
            var button = new Button
            {
                Content = $"{GetAgentIcon(agent.Category)} {agent.DisplayName}",
                Tag = agent,
                Style = (Style)FindResource("AgentButtonStyle"),
                ToolTip = agent.Description
            };

            button.Click += AgentButton_Click;
            AgentButtonsPanel.Children.Add(button);
        }
    }

    private string GetAgentIcon(string category)
    {
        return category.ToLower() switch
        {
            "ai_cell" => "🧠",
            "tool" => "🔧",
            "service" => "⚙️",
            "integration" => "🔗",
            _ => "🤖"
        };
    }

    private void AgentButton_Click(object sender, RoutedEventArgs e)
    {
        if (sender is Button button && button.Tag is AgentInfo agent)
        {
            SelectAgent(agent);
        }
    }

    private void SelectAgent(AgentInfo agent)
    {
        _selectedAgent = agent;
        ChatHeaderText.Text = $"Chatting with {agent.DisplayName}";
        ActiveAgentText.Text = agent.DisplayName;
        AgentStatusIndicator.Text = agent.Status.ToUpper();

        // Update capabilities display
        AgentCapabilitiesText.Text = string.Join(", ", agent.Capabilities);

        // Update status
        UpdateStatus($"Selected agent: {agent.DisplayName}");

        // Add system message
        AddSystemMessage($"Switched to agent: {agent.DisplayName} ({agent.Description})");
    }

    private async void SendMessageButton_Click(object sender, RoutedEventArgs e)
    {
        await SendMessage();
    }

    private async void ChatInputTextBox_KeyDown(object sender, KeyEventArgs e)
    {
        if (e.Key == Key.Enter && (Keyboard.Modifiers & ModifierKeys.Control) == ModifierKeys.Control)
        {
            e.Handled = true;
            await SendMessage();
        }
    }

    private async Task SendMessage()
    {
        if (_selectedAgent == null)
        {
            AddSystemMessage("Please select an agent first");
            return;
        }

        var message = ChatInputTextBox.Text.Trim();
        if (string.IsNullOrEmpty(message))
            return;

        // Add user message to chat
        AddUserMessage(message);
        ChatInputTextBox.Clear();

        // Show typing indicator
        ShowTypingIndicator();

        try
        {
            UpdateStatus("Sending message to agent...");

            var parameters = new Dictionary<string, object>
            {
                ["message"] = message,
                ["agent"] = _selectedAgent.Name,
                ["context"] = GetChatContext()
            };

            var response = await ExecuteAgentTool(_selectedAgent.Name, parameters);

            // Hide typing indicator
            HideTypingIndicator();

            // Add agent response
            AddAgentMessage(response);

            UpdateStatus("Message sent successfully");
        }
        catch (Exception ex)
        {
            HideTypingIndicator();
            AddSystemMessage($"Failed to send message: {ex.Message}");
            UpdateStatus("Message failed");
        }
    }

    private async Task<string> ExecuteAgentTool(string toolName, Dictionary<string, object> parameters)
    {
        try
        {
            var requestData = new { parameters };
            var json = JsonSerializer.Serialize(requestData);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync($"{_interfaceBridgeUrl}/tools/{toolName}/execute", content);
            response.EnsureSuccessStatusCode();

            var responseContent = await response.Content.ReadAsStringAsync();
            var result = JsonSerializer.Deserialize<AgentResponse>(responseContent);

            return result?.Result ?? "No response from agent";
        }
        catch (Exception ex)
        {
            throw new Exception($"Agent execution failed: {ex.Message}");
        }
    }

    private List<Dictionary<string, object>> GetChatContext()
    {
        // Return recent chat history for context
        return _chatHistory.TakeLast(10).Select(m => new Dictionary<string, object>
        {
            ["role"] = m.IsUser ? "user" : "agent",
            ["content"] = m.Content,
            ["timestamp"] = m.Timestamp
        }).ToList();
    }

    private void AddUserMessage(string message)
    {
        var chatMessage = new ChatMessage
        {
            Content = message,
            IsUser = true,
            Timestamp = DateTime.Now
        };

        _chatHistory.Add(chatMessage);
        AddMessageToUI(chatMessage);
    }

    private void AddAgentMessage(string message)
    {
        var chatMessage = new ChatMessage
        {
            Content = message,
            IsUser = false,
            Timestamp = DateTime.Now
        };

        _chatHistory.Add(chatMessage);
        AddMessageToUI(chatMessage);
    }

    private void AddSystemMessage(string message)
    {
        var chatMessage = new ChatMessage
        {
            Content = message,
            IsUser = false,
            IsSystem = true,
            Timestamp = DateTime.Now
        };

        AddMessageToUI(chatMessage);
    }

    private void AddMessageToUI(ChatMessage message)
    {
        var border = new Border
        {
            Margin = new Thickness(0, 5, 0, 5),
            Padding = new Thickness(15, 10, 15, 10),
            CornerRadius = new CornerRadius(8),
            MaxWidth = 600
        };

        var textBlock = new TextBlock
        {
            Text = message.Content,
            TextWrapping = TextWrapping.Wrap,
            FontSize = 13,
            Foreground = Brushes.White
        };

        border.Child = textBlock;

        if (message.IsSystem)
        {
            border.Background = new SolidColorBrush(Color.FromRgb(62, 62, 66));
            border.HorizontalAlignment = HorizontalAlignment.Center;
            border.Opacity = 0.8;
        }
        else if (message.IsUser)
        {
            border.Background = new SolidColorBrush(Color.FromRgb(0, 122, 204));
            border.HorizontalAlignment = HorizontalAlignment.Right;
        }
        else
        {
            border.Background = new SolidColorBrush(Color.FromRgb(45, 45, 48));
            border.HorizontalAlignment = HorizontalAlignment.Left;
        }

        ChatMessagesPanel.Children.Add(border);
        ScrollToBottom();
    }

    private void ShowTypingIndicator()
    {
        var typingBorder = new Border
        {
            Background = new SolidColorBrush(Color.FromRgb(45, 45, 48)),
            CornerRadius = new CornerRadius(8),
            Padding = new Thickness(15, 10, 15, 10),
            Margin = new Thickness(0, 5, 0, 5),
            HorizontalAlignment = HorizontalAlignment.Left,
            Name = "TypingIndicator"
        };

        var typingText = new TextBlock
        {
            Text = "Agent is typing...",
            Foreground = new SolidColorBrush(Color.FromRgb(170, 170, 170)),
            FontSize = 12,
            FontStyle = FontStyles.Italic
        };

        typingBorder.Child = typingText;
        ChatMessagesPanel.Children.Add(typingBorder);
        ScrollToBottom();
    }

    private void HideTypingIndicator()
    {
        var typingIndicator = ChatMessagesPanel.Children
            .OfType<Border>()
            .FirstOrDefault(b => b.Name == "TypingIndicator");

        if (typingIndicator != null)
        {
            ChatMessagesPanel.Children.Remove(typingIndicator);
        }
    }

    private void ScrollToBottom()
    {
        ChatScrollViewer.ScrollToBottom();
    }

    private async void LintCurrentFileButton_Click(object sender, RoutedEventArgs e)
    {
        if (_selectedAgent == null)
        {
            AddSystemMessage("Please select an agent first");
            return;
        }

        // This would integrate with VSCode extension to get current file
        AddSystemMessage("Linting current file... (Integration with VSCode extension needed)");
    }

    private async void FixE501Button_Click(object sender, RoutedEventArgs e)
    {
        if (_selectedAgent == null)
        {
            AddSystemMessage("Please select an agent first");
            return;
        }

        try
        {
            UpdateStatus("Running E501 fixer...");

            var parameters = new Dictionary<string, object>
            {
                ["operation"] = "fix_e501",
                ["dry_run"] = true
            };

            var result = await ExecuteAgentTool("agentic_e501_fixer", parameters);
            AddAgentMessage($"E501 Fix Results:\n{result}");

            UpdateStatus("E501 fixing completed");
        }
        catch (Exception ex)
        {
            AddSystemMessage($"E501 fixing failed: {ex.Message}");
            UpdateStatus("E501 fixing failed");
        }
    }

    private async void AnalyzeCodeButton_Click(object sender, RoutedEventArgs e)
    {
        if (_selectedAgent == null)
        {
            AddSystemMessage("Please select an agent first");
            return;
        }

        AddSystemMessage("Code analysis feature coming soon...");
    }

    private async void RefreshAgentsButton_Click(object sender, RoutedEventArgs e)
    {
        UpdateStatus("Refreshing agents...");
        await LoadAvailableAgents();
        SetupAgentButtons();
        UpdateStatus("Agents refreshed");
    }

    private void ClearChatButton_Click(object sender, RoutedEventArgs e)
    {
        ChatMessagesPanel.Children.Clear();
        _chatHistory.Clear();
        AddSystemMessage("Chat history cleared");
        UpdateStatus("Chat cleared");
    }

    private void SettingsButton_Click(object sender, RoutedEventArgs e)
    {
        // Open settings dialog
        AddSystemMessage("Settings dialog coming soon...");
    }

    private void AttachFileButton_Click(object sender, RoutedEventArgs e)
    {
        // Open file dialog for attachment
        AddSystemMessage("File attachment feature coming soon...");
    }

    private void VoiceInputButton_Click(object sender, RoutedEventArgs e)
    {
        // Start voice input
        AddSystemMessage("Voice input feature coming soon...");
    }

    private void StatusTimer_Tick(object sender, EventArgs e)
    {
        UpdateLastActivity();
    }

    private void ConnectionTimer_Tick(object sender, EventArgs e)
    {
        CheckConnection();
    }

    private async void CheckConnection()
    {
        try
        {
            var response = await _httpClient.GetAsync($"{_interfaceBridgeUrl}/health");
            UpdateConnectionStatus(response.IsSuccessStatusCode);
        }
        catch
        {
            UpdateConnectionStatus(false);
        }
    }

    private void UpdateConnectionStatus(bool isConnected)
    {
        _isConnected = isConnected;
        ConnectionStatus.Text = isConnected ? "🔗 Connected" : "❌ Disconnected";
        ConnectionStatus.Foreground = isConnected ?
            new SolidColorBrush(Color.FromRgb(0, 255, 0)) :
            new SolidColorBrush(Color.FromRgb(255, 0, 0));
    }

    private void UpdateStatus(string status)
    {
        StatusBarText.Text = status;
        LastActivityText.Text = $"Last activity: {DateTime.Now:HH:mm:ss}";
    }

    private void UpdateLastActivity()
    {
        if (_chatHistory.Any())
        {
            var lastMessage = _chatHistory.Last();
            LastActivityText.Text = $"Last message: {lastMessage.Timestamp:HH:mm:ss}";
        }
    }

    protected override void OnClosed(EventArgs e)
    {
        _statusTimer.Stop();
        _connectionTimer.Stop();
        _httpClient.Dispose();
        base.OnClosed(e);
    }
}

// Supporting classes
public class AgentInfo
{
    public string Name { get; set; }
    public string DisplayName { get; set; }
    public string Description { get; set; }
    public string Category { get; set; }
    public string Status { get; set; }
    public List<string> Capabilities { get; set; }
    public string Version { get; set; }
}

public class ChatMessage
{
    public string Content { get; set; }
    public bool IsUser { get; set; }
    public bool IsSystem { get; set; }
    public DateTime Timestamp { get; set; }
}

public class ToolsResponse
{
    public List<ToolInfo> Tools { get; set; }
    public int TotalCount { get; set; }
}

public class ToolInfo
{
    public string Name { get; set; }
    public string DisplayName { get; set; }
    public string Description { get; set; }
    public string Category { get; set; }
    public string Status { get; set; }
    public List<string> Capabilities { get; set; }
    public string Version { get; set; }
}

public class AgentResponse
{
    public string Result { get; set; }
    public bool Success { get; set; }
    public string Error { get; set; }
}