import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing")

# Set it globally so LangChain/OpenAI can access it
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

LLM_MODEL = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-3-small"

# Base directories
DOCS_BASE_DIR = "docs"
CHROMA_BASE_DIR = "chroma_db"
GLOBAL_VECTOR_DIR = os.path.join(CHROMA_BASE_DIR, "global")

# --- Jira ---
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "SCRUM")
JIRA_MAX_RESULTS = int(os.getenv("JIRA_MAX_RESULTS", 100))

if not all([JIRA_DOMAIN, JIRA_EMAIL, JIRA_API_TOKEN]):
    raise ValueError("Jira credentials are missing in .env file!")

# Base URL for Jira API
JIRA_BASE_URL = f"https://{JIRA_DOMAIN}/rest/api/3/issue"