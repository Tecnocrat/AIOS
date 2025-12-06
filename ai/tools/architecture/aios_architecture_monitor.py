"""
AIOS Architecture Status Monitor
===============================

Provides comprehensive status monitoring of the complete AIOS architecture:
AI Intelligence → Core Engine → Interface → Runtime Intelligence

This tool monitors all AIOS components and their integration connections.
Updated from biological naming to standardized AIOS architecture.
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
ai_path = os.path.join(current_dir, "..", "..", "ai")
sys.path.append(ai_path)

try:
    from runtime_dendritic_integration import get_runtime_dendritic_integration
    from enhanced_visual_intelligence_bridge import (
        get_enhanced_visual_intelligence_bridge,
    )
except ImportError as e:
    logging.warning(f"Some integrations not available: {e}")


class AIOSArchitectureMonitor:
    """
    Comprehensive monitor for the complete AIOS architecture.

    Monitors:
    - AI Intelligence (Python AI processing and algorithms)
    - Core Engine (C++ performance components and system foundation)
    - Interface (C# UI and service architecture)
    - Runtime Intelligence (System monitoring and optimization)
    - Integration Connections (communication bridges)
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

        self.integration_bridges = None
        self.visual_bridge = None

        # Component status tracking - Updated to AIOS architecture
        self.component_statuses = {
            "ai_intelligence": "unknown",
            "core_engine": "unknown",
            "interface": "unknown",
            "runtime": "unknown",
            "integration_bridges": "unknown",
        }

    def setup_logging(self):
        """Setup logging for the monitor."""
        log_dir = os.path.join(current_dir, "..", "logs")
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, "aios_architecture_monitor.log")

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)

    async def initialize(self) -> bool:
        """Initialize the AIOS architecture monitor."""
        try:
            self.logger.info(" Initializing AIOS Architecture Monitor...")

            # Initialize integration bridges
            try:
                self.integration_bridges = await get_runtime_dendritic_integration()
                self.component_statuses["integration_bridges"] = "active"
                self.logger.info(" Integration bridges active")
            except Exception as e:
                self.logger.warning(f" Integration bridges unavailable: {e}")
                self.component_statuses["integration_bridges"] = "unavailable"

            # Initialize visual bridge
            try:
                self.visual_bridge = await get_enhanced_visual_intelligence_bridge()
                self.component_statuses["runtime"] = "active"
                self.logger.info(" Enhanced visual intelligence bridge active")
            except Exception as e:
                self.logger.warning(f" Visual bridge unavailable: {e}")
                self.component_statuses["runtime"] = "limited"

            return True

        except Exception as e:
            self.logger.error(f" Failed to initialize monitor: {e}")
            return False

    async def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the AIOS architecture."""
        try:
            self.logger.info(" Generating comprehensive AIOS status...")

            status = {
                "timestamp": datetime.now().isoformat(),
                "aios_architecture": {"status": "analyzing", "compliance": "checking"},
                "components": {},
                "integration_bridges": {},
                "overall_health": "analyzing",
            }

            # Check Interface Components
            status["components"]["interface"] = await self._check_interface_supercell()

            # Check Runtime Intelligence
            status["components"]["runtime"] = await self._check_runtime()

            # Check AI Intelligence Component
            status["components"][
                "ai_intelligence"
            ] = await self._check_ai_intelligence_supercell()

            # Check Core Engine Component
            status["components"][
                "core_engine"
            ] = await self._check_core_engine_supercell()

            # Check Integration Bridges
            status["integration_bridges"] = await self._check_dendritic_connections()

            # Calculate overall health
            status["overall_health"] = self._calculate_overall_health(status)

            # Update AIOS architecture status
            status["aios_architecture"] = self._assess_aios_compliance(status)

            return status

        except Exception as e:
            self.logger.error(f"Error generating comprehensive status: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "error",
            }

    async def _check_interface_supercell(self) -> Dict[str, Any]:
        """Check Interface Supercell (C# WPF) status."""
        try:
            # Check for C# project files
            interface_path = os.path.join(current_dir, "..", "..", "interface")

            components = {
                "aios_ui": os.path.exists(os.path.join(interface_path, "AIOS.UI")),
                "aios_services": os.path.exists(
                    os.path.join(interface_path, "AIOS.Services")
                ),
                "aios_models": os.path.exists(
                    os.path.join(interface_path, "AIOS.Models")
                ),
                "runtime_service": os.path.exists(
                    os.path.join(
                        interface_path, "AIOS.Services", "RuntimeIntelligenceService.cs"
                    )
                ),
            }

            active_components = sum(1 for active in components.values() if active)
            total_components = len(components)

            return {
                "status": "active" if active_components >= 3 else "partial",
                "components": components,
                "health_score": active_components / total_components,
                "description": "Interface Supercell - C# WPF components",
                "primary_function": "User interface and system orchestration",
                "biological_type": "Independent Supercell",
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "health_score": 0.0}

    async def _check_runtime(self) -> Dict[str, Any]:
        """Check Runtime Intelligence status."""
        try:
            status = {
                "status": "active",
                "components": {
                    "integration_bridges": self.integration_bridges is not None,
                    "visual_bridge": self.visual_bridge is not None,
                    "enhanced_mode": False,
                },
                "health_score": 0.0,
                "description": "Runtime Intelligence - Python orchestration layer",
                "primary_function": "Bridge between Interface and AI Intelligence supercells",
                "biological_type": "Communication Layer",
            }

            # Check enhanced mode
            if self.visual_bridge:
                bridge_status = await self.visual_bridge.get_bridge_status()
                status["components"]["enhanced_mode"] = bridge_status.get(
                    "enhanced_mode", False
                )

            # Calculate health score
            active_components = sum(
                1 for active in status["components"].values() if active
            )
            total_components = len(status["components"])
            status["health_score"] = active_components / total_components

            if status["health_score"] < 0.5:
                status["status"] = "limited"

            return status

        except Exception as e:
            return {"status": "error", "error": str(e), "health_score": 0.0}

    async def _check_ai_intelligence_supercell(self) -> Dict[str, Any]:
        """Check AI Intelligence Supercell status."""
        try:
            ai_path = os.path.join(current_dir, "..", "..", "ai")

            # Check for AI Intelligence organs
            organs = {
                "cytoplasm": os.path.exists(os.path.join(ai_path, "cytoplasm")),
                "nucleus": os.path.exists(os.path.join(ai_path, "nucleus")),
                "membrane": os.path.exists(os.path.join(ai_path, "membrane")),
                "laboratory": os.path.exists(os.path.join(ai_path, "laboratory")),
                "information_storage": os.path.exists(
                    os.path.join(ai_path, "information_storage")
                ),
                "transport": os.path.exists(os.path.join(ai_path, "transport")),
            }

            # Check for integration bridges supervision
            integration_supervision = False
            if self.integration_bridges:
                try:
                    integration_status = (
                        await self.integration_bridges.get_integration_status()
                    )
                    integration_supervision = integration_status.get("active", False)
                except:
                    pass

            active_organs = sum(1 for active in organs.values() if active)
            total_organs = len(organs)

            return {
                "status": "active" if active_organs >= 4 else "developing",
                "organs": organs,
                "integration_supervision": integration_supervision,
                "health_score": active_organs / total_organs,
                "description": "AI Intelligence Component - AI processing and algorithms",
                "primary_function": "Advanced AI processing and consciousness simulation",
                "architecture_type": "AI Processing Component",
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "health_score": 0.0}

    async def _check_core_engine_supercell(self) -> Dict[str, Any]:
        """Check Core Engine Supercell status."""
        try:
            core_path = os.path.join(current_dir, "..", "..", "core")

            # Check for Core Engine tools
            tools = {
                "analysis_tools": os.path.exists(
                    os.path.join(core_path, "src", "analysis_tools")
                ),
                "assemblers": os.path.exists(
                    os.path.join(core_path, "src", "assemblers")
                ),
                "bridges": os.path.exists(os.path.join(core_path, "bridges")),
                "engines": os.path.exists(os.path.join(core_path, "src", "engines")),
                "cmake_build": os.path.exists(
                    os.path.join(core_path, "CMakeLists.txt")
                ),
            }

            # Check for integration bridge connections
            integration_connections = False
            if self.integration_bridges:
                try:
                    supervisor_status = (
                        await self.integration_bridges.cytoplasm_bridge.dendritic_supervisor.get_supervisor_status()
                    )
                    integration_connections = supervisor_status.get(
                        "core_engine_connected", False
                    )
                except:
                    pass

            active_tools = sum(1 for active in tools.values() if active)
            total_tools = len(tools)

            return {
                "status": "active" if active_tools >= 3 else "developing",
                "tools": tools,
                "integration_connections": integration_connections,
                "health_score": active_tools / total_tools,
                "description": "Core Engine Component - Low-level processing and optimization",
                "primary_function": "High-performance computing and system optimization",
                "architecture_type": "Processing Engine Component",
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "health_score": 0.0}

    async def _check_dendritic_connections(self) -> Dict[str, Any]:
        """Check integration bridge connection status."""
        try:
            connections = {
                "ai_core_bridge": False,
                "integration_supervisor": False,
                "interface_integration": False,
                "module_monitoring": False,
            }

            connection_health = 0.0

            if self.integration_bridges:
                try:
                    # Check bridge status
                    bridge_status = (
                        await self.integration_bridges.cytoplasm_bridge.get_bridge_status()
                    )
                    connections["ai_core_bridge"] = bridge_status.get("active", False)

                    # Check supervisor
                    supervisor_status = (
                        await self.integration_bridges.cytoplasm_bridge.dendritic_supervisor.get_supervisor_status()
                    )
                    connections["integration_supervisor"] = supervisor_status.get(
                        "active", False
                    )
                    connections["interface_integration"] = supervisor_status.get(
                        "core_engine_connected", False
                    )
                    connections["module_monitoring"] = supervisor_status.get(
                        "organ_monitoring_active", False
                    )

                except Exception as e:
                    self.logger.warning(f"Error checking integration bridges: {e}")

            active_connections = sum(1 for active in connections.values() if active)
            total_connections = len(connections)
            connection_health = active_connections / total_connections

            return {
                "status": "active" if connection_health >= 0.75 else "developing",
                "connections": connections,
                "health_score": connection_health,
                "description": "Integration bridges between components",
                "primary_function": "Inter-component communication and supervision",
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "health_score": 0.0}

    def _calculate_overall_health(self, status: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall AIOS architecture health."""
        try:
            component_scores = []
            integration_score = 0.0

            # Collect component health scores
            for component_name, component_data in status["components"].items():
                if (
                    isinstance(component_data, dict)
                    and "health_score" in component_data
                ):
                    component_scores.append(component_data["health_score"])

            # Get integration bridge score
            if "integration_bridges" in status and isinstance(
                status["integration_bridges"], dict
            ):
                integration_score = status["integration_bridges"].get(
                    "health_score", 0.0
                )

            # Calculate weighted health score
            if component_scores:
                avg_component_health = sum(component_scores) / len(component_scores)
                # Weight: 70% components, 30% integration bridges
                overall_score = (avg_component_health * 0.7) + (integration_score * 0.3)
            else:
                overall_score = 0.0

            # Determine health status
            if overall_score >= 0.8:
                health_status = "excellent"
            elif overall_score >= 0.6:
                health_status = "good"
            elif overall_score >= 0.4:
                health_status = "fair"
            else:
                health_status = "poor"

            return {
                "score": overall_score,
                "status": health_status,
                "component_count": len(component_scores),
                "integration_active": integration_score > 0.5,
            }

        except Exception as e:
            return {"score": 0.0, "status": "error", "error": str(e)}

    def _assess_aios_compliance(self, status: Dict[str, Any]) -> Dict[str, Any]:
        """Assess AIOS architecture compliance."""
        try:
            compliance_checks = {
                "component_independence": True,
                "integration_bridges": False,
                "proper_communication_flow": False,
                "module_monitoring": False,
            }

            # Check component independence
            components = status.get("components", {})
            interface_active = components.get("interface", {}).get("status") == "active"
            ai_intelligence_active = (
                components.get("ai_intelligence", {}).get("status") == "active"
            )
            core_engine_active = (
                components.get("core_engine", {}).get("status") == "active"
            )

            compliance_checks["component_independence"] = (
                interface_active and ai_intelligence_active and core_engine_active
            )

            # Check integration bridges
            bridge_data = status.get("integration_bridges", {})
            compliance_checks["integration_bridges"] = bridge_data.get(
                "connections", {}
            ).get("integration_bridge", False)

            # Check communication flow
            compliance_checks["proper_communication_flow"] = bridge_data.get(
                "connections", {}
            ).get("ai_core_bridge", False) and bridge_data.get("connections", {}).get(
                "interface_integration", False
            )

            # Check module monitoring
            compliance_checks["module_monitoring"] = bridge_data.get(
                "connections", {}
            ).get("module_monitoring", False)

            # Calculate compliance score
            compliance_score = sum(
                1 for check in compliance_checks.values() if check
            ) / len(compliance_checks)

            if compliance_score >= 0.75:
                compliance_status = "fully_compliant"
            elif compliance_score >= 0.5:
                compliance_status = "partially_compliant"
            else:
                compliance_status = "non_compliant"

            return {
                "status": compliance_status,
                "score": compliance_score,
                "checks": compliance_checks,
                "description": "Biological architecture compliance assessment",
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "score": 0.0}

    async def get_supercell_details(self, supercell_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific supercell."""
        try:
            if supercell_name == "interface_supercell":
                return await self._check_interface_supercell()
            elif supercell_name == "runtime":
                return await self._check_runtime()
            elif supercell_name == "ai_intelligence_supercell":
                return await self._check_ai_intelligence_supercell()
            elif supercell_name == "core_engine_supercell":
                return await self._check_core_engine_supercell()
            else:
                return {
                    "error": f"Unknown supercell: {supercell_name}",
                    "available_supercells": [
                        "interface_supercell",
                        "runtime",
                        "ai_intelligence_supercell",
                        "core_engine_supercell",
                    ],
                }

        except Exception as e:
            return {"error": str(e), "supercell": supercell_name}

    async def generate_status_report(self) -> str:
        """Generate a comprehensive status report."""
        try:
            status = await self.get_comprehensive_status()

            report = f"""
AIOS Architecture Status Report
===============================
Generated: {status['timestamp']}

 AIOS ARCHITECTURE OVERVIEW
Status: {status['aios_architecture']['status'].upper()}
Compliance: {status['aios_architecture']['score']:.2f} ({status['aios_architecture']['status']})
Overall Health: {status['overall_health']['score']:.2f} ({status['overall_health']['status'].upper()})

 COMPONENT STATUS
"""

            # Add component details
            for component_name, component_data in status["components"].items():
                if isinstance(component_data, dict):
                    report += f"""
{component_name.replace('_', ' ').title()}:
  Status: {component_data.get('status', 'unknown').upper()}
  Health: {component_data.get('health_score', 0.0):.2f}
  Type: {component_data.get('architecture_type', 'Unknown')}
  Function: {component_data.get('primary_function', 'Unknown')}
"""

            # Add integration bridges section
            integration_data = status.get("integration_bridges", {})
            report += f"""
 INTEGRATION BRIDGES
Status: {integration_data.get('status', 'unknown').upper()}
Health: {integration_data.get('health_score', 0.0):.2f}

Connection Details:
"""

            connections = integration_data.get("connections", {})
            for conn_name, conn_status in connections.items():
                status_icon = "" if conn_status else ""
                report += f"  {status_icon} {conn_name.replace('_', ' ').title()}\n"

            report += f"""
 ARCHITECTURE SUMMARY
Components Active: {status['overall_health'].get('component_count', 0)}
Integration Active: {'' if status['overall_health'].get('integration_active', False) else ''}
AIOS Compliance: {status['aios_architecture']['score']:.2f}

 RECOMMENDATIONS
"""

            # Add recommendations based on status
            if status["overall_health"]["score"] < 0.6:
                report += "- Critical: Improve component health scores\n"
            if not status["overall_health"].get("integration_active", False):
                report += "- Important: Establish integration bridges\n"
            if status["aios_architecture"]["score"] < 0.75:
                report += "- Recommended: Enhance AIOS architecture compliance\n"

            if status["overall_health"]["score"] >= 0.8:
                report += "- Excellent: Architecture is operating optimally\n"

            return report

        except Exception as e:
            return f"Error generating status report: {str(e)}"


# Global instance
_aios_architecture_monitor = None


async def get_aios_architecture_monitor() -> AIOSArchitectureMonitor:
    """Get the singleton AIOS architecture monitor."""
    global _aios_architecture_monitor

    if _aios_architecture_monitor is None:
        _aios_architecture_monitor = AIOSArchitectureMonitor()
        await _aios_architecture_monitor.initialize()

    return _aios_architecture_monitor


async def main():
    """Test the AIOS architecture monitor."""
    print(" AIOS Architecture Monitor")
    print("=" * 50)

    # Initialize monitor
    monitor = await get_aios_architecture_monitor()

    # Generate status report
    print(" Generating comprehensive status report...\n")
    report = await monitor.generate_status_report()
    print(report)


if __name__ == "__main__":
    asyncio.run(main())
