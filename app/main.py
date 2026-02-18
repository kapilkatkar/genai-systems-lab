from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.rag import router as rag_router
from app.routes.multi_agent import router as multi_agent_router

app = FastAPI(title="Multi-Domain RAG Service")

# ✅ CORS MUST come immediately after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ THEN include routers
app.include_router(rag_router)
app.include_router(multi_agent_router)


@app.get("/")
def health():
    return {"status": "RAG service running"}
