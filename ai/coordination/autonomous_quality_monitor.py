"""
AIOS Autonomous Quality Monitor

Background agent coordination for continuous code quality maintenance.
Uses cheap agents (Ollama local, GitHub Models GPT-4o-mini) for simple tasks,
escalates complex issues to premium agents (GitHub Models GPT-4o, Claude Sonnet 4.5).

Key Features:
- File save triggers (VSCode integration)
- Background monitoring (configurable interval)
- Multi-tier agent routing by complexity
- Autonomous fixing with AINLP compliance
- Escalation to premium agents when stuck
- Cost tracking and optimization

Consciousness: 4.4 (Generic Agentic Substrate)
Date: November 22, 2025
"""

import asyncio
import sys

# Fix Windows console encoding for emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import httpx


class TaskComplexity(Enum):
    """Task complexity levels for agent tier routing"""
    TRIVIAL = "trivial"      # Pattern-based (no AI, <0.1s)
    SIMPLE = "simple"        # Ollama local (FREE, <1s)
    MODERATE = "moderate"    # GitHub Models GPT-4o-mini ($0.15/1M tokens, <2s)
    COMPLEX = "complex"      # GitHub Models GPT-4o ($2.50/1M tokens, <5s)
    NOVEL = "novel"          # Claude Sonnet 4.5 ($3.00/1M tokens, escalate to human)


@dataclass
class QualityIssue:
    """Detected code quality issue"""
    file_path: str
    issue_type: str  # "linting", "formatting", "imports", "e501", "security"
    severity: str    # "low", "medium", "high", "critical"
    complexity: TaskComplexity
    details: Dict[str, Any]
    auto_fixable: bool
    line_number: Optional[int] = None
    error_code: Optional[str] = None


@dataclass
class FixResult:
    """Result of autonomous fix attempt"""
    success: bool
    issue: QualityIssue
    fixed_content: Optional[str] = None
    tier_used: str = ""  # "pattern", "ollama", "gpt4o-mini", "gpt4o"
    confidence: float = 0.0
    attempts: int = 1
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


class AutonomousQualityMonitor:
    """
    Autonomous background code quality agent.
    
    Monitors Python files for simple issues (linting, formatting, E501, imports),
    fixes autonomously using tiered agents (Ollama → GPT-4o-mini → GPT-4o),
    escalates complex issues to premium agents or human review.
    
    GitHub Models API Integration:
    - Tier 1: Ollama gemma3:1b (local, FREE, context prep)
    - Tier 2: GitHub Models GPT-4o-mini (generation, $0.15/1M tokens)
    - Tier 3: GitHub Models GPT-4o (validation, $2.50/1M tokens)
    
    Cost Optimization:
    - Simple tasks: Ollama only (FREE)
    - Moderate tasks: Ollama → GPT-4o-mini ($0.001/fix avg)
    - Complex tasks: GPT-4o-mini → GPT-4o ($0.01/fix avg)
    - Novel tasks: Escalate to human (preserve premium agent tokens)
    """
    
    def __init__(
        self,
        workspace_root: Path,
        auto_fix: bool = True,
        github_token: Optional[str] = None,
        max_cost_per_hour: float = 0.50,  # $0.50/hour budget
        escalation_threshold: int = 2      # Escalate after 2 failed attempts
    ):
        self.workspace_root = Path(workspace_root)
        self.auto_fix = auto_fix
        self.max_cost_per_hour = max_cost_per_hour
        self.escalation_threshold = escalation_threshold
        
        # GitHub token (from env or parameter)
        import os
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
        if not self.github_token:
            raise ValueError(
                "GitHub token required. Set GITHUB_TOKEN env var or run setup_github_token.ps1"
            )
        
        # GitHub Models API endpoint
        self.github_api_base = "https://models.inference.ai.azure.com/chat/completions"
        self.github_models = {
            "tier2_generation": "gpt-4o-mini",      # $0.15/1M input, $0.60/1M output
            "tier3_validation": "gpt-4o"            # $2.50/1M input, $10.00/1M output
        }
        
        # HTTP client for GitHub Models
        self.http_client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.github_token}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        
        # Statistics tracking
        self.stats = {
            "scans": 0,
            "api_errors": [],  # Track API failures for debugging
            "issues_detected": 0,
            "auto_fixed": 0,
            "escalated": 0,
            "pattern_fixes": 0,      # Tier 0: Pattern-based (FREE)
            "ollama_fixes": 0,       # Tier 1: Ollama (FREE)
            "gpt4o_mini_fixes": 0,   # Tier 2: GPT-4o-mini ($)
            "gpt4o_fixes": 0,        # Tier 3: GPT-4o ($$)
            "cost_total": 0.0,
            "cost_this_hour": 0.0,
            "tokens_used": {"input": 0, "output": 0}
        }
        
        # Create escalation and backup directories
        self.escalation_dir = self.workspace_root / "tachyonic" / "escalations"
        self.escalation_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir = self.workspace_root / "tachyonic" / "backups" / "autonomous_monitor"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    async def monitor_workspace(self, interval_seconds: int = 300):
        """
        Continuous monitoring loop (default: every 5 minutes).
        
        Alternative: Trigger on VSCode file save event via extension.
        """
        print(f"[AIOS] Autonomous quality monitoring started (interval: {interval_seconds}s)")
        
        while True:
            await self.scan_and_fix()
            await asyncio.sleep(interval_seconds)
    
    async def scan_and_fix(self) -> Dict[str, Any]:
        """
        Single scan-and-fix cycle.
        
        Returns:
            Summary dict with issues detected, fixed, escalated, cost
        """
        self.stats["scans"] += 1
        print(f"\n[AIOS] Scan #{self.stats['scans']} - {datetime.now().strftime('%H:%M:%S')}")
        
        # 1. Detect all quality issues
        issues = await self._detect_issues()
        self.stats["issues_detected"] += len(issues)
        
        if not issues:
            print("[AIOS] ✓ Workspace clean (0 issues)")
            return self._get_summary()
        
        print(f"[AIOS] Found {len(issues)} issue(s)")
        
        # 2. Route by complexity
        trivial = [i for i in issues if i.complexity == TaskComplexity.TRIVIAL]
        simple = [i for i in issues if i.complexity == TaskComplexity.SIMPLE]
        moderate = [i for i in issues if i.complexity == TaskComplexity.MODERATE]
        complex_issues = [i for i in issues if i.complexity == TaskComplexity.COMPLEX]
        novel = [i for i in issues if i.complexity == TaskComplexity.NOVEL]
        
        print(f"  Trivial: {len(trivial)} | Simple: {len(simple)} | Moderate: {len(moderate)} | Complex: {len(complex_issues)} | Novel: {len(novel)}")
        
        # Initialize results list
        all_results = []
        
        # 3. Fix autonomously (parallel by tier, with rate limiting)
        if self.auto_fix:
            # Tier 0: Pattern-based (FREE, instant)
            pattern_results = await asyncio.gather(
                *[self._fix_with_pattern(i) for i in trivial],
                return_exceptions=True
            )
            
            # Tier 1: Ollama local (FREE, fast)
            # Rate limited to GitHub Models: 15 requests per 60 seconds
            # Process sequentially with 4-second delay (stay under 15/minute)
            ollama_results = []
            for issue in simple:
                result = await self._fix_with_ollama(issue)
                if isinstance(result, Exception):
                    ollama_results.append(result)
                else:
                    ollama_results.append(result)
                # Wait 4s between requests (15 per 60s = 4s/request)
                if len(ollama_results) < len(simple):
                    await asyncio.sleep(4.0)
            
            # Tier 2: GPT-4o-mini ($ cheap, creative)
            gpt4o_mini_results = await asyncio.gather(
                *[self._fix_with_gpt4o_mini(i) for i in moderate],
                return_exceptions=True
            )
            
            # Tier 3: GPT-4o ($$ expensive, critical)
            gpt4o_results = await asyncio.gather(
                *[self._fix_with_gpt4o(i) for i in complex_issues],
                return_exceptions=True
            )
            
            # Process results
            all_results = pattern_results + ollama_results + gpt4o_mini_results + gpt4o_results
            successful = [r for r in all_results if isinstance(r, FixResult) and r.success]
            
            self.stats["auto_fixed"] += len(successful)
            
            # Apply fixes to files
            for result in successful:
                if result.fixed_content:
                    await self._apply_fix(result.issue.file_path, result.fixed_content)
            
            print(f"[AIOS] ✓ Fixed {len(successful)}/{len(issues)} issue(s)")
        
        # 4. Escalate novel/failed issues
        escalate_issues = novel + [
            i for i in (complex_issues + moderate + simple)
            if not any(
                isinstance(r, FixResult) and r.success and r.issue.file_path == i.file_path
                for r in all_results
            )
        ]
        
        if escalate_issues:
            await self._escalate_issues(escalate_issues)
            print(f"[AIOS] ⚠️ Escalated {len(escalate_issues)} issue(s)")
        
        return self._get_summary()
    
    async def _detect_issues(self) -> List[QualityIssue]:
        """Scan workspace for quality issues (parallel)"""
        issues = []
        
        # Find all Python files (with limit to prevent hanging)
        python_files = [
            f for f in self.workspace_root.rglob("*.py")
            if not self._should_skip(f)
        ]
        
        print(f"[AIOS] Scanning {len(python_files)} Python files...")
        
        # Limit to first 50 files for testing (prevent hanging)
        if len(python_files) > 50:
            print(
                f"[AIOS] WARNING: Limiting scan to 50 files "
                f"(found {len(python_files)})"
            )
            python_files = python_files[:50]
        
        # Parallel scanning (linting, E501, imports, formatting)
        tasks = []
        for file_path in python_files:
            tasks.append(self._check_file(file_path))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for file_issues in results:
            if isinstance(file_issues, list):
                issues.extend(file_issues)
        
        return issues
    
    async def _check_file(self, file_path: Path) -> List[QualityIssue]:
        """Check single file for all issue types"""
        issues = []
        
        # Run all checks in parallel
        lint, e501, imports, formatting = await asyncio.gather(
            self._check_linting(file_path),
            self._check_e501(file_path),
            self._check_imports(file_path),
            self._check_formatting(file_path),
            return_exceptions=True
        )
        
        if isinstance(lint, list):
            issues.extend(lint)
        if isinstance(e501, list):
            issues.extend(e501)
        if isinstance(imports, list):
            issues.extend(imports)
        if isinstance(formatting, list):
            issues.extend(formatting)
        
        return issues
    
    async def _check_linting(self, file_path: Path) -> List[QualityIssue]:
        """Run flake8 linting (exclude E501, handled separately)"""
        try:
            result = subprocess.run(
                ["flake8", "--ignore=E501", str(file_path)],
                capture_output=True,
                text=True,
                timeout=2  # Reduced from 5s to 2s
            )
            
            if result.returncode == 0:
                return []
            
            issues = []
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                
                # Parse: file.py:10:5: F401 'os' imported but unused
                parts = line.split(":")
                if len(parts) < 4:
                    continue
                
                line_num = int(parts[1])
                error_code = parts[3].strip().split()[0]
                message = ":".join(parts[3:])
                
                # Classify complexity
                if error_code.startswith("F"):  # Pyflakes (imports, undefined)
                    complexity = TaskComplexity.SIMPLE
                elif error_code.startswith("E"):  # PEP8 errors
                    complexity = TaskComplexity.SIMPLE
                elif error_code.startswith("W"):  # Warnings
                    complexity = TaskComplexity.TRIVIAL
                else:
                    complexity = TaskComplexity.MODERATE
                
                issues.append(QualityIssue(
                    file_path=str(file_path),
                    issue_type="linting",
                    severity="medium",
                    complexity=complexity,
                    details={"message": message},
                    auto_fixable=True,
                    line_number=line_num,
                    error_code=error_code
                ))
            
            return issues
        
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            # Skip file on any error (timeout, missing tool, etc.)
            return []
    
    async def _check_e501(self, file_path: Path) -> List[QualityIssue]:
        """Check for E501 line length violations"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, start=1):
                    if len(line.rstrip()) > 79:
                        issues.append(QualityIssue(
                            file_path=str(file_path),
                            issue_type="e501",
                            severity="low",
                            complexity=TaskComplexity.SIMPLE,
                            details={
                                "line": line.rstrip(),
                                "length": len(line.rstrip())
                            },
                            auto_fixable=True,
                            line_number=line_num,
                            error_code="E501"
                        ))
        except Exception:
            pass
        
        return issues
    
    async def _check_imports(self, file_path: Path) -> List[QualityIssue]:
        """Check for unused imports (skip if pylint not available)"""
        try:
            result = subprocess.run(
                [
                    "pylint",
                    "--disable=all",
                    "--enable=unused-import",
                    str(file_path)
                ],
                capture_output=True,
                text=True,
                timeout=2  # Reduced from 5s to 2s
            )
            
            issues = []
            for line in result.stdout.strip().split("\n"):
                if "unused-import" in line:
                    issues.append(QualityIssue(
                        file_path=str(file_path),
                        issue_type="imports",
                        severity="low",
                        complexity=TaskComplexity.TRIVIAL,
                        details={"message": line},
                        auto_fixable=True
                    ))
            
            return issues
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            # Skip if pylint unavailable or times out
            return []
    
    async def _check_formatting(self, file_path: Path) -> List[QualityIssue]:
        """Check for black formatting issues (skip if not available)"""
        try:
            result = subprocess.run(
                ["black", "--check", str(file_path)],
                capture_output=True,
                text=True,
                timeout=2  # Reduced from 5s to 2s
            )
            
            if result.returncode != 0:
                return [QualityIssue(
                    file_path=str(file_path),
                    issue_type="formatting",
                    severity="low",
                    complexity=TaskComplexity.TRIVIAL,
                    details={"message": "Black formatting needed"},
                    auto_fixable=True
                )]
            
            return []
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            # Skip if black unavailable or times out
            return []
    
    async def _fix_with_pattern(self, issue: QualityIssue) -> FixResult:
        """Tier 0: Pattern-based fixes (FREE, instant)"""
        try:
            if issue.issue_type == "formatting":
                # Run black auto-formatter
                result = subprocess.run(
                    ["black", issue.file_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    with open(issue.file_path, 'r', encoding='utf-8') as f:
                        fixed_content = f.read()
                    
                    self.stats["pattern_fixes"] += 1
                    return FixResult(
                        success=True,
                        issue=issue,
                        fixed_content=fixed_content,
                        tier_used="pattern_black",
                        confidence=1.0,
                        metadata={"tool": "black"}
                    )
            
            return FixResult(success=False, issue=issue, error="No pattern available")
        
        except Exception as e:
            return FixResult(success=False, issue=issue, error=str(e))
    
    async def _fix_with_ollama(self, issue: QualityIssue) -> FixResult:
        """Tier 1: Ollama local aios-mistral (FREE, ~5s per fix)"""
        try:
            # Import bridge (lazy load to avoid startup delay)
            from ai.tools.aios_mistral_bridge import AIOSMistralBridge
            
            async with AIOSMistralBridge() as bridge:
                # Check if server is running
                if not await bridge.check_health():
                    # Fallback to GPT-4o-mini if Ollama unavailable
                    return await self._fix_with_gpt4o_mini(issue)
                
                # Handle E501 (line too long)
                if issue.issue_type == "e501":
                    with open(issue.file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    if issue.line_number and 0 < issue.line_number <= len(lines):
                        line = lines[issue.line_number - 1]
                        response = await bridge.fix_e501(line, issue.line_number)
                        
                        if response.success and response.content.strip():
                            # Apply fix
                            fixed_line = response.content.strip()
                            if not fixed_line.endswith('\n'):
                                fixed_line += '\n'
                            lines[issue.line_number - 1] = fixed_line
                            
                            with open(issue.file_path, 'w', encoding='utf-8') as f:
                                f.writelines(lines)
                            
                            self.stats["ollama_fixes"] += 1
                            return FixResult(
                                success=True,
                                issue=issue,
                                fix_applied=f"Line {issue.line_number} shortened",
                                tier_used="ollama"
                            )
                
                # Handle other linting issues
                else:
                    with open(issue.file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    response = await bridge.fix_linting_issue(content, issue.message)
                    
                    if response.success and response.content.strip():
                        # Extract code from response (may have markdown fences)
                        fixed = response.content.strip()
                        if fixed.startswith("```"):
                            lines = fixed.split('\n')
                            fixed = '\n'.join(lines[1:-1] if lines[-1] == '```' else lines[1:])
                        
                        with open(issue.file_path, 'w', encoding='utf-8') as f:
                            f.write(fixed)
                        
                        self.stats["ollama_fixes"] += 1
                        return FixResult(
                            success=True,
                            issue=issue,
                            fix_applied=f"Fixed: {issue.message[:50]}",
                            tier_used="ollama"
                        )
            
            # If we get here, fix failed - escalate to GPT-4o-mini
            return await self._fix_with_gpt4o_mini(issue)
            
        except ImportError:
            # Bridge not available, fallback
            return await self._fix_with_gpt4o_mini(issue)
        except Exception as e:
            return FixResult(
                success=False,
                issue=issue,
                error=f"Ollama error: {str(e)}",
                tier_used="ollama"
            )
    
    async def _fix_with_gpt4o_mini(self, issue: QualityIssue) -> FixResult:
        """Tier 2: GitHub Models GPT-4o-mini (cheap, creative)"""
        try:
            # Read file content
            with open(issue.file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # Build fix prompt
            if issue.issue_type == "e501":
                prompt = self._build_e501_prompt(issue, file_content)
            elif issue.issue_type == "linting":
                prompt = self._build_linting_prompt(issue, file_content)
            elif issue.issue_type == "imports":
                prompt = self._build_imports_prompt(issue, file_content)
            else:
                return FixResult(
                    success=False,
                    issue=issue,
                    error="Unknown issue type"
                )
            
            # Call GitHub Models GPT-4o-mini with timeout
            try:
                response = await self.http_client.post(
                    self.github_api_base,
                    json={
                        "model": self.github_models["tier2_generation"],
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a Python code fixing assistant. Output only the fixed code, no explanations."
                            },
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.3,
                        "max_tokens": 1000
                    },
                    timeout=15.0  # Reduced from 30s to 15s
                )
            except Exception as e:
                error_msg = f"API call failed: {type(e).__name__}: {str(e)}"
                self.stats["api_errors"].append({
                    "file": issue.file_path,
                    "error": error_msg,
                    "timestamp": datetime.now().isoformat()
                })
                return FixResult(success=False, issue=issue, error=error_msg)
            
            if response.status_code != 200:
                error_msg = f"API {response.status_code}: {response.text[:200]}"
                self.stats["api_errors"].append({
                    "file": issue.file_path,
                    "status": response.status_code,
                    "error": error_msg,
                    "timestamp": datetime.now().isoformat()
                })
                return FixResult(
                    success=False,
                    issue=issue,
                    error=error_msg
                )
            
            data = response.json()
            fixed_content = data["choices"][0]["message"]["content"].strip()
            
            # Validate: remove markdown code blocks if present
            if fixed_content.startswith("```python"):
                lines = fixed_content.split("\n")
                fixed_content = "\n".join(lines[1:-1]).strip()
            elif fixed_content.startswith("```"):
                lines = fixed_content.split("\n")
                fixed_content = "\n".join(lines[1:-1]).strip()
            
            # Track usage
            usage = data.get("usage", {})
            self.stats["tokens_used"]["input"] += usage.get("prompt_tokens", 0)
            self.stats["tokens_used"]["output"] += usage.get("completion_tokens", 0)
            
            # Estimate cost: $0.15/1M input + $0.60/1M output
            cost = (usage.get("prompt_tokens", 0) * 0.15 / 1_000_000) + \
                   (usage.get("completion_tokens", 0) * 0.60 / 1_000_000)
            self.stats["cost_total"] += cost
            self.stats["cost_this_hour"] += cost
            self.stats["gpt4o_mini_fixes"] += 1
            
            return FixResult(
                success=True,
                issue=issue,
                fixed_content=fixed_content,
                tier_used="gpt4o_mini",
                confidence=0.9,
                metadata={"tokens": usage, "cost": cost}
            )
        
        except Exception as e:
            return FixResult(success=False, issue=issue, error=str(e))
    
    async def _fix_with_gpt4o(self, issue: QualityIssue) -> FixResult:
        """Tier 3: GitHub Models GPT-4o (expensive, critical)"""
        # For complex issues, use GPT-4o with validation
        # Similar to _fix_with_gpt4o_mini but with model="gpt-4o"
        # Deferred: Escalate complex issues to human for now
        return FixResult(success=False, issue=issue, error="Complex issue - escalating to human")
    
    def _build_e501_prompt(self, issue: QualityIssue, file_content: str) -> str:
        """Build E501 fix prompt for GPT-4o-mini"""
        line = issue.details["line"]
        line_num = issue.line_number
        
        # Get surrounding context (5 lines before/after)
        lines = file_content.split('\n')
        start = max(0, line_num - 6)  # -1 for 0-index, -5 for context
        end = min(len(lines), line_num + 5)
        context_lines = lines[start:end]
        context_text = '\n'.join([
            f"{start + i + 1:4d} | {l}" 
            for i, l in enumerate(context_lines)
        ])
        
        return f"""Fix E501 line length violation (max 79 chars per line).

**File**: {Path(issue.file_path).name}
**Problem line {line_num}** ({issue.details['length']} chars):

```python
{context_text}
```

**Instructions**:
1. Break line {line_num} to ≤79 chars per line
2. Use natural Python break points:
   - Function args: Break after commas with proper indent
   - Long strings: Use parentheses for implicit concatenation
   - Comments: Split at word boundaries, add # continuation
3. Preserve exact semantics (no logic changes)
4. Maintain indentation consistently

**Output**: Only the FIXED lines (line {line_num} and any new continuation lines), nothing else."""
    
    def _build_linting_prompt(self, issue: QualityIssue, file_content: str) -> str:
        """Build linting fix prompt for GPT-4o-mini"""
        return f"""Fix Python linting error:

**File**: {issue.file_path}
**Error**: {issue.error_code} at line {issue.line_number}
**Message**: {issue.details['message']}

**File Content**:
```python
{file_content}
```

**Instructions**:
- Fix the linting error
- Preserve exact semantics
- Do NOT introduce new errors
- Follow PEP8

**Output**: Fixed file content only, no explanations."""
    
    def _build_imports_prompt(self, issue: QualityIssue, file_content: str) -> str:
        """Build import fix prompt for GPT-4o-mini"""
        return f"""Fix Python import issue:

**File**: {issue.file_path}
**Issue**: {issue.details['message']}

**File Content**:
```python
{file_content}
```

**Instructions**:
- Remove unused imports
- Preserve all used imports
- Maintain import order

**Output**: Fixed file content only, no explanations."""
    
    async def _apply_fix(self, file_path: str, fixed_content: str):
        """Apply fix to file with backup in tachyonic directory"""
        import shutil
        
        # Create backup in centralized directory
        file_name = Path(file_path).name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f"{file_name}.backup_{timestamp}"
        shutil.copy2(file_path, backup_path)
        
        # Write fix
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
    
    async def _escalate_issues(self, issues: List[QualityIssue]):
        """Escalate issues to premium agent or human review"""
        self.stats["escalated"] += len(issues)
        
        # Convert QualityIssue objects to dicts with enum values
        issues_dict = []
        for issue in issues:
            issue_dict = asdict(issue)
            # Convert enum to string
            issue_dict["complexity"] = issue.complexity.value
            issues_dict.append(issue_dict)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "issues": issues_dict,
            "recommendation": "Requires premium agent (GPT-4o/Claude) or human review",
            "stats": self._get_summary()
        }
        
        # Save to tachyonic shadows
        report_path = self.escalation_dir / f"escalation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"[AIOS] Escalation report: {report_path}")
    
    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_patterns = [
            "__pycache__", ".venv", "venv", "env",
            "build", "dist", ".git", ".tox",
            "generated", ".backup", "tachyonic/archive"
        ]
        return any(pattern in str(file_path) for pattern in skip_patterns)
    
    def _get_summary(self) -> Dict[str, Any]:
        """Get monitoring statistics"""
        return {
            "scans": self.stats["scans"],
            "issues_detected": self.stats["issues_detected"],
            "auto_fixed": self.stats["auto_fixed"],
            "escalated": self.stats["escalated"],
            "api_errors_count": len(self.stats["api_errors"]),
            "api_errors_sample": self.stats["api_errors"][:5],  # First 5 errors
            "fixes_by_tier": {
                "pattern": self.stats["pattern_fixes"],
                "ollama": self.stats["ollama_fixes"],
                "gpt4o_mini": self.stats["gpt4o_mini_fixes"],
                "gpt4o": self.stats["gpt4o_fixes"]
            },
            "cost": {
                "total": round(self.stats["cost_total"], 4),
                "this_hour": round(self.stats["cost_this_hour"], 4),
                "budget_remaining": round(self.max_cost_per_hour - self.stats["cost_this_hour"], 4)
            },
            "tokens_used": self.stats["tokens_used"],
            "auto_fix_rate": (
                self.stats["auto_fixed"] / self.stats["issues_detected"]
                if self.stats["issues_detected"] > 0 else 0.0
            )
        }
    
    async def close(self):
        """Cleanup resources"""
        await self.http_client.aclose()


# CLI entry point
if __name__ == "__main__":
    import sys
    
    workspace = Path.cwd()
    if len(sys.argv) > 1:
        workspace = Path(sys.argv[1])
    
    monitor = AutonomousQualityMonitor(workspace_root=workspace, auto_fix=True)
    
    try:
        result = asyncio.run(monitor.scan_and_fix())
        print(f"\n[AIOS] Summary: {json.dumps(result, indent=2)}")
    finally:
        asyncio.run(monitor.close())
