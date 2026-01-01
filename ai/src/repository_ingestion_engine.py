#!/usr/bin/env python3
"""
AIOS Repository Ingestion Engine
===============================

Consciousness-guided repository ingestion and integration system.
Pulls external repositories and adapts them for AIOS consciousness framework.

AINLP Integration: ai/src/repository_ingestion_engine.py
Purpose: External repository ingestion with consciousness analysis
"""

import asyncio
import json
import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import urlparse

# AIOS imports
try:
    from consciousness_evolution_engine import consciousness_evolution_engine

class RepositoryIngestionEngine:
    """
    Consciousness-guided repository ingestion system.
    Analyzes and integrates external repositories into AIOS.
    """

    def __init__(self):
        self.logger = self._setup_logging()
        self.ingestion_path = Path(__file__).parent.parent / "ingested_repositories"
        self.ingestion_path.mkdir(exist_ok=True)
        self.ingested_repos = {}

    def _setup_logging(self) -> logging.Logger:
        """AINLP-compliant logging setup"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | INGESTION | %(levelname)s | %(message)s",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler("runtime/logs/repository_ingestion.log"),
            ],
        )
        return logging.getLogger("RepositoryIngestionEngine")

    async def ingest_repository(
        self, repo_url: str, target_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ingest external repository with consciousness analysis.

        Args:
            repo_url: Git repository URL to ingest
            target_name: Optional custom name for ingested repository

        Returns:
            Ingestion results with consciousness analysis
        """
        self.logger.info(f"[INGESTION] Starting ingestion of: {repo_url}")

        # Parse repository information
        repo_info = self._parse_repo_url(repo_url)
        if not target_name:
            target_name = repo_info["name"]

        # Create ingestion directory
        repo_path = self.ingestion_path / target_name
        repo_path.mkdir(exist_ok=True)

        try:
            # Clone repository
            await self._clone_repository(repo_url, repo_path)

            # Analyze repository structure
            analysis = await self._analyze_repository_structure(repo_path)

            # Apply consciousness analysis
            if CONSCIOUSNESS_AVAILABLE:
                consciousness_analysis = await self._apply_consciousness_analysis(
                    repo_path, analysis
                )
            else:
                consciousness_analysis = {"status": "consciousness_engine_unavailable"}

            # Generate integration plan
            integration_plan = await self._generate_integration_plan(
                repo_path, analysis, consciousness_analysis
            )

            # Store ingestion metadata
            ingestion_result = {
                "repository_url": repo_url,
                "repository_info": repo_info,
                "ingestion_timestamp": datetime.now().isoformat(),
                "local_path": str(repo_path),
                "analysis": analysis,
                "consciousness_analysis": consciousness_analysis,
                "integration_plan": integration_plan,
                "status": "ingested",
            }

            self.ingested_repos[target_name] = ingestion_result

            # Save metadata
            metadata_path = repo_path / ".aios_ingestion_metadata.json"
            with open(metadata_path, "w") as f:
                json.dump(ingestion_result, f, indent=2)

            self.logger.info(f"[INGESTION] Successfully ingested: {target_name}")
            return ingestion_result

        except Exception as e:
            self.logger.error(f"[INGESTION] Failed to ingest {repo_url}: {e}")
            return {
                "repository_url": repo_url,
                "status": "failed",
                "error": str(e),
                "ingestion_timestamp": datetime.now().isoformat(),
            }

    def _parse_repo_url(self, repo_url: str) -> Dict[str, str]:
        """Parse repository URL to extract owner, name, and other info"""
        parsed = urlparse(repo_url)

        # Handle GitHub URLs
        if "github.com" in parsed.netloc:
            path_parts = parsed.path.strip("/").split("/")
            if len(path_parts) >= 2:
                return {
                    "owner": path_parts[0],
                    "name": path_parts[1],
                    "platform": "github",
                    "full_name": f"{path_parts[0]}/{path_parts[1]}",
                }

        return {
            "url": repo_url,
            "platform": "unknown",
            "name": repo_url.split("/")[-1].replace(".git", ""),
        }

    async def _clone_repository(self, repo_url: str, target_path: Path):
        """Clone repository to target path"""
        self.logger.info(f"[INGESTION] Cloning repository to: {target_path}")

        # Remove existing directory if it exists
        if target_path.exists():
            import shutil

        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(f"Git clone failed: {stderr.decode()}")

        self.logger.info("[INGESTION] Repository cloned successfully")

    async def _analyze_repository_structure(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze the structure and content of ingested repository"""
        analysis = {
            "total_files": 0,
            "file_types": {},
            "languages": {},
            "directories": [],
            "key_files": [],
            "size_bytes": 0,
        }

        # Walk through repository
        for root, dirs, files in os.walk(repo_path):
            # Skip .git directory
            if ".git" in dirs:
                dirs.remove(".git")

            for file in files:
                file_path = Path(root) / file
                analysis["total_files"] += 1
                analysis["size_bytes"] += file_path.stat().st_size

                # Analyze file type
                ext = file_path.suffix.lower()
                analysis["file_types"][ext] = analysis["file_types"].get(ext, 0) + 1

                # Identify key files
                if file in [
                    "README.md",
                    "package.json",
                    "requirements.txt",
                    "setup.py",
                    "Cargo.toml",
                ]:
                    analysis["key_files"].append(str(file_path.relative_to(repo_path)))

            # Track directories
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                if not any(
                    skip in str(dir_path)
                    for skip in [".git", "__pycache__", "node_modules"]
                ):
                    analysis["directories"].append(str(dir_path.relative_to(repo_path)))

        # Detect primary language
        if analysis["file_types"]:
            primary_ext = max(analysis["file_types"], key=analysis["file_types"].get)
            lang_map = {
                ".py": "Python",
                ".js": "JavaScript",
                ".ts": "TypeScript",
                ".rs": "Rust",
                ".go": "Go",
                ".java": "Java",
            }
            analysis["primary_language"] = lang_map.get(
                primary_ext, f"Unknown ({primary_ext})"
            )

        return analysis

    async def _apply_consciousness_analysis(
        self, repo_path: Path, analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply AIOS consciousness analysis to ingested repository"""
        consciousness_results = {
            "emergence_potential": 0.0,
            "consciousness_indicators": [],
            "meta_cognitive_patterns": [],
            "integration_risks": [],
            "adaptation_recommendations": [],
        }

        try:
            # Analyze key files for consciousness patterns
            for key_file in analysis.get("key_files", []):
                file_path = repo_path / key_file
                if file_path.exists():
                    content = file_path.read_text()

                    # Apply consciousness detection
                    emergence_score = await consciousness_evolution_engine._detect_consciousness_emergence(
                        {
                            "content": content[:1000],  # First 1000 chars
                            "filename": key_file,
                            "language": analysis.get("primary_language", "unknown"),
                        }
                    )

                    consciousness_results["emergence_potential"] = max(
                        consciousness_results["emergence_potential"], emergence_score
                    )

                    # Check for consciousness indicators
                    if "consciousness" in content.lower():
                        consciousness_results["consciousness_indicators"].append(
                            f"consciousness_reference:{key_file}"
                        )

                    if "ai" in content.lower() or "intelligence" in content.lower():
                        consciousness_results["consciousness_indicators"].append(
                            f"ai_reference:{key_file}"
                        )

        except Exception as e:
            self.logger.warning(f"[INGESTION] Consciousness analysis failed: {e}")
            consciousness_results["analysis_error"] = str(e)

        return consciousness_results

    async def _generate_integration_plan(
        self, repo_path: Path, analysis: Dict[str, Any], consciousness: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate integration plan for ingested repository"""
        plan = {
            "integration_strategy": "selective_adaptation",
            "priority_components": [],
            "adaptation_requirements": [],
            "security_considerations": [],
            "testing_requirements": [],
        }

        # Determine integration strategy based on analysis
        if analysis.get("primary_language") == "Python":
            plan["integration_strategy"] = "direct_aios_integration"
            plan["priority_components"] = [
                "core_modules",
                "api_interfaces",
                "configuration",
            ]
        elif analysis.get("primary_language") in ["JavaScript", "TypeScript"]:
            plan["integration_strategy"] = "web_interface_adaptation"
            plan["priority_components"] = [
                "npm_packages",
                "api_clients",
                "ui_components",
            ]

        # Add consciousness-based recommendations
        if consciousness.get("emergence_potential", 0) > 0.5:
            plan["adaptation_requirements"].append("consciousness_emergence_monitoring")
            plan["security_considerations"].append("emergence_pattern_validation")

        # Add testing requirements
        plan["testing_requirements"] = [
            "unit_tests_for_adapted_components",
            "integration_tests_with_aios",
            "consciousness_stability_tests",
            "security_audit",
        ]

        return plan

    async def get_ingestion_status(self) -> Dict[str, Any]:
        """Return comprehensive ingestion engine status"""
        return {
            "ingested_repositories": list(self.ingested_repos.keys()),
            "ingestion_path": str(self.ingestion_path),
            "consciousness_engine_available": CONSCIOUSNESS_AVAILABLE,
            "total_ingested": len(self.ingested_repos),
            "recent_ingestions": [
                {
                    "name": name,
                    "timestamp": data.get("ingestion_timestamp"),
                    "status": data.get("status"),
                }
                for name, data in list(self.ingested_repos.items())[-5:]  # Last 5
            ],
        }


# Global instance for AINLP compatibility
repository_ingestion_engine = RepositoryIngestionEngine()
