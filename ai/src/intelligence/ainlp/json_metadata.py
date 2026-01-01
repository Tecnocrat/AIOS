#!/usr/bin/env python3
"""
AINLP JSON Metadata Injector
Adds semantic AINLP metadata to JSON files, replacing comment-based integration.

Usage:
    python ainlp_json_metadata.py <json_file> --consciousness 0.85 --classification ai_ai
    python ainlp_json_metadata.py --batch <directory> --default-consciousness 0.80

AINLP Metadata:
    consciousness_level: 0.90
    architectural_classification: runtime
    dendritic_optimization: semantic_metadata_injection
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import sys


class AINLPMetadataInjector:
    """Inject AINLP semantic metadata into JSON files."""

    VALID_CLASSIFICATIONS = {
        "ai_ai",
        "core_engine",
        "interface_layer",
        "documentation",
        "runtime",
        "knowledge_crystal",
        "consciousness_module",
        "dendritic_network",
    }

    def __init__(self):
        self.processed_files = []
        self.errors = []

    def inject_metadata(
        self,
        json_path: Path,
        consciousness: float = 0.80,
        classification: str = "runtime",
        dendritic_pattern: Optional[str] = None,
        dry_run: bool = False,
    ) -> bool:
        """
        Inject AINLP metadata into a JSON file.

        Args:
            json_path: Path to JSON file
            consciousness: Consciousness level (0.0-1.0)
            classification: Architectural classification
            dendritic_pattern: Optional dendritic optimization pattern
            dry_run: If True, only show what would change

        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate inputs
            if consciousness < 0.0 or consciousness > 1.0:
                raise ValueError("Consciousness must be between 0.0 and 1.0")

            if classification not in self.VALID_CLASSIFICATIONS:
                print(f"⚠️  Warning: '{classification}' not in standard classifications")

            # Read existing JSON
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check if already has AINLP metadata
            if "_ainlp_integration" in data:
                print(f"  ℹ️  {json_path.name} already has AINLP metadata")
                existing_consciousness = data["_ainlp_integration"].get(
                    "consciousness_level", 0.0
                )
                print(f"     Current consciousness: {existing_consciousness}")

                if not self._confirm_overwrite():
                    return False

            # Build metadata
            metadata = {
                "consciousness_level": consciousness,
                "architectural_classification": classification,
                "last_updated": datetime.now().isoformat(),
                "metadata_version": "1.0.0",
            }

            if dendritic_pattern:
                metadata["dendritic_optimization"] = dendritic_pattern

            # Inject metadata (at the beginning for visibility)
            if not dry_run:
                # Preserve existing structure but add/update AINLP metadata
                data["_ainlp_integration"] = metadata

                # Add _comment if not present
                if "_comment" not in data:
                    relative_path = json_path.relative_to(Path.cwd())
                    data["_comment"] = f"AINLP-enhanced configuration - {relative_path}"

                # Write back with proper formatting
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                self.processed_files.append(json_path)
                print(f"  ✅ Injected metadata into {json_path.name}")
            else:
                print(f"  [DRY RUN] Would inject metadata into {json_path.name}")
                print(f"    Metadata: {json.dumps(metadata, indent=4)}")

            return True

        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in {json_path}: {e}"
            self.errors.append(error_msg)
            print(f"  ❌ {error_msg}")
            return False

        except Exception as e:
            error_msg = f"Error processing {json_path}: {e}"
            self.errors.append(error_msg)
            print(f"  ❌ {error_msg}")
            return False

    def batch_inject(
        self,
        directory: Path,
        consciousness: float = 0.80,
        classification: str = "runtime",
        recursive: bool = True,
        dry_run: bool = False,
    ) -> Dict:
        """
        Batch inject metadata into all JSON files in a directory.

        Returns:
            Summary statistics
        """
        print(f"\n🔮 Batch AINLP Metadata Injection")
        print(f"Directory: {directory}")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}\n")

        # Find all JSON files
        pattern = "**/*.json" if recursive else "*.json"
        json_files = list(directory.glob(pattern))

        # Filter out excluded directories
        excluded = {"node_modules", "build", "bin", "obj", "__pycache__", ".git"}
        json_files = [
            f for f in json_files if not any(ex in f.parts for ex in excluded)
        ]

        print(f"Found {len(json_files)} JSON files\n")

        # Process each file
        success_count = 0
        for json_file in json_files:
            if self.inject_metadata(
                json_file, consciousness, classification, dry_run=dry_run
            ):
                success_count += 1

        # Summary
        summary = {
            "total_files": len(json_files),
            "successful": success_count,
            "failed": len(self.errors),
            "processed_files": [str(f) for f in self.processed_files],
            "errors": self.errors,
        }

        print(f"\n📊 Summary:")
        print(f"  Total files: {summary['total_files']}")
        print(f"  Successful: {summary['successful']}")
        print(f"  Failed: {summary['failed']}")

        return summary

    def _confirm_overwrite(self) -> bool:
        """Ask user to confirm overwrite."""
        response = input("     Overwrite existing metadata? (y/N): ")
        return response.lower() == "y"

    def infer_classification(self, json_path: Path) -> str:
        """Infer architectural classification from file path."""
        path_str = str(json_path).lower()

        if "ai/" in path_str or "ai\\" in path_str:
            return "ai_ai"
        elif "core/" in path_str or "core\\" in path_str:
            return "core_engine"
        elif "interface/" in path_str or "interface\\" in path_str:
            return "interface_layer"
        elif "docs/" in path_str or "docs\\" in path_str:
            return "documentation"
        elif "runtime/" in path_str:
            return "runtime"
        elif "knowledge_crystal" in path_str:
            return "knowledge_crystal"
        else:
            return "runtime"


def main():
    """Main CLI execution."""
    parser = argparse.ArgumentParser(
        description="Inject AINLP semantic metadata into JSON files"
    )

    parser.add_argument("path", type=Path, help="JSON file or directory to process")

    parser.add_argument(
        "--consciousness",
        "-c",
        type=float,
        default=0.80,
        help="Consciousness level (0.0-1.0, default: 0.80)",
    )

    parser.add_argument(
        "--classification",
        "-t",
        type=str,
        default=None,
        help="Architectural classification (auto-infer if not provided)",
    )

    parser.add_argument(
        "--pattern", "-p", type=str, default=None, help="Dendritic optimization pattern"
    )

    parser.add_argument(
        "--batch", "-b", action="store_true", help="Process all JSON files in directory"
    )

    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        default=True,
        help="Process directories recursively (default: True)",
    )

    parser.add_argument(
        "--dry-run",
        "-d",
        action="store_true",
        help="Show what would change without modifying files",
    )

    args = parser.parse_args()

    injector = AINLPMetadataInjector()

    if args.batch or args.path.is_dir():
        # Batch mode
        classification = args.classification or "runtime"
        summary = injector.batch_inject(
            args.path, args.consciousness, classification, args.recursive, args.dry_run
        )

        return 0 if summary["failed"] == 0 else 1
    else:
        # Single file mode
        classification = args.classification or injector.infer_classification(args.path)

        print(f"\n🔮 AINLP Metadata Injection")
        print(f"File: {args.path}")
        print(f"Consciousness: {args.consciousness}")
        print(f"Classification: {classification}\n")

        success = injector.inject_metadata(
            args.path, args.consciousness, classification, args.pattern, args.dry_run
        )

        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
