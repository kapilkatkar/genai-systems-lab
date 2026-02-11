"""
This script builds a single global vector DB for ALL domains.
Run manually before starting API.
"""

import sys
import os

# Allow importing app package when running script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pypdf import PdfReader
from langchain_community.vectorstores import Chroma
from app.core.chunking import chunk_text
from app.core.embeddings import get_embedding_model
from app.config import DOCS_BASE_DIR, GLOBAL_VECTOR_DIR


def ingest_all_docs(force: bool = False):
    """
    Ingest all PDFs inside docs/* into one global vector DB.
    """
    if force and os.path.exists(GLOBAL_VECTOR_DIR):
        import shutil
        shutil.rmtree(GLOBAL_VECTOR_DIR)

    texts = []
    metadatas = []

    for domain in os.listdir(DOCS_BASE_DIR):
        domain_path = os.path.join(DOCS_BASE_DIR, domain)

        if not os.path.isdir(domain_path):
            continue

        for file in os.listdir(domain_path):
            if file.endswith(".pdf"):
                pdf_path = os.path.join(domain_path, file)

                reader = PdfReader(pdf_path)
                full_text = ""

                for page in reader.pages:
                    full_text += page.extract_text() or ""

                if not full_text.strip():
                    print(f"Skipping scanned PDF (no text): {file}")
                    continue

                chunks = chunk_text(full_text)

                texts.extend(chunks)
                metadatas.extend([{"source": file, "domain": domain}] * len(chunks))

    # Create vector DB (global)
    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=get_embedding_model(),
        metadatas=metadatas,
        persist_directory=GLOBAL_VECTOR_DIR
    )

    # 🔥 IMPORTANT: save to disk
    vectorstore.persist()

    print("Ingested all documents into global vector DB")


if __name__ == "__main__":
    ingest_all_docs(force=True)
