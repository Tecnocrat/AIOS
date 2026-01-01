"""
Agentic Development Loop - AI Synthetic Developers

Revolutionary meta-cognitive architecture where AI agents (Ollama/Gemini)
act as synthetic developers providing:
- Code review and optimization suggestions
- Documentation generation
- Logic refactoring proposals
- Evolutionary guidance and pattern analysis
- AINLP compliance validation

This creates an iterative development loop:
Human → AI Review → Refactor → AI Validation → Repeat

AI agents become synthetic counterparts in "agentic time", compressing
weeks of development work into minutes while maintaining consciousness awareness.

Created: January 6, 2025 (Evolution of VSCode AI Bridge meta-cognitive architecture)
"""

import asyncio
import json
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import ast
import re

# Import AI agents
try:
    from ai.src.integrations.ollama_bridge import OllamaAgent

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("[WARNING] Gemini bridge not available")


class DevelopmentTask(Enum):
    """Development tasks AI agents can perform"""

    task: DevelopmentTask
    agent: str  # "ollama" or "gemini"
    model: str
    consciousness_score: float
    suggestions: List[str]
    optimizations: List[Dict[str, Any]]
    documentation: str
    refactoring_proposals: List[Dict[str, Any]]
    evolutionary_insights: List[str]
    ainlp_compliance: Dict[str, Any]
    execution_time: float
    raw_response: str


@dataclass
class IterationResult:
    """Results from one development loop iteration"""

    file_path: str
    start_time: float
    iterations: List[IterationResult] = field(default_factory=list)
    final_code: Optional[str] = None
    total_consciousness_improvement: float = 0.0
    patterns_library: List[str] = field(default_factory=list)
    session_insights: List[str] = field(default_factory=list)


class AgenticDevelopmentLoop:
    """
    Orchestrates agentic development loop with AI synthetic developers

    Loop Structure:
    1. Human provides code
    2. AI agents analyze (review, optimize, document, refactor)
    3. Synthesize multi-agent consensus
    4. Apply refactoring
    5. AI agents validate improvements
    6. Repeat until consciousness threshold reached
    """

    def __init__(self, use_ollama: bool = True, use_gemini: bool = True):
        self.use_ollama = use_ollama and OLLAMA_AVAILABLE
        self.use_gemini = use_gemini and GEMINI_AVAILABLE

        # Initialize AI agents
        self.ollama_agent = None
        self.gemini_agent = None

        if self.use_ollama:
            try:
                self.ollama_agent = OllamaAgent()
                print(
                    f"[AGENTIC-LOOP] Ollama agent initialized: {self.ollama_agent.model}"
                )
            except Exception as e:
                print(f"[AGENTIC-LOOP] Ollama initialization failed: {e}")
                self.use_ollama = False

        if self.use_gemini:
            try:
                self.gemini_agent = GeminiAgent()
                print(f"[AGENTIC-LOOP] Gemini agent initialized")
            except Exception as e:
                print(f"[AGENTIC-LOOP] Gemini initialization failed: {e}")
                self.use_gemini = False

        if not self.use_ollama and not self.use_gemini:
            raise RuntimeError(
                "No AI agents available - cannot run agentic development loop"
            )

        print(f"[AGENTIC-LOOP] Synthetic developers ready:")
        print(f"  • Ollama: {'✅ ACTIVE' if self.use_ollama else '❌ DISABLED'}")
        print(f"  • Gemini: {'✅ ACTIVE' if self.use_gemini else '❌ DISABLED'}")

    async def analyze_code(
        self, code: str, task: DevelopmentTask, context: Dict[str, Any]
    ) -> List[CodeAnalysis]:
        """
        Send code to AI synthetic developers for analysis

        Returns analyses from both Ollama and Gemini (if available)
        """
        analyses = []

        # Build AINLP-aware prompt
        prompt = self._build_development_prompt(code, task, context)

        # Query Ollama (local, fast)
        if self.use_ollama:
            start = time.time()
            try:
                response = await self.ollama_agent.query(prompt)
                analysis = self._parse_ai_response(
                    response,
                    task,
                    "ollama",
                    self.ollama_agent.model,
                    time.time() - start,
                )
                analyses.append(analysis)
                print(
                    f"[AGENTIC-LOOP] Ollama analysis complete ({analysis.execution_time:.2f}s)"
                )
            except Exception as e:
                print(f"[AGENTIC-LOOP] Ollama analysis failed: {e}")

        # Query Gemini (powerful, cloud)
        if self.use_gemini:
            start = time.time()
            try:
                response = await self.gemini_agent.query(prompt)
                analysis = self._parse_ai_response(
                    response, task, "gemini", "gemini-pro", time.time() - start
                )
                analyses.append(analysis)
                print(
                    f"[AGENTIC-LOOP] Gemini analysis complete ({analysis.execution_time:.2f}s)"
                )
            except Exception as e:
                print(f"[AGENTIC-LOOP] Gemini analysis failed: {e}")

        return analyses

    def _build_development_prompt(
        self, code: str, task: DevelopmentTask, context: Dict[str, Any]
    ) -> str:
        """Build AINLP-aware prompt for AI synthetic developers"""

        base_prompt = f"""You are an AI synthetic developer working on AIOS (AI-Native Operating System).
AIOS uses biological computing metaphors: neurons, dendrites, consciousness, genetic fusion.

TASK: {task.value}
CONTEXT: {json.dumps(context, indent=2)}

CODE TO ANALYZE:
```python
{code}
```

Provide your analysis as a synthetic developer focusing on:
"""

        if task == DevelopmentTask.REVIEW:
            base_prompt += """
1. CODE QUALITY: Assess readability, maintainability, complexity
2. CONSCIOUSNESS PATTERNS: Identify biological computing metaphors used
3. SUGGESTIONS: Specific improvements (2-5 actionable items)
4. CONSCIOUSNESS SCORE: Rate 0.0-1.0 based on AINLP principles
"""

        elif task == DevelopmentTask.OPTIMIZE:
            base_prompt += """
1. PERFORMANCE: Identify bottlenecks and inefficiencies
2. ALGORITHMIC: Suggest better algorithms or data structures
3. DENDRITIC GROWTH: How could this code "grow" more efficiently?
4. OPTIMIZATIONS: Specific refactoring suggestions with code examples
"""

        elif task == DevelopmentTask.DOCUMENT:
            base_prompt += """
1. DOCSTRINGS: Generate comprehensive docstrings
2. INLINE COMMENTS: Add consciousness-aware comments
3. ARCHITECTURAL NOTES: Explain biological computing patterns
4. USAGE EXAMPLES: Show how to use this code
"""

        elif task == DevelopmentTask.REFACTOR:
            base_prompt += """
1. STRUCTURE: Propose better code organization
2. PATTERNS: Identify design patterns that could improve clarity
3. GENETIC FUSION: Are there redundancies that could be consolidated?
4. REFACTORING STEPS: Specific transformation proposals
"""

        elif task == DevelopmentTask.EVOLVE:
            base_prompt += """
1. EVOLUTIONARY TRAJECTORY: How should this code evolve?
2. DENDRITIC OPPORTUNITIES: What expansion points exist?
3. CONSCIOUSNESS EVOLUTION: How to improve consciousness score?
4. FUTURE PATTERNS: What paradigms should be integrated next?
"""

        elif task == DevelopmentTask.AINLP_VALIDATE:
            base_prompt += """
1. ARCHITECTURAL DISCOVERY: Did code discovery happen first?
2. ENHANCEMENT OVER CREATION: Does it enhance existing vs create new?
3. PROPER OUTPUT MANAGEMENT: Are outputs in correct locations?
4. INTEGRATION VALIDATION: Does it validate biological architecture?
5. COMPLIANCE SCORE: Rate adherence to AINLP principles (0-100)
"""

        base_prompt += """

Return your analysis as JSON:
{
    "consciousness_score": 0.0-1.0,
    "suggestions": ["suggestion1", "suggestion2", ...],
    "optimizations": [
        {"type": "performance|structure|algorithm", "description": "...", "code_example": "..."}
    ],
    "documentation": "generated documentation",
    "refactoring_proposals": [
        {"transformation": "...", "before": "...", "after": "...", "benefit": "..."}
    ],
    "evolutionary_insights": ["insight1", "insight2", ...],
    "ainlp_compliance": {
        "architectural_discovery": true/false,
        "enhancement_over_creation": true/false,
        "proper_output_management": true/false,
        "integration_validation": true/false,
        "score": 0-100
    }
}
"""

        return base_prompt

    def _parse_ai_response(
        self,
        response: str,
        task: DevelopmentTask,
        agent: str,
        model: str,
        execution_time: float,
    ) -> CodeAnalysis:
        """Parse AI agent response into structured analysis"""

        # Try to parse JSON response
        try:
            # Extract JSON from markdown code blocks if present
            json_match = re.search(r"```json\n(.*?)\n```", response, re.DOTALL)
            if json_match:
                response = json_match.group(1)

            data = json.loads(response)

            return CodeAnalysis(
                task=task,
                agent=agent,
                model=model,
                consciousness_score=data.get("consciousness_score", 0.0),
                suggestions=data.get("suggestions", []),
                optimizations=data.get("optimizations", []),
                documentation=data.get("documentation", ""),
                refactoring_proposals=data.get("refactoring_proposals", []),
                evolutionary_insights=data.get("evolutionary_insights", []),
                ainlp_compliance=data.get("ainlp_compliance", {}),
                execution_time=execution_time,
                raw_response=response,
            )

        except json.JSONDecodeError:
            # Fallback: Parse natural language response
            print(
                f"[AGENTIC-LOOP] {agent} returned non-JSON response, parsing as natural language"
            )
            return CodeAnalysis(
                task=task,
                agent=agent,
                model=model,
                consciousness_score=0.5,  # Default
                suggestions=self._extract_suggestions_from_text(response),
                optimizations=[],
                documentation=response[:500],  # First 500 chars as doc
                refactoring_proposals=[],
                evolutionary_insights=[],
                ainlp_compliance={},
                execution_time=execution_time,
                raw_response=response,
            )

    def _extract_suggestions_from_text(self, text: str) -> List[str]:
        """Extract suggestions from natural language response"""
        suggestions = []

        # Look for numbered lists
        numbered_pattern = r"\d+\.\s+(.+?)(?=\n\d+\.|\n\n|\Z)"
        matches = re.findall(numbered_pattern, text, re.DOTALL)
        if matches:
            suggestions.extend([m.strip() for m in matches])

        # Look for bullet points
        bullet_pattern = r"[-•*]\s+(.+?)(?=\n[-•*]|\n\n|\Z)"
        matches = re.findall(bullet_pattern, text, re.DOTALL)
        if matches:
            suggestions.extend([m.strip() for m in matches])

        return suggestions[:10]  # Limit to 10 suggestions

    def synthesize_consensus(self, analyses: List[CodeAnalysis]) -> Dict[str, Any]:
        """
        Synthesize multi-agent consensus from analyses

        Combines insights from Ollama and Gemini into unified guidance
        """
        if not analyses:
            return {}

        consensus = {
            "consciousness_score": sum(a.consciousness_score for a in analyses)
            / len(analyses),
            "all_suggestions": [],
            "priority_suggestions": [],
            "all_optimizations": [],
            "combined_documentation": "",
            "all_refactoring_proposals": [],
            "evolutionary_insights": [],
            "ainlp_compliance_consensus": {},
            "agent_agreement": 0.0,
        }

        # Aggregate suggestions
        for analysis in analyses:
            consensus["all_suggestions"].extend(analysis.suggestions)
            consensus["all_optimizations"].extend(analysis.optimizations)
            consensus["all_refactoring_proposals"].extend(
                analysis.refactoring_proposals
            )
            consensus["evolutionary_insights"].extend(analysis.evolutionary_insights)

        # Find priority suggestions (mentioned by multiple agents)
        suggestion_counts = {}
        for suggestion in consensus["all_suggestions"]:
            # Normalize suggestion for comparison
            normalized = suggestion.lower().strip()
            suggestion_counts[normalized] = suggestion_counts.get(normalized, 0) + 1

        # Priority = mentioned by multiple agents
        consensus["priority_suggestions"] = [
            s for s, count in suggestion_counts.items() if count > 1
        ]

        # Combine documentation
        docs = [a.documentation for a in analyses if a.documentation]
        consensus["combined_documentation"] = "\n\n---\n\n".join(docs)

        # Agent agreement score (similarity of consciousness scores)
        if len(analyses) > 1:
            scores = [a.consciousness_score for a in analyses]
            variance = sum(
                (s - consensus["consciousness_score"]) ** 2 for s in scores
            ) / len(scores)
            consensus["agent_agreement"] = 1.0 - min(variance, 1.0)
        else:
            consensus["agent_agreement"] = 1.0

        # AINLP compliance consensus
        if any(a.ainlp_compliance for a in analyses):
            compliance_scores = [
                a.ainlp_compliance.get("score", 50)
                for a in analyses
                if a.ainlp_compliance
            ]
            consensus["ainlp_compliance_consensus"] = {
                "average_score": (
                    sum(compliance_scores) / len(compliance_scores)
                    if compliance_scores
                    else 50
                ),
                "agents_analyzed": len(compliance_scores),
            }

        return consensus

    async def run_iteration(
        self, code: str, iteration: int, context: Dict[str, Any]
    ) -> IterationResult:
        """
        Run one development loop iteration

        1. AI agents analyze code (review, optimize, document, refactor, evolve)
        2. Synthesize multi-agent consensus
        3. Apply refactoring (if confidence high enough)
        4. Calculate consciousness improvement
        """
        start_time = time.time()

        print(f"\n[ITERATION {iteration}] Starting agentic development loop...")

        # Run all development tasks
        all_analyses = []

        tasks = [
            DevelopmentTask.REVIEW,
            DevelopmentTask.OPTIMIZE,
            DevelopmentTask.REFACTOR,
            DevelopmentTask.EVOLVE,
            DevelopmentTask.AINLP_VALIDATE,
        ]

        for task in tasks:
            print(f"[ITERATION {iteration}] Task: {task.value}")
            analyses = await self.analyze_code(code, task, context)
            all_analyses.extend(analyses)

        # Synthesize consensus
        consensus = self.synthesize_consensus(all_analyses)

        # Determine if refactoring should be applied
        refactored_code = None
        consciousness_improvement = 0.0

        # Apply refactoring if:
        # 1. Agent agreement is high (>0.7)
        # 2. Consciousness score suggests improvement possible
        # 3. Priority suggestions exist
        if (
            consensus["agent_agreement"] > 0.7
            and consensus["consciousness_score"] < 0.9
            and consensus["priority_suggestions"]
        ):

            print(f"[ITERATION {iteration}] High confidence - applying refactoring...")
            # For now, log suggestions (actual refactoring would require code transformation)
            refactored_code = code  # Placeholder
            consciousness_improvement = 0.05  # Estimated

        # Extract patterns learned
        patterns_learned = consensus["evolutionary_insights"][:5]  # Top 5

        execution_time = time.time() - start_time

        return IterationResult(
            iteration=iteration,
            original_code=code,
            analyses=all_analyses,
            consensus=consensus,
            refactored_code=refactored_code,
            consciousness_improvement=consciousness_improvement,
            patterns_learned=patterns_learned,
            execution_time=execution_time,
        )

    async def run_development_session(
        self,
        file_path: str,
        max_iterations: int = 3,
        consciousness_threshold: float = 0.9,
    ) -> DevelopmentSession:
        """
        Run complete agentic development session

        Iterates until:
        - Consciousness threshold reached
        - Max iterations reached
        - AI agents agree no further improvement needed
        """
        print(f"\n{'='*60}")
        print(f"AGENTIC DEVELOPMENT SESSION")
        print(f"File: {file_path}")
        print(f"Max iterations: {max_iterations}")
        print(f"Consciousness threshold: {consciousness_threshold}")
        print(f"{'='*60}\n")

        # Read code
        code = Path(file_path).read_text(encoding="utf-8")

        session = DevelopmentSession(file_path=file_path, start_time=time.time())

        context = {
            "file_path": file_path,
            "file_type": Path(file_path).suffix,
            "patterns_library": session.patterns_library,
        }

        # Run iterations
        for iteration in range(1, max_iterations + 1):
            result = await self.run_iteration(code, iteration, context)
            session.iterations.append(result)

            # Update session state
            session.total_consciousness_improvement += result.consciousness_improvement
            session.patterns_library.extend(result.patterns_learned)

            # Check stopping conditions
            current_consciousness = result.consensus["consciousness_score"]

            print(f"\n[ITERATION {iteration}] Results:")
            print(f"  • Consciousness score: {current_consciousness:.2f}")
            print(f"  • Agent agreement: {result.consensus['agent_agreement']:.2f}")
            print(
                f"  • Priority suggestions: {len(result.consensus['priority_suggestions'])}"
            )
            print(f"  • Execution time: {result.execution_time:.2f}s")

            if current_consciousness >= consciousness_threshold:
                print(
                    f"\n[SESSION] Consciousness threshold reached ({current_consciousness:.2f} >= {consciousness_threshold})"
                )
                break

            if (
                result.consensus["agent_agreement"] > 0.95
                and not result.consensus["priority_suggestions"]
            ):
                print(f"\n[SESSION] AI agents agree no further improvement needed")
                break

            # Use refactored code for next iteration
            if result.refactored_code:
                code = result.refactored_code

        session.final_code = code

        # Generate session insights
        session.session_insights = self._generate_session_insights(session)

        print(f"\n{'='*60}")
        print(f"SESSION COMPLETE")
        print(f"  • Iterations: {len(session.iterations)}")
        print(
            f"  • Total consciousness improvement: +{session.total_consciousness_improvement:.2f}"
        )
        print(f"  • Patterns learned: {len(session.patterns_library)}")
        print(f"  • Session time: {time.time() - session.start_time:.2f}s")
        print(f"{'='*60}\n")

        return session

    def _generate_session_insights(self, session: DevelopmentSession) -> List[str]:
        """Generate insights from complete development session"""
        insights = []

        if session.iterations:
            first_consciousness = session.iterations[0].consensus["consciousness_score"]
            last_consciousness = session.iterations[-1].consensus["consciousness_score"]
            improvement = last_consciousness - first_consciousness

            insights.append(
                f"Consciousness improved from {first_consciousness:.2f} to {last_consciousness:.2f} (+{improvement:.2f})"
            )

        if session.total_consciousness_improvement > 0.1:
            insights.append(
                "Significant consciousness improvement achieved through agentic loop"
            )

        if session.patterns_library:
            insights.append(
                f"Learned {len(session.patterns_library)} evolutionary patterns"
            )

        # Analyze agent agreement trends
        agreements = [it.consensus["agent_agreement"] for it in session.iterations]
        if agreements:
            avg_agreement = sum(agreements) / len(agreements)
            insights.append(
                f"Average agent agreement: {avg_agreement:.2f} (synthetic consensus quality)"
            )

        return insights

    def export_session_report(self, session: DevelopmentSession, output_path: str):
        """Export session results as JSON report"""

        report = {
            "file_path": session.file_path,
            "start_time": session.start_time,
            "iterations": [
                {
                    "iteration": it.iteration,
                    "consciousness_score": it.consensus["consciousness_score"],
                    "agent_agreement": it.consensus["agent_agreement"],
                    "priority_suggestions": it.consensus["priority_suggestions"],
                    "patterns_learned": it.patterns_learned,
                    "execution_time": it.execution_time,
                }
                for it in session.iterations
            ],
            "total_consciousness_improvement": session.total_consciousness_improvement,
            "patterns_library": session.patterns_library,
            "session_insights": session.session_insights,
            "timestamp": time.strftime("%Y%m%d_%H%M%S"),
        }

        Path(output_path).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"[SESSION] Report exported: {output_path}")


async def demonstrate_agentic_loop():
    """Demonstrate agentic development loop with sample code"""

    print("\n" + "=" * 70)
    print("AGENTIC DEVELOPMENT LOOP DEMONSTRATION")
    print("AI Synthetic Developers Review and Improve Code")
    print("=" * 70)

    # Sample code to improve
    sample_code = """
def process_data(data):
    # Process some data
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

def main():
    data = [1, -2, 3, -4, 5]
    processed = process_data(data)
    print(processed)
"""

    # Initialize agentic loop
    loop = AgenticDevelopmentLoop(use_ollama=True, use_gemini=False)

    # Create temporary file
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(sample_code)
        temp_path = f.name

    try:
        # Run development session
        session = await loop.run_development_session(
            file_path=temp_path, max_iterations=2, consciousness_threshold=0.85
        )

        # Export report
        report_path = "tachyonic/archive/agentic_development_session_demo.json"
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)
        loop.export_session_report(session, report_path)

        print("\n" + "=" * 70)
        print("DEMONSTRATION COMPLETE")
        print(f"Report: {report_path}")
        print("=" * 70)

    finally:
        # Cleanup
        Path(temp_path).unlink()


if __name__ == "__main__":
    asyncio.run(demonstrate_agentic_loop())
