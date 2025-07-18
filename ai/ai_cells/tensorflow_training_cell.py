"""
TensorFlow Training Cell for AIOS Cellular Ecosystem

This module provides Python-based AI training capabilities that integrate
seamlessly with C++ performance inference cells through intercellular bridges.
"""

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

# Optional TensorFlow import with graceful fallback
# and direct submodule imports
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import callbacks, layers, mixed_precision, optimizers

    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    keras = None
    layers = None
    mixed_precision = None
    callbacks = None
    optimizers = None
    print("Warning: TensorFlow/Keras not available. Using mock implementation.")


@dataclass
class TrainingConfig:
    """Configuration for TensorFlow training sessions"""

    model_name: str
    learning_rate: float = 0.001
    batch_size: int = 32
    epochs: int = 10
    validation_split: float = 0.2
    early_stopping_patience: int = 5
    export_format: str = "savedmodel"  # For C++ compatibility
    target_inference_time: float = 1.0  # Target < 1ms for C++ cell


@dataclass
class TrainingMetrics:
    """Training performance metrics"""

    epoch: int
    loss: float
    accuracy: float
    val_loss: float
    val_accuracy: float
    training_time: float


@dataclass
class ModelExport:
    """
    Model export information for C++ cells and advanced AIOS workflows.
    Includes geometry/fractality/iteration metadata for holographic/fractal/
    exotic architectures.
    """

    export_path: str
    model_format: str
    input_signature: Dict[str, Any]
    output_signature: Dict[str, Any]
    optimization_level: str
    estimated_inference_time: float
    export_time: float = 0.0  # Timestamp of export
    model_hash: str = ""  # Hash of exported model or metadata
    geometry_metadata: Dict[str, Any] = field(
        default_factory=dict
    )  # Fractal/holographic/exotic geometry
    extra: Dict[str, Any] = field(default_factory=dict)  # For future extensibility


class TensorFlowTrainingCell:
    """
    TensorFlow Training Cell for AIOS Cellular Ecosystem

    Provides complete model creation, training, and export pipeline
    optimized for integration with C++ Performance Cells.
    Extensible for future multi-framework fractal harmonization.
    """

    def __init__(self, config: TrainingConfig):
        """
        Initialize the TensorFlow Training Cell

        Args:
            config: Training configuration
        """
        self.config = config
        self.model: Optional[Any] = None
        self.training_history: List[TrainingMetrics] = []
        self.is_trained = False
        self.export_info: Optional[ModelExport] = None
        self.framework = "tensorflow" if TENSORFLOW_AVAILABLE else "mock"

        # Initialize TensorFlow settings if available
        if TENSORFLOW_AVAILABLE:
            # Configure for optimal training
            keras.backend.clear_session()
            # Enable mixed precision for performance
            policy = mixed_precision.Policy("mixed_float16")
            mixed_precision.set_global_policy(policy)
            print(
                "TensorFlow Training Cell initialized with GPU support: "
                f"{len(tf.config.list_physical_devices('GPU')) > 0}"
            )
        else:
            print("TensorFlow Training Cell initialized in mock mode")
        print(f"Running on OS: {os.name}")

    def create_model(self, input_shape: Tuple[int, ...], num_classes: int) -> bool:
        """
        Create a TensorFlow model optimized for C++ inference

        Args:
            input_shape: Input tensor shape
            num_classes: Number of output classes

        Returns:
            True if model created successfully
        """
        try:
            if TENSORFLOW_AVAILABLE:
                # Create a simple but effective model
                self.model = keras.Sequential(
                    [
                        layers.InputLayer(input_shape=input_shape),
                        layers.Dense(128, activation="relu"),
                        layers.Dropout(0.2),
                        layers.Dense(64, activation="relu"),
                        layers.Dropout(0.2),
                        layers.Dense(num_classes, activation="softmax"),
                    ]
                )

                # Compile with optimizer suitable for inference optimization
                self.model.compile(
                    optimizer=optimizers.Adam(learning_rate=self.config.learning_rate),
                    loss="sparse_categorical_crossentropy",
                    metrics=["accuracy"],
                )

                print(f"Model created successfully for " f"{self.config.model_name}")
                print("Model summary:")
                self.model.summary()

            else:
                # Mock model for testing without TensorFlow
                self.model = {
                    "type": "mock_model",
                    "input_shape": input_shape,
                    "num_classes": num_classes,
                    "parameters": 10000,  # Mock parameter count
                }
                print(f"Mock model created for {self.config.model_name}")

            return True

        except Exception as e:
            print(f"Error creating model: {e}")
            return False

    def train(
        self,
        x_train: np.ndarray,
        y_train: np.ndarray,
        x_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
    ) -> bool:
        """
        Train the model with performance monitoring

        Args:
            x_train: Training input data
            y_train: Training labels
            x_val: Validation input data (optional)
            y_val: Validation labels (optional)

        Returns:
            True if training completed successfully
        """
        if self.model is None:
            print("Error: No model created. Call create_model() first.")
            return False

        try:
            start_time = time.time()

            if TENSORFLOW_AVAILABLE:
                # Prepare callbacks for optimal training
                cb = [
                    callbacks.EarlyStopping(
                        patience=self.config.early_stopping_patience,
                        restore_best_weights=True,
                    ),
                    callbacks.ReduceLROnPlateau(factor=0.5, patience=3, min_lr=1e-7),
                ]

                # Train the model
                if x_val is not None and y_val is not None:
                    validation_data = (x_val, y_val)
                else:
                    validation_data = None

                history = self.model.fit(
                    x_train,
                    y_train,
                    batch_size=self.config.batch_size,
                    epochs=self.config.epochs,
                    validation_split=(
                        self.config.validation_split if validation_data is None else 0.0
                    ),
                    validation_data=validation_data,
                    callbacks=cb,
                    verbose=1,
                )

                # Record training metrics
                for epoch in range(len(history.history["loss"])):
                    metrics = TrainingMetrics(
                        epoch=epoch + 1,
                        loss=history.history["loss"][epoch],
                        accuracy=(
                            history.history.get("accuracy", [0])[epoch]
                            if "accuracy" in history.history
                            else 0.0
                        ),
                        val_loss=(
                            history.history.get("val_loss", [0])[epoch]
                            if "val_loss" in history.history
                            else 0.0
                        ),
                        val_accuracy=(
                            history.history.get("val_accuracy", [0])[epoch]
                            if "val_accuracy" in history.history
                            else 0.0
                        ),
                        training_time=time.time() - start_time,
                    )
                    self.training_history.append(metrics)

            else:
                # Mock training for testing without TensorFlow
                for epoch in range(self.config.epochs):
                    # Simulate improving metrics
                    loss = 1.0 - (epoch * 0.1)
                    accuracy = epoch * 0.1 + 0.1

                    metrics = TrainingMetrics(
                        epoch=epoch + 1,
                        loss=max(0.1, loss),
                        accuracy=min(0.95, accuracy),
                        val_loss=max(0.15, loss + 0.05),
                        val_accuracy=min(0.90, accuracy - 0.05),
                        training_time=time.time() - start_time,
                    )
                    self.training_history.append(metrics)

                    time.sleep(0.1)  # Simulate training time
                    print(
                        f"Epoch {epoch + 1}/{self.config.epochs} - "
                        "Mock training progress"
                    )

            self.is_trained = True
            training_time = time.time() - start_time
            print(f"Training completed in {training_time:.2f} seconds")
            return True

        except Exception as e:
            print(f"Error during training: {e}")
            return False

    def export_for_cpp_inference(self, export_path: str) -> Optional[ModelExport]:
        """
        Export model for C++ Performance Cell inference, including advanced geometry/fractality/iteration metadata.

        Args:
            export_path: Path to save the exported model

        Returns:
            ModelExport information or None if failed
        """
        # Environment-aware export base directory
        export_base = os.environ.get("AIOS_TF_EXPORT_DIR", None)
        if export_base:
            export_path = os.path.join(export_base, os.path.basename(export_path))
        export_dir = Path(export_path)
        # Directory existence and permissions check
        if not os.path.exists(export_path):
            try:
                os.makedirs(export_path, exist_ok=True)
            except Exception as e:
                print("Failed to create export directory: " f"{e}")
                return None
        if not os.access(export_path, os.W_OK):
            print(f"Export path {export_path} is not writable.")
            return None

        if not self.is_trained:
            print("Error: Model not trained. Call train() first.")
            return None

        try:
            export_time = time.time()
            if TENSORFLOW_AVAILABLE and self.model is not None:
                # Export as SavedModel format for C++ compatibility
                savedmodel_path = export_dir / "savedmodel"
                tf.saved_model.save(self.model, str(savedmodel_path))
                input_signature = {
                    "shape": list(self.model.input_shape),
                    "dtype": "float32",
                }
                output_signature = {
                    "shape": list(self.model.output_shape),
                    "dtype": "float32",
                }
                estimated_time = self.config.target_inference_time * 0.8
                # Geometry/fractality/iteration metadata
                geometry_metadata = {
                    "input_shape": list(self.model.input_shape),
                    "output_shape": list(self.model.output_shape),
                    "fractal_depth": getattr(self.model, "fractal_depth", None),
                    "holographic": getattr(self.model, "holographic", False),
                }
                # Compute model hash (simple hash of metadata file for demo)
                model_hash = str(
                    hash(
                        str(input_signature) + str(output_signature) + str(export_time)
                    )
                )
            else:
                # Mock export for testing
                mock_model_path = export_dir / "mock_model.json"
                with open(mock_model_path, "w") as f:
                    json.dump(self.model, f, indent=2)
                input_signature = {"shape": [1, 10], "dtype": "float32"}
                output_signature = {"shape": [1, 5], "dtype": "float32"}
                estimated_time = 0.5
                geometry_metadata = {
                    "input_shape": [1, 10],
                    "output_shape": [1, 5],
                    "fractal_depth": None,
                    "holographic": False,
                }
                model_hash = str(
                    hash(
                        str(input_signature) + str(output_signature) + str(export_time)
                    )
                )
            # Create export information
            self.export_info = ModelExport(
                export_path=str(export_dir),
                model_format=self.config.export_format,
                input_signature=input_signature,
                output_signature=output_signature,
                optimization_level="standard",
                estimated_inference_time=estimated_time,
                export_time=export_time,
                model_hash=model_hash,
                geometry_metadata=geometry_metadata,
                extra={
                    "notes": "Exported for AIOS C++ cell, supports fractal/holographic/iteration metadata"
                },
            )
            # Save export metadata
            metadata_path = export_dir / "export_metadata.json"
            with open(metadata_path, "w") as f:
                json.dump(
                    {
                        "model_name": self.config.model_name,
                        "export_format": self.export_info.model_format,
                        "input_signature": self.export_info.input_signature,
                        "output_signature": self.export_info.output_signature,
                        "optimization_level": self.export_info.optimization_level,
                        "estimated_inference_time_ms": self.export_info.estimated_inference_time,
                        "export_timestamp": self.export_info.export_time,
                        "training_epochs": len(self.training_history),
                        "final_accuracy": (
                            self.training_history[-1].accuracy
                            if self.training_history
                            else 0.0
                        ),
                        "model_hash": self.export_info.model_hash,
                        "geometry_metadata": self.export_info.geometry_metadata,
                        "extra": self.export_info.extra,
                    },
                    f,
                    indent=2,
                )
            print(f"Model exported successfully to {export_path}")
            print("Estimated C++ inference time: " f"{estimated_time:.3f}ms")
            return self.export_info
        except Exception as e:
            print(f"Error exporting model: {e}")
            return None

    def get_training_metrics(self) -> List[TrainingMetrics]:
        """Get training history metrics"""
        return self.training_history

    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        info = {
            "model_name": self.config.model_name,
            "is_trained": self.is_trained,
            "training_epochs": len(self.training_history),
            "tensorflow_available": TENSORFLOW_AVAILABLE,
        }

        if self.training_history:
            final_metrics = self.training_history[-1]
            info.update(
                {
                    "final_accuracy": final_metrics.accuracy,
                    "final_loss": final_metrics.loss,
                    "total_training_time": final_metrics.training_time,
                }
            )

        if self.export_info:
            info.update(
                {
                    "export_path": self.export_info.export_path,
                    "estimated_inference_time_ms": self.export_info.estimated_inference_time,
                }
            )

        return info


def create_sample_model_workflow() -> bool:
    """
    Create a sample workflow demonstrating TensorFlow Training Cell

    Returns:
        True if workflow completed successfully
    """
    print("Creating sample TensorFlow Training Cell workflow...")
    # Create training configuration
    config = TrainingConfig(
        model_name="sample_classification_model",
        learning_rate=0.001,
        batch_size=32,
        epochs=5,
        target_inference_time=0.8,  # Target < 0.8ms for C++ cell
    )
    # Initialize training cell
    cell = TensorFlowTrainingCell(config)
    # Create sample data
    x_train = np.random.random((1000, 10)).astype(np.float32)
    y_train = np.random.randint(0, 5, 1000)
    x_val = np.random.random((200, 10)).astype(np.float32)
    y_val = np.random.randint(0, 5, 200)
    # Environment-aware export base directory
    export_base = os.environ.get("AIOS_TF_EXPORT_DIR", "/tmp/aios_tensorflow_exports")
    export_path = os.path.join(export_base, "sample_model")
    # Create model
    if not cell.create_model(input_shape=(10,), num_classes=5):
        return False

    # Train model
    if not cell.train(x_train, y_train, x_val, y_val):
        return False

    # Export for C++ inference
    export_info = cell.export_for_cpp_inference(export_path)

    if export_info:
        print(f"\n✅ Sample workflow completed successfully!")
        print(f"Model exported to: {export_info.export_path}")
        print(
            "Estimated C++ inference time: "
            f"{export_info.estimated_inference_time:.3f}ms"
        )
        return True
    else:
        return False


if __name__ == "__main__":
    # Run sample workflow when executed directly
    success = create_sample_model_workflow()
    exit(0 if success else 1)
