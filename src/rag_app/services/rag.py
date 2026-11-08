from functools import lru_cache

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from rag_app.core.config import get_settings


@lru_cache
def get_vector_store() -> Chroma:
    settings = get_settings()
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    return Chroma(
        collection_name=settings.chroma_collection,
        persist_directory=str(settings.chroma_dir),
        embedding_function=embeddings,
    )


@lru_cache
def get_chat_model() -> ChatOllama:
    settings = get_settings()
    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )


def answer_question(question: str) -> str:
    documents = get_vector_store().similarity_search(question, k=4)
    context = "\n\n".join(document.page_content for document in documents)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the question using the context below. If the context "
                "does not contain the answer, say so. Do not invent facts.\n\n"
                "Context:\n{context}",
            ),
            ("human", "{question}"),
        ]
    )
    response = (prompt | get_chat_model()).invoke(
        {"context": context or "No relevant documents found.", "question": question}
    )
    return str(response.content)
