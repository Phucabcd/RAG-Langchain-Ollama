from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag_app.core.config import get_settings


def ingest_documents() -> int:
    settings = get_settings()
    settings.documents_dir.mkdir(parents=True, exist_ok=True)

    documents = []
    for pattern, loader_cls, kwargs in (
        ("**/*.pdf", PyPDFLoader, {}),
        ("**/*.txt", TextLoader, {"encoding": "utf-8"}),
        ("**/*.md", TextLoader, {"encoding": "utf-8"}),
    ):
        documents.extend(
            DirectoryLoader(
                str(settings.documents_dir),
                glob=pattern,
                loader_cls=loader_cls,
                loader_kwargs=kwargs,
                silent_errors=False,
            ).load()
        )

    if not documents:
        raise FileNotFoundError(
            f"No .pdf, .txt, or .md files found in {settings.documents_dir}"
        )

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    ).split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=settings.chroma_collection,
        persist_directory=str(settings.chroma_dir),
    )
    return len(chunks)


if __name__ == "__main__":
    print(f"Ingested {ingest_documents()} document chunks.")
