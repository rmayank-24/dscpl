# ✝️ DSCPL – Your Spiritual Companion

🕊️ Rooted in scripture. Empowered by AI. Guided by grace.

[![Streamlit App](https://img.shields.io/badge/🧠%20Try%20the%20App-Click%20Here-brightgreen)](https://gods-messanger.streamlit.app/)

---

## 🌟 Overview

**DSCPL** is an AI-powered spiritual mentor built using **Streamlit**, **LangChain**, and **Google Gemini**. It provides thoughtful, scripture-rooted responses to spiritual queries, guided reflections, and daily devotionals – all tailored through the lens of Christianity.

---

## 🧩 Features

- 🙏 **Daily Devotion** – Bible verse, reflective prayer & declaration.
- 🧘 **Meditation** – Guided breathing with scripture and reflection.
- 🛡️ **Accountability** – Strength-based verses for personal struggles.
- 💬 **Chat Mode** – Ask spiritual questions or seek encouragement.
- 🆘 **SOS Help** – Instant spiritual comfort in tough times.
- 📖 **Dynamic RAG** – Fetches real-time Christian content from [Socialverse](https://socialverseapp.com).

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | Frontend UI |
| [LangChain](https://www.langchain.com/) | Agent + RAG |
| [FAISS](https://github.com/facebookresearch/faiss) | Vector Search |
| [Google Gemini API](https://ai.google.dev/) | LLM Backend |
| [HuggingFace Transformers](https://huggingface.co/) | Embeddings |
| [Socialverse API](https://api.socialverseapp.com) | Real-world Christian content |

---

## ⚙️ How It Works

1. `fetch_posts.py` pulls live data from **Socialverse** API.
2. `vector_store.py` creates a **FAISS index** of scripture-based content.
3. `rag_chain.py` retrieves the most relevant documents using LangChain's retriever.
4. `gemini_chain.py` generates graceful, scripture-based responses using **Gemini 1.5 Flash**.
5. `app.py` powers the Streamlit interface.

---

## 🚀 Live Demo

👉 [Click here to use the app](https://gods-messanger.streamlit.app)

---

## 📁 Project Structure

```
gods-grace/
│
├── app.py                    # Main Streamlit app
├── gemini_chain.py           # Google Gemini integration
├── utils.py                  # SOS / reflection prompt logic
│
└── rag/
    ├── fetch_posts.py        # Pull data from Socialverse API
    ├── vector_store.py       # Convert posts to FAISS vector store
    ├── rag_chain.py          # Query vector DB for context
    └── socialverse_data.json # Cached Socialverse data (optional)
```

---

## 👤 Author

**Mayank Rathi**  
B.Tech ECE | LNMIIT  
💼 SDE | Data Science | AI Engineer Aspirant  
🔗 [LinkedIn](https://linkedin.com/in/your-profile)  
📫 [GitHub](https://github.com/rmayank-24)

---

## 📜 License

This project is licensed under the MIT License.
