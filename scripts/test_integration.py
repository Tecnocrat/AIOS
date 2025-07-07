#!/usr/bin/env python3
"""
AIOS Integration Test

Test the integration between C++ core and Python AI modules.
"""

import sys
import os
import subprocess
import asyncio
from pathlib import Path

def supports_unicode():
    """Check if the current environment supports Unicode emojis"""
    try:
        # Try to encode a simple emoji
        '\u2705'.encode(sys.stdout.encoding or 'utf-8')
        return True
    except (UnicodeEncodeError, AttributeError):
        return False

# Set display characters based on environment capability
UNICODE_SUPPORT = supports_unicode()
CHECK_MARK = '\u2705' if UNICODE_SUPPORT else '[PASS]'
CROSS_MARK = '\u274c' if UNICODE_SUPPORT else '[FAIL]'
CELEBRATION = '\U0001F389' if UNICODE_SUPPORT else '[SUCCESS]'
WARNING = '\u26A0\uFE0F' if UNICODE_SUPPORT else '[WARNING]'

# Add AI module path
sys.path.append(str(Path(__file__).parent.parent / "ai" / "src"))

from core.nlp import NLPManager
from core.prediction import PredictionManager
from core.automation import AutomationManager
from core.learning import LearningManager
from core.integration import IntegrationBridge


async def test_ai_modules():
    """Test AI modules functionality"""
    print("Testing AI modules...")
    
    # Test NLP Manager
    nlp_config = {
        "primary": {"model": "test", "enabled": True},
        "fallback": {"model": "simple", "enabled": True}
    }
    nlp = NLPManager(nlp_config)
    await nlp.initialize()
    await nlp.start()
    
    # Test text processing
    result = await nlp.process("Hello, how are you?")
    print(f"NLP processing result: {result}")
    
    # Test Prediction Manager
    prediction_config = {
        "model": "test",
        "horizon": 24,
        "confidence_threshold": 0.7
    }
    prediction = PredictionManager(prediction_config)
    await prediction.initialize()
    await prediction.start()
    
    # Test prediction
    pred_result = await prediction.predict({"user_input": "predict weather"})
    print(f"Prediction result: {pred_result}")
    
    # Test Automation Manager
    automation_config = {
        "max_concurrent_tasks": 5,
        "task_timeout": 30
    }
    automation = AutomationManager(automation_config)
    await automation.initialize()
    await automation.start()
    
    # Test task execution
    task_result = await automation.execute_task({"task_name": "test_task", "message": "Hello"})
    print(f"Automation task result: {task_result}")
    
    # Test Learning Manager
    learning_config = {
        "model": "simple",
        "learning_rate": 0.001
    }
    learning = LearningManager(learning_config)
    await learning.initialize()
    await learning.start()
    
    # Test learning
    learning_result = await learning.update({"input": "test data", "output": "test result"})
    print(f"Learning result: {learning_result}")
    
    # Test Integration Bridge
    integration_config = {
        "cpp_core_path": str(Path(__file__).parent.parent / "core" / "build" / "bin" / "Debug" / "aios_main.exe"),
        "python_ai_path": str(Path(__file__).parent.parent / "ai" / "src")
    }
    integration = IntegrationBridge(integration_config)
    await integration.initialize()
    await integration.start()
    
    # Test integration
    integration_result = await integration.send_message("test_target", {"command": "test_command", "data": "test"})
    print(f"Integration result: {integration_result}")
    
    await nlp.stop()
    await prediction.stop()
    await automation.stop()
    await learning.stop()
    await integration.stop()
    
    print("All AI modules tested successfully!")


def test_cpp_core():
    """Test C++ core functionality"""
    print("Testing C++ core...")
    
    cpp_exe = Path(__file__).parent.parent / "core" / "build" / "bin" / "Debug" / "aios_main.exe"
    
    if not cpp_exe.exists():
        print(f"C++ executable not found: {cpp_exe}")
        return False
    
    # Test C++ core with basic commands
    try:
        # Create a simple test script for the C++ core
        test_commands = "help\nstatus\nhealth\nexit\n"
        
        result = subprocess.run(
            [str(cpp_exe)],
            input=test_commands,
            text=True,
            capture_output=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("C++ core executed successfully!")
            print("Output preview:")
            print(result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
            return True
        else:
            print(f"C++ core failed with return code: {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("C++ core test timed out")
        return False
    except Exception as e:
        print(f"Error testing C++ core: {e}")
        return False


async def main():
    """Main test function"""
    print("=" * 50)
    print("AIOS Integration Test")
    print("=" * 50)
    
    # Test C++ core
    cpp_success = test_cpp_core()
    
    print("\n" + "=" * 50)
    
    # Test Python AI modules
    try:
        await test_ai_modules()
        ai_success = True
    except Exception as e:
        print(f"AI modules test failed: {e}")
        ai_success = False
    
    print("\n" + "=" * 50)
    print("INTEGRATION TEST RESULTS")
    print("=" * 50)
    print(f"C++ Core: {CHECK_MARK if cpp_success else CROSS_MARK}")
    print(f"Python AI: {CHECK_MARK if ai_success else CROSS_MARK}")
    
    if cpp_success and ai_success:
        print(f"\n{CELEBRATION} ALL TESTS PASSED! AIOS system is ready!")
        return 0
    else:
        print(f"\n{WARNING} Some tests failed. Check the logs above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
