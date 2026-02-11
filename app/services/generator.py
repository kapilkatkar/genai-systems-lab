"""
Handles answer generation using OpenAI.
"""

from openai import OpenAI
from app.config import OPENAI_API_KEY, LLM_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(query: str, context_chunks: list[str]):

    context = "\n\n".join(context_chunks)

    system_prompt = (
        "You are a retrieval-based assistant. "
        "Answer ONLY using the provided context. "
        "If the answer is not found, say you don't know."
    )

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}"
            }
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
