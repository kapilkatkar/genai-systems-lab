"""
This script builds a single global vector DB for ALL domains.
Run manually before starting API.
"""

import sys
import os
import shutil
import logging

# Allow importing app package when running script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pypdf import PdfReader
from langchain_community.vectorstores import Chroma
from app.core.chunking import chunk_text
from app.core.embeddings import get_embedding_model
from app.config import DOCS_BASE_DIR, GLOBAL_VECTOR_DIR


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ingest_all_docs(force: bool = False):
    """
    Ingest all PDFs inside docs/* into one global vector DB.
    """

    # 🔥 Force rebuild option
    if force and os.path.exists(GLOBAL_VECTOR_DIR):
        logger.info("Removing existing global vector DB...")
        shutil.rmtree(GLOBAL_VECTOR_DIR)

    texts = []
    metadatas = []

    total_files = 0
    total_chunks = 0

    if not os.path.exists(DOCS_BASE_DIR):
        logger.warning("Docs base directory does not exist.")
        return

    for domain in os.listdir(DOCS_BASE_DIR):
        domain_path = os.path.join(DOCS_BASE_DIR, domain)

        if not os.path.isdir(domain_path):
            continue

        for file in os.listdir(domain_path):
            if not file.lower().endswith(".pdf"):
                continue

            pdf_path = os.path.join(domain_path, file)

            logger.info(f"Processing: {pdf_path}")

            try:
                reader = PdfReader(pdf_path)
            except Exception as e:
                logger.error(f"Failed to read {file}: {e}")
                continue

            file_chunk_count = 0

            # 🔥 Page-level chunking (memory efficient)
            for page in reader.pages:
                page_text = page.extract_text() or ""

                if not page_text.strip():
                    continue

                chunks = chunk_text(page_text)

                texts.extend(chunks)
                metadatas.extend([
                    {
                        "source": file,
                        "domain": domain,
                        "path": pdf_path
                    }
                ] * len(chunks))

                file_chunk_count += len(chunks)

            if file_chunk_count == 0:
                logger.warning(f"Skipping scanned or empty PDF: {file}")
                continue

            total_files += 1
            total_chunks += file_chunk_count

            logger.info(f"Added {file_chunk_count} chunks from {file}")

    if not texts:
        logger.warning("No documents found to ingest.")
        return

    logger.info("Creating global vector store...")

    # 🔥 Chroma auto-persists (no .persist() needed)
    Chroma.from_texts(
        texts=texts,
        embedding=get_embedding_model(),
        metadatas=metadatas,
        persist_directory=GLOBAL_VECTOR_DIR
    )

    logger.info("====================================")
    logger.info(f"Ingested {total_files} files")
    logger.info(f"Created {total_chunks} total chunks")
    logger.info("Global vector DB successfully built!")
    logger.info("====================================")


if __name__ == "__main__":
    ingest_all_docs(force=True)
