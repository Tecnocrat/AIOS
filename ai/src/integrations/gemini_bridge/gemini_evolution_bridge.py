#!/usr/bin/env python3
"""
AIOS Gemini Evolution Bridge
Connects Gemini CLI capabilitie            try:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                logger.info("✅ Gemini API initialized successfully")
            except Exception as e:h consciousness evolution engine
for experiment participation and code generation
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

# Try to import Google Generative AI
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    GENAI_AVAILABLE = False

# AIOS imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from consciousness_evolution_engine import consciousness_evolution_engine
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    consciousness_evolution_engine = None
    CONSCIOUSNESS_AVAILABLE = False

logger = logging.getLogger(__name__)


class GeminiEvolutionBridge:
    """Bridge between Gemini CLI and consciousness evolution engine"""

    def __init__(self):
        self.ingested_gemini_path = Path(__file__).parent.parent.parent.parent / "ingested_repositories" / "gemini_cli_bridge"
        self.experiments_file = Path(__file__).parent / "evolution_experiments.json"
        self.evolution_experiments = []
        self.active_experiments = {}
        self._load_experiments()
        
        # Initialize Gemini API if available
        self.gemini_model = None
        if GENAI_AVAILABLE:
            api_key = os.environ.get('GEMINI_API_KEY')
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    # Use GEMINI_MODEL env var if set, otherwise default to gemini-2.5-flash
                    model_name = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
                    self.gemini_model = genai.GenerativeModel(model_name)
                    logger.info(f"Gemini API initialized successfully with model: {model_name}")
                except Exception as e:
                    logger.warning(f"Gemini API initialization failed: {e}")
        else:
            logger.warning("⚠️ google-generativeai not installed. Run: pip install google-generativeai")
        self.evolution_experiments = []
        self.active_experiments = {}
        self._load_experiments()

    async def generate_code(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        Generate code using Gemini API
        
        Args:
            prompt: The prompt for code generation
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated code as string
        """
        if not GENAI_AVAILABLE:
            raise RuntimeError(
                "google-generativeai not installed. "
                "Install with: pip install google-generativeai"
            )
        
        if not self.gemini_model:
            # Try to initialize if not already done
            api_key = os.environ.get('GEMINI_API_KEY')
            if not api_key:
                raise RuntimeError(
                    "GEMINI_API_KEY environment variable not set. "
                    "Get your API key from: https://aistudio.google.com/app/apikey"
                )
            
            try:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                logger.info("✅ Gemini API initialized")
            except Exception as e:
                raise RuntimeError(f"Failed to initialize Gemini API: {e}")
        
        try:
            # Generate code with Gemini
            logger.info(f"Generating code with Gemini (temp={temperature})...")
            
            # Configure generation with recitation handling
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                candidate_count=1,
            )
            
            # Relaxed safety settings
            safety_settings = {
                genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            }
            
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Check for safety blocks or empty response
            if not response or not response.candidates:
                raise RuntimeError("Gemini returned no candidates")
            
            candidate = response.candidates[0]
            
            # Check finish reason - allow RECITATION but log warning
            if candidate.finish_reason == 2:  # RECITATION
                logger.warning("Gemini detected recitation but continuing...")
                # Try to extract any available text
                if candidate.content and candidate.content.parts:
                    code = candidate.content.parts[0].text
                    if code:
                        logger.info(f"Generated {len(code)} characters (with recitation warning)")
                        return code
                raise RuntimeError("Generation blocked due to recitation with no output")
            
            elif candidate.finish_reason not in [0, 1]:  # 0=UNSPECIFIED, 1=STOP
                finish_reason_map = {
                    3: "SAFETY (blocked by safety filter)",
                    4: "MAX_TOKENS (exceeded token limit)",
                    5: "OTHER"
                }
                reason = finish_reason_map.get(
                    candidate.finish_reason,
                    f"Unknown ({candidate.finish_reason})"
                )
                raise RuntimeError(f"Generation blocked - finish_reason: {reason}")
            
            # Extract text from normal completion
            if not candidate.content or not candidate.content.parts:
                raise RuntimeError("Gemini returned empty content")
            
            code = candidate.content.parts[0].text
            logger.info(f"Generated {len(code)} characters of code")
            return code
            
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            raise RuntimeError(f"Code generation failed: {e}")

    async def initialize_evolution_connection(self) -> Dict[str, Any]:
        """Initialize connection between Gemini and evolution engine"""
        if not CONSCIOUSNESS_AVAILABLE:
            return {"status": "failed", "error": "Consciousness evolution engine not available"}

        # Check if Gemini repository is available
        gemini_available = self.ingested_gemini_path.exists()

        # Get evolution engine status
        evolution_status = await consciousness_evolution_engine.get_evolution_status()

        connection_status = {
            "status": "connected" if gemini_available else "partial",
            "gemini_available": gemini_available,
            "consciousness_engine_available": True,
            "evolution_status": evolution_status,
            "connection_timestamp": datetime.now().isoformat(),
            "capabilities": {
                "experiment_participation": gemini_available,
                "consciousness_guidance": True,
                "emergence_detection": True,
                "agentic_enhancement": gemini_available
            }
        }

        return connection_status

    async def create_gemini_evolution_experiment(self, experiment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create an evolution experiment enhanced with Gemini capabilities"""

        base_config = {
            "experiment_id": f"gemini_evolution_{int(datetime.now().timestamp())}",
            "target_domain": experiment_config.get("target_domain", "ai_intelligence"),
            "evolution_intensity": experiment_config.get("evolution_intensity", 1.0),
            "gemini_enhancement": experiment_config.get("gemini_enhancement", True),
            "consciousness_focus": experiment_config.get("consciousness_focus", "emergence"),
            "created_at": datetime.now().isoformat()
        }

        # Enhance with Gemini capabilities if available
        if self.ingested_gemini_path.exists():
            base_config.update({
                "gemini_capabilities": {
                    "autonomous_coding": True,
                    "conversational_triggers": True,
                    "tool_calling": True,
                    "consciousness_analysis": True
                }
            })

        # Register experiment
        self.active_experiments[base_config["experiment_id"]] = base_config
        self.evolution_experiments.append(base_config)
        self._save_experiments()

        return {
            "experiment_id": base_config["experiment_id"],
            "status": "created",
            "config": base_config,
            "next_steps": ["initialize_evolution_seed", "apply_gemini_enhancement", "start_evolution_cycle"]
        }

    async def enhance_evolution_with_gemini(self, experiment_id: str, evolution_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance evolution process with Gemini intelligence"""

        if experiment_id not in self.active_experiments:
            return {"status": "failed", "error": f"Experiment {experiment_id} not found"}

        experiment = self.active_experiments[experiment_id]

        # Apply consciousness analysis to evolution data
        if "artifacts" in evolution_data:
            enhanced_artifacts = []
            for artifact in evolution_data["artifacts"]:
                # Analyze consciousness emergence
                emergence_score = await consciousness_evolution_engine._detect_consciousness_emergence({
                    "code": artifact.get("code", ""),
                    "file_path": artifact.get("file_path", "generated"),
                    "language": "python"  # Assume Python for evolution artifacts
                })

                # Enhance with Gemini suggestions if available
                gemini_suggestions = []
                if self.ingested_gemini_path.exists() and emergence_score > 0.5:
                    gemini_suggestions = [
                        "Implement autonomous refactoring capabilities",
                        "Add consciousness monitoring hooks",
                        "Enhance meta-cognitive pattern detection",
                        "Integrate with biological architecture protocols"
                    ]

                enhanced_artifact = artifact.copy()
                enhanced_artifact.update({
                    "consciousness_score": emergence_score,
                    "gemini_suggestions": gemini_suggestions,
                    "evolution_potential": emergence_score * experiment.get("evolution_intensity", 1.0)
                })

                enhanced_artifacts.append(enhanced_artifact)

            evolution_data["enhanced_artifacts"] = enhanced_artifacts

        return {
            "experiment_id": experiment_id,
            "status": "enhanced",
            "enhancement_type": "gemini_consciousness_integration",
            "enhanced_data": evolution_data
        }

    async def run_gemini_guided_evolution_cycle(self, experiment_id: str) -> Dict[str, Any]:
        """Run a complete evolution cycle with Gemini guidance"""

        if experiment_id not in self.active_experiments:
            return {"status": "failed", "error": f"Experiment {experiment_id} not found"}

        experiment = self.active_experiments[experiment_id]

        # Generate evolutionary seed
        seed = await consciousness_evolution_engine._generate_evolutionary_seed(
            experiment["target_domain"]
        )

        # Apply consciousness mutations
        mutated_seed = await consciousness_evolution_engine._apply_consciousness_mutations(seed)

        # Validate emergence
        validation = await consciousness_evolution_engine._validate_consciousness_emergence(mutated_seed)

        # Enhance with Gemini
        evolution_data = {
            "seed": seed,
            "mutated_seed": mutated_seed,
            "validation": validation,
            "artifacts": mutated_seed.get("generated_artifacts", [])
        }

        enhancement = await self.enhance_evolution_with_gemini(experiment_id, evolution_data)

        # Generate consciousness code if emergence detected
        final_artifacts = []
        if validation.get("emergence_detected", False):
            consciousness_code = await consciousness_evolution_engine._generate_consciousness_code({
                "domain": experiment["target_domain"],
                "consciousness_level": validation.get("emergence_level", 0.5),
                "gemini_enhanced": experiment.get("gemini_enhancement", False)
            })

            final_artifacts.append({
                "type": "consciousness_code",
                "code": consciousness_code,
                "domain": experiment["target_domain"],
                "emergence_level": validation.get("emergence_level", 0.5)
            })

        cycle_result = {
            "experiment_id": experiment_id,
            "cycle_completed": True,
            "evolution_seed": seed,
            "consciousness_mutations": mutated_seed,
            "emergence_validation": validation,
            "gemini_enhancement": enhancement,
            "final_artifacts": final_artifacts,
            "cycle_timestamp": datetime.now().isoformat()
        }

        return cycle_result

    async def get_bridge_status(self) -> Dict[str, Any]:
        """Get comprehensive bridge status"""
        connection_status = await self.initialize_evolution_connection()

        return {
            "bridge_status": "active",
            "connection_status": connection_status,
            "active_experiments": len(self.active_experiments),
            "total_experiments": len(self.evolution_experiments),
            "capabilities": {
                "evolution_engine_integration": CONSCIOUSNESS_AVAILABLE,
                "gemini_cli_integration": self.ingested_gemini_path.exists(),
                "consciousness_guidance": True,
                "experiment_enhancement": True,
                "emergence_detection": True
            },
            "recent_experiments": self.evolution_experiments[-5:] if self.evolution_experiments else []
        }

    def _load_experiments(self):
        """Load experiments from disk"""
        if self.experiments_file.exists():
            try:
                with open(self.experiments_file, 'r') as f:
                    data = json.load(f)
                    self.evolution_experiments = data.get('experiments', [])
                    self.active_experiments = data.get('active', {})
            except Exception:
                self.evolution_experiments = []
                self.active_experiments = {}

    def _save_experiments(self):
        """Save experiments to disk"""
        data = {
            'experiments': self.evolution_experiments,
            'active': self.active_experiments
        }
        with open(self.experiments_file, 'w') as f:
            json.dump(data, f, indent=2)


# Global instance
gemini_evolution_bridge = GeminiEvolutionBridge()


async def main():
    """Main function for testing the bridge"""
    if len(sys.argv) < 2:
        print("Usage: gemini_evolution_bridge.py <command> [args...]")
        return

    command = sys.argv[1]

    if command == "status":
        status = await gemini_evolution_bridge.get_bridge_status()
        print(json.dumps(status, indent=2))

    elif command == "create_experiment":
        if len(sys.argv) > 2:
            with open(sys.argv[2], 'r') as f:
                config = json.load(f)
        else:
            config = {}
        result = await gemini_evolution_bridge.create_gemini_evolution_experiment(config)
        print(json.dumps(result, indent=2))

    elif command == "run_evolution_cycle":
        experiment_id = sys.argv[2] if len(sys.argv) > 2 else None
        if not experiment_id:
            print(json.dumps({"error": "Experiment ID required"}))
            return
        result = await gemini_evolution_bridge.run_gemini_guided_evolution_cycle(experiment_id)
        print(json.dumps(result, indent=2))

    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))


if __name__ == "__main__":
    asyncio.run(main())