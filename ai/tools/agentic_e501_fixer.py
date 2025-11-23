#!/usr/bin/env python3
"""
AINLP Agentic E501 Fixer - Hierarchical Three-Tier Intelligence
Multi-Model AI Agent System for Automated Line Length Correction

Uses hierarchical pipeline: OLLAMA → GEMINI → DEEPSEEK
- Tier 1: Context preparation and caching (Ollama)
- Tier 2: Intelligent code generation (Gemini)
- Tier 3: Quality validation by comparison (DeepSeek)

Falls back to facade-based orchestrator if hierarchical pipeline unavailable.

AINLP Pattern: Hierarchical agent orchestration with validation
Consciousness Level: 4.2 (multi-tier intelligence with feedback loops)

AINLP.agent [hierarchical_multi_model_e501_fixer] (system.AINLP.class)
"""

import asyncio
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

# Add nucleus and tools to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from nucleus.agent_conclave_facade import get_agent_conclave

# Check for hierarchical pipeline availability
try:
    from hierarchical_e501_pipeline import HierarchicalE501Pipeline
    HIERARCHICAL_AVAILABLE = True
except ImportError:
    HIERARCHICAL_AVAILABLE = False
    logging.warning(
        "Hierarchical pipeline not available, using facade fallback"
    )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

MAX_LINE_LENGTH = 79


@dataclass
class FixResult:
    """Result of a line fix attempt."""
    file_path: str
    line_number: int
    original_line: str
    fixed_lines: List[str]
    agent_used: Optional[str]  # Changed from Enum to string
    success: bool
    confidence: float



class AgenticE501Fixer:
    """
    Agentic system with hierarchical three-tier intelligence for E501 fixing.
    
    Uses hierarchical pipeline (Ollama→Gemini→DeepSeek) when available.
    Falls back to agent conclave facade (3000+ lines orchestrator).
    Maintains formatting-specific logic locally.
    """

    def __init__(self, use_hierarchy: bool = True):
        """
        Initialize with hierarchical pipeline or facade fallback.
        
        Args:
            use_hierarchy: Use hierarchical pipeline if available (default)
        """
        self.conclave = get_agent_conclave()
        
        # Initialize hierarchical pipeline if available and requested
        self.hierarchical_pipeline = None
        if use_hierarchy and HIERARCHICAL_AVAILABLE:
            self.hierarchical_pipeline = HierarchicalE501Pipeline()
            logging.info(
                "Hierarchical pipeline initialized "
                "(Ollama→Gemini→DeepSeek)"
            )
        elif use_hierarchy and not HIERARCHICAL_AVAILABLE:
            logging.warning(
                "Hierarchical pipeline requested but unavailable, "
                "using facade"
            )
        
        self.stats = {
            "files_processed": 0,
            "lines_fixed": 0,
            "lines_scanned": 0,
            "agent_fixes": 0,
            "hierarchical_fixes": 0,
            "basic_fixes": 0
        }
        # Tachyonic archival for conversations
        archive_base = Path(__file__).parent.parent.parent
        self.conversation_archive_path = (
            archive_base / "tachyonic" / "agentic_conversations"
        )

    def _calculate_complexity(self, line: str) -> float:
        """Calculate complexity score of a line (0-1)."""
        score = 0.0

        # Length factor
        score += min(len(line) / 150, 0.5)

        # Special characters
        special_chars = sum(
            1 for c in line if c in '()[]{}.,:;+-*/=<>!'
        )
        score += min(special_chars / 20, 0.3)

        # Keywords indicating complexity
        complex_keywords = [
            'lambda', 'comprehension', 'decorator',
            'async', 'await'
        ]
        for keyword in complex_keywords:
            if keyword in line:
                score += 0.2

        return min(score, 1.0)

    async def fix_line_with_agent(
        self,
        line: str,
        line_number: int,
        file_path: str
    ) -> FixResult:
        """
        Fix a long line using agent conclave facade.
        
        Delegates to nucleus facade which orchestrates multi-agent consensus.
        """
        complexity = self._calculate_complexity(line)

        prompt = f"""Fix this Python line to comply with PEP 8 E501 (max 79
    characters).

Original line ({len(line)} characters):
{line}

Requirements:
1. Break the line intelligently while preserving functionality
2. Use proper Python line continuation (backslash or implicit)
3. Return ONLY the fixed Python code
4. Each line must be ≤79 characters
5. Do NOT include explanations or commentary

Return the fixed code as plain text, one line per line."""

        try:
            # Query agent conclave via facade
            response = await self.conclave.query(
                prompt=prompt,
                context={
                    "tool": "agentic_e501_fixer",
                    "task_type": "line_formatting",
                    "complexity": complexity,
                    "line_length": len(line),
                    "file_path": file_path,
                    "line_number": line_number
                }
            )

            # Parse response content - extract only code lines
            content_lines = response.content.split('\n')
            fixed_lines = []
            
            for line_text in content_lines:
                stripped = line_text.strip()
                # Skip empty lines, markdown, and decision text
                if not stripped:
                    continue
                if stripped.startswith('```'):
                    continue
                if any(word in stripped.lower() for word in [
                    'consensus', 'adopt', 'defer', 'reject',
                    'recommend', 'mixed', 'confidence'
                ]):
                    continue
                # This looks like actual code
                fixed_lines.append(stripped)
            
            success = all(len(l) <= MAX_LINE_LENGTH for l in fixed_lines)

            return FixResult(
                file_path=file_path,
                line_number=line_number,
                original_line=line,
                fixed_lines=fixed_lines,
                agent_used=response.agent_used,
                success=success,
                confidence=response.confidence
            )

        except Exception as e:
            logger.error(f"Agent facade failed: {e}")
            # Fallback to basic fixing
            return self._basic_fix_result(line, line_number, file_path)

    def _basic_fix_line(self, line: str) -> List[str]:
        """
        Basic pattern-based line breaking for when AI agents unavailable.
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
        import re
        
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

    def _basic_fix_result(
        self,
        line: str,
        line_number: int,
        file_path: str
    ) -> FixResult:
        """Create FixResult using basic pattern-based fixing."""
        fixed_lines = self._basic_fix_line(line)
        success = all(len(l) <= MAX_LINE_LENGTH for l in fixed_lines)
        
        return FixResult(
            file_path=file_path,
            line_number=line_number,
            original_line=line,
            fixed_lines=fixed_lines,
            agent_used=None,
            success=success,
            confidence=0.6 if success else 0.0
        )

    async def fix_line(
        self,
        line: str,
        line_number: int,
        file_path: str
    ) -> FixResult:
        """
        Fix a single long line using best available method.
        
        Priority:
        1. Hierarchical pipeline (Ollama→Gemini→DeepSeek) if available
        2. Agent conclave facade (orchestrator) as fallback
        3. Basic pattern matching as last resort
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

        # Try hierarchical pipeline first (preferred)
        if self.hierarchical_pipeline:
            try:
                result = await self.hierarchical_pipeline \
                    .fix_line_hierarchical(
                        line, file_path, line_number
                    )
                
                if result["success"]:
                    self.stats["hierarchical_fixes"] += 1
                    return FixResult(
                        file_path=file_path,
                        line_number=line_number,
                        original_line=line,
                        fixed_lines=result["fixed_lines"],
                        agent_used=result.get("agent_used"),
                        success=True,
                        confidence=result["confidence"]
                    )
                
            except Exception as e:
                logger.warning(
                    f"Hierarchical pipeline failed for line {line_number}: {e}"
                )
                logger.info("Falling back to agent conclave facade")

        # Fallback to agent conclave facade
        availability = self.conclave.check_availability()
        agents_available = any(availability.values())

        if agents_available:
            try:
                result = await self.fix_line_with_agent(
                    line, line_number, file_path
                )
                if result.success:
                    self.stats["agent_fixes"] += 1
                return result
            except Exception as e:
                logger.warning(
                    f"Agent conclave failed for line {line_number}: {e}"
                )
                # Continue to basic fixing

        # Use basic pattern-based fixing
        logger.info(f"Using basic fixer for line {line_number}")
        self.stats["basic_fixes"] += 1
        return self._basic_fix_result(line, line_number, file_path)

    async def fix_file(self, file_path: str, dry_run: bool = True):
        """Fix all E501 violations in a file using AI agents."""
        import json
        from datetime import datetime
        
        logger.info(f"Processing file: {file_path}")
        self.stats["files_processed"] += 1

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        fixed_lines = []
        fixes_applied = 0
        fix_results = []

        for i, line in enumerate(lines):
            self.stats["lines_scanned"] += 1
            line_content = line.rstrip('\n\r')

            if len(line_content) > MAX_LINE_LENGTH:
                try:
                    result = await self.fix_line(
                        line_content, i + 1, file_path
                    )

                    if result.success:
                        for fixed in result.fixed_lines:
                            fixed_lines.append(fixed + '\n')
                        fixes_applied += 1
                        self.stats["lines_fixed"] += 1

                        agent_str = result.agent_used or "basic"
                        logger.info(f"Fixed line {i+1} with {agent_str}")
                        fix_results.append({
                            "line_number": i + 1,
                            "original_length": len(line_content),
                            "agent_used": result.agent_used,
                            "success": True
                        })
                    else:
                        fixed_lines.append(line)
                        logger.warning(f"Failed to fix line {i+1}")
                        fix_results.append({
                            "line_number": i + 1,
                            "original_length": len(line_content),
                            "success": False
                        })

                except Exception as e:
                    logger.error(f"Error fixing line {i+1}: {e}")
                    fixed_lines.append(line)
                    fix_results.append({
                        "line_number": i + 1,
                        "error": str(e)
                    })
            else:
                fixed_lines.append(line)

        # Apply fixes if not dry run
        if not dry_run and fixes_applied > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(fixed_lines)
            logger.info(f"Applied {fixes_applied} fixes to {file_path}")

        return {
            "file": file_path,
            "fixes_applied": fixes_applied,
            "dry_run": dry_run,
            "fix_results": fix_results
        }


async def scan_file(file_path: str):
    """Scan a file for E501 violations without fixing."""
    violations = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            line = line.rstrip('\n\r')
            if len(line) > MAX_LINE_LENGTH:
                violations.append({
                    "line_number": i,
                    "length": len(line),
                    "line": line[:80] + "..." if len(line) > 80 else line
                })

    return {
        "file": str(file_path),
        "violation_count": len(violations),
        "violations": violations
    }


async def main():
    """Main CLI entry point with scan-only, JSON output, and fix modes."""
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="AI-powered E501 line length fixer using agent conclave"
    )
    parser.add_argument(
        "path",
        help="Python file or directory to process"
    )
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="Scan for E501 violations without fixing"
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output results as JSON (for bootloader parsing)"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply fixes to files (default: dry-run)"
    )
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Recursively process directories"
    )

    args = parser.parse_args()
    path = Path(args.path)

    # Determine files to process
    if path.is_file():
        files = [path]
    elif path.is_dir():
        if args.recursive:
            files = list(path.rglob("*.py"))
        else:
            files = list(path.glob("*.py"))
    else:
        print(f"Error: Path not found: {path}", file=sys.stderr)
        return 1

    # Scan-only mode
    if args.scan_only:
        results = []
        total_violations = 0

        for file_path in files:
            try:
                scan_result = await scan_file(str(file_path))
                total_violations += scan_result["violation_count"]
                results.append(scan_result)
            except Exception as e:
                logger.error(f"Failed to scan {file_path}: {e}")

        if args.json_output:
            # Output for bootloader parsing
            output = {
                "scan_type": "e501_violations",
                "total_files": len(files),
                "total_violations": total_violations,
                "files_with_violations": sum(
                    1 for r in results if r["violation_count"] > 0
                ),
                "results": results
            }
            print(json.dumps(output, indent=2))
        else:
            # Human-readable output
            print("\nE501 Scan Results:")
            print(f"Files scanned: {len(files)}")
            print(f"Total violations: {total_violations}")
            files_with = sum(1 for r in results if r['violation_count'] > 0)
            print(f"Files with violations: {files_with}")

            for result in results:
                if result["violation_count"] > 0:
                    vcount = result['violation_count']
                    print(f"\n{result['file']}: {vcount} violations")
                    for v in result["violations"]:
                        lnum = v['line_number']
                        llen = v['length']
                        print(f"  Line {lnum}: {llen} chars")

        return 0 if total_violations == 0 else 1

    # Fix mode
    fixer = AgenticE501Fixer()
    dry_run = not args.fix

    # Check agent availability
    availability = fixer.conclave.check_availability()
    agents_available = any(availability.values())

    if not agents_available:
        logger.warning(
            "No AI agents available. Will use basic pattern-based fixing."
        )
        print("\nWarning: No AI agents available", file=sys.stderr)
        print("Available agents:", availability, file=sys.stderr)

    # Process files
    results = []
    for file_path in files:
        try:
            logger.info(f"Processing {file_path}")
            result = await fixer.fix_file(str(file_path), dry_run)
            results.append(result)
        except Exception as e:
            logger.error(f"Failed to process {file_path}: {e}")
            results.append({"file": str(file_path), "error": str(e)})

    if args.json_output:
        output = {
            "fix_type": "e501_ai_fix",
            "dry_run": dry_run,
            "total_files": len(files),
            "agents_available": agents_available,
            "results": results,
            "stats": fixer.stats
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"\nProcessed {len(files)} files")
        mode_str = 'DRY RUN' if dry_run else 'APPLIED FIXES'
        print(f"Mode: {mode_str}")
        print(f"Stats: {fixer.stats}")

    return 0


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    sys.exit(asyncio.run(main()))
