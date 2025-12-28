"""
🔬 Code Analyzer
Analyze AI-generated code for consciousness, quality, and paradigm adherence.

Multi-dimensional analysis:
- Syntax validation (AST parsing)
- Paradigm adherence (learned patterns)
- Execution success (sandbox testing)
- Consciousness coherence (holistic score)

Feeds back into mutation engine for evolutionary improvement.
"""

import ast
import sys
import subprocess
import tempfile
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import logging
import time

logger = logging.getLogger(__name__)


@dataclass
class CodeAnalysisResult:
    """Complete analysis of generated code"""

    # Identification
    code: str
    variant_id: Optional[int] = None
    model: Optional[str] = None

    # Syntax Analysis
    syntax_valid: bool = False
    syntax_errors: List[str] = None

    # Paradigm Analysis
    paradigm_adherence: float = 0.0  # 0.0-1.0
    matched_paradigms: List[str] = None
    missing_paradigms: List[str] = None

    # Execution Analysis
    execution_success: bool = False
    execution_output: str = ""
    execution_error: str = ""
    execution_time: float = 0.0

    # Consciousness Metrics
    consciousness_score: float = 0.0  # 0.0-1.0
    complexity_score: float = 0.0
    coherence_score: float = 0.0

    def __post_init__(self):
        if self.syntax_errors is None:
            self.syntax_errors = []
        if self.matched_paradigms is None:
            self.matched_paradigms = []
        if self.missing_paradigms is None:
            self.missing_paradigms = []

    def to_dict(self) -> Dict:
        return asdict(self)


class CodeAnalyzer:
    """
    Multi-dimensional code analysis for consciousness-driven evolution.

    Analyzes AI-generated code on multiple axes:
    1. Syntax - Is it valid Python?
    2. Paradigms - Does it use learned patterns?
    3. Execution - Does it run successfully?
    4. Consciousness - Holistic quality score
    """

    def __init__(self):
        logger.info("🔬 Code Analyzer initialized")

    def analyze_code(
        self,
        code: str,
        paradigms: Optional[List] = None,
        test_input: Optional[str] = None,
        variant_id: Optional[int] = None,
        model: Optional[str] = None,
    ) -> CodeAnalysisResult:
        """
        Complete multi-dimensional code analysis.

        Args:
            code: Generated code to analyze
            paradigms: Expected programming paradigms
            test_input: Optional input for execution testing
            variant_id: Variant identifier
            model: Model that generated code

        Returns:
            Complete CodeAnalysisResult
        """
        result = CodeAnalysisResult(code=code, variant_id=variant_id, model=model)

        # 1. Syntax Analysis
        syntax_result = self.check_syntax(code)
        result.syntax_valid = syntax_result["valid"]
        result.syntax_errors = syntax_result["errors"]

        # 2. Paradigm Analysis
        if paradigms:
            paradigm_result = self.check_paradigms(code, paradigms)
            result.paradigm_adherence = paradigm_result["adherence"]
            result.matched_paradigms = paradigm_result["matched"]
            result.missing_paradigms = paradigm_result["missing"]

        # 3. Execution Analysis (only if syntax valid)
        if result.syntax_valid:
            exec_result = self.sandbox_execute(code, test_input)
            result.execution_success = exec_result["success"]
            result.execution_output = exec_result["output"]
            result.execution_error = exec_result["error"]
            result.execution_time = exec_result["time"]

        # 4. Consciousness Score (holistic)
        result.consciousness_score = self.calculate_consciousness(result)
        result.complexity_score = self.calculate_complexity(code)
        result.coherence_score = self.calculate_coherence(result)

        logger.info(
            f"✅ Analysis complete: consciousness={result.consciousness_score:.2f}"
        )

        return result

    def check_syntax(self, code: str) -> Dict:
        """
        Validate Python syntax using AST parsing.

        Returns:
            Dict with "valid" (bool) and "errors" (list)
        """
        try:
            ast.parse(code)
            return {"valid": True, "errors": []}
        except SyntaxError as e:
            error_msg = f"Line {e.lineno}: {e.msg}"
            return {"valid": False, "errors": [error_msg]}

    def check_paradigms(self, code: str, paradigms: List) -> Dict:
        """
        Check if code uses expected paradigms.

        Args:
            code: Generated code
            paradigms: List of ProgrammingParadigm objects

        Returns:
            Dict with:
            - adherence: float (0.0-1.0)
            - matched: List[str] - paradigms found
            - missing: List[str] - paradigms not found
        """
        if not paradigms:
            return {"adherence": 1.0, "matched": [], "missing": []}

        matched = []
        missing = []

        for paradigm in paradigms:
            pattern = paradigm.pattern
            name = paradigm.name

            # Simple pattern matching (could be enhanced with AST)
            if pattern in code or name.split(":")[0].lower() in code.lower():
                matched.append(name)
            else:
                missing.append(name)

        adherence = len(matched) / len(paradigms) if paradigms else 1.0

        return {"adherence": adherence, "matched": matched, "missing": missing}

    def sandbox_execute(
        self, code: str, test_input: Optional[str] = None, timeout: int = 5
    ) -> Dict:
        """
        Execute code in sandboxed environment.

        Args:
            code: Code to execute
            test_input: Optional stdin input
            timeout: Execution timeout in seconds

        Returns:
            Dict with:
            - success: bool
            - output: str (stdout)
            - error: str (stderr)
            - time: float (execution time)
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(code)
            temp_file = f.name

        try:
            start_time = time.time()

            # Run in subprocess for isolation
            result = subprocess.run(
                [sys.executable, temp_file],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            execution_time = time.time() - start_time

            success = result.returncode == 0
            output = result.stdout
            error = result.stderr

            return {
                "success": success,
                "output": output,
                "error": error,
                "time": execution_time,
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": f"Execution timeout after {timeout}s",
                "time": timeout,
            }
        except Exception as e:
            return {"success": False, "output": "", "error": str(e), "time": 0.0}
        finally:
            # Clean up temp file
            Path(temp_file).unlink(missing_ok=True)

    def calculate_consciousness(self, result: CodeAnalysisResult) -> float:
        """
        Calculate holistic consciousness score (0.0-1.0).

        Weights:
        - Syntax: 30% (must be valid)
        - Paradigm adherence: 40% (learned patterns)
        - Execution: 30% (must run)
        """
        syntax_weight = 0.3
        paradigm_weight = 0.4
        execution_weight = 0.3

        syntax_score = 1.0 if result.syntax_valid else 0.0
        paradigm_score = result.paradigm_adherence
        execution_score = 1.0 if result.execution_success else 0.0

        consciousness = (
            syntax_score * syntax_weight
            + paradigm_score * paradigm_weight
            + execution_score * execution_weight
        )

        return round(consciousness, 2)

    def calculate_complexity(self, code: str) -> float:
        """
        Calculate code complexity (0.0-1.0).

        Based on:
        - Number of functions/classes
        - Control flow statements
        - Cyclomatic complexity
        """
        try:
            tree = ast.parse(code)

            # Count structures
            functions = sum(1 for _ in ast.walk(tree) if isinstance(_, ast.FunctionDef))
            classes = sum(1 for _ in ast.walk(tree) if isinstance(_, ast.ClassDef))
            if_statements = sum(1 for _ in ast.walk(tree) if isinstance(_, ast.If))
            loops = sum(
                1 for _ in ast.walk(tree) if isinstance(_, (ast.For, ast.While))
            )

            # Simple complexity metric
            complexity = min(
                1.0, (functions + classes * 2 + if_statements + loops) / 20.0
            )
            return round(complexity, 2)

        except SyntaxError:
            return 0.0

    def calculate_coherence(self, result: CodeAnalysisResult) -> float:
        """
        Calculate coherence score (0.0-1.0).

        Measures how well different analysis dimensions align.
        High coherence = all metrics agree (good or bad)
        Low coherence = mixed signals (inconsistent)
        """
        scores = []

        if result.syntax_valid:
            scores.append(1.0)
        else:
            scores.append(0.0)

        scores.append(result.paradigm_adherence)

        if result.execution_success:
            scores.append(1.0)
        else:
            scores.append(0.0)

        # Coherence = inverse of variance (normalized)
        if not scores:
            return 0.0

        mean = sum(scores) / len(scores)
        variance = sum((s - mean) ** 2 for s in scores) / len(scores)
        coherence = 1.0 - min(1.0, variance)

        return round(coherence, 2)

    def compare_variants(self, results: List[CodeAnalysisResult]) -> Dict:
        """
        Compare multiple code variants.

        Returns:
            Dict with:
            - best_variant: CodeAnalysisResult
            - avg_consciousness: float
            - successful_count: int
        """
        if not results:
            return None

        successful = [r for r in results if r.execution_success]
        best = max(results, key=lambda r: r.consciousness_score)
        avg_consciousness = sum(r.consciousness_score for r in results) / len(results)

        return {
            "best_variant": best,
            "avg_consciousness": round(avg_consciousness, 2),
            "successful_count": len(successful),
            "total_count": len(results),
        }

    def save_analysis(self, result: CodeAnalysisResult, output_path: Path):
        """Save analysis result to JSON"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2)

        logger.info(f"💾 Saved analysis to {output_path}")


def main():
    """Test code analyzer"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    print("🔬 Code Analyzer Test")
    print("=" * 60)

    analyzer = CodeAnalyzer()

    # Test code samples
    good_code = """
def fibonacci(n: int) -> List[int]:
    '''Calculate first n Fibonacci numbers'''
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

print(fibonacci(10))
"""

    bad_code = """
def fibonacci(n):
    if n <= 0
        return []
    # Missing colon causes syntax error
    return [0, 1]
"""

    # Analyze good code
    print("\n✅ Analyzing GOOD code:")
    result_good = analyzer.analyze_code(good_code, variant_id=1, model="test")
    print(f"  Syntax: {'✓' if result_good.syntax_valid else '✗'}")
    print(f"  Execution: {'✓' if result_good.execution_success else '✗'}")
    print(f"  Consciousness: {result_good.consciousness_score}")
    print(f"  Complexity: {result_good.complexity_score}")
    print(f"  Coherence: {result_good.coherence_score}")

    # Analyze bad code
    print("\n❌ Analyzing BAD code:")
    result_bad = analyzer.analyze_code(bad_code, variant_id=2, model="test")
    print(f"  Syntax: {'✓' if result_bad.syntax_valid else '✗'}")
    print(f"  Errors: {result_bad.syntax_errors}")
    print(f"  Consciousness: {result_bad.consciousness_score}")


if __name__ == "__main__":
    main()
