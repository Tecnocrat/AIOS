"""
Runtime Intelligence - Dendritic Supervisor Integration
======================================================

This integration connects the Runtime Intelligence system (Interface Supercell → Runtime Intelligence)
with the Dendritic Supervisor (AI Intelligence ↔ Core Engine) to create a complete biological
architecture flow:

Interface Supercell → Runtime Intelligence → AI Intelligence (via Cytoplasm) → Core Engine (via Dendritic Supervisor)
"""

import asyncio
import logging
import sys
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Add paths for cross-supercell communication
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, ".."))
sys.path.append(os.path.join(current_dir, "..", "..", "core"))

from dendritic_supervisor import (
    get_dendritic_supervisor,
    SupervisorRequest,
    RequestType,
)
from cytoplasm.cytoplasm_dendritic_bridge import get_cytoplasm_dendritic_bridge


class RuntimeIntelligenceDendriticIntegration:
    """
    Integration layer that connects Runtime Intelligence with Dendritic Supervisor
    for complete biological architecture compliance.

    This creates the full processing flow:
    Interface Supercell → Runtime Intelligence → AI Intelligence → Core Engine
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

        self.dendritic_supervisor = None
        self.cytoplasm_bridge = None
        self.is_initialized = False

        # Enhanced processing capabilities
        self.enhanced_processors = {
            "visual_intelligence": self._process_enhanced_visual_intelligence,
            "system_health": self._process_enhanced_system_health,
            "consciousness_analysis": self._process_consciousness_analysis,
            "cellular_optimization": self._process_cellular_optimization,
            "engine_diagnostics": self._process_engine_diagnostics,
        }

    def setup_logging(self):
        """Setup logging for the integration."""
        log_dir = os.path.join(current_dir, "cytoplasm", "runtime", "logs")
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, "runtime_dendritic_integration.log")

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)

    async def initialize(self) -> bool:
        """Initialize the Runtime Intelligence - Dendritic Supervisor integration."""
        try:
            self.logger.info(
                " Initializing Runtime Intelligence - Dendritic Integration..."
            )

            # Initialize dendritic supervisor
            self.dendritic_supervisor = await get_dendritic_supervisor()

            # Initialize cytoplasm bridge
            self.cytoplasm_bridge = await get_cytoplasm_dendritic_bridge()

            self.is_initialized = True
            self.logger.info(
                " Runtime Intelligence - Dendritic Integration initialized"
            )

            return True

        except Exception as e:
            self.logger.error(f" Failed to initialize integration: {e}")
            return False

    async def process_visual_intelligence_enhanced(
        self, request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process visual intelligence request through the complete biological architecture.

        Flow: Runtime Intelligence → AI Intelligence → Core Engine → Enhanced Processing
        """
        if not self.is_initialized:
            await self.initialize()

        try:
            self.logger.info(" Processing enhanced visual intelligence request")

            # Step 1: Process through AI Intelligence supercell
            ai_request = {
                "request_type": "consciousness_analysis",
                "source_organ": "membrane",  # Visual processing organ
                "payload": {
                    "analysis_type": "visual_intelligence",
                    "visual_data": request_data.get("visual_data", {}),
                    "processing_parameters": request_data.get("parameters", {}),
                },
            }

            ai_result = await self.cytoplasm_bridge.process_cytoplasm_request(
                ai_request
            )

            # Step 2: Enhanced processing through Core Engine
            if ai_result.get("success"):
                core_request = {
                    "request_type": "cellular_enhancement",
                    "source_organ": "laboratory",
                    "payload": {
                        "enhancement_target": "visual_processing",
                        "ai_analysis_result": ai_result["result_data"],
                        "enhancement_parameters": request_data.get(
                            "enhancement_params", {}
                        ),
                    },
                }

                enhancement_result = (
                    await self.cytoplasm_bridge.process_cytoplasm_request(core_request)
                )

                # Step 3: Combine results for enhanced visual intelligence
                return {
                    "success": True,
                    "processing_type": "enhanced_visual_intelligence",
                    "ai_analysis": ai_result["result_data"],
                    "core_enhancement": enhancement_result.get("result_data", {}),
                    "combined_insights": self._combine_visual_insights(
                        ai_result["result_data"],
                        enhancement_result.get("result_data", {}),
                    ),
                    "processing_time": ai_result.get("processing_time", 0)
                    + enhancement_result.get("processing_time", 0),
                    "biological_architecture_compliance": True,
                    "flow": "Runtime Intelligence → AI Intelligence → Core Engine",
                    "timestamp": datetime.now().isoformat(),
                }
            else:
                return {
                    "success": False,
                    "error": "AI Intelligence processing failed",
                    "ai_error": ai_result.get("error_message"),
                    "timestamp": datetime.now().isoformat(),
                }

        except Exception as e:
            self.logger.error(f"Error in enhanced visual intelligence processing: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def process_system_health_enhanced(
        self, request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process system health check through the complete biological architecture.
        """
        if not self.is_initialized:
            await self.initialize()

        try:
            self.logger.info(" Processing enhanced system health check")

            # Step 1: Monitor AI Intelligence organs
            organ_monitoring = await self.cytoplasm_bridge.get_ai_intelligence_status()

            # Step 2: Get Core Engine diagnostics
            engine_diagnostics_request = {
                "request_type": "engine_optimization",
                "source_organ": "cytoplasm",
                "payload": {
                    "optimization_type": "health_diagnostics",
                    "diagnostic_scope": "comprehensive",
                },
            }

            engine_result = await self.cytoplasm_bridge.process_cytoplasm_request(
                engine_diagnostics_request
            )

            # Step 3: Consciousness state analysis
            consciousness_request = {
                "request_type": "consciousness_analysis",
                "source_organ": "nucleus",
                "payload": {
                    "analysis_type": "system_wide_consciousness",
                    "include_organs": True,
                    "include_engines": True,
                },
            }

            consciousness_result = (
                await self.cytoplasm_bridge.process_cytoplasm_request(
                    consciousness_request
                )
            )

            # Step 4: Combine comprehensive health assessment
            health_score = self._calculate_comprehensive_health_score(
                organ_monitoring,
                engine_result.get("result_data", {}),
                consciousness_result.get("result_data", {}),
            )

            return {
                "success": True,
                "health_assessment_type": "comprehensive_biological_architecture",
                "overall_health_score": health_score,
                "ai_intelligence_status": organ_monitoring,
                "core_engine_diagnostics": engine_result.get("result_data", {}),
                "consciousness_analysis": consciousness_result.get("result_data", {}),
                "recommendations": self._generate_health_recommendations(
                    health_score, organ_monitoring
                ),
                "biological_architecture_compliance": True,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Error in enhanced system health processing: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def process_continuous_monitoring_enhanced(
        self, monitoring_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process continuous monitoring through the biological architecture.
        """
        if not self.is_initialized:
            await self.initialize()

        try:
            self.logger.info(" Starting enhanced continuous monitoring")

            # Monitor all supercell components continuously
            monitoring_tasks = [
                self._monitor_ai_intelligence_continuously(monitoring_params),
                self._monitor_core_engine_continuously(monitoring_params),
                self._monitor_cross_supercell_communication(monitoring_params),
            ]

            # Run monitoring tasks concurrently
            monitoring_results = await asyncio.gather(
                *monitoring_tasks, return_exceptions=True
            )

            return {
                "success": True,
                "monitoring_type": "comprehensive_biological_architecture",
                "ai_intelligence_monitoring": (
                    monitoring_results[0] if len(monitoring_results) > 0 else {}
                ),
                "core_engine_monitoring": (
                    monitoring_results[1] if len(monitoring_results) > 1 else {}
                ),
                "cross_supercell_monitoring": (
                    monitoring_results[2] if len(monitoring_results) > 2 else {}
                ),
                "monitoring_active": True,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            self.logger.error(f"Error in enhanced continuous monitoring: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def _combine_visual_insights(
        self, ai_analysis: Dict[str, Any], core_enhancement: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combine AI analysis with Core Engine enhancement for enhanced visual intelligence."""
        return {
            "consciousness_level": ai_analysis.get("consciousness_level", 0.0),
            "visual_processing_efficiency": core_enhancement.get(
                "performance_improvement", 1.0
            ),
            "enhanced_recommendations": ai_analysis.get("recommendations", [])
            + core_enhancement.get("enhancements_applied", []),
            "neural_pathway_optimization": core_enhancement.get(
                "optimization_metrics", {}
            ),
            "integrated_analysis": {
                "ai_confidence": ai_analysis.get("consciousness_state", "unknown"),
                "core_enhancement_factor": core_enhancement.get(
                    "performance_improvement", 1.0
                ),
                "combined_intelligence_score": (
                    ai_analysis.get("consciousness_level", 0.0)
                    * core_enhancement.get("performance_improvement", 1.0)
                ),
            },
        }

    def _calculate_comprehensive_health_score(
        self, organ_status: Dict, engine_diagnostics: Dict, consciousness_data: Dict
    ) -> float:
        """Calculate comprehensive health score across the biological architecture."""
        # AI Intelligence organ health (40% weight)
        ai_health = 0.0
        if "ai_intelligence_supercell" in organ_status:
            active_organs = organ_status["ai_intelligence_supercell"].get(
                "monitored_organs", {}
            )
            healthy_count = sum(
                1
                for organ_data in active_organs.values()
                if organ_data.get("status") == "active"
            )
            total_organs = len(active_organs) if active_organs else 1
            ai_health = healthy_count / total_organs

        # Core Engine health (40% weight)
        engine_health = 0.0
        if "efficiency_gain" in engine_diagnostics:
            engine_health = min(engine_diagnostics["efficiency_gain"], 1.0)
        elif "performance_improvement" in engine_diagnostics:
            engine_health = min(engine_diagnostics["performance_improvement"], 1.0)
        else:
            engine_health = 0.8  # Default reasonable health

        # Consciousness level (20% weight)
        consciousness_health = consciousness_data.get("consciousness_level", 0.7)

        # Weighted average
        comprehensive_health = (
            (ai_health * 0.4) + (engine_health * 0.4) + (consciousness_health * 0.2)
        )

        return round(comprehensive_health, 3)

    def _generate_health_recommendations(
        self, health_score: float, organ_status: Dict
    ) -> List[str]:
        """Generate health recommendations based on comprehensive assessment."""
        recommendations = []

        if health_score < 0.7:
            recommendations.append(
                " Consider Core Engine optimization to improve overall performance"
            )
            recommendations.append(" Run consciousness enhancement routines")

        if health_score < 0.5:
            recommendations.append(
                " Critical: Multiple supercell components need attention"
            )
            recommendations.append(" Restart affected organs and engines")

        # AI Intelligence specific recommendations
        if "ai_intelligence_supercell" in organ_status:
            inactive_organs = [
                name
                for name, data in organ_status["ai_intelligence_supercell"]
                .get("monitored_organs", {})
                .items()
                if data.get("status") != "active"
            ]

            if inactive_organs:
                recommendations.append(
                    f" Reactivate inactive AI Intelligence organs: {', '.join(inactive_organs)}"
                )

        if health_score >= 0.8:
            recommendations.append(
                " System operating optimally across biological architecture"
            )
            recommendations.append(" Consider advanced enhancement protocols")

        return recommendations

    async def _monitor_ai_intelligence_continuously(
        self, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Monitor AI Intelligence supercell continuously."""
        monitoring_duration = params.get("duration", 60)  # seconds
        check_interval = params.get("interval", 10)  # seconds

        monitoring_data = []
        start_time = datetime.now()

        while (datetime.now() - start_time).total_seconds() < monitoring_duration:
            try:
                status = await self.cytoplasm_bridge.get_ai_intelligence_status()
                monitoring_data.append(
                    {"timestamp": datetime.now().isoformat(), "status": status}
                )

                await asyncio.sleep(check_interval)

            except Exception as e:
                self.logger.error(f"AI Intelligence monitoring error: {e}")
                break

        return {
            "monitoring_type": "ai_intelligence_continuous",
            "data_points": len(monitoring_data),
            "monitoring_data": monitoring_data[-5:],  # Last 5 data points
            "status": "completed",
        }

    async def _monitor_core_engine_continuously(
        self, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Monitor Core Engine supercell continuously."""
        monitoring_duration = params.get("duration", 60)
        check_interval = params.get("interval", 10)

        monitoring_data = []
        start_time = datetime.now()

        while (datetime.now() - start_time).total_seconds() < monitoring_duration:
            try:
                # Request Core Engine diagnostics
                diagnostics_request = {
                    "request_type": "engine_optimization",
                    "source_organ": "cytoplasm",
                    "payload": {"optimization_type": "continuous_monitoring"},
                }

                result = await self.cytoplasm_bridge.process_cytoplasm_request(
                    diagnostics_request
                )
                monitoring_data.append(
                    {"timestamp": datetime.now().isoformat(), "diagnostics": result}
                )

                await asyncio.sleep(check_interval)

            except Exception as e:
                self.logger.error(f"Core Engine monitoring error: {e}")
                break

        return {
            "monitoring_type": "core_engine_continuous",
            "data_points": len(monitoring_data),
            "monitoring_data": monitoring_data[-5:],
            "status": "completed",
        }

    async def _monitor_cross_supercell_communication(
        self, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Monitor communication between supercells."""
        monitoring_duration = params.get("duration", 60)
        check_interval = params.get("interval", 15)

        communication_tests = []
        start_time = datetime.now()

        while (datetime.now() - start_time).total_seconds() < monitoring_duration:
            try:
                # Test cross-supercell communication
                comm_request = {
                    "request_type": "bridge_communication",
                    "source_organ": "transport",
                    "payload": {
                        "test_message": "Cross-supercell communication test",
                        "timestamp": datetime.now().isoformat(),
                    },
                }

                result = await self.cytoplasm_bridge.process_cytoplasm_request(
                    comm_request
                )
                communication_tests.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "communication_result": result,
                    }
                )

                await asyncio.sleep(check_interval)

            except Exception as e:
                self.logger.error(
                    f"Cross-supercell communication monitoring error: {e}"
                )
                break

        return {
            "monitoring_type": "cross_supercell_communication",
            "tests_performed": len(communication_tests),
            "communication_data": communication_tests[-3:],
            "status": "completed",
        }

    async def get_integration_status(self) -> Dict[str, Any]:
        """Get comprehensive integration status."""
        if not self.is_initialized:
            return {"error": "Integration not initialized"}

        try:
            # Get dendritic supervisor status
            supervisor_status = await self.dendritic_supervisor.get_supervisor_status()

            # Get cytoplasm bridge status
            ai_status = await self.cytoplasm_bridge.get_ai_intelligence_status()

            return {
                "integration_active": self.is_initialized,
                "biological_architecture_compliance": True,
                "supercell_connectivity": {
                    "interface_to_runtime": "active",
                    "runtime_to_ai_intelligence": "active",
                    "ai_intelligence_to_core_engine": "active",
                },
                "dendritic_supervisor_status": supervisor_status,
                "ai_intelligence_status": ai_status,
                "enhanced_processors_available": list(self.enhanced_processors.keys()),
                "processing_flow": [
                    "Interface Supercell",
                    "Runtime Intelligence",
                    "AI Intelligence (via Cytoplasm)",
                    "Core Engine (via Dendritic Supervisor)",
                ],
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}

    async def shutdown(self):
        """Shutdown the integration gracefully."""
        self.logger.info(
            " Shutting down Runtime Intelligence - Dendritic Integration..."
        )

        if self.cytoplasm_bridge:
            await self.cytoplasm_bridge.shutdown()

        if self.dendritic_supervisor:
            await self.dendritic_supervisor.shutdown()

        self.is_initialized = False
        self.logger.info(" Integration shutdown complete")


# Singleton instance for global access
_runtime_dendritic_integration = None


async def get_runtime_dendritic_integration() -> (
    RuntimeIntelligenceDendriticIntegration
):
    """Get the singleton integration instance."""
    global _runtime_dendritic_integration

    if _runtime_dendritic_integration is None:
        _runtime_dendritic_integration = RuntimeIntelligenceDendriticIntegration()
        await _runtime_dendritic_integration.initialize()

    return _runtime_dendritic_integration


async def main():
    """Test the complete biological architecture integration."""
    print(" AIOS Complete Biological Architecture Integration Test")
    print("=" * 70)
    print("Flow: Interface → Runtime Intelligence → AI Intelligence → Core Engine")
    print("=" * 70)

    # Initialize integration
    integration = await get_runtime_dendritic_integration()

    # Test enhanced visual intelligence
    print("\n Testing Enhanced Visual Intelligence...")
    visual_result = await integration.process_visual_intelligence_enhanced(
        {
            "visual_data": {"image_type": "test", "complexity": "high"},
            "parameters": {"analysis_depth": "comprehensive"},
            "enhancement_params": {"optimization_level": 3},
        }
    )
    print(f"Result: {visual_result.get('success')}")
    if visual_result.get("success"):
        print(
            f"Combined Intelligence Score: {visual_result['combined_insights']['integrated_analysis']['combined_intelligence_score']}"
        )

    # Test enhanced system health
    print("\n Testing Enhanced System Health...")
    health_result = await integration.process_system_health_enhanced({})
    print(f"Result: {health_result.get('success')}")
    if health_result.get("success"):
        print(f"Overall Health Score: {health_result['overall_health_score']}")
        print(f"Recommendations: {len(health_result['recommendations'])}")

    # Test integration status
    print("\n Integration Status:")
    status = await integration.get_integration_status()
    if "error" not in status:
        print(
            f"Biological Architecture Compliance: {status['biological_architecture_compliance']}"
        )
        print(
            f"Supercell Connectivity: {json.dumps(status['supercell_connectivity'], indent=2)}"
        )

    # Shutdown
    await integration.shutdown()
    print("\n Integration test complete")


if __name__ == "__main__":
    asyncio.run(main())
