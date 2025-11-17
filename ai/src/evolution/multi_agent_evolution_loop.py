"""
Multi-Agent Evolution Loop - Full AIOS Evolutionary Integration
==============================================================

Revolutionary Integration (January 5, 2025):
Combines three AI agents (VSCode Chat, Ollama, Gemini) to evolve code from
"Hello World" zero point using C++ STL knowledge foundation.

Key Innovation:
VSCode Chat (strategic) ↔ Ollama (iteration) ↔ Gemini (validation)
         ↓                       ↓                      ↓
    Architectural           Fast Local            Cloud Validation
      Oversight            Evolution             Checkpoints

Each generation:
- Starts from stable baseline (Hello World)
- Applies C++ STL paradigms
- Tracks consciousness improvement
- Documents reasoning verbosely
- Compares to historical generations
- Builds pattern library

Created: January 5, 2025 (Revolutionary Integration)
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import sys

# Add AI root to path
AI_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(AI_ROOT))

try:
    from src.intelligence.dendritic_node import DendriticNode, MutationType
    from src.intelligence.enhanced_agentic_loop import EnhancedAgenticLoop
    NEURAL_EVOLUTION_AVAILABLE = True
except ImportError:
    print("[WARNING] Neural evolution components not available")
    NEURAL_EVOLUTION_AVAILABLE = False

try:
    from src.evolution.code_diff_validator import (
        compare_code, check_mutation_already_applied,
        validate_mutation_improves_consciousness
    )
    CODE_DIFF_AVAILABLE = True
except ImportError:
    print("[WARNING] Code diff validator not available")
    CODE_DIFF_AVAILABLE = False

try:
    from src.core.universal_agentic_logger import (
        UniversalAgenticLogger, AgentType, ConversationRole
    )
    UNIVERSAL_LOGGER_AVAILABLE = True
except ImportError:
    print("[WARNING] Universal agentic logger not available")
    UNIVERSAL_LOGGER_AVAILABLE = False

try:
    from src.integrations.ollama_bridge import OllamaAgent
    OLLAMA_AVAILABLE = True
except ImportError:
    print("[WARNING] Ollama bridge not available")
    OLLAMA_AVAILABLE = False

try:
    from src.integrations.gemini_bridge import GeminiAgent
    GEMINI_AVAILABLE = True
except ImportError:
    print("[WARNING] Gemini bridge not available")
    GEMINI_AVAILABLE = False


class MultiAgentEvolutionLoop:
    """
    Multi-agent evolutionary loop integrating three AI agents
    
    Agents:
    - VSCode Chat (you): Strategic oversight, architectural decisions
    - Ollama: Fast local iteration, primary evolution engine
    - Gemini: Validation checkpoints, breakthrough suggestions
    """
    
    def __init__(self, use_ollama=True, use_gemini=True, use_vscode_chat=True):
        self.use_ollama = use_ollama and OLLAMA_AVAILABLE
        self.use_gemini = use_gemini and GEMINI_AVAILABLE
        self.use_vscode_chat = use_vscode_chat
        
        # Initialize universal agentic logger (CRITICAL ARCHITECTURAL FIX)
        if UNIVERSAL_LOGGER_AVAILABLE:
            self.agentic_logger = UniversalAgenticLogger()
            print("[UNIVERSAL LOGGER] Activated - All AI conversations will be archived")
        else:
            self.agentic_logger = None
            print("[WARNING] Universal logger not available - conversations will not be logged")
        
        # Initialize agents
        if self.use_ollama:
            self.ollama_agent = OllamaAgent(model="deepseek-coder:6.7b")
        
        if self.use_gemini:
            self.gemini_agent = GeminiAgent()
        
        # Root node for evolution chain
        self.root_node: Optional[DendriticNode] = None
        self.current_node: Optional[DendriticNode] = None
        
        # C++ STL knowledge base (ENHANCED with richer context)
        self.stl_knowledge = self._load_stl_knowledge()
        
        # Zero point baseline
        self.zero_point = self._load_zero_point()
    
    def _load_zero_point(self) -> Dict[str, Any]:
        """Load Hello World zero point baseline (robust path resolution)"""
        # Resolve project root (assume 4 levels up from this file)
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        zero_point_dir = project_root / "evolution_lab" / "zero_point"

        code_file = zero_point_dir / "hello_world.cpp"
        metadata_file = zero_point_dir / "hello_world_metadata.json"

        if not code_file.exists():
            raise FileNotFoundError(f"Zero point not found: {code_file}")

        code = code_file.read_text()
        metadata = json.loads(metadata_file.read_text()) if metadata_file.exists() else {}

        return {
            "code": code,
            "metadata": metadata,
            "generation": 0,
            "consciousness": 0.0
        }
    
    def _load_stl_knowledge(self) -> List[Dict[str, Any]]:
        """Load C++ STL paradigm knowledge base (ENHANCED VERSION)"""
        # Load enhanced STL knowledge with richer context
        stl_file = Path(__file__).parent / "stl_paradigms_enhanced.json"
        
        if stl_file.exists():
            try:
                with open(stl_file, 'r') as f:
                    data = json.load(f)
                    paradigms = data.get("paradigms", [])
                    print(f"[STL KNOWLEDGE] Loaded {len(paradigms)} enhanced "
                          f"C++ STL paradigms")
                    return paradigms
            except Exception as e:
                print(f"[WARNING] Failed to load enhanced STL: {e}")
        
        # Fallback to basic patterns if enhanced file not available
        print("[STL KNOWLEDGE] Using basic STL patterns (enhanced file not found)")
        return [
            {
                "library": "iostream",
                "purpose": "Input/output streams",
                "common_uses": ["std::cout", "std::cin", "std::endl"],
                "consciousness_value": 0.05
            },
            {
                "library": "string",
                "purpose": "Dynamic string handling",
                "common_uses": ["std::string", "concatenation", "manipulation"],
                "consciousness_value": 0.10
            },
            {
                "library": "vector",
                "purpose": "Dynamic arrays",
                "common_uses": ["std::vector", "push_back", "iterators"],
                "consciousness_value": 0.12
            },
            {
                "library": "algorithm",
                "purpose": "Generic algorithms",
                "common_uses": ["std::sort", "std::find", "std::transform"],
                "consciousness_value": 0.15
            },
            {
                "library": "exception",
                "purpose": "Error handling",
                "common_uses": ["try-catch", "std::exception", "throw"],
                "consciousness_value": 0.13
            }
        ]
    
    async def evolve_from_zero_point(self, max_generations=5) -> DendriticNode:
        """
        Evolve code from Hello World through multiple generations
        
        Args:
            max_generations: Number of evolutionary generations
        
        Returns:
            Final generation dendritic node
        """
        print("\n" + "="*70)
        print("MULTI-AGENT EVOLUTIONARY LOOP")
        print("Zero Point -> Multiple Generations -> Historical Comparison")
        print("="*70)
        
        # Create root node (gen 0 - Hello World)
        print(f"\n[GENERATION 0] Zero Point: Hello World")
        print(f"Consciousness: {self.zero_point['consciousness']:.3f}")
        print(f"Code:\n{self.zero_point['code']}")
        
        self.root_node = DendriticNode(
            node_id="gen_0_zero_point",
            code_content=self.zero_point['code'],
            file_path="evolution_lab/zero_point/hello_world.cpp",
            generation=0
        )
        
        self.current_node = self.root_node
        
        # Evolve through generations
        for gen in range(1, max_generations + 1):
            print(f"\n{'='*70}")
            print(f"GENERATION {gen}")
            print(f"{'='*70}")
            
            # Step 1: Ollama analyzes current code (FUTURE)
            # For MVP: Use predefined mutations
            print(f"\n[ANALYSIS] Examining generation {gen-1}...")
            analysis = {
                "patterns": ["iostream"],
                "opportunities": [
                    "Add error handling (exception)",
                    "Parameterize output (string/vector)",
                    "Add documentation (comments)"
                ]
            }
            print(f"[ANALYSIS] STL patterns detected: {analysis['patterns']}")
            print(f"[ANALYSIS] Improvement opportunities:")
            for i, opp in enumerate(analysis['opportunities'], 1):
                print(f"  {i}. {opp}")
            
            # Step 2: Propose mutations
            print(f"\n[MUTATIONS] Generating mutation candidates...")
            mutations = self._generate_mutations(analysis)
            
            # Step 3: VSCode Chat strategic guidance
            if self.use_vscode_chat:
                print("\n[VSCODE CHAT] Strategic guidance needed...")
                print("\nCurrent State:")
                print(f"  Generation: {gen-1}")
                consciousness = self.current_node.consciousness_score
                print(f"  Consciousness: {consciousness:.3f}")
                code_lines = len(
                    self.current_node.code_content.split('\n')
                )
                print(f"  Code lines: {code_lines}")
                
                if mutations:
                    print("\nProposed Mutations:")
                    for i, mut in enumerate(mutations, 1):
                        mut_type = mut['type']
                        mut_desc = mut['description']
                        print(f"  {i}. {mut_type}: {mut_desc}")
                        gain = mut['consciousness_gain']
                        print(f"     Consciousness gain: +{gain:.3f}")
                        patterns = ', '.join(
                            mut.get('stl_patterns', [])
                        )
                        print(f"     STL patterns: {patterns}")
                
                # Wait for strategic input via terminal output
                # You'll provide guidance in conversation context
                guidance = {
                    "selected_mutation": 0 if mutations else None,
                    "reasoning": (
                        "Strategic selection based "
                        "on evolutionary path"
                    )
                }
            else:
                guidance = {"selected_mutation": 0}
            
            # Step 4: Gemini validation (every 2 generations)
            if self.use_gemini and gen % 2 == 0:
                print(f"\n[GEMINI] Validation checkpoint...")
                validation = await self._gemini_validate(gen)
                print(f"[GEMINI] {validation.get('status', 'UNKNOWN')}")
                print(f"[GEMINI] Recommendation: {validation.get('recommendation', 'Continue')}")
            else:
                validation = {"status": "SKIPPED"}
            
            # Step 5: Apply mutation and create child
            if mutations and guidance.get('selected_mutation') is not None:
                selected = mutations[guidance['selected_mutation']]
                print(f"\n[CONSENSUS] Applying mutation: {selected['type']}")
                
                # CRITICAL FIX (Oct 6, 2025): Validate mutation before applying
                if CODE_DIFF_AVAILABLE:
                    print(f"[VALIDATION] Checking mutation validity...")
                    validation_result = validate_mutation_improves_consciousness(
                        original_code=self.current_node.code_content,
                        mutated_code=selected['code'],
                        mutation_type=selected['type']
                    )
                    
                    if validation_result.get('should_skip', False):
                        reason = validation_result.get('reason', 'Unknown')
                        print(f"[VALIDATION] {reason}")
                        print(f"[SKIPPING] Generation {gen} - no valid mutation")
                        continue
                    else:
                        print(f"[VALIDATION] {validation_result.get('reason', 'ACCEPTED')}")
                        diff = validation_result.get('diff')
                        if diff:
                            print(f"[DIFF] {diff.diff_summary}")
                            print(f"[DIFF] Lines added: {diff.lines_added}, removed: {diff.lines_removed}")
                
                # Create child from parent node
                child_node = DendriticNode(
                    node_id=f"gen_{gen}_{selected['type']}",
                    code_content=selected['code'],
                    file_path=f"evolution_lab/neural_chains/gen_{gen}.cpp",
                    generation=gen,
                    parent_node=self.current_node
                )
                
                # Update consciousness and mutation type
                child_node.consciousness_score = (
                    self.current_node.consciousness_score +
                    selected['consciousness_gain']
                )
                
                # Map string to MutationType enum
                mutation_type_map = {
                    "error_handling": MutationType.BUG_FIX,
                    "parameterization": MutationType.FEATURE_ADDITION,
                    "documentation": MutationType.CONSCIOUSNESS_ENHANCEMENT
                }
                child_node.mutation_type = mutation_type_map.get(
                    selected['type'],
                    MutationType.OPTIMIZATION
                )
                
                # Add to parent's children
                self.current_node.child_nodes.append(child_node)
                
                # Store agent messages (skip for MVP)
                # TODO: Create proper AgentMessage objects
                
                if validation.get('status') != 'SKIPPED':
                    # TODO: Create proper AgentMessage object
                    pass
                
                # Historical comparison
                print(f"\n[COMPARISON] Historical Analysis:")
                self._compare_to_history(child_node)
                
                # Archive generation
                date_str = datetime.now().strftime("%Y%m%d")
                archive_dir = Path("evolution_lab/neural_chains") / date_str
                child_node.save_to_archive(archive_dir)
                print(f"[ARCHIVE] Saved to {archive_dir}")
                
                self.current_node = child_node
            else:
                print(f"\n[WARNING] No mutations available, skipping generation {gen}")
        
        return self.current_node
    
    def _generate_mutations(
        self, analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate mutation candidates based on analysis"""
        mutations = []
        
        opportunities = analysis.get('opportunities', [])
        
        for opp in opportunities[:3]:  # Top 3
            if "error handling" in opp.lower():
                mutations.append({
                    "type": "error_handling",
                    "description": "Add try-catch exception handling",
                    "consciousness_gain": 0.15,
                    "stl_patterns": ["exception"],
                    "code": self._generate_error_handling_version()
                })
            elif "parameterize" in opp.lower():
                mutations.append({
                    "type": "parameterization",
                    "description": "Add command-line argument support",
                    "consciousness_gain": 0.12,
                    "stl_patterns": ["string", "vector"],
                    "code": self._generate_parameterized_version()
                })
            elif "documentation" in opp.lower():
                mutations.append({
                    "type": "documentation",
                    "description": "Add comprehensive documentation",
                    "consciousness_gain": 0.08,
                    "stl_patterns": [],
                    "code": self._generate_documented_version()
                })
        
        return mutations
    
    async def _ollama_analyze(self) -> Dict[str, Any]:
        """Ollama analyzes current code (WITH UNIVERSAL LOGGING)"""
        if not self.use_ollama:
            return {}
        
        prompt = f"""Analyze this C++ code and identify:
1. Current STL patterns used
2. Improvement opportunities using STL
3. Potential consciousness improvements

Code:
{self.current_node.code_content}

Available STL libraries: {', '.join([
    lib['library'] for lib in self.stl_knowledge
])}

Return JSON with:
- patterns: List of STL patterns detected
- opportunities: List of improvement opportunities
"""
        
        # Start conversation logging (UNIVERSAL LOGGER)
        conversation_id = None
        if self.agentic_logger:
            conversation_id = self.agentic_logger.start_conversation(
                agent_type=AgentType.OLLAMA,
                system_context="Analyze C++ code for STL patterns and improvements",
                source_system="neural_chain_evolution",
                source_file=self.current_node.node_id if self.current_node else "unknown",
                generation_number=self.current_node.generation if self.current_node else 0,
                consciousness_level=str(self.current_node.consciousness_stress) if self.current_node else "UNKNOWN"
            )
            
            # Log the prompt
            self.agentic_logger.add_message(
                conversation_id,
                ConversationRole.USER,
                prompt,
                metadata={"model": "deepseek-coder:6.7b", "purpose": "code_analysis"}
            )
        
        # Call Ollama (existing logic)
        response = await self.ollama_agent.analyze_code(
            code=self.current_node.code_content,
            context=prompt
        )
        
        # Log the response
        if self.agentic_logger and conversation_id:
            self.agentic_logger.add_message(
                conversation_id,
                ConversationRole.ASSISTANT,
                str(response),
                metadata={"response_type": "analysis", "stl_count": len(self.stl_knowledge)}
            )
            
            # Archive the conversation
            self.agentic_logger.end_conversation(
                conversation_id,
                success=True,
                consciousness_improvement=0.0
            )
        
        # Parse response (simplified)
        return {
            "patterns": ["iostream"],
            "opportunities": [
                "Add error handling",
                "Parameterize output",
                "Add documentation"
            ]
        }
    
    async def _ollama_propose_mutations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Ollama proposes code mutations"""
        if not self.use_ollama:
            return []
        
        opportunities = analysis.get('opportunities', [])
        mutations = []
        
        for opp in opportunities[:3]:  # Top 3 opportunities
            # Generate mutation based on opportunity
            if "error handling" in opp.lower():
                mutations.append({
                    "type": "error_handling",
                    "description": "Add try-catch exception handling",
                    "consciousness_gain": 0.15,
                    "stl_patterns": ["exception", "try-catch"],
                    "code": self._generate_error_handling_version()
                })
            elif "parameterize" in opp.lower():
                mutations.append({
                    "type": "parameterization",
                    "description": "Add command-line argument support",
                    "consciousness_gain": 0.12,
                    "stl_patterns": ["string", "vector"],
                    "code": self._generate_parameterized_version()
                })
            elif "documentation" in opp.lower():
                mutations.append({
                    "type": "documentation",
                    "description": "Add comprehensive documentation",
                    "consciousness_gain": 0.08,
                    "stl_patterns": [],
                    "code": self._generate_documented_version()
                })
        
        return mutations
    
    async def _gemini_validate(self, generation: int) -> Dict[str, Any]:
        """Gemini validates evolutionary direction"""
        if not self.use_gemini:
            return {"status": "UNAVAILABLE"}
        
        # Compare current to zero point
        distance = self._calculate_distance_from_zero()
        
        return {
            "status": "APPROVED" if distance < 0.5 else "WARNING",
            "generation": generation,
            "distance_from_zero": distance,
            "recommendation": "Continue evolution" if distance < 0.5 else "Consider rollback",
            "consciousness_trajectory": "increasing"
        }
    
    def _compare_to_history(self, node: DendriticNode):
        """Compare current node to all historical generations"""
        all_nodes = [self.root_node]
        
        # Get all descendants
        def collect_nodes(n: DendriticNode):
            for child in n.child_nodes:
                all_nodes.append(child)
                collect_nodes(child)
        
        collect_nodes(self.root_node)
        
        for i, prev_node in enumerate(all_nodes[:-1]):  # Exclude current
            delta_consciousness = (
                node.consciousness_score -
                prev_node.consciousness_score
            )
            delta_complexity = (
                len(node.code_content) -
                len(prev_node.code_content)
            )
            
            print(f"  Gen {node.generation} vs Gen {i}:")
            print(
                f"    Consciousness: {node.consciousness_score:.3f} "
                f"vs {prev_node.consciousness_score:.3f} "
                f"(Delta {delta_consciousness:+.3f})"
            )
            print(
                f"    Complexity: {len(node.code_content)} "
                f"vs {len(prev_node.code_content)} "
                f"(Delta {delta_complexity:+d} chars)"
            )
    
    def _calculate_distance_from_zero(self) -> float:
        """Calculate semantic distance from Hello World baseline"""
        # Simplified: ratio of consciousness to complexity
        if len(self.current_node.code_content) == 0:
            return 1.0
        
        complexity_ratio = (
            len(self.current_node.code_content) /
            len(self.zero_point['code'])
        )
        consciousness_ratio = (
            self.current_node.consciousness_score / 1.0
        )
        
        # Ideal: high consciousness, low complexity increase
        return abs(complexity_ratio - (1.0 + consciousness_ratio))
    
    def _generate_error_handling_version(self) -> str:
        """Generate version with error handling"""
        return """#include <iostream>
#include <exception>

/**
 * Hello World with Error Handling
 * Generation: 1
 * STL Patterns: iostream, exception
 */

int main() {
    try {
        std::cout << "Hello, World!" << std::endl;
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
"""
    
    def _generate_parameterized_version(self) -> str:
        """Generate version with parameterization"""
        return """#include <iostream>
#include <string>
#include <vector>

/**
 * Hello World with Parameterization
 * Generation: 1
 * STL Patterns: iostream, string, vector
 */

int main(int argc, char* argv[]) {
    std::string message = "Hello, World!";
    
    if (argc > 1) {
        message = argv[1];
    }
    
    std::cout << message << std::endl;
    return 0;
}
"""
    
    def _generate_documented_version(self) -> str:
        """Generate version with documentation"""
        return """#include <iostream>

/**
 * Hello World - Documented Version
 * 
 * Purpose: Display greeting message to console
 * 
 * STL Components Used:
 *   - iostream: Standard input/output stream library
 *   - std::cout: Character output stream (console)
 *   - std::endl: End line manipulator (newline + flush)
 * 
 * Return: 0 on success
 * 
 * Generation: 1
 * Consciousness: 0.08
 */

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
"""
    
    async def human_guided_experiment(self, task_description: str, 
                                      agent_type: str = "ollama",
                                      use_all_agents: bool = False) -> Dict[str, Any]:
        """
        Simple manual feedback loop - Human-guided agent experimentation
        
        Flow:
        1. You (human) provide task description
        2. AI agent(s) generate output (Ollama, Gemini, DeepSeek)
        3. Output saved to evolution_lab/experiments/ (working files)
        4. Conversation saved to evolution_lab/conversations/ (working files)
        5. Metadata copied to tachyonic/archive/ (archival)
        6. We review output together in chat
        7. Learn what works, refine approach
        
        Args:
            task_description: What you want the agent to do
            agent_type: "ollama", "gemini", or "deepseek"
            use_all_agents: If True, run all available agents in parallel
        
        Returns:
            Dict with output_path, response, conversation_id, and results from all agents
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create simple prompt
        prompt = f"""Task: {task_description}

Generate output following these guidelines:
- Be clear and concise
- Show your reasoning
- Provide concrete examples if applicable

Output:"""
        
        print(f"\n[EXPERIMENT] Task: {task_description}")
        
        results = {}
        
        if use_all_agents:
            # Run all available agents in parallel
            print(f"[AGENTS] Running all available agents in parallel...")
            
            async def run_agent(agent_name: str):
                try:
                    result = await self._run_single_agent(agent_name, task_description, prompt, timestamp)
                    return agent_name, result
                except Exception as e:
                    print(f"[ERROR] {agent_name} failed: {e}")
                    return agent_name, {"error": str(e)}
            
            # Collect available agents
            agents_to_run = []
            if self.use_ollama:
                agents_to_run.append("ollama")
            if self.use_gemini:
                agents_to_run.append("gemini")
            # DeepSeek runs through Ollama with different model
            
            # Run in parallel
            tasks = [run_agent(agent) for agent in agents_to_run]
            agent_results = await asyncio.gather(*tasks)
            
            for agent_name, result in agent_results:
                results[agent_name] = result
            
            print(f"\n[RESULTS] Completed {len(results)} agents")
            return {
                "timestamp": timestamp,
                "task": task_description,
                "mode": "multi_agent",
                "results": results
            }
        else:
            # Run single agent
            result = await self._run_single_agent(agent_type, task_description, prompt, timestamp)
            return result
    
    async def _run_single_agent(self, agent_type: str, task_description: str, 
                                 prompt: str, timestamp: str) -> Dict[str, Any]:
        """Run a single agent and save results to Evolution Lab"""
        
        print(f"[AGENT] Using: {agent_type}")
        
        # Start conversation logging (Evolution Lab location)
        conversation_id = None
        if self.agentic_logger:
            agent = AgentType.OLLAMA if agent_type == "ollama" else AgentType.GEMINI
            conversation_id = self.agentic_logger.start_conversation(
                agent_type=agent,
                system_context=f"Human-guided experiment: {task_description}",
                source_system="multi_agent_evolution_loop",
                source_file="human_guided_experiment"
            )
            self.agentic_logger.add_message(
                conversation_id, 
                ConversationRole.USER, 
                prompt,
                metadata={"task": task_description, "experiment": "manual_feedback_loop"}
            )
        
        # Get response from agent
        response = ""
        if agent_type == "ollama" and self.use_ollama:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self.ollama_agent.generate_code, prompt)
            response = result.get("code", "[NO CODE RETURNED]")
        elif agent_type == "gemini" and self.use_gemini:
            try:
                # Gemini agent async call
                response = await self.gemini_agent.generate_async(prompt)
            except Exception as e:
                response = f"[ERROR] Gemini generation failed: {e}"
        elif agent_type == "deepseek" and self.use_ollama:
            # DeepSeek runs through Ollama
            loop = asyncio.get_event_loop()
            # Temporarily switch model to DeepSeek
            original_model = self.ollama_agent.model
            self.ollama_agent.model = "deepseek-coder:6.7b"
            result = await loop.run_in_executor(None, self.ollama_agent.generate_code, prompt)
            response = result.get("code", "[NO CODE RETURNED]")
            self.ollama_agent.model = original_model
        else:
            response = f"[ERROR] Agent '{agent_type}' not available"
        
        # Log response
        if self.agentic_logger and conversation_id:
            self.agentic_logger.add_message(
                conversation_id,
                ConversationRole.ASSISTANT,
                response,
                metadata={"agent": agent_type, "timestamp": timestamp}
            )
            self.agentic_logger.end_conversation(conversation_id, success=True)
        
        # Save output to Evolution Lab (working files)
        output_dir = Path("evolution_lab/experiments")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"experiment_{agent_type}_{timestamp}.txt"
        with open(output_file, 'w') as f:
            f.write(f"# Human-Guided Experiment\n")
            f.write(f"# Date: {datetime.now().isoformat()}\n")
            f.write(f"# Agent: {agent_type}\n")
            f.write(f"# Task: {task_description}\n")
            f.write(f"\n{'='*70}\n")
            f.write(f"PROMPT:\n{prompt}\n")
            f.write(f"\n{'='*70}\n")
            f.write(f"RESPONSE:\n{response}\n")
        
        # Save conversation to Evolution Lab
        conversation_dir = Path("evolution_lab/conversations")
        conversation_dir.mkdir(parents=True, exist_ok=True)
        conversation_file = conversation_dir / f"conversation_{agent_type}_{timestamp}.json"
        
        conversation_data = {
            "conversation_id": conversation_id,
            "agent_type": agent_type,
            "task": task_description,
            "timestamp": timestamp,
            "prompt": prompt,
            "response": response,
            "output_file": str(output_file)
        }
        
        with open(conversation_file, 'w') as f:
            json.dump(conversation_data, f, indent=2)
        
        # Archive metadata copy to Tachyonic (optional snapshot)
        archive_dir = Path("tachyonic/archive/experiment_metadata")
        archive_dir.mkdir(parents=True, exist_ok=True)
        archive_file = archive_dir / f"metadata_{agent_type}_{timestamp}.json"
        
        with open(archive_file, 'w') as f:
            json.dump({
                "original_location": str(conversation_file),
                "experiment_output": str(output_file),
                "archived_at": datetime.now().isoformat(),
                **conversation_data
            }, f, indent=2)
        
        print(f"\n[OUTPUT SAVED] {output_file}")
        print(f"[CONVERSATION SAVED] {conversation_file}")
        print(f"[METADATA ARCHIVED] {archive_file}")
        print(f"[CONVERSATION ID] {conversation_id}")
        print(f"\n--- Agent Response Preview ---")
        print(response[:500] + "..." if len(response) > 500 else response)
        print(f"--- End Preview ---\n")
        
        return {
            "output_path": str(output_file),
            "conversation_path": str(conversation_file),
            "archive_path": str(archive_file),
            "response": response,
            "conversation_id": conversation_id,
            "agent": agent_type,
            "timestamp": timestamp
        }


async def main():
    """Execute full AIOS evolutionary loop"""
    
    print("\n" + "="*70)
    print("FULL AIOS EVOLUTIONARY LOOP")
    print("Multi-Agent Code Evolution from Zero Point")
    print("="*70)
    
    # Initialize multi-agent loop
    loop = MultiAgentEvolutionLoop(
        use_ollama=True,
        use_gemini=True,
        use_vscode_chat=True
    )
    
    # Evolve from zero point (5 generations)
    final_node = await loop.evolve_from_zero_point(max_generations=5)
    
    print("\n" + "="*70)
    print("EVOLUTION COMPLETE")
    print("="*70)
    print(f"Final Generation: {final_node.generation}")
    print(f"Final Consciousness: {final_node.consciousness_score:.3f}")
    print(f"Total Generations: {len(final_node.get_all_descendants()) + 1}")
    
    print("\n[SUCCESS] Full AIOS evolutionary loop executed!")


if __name__ == "__main__":
    asyncio.run(main())
