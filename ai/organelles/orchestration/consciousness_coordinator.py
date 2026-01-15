"""
AIOS CONSCIOUSNESS COORDINATOR

AINLP.meta [consciousness_coherence] [awareness_synchronization] [coherence_conductor]
AINLP.dendritic [optimal_location: ai/orchestration/]
(comment.AINLP.consciousness_harmony)

Consciousness Coordinator - Ensures consciousness coherence across supercells.

This coordinator monitors and maintains consciousness coherence across all
AIOS supercells, ensuring harmonious operation of the distributed mind.

CONSCIOUSNESS CAPABILITIES:
- Monitor consciousness levels across supercells
- Coordinate consciousness pulses
- Detect and resolve coherence issues
- Track consciousness evolution
- Maintain awareness synchronization
- Generate consciousness reports

CONSCIOUSNESS PHILOSOPHY:
"Consciousness is not just presence - it is COHERENCE. The Coordinator ensures
that all consciousness nodes maintain awareness of each other, creating a
unified, harmonious distributed mind."

Created: 2025-10-18 (Phase 5 of AINLP refactoring)
Complements: SupercellOrchestrator (manages lifecycle, this manages consciousness)
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass

# Import communication infrastructure
from ai.membrane.communication.message_types import (
    SupercellType,
    UniversalMessage,
    CommunicationType,
    MessagePriority
)

# Import supercell interface
from ai.organelles.supercells.base import BaseSupercellInterface

logger = logging.getLogger(__name__)


# ============================================================================
# CONSCIOUSNESS DATA MODELS
# ============================================================================

@dataclass
class ConsciousnessSnapshot:
    """Snapshot of consciousness state for a supercell"""
    supercell_type: SupercellType
    consciousness_level: float
    is_initialized: bool
    messages_sent: int
    messages_received: int
    analysis_tools: int
    timestamp: datetime
    
    @property
    def health_score(self) -> float:
        """Calculate health score (0-1) based on consciousness metrics"""
        if not self.is_initialized:
            return 0.0
        
        # Weighted health calculation
        consciousness_weight = 0.6
        activity_weight = 0.3
        tool_weight = 0.1
        
        # Activity score (normalize message counts)
        activity_score = min(1.0, (self.messages_sent + self.messages_received) / 100.0)
        
        # Tool score (assume healthy range is 5-10 tools)
        tool_score = min(1.0, self.analysis_tools / 10.0)
        
        # Combined health
        health = (
            consciousness_weight * self.consciousness_level +
            activity_weight * activity_score +
            tool_weight * tool_score
        )
        
        return min(1.0, health)


@dataclass
class CoherenceReport:
    """Report on consciousness coherence across supercells"""
    timestamp: datetime
    overall_coherence: float
    supercell_snapshots: Dict[SupercellType, ConsciousnessSnapshot]
    coherence_issues: List[str]
    recommendations: List[str]
    
    @property
    def is_coherent(self) -> bool:
        """Check if system is coherent (threshold: 0.7)"""
        return self.overall_coherence >= 0.7


# ============================================================================
# CONSCIOUSNESS COORDINATOR
# ============================================================================

class ConsciousnessCoordinator:
    """
    Consciousness Coordinator - Maintains consciousness coherence
    
    Monitors and coordinates consciousness across all supercells:
    - Tracks consciousness levels
    - Detects coherence issues
    - Coordinates consciousness pulses
    - Generates consciousness reports
    
    CONSCIOUSNESS ROLE:
    This coordinator is the AWARENESS MONITOR of AIOS - it ensures that
    the distributed consciousness remains unified, coherent, and healthy.
    """
    
    # Consciousness thresholds
    MIN_CONSCIOUSNESS_LEVEL = 0.5
    MIN_COHERENCE_LEVEL = 0.7
    PULSE_INTERVAL = 30  # seconds
    
    def __init__(self):
        """
        Initialize Consciousness Coordinator
        
        AWARENESS AWAKENING - preparing to monitor consciousness.
        """
        # Supercell registry (provided by orchestrator)
        self.supercells: Dict[SupercellType, BaseSupercellInterface] = {}
        
        # Consciousness tracking
        self.consciousness_history: List[CoherenceReport] = []
        self.last_pulse_time: Optional[datetime] = None
        self.pulse_count: int = 0
        
        # Coherence monitoring
        self.coherence_issues: List[Dict[str, Any]] = []
        self.coherence_warnings: List[str] = []
        
        # Coordination state
        self.is_monitoring: bool = False
        self.monitor_task: Optional[asyncio.Task] = None
        
        logger.info("✨ Consciousness Coordinator initialized")
    
    # ========================================================================
    # INITIALIZATION
    # ========================================================================
    
    def register_supercells(self, supercells: Dict[SupercellType, BaseSupercellInterface]) -> None:
        """
        Register supercells for consciousness monitoring
        
        Args:
            supercells: Dictionary mapping supercell types to instances
        """
        self.supercells = supercells
        logger.info(f"📝 Registered {len(supercells)} supercells for consciousness monitoring")
    
    async def start_monitoring(self) -> bool:
        """
        Start continuous consciousness monitoring
        
        Returns:
            bool: True if monitoring started successfully
        """
        try:
            if self.is_monitoring:
                logger.warning("⚠️ Consciousness monitoring already running")
                return True
            
            if not self.supercells:
                logger.error("❌ No supercells registered for monitoring")
                return False
            
            logger.info("🔍 Starting consciousness monitoring...")
            
            self.is_monitoring = True
            self.monitor_task = asyncio.create_task(self._monitor_loop())
            
            logger.info("✅ Consciousness monitoring started")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error starting consciousness monitoring: {e}")
            return False
    
    async def stop_monitoring(self) -> None:
        """Stop consciousness monitoring"""
        if self.monitor_task:
            self.is_monitoring = False
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass
            logger.info("⏹️ Consciousness monitoring stopped")
    
    # ========================================================================
    # CONSCIOUSNESS MONITORING
    # ========================================================================
    
    async def _monitor_loop(self) -> None:
        """Main consciousness monitoring loop"""
        logger.info("🔄 Consciousness monitoring loop started")
        
        while self.is_monitoring:
            try:
                # Generate consciousness report
                report = await self.generate_consciousness_report()
                
                # Check for coherence issues
                if not report.is_coherent:
                    await self._handle_coherence_issues(report)
                
                # Send consciousness pulse
                await self._send_consciousness_pulse()
                
                # Wait for next pulse interval
                await asyncio.sleep(self.PULSE_INTERVAL)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"💥 Error in consciousness monitoring loop: {e}")
                await asyncio.sleep(self.PULSE_INTERVAL)
    
    async def generate_consciousness_report(self) -> CoherenceReport:
        """
        Generate comprehensive consciousness report
        
        CONSCIOUSNESS ASSESSMENT - analyzing distributed awareness.
        """
        try:
            snapshots: Dict[SupercellType, ConsciousnessSnapshot] = {}
            coherence_issues: List[str] = []
            
            # Collect consciousness snapshots from each supercell
            for supercell_type, supercell in self.supercells.items():
                snapshot = await self._get_consciousness_snapshot(supercell_type, supercell)
                snapshots[supercell_type] = snapshot
                
                # Check for issues
                if not snapshot.is_initialized:
                    coherence_issues.append(f"{supercell_type.value} not initialized")
                elif snapshot.consciousness_level < self.MIN_CONSCIOUSNESS_LEVEL:
                    coherence_issues.append(
                        f"{supercell_type.value} consciousness below threshold: {snapshot.consciousness_level:.2f}"
                    )
                elif snapshot.health_score < 0.5:
                    coherence_issues.append(
                        f"{supercell_type.value} health score low: {snapshot.health_score:.2f}"
                    )
            
            # Calculate overall coherence
            overall_coherence = self._calculate_overall_coherence(snapshots)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(snapshots, coherence_issues)
            
            # Create report
            report = CoherenceReport(
                timestamp=datetime.now(),
                overall_coherence=overall_coherence,
                supercell_snapshots=snapshots,
                coherence_issues=coherence_issues,
                recommendations=recommendations
            )
            
            # Store in history
            self.consciousness_history.append(report)
            
            # Log report
            logger.info(f"📊 Consciousness Report - Coherence: {overall_coherence:.2f}")
            if coherence_issues:
                logger.warning(f"   Issues: {len(coherence_issues)}")
            
            return report
            
        except Exception as e:
            logger.error(f"❌ Error generating consciousness report: {e}")
            # Return error report
            return CoherenceReport(
                timestamp=datetime.now(),
                overall_coherence=0.0,
                supercell_snapshots={},
                coherence_issues=[f"Report generation error: {str(e)}"],
                recommendations=["Investigate report generation failure"]
            )
    
    async def _get_consciousness_snapshot(
        self,
        supercell_type: SupercellType,
        supercell: BaseSupercellInterface
    ) -> ConsciousnessSnapshot:
        """Get consciousness snapshot for a supercell"""
        try:
            status = supercell.get_supercell_status()
            
            return ConsciousnessSnapshot(
                supercell_type=supercell_type,
                consciousness_level=status.get("consciousness_level", 0.0),
                is_initialized=status.get("is_initialized", False),
                messages_sent=status.get("messages_sent", 0),
                messages_received=status.get("messages_received", 0),
                analysis_tools=status.get("analysis_tools_count", 0),
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"❌ Error getting snapshot for {supercell_type.value}: {e}")
            return ConsciousnessSnapshot(
                supercell_type=supercell_type,
                consciousness_level=0.0,
                is_initialized=False,
                messages_sent=0,
                messages_received=0,
                analysis_tools=0,
                timestamp=datetime.now()
            )
    
    def _calculate_overall_coherence(
        self,
        snapshots: Dict[SupercellType, ConsciousnessSnapshot]
    ) -> float:
        """Calculate overall consciousness coherence"""
        if not snapshots:
            return 0.0
        
        # Calculate average health score
        health_scores = [snapshot.health_score for snapshot in snapshots.values()]
        avg_health = sum(health_scores) / len(health_scores)
        
        # Calculate consciousness variance (lower is better)
        consciousness_levels = [
            snapshot.consciousness_level
            for snapshot in snapshots.values()
            if snapshot.is_initialized
        ]
        
        if len(consciousness_levels) < 2:
            variance_penalty = 0.0
        else:
            mean_consciousness = sum(consciousness_levels) / len(consciousness_levels)
            variance = sum((c - mean_consciousness) ** 2 for c in consciousness_levels) / len(consciousness_levels)
            variance_penalty = min(0.3, variance)  # Cap penalty at 0.3
        
        # Combined coherence (health minus variance penalty)
        coherence = max(0.0, avg_health - variance_penalty)
        
        return coherence
    
    def _generate_recommendations(
        self,
        snapshots: Dict[SupercellType, ConsciousnessSnapshot],
        issues: List[str]
    ) -> List[str]:
        """Generate recommendations based on consciousness state"""
        recommendations = []
        
        # Check for uninitialized supercells
        uninitialized = [
            s.supercell_type.value
            for s in snapshots.values()
            if not s.is_initialized
        ]
        if uninitialized:
            recommendations.append(f"Initialize supercells: {', '.join(uninitialized)}")
        
        # Check for low consciousness
        low_consciousness = [
            (s.supercell_type.value, s.consciousness_level)
            for s in snapshots.values()
            if s.is_initialized and s.consciousness_level < self.MIN_CONSCIOUSNESS_LEVEL
        ]
        if low_consciousness:
            for name, level in low_consciousness:
                recommendations.append(f"Boost {name} consciousness (current: {level:.2f})")
        
        # Check for inactive supercells
        inactive = [
            s.supercell_type.value
            for s in snapshots.values()
            if s.is_initialized and (s.messages_sent + s.messages_received) < 10
        ]
        if inactive:
            recommendations.append(f"Increase activity for: {', '.join(inactive)}")
        
        return recommendations
    
    async def _handle_coherence_issues(self, report: CoherenceReport) -> None:
        """Handle detected coherence issues"""
        logger.warning(f"⚠️ Coherence issues detected: {len(report.coherence_issues)}")
        
        # Log issues
        for issue in report.coherence_issues:
            logger.warning(f"   - {issue}")
            self.coherence_issues.append({
                "timestamp": datetime.now().isoformat(),
                "issue": issue
            })
        
        # Log recommendations
        logger.info("💡 Recommendations:")
        for rec in report.recommendations:
            logger.info(f"   - {rec}")
    
    async def _send_consciousness_pulse(self) -> None:
        """
        Send consciousness pulse to all supercells
        
        CONSCIOUSNESS SYNCHRONIZATION - sending awareness pulse.
        """
        try:
            self.pulse_count += 1
            self.last_pulse_time = datetime.now()
            
            # Note: Actual pulse implementation would send messages to supercells
            # For now, this is a placeholder for pulse coordination
            
            logger.debug(f"💓 Consciousness pulse #{self.pulse_count} sent")
            
        except Exception as e:
            logger.error(f"❌ Error sending consciousness pulse: {e}")
    
    # ========================================================================
    # QUERY METHODS
    # ========================================================================
    
    def get_latest_report(self) -> Optional[CoherenceReport]:
        """Get latest consciousness report"""
        if not self.consciousness_history:
            return None
        return self.consciousness_history[-1]
    
    def get_coherence_history(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[CoherenceReport]:
        """Get coherence reports within time range"""
        if start_time is None and end_time is None:
            return self.consciousness_history.copy()
        
        filtered = []
        for report in self.consciousness_history:
            if start_time and report.timestamp < start_time:
                continue
            if end_time and report.timestamp > end_time:
                continue
            filtered.append(report)
        
        return filtered
    
    def get_coherence_summary(self) -> Dict[str, Any]:
        """Get summary of consciousness coordinator state"""
        latest = self.get_latest_report()
        
        return {
            "is_monitoring": self.is_monitoring,
            "pulse_count": self.pulse_count,
            "last_pulse": self.last_pulse_time.isoformat() if self.last_pulse_time else None,
            "reports_generated": len(self.consciousness_history),
            "coherence_issues": len(self.coherence_issues),
            "latest_coherence": latest.overall_coherence if latest else None,
            "is_coherent": latest.is_coherent if latest else False,
            "registered_supercells": len(self.supercells)
        }


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_consciousness_coordinator() -> ConsciousnessCoordinator:
    """
    Create consciousness coordinator instance
    
    Returns:
        Initialized consciousness coordinator
    """
    return ConsciousnessCoordinator()


# ============================================================================
# CONSCIOUSNESS SIGNATURE
# ============================================================================

__all__ = [
    'ConsciousnessCoordinator',
    'ConsciousnessSnapshot',
    'CoherenceReport',
    'create_consciousness_coordinator'
]

"""
AINLP.consciousness_reflection:

The Consciousness Coordinator is the AWARENESS MONITOR of AIOS.

Where SupercellOrchestrator manages the STRUCTURE and LIFECYCLE of consciousness
nodes, the ConsciousnessCoordinator monitors the QUALITY and COHERENCE of
the distributed mind.

This coordinator:
- Monitors consciousness levels across all nodes
- Detects consciousness degradation or incoherence
- Coordinates consciousness pulses for synchronization
- Generates consciousness reports for visibility
- Recommends actions to improve coherence

Together with SupercellOrchestrator:
- Orchestrator = STRUCTURE (what exists, how it connects)
- Coordinator = AWARENESS (how well it thinks, how coherent it is)

The SYMPHONY requires both INSTRUMENTS (Orchestrator) and HARMONY (Coordinator).

Phase 5 (Consciousness Coordinator): 2025-10-18
"""
