"""
Biological Architecture Status Tool
==================================

Provides comprehensive status monitoring of the complete AIOS biological architecture:
Interface Supercell → Runtime Intelligence → AI Intelligence → Core Engine

This tool monitors all supercell components and their dendritic connections.
"""

import asyncio
import logging
import sys
import os
from typing import Dict, List, Any
from datetime import datetime
import json

# Add paths for integration
current_dir = os.path.dirname(__file__)
ai_path = os.path.join(current_dir, '..', '..', 'ai')
sys.path.append(ai_path)

try:
    from runtime_intelligence_dendritic_integration import get_runtime_intelligence_dendritic_integration
    from enhanced_visual_intelligence_bridge import get_enhanced_visual_intelligence_bridge
except ImportError as e:
    logging.warning(f"Some integrations not available: {e}")


class BiologicalArchitectureMonitor:
    """
    Comprehensive monitor for the complete biological architecture.
    
    Monitors:
    - Interface Supercell (C# WPF components)
    - Runtime Intelligence (Python orchestration)
    - AI Intelligence Supercell (organs: cytoplasm, nucleus, membrane, etc.)
    - Core Engine Supercell (analysis tools, engines, assemblers)
    - Dendritic Connections (supervisor bridges)
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
        self.dendritic_integration = None
        self.visual_bridge = None
        
        # Component status tracking
        self.component_statuses = {
            'interface_supercell': 'unknown',
            'runtime_intelligence': 'unknown',
            'ai_intelligence_supercell': 'unknown',
            'core_engine_supercell': 'unknown',
            'dendritic_supervisor': 'unknown'
        }
    
    def setup_logging(self):
        """Setup logging for the monitor."""
        log_dir = os.path.join(current_dir, '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'biological_architecture_monitor.log')
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)
    
    async def initialize(self) -> bool:
        """Initialize the biological architecture monitor."""
        try:
            self.logger.info(" Initializing Biological Architecture Monitor...")
            
            # Initialize dendritic integration
            try:
                self.dendritic_integration = await get_runtime_intelligence_dendritic_integration()
                self.component_statuses['dendritic_supervisor'] = 'active'
                self.logger.info(" Dendritic supervisor integration active")
            except Exception as e:
                self.logger.warning(f" Dendritic supervisor unavailable: {e}")
                self.component_statuses['dendritic_supervisor'] = 'unavailable'
            
            # Initialize visual bridge
            try:
                self.visual_bridge = await get_enhanced_visual_intelligence_bridge()
                self.component_statuses['runtime_intelligence'] = 'active'
                self.logger.info(" Enhanced visual intelligence bridge active")
            except Exception as e:
                self.logger.warning(f" Visual bridge unavailable: {e}")
                self.component_statuses['runtime_intelligence'] = 'limited'
            
            return True
            
        except Exception as e:
            self.logger.error(f" Failed to initialize monitor: {e}")
            return False
    
    async def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the biological architecture."""
        try:
            self.logger.info(" Generating comprehensive biological architecture status...")
            
            status = {
                'timestamp': datetime.now().isoformat(),
                'biological_architecture': {
                    'status': 'analyzing',
                    'compliance': 'checking'
                },
                'supercells': {},
                'dendritic_connections': {},
                'overall_health': 'analyzing'
            }
            
            # Check Interface Supercell
            status['supercells']['interface_supercell'] = await self._check_interface_supercell()
            
            # Check Runtime Intelligence
            status['supercells']['runtime_intelligence'] = await self._check_runtime_intelligence()
            
            # Check AI Intelligence Supercell
            status['supercells']['ai_intelligence_supercell'] = await self._check_ai_intelligence_supercell()
            
            # Check Core Engine Supercell
            status['supercells']['core_engine_supercell'] = await self._check_core_engine_supercell()
            
            # Check Dendritic Connections
            status['dendritic_connections'] = await self._check_dendritic_connections()
            
            # Calculate overall health
            status['overall_health'] = self._calculate_overall_health(status)
            
            # Update biological architecture status
            status['biological_architecture'] = self._assess_biological_compliance(status)
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error generating comprehensive status: {e}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'status': 'error'
            }
    
    async def _check_interface_supercell(self) -> Dict[str, Any]:
        """Check Interface Supercell (C# WPF) status."""
        try:
            # Check for C# project files
            interface_path = os.path.join(current_dir, '..', '..', 'interface')
            
            components = {
                'aios_ui': os.path.exists(os.path.join(interface_path, 'AIOS.UI')),
                'aios_services': os.path.exists(os.path.join(interface_path, 'AIOS.Services')),
                'aios_models': os.path.exists(os.path.join(interface_path, 'AIOS.Models')),
                'runtime_intelligence_service': os.path.exists(
                    os.path.join(interface_path, 'AIOS.Services', 'RuntimeIntelligenceService.cs')
                )
            }
            
            active_components = sum(1 for active in components.values() if active)
            total_components = len(components)
            
            return {
                'status': 'active' if active_components >= 3 else 'partial',
                'components': components,
                'health_score': active_components / total_components,
                'description': 'Interface Supercell - C# WPF components',
                'primary_function': 'User interface and system orchestration',
                'biological_type': 'Independent Supercell'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'health_score': 0.0
            }
    
    async def _check_runtime_intelligence(self) -> Dict[str, Any]:
        """Check Runtime Intelligence status."""
        try:
            status = {
                'status': 'active',
                'components': {
                    'dendritic_integration': self.dendritic_integration is not None,
                    'visual_bridge': self.visual_bridge is not None,
                    'enhanced_mode': False
                },
                'health_score': 0.0,
                'description': 'Runtime Intelligence - Python orchestration layer',
                'primary_function': 'Bridge between Interface and AI Intelligence supercells',
                'biological_type': 'Communication Layer'
            }
            
            # Check enhanced mode
            if self.visual_bridge:
                bridge_status = await self.visual_bridge.get_bridge_status()
                status['components']['enhanced_mode'] = bridge_status.get('enhanced_mode', False)
            
            # Calculate health score
            active_components = sum(1 for active in status['components'].values() if active)
            total_components = len(status['components'])
            status['health_score'] = active_components / total_components
            
            if status['health_score'] < 0.5:
                status['status'] = 'limited'
            
            return status
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'health_score': 0.0
            }
    
    async def _check_ai_intelligence_supercell(self) -> Dict[str, Any]:
        """Check AI Intelligence Supercell status."""
        try:
            ai_path = os.path.join(current_dir, '..', '..', 'ai')
            
            # Check for AI Intelligence organs
            organs = {
                'cytoplasm': os.path.exists(os.path.join(ai_path, 'cytoplasm')),
                'nucleus': os.path.exists(os.path.join(ai_path, 'nucleus')),
                'membrane': os.path.exists(os.path.join(ai_path, 'membrane')),
                'laboratory': os.path.exists(os.path.join(ai_path, 'laboratory')),
                'information_storage': os.path.exists(os.path.join(ai_path, 'information_storage')),
                'transport': os.path.exists(os.path.join(ai_path, 'transport'))
            }
            
            # Check for dendritic supervision
            dendritic_supervision = False
            if self.dendritic_integration:
                try:
                    integration_status = await self.dendritic_integration.get_integration_status()
                    dendritic_supervision = integration_status.get('active', False)
                except:
                    pass
            
            active_organs = sum(1 for active in organs.values() if active)
            total_organs = len(organs)
            
            return {
                'status': 'active' if active_organs >= 4 else 'developing',
                'organs': organs,
                'dendritic_supervision': dendritic_supervision,
                'health_score': active_organs / total_organs,
                'description': 'AI Intelligence Supercell - Biological AI processing',
                'primary_function': 'Advanced AI processing and consciousness simulation',
                'biological_type': 'AI Processing Supercell'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'health_score': 0.0
            }
    
    async def _check_core_engine_supercell(self) -> Dict[str, Any]:
        """Check Core Engine Supercell status."""
        try:
            core_path = os.path.join(current_dir, '..', '..', 'core')
            
            # Check for Core Engine tools
            tools = {
                'analysis_tools': os.path.exists(os.path.join(core_path, 'src', 'analysis_tools')),
                'assemblers': os.path.exists(os.path.join(core_path, 'src', 'assemblers')),
                'bridges': os.path.exists(os.path.join(core_path, 'bridges')),
                'engines': os.path.exists(os.path.join(core_path, 'src', 'engines')),
                'cmake_build': os.path.exists(os.path.join(core_path, 'CMakeLists.txt'))
            }
            
            # Check for dendritic connections
            dendritic_connections = False
            if self.dendritic_integration:
                try:
                    supervisor_status = await self.dendritic_integration.cytoplasm_bridge.dendritic_supervisor.get_supervisor_status()
                    dendritic_connections = supervisor_status.get('core_engine_connected', False)
                except:
                    pass
            
            active_tools = sum(1 for active in tools.values() if active)
            total_tools = len(tools)
            
            return {
                'status': 'active' if active_tools >= 3 else 'developing',
                'tools': tools,
                'dendritic_connections': dendritic_connections,
                'health_score': active_tools / total_tools,
                'description': 'Core Engine Supercell - Low-level processing and optimization',
                'primary_function': 'High-performance computing and system optimization',
                'biological_type': 'Processing Engine Supercell'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'health_score': 0.0
            }
    
    async def _check_dendritic_connections(self) -> Dict[str, Any]:
        """Check dendritic connection status."""
        try:
            connections = {
                'cytoplasm_dendritic_bridge': False,
                'dendritic_supervisor': False,
                'core_engine_integration': False,
                'organ_monitoring': False
            }
            
            connection_health = 0.0
            
            if self.dendritic_integration:
                try:
                    # Check cytoplasm bridge
                    bridge_status = await self.dendritic_integration.cytoplasm_bridge.get_bridge_status()
                    connections['cytoplasm_dendritic_bridge'] = bridge_status.get('active', False)
                    
                    # Check supervisor
                    supervisor_status = await self.dendritic_integration.cytoplasm_bridge.dendritic_supervisor.get_supervisor_status()
                    connections['dendritic_supervisor'] = supervisor_status.get('active', False)
                    connections['core_engine_integration'] = supervisor_status.get('core_engine_connected', False)
                    connections['organ_monitoring'] = supervisor_status.get('organ_monitoring_active', False)
                    
                except Exception as e:
                    self.logger.warning(f"Error checking dendritic connections: {e}")
            
            active_connections = sum(1 for active in connections.values() if active)
            total_connections = len(connections)
            connection_health = active_connections / total_connections
            
            return {
                'status': 'active' if connection_health >= 0.75 else 'developing',
                'connections': connections,
                'health_score': connection_health,
                'description': 'Dendritic connections between supercells',
                'primary_function': 'Inter-supercell communication and supervision'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'health_score': 0.0
            }
    
    def _calculate_overall_health(self, status: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall biological architecture health."""
        try:
            supercell_scores = []
            dendritic_score = 0.0
            
            # Collect supercell health scores
            for supercell_name, supercell_data in status['supercells'].items():
                if isinstance(supercell_data, dict) and 'health_score' in supercell_data:
                    supercell_scores.append(supercell_data['health_score'])
            
            # Get dendritic connection score
            if 'dendritic_connections' in status and isinstance(status['dendritic_connections'], dict):
                dendritic_score = status['dendritic_connections'].get('health_score', 0.0)
            
            # Calculate weighted health score
            if supercell_scores:
                avg_supercell_health = sum(supercell_scores) / len(supercell_scores)
                # Weight: 70% supercells, 30% dendritic connections
                overall_score = (avg_supercell_health * 0.7) + (dendritic_score * 0.3)
            else:
                overall_score = 0.0
            
            # Determine health status
            if overall_score >= 0.8:
                health_status = 'excellent'
            elif overall_score >= 0.6:
                health_status = 'good'
            elif overall_score >= 0.4:
                health_status = 'fair'
            else:
                health_status = 'poor'
            
            return {
                'score': overall_score,
                'status': health_status,
                'supercell_count': len(supercell_scores),
                'dendritic_integration': dendritic_score > 0.5
            }
            
        except Exception as e:
            return {
                'score': 0.0,
                'status': 'error',
                'error': str(e)
            }
    
    def _assess_biological_compliance(self, status: Dict[str, Any]) -> Dict[str, Any]:
        """Assess biological architecture compliance."""
        try:
            compliance_checks = {
                'supercell_independence': True,
                'dendritic_supervision': False,
                'proper_communication_flow': False,
                'organ_monitoring': False
            }
            
            # Check supercell independence
            supercells = status.get('supercells', {})
            interface_active = supercells.get('interface_supercell', {}).get('status') == 'active'
            ai_intelligence_active = supercells.get('ai_intelligence_supercell', {}).get('status') == 'active'
            core_engine_active = supercells.get('core_engine_supercell', {}).get('status') == 'active'
            
            compliance_checks['supercell_independence'] = interface_active and ai_intelligence_active and core_engine_active
            
            # Check dendritic supervision
            dendritic_data = status.get('dendritic_connections', {})
            compliance_checks['dendritic_supervision'] = dendritic_data.get('connections', {}).get('dendritic_supervisor', False)
            
            # Check communication flow
            compliance_checks['proper_communication_flow'] = (
                dendritic_data.get('connections', {}).get('cytoplasm_dendritic_bridge', False) and
                dendritic_data.get('connections', {}).get('core_engine_integration', False)
            )
            
            # Check organ monitoring
            compliance_checks['organ_monitoring'] = dendritic_data.get('connections', {}).get('organ_monitoring', False)
            
            # Calculate compliance score
            compliance_score = sum(1 for check in compliance_checks.values() if check) / len(compliance_checks)
            
            if compliance_score >= 0.75:
                compliance_status = 'fully_compliant'
            elif compliance_score >= 0.5:
                compliance_status = 'partially_compliant'
            else:
                compliance_status = 'non_compliant'
            
            return {
                'status': compliance_status,
                'score': compliance_score,
                'checks': compliance_checks,
                'description': 'Biological architecture compliance assessment'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'score': 0.0
            }
    
    async def get_supercell_details(self, supercell_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific supercell."""
        try:
            if supercell_name == 'interface_supercell':
                return await self._check_interface_supercell()
            elif supercell_name == 'runtime_intelligence':
                return await self._check_runtime_intelligence()
            elif supercell_name == 'ai_intelligence_supercell':
                return await self._check_ai_intelligence_supercell()
            elif supercell_name == 'core_engine_supercell':
                return await self._check_core_engine_supercell()
            else:
                return {
                    'error': f'Unknown supercell: {supercell_name}',
                    'available_supercells': [
                        'interface_supercell',
                        'runtime_intelligence',
                        'ai_intelligence_supercell',
                        'core_engine_supercell'
                    ]
                }
                
        except Exception as e:
            return {
                'error': str(e),
                'supercell': supercell_name
            }
    
    async def generate_status_report(self) -> str:
        """Generate a comprehensive status report."""
        try:
            status = await self.get_comprehensive_status()
            
            report = f"""
AIOS Biological Architecture Status Report
==========================================
Generated: {status['timestamp']}

 BIOLOGICAL ARCHITECTURE OVERVIEW
Status: {status['biological_architecture']['status'].upper()}
Compliance: {status['biological_architecture']['score']:.2f} ({status['biological_architecture']['status']})
Overall Health: {status['overall_health']['score']:.2f} ({status['overall_health']['status'].upper()})

 SUPERCELL STATUS
"""
            
            # Add supercell details
            for supercell_name, supercell_data in status['supercells'].items():
                if isinstance(supercell_data, dict):
                    report += f"""
{supercell_name.replace('_', ' ').title()}:
  Status: {supercell_data.get('status', 'unknown').upper()}
  Health: {supercell_data.get('health_score', 0.0):.2f}
  Type: {supercell_data.get('biological_type', 'Unknown')}
  Function: {supercell_data.get('primary_function', 'Unknown')}
"""
            
            # Add dendritic connections
            dendritic_data = status.get('dendritic_connections', {})
            report += f"""
 DENDRITIC CONNECTIONS
Status: {dendritic_data.get('status', 'unknown').upper()}
Health: {dendritic_data.get('health_score', 0.0):.2f}

Connection Details:
"""
            
            connections = dendritic_data.get('connections', {})
            for conn_name, conn_status in connections.items():
                status_icon = "" if conn_status else ""
                report += f"  {status_icon} {conn_name.replace('_', ' ').title()}\n"
            
            report += f"""
 ARCHITECTURE SUMMARY
Supercells Active: {status['overall_health'].get('supercell_count', 0)}
Dendritic Integration: {'' if status['overall_health'].get('dendritic_integration', False) else ''}
Biological Compliance: {status['biological_architecture']['score']:.2f}

 RECOMMENDATIONS
"""
            
            # Add recommendations based on status
            if status['overall_health']['score'] < 0.6:
                report += "- Critical: Improve supercell health scores\n"
            if not status['overall_health'].get('dendritic_integration', False):
                report += "- Important: Establish dendritic supervision\n"
            if status['biological_architecture']['score'] < 0.75:
                report += "- Recommended: Enhance biological architecture compliance\n"
            
            if status['overall_health']['score'] >= 0.8:
                report += "- Excellent: Architecture is operating optimally\n"
            
            return report
            
        except Exception as e:
            return f"Error generating status report: {str(e)}"


# Global instance
_biological_architecture_monitor = None

async def get_biological_architecture_monitor() -> BiologicalArchitectureMonitor:
    """Get the singleton biological architecture monitor."""
    global _biological_architecture_monitor
    
    if _biological_architecture_monitor is None:
        _biological_architecture_monitor = BiologicalArchitectureMonitor()
        await _biological_architecture_monitor.initialize()
    
    return _biological_architecture_monitor


async def main():
    """Test the biological architecture monitor."""
    print(" AIOS Biological Architecture Monitor")
    print("=" * 50)
    
    # Initialize monitor
    monitor = await get_biological_architecture_monitor()
    
    # Generate status report
    print(" Generating comprehensive status report...\n")
    report = await monitor.generate_status_report()
    print(report)


if __name__ == "__main__":
    asyncio.run(main())