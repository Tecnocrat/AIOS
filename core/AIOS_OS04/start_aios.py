#!/usr/bin/env python3
"""
AIOS OS0.4 Startup Script
========================

Main entry point for AIOS OS0.4 system startup and management.
"""

import asyncio
import sys
from pathlib import Path

# Add core modules to path
sys.path.insert(0, str(Path(__file__).parent / "core"))

from aios_consciousness_engine import AIOSConsciousnessEngine
from aios_evolution_lab import EvolutionLabManager
from aios_knowledge_distillation import UnifiedKnowledgeDistillationEngine
from aios_admin_orchestrator import UnifiedAdminOrchestrationEngine
from aios_visual_interface import AIOSVisualInterfaceManager, VisualizationConfig
from aios_system_intelligence import SystemIntelligenceManager, SystemIntelligenceConfig

class AIOSSystem:
    """Main AIOS OS0.4 system orchestrator"""
    
    def __init__(self):
        self.modules = {}
        self.running = False
        
    async def initialize(self):
        """Initialize all AIOS modules"""
        print("🧠 Initializing AIOS OS0.4 System...")
        
        # Initialize core modules
        self.modules['consciousness'] = AIOSConsciousnessEngine()
        self.modules['evolution'] = EvolutionLabManager()
        self.modules['knowledge'] = UnifiedKnowledgeDistillationEngine()
        self.modules['admin'] = UnifiedAdminOrchestrationEngine()
        
        # Initialize interface modules
        viz_config = VisualizationConfig()
        self.modules['visual'] = AIOSVisualInterfaceManager(viz_config)
        
        intel_config = SystemIntelligenceConfig()
        self.modules['intelligence'] = SystemIntelligenceManager(intel_config)
        
        # Setup integrations
        visual = self.modules['visual']
        intelligence = self.modules['intelligence']
        
        visual.integrate_consciousness_module(self.modules['consciousness'])
        visual.integrate_evolution_module(self.modules['evolution'])
        visual.integrate_knowledge_module(self.modules['knowledge'])
        visual.integrate_admin_module(self.modules['admin'])
        
        intelligence.integrate_consciousness_module(self.modules['consciousness'])
        intelligence.integrate_evolution_module(self.modules['evolution'])
        intelligence.integrate_visual_interface(visual)
        
        print("✅ AIOS OS0.4 initialized successfully!")
        
    async def start(self):
        """Start the AIOS system"""
        await self.initialize()
        
        print("🚀 Starting AIOS OS0.4...")
        
        # Start system intelligence monitoring
        await self.modules['intelligence'].initialize()
        await self.modules['intelligence'].start()
        
        # Start visual interface
        await self.modules['visual'].initialize()
        await self.modules['visual'].start()
        
        self.running = True
        print("✅ AIOS OS0.4 started successfully!")
        print("🌐 Web dashboard available at: http://localhost:8080")
        print("🔍 System monitoring active")
        print("Press Ctrl+C to stop AIOS")
        
        # Keep running
        try:
            while self.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await self.stop()
            
    async def stop(self):
        """Stop the AIOS system"""
        print("🛑 Stopping AIOS OS0.4...")
        self.running = False
        
        if 'intelligence' in self.modules:
            await self.modules['intelligence'].stop()
            
        if 'visual' in self.modules:
            await self.modules['visual'].stop()
            
        print("✅ AIOS OS0.4 stopped successfully")

async def main():
    """Main entry point"""
    aios = AIOSSystem()
    await aios.start()

if __name__ == "__main__":
    asyncio.run(main())
