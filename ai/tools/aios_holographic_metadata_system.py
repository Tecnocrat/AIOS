#!/usr/bin/env python3
"""
AIOS Holographic Metadata System
Distributed spatial awareness for AI agentic chat engines

Location: ai/tools/aios_holographic_metadata_system.py
Purpose: Generate holographic metadata files in each relevant folder to provide
         AI engines with perfect spatial awareness and context knowledge
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('HolographicMetadata')

class AIOSHolographicMetadataSystem:
    """
    Creates distributed holographic metadata across AIOS workspace
    Each folder gets its own spatial awareness metadata file
    """
    
    def __init__(self, workspace_root: Path = None):
        self.workspace_root = workspace_root or Path(__file__).parents[2]
        self.metadata_filename = ".aios_spatial_metadata.json"
        
        # Tachyonic archival pattern with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.holographic_index_file = (
            f"tachyonic/archive/aios_holographic_index_{timestamp}.json"
        )
        
        # Configuration for metadata generation
        self.metadata_config = {
            "include_hidden": False,
            "max_file_depth": 10,
            "include_file_hashes": True,
            "include_content_analysis": True,
            "spatial_awareness_level": "detailed",
            "consciousness_integration": True,
            "file_type_monitoring": True,
            "track_file_changes": True
        }
        
        # File type monitoring configuration - Runtime Intelligence paths
        self.file_type_history_file = (
            "runtime_intelligence/analysis/aios_file_type_history.json"
        )
        self.monitoring_config = {
            "track_extensions": True,
            "track_counts": True,
            "track_size_changes": True,
            "history_retention_days": 90,
            "significant_change_threshold": 0.05  # 5% change is significant
        }
        
        # File type categorization for AIOS consciousness
        self.file_categories = {
            "consciousness": [".py", ".ps1", ".cpp", ".cs", ".h", ".hpp"],
            "documentation": [".md", ".txt", ".rst", ".json", ".yaml", ".yml"],
            "configuration": [".json", ".yaml", ".yml", ".toml", ".ini", ".config"],
            "executable": [".exe", ".dll", ".so", ".bat", ".sh", ".ps1"],
            "archive": [".zip", ".tar", ".gz", ".7z", ".rar"],
            "temporary": [".tmp", ".temp", ".log", ".cache", ".bak"]
        }
        
        # AIOS architectural areas for spatial classification
        self.architectural_areas = {
            "githooks": ["GitHook Architecture", "Governance"],
            "ai": ["AI Intelligence Layer", "Consciousness"],
            "interface": ["Interface Layer", "UI Components"],
            "core": ["Core Engine", "System Foundation"],
            "docs": ["Documentation", "Knowledge Base"],
            "runtime_intelligence": ["Runtime Intelligence", "Monitoring"],
            "tachyonic": ["Tachyonic Archive", "Historical Data"],
            "visual_interface": ["Visual Interface", "User Experience"]
        }
        
        logger.info("🧠 AIOS Holographic Metadata System initialized")
        logger.info(f"📂 Workspace: {self.workspace_root}")
        logger.info(f"🗃️ Metadata file pattern: {self.metadata_filename}")
    
    def generate_folder_metadata(self, folder_path: Path) -> Dict[str, Any]:
        """Generate comprehensive metadata for a specific folder"""
        
        if not folder_path.exists() or not folder_path.is_dir():
            logger.warning(f"⚠️ Folder not found or not directory: {folder_path}")
            return {}
        
        logger.info(f"📊 Generating metadata for: {folder_path}")
        
        # Basic folder information
        relative_path = folder_path.relative_to(self.workspace_root)
        folder_name = folder_path.name
        
        # Safely calculate parent path relative to workspace
        try:
            parent_relative = folder_path.parent.relative_to(self.workspace_root)
            parent_path_str = str(parent_relative)
        except ValueError:
            # Parent is outside workspace (e.g., for root directory)
            parent_path_str = ""
        
        metadata = {
            "spatial_metadata_version": "1.0.0",
            "generation_timestamp": datetime.now().isoformat(),
            "folder_info": {
                "name": folder_name,
                "absolute_path": str(folder_path.absolute()),
                "relative_path": str(relative_path),
                "parent_path": str(folder_path.parent.relative_to(self.workspace_root)) if folder_path.parent != self.workspace_root else "",
                "depth_level": len(relative_path.parts)
            },
            "architectural_classification": self._classify_architectural_area(relative_path),
            "spatial_context": self._analyze_spatial_context(folder_path),
            "content_analysis": self._analyze_folder_contents(folder_path),
            "consciousness_metrics": self._calculate_consciousness_metrics(folder_path),
            "navigation_aids": self._generate_navigation_aids(folder_path),
            "ai_guidance": self._generate_ai_guidance(folder_path, relative_path)
        }
        
        return metadata
    
    def _classify_architectural_area(self, relative_path: Path) -> Dict[str, Any]:
        """Classify folder into AIOS architectural areas"""
        
        path_parts = relative_path.parts
        primary_area = "unknown"
        secondary_areas = []
        
        for part in path_parts:
            part_lower = part.lower()
            for area_key, area_info in self.architectural_areas.items():
                if area_key in part_lower or any(keyword.lower() in part_lower for keyword in area_info):
                    if primary_area == "unknown":
                        primary_area = area_info[0]
                    else:
                        secondary_areas.append(area_info[0])
        
        return {
            "primary_area": primary_area,
            "secondary_areas": list(set(secondary_areas)),
            "path_classification": list(path_parts),
            "consciousness_level": self._determine_consciousness_level(primary_area)
        }
    
    def _determine_consciousness_level(self, area: str) -> str:
        """Determine consciousness level based on architectural area"""
        consciousness_levels = {
            "AI Intelligence Layer": "high",
            "Consciousness": "highest",
            "GitHook Architecture": "high", 
            "Core Engine": "high",
            "Runtime Intelligence": "medium",
            "Interface Layer": "medium",
            "Documentation": "low",
            "unknown": "minimal"
        }
        return consciousness_levels.get(area, "minimal")
    
    def _analyze_spatial_context(self, folder_path: Path) -> Dict[str, Any]:
        """Analyze spatial relationships and context"""
        
        # Get immediate neighbors (siblings)
        siblings = []
        if folder_path.parent.exists():
            siblings = [p.name for p in folder_path.parent.iterdir() if p.is_dir() and p != folder_path]
        
        # Get children directories
        children = [p.name for p in folder_path.iterdir() if p.is_dir()] if folder_path.exists() else []
        
        # Calculate spatial metrics
        total_size = sum(f.stat().st_size for f in folder_path.rglob('*') if f.is_file()) if folder_path.exists() else 0
        file_count = len([f for f in folder_path.rglob('*') if f.is_file()]) if folder_path.exists() else 0
        
        return {
            "sibling_folders": sorted(siblings),
            "child_folders": sorted(children),
            "spatial_metrics": {
                "total_size_bytes": total_size,
                "file_count": file_count,
                "folder_count": len(children),
                "size_category": self._categorize_size(total_size)
            },
            "spatial_relationships": {
                "has_siblings": len(siblings) > 0,
                "has_children": len(children) > 0,
                "isolation_level": "isolated" if len(siblings) == 0 and len(children) == 0 else "connected"
            }
        }
    
    def _categorize_size(self, size_bytes: int) -> str:
        """Categorize folder size"""
        if size_bytes < 1024:
            return "tiny"
        elif size_bytes < 1024 * 1024:
            return "small" 
        elif size_bytes < 1024 * 1024 * 10:
            return "medium"
        elif size_bytes < 1024 * 1024 * 100:
            return "large"
        else:
            return "massive"
    
    def _analyze_folder_contents(self, folder_path: Path) -> Dict[str, Any]:
        """Analyze folder contents in detail"""
        
        if not folder_path.exists():
            return {"error": "Folder does not exist"}
        
        files_by_type = {}
        important_files = []
        recent_files = []
        
        try:
            for file_path in folder_path.iterdir():
                if file_path.is_file():
                    file_ext = file_path.suffix.lower()
                    file_info = {
                        "name": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                        "category": self._categorize_file_type(file_ext)
                    }
                    
                    # Group by extension
                    if file_ext not in files_by_type:
                        files_by_type[file_ext] = []
                    files_by_type[file_ext].append(file_info)
                    
                    # Mark important files
                    if self._is_important_file(file_path):
                        important_files.append(file_info)
                    
                    # Track recent files (last 30 days)
                    if (datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)).days < 30:
                        recent_files.append(file_info)
        
        except PermissionError:
            logger.warning(f"Permission denied accessing: {folder_path}")
            return {"error": "Permission denied"}
        
        return {
            "files_by_type": files_by_type,
            "important_files": important_files[:10],  # Top 10 important files
            "recent_files": sorted(recent_files, key=lambda x: x['modified'], reverse=True)[:10],
            "content_summary": {
                "total_files": len([f for f in folder_path.iterdir() if f.is_file()]),
                "file_types": list(files_by_type.keys()),
                "dominant_type": max(files_by_type.keys(), key=lambda k: len(files_by_type[k])) if files_by_type else None
            }
        }
    
    def _categorize_file_type(self, file_ext: str) -> str:
        """Categorize file by extension"""
        for category, extensions in self.file_categories.items():
            if file_ext in extensions:
                return category
        return "other"
    
    def _is_important_file(self, file_path: Path) -> bool:
        """Determine if file is important for AIOS context"""
        important_patterns = [
            "readme", "index", "main", "core", "aios", "consciousness", 
            "config", "setup", "init", "__init__", "package.json", 
            "requirements.txt", "cmakelists.txt", ".sln", ".csproj"
        ]
        
        file_name_lower = file_path.name.lower()
        return any(pattern in file_name_lower for pattern in important_patterns)
    
    def _calculate_consciousness_metrics(self, folder_path: Path) -> Dict[str, Any]:
        """Calculate AIOS consciousness metrics for the folder"""
        
        consciousness_indicators = {
            "ai_files": 0,
            "consciousness_files": 0,
            "agentic_files": 0,
            "intelligence_files": 0
        }
        
        consciousness_keywords = {
            "ai_files": ["ai", "artificial", "intelligence"],
            "consciousness_files": ["consciousness", "aware", "cognitive"],
            "agentic_files": ["agentic", "agent", "autonomous"],
            "intelligence_files": ["intelligence", "smart", "neural"]
        }
        
        if folder_path.exists():
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    file_name_lower = file_path.name.lower()
                    for indicator, keywords in consciousness_keywords.items():
                        if any(keyword in file_name_lower for keyword in keywords):
                            consciousness_indicators[indicator] += 1
        
        # Calculate consciousness score (0-100)
        total_files = sum(consciousness_indicators.values())
        consciousness_score = min(total_files * 10, 100) if total_files > 0 else 0
        
        return {
            "consciousness_indicators": consciousness_indicators,
            "consciousness_score": consciousness_score,
            "consciousness_level": "high" if consciousness_score > 50 else "medium" if consciousness_score > 20 else "low"
        }
    
    def _generate_navigation_aids(self, folder_path: Path) -> Dict[str, Any]:
        """Generate navigation aids for AI engines"""
        
        # Find key entry points
        entry_points = []
        config_files = []
        
        if folder_path.exists():
            for file_path in folder_path.iterdir():
                if file_path.is_file():
                    file_name = file_path.name.lower()
                    if any(pattern in file_name for pattern in ["main", "index", "entry", "__init__"]):
                        entry_points.append(file_path.name)
                    elif any(pattern in file_name for pattern in ["config", "settings", "setup"]):
                        config_files.append(file_path.name)
        
        # Generate relative path to workspace root
        try:
            relative_to_root = folder_path.relative_to(self.workspace_root)
            breadcrumb = " > ".join(relative_to_root.parts)
        except ValueError:
            breadcrumb = str(folder_path)
        
        return {
            "entry_points": entry_points,
            "config_files": config_files,
            "breadcrumb_path": breadcrumb,
            "quick_commands": {
                "list_files": f"Get-ChildItem '{folder_path}' -Recurse",
                "find_python": f"Get-ChildItem '{folder_path}' -Recurse -Filter '*.py'",
                "find_scripts": f"Get-ChildItem '{folder_path}' -Recurse -Filter '*.ps1'"
            }
        }
    
    def _generate_ai_guidance(self, folder_path: Path, relative_path: Path) -> Dict[str, Any]:
        """Generate specific AI guidance for this folder"""
        
        folder_name = folder_path.name.lower()
        path_parts = relative_path.parts
        
        # Generate context-aware guidance
        guidance = {
            "primary_focus": "General development",
            "recommended_actions": [],
            "important_considerations": [],
            "related_folders": []
        }
        
        # GitHook-specific guidance
        if "githooks" in str(relative_path).lower():
            guidance.update({
                "primary_focus": "GitHook governance and validation",
                "recommended_actions": [
                    "Review pre-commit.ps1 for validation logic",
                    "Check governance/hook_policy.json for policy alignment",
                    "Test GitHook functionality with sample commits"
                ],
                "important_considerations": [
                    "Maintain AINLP compliance in hook scripts",
                    "Ensure consciousness coherence in validation logic",
                    "Preserve governance effectiveness"
                ]
            })
        
        # AI-specific guidance
        elif "ai" in str(relative_path).lower():
            guidance.update({
                "primary_focus": "AI intelligence and consciousness",
                "recommended_actions": [
                    "Validate consciousness coherence across components",
                    "Test agentic auto-controller functionality",
                    "Review AINLP pattern compliance"
                ],
                "important_considerations": [
                    "Maintain consciousness architecture integrity",
                    "Ensure agentic pattern consistency",
                    "Preserve dendritic growth capabilities"
                ]
            })
        
        # Interface-specific guidance
        elif "interface" in str(relative_path).lower():
            guidance.update({
                "primary_focus": "User interface and experience",
                "recommended_actions": [
                    "Validate UI component consistency",
                    "Test user workflow integration",
                    "Check consciousness-UI bridge functionality"
                ]
            })
        
        # Find related folders
        for part in path_parts:
            related_pattern = part.lower()
            for folder in self.workspace_root.rglob('*'):
                if folder.is_dir() and related_pattern in folder.name.lower() and folder != folder_path:
                    try:
                        rel_path = folder.relative_to(self.workspace_root)
                        guidance["related_folders"].append(str(rel_path))
                        if len(guidance["related_folders"]) >= 5:  # Limit to 5 related folders
                            break
                    except ValueError:
                        continue
        
        return guidance
    
    def scan_workspace_file_types(self) -> Dict[str, Any]:
        """
        Comprehensive file type analysis across entire AIOS workspace
        Returns current file type distribution and statistics
        """
        logger.info("🔍 Scanning workspace file types...")
        
        file_stats = {}
        total_files = 0
        total_size = 0
        scan_start = datetime.now()
        
        # Track by extension, category, and architecture area
        by_extension = {}
        by_category = {}
        by_architecture = {}
        
        for file_path in self.workspace_root.rglob('*'):
            if not file_path.is_file():
                continue
                
            try:
                # Skip problematic paths
                if any(skip in str(file_path).lower() 
                       for skip in ['node_modules', '.git', '__pycache__', '.vs']):
                    continue
                    
                total_files += 1
                file_size = file_path.stat().st_size
                total_size += file_size
                
                # Get extension and category
                ext = file_path.suffix.lower()
                category = self._categorize_file_type(ext)
                
                # Determine architecture area
                relative_path = file_path.relative_to(self.workspace_root)
                arch_area = self._classify_architectural_area(relative_path)
                primary_area = arch_area.get('primary_area', 'unknown')
                
                # Count by extension
                if ext not in by_extension:
                    by_extension[ext] = {'count': 0, 'size': 0, 'files': []}
                by_extension[ext]['count'] += 1
                by_extension[ext]['size'] += file_size
                by_extension[ext]['files'].append(str(relative_path))
                
                # Count by category
                if category not in by_category:
                    by_category[category] = {'count': 0, 'size': 0}
                by_category[category]['count'] += 1
                by_category[category]['size'] += file_size
                
                # Count by architecture area
                if primary_area not in by_architecture:
                    by_architecture[primary_area] = {'count': 0, 'size': 0}
                by_architecture[primary_area]['count'] += 1
                by_architecture[primary_area]['size'] += file_size
                
            except (PermissionError, OSError) as e:
                logger.debug(f"⚠️ Skipping file {file_path}: {e}")
                continue
        
        scan_duration = (datetime.now() - scan_start).total_seconds()
        
        # Sort by count (descending)
        sorted_extensions = dict(sorted(by_extension.items(), 
                                      key=lambda x: x[1]['count'], reverse=True))
        sorted_categories = dict(sorted(by_category.items(), 
                                      key=lambda x: x[1]['count'], reverse=True))
        sorted_architecture = dict(sorted(by_architecture.items(), 
                                        key=lambda x: x[1]['count'], reverse=True))
        
        file_stats = {
            "scan_timestamp": datetime.now().isoformat(),
            "scan_duration_seconds": round(scan_duration, 2),
            "workspace_root": str(self.workspace_root),
            "summary": {
                "total_files": total_files,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "unique_extensions": len(by_extension),
                "file_categories": len(by_category),
                "architecture_areas": len(by_architecture)
            },
            "by_extension": sorted_extensions,
            "by_category": sorted_categories,
            "by_architecture": sorted_architecture,
            "top_extensions": dict(list(sorted_extensions.items())[:20]),
            "language_analysis": self._analyze_programming_languages(sorted_extensions)
        }
        
        logger.info(f"📊 File type scan complete: {total_files} files analyzed")
        return file_stats
    
    def _analyze_programming_languages(self, extensions_data: Dict) -> Dict[str, Any]:
        """Analyze programming language distribution"""
        
        language_map = {
            '.py': 'Python',
            '.cs': 'C#',
            '.cpp': 'C++',
            '.c': 'C',
            '.h': 'C/C++ Headers',
            '.hpp': 'C++ Headers',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.html': 'HTML',
            '.css': 'CSS',
            '.json': 'JSON',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.md': 'Markdown',
            '.xaml': 'XAML',
            '.ps1': 'PowerShell',
            '.sh': 'Shell Script',
            '.asm': 'Assembly',
            '.sql': 'SQL'
        }
        
        languages = {}
        total_code_files = 0
        
        for ext, data in extensions_data.items():
            if ext in language_map:
                lang = language_map[ext]
                if lang not in languages:
                    languages[lang] = {'count': 0, 'size': 0, 'extensions': []}
                languages[lang]['count'] += data['count']
                languages[lang]['size'] += data['size']
                languages[lang]['extensions'].append(ext)
                total_code_files += data['count']
        
        # Sort by count
        sorted_languages = dict(sorted(languages.items(), 
                                     key=lambda x: x[1]['count'], reverse=True))
        
        return {
            "languages": sorted_languages,
            "total_code_files": total_code_files,
            "primary_languages": list(sorted_languages.keys())[:8],
            "code_vs_other_ratio": round(total_code_files / max(sum(d['count'] for d in extensions_data.values()), 1), 3)
        }
    
    def track_file_type_changes(self) -> Dict[str, Any]:
        """
        Track changes in file type distribution over time
        Stores history and detects significant changes
        """
        logger.info("📈 Tracking file type changes...")
        
        # Get current file type stats
        current_stats = self.scan_workspace_file_types()
        
        # Load historical data
        history_file = self.workspace_root / self.file_type_history_file
        history_data = []
        
        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
            except Exception as e:
                logger.warning(f"⚠️ Could not load history file: {e}")
                history_data = []
        
        # Add current stats to history
        history_entry = {
            "timestamp": current_stats["scan_timestamp"],
            "summary": current_stats["summary"],
            "top_extensions": current_stats["top_extensions"],
            "languages": current_stats["language_analysis"]["languages"]
        }
        
        history_data.append(history_entry)
        
        # Clean old entries (keep last 90 days)
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=self.monitoring_config["history_retention_days"])
        history_data = [entry for entry in history_data 
                       if datetime.fromisoformat(entry["timestamp"]) > cutoff_date]
        
        # Detect significant changes
        changes = self._detect_significant_changes(history_data)
        
        # Save updated history
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2, ensure_ascii=False)
            logger.info(f"📋 File type history updated: {history_file}")
        except Exception as e:
            logger.error(f"❌ Failed to save history: {e}")
        
        return {
            "current_stats": current_stats,
            "history_entries": len(history_data),
            "significant_changes": changes,
            "monitoring_active": True,
            "next_scan_recommended": (datetime.now() + timedelta(hours=24)).isoformat()
        }
    
    def _detect_significant_changes(self, history_data: List[Dict]) -> Dict[str, Any]:
        """Detect significant changes in file type distribution"""
        
        if len(history_data) < 2:
            return {"message": "Insufficient history for change detection"}
        
        current = history_data[-1]
        previous = history_data[-2]
        threshold = self.monitoring_config["significant_change_threshold"]
        
        changes = {
            "timestamp": current["timestamp"],
            "comparison_with": previous["timestamp"],
            "file_count_changes": {},
            "new_extensions": [],
            "removed_extensions": [],
            "significant_changes": []
        }
        
        # Compare file counts
        current_total = current["summary"]["total_files"]
        previous_total = previous["summary"]["total_files"]
        
        if previous_total > 0:
            total_change = (current_total - previous_total) / previous_total
            if abs(total_change) > threshold:
                changes["significant_changes"].append({
                    "type": "total_files",
                    "change_percent": round(total_change * 100, 2),
                    "current_count": current_total,
                    "previous_count": previous_total
                })
        
        # Compare extensions
        current_exts = set(current["top_extensions"].keys())
        previous_exts = set(previous["top_extensions"].keys())
        
        changes["new_extensions"] = list(current_exts - previous_exts)
        changes["removed_extensions"] = list(previous_exts - current_exts)
        
        # Compare counts for common extensions
        for ext in current_exts & previous_exts:
            current_count = current["top_extensions"][ext]["count"]
            previous_count = previous["top_extensions"][ext]["count"]
            
            if previous_count > 0:
                change_ratio = (current_count - previous_count) / previous_count
                if abs(change_ratio) > threshold:
                    changes["file_count_changes"][ext] = {
                        "change_percent": round(change_ratio * 100, 2),
                        "current_count": current_count,
                        "previous_count": previous_count
                    }
        
        return changes
    
    def create_holographic_metadata(self, target_folder: Path = None, overwrite: bool = False) -> Dict[str, str]:
        """Create holographic metadata file for a specific folder"""
        
        if target_folder is None:
            target_folder = self.workspace_root
        
        if not target_folder.exists():
            logger.error(f"❌ Target folder does not exist: {target_folder}")
            return {}
        
        # Check if metadata already exists
        metadata_file = target_folder / self.metadata_filename
        if metadata_file.exists() and not overwrite:
            logger.info(f"⏭️ Metadata already exists (skipping): {metadata_file}")
            return {str(target_folder): str(metadata_file)}
        
        logger.info(f"🔮 Creating holographic metadata for: {target_folder}")
        
        try:
            # Generate metadata
            metadata = self.generate_folder_metadata(target_folder)
            
            # Add overwrite information
            metadata["creation_info"] = {
                "overwrite_mode": overwrite,
                "previous_metadata_existed": metadata_file.exists()
            }
            
            # Save metadata file
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            action = "Updated" if metadata_file.exists() else "Created"
            logger.info(f"✅ Metadata {action.lower()}: {metadata_file}")
            return {str(target_folder): str(metadata_file)}
            
        except Exception as e:
            logger.error(f"❌ Failed to save metadata for {target_folder}: {e}")
            return {}
    
    def scan_and_create_holographic_system(self, max_depth: int = 3, overwrite: bool = False) -> Dict[str, Any]:
        """Scan workspace and create holographic metadata system"""
        
        logger.info("🌟 Creating AIOS Holographic Metadata System...")
        logger.info(f"📊 Max depth: {max_depth}")
        logger.info(f"🔄 Overwrite mode: {overwrite}")
        
        created_files = {}
        updated_files = {}
        skipped_files = {}
        folder_count = 0
        processed_count = 0
        
        # Scan and create metadata for relevant folders
        for folder in self.workspace_root.rglob('*'):
            if not folder.is_dir():
                continue
                
            folder_count += 1
            
            # Show progress every 50 folders
            if folder_count % 50 == 0:
                logger.info(f"📊 Scanned {folder_count} folders, processed {processed_count}...")
            
            try:
                # Calculate depth
                relative_path = folder.relative_to(self.workspace_root)
                depth = len(relative_path.parts)
                
                if depth > max_depth:
                    continue
                    
                if not self._should_create_metadata(folder):
                    continue
                
                # Check if metadata already exists
                metadata_file = folder / self.metadata_filename
                if metadata_file.exists() and not overwrite:
                    skipped_files[str(folder)] = str(metadata_file)
                    continue
                
                # Create metadata
                result = self.create_holographic_metadata(folder, overwrite=overwrite)
                if result:
                    if metadata_file.exists() and overwrite:
                        updated_files.update(result)
                    else:
                        created_files.update(result)
                    processed_count += 1
            
            except (ValueError, PermissionError, OSError) as e:
                logger.debug(f"⚠️ Skipping folder {folder}: {e}")
                continue
        
        # Combine all files for total count
        all_files = {**created_files, **updated_files, **skipped_files}
        
        # Create master holographic index
        index_data = {
            "holographic_system_version": "1.0.0",
            "creation_timestamp": datetime.now().isoformat(),
            "workspace_root": str(self.workspace_root),
            "generation_parameters": {
                "max_depth": max_depth,
                "overwrite_mode": overwrite
            },
            "metadata_files": {
                "created": created_files,
                "updated": updated_files,
                "skipped": skipped_files,
                "all_files": all_files
            },
            "system_stats": {
                "folders_scanned": folder_count,
                "folders_processed": processed_count,
                "metadata_files_created": len(created_files),
                "metadata_files_updated": len(updated_files),
                "metadata_files_skipped": len(skipped_files),
                "total_metadata_files": len(all_files),
                "coverage_percentage": (len(all_files) / max(folder_count, 1)) * 100 if folder_count > 0 else 0
            },
            "usage_instructions": {
                "for_ai_engines": "Read .aios_spatial_metadata.json in each folder for spatial awareness",
                "chat_mode_integration": "Always check spatial metadata before creating files or folders",
                "spatial_awareness": "Use metadata to understand folder relationships and context",
                "overwrite_command": "Use --overwrite flag to update existing metadata files"
            }
        }
        
        # Save master index (always overwrite)
        index_file = self.workspace_root / self.holographic_index_file
        try:
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            logger.info(f"📋 Master index updated: {index_file}")
        except Exception as e:
            logger.error(f"❌ Failed to save master index: {e}")
        
        # Report results
        logger.info("🎉 Holographic Metadata System operation complete!")
        logger.info(f"📊 Statistics:")
        logger.info(f"   Folders scanned: {folder_count}")
        logger.info(f"   Folders processed: {processed_count}")
        logger.info(f"   Metadata files created: {len(created_files)}")
        logger.info(f"   Metadata files updated: {len(updated_files)}")
        logger.info(f"   Metadata files skipped: {len(skipped_files)}")
        logger.info(f"   Total metadata files: {len(all_files)}")
        logger.info(f"   Coverage: {index_data['system_stats']['coverage_percentage']:.1f}%")
        
        return index_data
    
    def _should_create_metadata(self, folder: Path) -> bool:
        """Determine if folder should have metadata"""
        
        # Comprehensive skip patterns for system/build folders
        skip_patterns = [
            ".git", ".vs", ".vscode", "__pycache__", "node_modules", 
            "bin", "obj", "build", "debug", "release", ".pytest_cache",
            "env", "venv", ".env", "aios_env", ".idea", ".cache",
            "tmp", "temp", ".tmp", ".temp", "logs", ".logs",
            "coverage", ".coverage", ".nyc_output", "dist", ".dist"
        ]
        
        # Check folder name
        folder_name = folder.name.lower()
        if any(pattern.lower() in folder_name for pattern in skip_patterns):
            logger.debug(f"🚫 Skipping system folder: {folder}")
            return False
        
        # Check full path for nested system folders
        folder_path_str = str(folder).lower()
        if any(pattern.lower() in folder_path_str for pattern in skip_patterns):
            logger.debug(f"🚫 Skipping system path: {folder}")
            return False
        
        # Skip if we can't access the folder
        try:
            folder_contents = list(folder.iterdir())
        except (PermissionError, OSError) as e:
            logger.warning(f"⚠️ Cannot access folder {folder}: {e}")
            return False
        
        # Skip empty folders
        if not folder_contents:
            logger.debug(f"📭 Skipping empty folder: {folder}")
            return False
        
        # Always create for important AIOS folders
        important_patterns = ["ai", "githooks", "interface", "core", "docs", "runtime", "tachyonic", "orchestrator", "visual_interface"]
        if any(pattern in str(folder).lower() for pattern in important_patterns):
            logger.debug(f"⭐ Important AIOS folder: {folder}")
            return True
        
        # Create for folders with significant content (at least 2 files or 1 subfolder)
        file_count = len([f for f in folder_contents if f.is_file()])
        subfolder_count = len([f for f in folder_contents if f.is_dir()])
        
        has_significant_content = file_count >= 2 or subfolder_count >= 1
        if has_significant_content:
            logger.debug(f"📁 Significant content folder: {folder} ({file_count} files, {subfolder_count} subfolders)")
        
        return has_significant_content
    
    def read_spatial_metadata(self, folder_path: Path) -> Optional[Dict[str, Any]]:
        """Read spatial metadata for a folder"""
        
        metadata_file = folder_path / self.metadata_filename
        if not metadata_file.exists():
            logger.warning(f"⚠️ No spatial metadata found: {metadata_file}")
            return None
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Failed to read metadata: {e}")
            return None

def main():
    """CLI entry point for holographic metadata system"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AIOS Holographic Metadata System')
    parser.add_argument('--create-system', action='store_true', help='Create full holographic system')
    parser.add_argument('--create-folder', type=Path, help='Create metadata for specific folder')
    parser.add_argument('--read-metadata', type=Path, help='Read metadata for specific folder')
    parser.add_argument('--scan-file-types', action='store_true', help='Scan workspace file types')
    parser.add_argument('--track-changes', action='store_true', help='Track file type changes over time')
    parser.add_argument('--file-type-report', action='store_true', help='Generate comprehensive file type report')
    parser.add_argument('--max-depth', type=int, default=3, help='Maximum folder depth to process')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing metadata files')
    parser.add_argument('--workspace', type=Path, help='AIOS workspace root')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger('HolographicMetadata').setLevel(logging.DEBUG)
    
    system = AIOSHolographicMetadataSystem(args.workspace)
    
    if args.create_system:
        result = system.scan_and_create_holographic_system(args.max_depth, args.overwrite)
        print(f"\n🎉 Holographic System {'Updated' if args.overwrite else 'Created'}!")
        print(f"📊 Created: {result['system_stats']['metadata_files_created']}")
        print(f"🔄 Updated: {result['system_stats']['metadata_files_updated']}")
        print(f"⏭️ Skipped: {result['system_stats']['metadata_files_skipped']}")
        print(f"📈 Total: {result['system_stats']['total_metadata_files']}")
    elif args.create_folder:
        result = system.create_holographic_metadata(args.create_folder, args.overwrite)
        if result:
            print(f"✅ Metadata {'updated' if args.overwrite else 'created'} for: {args.create_folder}")
        else:
            print(f"❌ Failed to create metadata for: {args.create_folder}")
    elif args.read_metadata:
        metadata = system.read_spatial_metadata(args.read_metadata)
        if metadata:
            print(json.dumps(metadata, indent=2))
        else:
            print(f"❌ No metadata found for: {args.read_metadata}")
    elif args.scan_file_types:
        print("🔍 Scanning workspace file types...")
        result = system.scan_workspace_file_types()
        print(f"\n📊 File Type Analysis Complete!")
        print(f"Total Files: {result['summary']['total_files']:,}")
        print(f"Unique Extensions: {result['summary']['unique_extensions']}")
        print(f"Size: {result['summary']['total_size_mb']:.1f} MB")
        print(f"\n🔝 Top File Types:")
        for ext, data in list(result['top_extensions'].items())[:10]:
            print(f"  {ext or '(no ext)'}: {data['count']:,} files")
        print(f"\n💻 Primary Languages:")
        for lang in result['language_analysis']['primary_languages'][:5]:
            count = result['language_analysis']['languages'][lang]['count']
            print(f"  {lang}: {count:,} files")
    elif args.track_changes:
        print("� Tracking file type changes...")
        result = system.track_file_type_changes()
        print(f"\n✅ File Type Change Tracking Complete!")
        print(f"History Entries: {result['history_entries']}")
        
        changes = result['significant_changes']
        if 'significant_changes' in changes and changes['significant_changes']:
            print(f"\n⚠️ Significant Changes Detected:")
            for change in changes['significant_changes']:
                print(f"  {change['type']}: {change['change_percent']:+.1f}%")
        else:
            print(f"\n✅ No significant changes detected")
            
        if changes.get('new_extensions'):
            print(f"\n🆕 New Extensions: {', '.join(changes['new_extensions'])}")
        if changes.get('removed_extensions'):
            print(f"\n❌ Removed Extensions: {', '.join(changes['removed_extensions'])}")
            
    elif args.file_type_report:
        print("📋 Generating comprehensive file type report...")
        
        # Get current scan
        scan_result = system.scan_workspace_file_types()
        
        # Get change tracking
        track_result = system.track_file_type_changes()
        
        # Save comprehensive report to Runtime Intelligence analysis area
        report_file = (
            system.workspace_root
            / "runtime_intelligence/analysis/aios_file_type_report.json"
        )
        report_data = {
            "report_timestamp": datetime.now().isoformat(),
            "current_analysis": scan_result,
            "change_tracking": track_result,
            "report_summary": {
                "total_files_analyzed": scan_result['summary']['total_files'],
                "languages_detected": len(scan_result['language_analysis']['languages']),
                "monitoring_active": track_result['monitoring_active'],
                "significant_changes": len(track_result['significant_changes'].get('significant_changes', []))
            }
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Comprehensive report saved: {report_file}")
            print(f"📊 Files: {scan_result['summary']['total_files']:,}")
            print(f"💻 Languages: {len(scan_result['language_analysis']['languages'])}")
            print(f"📈 History: {track_result['history_entries']} entries")
        except Exception as e:
            print(f"❌ Failed to save report: {e}")
    else:
        print("�🔮 AIOS Holographic Metadata System with File Type Monitoring")
        print("📊 File Type Analysis:")
        print("  --scan-file-types        Analyze current file type distribution")
        print("  --track-changes          Track changes over time with history")
        print("  --file-type-report       Generate comprehensive report")
        print("🗃️ Spatial Metadata:")
        print("  --create-system          Generate full holographic metadata")
        print("  --create-folder <path>   Create metadata for specific folder")
        print("  --read-metadata <path>   Read folder metadata")
        print("⚙️ Options:")
        print("  --overwrite              Update existing metadata files")
        print("  --verbose                Enable detailed logging")

if __name__ == "__main__":
    main()