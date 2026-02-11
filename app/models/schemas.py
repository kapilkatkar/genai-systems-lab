from pydantic import BaseModel
from typing import Optional

class RAGResponse(BaseModel):
    answer: str
    domain: Optional[str]
    source: Optional[str]


class RAGRequest(BaseModel):
    query: str
    domain: str

class RAGResponse(BaseModel):
    answer: str
    domain: Optional[str]
    source: Optional[str]
