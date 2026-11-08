from fastapi import APIRouter

from rag_app.schemas.chat import ChatRequest, ChatResponse
from rag_app.services.rag import answer_question

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(answer=answer_question(request.question))
