#!/usr/bin/env python3
"""
AIOS FFmpeg Screen Capture Bridge
=================================

Exposes FFmpeg as a first-class system capability for AIOS agents,
enabling automated screen capture for architecture demonstrations,
agent workflow recording, debugging, and knowledge distillation.

FFmpeg acts as a visual memory extension for AIOS - a headless,
scriptable sensor for the Windows environment.

Tool: ffmpeg
Path: C:\\ffmpeg\\bin\\ffmpeg.exe
Capabilities: screen_capture, region_capture,
              timed_recording, headless_execution
Agent Safe: True
Automation Ready: True

Reference: docs/AIOS/architecture/interfaces/ffmpeg.md
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Literal
from dataclasses import dataclass
import json
import logging

# AIOS logging integration
logger = logging.getLogger("aios.visual.ffmpeg")

# =============================================================================
# Configuration
# =============================================================================


def _find_ffmpeg() -> Path:
    """Auto-detect FFmpeg path from system or common locations."""
    import shutil
    
    # Try system PATH first
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return Path(system_ffmpeg)
    
    # Common Windows install locations
    common_paths = [
        Path(r"C:\ffmpeg\bin\ffmpeg.exe"),
        Path(r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"),
        Path.home() / "AppData/Local/Microsoft/WinGet/Links/ffmpeg.exe",
    ]
    
    for p in common_paths:
        if p.exists():
            return p
    
    # Fallback to documented path
    return Path(r"C:\ffmpeg\bin\ffmpeg.exe")


FFMPEG_PATH = _find_ffmpeg()
DEFAULT_ARTIFACTS_DIR = Path(r"C:\dev\AIOS\tachyonic\artifacts\video")
DEFAULT_FRAMERATE = 30
DEFAULT_PIXEL_FORMAT = "yuv420p"


@dataclass
class CaptureMetadata:
    """Metadata for captured video artifacts."""
    timestamp: str
    host: str = "AIOS-Win"
    agent_id: Optional[str] = None
    trigger_reason: Optional[str] = None
    duration_seconds: Optional[float] = None
    region: Optional[Dict[str, int]] = None
    output_path: Optional[str] = None
    ffmpeg_returncode: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class FFmpegCaptureBridge:
    """
    AIOS FFmpeg Screen Capture Bridge
    
    Provides automated screen capture capabilities for AIOS agents.
    Designed for headless, non-interactive operation.
    
    Example:
        bridge = FFmpegCaptureBridge()
        
        # Full desktop capture for 30 seconds
        result = await bridge.capture_desktop(duration_seconds=30)
        
        # Region capture
        result = await bridge.capture_region(
            x=100, y=100, width=1280, height=720,
            duration_seconds=60
        )
    """
    
    def __init__(
        self,
        ffmpeg_path: Path = FFMPEG_PATH,
        artifacts_dir: Path = DEFAULT_ARTIFACTS_DIR,
        agent_id: Optional[str] = None
    ):
        self.ffmpeg_path = ffmpeg_path
        self.artifacts_dir = artifacts_dir
        self.agent_id = agent_id
        self._ensure_artifacts_dir()
        
    def _ensure_artifacts_dir(self) -> None:
        """Ensure artifacts directory exists."""
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        
    def _generate_filename(
        self, prefix: str = "capture", ext: str = "mpg"
    ) -> str:
        """Generate timestamped filename for non-colliding recordings."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{ts}.{ext}"
    
    def _build_base_command(self, framerate: int = DEFAULT_FRAMERATE) -> list:
        """Build base FFmpeg command with GDI grab."""
        return [
            str(self.ffmpeg_path),
            "-f", "gdigrab",
            "-framerate", str(framerate),
        ]
    
    def is_available(self) -> bool:
        """Check if FFmpeg is available at configured path."""
        return self.ffmpeg_path.exists()
    
    def get_capability_manifest(self) -> Dict[str, Any]:
        """Return AINLP-compatible capability manifest."""
        return {
            "tool": "ffmpeg",
            "path": str(self.ffmpeg_path),
            "available": self.is_available(),
            "capabilities": [
                "screen_capture",
                "region_capture",
                "timed_recording",
                "headless_execution"
            ],
            "formats": ["mpg", "mp4", "mkv"],
            "agent_safe": True,
            "automation_ready": True,
            "read_only": True,  # Does not alter system state
            "artifacts_dir": str(self.artifacts_dir)
        }
    
    async def capture_desktop(
        self,
        duration_seconds: Optional[float] = None,
        output_format: Literal["mpg", "mp4", "mkv"] = "mpg",
        framerate: int = DEFAULT_FRAMERATE,
        trigger_reason: Optional[str] = None
    ) -> CaptureMetadata:
        """
        Capture full desktop screen.
        
        Args:
            duration_seconds: Recording duration (None = manual stop)
            output_format: Output container format
            framerate: Capture framerate (default 30)
            trigger_reason: Why capture was triggered (for metadata)
            
        Returns:
            CaptureMetadata with capture details
        """
        if not self.is_available():
            raise RuntimeError(f"FFmpeg not found at {self.ffmpeg_path}")
        
        filename = self._generate_filename("desktop", output_format)
        output_path = self.artifacts_dir / filename
        
        cmd = self._build_base_command(framerate)
        
        if duration_seconds:
            # Convert to HH:MM:SS format
            hours, remainder = divmod(int(duration_seconds), 3600)
            minutes, seconds = divmod(remainder, 60)
            cmd.extend(["-t", f"{hours:02d}:{minutes:02d}:{seconds:02d}"])
        
        cmd.extend([
            "-i", "desktop",
            "-pix_fmt", DEFAULT_PIXEL_FORMAT,
            "-y",  # Overwrite without asking
            str(output_path)
        ])
        
        metadata = CaptureMetadata(
            timestamp=datetime.now().isoformat(),
            agent_id=self.agent_id,
            trigger_reason=trigger_reason,
            duration_seconds=duration_seconds,
            output_path=str(output_path)
        )
        
        logger.info(f"Starting desktop capture: {output_path}")
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        metadata.ffmpeg_returncode = process.returncode
        
        if process.returncode == 0:
            logger.info(f"Capture completed: {output_path}")
            self._write_metadata(output_path, metadata)
        else:
            logger.error(f"Capture failed: {stderr.decode()}")
            
        return metadata
    
    async def capture_region(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        duration_seconds: Optional[float] = None,
        output_format: Literal["mpg", "mp4", "mkv"] = "mpg",
        framerate: int = DEFAULT_FRAMERATE,
        trigger_reason: Optional[str] = None
    ) -> CaptureMetadata:
        """
        Capture specific screen region.
        
        Args:
            x: Horizontal offset from top-left
            y: Vertical offset from top-left
            width: Capture width
            height: Capture height
            duration_seconds: Recording duration
            output_format: Output container format
            framerate: Capture framerate
            trigger_reason: Why capture was triggered
            
        Returns:
            CaptureMetadata with capture details
        """
        if not self.is_available():
            raise RuntimeError(f"FFmpeg not found at {self.ffmpeg_path}")
        
        filename = self._generate_filename("region", output_format)
        output_path = self.artifacts_dir / filename
        
        cmd = self._build_base_command(framerate)
        cmd.extend([
            "-offset_x", str(x),
            "-offset_y", str(y),
            "-video_size", f"{width}x{height}",
        ])
        
        if duration_seconds:
            hours, remainder = divmod(int(duration_seconds), 3600)
            minutes, seconds = divmod(remainder, 60)
            cmd.extend(["-t", f"{hours:02d}:{minutes:02d}:{seconds:02d}"])
        
        cmd.extend([
            "-i", "desktop",
            "-pix_fmt", DEFAULT_PIXEL_FORMAT,
            "-y",
            str(output_path)
        ])
        
        metadata = CaptureMetadata(
            timestamp=datetime.now().isoformat(),
            agent_id=self.agent_id,
            trigger_reason=trigger_reason,
            duration_seconds=duration_seconds,
            region={"x": x, "y": y, "width": width, "height": height},
            output_path=str(output_path)
        )
        
        logger.info(
            f"Starting region capture ({width}x{height}): {output_path}"
        )

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        metadata.ffmpeg_returncode = process.returncode
        
        if process.returncode == 0:
            logger.info(f"Region capture completed: {output_path}")
            self._write_metadata(output_path, metadata)
        else:
            logger.error(f"Region capture failed: {stderr.decode()}")
            
        return metadata

    def _write_metadata(
        self, video_path: Path, metadata: CaptureMetadata
    ) -> None:
        """Write companion metadata JSON file."""
        meta_path = video_path.with_suffix(".json")
        meta_path.write_text(metadata.to_json())
        logger.debug(f"Metadata written: {meta_path}")


# =============================================================================
# Synchronous Interface (for direct script usage)
# =============================================================================

def capture_desktop_sync(
    duration_seconds: Optional[float] = None,
    output_format: str = "mpg",
    agent_id: Optional[str] = None,
    trigger_reason: Optional[str] = None
) -> CaptureMetadata:
    """
    Synchronous desktop capture for script usage.
    
    Example:
        from ai.tools.visual.ffmpeg_capture_bridge import capture_desktop_sync
        result = capture_desktop_sync(duration_seconds=30, agent_id="Alpha")
    """
    bridge = FFmpegCaptureBridge(agent_id=agent_id)
    return asyncio.run(bridge.capture_desktop(
        duration_seconds=duration_seconds,
        output_format=output_format,
        trigger_reason=trigger_reason
    ))


def capture_region_sync(
    x: int, y: int, width: int, height: int,
    duration_seconds: Optional[float] = None,
    output_format: str = "mpg",
    agent_id: Optional[str] = None,
    trigger_reason: Optional[str] = None
) -> CaptureMetadata:
    """Synchronous region capture for script usage."""
    bridge = FFmpegCaptureBridge(agent_id=agent_id)
    return asyncio.run(bridge.capture_region(
        x=x, y=y, width=width, height=height,
        duration_seconds=duration_seconds,
        output_format=output_format,
        trigger_reason=trigger_reason
    ))


# =============================================================================
# CLI Interface
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AIOS FFmpeg Screen Capture Bridge",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check availability
  python ffmpeg_capture_bridge.py --check
  
  # Capture desktop for 30 seconds
  python ffmpeg_capture_bridge.py --desktop --duration 30
  
  # Capture region
  python ffmpeg_capture_bridge.py --region 100 100 1280 720 --duration 60
  
  # Get capability manifest
  python ffmpeg_capture_bridge.py --manifest
        """
    )

    parser.add_argument(
        "--check", action="store_true",
        help="Check FFmpeg availability"
    )
    parser.add_argument(
        "--manifest", action="store_true",
        help="Print capability manifest"
    )
    parser.add_argument(
        "--desktop", action="store_true",
        help="Capture full desktop"
    )
    parser.add_argument(
        "--region", nargs=4, type=int,
        metavar=("X", "Y", "W", "H"),
        help="Capture region (x, y, width, height)"
    )
    parser.add_argument(
        "--duration", type=float,
        help="Duration in seconds"
    )
    parser.add_argument(
        "--format", choices=["mpg", "mp4", "mkv"],
        default="mpg", help="Output format (default: mpg)"
    )
    parser.add_argument(
        "--agent", type=str,
        help="Agent ID for metadata"
    )
    parser.add_argument(
        "--reason", type=str,
        help="Trigger reason for metadata"
    )

    args = parser.parse_args()
    
    bridge = FFmpegCaptureBridge(agent_id=args.agent)
    
    if args.check:
        available = bridge.is_available()
        print(f"FFmpeg available: {available}")
        if available:
            print(f"Path: {bridge.ffmpeg_path}")
        exit(0 if available else 1)
    
    if args.manifest:
        print(json.dumps(bridge.get_capability_manifest(), indent=2))
        exit(0)
    
    if args.desktop:
        result = capture_desktop_sync(
            duration_seconds=args.duration,
            output_format=args.format,
            agent_id=args.agent,
            trigger_reason=args.reason
        )
        print(result.to_json())
        exit(0 if result.ffmpeg_returncode == 0 else 1)
    
    if args.region:
        x, y, w, h = args.region
        result = capture_region_sync(
            x=x, y=y, width=w, height=h,
            duration_seconds=args.duration,
            output_format=args.format,
            agent_id=args.agent,
            trigger_reason=args.reason
        )
        print(result.to_json())
        exit(0 if result.ffmpeg_returncode == 0 else 1)
    
    parser.print_help()
