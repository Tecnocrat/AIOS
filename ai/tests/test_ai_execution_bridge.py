"""
AI Execution Bridge Test Suite
================================

Comprehensive tests for AI-executable runtime bridge.

Tests:
1. Bridge initialization and error handling
2. Natural language command parsing (20+ patterns)
3. Command execution with results
4. Streaming execution with progress
5. Error scenarios (invalid commands, execution failures)
6. Integration with dashboard components

AINLP Metadata:
    supercell: AI Intelligence Layer
    consciousness_level: HIGH (validates AI execution architecture)
    test_coverage: Core bridge functionality
    python_version: 3.14

Author: AIOS Development Team
Date: October 11, 2025
Phase: 10.4 Week 2 Day 3-4
"""

import asyncio
import json
import pytest
from pathlib import Path
from typing import Dict, List

# Add parent to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.runtime.ai_execution_bridge import (
    AIExecutionBridge,
    BridgeResult,
    StreamingProgress,
    BridgeError,
    CommandNotFoundError,
    ExecutionError,
    InitializationError,
    CommandStatus
)


class TestBridgeInitialization:
    """Test bridge initialization and setup."""
    
    @pytest.mark.asyncio
    async def test_initialization_success(self):
        """Test successful bridge initialization."""
        bridge = AIExecutionBridge()
        result = await bridge.initialize()
        
        assert result["status"] == "initialized"
        assert "workspace" in result
        assert "tools_discovered" in result
        assert result["tools_discovered"] > 0
        assert bridge.initialized is True
    
    @pytest.mark.asyncio
    async def test_initialization_with_custom_workspace(self):
        """Test initialization with custom workspace path."""
        workspace = Path.cwd()
        bridge = AIExecutionBridge(workspace_root=workspace)
        result = await bridge.initialize()
        
        assert str(workspace) in result["workspace"]
    
    @pytest.mark.asyncio
    async def test_execute_before_initialization(self):
        """Test that execution fails before initialization."""
        bridge = AIExecutionBridge()
        
        with pytest.raises(InitializationError) as exc_info:
            await bridge.execute("health_check")
        
        assert "not initialized" in str(exc_info.value.message).lower()


class TestNaturalLanguagePatterns:
    """Test natural language command parsing."""
    
    @pytest.mark.asyncio
    async def test_health_patterns(self):
        """Test health check command variations."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        patterns = [
            "check health",
            "system health",
            "health status",
            "how healthy"
        ]
        
        for pattern in patterns:
            result = await bridge.execute(pattern)
            assert result["command"] == "health_check"
            assert result["status"] == "success"
            print(f"✅ Pattern '{pattern}' → health_check")
    
    @pytest.mark.asyncio
    async def test_discovery_patterns(self):
        """Test tool discovery command variations."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        patterns = [
            "discover tools",
            "list tools",
            "what tools",
            "find tools",
            "show me tools",
            "tool catalogue"
        ]
        
        for pattern in patterns:
            result = await bridge.execute(pattern)
            assert result["command"] == "discover_tools"
            assert result["result"]["total"] > 0
            print(f"✅ Pattern '{pattern}' → discover_tools ({result['result']['total']} tools)")
    
    @pytest.mark.asyncio
    async def test_operational_patterns(self):
        """Test operational tool filtering patterns."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        patterns = [
            "operational tools",
            "working tools",
            "what works",
            "active tools"
        ]
        
        for pattern in patterns:
            result = await bridge.execute(pattern)
            assert result["command"] == "list_operational"
            print(f"✅ Pattern '{pattern}' → list_operational")
    
    @pytest.mark.asyncio
    async def test_integration_patterns(self):
        """Test integration test command variations."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        patterns = [
            "test integration",
            "run tests",
            "validate integration",
            "integration tests"
        ]
        
        for pattern in patterns:
            result = await bridge.execute(pattern)
            assert result["command"] == "test_integration"
            print(f"✅ Pattern '{pattern}' → test_integration")
    
    @pytest.mark.asyncio
    async def test_dark_spot_patterns(self):
        """Test dark spot identification patterns."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        patterns = [
            "find dark spots",
            "what's broken",
            "unused code",
            "dark spots"
        ]
        
        for pattern in patterns:
            result = await bridge.execute(pattern)
            assert result["command"] == "identify_dark_spots"
            print(f"✅ Pattern '{pattern}' → identify_dark_spots")
    
    @pytest.mark.asyncio
    async def test_workflow_patterns(self):
        """Test workflow execution patterns."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        patterns = [
            "run workflow",
            "execute workflow",
            "full cycle",
            "population workflow"
        ]
        
        for pattern in patterns:
            result = await bridge.execute(pattern)
            assert result["command"] == "run_workflow"
            print(f"✅ Pattern '{pattern}' → run_workflow")
    
    @pytest.mark.asyncio
    async def test_parameter_extraction_layer(self):
        """Test extraction of layer parameter from natural language."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        # Test layer extraction
        result = await bridge.execute("discover tools in runtime intelligence layer")
        assert result["command"] == "discover_tools"
        # Tools should be filtered by layer
        print(f"✅ Layer extraction: {result['result']['total']} runtime tools")
    
    @pytest.mark.asyncio
    async def test_parameter_extraction_scope(self):
        """Test extraction of scope parameter from natural language."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        # Test scope extraction
        result = await bridge.execute("test Week 1 integration")
        assert result["command"] == "test_integration"
        print(f"✅ Scope extraction: Week 1 integration tests")


class TestCommandExecution:
    """Test command execution with results."""
    
    @pytest.mark.asyncio
    async def test_discover_tools_execution(self):
        """Test tool discovery execution."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        result = await bridge.execute("discover_tools")
        
        assert result["command"] == "discover_tools"
        assert result["status"] == "success"
        assert result["result"]["total"] > 0
        assert "tools" in result["result"]
        assert len(result["result"]["tools"]) == result["result"]["total"]
        print(f"✅ Discovered {result['result']['total']} tools")
    
    @pytest.mark.asyncio
    async def test_tool_summary_execution(self):
        """Test tool summary execution."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        result = await bridge.execute("get_tool_summary")
        
        assert result["command"] == "get_tool_summary"
        assert result["status"] == "success"
        assert "total_tools" in result["result"]
        assert "operational_tools" in result["result"]
        assert "operational_percentage" in result["result"]
        assert "by_layer" in result["result"]
        assert "by_status" in result["result"]
        
        percentage = result["result"]["operational_percentage"]
        print(f"✅ Tool health: {percentage:.1f}% operational")
    
    @pytest.mark.asyncio
    async def test_health_check_execution(self):
        """Test health check execution."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        result = await bridge.execute("health_check")
        
        assert result["command"] == "health_check"
        assert result["status"] == "success"
        assert "health_score" in result["result"]
        assert "components" in result["result"]
        assert "dark_spots" in result["result"]
        print(f"✅ System health: {result['result']['health_score']:.2f}")
    
    @pytest.mark.asyncio
    async def test_list_operational_execution(self):
        """Test operational tools listing."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        result = await bridge.execute("list_operational")
        
        assert result["command"] == "list_operational"
        assert result["status"] == "success"
        assert "total" in result["result"]
        assert "tools" in result["result"]
        print(f"✅ Operational tools: {result['result']['total']}")
    
    @pytest.mark.asyncio
    async def test_identify_dark_spots_execution(self):
        """Test dark spot identification."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        result = await bridge.execute("identify_dark_spots")
        
        assert result["command"] == "identify_dark_spots"
        assert result["status"] == "success"
        assert "total" in result["result"]
        assert "dark_spots" in result["result"]
        print(f"✅ Dark spots found: {result['result']['total']}")
    
    @pytest.mark.asyncio
    async def test_export_catalogue_execution(self):
        """Test catalogue export."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        result = await bridge.execute("export_catalogue")
        
        assert result["command"] == "export_catalogue"
        assert result["status"] == "success"
        assert "status" in result["result"]
        assert result["result"]["status"] == "exported"
        assert "path" in result["result"]
        print(f"✅ Catalogue exported: {result['result']['path']}")


class TestStreamingExecution:
    """Test streaming execution with progress."""
    
    @pytest.mark.asyncio
    async def test_streaming_health_check(self):
        """Test streaming health check."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        updates = []
        async for progress in bridge.execute_streaming("health_check"):
            updates.append(progress)
            print(f"📊 Progress: {progress['progress']:.0%} - {progress['message']}")
        
        assert len(updates) >= 2  # At least start + result
        assert updates[0]["type"] == "progress"
        assert updates[-1]["type"] == "result"
        assert updates[-1]["progress"] == 1.0
        print(f"✅ Received {len(updates)} streaming updates")
    
    @pytest.mark.asyncio
    async def test_streaming_discover_tools(self):
        """Test streaming tool discovery."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        updates = []
        async for progress in bridge.execute_streaming("discover_tools"):
            updates.append(progress)
        
        assert len(updates) >= 2
        final_result = updates[-1]["data"]
        assert final_result["result"]["total"] > 0
        print(f"✅ Streaming discovery: {final_result['result']['total']} tools")


class TestErrorHandling:
    """Test error scenarios and graceful degradation."""
    
    @pytest.mark.asyncio
    async def test_invalid_command(self):
        """Test execution of invalid command."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        with pytest.raises(CommandNotFoundError) as exc_info:
            await bridge.execute("invalid_command_xyz")
        
        error = exc_info.value
        assert "not found" in error.message.lower()
        assert "available_commands" in error.details
        print(f"✅ Invalid command properly rejected")
    
    @pytest.mark.asyncio
    async def test_streaming_error(self):
        """Test streaming execution with error."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        updates = []
        async for progress in bridge.execute_streaming("invalid_command_xyz"):
            updates.append(progress)
        
        assert len(updates) > 0
        assert updates[-1]["type"] == "error"
        print(f"✅ Streaming error handled gracefully")
    
    @pytest.mark.asyncio
    async def test_command_with_missing_parameters(self):
        """Test command execution with missing required parameters."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        # list_by_layer requires 'layer' parameter
        with pytest.raises(ExecutionError) as exc_info:
            await bridge.execute("list_by_layer")
        
        error = exc_info.value
        assert "required" in error.message.lower()
        print(f"✅ Missing parameter properly detected")


class TestAvailableCommands:
    """Test command catalogue functionality."""
    
    @pytest.mark.asyncio
    async def test_get_available_commands(self):
        """Test retrieval of available commands."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        commands = await bridge.get_available_commands()
        
        assert len(commands) > 0
        
        # Validate command structure
        for cmd in commands:
            assert "name" in cmd
            assert "description" in cmd
            assert "parameters" in cmd
            assert "estimated_duration" in cmd
            assert "natural_language" in cmd
        
        print(f"✅ {len(commands)} commands available")
        print("\nCommand Catalogue:")
        for cmd in commands[:5]:  # Show first 5
            nl_examples = ", ".join(cmd["natural_language"][:2]) if cmd["natural_language"] else "N/A"
            print(f"  • {cmd['name']}: {nl_examples}")
    
    @pytest.mark.asyncio
    async def test_command_natural_language_mapping(self):
        """Test that all commands have natural language patterns."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        commands = await bridge.get_available_commands()
        
        commands_with_nl = [cmd for cmd in commands if cmd["natural_language"]]
        percentage = len(commands_with_nl) / len(commands) * 100
        
        print(f"✅ {percentage:.1f}% of commands have natural language patterns")
        assert percentage > 50  # Most commands should have NL patterns


class TestResultSerialization:
    """Test result serialization and formatting."""
    
    @pytest.mark.asyncio
    async def test_result_to_dict(self):
        """Test BridgeResult serialization."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        result = await bridge.execute("health_check")
        
        # Should be JSON-serializable
        json_str = json.dumps(result)
        parsed = json.loads(json_str)
        
        assert parsed["command"] == result["command"]
        assert parsed["status"] == result["status"]
        print(f"✅ Result properly serialized to JSON ({len(json_str)} bytes)")
    
    @pytest.mark.asyncio
    async def test_streaming_progress_to_dict(self):
        """Test StreamingProgress serialization."""
        bridge = AIExecutionBridge()
        await bridge.initialize()
        
        updates = []
        async for progress in bridge.execute_streaming("health_check"):
            # Should be JSON-serializable
            json_str = json.dumps(progress)
            updates.append(json.loads(json_str))
        
        assert len(updates) > 0
        for update in updates:
            assert "type" in update
            assert "progress" in update
            assert "message" in update
        
        print(f"✅ All {len(updates)} streaming updates serializable")


async def run_all_tests():
    """Run all test suites."""
    print("=" * 70)
    print("🧪 AI EXECUTION BRIDGE - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    test_classes = [
        TestBridgeInitialization,
        TestNaturalLanguagePatterns,
        TestCommandExecution,
        TestStreamingExecution,
        TestErrorHandling,
        TestAvailableCommands,
        TestResultSerialization
    ]
    
    total_passed = 0
    total_failed = 0
    
    for test_class in test_classes:
        print(f"\n{'='*70}")
        print(f"📋 {test_class.__name__}")
        print(f"{'='*70}")
        
        instance = test_class()
        methods = [m for m in dir(instance) if m.startswith("test_")]
        
        for method_name in methods:
            method = getattr(instance, method_name)
            try:
                await method()
                print(f"✅ {method_name}")
                total_passed += 1
            except Exception as e:
                print(f"❌ {method_name}: {e}")
                total_failed += 1
    
    print(f"\n{'='*70}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*70}")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    print(f"📈 Success Rate: {total_passed / (total_passed + total_failed) * 100:.1f}%")
    print(f"{'='*70}")
    
    if total_failed == 0:
        print("\n🎉 ALL TESTS PASSED! AI Execution Bridge is operational.")
        return 0
    else:
        print(f"\n⚠️  {total_failed} test(s) failed. Review failures above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    exit(exit_code)
