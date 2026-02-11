from fastapi import APIRouter
from app.models.schemas import RAGRequest, RAGResponse
from app.services.rag_service import rag_pipeline

router = APIRouter()


@router.post("/rag", response_model=RAGResponse)
def query_rag(request: RAGRequest):

    result = rag_pipeline(request.query, request.domain)

    return RAGResponse(**result)
