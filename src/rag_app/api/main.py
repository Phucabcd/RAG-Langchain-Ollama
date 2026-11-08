from fastapi import FastAPI

from rag_app.api.routes.chat import router as chat_router

app = FastAPI(title="LangChain Ollama RAG API")
app.include_router(chat_router, prefix="/api")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
