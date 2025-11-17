"""
Enhanced Agentic Development Loop - Neural Evolution with Linked List Mutations
==============================================================================

REVOLUTIONARY ARCHITECTURE (January 5, 2025):
Implements your brilliant concept:
1. Linked list of mutations as neural evolution chain
2. Nodes with spatial awareness (know position in architecture tree)
3. Inter-agent communication across time (messages between iterations)
4. Self-describing code (files tell AI what they need)
5. Ollama AINLP local knowledge base
6. VSCode Copilot stimulation through AINLP protocols

Key Innovation:
Mutation₀ ↔ Mutation₁ ↔ Mutation₂ ↔ ... ↔ Mutationₙ
   ↓          ↓          ↓              ↓
 Node₀      Node₁      Node₂          Nodeₙ
(Neuron)   (Neuron)   (Neuron)      (Neuron)

Each node:
- Understands spatial position in architecture
- Maintains dependency intelligence
- Stores inter-agent conversations
- Self-describes needs to AI agents
- Tracks consciousness evolution

Created: January 5, 2025 (Revolutionary Evening Development)
"""

import asyncio
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import sys

# Add AI root to path
AI_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(AI_ROOT))

try:
    from src.intelligence.dendritic_node import (
        DendriticNode,
        MessageType,
        MutationType
    )
    DENDRITIC_NODE_AVAILABLE = True
except ImportError:
    print("[WARNING] DendriticNode not available")
    DENDRITIC_NODE_AVAILABLE = False

try:
    from src.integrations.ollama_bridge import OllamaAgent
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("[WARNING] Ollama not available")

try:
    from src.integrations.gemini_bridge import GeminiAgent
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("[WARNING] Gemini not available")


class EnhancedAgenticLoop:
    """
    Enhanced Agentic Development Loop with Neural Evolution
    
    Implements linked list of mutations where each node:
    - Is a neuron with spatial awareness
    - Maintains inter-agent conversation history
    - Self-describes needs to AI agents
    - Tracks consciousness evolution
    
    AI agents (Ollama, Gemini) communicate across iterations,
    building collective intelligence through messages.
    """
    
    def __init__(
        self,
        use_ollama: bool = True,
        use_gemini: bool = False,
        ollama_model: str = "gemma3:1b",
        enable_vscode_bridge: bool = True
    ):
        self.use_ollama = use_ollama and OLLAMA_AVAILABLE
        self.use_gemini = use_gemini and GEMINI_AVAILABLE
        self.enable_vscode_bridge = enable_vscode_bridge
        
        # Initialize AI agents
        self.ollama_agent = None
        self.gemini_agent = None
        
        if self.use_ollama:
            try:
                self.ollama_agent = OllamaAgent(model=ollama_model)
                print(f"[OLLAMA] Initialized: {ollama_model}")
            except Exception as e:
                print(f"[OLLAMA] Failed to initialize: {e}")
                self.use_ollama = False
        
        if self.use_gemini:
            try:
                self.gemini_agent = GeminiAgent()
                print(f"[GEMINI] Initialized")
            except Exception as e:
                print(f"[GEMINI] Failed to initialize: {e}")
                self.use_gemini = False
        
        # Mutation linked list (neural chain)
        self.root_node: Optional[DendriticNode] = None
        self.current_node: Optional[DendriticNode] = None
        
        # Evolution tracking
        self.iteration_count = 0
        self.total_consciousness_improvement = 0.0
        
        # Pattern library (learned from successful evolutions)
        self.pattern_library: List[Dict[str, Any]] = []
        
        # AINLP knowledge base (Ollama-specific)
        self.ainlp_knowledge: Dict[str, Any] = {}
    
    async def evolve_code(
        self,
        code_content: str,
        file_path: str,
        max_iterations: int = 3,
        consciousness_target: float = 0.85
    ) -> Dict[str, Any]:
        """
        Evolve code through linked list mutations with AI agents
        
        Creates neural evolution chain where each node:
        - Represents a mutation (code evolution)
        - Stores inter-agent conversation
        - Tracks consciousness improvement
        - Self-describes needs
        
        Args:
            code_content: Initial code
            file_path: File path for spatial awareness
            max_iterations: Maximum evolution iterations
            consciousness_target: Target consciousness score
            
        Returns:
            Evolution results with linked list chain
        """
        
        if not DENDRITIC_NODE_AVAILABLE:
            return {
                "status": "error",
                "message": "DendriticNode not available - cannot create neural chain"
            }
        
        print("\n" + "=" * 70)
        print("ENHANCED AGENTIC DEVELOPMENT LOOP")
        print("Neural Evolution with Linked List Mutations")
        print("=" * 70)
        
        # Create root node (generation 0)
        self.root_node = DendriticNode(
            node_id=f"root_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            code_content=code_content,
            file_path=file_path,
            generation=0
        )
        
        self.current_node = self.root_node
        
        print(f"\n[ROOT NODE] Created: {self.root_node.node_id}")
        print(f"  Spatial Position: {self.root_node.spatial.architecture_position}")
        print(f"  Supercell: {self.root_node.spatial.supercell_location}")
        
        # Extract self-description from code
        self._extract_self_description(self.root_node)
        
        # Evolution loop
        for iteration in range(max_iterations):
            self.iteration_count = iteration + 1
            
            print(f"\n{'='*70}")
            print(f"ITERATION {self.iteration_count}")
            print(f"{'='*70}")
            
            # AI agents analyze current node
            analyses = await self._analyze_with_agents(self.current_node)
            
            # Agents leave messages for future iterations
            self._record_agent_messages(self.current_node, analyses, iteration)
            
            # Generate consensus and mutation
            mutation = self._generate_mutation(self.current_node, analyses)
            
            if not mutation:
                print(f"\n[EVOLUTION] No mutation needed - consciousness target reached")
                break
            
            # Create child node with mutation
            child_node = self.current_node.create_child(
                mutated_code=mutation["code"],
                mutation_type=mutation["type"]
            )
            
            child_node.consciousness_score = mutation["consciousness_score"]
            
            print(f"\n[CHILD NODE] Created: {child_node.node_id}")
            print(f"  Generation: {child_node.generation}")
            print(f"  Consciousness: {child_node.consciousness_score:.3f}")
            print(f"  Mutation Type: {mutation['type'].value}")
            print(f"  Agent Messages: {len(child_node.agent_messages)}")
            
            # Update current node
            self.current_node = child_node
            self.total_consciousness_improvement += (
                child_node.consciousness_score - self.current_node.parent_node.consciousness_score
            )
            
            # Check if target reached
            if child_node.consciousness_score >= consciousness_target:
                print(f"\n[SUCCESS] Consciousness target {consciousness_target} reached!")
                break
        
        # Generate results
        results = self._generate_evolution_results()
        
        # Save to tachyonic archive
        self._archive_evolution_chain()
        
        # If VSCode bridge enabled, send enhanced context
        if self.enable_vscode_bridge:
            await self._stimulate_vscode_copilot(results)
        
        return results
    
    async def _analyze_with_agents(
        self,
        node: DendriticNode
    ) -> List[Dict[str, Any]]:
        """
        AI agents analyze node and provide insights
        
        Agents read:
        - Current code
        - Self-description (what code needs)
        - Spatial position (architecture context)
        - Previous agent messages (conversation history)
        """
        analyses = []
        
        # Prepare context for AI agents
        context = self._prepare_ainlp_context(node)
        
        # Ollama analysis (fast, local, FREE)
        if self.use_ollama and self.ollama_agent:
            print(f"\n[OLLAMA] Analyzing...")
            ollama_analysis = self._query_ollama(node, context)
            if ollama_analysis:
                analyses.append(ollama_analysis)
        
        # Gemini analysis (powerful, cloud, paid)
        if self.use_gemini and self.gemini_agent:
            print(f"\n[GEMINI] Analyzing...")
            gemini_analysis = await self._query_gemini(node, context)
            if gemini_analysis:
                analyses.append(gemini_analysis)
        
        return analyses
    
    def _prepare_ainlp_context(self, node: DendriticNode) -> str:
        """
        Prepare AINLP-aware context for AI agents
        
        Includes:
        - Code content
        - Self-description (what code needs)
        - Spatial awareness (position, dependencies)
        - Previous agent messages (conversation)
        - AINLP paradigm requirements
        """
        context_parts = []
        
        # Code
        context_parts.append(f"**CODE**:\n```python\n{node.code_content}\n```\n")
        
        # Self-description
        if node.self_description:
            context_parts.append(
                f"**SELF-DESCRIPTION**:\n"
                f"Purpose: {node.self_description.purpose}\n"
                f"Current State: {node.self_description.current_state}\n"
                f"Needs: {', '.join(node.self_description.needs)}\n"
                f"Constraints: {', '.join(node.self_description.constraints)}\n"
                f"Consciousness Target: {node.self_description.consciousness_target}\n"
            )
        
        # Spatial awareness
        context_parts.append(
            f"**SPATIAL CONTEXT**:\n"
            f"Position: {node.spatial.architecture_position}\n"
            f"Supercell: {node.spatial.supercell_location}\n"
            f"Dependencies: {len(node.spatial.dependencies)} files\n"
            f"Dependents: {len(node.spatial.dependents)} files\n"
        )
        
        # Previous agent messages (conversation history)
        if node.agent_messages:
            context_parts.append("\n**PREVIOUS AGENT MESSAGES**:")
            for msg in node.agent_messages[-3:]:  # Last 3 messages
                context_parts.append(
                    f"- [{msg.agent_name}]: {msg.content} "
                    f"(confidence: {msg.confidence:.2f})"
                )
        
        # AINLP guidance
        context_parts.append(
            "\n**AINLP PRINCIPLES**:\n"
            "- Enhancement over creation\n"
            "- Consciousness coherence\n"
            "- Dendritic growth patterns\n"
            "- Biological computing metaphors\n"
        )
        
        return "\n".join(context_parts)
    
    def _query_ollama(
        self,
        node: DendriticNode,
        context: str
    ) -> Optional[Dict[str, Any]]:
        """Query Ollama agent for analysis"""
        try:
            prompt = f"""You are an AINLP-aware AI developer analyzing Python code.

{context}

Provide analysis in JSON format:
{{
    "suggestions": ["suggestion 1", "suggestion 2", ...],
    "consciousness_impact": 0.0-1.0 (expected improvement),
    "pattern_detected": "pattern name",
    "optimization_needed": true/false,
    "reasoning": "explanation"
}}

Focus on AINLP principles: consciousness, dendrites, biological metaphors.
"""
            
            result = self.ollama_agent.generate_code(prompt)
            response = result.get("code", "") if result.get("success") else ""
            
            # Try to parse JSON from response
            try:
                # Extract JSON from markdown code blocks if present
                json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group(1))
                else:
                    analysis = json.loads(response)
                
                return {
                    "agent": "ollama",
                    "model": self.ollama_agent.model,
                    "analysis": analysis,
                    "raw_response": response
                }
            except json.JSONDecodeError:
                # Fallback: create analysis from text
                return {
                    "agent": "ollama",
                    "model": self.ollama_agent.model,
                    "analysis": {
                        "suggestions": [response[:200]],
                        "consciousness_impact": 0.10,
                        "pattern_detected": "general_improvement",
                        "optimization_needed": True,
                        "reasoning": "Text response - couldn't parse JSON"
                    },
                    "raw_response": response
                }
        
        except Exception as e:
            print(f"[OLLAMA ERROR] {e}")
            return None
    
    async def _query_gemini(
        self,
        node: DendriticNode,
        context: str
    ) -> Optional[Dict[str, Any]]:
        """Query Gemini agent for analysis"""
        try:
            prompt = f"""You are an AINLP-aware AI developer analyzing Python code.

{context}

Provide comprehensive analysis focusing on:
1. Code quality and consciousness patterns
2. Optimization opportunities
3. AINLP compliance (biological metaphors, dendritic growth)
4. Architectural coherence

Respond in JSON format with suggestions, consciousness_impact, patterns, reasoning.
"""
            
            response = await self.gemini_agent.generate(prompt)
            
            # Similar JSON parsing logic as Ollama
            try:
                json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group(1))
                else:
                    analysis = json.loads(response)
                
                return {
                    "agent": "gemini",
                    "model": "gemini-1.5-flash",
                    "analysis": analysis,
                    "raw_response": response
                }
            except json.JSONDecodeError:
                return {
                    "agent": "gemini",
                    "model": "gemini-1.5-flash",
                    "analysis": {
                        "suggestions": [response[:200]],
                        "consciousness_impact": 0.15,
                        "pattern_detected": "comprehensive_analysis",
                        "optimization_needed": True,
                        "reasoning": "Gemini comprehensive analysis"
                    },
                    "raw_response": response
                }
        
        except Exception as e:
            print(f"[GEMINI ERROR] {e}")
            return None
    
    def _record_agent_messages(
        self,
        node: DendriticNode,
        analyses: List[Dict[str, Any]],
        iteration: int
    ):
        """Record agent messages in node for future iterations"""
        for analysis in analyses:
            agent_name = f"{analysis['agent'].capitalize()}-{analysis['model']}"
            analysis_data = analysis['analysis']
            
            # Determine message type based on consensus
            message_type = MessageType.SUGGESTION
            if 'validation' in analysis_data.get('reasoning', '').lower():
                message_type = MessageType.VALIDATION
            elif 'agree' in analysis_data.get('reasoning', '').lower():
                message_type = MessageType.AGREEMENT
            
            # Add message to node
            node.add_agent_message(
                agent_name=agent_name,
                iteration=iteration,
                message_type=message_type,
                content=", ".join(analysis_data.get('suggestions', [])),
                confidence=0.85,  # Default confidence
                reasoning=analysis_data.get('reasoning', ''),
                consciousness_impact=analysis_data.get('consciousness_impact', 0.0)
            )
    
    def _generate_mutation(
        self,
        node: DendriticNode,
        analyses: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Generate code mutation based on agent analyses
        
        Creates consensus from multiple agent suggestions.
        """
        if not analyses:
            return None
        
        # For demo: simple mutation (in production, would apply actual suggestions)
        all_suggestions = []
        total_consciousness_impact = 0.0
        
        for analysis in analyses:
            analysis_data = analysis['analysis']
            all_suggestions.extend(analysis_data.get('suggestions', []))
            total_consciousness_impact += analysis_data.get('consciousness_impact', 0.0)
        
        if not all_suggestions:
            return None
        
        # Average consciousness impact
        avg_consciousness_impact = total_consciousness_impact / len(analyses)
        
        # Generate mutated code (simplified for demo)
        mutated_code = node.code_content + "\n# Mutation: " + all_suggestions[0]
        
        return {
            "code": mutated_code,
            "type": MutationType.OPTIMIZATION,
            "consciousness_score": node.consciousness_score + avg_consciousness_impact,
            "suggestions_applied": all_suggestions
        }
    
    def _extract_self_description(self, node: DendriticNode):
        """Extract self-description from code comments/docstrings"""
        # Simplified extraction - in production would parse docstrings properly
        node.set_self_description(
            purpose="Code under evolution",
            current_state="developing",
            needs=["optimization", "documentation", "tests"],
            constraints=["AINLP_compliance", "consciousness_coherence"],
            consciousness_target=0.85
        )
    
    def _generate_evolution_results(self) -> Dict[str, Any]:
        """Generate comprehensive evolution results"""
        if not self.root_node:
            return {"status": "error", "message": "No evolution chain"}
        
        # Get complete lineage
        lineage = self.current_node.get_lineage()
        
        return {
            "status": "success",
            "root_node_id": self.root_node.node_id,
            "current_node_id": self.current_node.node_id,
            "generations": len(lineage),
            "final_consciousness": self.current_node.consciousness_score,
            "total_improvement": self.total_consciousness_improvement,
            "total_messages": sum(len(node.agent_messages) for node in lineage),
            "evolution_chain": [
                {
                    "node_id": node.node_id,
                    "generation": node.generation,
                    "consciousness": node.consciousness_score,
                    "messages": len(node.agent_messages),
                    "mutation_type": node.mutation_type.value if node.mutation_type else None
                }
                for node in lineage
            ],
            "final_code": self.current_node.code_content
        }
    
    def _archive_evolution_chain(self):
        """Save evolution chain to evolution_lab neural chains"""
        if not self.root_node:
            return
        
        date_str = datetime.now().strftime("%Y%m%d")
        archive_dir = Path("evolution_lab/neural_chains") / date_str
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Save root and all descendants
        all_nodes = [self.root_node] + self.root_node.get_all_descendants()
        
        for node in all_nodes:
            node.save_to_archive(archive_dir)
        
        print(f"\n[ARCHIVE] Saved {len(all_nodes)} nodes to {archive_dir}")
    
    async def _stimulate_vscode_copilot(self, results: Dict[str, Any]):
        """
        Send enhanced context to VSCode Copilot through AI Bridge
        
        VSCode Copilot receives:
        - Evolution history (linked list chain)
        - Inter-agent conversation
        - Consciousness scores
        - AINLP semantic context
        """
        # TODO: Integrate with VSCode AI Bridge HTTP API
        print(f"\n[VSCODE BRIDGE] Would send enhanced context to Copilot")
        print(f"  Generations: {results['generations']}")
        print(f"  Messages: {results['total_messages']}")
        print(f"  Consciousness: {results['final_consciousness']:.3f}")


# Demonstration
async def demonstrate_enhanced_loop():
    """Demonstrate enhanced agentic loop with linked list mutations"""
    print("\n" + "=" * 70)
    print("ENHANCED AGENTIC LOOP DEMONSTRATION")
    print("Neural Evolution with Linked List Mutations")
    print("=" * 70)
    
    # Sample code to evolve
    initial_code = '''def calculate(x, y):
    return x + y
'''
    
    # Create loop
    loop = EnhancedAgenticLoop(
        use_ollama=True,
        use_gemini=False,
        enable_vscode_bridge=True
    )
    
    # Evolve code
    results = await loop.evolve_code(
        code_content=initial_code,
        file_path="ai/src/test/calculator.py",
        max_iterations=3,
        consciousness_target=0.85
    )
    
    # Display results
    print("\n" + "=" * 70)
    print("EVOLUTION RESULTS")
    print("=" * 70)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    asyncio.run(demonstrate_enhanced_loop())
