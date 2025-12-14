using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Threading;
using AIOS.Models;
using AIOS.Services;

namespace AIOS.UI;

/// <summary>
/// File Explorer Window for AIOS - Code Quality and File Management Hub
/// Provides directory browsing, file analysis, and integrated linting operations
/// </summary>
public partial class FileExplorerWindow : Window
{
    private readonly HttpClient _httpClient;
    private readonly DispatcherTimer _statusTimer;
    private readonly DispatcherTimer _connectionTimer;
    private ObservableCollection<FileSystemItem> _currentDirectoryItems;
    private string _currentDirectory;
    private bool _isConnected;
    private string _interfaceBridgeUrl = "http://localhost:8000";
    private List<FileSystemItem> _selectedFiles;
    private List<string> _recentOperations;

    public FileExplorerWindow()
    {
        InitializeComponent();

        _httpClient = new HttpClient();
        _httpClient.Timeout = TimeSpan.FromSeconds(30);

        _currentDirectoryItems = new ObservableCollection<FileSystemItem>();
        _selectedFiles = new List<FileSystemItem>();
        _recentOperations = new List<string>();

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
            UpdateStatus("Initializing file explorer...");
            await LoadDirectoryTree();
            _statusTimer.Start();
            _connectionTimer.Start();
            UpdateStatus("File explorer ready");
        }
        catch (Exception ex)
        {
            UpdateStatus($"Initialization failed: {ex.Message}");
        }
    }

    private async Task LoadDirectoryTree()
    {
        try
        {
            var rootPath = @"C:\dev\AIOS";
            var rootItem = CreateDirectoryItem(new DirectoryInfo(rootPath));
            DirectoryTreeView.Items.Clear();
            DirectoryTreeView.Items.Add(rootItem);
        }
        catch (Exception ex)
        {
            UpdateStatus($"Failed to load directory tree: {ex.Message}");
        }
    }

    private TreeViewItem CreateDirectoryItem(DirectoryInfo dirInfo)
    {
        var item = new TreeViewItem
        {
            Header = $"📁 {dirInfo.Name}",
            Tag = dirInfo.FullName
        };

        try
        {
            foreach (var subDir in dirInfo.GetDirectories())
            {
                // Only add subdirectories that are relevant to AIOS
                if (IsRelevantDirectory(subDir))
                {
                    var subItem = CreateDirectoryItem(subDir);
                    item.Items.Add(subItem);
                }
            }
        }
        catch
        {
            // Ignore access denied errors
        }

        return item;
    }

    private bool IsRelevantDirectory(DirectoryInfo dir)
    {
        var relevantNames = new[] { "ai", "core", "interface", "docs", "runtime", "tachyonic", "evolution_lab" };
        return relevantNames.Contains(dir.Name.ToLower()) ||
               dir.Name.StartsWith("AIOS.") ||
               dir.Name.Contains("AIOS");
    }

    private void DirectoryTreeView_SelectedItemChanged(object sender, RoutedPropertyChangedEventArgs<object> e)
    {
        if (e.NewValue is TreeViewItem item && item.Tag is string path)
        {
            LoadDirectoryContents(path);
        }
    }

    private void LoadDirectoryContents(string path)
    {
        try
        {
            _currentDirectory = path;
            CurrentPathText.Text = path;

            var dirInfo = new DirectoryInfo(path);
            _currentDirectoryItems.Clear();

            // Add parent directory if not root
            if (dirInfo.Parent != null)
            {
                _currentDirectoryItems.Add(new FileSystemItem
                {
                    Name = "..",
                    FullPath = dirInfo.Parent.FullName,
                    IsDirectory = true,
                    Icon = "📁",
                    Size = "",
                    Modified = ""
                });
            }

            // Add subdirectories
            foreach (var subDir in dirInfo.GetDirectories().OrderBy(d => d.Name))
            {
                _currentDirectoryItems.Add(new FileSystemItem
                {
                    Name = subDir.Name,
                    FullPath = subDir.FullName,
                    IsDirectory = true,
                    Icon = "📁",
                    Size = "",
                    Modified = subDir.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
                });
            }

            // Add files
            foreach (var file in dirInfo.GetFiles().OrderBy(f => f.Name))
            {
                _currentDirectoryItems.Add(new FileSystemItem
                {
                    Name = file.Name,
                    FullPath = file.FullName,
                    IsDirectory = false,
                    Icon = GetFileIcon(file.Extension),
                    Size = FormatFileSize(file.Length),
                    Modified = file.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
                });
            }

            FileListBox.ItemsSource = _currentDirectoryItems;
            UpdateSelectedFilesText();
            UpdateStatus($"Loaded directory: {path}");
        }
        catch (Exception ex)
        {
            UpdateStatus($"Failed to load directory: {ex.Message}");
        }
    }

    private string GetFileIcon(string extension)
    {
        return extension.ToLower() switch
        {
            ".py" => "🐍",
            ".cs" => "🔷",
            ".cpp" => "⚡",
            ".h" => "📋",
            ".xaml" => "🎨",
            ".json" => "📄",
            ".md" => "📝",
            ".txt" => "📄",
            ".exe" => "⚙️",
            ".dll" => "🔧",
            _ => "📄"
        };
    }

    private string FormatFileSize(long bytes)
    {
        string[] sizes = { "B", "KB", "MB", "GB" };
        int order = 0;
        double size = bytes;

        while (size >= 1024 && order < sizes.Length - 1)
        {
            order++;
            size /= 1024;
        }

        return $"{size:0.##} {sizes[order]}";
    }

    private void FileListBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        _selectedFiles = FileListBox.SelectedItems.Cast<FileSystemItem>().ToList();
        UpdateSelectedFilesText();
    }

    private void UpdateSelectedFilesText()
    {
        if (_selectedFiles.Count == 0)
        {
            SelectedFilesText.Text = "No files selected";
        }
        else if (_selectedFiles.Count == 1)
        {
            SelectedFilesText.Text = $"1 file selected: {_selectedFiles[0].Name}";
        }
        else
        {
            SelectedFilesText.Text = $"{_selectedFiles.Count} files selected";
        }
    }

    private async void LintDirectoryButton_Click(object sender, RoutedEventArgs e)
    {
        if (string.IsNullOrEmpty(_currentDirectory))
        {
            UpdateStatus("No directory selected");
            return;
        }

        await RunDirectoryLinting(_currentDirectory, false);
    }

    private async void FixE501DirectoryButton_Click(object sender, RoutedEventArgs e)
    {
        if (string.IsNullOrEmpty(_currentDirectory))
        {
            UpdateStatus("No directory selected");
            return;
        }

        await RunDirectoryLinting(_currentDirectory, true);
    }

    private async Task RunDirectoryLinting(string directoryPath, bool fixIssues)
    {
        try
        {
            UpdateStatus($"{(fixIssues ? "Fixing" : "Analyzing")} E501 issues in directory...");
            ShowProgress(true);

            var parameters = new Dictionary<string, object>
            {
                ["operation"] = fixIssues ? "fix_directory" : "analyze_directory",
                ["directory"] = directoryPath,
                ["recursive"] = true
            };

            var result = await ExecuteAgentTool("agentic_e501_fixer", parameters);

            AddRecentOperation($"{(fixIssues ? "Fixed" : "Analyzed")} E501 in {Path.GetFileName(directoryPath)}");
            UpdateStatus($"{(fixIssues ? "Fixed" : "Analyzed")} E501 issues in directory");

            // Parse and display results
            UpdateAnalysisResults(result);

            ShowProgress(false);
        }
        catch (Exception ex)
        {
            ShowProgress(false);
            UpdateStatus($"Directory {(fixIssues ? "fixing" : "analysis")} failed: {ex.Message}");
        }
    }

    private async void LintSelectedButton_Click(object sender, RoutedEventArgs e)
    {
        if (!_selectedFiles.Any())
        {
            UpdateStatus("No files selected");
            return;
        }

        await RunFileLinting(_selectedFiles.Where(f => !f.IsDirectory).Select(f => f.FullPath).ToList(), false);
    }

    private async void FixE501SelectedButton_Click(object sender, RoutedEventArgs e)
    {
        if (!_selectedFiles.Any())
        {
            UpdateStatus("No files selected");
            return;
        }

        await RunFileLinting(_selectedFiles.Where(f => !f.IsDirectory).Select(f => f.FullPath).ToList(), true);
    }

    private async Task RunFileLinting(List<string> filePaths, bool fixIssues)
    {
        try
        {
            UpdateStatus($"{(fixIssues ? "Fixing" : "Analyzing")} {filePaths.Count} selected files...");
            ShowProgress(true);

            var parameters = new Dictionary<string, object>
            {
                ["operation"] = fixIssues ? "fix_files" : "analyze_files",
                ["files"] = filePaths
            };

            var result = await ExecuteAgentTool("agentic_e501_fixer", parameters);

            AddRecentOperation($"{(fixIssues ? "Fixed" : "Analyzed")} {filePaths.Count} files");
            UpdateStatus($"{(fixIssues ? "Fixed" : "Analyzed")} selected files");

            UpdateAnalysisResults(result);

            ShowProgress(false);
        }
        catch (Exception ex)
        {
            ShowProgress(false);
            UpdateStatus($"File {(fixIssues ? "fixing" : "analysis")} failed: {ex.Message}");
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

    private void UpdateAnalysisResults(string result)
    {
        try
        {
            // Parse the result to extract metrics
            // This is a simplified parsing - in reality you'd parse the actual agent response format
            var lines = result.Split('\n');
            var e501Count = lines.Count(l => l.Contains("E501"));
            var filesAnalyzed = lines.Count(l => l.Contains("File:"));

            E501CountText.Text = e501Count.ToString();
            FilesAnalyzedText.Text = filesAnalyzed.ToString();
        }
        catch
        {
            // If parsing fails, just update with basic info
            E501CountText.Text = "N/A";
            FilesAnalyzedText.Text = "N/A";
        }
    }

    private void AddRecentOperation(string operation)
    {
        _recentOperations.Insert(0, $"{DateTime.Now:HH:mm:ss} - {operation}");
        if (_recentOperations.Count > 10)
        {
            _recentOperations.RemoveAt(_recentOperations.Count - 1);
        }

        RecentOperationsList.ItemsSource = null;
        RecentOperationsList.ItemsSource = _recentOperations;
        LastOperationText.Text = operation;
    }

    private void AnalyzeDirectoryButton_Click(object sender, RoutedEventArgs e)
    {
        UpdateStatus("Directory analysis feature coming soon...");
    }

    private void BackupDirectoryButton_Click(object sender, RoutedEventArgs e)
    {
        UpdateStatus("Directory backup feature coming soon...");
    }

    private void ViewFileButton_Click(object sender, RoutedEventArgs e)
    {
        if (_selectedFiles.Count == 1 && !_selectedFiles[0].IsDirectory)
        {
            UpdateStatus($"Viewing file: {_selectedFiles[0].Name}");
            // In a real implementation, this would open the file in an editor
        }
        else
        {
            UpdateStatus("Select a single file to view");
        }
    }

    private async void BatchLintButton_Click(object sender, RoutedEventArgs e)
    {
        UpdateStatus("Batch linting feature coming soon...");
    }

    private async void BatchFixButton_Click(object sender, RoutedEventArgs e)
    {
        UpdateStatus("Batch E501 fixing feature coming soon...");
    }

    private void GoToAIButton_Click(object sender, RoutedEventArgs e)
    {
        LoadDirectoryContents(@"C:\dev\AIOS\ai");
    }

    private void GoToCoreButton_Click(object sender, RoutedEventArgs e)
    {
        LoadDirectoryContents(@"C:\dev\AIOS\core");
    }

    private void GoToInterfaceButton_Click(object sender, RoutedEventArgs e)
    {
        LoadDirectoryContents(@"C:\dev\AIOS\interface");
    }

    private async void RefreshButton_Click(object sender, RoutedEventArgs e)
    {
        UpdateStatus("Refreshing...");
        await LoadDirectoryTree();
        if (!string.IsNullOrEmpty(_currentDirectory))
        {
            LoadDirectoryContents(_currentDirectory);
        }
        UpdateStatus("Refreshed");
    }

    private void SettingsButton_Click(object sender, RoutedEventArgs e)
    {
        UpdateStatus("Settings dialog coming soon...");
    }

    private void StatusTimer_Tick(object sender, EventArgs e)
    {
        UpdateAgentStatus();
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
            System.Windows.Media.Brushes.LimeGreen :
            System.Windows.Media.Brushes.Red;
    }

    private void UpdateAgentStatus()
    {
        AgentStatusText.Text = _isConnected ? "Ready" : "Disconnected";
        AgentStatusText.Foreground = _isConnected ?
            System.Windows.Media.Brushes.LimeGreen :
            System.Windows.Media.Brushes.Red;
    }

    private void UpdateStatus(string status)
    {
        StatusBarText.Text = status;
    }

    private void ShowProgress(bool show)
    {
        OperationProgressBar.Visibility = show ? Visibility.Visible : Visibility.Collapsed;
        ProgressText.Text = show ? "Processing..." : "";
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
public class FileSystemItem
{
    public string Name { get; set; }
    public string FullPath { get; set; }
    public bool IsDirectory { get; set; }
    public string Icon { get; set; }
    public string Size { get; set; }
    public string Modified { get; set; }
}

<<<<<<< HEAD
// TEMP: Commented out due to duplicate definition error (Phase 11 Day 1)
// public class AgentResponse
// {
//     public string Result { get; set; }
//     public bool Success { get; set; }
//     public string Error { get; set; }
// }
=======
public class AgentResponse
{
    public string Result { get; set; }
    public bool Success { get; set; }
    public string Error { get; set; }
}
>>>>>>> origin/OS0.6.2.grok
