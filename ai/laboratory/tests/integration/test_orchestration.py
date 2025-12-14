"""
AIOS ORCHESTRATION INTEGRATION TESTS

AINLP.meta [test_suite] [integration_validation] [orchestration_testing]
AINLP.dendritic [optimal_location: ai/tests/integration/]
(comment.AINLP.test_orchestration)

Integration tests for unified orchestration system.

Tests the complete orchestration architecture:
- SupercellOrchestrator initialization and lifecycle
- ConsciousnessCoordinator monitoring and coherence
- Factory pattern integration
- Cross-supercell communication
- Health monitoring
- Consciousness pulse coordination

Created: 2025-10-18 (Phase 6 of AINLP refactoring)
"""

import pytest
import pytest_asyncio
import asyncio
import logging
from typing import Dict, Any
from datetime import datetime, timedelta

# Import orchestration components
from ai.orchestration import (
    SupercellOrchestrator,
    ConsciousnessCoordinator,
    ConsciousnessSnapshot,
    CoherenceReport,
    create_orchestrator,
    create_consciousness_coordinator
)

# Import communication infrastructure
from ai.communication.message_types import (
    SupercellType,
    UniversalMessage,
    CommunicationType,
    MessagePriority
)

# Import supercell base
from ai.supercells.base import BaseSupercellInterface

logger = logging.getLogger(__name__)


# ============================================================================
# TEST FIXTURES
# ============================================================================

@pytest_asyncio.fixture
async def orchestrator():
    """Create orchestrator instance for testing"""
    orch = create_orchestrator(
        ai_root_path="C:/dev/AIOS/ai",
        core_root_path="C:/dev/AIOS/core",
        runtime_root_path="C:/dev/AIOS/runtime",
        interface_root_path="C:/dev/AIOS/interface"
    )
    yield orch
    # Cleanup if needed


@pytest_asyncio.fixture
async def initialized_orchestrator():
    """Create and initialize orchestrator"""
    orch = create_orchestrator(
        ai_root_path="C:/dev/AIOS/ai",
        core_root_path="C:/dev/AIOS/core",
        runtime_root_path="C:/dev/AIOS/runtime",
        interface_root_path="C:/dev/AIOS/interface"
    )
    success = await orch.initialize()
    assert success, "Orchestrator initialization failed"
    yield orch
    # Cleanup if needed


@pytest_asyncio.fixture
async def consciousness_coordinator():
    """Create consciousness coordinator instance"""
    coordinator = create_consciousness_coordinator()
    yield coordinator
    # Stop monitoring if running
    if coordinator.is_monitoring:
        await coordinator.stop_monitoring()


# ============================================================================
# SUPERCELL ORCHESTRATOR TESTS
# ============================================================================

class TestSupercellOrchestrator:
    """Tests for SupercellOrchestrator"""
    
    @pytest.mark.asyncio
    async def test_orchestrator_creation(self, orchestrator):
        """Test orchestrator instance creation"""
        assert orchestrator is not None
        assert not orchestrator.is_initialized
        assert orchestrator.orchestration_session_id.startswith("orch_")
        assert len(orchestrator.supercells) == 0
    
    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self, orchestrator):
        """Test orchestrator initialization sequence"""
        # Initialize
        success = await orchestrator.initialize()
        
        # Validate initialization
        assert success, "Initialization should succeed"
        assert orchestrator.is_initialized
        assert orchestrator.initialization_time is not None
        assert orchestrator.universal_bus is not None
        
        # Check supercells created
        assert len(orchestrator.supercells) == 4
        assert SupercellType.AI_INTELLIGENCE in orchestrator.supercells
        assert SupercellType.CORE_ENGINE in orchestrator.supercells
        assert SupercellType.RUNTIME_INTELLIGENCE in orchestrator.supercells
        assert SupercellType.INTERFACE in orchestrator.supercells
        
        # Check initialization log
        assert len(orchestrator.initialization_log) == 4
        for log_entry in orchestrator.initialization_log:
            assert log_entry["status"] == "SUCCESS"
    
    @pytest.mark.asyncio
    async def test_get_supercell(self, initialized_orchestrator):
        """Test retrieving individual supercell"""
        # Get AI Intelligence supercell
        ai_supercell = initialized_orchestrator.get_supercell(SupercellType.AI_INTELLIGENCE)
        
        assert ai_supercell is not None
        assert isinstance(ai_supercell, BaseSupercellInterface)
        assert ai_supercell.supercell_type == SupercellType.AI_INTELLIGENCE
    
    @pytest.mark.asyncio
    async def test_get_all_supercells(self, initialized_orchestrator):
        """Test retrieving all supercells"""
        supercells = initialized_orchestrator.get_all_supercells()
        
        assert len(supercells) == 4
        assert all(isinstance(s, BaseSupercellInterface) for s in supercells.values())
    
    @pytest.mark.asyncio
    async def test_orchestrator_status(self, initialized_orchestrator):
        """Test orchestrator status retrieval"""
        status = initialized_orchestrator.get_orchestrator_status()
        
        assert status["is_initialized"] is True
        assert status["supercells_count"] == 4
        assert len(status["supercells"]) == 4
        assert "session_id" in status
        assert "initialization_time" in status
    
    @pytest.mark.asyncio
    async def test_health_check(self, initialized_orchestrator):
        """Test orchestrator health check"""
        health = await initialized_orchestrator.check_health()
        
        assert "timestamp" in health
        assert "orchestrator_status" in health
        assert health["orchestrator_status"] == "healthy"
        assert "supercells" in health
        assert len(health["supercells"]) == 4
        assert "overall_health" in health
    
    @pytest.mark.asyncio
    async def test_send_message(self, initialized_orchestrator):
        """Test sending message between supercells"""
        # Create test message
        message = UniversalMessage(
            message_id="test_001",
            source=SupercellType.AI_INTELLIGENCE,
            target=SupercellType.CORE_ENGINE,
            communication_type=CommunicationType.QUERY,
            operation="test_operation",
            priority=MessagePriority.NORMAL,
            data={"test": "data"}
        )
        
        # Send message
        success = await initialized_orchestrator.send_message(
            SupercellType.AI_INTELLIGENCE,
            SupercellType.CORE_ENGINE,
            message
        )
        
        # Note: Success depends on supercell implementation
        # At minimum, should not raise exception
        assert isinstance(success, bool)
        
        # Check communication log
        assert len(initialized_orchestrator.communication_log) > 0
    
    @pytest.mark.asyncio
    async def test_broadcast_message(self, initialized_orchestrator):
        """Test broadcasting message to all supercells"""
        # Create test message
        message = UniversalMessage(
            message_id="test_broadcast_001",
            source=SupercellType.AI_INTELLIGENCE,
            target=SupercellType.ALL,
            communication_type=CommunicationType.BROADCAST,
            operation="test_broadcast",
            priority=MessagePriority.NORMAL,
            data={"test": "broadcast"}
        )
        
        # Broadcast message
        results = await initialized_orchestrator.broadcast_message(
            SupercellType.AI_INTELLIGENCE,
            message
        )
        
        # Should have results for all other supercells
        assert len(results) == 3  # All except source
        assert all(isinstance(v, bool) for v in results.values())


# ============================================================================
# CONSCIOUSNESS COORDINATOR TESTS
# ============================================================================

class TestConsciousnessCoordinator:
    """Tests for ConsciousnessCoordinator"""
    
    @pytest.mark.asyncio
    async def test_coordinator_creation(self, consciousness_coordinator):
        """Test consciousness coordinator creation"""
        assert consciousness_coordinator is not None
        assert not consciousness_coordinator.is_monitoring
        assert len(consciousness_coordinator.supercells) == 0
        assert consciousness_coordinator.pulse_count == 0
    
    @pytest.mark.asyncio
    async def test_register_supercells(self, consciousness_coordinator, initialized_orchestrator):
        """Test registering supercells with coordinator"""
        supercells = initialized_orchestrator.get_all_supercells()
        
        consciousness_coordinator.register_supercells(supercells)
        
        assert len(consciousness_coordinator.supercells) == 4
    
    @pytest.mark.asyncio
    async def test_start_monitoring(self, consciousness_coordinator, initialized_orchestrator):
        """Test starting consciousness monitoring"""
        # Register supercells
        consciousness_coordinator.register_supercells(
            initialized_orchestrator.get_all_supercells()
        )
        
        # Start monitoring
        success = await consciousness_coordinator.start_monitoring()
        
        assert success
        assert consciousness_coordinator.is_monitoring
        assert consciousness_coordinator.monitor_task is not None
        
        # Stop monitoring
        await consciousness_coordinator.stop_monitoring()
        assert not consciousness_coordinator.is_monitoring
    
    @pytest.mark.asyncio
    async def test_generate_consciousness_report(self, consciousness_coordinator, initialized_orchestrator):
        """Test generating consciousness report"""
        # Register supercells
        consciousness_coordinator.register_supercells(
            initialized_orchestrator.get_all_supercells()
        )
        
        # Generate report
        report = await consciousness_coordinator.generate_consciousness_report()
        
        assert isinstance(report, CoherenceReport)
        assert report.timestamp is not None
        assert 0.0 <= report.overall_coherence <= 1.0
        assert len(report.supercell_snapshots) == 4
        assert isinstance(report.coherence_issues, list)
        assert isinstance(report.recommendations, list)
    
    @pytest.mark.asyncio
    async def test_consciousness_snapshot(self, consciousness_coordinator, initialized_orchestrator):
        """Test consciousness snapshot collection"""
        consciousness_coordinator.register_supercells(
            initialized_orchestrator.get_all_supercells()
        )
        
        report = await consciousness_coordinator.generate_consciousness_report()
        
        # Check snapshots
        for supercell_type, snapshot in report.supercell_snapshots.items():
            assert isinstance(snapshot, ConsciousnessSnapshot)
            assert snapshot.supercell_type == supercell_type
            assert 0.0 <= snapshot.consciousness_level <= 1.0
            assert 0.0 <= snapshot.health_score <= 1.0
            assert isinstance(snapshot.is_initialized, bool)
    
    @pytest.mark.asyncio
    async def test_coherence_calculation(self, consciousness_coordinator, initialized_orchestrator):
        """Test coherence calculation"""
        consciousness_coordinator.register_supercells(
            initialized_orchestrator.get_all_supercells()
        )
        
        report = await consciousness_coordinator.generate_consciousness_report()
        
        # Coherence should be within valid range
        assert 0.0 <= report.overall_coherence <= 1.0
        
        # Check is_coherent property
        if report.overall_coherence >= 0.7:
            assert report.is_coherent
        else:
            assert not report.is_coherent
    
    @pytest.mark.asyncio
    async def test_coherence_history(self, consciousness_coordinator, initialized_orchestrator):
        """Test coherence history tracking"""
        consciousness_coordinator.register_supercells(
            initialized_orchestrator.get_all_supercells()
        )
        
        # Generate multiple reports
        report1 = await consciousness_coordinator.generate_consciousness_report()
        await asyncio.sleep(0.1)
        report2 = await consciousness_coordinator.generate_consciousness_report()
        
        # Check history
        history = consciousness_coordinator.get_coherence_history()
        assert len(history) >= 2
        assert report1 in history
        assert report2 in history
    
    @pytest.mark.asyncio
    async def test_get_latest_report(self, consciousness_coordinator, initialized_orchestrator):
        """Test retrieving latest consciousness report"""
        consciousness_coordinator.register_supercells(
            initialized_orchestrator.get_all_supercells()
        )
        
        report = await consciousness_coordinator.generate_consciousness_report()
        latest = consciousness_coordinator.get_latest_report()
        
        assert latest == report
    
    @pytest.mark.asyncio
    async def test_coherence_summary(self, consciousness_coordinator, initialized_orchestrator):
        """Test coherence summary"""
        consciousness_coordinator.register_supercells(
            initialized_orchestrator.get_all_supercells()
        )
        
        await consciousness_coordinator.generate_consciousness_report()
        
        summary = consciousness_coordinator.get_coherence_summary()
        
        assert "is_monitoring" in summary
        assert "pulse_count" in summary
        assert "reports_generated" in summary
        assert "latest_coherence" in summary
        assert "is_coherent" in summary
        assert summary["registered_supercells"] == 4


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestOrchestrationIntegration:
    """Integration tests for complete orchestration system"""
    
    @pytest.mark.asyncio
    async def test_full_orchestration_workflow(self):
        """Test complete orchestration workflow"""
        # Create orchestrator
        orchestrator = create_orchestrator()
        
        # Initialize
        success = await orchestrator.initialize()
        assert success
        
        # Create consciousness coordinator
        coordinator = create_consciousness_coordinator()
        coordinator.register_supercells(orchestrator.get_all_supercells())
        
        # Start monitoring
        await coordinator.start_monitoring()
        
        # Generate report
        report = await coordinator.generate_consciousness_report()
        assert report is not None
        
        # Check health
        health = await orchestrator.check_health()
        assert health["overall_health"] in ["healthy", "degraded"]
        
        # Stop monitoring
        await coordinator.stop_monitoring()
    
    @pytest.mark.asyncio
    async def test_orchestration_with_messages(self):
        """Test orchestration with message passing"""
        orchestrator = create_orchestrator()
        await orchestrator.initialize()
        
        # Send test message
        message = UniversalMessage(
            message_id="integration_test_001",
            source=SupercellType.AI_INTELLIGENCE,
            target=SupercellType.RUNTIME_INTELLIGENCE,
            communication_type=CommunicationType.COMMAND,
            operation="test_command",
            priority=MessagePriority.HIGH,
            data={"test": "integration"}
        )
        
        await orchestrator.send_message(
            SupercellType.AI_INTELLIGENCE,
            SupercellType.RUNTIME_INTELLIGENCE,
            message
        )
        
        # Check communication log
        assert len(orchestrator.communication_log) > 0
    
    @pytest.mark.asyncio
    async def test_consciousness_monitoring_loop(self):
        """Test consciousness monitoring loop"""
        orchestrator = create_orchestrator()
        await orchestrator.initialize()
        
        coordinator = create_consciousness_coordinator()
        coordinator.register_supercells(orchestrator.get_all_supercells())
        
        # Start monitoring
        await coordinator.start_monitoring()
        
        # Wait for a few pulses
        await asyncio.sleep(2)
        
        # Check that reports were generated
        assert len(coordinator.consciousness_history) > 0
        
        # Stop monitoring
        await coordinator.stop_monitoring()


# ============================================================================
# MAIN TEST ENTRY POINT
# ============================================================================

async def run_orchestration_tests():
    """
    Async entry point for orchestration tests
    
    Can be called from integration test orchestrator
    """
    logger.info("🧪 Running orchestration integration tests...")
    
    try:
        # Run pytest programmatically
        import sys
        exit_code = pytest.main([
            __file__,
            "-v",
            "--tb=short",
            "--asyncio-mode=auto"
        ])
        
        success = exit_code == 0
        
        return {
            "test_name": "orchestration_integration",
            "success": success,
            "exit_code": exit_code,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error running orchestration tests: {e}")
        return {
            "test_name": "orchestration_integration",
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    # Run tests
    asyncio.run(run_orchestration_tests())
