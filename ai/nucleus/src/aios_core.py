"""
AIOS AI Core Logic (extracted from __init__.py)
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from .core.automation import AutomationManager
from .core.integration import IntegrationBridge
from .core.learning import LearningManager
from .core.nlp import NLPManager
from .core.prediction import PredictionManager
from .maintenance.system_health import (
    run_system_health_check_async,
)

# AINLP.loader [latent:List] (auto.AINLP.class)
#   from typing import List
#   Reason: Reserved for future type annotations, microarchitectural
#   expansion, and holographic self-reliance.
#   AINLP.mind: Consider if/when List is needed for future subsystem
#   harmonization or AI self-conscious layer upgrades.

# AINLP.loader [latent:Union] (auto.AINLP.class)
#   from typing import Union
#   Reason: Reserved for future type annotations, multi-type interface
#   expansion, and emergent complexity.
#   AINLP.mind: Consider if/when Union is needed for polymorphic API or
#   advanced context harmonization.


logger = logging.getLogger(__name__)


class AICore:
    """
    Main AI Core class that orchestrates all AI functionality.
    """

    def __init__(self, config_path: str = "../../infrastructure/config/ai-models.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.is_initialized = False
        self.is_running = False
        self.nlp_manager = NLPManager(self.config.get("models", {}).get("nlp", {}))
        self.prediction_manager = PredictionManager(
            self.config.get("models", {}).get("prediction", {})
        )
        self.automation_manager = AutomationManager(
            self.config.get("models", {}).get("automation", {})
        )
        self.learning_manager = LearningManager(self.config.get("training", {}))
        self.integration_bridge = IntegrationBridge(self.config.get("integration", {}))
        logger.info("AI Core initialized with config: %s", config_path)

    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(
                "Config file not found: %s, using defaults", self.config_path
            )
            return {}
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON in config file: %s", e)
            raise

    async def initialize(self) -> bool:
        try:
            logger.info("Initializing AI Core subsystems...")
            await self.nlp_manager.initialize()
            await self.prediction_manager.initialize()
            await self.automation_manager.initialize()
            await self.learning_manager.initialize()
            await self.integration_bridge.initialize()
            self.is_initialized = True
            logger.info("AI Core initialization completed successfully")
            # Fire-and-forget a background system health scan after init
            try:
                asyncio.create_task(run_system_health_check_async())
            except Exception as _exc:
                logger.debug("Health check scheduling failed: %s", _exc)
            return True
        except Exception as e:
            logger.error("Failed to initialize AI Core: %s", e)
            # Attempt a health scan to capture diagnostics on failure
            try:
                asyncio.create_task(run_system_health_check_async())
            except Exception:
                pass
            return False

    async def start(self) -> bool:
        if not self.is_initialized:
            logger.error("AI Core not initialized. Call initialize() first.")
            return False
        try:
            logger.info("Starting AI Core services...")
            await self.nlp_manager.start()
            await self.prediction_manager.start()
            await self.automation_manager.start()
            await self.learning_manager.start()
            await self.integration_bridge.start()
            self.is_running = True
            logger.info("AI Core services started successfully")
            # Opportunistic background system health scan after start
            try:
                asyncio.create_task(run_system_health_check_async())
            except Exception as _exc:
                logger.debug("Health check scheduling failed: %s", _exc)
            return True
        except Exception as e:
            logger.error("Failed to start AI Core services: %s", e)
            # Attempt a health scan to capture diagnostics on failure
            try:
                asyncio.create_task(run_system_health_check_async())
            except Exception:
                pass
            return False

    async def stop(self):
        if not self.is_running:
            return
        logger.info("Stopping AI Core services...")
        await self.integration_bridge.stop()
        await self.learning_manager.stop()
        await self.automation_manager.stop()
        await self.prediction_manager.stop()
        await self.nlp_manager.stop()
        self.is_running = False
        logger.info("AI Core services stopped")

    async def process_natural_language(
        self, text: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not self.is_running:
            raise RuntimeError("AI Core is not running")
        try:
            nlp_result = await self.nlp_manager.process(text, context)
            intent = nlp_result.get("intent", "unknown")
            if intent == "automation":
                automation_result = await self.automation_manager.process_task(
                    nlp_result
                )
                return {
                    "status": "success",
                    "intent": intent,
                    "nlp_result": nlp_result,
                    "automation_result": automation_result,
                }
            if intent == "prediction":
                prediction_result = await self.prediction_manager.predict(nlp_result)
                return {
                    "status": "success",
                    "intent": intent,
                    "nlp_result": nlp_result,
                    "prediction_result": prediction_result,
                }
            return {
                "status": "success",
                "intent": intent,
                "nlp_result": nlp_result,
                "message": "Natural language processed successfully",
            }
        except Exception as e:
            logger.error("Error processing natural language: %s", e)
            return {
                "status": "error",
                "error": str(e),
                "message": "Failed to process natural language input",
            }

    async def get_system_prediction(
        self, metric: str, horizon: int = 60
    ) -> Dict[str, Any]:
        if not self.is_running:
            raise RuntimeError("AI Core is not running")
        return await self.prediction_manager.predict_resource(metric, horizon)

    async def execute_automation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_running:
            raise RuntimeError("AI Core is not running")
        return await self.automation_manager.execute_task(task)

    async def update_learning(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_running:
            raise RuntimeError("AI Core is not running")
        return await self.learning_manager.update(data)

    def get_status(self) -> Dict[str, Any]:
        """Return the status of the AI Core and its subsystems."""
        return {
            "core": {
                "initialized": self.is_initialized,
                "running": self.is_running,
                "config_path": str(self.config_path),
            },
            "subsystems": {
                "nlp": self.nlp_manager.get_status(),
                "prediction": self.prediction_manager.get_status(),
                "automation": self.automation_manager.get_status(),
                "learning": self.learning_manager.get_status(),
                "integration": self.integration_bridge.get_status(),
            },
        }

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check on all AI Core subsystems."""
        health_results = {}
        try:
            health_results["nlp"] = await self.nlp_manager.health_check()
            health_results["prediction"] = await self.prediction_manager.health_check()
            health_results["automation"] = await self.automation_manager.health_check()
            health_results["learning"] = await self.learning_manager.health_check()
            health_results["integration"] = await self.integration_bridge.health_check()
            all_healthy = all(
                result.get("healthy", False) for result in health_results.values()
            )
            return {
                "overall_health": ("healthy" if all_healthy else "unhealthy"),
                "subsystems": health_results,
                "timestamp": asyncio.get_event_loop().time(),
            }
        except Exception as exc:  # More specific than bare Exception
            logger.error("Health check failed: %s", exc)
            return {
                "overall_health": "error",
                "error": str(exc),
                "timestamp": asyncio.get_event_loop().time(),
            }


# Global AI Core instance
_ai_core_instance: Optional[AICore] = None


def get_ai_core() -> AICore:
    """Return the global AI Core instance."""
    global _ai_core_instance
    if _ai_core_instance is None:
        _ai_core_instance = AICore()
    return _ai_core_instance


async def initialize_ai_core(
    config_path: str = "../../infrastructure/config/ai-models.json",
) -> bool:
    """Initialize the global AI Core instance."""
    global _ai_core_instance
    _ai_core_instance = AICore(config_path)
    return await _ai_core_instance.initialize()


async def start_ai_core() -> bool:
    """Start the global AI Core instance."""
    ai_core = get_ai_core()
    return await ai_core.start()


async def stop_ai_core():
    """Stop the global AI Core instance."""
    global _ai_core_instance
    if _ai_core_instance is not None:
        await _ai_core_instance.stop()
        _ai_core_instance = None
