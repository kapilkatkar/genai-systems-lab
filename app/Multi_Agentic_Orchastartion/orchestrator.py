from app.Multi_Agentic_Orchastartion.agent_classifier import AgentClassifier
from app.Multi_Agentic_Orchastartion.intent_classifier import IntentClassifier
from app.Multi_Agentic_Orchastartion.tool_selector import ToolSelector
from app.Multi_Agentic_Orchastartion.memory import AgentMemory
from app.Multi_Agentic_Orchastartion.tools import get_tool_meta

class Orchestrator:
    def __init__(self, agents):
        self.agents = agents
        self.agent_classifier = AgentClassifier()
        self.intent_classifier = IntentClassifier()
        self.tool_selector = ToolSelector()
        self.memory = AgentMemory()
        self.tool_meta = get_tool_meta()

    def run(self, task: str):
        # Default structured output
        output_struct = {
            "agent": None,
            "intent": None,
            "tool": None,
            "policy_result": {},
            "data_result": {},
            "action_result": {}
        }

        # Agent Selection
        agent_name = self.agent_classifier.classify(task, self.agents)
        agent = next((a for a in self.agents if a.name == agent_name), None)
        output_struct["agent"] = agent_name

        if not agent:
            output_struct["action_result"] = {"error": f"Agent '{agent_name}' not found."}
            return output_struct

        # Intent Classification
        intent = self.intent_classifier.classify(task)
        output_struct["intent"] = intent

        # Filter tools by intent category
        candidate_tools = [
            t for t in agent.tools if self.tool_meta[t.name]["category"] == intent
        ]

        if not candidate_tools:
            output_struct["tool"] = "none"
            output_struct["action_result"] = {"error": f"No tool available for intent '{intent}'."}
            return output_struct

        # Tool Selection
        selected_tool_name = self.tool_selector.select(task, candidate_tools)
        selected_tool_name = selected_tool_name.strip().lower().replace(".", "").split()[-1]

        # Find tool safely
        selected_tool = next((t for t in candidate_tools if t.name.lower() == selected_tool_name), candidate_tools[0])
        selected_tool_name = selected_tool.name
        output_struct["tool"] = selected_tool_name

        # Execute the tool
        tool_output = selected_tool.func(task, agent_name)

        # Assign output to the correct field based on intent
        if intent.lower() == "policy":
            output_struct["policy_result"] = tool_output if isinstance(tool_output, dict) else {"result": tool_output}
        elif intent.lower() == "data_assist":
            output_struct["data_result"] = tool_output if isinstance(tool_output, dict) else {"result": tool_output}
        else:  # default: action
            output_struct["action_result"] = tool_output if isinstance(tool_output, dict) else {"result": tool_output}

        # Save structured output to memory
        self.memory.add(agent_name, output_struct)

        return output_struct
