# rag/rag_chain.py

from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

def get_rag_context(query, index_path="rag/faiss_index"):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vector_db.as_retriever()

    docs = retriever.get_relevant_documents(query)
    if not docs:
        return "No relevant spiritual content found."

    context = "\n".join([doc.page_content.strip() for doc in docs[:3]])
    return context
