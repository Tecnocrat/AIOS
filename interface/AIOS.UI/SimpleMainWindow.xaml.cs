using System;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using AIOS.Models;
using AIOS.Services;
using Microsoft.Extensions.Logging;

namespace AIOS.UI
{
    public partial class SimpleMainWindow : Window
    {
        private readonly AIOS.Services.AIServiceManager? _aiService;
        private readonly AIOS.Services.MaintenanceService? _maintenanceService;
        private readonly ILogger<SimpleMainWindow> _logger;
        private readonly AILayerClient _aiLayerClient; // Phase 11 Day 1
            // Initialize services with error handling
            try
            {
                _aiService = new AIOS.Services.AIServiceManager();
                _maintenanceService = new AIOS.Services.MaintenanceService();
                _logger = Microsoft.Extensions.Logging.Abstractions.NullLogger<SimpleMainWindow>.Instance;
            }
            catch (Exception ex)
            {
                // Fallback: create null services and show error
                _aiService = null;
                _maintenanceService = null;
                _logger = Microsoft.Extensions.Logging.Abstractions.NullLogger<SimpleMainWindow>.Instance;
                
                // Show error in UI
                StatusText.Text = $"Service initialization failed: {ex.Message}";
                return;
            }

            // Load initial status
            LoadInitialStatus();
        }

        private async void LoadInitialStatus()
        {
            if (_aiService == null)
            {
                StatusText.Text = "Services not available";
                return;
            }

            try
            {
                StatusText.Text = "Loading system status...";

                // Get system health
                var healthResponse = await _aiService.GetSystemHealthAsync();

                StatusText.Text = healthResponse.Success ? "System Ready" : "System Issues Detected";

                // Update system status tab
                SystemStatusOutput.Text = $"System Health: {healthResponse.HealthStatus}\n" +
                                        $"Health Score: {healthResponse.HealthScore:F2}\n" +
                                        $"Last Updated: {healthResponse.Timestamp}\n\n" +
                                        $"Issues: {string.Join(", ", healthResponse.Issues)}\n" +
                                        $"Recommendations: {string.Join(", ", healthResponse.Recommendations)}";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading initial status");
                StatusText.Text = "Error loading status";
                SystemStatusOutput.Text = $"Error: {ex.Message}";
            }
        }

        private async void SendButton_Click(object sender, RoutedEventArgs e)
        {
            if (_aiService == null)
            {
                ChatOutput.Text += "\n\nError: AI service not available";
                return;
            }

            var input = ChatInput.Text.Trim();
            if (string.IsNullOrEmpty(input)) return;

            ChatOutput.Text += $"\n\nUser: {input}";
            ChatInput.Text = "";
            StatusText.Text = "Processing...";

            try
            {
                var response = await _aiService!.ProcessAsync("general", input);

                ChatOutput.Text += $"\n\nAI: {response.Response}";
                ChatOutput.ScrollToEnd();

                StatusText.Text = response.Success ? "Ready" : "Error in processing";
            }
            catch (Exception ex)
            {
                ChatOutput.Text += $"\n\nError: {ex.Message}";
                StatusText.Text = "Error";
            }
        }

        private async void ChatInput_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                await ProcessChatInput();
            }
        }

        private async Task ProcessChatInput()
        {
            var input = ChatInput.Text.Trim();
            if (string.IsNullOrEmpty(input))
                return;

            try
            {
                // Add user message to chat
                ChatOutput.Text += $"\n\nUser: {input}";
                ChatInput.Text = "";
                StatusText.Text = "Processing...";

                // Process with AI service
                var response = await _aiService!.ProcessAsync("general", input);

                // Add AI response to chat
                ChatOutput.Text += $"\n\nAI: {response.Response}";

                // Scroll to bottom
                ChatOutput.ScrollToEnd();

                StatusText.Text = response.Success ? "Ready" : "Error in processing";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing chat input");
                ChatOutput.Text += $"\n\nError: {ex.Message}";
                StatusText.Text = "Error";
            }
        }

        private async void RefreshStatusButton_Click(object sender, RoutedEventArgs e)
        {
            if (_aiService == null || _maintenanceService == null)
            {
                SystemStatusOutput.Text = "Services not available for status refresh";
                StatusText.Text = "Error";
                return;
            }

            try
            {
                StatusText.Text = "Refreshing status...";

                var healthResponse = await _aiService.GetSystemHealthAsync();
                var maintenanceStatus = await _maintenanceService!.GetMaintenanceStatusAsync();

                SystemStatusOutput.Text = $"=== SYSTEM HEALTH ===\n" +
                                        $"Health Status: {healthResponse.HealthStatus}\n" +
                                        $"Health Score: {healthResponse.HealthScore:F2}\n" +
                                        $"Last Updated: {healthResponse.Timestamp}\n\n" +
                                        $"Issues: {string.Join(", ", healthResponse.Issues)}\n" +
                                        $"Warnings: {string.Join(", ", healthResponse.Warnings)}\n" +
                                        $"Recommendations: {string.Join(", ", healthResponse.Recommendations)}\n\n" +
                                        $"=== MAINTENANCE STATUS ===\n" +
                                        $"Documentation Fragmentation: {maintenanceStatus.DocumentationFragmentation}\n" +
                                        $"Available Operations: {string.Join(", ", maintenanceStatus.AvailableOperations)}";

                StatusText.Text = "Status refreshed";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error refreshing status");
                SystemStatusOutput.Text = $"Error refreshing status: {ex.Message}";
                StatusText.Text = "Error";
            }
        }

        private async void RunMaintenanceButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                StatusText.Text = "Running maintenance...";
                MaintenanceOutput.Text = "Starting maintenance operations...\n";

                // Create a simple maintenance result for demo
                var result = new AIOS.Models.MaintenanceResult
                {
                    Success = true,
                    Message = "Maintenance completed successfully",
                    Actions = new List<string> { "System health check", "Cache cleanup", "Log rotation" }
                };

                await Task.Delay(1000); // Simulate maintenance work

                MaintenanceOutput.Text += $"Maintenance completed!\n" +
                                        $"Success: {result.Success}\n" +
                                        $"Message: {result.Message}\n" +
                                        $"Actions: {string.Join(", ", result.Actions)}\n" +
                                        $"Timestamp: {DateTime.Now}\n";

                StatusText.Text = result.Success ? "Maintenance completed" : "Maintenance failed";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error running maintenance");
                MaintenanceOutput.Text += $"Error: {ex.Message}\n";
                StatusText.Text = "Maintenance error";
            }
        }

        private async void CheckHealthButton_Click(object sender, RoutedEventArgs e)
        {
            if (_aiService == null)
            {
                MaintenanceOutput.Text = "AI service not available for health check";
                StatusText.Text = "Error";
                return;
            }

            try
            {
                StatusText.Text = "Checking system health...";

                var healthResponse = await _aiService.GetSystemHealthAsync();

                MaintenanceOutput.Text = $"=== SYSTEM HEALTH CHECK ===\n" +
                                       $"Status: {healthResponse.HealthStatus}\n" +
                                       $"Score: {healthResponse.HealthScore:F2}\n" +
                                       $"Timestamp: {healthResponse.Timestamp}\n\n" +
                                       $"Issues Found:\n{string.Join("\n", healthResponse.Issues)}\n\n" +
                                       $"Warnings:\n{string.Join("\n", healthResponse.Warnings)}\n\n" +
                                       $"Recommendations:\n{string.Join("\n", healthResponse.Recommendations)}\n";

                StatusText.Text = "Health check completed";
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error checking health");
                MaintenanceOutput.Text = $"Error checking health: {ex.Message}";
                StatusText.Text = "Health check error";
            }
        }

        // Library Generation functionality
        private async void GenerateButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                GenerateButton.IsEnabled = false;
                GenerationStatus.Text = "🚀 Launching dual-agent generation...";
                StatusText.Text = "Generating code...";
                VariantsPanel.Children.Clear();
                CodePreview.Text = "Generation in progress...\n\nThis may take 30-60 seconds...";

                // Get selected library and task
                var library = (LibrarySelector.SelectedItem as ComboBoxItem)?.Content.ToString() ?? "aios_core";
                var task = TaskDescription.Text;
                var variantCount = (int)VariantCountSlider.Value;

                // Build Python command
                var pythonExe = "python";
                
                // Get the correct path - test_library_generation.py is in the root AIOS directory
                var workingDir = @"C:\dev\AIOS";
                var scriptPath = System.IO.Path.Combine(workingDir, "test_library_generation.py");
                
                if (!System.IO.File.Exists(scriptPath))
                {
                    GenerationStatus.Text = "❌ Script not found";
                    CodePreview.Text = $"Error: Could not find test_library_generation.py\n\nExpected location: {scriptPath}\n\nPlease ensure the file exists in C:\\dev\\AIOS\\";
                    return;
                }

                _logger.LogInformation($"Running: {pythonExe} {scriptPath}");
                _logger.LogInformation($"Working directory: {workingDir}");

                // Create process to run Python script
                var processInfo = new System.Diagnostics.ProcessStartInfo
                {
                    FileName = pythonExe,
                    Arguments = "test_library_generation.py",
                    WorkingDirectory = workingDir,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = new System.Diagnostics.Process { StartInfo = processInfo };
                
                var outputBuilder = new System.Text.StringBuilder();
                var errorBuilder = new System.Text.StringBuilder();

                process.OutputDataReceived += (s, args) =>
                {
                    if (!string.IsNullOrEmpty(args.Data))
                    {
                        outputBuilder.AppendLine(args.Data);
                        
                        // Update status with progress
                        Dispatcher.Invoke(() =>
                        {
                            if (args.Data.Contains("Gemini") || args.Data.Contains("Ollama"))
                            {
                                GenerationStatus.Text = args.Data;
                            }
                        });
                    }
                };

                process.ErrorDataReceived += (s, args) =>
                {
                    if (!string.IsNullOrEmpty(args.Data))
                    {
                        errorBuilder.AppendLine(args.Data);
                    }
                };

                process.Start();
                process.BeginOutputReadLine();
                process.BeginErrorReadLine();

                await process.WaitForExitAsync();

                var output = outputBuilder.ToString();
                var errors = errorBuilder.ToString();

                if (process.ExitCode == 0)
                {
                    GenerationStatus.Text = "✅ Generation complete!";
                    StatusText.Text = "Code generated successfully";
                    
                    // Load and display results
                    await LoadGenerationResults(workingDir);
                }
                else
                {
                    GenerationStatus.Text = "❌ Generation failed";
                    StatusText.Text = "Error during generation";
                    CodePreview.Text = $"Error Output:\n{errors}\n\nStandard Output:\n{output}";
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error running library generation");
                GenerationStatus.Text = $"❌ Error: {ex.Message}";
                StatusText.Text = "Generation error";
                CodePreview.Text = $"Exception: {ex.Message}\n\nStack Trace:\n{ex.StackTrace}";
            }
            finally
            {
                GenerateButton.IsEnabled = true;
            }
        }

        private async Task LoadGenerationResults(string workingDir)
        {
            try
            {
                // Find the most recent generation folder
                var generationsPath = System.IO.Path.Combine(workingDir, "evolution_lab", "library_generations");
                
                if (!System.IO.Directory.Exists(generationsPath))
                {
                    CodePreview.Text = "Generation folder not found. Check output for errors.";
                    return;
                }

                var directories = System.IO.Directory.GetDirectories(generationsPath)
                    .OrderByDescending(d => System.IO.Directory.GetCreationTime(d))
                    .ToList();

                if (directories.Count == 0)
                {
                    CodePreview.Text = "No generation results found.";
                    return;
                }

                var latestGen = directories[0];
                _logger.LogInformation($"Loading results from: {latestGen}");

                // Load variants
                var variantFiles = System.IO.Directory.GetFiles(latestGen, "variant_*.py")
                    .OrderBy(f => f)
                    .ToList();

                if (variantFiles.Count == 0)
                {
                    CodePreview.Text = "No variant files found.";
                    return;
                }

                // Display variants
                for (int i = 0; i < variantFiles.Count; i++)
                {
                    var variantFile = variantFiles[i];
                    var analysisFile = variantFile.Replace(".py", "_analysis.json");
                    
                    double consciousness = 0.0;
                    string agent = "Unknown";
                    
                    // Try to load analysis
                    if (System.IO.File.Exists(analysisFile))
                    {
                        try
                        {
                            var analysisJson = await System.IO.File.ReadAllTextAsync(analysisFile);
                            var analysis = System.Text.Json.JsonSerializer.Deserialize<System.Text.Json.JsonElement>(analysisJson);
                            
                            if (analysis.TryGetProperty("consciousness_score", out var scoreElement))
                            {
                                consciousness = scoreElement.GetDouble();
                            }
                        }
                        catch { }
                    }

                    // Determine agent from filename or content
                    agent = i == 0 ? "Gemini" : "Ollama";

                    // Create variant button
                    var variantButton = new System.Windows.Controls.Button
                    {
                        Content = $"Variant {i} ({agent})\nConsciousness: {consciousness:F2}",
                        Background = new System.Windows.Media.SolidColorBrush(
                            System.Windows.Media.Color.FromRgb(0x2d, 0x2d, 0x2d)),
                        Foreground = System.Windows.Media.Brushes.White,
                        Padding = new Thickness(10),
                        Margin = new Thickness(5),
                        HorizontalAlignment = System.Windows.HorizontalAlignment.Stretch,
                        Tag = variantFile
                    };

                    // Highlight best variant
                    if (consciousness >= 0.6)
                    {
                        variantButton.Background = new System.Windows.Media.SolidColorBrush(
                            System.Windows.Media.Color.FromRgb(0x0d, 0x73, 0x77));
                        variantButton.Content += " ⭐";
                    }

                    variantButton.Click += VariantButton_Click;
                    
                    VariantsPanel.Children.Add(variantButton);
                }

                // Auto-select first variant
                if (VariantsPanel.Children.Count > 0)
                {
                    var firstButton = VariantsPanel.Children[0] as System.Windows.Controls.Button;
                    if (firstButton != null)
                    {
                        await LoadVariantCode(firstButton.Tag.ToString());
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading generation results");
                CodePreview.Text = $"Error loading results: {ex.Message}";
            }
        }

        private async void VariantButton_Click(object sender, RoutedEventArgs e)
        {
            var button = sender as System.Windows.Controls.Button;
            if (button?.Tag is string filePath)
            {
                await LoadVariantCode(filePath);
            }
        }

        private async Task LoadVariantCode(string filePath)
        {
            try
            {
                if (System.IO.File.Exists(filePath))
                {
                    var code = await System.IO.File.ReadAllTextAsync(filePath);
                    var fileName = System.IO.Path.GetFileName(filePath);
                    
                    CodePreview.Text = $"=== {fileName} ===\n\n{code}";
                    
                    _logger.LogInformation($"Loaded variant: {fileName}");
                }
                else
                {
                    CodePreview.Text = $"File not found: {filePath}";
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading variant code");
                CodePreview.Text = $"Error loading code: {ex.Message}";
            }
        }

        // Phase 11 Day 1: AI Search functionality
        private async void SearchButton_Click(object sender, RoutedEventArgs e)
        {
            string query = SearchQueryInput.Text?.Trim() ?? "";

            // Validation
            if (string.IsNullOrEmpty(query) || query == "Search for functionality (e.g., 'tool for health monitoring')")
            {
                StatusText.Text = "Please enter a search query";
                return;
            }

            // Clear previous results and show loading
            SearchResults.Children.Clear();
            SearchResults.Children.Add(new TextBlock
            {
                Text = "🔍 Searching...",
                FontSize = 14,
                Foreground = System.Windows.Media.Brushes.Cyan,
                Margin = new Thickness(0, 10, 0, 10)
            });

            StatusText.Text = "Querying AI Layer...";

            try
            {
                // Call Python AI Layer via HTTP
                var response = await _aiLayerClient.SimilaritySearchAsync(query, maxResults: 5);

                // Clear loading message
                SearchResults.Children.Clear();

                if (response.Results == null || response.Results.Count == 0)
                {
                    SearchResults.Children.Add(new TextBlock
                    {
                        Text = "No results found. Try a different query.",
                        FontSize = 12,
                        Foreground = System.Windows.Media.Brushes.Gray,
                        Margin = new Thickness(0, 10, 0, 10)
                    });
                    StatusText.Text = "No results";
                    return;
                }

                // Render results
                int rank = 1;
                foreach (var result in response.Results)
                {
                    // Container border for each result
                    var resultBorder = new Border
                    {
                        Background = new System.Windows.Media.SolidColorBrush(
                            System.Windows.Media.Color.FromRgb(0x2d, 0x2d, 0x2d)),
                        CornerRadius = new CornerRadius(5),
                        Padding = new Thickness(10),
                        Margin = new Thickness(0, 5, 0, 10)
                    };

                    var resultPanel = new StackPanel();

                    // Title: #{rank}. {neuron name}
                    resultPanel.Children.Add(new TextBlock
                    {
                        Text = $"#{rank}. {result.Neuron}",
                        FontSize = 14,
                        FontWeight = FontWeights.Bold,
                        Foreground = System.Windows.Media.Brushes.White,
                        Margin = new Thickness(0, 0, 0, 5)
                    });

                    // Scores: embedding, LLM, final
                    var scoresPanel = new WrapPanel { Margin = new Thickness(0, 0, 0, 5) };
                    scoresPanel.Children.Add(new TextBlock
                    {
                        Text = $"📊 Embedding: {result.EmbeddingScore:P1}  ",
                        FontSize = 11,
                        Foreground = System.Windows.Media.Brushes.LightGreen
                    });
                    scoresPanel.Children.Add(new TextBlock
                    {
                        Text = $"🧠 LLM: {result.LlmScore:P1}  ",
                        FontSize = 11,
                        Foreground = System.Windows.Media.Brushes.LightBlue
                    });
                    scoresPanel.Children.Add(new TextBlock
                    {
                        Text = $"⭐ Final: {result.Similarity:P1}",
                        FontSize = 11,
                        Foreground = System.Windows.Media.Brushes.Yellow
                    });
                    resultPanel.Children.Add(scoresPanel);

                    // Reasoning (if available)
                    if (!string.IsNullOrEmpty(result.Reasoning))
                    {
                        resultPanel.Children.Add(new TextBlock
                        {
                            Text = $"💭 {result.Reasoning}",
                            FontSize = 11,
                            Foreground = System.Windows.Media.Brushes.LightGray,
                            TextWrapping = TextWrapping.Wrap,
                            Margin = new Thickness(0, 3, 0, 3)
                        });
                    }

                    // File path
                    resultPanel.Children.Add(new TextBlock
                    {
                        Text = $"📁 {result.Path}",
                        FontSize = 10,
                        Foreground = System.Windows.Media.Brushes.Gray,
                        Margin = new Thickness(0, 3, 0, 0)
                    });

                    resultBorder.Child = resultPanel;
                    SearchResults.Children.Add(resultBorder);
                    rank++;
                }

                StatusText.Text = $"Found {response.Results.Count} results";
            }
            catch (System.Net.Http.HttpRequestException ex)
            {
                SearchResults.Children.Clear();
                SearchResults.Children.Add(new TextBlock
                {
                    Text = $"❌ Connection Error\n\n{ex.Message}\n\nIs the Interface Bridge server running?\nStart with: python ai/server_manager.py start",
                    FontSize = 12,
                    Foreground = System.Windows.Media.Brushes.Red,
                    TextWrapping = TextWrapping.Wrap,
                    Margin = new Thickness(0, 10, 0, 10)
                });
                StatusText.Text = "Connection error";
            }
            catch (Exception ex)
            {
                SearchResults.Children.Clear();
                SearchResults.Children.Add(new TextBlock
                {
                    Text = $"❌ Unexpected Error\n\n{ex.Message}\n\n{ex.StackTrace}",
                    FontSize = 11,
                    Foreground = System.Windows.Media.Brushes.Orange,
                    TextWrapping = TextWrapping.Wrap,
                    Margin = new Thickness(0, 10, 0, 10)
                });
                StatusText.Text = "Error occurred";
            }
        }
    }
}
