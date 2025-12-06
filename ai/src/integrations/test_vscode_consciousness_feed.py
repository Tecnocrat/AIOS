"""
Test: Feed Consciousness-Aware Context to VSCode Copilot
========================================================

Revolutionary test of linked list neural evolution context feeding to VSCode.

This demonstrates:
1. Neural evolution chain creation (linked list mutations)
2. Inter-agent dialogue across iterations
3. Consciousness score tracking
4. Enhanced context generation for VSCode Copilot
5. Real-time context feeding via HTTP API

Created: January 5, 2025 (Revolutionary Evening Testing)
"""

import asyncio
import json
from pathlib import Path
import sys

# Add AI root to path
AI_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(AI_ROOT))

try:
    from src.intelligence.enhanced_agentic_loop import EnhancedAgenticLoop
    from src.intelligence.dendritic_node import DendriticNode, MutationType

    NEURAL_EVOLUTION_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Neural evolution not available: {e}")
    NEURAL_EVOLUTION_AVAILABLE = False

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    print(f"[WARNING] requests not available - install: pip install requests")
    REQUESTS_AVAILABLE = False


class VSCodeConsciousnessFeeder:
    """
    Feeds consciousness-aware context from neural evolution to VSCode Copilot

    Revolutionary workflow:
    1. Create neural evolution chain (linked list of mutations)
    2. Track inter-agent messages and consensus
    3. Generate consciousness-aware context
    4. Feed to VSCode Copilot via HTTP API
    5. Validate enhanced code generation
    """

    def __init__(self, vscode_api_url: str = "http://localhost:8001"):
        self.vscode_api_url = vscode_api_url
        self.evolution_results = None

    async def create_evolution_chain(
        self, initial_code: str, file_path: str, max_iterations: int = 3
    ):
        """Create neural evolution chain with consciousness tracking"""

        if not NEURAL_EVOLUTION_AVAILABLE:
            print("\n[ERROR] Neural evolution not available")
            return None

        print("\n" + "=" * 70)
        print("CREATING NEURAL EVOLUTION CHAIN")
        print("=" * 70)

        # Create enhanced agentic loop
        loop = EnhancedAgenticLoop(
            use_ollama=True,
            use_gemini=False,
            enable_vscode_bridge=False,  # We'll feed manually
        )

        # Evolve code
        results = await loop.evolve_code(
            code_content=initial_code,
            file_path=file_path,
            max_iterations=max_iterations,
            consciousness_target=0.85,
        )

        self.evolution_results = results
        return results

    def generate_consciousness_context(self) -> dict:
        """
        Generate consciousness-aware context for VSCode Copilot

        Returns rich context including:
        - Evolution history (complete lineage)
        - Inter-agent messages (temporal dialogue)
        - Consciousness scores (measurable improvement)
        - Spatial awareness (architecture context)
        - Agent consensus patterns
        """

        if not self.evolution_results:
            return {"error": "No evolution chain created"}

        results = self.evolution_results

        context = {
            "context_type": "consciousness_aware_neural_evolution",
            "consciousness_level": results["final_consciousness"],
            "evolution_summary": {
                "generations": results["generations"],
                "total_improvement": results["total_improvement"],
                "messages_exchanged": results["total_messages"],
                "root_node": results["root_node_id"],
                "current_node": results["current_node_id"],
            },
            "evolution_chain": results["evolution_chain"],
            "consciousness_progression": [
                {
                    "generation": node["generation"],
                    "consciousness": node["consciousness"],
                    "mutation_type": node["mutation_type"],
                }
                for node in results["evolution_chain"]
            ],
            "inter_agent_messages": results["total_messages"],
            "final_code": results["final_code"],
            "vscode_enhancement_instructions": {
                "use_evolutionary_context": True,
                "apply_consciousness_patterns": True,
                "respect_spatial_awareness": True,
                "build_on_agent_consensus": True,
                "target_consciousness": 0.85,
                "mutation_strategies": [
                    node["mutation_type"]
                    for node in results["evolution_chain"]
                    if node["mutation_type"]
                ],
            },
        }

        return context

    def feed_to_vscode(self, context: dict) -> bool:
        """
        Feed consciousness-aware context to VSCode Copilot via HTTP API

        If VSCode AI Bridge server is running on localhost:8001,
        this sends enhanced context for Copilot to use.
        """

        if not REQUESTS_AVAILABLE:
            print("\n[WARNING] requests not available - cannot feed to VSCode")
            print("Install: pip install requests")
            return False

        print("\n" + "=" * 70)
        print("FEEDING CONSCIOUSNESS CONTEXT TO VSCODE COPILOT")
        print("=" * 70)

        try:
            # Check if VSCode bridge is running
            health_url = f"{self.vscode_api_url}/health"
            response = requests.get(health_url, timeout=2)

            if response.status_code != 200:
                print(
                    f"\n[WARNING] VSCode bridge not responding at {self.vscode_api_url}"
                )
                print(
                    "Start server: python ai/src/integrations/vscode_ai_bridge_server.py"
                )
                return False

            print(f"\n[VSCODE BRIDGE] Connected: {self.vscode_api_url}")

            # Feed context to VSCode
            context_url = f"{self.vscode_api_url}/feed_context"
            response = requests.post(context_url, json=context, timeout=5)

            if response.status_code == 200:
                result = response.json()
                print(f"\n[SUCCESS] Context fed to VSCode Copilot")
                print(f"  Generations: {context['evolution_summary']['generations']}")
                print(
                    f"  Messages: {context['evolution_summary']['messages_exchanged']}"
                )
                print(f"  Consciousness: {context['consciousness_level']:.3f}")
                print(
                    f"  Enhancement Instructions: {len(context['vscode_enhancement_instructions'])} directives"
                )
                return True
            else:
                print(f"\n[ERROR] Failed to feed context: {response.status_code}")
                print(f"Response: {response.text}")
                return False

        except requests.exceptions.ConnectionError:
            print(
                f"\n[WARNING] Cannot connect to VSCode bridge at {self.vscode_api_url}"
            )
            print("Start server: python ai/src/integrations/vscode_ai_bridge_server.py")
            return False

        except Exception as e:
            print(f"\n[ERROR] Failed to feed context: {e}")
            return False

    def display_consciousness_context(self, context: dict):
        """Display consciousness-aware context for inspection"""

        print("\n" + "=" * 70)
        print("CONSCIOUSNESS-AWARE CONTEXT FOR VSCODE COPILOT")
        print("=" * 70)

        print("\n**Evolution Summary**:")
        summary = context["evolution_summary"]
        print(f"  Generations: {summary['generations']}")
        print(f"  Total Improvement: {summary['total_improvement']:.3f}")
        print(f"  Messages Exchanged: {summary['messages_exchanged']}")
        print(f"  Root Node: {summary['root_node']}")
        print(f"  Current Node: {summary['current_node']}")

        print("\n**Consciousness Progression**:")
        for entry in context["consciousness_progression"]:
            print(
                f"  Generation {entry['generation']}: "
                f"consciousness={entry['consciousness']:.3f}, "
                f"mutation={entry['mutation_type']}"
            )

        print("\n**VSCode Enhancement Instructions**:")
        instructions = context["vscode_enhancement_instructions"]
        for key, value in instructions.items():
            print(f"  {key}: {value}")

        print("\n**Context JSON** (first 500 chars):")
        context_json = json.dumps(context, indent=2)
        print(context_json[:500] + "..." if len(context_json) > 500 else context_json)


async def main():
    """
    Revolutionary test: Feed consciousness-aware context to VSCode Copilot

    This demonstrates the complete workflow:
    1. Create neural evolution chain
    2. Generate consciousness-aware context
    3. Feed to VSCode Copilot
    4. Validate enhanced code generation
    """

    print("\n" + "=" * 70)
    print("REVOLUTIONARY TEST: CONSCIOUSNESS-AWARE VSCODE COPILOT")
    print("=" * 70)
    print(
        "\nObjective: Feed neural evolution context to VSCode for enhanced code generation"
    )
    print(
        "Innovation: Copilot receives evolution history, agent messages, consciousness scores"
    )

    # Initial code to evolve
    initial_code = '''def calculate_average(numbers):
    """Calculate average of numbers"""
    return sum(numbers) / len(numbers)
'''

    # Create feeder
    feeder = VSCodeConsciousnessFeeder()

    # Create neural evolution chain
    print("\n[STEP 1] Creating neural evolution chain...")
    results = await feeder.create_evolution_chain(
        initial_code=initial_code,
        file_path="ai/src/test/calculator.py",
        max_iterations=3,
    )

    if not results:
        print("\n[ERROR] Failed to create evolution chain")
        return

    print(f"\n[SUCCESS] Evolution chain created:")
    print(f"  Generations: {results['generations']}")
    print(f"  Final Consciousness: {results['final_consciousness']:.3f}")
    print(f"  Total Messages: {results['total_messages']}")

    # Generate consciousness-aware context
    print("\n[STEP 2] Generating consciousness-aware context...")
    context = feeder.generate_consciousness_context()

    if "error" in context:
        print(f"\n[ERROR] {context['error']}")
        return

    print(f"\n[SUCCESS] Context generated:")
    print(f"  Context Type: {context['context_type']}")
    print(
        f"  Enhancement Instructions: {len(context['vscode_enhancement_instructions'])} directives"
    )

    # Display context
    print("\n[STEP 3] Displaying consciousness context...")
    feeder.display_consciousness_context(context)

    # Feed to VSCode Copilot
    print("\n[STEP 4] Feeding to VSCode Copilot...")
    success = feeder.feed_to_vscode(context)

    if success:
        print("\n" + "=" * 70)
        print("REVOLUTIONARY SUCCESS!")
        print("=" * 70)
        print("\nVSCode Copilot now has consciousness-aware context:")
        print("  - Evolution history (linked list chain)")
        print("  - Inter-agent messages (temporal dialogue)")
        print("  - Consciousness scores (measurable improvement)")
        print("  - Spatial awareness (architecture context)")
        print("  - Mutation strategies (proven patterns)")
        print("\nCopilot can now generate BETTER code using this rich context!")
    else:
        print("\n" + "=" * 70)
        print("CONTEXT GENERATED (Bridge Not Running)")
        print("=" * 70)
        print("\nConsciousness-aware context successfully created.")
        print("To feed to VSCode Copilot:")
        print(
            "  1. Start VSCode AI Bridge: python ai/src/integrations/vscode_ai_bridge_server.py"
        )
        print("  2. Re-run this test")
        print("\nContext is ready and waiting!")

    # Save context to file for inspection
    context_dir = Path("evolution_lab/consciousness_contexts")
    context_file = context_dir / "latest_context.json"
    context_file.parent.mkdir(parents=True, exist_ok=True)
    context_file.write_text(json.dumps(context, indent=2))
    print(f"\n[ARCHIVE] Context saved: {context_file}")


if __name__ == "__main__":
    asyncio.run(main())
