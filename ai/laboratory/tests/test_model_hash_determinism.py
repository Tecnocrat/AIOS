"""Tests for deterministic model hash (CEL-HASH-02)."""
import os
import tempfile
import numpy as np
from ai.ai_cells.tensorflow_training_cell import TensorFlowTrainingCell, TrainingConfig


def test_deterministic_hash_length_and_format():
    cfg = TrainingConfig(model_name="hash_test_model", epochs=1)
    cell = TensorFlowTrainingCell(cfg)
    assert cell.create_model(input_shape=(4,), num_classes=3)
    x = np.random.random((20, 4)).astype(np.float32)
    y = np.random.randint(0, 3, 20)
    assert cell.train(x, y)
    with tempfile.TemporaryDirectory() as tmp:
        p = os.path.join(tmp, "exp")
        info = cell.export_for_cpp_inference(p)
        assert info is not None
        assert len(info.model_hash) == 64
        assert all(c in '0123456789abcdef' for c in info.model_hash)
