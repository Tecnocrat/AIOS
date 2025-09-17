"""Minimal tests for AI Cell Manager registry integration.

Focus: ensure registry returns tensorflow adapter and manager can register a workflow.
"""
import time
import numpy as np
from ai.ai_cells import list_adapters
from ai.ai_cells.ai_cell_manager import AICellManager, create_sample_workflow


def test_registry_lists_tensorflow():
    adapters = list_adapters()
    assert "tensorflow" in adapters


def test_manager_registers_workflow(tmp_path):
    mgr = AICellManager(workspace_path=str(tmp_path / "ws"))
    wf = create_sample_workflow()
    assert mgr.register_workflow(wf)


def test_manager_executes_minimal_workflow(tmp_path):
    mgr = AICellManager(workspace_path=str(tmp_path / "ws2"))
    wf = create_sample_workflow()
    assert mgr.register_workflow(wf)
    x_train = np.random.random((20, 10)).astype(np.float32)
    y_train = np.random.randint(0, 5, 20)
    x_val = np.random.random((5, 10)).astype(np.float32)
    y_val = np.random.randint(0, 5, 5)
    started = mgr.execute_workflow(wf.workflow_id, {
        'x_train': x_train,
        'y_train': y_train,
        'x_val': x_val,
        'y_val': y_val,
    })
    assert started
    deadline = time.time() + 60
    while time.time() < deadline:
        status = mgr.get_workflow_status(wf.workflow_id)
        if status and status.status in {"completed", "failed"}:
            break
        time.sleep(1)
    status = mgr.get_workflow_status(wf.workflow_id)
    assert status is not None
    assert status.status in {"completed", "failed"}
