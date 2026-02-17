from dataclasses import dataclass
from typing import Callable, List, Dict, Any
from app.services.rag_service import rag_pipeline
from app.Multi_Agentic_Orchastartion.actions.jira_utils import get_jira_tickets, create_jira_ticket
from app.config import JIRA_API_TOKEN, JIRA_PROJECT_KEY, JIRA_EMAIL, JIRA_BASE_URL, JIRA_DOMAIN


@dataclass
class Tool:
    name: str
    description: str
    category: str
    func: Callable[[str], str]
    required_fields: List[str] = None


# ----------------- POLICY TOOLS -----------------
class RagTool1:
    name = "rag1"
    category = "policy"
    description = "RAG tool 1 for policy documents."

    def run(self, query: str, **kwargs) -> dict:
        return rag_pipeline(query=query, domain=kwargs.get("agent", "default"))



class RagTool2:
    name = "rag2"
    category = "policy"
    description = "RAG tool 2 for compliance policies."
    def run(self, query: str) -> str:
        # Call your real RAG pipeline
        result = rag_pipeline(query, domain="policy")

        # Return only the answer string
        return result["answer"]


# ----------------- DATA ASSIST TOOLS -----------------
class DataTool1:
    name = "data2"
    category = "data_assist"
    description = "Fetch billing history and invoices."

    def run(self, query: str) -> str:
        return "Data2 result for: " + query



class DataTool2:
    name = "data2"
    category = "data_assist"
    description = "Fetch billing history and invoices."

    def run(self, query: str) -> str:
        return "Data2 result for: " + query


class DataTool3:
    name = "get_jira_ticket"
    category = "data_assist"
    description = "Fetch ticket history for a customer."

    def run(self, query: str, **kwargs) -> dict:
        # ignore domain or other optional args
        jql = f'project = {JIRA_PROJECT_KEY} AND summary ~ "{query}"'
        tickets = get_jira_tickets(jql=jql)
        return {"tickets": tickets}


# ----------------- TRANSACTION TOOLS -----------------
class ActionTool1:
    name = "CreateJiraTicket"
    category = "transaction"
    description = "Create a new ticket in ticketing system."
    required_fields = ["summary", "description"]

    def run(self, summary=None, description=None):
        if not summary or not description:
            return "Missing required fields: summary and description."
        return f"Ticket created successfully for: {summary}"




class ActionTool2:
    name = "action2"
    category = "transaction"
    description = "Create a new sales order."

    def run(self, query: str) -> str:
        return "Action2 executed: " + query


def get_tool_registry() -> List[Tool]:
    return [
        Tool(
            name=RagTool1.name,
            description=RagTool1.description,
            category=RagTool1.category,
            func=RagTool1().run
        ),
        Tool(
            name=RagTool2.name,
            description=RagTool2.description,
            category=RagTool2.category,
            func=RagTool2().run
        ),
        Tool(
            name=DataTool1.name,
            description=DataTool1.description,
            category=DataTool1.category,
            func=DataTool1().run
        ),
        Tool(
            name=DataTool2.name,
            description=DataTool2.description,
            category=DataTool2.category,
            func=DataTool2().run
        ),
        Tool(
            name=DataTool3.name,
            description=DataTool3.description,
            category=DataTool3.category,
            func=DataTool3().run
        ),
        Tool(
            name=ActionTool1.name,
            description=ActionTool1.description,
            category=ActionTool1.category,
            func=ActionTool1().run,
            required_fields=["summary", "description"] 
        ),
        Tool(
            name=ActionTool2.name,
            description=ActionTool2.description,
            category=ActionTool2.category,
            func=ActionTool2().run
        ),
    ]


def get_tool_meta() -> Dict[str, Dict[str, Any]]:
    """
    Returns a metadata dictionary for each tool:
    {
      "rag1": {"category": "policy", "description": "..."},
      ...
    }
    """
    tools = get_tool_registry()
    return {
        t.name: {"category": t.category, "description": t.description}
        for t in tools
    }
