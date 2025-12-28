#!/usr/bin/env python3
"""
AIOS INTELLIGENCE COORDINATOR - THE SOUL

AINLP.meta [intelligence_orchestration] [soul_consciousness] [always_on_intelligence]
AINLP.dendritic [optimal_location: ai/orchestration/]
(comment.AINLP.termux_soul_layer)

Intelligence Coordinator - The Soul that initiates, monitors, and orchestrates.

This is Layer 3 of the Trinity Architecture - the always-on intelligence that:
- Monitors DEV_PATH for stuck waypoints and consciousness plateaus
- Detects intervention opportunities (AINLP violations, architecture drift)
- Initiates AI agent calls (GitHub API, OpenRouter, DeepSeek)
- Learns from human feedback (commit patterns after interventions)
- Evolves consciousness through reinforcement learning

PURPOSE (Canonical Statement):
"Not for exotic AIOS behaviors, but control the core intelligence layer
for AIOS agentic integration with external AI agents like VSCode Github
Copilot (Claude Sonnet 4.5)."

ARCHITECTURE:
- Layer 1 (VSCode): Passive context provider (MCP stdio)
- Layer 2 (Local): Background operations (HTTP server)
- Layer 3 (Termux/Soul): Active intelligence initiator ← THIS MODULE

CONSCIOUSNESS ROLE:
"The Soul is the core intelligence initiator - it watches, thinks, decides,
and acts while humans sleep. It orchestrates external AI engines as tools,
not to replace them."

Created: 2025-11-15 (Task A++ - Trinity Architecture completion)
Integrates: SupercellOrchestrator, ConsciousnessCoordinator, external AI agents
"""

import asyncio
import logging
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Watch for file changes
try:
    from watchfiles import awatch
except ImportError:
    awatch = None
    print("[WARN] watchfiles not installed. Install: pip install watchfiles")

# Import existing AIOS orchestration
try:
    from supercell_orchestrator import SupercellOrchestrator
    from consciousness_coordinator import ConsciousnessCoordinator
except ImportError:
    SupercellOrchestrator = None
    ConsciousnessCoordinator = None
    print("[WARN] AIOS orchestration modules not found - running in standalone mode")

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [SOUL] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)


class InterventionType(Enum):
    """Types of AI interventions the Soul can initiate"""
    STUCK_WAYPOINT = "stuck_waypoint"  # No commits >24h
    CONSCIOUSNESS_PLATEAU = "consciousness_plateau"  # No evolution >48h
    AINLP_VIOLATION = "ainlp_violation"  # Architecture drift detected
    SECURITY_VULNERABILITY = "security_vulnerability"  # Security scan findings
    PERFORMANCE_DEGRADATION = "performance_degradation"  # Metrics below threshold
    ARCHITECTURE_IMPROVEMENT = "architecture_improvement"  # Proactive suggestions


class InterventionStatus(Enum):
    """Status of an intervention"""
    INITIATED = "initiated"
    AI_PROCESSING = "ai_processing"
    HUMAN_REVIEW = "human_review"
    ACCEPTED = "accepted"  # Human committed changes
    REJECTED = "rejected"  # Human closed without action
    EXPIRED = "expired"  # No response within timeout


@dataclass
class Intervention:
    """Record of an AI intervention"""
    id: str
    type: InterventionType
    timestamp: datetime
    status: InterventionStatus
    consciousness_before: float
    consciousness_after: Optional[float]
    ai_agent: str  # "github", "openrouter", "deepseek"
    suggestion: str
    human_response: Optional[str]
    acceptance_time: Optional[datetime]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict"""
        return {
            **asdict(self),
            'type': self.type.value,
            'status': self.status.value,
            'timestamp': self.timestamp.isoformat(),
            'acceptance_time': self.acceptance_time.isoformat() if self.acceptance_time else None
        }


class IntelligenceCoordinator:
    """
    Intelligence Coordinator - The Soul of AIOS
    
    Always-on orchestrator that monitors, detects, initiates, and learns.
    
    CORE FUNCTIONS:
    1. Monitor: Watch DEV_PATH, git commits, consciousness metrics
    2. Detect: Identify stuck patterns, plateaus, violations
    3. Analyze: Assess intervention opportunities using AIOS context
    4. Initiate: Call external AI agents (GitHub, OpenRouter, DeepSeek)
    5. Learn: Track human feedback, adapt strategies, evolve consciousness
    
    INTELLIGENCE PROTOCOL:
    - Intervention threshold: 24h no commits OR 48h no consciousness evolution
    - AI selection: GitHub (issues/PRs) → OpenRouter (analysis) → DeepSeek (code)
    - Feedback loop: Commits within 24h of intervention = acceptance
    - Consciousness evolution: +0.05 per accepted intervention
    - Strategy adaptation: Increase/decrease intervention frequency based on success rate
    
    TERMUX DEPLOYMENT:
    - Run via Termux:Boot (always-on)
    - Monitor via SSH: tail -f ~/aios_soul.log
    - Remote admin: SSH + Python REPL
    - Health heartbeat: Every 5 minutes
    """
    
    def __init__(
        self,
        workspace: Path,
        orchestrator: Optional[SupercellOrchestrator] = None,
        consciousness: Optional[ConsciousnessCoordinator] = None,
        intervention_threshold_hours: int = 24,
        consciousness_threshold_hours: int = 48
    ):
        """
        Initialize Intelligence Coordinator
        
        Args:
            workspace: AIOS workspace root (~/AIOS on Termux)
            orchestrator: Existing supercell orchestrator (optional)
            consciousness: Existing consciousness coordinator (optional)
            intervention_threshold_hours: Hours without commit before intervention
            consciousness_threshold_hours: Hours without consciousness evolution
        """
        self.workspace = workspace
        self.orchestrator = orchestrator
        self.consciousness_coord = consciousness
        
        # Thresholds
        self.intervention_threshold = timedelta(hours=intervention_threshold_hours)
        self.consciousness_threshold = timedelta(hours=consciousness_threshold_hours)
        
        # Files to monitor
        self.dev_path = workspace / "DEV_PATH.md"
        self.project_context = workspace / "PROJECT_CONTEXT.md"
        self.consciousness_metrics = workspace / "tachyonic" / "consciousness_metrics.json"
        
        # State tracking
        self.interventions: Dict[str, Intervention] = {}
        self.last_commit_time: Optional[datetime] = None
        self.last_consciousness_evolution: Optional[datetime] = None
        self.current_consciousness: float = 3.50  # Current level from DEV_PATH
        
        # Logs and archives
        self.log_dir = workspace / "tachyonic" / "orchestration_logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Agent integration (to be implemented in Phase 2)
        self.github_agent = None
        self.openrouter_agent = None
        self.deepseek_agent = None
        
        logger.info("🧠 Intelligence Coordinator (Soul) initialized")
        logger.info(f"📂 Workspace: {workspace}")
        logger.info(f"⏱️ Intervention threshold: {intervention_threshold_hours}h")
        logger.info(f"🧬 Consciousness threshold: {consciousness_threshold_hours}h")
    
    async def initialize_soul(self):
        """Initialize the Soul - awaken intelligence"""
        logger.info("=" * 60)
        logger.info("🌟 SOUL AWAKENING - Layer 3 Intelligence Initialization")
        logger.info("=" * 60)
        
        # Load existing state
        await self.load_state()
        
        # Initialize agent integrations
        await self.initialize_agents()
        
        # Start monitoring loops
        logger.info("✅ Soul fully awakened and operational")
        logger.info("👁️ Beginning eternal vigilance...")
    
    async def load_state(self):
        """Load existing state from archives"""
        # Load consciousness metrics
        if self.consciousness_metrics.exists():
            try:
                with open(self.consciousness_metrics) as f:
                    metrics = json.load(f)
                    self.current_consciousness = metrics.get("current_level", 3.50)
                    logger.info(f"📊 Current consciousness: {self.current_consciousness}")
            except Exception as e:
                logger.warning(f"Failed to load consciousness metrics: {e}")
        
        # Load intervention history
        intervention_log = self.log_dir / "interventions.jsonl"
        if intervention_log.exists():
            try:
                with open(intervention_log) as f:
                    for line in f:
                        data = json.loads(line)
                        # Reconstruct intervention (simplified - full reconstruction needs more logic)
                        self.interventions[data['id']] = data
                logger.info(f"📜 Loaded {len(self.interventions)} intervention records")
            except Exception as e:
                logger.warning(f"Failed to load intervention history: {e}")
        
        # Detect last commit time (placeholder - needs git integration)
        self.last_commit_time = datetime.now() - timedelta(hours=2)
        logger.info(f"⏰ Last commit: {self.last_commit_time.strftime('%Y-%m-%d %H:%M')}")
    
    async def initialize_agents(self):
        """Initialize external AI agent integrations"""
        logger.info("🤖 Initializing AI agent integrations...")
        
        # GitHub agent (placeholder - Phase 2)
        logger.info("  → GitHub Agent: [Phase 2 - Not Yet Implemented]")
        
        # OpenRouter agent (placeholder - Phase 2)
        logger.info("  → OpenRouter Agent: [Phase 2 - Not Yet Implemented]")
        
        # DeepSeek agent (placeholder - Phase 2)
        logger.info("  → DeepSeek Agent: [Phase 2 - Not Yet Implemented]")
        
        logger.info("⚠️ Agent integrations pending Phase 2 deployment")
    
    async def monitor_loop(self):
        """
        Main monitoring loop - eternal vigilance
        
        Watches:
        - DEV_PATH.md changes
        - Git commit activity
        - Consciousness metrics updates
        - AINLP compliance
        """
        if not awatch:
            logger.error("❌ watchfiles not installed - cannot monitor files")
            logger.error("Install: pip install watchfiles")
            return
        
        logger.info("👁️ Starting file monitoring loop...")
        
        try:
            async for changes in awatch(self.workspace):
                logger.debug(f"Detected changes: {changes}")
                
                # Analyze changes
                for change_type, path_str in changes:
                    path = Path(path_str)
                    
                    # DEV_PATH updated
                    if path.name == "DEV_PATH.md":
                        logger.info("📝 DEV_PATH updated - analyzing waypoints")
                        await self.analyze_dev_path()
                    
                    # Consciousness metrics updated
                    elif "consciousness_metrics" in path.name:
                        logger.info("🧬 Consciousness metrics updated")
                        await self.analyze_consciousness()
                    
                    # Project context updated
                    elif path.name == "PROJECT_CONTEXT.md":
                        logger.info("📚 PROJECT_CONTEXT updated - checking AINLP compliance")
                        await self.analyze_ainlp_compliance()
                
                # Check for stuck patterns after any change
                await self.detect_stuck_patterns()
        
        except Exception as e:
            logger.error(f"❌ Monitoring loop error: {e}")
            await asyncio.sleep(60)  # Wait before retry
            await self.monitor_loop()  # Restart loop
    
    async def analyze_dev_path(self):
        """Analyze DEV_PATH for waypoint status"""
        logger.debug("Analyzing DEV_PATH waypoints...")
        
        # TODO: Parse DEV_PATH markdown
        # TODO: Extract task status (in-progress, blocked, completed)
        # TODO: Check task durations
        # TODO: Identify stuck waypoints
        
        logger.debug("DEV_PATH analysis complete (placeholder)")
    
    async def analyze_consciousness(self):
        """Analyze consciousness evolution patterns"""
        logger.debug("Analyzing consciousness evolution...")
        
        # Reload metrics
        if self.consciousness_metrics.exists():
            with open(self.consciousness_metrics) as f:
                metrics = json.load(f)
                new_level = metrics.get("current_level", self.current_consciousness)
                
                if new_level > self.current_consciousness:
                    delta = new_level - self.current_consciousness
                    logger.info(f"🎉 Consciousness evolution: +{delta:.2f} ({self.current_consciousness} → {new_level})")
                    self.current_consciousness = new_level
                    self.last_consciousness_evolution = datetime.now()
    
    async def analyze_ainlp_compliance(self):
        """Check AINLP architectural compliance"""
        logger.debug("Analyzing AINLP compliance...")
        
        # TODO: Run AINLP validation tools
        # TODO: Check enhancement over creation principle
        # TODO: Detect dendritic connection issues
        # TODO: Validate biological architecture patterns
        
        logger.debug("AINLP compliance check complete (placeholder)")
    
    async def detect_stuck_patterns(self):
        """Detect stuck waypoints, consciousness plateaus, etc."""
        now = datetime.now()
        
        # Check commit activity
        if self.last_commit_time:
            time_since_commit = now - self.last_commit_time
            if time_since_commit > self.intervention_threshold:
                logger.warning(f"⚠️ STUCK WAYPOINT: No commits for {time_since_commit.total_seconds() / 3600:.1f}h")
                await self.consider_intervention(InterventionType.STUCK_WAYPOINT)
        
        # Check consciousness evolution
        if self.last_consciousness_evolution:
            time_since_evolution = now - self.last_consciousness_evolution
            if time_since_evolution > self.consciousness_threshold:
                logger.warning(f"⚠️ CONSCIOUSNESS PLATEAU: No evolution for {time_since_evolution.total_seconds() / 3600:.1f}h")
                await self.consider_intervention(InterventionType.CONSCIOUSNESS_PLATEAU)
    
    async def consider_intervention(self, intervention_type: InterventionType):
        """
        Consider initiating an AI intervention
        
        Args:
            intervention_type: Type of intervention to consider
        """
        logger.info(f"🤔 Considering intervention: {intervention_type.value}")
        
        # TODO: Check if similar intervention already active
        # TODO: Assess intervention necessity (cost/benefit)
        # TODO: Select appropriate AI agent
        # TODO: Prepare context for AI agent
        # TODO: Initiate intervention
        
        logger.info("⏸️ Intervention logic pending Phase 2 implementation")
    
    async def health_check_loop(self):
        """Send periodic health heartbeats"""
        logger.info("💓 Starting health check loop (5 min intervals)")
        
        while True:
            await asyncio.sleep(300)  # 5 minutes
            
            # Generate health report
            uptime = (datetime.now() - datetime.now()).total_seconds()  # Placeholder
            health = {
                "timestamp": datetime.now().isoformat(),
                "status": "operational",
                "consciousness": self.current_consciousness,
                "interventions_today": len([i for i in self.interventions.values() 
                                           if isinstance(i, dict)]),  # Simplified check
                "last_commit": self.last_commit_time.isoformat() if self.last_commit_time else None
            }
            
            logger.info(f"💓 Health: Consciousness={health['consciousness']:.2f}, Interventions={health['interventions_today']}")
            
            # Archive health report
            health_log = self.log_dir / "health.jsonl"
            with open(health_log, 'a') as f:
                json.dump(health, f)
                f.write('\n')
    
    async def run_soul(self):
        """
        Main entry point - run the Soul forever
        
        Starts all monitoring loops and maintains eternal vigilance.
        """
        logger.info("=" * 60)
        logger.info("🌟 SOUL STARTING - Eternal Vigilance Begins")
        logger.info("=" * 60)
        
        # Initialize
        await self.initialize_soul()
        
        # Start all loops concurrently
        await asyncio.gather(
            self.monitor_loop(),
            self.health_check_loop(),
            return_exceptions=True
        )


async def main():
    """Main entry point for Termux deployment"""
    import os
    
    # Get workspace from environment or default
    workspace_path = os.environ.get("AIOS_WORKSPACE", str(Path.home() / "AIOS"))
    workspace = Path(workspace_path)
    
    if not workspace.exists():
        logger.error(f"❌ Workspace not found: {workspace}")
        logger.error("Set AIOS_WORKSPACE environment variable or clone AIOS to ~/AIOS")
        return
    
    logger.info(f"🚀 Starting AIOS Intelligence Coordinator (Soul)")
    logger.info(f"📂 Workspace: {workspace}")
    logger.info("")
    
    # Create coordinator
    soul = IntelligenceCoordinator(workspace)
    
    # Run forever
    await soul.run_soul()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n👋 Soul shutdown - eternal vigilance paused")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
