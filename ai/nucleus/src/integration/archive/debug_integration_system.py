"""
AIOS Debug Integration System
Context-aware debugging with fractal recovery capabilities
"""

import asyncio
import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional


class DebugSessionType(Enum):
    QUICK = "quick"          # < 30 minutes
    STANDARD = "standard"    # 30 minutes - 2 hours
    EXTENDED = "extended"    # > 2 hours
    EMERGENCY = "emergency"  # Critical issues


class DebugSessionStatus(Enum):
    ACTIVE = "active"
    COMPLETING = "completing"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


@dataclass
class DebugContextSnapshot:
    """Snapshot of system context before debugging"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    debug_target: str = ""
    description: str = ""
    development_phase: str = ""
    fractal_coherence: float = 0.0
    system_health: float = 0.0
    component_states: Dict[str, Any] = field(default_factory=dict)
    active_tasks: List[str] = field(default_factory=list)
    holographic_context: Dict[str, Any] = field(default_factory=dict)
    ai_learning_state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DebugSession:
    """Active debug session tracking"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    target: str = ""
    description: str = ""
    session_type: DebugSessionType = DebugSessionType.STANDARD
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    snapshot_id: str = ""
    status: DebugSessionStatus = DebugSessionStatus.ACTIVE
    findings: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    context_health: float = 1.0
    last_health_check: datetime = field(default_factory=datetime.now)


@dataclass
class DebugRecoveryResult:
    """Result of context recovery from debug session"""
    snapshot_id: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    steps_executed: List[str] = field(default_factory=list)
    success: bool = False
    error: str = ""
    restored_coherence: float = 0.0
    debug_insights_integrated: bool = False


class DebugIntegrationSystem:
    """
    Main debug integration system for AIOS
    Provides context-aware debugging with fractal recovery
    """

    def __init__(self, fractal_ai, holographic_sync, context_recovery):
        self.fractal_ai = fractal_ai
        self.holographic_sync = holographic_sync
        self.context_recovery = context_recovery

        self.active_sessions: Dict[str, DebugSession] = {}
        self.debug_snapshots: Dict[str, DebugContextSnapshot] = {}
        self.session_history: List[DebugSession] = []

        self.logger = logging.getLogger(__name__)

        # Initialize monitoring
        self._monitoring_active = True
        asyncio.create_task(self._monitor_debug_sessions())

    async def start_debug_session(self, debug_target: str,
                                  description: Optional[str] = None,
                                  session_type: Optional[DebugSessionType] = None
                                  ) -> DebugSession:
        """Start a new debug session with context preservation"""
        if session_type is None:
            session_type = DebugSessionType.STANDARD

        try:
            print(f"\n Starting Debug Session: {debug_target}")

            # Create debug context snapshot
            snapshot = await self._create_debug_snapshot(debug_target,
                                                         description)
            print(f" Debug snapshot created: {snapshot.id}")

            # Initialize debug session
            session = DebugSession(
                target=debug_target,
                description=description or f"Debug session for {debug_target}",
                session_type=session_type,
                snapshot_id=snapshot.id
            )

            self.active_sessions[session.id] = session

            # Update system context
            await self._update_debug_mode(True, session.id)

            print(f" Debug session active: {session.id}")
            print(f" Session type: {session_type.value}")
            print(f" Target: {debug_target}")

            return session

        except Exception as e:
            self.logger.error(f"Failed to start debug session: {e}")
            raise DebugSessionError(f"Failed to start debug session: {e}")

    async def complete_debug_session(self, session_id: str,
                                     debug_findings: Optional[List[str]] = None,
                                     restore_context: bool = True
                                     ) -> DebugRecoveryResult:
        """Complete debug session and restore context"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Debug session not found: {session_id}")

        session = self.active_sessions[session_id]
        findings = debug_findings or []

        print(f"\n Completing Debug Session: {session_id}")
        print(f" Debug findings: {len(findings)} items")

        try:
            # Update session
            session.status = DebugSessionStatus.COMPLETING
            session.end_time = datetime.now()
            session.findings = findings

            recovery_result = None

            # Restore context if requested
            if restore_context and session.snapshot_id:
                print(" Restoring pre-debug context...")
                recovery_result = await self._restore_debug_context(
                    session.snapshot_id, findings
                )

                if recovery_result.success:
                    print(" Context restored successfully")
                else:
                    print(f" Context restoration failed: "
                          f"{recovery_result.error}")

            # Complete session
            session.status = DebugSessionStatus.COMPLETED
            self.active_sessions.pop(session_id)
            self.session_history.append(session)

            # Update system context
            await self._update_debug_mode(False, None)

            print(f" Debug session completed: {session_id}")

            return recovery_result or DebugRecoveryResult(
                snapshot_id=session.snapshot_id,
                success=True,
                steps_executed=["Debug session completed without restoration"]
            )

        except Exception as e:
            session.status = DebugSessionStatus.FAILED
            self.logger.error(f"Failed to complete debug session: {e}")
            raise DebugSessionError(f"Failed to complete debug session: {e}")

    async def create_debug_snapshot(self, debug_target: str,
                                    description: str = None
                                    ) -> DebugContextSnapshot:
        """Create a debug context snapshot manually"""
        return await self._create_debug_snapshot(debug_target, description)

    async def restore_from_snapshot(self, snapshot_id: str,
                                    debug_insights: List[str] = None
                                    ) -> DebugRecoveryResult:
        """Restore context from a specific debug snapshot"""
        if snapshot_id not in self.debug_snapshots:
            raise ValueError(f"Debug snapshot not found: {snapshot_id}")

        return await self._restore_debug_context(snapshot_id, debug_insights)

    async def get_debug_session_status(self, session_id: str = None
                                       ) -> Dict[str, Any]:
        """Get status of debug sessions"""
        if session_id:
            if session_id not in self.active_sessions:
                return {"error": f"Session not found: {session_id}"}

            session = self.active_sessions[session_id]
            return {
                "session_id": session.id,
                "target": session.target,
                "status": session.status.value,
                "duration": str(datetime.now() - session.start_time),
                "context_health": session.context_health,
                "warnings": session.warnings,
                "findings_count": len(session.findings)
            }
        else:
            return {
                "active_sessions": len(self.active_sessions),
                "total_snapshots": len(self.debug_snapshots),
                "session_history": len(self.session_history),
                "sessions": [
                    {
                        "id": s.id,
                        "target": s.target,
                        "status": s.status.value,
                        "duration": str(datetime.now() - s.start_time)
                    }
                    for s in self.active_sessions.values()
                ]
            }

    async def process_debug_command(self, command: str) -> Dict[str, Any]:
        """Process natural language debug commands"""
        command_lower = command.lower()

        try:
            # Save debug context commands
            if any(phrase in command_lower for phrase in [
                "save debug context", "create debug snapshot",
                "preserve current state"
            ]):
                target = self._extract_debug_target(command)
                snapshot = await self.create_debug_snapshot(target, command)
                return {
                    "success": True,
                    "action": "debug_snapshot_created",
                    "snapshot_id": snapshot.id,
                    "message": f"Debug snapshot created for: {target}"
                }

            # Start debugging commands
            elif any(phrase in command_lower for phrase in [
                "start debugging", "debug with context", "begin debug session"
            ]):
                target = self._extract_debug_target(command)
                session_type = self._extract_session_type(command)
                session = await self.start_debug_session(target, command,
                                                         session_type)
                return {
                    "success": True,
                    "action": "debug_session_started",
                    "session_id": session.id,
                    "message": f"Debug session started for: {target}"
                }

            # Restore context commands
            elif any(phrase in command_lower for phrase in [
                "restore context", "return to development",
                "complete debug session"
            ]):
                if self.active_sessions:
                    # Get first active session
                    session_id = list(self.active_sessions.keys())[0]
                    findings = self._extract_debug_findings(command)
                    result = await self.complete_debug_session(session_id,
                                                               findings)
                    return {
                        "success": True,
                        "action": "context_restored",
                        "session_id": session_id,
                        "message": "Debug session completed and restored"
                    }
                else:
                    return {
                        "success": False,
                        "error": "No active debug session to complete"
                    }

            # Status commands
            elif any(phrase in command_lower for phrase in [
                "debug status", "session status", "debug info"
            ]):
                status = await self.get_debug_session_status()
                return {
                    "success": True,
                    "action": "debug_status",
                    "status": status
                }

            else:
                return {
                    "success": False,
                    "error": f"Unknown debug command: {command}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "action": "debug_command_failed"
            }

    # Private methods
    async def _create_debug_snapshot(self, debug_target: str,
                                     description: str = None
                                     ) -> DebugContextSnapshot:
        """Create a comprehensive debug context snapshot"""

        # Get current system state
        fractal_state = await self.fractal_ai.get_current_state()
        holographic_context = await self.holographic_sync.get_sync_state()
        context_health = await self.context_recovery.check_context_health()

        snapshot = DebugContextSnapshot(
            debug_target=debug_target,
            description=description or f"Debug snapshot for {debug_target}",
            development_phase=self._get_development_phase(),
            fractal_coherence=fractal_state.get("coherence", 0.0),
            system_health=context_health.get("score", 0.0),
            component_states=await self._get_all_component_states(),
            active_tasks=self._get_active_tasks(),
            holographic_context=holographic_context,
            ai_learning_state=fractal_state.get("learning_state", {})
        )

        self.debug_snapshots[snapshot.id] = snapshot

        self.logger.info(f"Debug snapshot created: {snapshot.id}")
        return snapshot

    async def _restore_debug_context(self, snapshot_id: str,
                                     debug_insights: List[str] = None
                                     ) -> DebugRecoveryResult:
        """Restore context from debug snapshot"""

        snapshot = self.debug_snapshots[snapshot_id]
        result = DebugRecoveryResult(snapshot_id=snapshot_id)

        try:
            # Step 1: Restore fractal AI state
            await self.fractal_ai.restore_state(snapshot.ai_learning_state)
            result.steps_executed.append("Fractal AI state restored")

            # Step 2: Restore holographic synchronization
            await self.holographic_sync.restore_sync_state(
                snapshot.holographic_context)
            result.steps_executed.append("Holographic synchronization restored")

            # Step 3: Restore component states
            await self._restore_component_states(snapshot.component_states)
            result.steps_executed.append("Component states restored")

            # Step 4: Integrate debug insights
            if debug_insights:
                await self._integrate_debug_insights(debug_insights, snapshot)
                result.steps_executed.append(
                    f"Integrated {len(debug_insights)} debug insights")
                result.debug_insights_integrated = True

            # Step 5: Restore development phase
            await self._restore_development_phase(snapshot.development_phase)
            result.steps_executed.append("Development phase restored")

            # Step 6: Verify context integrity
            integrity_check = await self._verify_context_integrity(snapshot)
            result.steps_executed.append(
                f"Context integrity: {'Valid' if integrity_check else 'Compromised'}")

            # Step 7: Calculate restored coherence
            current_state = await self.fractal_ai.get_current_state()
            result.restored_coherence = current_state.get("coherence", 0.0)

            result.success = True
            result.end_time = datetime.now()

            self.logger.info(f"Successfully restored from snapshot: {snapshot_id}")

        except Exception as e:
            result.success = False
            result.error = str(e)
            result.end_time = datetime.now()
            result.steps_executed.append(f"Recovery failed: {str(e)}")
            self.logger.error(f"Debug context recovery failed: {e}")

        return result

    async def _monitor_debug_sessions(self):
        """Monitor active debug sessions"""
        while self._monitoring_active:
            try:
                for session in list(self.active_sessions.values()):
                    # Check session duration
                    duration = datetime.now() - session.start_time

                    # Warn about long sessions
                    if (duration > timedelta(hours=2) and
                            session.session_type != DebugSessionType.EXTENDED):
                        warning = (f"Session duration {duration.total_seconds()/3600:.1f} "
                                   f"hours - consider upgrading to Extended")
                        if warning not in session.warnings:
                            session.warnings.append(warning)

                    # Check context health
                    context_health = await self.context_recovery.check_context_health()
                    session.context_health = context_health.get("score", 0.0)
                    session.last_health_check = datetime.now()

                    if session.context_health < 0.7:
                        warning = (f"Context health degraded during debugging: "
                                   f"{session.context_health:.2f}")
                        if warning not in session.warnings:
                            session.warnings.append(warning)

                await asyncio.sleep(30)  # Check every 30 seconds

            except Exception as e:
                self.logger.error(f"Debug session monitoring error: {e}")
                await asyncio.sleep(60)  # Wait longer on error

    # Helper methods
    def _extract_debug_target(self, command: str) -> str:
        """Extract debug target from command"""
        # Simple extraction - could be enhanced with NLP
        keywords = ["debug", "debugging", "investigate", "analyze"]
        words = command.lower().split()

        for i, word in enumerate(words):
            if word in keywords and i + 1 < len(words):
                return words[i + 1]

        return "unknown_target"

    def _extract_session_type(self, command: str) -> DebugSessionType:
        """Extract session type from command"""
        command_lower = command.lower()

        if "quick" in command_lower:
            return DebugSessionType.QUICK
        elif "extended" in command_lower or "deep" in command_lower:
            return DebugSessionType.EXTENDED
        elif "emergency" in command_lower or "critical" in command_lower:
            return DebugSessionType.EMERGENCY
        else:
            return DebugSessionType.STANDARD

    def _extract_debug_findings(self, command: str) -> List[str]:
        """Extract debug findings from command"""
        # Simple extraction - in practice would be more sophisticated
        if "found" in command.lower() or "discovered" in command.lower():
            return [f"Debug finding from command: {command}"]
        return []

    def _get_development_phase(self) -> str:
        """Get current development phase"""
        # This would integrate with project management system
        return "active_development"

    async def _get_all_component_states(self) -> Dict[str, Any]:
        """Get states of all system components"""
        return {
            "fractal_ai": await self.fractal_ai.get_current_state(),
            "holographic_sync": await self.holographic_sync.get_sync_state(),
            "context_recovery": await self.context_recovery.get_recovery_state(),
            "timestamp": datetime.now().isoformat()
        }

    def _get_active_tasks(self) -> List[str]:
        """Get list of active tasks"""
        # This would integrate with task management system
        return ["debug_integration_development", "fractal_holographic_testing"]

    async def _update_debug_mode(self, debug_mode: bool, session_id: str = None):
        """Update system debug mode"""
        await self.holographic_sync.update_context("debug_mode", debug_mode)
        if session_id:
            await self.holographic_sync.update_context("active_debug_session",
                                                        session_id)

    async def _restore_component_states(self, component_states: Dict[str, Any]):
        """Restore states of all components"""
        for component, state in component_states.items():
            if component == "fractal_ai":
                await self.fractal_ai.restore_state(state)
            elif component == "holographic_sync":
                await self.holographic_sync.restore_sync_state(state)
            # Add other components as needed

    async def _integrate_debug_insights(self, insights: List[str],
                                        snapshot: DebugContextSnapshot):
        """Integrate debug insights into system knowledge"""
        # Add insights to AI learning
        await self.fractal_ai.integrate_learning({
            "debug_insights": insights,
            "debug_target": snapshot.debug_target,
            "integration_timestamp": datetime.now().isoformat()
        })

        # Update holographic context
        await self.holographic_sync.update_context("debug_learnings", {
            "insights": insights,
            "enhanced_by_debug": True,
            "debug_session_id": snapshot.id
        })

    async def _restore_development_phase(self, development_phase: str):
        """Restore development phase"""
        await self.holographic_sync.update_context("development_phase",
                                                    development_phase)

    async def _verify_context_integrity(self,
                                        snapshot: DebugContextSnapshot) -> bool:
        """Verify context integrity after restoration"""
        try:
            current_state = await self.fractal_ai.get_current_state()
            current_coherence = current_state.get("coherence", 0.0)
            snapshot_coherence = snapshot.fractal_coherence

            # Allow 20% coherence variation
            coherence_diff = abs(current_coherence - snapshot_coherence)
            return coherence_diff < 0.2
        except Exception:
            return False

    def shutdown(self):
        """Shutdown debug integration system"""
        self._monitoring_active = False
        self.logger.info("Debug integration system shutdown")


class DebugSessionError(Exception):
    """Exception raised during debug session operations"""
    pass


# Example usage and testing
async def demo_debug_integration():
    """Demonstrate debug integration capabilities"""
    print(" AIOS Debug Integration System Demo")
    print("=" * 50)

    # Mock dependencies for demo
    class MockFractalAI:
        async def get_current_state(self):
            return {"coherence": 0.85, "learning_state": {"patterns": 42}}

        async def restore_state(self, state):
            print(f"    Restoring fractal AI state: {state}")

        async def integrate_learning(self, learning):
            print(f"    Integrating debug learning: {learning}")

    class MockHolographicSync:
        async def get_sync_state(self):
            return {"components": 5, "sync_health": 0.92}

        async def restore_sync_state(self, state):
            print(f"    Restoring holographic sync: {state}")

        async def update_context(self, key, value):
            print(f"    Context update: {key} = {value}")

    class MockContextRecovery:
        async def check_context_health(self):
            return {"score": 0.88, "healthy": True}

        async def get_recovery_state(self):
            return {"recovery_points": 3, "health": "good"}

    # Initialize debug integration
    debug_system = DebugIntegrationSystem(
        MockFractalAI(),
        MockHolographicSync(),
        MockContextRecovery()
    )

    try:
        # Demo 1: Start debug session
        print("\n Demo 1: Starting Debug Session")
        session = await debug_system.start_debug_session(
            "context_persistence_ui",
            "Investigating context loss in UI component",
            DebugSessionType.STANDARD
        )

        # Demo 2: Check status
        print("\n Demo 2: Debug Session Status")
        status = await debug_system.get_debug_session_status(session.id)
        print(f"Status: {json.dumps(status, indent=2)}")

        # Demo 3: Process debug commands
        print("\n Demo 3: Processing Debug Commands")
        commands = [
            "Save debug context for memory leak investigation",
            "Start debugging the fractal synchronization module",
            "Debug status",
            "Complete debug session with findings: memory optimization needed"
        ]

        for command in commands:
            print(f"\nCommand: '{command}'")
            result = await debug_system.process_debug_command(command)
            print(f"Result: {json.dumps(result, indent=2)}")

        # Demo 4: Complete session
        print("\n Demo 4: Completing Debug Session")
        findings = [
            "Context loss occurs during UI refresh",
            "Memory leak in holographic display component",
            "Fractal coherence drops during high-frequency updates"
        ]

        recovery = await debug_system.complete_debug_session(
            session.id, findings, restore_context=True
        )

        print(f"Recovery result: {recovery.success}")
        print(f"Steps executed: {recovery.steps_executed}")

        print("\n Debug Integration Demo Complete!")

    finally:
        debug_system.shutdown()


if __name__ == "__main__":
    asyncio.run(demo_debug_integration())
