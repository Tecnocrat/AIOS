"""
Comprehensive Test Suite for AIOS Fractal Holographic System
This test suite validates the fractal/holographic development protocol
and context recovery system.
"""

import asyncio
import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

# Add the source directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from integration.context_recovery_system import (
    ContextHealth,
    ContextRecoverySystem,
    process_context_loss_query,
)
from integration.holographic_synchronization import (
    ComponentState,
    ComponentType,
    ContextAwareHolographicSync,
    HolographicMessage,
)


class TestContextRecoverySystem:
    """Test suite for the context recovery system"""

    def setup_method(self):
        """Setup test environment"""
        self.temp_workspace = Path("test_workspace")
        self.temp_workspace.mkdir(exist_ok=True)
        self.recovery_system = ContextRecoverySystem(str(self.temp_workspace))

    def teardown_method(self):
        """Clean up test environment"""
        import shutil

        if self.temp_workspace.exists():
            shutil.rmtree(self.temp_workspace)

    def test_context_health_calculation_healthy(self):
        """Test context health calculation for healthy state"""
        health = self.recovery_system.calculate_context_health(
            "Everything is working fine"
        )

        assert health.is_healthy()
        assert health.score >= 0.7
        assert not health.needs_immediate_recovery()

    def test_context_health_calculation_context_loss(self):
        """Test context health calculation when context loss is detected"""
        health = self.recovery_system.calculate_context_health(
            "I think we're losing context"
        )

        assert not health.is_healthy()
        assert health.needs_immediate_recovery()
        assert health.score < 0.4
        assert any("losing context" in indicator for indicator in health.indicators)

    def test_context_health_calculation_build_failure(self):
        """Test context health calculation for build failures"""
        health = self.recovery_system.calculate_context_health("The build failed")

        assert not health.is_healthy()
        assert health.score < 0.7
        assert any("build" in indicator.lower() for indicator in health.indicators)

    def test_context_health_calculation_file_not_found(self):
        """Test context health calculation for file system issues"""
        health = self.recovery_system.calculate_context_health("File not found error")

        assert not health.is_healthy()
        assert health.needs_immediate_recovery()
        assert health.score < 0.4

    def test_context_health_calculation_time_based(self):
        """Test context health calculation based on time since last recovery"""
        # Set last recovery to 50 hours ago
        self.recovery_system.last_recovery = datetime.now() - timedelta(hours=50)

        health = self.recovery_system.calculate_context_health("")

        assert not health.is_healthy()
        assert any("hours" in indicator for indicator in health.indicators)

    def test_should_trigger_recovery_immediate(self):
        """Test immediate recovery trigger"""
        should_trigger = self.recovery_system.should_trigger_recovery(
            "We're losing context"
        )
        assert should_trigger

    def test_should_trigger_recovery_iteration_based(self):
        """Test iteration-based recovery trigger"""
        self.recovery_system.iteration_count = 10  # Above threshold
        should_trigger = self.recovery_system.should_trigger_recovery("")
        assert should_trigger

    def test_should_trigger_recovery_health_based(self):
        """Test health-based recovery trigger"""
        should_trigger = self.recovery_system.should_trigger_recovery(
            "Build is failing"
        )
        assert should_trigger

    def test_should_not_trigger_recovery_healthy(self):
        """Test that recovery is not triggered when healthy"""
        self.recovery_system.iteration_count = 3  # Below threshold
        should_trigger = self.recovery_system.should_trigger_recovery(
            "Everything is good"
        )
        assert not should_trigger

    def test_execute_context_recovery(self):
        """Test context recovery execution"""
        # Create some test documentation files
        docs_dir = self.temp_workspace / "docs"
        docs_dir.mkdir(exist_ok=True)

        (docs_dir / "ARCHITECTURE.md").write_text("# Architecture")
        (docs_dir / "DEVELOPMENT.md").write_text("# Development")

        recovery_log = self.recovery_system.execute_context_recovery()

        assert "timestamp" in recovery_log
        assert "steps_executed" in recovery_log
        assert "Full codebase reconnaissance" in recovery_log["steps_executed"]
        assert "System health validation" in recovery_log["steps_executed"]
        assert "Context tracking update" in recovery_log["steps_executed"]

        # Check that iteration count was reset
        assert self.recovery_system.iteration_count == 0

    def test_recovery_actions_for_critical_health(self):
        """Test recovery actions for critical health states"""
        health = ContextHealth(
            score=0.2,
            indicators=["Critical issues"],
            last_check=datetime.now(),
            recovery_actions=[],
        )

        actions = self.recovery_system.get_recovery_actions(health)

        assert "Execute immediate context recovery" in actions
        assert "Read all mandatory documentation files" in actions
        assert "Verify system health and build state" in actions

    def test_process_context_loss_query_with_recovery(self):
        """Test context loss query processing with recovery"""
        result = process_context_loss_query(
            "I'm losing context", str(self.temp_workspace)
        )

        assert result["context_loss_detected"]
        assert result["recovery_executed"]
        assert "recovery_log" in result
        assert "Context recovery completed" in result["message"]

    def test_process_context_loss_query_no_recovery(self):
        """Test context loss query processing without recovery"""
        result = process_context_loss_query("Status update", str(self.temp_workspace))

        assert not result["context_loss_detected"]
        assert not result["recovery_executed"]
        assert "context_health" in result
        assert "System operational" in result["message"]


class TestHolographicSynchronization:
    """Test suite for holographic synchronization"""

    def setup_method(self):
        """Setup test environment"""
        self.temp_workspace = Path("test_workspace")
        self.temp_workspace.mkdir(exist_ok=True)
        self.sync_system = ContextAwareHolographicSync(str(self.temp_workspace))

    def teardown_method(self):
        """Clean up test environment"""
        import shutil

        if self.temp_workspace.exists():
            shutil.rmtree(self.temp_workspace)

    def test_sync_with_healthy_context(self):
        """Test synchronization with healthy context"""
        components = [ComponentType.CPP_CORE, ComponentType.PYTHON_AI]

        sync_result = self.sync_system.sync_with_context_preservation(
            components, "Normal operation"
        )

        assert "timestamp" in sync_result
        assert "components_synced" in sync_result
        assert "holographic_coherence" in sync_result
        assert len(sync_result["components_synced"]) == 2

    def test_sync_with_context_recovery_trigger(self):
        """Test synchronization when context recovery is triggered"""
        # Mock the context recovery system
        mock_recovery = Mock()
        mock_recovery.calculate_context_health.return_value = ContextHealth(
            score=0.3,
            indicators=["Context loss detected"],
            last_check=datetime.now(),
            recovery_actions=["Execute recovery"],
        )
        mock_recovery.should_trigger_recovery.return_value = True
        mock_recovery.execute_context_recovery.return_value = {
            "timestamp": datetime.now().isoformat()
        }

        self.sync_system.context_recovery = mock_recovery

        components = [ComponentType.CPP_CORE]
        sync_result = self.sync_system.sync_with_context_preservation(
            components, "We're losing context"
        )

        assert sync_result["status"] == "context_recovery_triggered"
        assert "Context recovery executed" in sync_result["message"]

    def test_component_sync_cpp_core(self):
        """Test individual component synchronization - C++ Core"""
        result = self.sync_system._sync_cpp_core("Test context")

        assert "fractal_memory_coherence" in result
        assert "holographic_state_sync" in result
        assert result["holographic_state_sync"] is True

    def test_component_sync_python_ai(self):
        """Test individual component synchronization - Python AI"""
        result = self.sync_system._sync_python_ai("Test context")

        assert "neural_network_coherence" in result
        assert "fractal_learning_active" in result
        assert result["fractal_learning_active"] is True

    def test_component_sync_csharp_ui(self):
        """Test individual component synchronization - C# UI"""
        result = self.sync_system._sync_csharp_ui("Test context")

        assert "fractal_context_manager" in result
        assert "vscode_bridge_status" in result
        assert result["vscode_bridge_status"] == "connected"

    def test_system_context_status_without_recovery(self):
        """Test system context status when recovery system is unavailable"""
        status = self.sync_system.get_system_context_status()

        assert status["status"] == "context_recovery_unavailable"

    def test_system_context_status_with_recovery(self):
        """Test system context status with recovery system"""
        # Mock the context recovery system
        mock_recovery = Mock()
        mock_recovery.calculate_context_health.return_value = ContextHealth(
            score=0.8,
            indicators=[],
            last_check=datetime.now(),
            recovery_actions=["Continue normal operation"],
        )
        mock_recovery.get_recovery_actions.return_value = ["Continue normal operation"]

        self.sync_system.context_recovery = mock_recovery

        status = self.sync_system.get_system_context_status()

        assert "context_health_score" in status
        assert "context_status" in status
        assert status["context_status"] == "healthy"
        assert not status["recovery_needed"]


class TestFractalHolographicIntegration:
    """Integration tests for the complete fractal holographic system"""

    def setup_method(self):
        """Setup integration test environment"""
        self.temp_workspace = Path("test_workspace")
        self.temp_workspace.mkdir(exist_ok=True)

        # Create test configuration
        config_dir = self.temp_workspace / "config"
        config_dir.mkdir(exist_ok=True)

        system_config = {
            "name": "AIOS",
            "version": "0.4",
            "fractal_enabled": True,
            "holographic_sync": True,
        }

        with open(config_dir / "system.json", "w") as f:
            json.dump(system_config, f)

    def teardown_method(self):
        """Clean up integration test environment"""
        import shutil

        if self.temp_workspace.exists():
            shutil.rmtree(self.temp_workspace)

    def test_end_to_end_context_recovery_flow(self):
        """Test complete end-to-end context recovery flow"""
        # Initialize systems
        recovery_system = ContextRecoverySystem(str(self.temp_workspace))
        sync_system = ContextAwareHolographicSync(str(self.temp_workspace))

        # Simulate context loss scenario
        user_input = "I'm losing context and the build is failing"

        # Process context loss query
        result = process_context_loss_query(user_input, str(self.temp_workspace))

        assert result["context_loss_detected"]
        assert result["recovery_executed"]

        # Verify sync system can handle the recovered context
        components = [ComponentType.CPP_CORE, ComponentType.PYTHON_AI]
        sync_result = sync_system.sync_with_context_preservation(components, user_input)

        # Should trigger recovery again due to user input
        assert sync_result["status"] == "context_recovery_triggered"

    def test_fractal_coherence_maintenance(self):
        """Test that fractal coherence is maintained across operations"""
        sync_system = ContextAwareHolographicSync(str(self.temp_workspace))

        # Multiple synchronization operations
        components = [
            ComponentType.CPP_CORE,
            ComponentType.PYTHON_AI,
            ComponentType.CSHARP_UI,
        ]

        for i in range(5):
            sync_result = sync_system.sync_with_context_preservation(
                components, f"Operation {i}"
            )

            assert "holographic_coherence" in sync_result
            assert isinstance(sync_result["holographic_coherence"], float)
            assert 0.0 <= sync_result["holographic_coherence"] <= 1.0

    def test_multi_component_synchronization(self):
        """Test synchronization across all major components"""
        sync_system = ContextAwareHolographicSync(str(self.temp_workspace))

        all_components = [
            ComponentType.CPP_CORE,
            ComponentType.PYTHON_AI,
            ComponentType.CSHARP_UI,
            ComponentType.VSCODE_EXTENSION,
            ComponentType.AINLP_COMPILER,
        ]

        sync_result = sync_system.sync_with_context_preservation(
            all_components, "Full system sync"
        )

        assert len(sync_result["components_synced"]) == 5
        assert "holographic_coherence" in sync_result

        # Verify each component was synchronized
        component_names = [
            comp["component"] for comp in sync_result["components_synced"]
        ]
        expected_names = [comp.value for comp in all_components]

        for expected_name in expected_names:
            assert expected_name in component_names


@pytest.mark.asyncio
async def test_async_holographic_operations():
    """Test asynchronous holographic operations"""
    # This test would validate async operations in the holographic system
    await asyncio.sleep(0.1)  # Simulate async operation

    # Test async context recovery
    assert True  # Placeholder for async testing

    # Test async component synchronization
    assert True  # Placeholder for async testing


def test_performance_benchmarks():
    """Test performance benchmarks for the fractal holographic system"""
    workspace = Path("test_workspace")
    workspace.mkdir(exist_ok=True)

    try:
        # Benchmark context recovery
        recovery_system = ContextRecoverySystem(str(workspace))

        start_time = time.time()
        for i in range(10):
            health = recovery_system.calculate_context_health(f"Test input {i}")
            assert health.score >= 0.0
        end_time = time.time()

        assert (end_time - start_time) < 1.0  # Should complete within 1 second

        # Benchmark synchronization
        sync_system = ContextAwareHolographicSync(str(workspace))

        start_time = time.time()
        for i in range(5):
            sync_result = sync_system.sync_with_context_preservation(
                [ComponentType.CPP_CORE], f"Benchmark test {i}"
            )
            assert "holographic_coherence" in sync_result
        end_time = time.time()

        assert (end_time - start_time) < 2.0  # Should complete within 2 seconds

    finally:
        import shutil

        if workspace.exists():
            shutil.rmtree(workspace)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
