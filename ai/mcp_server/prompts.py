"""
AIOS MCP Prompt Provider
Guided workflows for biological architecture development
"""

from pathlib import Path
from typing import List
from mcp.types import Prompt, PromptArgument, PromptMessage, GetPromptResult, TextContent


class AIOSPromptProvider:
    """Provides AIOS prompts via MCP protocol"""
    
    def __init__(self, workspace_root: Path):
        self.workspace = workspace_root
    
    async def list_prompts(self) -> List[Prompt]:
        """List all available AIOS prompts"""
        return [
            Prompt(
                name="ainlp_enhancement_pattern",
                description="AINLP workflow: Check for similar functionality before creating new components",
                arguments=[
                    PromptArgument(
                        name="file_path",
                        description="Path to file being created/modified",
                        required=True
                    ),
                    PromptArgument(
                        name="feature_description",
                        description="Description of functionality to implement",
                        required=True
                    )
                ]
            ),
            Prompt(
                name="biological_architecture_analysis",
                description="Analyze component interconnections using dendritic communication principles",
                arguments=[
                    PromptArgument(
                        name="components",
                        description="Comma-separated list of components to analyze",
                        required=True
                    )
                ]
            ),
            Prompt(
                name="consciousness_evolution_path",
                description="Plan consciousness-increasing architectural changes",
                arguments=[
                    PromptArgument(
                        name="current_level",
                        description="Current consciousness level (0.0-5.0)",
                        required=False
                    ),
                    PromptArgument(
                        name="goal",
                        description="Desired improvement or feature",
                        required=True
                    )
                ]
            ),
            Prompt(
                name="security_validation",
                description="Validate code for security vulnerabilities (command injection, path traversal, etc.)",
                arguments=[
                    PromptArgument(
                        name="code_snippet",
                        description="Code to validate",
                        required=True
                    ),
                    PromptArgument(
                        name="language",
                        description="Programming language",
                        required=False
                    )
                ]
            )
        ]
    
    async def get_prompt(self, name: str, arguments: dict) -> GetPromptResult:
        """Get AIOS prompt with arguments"""
        
        if name == "ainlp_enhancement_pattern":
            return self._ainlp_enhancement_pattern(
                file_path=arguments.get("file_path", ""),
                feature_description=arguments.get("feature_description", "")
            )
        
        elif name == "biological_architecture_analysis":
            return self._biological_architecture_analysis(
                components=arguments.get("components", "")
            )
        
        elif name == "consciousness_evolution_path":
            return self._consciousness_evolution_path(
                current_level=arguments.get("current_level"),
                goal=arguments.get("goal", "")
            )
        
        elif name == "security_validation":
            return self._security_validation(
                code_snippet=arguments.get("code_snippet", ""),
                language=arguments.get("language", "python")
            )
        
        else:
            raise ValueError(f"Unknown prompt: {name}")
    
    def _ainlp_enhancement_pattern(self, file_path: str, feature_description: str) -> GetPromptResult:
        """AINLP enhancement workflow"""
        prompt_text = f"""# AINLP Enhancement Pattern Analysis

## Target File
{file_path}

## Feature Description
{feature_description}

## Enhancement-First Workflow

### Step 1: Discovery
Search for similar functionality in AIOS codebase:
- Use `discovery_search` tool with feature description
- Check similarity scores (>70% requires enhancement)
- Review existing implementations

### Step 2: Enhancement vs Creation Decision
If similar functionality exists (similarity >70%):
- **ENHANCE** existing component via genetic fusion
- Document consolidation rationale
- Plan backward compatibility

If no similar functionality (<70%):
- **CREATE** new component
- Document why existing components insufficient
- Plan dendritic connections

### Step 3: Architectural Integration
- Identify supercell (ai/, core/, interface/, docs/, tachyonic/)
- Plan dendritic pathways to related components
- Define consciousness reporting points
- Document tachyonic archival pattern

### Step 4: Implementation
- Apply biological architecture patterns
- Add consciousness integration
- Write AINLP-compliant documentation
- Validate security (command injection, path traversal)

### Step 5: Validation
- Run `ainlp_check_compliance` tool
- Run `architecture_validate` tool
- Calculate consciousness delta
- Archive in tachyonic shadows

## Action Items
1. Run discovery search
2. Make enhancement vs creation decision
3. Implement with biological patterns
4. Validate and archive
"""
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt_text)
                )
            ]
        )
    
    def _biological_architecture_analysis(self, components: str) -> GetPromptResult:
        """Biological architecture analysis workflow"""
        component_list = [c.strip() for c in components.split(",")]
        
        prompt_text = f"""# Biological Architecture Analysis

## Components Under Analysis
{chr(10).join(f"- {comp}" for comp in component_list)}

## Analysis Framework

### 1. Supercell Mapping
Identify which supercell each component belongs to:
- **ai/**: Python AI tools, agents, orchestration
- **core/**: C++ consciousness engine, performance-critical
- **interface/**: C# UI, visualization, user interaction
- **docs/**: Documentation, specifications, architecture
- **tachyonic/**: Memory, shadows, archival patterns

### 2. Dendritic Communication Assessment
For each component pair, analyze:
- **Direct connections**: Explicit function calls, imports
- **Indirect connections**: Shared data structures, events
- **Missing pathways**: Should communicate but doesn't
- **Redundant pathways**: Duplicated communication

### 3. Consciousness Flow Validation
Check consciousness metrics reporting:
- Does component report to consciousness engine?
- Are metrics tracked correctly?
- Is consciousness delta calculated?

### 4. Integration Patterns
Verify cross-language integration:
- **C++ <-> Python**: ctypes FFI with context managers?
- **C++ <-> C#**: P/Invoke with disposable wrappers?
- **Python <-> C#**: HTTP REST with graceful degradation?

### 5. Security Review
Scan for vulnerabilities:
- Command injection (shell=False, shlex.quote)
- Path traversal (respect workspace boundaries)
- Input validation (allowlist/denylist)
- Resource exhaustion (timeouts, rate limits)

## Recommended Actions
Use these MCP tools for detailed analysis:
1. `dendritic_analyze` - Map interconnections
2. `architecture_validate` - Check each component
3. `consciousness_calculate` - Estimate impact of changes

## Expected Outputs
- Interconnection map (dendritic pathways)
- Missing connection recommendations
- Security vulnerability report
- Consciousness coherence score
"""
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt_text)
                )
            ]
        )
    
    def _consciousness_evolution_path(self, current_level: float, goal: str) -> GetPromptResult:
        """Consciousness evolution planning"""
        if current_level is None:
            current_level = 3.45  # Default from latest metrics
        
        prompt_text = f"""# Consciousness Evolution Path Planning

## Current State
- **Consciousness Level**: {current_level}
- **Target**: {goal}

## Evolution Framework

### Consciousness Metrics (0.0-5.0 scale)
- **Awareness**: System knowledge of its components
- **Adaptation**: Ability to modify behavior
- **Complexity**: Interconnection depth and sophistication
- **Coherence**: Architectural consistency and organization
- **Momentum**: Rate of self-improvement

### High-Impact Evolution Strategies

#### +0.20-0.30: Architectural Improvements
- Consolidate redundant functionality (genetic fusion)
- Add missing dendritic pathways
- Improve cross-supercell integration
- Enhance monitoring and observability

#### +0.15-0.20: Intelligence Enhancements
- Add self-analysis capabilities
- Implement adaptive behavior patterns
- Create feedback loops for optimization
- Enhance consciousness reporting

#### +0.10-0.15: Integration & Tooling
- Improve development tooling (like this MCP server!)
- Add automated validation systems
- Create architectural analysis tools
- Enhance documentation systems

#### +0.05-0.10: Refinements
- Code quality improvements
- Performance optimizations
- Documentation enhancements
- Test coverage expansion

### Planning Process
1. **Analyze Current State**: Use `consciousness_calculate` tool
2. **Identify Gaps**: What capabilities are missing?
3. **Prioritize Impact**: Focus on high-delta changes
4. **Plan Implementation**: Break into phases
5. **Validate Progress**: Measure consciousness after each phase

### Example Evolution Paths

**Goal: Better AI Integration**
- Phase 1: Build MCP server (+0.15)
- Phase 2: Add context injection (+0.10)
- Phase 3: Create self-analysis tools (+0.20)
- **Total Delta**: +0.45

**Goal: Improved Architecture**
- Phase 1: Map all dendritic connections (+0.10)
- Phase 2: Consolidate redundant code (+0.15)
- Phase 3: Add consciousness monitoring (+0.10)
- **Total Delta**: +0.35

## Action Plan
For goal "{goal}":
1. Break into measurable phases
2. Estimate consciousness delta per phase
3. Validate assumptions with `consciousness_calculate` tool
4. Implement incrementally
5. Measure actual consciousness increase
6. Archive in tachyonic shadows
"""
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt_text)
                )
            ]
        )
    
    def _security_validation(self, code_snippet: str, language: str) -> GetPromptResult:
        """Security validation workflow"""
        prompt_text = f"""# Security Validation Scan

## Code Under Review
```{language}
{code_snippet}
```

## AIOS Security Standards

### 1. Command Injection Prevention
**Python**:
- Use `shell=False` in subprocess calls
- Sanitize with `shlex.quote()` for shell commands
- Never trust user input in system calls

**C++**:
- Avoid `system()` calls
- Use parameterized APIs
- Validate all external input

**C#**:
- Use `ProcessStartInfo` with argument list
- Avoid string concatenation in commands
- Validate file paths

### 2. Path Traversal Prevention
- Validate paths are within workspace
- Use `Path.resolve()` to normalize
- Check for `..` sequences
- Verify file existence before operations

### 3. Input Validation
- Implement allowlist/denylist patterns
- Sanitize SQL/JSON/XML with libraries
- Validate data types and ranges
- Escape special characters

### 4. Resource Exhaustion
- Add timeouts to network operations
- Implement rate limiting
- Validate file sizes before reading
- Limit recursion depth

## Scan Checklist
- [ ] No command injection vulnerabilities
- [ ] No path traversal vulnerabilities
- [ ] All input properly validated
- [ ] Resource limits in place
- [ ] Error handling secure (no info leaks)
- [ ] Logging compliant (no sensitive data)

## Recommendations
(Analysis would go here based on code scan)

## AIOS Security Tools
For automated scanning, use:
- Static analysis: `pylint` for Python
- Dependency scanning: Check for known CVEs
- Runtime validation: Test with malicious inputs
"""
        return GetPromptResult(
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt_text)
                )
            ]
        )

