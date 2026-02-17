from fastapi import APIRouter
from app.models.schemas import MultiAgentRequest, MultiAgentResponse
from app.services.multi_agent_service import run_multi_agent

router = APIRouter()

@router.post("/multi_agent", response_model=MultiAgentResponse)
async def multi_agent(request: MultiAgentRequest):
    # Run multi-agent orchestration
    output = await run_multi_agent(request.query)

    return MultiAgentResponse(**output)
