# app/Multi_Agentic_Orchastartion/memory.py
from collections import defaultdict
from typing import Dict, Any, List, Optional

class AgentMemory:
    def __init__(self):
        # Normal message memory: {agent_name: [messages]}
        self.memory = defaultdict(list)
        # Pending transaction memory: {agent_name: txn_dict}
        self.pending_transactions: Dict[str, Dict[str, Any]] = {}

    # ---------------- Normal Memory ----------------
    def add(self, agent_name: str, message: Dict[str, Any]):
        self.memory[agent_name].append(message)

    def get(self, agent_name: str) -> List[Dict[str, Any]]:
        return self.memory.get(agent_name, [])

    def clear(self, agent_name: str):
        self.memory[agent_name] = []

    def clear_all(self):
        self.memory = defaultdict(list)

    # ---------------- Pending Transactions ----------------
    def set_pending_transaction(
        self, agent_name: str, tool_name: str, required_fields: List[str], collected_fields: Optional[Dict[str, Any]] = None
    ):
        self.pending_transactions[agent_name] = {
            "tool": tool_name,
            "required_fields": required_fields,
            "collected_fields": collected_fields or {}
        }

    def get_pending_transaction(self, agent_name: str) -> Optional[Dict[str, Any]]:
        return self.pending_transactions.get(agent_name)

    def clear_pending_transaction(self, agent_name: str):
        if agent_name in self.pending_transactions:
            del self.pending_transactions[agent_name]
