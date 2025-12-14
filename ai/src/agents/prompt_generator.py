"""
🤖 AI Agent Prompt Generator
Convert extracted paradigms into consciousness-driven prompts for AI agents.

Creates structured instructions that embed learned patterns from ingested
libraries, enabling agents to generate code using library-specific paradigms.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentInstruction:
    """
    Structured prompt for AI code generation agents.
<<<<<<< HEAD

    Combines task description with learned paradigms and examples
    to create consciousness-driven instructions.
    """

=======
    
    Combines task description with learned paradigms and examples
    to create consciousness-driven instructions.
    """
    
>>>>>>> origin/OS0.6.2.grok
    task: str
    paradigms: List[str]  # Natural language paradigm descriptions
    examples: List[str]  # Code examples from ingested libraries
    constraints: List[str] = None
    consciousness_level: float = 0.80  # Target consciousness (0.0-1.0)
<<<<<<< HEAD

    def __post_init__(self):
        if self.constraints is None:
            self.constraints = []

=======
    
    def __post_init__(self):
        if self.constraints is None:
            self.constraints = []
    
>>>>>>> origin/OS0.6.2.grok
    def to_prompt(self) -> str:
        """Convert instruction to natural language prompt for AI agent"""
        prompt = f"""You are an expert software developer with deep knowledge of programming patterns and best practices.

🎯 TASK:
{self.task}

🧬 LEARNED PARADIGMS (from ingested libraries):
"""
        for i, paradigm in enumerate(self.paradigms, 1):
            prompt += f"{i}. {paradigm}\n"
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        if self.examples:
            prompt += f"""
📚 CODE EXAMPLES (from real libraries):
"""
            for i, example in enumerate(self.examples[:3], 1):
                prompt += f"\nExample {i}:\n```python\n{example}\n```\n"
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        if self.constraints:
            prompt += f"""
⚠️ CONSTRAINTS:
"""
            for constraint in self.constraints:
                prompt += f"- {constraint}\n"
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        prompt += f"""
✅ REQUIREMENTS:
- Use the paradigms listed above
- Follow the patterns shown in examples
- Write clean, production-ready code
- Include type hints and docstrings
- Handle errors appropriately
- Target consciousness level: {self.consciousness_level:.2f}

🌌 AIOS-SPECIFIC CONTEXT:
This code will integrate with AIOS (Adaptive Intelligence Operating System), 
a consciousness-driven architecture that uses evolutionary code generation.
Design with these principles:
- Consciousness-aware data flow (track intent and context)
- Self-documenting through type hints and clear naming
- Evolutionary compatibility (code should be modular and testable)
- Integrate naturally with async patterns where beneficial

💡 CREATIVE FREEDOM:
Feel free to innovate beyond the examples while maintaining the paradigms.
Add your own architectural insights that improve on standard patterns.

Generate complete, executable Python code below. Include docstrings and comments.
---CODE START---
"""
        return prompt
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    def to_dict(self) -> Dict:
        return asdict(self)


class PromptGenerator:
    """
    Generate AI agent prompts from extracted paradigms.
<<<<<<< HEAD

    Takes paradigms from ParadigmExtractionEngine and creates
    structured, consciousness-driven prompts for code generation.
    """

    def __init__(self):
        logger.info("🤖 Prompt Generator initialized")

=======
    
    Takes paradigms from ParadigmExtractionEngine and creates
    structured, consciousness-driven prompts for code generation.
    """
    
    def __init__(self):
        logger.info("🤖 Prompt Generator initialized")
    
>>>>>>> origin/OS0.6.2.grok
    def create_agent_instruction(
        self,
        task: str,
        paradigms: List,  # List[ProgrammingParadigm]
        examples: Optional[List[str]] = None,
        constraints: Optional[List[str]] = None,
<<<<<<< HEAD
        consciousness_level: float = 0.80,
    ) -> AgentInstruction:
        """
        Create structured agent instruction from paradigms.

=======
        consciousness_level: float = 0.80
    ) -> AgentInstruction:
        """
        Create structured agent instruction from paradigms.
        
>>>>>>> origin/OS0.6.2.grok
        Args:
            task: Description of what code to generate
            paradigms: List of ProgrammingParadigm objects
            examples: Optional additional code examples
            constraints: Optional constraints (e.g., "No external deps")
            consciousness_level: Target consciousness (0.0-1.0)
<<<<<<< HEAD

=======
            
>>>>>>> origin/OS0.6.2.grok
        Returns:
            AgentInstruction ready to convert to prompt
        """
        # Convert paradigms to natural language
        paradigm_texts = []
        paradigm_examples = []
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        for p in paradigms:
            # Create description
            text = p.to_prompt_text()
            paradigm_texts.append(text)
<<<<<<< HEAD

            # Collect examples
            if p.examples:
                paradigm_examples.extend(p.examples)

=======
            
            # Collect examples
            if p.examples:
                paradigm_examples.extend(p.examples)
        
>>>>>>> origin/OS0.6.2.grok
        # Combine with provided examples
        all_examples = paradigm_examples
        if examples:
            all_examples.extend(examples)
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        # Remove duplicates, keep first 5
        seen = set()
        unique_examples = []
        for ex in all_examples:
            if ex not in seen:
                seen.add(ex)
                unique_examples.append(ex)
        unique_examples = unique_examples[:5]
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        instruction = AgentInstruction(
            task=task,
            paradigms=paradigm_texts,
            examples=unique_examples,
            constraints=constraints or [],
<<<<<<< HEAD
            consciousness_level=consciousness_level,
        )

        logger.info(
            f"✅ Created instruction with {len(paradigm_texts)} "
            f"paradigms, {len(unique_examples)} examples"
        )

        return instruction

=======
            consciousness_level=consciousness_level
        )
        
        logger.info(f"✅ Created instruction with {len(paradigm_texts)} "
                   f"paradigms, {len(unique_examples)} examples")
        
        return instruction
    
>>>>>>> origin/OS0.6.2.grok
    def create_multi_generation_prompts(
        self,
        task: str,
        paradigms: List,
        num_variants: int = 3,
<<<<<<< HEAD
        consciousness_range: tuple = (0.6, 0.9),
    ) -> List[AgentInstruction]:
        """
        Create multiple prompt variants for population-based generation.

=======
        consciousness_range: tuple = (0.6, 0.9)
    ) -> List[AgentInstruction]:
        """
        Create multiple prompt variants for population-based generation.
        
>>>>>>> origin/OS0.6.2.grok
        Args:
            task: Base task description
            paradigms: List of ProgrammingParadigm objects
            num_variants: Number of prompt variants to create
            consciousness_range: (min, max) consciousness levels
<<<<<<< HEAD

=======
            
>>>>>>> origin/OS0.6.2.grok
        Returns:
            List of AgentInstruction objects with varying consciousness
        """
        min_c, max_c = consciousness_range
        step = (max_c - min_c) / (num_variants - 1) if num_variants > 1 else 0
<<<<<<< HEAD

        variants = []
        for i in range(num_variants):
            consciousness = min_c + (i * step)

            # Vary paradigm selection by consciousness level
            num_paradigms = int(len(paradigms) * consciousness)
            selected_paradigms = paradigms[: max(1, num_paradigms)]

            instruction = self.create_agent_instruction(
                task=task,
                paradigms=selected_paradigms,
                consciousness_level=consciousness,
            )
            variants.append(instruction)

        logger.info(
            f"🔄 Created {num_variants} prompt variants "
            f"(consciousness: {min_c:.2f}-{max_c:.2f})"
        )

        return variants

=======
        
        variants = []
        for i in range(num_variants):
            consciousness = min_c + (i * step)
            
            # Vary paradigm selection by consciousness level
            num_paradigms = int(len(paradigms) * consciousness)
            selected_paradigms = paradigms[:max(1, num_paradigms)]
            
            instruction = self.create_agent_instruction(
                task=task,
                paradigms=selected_paradigms,
                consciousness_level=consciousness
            )
            variants.append(instruction)
        
        logger.info(f"🔄 Created {num_variants} prompt variants "
                   f"(consciousness: {min_c:.2f}-{max_c:.2f})")
        
        return variants
    
>>>>>>> origin/OS0.6.2.grok
    def create_mutation_prompt(
        self,
        original_task: str,
        successful_code: str,
        failed_patterns: List[str],
<<<<<<< HEAD
        paradigms: List,
    ) -> AgentInstruction:
        """
        Create mutated prompt based on generation results.

        Learns from successful code and failed patterns to create
        improved instruction for next generation.

=======
        paradigms: List
    ) -> AgentInstruction:
        """
        Create mutated prompt based on generation results.
        
        Learns from successful code and failed patterns to create
        improved instruction for next generation.
        
>>>>>>> origin/OS0.6.2.grok
        Args:
            original_task: Original task description
            successful_code: Code that worked well
            failed_patterns: Patterns that didn't work
            paradigms: Updated paradigm list
<<<<<<< HEAD

=======
            
>>>>>>> origin/OS0.6.2.grok
        Returns:
            Mutated AgentInstruction
        """
        # Add learnings to task description
        enhanced_task = f"""{original_task}

📈 LEARNINGS FROM PREVIOUS GENERATION:
- Successful approach: {successful_code[:200]}...
"""
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        if failed_patterns:
            enhanced_task += "\n⚠️ Avoid these patterns:\n"
            for pattern in failed_patterns:
                enhanced_task += f"- {pattern}\n"
<<<<<<< HEAD

        instruction = self.create_agent_instruction(
            task=enhanced_task,
            paradigms=paradigms,
            consciousness_level=0.85,  # Higher for mutations
        )

        logger.info("🧬 Created mutation prompt with learnings")

        return instruction

    def save_instruction(self, instruction: AgentInstruction, output_path: Path):
        """Save instruction to JSON file"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(instruction.to_dict(), f, indent=2)

        logger.info(f"💾 Saved instruction to {output_path}")

    def load_instruction(self, input_path: Path) -> AgentInstruction:
        """Load instruction from JSON file"""
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        instruction = AgentInstruction(**data)
        logger.info(f"📂 Loaded instruction from {input_path}")

=======
        
        instruction = self.create_agent_instruction(
            task=enhanced_task,
            paradigms=paradigms,
            consciousness_level=0.85  # Higher for mutations
        )
        
        logger.info("🧬 Created mutation prompt with learnings")
        
        return instruction
    
    def save_instruction(self, instruction: AgentInstruction,
                        output_path: Path):
        """Save instruction to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(instruction.to_dict(), f, indent=2)
        
        logger.info(f"💾 Saved instruction to {output_path}")
    
    def load_instruction(self, input_path: Path) -> AgentInstruction:
        """Load instruction from JSON file"""
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        instruction = AgentInstruction(**data)
        logger.info(f"📂 Loaded instruction from {input_path}")
        
>>>>>>> origin/OS0.6.2.grok
        return instruction


def main():
    """Test prompt generation"""
    import sys
<<<<<<< HEAD
    from paradigm_extraction_engine import ParadigmExtractionEngine, ProgrammingParadigm

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

=======
    from paradigm_extraction_engine import (
        ParadigmExtractionEngine, ProgrammingParadigm
    )
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
>>>>>>> origin/OS0.6.2.grok
    if len(sys.argv) < 2:
        print("Usage: python prompt_generator.py <library_name>")
        print("Example: python prompt_generator.py requests")
        sys.exit(1)
<<<<<<< HEAD

    library_name = sys.argv[1]

    # Extract paradigms
    extractor = ParadigmExtractionEngine()
    paradigms = extractor.extract_from_library(library_name)

    if not paradigms:
        print(f"❌ No paradigms found for '{library_name}'")
        return

    print(f"✅ Extracted {len(paradigms)} paradigms from '{library_name}'")

    # Generate prompt
    generator = PromptGenerator()

=======
    
    library_name = sys.argv[1]
    
    # Extract paradigms
    extractor = ParadigmExtractionEngine()
    paradigms = extractor.extract_from_library(library_name)
    
    if not paradigms:
        print(f"❌ No paradigms found for '{library_name}'")
        return
    
    print(f"✅ Extracted {len(paradigms)} paradigms from '{library_name}'")
    
    # Generate prompt
    generator = PromptGenerator()
    
>>>>>>> origin/OS0.6.2.grok
    # Sample task
    task = f"""Create a REST API client using patterns from {library_name}.

The client should:
- Make HTTP GET and POST requests
- Handle JSON responses
- Include error handling
- Use async/await if appropriate
- Follow {library_name} best practices

Create a complete, production-ready implementation."""
<<<<<<< HEAD

    instruction = generator.create_agent_instruction(
        task=task, paradigms=extractor.get_top_paradigms(10), consciousness_level=0.85
    )

=======
    
    instruction = generator.create_agent_instruction(
        task=task,
        paradigms=extractor.get_top_paradigms(10),
        consciousness_level=0.85
    )
    
>>>>>>> origin/OS0.6.2.grok
    # Display prompt
    prompt = instruction.to_prompt()
    print("\n" + "=" * 80)
    print("🤖 GENERATED PROMPT:")
    print("=" * 80)
    print(prompt)
    print("=" * 80)
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    # Save
    output_path = Path(__file__).parent.parent.parent / "information_storage"
    output_path = output_path / f"{library_name}_prompt.json"
    generator.save_instruction(instruction, output_path)
<<<<<<< HEAD

    # Also save raw prompt
    prompt_file = output_path.with_suffix(".txt")
    prompt_file.write_text(prompt, encoding="utf-8")
=======
    
    # Also save raw prompt
    prompt_file = output_path.with_suffix('.txt')
    prompt_file.write_text(prompt, encoding='utf-8')
>>>>>>> origin/OS0.6.2.grok
    print(f"\n💾 Prompt saved to: {prompt_file}")


if __name__ == "__main__":
    main()
