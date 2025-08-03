"""
Pydantic models for AIOS VSCode Integration Server
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel


class AIOSRequest(BaseModel):
    """
    Request model for general AIOS operations.
    Contains message, context, processing flags, and response format options.
    """
    message: str
    context: Optional[Dict[str, Any]] = None
    processing: Optional[Dict[str, bool]] = None
    response_format: Optional[Dict[str, bool]] = None


class AIOSResponse(BaseModel):
    """
    Response model for AIOS operations.
    Includes response text, confidence, suggested actions, processing time,
    metrics, and metadata.
    """
    response_text: str
    confidence: float
    suggested_actions: list = []
    processing_time: float
    cellular_metrics: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class BridgeTestRequest(BaseModel):
    """
    Request model for bridge testing between modules.
    Specifies type, source, target, and data payload.
    """
    type: str
    source: str
    target: str
    data: Dict[str, Any]


class PerformanceTestRequest(BaseModel):
    """
    Request model for performance testing.
    Includes test type, requested metrics, and sample data.
    """
    test_type: str
    metrics_requested: list
    sample_data: str


class CodeReviewRequest(BaseModel):
    """
    Request model for code review operations.
    Contains code, language, and optional context.
    """
    code: str
    language: str
    context: Optional[Dict[str, Any]] = None


class CodeRefactorRequest(BaseModel):
    """
    Request model for code refactoring operations.
    Contains code, language, and optional context.
    """
    code: str
    language: str
    context: Optional[Dict[str, Any]] = None


class ArchitectureAnalyzeRequest(BaseModel):
    """
    Request model for architecture analysis.
    Includes list of files and optional context.
    """
    files: list
    context: Optional[Dict[str, Any]] = None


class NLUIntentRequest(BaseModel):
    """
    Request model for natural language understanding (NLU) intent recognition.
    Contains message and optional context.
    """
    message: str
    context: Optional[Dict[str, Any]] = None


class BridgeStatusRequest(BaseModel):
    """
    Request model for querying bridge status.
    Includes modules and optional context.
    """
    modules: list
    context: Optional[Dict[str, Any]] = None


class VisualizeRequest(BaseModel):
    """
    Request model for visualization operations.
    Includes files and optional context.
    """
    files: list
    context: Optional[Dict[str, Any]] = None


class AutomationRequest(BaseModel):
    """
    Request model for intelligent automation tasks.
    Specifies task, optional code, and context.
    """
    task: str
    code: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
