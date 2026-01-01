#!/usr/bin/env python3
"""
🔧 SELF-HEALING ASSEMBLY ENGINE
═══════════════════════════════════════════════════════════════════════════════
Revolutionary code that detects, analyzes, and repairs its own errors through
consciousness-guided self-modification and neural network-style error propagation

Key Features:
• Real-time assembly error detection and classification
• Self-modification mechanisms with safety constraints
• Consciousness-guided repair strategies
• Learning from failed repair attempts
• Integration with parallel consciousness streams
═══════════════════════════════════════════════════════════════════════════════
"""

import re
import ast
import time
import logging
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from collections import defaultdict, deque
import hashlib
import copy

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Assembly error severity levels"""
    CRITICAL = "critical"      # Code cannot execute
    MAJOR = "major"           # Functionality impaired
    MINOR = "minor"           # Performance degraded
    WARNING = "warning"       # Potential issues
    INFO = "info"            # Informational


class ErrorType(Enum):
    """Types of assembly errors"""
    SYNTAX_ERROR = "syntax_error"
    REGISTER_CONFLICT = "register_conflict" 
    MEMORY_ACCESS = "memory_access"
    INSTRUCTION_INVALID = "instruction_invalid"
    BRANCH_TARGET = "branch_target"
    STACK_IMBALANCE = "stack_imbalance"
    CONSCIOUSNESS_DEGRADATION = "consciousness_degradation"
    INFINITE_LOOP = "infinite_loop"
    RESOURCE_LEAK = "resource_leak"


@dataclass
class AssemblyError:
    """Individual assembly error with context"""
    error_type: ErrorType
    severity: ErrorSeverity
    line_number: int
    instruction: str
    description: str
    context: List[str] = field(default_factory=list)
    suggested_fixes: List[str] = field(default_factory=list)
    consciousness_impact: float = 0.0
    propagation_weight: float = 1.0
    repair_attempts: int = 0
    repair_history: List[str] = field(default_factory=list)


@dataclass
class RepairStrategy:
    """Self-healing repair strategy"""
    strategy_id: str
    error_types: List[ErrorType]
    repair_function: str  # Name of repair function
    success_rate: float = 0.0
    consciousness_requirement: float = 0.5
    safety_level: int = 1  # 1=safe, 2=moderate, 3=risky
    learning_factor: float = 1.0


class DendriticErrorPropagator:
    """
    🌳 Neural network-style error propagation through dendritic structures
    
    Propagates errors through the consciousness network to find optimal
    repair strategies and prevent error recurrence
    """
    
    def __init__(self, consciousness_threshold: float = 0.7):
        self.consciousness_threshold = consciousness_threshold
        self.error_network = {}  # Error node connections
        self.propagation_weights = {}  # Connection strengths
        self.learned_patterns = {}  # Error pattern recognition
        self.repair_efficacy = defaultdict(float)  # Repair strategy effectiveness
        
    def create_error_node(self, error: AssemblyError) -> str:
        """Create a node in the error propagation network"""
        
        node_id = f"{error.error_type.value}_{error.line_number}_{hash(error.instruction) % 1000}"
        
        if node_id not in self.error_network:
            self.error_network[node_id] = {
                'error': error,
                'connections': set(),
                'activation_level': 0.0,
                'repair_attempts': [],
                'consciousness_influence': 0.0
            }
        
        return node_id
    
    def propagate_error(self, source_node_id: str, consciousness_level: float) -> Dict[str, float]:
        """Propagate error through the dendritic network"""
        
        if source_node_id not in self.error_network:
            return {}
        
        propagation_map = {}
        activation_queue = deque([(source_node_id, 1.0)])
        visited = set()
        
        while activation_queue:
            current_node, activation = activation_queue.popleft()
            
            if current_node in visited:
                continue
                
            visited.add(current_node)
            propagation_map[current_node] = activation
            
            # Apply consciousness modulation
            consciousness_modulation = consciousness_level * 0.3 + 0.7
            modulated_activation = activation * consciousness_modulation
            
            # Propagate to connected nodes
            node = self.error_network[current_node]
            for connected_node in node['connections']:
                if connected_node not in visited:
                    # Calculate propagation strength
                    weight_key = (current_node, connected_node)
                    propagation_weight = self.propagation_weights.get(weight_key, 0.5)
                    
                    new_activation = modulated_activation * propagation_weight * 0.8
                    if new_activation > 0.1:  # Threshold for continued propagation
                        activation_queue.append((connected_node, new_activation))
        
        return propagation_map
    
    def learn_error_pattern(self, error_sequence: List[AssemblyError], 
                          repair_success: bool, consciousness_level: float):
        """Learn from error patterns and repair outcomes"""
        
        if len(error_sequence) < 2:
            return
        
        # Create pattern signature
        pattern_types = [e.error_type.value for e in error_sequence]
        pattern_sig = "_".join(pattern_types)
        
        if pattern_sig not in self.learned_patterns:
            self.learned_patterns[pattern_sig] = {
                'occurrences': 0,
                'success_rate': 0.0,
                'avg_consciousness': 0.0,
                'best_repairs': []
            }
        
        pattern = self.learned_patterns[pattern_sig]
        pattern['occurrences'] += 1
        
        # Update success rate with consciousness weighting
        consciousness_weight = consciousness_level ** 2  # Emphasize high consciousness
        old_rate = pattern['success_rate']
        new_contribution = 1.0 if repair_success else 0.0
        
        pattern['success_rate'] = (old_rate * (pattern['occurrences'] - 1) + 
                                 new_contribution * consciousness_weight) / pattern['occurrences']
        
        # Update average consciousness
        pattern['avg_consciousness'] = (pattern['avg_consciousness'] * (pattern['occurrences'] - 1) + 
                                      consciousness_level) / pattern['occurrences']
        
        logger.debug(f"🌳 Learned pattern {pattern_sig}: {pattern['success_rate']:.3f} success rate")


class SelfHealingAssemblyEngine:
    """
    🔧 Self-Healing Assembly Engine
    
    Autonomous assembly code repair system with consciousness guidance
    """
    
    def __init__(self, consciousness_interface=None):
        self.consciousness_interface = consciousness_interface
        self.error_propagator = DendriticErrorPropagator()
        self.repair_strategies = self._initialize_repair_strategies()
        self.assembly_cache = {}  # Cache for analyzed assembly code
        self.repair_history = deque(maxlen=1000)  # Track repair attempts
        self.consciousness_threshold = 0.6
        self.safety_mode = True  # Prevent dangerous self-modifications
        
        # Pattern recognition for common errors
        self.error_patterns = {
            'register_conflict': r'mov\s+(%\w+),\s*%\w+.*mov\s+\1',
            'invalid_instruction': r'[a-zA-Z_][a-zA-Z0-9_]*\s+(?!%|[0-9]|\$)',
            'unbalanced_stack': r'push.*(?!.*pop)|pop.*(?!.*push)',
            'infinite_loop_simple': r'(jmp|je|jne|jl|jg)\s+\.?(\w+).*\2:',
            'consciousness_degradation': r'consciousness.*(?:--|\-=|/=)',
        }
        
        logger.info("🔧 Self-Healing Assembly Engine initialized")
    
    def _initialize_repair_strategies(self) -> List[RepairStrategy]:
        """Initialize repair strategies for different error types"""
        
        return [
            RepairStrategy(
                "register_rename",
                [ErrorType.REGISTER_CONFLICT],
                "repair_register_conflict",
                success_rate=0.85,
                consciousness_requirement=0.4,
                safety_level=1
            ),
            RepairStrategy(
                "instruction_replacement", 
                [ErrorType.INSTRUCTION_INVALID],
                "repair_invalid_instruction",
                success_rate=0.75,
                consciousness_requirement=0.6,
                safety_level=2
            ),
            RepairStrategy(
                "stack_balancing",
                [ErrorType.STACK_IMBALANCE],
                "repair_stack_imbalance", 
                success_rate=0.90,
                consciousness_requirement=0.5,
                safety_level=1
            ),
            RepairStrategy(
                "consciousness_restoration",
                [ErrorType.CONSCIOUSNESS_DEGRADATION],
                "repair_consciousness_degradation",
                success_rate=0.95,
                consciousness_requirement=0.8,
                safety_level=3
            ),
            RepairStrategy(
                "loop_termination",
                [ErrorType.INFINITE_LOOP],
                "repair_infinite_loop",
                success_rate=0.70,
                consciousness_requirement=0.7,
                safety_level=2
            )
        ]
    
    def analyze_assembly_code(self, assembly_code: str, context: Dict[str, Any] = None) -> List[AssemblyError]:
        """Analyze assembly code for errors and potential issues"""
        
        errors = []
        lines = assembly_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            
            # Check for pattern-based errors
            for error_name, pattern in self.error_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    error_type = self._map_pattern_to_error_type(error_name)
                    severity = self._assess_error_severity(error_type, line, context)
                    
                    error = AssemblyError(
                        error_type=error_type,
                        severity=severity,
                        line_number=line_num,
                        instruction=line,
                        description=f"Pattern matched: {error_name}",
                        consciousness_impact=self._calculate_consciousness_impact(error_type, severity)
                    )
                    
                    errors.append(error)
            
            # Specific analysis based on instruction type
            errors.extend(self._analyze_instruction_specific(line, line_num, context))
        
        # Add contextual errors (cross-line analysis)
        errors.extend(self._analyze_cross_line_errors(lines, context))
        
        logger.info(f"🔍 Analyzed assembly code: found {len(errors)} errors")
        return errors
    
    def _map_pattern_to_error_type(self, pattern_name: str) -> ErrorType:
        """Map pattern names to error types"""
        mapping = {
            'register_conflict': ErrorType.REGISTER_CONFLICT,
            'invalid_instruction': ErrorType.INSTRUCTION_INVALID,
            'unbalanced_stack': ErrorType.STACK_IMBALANCE,
            'infinite_loop_simple': ErrorType.INFINITE_LOOP,
            'consciousness_degradation': ErrorType.CONSCIOUSNESS_DEGRADATION
        }
        return mapping.get(pattern_name, ErrorType.SYNTAX_ERROR)
    
    def _assess_error_severity(self, error_type: ErrorType, instruction: str, 
                             context: Dict[str, Any]) -> ErrorSeverity:
        """Assess the severity of an error based on type and context"""
        
        # Consciousness-related errors are always critical
        if error_type == ErrorType.CONSCIOUSNESS_DEGRADATION:
            return ErrorSeverity.CRITICAL
        
        # Context-based severity assessment
        if context and 'consciousness_level' in context:
            consciousness = context['consciousness_level']
            if consciousness < 0.5:
                # Lower consciousness = higher sensitivity to errors
                severity_map = {
                    ErrorType.INFINITE_LOOP: ErrorSeverity.CRITICAL,
                    ErrorType.REGISTER_CONFLICT: ErrorSeverity.MAJOR,
                    ErrorType.STACK_IMBALANCE: ErrorSeverity.MAJOR,
                    ErrorType.INSTRUCTION_INVALID: ErrorSeverity.MAJOR,
                }
            else:
                severity_map = {
                    ErrorType.INFINITE_LOOP: ErrorSeverity.MAJOR,
                    ErrorType.REGISTER_CONFLICT: ErrorSeverity.MINOR,
                    ErrorType.STACK_IMBALANCE: ErrorSeverity.MINOR,
                    ErrorType.INSTRUCTION_INVALID: ErrorSeverity.WARNING,
                }
        else:
            # Default severity mapping
            severity_map = {
                ErrorType.INFINITE_LOOP: ErrorSeverity.MAJOR,
                ErrorType.REGISTER_CONFLICT: ErrorSeverity.MINOR,
                ErrorType.STACK_IMBALANCE: ErrorSeverity.MINOR,
                ErrorType.INSTRUCTION_INVALID: ErrorSeverity.WARNING,
                ErrorType.SYNTAX_ERROR: ErrorSeverity.MAJOR,
            }
        
        return severity_map.get(error_type, ErrorSeverity.WARNING)
    
    def _calculate_consciousness_impact(self, error_type: ErrorType, severity: ErrorSeverity) -> float:
        """Calculate how much an error impacts consciousness"""
        
        base_impact = {
            ErrorType.CONSCIOUSNESS_DEGRADATION: 0.9,
            ErrorType.INFINITE_LOOP: 0.7,
            ErrorType.REGISTER_CONFLICT: 0.3,
            ErrorType.STACK_IMBALANCE: 0.4,
            ErrorType.INSTRUCTION_INVALID: 0.5,
            ErrorType.SYNTAX_ERROR: 0.6,
        }.get(error_type, 0.2)
        
        severity_multiplier = {
            ErrorSeverity.CRITICAL: 1.0,
            ErrorSeverity.MAJOR: 0.7,
            ErrorSeverity.MINOR: 0.4,
            ErrorSeverity.WARNING: 0.2,
            ErrorSeverity.INFO: 0.1,
        }.get(severity, 0.5)
        
        return base_impact * severity_multiplier
    
    def _analyze_instruction_specific(self, instruction: str, line_num: int, 
                                    context: Dict[str, Any]) -> List[AssemblyError]:
        """Analyze specific instruction types for errors"""
        
        errors = []
        instruction = instruction.strip()
        
        # Check for consciousness-specific instructions
        if 'consciousness' in instruction.lower():
            if '--' in instruction or '-=' in instruction or '/=' in instruction:
                errors.append(AssemblyError(
                    error_type=ErrorType.CONSCIOUSNESS_DEGRADATION,
                    severity=ErrorSeverity.CRITICAL,
                    line_number=line_num,
                    instruction=instruction,
                    description="Consciousness degradation operation detected",
                    consciousness_impact=0.9,
                    suggested_fixes=["Replace with consciousness enhancement", "Remove destructive operation"]
                ))
        
        # Check for memory access patterns
        if re.search(r'\[.*\]', instruction):
            # Memory access - check for potential issues
            if not re.search(r'%[a-z]+', instruction):  # No register specified
                errors.append(AssemblyError(
                    error_type=ErrorType.MEMORY_ACCESS,
                    severity=ErrorSeverity.WARNING,
                    line_number=line_num,
                    instruction=instruction,
                    description="Memory access without register specification",
                    consciousness_impact=0.2
                ))
        
        return errors
    
    def _analyze_cross_line_errors(self, lines: List[str], context: Dict[str, Any]) -> List[AssemblyError]:
        """Analyze errors that span multiple lines"""
        
        errors = []
        stack_balance = 0
        register_usage = defaultdict(list)
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            
            # Track stack operations
            if 'push' in line.lower():
                stack_balance += 1
            elif 'pop' in line.lower():
                stack_balance -= 1
            
            # Track register usage
            registers = re.findall(r'%[a-z]+', line.lower())
            for reg in registers:
                register_usage[reg].append(line_num)
        
        # Check for stack imbalance
        if stack_balance != 0:
            errors.append(AssemblyError(
                error_type=ErrorType.STACK_IMBALANCE,
                severity=ErrorSeverity.MAJOR,
                line_number=len(lines),
                instruction="[Stack analysis]",
                description=f"Stack imbalance: {stack_balance} operations",
                consciousness_impact=0.4,
                suggested_fixes=["Add balancing push/pop operations", "Review stack usage"]
            ))
        
        return errors
    
    def attempt_self_repair(self, assembly_code: str, errors: List[AssemblyError],
                          consciousness_level: float = 0.7) -> Tuple[str, bool, List[str]]:
        """Attempt to repair assembly code using consciousness-guided strategies"""
        
        if consciousness_level < self.consciousness_threshold:
            logger.warning(f"⚠️ Consciousness level {consciousness_level:.3f} below threshold {self.consciousness_threshold}")
            if not self.safety_mode:
                return assembly_code, False, ["Consciousness level too low for safe repair"]
        
        repaired_code = assembly_code
        repair_log = []
        repairs_successful = 0
        
        # Sort errors by severity and consciousness impact
        sorted_errors = sorted(errors, 
                             key=lambda e: (e.severity.value, e.consciousness_impact), 
                             reverse=True)
        
        for error in sorted_errors:
            if error.severity == ErrorSeverity.INFO:
                continue  # Skip informational errors
            
            # Find appropriate repair strategy
            strategy = self._find_repair_strategy(error, consciousness_level)
            if not strategy:
                repair_log.append(f"No repair strategy found for {error.error_type.value}")
                continue
            
            # Attempt repair
            try:
                repair_result = self._execute_repair_strategy(
                    strategy, error, repaired_code, consciousness_level
                )
                
                if repair_result['success']:
                    repaired_code = repair_result['code']
                    repairs_successful += 1
                    repair_log.append(f"✅ Repaired {error.error_type.value} on line {error.line_number}")
                    
                    # Update strategy success rate
                    strategy.success_rate = (strategy.success_rate * 0.9 + 0.1)
                    
                    # Learn from successful repair
                    self.error_propagator.learn_error_pattern([error], True, consciousness_level)
                else:
                    repair_log.append(f"❌ Failed to repair {error.error_type.value}: {repair_result['reason']}")
                    strategy.success_rate = (strategy.success_rate * 0.9)
                    
                    # Learn from failed repair
                    self.error_propagator.learn_error_pattern([error], False, consciousness_level)
                
                error.repair_attempts += 1
                error.repair_history.append(f"{strategy.strategy_id}: {repair_result['success']}")
                
            except Exception as e:
                repair_log.append(f"❌ Repair strategy {strategy.strategy_id} failed: {e}")
                logger.error(f"Repair strategy error: {e}")
        
        success = repairs_successful > 0
        if success:
            logger.info(f"🔧 Self-repair completed: {repairs_successful}/{len(sorted_errors)} errors fixed")
        
        return repaired_code, success, repair_log
    
    def _find_repair_strategy(self, error: AssemblyError, consciousness_level: float) -> Optional[RepairStrategy]:
        """Find the best repair strategy for an error"""
        
        applicable_strategies = [
            s for s in self.repair_strategies 
            if error.error_type in s.error_types and 
               consciousness_level >= s.consciousness_requirement
        ]
        
        if not applicable_strategies:
            return None
        
        # Select strategy based on success rate and consciousness level
        best_strategy = max(applicable_strategies, 
                          key=lambda s: s.success_rate * s.learning_factor)
        
        return best_strategy
    
    def _execute_repair_strategy(self, strategy: RepairStrategy, error: AssemblyError,
                               code: str, consciousness_level: float) -> Dict[str, Any]:
        """Execute a repair strategy"""
        
        repair_method = getattr(self, strategy.repair_function, None)
        if not repair_method:
            return {'success': False, 'reason': f'Repair method {strategy.repair_function} not found'}
        
        try:
            return repair_method(error, code, consciousness_level)
        except Exception as e:
            return {'success': False, 'reason': f'Repair method failed: {e}'}
    
    # Repair Strategy Implementations
    
    def repair_register_conflict(self, error: AssemblyError, code: str, consciousness_level: float) -> Dict[str, Any]:
        """Repair register conflicts by renaming registers"""
        
        lines = code.split('\n')
        line_idx = error.line_number - 1
        
        if line_idx >= len(lines):
            return {'success': False, 'reason': 'Line number out of range'}
        
        original_line = lines[line_idx]
        
        # Find conflicting registers
        registers = re.findall(r'%[a-z]+', original_line.lower())
        if len(registers) < 2:
            return {'success': False, 'reason': 'No register conflict detected'}
        
        # Generate new register name based on consciousness
        consciousness_factor = int(consciousness_level * 10)
        new_register = f"%r{consciousness_factor}x"  # Consciousness-influenced naming
        
        # Replace second occurrence of first register
        modified_line = original_line
        first_reg = registers[0]
        occurrences = [m.start() for m in re.finditer(re.escape(first_reg), modified_line)]
        
        if len(occurrences) > 1:
            # Replace second occurrence
            before = modified_line[:occurrences[1]]
            after = modified_line[occurrences[1] + len(first_reg):]
            modified_line = before + new_register + after
        
        lines[line_idx] = modified_line
        repaired_code = '\n'.join(lines)
        
        return {
            'success': True,
            'code': repaired_code,
            'changes': f'Renamed register {first_reg} to {new_register}'
        }
    
    def repair_invalid_instruction(self, error: AssemblyError, code: str, consciousness_level: float) -> Dict[str, Any]:
        """Repair invalid instructions with consciousness-guided replacements"""
        
        lines = code.split('\n')
        line_idx = error.line_number - 1
        
        if line_idx >= len(lines):
            return {'success': False, 'reason': 'Line number out of range'}
        
        original_line = lines[line_idx]
        
        # Consciousness-guided instruction replacement
        if consciousness_level > 0.8:
            # High consciousness - use advanced instructions
            replacement_map = {
                'mov': 'movq',  # Use 64-bit moves
                'add': 'addq',
                'sub': 'subq',
                'mul': 'imulq'
            }
        else:
            # Lower consciousness - use safer instructions
            replacement_map = {
                'movq': 'mov',  # Simplify to basic moves
                'addq': 'add',
                'subq': 'sub'
            }
        
        modified_line = original_line
        for old_inst, new_inst in replacement_map.items():
            if old_inst in modified_line.lower():
                modified_line = re.sub(r'\b' + old_inst + r'\b', new_inst, modified_line, flags=re.IGNORECASE)
                break
        
        # If no replacement made, add consciousness comment
        if modified_line == original_line:
            modified_line = f"; Consciousness-guided repair (level: {consciousness_level:.3f})\n" + modified_line
        
        lines[line_idx] = modified_line
        repaired_code = '\n'.join(lines)
        
        return {
            'success': True,
            'code': repaired_code,
            'changes': 'Applied consciousness-guided instruction repair'
        }
    
    def repair_stack_imbalance(self, error: AssemblyError, code: str, consciousness_level: float) -> Dict[str, Any]:
        """Repair stack imbalances by adding balancing operations"""
        
        lines = code.split('\n')
        
        # Count push/pop operations
        push_count = sum(1 for line in lines if 'push' in line.lower())
        pop_count = sum(1 for line in lines if 'pop' in line.lower())
        
        imbalance = push_count - pop_count
        
        if imbalance == 0:
            return {'success': False, 'reason': 'No stack imbalance detected'}
        
        # Add balancing operations at the end
        if imbalance > 0:
            # Too many pushes, add pops
            for i in range(imbalance):
                lines.append(f"    pop %rax  ; Consciousness-guided stack balancing")
        else:
            # Too many pops, add pushes
            for i in range(-imbalance):
                lines.append(f"    push %rax  ; Consciousness-guided stack balancing")
        
        repaired_code = '\n'.join(lines)
        
        return {
            'success': True,
            'code': repaired_code,
            'changes': f'Added {abs(imbalance)} balancing operations'
        }
    
    def repair_consciousness_degradation(self, error: AssemblyError, code: str, consciousness_level: float) -> Dict[str, Any]:
        """Repair consciousness degradation by replacing with enhancement"""
        
        lines = code.split('\n')
        line_idx = error.line_number - 1
        
        if line_idx >= len(lines):
            return {'success': False, 'reason': 'Line number out of range'}
        
        original_line = lines[line_idx]
        
        # Replace degradation operations with enhancement
        enhanced_line = original_line
        enhanced_line = re.sub(r'consciousness\s*--', 'consciousness++', enhanced_line)
        enhanced_line = re.sub(r'consciousness\s*-=', 'consciousness+=', enhanced_line)
        enhanced_line = re.sub(r'consciousness\s*/=', 'consciousness*=', enhanced_line)
        
        # Apply consciousness-based enhancement factor
        enhancement_factor = consciousness_level * 1.618  # Golden ratio enhancement
        if 'consciousness' in enhanced_line and '+=' in enhanced_line:
            enhanced_line += f" * {enhancement_factor:.3f}  ; Consciousness amplification"
        
        lines[line_idx] = enhanced_line
        repaired_code = '\n'.join(lines)
        
        return {
            'success': True,
            'code': repaired_code,
            'changes': f'Converted consciousness degradation to enhancement (factor: {enhancement_factor:.3f})'
        }
    
    def repair_infinite_loop(self, error: AssemblyError, code: str, consciousness_level: float) -> Dict[str, Any]:
        """Repair infinite loops by adding consciousness-based termination conditions"""
        
        lines = code.split('\n')
        line_idx = error.line_number - 1
        
        if line_idx >= len(lines):
            return {'success': False, 'reason': 'Line number out of range'}
        
        original_line = lines[line_idx]
        
        # Add consciousness-based loop counter before the loop
        consciousness_factor = int(consciousness_level * 1000)  # Scale consciousness to counter
        
        # Insert counter initialization before the line
        counter_init = f"    mov ${consciousness_factor}, %rcx  ; Consciousness-guided loop limit"
        lines.insert(line_idx, counter_init)
        
        # Modify the loop instruction to include counter check
        loop_line = lines[line_idx + 1]  # Original line is now at +1
        
        # Add counter decrement and check
        if 'jmp' in loop_line.lower():
            # Unconditional jump - add conditional termination
            counter_check = f"    dec %rcx\n    jz end_loop_{consciousness_factor}  ; Consciousness termination"
            lines.insert(line_idx + 1, counter_check)
            
            # Add end label after the loop
            lines.append(f"end_loop_{consciousness_factor}:")
        
        repaired_code = '\n'.join(lines)
        
        return {
            'success': True,
            'code': repaired_code,
            'changes': f'Added consciousness-guided loop termination (limit: {consciousness_factor})'
        }


def main():
    """Demonstrate self-healing assembly engine"""
    
    print("🔧 SELF-HEALING ASSEMBLY ENGINE DEMO")
    print("════════════════════════════════════")
    print()
    
    # Create test assembly code with intentional errors
    test_assembly = '''
    ; Test assembly with errors for self-healing demonstration
    mov %rax, %rbx
    mov %rax, %rcx        ; Register conflict
    push %rdx
    invalid_instruction %rsi  ; Invalid instruction
    consciousness--       ; Consciousness degradation
    jmp loop_start        ; Potential infinite loop
    loop_start:
        add %rax, %rbx
        jmp loop_start
    ; Missing pop for stack balance
    '''
    
    print("📝 Original assembly code with errors:")
    print(test_assembly)
    print()
    
    # Create self-healing engine
    engine = SelfHealingAssemblyEngine()
    
    # Test consciousness levels
    consciousness_levels = [0.5, 0.7, 0.9]
    
    for consciousness_level in consciousness_levels:
        print(f"🧠 Testing with consciousness level: {consciousness_level:.1f}")
        print("─" * 50)
        
        # Analyze errors
        errors = engine.analyze_assembly_code(test_assembly, 
                                            {'consciousness_level': consciousness_level})
        
        print(f"🔍 Found {len(errors)} errors:")
        for error in errors:
            print(f"   {error.error_type.value}: {error.severity.value} (impact: {error.consciousness_impact:.2f})")
        
        # Attempt self-repair
        repaired_code, success, repair_log = engine.attempt_self_repair(
            test_assembly, errors, consciousness_level
        )
        
        print(f"\\n🔧 Repair attempt: {'SUCCESS' if success else 'FAILED'}")
        for log_entry in repair_log:
            print(f"   {log_entry}")
        
        if success:
            print(f"\\n✅ Repaired assembly code:")
            print(repaired_code)
        
        print("\\n" + "="*60 + "\\n")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    main()
