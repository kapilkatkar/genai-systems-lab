"""
This file returns embedding model instance.
Used during ingestion and retrieval.
"""

"""
This file returns embedding model instance.
Used during ingestion and retrieval.
"""

from app.config import OPENAI_API_KEY, EMBEDDING_MODEL

# Flexible import for embeddings across langchain versions
OpenAIEmbeddings = None
try:
    from langchain.embeddings import OpenAIEmbeddings  # type: ignore
except Exception:
    try:
        from langchain_openai import OpenAIEmbeddings  # type: ignore
    except Exception:
        OpenAIEmbeddings = None

def get_embedding_model():
    """
    Create and return OpenAI embedding model.
    """
    if OpenAIEmbeddings is None:
        raise ImportError("No OpenAIEmbeddings available; install/upgrade langchain or langchain-openai")

    try:
        return OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            api_key=OPENAI_API_KEY
        )
    except TypeError:
        # fallback for different constructor signatures
        return OpenAIEmbeddings()