"""
Test suite for TensorFlow Training Cell

Tests the Python AI training capabilities without requiring full TensorFlow installation.
"""

import sys
import os
import numpy as np
import tempfile
import shutil
from pathlib import Path

# Add the ai_cells package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ai_cells'))

from tensorflow_training_cell import TensorFlowTrainingCell, TrainingConfig


def test_training_cell_creation():
    """Test TensorFlow Training Cell creation"""
    print("Testing TensorFlow Training Cell creation...")
    
    config = TrainingConfig(
        model_name="test_model",
        learning_rate=0.001,
        batch_size=16,
        epochs=2
    )
    
    cell = TensorFlowTrainingCell(config)
    assert cell.config.model_name == "test_model"
    assert cell.config.learning_rate == 0.001
    assert not cell.is_trained
    
    print("✓ Training cell creation test passed")


def test_model_creation():
    """Test model creation"""
    print("Testing model creation...")
    
    config = TrainingConfig(model_name="test_model", epochs=1)
    cell = TensorFlowTrainingCell(config)
    
    # Test model creation
    success = cell.create_model(input_shape=(10,), num_classes=3)
    assert success
    assert cell.model is not None
    
    print("✓ Model creation test passed")


def test_training_workflow():
    """Test complete training workflow"""
    print("Testing complete training workflow...")
    
    config = TrainingConfig(
        model_name="test_training_model",
        epochs=2,
        batch_size=8
    )
    cell = TensorFlowTrainingCell(config)
    
    # Create model
    assert cell.create_model(input_shape=(5,), num_classes=2)
    
    # Create sample data
    x_train = np.random.random((100, 5)).astype(np.float32)
    y_train = np.random.randint(0, 2, 100)
    x_val = np.random.random((20, 5)).astype(np.float32)
    y_val = np.random.randint(0, 2, 20)
    
    # Train model
    success = cell.train(x_train, y_train, x_val, y_val)
    assert success
    assert cell.is_trained
    assert len(cell.training_history) == config.epochs
    
    # Check training metrics
    metrics = cell.get_training_metrics()
    assert len(metrics) == config.epochs
    assert all(m.epoch > 0 for m in metrics)
    
    print("✓ Training workflow test passed")


def test_model_export():
    """Test model export for C++ inference"""
    print("Testing model export...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config = TrainingConfig(model_name="export_test_model", epochs=1)
        cell = TensorFlowTrainingCell(config)
        
        # Create and train model
        assert cell.create_model(input_shape=(3,), num_classes=2)
        
        x_train = np.random.random((50, 3)).astype(np.float32)
        y_train = np.random.randint(0, 2, 50)
        
        assert cell.train(x_train, y_train)
        
        # Export model
        export_path = os.path.join(temp_dir, "exported_model")
        export_info = cell.export_for_cpp_inference(export_path)
        
        assert export_info is not None
        assert export_info.export_path == export_path
        assert export_info.estimated_inference_time > 0
        assert "shape" in export_info.input_signature
        assert "shape" in export_info.output_signature
        
        # Check that export files exist
        export_dir = Path(export_path)
        assert export_dir.exists()
        assert (export_dir / "export_metadata.json").exists()
        
        print("✓ Model export test passed")


def test_model_info():
    """Test model information retrieval"""
    print("Testing model info...")
    
    config = TrainingConfig(model_name="info_test_model", epochs=1)
    cell = TensorFlowTrainingCell(config)
    
    # Initial info
    info = cell.get_model_info()
    assert info["model_name"] == "info_test_model"
    assert not info["is_trained"]
    assert info["training_epochs"] == 0
    
    # After training
    assert cell.create_model(input_shape=(4,), num_classes=3)
    x_train = np.random.random((30, 4)).astype(np.float32)
    y_train = np.random.randint(0, 3, 30)
    assert cell.train(x_train, y_train)
    
    info = cell.get_model_info()
    assert info["is_trained"]
    assert info["training_epochs"] == 1
    assert "final_accuracy" in info
    assert "total_training_time" in info
    
    print("✓ Model info test passed")


def test_sample_workflow():
    """Test the sample workflow function"""
    print("Testing sample workflow...")
    
    from tensorflow_training_cell import create_sample_model_workflow
    
    # This should work even without TensorFlow installed (mock mode)
    success = create_sample_model_workflow()
    assert success
    
    print("✓ Sample workflow test passed")


def run_all_tests():
    """Run all TensorFlow Training Cell tests"""
    print("Running TensorFlow Training Cell Tests")
    print("=" * 50)
    
    try:
        test_training_cell_creation()
        test_model_creation()
        test_training_workflow()
        test_model_export()
        test_model_info()
        test_sample_workflow()
        
        print("\n🎉 All TensorFlow Training Cell tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)