import os

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(page_title="RAG Chat", page_icon="💬")
st.title("LangChain + Ollama RAG")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Nhập câu hỏi về tài liệu của bạn")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Đang tìm câu trả lời..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/api/chat",
                    json={"question": question},
                    timeout=120,
                )
                response.raise_for_status()
                answer = response.json()["answer"]
            except requests.RequestException as exc:
                answer = f"Không thể kết nối tới API: {exc}"
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
