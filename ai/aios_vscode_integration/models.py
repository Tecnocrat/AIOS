"""
Pydantic models for AIOS VSCode Integration Server
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel


class AIOSRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    processing: Optional[Dict[str, bool]] = None
    response_format: Optional[Dict[str, bool]] = None


class AIOSResponse(BaseModel):
    response_text: str
    confidence: float
    suggested_actions: list = []
    processing_time: float
    cellular_metrics: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class BridgeTestRequest(BaseModel):
    type: str
    source: str
    target: str
    data: Dict[str, Any]


class PerformanceTestRequest(BaseModel):
    test_type: str
    metrics_requested: list
    sample_data: str


class CodeReviewRequest(BaseModel):
    code: str
    language: str
    context: Optional[Dict[str, Any]] = None


class CodeRefactorRequest(BaseModel):
    code: str
    language: str
    context: Optional[Dict[str, Any]] = None


class ArchitectureAnalyzeRequest(BaseModel):
    files: list
    context: Optional[Dict[str, Any]] = None


class NLUIntentRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None


class BridgeStatusRequest(BaseModel):
    modules: list
    context: Optional[Dict[str, Any]] = None


class VisualizeRequest(BaseModel):
    files: list
    context: Optional[Dict[str, Any]] = None


class AutomationRequest(BaseModel):
    task: str
    code: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
