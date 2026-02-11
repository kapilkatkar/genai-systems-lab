import os
from langchain_chroma import Chroma
from app.core.embeddings import get_embedding_model
from app.config import CHROMA_BASE_DIR, GLOBAL_VECTOR_DIR


def get_vectorstore():
    """
    Load persisted Chroma vectorstore (global).
    """
    if not os.path.exists(GLOBAL_VECTOR_DIR):
        raise ValueError(f"Vectorstore not found at: {GLOBAL_VECTOR_DIR}")

    print("Loading vectorstore from:", GLOBAL_VECTOR_DIR)

    return Chroma(
        persist_directory=GLOBAL_VECTOR_DIR,
        embedding_function=get_embedding_model()
    )
