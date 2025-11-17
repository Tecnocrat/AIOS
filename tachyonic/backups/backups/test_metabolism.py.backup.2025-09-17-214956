"""
Simple test of documentation metabolism system
"""

import sys
from pathlib import Path

# Add the tachyonic directory to path
sys.path.append(str(Path(__file__).parent))

from supercell_knowledge_injector import SupercellKnowledgeInjector

def test_documentation_metabolism():
    """Test the documentation metabolism system"""
    print("Testing AIOS Documentation Metabolism System")
    print("=" * 45)
    
    # Initialize the knowledge injector
    injector = SupercellKnowledgeInjector()
    print(" Tachyonic Archive initialized")
    
    # Test the documentation ingestion (will scan /docs directory)
    try:
        results = injector.ingest_documentation_files()
        print(f" Documentation metabolism completed")
        print(f"   Files processed: {len(results.get('processed_files', []))}")
        print(f"   Crystals created: {len(results.get('knowledge_crystals_created', []))}")
        print(f"   Patterns extracted: {len(results.get('patterns_extracted', []))}")
        
        return True
        
    except Exception as e:
        print(f" Metabolism failed: {e}")
        return False

if __name__ == "__main__":
    success = test_documentation_metabolism()
    if success:
        print("\n Documentation metabolism system operational!")
        print("The biological metaphor is working:")
        print("• /docs = Digestive system for AI documentation")  
        print("• Tachyonic Archive = Brain/DNA knowledge center")
        print("• AIOS prevents documentation chaos through metabolism")
    else:
        print("\n Test failed")