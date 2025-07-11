"""
AIOS AI Cells Package

This package provides AI training capabilities for the AIOS cellular ecosystem,
enabling seamless communication between Python AI training cells and C++
high-performance inference cells.
"""

from .tensorflow_training_cell import (
    TensorFlowTrainingCell,
    TrainingConfig,
    TrainingMetrics,
    ModelExport,
    create_sample_model_workflow
)

from .ai_cell_manager import (
    AICellManager,
    CellularWorkflow,
    WorkflowStatus,
    IntercellularMessage,
    create_sample_workflow
)

__version__ = "0.4.0"
__author__ = "AIOS Team"

__all__ = [
    # TensorFlow Training Cell
    "TensorFlowTrainingCell",
    "TrainingConfig", 
    "TrainingMetrics",
    "ModelExport",
    "create_sample_model_workflow",
    
    # AI Cell Manager
    "AICellManager",
    "CellularWorkflow",
    "WorkflowStatus", 
    "IntercellularMessage",
    "create_sample_workflow"
]