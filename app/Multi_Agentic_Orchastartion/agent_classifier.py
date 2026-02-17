from dataclasses import dataclass
from typing import List
from openai import OpenAI
from app.config import OPENAI_API_KEY, LLM_MODEL

from app.Multi_Agentic_Orchastartion.tools import Tool

client = OpenAI(api_key=OPENAI_API_KEY)


@dataclass
class Agent:
    name: str
    description: str
    tools: List[Tool]


class AgentClassifier:
    def __init__(self):
        self.llm = client

    def classify(self, task: str, agents: List[Agent]) -> str:
        print("🔎 AgentClassifier: started")  

        prompt = f"""
        You are an assistant that routes user queries to the correct agent.
        Choose the best agent from the list below based on the task.

        Agents:
        {', '.join([f"{a.name}: {a.description}" for a in agents])}

        Task: {task}

        Return ONLY the agent name.
        """

        response = self.llm.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        agent_name = response.choices[0].message.content.strip()
        print(f"✅ AgentClassifier: selected -> {agent_name}") 

        return agent_name


def get_agent_registry(tools: List[Tool]) -> List[Agent]:
    tool_dict = {t.name: t for t in tools}

    return [
        Agent(
            name="billing",
            description="You are responsible for handling queries related to billing and retry configurations. This includes GST matters such as invoice, credit note, debit note, voucher, Section 31, Section 34, reverse charge, and compliance-related questions. It also covers retry mechanisms including retry logic, backoff strategies, hybrid models, webhook failures, timeout issues, HTTP errors, retry window settings, and max retry configurations.",
            tools=[
                tool_dict["rag1"],
                tool_dict["data2"],
                tool_dict["action1"],
            ]
        ),
        Agent(
            name="compliance",
            description="You are responsible for handling queries related to data protection and compliance, which include data protection, personal data, policy objective, applicability, staff data, beneficiary data, donor data, processing principles, legal basis, purpose limitation, data subject rights, access requests, modification requests, security measures, third-party transfer, law enforcement disclosure, data retention, violations, compliance responsibility.",
            tools=[
                tool_dict["rag1"],
                tool_dict["data2"],
            ]
        ),
        Agent(
            name="marketing",
            description="You are responsible for handling queries related to marketing, which include marketing policy, marketing plan, internal environment, external environment, consumer behavior, consumer needs, marketing partnerships, value creation, policy components, policy tools, policy types, objectives, top-down approach, bottom-up approach, global integration, WTO adaptation, strategic marketing.",
            tools=[
                tool_dict["rag1"],
                tool_dict["data2"],
            ]
        ),
        Agent(
            name="sales",
            description="HYou are responsible for handling queries related to sales and payments, which include topics such as commission, contractual terms, withholding, eligibility, pro-rata payments, cut-off periods, invoiced fees, payment conditions, notice period, and employment status.",
            tools=[
                tool_dict["rag1"],
                tool_dict["data2"],
                tool_dict["action2"],
            ]
        ),
        Agent(
            name="support",
            description="You are responsible for handling queries related to employee leave and holiday policies, which include leave policy, eligibility, exclusions, privilege leave, accrual, carry-forward, public holidays, casual leave, optional holidays, special casual leave, compensatory leave, blood donation, earned leave, vacation, combination, maximum limits, annual credit, entitlements.",
            tools=[
                tool_dict["rag1"],
                tool_dict["data2"],
                tool_dict["action1"],
            ]
        ),
        Agent(
            name="tickets",
            description="You are responsible for handling queries related to tickets and requests in JIRA Service Desk, which includes ticket, request, issue, customer portal, email channel, request form, request type, issue type, queue, agent assignment, public comment, internal comment, workflow, attachments, resolved status, SLA, knowledge base, collaborator, status updates, tracking.",
            tools=[
                tool_dict["rag1"],
                tool_dict["get_jira_ticket"],
                tool_dict["action1"],
            ]
        ),
    ]
