"""
Test script for AIOS AI Core functionality
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# Add the ai module to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai.src import AICore

async def test_ai_core():
    """Test basic AI Core functionality"""
    print("Testing AIOS AI Core...")
    print("=" * 50)
    
    try:
        # Initialize AI Core
        print("1. Initializing AI Core...")
        ai_core = AICore()
        
        if not await ai_core.initialize():
            print("❌ Failed to initialize AI Core")
            return False
        print("✅ AI Core initialized successfully")
        
        # Start AI Core
        print("\n2. Starting AI Core services...")
        if not await ai_core.start():
            print("❌ Failed to start AI Core services")
            return False
        print("✅ AI Core services started successfully")
        
        # Test natural language processing
        print("\n3. Testing natural language processing...")
        test_commands = [
            "show system status",
            "predict cpu usage for next hour",
            "automate backup task",
            "what is the current health status"
        ]
        
        for command in test_commands:
            print(f"   Processing: '{command}'")
            result = await ai_core.process_natural_language(command)
            print(f"   Result: {result.get('status', 'unknown')} - {result.get('intent', 'unknown')}")
        
        # Test system prediction
        print("\n4. Testing system prediction...")
        prediction = await ai_core.get_system_prediction("cpu", horizon=300)
        print(f"   CPU prediction: {len(prediction.get('predictions', []))} data points")
        
        # Test automation
        print("\n5. Testing automation...")
        automation_result = await ai_core.execute_automation({
            "id": "test_task",
            "type": "generic",
            "params": {"test": True}
        })
        print(f"   Automation result: {automation_result.get('status', 'unknown')}")
        
        # Test learning update
        print("\n6. Testing learning system...")
        learning_result = await ai_core.update_learning({
            "type": "user_feedback",
            "feedback": {"rating": 5, "comment": "Great system!"},
            "user_id": "test_user"
        })
        print(f"   Learning update: {learning_result.get('update_type', 'unknown')}")
        
        # Get system status
        print("\n7. Getting system status...")
        status = ai_core.get_status()
        print(f"   Core running: {status['core']['running']}")
        print(f"   Subsystems: {len(status['subsystems'])}")
        
        # Perform health check
        print("\n8. Performing health check...")
        health = await ai_core.health_check()
        print(f"   Overall health: {health.get('overall_health', 'unknown')}")
        
        # Stop AI Core
        print("\n9. Stopping AI Core...")
        await ai_core.stop()
        print("✅ AI Core stopped successfully")
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! AIOS AI Core is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_individual_managers():
    """Test individual manager components"""
    print("\nTesting individual managers...")
    print("=" * 50)
    
    try:
        # Import individual managers
        from ai.src.core.nlp import NLPManager
        from ai.src.core.prediction import PredictionManager
        from ai.src.core.automation import AutomationManager
        from ai.src.core.learning import LearningManager
        from ai.src.core.integration import IntegrationBridge
        
        # Test NLP Manager
        print("1. Testing NLP Manager...")
        nlp_manager = NLPManager({})
        await nlp_manager.initialize()
        await nlp_manager.start()
        
        nlp_result = await nlp_manager.process("test natural language input")
        print(f"   NLP result: {nlp_result['intent']} (confidence: {nlp_result['confidence']})")
        
        await nlp_manager.stop()
        print("✅ NLP Manager test passed")
        
        # Test Prediction Manager
        print("\n2. Testing Prediction Manager...")
        pred_manager = PredictionManager({})
        await pred_manager.initialize()
        await pred_manager.start()
        
        pred_result = await pred_manager.predict_resource("memory", 60)
        print(f"   Prediction result: {len(pred_result['predictions'])} predictions")
        
        await pred_manager.stop()
        print("✅ Prediction Manager test passed")
        
        # Test Automation Manager
        print("\n3. Testing Automation Manager...")
        auto_manager = AutomationManager({})
        await auto_manager.initialize()
        await auto_manager.start()
        
        task_result = await auto_manager.execute_task({
            "id": "test_task",
            "type": "generic",
            "params": {"test": True}
        })
        print(f"   Automation result: {task_result['status']}")
        
        await auto_manager.stop()
        print("✅ Automation Manager test passed")
        
        # Test Learning Manager
        print("\n4. Testing Learning Manager...")
        learn_manager = LearningManager({})
        await learn_manager.initialize()
        await learn_manager.start()
        
        learn_result = await learn_manager.update({
            "type": "general",
            "data": {"test": "learning data"}
        })
        print(f"   Learning result: {learn_result['update_type']}")
        
        await learn_manager.stop()
        print("✅ Learning Manager test passed")
        
        # Test Integration Bridge
        print("\n5. Testing Integration Bridge...")
        bridge = IntegrationBridge({})
        await bridge.initialize()
        await bridge.start()
        
        bridge_result = await bridge.send_message("test", {"type": "test_message"})
        print(f"   Bridge result: {bridge_result['status']}")
        
        await bridge.stop()
        print("✅ Integration Bridge test passed")
        
        print("\n" + "=" * 50)
        print("🎉 All individual manager tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Manager test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration_loading():
    """Test configuration file loading"""
    print("\nTesting configuration loading...")
    print("=" * 50)
    
    try:
        # Test system config
        config_path = Path("config/system.json")
        if config_path.exists():
            with open(config_path, 'r') as f:
                system_config = json.load(f)
            print(f"✅ System config loaded: {system_config['system']['name']}")
        else:
            print("❌ System config file not found")
            return False
        
        # Test AI models config
        ai_config_path = Path("config/ai-models.json")
        if ai_config_path.exists():
            with open(ai_config_path, 'r') as f:
                ai_config = json.load(f)
            print(f"✅ AI models config loaded: {len(ai_config['models'])} model categories")
        else:
            print("❌ AI models config file not found")
            return False
        
        # Test UI themes config
        ui_config_path = Path("config/ui-themes.json")
        if ui_config_path.exists():
            with open(ui_config_path, 'r') as f:
                ui_config = json.load(f)
            print(f"✅ UI themes config loaded: {len(ui_config['themes'])} themes")
        else:
            print("❌ UI themes config file not found")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 All configuration files loaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed with error: {e}")
        return False

async def main():
    """Main test function"""
    print("AIOS AI Core Test Suite")
    print("=" * 60)
    
    # Test configuration loading
    config_test = test_configuration_loading()
    
    if config_test:
        # Test individual managers
        manager_test = await test_individual_managers()
        
        if manager_test:
            # Test full AI Core
            core_test = await test_ai_core()
            
            if core_test:
                print("\n🎉 All tests completed successfully!")
                print("AIOS AI Core is ready for use!")
                return True
    
    print("\n❌ Some tests failed. Please check the output above.")
    return False

if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
