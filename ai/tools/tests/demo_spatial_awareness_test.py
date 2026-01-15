#!/usr/bin/env python3
"""
AIOS Spatial Awareness Demo
Demonstrates the complete holographic metadata + GitHook intelligence workflow
"""

import os
import json
import subprocess
from pathlib import Path

def test_spatial_awareness():
    """Test the holographic metadata system for spatial awareness"""
    print("🧠 AIOS Spatial Awareness Demo")
    print("=" * 50)
    
    # 1. Check spatial metadata for AI folder
    ai_folder = Path("ai")
    metadata_file = ai_folder / ".aios_spatial_metadata.json"
    
    if metadata_file.exists():
        print(f"✅ Found spatial metadata: {metadata_file}")
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        print(f"📊 Folder: {metadata['folder_info']['name']}")
        print(f"🏗️ Classification: {metadata['architectural_classification']['primary_area']}")
        print(f"🧠 Consciousness Level: {metadata['architectural_classification']['consciousness_level']}")
        
        if 'ai_guidance' in metadata:
            print(f"🤖 AI Guidance: {metadata['ai_guidance']}")
        
        if 'content_analysis' in metadata:
            print(f"📁 File count: {metadata['content_analysis']['files_by_type']}")
    else:
        print("❌ No spatial metadata found - this would be flagged!")
    
    # 2. Test GitHook intelligence integration
    print("\n🔗 GitHook Intelligence Integration:")
    intelligence_file = Path(".githooks/modules/information_storage/ai_intelligence_extrusion.jsonl")
    
    if intelligence_file.exists():
        print(f"✅ GitHook intelligence active: {intelligence_file}")
        # Get latest intelligence
        try:
            result = subprocess.run([
                "python", "ai/membrane/aios_cross_dialogue_intelligence.py"
            ], capture_output=True, text=True)
            
            if "Fresh intelligence retrieved" in result.stdout:
                print("✅ Real-time intelligence bridge operational")
            else:
                print("⚠️ Intelligence bridge may need refresh")
                
        except Exception as e:
            print(f"❌ Intelligence bridge error: {e}")
    else:
        print("❌ GitHook intelligence not configured")
    
    # 3. Test holographic system stats
    print("\n📊 Holographic System Statistics:")
    index_file = Path("aios_holographic_index.json")
    
    if index_file.exists():
        with open(index_file, 'r') as f:
            index_data = json.load(f)
        
        print(f"📁 Metadata files created: {len(index_data['metadata_files']['created'])}")
        print(f"🔄 Last updated: {index_data['creation_timestamp']}")
        print(f"📈 System version: {index_data['holographic_system_version']}")
    else:
        print("❌ Holographic index not found")

if __name__ == "__main__":
    test_spatial_awareness()