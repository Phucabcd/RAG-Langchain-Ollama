# LangChain + Ollama RAG

Khung project RAG dùng FastAPI, Streamlit, Ollama (Llama 3.1 8B), embedding
`all-MiniLM-L6-v2` và Chroma.

## Cấu trúc

```text
.
├── data/
│   ├── chroma/                 # Chroma persistence (được tạo khi ingest)
│   └── documents/              # Thả tài liệu .txt/.md/.pdf vào đây
├── src/rag_app/
│   ├── api/routes/             # API endpoints
│   ├── core/                   # Cấu hình
│   ├── ingestion/              # Đọc, chia nhỏ và lưu tài liệu
│   ├── schemas/                # Request/response models
│   └── services/               # RAG chain
├── streamlit_app.py            # Giao diện chat
└── requirements.txt
```

## Khởi chạy

Yêu cầu Python 3.10+ và [Ollama](https://ollama.com/) đã cài đặt.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
ollama pull llama3.1:8b
```

Embedding được tải từ Hugging Face khi chạy ingestion lần đầu. Nếu máy đã cài
Ollama, chạy API và giao diện ở hai terminal:

```bash
PYTHONPATH=src uvicorn rag_app.api.main:app --reload
```

```bash
streamlit run streamlit_app.py
```

## Nạp tài liệu

Đặt file `.txt`, `.md` hoặc `.pdf` trong `data/documents/`, sau đó chạy:

```bash
PYTHONPATH=src python -m rag_app.ingestion.loader
```

API chat: `POST /api/chat` với JSON `{"question": "..."}`. API docs có tại
`/docs`.
