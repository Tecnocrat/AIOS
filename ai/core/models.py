"""
Basic models for AIOS bridge endpoints and AINLP scaffolding
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class BridgeTestRequest(BaseModel):
    source: str
    target: str
    data: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None


class BridgeStatusRequest(BaseModel):
    modules: List[str]
    context: Optional[Dict[str, Any]] = None


# Future AINLP scaffolding


class AINLPCell(BaseModel):
    cell_id: str
    cell_type: str
    state: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class AINLPContext(BaseModel):
    cells: List[AINLPCell]
    global_state: Optional[Dict[str, Any]] = None
