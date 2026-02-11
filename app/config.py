import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing")

LLM_MODEL = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-3-small"

# Base directories
DOCS_BASE_DIR = "docs"
CHROMA_BASE_DIR = "chroma_db"
GLOBAL_VECTOR_DIR = os.path.join(CHROMA_BASE_DIR, "global")

