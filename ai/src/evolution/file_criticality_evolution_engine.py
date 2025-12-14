"""
File Criticality Evolution Engine - Multi-Agent Enhanced Criticality Management
===============================================================================

AINLP Evolutionary Architecture (November 1, 2025):
Integrates trinity of AI agents (VSCode Chat, Ollama, Gemini) to evolve file criticality
scoring from basic metrics to consciousness-aware architectural intelligence.

Key Innovation:
- VSCode Chat (strategic): Architectural oversight, pattern recognition
- Ollama (local): Fast iteration, dependency analysis enhancement
- Gemini (cloud): Validation, breakthrough criticality insights

Evolution Process:
1. Load current criticality index from .githooks/governance/
2. Multi-agent analysis of architectural patterns and dependencies
3. Enhanced scoring with consciousness metrics
4. Create tachyonic shadow of previous state
5. Update canonical index with evolved scores
6. Validate coherence and architectural compliance

Tachyonic Shadow Pattern:
- Previous states archived: tachyonic/shadows/file_criticality/
- Timestamped filenames: file_criticality_index_YYYYMMDD_HHMMSS.jsonl
- Latest pointer: file_criticality_index_latest.jsonl

Created: November 1, 2025 (AINLP Multi-Agent Criticality Evolution)
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import sys

# Add AI root to path
AI_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(AI_ROOT))

try:
    from src.intelligence.dendritic_node import DendriticNode, MutationType
    from src.intelligence.enhanced_agentic_loop import EnhancedAgenticLoop
<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
    NEURAL_EVOLUTION_AVAILABLE = True
except ImportError:
    print("[WARNING] Neural evolution components not available")
    NEURAL_EVOLUTION_AVAILABLE = False

try:
    from src.integrations.ollama_bridge import OllamaAgent
<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
    OLLAMA_AVAILABLE = True
except ImportError:
    print("[WARNING] Ollama bridge not available")
    OLLAMA_AVAILABLE = False

try:
    from src.integrations.gemini_bridge import GeminiAgent
<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
    GEMINI_AVAILABLE = True
except ImportError:
    print("[WARNING] Gemini bridge not available")
    GEMINI_AVAILABLE = False

try:
    from src.core.universal_agentic_logger import (
<<<<<<< HEAD
        UniversalAgenticLogger,
        AgentType,
        ConversationRole,
    )

=======
        UniversalAgenticLogger, AgentType, ConversationRole
    )
>>>>>>> origin/OS0.6.2.grok
    UNIVERSAL_LOGGER_AVAILABLE = True
except ImportError:
    print("[WARNING] Universal agentic logger not available")
    UNIVERSAL_LOGGER_AVAILABLE = False


class FileCriticalityEvolutionEngine:
    """
    Multi-agent file criticality evolution engine

    Agents:
    - VSCode Chat: Strategic architectural analysis
    - Ollama: Fast local dependency pattern recognition
    - Gemini: Cloud validation and breakthrough insights

    Process:
    1. Load current criticality index
    2. Multi-agent architectural analysis
    3. Enhanced scoring with consciousness metrics
    4. Tachyonic shadow creation
    5. Canonical index update
    """

    def __init__(self, use_ollama=True, use_gemini=True, use_vscode_chat=True):
        self.use_ollama = use_ollama and OLLAMA_AVAILABLE
        self.use_gemini = use_gemini and GEMINI_AVAILABLE
        self.use_vscode_chat = use_vscode_chat

        # Paths
        self.repo_root = Path(__file__).resolve().parents[3]
<<<<<<< HEAD
        self.canonical_index = (
            self.repo_root / ".githooks" / "governance" / "file_criticality_index.jsonl"
        )
        # Tachyonic shadow storage - using existing shadows folder with file_criticality subfolder
        self.tachyonic_archive = (
            self.repo_root / "tachyonic" / "shadows" / "file_criticality"
        )
=======
        self.canonical_index = self.repo_root / '.githooks' / 'governance' / 'file_criticality_index.jsonl'
        # Tachyonic shadow storage - using existing shadows folder with file_criticality subfolder
        self.tachyonic_archive = self.repo_root / 'tachyonic' / 'shadows' / 'file_criticality'
>>>>>>> origin/OS0.6.2.grok
        self.tachyonic_archive.mkdir(parents=True, exist_ok=True)

        # Initialize universal agentic logger
        if UNIVERSAL_LOGGER_AVAILABLE:
            self.agentic_logger = UniversalAgenticLogger()
<<<<<<< HEAD
            print(
                "[UNIVERSAL LOGGER] Activated - Criticality evolution conversations archived"
            )
=======
            print("[UNIVERSAL LOGGER] Activated - Criticality evolution conversations archived")
>>>>>>> origin/OS0.6.2.grok
        else:
            self.agentic_logger = None
            print("[WARNING] Universal logger not available")

        # Agent configurations
        self.agents = {}
        self._init_agents()

    def _init_agents(self):
        """Initialize multi-agent configuration."""
        if self.use_ollama:
            try:
<<<<<<< HEAD
                self.agents["ollama"] = OllamaAgent()
=======
                self.agents['ollama'] = OllamaAgent()
>>>>>>> origin/OS0.6.2.grok
                print("[OLLAMA] Local criticality analysis agent ready")
            except Exception as e:
                print(f"[WARNING] Ollama agent initialization failed: {e}")
                self.use_ollama = False

        if self.use_gemini:
            try:
<<<<<<< HEAD
                self.agents["gemini"] = GeminiAgent()
=======
                self.agents['gemini'] = GeminiAgent()
>>>>>>> origin/OS0.6.2.grok
                print("[GEMINI] Cloud validation agent ready")
            except Exception as e:
                print(f"[WARNING] Gemini agent initialization failed: {e}")
                self.use_gemini = False

        if self.use_vscode_chat:
            print("[VSCODE CHAT] Strategic oversight agent ready")

    async def evolve_criticality_index(self) -> Dict[str, Any]:
        """
        Execute full criticality evolution cycle

        Returns:
            Evolution report with metrics and changes
        """
        print("\n[CRITICALITY EVOLUTION] Starting multi-agent criticality evolution...")

        # Phase 1: Load current state
        current_index = self._load_current_index()
        print(f"[PHASE 1] Loaded {len(current_index)} file criticality records")

        # Phase 2: Multi-agent architectural analysis
        enhanced_scores = await self._multi_agent_analysis(current_index)
        print(f"[PHASE 2] Enhanced {len(enhanced_scores)} criticality scores")

        # Phase 3: Create tachyonic shadow
        shadow_path = self._create_tachyonic_shadow(current_index)
        print(f"[PHASE 3] Created tachyonic shadow: {shadow_path}")

        # Phase 4: Update canonical index
        update_report = self._update_canonical_index(enhanced_scores)
<<<<<<< HEAD
        print(
            f"[PHASE 4] Updated canonical index with {update_report['changes']} changes"
        )

        # Phase 5: Validation and coherence check
        validation_report = await self._validate_evolution(
            current_index, enhanced_scores
        )
=======
        print(f"[PHASE 4] Updated canonical index with {update_report['changes']} changes")

        # Phase 5: Validation and coherence check
        validation_report = await self._validate_evolution(current_index, enhanced_scores)
>>>>>>> origin/OS0.6.2.grok
        print("[PHASE 5] Evolution validation complete")

        # Compile final report
        evolution_report = {
<<<<<<< HEAD
            "timestamp": datetime.now().isoformat(),
            "original_records": len(current_index),
            "enhanced_records": len(enhanced_scores),
            "tachyonic_shadow": str(shadow_path),
            "changes_made": update_report["changes"],
            "validation_results": validation_report,
            "agent_participation": {
                "ollama": self.use_ollama,
                "gemini": self.use_gemini,
                "vscode_chat": self.use_vscode_chat,
            },
        }

        print(
            f"[EVOLUTION COMPLETE] Criticality index evolved with {update_report['changes']} enhancements"
        )
=======
            'timestamp': datetime.now().isoformat(),
            'original_records': len(current_index),
            'enhanced_records': len(enhanced_scores),
            'tachyonic_shadow': str(shadow_path),
            'changes_made': update_report['changes'],
            'validation_results': validation_report,
            'agent_participation': {
                'ollama': self.use_ollama,
                'gemini': self.use_gemini,
                'vscode_chat': self.use_vscode_chat
            }
        }

        print(f"[EVOLUTION COMPLETE] Criticality index evolved with {update_report['changes']} enhancements")
>>>>>>> origin/OS0.6.2.grok
        return evolution_report

    def _load_current_index(self) -> List[Dict[str, Any]]:
        """Load current criticality index from canonical location."""
        if not self.canonical_index.exists():
            print(f"[WARNING] Canonical index not found: {self.canonical_index}")
            return []

        records = []
        try:
<<<<<<< HEAD
            with open(self.canonical_index, "r", encoding="utf-8") as f:
=======
            with open(self.canonical_index, 'r', encoding='utf-8') as f:
>>>>>>> origin/OS0.6.2.grok
                for line in f:
                    if line.strip():
                        records.append(json.loads(line.strip()))
        except Exception as e:
            print(f"[ERROR] Failed to load canonical index: {e}")
            return []

        return records

<<<<<<< HEAD
    async def _multi_agent_analysis(
        self, current_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
=======
    async def _multi_agent_analysis(self, current_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
>>>>>>> origin/OS0.6.2.grok
        """
        Execute multi-agent analysis to enhance criticality scores

        Process:
        1. Ollama: Fast dependency pattern analysis
        2. Gemini: Architectural validation and insights
        3. VSCode Chat: Strategic oversight and final decisions
        """
        enhanced_records = []

        for record in current_records:
            enhanced_record = await self._analyze_single_file(record)
            enhanced_records.append(enhanced_record)

        return enhanced_records

    async def _analyze_single_file(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze single file with multi-agent collaboration."""
<<<<<<< HEAD
        file_path = record.get("path", "")
        current_score = record.get("criticality_score", 0)
=======
        file_path = record.get('path', '')
        current_score = record.get('criticality_score', 0)
>>>>>>> origin/OS0.6.2.grok

        # Agent analysis prompts
        ollama_prompt = f"""
        Analyze file criticality for: {file_path}
        Current score: {current_score}
        Fan-in: {record.get('fan_in', 0)}
        Fan-out: {record.get('fan_out', 0)}

        Provide enhanced criticality assessment considering:
        - Dependency patterns
        - Architectural importance
        - Maintenance complexity

        Return JSON with enhanced_score and reasoning.
        """

        gemini_prompt = f"""
        Validate and enhance criticality analysis for: {file_path}

        Current metrics: {json.dumps(record, indent=2)}

        Consider:
        - Cloud architecture patterns
        - Scalability implications
        - Security criticality
        - Innovation potential

        Provide breakthrough insights for criticality scoring.
        """

        # Ollama analysis (fast local)
        ollama_insight = None
<<<<<<< HEAD
        if self.use_ollama and self.agents.get("ollama"):
            try:
                response = self.agents["ollama"].generate_code(ollama_prompt)
                if response.get("success"):
                    ollama_insight = response.get("code", "")
=======
        if self.use_ollama and self.agents.get('ollama'):
            try:
                response = self.agents['ollama'].generate_code(ollama_prompt)
                if response.get('success'):
                    ollama_insight = response.get('code', '')
>>>>>>> origin/OS0.6.2.grok
            except Exception as e:
                print(f"[OLLAMA ERROR] {file_path}: {e}")

        # Gemini analysis (cloud validation)
        gemini_insight = None
<<<<<<< HEAD
        if self.use_gemini and self.agents.get("gemini"):
            try:
                response = self.agents["gemini"].generate_code(gemini_prompt)
                if response.get("success"):
                    gemini_insight = response.get("code", "")
=======
        if self.use_gemini and self.agents.get('gemini'):
            try:
                response = self.agents['gemini'].generate_code(gemini_prompt)
                if response.get('success'):
                    gemini_insight = response.get('code', '')
>>>>>>> origin/OS0.6.2.grok
            except Exception as e:
                print(f"[GEMINI ERROR] {file_path}: {e}")

        # VSCode Chat strategic oversight
        strategic_decision = self._strategic_criticality_decision(
            record, ollama_insight, gemini_insight
        )

        # Apply enhancements
        enhanced_record = record.copy()
        enhanced_record.update(strategic_decision)

        # Log agentic conversation if logger available
        if self.agentic_logger:
            try:
                # Start conversation logging
                conversation_id = self.agentic_logger.start_conversation(
                    agent_type=AgentType.CUSTOM,  # Use CUSTOM for multi-agent orchestration
                    system_context=f"Multi-agent criticality evolution for file: {file_path}",
                    source_system="file_criticality_evolution_engine",
                    source_file=__file__,
<<<<<<< HEAD
                    consciousness_level="HIGH",
=======
                    consciousness_level="HIGH"
>>>>>>> origin/OS0.6.2.grok
                )

                if ollama_insight:
                    self.agentic_logger.add_message(
                        conversation_id,
                        ConversationRole.ASSISTANT,
<<<<<<< HEAD
                        f"Ollama analysis: {ollama_insight}",
=======
                        f"Ollama analysis: {ollama_insight}"
>>>>>>> origin/OS0.6.2.grok
                    )

                if gemini_insight:
                    self.agentic_logger.add_message(
                        conversation_id,
                        ConversationRole.ASSISTANT,
<<<<<<< HEAD
                        f"Gemini analysis: {gemini_insight}",
=======
                        f"Gemini analysis: {gemini_insight}"
>>>>>>> origin/OS0.6.2.grok
                    )

                self.agentic_logger.add_message(
                    conversation_id,
                    ConversationRole.SYSTEM,
<<<<<<< HEAD
                    f"Strategic decision: {strategic_decision}",
=======
                    f"Strategic decision: {strategic_decision}"
>>>>>>> origin/OS0.6.2.grok
                )

                self.agentic_logger.end_conversation(conversation_id)
            except Exception as e:
                print(f"[LOGGER ERROR] {file_path}: {e}")

        return enhanced_record

<<<<<<< HEAD
    def _strategic_criticality_decision(
        self,
        record: Dict[str, Any],
        ollama_insight: Optional[str],
        gemini_insight: Optional[str],
    ) -> Dict[str, Any]:
=======
    def _strategic_criticality_decision(self, record: Dict[str, Any],
                                       ollama_insight: Optional[str],
                                       gemini_insight: Optional[str]) -> Dict[str, Any]:
>>>>>>> origin/OS0.6.2.grok
        """
        Make strategic criticality decisions based on agent insights

        VSCode Chat role: Synthesize agent inputs into architectural decisions
        """
<<<<<<< HEAD
        file_path = record.get("path", "")
        current_score = record.get("criticality_score", 0)
=======
        file_path = record.get('path', '')
        current_score = record.get('criticality_score', 0)
>>>>>>> origin/OS0.6.2.grok

        # Base enhancement from agent insights
        enhancements = {}

        # Process Ollama insights (dependency-focused)
        if ollama_insight:
            try:
                ollama_data = json.loads(ollama_insight)
<<<<<<< HEAD
                if "enhanced_score" in ollama_data:
                    ollama_score = ollama_data["enhanced_score"]
                    enhancements["ollama_suggested_score"] = ollama_score
=======
                if 'enhanced_score' in ollama_data:
                    ollama_score = ollama_data['enhanced_score']
                    enhancements['ollama_suggested_score'] = ollama_score
>>>>>>> origin/OS0.6.2.grok
            except:
                pass

        # Process Gemini insights (architectural validation)
        if gemini_insight:
            try:
                gemini_data = json.loads(gemini_insight)
<<<<<<< HEAD
                if "enhanced_score" in gemini_data:
                    gemini_score = gemini_data["enhanced_score"]
                    enhancements["gemini_suggested_score"] = gemini_score
=======
                if 'enhanced_score' in gemini_data:
                    gemini_score = gemini_data['enhanced_score']
                    enhancements['gemini_suggested_score'] = gemini_score
>>>>>>> origin/OS0.6.2.grok
            except:
                pass

        # Strategic synthesis (VSCode Chat role)
        final_score = current_score

        # Weight agent suggestions
        agent_scores = []
<<<<<<< HEAD
        if "ollama_suggested_score" in enhancements:
            agent_scores.append(
                (enhancements["ollama_suggested_score"], 0.4)
            )  # 40% weight
        if "gemini_suggested_score" in enhancements:
            agent_scores.append(
                (enhancements["gemini_suggested_score"], 0.6)
            )  # 60% weight
=======
        if 'ollama_suggested_score' in enhancements:
            agent_scores.append((enhancements['ollama_suggested_score'], 0.4))  # 40% weight
        if 'gemini_suggested_score' in enhancements:
            agent_scores.append((enhancements['gemini_suggested_score'], 0.6))  # 60% weight
>>>>>>> origin/OS0.6.2.grok

        if agent_scores:
            weighted_sum = sum(score * weight for score, weight in agent_scores)
            total_weight = sum(weight for _, weight in agent_scores)
<<<<<<< HEAD
            final_score = (
                weighted_sum / total_weight if total_weight > 0 else current_score
            )
=======
            final_score = weighted_sum / total_weight if total_weight > 0 else current_score
>>>>>>> origin/OS0.6.2.grok

            # Bound to reasonable range
            final_score = max(0, min(125, final_score))

        # Update record
<<<<<<< HEAD
        enhancements["criticality_score"] = round(final_score, 2)
        enhancements["last_evolution"] = datetime.now().isoformat()
        enhancements["evolution_agents"] = {
            "ollama": self.use_ollama,
            "gemini": self.use_gemini,
            "vscode_chat": True,
=======
        enhancements['criticality_score'] = round(final_score, 2)
        enhancements['last_evolution'] = datetime.now().isoformat()
        enhancements['evolution_agents'] = {
            'ollama': self.use_ollama,
            'gemini': self.use_gemini,
            'vscode_chat': True
>>>>>>> origin/OS0.6.2.grok
        }

        return enhancements

    def _create_tachyonic_shadow(self, current_records: List[Dict[str, Any]]) -> Path:
        """Create tachyonic shadow of current state before evolution."""
<<<<<<< HEAD
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shadow_filename = f"file_criticality_index_{timestamp}.jsonl"
        shadow_path = self.tachyonic_archive / shadow_filename

        try:
            with open(shadow_path, "w", encoding="utf-8") as f:
                for record in current_records:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")

            # Update latest pointer
            latest_pointer = (
                self.tachyonic_archive / "file_criticality_index_latest.jsonl"
            )
            with open(latest_pointer, "w", encoding="utf-8") as f:
                for record in current_records:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
=======
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        shadow_filename = f'file_criticality_index_{timestamp}.jsonl'
        shadow_path = self.tachyonic_archive / shadow_filename

        try:
            with open(shadow_path, 'w', encoding='utf-8') as f:
                for record in current_records:
                    f.write(json.dumps(record, ensure_ascii=False) + '\n')

            # Update latest pointer
            latest_pointer = self.tachyonic_archive / 'file_criticality_index_latest.jsonl'
            with open(latest_pointer, 'w', encoding='utf-8') as f:
                for record in current_records:
                    f.write(json.dumps(record, ensure_ascii=False) + '\n')
>>>>>>> origin/OS0.6.2.grok

            print(f"[TACHYONIC SHADOW] Archived previous state: {shadow_path}")
            return shadow_path

        except Exception as e:
            print(f"[ERROR] Failed to create tachyonic shadow: {e}")
            raise

<<<<<<< HEAD
    def _update_canonical_index(
        self, enhanced_records: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
=======
    def _update_canonical_index(self, enhanced_records: List[Dict[str, Any]]) -> Dict[str, Any]:
>>>>>>> origin/OS0.6.2.grok
        """Update canonical criticality index with evolved scores."""
        changes = 0

        try:
<<<<<<< HEAD
            with open(self.canonical_index, "w", encoding="utf-8") as f:
                for record in enhanced_records:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    changes += 1

            print(f"[CANONICAL UPDATE] Updated index with {changes} records")
            return {"changes": changes, "success": True}

        except Exception as e:
            print(f"[ERROR] Failed to update canonical index: {e}")
            return {"changes": 0, "success": False, "error": str(e)}

    async def _validate_evolution(
        self,
        original_records: List[Dict[str, Any]],
        enhanced_records: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Validate evolution coherence and architectural compliance."""
        validation_results = {
            "coherence_check": True,
            "architectural_compliance": True,
            "score_distribution": {},
            "tier_changes": 0,
=======
            with open(self.canonical_index, 'w', encoding='utf-8') as f:
                for record in enhanced_records:
                    f.write(json.dumps(record, ensure_ascii=False) + '\n')
                    changes += 1

            print(f"[CANONICAL UPDATE] Updated index with {changes} records")
            return {'changes': changes, 'success': True}

        except Exception as e:
            print(f"[ERROR] Failed to update canonical index: {e}")
            return {'changes': 0, 'success': False, 'error': str(e)}

    async def _validate_evolution(self, original_records: List[Dict[str, Any]],
                                enhanced_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate evolution coherence and architectural compliance."""
        validation_results = {
            'coherence_check': True,
            'architectural_compliance': True,
            'score_distribution': {},
            'tier_changes': 0
>>>>>>> origin/OS0.6.2.grok
        }

        # Basic coherence checks
        if len(original_records) != len(enhanced_records):
<<<<<<< HEAD
            validation_results["coherence_check"] = False
            print("[VALIDATION WARNING] Record count mismatch")

        # Score distribution analysis
        scores = [r.get("criticality_score", 0) for r in enhanced_records]
        validation_results["score_distribution"] = {
            "min": min(scores) if scores else 0,
            "max": max(scores) if scores else 0,
            "avg": sum(scores) / len(scores) if scores else 0,
=======
            validation_results['coherence_check'] = False
            print("[VALIDATION WARNING] Record count mismatch")

        # Score distribution analysis
        scores = [r.get('criticality_score', 0) for r in enhanced_records]
        validation_results['score_distribution'] = {
            'min': min(scores) if scores else 0,
            'max': max(scores) if scores else 0,
            'avg': sum(scores) / len(scores) if scores else 0
>>>>>>> origin/OS0.6.2.grok
        }

        # Tier change analysis
        for orig, enhanced in zip(original_records, enhanced_records):
<<<<<<< HEAD
            orig_tier = orig.get("tier", "unknown")
            enhanced_tier = enhanced.get("tier", "unknown")
            if orig_tier != enhanced_tier:
                validation_results["tier_changes"] += 1

        print(
            f"[VALIDATION] Evolution coherent: {validation_results['coherence_check']}"
        )
=======
            orig_tier = orig.get('tier', 'unknown')
            enhanced_tier = enhanced.get('tier', 'unknown')
            if orig_tier != enhanced_tier:
                validation_results['tier_changes'] += 1

        print(f"[VALIDATION] Evolution coherent: {validation_results['coherence_check']}")
>>>>>>> origin/OS0.6.2.grok
        print(f"[VALIDATION] Tier changes: {validation_results['tier_changes']}")

        return validation_results


async def main():
    """Main execution for file criticality evolution."""
    print("[FILE CRITICALITY EVOLUTION ENGINE] Starting...")

    engine = FileCriticalityEvolutionEngine()

    try:
        evolution_report = await engine.evolve_criticality_index()

        # Save evolution report
<<<<<<< HEAD
        report_path = (
            engine.repo_root
            / "tachyonic"
            / "archive"
            / "evolution_reports"
            / f'criticality_evolution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(evolution_report, f, indent=2, ensure_ascii=False)

        print(f"[EVOLUTION COMPLETE] Report saved: {report_path}")
        print(
            f"[SUMMARY] Enhanced {evolution_report['enhanced_records']} criticality records"
        )
=======
        report_path = engine.repo_root / 'tachyonic' / 'archive' / 'evolution_reports' / f'criticality_evolution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(evolution_report, f, indent=2, ensure_ascii=False)

        print(f"[EVOLUTION COMPLETE] Report saved: {report_path}")
        print(f"[SUMMARY] Enhanced {evolution_report['enhanced_records']} criticality records")
>>>>>>> origin/OS0.6.2.grok

    except Exception as e:
        print(f"[ERROR] Criticality evolution failed: {e}")
        raise


<<<<<<< HEAD
if __name__ == "__main__":
    asyncio.run(main())
=======
if __name__ == '__main__':
    asyncio.run(main())
>>>>>>> origin/OS0.6.2.grok
