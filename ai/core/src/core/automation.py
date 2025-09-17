"""
Automation Manager for AIOS

This module handles intelligent automation tasks including
scheduling, execution, and workflow management.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AutomationManager:
    """
    Automation Manager
    Handles intelligent automation tasks and workflow management.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.is_initialized = False
        self.is_running = False
        self.task_classifier = config.get("taskClassifier", {})
        self.models = {}
        self.active_tasks = {}
        logger.info("Automation Manager initialized")

    async def initialize(self) -> bool:
        try:
            logger.info("Initializing automation models...")
            self.models["task_classifier"] = {
                "name": self.task_classifier.get("name", "unknown"),
                "type": self.task_classifier.get("type", "unknown"),
                "loaded": True,
                "classes": self.task_classifier.get("config", {}).get("classes", []),
            }
            self.is_initialized = True
            logger.info("Automation models initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize automation models: {e}")
            return False

    async def start(self) -> bool:
        if not self.is_initialized:
            logger.error("Automation Manager not initialized")
            return False
        try:
            logger.info("Starting automation services...")
            self.is_running = True
            logger.info("Automation services started successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to start automation services: {e}")
            return False

    async def stop(self):
        if not self.is_running:
            return
        logger.info("Stopping automation services...")
        for task_id in list(self.active_tasks.keys()):
            await self._stop_task(task_id)
        self.is_running = False
        logger.info("Automation services stopped")

    async def process_task(self, nlp_result: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_running:
            raise RuntimeError("Automation Manager is not running")
        try:
            task_type = self._classify_task(nlp_result)
            task_params = self._extract_task_params(nlp_result)
            task = {
                "id": f"task_{len(self.active_tasks) + 1}",
                "type": task_type,
                "params": task_params,
                "source": "nlp",
                "nlp_result": nlp_result,
            }
            result = await self.execute_task(task)
            return {
                "task_created": True,
                "task_id": task["id"],
                "task_type": task_type,
                "execution_result": result,
            }
        except Exception as e:
            logger.error(f"Error processing task: {e}")
            raise

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        if not self.is_running:
            raise RuntimeError("Automation Manager is not running")
        try:
            task_id = task.get("id", "unknown")
            task_type = task.get("type", "unknown")
            logger.info(f"Executing task {task_id} of type {task_type}")
            self.active_tasks[task_id] = {
                "task": task,
                "status": "running",
                "start_time": asyncio.get_event_loop().time(),
            }
            if task_type == "file_operation":
                result = await self._execute_file_operation(task)
            elif task_type == "system_command":
                result = await self._execute_system_command(task)
            elif task_type == "ui_action":
                result = await self._execute_ui_action(task)
            elif task_type == "data_processing":
                result = await self._execute_data_processing(task)
            else:
                result = await self._execute_generic_task(task)
            self.active_tasks[task_id]["status"] = "completed"
            self.active_tasks[task_id]["result"] = result
            self.active_tasks[task_id]["end_time"] = asyncio.get_event_loop().time()
            logger.info(f"Task {task_id} completed successfully")
            return {"task_id": task_id, "status": "completed", "result": result}
        except Exception as e:
            logger.error(f"Error executing task: {e}")
            if task_id in self.active_tasks:
                self.active_tasks[task_id]["status"] = "failed"
                self.active_tasks[task_id]["error"] = str(e)
            raise

    def _classify_task(self, nlp_result: Dict[str, Any]) -> str:
        entities = nlp_result.get("entities", [])
        input_text = nlp_result.get("input", "").lower()
        if any(
            word in input_text
            for word in ["file", "folder", "directory", "copy", "move"]
        ):
            return "file_operation"
        elif any(
            word in input_text for word in ["run", "execute", "command", "process"]
        ):
            return "system_command"
        elif any(
            word in input_text for word in ["click", "button", "window", "interface"]
        ):
            return "ui_action"
        elif any(
            word in input_text for word in ["data", "process", "analyze", "calculate"]
        ):
            return "data_processing"
        else:
            return "generic"

    def _extract_task_params(self, nlp_result: Dict[str, Any]) -> Dict[str, Any]:
        params = {}
        entities = nlp_result.get("entities", [])
        for entity in entities:
            if entity["type"] == "metric":
                params["metric"] = entity["value"]
            elif entity["type"] == "number":
                params["number"] = entity["value"]
        input_text = nlp_result.get("input", "")
        params["original_text"] = input_text
        return params

    async def _execute_file_operation(self, task: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.1)
        return {"operation": "file_operation", "result": "File operation completed"}

    async def _execute_system_command(self, task: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.1)
        return {"operation": "system_command", "result": "System command executed"}

    async def _execute_ui_action(self, task: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.1)
        return {"operation": "ui_action", "result": "UI action completed"}

    async def _execute_data_processing(self, task: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.2)
        return {"operation": "data_processing", "result": "Data processing completed"}

    async def _execute_generic_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.1)
        return {"operation": "generic", "result": "Generic task completed"}

    async def _stop_task(self, task_id: str):
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["status"] = "stopped"
            logger.info(f"Task {task_id} stopped")

    def get_status(self) -> Dict[str, Any]:
        return {
            "initialized": self.is_initialized,
            "running": self.is_running,
            "models": self.models,
            "active_tasks": len(self.active_tasks),
            "config": self.config,
        }

    async def health_check(self) -> Dict[str, Any]:
        try:
            test_task = {
                "id": "health_check_task",
                "type": "generic",
                "params": {"test": True},
            }
            test_result = await self.execute_task(test_task)
            return {
                "healthy": True,
                "test_result": test_result,
                "models_loaded": len(self.models) > 0,
                "active_tasks": len(self.active_tasks),
            }
        except Exception as e:
            logger.error(f"Automation health check failed: {e}")
            return {"healthy": False, "error": str(e)}
