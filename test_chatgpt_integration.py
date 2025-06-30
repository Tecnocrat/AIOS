#!/usr/bin/env python3
"""
Test script to verify the chatgpt_integration path works correctly
"""
import os
import sys

def test_chatgpt_integration_path():
    """Test that the chatgpt_integration directory exists and is accessible"""
    chatgpt_integration_path = r"C:\dev\AIOS\chatgpt_integration"
    
    print("=== Testing ChatGPT Integration Path ===")
    print(f"Testing path: {chatgpt_integration_path}")
    
    if os.path.exists(chatgpt_integration_path):
        print("✅ Directory exists")
        
        # Test key subdirectories
        key_dirs = ["ingestion", "md"]
        for dir_name in key_dirs:
            dir_path = os.path.join(chatgpt_integration_path, dir_name)
            if os.path.exists(dir_path):
                print(f"✅ {dir_name}/ directory exists")
            else:
                print(f"❌ {dir_name}/ directory missing")
        
        # Test key files
        key_files = ["chatgpt.py"]
        for file_name in key_files:
            file_path = os.path.join(chatgpt_integration_path, file_name)
            if os.path.exists(file_path):
                print(f"✅ {file_name} exists")
            else:
                print(f"❌ {file_name} missing")
        
        # Count total files
        total_files = 0
        for root, dirs, files in os.walk(chatgpt_integration_path):
            total_files += len(files)
        print(f"📊 Total files in chatgpt_integration: {total_files}")
        
    else:
        print("❌ Directory does not exist")
        return False
    
    # Test old path doesn't exist (or is marked for deletion)
    old_chatgpt_path = r"C:\dev\chatgpt"
    if os.path.exists(old_chatgpt_path):
        print(f"⚠️  Old chatgpt directory still exists at: {old_chatgpt_path}")
        print("    This should be removed once no processes are accessing it.")
    else:
        print("✅ Old chatgpt directory has been removed")
    
    print("\n=== Test Complete ===")
    return True

if __name__ == "__main__":
    success = test_chatgpt_integration_path()
    sys.exit(0 if success else 1)
