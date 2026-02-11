"""
This file handles text splitting into chunks.
Chunking quality affects retrieval quality.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text: str):
    """
    Split large document text into smaller overlapping chunks.
    """
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,     # size of each chunk
        chunk_overlap=150   # overlap to maintain context continuity
    )
    return splitter.split_text(text)
