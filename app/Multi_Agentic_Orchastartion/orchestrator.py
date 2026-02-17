# orchestrator.py
from app.Multi_Agentic_Orchastartion.agent_classifier import AgentClassifier
from app.Multi_Agentic_Orchastartion.intent_classifier import IntentClassifier
from app.Multi_Agentic_Orchastartion.tool_selector import ToolSelector
from app.Multi_Agentic_Orchastartion.memory import AgentMemory
from app.Multi_Agentic_Orchastartion.actions.fileds_excractor import extract_fields_from_message


class Orchestrator:
    def __init__(self, agents):
        self.agents = agents
        self.agent_classifier = AgentClassifier()
        self.intent_classifier = IntentClassifier()
        self.tool_selector = ToolSelector()
        self.memory = AgentMemory()

    def run(self, task: str):
        print("\n--- Orchestrator: New task ---")
        print(f"User task: {task}")

        output_struct = {
            "agent": None,
            "intent": None,
            "tool": None,
            "policy_result": {},
            "data_result": {},
            "action_result": {}
        }

        # 1️⃣ Agent selection
        agent_name = self.agent_classifier.classify(task, self.agents)
        agent = next((a for a in self.agents if a.name == agent_name), None)
        output_struct["agent"] = agent_name
        if not agent:
            output_struct["action_result"] = {"error": f"Agent '{agent_name}' not found."}
            return output_struct

        # 2️⃣ Intent classification
        intent = self.intent_classifier.classify(task)
        output_struct["intent"] = intent

        # 3️⃣ Pending transaction (only for transactions)
        if intent.lower() == "transaction":
            pending_txn = self.memory.get_pending_transaction(agent_name)
            if pending_txn:
                print(f"Pending transaction found for agent '{agent_name}': {pending_txn}")
                collected_fields = extract_fields_from_message(task, pending_txn["required_fields"])
                pending_txn["collected_fields"].update({k: v for k, v in collected_fields.items() if v})

                missing = [f for f in pending_txn["required_fields"] if not pending_txn["collected_fields"].get(f)]
                if missing:
                    return {
                        "agent": agent_name,
                        "intent": "transaction",
                        "tool": pending_txn["tool"],
                        "action_result": {"message": f"Missing required fields: {', '.join(missing)}"}
                    }

                tool_obj = next((t for t in agent.tools if t.name == pending_txn["tool"]), None)
                if tool_obj:
                    exec_kwargs = pending_txn["collected_fields"].copy()
                    exec_kwargs["query"] = task
                    tool_output = tool_obj.func(**exec_kwargs)
                    self.memory.clear_pending_transaction(agent_name)
                    output_struct["tool"] = tool_obj.name
                    output_struct["action_result"] = {"message": tool_output}
                    return output_struct

        # 4️⃣ Tool selection
        candidate_tools = [
            t for t in agent.tools if getattr(t, "category", "").lower() == intent.lower()
        ]
        if not candidate_tools:
            output_struct["tool"] = "none"
            output_struct["action_result"] = {"error": f"No tool available for intent '{intent}'."}
            return output_struct

        selected_tool_name = self.tool_selector.select(task, candidate_tools)
        selected_tool = next(
            (t for t in candidate_tools if t.name.lower() == selected_tool_name.lower()),
            candidate_tools[0]
        )
        output_struct["tool"] = selected_tool.name

        # 5️⃣ Required fields ONLY for transactions
        required_fields = getattr(selected_tool, "required_fields", []) or []
        collected_fields = {}
        if intent.lower() == "transaction" and required_fields:
            collected_fields = extract_fields_from_message(task, required_fields)
            missing = [f for f in required_fields if not collected_fields.get(f)]
            if missing:
                self.memory.set_pending_transaction(agent_name, selected_tool.name, required_fields, collected_fields)
                return {
                    "agent": agent_name,
                    "intent": "transaction",
                    "tool": selected_tool.name,
                    "action_result": {"message": f"Missing required fields: {', '.join(missing)}"}
                }

        # 6️⃣ Execute tool
        exec_kwargs = collected_fields.copy() if collected_fields else {}

        # For policy/data_assist, pass query only, ignore missing args
        if intent.lower() in ["policy", "data_assist"]:
            exec_kwargs = {"query": task, "agent": agent_name, "intent": intent}

        try:
            tool_output = selected_tool.func(**exec_kwargs)
        except TypeError as e:
            tool_output = f"Error executing tool '{selected_tool.name}': {str(e)}"

        # 7️⃣ Build output
        if intent.lower() == "policy":
            output_struct["policy_result"] = tool_output if isinstance(tool_output, dict) else {"result": tool_output}
        elif intent.lower() == "data_assist":
            output_struct["data_result"] = tool_output if isinstance(tool_output, dict) else {"result": tool_output}
        else:
            output_struct["action_result"] = {"message": tool_output} if isinstance(tool_output, str) else tool_output

        # 8️⃣ Save to memory
        self.memory.add(agent_name, output_struct)
        return output_struct
