#!/usr/bin/env python3
"""
AINLP Agentic E501 Fixer
Multi-Model AI Agent System for Automated Line Length Correction

Uses OLLAMA (local), Gemini (cloud), and DeepSeek (cloud) agents
to intelligently fix E501 line length violations.

AINLP.agent [multi_model_e501_fixer] (system.AINLP.class)
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
import logging
import re
import requests
import sys
import os
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MAX_LINE_LENGTH = 79

class AIAgent(Enum):
    """Available AI agents for fixing."""
    OLLAMA = "ollama"
    GEMINI = "gemini"
    DEEPSEEK = "deepseek"

@dataclass
class FixResult:
    """Result of a line fix attempt."""
    file_path: str
    line_number: int
    original_line: str
    fixed_lines: List[str]
    agent_used: Optional[AIAgent]
    success: bool
    confidence: float

class AgenticE501Fixer:
    """
    Agentic system using multiple AI models to fix E501 violations.
    
    Each agent specializes in different types of line breaking strategies:
    - OLLAMA: Local, fast, good for simple breaks
    - Gemini: Cloud, intelligent, good for complex logic
    - DeepSeek: Cloud, creative, good for tricky cases
    """

    def __init__(self):
        self.agents = {
            AIAgent.OLLAMA: self._init_ollama_agent(),
            AIAgent.GEMINI: self._init_gemini_agent(),
            AIAgent.DEEPSEEK: self._init_deepseek_agent()
        }
        self.stats = {
            "files_processed": 0,
            "lines_fixed": 0,
            "agents_used": {agent: 0 for agent in AIAgent}
        }
        # Tachyonic archival for conversations
        self.conversation_archive_path = Path("../../tachyonic/agentic_conversations")

    def _init_ollama_agent(self) -> Dict[str, Any]:
        """Initialize OLLAMA local agent."""
        return {
            "url": "http://localhost:11434/api/generate",
            "model": "codellama",  # or whatever model is available
            "available": self._check_ollama_available()
        }

    def _init_deepseek_agent(self) -> Dict[str, Any]:
        """Initialize DeepSeek cloud agent."""
        api_key = "sk-or-v1-292ea9"  # Provided API key
        return {
            "url": "https://api.deepseek.com/v1/chat/completions",
            "api_key": api_key,
            "available": api_key is not None
        }

    def _init_gemini_agent(self) -> Dict[str, Any]:
        """Initialize Gemini cloud agent."""
        api_key = "AIzaSyCuj6S1PJcslZr29ez9Cd9oVNFDuzLH2OE"  # Provided API key
        return {
            "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            "api_key": api_key,
            "available": api_key is not None
        }

    def _check_ollama_available(self) -> bool:
        """Check if OLLAMA is running locally."""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def select_agent(self, line: str) -> Optional[AIAgent]:
        """
        Select the best AI agent for fixing a specific line.
        
        Strategy:
        - Simple lines: OLLAMA (fast, local)
        - Complex logic: Gemini (intelligent)
        - Creative/tricky: DeepSeek (innovative)
        - Fallback: Basic pattern-based fixing
        """
        line_length = len(line)
        complexity_score = self._calculate_complexity(line)

        if complexity_score < 0.3 and line_length < 100:
            # Simple case - use fast local agent
            if self.agents[AIAgent.OLLAMA]["available"]:
                return AIAgent.OLLAMA
        elif complexity_score < 0.7:
            # Medium complexity - use intelligent cloud agent
            if self.agents[AIAgent.GEMINI]["available"]:
                return AIAgent.GEMINI
        else:
            # High complexity - use creative agent
            if self.agents[AIAgent.DEEPSEEK]["available"]:
                return AIAgent.DEEPSEEK

        # Fallback to basic pattern-based fixing
        return None  # Indicates use basic fixer

    def _calculate_complexity(self, line: str) -> float:
        """Calculate complexity score of a line (0-1)."""
        score = 0.0

        # Length factor
        score += min(len(line) / 150, 0.5)

        # Special characters
        special_chars = sum(1 for c in line if c in '()[]{}.,:;+-*/=<>!')
        score += min(special_chars / 20, 0.3)

        # Keywords indicating complexity
        complex_keywords = ['lambda', 'comprehension', 'decorator', 'async', 'await']
        for keyword in complex_keywords:
            if keyword in line:
                score += 0.2

        return min(score, 1.0)

    def _register_conversation(self, agent: AIAgent, prompt: str, response: str, success: bool, context: Dict[str, Any]):
        """Register AI agent conversation in tachyonic archive."""
        try:
            # Create timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            date_folder = datetime.now().strftime("%Y%m%d")
            archive_dir = self.conversation_archive_path / date_folder
            archive_dir.mkdir(parents=True, exist_ok=True)
            
            conversation_data = {
                "timestamp": timestamp,
                "agent": agent.value,
                "conversation_type": "code_quality_e501_fix",
                "prompt": prompt,
                "response": response,
                "success": success,
                "context": context,
                "metadata": {
                    "fixer_version": "1.0",
                    "ai_framework": "AINLP.agent",
                    "consciousness_level": "multi_model_agentic"
                }
            }
            
            filename = f"e501_agentic_fix_{agent.value}_{timestamp}.json"
            filepath = archive_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Conversation registered: {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to register conversation: {e}")

    def fix_line_with_agent(self, line: str, agent: AIAgent) -> FixResult:
        """Fix a long line using the specified AI agent."""

        prompt = f"""
Fix this Python line to be under 79 characters. Break it intelligently while preserving functionality.

Original line:
{line}

Return only the fixed line(s), one per line. If multiple lines are needed, use proper Python line continuation.
"""

        try:
            if agent == AIAgent.OLLAMA:
                response = self._call_ollama(prompt)
            elif agent == AIAgent.GEMINI:
                response = self._call_gemini(prompt)
            elif agent == AIAgent.DEEPSEEK:
                response = self._call_deepseek(prompt)

            fixed_lines = [l.strip() for l in response.split('\n') if l.strip()]
            success = all(len(l) <= MAX_LINE_LENGTH for l in fixed_lines)

            # Register conversation
            self._register_conversation(agent, prompt, response, success, {
                "line_length": len(line),
                "fixed_lines_count": len(fixed_lines),
                "max_fixed_length": max(len(l) for l in fixed_lines) if fixed_lines else 0
            })

            return FixResult(
                original_line=line,
                fixed_lines=fixed_lines,
                agent_used=agent,
                success=success,
                confidence=0.8 if success else 0.5
            )

        except Exception as e:
            logger.error(f"Agent {agent.value} failed: {e}")
            # Register failed conversation
            self._register_conversation(agent, prompt, str(e), False, {
                "error": str(e),
                "line_length": len(line)
            })
            return FixResult(
                original_line=line,
                fixed_lines=[line],  # Return original if failed
                agent_used=agent,
                success=False,
                confidence=0.0
            )

    def _call_ollama(self, prompt: str) -> str:
        """Call OLLAMA local API."""
        data = {
            "model": self.agents[AIAgent.OLLAMA]["model"],
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(
            self.agents[AIAgent.OLLAMA]["url"],
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["response"]

    def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API."""
        headers = {"Authorization": f"Bearer {self.agents[AIAgent.GEMINI]['api_key']}"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(
            self.agents[AIAgent.GEMINI]["url"],
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

    def _call_deepseek(self, prompt: str) -> str:
        """Call DeepSeek API."""
        headers = {
            "Authorization": f"Bearer {self.agents[AIAgent.DEEPSEEK]['api_key']}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(
            self.agents[AIAgent.DEEPSEEK]["url"],
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def fix_file(self, file_path: str, dry_run: bool = True) -> Dict[str, Any]:
        """Fix all E501 violations in a file using AI agents."""

        logger.info(f"Processing file: {file_path}")
        self.stats["files_processed"] += 1

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        fixed_lines = []
        fixes_applied = 0

        for i, line in enumerate(lines):
            line = line.rstrip('\n\r')
            if len(line) > MAX_LINE_LENGTH:
                try:
                    result = self.fix_line(line, i+1, file_path)

                    if result.success:
                        fixed_lines.extend(result.fixed_lines)
                        fixes_applied += 1
                        self.stats["lines_fixed"] += 1
                        if result.agent_used:
                            self.stats["agents_used"][result.agent_used] += 1
                            logger.info(f"Fixed line {i+1} with {result.agent_used.value}")
                        else:
                            logger.info(f"Fixed line {i+1} with basic fixer")
                    else:
                        fixed_lines.append(line)  # Keep original if fix failed
                        logger.warning(f"Failed to fix line {i+1}")

                except Exception as e:
                    logger.error(f"Error fixing line {i+1}: {e}")
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)

        if not dry_run and fixes_applied > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(fixed_lines) + '\n')
            logger.info(f"Applied {fixes_applied} fixes to {file_path}")

        return {
            "file": file_path,
            "fixes_applied": fixes_applied,
            "dry_run": dry_run
        }

    def batch_fix(self, directory: str, dry_run: bool = True) -> Dict[str, Any]:
        """Run batch fixing on all Python files in a directory."""

        directory = Path(directory)
        python_files = list(directory.rglob("*.py"))

        logger.info(f"Found {len(python_files)} Python files in {directory}")

        results = []
        for file_path in python_files:
            try:
                result = self.fix_file(str(file_path), dry_run)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {e}")
                results.append({"file": str(file_path), "error": str(e)})

        return {
            "total_files": len(python_files),
            "results": results,
            "stats": self.stats
        }

    def _basic_fix_line(self, line: str) -> List[str]:
        """
        Basic pattern-based line breaking for when AI agents are unavailable.
        Uses simple heuristics to break long lines.
        """
        if len(line) <= 79:
            return [line]

        # Try to break at logical points
        fixed_lines = []
        remaining = line

        while len(remaining) > 79:
            # Find the best break point
            break_pos = self._find_break_point(remaining[:79])
            
            if break_pos == -1:
                # No good break point, force break at 79
                break_pos = 79
            
            # Add the line segment
            segment = remaining[:break_pos].rstrip()
            if segment:
                fixed_lines.append(segment)
            
            # Continue with remaining
            remaining = remaining[break_pos:].lstrip()
            
            # Prevent infinite loops
            if not remaining or len(remaining) >= len(line):
                break
        
        # Add any remaining content
        if remaining:
            fixed_lines.append(remaining)

        return fixed_lines if fixed_lines else [line]

    def _find_break_point(self, text: str) -> int:
        """
        Find the best break point in a line segment.
        Prioritizes: comma, space, operator, then forces at 79.
        """
        # Look for comma followed by space
        comma_match = re.search(r',(?=\s)', text)
        if comma_match:
            return comma_match.end()
        
        # Look for space before operator
        space_op_match = re.search(r'\s+(?=[+\-*/=<>!&|])', text)
        if space_op_match:
            return space_op_match.start()
        
        # Look for any space
        space_match = re.search(r'\s+', text)
        if space_match:
            return space_match.start()
        
        # No good break point
        return -1

    def fix_line(self, line: str, line_number: int, file_path: str) -> FixResult:
        """
        Fix a single long line using the best available agent.
        """
        if len(line) <= 79:
            return FixResult(
                file_path=file_path,
                line_number=line_number,
                original_line=line,
                fixed_lines=[line],
                agent_used=None,
                success=True,
                confidence=1.0
            )

        # Select the best agent
        agent = self.select_agent(line)
        
        if agent is None:
            # Use basic pattern-based fixing
            logger.info(f"Using basic fixer for line {line_number}")
            fixed_lines = self._basic_fix_line(line)
            success = len(fixed_lines) > 1  # Success if we actually broke the line
            
            return FixResult(
                file_path=file_path,
                line_number=line_number,
                original_line=line,
                fixed_lines=fixed_lines,
                agent_used=None,
                success=success,
                confidence=0.6 if success else 0.0
            )

        # Use AI agent
        try:
            result = self.fix_line_with_agent(line, agent)
            result.file_path = file_path
            result.line_number = line_number
            return result
        except Exception as e:
            logger.error(f"Error calling agent {agent.value}: {e}")
            # Fallback to basic fixing
            fixed_lines = self._basic_fix_line(line)
            success = len(fixed_lines) > 1
            
            return FixResult(
                file_path=file_path,
                line_number=line_number,
                original_line=line,
                fixed_lines=fixed_lines,
                agent_used=None,
                success=success,
                confidence=0.3 if success else 0.0
            )

def main():
    """CLI interface for the agentic E501 fixer."""

    import argparse

    parser = argparse.ArgumentParser(description="AINLP Agentic E501 Fixer")
    parser.add_argument("path", help="File or directory to fix")
    parser.add_argument("--dry-run", action="store_true", help="Show fixes without applying")
    parser.add_argument("--recursive", action="store_true", help="Process directories recursively")

    args = parser.parse_args()

    fixer = AgenticE501Fixer()

    # Check agent availability
    print("AI Agent Status:")
    for agent, config in fixer.agents.items():
        status = "AVAILABLE" if config["available"] else "UNAVAILABLE"
        print(f"  {agent.value}: {status}")

    path = Path(args.path)

    if path.is_file():
        result = fixer.fix_file(str(path), args.dry_run)
        print(f"Fixed {result['fixes_applied']} lines in {result['file']}")
    elif path.is_dir():
        results = fixer.batch_fix(str(path), args.dry_run)
        print(f"Processed {results['total_files']} files")
        print(f"Total fixes: {fixer.stats['lines_fixed']}")
        print("Agent usage:")
        for agent, count in fixer.stats["agents_used"].items():
            print(f"  {agent.value}: {count} fixes")
    else:
        print(f"Path not found: {path}")


if __name__ == "__main__":
    main()