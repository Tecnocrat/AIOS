"""
AIOS Cellular Integration Test Script

This script tests the harmonized integration of ai_cells core components:
- AICellManager
- TensorFlowTrainingCell (via protocol)
- Adapter registry

This is not a unit test, but a protocol/integration smoke test.
"""
import sys
import os
import numpy as np
# Ensure the ai_cells module is importable when running from the tests folder
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)


def test_ai_cells_integration():
    from ai_cells.ai_cell_manager import AICellManager, create_sample_workflow
    manager = AICellManager()
    workflow = create_sample_workflow()
    assert manager.register_workflow(workflow), "Workflow registration failed"
    x_train = np.random.random((100, 10)).astype(np.float32)
    y_train = np.random.randint(0, 5, 100)
    x_val = np.random.random((20, 10)).astype(np.float32)
    y_val = np.random.randint(0, 5, 20)
    training_data = {
        'x_train': x_train,
        'y_train': y_train,
        'x_val': x_val,
        'y_val': y_val
    }
    assert manager.execute_workflow(
        workflow.workflow_id, training_data
    ), "Workflow execution failed"
    # Wait for completion
    import time
    while True:
        status = manager.get_workflow_status(workflow.workflow_id)
        if status and status.status in ["completed", "failed"]:
            break
        time.sleep(1)
    assert status.status == "completed", (
        f"Workflow did not complete: {status.status}"
    )
    print("AIOS ai_cells integration test PASSED.")


if __name__ == "__main__":
    test_ai_cells_integration()
