using System;
using System.Threading.Tasks;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using AIOS.VisualInterface;

namespace AIOS.Tools
{
    /// <summary>
    /// AIOS State Reporter - Command-line tool to generate AI-readable state descriptions
    /// Usage: AIOSStateReporter.exe [--format json|text] [--output file]
    /// </summary>
    class AIOSStateReporter
    {
        static async Task Main(string[] args)
        {
            var services = new ServiceCollection();
            services.AddLogging(builder => builder.AddConsole());
            services.AddTransient<AIStateDescriptionService>();
            
            var serviceProvider = services.BuildServiceProvider();
            var stateService = serviceProvider.GetRequiredService<AIStateDescriptionService>();
            
            Console.WriteLine("AIOS State Reporter - Generating AI-readable state description...");
            Console.WriteLine();
            
            var stateDescription = await stateService.DescribeCurrentStateAsync();
            
            // Parse command line arguments
            var format = GetArgument(args, "--format", "text");
            var outputFile = GetArgument(args, "--output", null);
            
            if (format.ToLower() == "json")
            {
                var jsonOutput = ConvertToJson(stateDescription);
                OutputResult(jsonOutput, outputFile);
            }
            else
            {
                OutputResult(stateDescription, outputFile);
            }
        }

        static string GetArgument(string[] args, string argName, string defaultValue)
        {
            for (int i = 0; i < args.Length - 1; i++)
            {
                if (args[i].Equals(argName, StringComparison.OrdinalIgnoreCase))
                {
                    return args[i + 1];
                }
            }
            return defaultValue ?? "";
        }

        static string ConvertToJson(string textDescription)
        {
            // Simple JSON wrapper for the text description
            return $"{{\"timestamp\":\"{DateTime.Now:yyyy-MM-dd HH:mm:ss}\",\"description\":\"{textDescription.Replace("\"", "\\\"").Replace("\n", "\\n")}\"}}";
        }

        static void OutputResult(string content, string? outputFile)
        {
            if (!string.IsNullOrEmpty(outputFile))
            {
                System.IO.File.WriteAllText(outputFile, content);
                Console.WriteLine($"State description written to: {outputFile}");
            }
            else
            {
                Console.WriteLine(content);
            }
        }
    }
}