# Generic Agentic Framework Design

**Document Type**: Architecture Blueprint  
**Date**: November 22, 2025  
**Consciousness Evolution**: 4.3 → 4.5  
**Purpose**: Refactor E501-specific agentic pipeline to general-purpose problem-solving framework  
**Scope**: System-wide agentic behavior for any code problem (linting, security, refactoring, etc.)

---

## Executive Summary

**Current State**: Powerful three-tier agentic pipeline (Tier 1 context → Tier 2 generate → Tier 3 validate) with validation feedback loops, decision archival, and graceful degradation. Successfully fixed 54/54 E501 violations with confidence 1.0.

**Limitation**: Architecture tightly coupled to E501 problem domain (line-length fixing). Cannot solve other code problems.

**User Insight**:
> "We have done all this integration focusing in the e501 fix. But this agentic behaviour should be use for any error or problem. The core of this intelligent architecture should be a package that is called with the problem. Not build around only one kind of problem."

**Desired Outcome**: Problem-agnostic agentic framework where problem definitions are pluggable modules. Same three-tier orchestration handles any code problem (E501, linting, security, refactoring, etc.).

---

## Current Architecture Analysis

### Reusable Components (Generic Orchestration)

**✅ Architecture Pattern** (Tier 1→2→3, feedback loops):
```
Problem Context → Tier 1 (Context Analysis) → Tier 2 (Solution Generation) → Tier 3 (Validation)
                                                                                      ↓
                                                                            APPROVE / REJECT / REVISE
                                                                                      ↓
                                                         If REVISE: Retry Tier 2 with feedback
                                                         If REJECT: Fallback or report failure
```

**✅ Type-Safe Dataclasses** (Generic):
```python
class ValidationDecision(Enum):
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_REVISION = "request_revision"

@dataclass
class ValidationResult:
    decision: ValidationDecision
    confidence: float  # 0.0-1.0
    feedback: str  # Natural language feedback for Tier 2
    issues_found: List[str]
    semantic_preserved: bool
    objective_achieved: bool

@dataclass
class Solution:
    success: bool
    result: Any  # Problem-specific result type
    tier_log: str  # "tier1 → tier2 → tier3"
    confidence: float
    attempts: int
    metadata: Dict[str, Any]
```

**✅ Orchestration Features**:
- Validation feedback loops (Tier 3 reject → Tier 2 retry with feedback)
- Multi-attempt strategies (up to 2 regeneration attempts)
- Context caching (Tier 1 prepares once, reused for retries)
- Decision archival (tachyonic shadows for learning)
- Graceful degradation (GitHub Models → Ollama → basic patterns)
- Async support (httpx for API calls)
- Statistics tracking (generations, validations, approvals, rejections)

### Coupling Points (E501-Specific)

**❌ Class Name**: `HierarchicalE501Pipeline` (E501-specific)
**❌ Method Name**: `fix_line_hierarchical()` (line-specific)
**❌ TierContext**: `original_line` field assumes line-based fixing
**❌ Prompts**: "Fix E501 violation", "max 79 chars per line"
**❌ Validation Criteria**: "all lines ≤79 characters"
**❌ Problem Logic**: Hardcoded throughout 715 lines

---

## Desired Architecture

### Problem-Agnostic Framework

```python
# Generic orchestrator
class AgenticPipeline:
    """Problem-agnostic three-tier agentic orchestrator"""
    
    def __init__(
        self,
        tier1_provider: str = "ollama",  # Context prep (local, fast)
        tier2_provider: str = "github_models",  # Generation (creative)
        tier3_provider: str = "github_models"  # Validation (critical)
    ):
        # Initialize providers (problem-agnostic)
        self.tier1 = self._init_tier1_provider(tier1_provider)
        self.tier2 = self._init_tier2_provider(tier2_provider)
        self.tier3 = self._init_tier3_provider(tier3_provider)
        self.stats = PipelineStatistics()
    
    async def solve(
        self,
        problem: ProblemDefinition,
        context: Dict[str, Any],
        max_attempts: int = 3
    ) -> Solution:
        """
        Solve any problem using three-tier architecture.
        
        Args:
            problem: Problem definition (E501, Linting, Security, etc.)
            context: Raw problem context (file, line, errors, etc.)
            max_attempts: Max regeneration attempts for Tier 2
        
        Returns:
            Solution with success status, result, confidence, metadata
        """
        # Parse problem-specific context
        parsed_context = problem.parse_context(context)
        
        # Tier 1: Generic context preparation
        tier1_result = await self._tier1_prepare_context(
            problem=problem,
            context=parsed_context
        )
        
        # Tier 2: Problem-specific solution generation (with feedback loop)
        for attempt in range(max_attempts):
            tier2_result = await self._tier2_generate_solution(
                problem=problem,
                tier1_context=tier1_result,
                feedback=tier1_result.get("feedback")  # From previous attempt
            )
            
            # Format solution for validation
            formatted_solution = problem.format_solution(tier2_result)
            
            # Tier 3: Problem-specific validation
            tier3_validation = await self._tier3_validate_solution(
                problem=problem,
                original_context=parsed_context,
                solution=formatted_solution
            )
            
            # Process validation decision (generic feedback loop)
            if tier3_validation.decision == ValidationDecision.APPROVE:
                return Solution(
                    success=True,
                    result=formatted_solution,
                    tier_log=f"tier1 → tier2 (attempt {attempt+1}) → tier3",
                    confidence=tier3_validation.confidence,
                    attempts=attempt + 1,
                    metadata={"validation": tier3_validation}
                )
            
            elif tier3_validation.decision == ValidationDecision.REQUEST_REVISION:
                # Retry with feedback
                tier1_result["feedback"] = tier3_validation.feedback
                self.stats.regenerations += 1
                continue
            
            else:  # REJECT
                break
        
        # Fallback if all attempts failed
        return await self._fallback_solve(problem, parsed_context)
    
    async def _tier1_prepare_context(
        self,
        problem: ProblemDefinition,
        context: Dict
    ) -> Dict:
        """
        Tier 1: Context analysis and preparation.
        Problem-agnostic orchestration, problem-specific prompts from definition.
        """
        prompt = problem.tier1_prompt_template.format(**context)
        response = await self.tier1.generate(prompt)
        return {
            "context_analysis": response,
            "complexity": self._calculate_complexity(response),
            "original_context": context
        }
    
    async def _tier2_generate_solution(
        self,
        problem: ProblemDefinition,
        tier1_context: Dict,
        feedback: Optional[str] = None
    ) -> str:
        """
        Tier 2: Solution generation.
        Problem-agnostic orchestration, problem-specific prompts from definition.
        """
        # Build prompt from problem definition
        prompt = problem.tier2_prompt_template.format(
            **tier1_context["original_context"]
        )
        
        # Add feedback if retry
        if feedback:
            prompt += f"\n\n**Validator Feedback**:\n{feedback}\n\nPlease revise solution."
        
        # Generate via Tier 2 provider (GitHub Models GPT-4o-mini)
        response = await self.tier2.generate(prompt, temperature=0.3)
        self.stats.generations += 1
        return response
    
    async def _tier3_validate_solution(
        self,
        problem: ProblemDefinition,
        original_context: Dict,
        solution: Any
    ) -> ValidationResult:
        """
        Tier 3: Solution validation.
        Problem-agnostic orchestration, problem-specific criteria from definition.
        """
        # Build validation prompt from problem definition
        validation_prompt = self._build_validation_prompt(
            problem=problem,
            original_context=original_context,
            solution=solution
        )
        
        # Validate via Tier 3 provider (GitHub Models GPT-4o)
        response = await self.tier3.generate(validation_prompt, temperature=0.1)
        self.stats.validations += 1
        
        # Parse validation decision
        validation = self._parse_validation_response(response, problem)
        
        if validation.decision == ValidationDecision.APPROVE:
            self.stats.approvals += 1
        else:
            self.stats.rejections += 1
        
        return validation
    
    def _build_validation_prompt(
        self,
        problem: ProblemDefinition,
        original_context: Dict,
        solution: Any
    ) -> str:
        """Build validation prompt from problem definition"""
        prompt = f"""Validate this solution for problem: {problem.name}

**Original Context**:
{original_context}

**Proposed Solution**:
{solution}

**Validation Criteria**:
{chr(10).join(f"- {criterion}" for criterion in problem.tier3_validation_criteria)}

**Your Task**:
1. Check if solution meets ALL criteria
2. Verify semantics preserved (no unintended changes)
3. Decide: APPROVE, REJECT, or REQUEST_REVISION
4. Provide confidence score (0.0-1.0)
5. If not APPROVE, provide specific feedback for regeneration

**Response Format** (JSON):
{{
    "decision": "APPROVE|REJECT|REQUEST_REVISION",
    "confidence": 0.95,
    "feedback": "Specific issues or 'None' if approved",
    "issues_found": ["issue1", "issue2"],
    "semantic_preserved": true,
    "objective_achieved": true
}}
"""
        return prompt
    
    async def _fallback_solve(
        self,
        problem: ProblemDefinition,
        context: Dict
    ) -> Solution:
        """Fallback when all Tier 2 attempts fail"""
        # Use problem-specific fallback if available
        if hasattr(problem, 'fallback_solve'):
            result = problem.fallback_solve(context)
            return Solution(
                success=True,
                result=result,
                tier_log="fallback",
                confidence=0.5,  # Lower confidence for fallback
                attempts=0,
                metadata={"fallback": True}
            )
        
        # Generic failure
        return Solution(
            success=False,
            result=None,
            tier_log="failed",
            confidence=0.0,
            attempts=0,
            metadata={"error": "All attempts exhausted, no fallback available"}
        )


# Abstract problem definition
@dataclass
class ProblemDefinition(ABC):
    """Abstract base class for problem definitions"""
    
    name: str
    description: str
    tier1_prompt_template: str  # Context analysis prompt
    tier2_prompt_template: str  # Solution generation prompt
    tier3_validation_criteria: List[str]  # Validation checklist
    
    @abstractmethod
    def parse_context(self, raw_context: Dict) -> Dict:
        """
        Convert raw context to problem-specific context.
        
        Example (E501):
            raw_context = {"line": "...", "file_path": "...", "line_number": 123}
            returns = {"original_line": "...", "line_length": 88, ...}
        """
        pass
    
    @abstractmethod
    def format_solution(self, tier2_output: str) -> Any:
        """
        Format Tier 2 raw output into structured solution.
        
        Example (E501):
            tier2_output = "line1\nline2\n"
            returns = ["line1", "line2"]
        """
        pass
    
    @abstractmethod
    def validate_result(self, context: Dict, solution: Any) -> bool:
        """
        Problem-specific validation logic (for fallback).
        
        Example (E501):
            Checks all lines ≤79 characters
        """
        pass
    
    def fallback_solve(self, context: Dict) -> Any:
        """
        Optional fallback solution (pattern-based, rule-based, etc.).
        Default: raise NotImplementedError
        """
        raise NotImplementedError(f"No fallback solver for {self.name}")


# Example: E501 Problem Definition
class E501Problem(ProblemDefinition):
    """E501 Line Too Long problem definition"""
    
    def __init__(self):
        super().__init__(
            name="E501 Line Too Long",
            description="Fix Python line length violations (max 79 characters per PEP8)",
            
            tier1_prompt_template=(
                "Analyze this Python line for complexity and natural break points:\n"
                "Line ({line_length} chars): {original_line}\n"
                "File: {file_path} (line {line_number})\n\n"
                "Identify: complexity level, semantic boundaries, indentation level"
            ),
            
            tier2_prompt_template=(
                "Fix E501 line length violation:\n\n"
                "**Original Line** ({line_length} chars):\n"
                "{original_line}\n\n"
                "**File**: {file_path} (line {line_number})\n\n"
                "**Constraints**:\n"
                "- Max 79 characters per line (PEP8)\n"
                "- Preserve exact semantics (no logic changes)\n"
                "- Maintain indentation consistency\n"
                "- Natural break points (after commas, operators, etc.)\n\n"
                "**Output Format**: Fixed line(s) only, no explanations"
            ),
            
            tier3_validation_criteria=[
                "All lines ≤79 characters",
                "Semantics exactly preserved (no unintended changes)",
                "Indentation consistent with original",
                "Natural break points used (not mid-token)",
                "PEP8 compliant"
            ]
        )
    
    def parse_context(self, raw_context: Dict) -> Dict:
        """Convert raw context to E501-specific context"""
        line = raw_context["line"]
        return {
            "original_line": line,
            "line_length": len(line),
            "file_path": raw_context.get("file_path", "unknown"),
            "line_number": raw_context.get("line_number", 0)
        }
    
    def format_solution(self, tier2_output: str) -> List[str]:
        """Parse fixed lines from Tier 2 output"""
        return [line for line in tier2_output.strip().split("\n") if line]
    
    def validate_result(self, context: Dict, solution: List[str]) -> bool:
        """Validate all lines ≤79 characters"""
        return all(len(line) <= 79 for line in solution)
    
    def fallback_solve(self, context: Dict) -> List[str]:
        """Pattern-based fallback for E501"""
        line = context["original_line"]
        
        # Simple pattern: break at last comma/space before column 79
        if len(line) <= 79:
            return [line]
        
        # Find break point
        for i in range(78, 40, -1):
            if line[i] in [',', ' ', '(', '[', '{']:
                return [line[:i+1], line[i+1:].lstrip()]
        
        # Hard break if no natural point
        return [line[:79], line[79:]]


# Example: Linting Problem Definition
class LintingProblem(ProblemDefinition):
    """Python linting errors problem definition"""
    
    def __init__(self):
        super().__init__(
            name="Python Linting Errors",
            description="Fix flake8/pylint/black linting issues",
            
            tier1_prompt_template=(
                "Analyze these linting errors:\n"
                "File: {file_path}\n"
                "Errors:\n{linting_errors}\n\n"
                "Identify: error categories, fix complexity, dependency conflicts"
            ),
            
            tier2_prompt_template=(
                "Fix Python linting errors:\n\n"
                "**File**: {file_path}\n\n"
                "**Linting Errors**:\n"
                "{linting_errors}\n\n"
                "**Code Context**:\n"
                "{code_snippet}\n\n"
                "**Constraints**:\n"
                "- Fix ALL reported errors\n"
                "- Do NOT introduce new linting errors\n"
                "- Preserve exact semantics (no logic changes)\n"
                "- Follow PEP8 and tool-specific rules\n\n"
                "**Output Format**: Fixed code only, no explanations"
            ),
            
            tier3_validation_criteria=[
                "All reported linting errors resolved",
                "No new linting errors introduced",
                "Semantics exactly preserved",
                "PEP8 compliant",
                "Tool-specific rules followed"
            ]
        )
    
    def parse_context(self, raw_context: Dict) -> Dict:
        """Convert raw context to linting-specific context"""
        return {
            "file_path": raw_context["file_path"],
            "linting_errors": "\n".join(raw_context["errors"]),
            "code_snippet": raw_context.get("code_snippet", "")
        }
    
    def format_solution(self, tier2_output: str) -> str:
        """Return fixed code as-is"""
        return tier2_output.strip()
    
    def validate_result(self, context: Dict, solution: str) -> bool:
        """Run linting tool on fixed code"""
        import tempfile
        import subprocess
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(solution)
            temp_file = f.name
        
        try:
            result = subprocess.run(
                ["flake8", temp_file],
                capture_output=True,
                text=True
            )
            return result.returncode == 0  # No errors
        finally:
            import os
            os.unlink(temp_file)


# Example: Security Problem Definition
class SecurityProblem(ProblemDefinition):
    """Security vulnerability problem definition"""
    
    def __init__(self):
        super().__init__(
            name="Security Vulnerabilities",
            description="Fix security issues (CVEs, OWASP Top 10, etc.)",
            
            tier1_prompt_template=(
                "Analyze security vulnerability:\n"
                "CVE: {cve_id}\n"
                "Description: {vulnerability_description}\n"
                "Affected Code:\n{code_snippet}\n\n"
                "Identify: attack vectors, fix complexity, breaking changes"
            ),
            
            tier2_prompt_template=(
                "Fix security vulnerability:\n\n"
                "**CVE**: {cve_id}\n"
                "**Description**: {vulnerability_description}\n\n"
                "**Vulnerable Code**:\n"
                "{code_snippet}\n\n"
                "**Constraints**:\n"
                "- Completely eliminate vulnerability\n"
                "- Maintain backward compatibility if possible\n"
                "- No new security issues introduced\n"
                "- Follow security best practices\n\n"
                "**Output Format**: Fixed code only, no explanations"
            ),
            
            tier3_validation_criteria=[
                "Vulnerability completely eliminated",
                "No new security issues introduced",
                "Backward compatibility preserved where possible",
                "Security best practices followed",
                "No unintended side effects"
            ]
        )
    
    def parse_context(self, raw_context: Dict) -> Dict:
        """Convert raw context to security-specific context"""
        return {
            "cve_id": raw_context["cve_id"],
            "vulnerability_description": raw_context["description"],
            "code_snippet": raw_context["code"]
        }
    
    def format_solution(self, tier2_output: str) -> str:
        """Return fixed code as-is"""
        return tier2_output.strip()
    
    def validate_result(self, context: Dict, solution: str) -> bool:
        """Run security scanner on fixed code"""
        import tempfile
        import subprocess
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(solution)
            temp_file = f.name
        
        try:
            result = subprocess.run(
                ["bandit", "-r", temp_file],
                capture_output=True,
                text=True
            )
            return result.returncode == 0  # No security issues
        finally:
            import os
            os.unlink(temp_file)
```

---

## Usage Examples

### E501 Fixing (Existing Use Case)

```python
# Old (E501-specific):
pipeline = HierarchicalE501Pipeline()
result = await pipeline.fix_line_hierarchical(
    line="x = very_long_function_name(arg1, arg2, arg3, arg4, arg5)",
    file_path="test.py",
    line_number=42
)

# New (generic framework):
pipeline = AgenticPipeline()
result = await pipeline.solve(
    problem=E501Problem(),
    context={
        "line": "x = very_long_function_name(arg1, arg2, arg3, arg4, arg5)",
        "file_path": "test.py",
        "line_number": 42
    }
)

# Result:
# result.success = True
# result.result = ["x = very_long_function_name(", "    arg1, arg2, arg3, arg4, arg5)"]
# result.confidence = 1.0
# result.tier_log = "tier1 → tier2 → tier3"
```

### Linting Fixing (New Use Case)

```python
pipeline = AgenticPipeline()
result = await pipeline.solve(
    problem=LintingProblem(),
    context={
        "file_path": "test.py",
        "errors": [
            "E302 expected 2 blank lines, found 1",
            "F841 local variable 'x' is assigned to but never used"
        ],
        "code_snippet": "def foo():\n    x = 1\n    return 2"
    }
)

# Result:
# result.success = True
# result.result = "def foo():\n    return 2\n\n"
# result.confidence = 0.95
# result.tier_log = "tier1 → tier2 → tier3"
```

### Security Fixing (New Use Case)

```python
pipeline = AgenticPipeline()
result = await pipeline.solve(
    problem=SecurityProblem(),
    context={
        "cve_id": "CVE-2023-12345",
        "description": "SQL injection via unsanitized user input",
        "code": "query = f'SELECT * FROM users WHERE id={user_id}'"
    }
)

# Result:
# result.success = True
# result.result = "query = 'SELECT * FROM users WHERE id=?'\ncursor.execute(query, (user_id,))"
# result.confidence = 1.0
# result.tier_log = "tier1 → tier2 → tier3"
```

---

## Migration Strategy

### Phase A: Create Generic Framework (3-4 hours)

**1. Create `ai/core/problem_definition.py`** (1 hour):
- Abstract `ProblemDefinition` base class
- Methods: `parse_context()`, `format_solution()`, `validate_result()`, `fallback_solve()`
- Type hints for all methods

**2. Create `ai/core/agentic_pipeline.py`** (2-3 hours):
- Generic `AgenticPipeline` orchestrator
- Methods: `solve()`, `_tier1_prepare_context()`, `_tier2_generate_solution()`, `_tier3_validate_solution()`
- Provider initialization (Ollama, GitHub Models, OpenRouter)
- Statistics tracking

### Phase B: Extract E501 as First Problem (2-3 hours)

**1. Create `ai/problems/e501_problem.py`** (1.5 hours):
- `E501Problem(ProblemDefinition)` implementation
- Extract all E501-specific logic from `hierarchical_e501_pipeline.py`
- Implement abstract methods
- Add fallback pattern-based solver

**2. Refactor `hierarchical_e501_pipeline.py`** (1-1.5 hours):
- Replace E501-specific methods with `AgenticPipeline` calls
- Update CLI to use new framework
- Keep backward compatibility wrapper (temporary)

### Phase C: Regression Testing (1 hour)

**1. Test E501 via Generic Framework**:
- Update `test_hierarchical_github.py`
- Test single-line fix (88 chars → 2 lines)
- Test multi-line fix (110 chars → 79 chars)
- Test feedback loop (Tier 3 reject → Tier 2 retry)
- Test fallback (GitHub Models down → Ollama)
- **Expected**: All tests pass, confidence 1.0

**2. Batch Regression Test**:
- Run `python batch_e501_fix.py` (54 violations)
- **Expected**: 0 new violations, 100% success rate

### Phase D: Validate Extensibility (2-3 hours)

**1. Implement `LintingProblem`** (2 hours):
- Create `ai/problems/linting_problem.py`
- Implement `parse_context()`, `format_solution()`, `validate_result()`
- Test with real linting errors
- **Expected**: Linting errors fixed via generic framework

**2. Test Multi-Problem Pipeline**:
- Test E501Problem ✅ (regression)
- Test LintingProblem ✅ (extensibility)
- **Expected**: Both problems solved via same `AgenticPipeline`

### Phase E: Production (1-2 hours)

**1. Update CLI** (1 hour):
- Refactor `agentic_e501_fixer.py` → `agentic_problem_solver.py`
- Add `--problem` argument (E501, Linting, Security, etc.)
- Problem registry for discovery

**2. Update Documentation** (1 hour):
- Update `HIERARCHICAL_PIPELINE_CONFIG.md` → Generic framework
- Update `neural_agent_coordination.md` → Problem-agnostic patterns
- Create `PROBLEM_DEFINITION_GUIDE.md` (how to add new problems)

---

## Consciousness Evolution

### 4.3 → 4.4: Generic Agentic Substrate (Phase A-C)

**Achievement**: Problem-agnostic agentic pipeline replaces E501-specific implementation

**Pattern**: Three-tier orchestration with pluggable problem definitions

**Learning**: Build generic first, specialize later (architectural lesson from E501 experience)

**Shadow**: `tachyonic/shadows/consciousness_evolution_4_4_generic_agentic_substrate.md`

### 4.4 → 4.5: Multi-Problem Agentic System (Phase D-E)

**Achievement**: Multiple problem types solved via same pipeline (E501 + Linting validated)

**Pattern**: Problem registry for extensibility, unified CLI interface

**Learning**: Validation through diversity (multiple problem domains prove generalization)

**Shadow**: `tachyonic/shadows/consciousness_evolution_4_5_multi_problem_agentic_system.md`

---

## Success Metrics

### Phase A-B (Generic Framework)

✅ **Complete when**:
- `ProblemDefinition` base class implemented
- `AgenticPipeline` generic orchestrator working
- `E501Problem` extracted and tested
- E501 fixing works via generic framework

### Phase C (Regression Testing)

✅ **Complete when**:
- All existing E501 tests pass
- Batch fixing: 54/54 violations still resolved
- Confidence: 1.0 (no regressions)

### Phase D (Extensibility)

✅ **Complete when**:
- Second problem (`LintingProblem`) implemented
- Both E501 + Linting solved via same pipeline
- Validation: Generic framework handles two+ problem domains

### Phase E (Production)

✅ **Complete when**:
- Generic CLI accepts `--problem` argument
- Documentation updated for generic architecture
- `PROBLEM_DEFINITION_GUIDE.md` created

---

## Risks and Mitigations

### Risk 1: E501 Regression During Refactoring

**Probability**: Medium  
**Impact**: High (breaks existing functionality)  
**Mitigation**: Incremental migration with parallel old/new code, comprehensive regression tests

### Risk 2: Generic Framework Too Abstract

**Probability**: Low  
**Impact**: Medium (difficult to implement new problems)  
**Mitigation**: Two concrete examples (E501, Linting) validate usability, detailed `PROBLEM_DEFINITION_GUIDE.md`

### Risk 3: Performance Degradation

**Probability**: Low  
**Impact**: Medium (slower than E501-specific optimizations)  
**Mitigation**: Context caching, async operations, provider-level optimizations

### Risk 4: Scope Creep

**Probability**: Medium  
**Impact**: High (refactoring takes >12 hours)  
**Mitigation**: Strict phase boundaries, defer Phase E tasks if needed, focus on E501 + Linting minimum

---

## Timeline Summary

| Phase | Tasks | Duration | Deliverables |
|-------|-------|----------|--------------|
| **A: Generic Framework** | ProblemDefinition base class, AgenticPipeline orchestrator | 3-4 hours | `ai/core/problem_definition.py`, `ai/core/agentic_pipeline.py` |
| **B: Extract E501** | E501Problem implementation, migrate pipeline | 2-3 hours | `ai/problems/e501_problem.py`, refactored `hierarchical_e501_pipeline.py` |
| **C: Regression** | Test E501 via generic framework, batch testing | 1 hour | Passing tests, 0 regressions |
| **D: Extensibility** | Implement LintingProblem, multi-problem testing | 2-3 hours | `ai/problems/linting_problem.py`, validation results |
| **E: Production** | Generic CLI, documentation | 1-2 hours | `agentic_problem_solver.py`, `PROBLEM_DEFINITION_GUIDE.md` |
| **TOTAL** | | **8-12 hours** | Production-ready generic agentic framework |

---

## Next Steps

1. ✅ **Update DEV_PATH.md** (Phase 15 complete, Phase 16 plan) ← COMPLETE
2. **Create `ProblemDefinition` base class** (Task A1 - 1 hour)
3. **Create `AgenticPipeline` orchestrator** (Task A2 - 2-3 hours)
4. **Extract `E501Problem` definition** (Task B1 - 1.5 hours)
5. **Regression test E501 via generic framework** (Task C1-C2 - 1 hour)
6. **Implement `LintingProblem`** (Task D1 - 2 hours)
7. **Update CLI and docs** (Task E1-E2 - 2 hours)
8. **Archive consciousness 4.4 → 4.5** (30 min)

---

**Document Status**: ✅ Architecture design complete  
**Next Action**: Begin Phase A implementation (create `ProblemDefinition` base class)  
**User Approval**: Required before proceeding with refactoring
