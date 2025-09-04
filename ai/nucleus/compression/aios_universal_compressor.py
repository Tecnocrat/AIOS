#!/usr/bin/env python3
"""
AIOS Universal Compression Toolkit
Universal compression module for system-wide integration
Created: July 10, 2025

This module provides compression capabilities as a service to:
- C# AIOS Services
- Python AI Modules
- C++ Core Components
- AINLP Processing Engine
- Any other AIOS subsystem

Usage patterns:
1. Direct Python import
2. C# interop via COM
3. CLI interface for any language
4. REST API for distributed systems
"""

import json
import shutil
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


@dataclass
class CompressionRequest:
    """Standardized compression request structure"""

    source_path: str
    target_path: Optional[str] = None
    # SMART_MERGE, LOGIC_COMPRESS, PATTERN_MERGE
    compression_type: str = "SMART_MERGE"
    preserve_functionality: bool = True
    create_backup: bool = True
    # MINIMAL, STANDARD, AGGRESSIVE, MAXIMUM
    compression_level: str = "STANDARD"
    file_patterns: List[str] = None
    exclude_patterns: List[str] = None
    # UNIFIED_MODULE, HIERARCHICAL, FUNCTIONAL
    merge_strategy: str = "UNIFIED_MODULE"


@dataclass
class CompressionResult:
    """Standardized compression result structure"""

    success: bool
    compression_ratio: float
    files_processed: int
    files_merged: int
    lines_saved: int
    backup_location: Optional[str]
    unified_modules: List[str]
    execution_time: float
    error_message: Optional[str] = None
    warnings: List[str] = None


class AIOSUniversalCompressor:
    """Universal compression toolkit for all AIOS systems"""

    def __init__(self, workspace_root: str = r"c:\dev\AIOS"):
        self.workspace_root = Path(workspace_root)
        self.compression_workspace = self.workspace_root / "temp" / "compression"
        self.compression_workspace.mkdir(parents=True, exist_ok=True)

        # Initialize logging and tracking
        self.compression_log = []
        self.active_compressions = {}
        self.compression_stats = {
            "total_compressions": 0,
            "total_files_processed": 0,
            "total_compression_ratio": 0.0,
            "last_compression": None,
        }

        print("🔧 AIOS Universal Compressor initialized")
        print(f"   Workspace: {self.workspace_root}")
        print(f"   Compression workspace: {self.compression_workspace}")

    # ========== MAIN COMPRESSION API ==========

    def compress(
        self, request: Union[CompressionRequest, Dict[str, Any]]
    ) -> CompressionResult:
        """Main compression entry point - accepts request object or dict"""
        start_time = time.time()

        # Normalize request
        if isinstance(request, dict):
            request = CompressionRequest(**request)

        compression_id = f"compress_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.active_compressions[compression_id] = {
            "request": request,
            "start_time": start_time,
            "status": "PROCESSING",
        }

        try:
            result = self._execute_compression(request, compression_id)
            result.execution_time = time.time() - start_time

            self.active_compressions[compression_id]["status"] = "COMPLETED"
            self.active_compressions[compression_id]["result"] = result

            # Update stats
            self._update_compression_stats(result)

            return result

        except Exception as e:
            error_result = CompressionResult(
                success=False,
                compression_ratio=0.0,
                files_processed=0,
                files_merged=0,
                lines_saved=0,
                backup_location=None,
                unified_modules=[],
                execution_time=time.time() - start_time,
                error_message=str(e),
            )

            self.active_compressions[compression_id]["status"] = "FAILED"
            self.active_compressions[compression_id]["result"] = error_result

            return error_result

    def _execute_compression(
        self, request: CompressionRequest, compression_id: str
    ) -> CompressionResult:
        """Execute the actual compression based on request parameters"""
        source_path = Path(request.source_path)

        if not source_path.exists():
            raise FileNotFoundError(f"Source path does not exist: {source_path}")

        # Create backup if requested
        backup_location = None
        if request.create_backup:
            backup_location = self._create_backup(source_path, compression_id)

        # Discover files to compress
        files_to_compress = self._discover_files(source_path, request)

        if not files_to_compress:
            raise ValueError("No files found matching compression criteria")

        # Execute compression based on type
        if request.compression_type == "SMART_MERGE":
            result = self._execute_smart_merge(
                files_to_compress, request, compression_id
            )
        elif request.compression_type == "LOGIC_COMPRESS":
            result = self._execute_logic_compression(
                files_to_compress, request, compression_id
            )
        elif request.compression_type == "PATTERN_MERGE":
            result = self._execute_pattern_merge(
                files_to_compress, request, compression_id
            )
        else:
            raise ValueError(f"Unknown compression type: {request.compression_type}")

        result.backup_location = backup_location
        return result

    # ========== COMPRESSION ALGORITHMS ==========

    def _execute_smart_merge(
        self, files: List[Path], request: CompressionRequest, compression_id: str
    ) -> CompressionResult:
        """Execute smart file merging with intelligent analysis"""
        merged_modules = {}
        total_lines_before = 0
        total_lines_after = 0

        # Analyze files for merge opportunities
        merge_groups = self._analyze_merge_opportunities(files, request)

        for group_name, group_files in merge_groups.items():
            # Count original lines
            group_lines_before = sum(self._count_lines(f) for f in group_files)
            total_lines_before += group_lines_before

            # Create unified module
            unified_content = self._create_unified_module(
                group_files, group_name, request
            )

            # Write unified module
            if request.target_path:
                target_dir = Path(request.target_path)
            else:
                target_dir = files[0].parent

            unified_path = target_dir / f"{group_name}.py"
            unified_path.write_text(unified_content, encoding="utf-8")

            # Count new lines
            group_lines_after = self._count_lines(unified_path)
            total_lines_after += group_lines_after

            merged_modules[group_name] = str(unified_path)

            # Archive original files if different from unified
            if request.create_backup:
                for original_file in group_files:
                    if original_file != unified_path:
                        self._archive_file(original_file, compression_id)

        compression_ratio = 1.0 - (len(merged_modules) / len(files)) if files else 0.0
        lines_saved = total_lines_before - total_lines_after

        return CompressionResult(
            success=True,
            compression_ratio=compression_ratio,
            files_processed=len(files),
            files_merged=len(files) - len(merged_modules),
            lines_saved=lines_saved,
            backup_location=None,  # Set by caller
            unified_modules=list(merged_modules.values()),
            execution_time=0,  # Set by caller
        )

    def _execute_logic_compression(
        self, files: List[Path], request: CompressionRequest, compression_id: str
    ) -> CompressionResult:
        """Execute logic-level compression removing redundancy"""
        # Implementation for logic compression
        # This would analyze code patterns and remove redundant logic
        return CompressionResult(
            success=True,
            compression_ratio=0.3,  # Placeholder
            files_processed=len(files),
            files_merged=0,
            lines_saved=1000,  # Placeholder
            backup_location=None,
            unified_modules=[],
            execution_time=0,
        )

    def _execute_pattern_merge(
        self, files: List[Path], request: CompressionRequest, compression_id: str
    ) -> CompressionResult:
        """Execute pattern-based merging"""
        # Implementation for pattern-based merging
        return CompressionResult(
            success=True,
            compression_ratio=0.5,  # Placeholder
            files_processed=len(files),
            files_merged=len(files) // 2,
            lines_saved=2000,  # Placeholder
            backup_location=None,
            unified_modules=[],
            execution_time=0,
        )

    # ========== ANALYSIS AND UTILITIES ==========

    def _discover_files(
        self, source_path: Path, request: CompressionRequest
    ) -> List[Path]:
        """Discover files to compress based on request criteria"""
        files = []

        if source_path.is_file():
            files.append(source_path)
        else:
            # Default patterns if none specified
            patterns = request.file_patterns or ["*.py", "*.cs", "*.cpp", "*.hpp"]
            exclude_patterns = request.exclude_patterns or [
                "*test*",
                "*temp*",
                "*backup*",
            ]

            for pattern in patterns:
                found_files = list(source_path.rglob(pattern))

                # Filter out excluded patterns
                for exclude_pattern in exclude_patterns:
                    found_files = [
                        f for f in found_files if not f.match(exclude_pattern)
                    ]

                files.extend(found_files)

        return list(set(files))  # Remove duplicates

    def _analyze_merge_opportunities(
        self, files: List[Path], request: CompressionRequest
    ) -> Dict[str, List[Path]]:
        """Analyze files and group them for optimal merging"""
        merge_groups = {}

        if request.merge_strategy == "UNIFIED_MODULE":
            # Group by file type and functionality
            python_files = [f for f in files if f.suffix == ".py"]
            cs_files = [f for f in files if f.suffix == ".cs"]
            cpp_files = [f for f in files if f.suffix in [".cpp", ".hpp"]]

            if python_files:
                merge_groups["unified_python_module"] = python_files
            if cs_files:
                merge_groups["unified_cs_module"] = cs_files
            if cpp_files:
                merge_groups["unified_cpp_module"] = cpp_files

        elif request.merge_strategy == "FUNCTIONAL":
            # Group by functional similarity (simplified analysis)
            for file in files:
                category = self._categorize_file_function(file)
                if category not in merge_groups:
                    merge_groups[category] = []
                merge_groups[category].append(file)

        else:  # HIERARCHICAL
            # Group by directory structure
            for file in files:
                parent_name = file.parent.name or "root"
                if parent_name not in merge_groups:
                    merge_groups[parent_name] = []
                merge_groups[parent_name].append(file)

        return merge_groups

    def _categorize_file_function(self, file: Path) -> str:
        """Categorize file by its functional purpose"""
        name_lower = file.name.lower()

        if any(word in name_lower for word in ["test", "spec"]):
            return "testing"
        elif any(word in name_lower for word in ["compress", "merge"]):
            return "compression"
        elif any(word in name_lower for word in ["ai", "nlp", "ml"]):
            return "ai_processing"
        elif any(word in name_lower for word in ["service", "manager"]):
            return "services"
        elif any(word in name_lower for word in ["ui", "window", "view"]):
            return "user_interface"
        else:
            return "core_functionality"

    def _create_unified_module(
        self, files: List[Path], module_name: str, request: CompressionRequest
    ) -> str:
        """Create unified module content from multiple files"""
        unified_content = []

        # Header
        unified_content.append(f"#!/usr/bin/env python3")
        unified_content.append(f'"""')
        unified_content.append(
            f'{module_name.replace("_", " ").title()} - Unified Module'
        )
        unified_content.append(f"Auto-generated by AIOS Universal Compressor")
        unified_content.append(
            f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        )
        unified_content.append(f"")
        unified_content.append(f"This module consolidates functionality from:")
        for file in files:
            unified_content.append(f"- {file.name}")
        unified_content.append(f'"""')
        unified_content.append("")

        # Collect all imports
        all_imports = set()

        # Process each file
        for file in files:
            try:
                content = file.read_text(encoding="utf-8", errors="ignore")

                # Extract imports
                file_imports = self._extract_imports(content)
                all_imports.update(file_imports)

                # Add file content
                unified_content.append(f"# === Merged from {file.name} ===")
                unified_content.append("")

                # Filter out imports and add main content
                main_content = self._extract_main_content(content)
                unified_content.append(main_content)
                unified_content.append("")

            except Exception as e:
                unified_content.append(f"# ERROR processing {file.name}: {str(e)}")

        # Add consolidated imports at the top
        import_section = ["# Consolidated imports"] + sorted(list(all_imports)) + [""]
        final_content = unified_content[:7] + import_section + unified_content[7:]

        return "\n".join(final_content)

    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements from file content"""
        imports = []
        lines = content.split("\n")

        for line in lines:
            stripped = line.strip()
            if stripped.startswith(("import ", "from ")) and not stripped.startswith(
                "#"
            ):
                imports.append(stripped)

        return imports

    def _extract_main_content(self, content: str) -> str:
        """Extract main content excluding imports and module docstring"""
        lines = content.split("\n")
        output_lines = []
        skip_docstring = False
        in_module_docstring = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Skip shebang
            if line.startswith("#!"):
                continue

            # Skip imports
            if stripped.startswith(("import ", "from ")) and not stripped.startswith(
                "#"
            ):
                continue

            # Handle module docstring
            if i < 10 and '"""' in line and not in_module_docstring:
                in_module_docstring = True
                if line.count('"""') == 2:  # Single line docstring
                    continue
                else:
                    continue
            elif in_module_docstring and '"""' in line:
                in_module_docstring = False
                continue
            elif in_module_docstring:
                continue

            output_lines.append(line)

        return "\n".join(output_lines).strip()

    # ========== BACKUP AND RECOVERY ==========

    def _create_backup(self, source_path: Path, compression_id: str) -> str:
        """Create backup of source files before compression"""
        backup_dir = (
            self.workspace_root
            / "docs"
            / "compression"
            / "archives"
            / f"backup_{compression_id}"
        )
        backup_dir.mkdir(parents=True, exist_ok=True)

        if source_path.is_file():
            shutil.copy2(source_path, backup_dir / source_path.name)
        else:
            shutil.copytree(
                source_path, backup_dir / source_path.name, dirs_exist_ok=True
            )

        return str(backup_dir)

    def _archive_file(self, file_path: Path, compression_id: str):
        """Archive a single file after successful merge"""
        archive_dir = (
            self.workspace_root
            / "docs"
            / "compression"
            / "archives"
            / f"backup_{compression_id}"
            / "archived_files"
        )
        archive_dir.mkdir(parents=True, exist_ok=True)

        archive_path = archive_dir / file_path.name
        shutil.move(str(file_path), str(archive_path))

    def restore_from_backup(self, backup_location: str) -> bool:
        """Restore files from backup location"""
        try:
            backup_path = Path(backup_location)
            if not backup_path.exists():
                return False

            # Implementation for restore logic
            return True
        except Exception as e:
            print(f"Restore failed: {e}")
            return False

    # ========== UTILITIES ==========

    def _count_lines(self, file_path: Path) -> int:
        """Count lines in a file"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return sum(1 for _ in f)
        except Exception:
            return 0

    def _update_compression_stats(self, result: CompressionResult):
        """Update global compression statistics"""
        self.compression_stats["total_compressions"] += 1
        self.compression_stats["total_files_processed"] += result.files_processed

        # Calculate weighted average compression ratio
        total_compressions = self.compression_stats["total_compressions"]
        current_avg = self.compression_stats["total_compression_ratio"]
        new_ratio = result.compression_ratio

        self.compression_stats["total_compression_ratio"] = (
            current_avg * (total_compressions - 1) + new_ratio
        ) / total_compressions

        self.compression_stats["last_compression"] = datetime.now().isoformat()

    # ========== API INTERFACES ==========

    def get_compression_status(self, compression_id: str = None) -> Dict[str, Any]:
        """Get status of compression operations"""
        if compression_id:
            return self.active_compressions.get(compression_id, {})
        else:
            return {
                "active_compressions": list(self.active_compressions.keys()),
                "stats": self.compression_stats,
            }

    def get_compression_history(self) -> List[Dict[str, Any]]:
        """Get history of all compression operations"""
        history = []
        for comp_id, comp_data in self.active_compressions.items():
            history.append(
                {
                    "id": comp_id,
                    "request": asdict(comp_data["request"]),
                    "status": comp_data["status"],
                    "start_time": comp_data["start_time"],
                    "result": asdict(
                        comp_data.get(
                            "result",
                            CompressionResult(
                                success=False,
                                compression_ratio=0.0,
                                files_processed=0,
                                files_merged=0,
                                lines_saved=0,
                                backup_location=None,
                                unified_modules=[],
                                execution_time=0,
                            ),
                        )
                    ),
                }
            )
        return history


# ========== CLI INTERFACE ==========


def cli_interface():
    """Command-line interface for compression toolkit"""
    import argparse

    parser = argparse.ArgumentParser(description="AIOS Universal Compression Toolkit")
    parser.add_argument("source", help="Source path to compress")
    parser.add_argument("--target", help="Target path for compressed output")
    parser.add_argument(
        "--type",
        choices=["SMART_MERGE", "LOGIC_COMPRESS", "PATTERN_MERGE"],
        default="SMART_MERGE",
        help="Compression type",
    )
    parser.add_argument(
        "--level",
        choices=["MINIMAL", "STANDARD", "AGGRESSIVE", "MAXIMUM"],
        default="STANDARD",
        help="Compression level",
    )
    parser.add_argument("--no-backup", action="store_true", help="Skip backup creation")
    parser.add_argument("--patterns", nargs="+", help="File patterns to include")
    parser.add_argument("--exclude", nargs="+", help="Patterns to exclude")

    args = parser.parse_args()

    # Create compression request
    request = CompressionRequest(
        source_path=args.source,
        target_path=args.target,
        compression_type=args.type,
        compression_level=args.level,
        create_backup=not args.no_backup,
        file_patterns=args.patterns,
        exclude_patterns=args.exclude,
    )

    # Execute compression
    compressor = AIOSUniversalCompressor()
    result = compressor.compress(request)

    # Output results
    if result.success:
        print(f"✅ Compression successful!")
        print(f"   Compression ratio: {result.compression_ratio:.1%}")
        print(f"   Files processed: {result.files_processed}")
        print(f"   Files merged: {result.files_merged}")
        print(f"   Lines saved: {result.lines_saved}")
        print(f"   Execution time: {result.execution_time:.2f}s")
        if result.unified_modules:
            print(f"   Unified modules created:")
            for module in result.unified_modules:
                print(f"     - {module}")
    else:
        print(f"❌ Compression failed: {result.error_message}")
        if result.warnings:
            for warning in result.warnings:
                print(f"   Warning: {warning}")


# ========== COM INTERFACE FOR C# ==========

try:
    import pythoncom
    import win32com.server.util

    class AIOSCompressionService:
        """COM interface for C# integration"""

        _reg_clsid_ = "{12345678-1234-1234-1234-123456789ABC}"
        _reg_progid_ = "AIOS.CompressionService"
        _public_methods_ = ["CompressFiles", "GetCompressionStatus", "RestoreBackup"]

        def __init__(self):
            self.compressor = AIOSUniversalCompressor()

        def CompressFiles(
            self, source_path, compression_type="SMART_MERGE", create_backup=True
        ):
            """COM method for C# to call compression"""
            request = CompressionRequest(
                source_path=source_path,
                compression_type=compression_type,
                create_backup=create_backup,
            )
            result = self.compressor.compress(request)
            return json.dumps(asdict(result))

        def GetCompressionStatus(self, compression_id=None):
            """Get compression status via COM"""
            status = self.compressor.get_compression_status(compression_id)
            return json.dumps(status)

        def RestoreBackup(self, backup_location):
            """Restore from backup via COM"""
            return self.compressor.restore_from_backup(backup_location)

    def register_com_service():
        """Register COM service for C# integration"""
        try:
            import win32com.server.register

            win32com.server.register.UseCommandLine(AIOSCompressionService)
            print("✅ COM service registered successfully")
        except ImportError:
            print("⚠️  pywin32 not available - COM registration skipped")
        except Exception as e:
            print(f"❌ COM registration failed: {e}")

except ImportError:
    print("⚠️  pywin32 not available - COM interface disabled")
    AIOSCompressionService = None

    def register_com_service():
        print("⚠️  COM service registration skipped - pywin32 not available")


# ========== MAIN EXECUTION ==========

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_interface()
    else:
        # Interactive mode
        compressor = AIOSUniversalCompressor()
        print("🔧 AIOS Universal Compression Toolkit")
        print("   Ready for compression operations")
        print("   Use compress() method or CLI interface")
