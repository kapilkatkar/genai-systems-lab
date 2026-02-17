from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


class ToolSelector:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0)

    def select(self, task: str, tools: list) -> str:
        print("🔎 ToolSelector: started")

        prompt = "Choose the best tool for the task based on tool descriptions.\n\n"
        prompt += f"Task: {task}\n\nTools:\n"
        for t in tools:
            prompt += f"- {t.name}: {t.description}\n"
        prompt += "\nReturn ONLY the tool name."

        response = self.llm.generate([[HumanMessage(content=prompt)]])
        tool_name = response.generations[0][0].message.content.strip()

        print(f"✅ ToolSelector: selected -> {tool_name}")
        return tool_name
