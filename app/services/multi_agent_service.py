import asyncio
from app.Multi_Agentic_Orchastartion.tools import get_tool_registry
from app.Multi_Agentic_Orchastartion.agent_classifier import get_agent_registry
from app.Multi_Agentic_Orchastartion.orchestrator import Orchestrator

# Initialize tools and agents once
tools = get_tool_registry()
agents = get_agent_registry(tools)
orchestrator = Orchestrator(agents)


async def run_multi_agent(query: str) -> dict:
    """
    Main entry for multi-agent orchestration.
    Runs sync orchestrator safely inside async context.
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, orchestrator.run, query)
    return result
