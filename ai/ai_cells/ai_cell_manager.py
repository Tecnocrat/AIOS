"""
AI Cell Manager for AIOS Cellular Ecosystem

Orchestrates training workflows and coordinates communication between
Python AI Training Cells and C++ Performance Inference Cells.
"""

import logging
# import os AINLP.loader [latent:os] (auto.AINLP.class)
# import json AINLP.loader [latent:json] (auto.AINLP.class)
import time
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# Import AIOS cellular components
from .tensorflow_training_cell import TrainingConfig
from . import create_training_cell, TrainingCellProtocol


@dataclass
class CellularWorkflow:
    """Definition of a cellular AI workflow"""
    workflow_id: str
    name: str
    description: str
    training_config: TrainingConfig
    data_pipeline: Optional[Callable] = None
    post_training_hooks: List[Callable] = None
    target_deployment: str = "cpp_inference_cell"


@dataclass
class WorkflowStatus:
    """Status of a cellular workflow execution"""
    workflow_id: str
    status: str  # 'pending', 'training', 'exporting', 'completed', 'failed'
    progress: float  # 0.0 to 1.0
    current_epoch: int
    total_epochs: int
    estimated_completion_time: float
    error_message: Optional[str] = None


@dataclass
class IntercellularMessage:
    """Message for intercellular communication"""
    source_cell: str
    target_cell: str
    message_type: str
    payload: Dict[str, Any]
    timestamp: float
    priority: int = 0  # 0 = normal, 1 = high, 2 = critical


class AICellManager:
    """
    AI Cell Manager for AIOS Cellular Ecosystem

    Orchestrates training workflows and coordinates communication between
    Python AI Training Cells and C++ Performance Inference Cells.
    """

    def __init__(self, workspace_path: str = "/tmp/aios_cellular_workspace"):
        """
        Initialize the AI Cell Manager

        Args:
            workspace_path: Path for cellular workspace and model exports
        """
        self.workspace_path = Path(workspace_path)
        self.workspace_path.mkdir(parents=True, exist_ok=True)

        # Cellular ecosystem state
        self.active_workflows = {}  # type: Dict[str, CellularWorkflow]
        self.workflow_status = {}  # type: Dict[str, WorkflowStatus]
        self.training_cells = {}  # type: Dict[str, TrainingCellProtocol]
        self.intercellular_messages = []  # type: List[IntercellularMessage]

        # Execution management
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.active_futures = {}  # type: Dict[str, Future]

        # Setup logging
        self._setup_logging()

        self.logger.info(
            "AI Cell Manager initialized for AIOS Cellular Ecosystem"
        )
        self.logger.info(f"Workspace: {self.workspace_path}")

    def _setup_logging(self):
        """Setup logging for the cell manager"""
        log_path = self.workspace_path / "logs"
        log_path.mkdir(exist_ok=True)

        self.logger = logging.getLogger("AICellManager")
        self.logger.setLevel(logging.INFO)

        # File handler
        file_handler = logging.FileHandler(log_path / "cell_manager.log")
        file_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(name)s %(levelname)s %(message)s'
            )
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter('%(levelname)s - %(message)s')
        )

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def register_workflow(self, workflow: CellularWorkflow) -> bool:
        """
        Register a new cellular workflow

        Args:
            workflow: The workflow to register

        Returns:
            True if registration successful
        """
        try:
            if workflow.workflow_id in self.active_workflows:
                self.logger.warning(f"Workflow {workflow.workflow_id} already registered")
                return False

            self.active_workflows[workflow.workflow_id] = workflow
            self.workflow_status[workflow.workflow_id] = WorkflowStatus(
                workflow_id=workflow.workflow_id,
                status="pending",
                progress=0.0,
                current_epoch=0,
                total_epochs=workflow.training_config.epochs,
                estimated_completion_time=0.0
            )

            self.logger.info(f"Registered workflow: {workflow.name} ({workflow.workflow_id})")
            return True

        except Exception as e:
            self.logger.error(f"Error registering workflow: {e}")
            return False

    def execute_workflow(self, workflow_id: str, training_data: Dict[str, Any]) -> bool:
        """
        Execute a cellular workflow asynchronously

        Args:
            workflow_id: ID of the workflow to execute
            training_data: Training data dict with 'x_train', 'y_train', etc.

        Returns:
            True if execution started successfully
        """
        if workflow_id not in self.active_workflows:
            self.logger.error(f"Workflow {workflow_id} not found")
            return False

        if workflow_id in self.active_futures:
            self.logger.warning(f"Workflow {workflow_id} already executing")
            return False

        try:
            workflow = self.active_workflows[workflow_id]
            self.workflow_status[workflow_id].status = "training"

            # Submit workflow execution to thread pool
            future = self.executor.submit(self._execute_workflow_impl, workflow, training_data)
            self.active_futures[workflow_id] = future

            self.logger.info(f"Started execution of workflow: {workflow.name}")
            return True

        except Exception as e:
            self.logger.error(f"Error starting workflow execution: {e}")
            self.workflow_status[workflow_id].status = "failed"
            self.workflow_status[workflow_id].error_message = str(e)
            return False

    def _execute_workflow_impl(self, workflow: CellularWorkflow, training_data: Dict[str, Any]):
        """
        Internal implementation of workflow execution

        Args:
            workflow: The workflow to execute
            training_data: Training data
        """
        workflow_id = workflow.workflow_id

        try:
            self.logger.info(f"Executing cellular workflow: {workflow.name}")

            # Create and initialize training cell
            try:
                training_cell = create_training_cell("tensorflow", workflow.training_config)
            except KeyError as e:
                raise RuntimeError(f"Requested framework not available: {e}")
            self.training_cells[workflow_id] = training_cell

            # Extract training data
            x_train = training_data.get('x_train')
            y_train = training_data.get('y_train')
            x_val = training_data.get('x_val')
            y_val = training_data.get('y_val')

            if x_train is None or y_train is None:
                raise ValueError("Training data (x_train, y_train) required")

            # Apply data pipeline if provided
            if workflow.data_pipeline:
                self.logger.info("Applying data pipeline transformations...")
                x_train, y_train, x_val, y_val = workflow.data_pipeline(x_train, y_train, x_val, y_val)

            # Determine input shape and number of classes
            input_shape = x_train.shape[1:] if len(x_train.shape) > 1 else (x_train.shape[0],)
            num_classes = len(set(y_train)) if hasattr(y_train, '__iter__') else 10

            # Create model
            self.logger.info("Creating model...")
            if not training_cell.create_model(input_shape, num_classes):
                raise RuntimeError("Failed to create model")

            # Update progress
            self.workflow_status[workflow_id].progress = 0.1

            # Send intercellular message about training start
            self._send_intercellular_message(
                source_cell="ai_cell_manager",
                target_cell="system_monitor",
                message_type="training_started",
                payload={
                    "workflow_id": workflow_id,
                    "model_name": workflow.training_config.model_name,
                    "input_shape": input_shape,
                    "num_classes": num_classes
                }
            )

            # Train model with progress tracking
            self.logger.info("Starting model training...")

            # Custom training loop with progress updates
            start_time = time.time()
            if not training_cell.train(x_train, y_train, x_val, y_val):
                raise RuntimeError("Training failed")

            training_time = time.time() - start_time
            self.workflow_status[workflow_id].progress = 0.8

            # Run post-training hooks
            if workflow.post_training_hooks:
                self.logger.info("Running post-training hooks...")
                for hook in workflow.post_training_hooks:
                    hook(training_cell, workflow)

            # Export model for C++ inference cell
            self.logger.info("Exporting model for C++ inference cell...")
            self.workflow_status[workflow_id].status = "exporting"

            export_path = self.workspace_path / "exports" / workflow_id
            export_info = training_cell.export_for_cpp_inference(str(export_path))

            if not export_info:
                raise RuntimeError("Model export failed")

            # Send intercellular message about completion
            self._send_intercellular_message(
                source_cell="ai_cell_manager",
                target_cell="cpp_inference_cell",
                message_type="model_ready",
                payload={
                    "workflow_id": workflow_id,
                    "export_path": export_info.export_path,
                    "model_format": export_info.model_format,
                    "estimated_inference_time_ms": export_info.estimated_inference_time,
                    "input_signature": export_info.input_signature,
                    "output_signature": export_info.output_signature
                },
                priority=1  # High priority for deployment
            )

            # Update final status
            self.workflow_status[workflow_id].status = "completed"
            self.workflow_status[workflow_id].progress = 1.0

            self.logger.info(f"Workflow {workflow.name} completed successfully!")
            self.logger.info(f"Training time: {training_time:.2f}s")
            self.logger.info(f"Model exported to: {export_info.export_path}")
            self.logger.info(f"Estimated C++ inference time: {export_info.estimated_inference_time:.3f}ms")

        except Exception as e:
            self.logger.error(f"Workflow {workflow_id} failed: {e}")
            self.workflow_status[workflow_id].status = "failed"
            self.workflow_status[workflow_id].error_message = str(e)

            # Send failure message
            self._send_intercellular_message(
                source_cell="ai_cell_manager",
                target_cell="system_monitor",
                message_type="workflow_failed",
                payload={
                    "workflow_id": workflow_id,
                    "error": str(e)
                },
                priority=2  # Critical priority for failures
            )

        finally:
            # Clean up
            if workflow_id in self.active_futures:
                del self.active_futures[workflow_id]

    def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowStatus]:
        """Get the status of a workflow"""
        return self.workflow_status.get(workflow_id)

    def list_active_workflows(self) -> List[str]:
        """Get list of active workflow IDs"""
        return list(self.active_workflows.keys())

    def get_training_cell(self, workflow_id: str) -> Optional[TrainingCellProtocol]:
        """Get the training cell for a workflow"""
        return self.training_cells.get(workflow_id)

    def _send_intercellular_message(self, source_cell: str, target_cell: str,
                                   message_type: str, payload: Dict[str, Any],
                                   priority: int = 0):
        """Send an intercellular message"""
        message = IntercellularMessage(
            source_cell=source_cell,
            target_cell=target_cell,
            message_type=message_type,
            payload=payload,
            timestamp=time.time(),
            priority=priority
        )

        self.intercellular_messages.append(message)
        self.logger.debug(f"Sent message: {source_cell} -> {target_cell} ({message_type})")

    def get_intercellular_messages(self, target_cell: Optional[str] = None) -> List[IntercellularMessage]:
        """Get intercellular messages, optionally filtered by target cell"""
        if target_cell:
            return [msg for msg in self.intercellular_messages if msg.target_cell == target_cell]
        return self.intercellular_messages

    def clear_intercellular_messages(self):
        """Clear intercellular message queue"""
        self.intercellular_messages.clear()

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            "active_workflows": len(self.active_workflows),
            "running_workflows": len([s for s in self.workflow_status.values()
                                    if s.status in ["training", "exporting"]]),
            "completed_workflows": len([s for s in self.workflow_status.values()
                                      if s.status == "completed"]),
            "failed_workflows": len([s for s in self.workflow_status.values()
                                   if s.status == "failed"]),
            "pending_messages": len(self.intercellular_messages),
            "workspace_path": str(self.workspace_path),
            "executor_active": not self.executor._shutdown
        }

    def shutdown(self):
        """Shutdown the cell manager and cleanup resources"""
        self.logger.info("Shutting down AI Cell Manager...")

        # Wait for active workflows to complete
        for workflow_id, future in self.active_futures.items():
            self.logger.info(f"Waiting for workflow {workflow_id} to complete...")
            try:
                future.result(timeout=30)  # 30 second timeout
            except Exception as e:
                self.logger.warning(f"Workflow {workflow_id} terminated with error: {e}")

        # Shutdown executor
        self.executor.shutdown(wait=True)

        self.logger.info("AI Cell Manager shutdown complete")


def create_sample_workflow() -> CellularWorkflow:
    """Create a sample cellular workflow for testing"""
    config = TrainingConfig(
        model_name="sample_cellular_model",
        learning_rate=0.001,
        batch_size=32,
        epochs=3,
        target_inference_time=0.5  # Target < 0.5ms for C++ cell
    )

    return CellularWorkflow(
        workflow_id="sample_workflow_001",
        name="Sample Classification Workflow",
        description="Sample workflow demonstrating Python training → C++ inference",
        training_config=config,
        target_deployment="cpp_inference_cell"
    )


if __name__ == "__main__":
    # Demo of AI Cell Manager
    import numpy as np

    print("AIOS AI Cell Manager Demo")
    print("=" * 40)

    # Initialize cell manager
    manager = AICellManager()

    # Create and register sample workflow
    workflow = create_sample_workflow()
    if manager.register_workflow(workflow):
        print(f"✓ Registered workflow: {workflow.name}")

    # Create sample training data
    x_train = np.random.random((1000, 10)).astype(np.float32)
    y_train = np.random.randint(0, 5, 1000)
    x_val = np.random.random((200, 10)).astype(np.float32)
    y_val = np.random.randint(0, 5, 200)

    training_data = {
        'x_train': x_train,
        'y_train': y_train,
        'x_val': x_val,
        'y_val': y_val
    }

    # Execute workflow
    if manager.execute_workflow(workflow.workflow_id, training_data):
        print(f"✓ Started workflow execution")

        # Monitor progress
        while True:
            status = manager.get_workflow_status(workflow.workflow_id)
            if status:
                print(f"Status: {status.status}, Progress: {status.progress:.2f}")

                if status.status in ["completed", "failed"]:
                    break

                time.sleep(2)

    # Show system status
    system_status = manager.get_system_status()
    print(f"\nSystem Status: {system_status}")

    # Show intercellular messages
    messages = manager.get_intercellular_messages()
    print(f"\nIntercellular Messages: {len(messages)}")
    for msg in messages[-3:]:  # Show last 3 messages
        print(f"  {msg.source_cell} -> {msg.target_cell}: {msg.message_type}")

    # Cleanup
    manager.shutdown()
    print("\n✓ Demo completed")
