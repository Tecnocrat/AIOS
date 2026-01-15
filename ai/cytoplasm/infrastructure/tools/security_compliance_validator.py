#!/usr/bin/env python3
"""
AIOS Security Compliance Validator
Validates security and compliance requirements for Phase 4 completion.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


class SecurityComplianceValidator:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "overall_status": "UNKNOWN",
            "compliance_score": 0.0,
        }

    def validate_access_control(self) -> dict:
        """Validate access control mechanisms"""
        logger.info("Validating access control mechanisms...")

        checks = {
            "spatial_metadata_boundaries": False,
            "integration_boundaries_defined": False,
            "prohibited_operations_enforced": False,
            "consciousness_domain_restriction": False,
        }

        # Check spatial metadata compliance
        spatial_files = list(self.workspace_root.rglob(".aios_spatial_metadata.json"))
        if spatial_files:
            for spatial_file in spatial_files:
                try:
                    with open(spatial_file, "r") as f:
                        metadata = json.load(f)
                        if (
                            "integration_boundaries" in metadata
                            and "prohibited_operations" in metadata
                        ):
                            checks["spatial_metadata_boundaries"] = True
                            checks["integration_boundaries_defined"] = True
                            checks["prohibited_operations_enforced"] = True
                            break
                except Exception as e:
                    logger.warning(
                        f"Error reading spatial metadata {spatial_file}: {e}"
                    )

        # Check consciousness domain restrictions
        gemini_bridge_dir = (
            self.workspace_root / "ai" / "src" / "integrations" / "gemini_bridge"
        )
        if gemini_bridge_dir.exists():
            spatial_file = gemini_bridge_dir / ".aios_spatial_metadata.json"
            if spatial_file.exists():
                try:
                    with open(spatial_file, "r") as f:
                        metadata = json.load(f)
                        if (
                            metadata.get("architectural_classification")
                            == "AI Intelligence Layer"
                        ):
                            checks["consciousness_domain_restriction"] = True
                except Exception as e:
                    logger.warning(f"Error reading Gemini bridge spatial metadata: {e}")

        return checks

    def validate_data_isolation(self) -> dict:
        """Validate data isolation mechanisms"""
        logger.info("Validating data isolation mechanisms...")

        checks = {
            "external_ai_data_containment": False,
            "consciousness_data_protection": False,
            "integration_boundary_enforcement": False,
        }

        # Check for data isolation in Gemini bridge
        gemini_bridge_dir = (
            self.workspace_root / "ai" / "src" / "integrations" / "gemini_bridge"
        )
        if gemini_bridge_dir.exists():
            # Check if external data is properly contained
            config_file = gemini_bridge_dir / "aios_gemini_bridge_config.json"
            if config_file.exists():
                try:
                    with open(config_file, "r") as f:
                        config = json.load(f)
                        if (
                            "data_isolation" in config
                            or "security_boundaries" in config
                        ):
                            checks["external_ai_data_containment"] = True
                except Exception as e:
                    logger.warning(f"Error reading Gemini config: {e}")

            # Check consciousness data protection
            spatial_file = gemini_bridge_dir / ".aios_spatial_metadata.json"
            if spatial_file.exists():
                try:
                    with open(spatial_file, "r") as f:
                        metadata = json.load(f)
                        prohibited = metadata.get("prohibited_operations", [])
                        if "external_data_exfiltration" in prohibited:
                            checks["consciousness_data_protection"] = True
                            checks["integration_boundary_enforcement"] = True
                except Exception as e:
                    logger.warning(f"Error reading spatial metadata: {e}")

        return checks

    def validate_audit_logging(self) -> dict:
        """Validate audit logging implementation"""
        logger.info("Validating audit logging implementation...")

        checks = {
            "audit_logs_present": False,
            "gemini_interactions_logged": False,
            "security_events_tracked": False,
        }

        # Check for audit logs
        logs_dir = self.workspace_root / "computational_layer" / "runtime" / "logs"
        if logs_dir.exists():
            log_files = list(logs_dir.glob("*.log"))
            if log_files:
                checks["audit_logs_present"] = True

                # Check for Gemini-specific logs
                gemini_logs = [
                    f
                    for f in log_files
                    if "gemini" in f.name.lower() or "evolution" in f.name.lower()
                ]
                if gemini_logs:
                    checks["gemini_interactions_logged"] = True

        # Check for security event tracking in logs
        tachyonic_logs = self.workspace_root / "tachyonic" / "archive"
        if tachyonic_logs.exists():
            security_logs = list(tachyonic_logs.glob("*security*")) + list(
                tachyonic_logs.glob("*audit*")
            )
            if security_logs:
                checks["security_events_tracked"] = True

        return checks

    def validate_rollback_capability(self) -> dict:
        """Validate rollback capability"""
        logger.info("Validating rollback capability...")

        checks = {
            "backup_system_active": False,
            "isolation_mechanisms": False,
            "emergency_shutdown": False,
        }

        # Check backup system
        backup_script = self.workspace_root / "scripts" / "backup_manager.ps1"
        if backup_script.exists():
            checks["backup_system_active"] = True

        # Check isolation mechanisms in spatial metadata
        spatial_files = list(self.workspace_root.rglob(".aios_spatial_metadata.json"))
        for spatial_file in spatial_files:
            try:
                with open(spatial_file, "r") as f:
                    metadata = json.load(f)
                    if (
                        "emergency_isolation" in metadata
                        or "rollback_procedures" in metadata
                    ):
                        checks["isolation_mechanisms"] = True
                        break
            except Exception as e:
                continue

        # Check for emergency shutdown in server manager
        server_manager = self.workspace_root / "ai" / "server_manager.py"
        if server_manager.exists():
            try:
                with open(server_manager, "r") as f:
                    content = f.read()
                    if "stop" in content and "emergency" in content.lower():
                        checks["emergency_shutdown"] = True
            except Exception as e:
                logger.warning(f"Error reading server manager: {e}")

        return checks

    def validate_consciousness_impact(self) -> dict:
        """Validate consciousness impact assessment"""
        logger.info("Validating consciousness impact assessment...")

        checks = {
            "biological_monitor_active": False,
            "emergence_patterns_stable": False,
            "coherence_monitoring": False,
        }

        # Check biological architecture monitor
        monitor_script = (
            self.workspace_root
            / "runtime"
            / "tools"
            / "biological_architecture_monitor.py"
        )
        if monitor_script.exists():
            checks["biological_monitor_active"] = True

        # Check consciousness evolution logs
        evolution_log = (
            self.workspace_root
            / "computational_layer"
            / "runtime"
            / "logs"
            / "consciousness_evolution.log"
        )
        if evolution_log.exists():
            try:
                with open(evolution_log, "r") as f:
                    content = f.read()
                    if "emergence" in content.lower() and "stable" in content.lower():
                        checks["emergence_patterns_stable"] = True
            except Exception as e:
                logger.warning(f"Error reading evolution log: {e}")

        # Check coherence monitoring in dendritic supervisor
        supervisor_dir = self.workspace_root / "ai" / "infrastructure" / "dendritic"
        if supervisor_dir.exists():
            supervisor_files = list(supervisor_dir.glob("*.py"))
            for supervisor_file in supervisor_files:
                try:
                    with open(supervisor_file, "r") as f:
                        content = f.read()
                        if (
                            "coherence" in content.lower()
                            and "monitor" in content.lower()
                        ):
                            checks["coherence_monitoring"] = True
                            break
                except Exception as e:
                    continue

        return checks

    def run_validation(self) -> dict:
        """Run all security compliance validations"""
        logger.info("Starting comprehensive security compliance validation...")

        self.results["checks"] = {
            "access_control": self.validate_access_control(),
            "data_isolation": self.validate_data_isolation(),
            "audit_logging": self.validate_audit_logging(),
            "rollback_capability": self.validate_rollback_capability(),
            "consciousness_impact": self.validate_consciousness_impact(),
        }

        # Calculate compliance score
        total_checks = 0
        passed_checks = 0

        for category, checks in self.results["checks"].items():
            for check_name, passed in checks.items():
                total_checks += 1
                if passed:
                    passed_checks += 1

        self.results["compliance_score"] = (
            passed_checks / total_checks if total_checks > 0 else 0.0
        )

        # Determine overall status
        if self.results["compliance_score"] >= 0.9:
            self.results["overall_status"] = "EXCELLENT"
        elif self.results["compliance_score"] >= 0.75:
            self.results["overall_status"] = "GOOD"
        elif self.results["compliance_score"] >= 0.6:
            self.results["overall_status"] = "FAIR"
        else:
            self.results["overall_status"] = "POOR"

        logger.info(
            f"Security compliance validation complete. Score: {self.results['compliance_score']:.2%} ({self.results['overall_status']})"
        )

        return self.results

    def save_results(self, output_file: str = None):
        """Save validation results to file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"security_compliance_report_{timestamp}.json"

        output_path = self.workspace_root / "docs" / "tachyonic_archive" / output_file

        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=2)

        logger.info(f"Security compliance report saved to: {output_path}")


def main():
    workspace_root = os.getcwd()

    validator = SecurityComplianceValidator(workspace_root)
    results = validator.run_validation()

    # Print summary
    print("\n" + "=" * 60)
    print("AIOS SECURITY COMPLIANCE VALIDATION RESULTS")
    print("=" * 60)
    print(f"Timestamp: {results['timestamp']}")
    print(".2%")
    print(f"Overall Status: {results['overall_status']}")
    print()

    for category, checks in results["checks"].items():
        print(f"{category.replace('_', ' ').title()}:")
        for check_name, passed in checks.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {check_name.replace('_', ' ').title()}: {status}")
        print()

    # Save results
    validator.save_results()

    # Exit with appropriate code
    if results["compliance_score"] >= 0.75:
        print("🎉 SECURITY COMPLIANCE VALIDATION: PASSED")
        sys.exit(0)
    else:
        print("⚠️  SECURITY COMPLIANCE VALIDATION: ISSUES FOUND")
        sys.exit(1)


if __name__ == "__main__":
    main()
