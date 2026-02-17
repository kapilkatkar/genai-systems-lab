from fastapi import FastAPI
from app.routes.rag import router as rag_router
from app.routes.multi_agent import router as multi_agent_router

app = FastAPI(title="Multi-Domain RAG Service")

app.include_router(rag_router)
app.include_router(multi_agent_router)


@app.get("/")
def health():
    return {"status": "RAG service running"}
