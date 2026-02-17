from openai import OpenAI
from app.config import OPENAI_API_KEY, LLM_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


class IntentClassifier:
    def classify(self, task: str) -> str:
        print("🔎 IntentClassifier: started")  
        prompt = f"""
        Classify the user's intent into one of these categories:
        1) policy
        2) data_assist
        3) transaction

        Policy patterns:
        - What is + [something]
        - Explain + [something]
        - How + [something] works
        - What are the rules for + [something]
        - Is it allowed to + [something]
        - What is the policy for + [something]
        - How do we handle + [something]
        - What is the process for + [something]
        - What are the guidelines for + [something]
        - What is the requirement for + [something]

        Data Assist patterns:
        - Show me + [data]
        - List + [data]
        - Get me + [data]
        - Fetch + [data]
        - Give me + [data]
        - Retrieve + [data]
        - Find + [data]
        - What is the status of + [data]
        - How many + [data]
        - Show all + [data]

        Transaction patterns:
        - Create + [something]
        - Open + [something]
        - Update + [something]
        - Modify + [something]
        - Delete + [something]
        - Close + [something]
        - Assign + [something]
        - Escalate + [something]
        - Cancel + [something]
        - Add + [something]
        - Remove + [something]
        - Apply + [something]

        Task: {task}

        IMPORTANT:
        Return ONLY ONE of these EXACT WORDS:
        policy OR data_assist OR transaction
        """

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        output = response.choices[0].message.content.strip().lower()
        print(f"✅ IntentClassifier: selected -> {output}") 

        if "policy" in output:
            return "policy"
        if "data" in output:
            return "data_assist"
        if "transaction" in output or "action" in output:
            return "transaction"

        return "policy"
