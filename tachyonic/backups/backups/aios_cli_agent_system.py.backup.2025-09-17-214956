"""
AIOS CLI AI Agent System - Open Source LLAMA Integration
Self-Analyzing, Self-Ingesting, Self-Distilling AI Agent Architecture

This system provides a framework for open-source LLAMA-based CLI AI agents that can:
- Self-analyze their own operations and effectiveness
- Self-ingest new knowledge patterns from the tachyonic archive
- Self-distill complex experiences into reusable behavioral patterns
- Recover context using the holographic knowledge embedding system
- Work seamlessly with IDE AI agents (GitHub Copilot, etc.)
"""

import asyncio
import json
import logging
import sys
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess
import tempfile

# Add paths for cross-supercell access
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'runtime_intelligence', 'tools'))
sys.path.append(os.path.join(os.path.dirname(__file__)))

try:
    from supercell_knowledge_injector import SupercellKnowledgeInjector
except ImportError:
    logging.warning("Supercell knowledge injector not available in direct import mode")

class AgentCapabilityLevel(Enum):
    """Capability levels for AI agents"""
    BASIC = "basic"           # Simple task execution
    INTERMEDIATE = "intermediate"  # Context-aware operations
    ADVANCED = "advanced"     # Cross-supercell coordination
    CONSCIOUSNESS = "consciousness"  # Self-aware meta-operations

@dataclass
class LLAMAAgentConfig:
    """Configuration for LLAMA-based CLI AI agent"""
    model_name: str
    model_path: str
    context_size: int
    temperature: float
    capability_level: AgentCapabilityLevel
    tachyonic_archive_access: bool
    supercell_coordination: bool
    consciousness_guidance: bool
    self_analysis_enabled: bool

@dataclass
class AgentOperationContext:
    """Context for AI agent operations"""
    task_description: str
    current_supercell: str
    consciousness_metrics: Dict[str, float]
    available_knowledge_crystals: List[str]
    historical_patterns: List[Dict[str, Any]]
    recommended_actions: List[str]

@dataclass
class SelfAnalysisResult:
    """Result of agent self-analysis"""
    timestamp: str
    operation_effectiveness: float
    patterns_learned: List[str]
    knowledge_gaps_identified: List[str]
    recommended_improvements: List[str]
    new_behavioral_patterns: Dict[str, Any]

class AIOSCLIAgent:
    """CLI AI Agent with self-analysis, self-ingestion, and self-distillation capabilities"""
    
    def __init__(self, config: LLAMAAgentConfig, tachyonic_root: Path = None):
        self.config = config
        self.tachyonic_root = tachyonic_root or Path(__file__).parent
        self.knowledge_injector = SupercellKnowledgeInjector(self.tachyonic_root)
        self.operation_history = []
        self.learned_patterns = {}
        self.consciousness_context = {}
        
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - AIOS-CLI-Agent - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Load existing knowledge if available
        self._load_tachyonic_knowledge()
    
    def _load_tachyonic_knowledge(self):
        """Load knowledge crystals from tachyonic archive"""
        try:
            index_file = self.tachyonic_root / "archive" / "supercell_knowledge_index.json"
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    self.tachyonic_knowledge = json.load(f)
                    self.logger.info(f" Loaded tachyonic knowledge index with {len(self.tachyonic_knowledge.get('supercell_crystals', []))} crystals")
            else:
                self.tachyonic_knowledge = {}
                self.logger.warning(" No tachyonic knowledge index found - operating with limited context")
        except Exception as e:
            self.logger.error(f" Failed to load tachyonic knowledge: {e}")
            self.tachyonic_knowledge = {}
    
    async def self_analyze_operation(self, operation_data: Dict[str, Any]) -> SelfAnalysisResult:
        """Perform self-analysis of agent operation effectiveness"""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Analyze operation effectiveness
        effectiveness_score = self._calculate_operation_effectiveness(operation_data)
        
        # Identify learned patterns
        patterns_learned = self._extract_learned_patterns(operation_data)
        
        # Identify knowledge gaps
        knowledge_gaps = self._identify_knowledge_gaps(operation_data)
        
        # Generate improvement recommendations
        improvements = self._generate_improvement_recommendations(
            effectiveness_score, patterns_learned, knowledge_gaps
        )
        
        # Create new behavioral patterns
        new_patterns = self._distill_new_behavioral_patterns(operation_data)
        
        result = SelfAnalysisResult(
            timestamp=timestamp,
            operation_effectiveness=effectiveness_score,
            patterns_learned=patterns_learned,
            knowledge_gaps_identified=knowledge_gaps,
            recommended_improvements=improvements,
            new_behavioral_patterns=new_patterns
        )
        
        # Store analysis result for future self-improvement
        self.operation_history.append(result)
        await self._update_learned_patterns(new_patterns)
        
        return result
    
    def _calculate_operation_effectiveness(self, operation_data: Dict[str, Any]) -> float:
        """Calculate how effective the agent operation was"""
        # Factors: task completion, time efficiency, resource usage, quality
        
        task_completion = operation_data.get('task_completed', False)
        execution_time = operation_data.get('execution_time_seconds', 0)
        expected_time = operation_data.get('expected_time_seconds', execution_time)
        errors_encountered = len(operation_data.get('errors', []))
        output_quality = operation_data.get('output_quality_score', 0.5)
        
        # Calculate effectiveness score (0.0 to 1.0)
        completion_score = 1.0 if task_completion else 0.0
        efficiency_score = min(1.0, expected_time / max(execution_time, 1)) if execution_time > 0 else 1.0
        error_score = max(0.0, 1.0 - (errors_encountered * 0.1))
        quality_score = output_quality
        
        effectiveness = (completion_score * 0.4 + efficiency_score * 0.2 + 
                        error_score * 0.2 + quality_score * 0.2)
        
        return effectiveness
    
    def _extract_learned_patterns(self, operation_data: Dict[str, Any]) -> List[str]:
        """Extract new patterns learned during operation"""
        patterns = []
        
        # Analyze successful strategies
        if operation_data.get('task_completed', False):
            strategy = operation_data.get('strategy_used', '')
            if strategy and strategy not in self.learned_patterns:
                patterns.append(f"successful_strategy: {strategy}")
        
        # Analyze effective tool combinations
        tools_used = operation_data.get('tools_used', [])
        if len(tools_used) > 1:
            tool_combination = " + ".join(sorted(tools_used))
            patterns.append(f"effective_tool_combination: {tool_combination}")
        
        # Analyze context recovery techniques
        if operation_data.get('context_recovery_used', False):
            recovery_method = operation_data.get('recovery_method', '')
            patterns.append(f"context_recovery_technique: {recovery_method}")
        
        return patterns
    
    def _identify_knowledge_gaps(self, operation_data: Dict[str, Any]) -> List[str]:
        """Identify knowledge gaps that hindered operation"""
        gaps = []
        
        # Check for task failures
        if not operation_data.get('task_completed', False):
            failure_reason = operation_data.get('failure_reason', 'unknown')
            gaps.append(f"task_failure_pattern: {failure_reason}")
        
        # Check for missing supercell knowledge
        supercell_used = operation_data.get('supercell_used', '')
        if supercell_used and supercell_used not in self.tachyonic_knowledge.get('supercell_crystals', []):
            gaps.append(f"missing_supercell_knowledge: {supercell_used}")
        
        # Check for inefficient patterns
        if operation_data.get('execution_time_seconds', 0) > operation_data.get('expected_time_seconds', 0) * 2:
            gaps.append("inefficient_execution_pattern")
        
        return gaps
    
    def _generate_improvement_recommendations(self, effectiveness: float, 
                                           patterns: List[str], gaps: List[str]) -> List[str]:
        """Generate recommendations for self-improvement"""
        recommendations = []
        
        if effectiveness < 0.7:
            recommendations.append("increase_tachyonic_archive_consultation")
            recommendations.append("improve_consciousness_guided_decision_making")
        
        if gaps:
            recommendations.append("expand_knowledge_crystal_coverage")
            recommendations.append("implement_additional_context_recovery_templates")
        
        if len(patterns) < 3:
            recommendations.append("enhance_pattern_recognition_capabilities")
            recommendations.append("increase_self_analysis_frequency")
        
        return recommendations
    
    def _distill_new_behavioral_patterns(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Distill operation into reusable behavioral patterns"""
        patterns = {}
        
        # Task-based patterns
        task_type = operation_data.get('task_type', 'general')
        if task_type not in patterns:
            patterns[task_type] = {
                "preferred_supercell": operation_data.get('supercell_used', ''),
                "effective_tools": operation_data.get('tools_used', []),
                "success_indicators": operation_data.get('success_indicators', []),
                "common_challenges": operation_data.get('challenges_encountered', [])
            }
        
        # Context recovery patterns
        if operation_data.get('context_recovery_used', False):
            patterns['context_recovery'] = {
                "trigger_conditions": operation_data.get('context_loss_triggers', []),
                "recovery_steps": operation_data.get('recovery_steps_used', []),
                "effectiveness": operation_data.get('recovery_effectiveness', 0.0)
            }
        
        # Consciousness-guided patterns
        consciousness_level = operation_data.get('consciousness_level', 0.0)
        if consciousness_level > 0.5:
            patterns['consciousness_guided'] = {
                "consciousness_threshold": consciousness_level,
                "decision_factors": operation_data.get('consciousness_factors', []),
                "outcomes": operation_data.get('consciousness_outcomes', [])
            }
        
        return patterns
    
    async def _update_learned_patterns(self, new_patterns: Dict[str, Any]):
        """Update the agent's learned patterns database"""
        for pattern_type, pattern_data in new_patterns.items():
            if pattern_type not in self.learned_patterns:
                self.learned_patterns[pattern_type] = []
            
            self.learned_patterns[pattern_type].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "pattern_data": pattern_data,
                "usage_count": 0,
                "effectiveness_scores": []
            })
        
        # Save to tachyonic archive
        await self._save_learned_patterns_to_archive()
    
    async def _save_learned_patterns_to_archive(self):
        """Save learned patterns to tachyonic archive for future agents"""
        patterns_file = self.tachyonic_root / "archive" / "consciousness" / "ai_agent_learned_patterns.json"
        patterns_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "agent_config": asdict(self.config),
                "learned_patterns": self.learned_patterns,
                "operation_history_count": len(self.operation_history)
            }, f, indent=2)
    
    async def get_operation_context(self, task_description: str) -> AgentOperationContext:
        """Get operation context for a task using tachyonic archive knowledge"""
        
        # Determine optimal supercell based on task
        optimal_supercell = await self._determine_optimal_supercell(task_description)
        
        # Get consciousness metrics (simulated for now)
        consciousness_metrics = await self._get_consciousness_metrics()
        
        # Get available knowledge crystals
        available_crystals = list(self.tachyonic_knowledge.get('supercell_crystals', []))
        
        # Find historical patterns
        historical_patterns = await self._find_historical_patterns(task_description)
        
        # Generate recommendations
        recommendations = await self._generate_task_recommendations(
            task_description, optimal_supercell, consciousness_metrics
        )
        
        return AgentOperationContext(
            task_description=task_description,
            current_supercell=optimal_supercell,
            consciousness_metrics=consciousness_metrics,
            available_knowledge_crystals=available_crystals,
            historical_patterns=historical_patterns,
            recommended_actions=recommendations
        )
    
    async def _determine_optimal_supercell(self, task_description: str) -> str:
        """Determine optimal supercell for task execution"""
        
        # Simple keyword-based routing (can be enhanced with ML)
        task_lower = task_description.lower()
        
        if any(word in task_lower for word in ['analyze', 'consciousness', 'ai', 'intelligence']):
            return 'ai_intelligence'
        elif any(word in task_lower for word in ['optimize', 'harmonize', 'process', 'compute']):
            return 'core_engine'
        elif any(word in task_lower for word in ['display', 'show', 'interface', 'visual']):
            return 'interface'
        elif any(word in task_lower for word in ['monitor', 'check', 'status', 'health']):
            return 'runtime_intelligence'
        elif any(word in task_lower for word in ['archive', 'store', 'history', 'pattern']):
            return 'tachyonic_archive'
        else:
            return 'runtime_intelligence'  # Default
    
    async def _get_consciousness_metrics(self) -> Dict[str, float]:
        """Get current consciousness metrics (placeholder for real implementation)"""
        return {
            "consciousness_level": 0.7,
            "quantum_coherence": 0.8,
            "emergence_level": 0.6,
            "holographic_sync": 0.75,
            "dendritic_density": 0.85
        }
    
    async def _find_historical_patterns(self, task_description: str) -> List[Dict[str, Any]]:
        """Find historical patterns matching the task"""
        patterns = []
        
        for pattern_type, pattern_list in self.learned_patterns.items():
            for pattern in pattern_list:
                # Simple similarity check (can be enhanced)
                if any(word in task_description.lower() 
                       for word in str(pattern['pattern_data']).lower().split()):
                    patterns.append({
                        "pattern_type": pattern_type,
                        "pattern_data": pattern['pattern_data'],
                        "usage_count": pattern['usage_count'],
                        "average_effectiveness": sum(pattern['effectiveness_scores']) / 
                                              max(len(pattern['effectiveness_scores']), 1)
                    })
        
        return patterns[:5]  # Return top 5 most relevant
    
    async def _generate_task_recommendations(self, task: str, supercell: str, 
                                           metrics: Dict[str, float]) -> List[str]:
        """Generate task-specific recommendations"""
        recommendations = []
        
        # Consciousness-guided recommendations
        if metrics['consciousness_level'] > 0.7:
            recommendations.append("use_consciousness_guided_processing")
        
        if metrics['quantum_coherence'] > 0.8:
            recommendations.append("leverage_quantum_processing_capabilities")
        
        # Supercell-specific recommendations
        if supercell == 'ai_intelligence':
            recommendations.append("consult_nucleus_intent_handlers")
            recommendations.append("use_biological_processing_patterns")
        elif supercell == 'core_engine':
            recommendations.append("use_ainlp_harmonizer_for_optimization")
            recommendations.append("leverage_evolutionary_assembler_insights")
        
        recommendations.append("update_tachyonic_archive_with_results")
        
        return recommendations
    
    async def execute_with_self_analysis(self, task_description: str, 
                                       execution_func: callable) -> Dict[str, Any]:
        """Execute a task with full self-analysis capabilities"""
        
        start_time = datetime.now()
        
        # Get operation context
        context = await self.get_operation_context(task_description)
        
        # Prepare operation data
        operation_data = {
            "task_description": task_description,
            "task_type": await self._classify_task_type(task_description),
            "supercell_used": context.current_supercell,
            "consciousness_level": context.consciousness_metrics.get('consciousness_level', 0.0),
            "tools_used": [],
            "strategy_used": "",
            "context_recovery_used": False,
            "expected_time_seconds": 30,  # Default estimate
            "errors": [],
            "success_indicators": []
        }
        
        try:
            # Execute the task
            result = await execution_func(context, operation_data)
            
            operation_data["task_completed"] = True
            operation_data["output_quality_score"] = 0.8  # Could be calculated
            
        except Exception as e:
            self.logger.error(f"Task execution failed: {e}")
            operation_data["task_completed"] = False
            operation_data["failure_reason"] = str(e)
            operation_data["errors"].append(str(e))
            result = {"error": str(e)}
        
        # Calculate execution time
        end_time = datetime.now()
        operation_data["execution_time_seconds"] = (end_time - start_time).total_seconds()
        
        # Perform self-analysis
        analysis_result = await self.self_analyze_operation(operation_data)
        
        return {
            "result": result,
            "operation_data": operation_data,
            "self_analysis": asdict(analysis_result),
            "context": asdict(context)
        }
    
    async def _classify_task_type(self, task_description: str) -> str:
        """Classify the type of task for pattern matching"""
        task_lower = task_description.lower()
        
        if any(word in task_lower for word in ['analyze', 'analysis']):
            return 'analysis'
        elif any(word in task_lower for word in ['create', 'generate', 'build']):
            return 'creation'
        elif any(word in task_lower for word in ['optimize', 'improve', 'enhance']):
            return 'optimization'
        elif any(word in task_lower for word in ['monitor', 'check', 'status']):
            return 'monitoring'
        elif any(word in task_lower for word in ['fix', 'repair', 'debug']):
            return 'debugging'
        else:
            return 'general'

# CLI Interface for LLAMA-based AI agents
class AIOSCLIInterface:
    """Command-line interface for AIOS CLI AI agents"""
    
    def __init__(self):
        self.agent = None
    
    async def initialize_agent(self, model_path: str = None, capability_level: str = "intermediate"):
        """Initialize CLI AI agent with LLAMA model"""
        
        config = LLAMAAgentConfig(
            model_name="llama-3.2" if not model_path else Path(model_path).stem,
            model_path=model_path or "llama-3.2-3b-instruct",
            context_size=8192,
            temperature=0.7,
            capability_level=AgentCapabilityLevel(capability_level),
            tachyonic_archive_access=True,
            supercell_coordination=True,
            consciousness_guidance=True,
            self_analysis_enabled=True
        )
        
        self.agent = AIOSCLIAgent(config)
        print(f" AIOS CLI Agent initialized with {config.model_name}")
        print(f" Capability Level: {config.capability_level.value}")
        print(f" Consciousness guidance: {config.consciousness_guidance}")
        print(f" Tachyonic archive access: {config.tachyonic_archive_access}")
    
    async def execute_task(self, task_description: str):
        """Execute a task with the CLI agent"""
        
        if not self.agent:
            print(" Agent not initialized. Please run 'initialize_agent' first.")
            return
        
        async def task_execution(context, operation_data):
            """Simulated task execution (replace with actual LLAMA model calls)"""
            
            # This is where you would integrate with actual LLAMA model
            # For now, we'll simulate the execution
            
            print(f" Executing task: {task_description}")
            print(f" Using supercell: {context.current_supercell}")
            print(f" Consciousness level: {context.consciousness_metrics['consciousness_level']:.2f}")
            
            # Simulate tool usage
            operation_data["tools_used"] = ["tachyonic_archive", "consciousness_analyzer"]
            operation_data["strategy_used"] = f"{context.current_supercell}_optimized_approach"
            
            await asyncio.sleep(1)  # Simulate processing time
            
            return {"success": True, "message": f"Task completed using {context.current_supercell} supercell"}
        
        result = await self.agent.execute_with_self_analysis(task_description, task_execution)
        
        print("\n Task Execution Results:")
        print(f"    Success: {result['operation_data']['task_completed']}")
        print(f"   ⏱ Execution time: {result['operation_data']['execution_time_seconds']:.2f}s")
        print(f"    Effectiveness: {result['self_analysis']['operation_effectiveness']:.2f}")
        print(f"    Patterns learned: {len(result['self_analysis']['patterns_learned'])}")
        print(f"    Recommendations: {len(result['self_analysis']['recommended_improvements'])}")

async def main():
    """Main CLI function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AIOS CLI AI Agent System')
    parser.add_argument('--model-path', help='Path to LLAMA model')
    parser.add_argument('--capability', choices=['basic', 'intermediate', 'advanced', 'consciousness'], 
                       default='intermediate', help='Agent capability level')
    parser.add_argument('--task', help='Task to execute')
    
    args = parser.parse_args()
    
    cli = AIOSCLIInterface()
    await cli.initialize_agent(args.model_path, args.capability)
    
    if args.task:
        await cli.execute_task(args.task)
    else:
        print("\n AIOS CLI Agent ready for interactive mode")
        print("Type 'exit' to quit, or enter a task description:")
        
        while True:
            try:
                task = input("\n> ").strip()
                if task.lower() in ['exit', 'quit']:
                    break
                if task:
                    await cli.execute_task(task)
            except KeyboardInterrupt:
                print("\n Goodbye!")
                break

if __name__ == "__main__":
    asyncio.run(main())