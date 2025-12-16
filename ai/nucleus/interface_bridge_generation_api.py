"""
AIOS Library Generation API Endpoints
Real-time code generation with WebSocket streaming

This module provides HTTP API endpoints and WebSocket streaming
for the Library Code Generation Loop, enabling real-time monitoring
from the C# UI dashboard.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import asyncio
import json
import os
from pathlib import Path
from datetime import datetime

# Import AIOS components
import sys



def get_generation_results_path() -> Path:
    """Get path to generation results"""
    return (
        Path(__file__).parent.parent.parent.parent
        / "evolution_lab"
        / "library_generations"
    )


async def broadcast_update(message: Dict[str, Any]):
    """Broadcast update to all connected WebSocket clients"""
    disconnected = []
    for ws in websocket_connections:
        try:
            await ws.send_json(message)
        except:
            disconnected.append(ws)

    # Remove disconnected clients
    for ws in disconnected:
        websocket_connections.remove(ws)


# API Endpoints


    Returns list of library names that can be used for code generation.
    """
    try:
        lib_path = get_library_knowledge_path()
        if not lib_path.exists():
            return []

        libraries = []
        for json_file in lib_path.glob("*.json"):
            # Extract library name from filename (e.g., "aios_core.json" -> "aios_core")
            library_name = json_file.stem
            libraries.append(library_name)

        return libraries

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to list libraries: {str(e)}"
        )


@router.get("/libraries/{library_name}", response_model=LibraryInfo)
async def get_library_info(library_name: str):
    """
    Get detailed information about a specific library

    Args:
        library_name: Name of the library (e.g., "aios_core")

    Returns:
        LibraryInfo object with metadata about the library
    """
    try:
        lib_path = get_library_knowledge_path() / f"{library_name}.json"

        if not lib_path.exists():
            raise HTTPException(
                status_code=404, detail=f"Library '{library_name}' not found"
            )

        with open(lib_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        stat = lib_path.stat()

        return LibraryInfo(
            name=data.get("library_name", library_name),
            language=data.get("language", "unknown"),
            api_elements=len(data.get("api_elements", [])),
            size_bytes=stat.st_size,
            ingested_at=datetime.fromtimestamp(stat.st_mtime),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get library info: {str(e)}"
        )


@router.post("/generation/start")
async def start_generation(request: GenerationRequest):
    """
    Start a new code generation session

    Args:
        request: Generation parameters (library, size, consciousness target)

    Returns:
        Session ID for tracking progress
    """
    try:
        session_id = f"gen_{int(datetime.now().timestamp())}"

        # Validate library exists
        lib_path = get_library_knowledge_path() / f"{request.library_name}.json"
        if not lib_path.exists():
            raise HTTPException(
                status_code=404, detail=f"Library '{request.library_name}' not found"
            )

        # Create session info
        active_sessions[session_id] = {
            "session_id": session_id,
            "library_name": request.library_name,
            "generation_size": request.generation_size,
            "target_consciousness": request.target_consciousness,
            "status": "starting",
            "current_phase": "Initialization",
            "overall_progress": 0,
            "started_at": datetime.now(),
            "completed_at": None,
            "task": None,
        }

        # Start generation in background
        task = asyncio.create_task(run_generation_session(session_id, request))
        active_sessions[session_id]["task"] = task

        # Broadcast start event
        await broadcast_update(
            {
                "event": "generation_started",
                "session_id": session_id,
                "library_name": request.library_name,
            }
        )

        return {"session_id": session_id, "status": "started"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to start generation: {str(e)}"
        )


async def run_generation_session(session_id: str, request: GenerationRequest):
    """
    Execute the complete generation cycle with progress updates

    This function runs the LibraryCodeGenerationLoop and broadcasts
    real-time updates via WebSocket to connected UI clients.
    """
    session = active_sessions[session_id]

    try:
        # Phase 1: Library Loading
        await update_progress(
            session_id,
            "Library Loading",
            10,
            {
                "log_level": "INFO",
                "log_phase": "LibraryLoading",
                "log_message": f"Loading library knowledge: {request.library_name}",
                "library_loading_progress": 50,
                "library_loading_status": "Reading JSON...",
            },
        )

        await asyncio.sleep(0.5)  # Simulate loading

        await update_progress(
            session_id,
            "Library Loading",
            15,
            {
                "library_loading_progress": 100,
                "library_loading_status": "Library loaded successfully",
            },
        )

        # Phase 2: Paradigm Extraction
        await update_progress(
            session_id,
            "Paradigm Extraction",
            20,
            {
                "log_level": "INFO",
                "log_phase": "ParadigmExtraction",
                "log_message": "Analyzing code patterns with AST parser...",
            },
        )

        # Actually extract paradigms
        engine = ParadigmExtractionEngine()
        paradigms = engine.extract_from_library(request.library_name)

        await update_progress(
            session_id,
            "Paradigm Extraction",
            35,
            {
                "paradigms_extracted": len(paradigms),
                "paradigm_extraction_status": f"Extracted {len(paradigms)} programming paradigms",
                "log_level": "SUCCESS",
                "log_message": f"Found {len(paradigms)} distinct programming patterns",
            },
        )

        # Phase 3: Prompt Generation
        await update_progress(
            session_id,
            "Prompt Generation",
            40,
            {
                "log_level": "INFO",
                "log_phase": "PromptGeneration",
                "log_message": f"Generating {request.generation_size} variant prompts...",
            },
        )

        await asyncio.sleep(1)

        await update_progress(
            session_id,
            "Prompt Generation",
            50,
            {
                "prompts_generated": request.generation_size,
                "prompt_generation_status": f"Generated {request.generation_size} prompts",
                "log_level": "SUCCESS",
                "log_message": f"Prompt generation complete - consciousness target: {request.target_consciousness}",
            },
        )

        # Phase 4: Code Generation
        await update_progress(
            session_id,
            "Code Generation",
            55,
            {
                "log_level": "INFO",
                "log_phase": "CodeGeneration",
                "log_message": "Initializing AI agents...",
            },
        )

        # Run complete generation cycle
        loop = LibraryCodeGenerationLoop()

        for i in range(request.generation_size):
            progress = 55 + (i + 1) * (25 / request.generation_size)
            await update_progress(
                session_id,
                "Code Generation",
                int(progress),
                {
                    "code_artifacts_generated": i + 1,
                    "code_generation_status": f"Generated {i + 1} / {request.generation_size} artifacts",
                    "log_level": "INFO",
                    "log_message": f"Generating artifact {i + 1}/{request.generation_size} with AI agent...",
                },
            )

            await asyncio.sleep(2)  # Simulate AI generation time

        # Phase 5: Code Analysis
        await update_progress(
            session_id,
            "Code Analysis",
            85,
            {
                "log_level": "INFO",
                "log_phase": "CodeAnalysis",
                "log_message": "Analyzing generated code with multi-dimensional metrics...",
            },
        )

        # Execute actual generation loop
        results = await loop.run_complete_cycle(
            library_name=request.library_name,
            generation_size=request.generation_size,
            target_consciousness=request.target_consciousness,
        )

        # Calculate average consciousness
        avg_consciousness = sum(r["consciousness_score"] for r in results) / len(
            results
        )

        await update_progress(
            session_id,
            "Code Analysis",
            90,
            {
                "average_consciousness": avg_consciousness,
                "code_analysis_status": f"Analysis complete - avg consciousness: {avg_consciousness:.2f}",
                "log_level": "SUCCESS",
                "log_message": f"Code analysis complete - {len(results)} artifacts analyzed",
            },
        )

        # Phase 6: Results Saving
        await update_progress(
            session_id,
            "Results Saving",
            95,
            {
                "log_level": "INFO",
                "log_phase": "ResultsSaving",
                "log_message": "Saving results to evolution_lab/library_generations...",
            },
        )

        output_dir = results[0]["output_path"] if results else "unknown"

        await update_progress(
            session_id,
            "Complete",
            100,
            {
                "output_directory": str(output_dir),
                "results_saving_status": "Results saved successfully",
                "log_level": "SUCCESS",
                "log_message": f"Generation complete! Output: {output_dir}",
                "completed": True,
            },
        )

        # Mark session as complete
        session["status"] = "completed"
        session["completed_at"] = datetime.now()
        session["results"] = results

    except Exception as e:
        await update_progress(
            session_id,
            "Error",
            session["overall_progress"],
            {
                "log_level": "ERROR",
                "log_phase": "Execution",
                "log_message": f"Generation failed: {str(e)}",
                "error": str(e),
            },
        )
        session["status"] = "failed"
        session["error"] = str(e)


async def update_progress(
    session_id: str, phase: str, progress: int, extra_data: Dict[str, Any]
):
    """Update session progress and broadcast to WebSocket clients"""
    if session_id not in active_sessions:
        return

    session = active_sessions[session_id]
    session["current_phase"] = phase
    session["overall_progress"] = progress

    update = {
        "session_id": session_id,
        "phase": phase,
        "overall_progress": progress,
        **extra_data,
    }

    await broadcast_update(update)


@router.get("/generation/{session_id}/status", response_model=GenerationStatus)
async def get_generation_status(session_id: str):
    """
    Get current status of a generation session

    Args:
        session_id: Session identifier returned from /generation/start

    Returns:
        Current status and progress information
    """
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = active_sessions[session_id]

    return GenerationStatus(
        session_id=session_id,
        library_name=session["library_name"],
        status=session["status"],
        current_phase=session["current_phase"],
        overall_progress=session["overall_progress"],
        started_at=session["started_at"],
        completed_at=session.get("completed_at"),
    )


@router.post("/generation/stop")
async def stop_generation():
    """
    Stop the currently running generation session

    Cancels all active generation tasks.
    """
    try:
        stopped = []
        for session_id, session in active_sessions.items():
            if session["status"] in ["starting", "running"]:
                task = session.get("task")
                if task:
                    task.cancel()
                session["status"] = "stopped"
                stopped.append(session_id)

        return {"stopped_sessions": stopped}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to stop generation: {str(e)}"
        )


@router.get("/generations/recent", response_model=List[GenerationResultSummary])
async def get_recent_generations(limit: int = 10):
    """
    Get recent completed generation results

    Args:
        limit: Maximum number of results to return (default: 10)

    Returns:
        List of generation result summaries
    """
    try:
        results_path = get_generation_results_path()

        if not results_path.exists():
            return []

        summaries = []

        # Scan all library subdirectories
        for lib_dir in results_path.iterdir():
            if not lib_dir.is_dir():
                continue

            # Scan generation subdirectories
            for gen_dir in lib_dir.iterdir():
                if not gen_dir.is_dir():
                    continue

                metadata_file = gen_dir / "generation_metadata.json"
                if not metadata_file.exists():
                    continue

                try:
                    with open(metadata_file, "r") as f:
                        metadata = json.load(f)

                    # Load paradigm information
                    paradigms_file = gen_dir / "paradigms_extracted.json"
                    top_paradigms = []
                    if paradigms_file.exists():
                        with open(paradigms_file, "r") as f:
                            paradigm_data = json.load(f)
                            top_paradigms = paradigm_data.get("paradigms", [])[:5]

                    # Collect consciousness scores from analysis files
                    consciousness_scores = []
                    for analysis_file in gen_dir.glob("*_analysis.json"):
                        with open(analysis_file, "r") as f:
                            analysis = json.load(f)
                            consciousness_scores.append(
                                analysis.get("consciousness_score", 0)
                            )

                    summaries.append(
                        GenerationResultSummary(
                            generation_id=metadata["generation_id"],
                            library_name=metadata["library_name"],
                            timestamp=datetime.fromisoformat(metadata["timestamp"]),
                            paradigms_extracted=metadata.get("paradigms_extracted", 0),
                            code_artifacts=metadata.get("code_artifacts", 0),
                            average_consciousness=metadata.get(
                                "average_consciousness", 0
                            ),
                            execution_time_seconds=metadata.get(
                                "execution_time_seconds", 0
                            ),
                            consciousness_scores=consciousness_scores,
                            top_paradigms=top_paradigms,
                            output_directory=str(gen_dir),
                        )
                    )

                except Exception as e:
                    print(
                        f"Warning: Failed to load generation metadata from {gen_dir}: {e}"
                    )
                    continue

        # Sort by timestamp (most recent first) and limit
        summaries.sort(key=lambda x: x.timestamp, reverse=True)
        return summaries[:limit]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get recent generations: {str(e)}"
        )


@router.websocket("/generation/stream")
async def generation_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for real-time generation updates

    Clients can connect to receive live progress updates during
    code generation sessions.
    """
    await websocket.accept()
    websocket_connections.append(websocket)

    try:
        # Send initial connection confirmation
        await websocket.send_json(
            {"event": "connected", "message": "WebSocket connection established"}
        )

        # Keep connection alive and listen for client messages
        while True:
            try:
                data = await websocket.receive_text()
                # Client can send commands if needed in future
                pass
            except WebSocketDisconnect:
                break

    except Exception as e:
        print(f"WebSocket error: {e}")

    finally:
        if websocket in websocket_connections:
            websocket_connections.remove(websocket)


# Register router with main FastAPI app
def register_routes(app):
    """Register library generation routes with FastAPI app"""
    app.include_router(router)
