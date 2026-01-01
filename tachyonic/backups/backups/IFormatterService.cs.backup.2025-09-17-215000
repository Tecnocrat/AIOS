using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace AIOS.Models
{
    /// <summary>
    /// Interface for code formatting service
    /// AINLP.interface [code_formatting] (comment.AINLP.class)
    /// </summary>
    public interface IFormatterService
    {
        /// <summary>
        /// Register the formatter tool with AIOS
        /// </summary>
        void RegisterFormatterTool();

        /// <summary>
        /// Fix E501 line length violations in a Python file
        /// </summary>
        /// <param name="filePath">Path to the Python file</param>
        /// <returns>E501 fix result</returns>
        Task<E501FixResult> FixFileAsync(string filePath);

        /// <summary>
        /// Check for E501 violations without fixing
        /// </summary>
        /// <param name="filePath">Path to the Python file</param>
        /// <returns>List of E501 violations</returns>
        Task<E501CheckResult> CheckFileAsync(string filePath);
    }

    /// <summary>
    /// Result of E501 fix operation
    /// AINLP.model [e501_fix_result] (comment.AINLP.class)
    /// </summary>
    public class E501FixResult
    {
        public bool Success { get; set; }
        public string ErrorMessage { get; set; } = "";
        public int LinesFixed { get; set; }
        public int TotalViolations { get; set; }
        public string Summary { get; set; } = "";
        public double ProcessingTimeMs { get; set; }
    }

    /// <summary>
    /// Result of E501 check operation
    /// AINLP.model [e501_check_result] (comment.AINLP.class)
    /// </summary>
    public class E501CheckResult
    {
        public bool HasViolations { get; set; }
        public int ViolationCount { get; set; }
        public List<E501Violation> Violations { get; set; } = new List<E501Violation>();
        public string Summary { get; set; } = "";
    }

    /// <summary>
    /// Individual E501 violation details
    /// AINLP.model [e501_violation] (comment.AINLP.class)
    /// </summary>
    public class E501Violation
    {
        public int LineNumber { get; set; }
        public int LineLength { get; set; }
        public string LineContent { get; set; } = "";
        public string FixSuggestion { get; set; } = "";
    }
}
