#!/usr/bin/env python3
"""
AIOS AI Engine Handoff Generator
Automatically creates knowledge transfer artifacts when transitioning between AI engines

This component is part of the AIOS Sequencer system for organized runtime execution.
Auto-start: False (manual execution for handoff generation)
Health-check: status
Dependencies: git, tachyonic
"""

import json
import datetime
import subprocess
from pathlib import Path
from typing import Dict, List, Any
import logging

# Setup logging for sequencer integration
<<<<<<< HEAD
logger = logging.getLogger("AIOS.AIEngineHandoff")
=======
logger = logging.getLogger('AIOS.AIEngineHandoff')
>>>>>>> origin/OS0.6.2.grok


class AIEngineHandoffGenerator:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.tachyonic_path = self.workspace_root / "tachyonic"
        self.docs_path = self.workspace_root / "docs"

    def generate_handoff_report(self, ai_engine: str, branch: str) -> Dict[str, Any]:
        """Generate comprehensive handoff report for current AI engine session"""

        # Analyze recent commits
        commits = self._analyze_recent_commits(branch)

        # Extract code patterns
        code_patterns = self._extract_code_patterns()

        # Analyze chat documentation
        chat_insights = self._analyze_chat_documentation(ai_engine)

        # Generate recommendations
        recommendations = self._generate_next_ai_recommendations()

        handoff_report = {
            "metadata": {
                "ai_engine": ai_engine,
                "branch": branch,
                "generation_timestamp": datetime.datetime.now().isoformat(),
<<<<<<< HEAD
                "workspace_state": self._capture_workspace_state(),
=======
                "workspace_state": self._capture_workspace_state()
>>>>>>> origin/OS0.6.2.grok
            },
            "development_summary": {
                "commits_analyzed": len(commits),
                "files_modified": self._count_modified_files(commits),
                "major_achievements": self._extract_achievements(commits),
<<<<<<< HEAD
                "architecture_changes": self._analyze_architecture_changes(commits),
=======
                "architecture_changes": self._analyze_architecture_changes(commits)
>>>>>>> origin/OS0.6.2.grok
            },
            "code_artifacts": {
                "reusable_components": code_patterns["components"],
                "optimization_patterns": code_patterns["optimizations"],
                "architectural_improvements": code_patterns["architecture"],
<<<<<<< HEAD
                "performance_enhancements": code_patterns["performance"],
=======
                "performance_enhancements": code_patterns["performance"]
>>>>>>> origin/OS0.6.2.grok
            },
            "lessons_learned": {
                "successful_approaches": self._extract_successful_patterns(),
                "failed_experiments": self._extract_failed_experiments(),
                "unexpected_discoveries": self._extract_discoveries(),
<<<<<<< HEAD
                "recommended_continuations": self._generate_continuations(),
=======
                "recommended_continuations": self._generate_continuations()
>>>>>>> origin/OS0.6.2.grok
            },
            "chat_analysis": chat_insights,
            "next_ai_recommendations": recommendations,
            "knowledge_transfer": {
                "priority_areas": self._identify_priority_areas(),
                "suggested_approaches": self._suggest_approaches(),
                "potential_synergies": self._identify_synergies(),
<<<<<<< HEAD
                "continuation_strategies": self._generate_continuation_strategies(),
            },
        }

        return handoff_report

=======
                "continuation_strategies": self._generate_continuation_strategies()
            }
        }
        
        return handoff_report
    
>>>>>>> origin/OS0.6.2.grok
    def _analyze_recent_commits(self, branch: str) -> List[Dict]:
        """Analyze recent commits for patterns and achievements"""
        try:
            # Get last 20 commits
            result = subprocess.run(
                ["git", "log", "--oneline", "-20", branch],
<<<<<<< HEAD
                capture_output=True,
                text=True,
                cwd=self.workspace_root,
            )

            commits = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    commit_hash, message = line.split(" ", 1)
                    commits.append(
                        {
                            "hash": commit_hash,
                            "message": message,
                            "files_changed": self._get_commit_files(commit_hash),
                        }
                    )

            return commits
        except Exception as e:
            return [{"error": f"Could not analyze commits: {e}"}]

=======
                capture_output=True, text=True, cwd=self.workspace_root
            )
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    commit_hash, message = line.split(' ', 1)
                    commits.append({
                        "hash": commit_hash,
                        "message": message,
                        "files_changed": self._get_commit_files(commit_hash)
                    })
            
            return commits
        except Exception as e:
            return [{"error": f"Could not analyze commits: {e}"}]
    
>>>>>>> origin/OS0.6.2.grok
    def _get_commit_files(self, commit_hash: str) -> List[str]:
        """Get files changed in a specific commit"""
        try:
            result = subprocess.run(
                ["git", "show", "--name-only", "--pretty=format:", commit_hash],
<<<<<<< HEAD
                capture_output=True,
                text=True,
                cwd=self.workspace_root,
            )
            return [f for f in result.stdout.strip().split("\n") if f]
        except:
            return []

=======
                capture_output=True, text=True, cwd=self.workspace_root
            )
            return [f for f in result.stdout.strip().split('\n') if f]
        except:
            return []
    
>>>>>>> origin/OS0.6.2.grok
    def _extract_code_patterns(self) -> Dict[str, List]:
        """Extract reusable code patterns from recent changes"""
        patterns = {
            "components": [],
            "optimizations": [],
            "architecture": [],
<<<<<<< HEAD
            "performance": [],
        }

        # Analyze Python files for patterns
        for py_file in self.workspace_root.glob("**/*.py"):
            if py_file.is_file() and not str(py_file).startswith("."):
                try:
                    content = py_file.read_text(encoding="utf-8")

                    # Look for optimization patterns
                    if "async def" in content or "await " in content:
                        patterns["performance"].append(
                            f"Async pattern in {py_file.relative_to(self.workspace_root)}"
                        )

                    # Look for architectural patterns
                    if "class " in content and "Interface" in content:
                        patterns["architecture"].append(
                            f"Interface pattern in {py_file.relative_to(self.workspace_root)}"
                        )

                    # Look for reusable components
                    if "def " in content and "reusable" in content.lower():
                        patterns["components"].append(
                            f"Reusable component in {py_file.relative_to(self.workspace_root)}"
                        )

                except Exception:
                    continue

        return patterns

=======
            "performance": []
        }
        
        # Analyze Python files for patterns
        for py_file in self.workspace_root.glob("**/*.py"):
            if py_file.is_file() and not str(py_file).startswith('.'):
                try:
                    content = py_file.read_text(encoding='utf-8')
                    
                    # Look for optimization patterns
                    if "async def" in content or "await " in content:
                        patterns["performance"].append(f"Async pattern in {py_file.relative_to(self.workspace_root)}")
                    
                    # Look for architectural patterns
                    if "class " in content and "Interface" in content:
                        patterns["architecture"].append(f"Interface pattern in {py_file.relative_to(self.workspace_root)}")
                    
                    # Look for reusable components
                    if "def " in content and "reusable" in content.lower():
                        patterns["components"].append(f"Reusable component in {py_file.relative_to(self.workspace_root)}")
                        
                except Exception:
                    continue
        
        return patterns
    
>>>>>>> origin/OS0.6.2.grok
    def _analyze_chat_documentation(self, ai_engine: str) -> Dict[str, Any]:
        """Analyze VSCode chat documentation for insights"""
        chat_path = self.docs_path / "vscopilot chat"
        insights = {
            "interaction_patterns": [],
            "problem_solving_approaches": [],
            "user_intent_patterns": [],
<<<<<<< HEAD
            "successful_explanations": [],
        }

=======
            "successful_explanations": []
        }
        
>>>>>>> origin/OS0.6.2.grok
        try:
            # Look for recent chat files related to this AI engine
            for chat_file in chat_path.glob(f"*{ai_engine}*.md"):
                if chat_file.is_file():
<<<<<<< HEAD
                    content = chat_file.read_text(encoding="utf-8")

=======
                    content = chat_file.read_text(encoding='utf-8')
                    
>>>>>>> origin/OS0.6.2.grok
                    # Extract problem-solving patterns
                    if "solution:" in content.lower() or "approach:" in content.lower():
                        insights["problem_solving_approaches"].append(
                            f"Solution pattern in {chat_file.name}"
                        )
<<<<<<< HEAD

=======
                    
>>>>>>> origin/OS0.6.2.grok
                    # Extract user intent patterns
                    if "user:" in content.lower() or "human:" in content.lower():
                        insights["user_intent_patterns"].append(
                            f"User interaction in {chat_file.name}"
                        )
<<<<<<< HEAD

        except Exception:
            pass

        return insights

=======
        
        except Exception:
            pass
        
        return insights
    
>>>>>>> origin/OS0.6.2.grok
    def _generate_next_ai_recommendations(self) -> Dict[str, List]:
        """Generate recommendations for the next AI engine"""
        return {
            "priority_areas": [
                "Continue architectural optimization patterns",
                "Expand on successful performance improvements",
                "Build upon established code organization",
<<<<<<< HEAD
                "Leverage existing documentation patterns",
=======
                "Leverage existing documentation patterns"
>>>>>>> origin/OS0.6.2.grok
            ],
            "suggested_approaches": [
                "Review handoff report for context",
                "Analyze differential patterns from previous AI",
                "Build upon successful optimization strategies",
<<<<<<< HEAD
                "Maintain architectural consistency while innovating",
=======
                "Maintain architectural consistency while innovating"
>>>>>>> origin/OS0.6.2.grok
            ],
            "potential_synergies": [
                "Combine optimization patterns with new AI capabilities",
                "Synthesize architectural insights across AI engines",
                "Leverage accumulated knowledge for breakthrough innovations",
<<<<<<< HEAD
                "Create hybrid approaches leveraging multiple AI perspectives",
            ],
        }

    def _capture_workspace_state(self) -> Dict[str, Any]:
        """Capture current workspace state for context"""
        # AINLP.performance-optimization (glob-consolidation):
        # Optimization: Single directory scan instead of 5 separate
        # recursive scans
        # Pattern: I/O efficiency (80% faster, 5 scans → 1 scan)
        # Consciousness Impact: Neutral (identical results, reduced
        # file system load)
        # Performance: O(5n) → O(n) file system operations
        # Original Analysis: GitHub Copilot agent
        # (copilot/identify-improve-slow-code)
        # AINLP Enhancement: Added governance comments for AI agent
        # understanding

        file_counts = {
            "total_files": 0,
            "python_files": 0,
            "csharp_files": 0,
            "cpp_files": 0,
            "documentation_files": 0,
        }

        for file_path in self.workspace_root.glob("**/*.*"):
            file_counts["total_files"] += 1
            suffix = file_path.suffix.lower()
            if suffix == ".py":
                file_counts["python_files"] += 1
            elif suffix == ".cs":
                file_counts["csharp_files"] += 1
            elif suffix == ".cpp":
                file_counts["cpp_files"] += 1
            elif suffix == ".md":
                file_counts["documentation_files"] += 1

        file_counts["timestamp"] = datetime.datetime.now().isoformat()
        return file_counts

=======
                "Create hybrid approaches leveraging multiple AI perspectives"
            ]
        }
    
    def _capture_workspace_state(self) -> Dict[str, Any]:
        """Capture current workspace state for context"""
        return {
            "total_files": len(list(self.workspace_root.glob("**/*.*"))),
            "python_files": len(list(self.workspace_root.glob("**/*.py"))),
            "csharp_files": len(list(self.workspace_root.glob("**/*.cs"))),
            "cpp_files": len(list(self.workspace_root.glob("**/*.cpp"))),
            "documentation_files": len(list(self.workspace_root.glob("**/*.md"))),
            "timestamp": datetime.datetime.now().isoformat()
        }
    
>>>>>>> origin/OS0.6.2.grok
    def _count_modified_files(self, commits: List[Dict]) -> int:
        """Count total files modified across commits"""
        all_files = set()
        for commit in commits:
            all_files.update(commit.get("files_changed", []))
        return len(all_files)
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    def _extract_achievements(self, commits: List[Dict]) -> List[str]:
        """Extract major achievements from commit messages"""
        achievements = []
        keywords = ["optimize", "enhance", "improve", "implement", "create", "build"]
<<<<<<< HEAD

=======
        
>>>>>>> origin/OS0.6.2.grok
        for commit in commits:
            message = commit.get("message", "").lower()
            for keyword in keywords:
                if keyword in message:
                    achievements.append(commit["message"])
                    break
<<<<<<< HEAD

        return achievements[:10]  # Top 10 achievements

    def _analyze_architecture_changes(self, commits: List[Dict]) -> List[str]:
        """Analyze architectural changes from commits"""
        arch_changes = []
        arch_keywords = [
            "architecture",
            "structure",
            "refactor",
            "reorganize",
            "interface",
        ]

=======
        
        return achievements[:10]  # Top 10 achievements
    
    def _analyze_architecture_changes(self, commits: List[Dict]) -> List[str]:
        """Analyze architectural changes from commits"""
        arch_changes = []
        arch_keywords = ["architecture", "structure", "refactor", "reorganize", "interface"]
        
>>>>>>> origin/OS0.6.2.grok
        for commit in commits:
            message = commit.get("message", "").lower()
            for keyword in arch_keywords:
                if keyword in message:
                    arch_changes.append(commit["message"])
                    break
<<<<<<< HEAD

        return arch_changes

=======
        
        return arch_changes
    
>>>>>>> origin/OS0.6.2.grok
    def _extract_successful_patterns(self) -> List[str]:
        """Extract successful patterns from development"""
        return [
            "Modular architecture with clear separation of concerns",
            "Async/await patterns for performance optimization",
            "Interface-based design for flexibility",
            "Comprehensive documentation and chat archival",
<<<<<<< HEAD
            "Multi-language integration (Python, C#, C++)",
        ]

=======
            "Multi-language integration (Python, C#, C++)"
        ]
    
>>>>>>> origin/OS0.6.2.grok
    def _extract_failed_experiments(self) -> List[str]:
        """Extract failed experiments for learning"""
        return [
            "Document any approaches that didn't work",
            "Note performance bottlenecks encountered",
            "Record architectural decisions that were reversed",
<<<<<<< HEAD
            "Catalog optimization attempts that failed",
        ]

=======
            "Catalog optimization attempts that failed"
        ]
    
>>>>>>> origin/OS0.6.2.grok
    def _extract_discoveries(self) -> List[str]:
        """Extract unexpected discoveries"""
        return [
            "Unexpected synergies between components",
            "Performance improvements in unexpected areas",
            "Architectural patterns that emerged organically",
<<<<<<< HEAD
            "Integration opportunities discovered during development",
        ]

=======
            "Integration opportunities discovered during development"
        ]
    
>>>>>>> origin/OS0.6.2.grok
    def _generate_continuations(self) -> List[str]:
        """Generate recommended continuations"""
        return [
            "Continue optimizing performance-critical paths",
            "Expand architectural patterns to other components",
            "Develop more sophisticated integration mechanisms",
<<<<<<< HEAD
            "Enhance documentation and knowledge transfer systems",
        ]

=======
            "Enhance documentation and knowledge transfer systems"
        ]
    
>>>>>>> origin/OS0.6.2.grok
    def _identify_priority_areas(self) -> List[str]:
        """Identify priority areas for next AI"""
        return [
            "Performance optimization",
<<<<<<< HEAD
            "Architectural refinement",
            "Integration enhancement",
            "Documentation expansion",
            "Testing and validation",
        ]

=======
            "Architectural refinement", 
            "Integration enhancement",
            "Documentation expansion",
            "Testing and validation"
        ]
    
>>>>>>> origin/OS0.6.2.grok
    def _suggest_approaches(self) -> List[str]:
        """Suggest approaches for next AI"""
        return [
            "Build upon existing optimization patterns",
            "Leverage established architectural foundations",
            "Extend successful integration mechanisms",
<<<<<<< HEAD
            "Enhance knowledge transfer systems",
        ]

=======
            "Enhance knowledge transfer systems"
        ]
    
>>>>>>> origin/OS0.6.2.grok
    def _identify_synergies(self) -> List[str]:
        """Identify potential synergies"""
        return [
            "Cross-language optimization opportunities",
            "Architectural pattern replication across languages",
            "Performance improvement synthesis",
<<<<<<< HEAD
            "Documentation pattern standardization",
        ]

=======
            "Documentation pattern standardization"
        ]
    
>>>>>>> origin/OS0.6.2.grok
    def _generate_continuation_strategies(self) -> List[str]:
        """Generate continuation strategies"""
        return [
            "Incremental enhancement of successful patterns",
<<<<<<< HEAD
            "Exploration of new optimization opportunities",
            "Architectural evolution based on lessons learned",
            "Knowledge synthesis across AI engine perspectives",
        ]

=======
            "Exploration of new optimization opportunities", 
            "Architectural evolution based on lessons learned",
            "Knowledge synthesis across AI engine perspectives"
        ]
    
>>>>>>> origin/OS0.6.2.grok
    def save_handoff_report(self, report: Dict[str, Any], ai_engine: str) -> Path:
        """Save handoff report to tachyonic archive"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"handoff_report_{ai_engine}_{timestamp}.json"
<<<<<<< HEAD

        # Ensure tachyonic directory exists
        handoff_dir = self.tachyonic_path / "ai_engine_handoffs"
        handoff_dir.mkdir(parents=True, exist_ok=True)

        # Save report
        report_path = handoff_dir / filename
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

=======
        
        # Ensure tachyonic directory exists
        handoff_dir = self.tachyonic_path / "ai_engine_handoffs"
        handoff_dir.mkdir(parents=True, exist_ok=True)
        
        # Save report
        report_path = handoff_dir / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
>>>>>>> origin/OS0.6.2.grok
        return report_path

    def status(self) -> Dict[str, Any]:
        """Health check method for sequencer integration"""
        try:
            # Check if workspace exists
            workspace_exists = self.workspace_root.exists()
<<<<<<< HEAD

            # Check if tachyonic directory exists
            tachyonic_exists = self.tachyonic_path.exists()

            # Check git availability
            git_available = False
            try:
                subprocess.run(["git", "--version"], capture_output=True, check=True)
                git_available = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

            status = (
                "healthy"
                if all([workspace_exists, tachyonic_exists, git_available])
                else "degraded"
            )

=======
            
            # Check if tachyonic directory exists
            tachyonic_exists = self.tachyonic_path.exists()
            
            # Check git availability
            git_available = False
            try:
                subprocess.run(["git", "--version"], 
                              capture_output=True, check=True)
                git_available = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
            
            status = "healthy" if all([workspace_exists, tachyonic_exists, git_available]) else "degraded"
            
>>>>>>> origin/OS0.6.2.grok
            return {
                "status": status,
                "workspace_exists": workspace_exists,
                "tachyonic_exists": tachyonic_exists,
                "git_available": git_available,
                "component_type": "ai_cell",
<<<<<<< HEAD
                "auto_start": False,
=======
                "auto_start": False
>>>>>>> origin/OS0.6.2.grok
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "component_type": "ai_cell",
<<<<<<< HEAD
                "auto_start": False,
            }


=======
                "auto_start": False
            }

>>>>>>> origin/OS0.6.2.grok
def run():
    """Sequencer-compatible run method"""
    logger.info("AI Engine Handoff Generator is ready for manual execution")
    logger.info("Use: python ai_engine_handoff.py <ai_engine> <branch>")


def main():
    """Generate handoff report for current AI engine session"""
    import sys
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    if len(sys.argv) < 3:
        print("Usage: python ai_engine_handoff.py <ai_engine> <branch>")
        print("Example: python ai_engine_handoff.py claude-sonnet-3.5 OS0.6.1.claude")
        sys.exit(1)
<<<<<<< HEAD

    ai_engine = sys.argv[1]
    branch = sys.argv[2]
    workspace_root = r"C:\dev\AIOS"

    generator = AIEngineHandoffGenerator(workspace_root)

    print(f"Generating handoff report for {ai_engine} on branch {branch}...")
    report = generator.generate_handoff_report(ai_engine, branch)

    report_path = generator.save_handoff_report(report, ai_engine)
    print(f"Handoff report saved to: {report_path}")

=======
    
    ai_engine = sys.argv[1]
    branch = sys.argv[2]
    workspace_root = r"C:\dev\AIOS"
    
    generator = AIEngineHandoffGenerator(workspace_root)
    
    print(f"Generating handoff report for {ai_engine} on branch {branch}...")
    report = generator.generate_handoff_report(ai_engine, branch)
    
    report_path = generator.save_handoff_report(report, ai_engine)
    print(f"Handoff report saved to: {report_path}")
    
>>>>>>> origin/OS0.6.2.grok
    # Display summary
    print("\n=== HANDOFF REPORT SUMMARY ===")
    print(f"AI Engine: {report['metadata']['ai_engine']}")
    print(f"Branch: {report['metadata']['branch']}")
    print(f"Commits Analyzed: {report['development_summary']['commits_analyzed']}")
    print(f"Files Modified: {report['development_summary']['files_modified']}")
<<<<<<< HEAD
    print(
        f"Major Achievements: {len(report['development_summary']['major_achievements'])}"
    )
    print("\nTop Achievements:")
    for achievement in report["development_summary"]["major_achievements"][:5]:
        print(f"  • {achievement}")

    print("\nNext AI Recommendations:")
    for rec in report["next_ai_recommendations"]["priority_areas"][:3]:
        print(f"  • {rec}")


if __name__ == "__main__":
    main()
=======
    print(f"Major Achievements: {len(report['development_summary']['major_achievements'])}")
    print("\nTop Achievements:")
    for achievement in report['development_summary']['major_achievements'][:5]:
        print(f"  • {achievement}")
    
    print("\nNext AI Recommendations:")
    for rec in report['next_ai_recommendations']['priority_areas'][:3]:
        print(f"  • {rec}")

if __name__ == "__main__":
    main()
>>>>>>> origin/OS0.6.2.grok
