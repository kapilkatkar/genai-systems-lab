from pydantic import BaseModel
from typing import Optional
from typing import Any, Dict

class RAGResponse(BaseModel):
    answer: str
    domain: Optional[str]
    source: Optional[str]

class RAGRequest(BaseModel):
    query: str
    domain: str

class MultiAgentRequest(BaseModel):
    query: str


class MultiAgentResponse(BaseModel):
    agent: str
    intent: str
    tool: str
    policy_result: Dict[str, Any] = {}
    data_result: Dict[str, Any] = {}
    action_result: Dict[str, Any] = {}