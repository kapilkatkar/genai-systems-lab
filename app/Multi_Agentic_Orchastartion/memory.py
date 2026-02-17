from collections import defaultdict


class AgentMemory:
    def __init__(self):
        # memory structure: {agent_name: [messages]}
        self.memory = defaultdict(list)

    def add(self, agent_name: str, message: str):
        self.memory[agent_name].append(message)

    def get(self, agent_name: str):
        return self.memory.get(agent_name, [])

    def clear(self, agent_name: str):
        self.memory[agent_name] = []

    def clear_all(self):
        self.memory = defaultdict(list)
