import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import pytest

# Ensure package paths are available
ROOT = Path(__file__).resolve().parents[1]
for extra in [ROOT, ROOT / "src", ROOT / "ai_cells", ROOT / "intercellular"]:
    p = str(extra)
    if p not in sys.path:
        sys.path.insert(0, p)

from tensorflow_training_cell import TensorFlowTrainingCell, TrainingConfig  # type: ignore


@pytest.fixture(scope="session")
def export_info(tmp_path_factory):
    """Train and export a tiny model once per session and return export_info."""
    tmp_dir = tmp_path_factory.mktemp("tf_export")
    config = TrainingConfig(model_name="fixture_model", epochs=1, batch_size=8)
    cell = TensorFlowTrainingCell(config)
    assert cell.create_model(input_shape=(5,), num_classes=3)

    # Minimal data for quick run
    x = np.random.random((30, 5)).astype(np.float32)
    y = np.random.randint(0, 3, 30)
    assert cell.train(x, y)

    export_path = str(tmp_dir / "exported_model")
    info = cell.export_for_cpp_inference(export_path)
    assert info is not None
    return info


@pytest.fixture(scope="session")
def test_data():
    """Provide a small test tensor pair (x, y)."""
    x_val = np.random.random((10, 5)).astype(np.float32)
    y_val = np.random.randint(0, 3, 10)
    return (x_val, y_val)
# Ensure test imports resolve across project structure
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Add ai root, src, ai_cells, intercellular to sys.path
paths = [
    ROOT,
    ROOT / 'src',
    ROOT / 'ai_cells',
    ROOT / 'intercellular',
]
for p in paths:
    p = str(p)
    if p not in sys.path:
        sys.path.insert(0, p)
