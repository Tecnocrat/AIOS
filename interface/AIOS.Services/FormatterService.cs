using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using AIOS.Models;

namespace AIOS.Services
{
    /// <summary>
    /// AINLP Code Formatter Service
    /// Integrates with AIOS architecture for code quality improvements
    /// AINLP.service [code_formatting_implementation] (comment.AINLP.class)
    /// </summary>
    public class FormatterService : IFormatterService
    {
        private readonly ILogger<FormatterService> _logger;
        private const int MAX_LINE_LENGTH = 79;

        public FormatterService(ILogger<FormatterService> logger)
        {
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }

        public void RegisterFormatterTool()
        {
            _logger.LogInformation("AINLP Code Formatter Tool registered with AIOS");
        }

        public async Task<E501FixResult> FixFileAsync(string filePath)
        {
            var stopwatch = System.Diagnostics.Stopwatch.StartNew();

            try
            {
                _logger.LogInformation($"Starting E501 fix for: {filePath}");

                if (!File.Exists(filePath))
                {
                    return new E501FixResult
                    {
                        Success = false,
                        ErrorMessage = $"File not found: {filePath}"
                    };
                }

                var lines = await File.ReadAllLinesAsync(filePath, Encoding.UTF8);
                var fixedLines = new List<string>();
                int violationsFixed = 0;
                int totalViolations = 0;

                for (int i = 0; i < lines.Length; i++)
                {
                    var line = lines[i];

                    if (line.Length > MAX_LINE_LENGTH)
                    {
                        totalViolations++;
                        var fixedLinesList = FixLongLine(line, i + 1);

                        if (fixedLinesList.Count > 1 || fixedLinesList[0].Length <= MAX_LINE_LENGTH)
                        {
                            violationsFixed++;
                            fixedLines.AddRange(fixedLinesList);
                        }
                        else
                        {
                            fixedLines.Add(line); // Keep original if fix failed
                        }
                    }
                    else
                    {
                        fixedLines.Add(line);
                    }
                }

                // Write back the fixed content
                await File.WriteAllLinesAsync(filePath, fixedLines, Encoding.UTF8);

                stopwatch.Stop();

                return new E501FixResult
                {
                    Success = true,
                    LinesFixed = violationsFixed,
                    TotalViolations = totalViolations,
                    Summary = $"Fixed {violationsFixed}/{totalViolations} E501 violations",
                    ProcessingTimeMs = stopwatch.ElapsedMilliseconds
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error fixing E501 violations in {filePath}");
                return new E501FixResult
                {
                    Success = false,
                    ErrorMessage = ex.Message,
                    ProcessingTimeMs = stopwatch.ElapsedMilliseconds
                };
            }
        }

        public async Task<E501CheckResult> CheckFileAsync(string filePath)
        {
            try
            {
                if (!File.Exists(filePath))
                {
                    return new E501CheckResult
                    {
                        HasViolations = false,
                        Summary = $"File not found: {filePath}"
                    };
                }

                var lines = await File.ReadAllLinesAsync(filePath, Encoding.UTF8);
                var violations = new List<E501Violation>();

                for (int i = 0; i < lines.Length; i++)
                {
                    var line = lines[i];

                    if (line.Length > MAX_LINE_LENGTH)
                    {
                        violations.Add(new E501Violation
                        {
                            LineNumber = i + 1,
                            LineLength = line.Length,
                            LineContent = line.Length > 100 ? line.Substring(0, 100) + "..." : line,
                            FixSuggestion = GetFixSuggestion(line)
                        });
                    }
                }

                return new E501CheckResult
                {
                    HasViolations = violations.Any(),
                    ViolationCount = violations.Count,
                    Violations = violations,
                    Summary = violations.Any()
                        ? $"Found {violations.Count} E501 violations"
                        : "No E501 violations found"
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error checking E501 violations in {filePath}");
                return new E501CheckResult
                {
                    HasViolations = false,
                    Summary = $"Error: {ex.Message}"
                };
            }
        }

        private List<string> FixLongLine(string line, int lineNumber)
        {
            var indent = GetIndentation(line);
            var trimmedLine = line.TrimStart();

            // Fix print statements
            if (trimmedLine.StartsWith("print("))
            {
                return FixPrintStatement(line, indent);
            }

            // Fix import statements
            if (trimmedLine.StartsWith("from ") && trimmedLine.Contains(" import "))
            {
                return FixImportStatement(line, indent);
            }

            // Fix function calls with parameters
            if (trimmedLine.Contains("(") && trimmedLine.Contains(")") && trimmedLine.Contains(","))
            {
                return FixFunctionCall(line, indent);
            }

            // Fix dictionary/list assignments
            if (trimmedLine.Contains("=") && (trimmedLine.Contains("{") || trimmedLine.Contains("[")))
            {
                return FixAssignment(line, indent);
            }

            // Default: try to break at comma or operator
            return BreakAtComma(line, indent);
        }

        private List<string> FixPrintStatement(string line, string indent)
        {
            var match = Regex.Match(line.Trim(), @"print\((.+)\)");
            if (!match.Success)
                return new List<string> { line };

            var content = match.Groups[1].Value;

            // Handle quoted strings
            if (content.StartsWith("\"") && content.EndsWith("\""))
            {
                var innerContent = content.Substring(1, content.Length - 2);

                // Look for natural break points like " | " or similar
                if (innerContent.Contains(" | "))
                {
                    var parts = innerContent.Split(new[] { " | " }, StringSplitOptions.None);
                    var result = new List<string> { indent + "print(" };

                    for (int i = 0; i < parts.Length; i++)
                    {
                        var part = parts[i].Trim();
                        if (i == 0)
                            result.Add(indent + "    \"" + part + " |\"");
                        else if (i == parts.Length - 1)
                            result.Add(indent + "    \" " + part + "\"");
                        else
                            result.Add(indent + "    \" " + part + " |\"");
                    }

                    result.Add(indent + ")");
                    return result;
                }
            }

            // Fallback for other print statements
            return new List<string> { line };
        }

        private List<string> FixImportStatement(string line, string indent)
        {
            var parts = line.Split(new[] { " import " }, StringSplitOptions.None);
            if (parts.Length == 2)
            {
                return new List<string>
                {
                    parts[0] + " import (",
                    indent + "    " + parts[1].Trim(),
                    indent + ")"
                };
            }
            return new List<string> { line };
        }

        private List<string> FixFunctionCall(string line, string indent)
        {
            var openParen = line.IndexOf('(');
            var closeParen = line.LastIndexOf(')');

            if (openParen > 0 && closeParen > openParen)
            {
                var funcName = line.Substring(0, openParen + 1);
                var parameters = line.Substring(openParen + 1, closeParen - openParen - 1);
                var endPart = line.Substring(closeParen);

                if (parameters.Contains(","))
                {
                    var paramList = parameters.Split(',')
                        .Select(p => p.Trim())
                        .ToList();

                    var result = new List<string> { indent + funcName };

                    for (int i = 0; i < paramList.Count; i++)
                    {
                        var comma = i < paramList.Count - 1 ? "," : "";
                        result.Add(indent + "    " + paramList[i] + comma);
                    }

                    result.Add(indent + endPart);
                    return result;
                }
            }

            return new List<string> { line };
        }

        private List<string> FixAssignment(string line, string indent)
        {
            var equalIndex = line.IndexOf('=');
            if (equalIndex > 0)
            {
                var varPart = line.Substring(0, equalIndex).TrimEnd();
                var valuePart = line.Substring(equalIndex + 1).TrimStart();

                return new List<string>
                {
                    indent + varPart + " = (",
                    indent + "    " + valuePart,
                    indent + ")"
                };
            }

            return new List<string> { line };
        }

        private List<string> BreakAtComma(string line, string indent)
        {
            var commaIndex = line.LastIndexOf(',', Math.Min(line.Length - 1, MAX_LINE_LENGTH));

            if (commaIndex > 0)
            {
                var firstPart = line.Substring(0, commaIndex + 1);
                var secondPart = line.Substring(commaIndex + 1).TrimStart();

                return new List<string>
                {
                    firstPart,
                    indent + secondPart
                };
            }

            return new List<string> { line };
        }

        private string GetIndentation(string line)
        {
            var indent = "";
            foreach (char c in line)
            {
                if (c == ' ' || c == '\t')
                    indent += c;
                else
                    break;
            }
            return indent;
        }

        private string GetFixSuggestion(string line)
        {
            var trimmed = line.TrimStart();

            if (trimmed.StartsWith("print("))
                return "Break into multi-line print statement";
            else if (trimmed.StartsWith("from ") && trimmed.Contains(" import "))
                return "Use parentheses for import wrapping";
            else if (trimmed.Contains("(") && trimmed.Contains(","))
                return "Break function parameters across lines";
            else if (trimmed.Contains("="))
                return "Break assignment across lines";
            else
                return "Break at comma or natural boundary";
        }
    }
}
