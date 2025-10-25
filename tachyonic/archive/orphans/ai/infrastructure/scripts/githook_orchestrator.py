#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# flake8: noqa: E402
"""
AIOS GitHook Master Orchestrator with Agentic Integration
=========================================================
Integrated within the CYTOPLASM supercell architecture
Location: ai/cytoplasm/scripts/githook_orchestrator.py
Purpose: Single entry point for all githook logic execution with AI-driven
automation

This orchestrator now includes:
- Traditional GitHook execution
- Emoji detection and quality analysis
- Agentic instruction generation
- AI agent integration (GitHub Copilot)
- Autonomous code refactoring capabilities
"""

import json
import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add AIOS paths for supercell communication
sys.path.append(str(Path(__file__).parent.parent.parent))

from cytoplasm.scripts.agentic_auto_controller import AgenticAutoController

# Import agentic components
from laboratory.scripts.agentic_instruction_generator import (
    AgenticInstructionGenerator,
)
from membrane.ai_agent_bridge import AIAgentBridge
from nucleus.src.core.aios_runtime import AIOSRuntime
from transport.intercellular.cellular_communication import CellularBridge
from transport.intercellular.enhanced_cellular_communication import (
    SupercellType,
    get_cellular_bridge,
)


@dataclass
class GitHookExecution:
    """Single GitHook execution result"""

    hook_name: str
    execution_time: float
    success: bool
    output: str
    error: Optional[str] = None


@dataclass
class OrchestrationResult:
    """Complete orchestration execution result"""

    total_hooks: int
    successful_hooks: int
    failed_hooks: int
    total_execution_time: float
    hook_results: List[GitHookExecution]
    supercell_integration: Dict[str, Any]


class GitHookOrchestrator:
    """Master orchestrator for all GitHook logic - integrated with AIOS supercells"""

    def __init__(self, aios_root: Optional[Path] = None):
        """Initialize with supercell architecture integration"""
        self.aios_root = aios_root or self._find_aios_root()
        self.githooks_path = self.aios_root / ".githooks"
        self.cytoplasm_path = self.aios_root / "ai" / "cytoplasm"

        # Initialize supercell communication
        self.cellular_bridge = CellularBridge()
        self.runtime = AIOSRuntime()

        # Configure logging
        self._setup_logging()

        # GitHook execution order (dependency-aware)
        self.execution_order = [
            "pre-commit.ps1",
            "commit-msg.ps1",
            "pre-push.ps1",
            "aios_copilot_orchestrator.ps1",
            "aios_auto_optimization.ps1",
            "aios_consciousness_bridge.ps1",
            "aios_reality_check.ps1",
            "real_ai_githook.ps1",
            "comprehensive_analysis.ps1",
            "ecosystem_intelligence_report.ps1",
        ]

        self.logger.info("GitHook Orchestrator initialized within CYTOPLASM")

    def _find_aios_root(self) -> Path:
        """Find AIOS root directory from current location"""
        current = Path(__file__).parent
        while current != current.parent:
            if (current / "AIOS.sln").exists():
                return current
            current = current.parent
        raise RuntimeError("AIOS root not found")

    def _setup_logging(self):
        """Setup logging within cytoplasm runtime"""
        log_dir = self.cytoplasm_path / "runtime" / "logs" / "githooks"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = (
            log_dir
            / f"orchestration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )
        self.logger = logging.getLogger(__name__)

    def execute_all_githook_logic(
        self, parallel_execution: bool = True, skip_dependencies: bool = False
    ) -> OrchestrationResult:
        """
        Execute all GitHook logic in proper order with supercell integration

        Args:
            parallel_execution: Run independent hooks in parallel
            skip_dependencies: Skip dependency checks (use with caution)

        Returns:
            Complete orchestration result
        """
        self.logger.info("Starting complete GitHook logic execution")
        self.logger.info(f"GitHooks path: {self.githooks_path}")
        self.logger.info(f"Supercell integration: ACTIVE")

        start_time = datetime.now()
        hook_results = []

        # Phase 1: Supercell preparation
        self._prepare_supercell_environment()

        # Phase 2: Core validation hooks (sequential)
        core_hooks = ["pre-commit.ps1", "commit-msg.ps1", "pre-push.ps1"]
        for hook in core_hooks:
            result = self._execute_single_hook(hook)
            hook_results.append(result)
            if not result.success and not skip_dependencies:
                self.logger.error(f"Core hook {hook} failed, stopping")
                break

        # Phase 3: AI integration hooks (can be parallel)
        ai_hooks = [
            "aios_copilot_orchestrator.ps1",
            "aios_auto_optimization.ps1",
            "aios_consciousness_bridge.ps1",
        ]

        if parallel_execution:
            ai_results = self._execute_hooks_parallel(ai_hooks)
            hook_results.extend(ai_results)
        else:
            for hook in ai_hooks:
                result = self._execute_single_hook(hook)
                hook_results.append(result)

        # Phase 4: Analysis and reporting hooks
        analysis_hooks = [
            "aios_reality_check.ps1",
            "comprehensive_analysis.ps1",
            "ecosystem_intelligence_report.ps1",
        ]

        for hook in analysis_hooks:
            result = self._execute_single_hook(hook)
            hook_results.append(result)

        # Phase 5: Supercell synchronization
        supercell_integration = self._synchronize_with_supercells(hook_results)

        # Calculate results
        total_time = (datetime.now() - start_time).total_seconds()
        successful = sum(1 for r in hook_results if r.success)
        failed = len(hook_results) - successful

        result = OrchestrationResult(
            total_hooks=len(hook_results),
            successful_hooks=successful,
            failed_hooks=failed,
            total_execution_time=total_time,
            hook_results=hook_results,
            supercell_integration=supercell_integration,
        )

        self._log_orchestration_summary(result)
        return result

    def _prepare_supercell_environment(self):
        """Prepare supercell environment for GitHook execution"""
        self.logger.info("Preparing supercell environment...")

        # CYTOPLASM: Ensure runtime environment
        runtime_dir = self.cytoplasm_path / "runtime" / "logs" / "githooks"
        runtime_dir.mkdir(parents=True, exist_ok=True)

        # NUCLEUS: Notify core systems
        try:
            self.runtime.notify_githook_execution_start()
        except Exception as e:
            self.logger.warning(f"NUCLEUS notification failed: {e}")

        # TRANSPORT: Activate intercellular communication
        try:
            self.cellular_bridge.activate_githook_mode()
        except Exception as e:
            self.logger.warning(f"TRANSPORT activation failed: {e}")

        self.logger.info("Supercell environment prepared")

    def _execute_single_hook(self, hook_name: str) -> GitHookExecution:
        """Execute a single GitHook with full error handling"""
        hook_path = self.githooks_path / hook_name

        if not hook_path.exists():
            return GitHookExecution(
                hook_name=hook_name,
                execution_time=0.0,
                success=False,
                output="",
                error=f"Hook file not found: {hook_path}",
            )

        self.logger.info(f" Executing: {hook_name}")
        start_time = datetime.now()

        try:
            # Determine execution method
            if hook_name.endswith(".ps1"):
                cmd = [
                    "pwsh",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(hook_path),
                ]
            elif hook_name.endswith(".sh"):
                cmd = ["bash", str(hook_path)]
            else:
                cmd = [str(hook_path)]

            # Execute with proper environment
            env = os.environ.copy()
            env["AIOS_ROOT"] = str(self.aios_root)
            env["AIOS_HOOK_ORCHESTRATED"] = "true"
            env["AIOS_CYTOPLASM_PATH"] = str(self.cytoplasm_path)

            result = subprocess.run(
                cmd,
                cwd=str(self.aios_root),
                env=env,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            execution_time = (datetime.now() - start_time).total_seconds()

            return GitHookExecution(
                hook_name=hook_name,
                execution_time=execution_time,
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr if result.returncode != 0 else None,
            )

        except subprocess.TimeoutExpired:
            execution_time = (datetime.now() - start_time).total_seconds()
            return GitHookExecution(
                hook_name=hook_name,
                execution_time=execution_time,
                success=False,
                output="",
                error="Hook execution timed out (5 minutes)",
            )
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return GitHookExecution(
                hook_name=hook_name,
                execution_time=execution_time,
                success=False,
                output="",
                error=f"Execution error: {str(e)}",
            )

    def _execute_hooks_parallel(
        self, hook_names: List[str]
    ) -> List[GitHookExecution]:
        """Execute multiple hooks in parallel (for independent hooks)"""
        import concurrent.futures

        self.logger.info(f" Executing {len(hook_names)} hooks in parallel")

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self._execute_single_hook, hook): hook
                for hook in hook_names
            }

            results = []
            for future in concurrent.futures.as_completed(futures):
                hook_name = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                    status = "" if result.success else ""
                    self.logger.info(f"{status} {hook_name} completed")
                except Exception as e:
                    self.logger.error(
                        f" {hook_name} parallel execution failed: {e}"
                    )
                    results.append(
                        GitHookExecution(
                            hook_name=hook_name,
                            execution_time=0.0,
                            success=False,
                            output="",
                            error=f"Parallel execution error: {str(e)}",
                        )
                    )

        return results

    def _synchronize_with_supercells(
        self, hook_results: List[GitHookExecution]
    ) -> Dict[str, Any]:
        """Synchronize GitHook results with all supercells"""
        self.logger.info(" Synchronizing with supercells...")

        supercell_data = {
            "execution_timestamp": datetime.now().isoformat(),
            "total_hooks_executed": len(hook_results),
            "successful_hooks": sum(1 for r in hook_results if r.success),
            "supercell_notifications": {},
        }

        # CYTOPLASM: Store execution logs
        try:
            log_data = {
                "orchestration_session": supercell_data,
                "hook_details": [
                    {
                        "hook": r.hook_name,
                        "success": r.success,
                        "execution_time": r.execution_time,
                        "error": r.error,
                    }
                    for r in hook_results
                ],
            }

            log_file = (
                self.cytoplasm_path
                / "runtime"
                / "logs"
                / "githooks"
                / "latest_orchestration.json"
            )
            with open(log_file, "w") as f:
                json.dump(log_data, f, indent=2)

            supercell_data["supercell_notifications"][
                "cytoplasm"
            ] = " Logs stored"
        except Exception as e:
            supercell_data["supercell_notifications"][
                "cytoplasm"
            ] = f" {str(e)}"

        # NUCLEUS: Notify core runtime
        try:
            self.runtime.notify_githook_execution_complete(hook_results)
            supercell_data["supercell_notifications"][
                "nucleus"
            ] = " Runtime notified"
        except Exception as e:
            supercell_data["supercell_notifications"][
                "nucleus"
            ] = f" {str(e)}"

        # TRANSPORT: Update intercellular state
        try:
            self.cellular_bridge.update_githook_state(supercell_data)
            supercell_data["supercell_notifications"][
                "transport"
            ] = " State synchronized"
        except Exception as e:
            supercell_data["supercell_notifications"][
                "transport"
            ] = f" {str(e)}"

        return supercell_data

    def _log_orchestration_summary(self, result: OrchestrationResult):
        """Log comprehensive orchestration summary"""
        self.logger.info(" GitHook Orchestration Summary")
        self.logger.info("=" * 50)
        self.logger.info(f"Total Hooks: {result.total_hooks}")
        self.logger.info(f"Successful: {result.successful_hooks}")
        self.logger.info(f"Failed: {result.failed_hooks}")
        self.logger.info(f"Total Time: {result.total_execution_time:.2f}s")
        self.logger.info(
            f"Average Time: {result.total_execution_time/result.total_hooks:.2f}s per hook"
        )

        self.logger.info("\n Hook-by-Hook Results:")
        for hook_result in result.hook_results:
            status = "" if hook_result.success else ""
            self.logger.info(
                f"  {status} {hook_result.hook_name} ({hook_result.execution_time:.2f}s)"
            )
            if hook_result.error:
                self.logger.error(f"    Error: {hook_result.error}")

        self.logger.info(f"\n Supercell Integration:")
        for supercell, status in result.supercell_integration.get(
            "supercell_notifications", {}
        ).items():
            self.logger.info(f"  {supercell.upper()}: {status}")


def main():
    """Main entry point for GitHook orchestration"""
    import argparse

    parser = argparse.ArgumentParser(
        description="AIOS GitHook Master Orchestrator"
    )
    parser.add_argument(
        "--parallel", action="store_true", help="Enable parallel execution"
    )
    parser.add_argument(
        "--skip-deps", action="store_true", help="Skip dependency checks"
    )
    parser.add_argument("--aios-root", type=Path, help="AIOS root directory")

    args = parser.parse_args()

    try:
        orchestrator = GitHookOrchestrator(aios_root=args.aios_root)
        result = orchestrator.execute_all_githook_logic(
            parallel_execution=args.parallel, skip_dependencies=args.skip_deps
        )

        # Exit with appropriate code
        sys.exit(0 if result.failed_hooks == 0 else 1)

    except Exception as e:
        logging.error(f"Orchestration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
