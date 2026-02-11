"""
Main RAG pipeline orchestration.
"""

from app.core.vectorstore import get_vectorstore
from app.services.retrieval import retrieve_chunks
from app.services.generator import generate_answer


def rag_pipeline(query: str, domain: str):

    vectorstore = get_vectorstore()

    retrieved = retrieve_chunks(vectorstore, query, domain)

    print("Retrieved chunks count:", len(retrieved))
    print("First chunk preview:", retrieved[0]["text"][:200] if retrieved else "None")

    if not retrieved:
        return {
            "answer": "Sorry, I don’t have this information.",
            "domain": None,
            "source": None
        }

    chunks = [item["text"] for item in retrieved]
    answer = generate_answer(query, chunks)

    # Return metadata of the top chunk
    top_meta = retrieved[0]

    print("Model Answer:", answer)

    return {
        "answer": answer,
        "domain": top_meta["domain"],
        "source": top_meta["source"]
    }
