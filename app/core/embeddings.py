"""
This file returns embedding model instance.
Used during ingestion and retrieval.
"""

from langchain_openai import OpenAIEmbeddings
from app.config import OPENAI_API_KEY, EMBEDDING_MODEL

def get_embedding_model():
    """
    Create and return OpenAI embedding model.
    """
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        api_key=OPENAI_API_KEY
    )